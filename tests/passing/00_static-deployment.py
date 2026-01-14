#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Test for static deployment requirements.
Verifies the app functions as a static single-page app with no server-side code.
"""

import os
import re
import sys
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    # Get project root (assuming test is run from project root)
    project_root = Path.cwd()
    released_dir = project_root / 'released'

    # $REQ_STATIC_001: Static Single-Page Application
    # Verify that index.html exists and is a static file
    index_html = released_dir / 'index.html'
    assert index_html.exists(), f"index.html not found at {index_html}"  # $REQ_STATIC_001

    # Read the HTML content
    html_content = index_html.read_text(encoding='utf-8')

    # $REQ_STATIC_002: File Protocol Support
    # The HTML should not have any restrictions that prevent file:// protocol
    # Check for no server-side includes, no PHP, no server endpoints
    assert '<?php' not in html_content, "PHP code found - not static"  # $REQ_STATIC_002
    assert '<%' not in html_content, "Server-side template tags found - not static"  # $REQ_STATIC_002

    # $REQ_STATIC_003: Local Static Dependencies
    # Verify Cytoscape.js is included locally (not from CDN)
    cytoscape_local_pattern = r'<script\s+src="cytoscape[^"]*\.js"'
    assert re.search(cytoscape_local_pattern, html_content), \
        "Cytoscape.js not included as local file"  # $REQ_STATIC_003

    # Verify Cytoscape.js file exists locally
    cytoscape_match = re.search(r'<script\s+src="([^"]*cytoscape[^"]*\.js)"', html_content)
    assert cytoscape_match, "Could not find cytoscape script tag"  # $REQ_STATIC_003
    cytoscape_path = cytoscape_match.group(1)
    cytoscape_file = released_dir / cytoscape_path
    assert cytoscape_file.exists(), f"Cytoscape.js file not found: {cytoscape_file}"  # $REQ_STATIC_003

    # $REQ_STATIC_005: No Remote URL Fetching
    # Check for no CDN links, no remote script/stylesheet sources
    remote_patterns = [
        r'https?://cdn\.',
        r'https?://[^"\']*\.cloudflare\.com',
        r'https?://[^"\']*\.jsdelivr\.net',
        r'https?://[^"\']*\.unpkg\.com',
        r'https?://[^"\']*\.googleapis\.com',
    ]
    for pattern in remote_patterns:
        assert not re.search(pattern, html_content, re.IGNORECASE), \
            f"Remote URL found matching pattern {pattern}"  # $REQ_STATIC_005

    # Check for no absolute HTTP/HTTPS URLs in script src or link href
    script_remote = re.search(r'<script[^>]+src="https?://', html_content, re.IGNORECASE)
    assert not script_remote, "Remote script URL found"  # $REQ_STATIC_005

    link_remote = re.search(r'<link[^>]+href="https?://', html_content, re.IGNORECASE)
    assert not link_remote, "Remote stylesheet URL found"  # $REQ_STATIC_005

    # $REQ_STATIC_006: No Server APIs
    # Check that JavaScript doesn't make fetch/XMLHttpRequest calls to external APIs
    # Read app.js to check for server API calls
    app_js = released_dir / 'app.js'
    assert app_js.exists(), f"app.js not found at {app_js}"  # $REQ_STATIC_006

    js_content = app_js.read_text(encoding='utf-8')

    # Check for no fetch to external URLs (allow relative paths only)
    fetch_external = re.search(r'fetch\s*\(\s*["\']https?://', js_content, re.IGNORECASE)
    assert not fetch_external, "External fetch API call found"  # $REQ_STATIC_006

    # Check for no XMLHttpRequest to external URLs
    xhr_external = re.search(r'XMLHttpRequest.*open\([^)]*https?://', js_content, re.IGNORECASE | re.DOTALL)
    assert not xhr_external, "External XMLHttpRequest call found"  # $REQ_STATIC_006

    # $REQ_STATIC_004: No Build Step
    # Verify that the app can run directly without build artifacts
    # Check that there's no package.json build scripts required
    # The presence of ready-to-use HTML/JS/CSS files indicates no build needed
    assert (released_dir / 'styles.css').exists(), "styles.css not found"  # $REQ_STATIC_004
    assert app_js.exists(), "app.js not found"  # $REQ_STATIC_004

    # Verify no module bundler artifacts that would require building
    # Check JS doesn't use module imports that need bundling
    assert 'import ' not in js_content or '// import' in js_content, \
        "ES6 imports found - requires build step"  # $REQ_STATIC_004
    assert 'require(' not in js_content or '// require' in js_content, \
        "CommonJS require found - requires build step"  # $REQ_STATIC_004

    print("✓ All static deployment requirements verified")


if __name__ == '__main__':
    main()
