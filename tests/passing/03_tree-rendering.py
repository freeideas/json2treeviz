#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = ["playwright"]
# ///

import sys
import os

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import subprocess
import json
from pathlib import Path
import atexit
import time

# Import the web server helper
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'ai-coder' / 'scripts'))
from websrvr import start_server, get_server_url, stop_server

# Setup cleanup on exit
atexit.register(stop_server)

def main():
    # Start web server on the released directory
    released_dir = Path(__file__).resolve().parent.parent.parent / 'released'
    if not released_dir.exists():
        print("Error: released directory not found")
        sys.exit(97)

    port = start_server(str(released_dir))
    base_url = get_server_url(port)

    # Import playwright after ensuring it's installed
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Installing Playwright browsers...")
        subprocess.run([
            sys.executable, '-m', 'playwright', 'install', 'chromium'
        ], check=True, encoding='utf-8')
        from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # Navigate to the app
            page.goto(base_url)
            page.wait_for_load_state('networkidle')

            # Test data with various types
            test_json = {
                "name": "Root Object",
                "count": 42,
                "active": True,
                "nullField": None,
                "nested": {
                    "child": "value"
                },
                "items": [
                    {"id": 1, "label": "First"},
                    {"id": 2, "label": "Second"}
                ]
            }

            # Input the JSON
            json_textarea = page.locator('#json-input')
            json_textarea.fill(json.dumps(test_json))

            # Click visualize button
            page.locator('#visualize-button').click()

            # Wait for tree to render
            page.wait_for_selector('#tree-container', state='visible')
            time.sleep(1)  # Give Cytoscape time to render

            # $REQ_TREE_RENDERING_001: Render JSON as Tree
            # Check that Cytoscape is initialized and has elements
            cy_exists = page.evaluate('''() => {
                return typeof cy !== 'undefined' && cy !== null;
            }''')
            assert cy_exists, "Cytoscape instance should exist"  # $REQ_TREE_RENDERING_001

            # $REQ_TREE_RENDERING_002: Objects Become Nodes
            # Check that we have nodes in the graph
            node_count = page.evaluate('() => cy.nodes().length')
            assert node_count > 0, "Tree should have nodes"  # $REQ_TREE_RENDERING_002

            # $REQ_TREE_RENDERING_003: Primitive Fields Displayed as Node Labels
            # Check that primitive fields appear in labels
            labels = page.evaluate('() => cy.nodes().map(n => n.data("label"))')

            # Root node should show primitive fields but not null field
            root_labels = [l for l in labels if 'name:' in l.lower() or 'count:' in l.lower() or 'active:' in l.lower()]
            assert len(root_labels) > 0, "Should have node with primitive fields"  # $REQ_TREE_RENDERING_003

            # Find the root node label
            root_label = None
            for label in labels:
                if 'Root Object' in label:
                    root_label = label
                    break

            assert root_label is not None, "Should find root node with name field"  # $REQ_TREE_RENDERING_003
            assert 'count:' in root_label.lower() or '42' in root_label, "Should show count field"  # $REQ_TREE_RENDERING_003
            assert 'active:' in root_label.lower() or 'true' in root_label.lower(), "Should show boolean field"  # $REQ_TREE_RENDERING_003

            # $REQ_TREE_RENDERING_004: Null Fields Not Shown as Labels
            # Check that null field does NOT appear in any label
            has_null_field = any('nullField' in str(label) for label in labels)
            assert not has_null_field, "Null fields should not appear in labels"  # $REQ_TREE_RENDERING_004

            # $REQ_TREE_RENDERING_005: Nested Objects and Arrays Become Child Nodes
            # Check that nested object has a child relationship
            edges = page.evaluate('() => cy.edges().length')
            assert edges > 0, "Should have edges connecting parent and child nodes"  # $REQ_TREE_RENDERING_005

            # $REQ_TREE_RENDERING_006: Arrays Become Nodes with Children
            # Check that array node exists and has children
            array_labels = [l for l in labels if 'items' in l.lower() and '[' in l]
            assert len(array_labels) > 0, "Should have array node with element count"  # $REQ_TREE_RENDERING_006

            # Check that array has child nodes (the elements)
            array_has_children = page.evaluate('''() => {
                const arrayNode = cy.nodes().filter(n => {
                    const label = n.data('label');
                    return label && label.toLowerCase().includes('items') && label.includes('[');
                });
                if (arrayNode.length > 0) {
                    return arrayNode[0].outgoers('node').length > 0;
                }
                return false;
            }''')
            assert array_has_children, "Array node should have child nodes"  # $REQ_TREE_RENDERING_006

            # $REQ_TREE_RENDERING_007: Nodes Are Collapsible
            # Test collapsing functionality
            initial_visible_nodes = page.evaluate('() => cy.nodes().filter(n => n.style("display") !== "none").length')

            # Click on the root node to collapse it
            page.evaluate('''() => {
                const rootNode = cy.nodes()[0];
                rootNode.emit('tap');
            }''')

            time.sleep(0.5)  # Wait for collapse animation/layout

            # Check that some nodes are now hidden
            after_collapse_visible = page.evaluate('() => cy.nodes().filter(n => n.style("display") !== "none").length')
            assert after_collapse_visible < initial_visible_nodes, "Collapsing should hide descendant nodes"  # $REQ_TREE_RENDERING_007

            # Click again to expand
            page.evaluate('''() => {
                const rootNode = cy.nodes()[0];
                rootNode.emit('tap');
            }''')

            time.sleep(0.5)  # Wait for expand animation/layout

            # Check that nodes are visible again
            after_expand_visible = page.evaluate('() => cy.nodes().filter(n => n.style("display") !== "none").length')
            assert after_expand_visible > after_collapse_visible, "Expanding should show descendant nodes again"  # $REQ_TREE_RENDERING_007

            print("All tests passed!")

        finally:
            browser.close()

if __name__ == '__main__':
    main()
