#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = ["playwright"]
# ///

import sys
import os
import json
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure we're running from project root
os.chdir(Path(__file__).resolve().parent.parent.parent)

# Import test web server
sys.path.insert(0, str(Path('./ai-coder/scripts').resolve()))
from websrvr import start_server, get_server_url, stop_server

def test_node_labels():
    """Test node label requirements."""

    # Start web server
    port = start_server('./released')
    url = get_server_url(port)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the app
        page.goto(url)
        page.wait_for_load_state('networkidle')

        # Helper function to test JSON transformation
        def test_json(json_data, check_fn):
            """Load JSON into the app and run a check function."""
            json_str = json.dumps(json_data)

            # Ensure form is visible (expand if collapsed)
            if not page.is_visible('#input-form'):
                page.click('#toggle-form')
                page.wait_for_timeout(100)

            # Clear the textarea and input the JSON
            page.fill('#json-input', json_str)

            # Click visualize button
            page.click('#visualize-button')
            page.wait_for_timeout(500)  # Wait for rendering

            # Run the check function
            check_fn(page)

        # $REQ_NODE_LABELS_001: Primitive Fields Displayed as Labels
        # Test that primitive fields (string, number, boolean) are shown as labels
        test_json(  # $REQ_NODE_LABELS_001
            {"name": "Alice", "age": 30, "active": True, "score": 95.5},
            lambda p: (
                # Check that node label contains all primitive field values
                p.wait_for_function("""() => {
                    if (!cy) return false;
                    const nodes = cy.nodes();
                    if (nodes.length === 0) return false;
                    const label = nodes[0].data('label');
                    return label.includes('name: Alice') &&
                           label.includes('age: 30') &&
                           label.includes('active: true') &&
                           label.includes('score: 95.5');
                }""")
            )
        )
        print("✓ $REQ_NODE_LABELS_001: Primitive fields displayed as labels")

        # $REQ_NODE_LABELS_002: Null Values Excluded from Labels
        # Test that null values are not shown in labels
        test_json(  # $REQ_NODE_LABELS_002
            {"firstName": "Bob", "middleName": None, "lastName": "Smith", "title": None, "age": 25},
            lambda p: (
                # Check that node label does not contain the null fields
                p.wait_for_function("""() => {
                    if (!cy) return false;
                    const nodes = cy.nodes();
                    if (nodes.length === 0) return false;
                    const label = nodes[0].data('label');
                    // Should include non-null fields
                    const hasValidFields = label.includes('firstName: Bob') &&
                                          label.includes('lastName: Smith') &&
                                          label.includes('age: 25');
                    // Should NOT include null fields
                    const lacksNullFields = !label.includes('middleName') &&
                                           !label.includes('title');
                    return hasValidFields && lacksNullFields;
                }""")
            )
        )
        print("✓ $REQ_NODE_LABELS_002: Null values excluded from labels")

        browser.close()

    stop_server()
    print("\nAll node label tests passed!")

if __name__ == '__main__':
    test_node_labels()
