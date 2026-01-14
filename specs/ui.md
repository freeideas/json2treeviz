# UI

## Inputs
- A paste area (textarea) for JSON text, pre-loaded with [example-data.json](example-data.json) on page load.
- The textarea must also act as the drag-and-drop zone for `.json` files.
- A file picker as an alternative to drag-and-drop.
- A "Visualize" button to trigger the visualization.

## Input form behavior
- The input form (textarea, file picker, and button) is collapsible.
- Pasting JSON or dropping a file only populates the textarea -- no immediate action.
- Clicking "Visualize" collapses the form and renders the tree.
- The collapsed form can be expanded again to modify the input.

## Output
- Render the JSON as a tree using Cytoscape.js.
- Nodes are collapsible by toggling children.
