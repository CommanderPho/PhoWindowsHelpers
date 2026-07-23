"""
FastCopy Wrapper — Core Engine
==============================
Builds FastCopy command lines and manages subprocess execution.
Shared by both the CLI and GUI interfaces.
"""

from __future__ import annotations

import ctypes
import fnmatch
import logging
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------
DEFAULT_FASTCOPY_EXE = Path(r"C:\Users\pho\bin\FastCopy\FastCopy.exe")


def find_fastcopy_exe(override: Optional[str] = None) -> Path:
    """Resolve FastCopy.exe location.

    Priority:
    1. Explicit *override* argument
    2. FASTCOPY_HOME environment variable
    3. DEFAULT_FASTCOPY_EXE constant
    """
    if override:
        p = Path(override)
        if p.is_file():
            return p
        raise FileNotFoundError(f"FastCopy executable not found at: {p}")

    env_home = os.environ.get("FASTCOPY_HOME")
    if env_home:
        p = Path(env_home) / "FastCopy.exe"
        if p.is_file():
            return p

    if DEFAULT_FASTCOPY_EXE.is_file():
        return DEFAULT_FASTCOPY_EXE

    raise FileNotFoundError(
        f"FastCopy.exe not found. Checked:\n"
        f"  - FASTCOPY_HOME env var\n"
        f"  - {DEFAULT_FASTCOPY_EXE}\n"
        f"Set FASTCOPY_HOME or pass --fastcopy <path>."
    )


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
@dataclass
class FastCopyConfig:
    """All parameters needed to build a FastCopy command."""

    sources: List[str] = field(default_factory=list)
    destination: str = ""

    # Operation mode: "copy", "move", or "symlink"
    #   symlink = copy to dest, delete source, create symlink at source → dest
    mode: str = "copy"

    # Flags
    dry_run: bool = False
    verify: bool = False
    no_verify: bool = False  # explicit opt-out of auto-verify in move/symlink
    nonstop: bool = False

    # Filters
    include: str = ""
    exclude: str = ""

    # Speed: full | autoslow | 75 | 50 | 25
    speed: str = "full"

    # Logging
    log_path: str = ""

    # FastCopy executable override
    fastcopy_exe: str = ""

    @property
    def is_destructive(self) -> bool:
        """True if this mode deletes source files."""
        return self.mode in ("move", "symlink")

    def effective_verify(self) -> bool:
        """Verify is auto-enabled for move/symlink unless explicitly disabled."""
        if self.no_verify:
            return False
        if self.is_destructive:
            return True
        return self.verify

    def effective_error_stop(self) -> bool:
        """In destructive modes we always stop on error for safety."""
        if self.is_destructive:
            return True
        return not self.nonstop


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
@dataclass
class SymlinkResult:
    """Outcome of a single source → symlink replacement."""

    source: str
    target: str  # the destination the symlink points to
    success: bool = False
    message: str = ""


@dataclass
class CopyResult:
    """Outcome of a FastCopy operation."""

    return_code: int = -1
    success: bool = False
    elapsed_seconds: float = 0.0
    output_lines: List[str] = field(default_factory=list)
    command: str = ""
    symlink_results: List[SymlinkResult] = field(default_factory=list)

    @property
    def output_text(self) -> str:
        return "\n".join(self.output_lines)


# ---------------------------------------------------------------------------
# Speed mapping
# ---------------------------------------------------------------------------
_SPEED_MAP = {
    "full": "full",
    "autoslow": "autoslow",
    "75": "75%",
    "50": "50%",
    "25": "25%",
}


def _human_size(nbytes: int) -> str:
    """Format a byte count as a human-readable string (e.g. 1.2 MB)."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}" if unit != "B" else f"{nbytes} {unit}"
        nbytes /= 1024  # type: ignore[assignment]
    return f"{nbytes:.1f} PB"


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
class FastCopyRunner:
    """Builds and executes a FastCopy command from a :class:`FastCopyConfig`."""

    def __init__(self, config: FastCopyConfig) -> None:
        self.config = config
        self._exe = find_fastcopy_exe(config.fastcopy_exe or None)

    # -- command building ---------------------------------------------------

    def build_command(self) -> List[str]:
        """Translate config into a FastCopy CLI argument list.

        This builds the command for *real* operations only.
        Dry-run is handled separately by :meth:`run_dry_run`
        since FastCopy has no CLI dry-run flag.
        """
        cfg = self.config
        cmd: List[str] = [str(self._exe)]

        # --- mode ---
        if cfg.mode == "move":
            cmd.append("/cmd=move")
        elif cfg.mode == "symlink":
            # Symlink mode uses copy (diff), then we handle
            # delete + symlink creation as a post-process step.
            cmd.append("/cmd=diff")
        else:
            cmd.append("/cmd=diff")

        # --- verify ---
        if cfg.effective_verify():
            cmd.append("/verify")

        # --- error handling ---
        if cfg.effective_error_stop():
            cmd.append("/error_stop")
        else:
            cmd.append("/error_stop=FALSE")

        # --- speed ---
        speed_val = _SPEED_MAP.get(cfg.speed, "full")
        cmd.append(f"/speed={speed_val}")

        # --- filters ---
        if cfg.include:
            cmd.append(f'/include="{cfg.include}"')
        if cfg.exclude:
            cmd.append(f'/exclude="{cfg.exclude}"')

        # --- logging ---
        cmd.append("/log")
        cmd.append("/filelog")
        if cfg.log_path:
            cmd.append(f'/logfile="{cfg.log_path}"')

        # --- auto close (non-GUI) ---
        cmd.append("/auto_close")

        # --- sources ---
        for src in cfg.sources:
            cmd.append(f'"{src}"')

        # --- destination ---
        if cfg.destination:
            dest = cfg.destination
            # Ensure trailing backslash so FastCopy copies *into* dest
            if not dest.endswith("\\") and not dest.endswith("/"):
                dest += "\\"
            cmd.append(f'/to="{dest}"')

        return cmd

    def build_command_string(self) -> str:
        """Return the command as a single string for display / shell execution."""
        return " ".join(self.build_command())

    # -- execution ----------------------------------------------------------

    def run(
        self,
        on_output: Optional[Callable[[str], None]] = None,
    ) -> CopyResult:
        """Execute the FastCopy command.

        Parameters
        ----------
        on_output : callable, optional
            Called with each line of stdout/stderr as it arrives.
            Useful for streaming output to a GUI text widget.

        Returns
        -------
        CopyResult
        """
        cmd_str = self.build_command_string()
        logger.info("Executing: %s", cmd_str)

        result = CopyResult(command=cmd_str)
        start = time.monotonic()

        try:
            proc = subprocess.Popen(
                cmd_str,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True,  # needed for quoted paths on Windows
                encoding="utf-8",
                errors="replace",
            )

            assert proc.stdout is not None
            for line in proc.stdout:
                line = line.rstrip("\n\r")
                result.output_lines.append(line)
                if on_output:
                    on_output(line)

            proc.wait()
            result.return_code = proc.returncode
            result.success = proc.returncode == 0

        except FileNotFoundError:
            msg = f"FastCopy executable not found: {self._exe}"
            logger.error(msg)
            result.output_lines.append(f"ERROR: {msg}")
        except Exception as exc:
            msg = f"Unexpected error: {exc}"
            logger.error(msg)
            result.output_lines.append(f"ERROR: {msg}")

        result.elapsed_seconds = time.monotonic() - start
        return result

    def run_dry_run(
        self,
        on_output: Optional[Callable[[str], None]] = None,
    ) -> CopyResult:
        """Scan source files and show what would be copied/moved.

        FastCopy has no CLI dry-run flag (``/listing`` is GUI-only),
        so we perform a pure-Python directory walk with the same
        include/exclude filter logic and report the results.
        """
        cfg = self.config
        result = CopyResult(command=self.build_command_string())
        start = time.monotonic()

        def _emit(line: str, tag: str = "") -> None:
            result.output_lines.append(line)
            if on_output:
                on_output(line)

        # Parse semicolon-separated filter patterns
        inc_patterns = [
            p.strip() for p in cfg.include.split(";") if p.strip()
        ] if cfg.include else []
        exc_patterns = [
            p.strip() for p in cfg.exclude.split(";") if p.strip()
        ] if cfg.exclude else []

        def _matches_any(name: str, patterns: List[str]) -> bool:
            return any(fnmatch.fnmatch(name.lower(), p.lower()) for p in patterns)

        mode_label = {
            "copy": "COPY",
            "move": "MOVE (delete source after copy)",
            "symlink": "MOVE + SYMLINK (copy, delete source, create symlink)",
        }.get(cfg.mode, cfg.mode.upper())

        _emit(f"Mode: {mode_label}")
        _emit(f"Destination: {cfg.destination}")
        if inc_patterns:
            _emit(f"Include filter: {cfg.include}")
        if exc_patterns:
            _emit(f"Exclude filter: {cfg.exclude}")
        _emit("")

        total_files = 0
        total_dirs = 0
        total_bytes = 0

        for src in cfg.sources:
            src_path = Path(src.strip().strip('"'))
            _emit(f"--- Source: {src_path} ---")

            if not src_path.exists():
                _emit(f"  WARNING: path does not exist")
                continue

            if src_path.is_file():
                # Single file
                name = src_path.name
                if inc_patterns and not _matches_any(name, inc_patterns):
                    _emit(f"  SKIP (include filter): {name}")
                    continue
                if exc_patterns and _matches_any(name, exc_patterns):
                    _emit(f"  SKIP (exclude filter): {name}")
                    continue
                size = src_path.stat().st_size
                total_files += 1
                total_bytes += size
                _emit(f"  + {name}  ({_human_size(size)})")
            else:
                # Directory tree
                try:
                    for root_dir, dirs, files in os.walk(src_path):
                        rel_root = Path(root_dir).relative_to(src_path)

                        # Filter directories (exclude only)
                        if exc_patterns:
                            dirs[:] = [
                                d for d in dirs
                                if not _matches_any(d, exc_patterns)
                            ]

                        for fname in sorted(files):
                            if inc_patterns and not _matches_any(fname, inc_patterns):
                                continue
                            if exc_patterns and _matches_any(fname, exc_patterns):
                                continue

                            fpath = Path(root_dir) / fname
                            try:
                                size = fpath.stat().st_size
                            except OSError:
                                size = 0

                            total_files += 1
                            total_bytes += size
                            display = str(rel_root / fname) if str(rel_root) != "." else fname
                            _emit(f"  + {display}  ({_human_size(size)})")

                        # Count dirs for summary
                        total_dirs += len(dirs)

                except PermissionError as exc:
                    _emit(f"  ERROR: {exc}")

        _emit("")
        _emit(f"Summary: {total_files} file(s) in {total_dirs} dir(s), "
              f"{_human_size(total_bytes)} total")
        _emit("")
        _emit("Would run:")
        _emit(f"  {result.command}")

        result.success = True
        result.return_code = 0
        result.elapsed_seconds = time.monotonic() - start
        return result

    # -- symlink post-processing --------------------------------------------

    def _resolve_symlink_target(self, source: str) -> Path:
        """Determine the destination path that *source* was copied into.

        FastCopy copies ``source`` into ``destination\\``, preserving
        the leaf name.  E.g. source ``C:\\Data\\Photos`` copied to
        ``D:\\Backup\\`` ends up at ``D:\\Backup\\Photos``.
        """
        src_path = Path(source)
        dest_dir = Path(self.config.destination)
        return dest_dir / src_path.name

    def run_with_symlink(
        self,
        on_output: Optional[Callable[[str], None]] = None,
    ) -> CopyResult:
        """Copy files, then replace each source with a symlink to the destination.

        Workflow (mirrors FastCopy-Symlink.ps1):
        1. Copy via FastCopy (``/cmd=diff`` + ``/verify``)
        2. For each source:
           a. Verify the destination exists
           b. Delete the source
           c. Create a symlink:  source → destination

        If the copy fails, **no** sources are deleted.
        If any individual symlink step fails, it is logged but
        remaining sources are still attempted.

        Parameters
        ----------
        on_output : callable, optional
            Streaming output callback (same as :meth:`run`).

        Returns
        -------
        CopyResult
            Includes per-source :class:`SymlinkResult` entries.
        """
        # Phase 1: copy
        result = self.run(on_output=on_output)

        if not result.success:
            msg = "Copy phase failed — skipping symlink creation."
            logger.warning(msg)
            result.output_lines.append(f"\nWARNING: {msg}")
            if on_output:
                on_output(f"\nWARNING: {msg}")
            return result

        if on_output:
            on_output("")
            on_output("--- Symlink Phase ---")

        # Phase 2: for each source, delete & symlink
        all_ok = True
        for src in self.config.sources:
            src_path = Path(src.strip().strip('"'))
            target_path = self._resolve_symlink_target(str(src_path))

            sr = SymlinkResult(source=str(src_path), target=str(target_path))

            # 2a. Verify destination exists
            if not target_path.exists():
                sr.message = f"Destination not found: {target_path} — skipping."
                sr.success = False
                all_ok = False
                logger.warning(sr.message)
                result.output_lines.append(f"WARNING: {sr.message}")
                if on_output:
                    on_output(f"⚠ {sr.message}")
                result.symlink_results.append(sr)
                continue

            # 2b. Delete source
            try:
                if src_path.is_dir():
                    shutil.rmtree(src_path)
                elif src_path.exists():
                    src_path.unlink()
                else:
                    # Source already gone (FastCopy may have moved it?)
                    pass
            except OSError as exc:
                sr.message = f"Failed to delete source: {exc}"
                sr.success = False
                all_ok = False
                logger.error(sr.message)
                result.output_lines.append(f"ERROR: {sr.message}")
                if on_output:
                    on_output(f"❌ {sr.message}")
                result.symlink_results.append(sr)
                continue

            # 2c. Create symlink
            try:
                is_dir = target_path.is_dir()
                src_path.symlink_to(target_path, target_is_directory=is_dir)
                sr.success = True
                sr.message = f"Symlink created: {src_path} → {target_path}"
                logger.info(sr.message)
                result.output_lines.append(sr.message)
                if on_output:
                    on_output(f"🔗 {sr.message}")
            except OSError as exc:
                sr.message = f"Failed to create symlink: {exc}"
                sr.success = False
                all_ok = False
                logger.error(sr.message)
                result.output_lines.append(f"ERROR: {sr.message}")
                if on_output:
                    on_output(f"❌ {sr.message}")

            result.symlink_results.append(sr)

        if on_output:
            on_output("--- End Symlink Phase ---")

        result.success = result.success and all_ok
        return result


# ---------------------------------------------------------------------------
# Utility: admin check
# ---------------------------------------------------------------------------
def is_admin() -> bool:
    """Return True if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore[union-attr]
    except Exception:
        return False
