#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = ["playwright"]
# ///

"""Test JSON input functionality."""

import atexit
import json
import subprocess
import sys
import time
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Import web server helper
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'ai-coder' / 'scripts'))
from websrvr import start_server, get_server_url, stop_server

# Ensure cleanup
atexit.register(stop_server)

# Start the web server
port = start_server('./released')
url = get_server_url(port)

print(f"Starting browser tests on {url}")

# Import Playwright
from playwright.sync_api import sync_playwright

def test_json_input():
    """Test all JSON input requirements."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # Navigate to the application
            page.goto(url)
            page.wait_for_load_state('networkidle')

            # $REQ_JSON_INPUT_001: Textarea for JSON Text
            textarea = page.locator('#json-input')
            assert textarea.count() == 1, "Textarea must exist"
            print("✓ $REQ_JSON_INPUT_001: Textarea exists")

            # $REQ_JSON_INPUT_007: Example Data Pre-loaded on Page Load
            # Read the expected example data
            example_data_path = Path('specs') / 'example-data.json'
            with open(example_data_path, 'r', encoding='utf-8') as f:
                expected_data = json.load(f)

            # Get the actual textarea content
            actual_text = textarea.input_value()
            actual_data = json.loads(actual_text)

            assert actual_data == expected_data, "Textarea must be pre-loaded with example-data.json contents"
            print("✓ $REQ_JSON_INPUT_007: Example data pre-loaded on page load")

            # $REQ_JSON_INPUT_005: Paste Populates Textarea
            # Clear and paste new content
            test_json = '{"test": "data"}'
            textarea.fill(test_json)
            new_value = textarea.input_value()
            assert new_value == test_json, "Pasting must populate textarea"
            print("✓ $REQ_JSON_INPUT_005: Paste populates textarea without triggering visualization")

            # Verify visualization hasn't triggered (tree container should still be hidden)
            tree_container = page.locator('#tree-container')
            assert tree_container.evaluate('el => el.style.display') == 'none', "Paste should not trigger visualization"

            # $REQ_JSON_INPUT_003: File Picker
            file_picker = page.locator('#file-picker')
            assert file_picker.count() == 1, "File picker input must exist"
            assert file_picker.get_attribute('accept') == '.json', "File picker must accept .json files"

            file_picker_button = page.locator('#file-picker-button')
            assert file_picker_button.count() == 1, "File picker button must exist"
            print("✓ $REQ_JSON_INPUT_003: File picker exists")

            # Test file picker functionality
            # Create a temporary JSON file
            tmp_dir = Path('./tmp')
            tmp_dir.mkdir(exist_ok=True)
            test_file = tmp_dir / 'test-input.json'
            test_data = {"file": "loaded", "value": 123}
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f)

            # Use file picker to load the file
            file_picker.set_input_files(str(test_file))

            # Wait a bit for the file to be read
            time.sleep(0.5)

            # Verify the textarea was populated with file contents
            loaded_text = textarea.input_value()
            loaded_data = json.loads(loaded_text)
            assert loaded_data == test_data, "File picker must populate textarea with file contents"

            # Verify visualization hasn't triggered
            assert tree_container.evaluate('el => el.style.display') == 'none', "File picker should not trigger visualization"
            print("✓ File picker populates textarea without triggering visualization")

            # $REQ_JSON_INPUT_002: Drag-and-Drop Zone
            # $REQ_JSON_INPUT_004: Drag-and-Drop Populates Textarea
            # Note: Playwright doesn't easily simulate drag-and-drop with files,
            # but we can verify the event handlers exist by checking the implementation

            # Create another test file for drag-and-drop
            drop_file = tmp_dir / 'drop-test.json'
            drop_data = {"dropped": True, "count": 42}
            with open(drop_file, 'w', encoding='utf-8') as f:
                json.dump(drop_data, f)

            # Simulate drag-and-drop using Playwright's file chooser API
            # We'll dispatch the drop event with a DataTransfer
            with open(drop_file, 'r', encoding='utf-8') as f:
                drop_content = f.read()

            # Use JavaScript to simulate the drop
            page.evaluate('''(content) => {
                const textarea = document.getElementById('json-input');
                const dataTransfer = new DataTransfer();
                const file = new File([content], 'drop-test.json', { type: 'application/json' });
                dataTransfer.items.add(file);

                const dropEvent = new DragEvent('drop', {
                    dataTransfer: dataTransfer,
                    bubbles: true,
                    cancelable: true
                });
                textarea.dispatchEvent(dropEvent);
            }''', drop_content)

            # Wait for the file to be processed
            time.sleep(0.5)

            # Verify the textarea was populated
            dropped_text = textarea.input_value()
            dropped_data = json.loads(dropped_text)
            assert dropped_data == drop_data, "Drag-and-drop must populate textarea with file contents"

            # Verify visualization hasn't triggered
            assert tree_container.evaluate('el => el.style.display') == 'none', "Drag-and-drop should not trigger visualization"
            print("✓ $REQ_JSON_INPUT_002: Drag-and-drop zone works")
            print("✓ $REQ_JSON_INPUT_004: Drag-and-drop populates textarea without triggering visualization")

            # $REQ_JSON_INPUT_006: Visualize Button
            visualize_button = page.locator('#visualize-button')
            assert visualize_button.count() == 1, "Visualize button must exist"
            print("✓ $REQ_JSON_INPUT_006: Visualize button exists")

            # Test that visualize button actually triggers visualization
            # Fill with valid JSON first
            textarea.fill(json.dumps(expected_data))
            visualize_button.click()

            # Wait for visualization to render
            time.sleep(1)

            # Verify tree container is now visible
            assert tree_container.evaluate('el => el.style.display') == 'block', "Visualize button must trigger tree rendering"
            print("✓ Visualize button triggers visualization")

            print("\n✓ All JSON input tests passed!")

        finally:
            browser.close()

if __name__ == '__main__':
    test_json_input()
