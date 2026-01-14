# Transform

## Parsing
- Parse the JSON text into a JS value.

## Tree construction
- Objects become nodes.
  - Primitive fields (string/number/bool) are shown as labels on the object node.
  - Fields with `null` values are not shown as labels.
  - Nested objects and arrays become child nodes.
- Arrays become nodes with one child per element.

## Hierarchy override for arrays of objects
- If an array is a list of objects and each object has `id` and a parent id field, the array is interpreted as a parent/child tree instead of a flat list.
- A parent id field is any key whose name matches `parent[^a-zA-Z0-9]?id` (case-insensitive), such as `Parent-ID`, `ParentID`, `parent$id`, or `pArEnT.iD`.
- Parent/child relationship is defined by matching the parent id field value to `id`.
- See [example-data.json](example-data.json) for a sample hierarchical dataset.
