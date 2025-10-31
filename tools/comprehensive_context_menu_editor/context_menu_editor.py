import json
import os
import sys
import uuid
import tkinter as tk
from tkinter import messagebox, ttk
import ctypes
import re

try:
    import winreg
except ImportError:
    winreg = None

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

APP_TITLE = "Comprehensive Context Menu Editor (Minimal)"


def get_script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


DATA_DIR = os.path.join(get_script_dir(), "hidden_entries")
MODS_PATH = os.path.join(get_script_dir(), "registry_modifications.json")


HK_NAME_TO_CONST = {
    "HKCR": winreg.HKEY_CLASSES_ROOT if winreg else None,
}


# Common context menu locations to scan under HKCR
SCAN_SUBKEYS = [
    r"*\\shell",
    r"*\\shellex\\ContextMenuHandlers",
    r"AllFileSystemObjects\\shellex\\ContextMenuHandlers",
    r"Directory\\Background\\shell",
    r"Directory\\Background\\shellex\\ContextMenuHandlers",
    r"Directory\\shell",
    r"Directory\\shellex\\ContextMenuHandlers",
    r"Drive\\shell",
    r"Drive\\shellex\\ContextMenuHandlers",
    r"Folder\\shell",
    r"Folder\\shellex\\ContextMenuHandlers",
    r"lnkfile\\shellex\\ContextMenuHandlers",
]


def ensure_data_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MODS_PATH):
        with open(MODS_PATH, "w", encoding="utf-8") as f:
            json.dump({"hidden": {}}, f, indent=2)


def load_modifications() -> dict:
    if not os.path.exists(MODS_PATH):
        return {"hidden": {}}
    with open(MODS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_modifications(mods: dict) -> None:
    with open(MODS_PATH, "w", encoding="utf-8") as f:
        json.dump(mods, f, indent=2)


def list_subkeys(hive, subkey_path: str) -> list:
    subkeys = []
    try:
        with winreg.OpenKey(hive, subkey_path, 0, winreg.KEY_READ) as key:
            index = 0
            while True:
                try:
                    name = winreg.EnumKey(key, index)
                    subkeys.append(name)
                    index += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass
    return subkeys


def list_values(hive, subkey_path: str) -> list:
    values = []
    try:
        with winreg.OpenKey(hive, subkey_path, 0, winreg.KEY_READ) as key:
            index = 0
            while True:
                try:
                    name, data, vtype = winreg.EnumValue(key, index)
                    values.append((name, data, vtype))
                    index += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass
    return values


def read_key_recursive(hive, subkey_path: str) -> dict:
    node = {"__values__": {}}
    for name, data, vtype in list_values(hive, subkey_path):
        node["__values__"][name] = {"type": vtype, "data": data}
    for sub in list_subkeys(hive, subkey_path):
        child_path = subkey_path + "\\" + sub
        node[sub] = read_key_recursive(hive, child_path)
    return node


def create_key_if_missing(hive, subkey_path: str):
    parts = subkey_path.split("\\")
    current = ""
    for part in parts:
        current = part if not current else current + "\\" + part
        try:
            winreg.CreateKey(hive, current)
        except PermissionError:
            raise


def write_key_recursive(hive, subkey_path: str, data: dict):
    create_key_if_missing(hive, subkey_path)
    with winreg.OpenKey(hive, subkey_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY) as key:
        for name, entry in data.get("__values__", {}).items():
            winreg.SetValueEx(key, name, 0, entry["type"], entry["data"])
    for sub, subdata in data.items():
        if sub == "__values__":
            continue
        child_path = subkey_path + "\\" + sub
        write_key_recursive(hive, child_path, subdata)


def delete_key_tree(hive, subkey_path: str):
    # delete children first
    try:
        with winreg.OpenKey(hive, subkey_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            while True:
                try:
                    child = winreg.EnumKey(key, 0)
                    delete_key_tree(hive, subkey_path + "\\" + child)
                except OSError:
                    break
    except FileNotFoundError:
        return
    # then delete this key
    try:
        winreg.DeleteKey(hive, subkey_path)
    except FileNotFoundError:
        pass


def _values_to_dict(values_list: list) -> dict:
    out = {}
    for name, data, _ in values_list:
        out[name] = data
    return out


def _read_menu_text_from_registry(hive, full_path: str) -> str:
    vals = _values_to_dict(list_values(hive, full_path))
    if isinstance(vals.get("MUIVerb"), str) and vals.get("MUIVerb").strip():
        return vals.get("MUIVerb").strip()
    if isinstance(vals.get(""), str) and vals.get("").strip():
        return vals.get("").strip()
    # For shellex handlers, try CLSID friendly name
    last = full_path.rsplit("\\", 1)[-1]
    if re.fullmatch(r"\{[0-9A-Fa-f\-]{36}\}", last):
        clsid_path = f"CLSID\\{last}"
        try:
            name_vals = _values_to_dict(list_values(hive, clsid_path))
            if isinstance(name_vals.get(""), str) and name_vals.get("").strip():
                return name_vals.get("").strip()
        except Exception:
            pass
    return last


def _resolve_icon_spec_for_shell(hive, full_path: str) -> str | None:
    vals = _values_to_dict(list_values(hive, full_path))
    if "Icon" in vals and str(vals["Icon"]).strip():
        return str(vals["Icon"]).strip()
    # Fallback: command subkey default exe
    cmd_vals = _values_to_dict(list_values(hive, full_path + "\\command"))
    cmd = str(cmd_vals.get("", "")).strip()
    exe = _extract_exe_from_command(cmd)
    return f"{exe},0" if exe else None


def _resolve_icon_spec_for_shellex(hive, full_path: str) -> str | None:
    # full_path ends with GUID or handler key
    clsid = full_path.rsplit("\\", 1)[-1]
    if not re.fullmatch(r"\{[0-9A-Fa-f\-]{36}\}", clsid):
        return None
    default_icon_path = f"CLSID\\{clsid}\\DefaultIcon"
    di_vals = _values_to_dict(list_values(hive, default_icon_path))
    if "" in di_vals and str(di_vals[""]).strip():
        return str(di_vals[""]).strip()
    inproc_path = f"CLSID\\{clsid}\\InprocServer32"
    ip_vals = _values_to_dict(list_values(hive, inproc_path))
    if "" in ip_vals and str(ip_vals[""]).strip():
        return f"{ip_vals['']},0"
    return None


def _extract_exe_from_command(command: str) -> str | None:
    # Match quoted path or first token ending with .exe
    m = re.search(r'"([^"]+\.exe)"', command, re.IGNORECASE)
    if m and os.path.exists(os.path.expandvars(m.group(1))):
        return os.path.expandvars(m.group(1))
    m = re.search(r'(\S+\.exe)', command, re.IGNORECASE)
    if m and os.path.exists(os.path.expandvars(m.group(1))):
        return os.path.expandvars(m.group(1))
    return None


def _parse_icon_spec(icon_spec: str | None) -> tuple[str, int] | None:
    if not icon_spec:
        return None
    try:
        path_part, index_part = icon_spec.split(",", 1)
    except ValueError:
        path_part, index_part = icon_spec, "0"
    path = os.path.expandvars(path_part.strip().strip('"'))
    try:
        index = int(index_part.strip())
    except ValueError:
        index = 0
    return path, index


def _load_ico_photoimage(path: str, size: tuple[int, int] = (16, 16)):
    # Prefer PIL for robust ICO loading and resizing; fallback to Tk native loader
    if os.path.exists(path):
        if ImageTk is not None and Image is not None:
            try:
                img = Image.open(path)
                # Resize if needed to keep UI compact
                try:
                    resample = Image.Resampling.LANCZOS  # Pillow >=9
                except Exception:
                    resample = Image.LANCZOS  # Older Pillow
                img = img.resize(size, resample)
                return ImageTk.PhotoImage(img)
            except Exception:
                pass
        try:
            return tk.PhotoImage(file=path)
        except Exception:
            return None
    return None


def scan_available_items() -> list:
    """Return list of dicts: {id, hive_name, path, key_name, display, menu_text, icon_spec}"""
    items = []
    hive = HK_NAME_TO_CONST["HKCR"]
    for base in SCAN_SUBKEYS:
        for name in list_subkeys(hive, base):
            full_path = base + "\\" + name
            menu_text = _read_menu_text_from_registry(hive, full_path)
            icon_spec = None
            if base.endswith("\\shell") or "\\shell\\" in full_path:
                icon_spec = _resolve_icon_spec_for_shell(hive, full_path)
            elif "shellex\\ContextMenuHandlers" in base or "shellex\\ContextMenuHandlers" in full_path:
                icon_spec = _resolve_icon_spec_for_shellex(hive, full_path)
            items.append({
                "id": f"HKCR:{full_path}",
                "hive_name": "HKCR",
                "path": base,
                "key_name": name,
                "display": menu_text,
                "menu_text": menu_text,
                "icon_spec": icon_spec,
            })
    return items


def export_key_to_file(hive_name: str, full_path: str, out_path: str):
    hive = HK_NAME_TO_CONST[hive_name]
    data = read_key_recursive(hive, full_path)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"hive": hive_name, "path": full_path, "tree": data}, f, indent=2)


def import_key_from_file(in_path: str):
    with open(in_path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    hive = HK_NAME_TO_CONST[obj["hive"]]
    write_key_recursive(hive, obj["path"], obj["tree"])


def sanitize_filename(text: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in text)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)

        ensure_data_dirs()
        self.mods = load_modifications()

        # UI
        main = ttk.Frame(root, padding=8)
        main.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # Make list columns expand
        main.columnconfigure(0, weight=1)
        main.columnconfigure(2, weight=1)
        main.rowconfigure(3, weight=1)

        # Admin status
        self.admin_label = ttk.Label(main, text=self._admin_status_text(), foreground=("#a00" if not self._is_admin() else "#0a0"))
        self.admin_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))

        # Filter
        filter_frame = ttk.Frame(main)
        filter_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 6))
        filter_frame.columnconfigure(1, weight=1)
        ttk.Label(filter_frame, text="Filter:").grid(row=0, column=0, padx=(0, 6))
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var)
        self.filter_entry.grid(row=0, column=1, sticky="ew")
        ttk.Button(filter_frame, text="Clear", command=lambda: self._set_filter("")).grid(row=0, column=2, padx=(6, 0))

        cols = ("Available", "Hidden items")
        ttk.Label(main, text=cols[0]).grid(row=2, column=0, sticky="w")
        ttk.Label(main, text=cols[1]).grid(row=2, column=2, sticky="w")

        # Frames with scrollbars for each list
        avail_frame = ttk.Frame(main)
        hidden_frame = ttk.Frame(main)
        avail_frame.grid(row=3, column=0, sticky="nsew")
        hidden_frame.grid(row=3, column=2, sticky="nsew")

        avail_frame.columnconfigure(0, weight=1)
        avail_frame.rowconfigure(0, weight=1)
        hidden_frame.columnconfigure(0, weight=1)
        hidden_frame.rowconfigure(0, weight=1)

        # Treeviews (Available and Hidden)
        self.tree_available = ttk.Treeview(avail_frame, columns=("menu_text", "id"), show="tree headings", height=24, selectmode="extended")
        self.tree_available.heading("menu_text", text="Menu Text")
        self.tree_available.heading("id", text="Registry ID")
        self.tree_available.column("menu_text", width=300, anchor="w")
        self.tree_available.column("id", width=500, anchor="w")
        self.tree_available.grid(row=0, column=0, sticky="nsew")
        ysb_av = ttk.Scrollbar(avail_frame, orient="vertical", command=self.tree_available.yview)
        self.tree_available.configure(yscrollcommand=ysb_av.set)
        ysb_av.grid(row=0, column=1, sticky="ns")

        self.tree_hidden = ttk.Treeview(hidden_frame, columns=("menu_text", "id"), show="tree headings", height=24, selectmode="extended")
        self.tree_hidden.heading("menu_text", text="Menu Text")
        self.tree_hidden.heading("id", text="Registry ID")
        self.tree_hidden.column("menu_text", width=300, anchor="w")
        self.tree_hidden.column("id", width=500, anchor="w")
        self.tree_hidden.grid(row=0, column=0, sticky="nsew")
        ysb_hi = ttk.Scrollbar(hidden_frame, orient="vertical", command=self.tree_hidden.yview)
        self.tree_hidden.configure(yscrollcommand=ysb_hi.set)
        ysb_hi.grid(row=0, column=1, sticky="ns")

        # middle buttons
        mid = ttk.Frame(main)
        mid.grid(row=3, column=1, padx=6, sticky="ns")
        ttk.Button(mid, text=">>", command=self.hide_selected).grid(row=0, column=0, pady=2)
        ttk.Button(mid, text="<<", command=self.restore_selected).grid(row=1, column=0, pady=2)
        ttk.Button(mid, text="Refresh", command=self.refresh).grid(row=2, column=0, pady=8)

        # bindings
        self.tree_available.bind("<Double-Button-1>", lambda e: self.hide_selected())
        self.tree_hidden.bind("<Double-Button-1>", lambda e: self.restore_selected())
        self.filter_entry.bind("<KeyRelease>", lambda e: self.apply_filter())

        # internal state mapping from display text to item dict
        self.available_all = []  # list of items
        self.available_map = {}  # iid -> item
        self.hidden_index = []   # list of hidden metas (kept for compatibility)
        self.hidden_map = {}     # iid -> meta
        self._image_refs = {}    # iid -> PhotoImage
        self._icon_cache = {}    # icon_spec -> PhotoImage
        self.refresh()

    def _is_admin(self) -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def _admin_status_text(self) -> str:
        return "Running as Administrator" if self._is_admin() else "Not running as Administrator — registry changes may fail"

    def refresh(self):
        # Clear trees
        for tv in (self.tree_available, self.tree_hidden):
            for child in tv.get_children(""):
                tv.delete(child)
        self.available_all = []
        self.available_map = {}
        self.hidden_index = []
        self.hidden_map = {}
        self._image_refs = {}
        self._icon_cache = {}

        mods = load_modifications()
        hidden_map = mods.get("hidden", {})

        # Load available from registry, filtering ones already hidden (by id)
        current = scan_available_items()
        for item in sorted(current, key=lambda x: x["menu_text"].lower()):
            if item["id"] in hidden_map:
                # If it's actually present in registry despite being marked hidden, skip marking available
                # It will appear on the left only if not hidden
                continue
            self.available_all.append(item)

        self.apply_filter()

        # Hidden items are exactly those in modifications
        for hid in sorted(hidden_map.values(), key=lambda x: x.get("display", "").lower()):
            iid = hid["id"]
            menu_text = hid.get("display", iid)
            icon = self._get_or_load_icon(hid.get("icon_spec"))
            if icon is not None:
                self.tree_hidden.insert("", tk.END, iid=iid, text=menu_text, image=icon, values=(menu_text, iid))
                self._image_refs[iid] = icon
            else:
                self.tree_hidden.insert("", tk.END, iid=iid, text=menu_text, values=(menu_text, iid))
            self.hidden_index.append(hid)
            self.hidden_map[iid] = hid

    def hide_selected(self):
        sel = self.tree_available.selection()
        if not sel:
            return
        errors = []
        for iid in sel:
            item = self.available_map.get(iid)
            try:
                self._hide_item(item)
            except Exception as e:
                errors.append(f"{item['display']}: {e}")
        if errors:
            messagebox.showerror(APP_TITLE, "Some items failed to hide:\n" + "\n".join(errors))
        else:
            messagebox.showinfo(APP_TITLE, f"Hidden {len(sel)} item(s)")
        self.refresh()

    def _hide_item(self, item: dict):
        hive_name = item["hive_name"]
        full_path = f"{item['path']}\\{item['key_name']}"
        item_id = item["id"]

        # Export
        uid = str(uuid.uuid4())
        file_name = sanitize_filename(item_id) + "__" + uid + ".json"
        file_path = os.path.join(DATA_DIR, file_name)
        export_key_to_file(hive_name, full_path, file_path)

        # Delete from registry
        hive = HK_NAME_TO_CONST[hive_name]
        delete_key_tree(hive, full_path)

        # Record modification
        mods = load_modifications()
        mods.setdefault("hidden", {})[item_id] = {
            "id": item_id,
            "hive": hive_name,
            "path": full_path,
            "display": item["display"],
            "icon_spec": item.get("icon_spec"),
            "file": os.path.relpath(file_path, get_script_dir()),
        }
        save_modifications(mods)

    def restore_selected(self):
        sel = self.tree_hidden.selection()
        if not sel:
            return
        errors = []
        for iid in sel:
            meta = self.hidden_map.get(iid)
            try:
                self._restore_item(meta)
            except Exception as e:
                errors.append(f"{meta.get('display', meta['id'])}: {e}")
        if errors:
            messagebox.showerror(APP_TITLE, "Some items failed to restore:\n" + "\n".join(errors))
        else:
            messagebox.showinfo(APP_TITLE, f"Restored {len(sel)} item(s)")
        self.refresh()

    def _restore_item(self, meta: dict):
        file_path = os.path.join(get_script_dir(), meta["file"]) if not os.path.isabs(meta["file"]) else meta["file"]
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing backup file: {file_path}")

        # Restore into registry
        import_key_from_file(file_path)

        # Update modifications and remove backup file
        mods = load_modifications()
        mods.get("hidden", {}).pop(meta["id"], None)
        save_modifications(mods)
        try:
            os.remove(file_path)
        except OSError:
            pass

    def _set_filter(self, text: str):
        self.filter_var.set(text)
        self.apply_filter()

    def apply_filter(self):
        query = self.filter_var.get().strip().lower()
        for child in self.tree_available.get_children(""):
            self.tree_available.delete(child)
        self.available_map = {}
        # Insert rows with placeholder icons for now (actual icon loading will be resolved later)
        for item in self.available_all:
            menu_text = item.get("menu_text") or item.get("display") or item.get("id")
            if query and (query not in str(menu_text).lower() and query not in item['id'].lower()):
                continue
            iid = item['id']
            icon = self._get_or_load_icon(item.get("icon_spec"))
            if icon is not None:
                self.tree_available.insert("", tk.END, iid=iid, text=menu_text, image=icon, values=(menu_text, item['id']))
                self._image_refs[iid] = icon
            else:
                self.tree_available.insert("", tk.END, iid=iid, text=menu_text, values=(menu_text, item['id']))
            self.available_map[iid] = item

    def _get_or_load_icon(self, icon_spec: str | None):
        if not icon_spec:
            return None
        if icon_spec in self._icon_cache:
            return self._icon_cache[icon_spec]
        parsed = _parse_icon_spec(icon_spec)
        if not parsed:
            return None
        path, index = parsed
        # For now, support only direct .ico paths; ignore index.
        if path.lower().endswith('.ico'):
            photo = _load_ico_photoimage(path)
            if photo is not None:
                self._icon_cache[icon_spec] = photo
                return photo
        return None


def main():
    if os.name != "nt" or winreg is None:
        print("This tool only runs on Windows with Python's winreg available.")
        sys.exit(1)

    # Auto-elevate: if not admin, relaunch with UAC
    try:
        is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        is_admin = False
    if not is_admin:
        params = "\"" + os.path.abspath(__file__) + "\""
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)
        except Exception:
            # If elevation fails, continue but warn inside app
            pass

    ensure_data_dirs()
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()


