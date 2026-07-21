"""
FastCopy Wrapper — GUI Interface
=================================
Tkinter-based GUI for interactive FastCopy operations.

Launch directly::

    python -m tools.fastcopy_wrapper gui
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

from .fastcopy_tool import CopyResult, FastCopyConfig, FastCopyRunner, find_fastcopy_exe

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
_BG = "#1e1e2e"          # dark background
_BG_CARD = "#2a2a3c"     # card / frame background
_BG_INPUT = "#33334d"    # input field background
_FG = "#cdd6f4"          # primary foreground text
_FG_DIM = "#8888aa"      # dimmed / secondary text
_ACCENT = "#89b4fa"      # accent blue
_ACCENT_HOVER = "#74c7ec" # lighter accent on hover
_GREEN = "#a6e3a1"       # success green
_RED = "#f38ba8"         # error red
_YELLOW = "#f9e2af"      # warning yellow
_BORDER = "#45475a"      # subtle border
_BTN_BG = "#45475a"      # button default background
_BTN_FG = "#cdd6f4"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_label(parent: tk.Widget, text: str, **kw) -> tk.Label:
    return tk.Label(
        parent, text=text, bg=_BG_CARD, fg=_FG,
        font=("Segoe UI", 10), anchor="w", **kw,
    )


def _make_entry(parent: tk.Widget, **kw) -> tk.Entry:
    return tk.Entry(
        parent, bg=_BG_INPUT, fg=_FG, insertbackground=_FG,
        font=("Segoe UI", 10), relief="flat",
        highlightthickness=1, highlightbackground=_BORDER,
        highlightcolor=_ACCENT, **kw,
    )


class HoverButton(tk.Button):
    """A flat button with hover color change."""

    def __init__(self, master, bg=_BTN_BG, fg=_BTN_FG,
                 hover_bg=_ACCENT, hover_fg="#11111b", **kw):
        super().__init__(
            master, bg=bg, fg=fg, relief="flat", cursor="hand2",
            font=("Segoe UI Semibold", 10),
            activebackground=hover_bg, activeforeground=hover_fg, **kw,
        )
        self._bg = bg
        self._hover_bg = hover_bg
        self._hover_fg = hover_fg
        self._fg = fg
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _evt):
        self.config(bg=self._hover_bg, fg=self._hover_fg)

    def _on_leave(self, _evt):
        self.config(bg=self._bg, fg=self._fg)


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------
class FastCopyGUI:
    """Main window for the FastCopy Wrapper GUI."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._running = False
        self._thread: Optional[threading.Thread] = None

        self._setup_window()
        self._create_widgets()

    # -- window setup -------------------------------------------------------

    def _setup_window(self) -> None:
        self.root.title("FastCopy Tool")
        self.root.configure(bg=_BG)
        self.root.minsize(720, 620)
        self.root.geometry("780x700")

        # Try to set a dark title bar on Windows 10/11
        try:
            from ctypes import windll, byref, sizeof, c_int
            hwnd = windll.user32.GetParent(self.root.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = c_int(1)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                byref(value), sizeof(value),
            )
        except Exception:
            pass

    # -- widget creation ----------------------------------------------------

    def _create_widgets(self) -> None:
        # Header
        header = tk.Frame(self.root, bg=_BG, pady=8)
        header.pack(fill="x")
        tk.Label(
            header, text="⚡ FastCopy Tool", bg=_BG, fg=_ACCENT,
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left", padx=16)
        tk.Label(
            header, text="Fast file copy & move with dry-run support",
            bg=_BG, fg=_FG_DIM, font=("Segoe UI", 10),
        ).pack(side="left", padx=(0, 16))

        # Main card
        card = tk.Frame(self.root, bg=_BG_CARD, bd=0, padx=16, pady=12)
        card.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self._build_source_section(card)
        self._build_dest_section(card)
        ttk.Separator(card).pack(fill="x", pady=8)
        self._build_options_section(card)
        ttk.Separator(card).pack(fill="x", pady=8)
        self._build_filter_section(card)
        ttk.Separator(card).pack(fill="x", pady=8)
        self._build_action_buttons(card)
        self._build_output_section(card)

    # -- source paths -------------------------------------------------------

    def _build_source_section(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=_BG_CARD)
        frame.pack(fill="x", pady=(0, 4))

        _make_label(frame, text="Source Path(s):").pack(anchor="w")

        btn_row = tk.Frame(frame, bg=_BG_CARD)
        btn_row.pack(fill="x", pady=(2, 0))

        self._source_entry = _make_entry(btn_row)
        self._source_entry.pack(side="left", fill="x", expand=True, ipady=3)

        HoverButton(btn_row, text=" + Add ", command=self._add_source).pack(
            side="left", padx=(4, 0),
        )
        HoverButton(btn_row, text=" 📁 Browse ", command=self._browse_source).pack(
            side="left", padx=(4, 0),
        )

        # Listbox for added sources
        list_frame = tk.Frame(frame, bg=_BG_INPUT, highlightthickness=1,
                              highlightbackground=_BORDER)
        list_frame.pack(fill="x", pady=(4, 0))

        self._source_listbox = tk.Listbox(
            list_frame, bg=_BG_INPUT, fg=_FG, selectbackground=_ACCENT,
            selectforeground="#11111b", font=("Consolas", 9),
            height=3, relief="flat", bd=0, activestyle="none",
        )
        self._source_listbox.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(list_frame, command=self._source_listbox.yview)
        sb.pack(side="right", fill="y")
        self._source_listbox.config(yscrollcommand=sb.set)

        rm_btn = HoverButton(
            frame, text=" ✕ Remove Selected ",
            bg=_BG_INPUT, hover_bg=_RED,
            command=self._remove_source,
        )
        rm_btn.pack(anchor="e", pady=(2, 0))

    def _add_source(self) -> None:
        path = self._source_entry.get().strip()
        if path:
            self._source_listbox.insert(tk.END, path)
            self._source_entry.delete(0, tk.END)

    def _browse_source(self) -> None:
        path = filedialog.askdirectory(title="Select Source Directory")
        if path:
            self._source_listbox.insert(tk.END, path)

    def _remove_source(self) -> None:
        sel = self._source_listbox.curselection()
        if sel:
            self._source_listbox.delete(sel[0])

    # -- destination --------------------------------------------------------

    def _build_dest_section(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=_BG_CARD)
        frame.pack(fill="x", pady=(4, 0))

        _make_label(frame, text="Destination:").pack(anchor="w")

        row = tk.Frame(frame, bg=_BG_CARD)
        row.pack(fill="x", pady=(2, 0))

        self._dest_entry = _make_entry(row)
        self._dest_entry.pack(side="left", fill="x", expand=True, ipady=3)

        HoverButton(row, text=" 📁 Browse ", command=self._browse_dest).pack(
            side="left", padx=(4, 0),
        )

    def _browse_dest(self) -> None:
        path = filedialog.askdirectory(title="Select Destination Directory")
        if path:
            self._dest_entry.delete(0, tk.END)
            self._dest_entry.insert(0, path)

    # -- options (mode, verify, dry-run) ------------------------------------

    def _build_options_section(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=_BG_CARD)
        frame.pack(fill="x")

        # Mode
        mode_frame = tk.Frame(frame, bg=_BG_CARD)
        mode_frame.pack(side="left", padx=(0, 24))

        _make_label(mode_frame, text="Mode:").pack(anchor="w")
        self._mode_var = tk.StringVar(value="copy")

        rb_frame = tk.Frame(mode_frame, bg=_BG_CARD)
        rb_frame.pack(anchor="w")

        for text, val in [("Copy", "copy"), ("Move", "move")]:
            rb = tk.Radiobutton(
                rb_frame, text=text, variable=self._mode_var, value=val,
                bg=_BG_CARD, fg=_FG, selectcolor=_BG_INPUT,
                activebackground=_BG_CARD, activeforeground=_ACCENT,
                font=("Segoe UI", 10), command=self._on_mode_change,
            )
            rb.pack(side="left", padx=(0, 12))

        # Checkboxes
        cb_frame = tk.Frame(frame, bg=_BG_CARD)
        cb_frame.pack(side="left")

        self._verify_var = tk.BooleanVar(value=False)
        self._dryrun_var = tk.BooleanVar(value=False)
        self._nonstop_var = tk.BooleanVar(value=False)

        for text, var in [
            ("Verify", self._verify_var),
            ("Dry-Run", self._dryrun_var),
            ("Non-Stop", self._nonstop_var),
        ]:
            cb = tk.Checkbutton(
                cb_frame, text=text, variable=var,
                bg=_BG_CARD, fg=_FG, selectcolor=_BG_INPUT,
                activebackground=_BG_CARD, activeforeground=_ACCENT,
                font=("Segoe UI", 10),
            )
            cb.pack(side="left", padx=(0, 12))

        # Speed
        speed_frame = tk.Frame(frame, bg=_BG_CARD)
        speed_frame.pack(side="left", padx=(8, 0))

        _make_label(speed_frame, text="Speed:").pack(anchor="w")
        self._speed_var = tk.StringVar(value="full")
        speed_combo = ttk.Combobox(
            speed_frame, textvariable=self._speed_var, state="readonly",
            values=["full", "autoslow", "75", "50", "25"], width=10,
        )
        speed_combo.pack()

    def _on_mode_change(self) -> None:
        if self._mode_var.get() == "move":
            self._verify_var.set(True)
        # Don't force-uncheck when switching back to copy

    # -- filters ------------------------------------------------------------

    def _build_filter_section(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=_BG_CARD)
        frame.pack(fill="x")

        # Include
        inc_frame = tk.Frame(frame, bg=_BG_CARD)
        inc_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        _make_label(inc_frame, text="Include:").pack(anchor="w")
        self._include_entry = _make_entry(inc_frame)
        self._include_entry.pack(fill="x", ipady=3)

        # Exclude
        exc_frame = tk.Frame(frame, bg=_BG_CARD)
        exc_frame.pack(side="left", fill="x", expand=True)
        _make_label(exc_frame, text="Exclude:").pack(anchor="w")
        self._exclude_entry = _make_entry(exc_frame)
        self._exclude_entry.pack(fill="x", ipady=3)

    # -- action buttons -----------------------------------------------------

    def _build_action_buttons(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=_BG_CARD, pady=8)
        frame.pack(fill="x")

        self._exec_btn = HoverButton(
            frame, text="  ▶  Execute  ",
            bg="#45475a", hover_bg=_GREEN, hover_fg="#11111b",
            command=self._on_execute,
        )
        self._exec_btn.pack(side="left", padx=(0, 8), ipady=4)

        self._preview_btn = HoverButton(
            frame, text="  📋  Dry-Run Preview  ",
            bg="#45475a", hover_bg=_YELLOW, hover_fg="#11111b",
            command=self._on_preview,
        )
        self._preview_btn.pack(side="left", padx=(0, 8), ipady=4)

        self._cancel_btn = HoverButton(
            frame, text="  ⏹  Cancel  ",
            bg="#45475a", hover_bg=_RED, hover_fg="#11111b",
            command=self._on_cancel, state="disabled",
        )
        self._cancel_btn.pack(side="left", ipady=4)

        # Status label (right side)
        self._status_label = tk.Label(
            frame, text="Ready", bg=_BG_CARD, fg=_FG_DIM,
            font=("Segoe UI", 10, "italic"),
        )
        self._status_label.pack(side="right")

    # -- output area --------------------------------------------------------

    def _build_output_section(self, parent: tk.Frame) -> None:
        frame = tk.Frame(parent, bg=_BG_CARD)
        frame.pack(fill="both", expand=True, pady=(0, 4))

        header_row = tk.Frame(frame, bg=_BG_CARD)
        header_row.pack(fill="x")
        _make_label(header_row, text="Output / Log:").pack(side="left")

        HoverButton(
            header_row, text=" Clear ",
            bg=_BG_INPUT, hover_bg=_RED, command=self._clear_output,
        ).pack(side="right")

        self._output_text = scrolledtext.ScrolledText(
            frame, bg="#181825", fg=_FG, insertbackground=_FG,
            font=("Consolas", 9), relief="flat", state="disabled",
            highlightthickness=1, highlightbackground=_BORDER,
            wrap="word",
        )
        self._output_text.pack(fill="both", expand=True, pady=(4, 0))

        # Tag configuration for colored output
        self._output_text.tag_configure("info", foreground=_FG)
        self._output_text.tag_configure("success", foreground=_GREEN)
        self._output_text.tag_configure("error", foreground=_RED)
        self._output_text.tag_configure("warning", foreground=_YELLOW)
        self._output_text.tag_configure("accent", foreground=_ACCENT)
        self._output_text.tag_configure("add", foreground=_GREEN)
        self._output_text.tag_configure("remove", foreground=_RED)

    # -- output helpers -----------------------------------------------------

    def _append_output(self, text: str, tag: str = "info") -> None:
        """Thread-safe append to the output text widget."""
        def _do():
            self._output_text.config(state="normal")
            self._output_text.insert(tk.END, text + "\n", tag)
            self._output_text.see(tk.END)
            self._output_text.config(state="disabled")
        self.root.after(0, _do)

    def _clear_output(self) -> None:
        self._output_text.config(state="normal")
        self._output_text.delete("1.0", tk.END)
        self._output_text.config(state="disabled")

    def _set_status(self, text: str, color: str = _FG_DIM) -> None:
        def _do():
            self._status_label.config(text=text, fg=color)
        self.root.after(0, _do)

    # -- gather config from UI ---------------------------------------------

    def _gather_config(self, force_dry_run: bool = False) -> FastCopyConfig | None:
        """Build a FastCopyConfig from the current UI state."""
        sources = list(self._source_listbox.get(0, tk.END))
        destination = self._dest_entry.get().strip()

        if not sources:
            messagebox.showwarning("Missing Source", "Add at least one source path.")
            return None
        if not destination:
            messagebox.showwarning("Missing Destination", "Specify a destination path.")
            return None

        return FastCopyConfig(
            sources=sources,
            destination=destination,
            mode=self._mode_var.get(),
            dry_run=force_dry_run or self._dryrun_var.get(),
            verify=self._verify_var.get(),
            nonstop=self._nonstop_var.get(),
            include=self._include_entry.get().strip(),
            exclude=self._exclude_entry.get().strip(),
            speed=self._speed_var.get(),
        )

    # -- button handlers ----------------------------------------------------

    def _set_running(self, running: bool) -> None:
        self._running = running
        state = "disabled" if running else "normal"
        cancel_state = "normal" if running else "disabled"
        self._exec_btn.config(state=state)
        self._preview_btn.config(state=state)
        self._cancel_btn.config(state=cancel_state)

    def _on_execute(self) -> None:
        config = self._gather_config()
        if config is None:
            return

        # Move mode confirmation
        if config.mode == "move" and not config.dry_run:
            if not messagebox.askyesno(
                "Confirm Move",
                "Move mode will DELETE source files after successful copy.\n\n"
                f"Verify: {'ON' if config.effective_verify() else 'OFF'}\n\n"
                "Continue?",
            ):
                return

        self._run_fastcopy(config)

    def _on_preview(self) -> None:
        config = self._gather_config(force_dry_run=True)
        if config is None:
            return
        self._run_fastcopy(config)

    def _on_cancel(self) -> None:
        # Signal the thread — we can't kill the subprocess cleanly from here
        # but we can set a flag
        self._running = False
        self._set_status("Cancelling...", _YELLOW)

    def _run_fastcopy(self, config: FastCopyConfig) -> None:
        """Run FastCopy in a background thread."""
        self._clear_output()
        self._set_running(True)

        action = "DRY-RUN PREVIEW" if config.dry_run else config.mode.upper()
        self._set_status(f"Running: {action}...", _ACCENT)
        self._append_output(f"{'='*56}", "accent")
        self._append_output(f"  FastCopy Tool — {action}", "accent")
        self._append_output(f"{'='*56}", "accent")

        try:
            runner = FastCopyRunner(config)
        except FileNotFoundError as exc:
            self._append_output(f"ERROR: {exc}", "error")
            self._set_running(False)
            self._set_status("Error", _RED)
            return

        self._append_output(f"Command: {runner.build_command_string()}\n", "info")

        def _output_callback(line: str) -> None:
            if not self._running:
                return
            # Color listing lines
            tag = "info"
            stripped = line.lstrip()
            if stripped.startswith("+"):
                tag = "add"
            elif stripped.startswith("-"):
                tag = "remove"
            elif "error" in line.lower() or "ERROR" in line:
                tag = "error"
            self._append_output(line, tag)

        def _worker() -> None:
            result: CopyResult = runner.run(on_output=_output_callback)

            # Summary
            if result.success:
                self._append_output(
                    f"\n✅ Completed successfully ({result.elapsed_seconds:.1f}s)",
                    "success",
                )
                self._set_status("Completed", _GREEN)
            else:
                self._append_output(
                    f"\n❌ Failed (exit code {result.return_code}, "
                    f"{result.elapsed_seconds:.1f}s)",
                    "error",
                )
                self._set_status("Failed", _RED)

            self.root.after(0, lambda: self._set_running(False))

        self._thread = threading.Thread(target=_worker, daemon=True)
        self._thread.start()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def launch_gui() -> None:
    """Create and run the GUI application."""
    root = tk.Tk()

    # Style ttk widgets to match the dark theme
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TCombobox",
                     fieldbackground=_BG_INPUT, background=_BTN_BG,
                     foreground=_FG, bordercolor=_BORDER,
                     arrowcolor=_FG)
    style.configure("TSeparator", background=_BORDER)

    _app = FastCopyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
