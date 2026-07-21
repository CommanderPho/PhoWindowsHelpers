"""
FastCopy Wrapper — CLI Interface
================================
Command-line interface built on argparse.

Usage examples::

    # Dry-run preview
    python -m tools.fastcopy_wrapper cli --dry-run "D:\\Photos" "E:\\Backup"

    # Move with verification (auto-enabled)
    python -m tools.fastcopy_wrapper cli --mode move "D:\\Downloads\\*.iso" "E:\\ISOs"

    # Copy multiple sources, exclude temp files
    python -m tools.fastcopy_wrapper cli --exclude "*.tmp;thumbs.db" "C:\\Src1" "C:\\Src2" "D:\\Dest"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .fastcopy_tool import CopyResult, FastCopyConfig, FastCopyRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fastcopy-tool",
        description="FastCopy Wrapper — fast file copy/move with dry-run and verification.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  %(prog)s --dry-run "D:\\Photos\\2024" "E:\\Backup\\Photos"\n'
            '  %(prog)s --mode move "D:\\Downloads\\*.iso" "E:\\ISOs"\n'
            '  %(prog)s --exclude "*.tmp;thumbs.db" "C:\\Src1" "C:\\Src2" "D:\\Dest"\n'
        ),
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="Source path(s) followed by the destination directory (last argument).",
    )

    parser.add_argument(
        "--mode",
        choices=["copy", "move"],
        default="copy",
        help="Operation mode (default: copy).",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be copied/moved without making changes.",
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify copied files with hash check (auto-enabled for move mode).",
    )

    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Disable verification even in move mode.",
    )

    parser.add_argument(
        "--include",
        default="",
        help='Include filter (e.g. "*.txt;*.jpg").',
    )

    parser.add_argument(
        "--exclude",
        default="",
        help='Exclude filter (e.g. "*.tmp;thumbs.db").',
    )

    parser.add_argument(
        "--log",
        default="",
        metavar="PATH",
        help="Path to write log file.",
    )

    parser.add_argument(
        "--speed",
        choices=["full", "autoslow", "75", "50", "25"],
        default="full",
        help="Speed control (default: full).",
    )

    parser.add_argument(
        "--nonstop",
        action="store_true",
        help="Continue on errors instead of stopping.",
    )

    parser.add_argument(
        "--fastcopy",
        default="",
        metavar="EXE_PATH",
        help="Path to FastCopy.exe (default: auto-detect).",
    )

    return parser


def _print_line(line: str) -> None:
    """Callback to print each output line as it arrives."""
    print(line, flush=True)


def run_cli(argv: list[str] | None = None) -> int:
    """Parse arguments and execute the FastCopy operation.

    Returns the process exit code (0 = success).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # Need at least 2 paths: source(s) + destination
    if len(args.paths) < 2:
        parser.error("Need at least one source and a destination path.")

    sources = args.paths[:-1]
    destination = args.paths[-1]

    config = FastCopyConfig(
        sources=sources,
        destination=destination,
        mode=args.mode,
        dry_run=args.dry_run,
        verify=args.verify,
        no_verify=args.no_verify,
        nonstop=args.nonstop,
        include=args.include,
        exclude=args.exclude,
        speed=args.speed,
        log_path=args.log,
        fastcopy_exe=args.fastcopy,
    )

    # -- header --
    action = "DRY-RUN PREVIEW" if config.dry_run else config.mode.upper()
    print(f"\n{'='*60}")
    print(f"  FastCopy Tool — {action}")
    print(f"{'='*60}")
    print(f"  Sources:     {', '.join(sources)}")
    print(f"  Destination: {destination}")
    print(f"  Mode:        {config.mode}")
    print(f"  Verify:      {config.effective_verify()}")
    print(f"  Error stop:  {config.effective_error_stop()}")
    if config.include:
        print(f"  Include:     {config.include}")
    if config.exclude:
        print(f"  Exclude:     {config.exclude}")
    print(f"{'='*60}\n")

    try:
        runner = FastCopyRunner(config)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # Show the command being run
    print(f"Command: {runner.build_command_string()}\n")

    # -- move-mode safety reminder --
    if config.mode == "move" and not config.dry_run:
        if config.effective_verify():
            print("NOTE: Verify is enabled for move mode. Source files will")
            print("      only be deleted after successful copy + verification.\n")
        else:
            print("WARNING: Verify is DISABLED for move mode (--no-verify).")
            print("         Source files will be deleted after copy WITHOUT")
            print("         hash verification.\n")

    # -- execute --
    print("--- Output ---")
    result: CopyResult = runner.run(on_output=_print_line)
    print("--- End ---\n")

    # -- summary --
    status = "SUCCESS" if result.success else "FAILED"
    print(f"Status:  {status} (exit code {result.return_code})")
    print(f"Elapsed: {result.elapsed_seconds:.1f}s")

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(run_cli())
