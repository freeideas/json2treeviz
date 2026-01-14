# Static Deployment

Documents requirements for the app to function as a static single-page app with no server-side code, working over file:// protocol.

## $REQ_STATIC_001: Static Single-Page Application
**Source:** ./specs/requirements.md (Section: "Functional")

The application must run as a static single-page web app with no server-side code.

## $REQ_STATIC_002: File Protocol Support
**Source:** ./specs/tech.md (Section: root)

The application must work when opened via the `file://` protocol (i.e., double-clicking the HTML file).

## $REQ_STATIC_003: Local Static Dependencies
**Source:** ./specs/tech.md (Section: root)

Cytoscape.js must be included as local static files so the app works over `file://`.

## $REQ_STATIC_004: No Build Step
**Source:** ./specs/tech.md (Section: root)

The application must not require a build step to run.

## $REQ_STATIC_005: No Remote URL Fetching
**Source:** ./specs/requirements.md (Section: "Non-goals")

The application must not fetch resources from remote URLs.

## $REQ_STATIC_006: No Server APIs
**Source:** ./specs/requirements.md (Section: "Non-goals")

The application must not use server APIs.
