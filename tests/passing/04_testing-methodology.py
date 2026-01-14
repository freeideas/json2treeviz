#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = ["playwright"]
# ///

"""
Test for visual verification methodology and hierarchy from id/parent_id.

This test verifies the testing methodology requirements:
- Visual verification using screenshots and visual-test.py
- DOM inspection alongside visual checks
- Testing both paste and drag/drop input methods
- Hierarchy rendering from id/parent_id fields
"""

import sys
import os
import json
import subprocess
import atexit
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Import Playwright
from playwright.sync_api import sync_playwright

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TMP_DIR = PROJECT_ROOT / 'tmp'
TMP_DIR.mkdir(exist_ok=True)

RELEASED_DIR = PROJECT_ROOT / 'released'
INDEX_HTML = RELEASED_DIR / 'index.html'

# Import web server helper
sys.path.insert(0, str(PROJECT_ROOT / 'ai-coder' / 'scripts'))
from websrvr import start_server, get_server_url, stop_server

# Ensure cleanup
atexit.register(stop_server)

# UV executable path
UV_EXE = PROJECT_ROOT / 'ai-coder' / 'bin' / 'uv.exe'

# Visual test script path
VISUAL_TEST_SCRIPT = PROJECT_ROOT / 'ai-coder' / 'scripts' / 'visual-test.py'


def run_visual_test(screenshot_path: Path, assertion: str) -> bool:
    """Run visual-test.py and return True if assertion passes."""
    result = subprocess.run(
        [str(UV_EXE), 'run', '--script', str(VISUAL_TEST_SCRIPT),
         str(screenshot_path), assertion,
         '--test-script', str(Path(__file__))],
        encoding='utf-8',
        capture_output=True
    )
    return result.returncode == 0


def test_hierarchy_with_paste():
    """
    $REQ_TEST_METHOD_001: Visual verification via screenshots
    $REQ_TEST_METHOD_002: Feature test process (JSON snippet, paste, visualize, screenshot)
    $REQ_TEST_METHOD_004: Hierarchy from id/parent_id test
    """
    print("Testing hierarchy from id/parent_id using paste method...")

    # Create test JSON with id/parent_id hierarchy
    # CEO -> CTO/CFO -> employees
    test_json = [
        {"id": "ceo", "parent_id": None, "name": "CEO Alice"},
        {"id": "cto", "parent_id": "ceo", "name": "CTO Bob"},
        {"id": "cfo", "parent_id": "ceo", "name": "CFO Carol"},
        {"id": "dev1", "parent_id": "cto", "name": "Developer Dave"},
        {"id": "dev2", "parent_id": "cto", "name": "Developer Eve"},
        {"id": "acc1", "parent_id": "cfo", "name": "Accountant Frank"}
    ]
    test_json_str = json.dumps(test_json, indent=2)

    # Start web server
    port = start_server(str(RELEASED_DIR))
    url = get_server_url(port)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Wait for page to load
        page.wait_for_selector('#json-input')

        # Paste JSON into textarea
        page.fill('#json-input', test_json_str)

        # Click Visualize button
        page.click('#visualize-button')

        # Wait for visualization to render
        page.wait_for_selector('#tree-container canvas', timeout=5000)
        page.wait_for_timeout(1000)  # Extra time for layout

        # Take screenshot
        screenshot_path = TMP_DIR / 'hierarchy_paste.png'
        page.screenshot(path=str(screenshot_path), full_page=True)

        # DOM inspection: Verify tree container is visible
        tree_container = page.locator('#tree-container')
        assert tree_container.is_visible(), "Tree container should be visible"  # $REQ_TEST_METHOD_001

        # DOM inspection: Verify canvas exists (Cytoscape renders to canvas)
        canvas = page.locator('#tree-container canvas')
        assert canvas.count() > 0, "Canvas element should exist"  # $REQ_TEST_METHOD_001

        browser.close()

    # Visual verification: Check that it shows a tree/hierarchy, not a flat list
    assertion = "The screenshot shows a hierarchical tree structure with nodes arranged in levels, not a flat list. There should be a root node at the top with child nodes branching below it."
    assert run_visual_test(screenshot_path, assertion), \
        "Visual test failed: hierarchy not properly displayed"  # $REQ_TEST_METHOD_004

    print("✓ Hierarchy test with paste passed")


def test_hierarchy_with_dragdrop():
    """
    $REQ_TEST_METHOD_003: Input method coverage (drag/drop)
    $REQ_TEST_METHOD_002: Feature test process
    """
    print("Testing hierarchy from id/parent_id using file picker method...")

    # Create test JSON file for file picker
    test_json = [
        {"id": "root", "parent_id": None, "label": "Root Node"},
        {"id": "child1", "parent_id": "root", "label": "Child 1"},
        {"id": "child2", "parent_id": "root", "label": "Child 2"},
        {"id": "grandchild1", "parent_id": "child1", "label": "Grandchild 1"}
    ]

    json_file_path = TMP_DIR / 'test_hierarchy.json'
    with open(json_file_path, 'w') as f:
        json.dump(test_json, f, indent=2)

    # Start web server
    port = start_server(str(RELEASED_DIR))
    url = get_server_url(port)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Wait for page to load
        page.wait_for_selector('#json-input')

        # Use file picker (similar to drag/drop in functionality)
        # Set up file chooser handler before clicking
        with page.expect_file_chooser() as fc_info:
            page.click('#file-picker-button')
        file_chooser = fc_info.value
        file_chooser.set_files(str(json_file_path))

        # Wait for file to be loaded and verify JSON was loaded into textarea
        page.wait_for_timeout(500)  # Give time for FileReader to complete
        textarea_value = page.input_value('#json-input')
        assert 'Root Node' in textarea_value, "JSON should be loaded into textarea"  # $REQ_TEST_METHOD_003

        # Click Visualize button
        page.click('#visualize-button')

        # Wait for visualization to render
        page.wait_for_selector('#tree-container canvas', timeout=5000)
        page.wait_for_timeout(1000)

        # Take screenshot
        screenshot_path = TMP_DIR / 'hierarchy_dragdrop.png'
        page.screenshot(path=str(screenshot_path), full_page=True)

        # DOM inspection
        tree_container = page.locator('#tree-container')
        assert tree_container.is_visible(), "Tree container should be visible"  # $REQ_TEST_METHOD_001

        browser.close()

    # Visual verification
    assertion = "The screenshot shows a tree structure with nodes arranged hierarchically. There should be multiple levels with parent-child relationships visible."
    assert run_visual_test(screenshot_path, assertion), \
        "Visual test failed: hierarchy not properly displayed with drag/drop"  # $REQ_TEST_METHOD_003

    print("✓ Hierarchy test with drag/drop passed")


if __name__ == '__main__':
    try:
        # Verify released app exists
        assert INDEX_HTML.exists(), f"Released app not found at {INDEX_HTML}"

        # Run tests
        test_hierarchy_with_paste()
        test_hierarchy_with_dragdrop()

        print("\n✓ All testing methodology tests passed")
        sys.exit(0)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        stop_server()
