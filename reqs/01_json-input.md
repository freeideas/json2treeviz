# JSON Input

Documents how the user provides JSON data to the application -- textarea paste, drag-and-drop of files, and file picker.

## $REQ_JSON_INPUT_001: Textarea for JSON Text
**Source:** ./specs/ui.md (Section: "Inputs")

The application must provide a textarea where users can paste JSON text.

## $REQ_JSON_INPUT_002: Drag-and-Drop Zone
**Source:** ./specs/ui.md (Section: "Inputs")

The textarea must also act as the drag-and-drop zone for `.json` files.

## $REQ_JSON_INPUT_003: File Picker
**Source:** ./specs/ui.md (Section: "Inputs")

The application must provide a file picker as an alternative to drag-and-drop for loading `.json` files.

## $REQ_JSON_INPUT_004: Drag-and-Drop Populates Textarea
**Source:** ./specs/ui.md (Section: "Input form behavior")

Dropping a file onto the textarea must populate the textarea with the file contents without triggering immediate visualization.

## $REQ_JSON_INPUT_005: Paste Populates Textarea
**Source:** ./specs/ui.md (Section: "Input form behavior")

Pasting JSON into the textarea must populate the textarea without triggering immediate visualization.

## $REQ_JSON_INPUT_006: Visualize Button
**Source:** ./specs/ui.md (Section: "Inputs")

The application must provide a "Visualize" button to trigger the visualization.

## $REQ_JSON_INPUT_007: Example Data Pre-loaded on Page Load
**Source:** ./specs/ui.md (Section: "Inputs")

The textarea must be pre-loaded with the contents of example-data.json on page load.
