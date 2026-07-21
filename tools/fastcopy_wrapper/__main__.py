"""
FastCopy Wrapper — Entry Point
==============================
``python -m tools.fastcopy_wrapper``  → launches the GUI
``python -m tools.fastcopy_wrapper cli [OPTIONS] SRC... DEST``  → runs the CLI
``python -m tools.fastcopy_wrapper gui``  → launches the GUI explicitly
"""

from __future__ import annotations

import sys


def main() -> None:
    args = sys.argv[1:]

    # Explicit sub-command
    if args and args[0].lower() == "gui":
        from .gui import launch_gui
        launch_gui()
        return

    if args and args[0].lower() == "cli":
        from .cli import run_cli
        sys.exit(run_cli(args[1:]))

    # If no sub-command but arguments are given, assume CLI
    if args:
        from .cli import run_cli
        sys.exit(run_cli(args))

    # No arguments at all → launch GUI
    from .gui import launch_gui
    launch_gui()


if __name__ == "__main__":
    main()
