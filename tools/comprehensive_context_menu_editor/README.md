This tool presents a simple GUI to hide ANY items from the Windows context menus, even the ones added by applications and accessible only via the registry.

- Always backup the Windows Registry before making any changes
- Keep track of the specific keys that are "hidden" (removed) so they can easily be re-inserted later.
- The program begins by scanning the Windows registry to discover all context menu items and present on the system
- It prevents these to the user graphically as a table/list, which each row containing the name/key/icon if available/etc
- To the right of this list should be another table labeled "Hidden items", which is initially empty. The user can double click on an item in either list to move it to the other one.
- When moved to the "hidden" list, it is copied to the local "hidden_entries" filesystem folder, an entry is added to a local `registry_modifications.json` file to make note of its name/location, and then removed from the registry.
- When restored from the "hidden" list, the inverse is done.

Run (Windows only)
- Install Python 3.8+.
- Run as Administrator for registry edits to succeed.
- Execute:
  - `python tools/comprehensive_context_menu_editor/context_menu_editor.py`
  - If not elevated, the tool will auto-prompt for elevation (UAC) and relaunch.

Features (minimal implementation)
- Shows available vs hidden context menu items from common `HKCR` locations.
- Double-click or use buttons to hide/restore (multi-select supported).
- Hidden entries are exported as JSON into `hidden_entries/` and tracked in `registry_modifications.json`.
- Filter box to quickly search available items.