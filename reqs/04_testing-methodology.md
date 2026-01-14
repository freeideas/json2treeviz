# Testing Methodology

Documents the mandated visual verification approach for testing -- using screenshots and visual-test.py alongside DOM inspection.

## $REQ_TEST_METHOD_001: Visual Verification Required
**Source:** ./specs/TESTING.md (Section: "Visual verification")

Tests must use visual verification via `visual-test.py` as well as DOM inspection.

## $REQ_TEST_METHOD_002: Feature Test Process
**Source:** ./specs/TESTING.md (Section: "Visual verification")

For each feature tested: (1) create a small JSON snippet that exercises the feature, (2) paste it into the app and click "Visualize", (3) take a screenshot and verify it shows the expected result.

## $REQ_TEST_METHOD_003: Input Method Coverage
**Source:** ./specs/TESTING.md (Section: "Visual verification")

If reasonably possible, tests must try both pasting JSON text and using drag/drop.

## $REQ_TEST_METHOD_004: Hierarchy from id/parent_id Test
**Source:** ./specs/TESTING.md (Section: "Required tests / Hierarchy from id/parent_id")

Create a JSON array of objects with `id` and `parent_id` fields representing a tree (e.g., CEO -> CTO/CFO -> employees). Visually verify the result looks like a tree or hierarchy, not a flat list.
