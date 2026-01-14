# Input Form Behavior

Documents the behavior of the input form -- collapsibility, the Visualize button action, and expand/collapse interaction.

## $REQ_INPUT_FORM_001: Input Form is Collapsible
**Source:** ./specs/ui.md (Section: "Input form behavior")

The input form (textarea, file picker, and button) must be collapsible.

## $REQ_INPUT_FORM_002: No Immediate Action on Paste or Drop
**Source:** ./specs/ui.md (Section: "Input form behavior")

Pasting JSON or dropping a file must only populate the textarea without triggering any immediate visualization action.

## $REQ_INPUT_FORM_003: Visualize Button Collapses Form and Renders Tree
**Source:** ./specs/ui.md (Section: "Input form behavior")

Clicking the "Visualize" button must collapse the input form and render the tree visualization.

## $REQ_INPUT_FORM_004: Collapsed Form Can Be Expanded
**Source:** ./specs/ui.md (Section: "Input form behavior")

The collapsed form must be expandable again to allow modification of the input.
