# Testing

## Visual verification

Tests must use visual verification via `visual-test.py` as well as DOM inspection.

For each feature:
1. Create a small JSON snippet that exercises the feature.
2. Paste it into the app and click "Visualize".
3. Take a screenshot and verify it shows the expected result.
4. If reasonably possible, try both pasting json text and using drag/drop.

## Required tests

### Hierarchy from id/parent_id

Create a JSON array of objects with `id` and `parent_id` fields representing a tree (e.g., CEO -> CTO/CFO -> employees). Visually verify the result looks like a tree or hierarchy, not a flat list.