# Requirements

## Functional
- Must run as a static single-page web app with no server-side code.
- Must accept JSON from user input only:
  - Paste into a text area.
  - Drag-and-drop a `.json` file (or file picker) and load its contents.
- Must parse any valid JSON input and visualize it as a tree.
- Must render tree nodes that are collapsible by toggling children.

## JSON-to-tree special case
- If a JSON array is a list of objects and the objects contain both `id` and a parent id field, the list must be interpreted as a hierarchy rather than a flat list.
- A parent id field is any key whose name matches `parent[^a-zA-Z0-9]?id` (case-insensitive), such as `Parent-ID`, `ParentID`, `parent$id`, or `pArEnT.iD`.
- Parent/child relationship is defined by matching the parent id field value to `id`.

## Node labels
- Primitive fields on a JSON object must appear as labels on the node.
- Fields with `null` values must not be shown as labels.

## Non-goals
- No remote URL fetching.
- No server APIs.
- No persistence.
