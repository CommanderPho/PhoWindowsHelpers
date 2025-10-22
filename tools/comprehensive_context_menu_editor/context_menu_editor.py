import json
import os
import sys
import uuid
import tkinter as tk
from tkinter import messagebox, ttk
import ctypes

try:
    import winreg
except ImportError:
    winreg = None


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


def scan_available_items() -> list:
    """Return list of dicts: {id, hive_name, path, key_name, display}"""
    items = []
    hive = HK_NAME_TO_CONST["HKCR"]
    for base in SCAN_SUBKEYS:
        for name in list_subkeys(hive, base):
            full_path = base + "\\" + name
            values = list_values(hive, full_path)
            display = None
            for vname, vdata, _ in values:
                if vname == "":  # default
                    display = str(vdata)
                    break
            if not display:
                display = name
            items.append({
                "id": f"HKCR:{full_path}",
                "hive_name": "HKCR",
                "path": base,
                "key_name": name,
                "display": display,
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

        self.list_available = tk.Listbox(avail_frame, width=50, height=24, exportselection=False, selectmode=tk.EXTENDED)
        ysb_av = ttk.Scrollbar(avail_frame, orient="vertical", command=self.list_available.yview)
        xsb_av = ttk.Scrollbar(avail_frame, orient="horizontal", command=self.list_available.xview)
        self.list_available.configure(yscrollcommand=ysb_av.set, xscrollcommand=xsb_av.set)
        self.list_available.grid(row=0, column=0, sticky="nsew")
        ysb_av.grid(row=0, column=1, sticky="ns")
        xsb_av.grid(row=1, column=0, sticky="ew")

        self.list_hidden = tk.Listbox(hidden_frame, width=50, height=24, exportselection=False, selectmode=tk.EXTENDED)
        ysb_hi = ttk.Scrollbar(hidden_frame, orient="vertical", command=self.list_hidden.yview)
        xsb_hi = ttk.Scrollbar(hidden_frame, orient="horizontal", command=self.list_hidden.xview)
        self.list_hidden.configure(yscrollcommand=ysb_hi.set, xscrollcommand=xsb_hi.set)
        self.list_hidden.grid(row=0, column=0, sticky="nsew")
        ysb_hi.grid(row=0, column=1, sticky="ns")
        xsb_hi.grid(row=1, column=0, sticky="ew")

        # middle buttons
        mid = ttk.Frame(main)
        mid.grid(row=3, column=1, padx=6, sticky="ns")
        ttk.Button(mid, text=">>", command=self.hide_selected).grid(row=0, column=0, pady=2)
        ttk.Button(mid, text="<<", command=self.restore_selected).grid(row=1, column=0, pady=2)
        ttk.Button(mid, text="Refresh", command=self.refresh).grid(row=2, column=0, pady=8)

        # bindings
        self.list_available.bind("<Double-Button-1>", lambda e: self.hide_selected())
        self.list_hidden.bind("<Double-Button-1>", lambda e: self.restore_selected())
        self.filter_entry.bind("<KeyRelease>", lambda e: self.apply_filter())

        # internal state mapping from display text to item dict
        self.available_index = []
        self.available_all = []
        self.hidden_index = []
        self.refresh()

    def _is_admin(self) -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def _admin_status_text(self) -> str:
        return "Running as Administrator" if self._is_admin() else "Not running as Administrator — registry changes may fail"

    def refresh(self):
        self.list_available.delete(0, tk.END)
        self.list_hidden.delete(0, tk.END)
        self.available_index = []
        self.available_all = []
        self.hidden_index = []

        mods = load_modifications()
        hidden_map = mods.get("hidden", {})

        # Load available from registry, filtering ones already hidden (by id)
        current = scan_available_items()
        for item in sorted(current, key=lambda x: x["display"].lower()):
            if item["id"] in hidden_map:
                # If it's actually present in registry despite being marked hidden, skip marking available
                # It will appear on the left only if not hidden
                continue
            self.available_all.append(item)

        self.apply_filter()

        # Hidden items are exactly those in modifications
        for hid in sorted(hidden_map.values(), key=lambda x: x.get("display", "").lower()):
            text = f"{hid.get('display', hid['id'])}  —  {hid['id']}"
            self.list_hidden.insert(tk.END, text)
            self.hidden_index.append(hid)

    def hide_selected(self):
        selections = self.list_available.curselection()
        if not selections:
            return
        errors = []
        for i in selections:
            item = self.available_index[i]
            try:
                self._hide_item(item)
            except Exception as e:
                errors.append(f"{item['display']}: {e}")
        if errors:
            messagebox.showerror(APP_TITLE, "Some items failed to hide:\n" + "\n".join(errors))
        else:
            messagebox.showinfo(APP_TITLE, f"Hidden {len(selections)} item(s)")
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
            "file": os.path.relpath(file_path, get_script_dir()),
        }
        save_modifications(mods)

    def restore_selected(self):
        selections = self.list_hidden.curselection()
        if not selections:
            return
        errors = []
        for i in selections:
            meta = self.hidden_index[i]
            try:
                self._restore_item(meta)
            except Exception as e:
                errors.append(f"{meta.get('display', meta['id'])}: {e}")
        if errors:
            messagebox.showerror(APP_TITLE, "Some items failed to restore:\n" + "\n".join(errors))
        else:
            messagebox.showinfo(APP_TITLE, f"Restored {len(selections)} item(s)")
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
        self.list_available.delete(0, tk.END)
        self.available_index = []
        for item in self.available_all:
            text = f"{item['display']}  —  {item['id']}"
            if query and (query not in item['display'].lower() and query not in item['id'].lower()):
                continue
            self.list_available.insert(tk.END, text)
            self.available_index.append(item)


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


