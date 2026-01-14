# Tree Rendering

Documents how the tree is visually rendered using Cytoscape.js, including node display and collapsible behavior.

## $REQ_TREE_RENDERING_001: Render JSON as Tree
**Source:** ./specs/ui.md (Section: "Output")

The JSON must be rendered as a tree using Cytoscape.js.

## $REQ_TREE_RENDERING_002: Objects Become Nodes
**Source:** ./specs/transform.md (Section: "Tree construction")

Objects in the JSON become nodes in the rendered tree.

## $REQ_TREE_RENDERING_003: Primitive Fields Displayed as Node Labels
**Source:** ./specs/requirements.md (Section: "Node labels")

Primitive fields (string, number, boolean) on a JSON object must appear as labels on the node.

## $REQ_TREE_RENDERING_004: Null Fields Not Shown as Labels
**Source:** ./specs/requirements.md (Section: "Node labels")

Fields with `null` values must not be shown as labels on the node.

## $REQ_TREE_RENDERING_005: Nested Objects and Arrays Become Child Nodes
**Source:** ./specs/transform.md (Section: "Tree construction")

Nested objects and arrays within an object become child nodes of that object's node.

## $REQ_TREE_RENDERING_006: Arrays Become Nodes with Children
**Source:** ./specs/transform.md (Section: "Tree construction")

Arrays become nodes with one child node per element.

## $REQ_TREE_RENDERING_007: Nodes Are Collapsible
**Source:** ./specs/requirements.md (Section: "Functional")

Tree nodes must be collapsible by toggling their children.
