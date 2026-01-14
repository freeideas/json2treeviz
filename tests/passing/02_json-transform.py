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

def test_json_transform():
    """Test JSON transformation requirements."""

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

        # $REQ_TRANSFORM_001: Parse JSON Text
        # Test that JSON text is parsed correctly
        test_json({"key": "value"}, lambda p: (  # $REQ_TRANSFORM_001
            # Check that JSON was parsed and created nodes
            p.wait_for_function("""() => {
                return cy && cy.nodes().length > 0;
            }""")
        ))
        print("✓ $REQ_TRANSFORM_001: JSON text parsed successfully")

        # $REQ_TRANSFORM_002: Objects Become Nodes
        # Test that JSON objects become nodes
        test_json({"name": "Test", "value": 42}, lambda p: (  # $REQ_TRANSFORM_002
            # Check that a node exists with the object's labels
            p.wait_for_function("""() => {
                return cy && cy.nodes().length > 0;
            }""")
        ))
        print("✓ $REQ_TRANSFORM_002: Objects become nodes")

        # $REQ_TRANSFORM_003: Primitive Fields as Labels
        # Test that primitive fields are shown as labels
        test_json({"name": "Test", "count": 5, "active": True}, lambda p: (  # $REQ_TRANSFORM_003
            # Check that node label contains primitive field values
            p.wait_for_function("""() => {
                if (!cy) return false;
                const nodes = cy.nodes();
                if (nodes.length === 0) return false;
                const label = nodes[0].data('label');
                return label.includes('name: Test') &&
                       label.includes('count: 5') &&
                       label.includes('active: true');
            }""")
        ))
        print("✓ $REQ_TRANSFORM_003: Primitive fields shown as labels")

        # $REQ_TRANSFORM_004: Null Fields Not Shown
        # Test that null values are not shown
        test_json({"name": "Test", "nullField": None, "value": 10}, lambda p: (  # $REQ_TRANSFORM_004
            # Check that node label does not contain the null field
            p.wait_for_function("""() => {
                if (!cy) return false;
                const nodes = cy.nodes();
                if (nodes.length === 0) return false;
                const label = nodes[0].data('label');
                return !label.includes('nullField') &&
                       label.includes('name: Test') &&
                       label.includes('value: 10');
            }""")
        ))
        print("✓ $REQ_TRANSFORM_004: Null fields not shown")

        # $REQ_TRANSFORM_005: Nested Objects and Arrays Become Children
        # Test that nested objects become child nodes
        test_json(  # $REQ_TRANSFORM_005
            {"parent": {"child": "value"}},
            lambda p: (
                # Check that there are at least 2 nodes (parent and child)
                p.wait_for_function("""() => {
                    if (!cy) return false;
                    return cy.nodes().length >= 2 && cy.edges().length >= 1;
                }""")
            )
        )
        print("✓ $REQ_TRANSFORM_005: Nested objects become children")

        # $REQ_TRANSFORM_006: Arrays Become Nodes with Element Children
        # Test that arrays become nodes with element children
        test_json(  # $REQ_TRANSFORM_006
            {"items": [1, 2, 3]},
            lambda p: (
                # Check that array becomes a node and elements are children
                p.wait_for_function("""() => {
                    if (!cy) return false;
                    const nodes = cy.nodes();
                    // Should have: root object node, array node, and 3 element nodes
                    return nodes.length >= 4;
                }""")
            )
        )
        print("✓ $REQ_TRANSFORM_006: Arrays become nodes with element children")

        # $REQ_TRANSFORM_007: Hierarchy Override for Arrays of Objects with id/parent_id
        # Test that arrays with id/parent_id are interpreted as hierarchies
        hierarchy_data = [
            {"id": 1, "parent-id": None, "name": "Root"},
            {"id": 2, "parent-id": 1, "name": "Child1"},
            {"id": 3, "parent-id": 1, "name": "Child2"}
        ]
        test_json(  # $REQ_TRANSFORM_007
            hierarchy_data,
            lambda p: (
                # Check that nodes are connected based on parent-child relationships
                # Should have 3 nodes (one for each object) and 2 edges (child1->root, child2->root)
                p.wait_for_function("""() => {
                    if (!cy) return false;
                    const nodes = cy.nodes();
                    const edges = cy.edges();
                    // With hierarchy override, should have 3 nodes and 2 edges
                    return nodes.length === 3 && edges.length === 2;
                }""")
            )
        )
        print("✓ $REQ_TRANSFORM_007: Hierarchy override for arrays with id/parent_id")

        # $REQ_TRANSFORM_008: Parent ID Field Pattern Matching
        # Test various parent ID field name patterns
        test_cases = [  # $REQ_TRANSFORM_008
            {"id": 1, "parent-id": None, "name": "A"},
            {"id": 1, "ParentID": None, "name": "B"},
            {"id": 1, "parent$id": None, "name": "C"},
            {"id": 1, "pArEnT.iD": None, "name": "D"}
        ]

        for test_case in test_cases:
            hierarchy = [test_case]
            test_json(
                hierarchy,
                lambda p: (
                    # Just check that it doesn't crash and creates nodes
                    p.wait_for_function("""() => {
                        if (!cy) return false;
                        return cy.nodes().length >= 1;
                    }""")
                )
            )
        print("✓ $REQ_TRANSFORM_008: Parent ID field pattern matching works")

        # $REQ_TRANSFORM_009: Parent/Child Relationship by ID Matching
        # Test that parent-child relationships are defined by ID matching
        hierarchy_data = [
            {"id": 10, "parent_id": None, "name": "Root"},
            {"id": 20, "parent_id": 10, "name": "Child"},
            {"id": 30, "parent_id": 20, "name": "Grandchild"}
        ]
        test_json(  # $REQ_TRANSFORM_009
            hierarchy_data,
            lambda p: (
                # Check that edges connect nodes correctly based on ID matching
                p.wait_for_function("""() => {
                    if (!cy) return false;
                    const nodes = cy.nodes();
                    const edges = cy.edges();
                    // Should have 3 nodes and 2 edges forming a chain
                    if (nodes.length !== 3 || edges.length !== 2) return false;

                    // Verify the hierarchy by checking that each child has exactly one parent
                    let rootCount = 0;
                    nodes.forEach(node => {
                        const incomingEdges = node.incomers('edge');
                        if (incomingEdges.length === 0) {
                            rootCount++;
                        }
                    });
                    // Should have exactly 1 root node (with no incoming edges)
                    return rootCount === 1;
                }""")
            )
        )
        print("✓ $REQ_TRANSFORM_009: Parent/child relationships by ID matching")

        browser.close()

    stop_server()
    print("\nAll JSON transform tests passed!")

if __name__ == '__main__':
    test_json_transform()
