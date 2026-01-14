# Node Labels

Documents how primitive fields on JSON objects appear as labels on tree nodes, and the exclusion of null values.

## $REQ_NODE_LABELS_001: Primitive Fields Displayed as Labels
**Source:** ./specs/requirements.md (Section: "Node labels")

Primitive fields (string, number, boolean) on a JSON object must be shown as labels on the object's tree node.

## $REQ_NODE_LABELS_002: Null Values Excluded from Labels
**Source:** ./specs/requirements.md (Section: "Node labels")

Fields with `null` values must not be shown as labels on tree nodes.
