# Build Requirements

Requirements for the contents of the `./released/` directory.

## $REQ_BUILD_001: No Build Step Required
**Source:** ./specs/tech.md (Section: root)

The application must not require a build step.

## $REQ_BUILD_002: Static Single-Page Web App
**Source:** ./specs/requirements.md (Section: "Functional")

The `./released/` directory must contain a static single-page web app (HTML, JavaScript, CSS) with no server-side code.

## $REQ_BUILD_003: Cytoscape as Local Static Files
**Source:** ./specs/tech.md (Section: root)

Cytoscape.js must be included as local static files within `./released/` so the app works when opened via `file://` protocol.

## $REQ_BUILD_004: Works Over file:// Protocol
**Source:** ./specs/tech.md (Section: root)

The released app must be fully functional when opened directly from the filesystem (via `file://` URL) without requiring a web server.
