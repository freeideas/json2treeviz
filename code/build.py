#!/usr/bin/env uvrun
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import sys
import os
import shutil
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# $REQ_BUILD_001: No Build Step Required
# $REQ_BUILD_002: Static Single-Page Web App
# $REQ_BUILD_003: Cytoscape as Local Static Files
# $REQ_BUILD_004: Works Over file:// Protocol

def main():
    # Get the directory paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    released_dir = project_root / 'released'

    print("Building json2treeviz...")
    print(f"Code directory: {script_dir}")
    print(f"Output directory: {released_dir}")

    # Create the released directory
    if released_dir.exists():
        print(f"Cleaning existing {released_dir}...")
        shutil.rmtree(released_dir)

    released_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created {released_dir}")

    # Files to copy
    files_to_copy = [
        'index.html',
        'app.js',
        'styles.css',
        'cytoscape.min.js'
    ]

    # Copy files to released directory
    for filename in files_to_copy:
        source = script_dir / filename
        destination = released_dir / filename

        if not source.exists():
            print(f"ERROR: Required file not found: {source}")
            return 1

        shutil.copy2(source, destination)
        print(f"Copied {filename}")

    # $REQ_JSON_INPUT_007: Copy example-data.json from specs
    example_data_source = project_root / 'specs' / 'example-data.json'
    example_data_dest = released_dir / 'example-data.json'
    if example_data_source.exists():
        shutil.copy2(example_data_source, example_data_dest)
        print(f"Copied example-data.json")
    else:
        print(f"WARNING: example-data.json not found at {example_data_source}")

    print("\nBuild completed successfully!")
    print(f"Output files in: {released_dir}")
    print("\nTo use the application:")
    print(f"  Open {released_dir / 'index.html'} in a web browser")

    return 0

if __name__ == '__main__':
    sys.exit(main())
