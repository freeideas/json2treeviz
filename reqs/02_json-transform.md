# JSON Transform

Documents how JSON text is parsed and converted into a tree structure, including the hierarchy override logic for arrays of objects with id/parent_id fields.

## $REQ_TRANSFORM_001: Parse JSON Text
**Source:** ./specs/transform.md (Section: "Parsing")

The application must parse JSON text into a JavaScript value.

## $REQ_TRANSFORM_002: Objects Become Nodes
**Source:** ./specs/transform.md (Section: "Tree construction")

JSON objects must become nodes in the tree visualization.

## $REQ_TRANSFORM_003: Primitive Fields as Labels
**Source:** ./specs/transform.md (Section: "Tree construction")

Primitive fields (string/number/bool) on a JSON object must be shown as labels on the object node.

## $REQ_TRANSFORM_004: Null Fields Not Shown
**Source:** ./specs/transform.md (Section: "Tree construction")

Fields with `null` values must not be shown as labels on nodes.

## $REQ_TRANSFORM_005: Nested Objects and Arrays Become Children
**Source:** ./specs/transform.md (Section: "Tree construction")

Nested objects and arrays within a JSON object must become child nodes of the object node.

## $REQ_TRANSFORM_006: Arrays Become Nodes with Element Children
**Source:** ./specs/transform.md (Section: "Tree construction")

Arrays must become nodes with one child per element.

## $REQ_TRANSFORM_007: Hierarchy Override for Arrays of Objects with id/parent_id
**Source:** ./specs/transform.md (Section: "Hierarchy override for arrays of objects")

If an array is a list of objects and each object has `id` and a parent id field, the array must be interpreted as a parent/child tree instead of a flat list.

## $REQ_TRANSFORM_008: Parent ID Field Pattern Matching
**Source:** ./specs/transform.md (Section: "Hierarchy override for arrays of objects")

A parent id field is any key whose name matches `parent[^a-zA-Z0-9]?id` (case-insensitive), such as `Parent-ID`, `ParentID`, `parent$id`, or `pArEnT.iD`.

## $REQ_TRANSFORM_009: Parent/Child Relationship by ID Matching
**Source:** ./specs/transform.md (Section: "Hierarchy override for arrays of objects")

Parent/child relationship must be defined by matching the parent id field value to `id`.
