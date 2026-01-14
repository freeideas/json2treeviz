#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import sys
import os
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def main():
    # Assume CWD is project root
    project_root = Path.cwd()
    released_dir = project_root / 'released'

    print("Testing build output requirements...")

    # $REQ_BUILD_001: No Build Step Required
    # This requirement states the app should be static files with no compilation
    # We verify this by checking that the released directory contains only static files

    # $REQ_BUILD_002: Static Single-Page Web App
    # Verify the released directory exists and contains HTML, JS, CSS files
    assert released_dir.exists(), f"Released directory must exist: {released_dir}"  # $REQ_BUILD_002

    required_files = {
        'index.html': 'HTML',  # $REQ_BUILD_002
        'app.js': 'JavaScript',  # $REQ_BUILD_002
        'styles.css': 'CSS',  # $REQ_BUILD_002
    }

    for filename, filetype in required_files.items():
        filepath = released_dir / filename
        assert filepath.exists(), f"Required {filetype} file must exist: {filename}"  # $REQ_BUILD_002
        assert filepath.is_file(), f"{filename} must be a file, not a directory"  # $REQ_BUILD_002

    # $REQ_BUILD_003: Cytoscape as Local Static Files
    cytoscape_file = released_dir / 'cytoscape.min.js'
    assert cytoscape_file.exists(), "Cytoscape.js must be included as a local file"  # $REQ_BUILD_003
    assert cytoscape_file.is_file(), "cytoscape.min.js must be a file"  # $REQ_BUILD_003

    # Verify it's actually a JavaScript file with some content
    cytoscape_content = cytoscape_file.read_text(encoding='utf-8')
    assert len(cytoscape_content) > 1000, "Cytoscape.js file appears too small to be valid"  # $REQ_BUILD_003

    # $REQ_BUILD_004: Works Over file:// Protocol
    # Verify the HTML file references local files (not CDN URLs)
    index_html = released_dir / 'index.html'
    html_content = index_html.read_text(encoding='utf-8')

    # Check that HTML references the local cytoscape file
    assert 'cytoscape.min.js' in html_content, "HTML must reference local cytoscape.min.js"  # $REQ_BUILD_004

    # Check that HTML doesn't use CDN links for Cytoscape
    assert 'cdn.jsdelivr.net' not in html_content.lower(), "HTML must not use CDN links (violates file:// requirement)"  # $REQ_BUILD_004
    assert 'unpkg.com' not in html_content.lower(), "HTML must not use CDN links (violates file:// requirement)"  # $REQ_BUILD_004

    # Check that HTML references local CSS and JS files
    assert 'styles.css' in html_content, "HTML must reference local styles.css"  # $REQ_BUILD_004
    assert 'app.js' in html_content, "HTML must reference local app.js"  # $REQ_BUILD_004

    # $REQ_BUILD_001: Verify no compiled artifacts
    # The directory should only contain static files, no .exe, .dll, .so, etc.
    for item in released_dir.iterdir():
        if item.is_file():
            suffix = item.suffix.lower()
            # Allow only static web files
            allowed_extensions = ['.html', '.js', '.css', '.json', '.txt', '.md', '.svg', '.png', '.jpg', '.jpeg', '.gif', '.ico']
            assert suffix in allowed_extensions, f"Released directory should only contain static files, found: {item.name}"  # $REQ_BUILD_001

    print("✓ All build output requirements verified")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Test error: {e}")
        sys.exit(1)
