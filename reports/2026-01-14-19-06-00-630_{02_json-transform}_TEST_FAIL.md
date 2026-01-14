# Test Report: 02_json-transform

**Status:** FAIL
**Exit Code:** 1
**Timestamp:** 2026-01-14-19-06-00-630
**Test File:** tests/failing/02_json-transform.py

## Output

```
[stderr] Installed 4 packages in 698ms
✓ $REQ_TRANSFORM_001: JSON text parsed successfully
[stderr] Traceback (most recent call last):
[stderr]   File "C:\Users\Human\Desktop\prjx\json2treeviz\tests\failing\02_json-transform.py", line 218, in <module>
[stderr]     test_json_transform()
[stderr]     ~~~~~~~~~~~~~~~~~~~^^
[stderr]   File "C:\Users\Human\Desktop\prjx\json2treeviz\tests\failing\02_json-transform.py", line 63, in test_json_transform
[stderr]     test_json({"name": "Test", "value": 42}, lambda p: (
[stderr]     ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]         # Check that a node exists with the object's labels
[stderr]         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]     ...<2 lines>...
[stderr]         }""")
[stderr]         ^^^^^
[stderr]     ))
[stderr]     ^^
[stderr]   File "C:\Users\Human\Desktop\prjx\json2treeviz\tests\failing\02_json-transform.py", line 47, in test_json
[stderr]     page.fill('#json-input', json_str)
[stderr]     ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\sync_api\_generated.py", line 10173, in fill
[stderr]     self._sync(
[stderr]     ~~~~~~~~~~^
[stderr]         self._impl_obj.fill(
[stderr]         ^^^^^^^^^^^^^^^^^^^^
[stderr]     ...<6 lines>...
[stderr]         )
[stderr]         ^
[stderr]     )
[stderr]     ^
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\_impl\_sync_base.py", line 115, in _sync
[stderr]     return task.result()
[stderr]            ~~~~~~~~~~~^^
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\_impl\_page.py", line 893, in fill
[stderr]     return await self._main_frame.fill(**locals_to_params(locals()))
[stderr]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\_impl\_frame.py", line 607, in fill
[stderr]     await self._fill(**locals_to_params(locals()))
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\_impl\_frame.py", line 619, in _fill
[stderr]     await self._channel.send("fill", self._timeout, locals_to_params(locals()))
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\_impl\_connection.py", line 69, in send
[stderr]     return await self._connection.wrap_api_call(
[stderr]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]     ...<3 lines>...
[stderr]     )
[stderr]     ^
[stderr]   File "C:\Users\Human\AppData\Local\uv\cache\environments-v2\02-json-transform-479c000ea8f165fa\Lib\site-packages\playwright\_impl\_connection.py", line 559, in wrap_api_call
[stderr]     raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
[stderr] playwright._impl._errors.TimeoutError: Page.fill: Timeout 30000ms exceeded.
[stderr] Call log:
[stderr]   - waiting for locator("#json-input")
[stderr]     - locator resolved to <textarea rows="10" id="json-input" placeholder="Paste JSON here or drag and drop a .json file..."></textarea>
[stderr]     - fill("{"name": "Test", "value": 42}")
[stderr]   - attempting fill action
[stderr]     2 × waiting for element to be visible, enabled and editable
[stderr]       - element is not visible
[stderr]     - retrying fill action
[stderr]     - waiting 20ms
[stderr]     2 × waiting for element to be visible, enabled and editable
[stderr]       - element is not visible
[stderr]     - retrying fill action
[stderr]       - waiting 100ms
[stderr]     59 × waiting for element to be visible, enabled and editable
[stderr]        - element is not visible
[stderr]      - retrying fill action
[stderr]        - waiting 500ms
[stderr] 

```
