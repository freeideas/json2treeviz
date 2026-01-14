#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = ["playwright"]
# ///

import sys
import os
import time
import atexit
import urllib.request
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add ai-coder/scripts to path for websrvr import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'ai-coder' / 'scripts'))

from playwright.sync_api import sync_playwright
from websrvr import start_server, get_server_url, stop_server

_playwright = None
_browser = None
_context = None

def cleanup():
    """Cleanup browser and server resources."""
    global _context, _browser, _playwright
    try:
        if _context:
            _context.close()
        if _browser:
            _browser.close()
        if _playwright:
            _playwright.stop()
        stop_server()
    except:
        pass

atexit.register(cleanup)

def main():
    global _playwright, _browser, _context

    # Start web server
    port = start_server('./released')
    url = get_server_url(port)

    print(f"Testing at {url}")

    # Initialize Playwright
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(headless=True)
    _context = _browser.new_context()
    page = _context.new_page()

    # Navigate to the page
    page.goto(url)
    page.wait_for_load_state('networkidle')

    # $REQ_INPUT_FORM_001: Input Form is Collapsible
    # Verify the input form exists and is visible initially
    input_form = page.locator('#input-form')
    assert input_form.is_visible(), "Input form should be visible initially"

    # Verify toggle button exists but is hidden initially
    toggle_button = page.locator('#toggle-form')
    assert not toggle_button.is_visible(), "Toggle button should be hidden initially"

    # $REQ_INPUT_FORM_002: No Immediate Action on Paste or Drop
    # Paste JSON into textarea
    textarea = page.locator('#json-input')
    test_json = '{"test": "data", "value": 123}'
    textarea.fill(test_json)

    # Wait a moment to ensure no automatic action occurs
    time.sleep(0.5)

    # Verify tree container is still hidden (no automatic visualization)
    tree_container = page.locator('#tree-container')
    assert not tree_container.is_visible(), "Tree should not render automatically on paste"

    # Verify input form is still visible
    assert input_form.is_visible(), "Input form should still be visible after paste"

    # $REQ_INPUT_FORM_003: Visualize Button Collapses Form and Renders Tree
    # Click the Visualize button
    visualize_button = page.locator('#visualize-button')
    visualize_button.click()

    # Wait for tree to render
    page.wait_for_timeout(500)

    # Verify input form is now collapsed (hidden)
    assert not input_form.is_visible(), "Input form should be collapsed after clicking Visualize"

    # Verify tree container is now visible
    assert tree_container.is_visible(), "Tree container should be visible after clicking Visualize"

    # Verify toggle button is now visible
    assert toggle_button.is_visible(), "Toggle button should be visible after form collapses"

    # Verify tree has been rendered (check for cytoscape canvas)
    canvas = page.locator('#tree-container canvas')
    assert canvas.count() > 0, "Tree should be rendered with canvas element"

    # $REQ_INPUT_FORM_004: Collapsed Form Can Be Expanded
    # Click the toggle button to expand the form
    toggle_button.click()
    page.wait_for_timeout(200)

    # Verify input form is visible again
    assert input_form.is_visible(), "Input form should be visible after clicking toggle button"

    # Verify the textarea still contains the original data
    current_value = textarea.input_value()
    assert current_value == test_json, "Textarea should retain the JSON data after expansion"

    # Verify we can collapse again by clicking toggle button
    toggle_button.click()
    page.wait_for_timeout(200)
    assert not input_form.is_visible(), "Input form should be collapsed again after clicking toggle"

    # Expand one more time to verify it's still functional
    toggle_button.click()
    page.wait_for_timeout(200)
    assert input_form.is_visible(), "Input form should be expandable multiple times"

    print("✓ All input form behavior tests passed")
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"✗ Test failed: {e}", file=sys.stderr)
        sys.exit(1)
