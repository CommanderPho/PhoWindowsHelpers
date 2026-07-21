"""
FastCopy Wrapper — Core Engine
==============================
Builds FastCopy command lines and manages subprocess execution.
Shared by both the CLI and GUI interfaces.
"""

from __future__ import annotations

import logging
import os
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

    # Operation mode
    mode: str = "copy"  # "copy" or "move"

    # Flags
    dry_run: bool = False
    verify: bool = False
    no_verify: bool = False  # explicit opt-out of auto-verify in move
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

    def effective_verify(self) -> bool:
        """Verify is auto-enabled for move unless explicitly disabled."""
        if self.no_verify:
            return False
        if self.mode == "move":
            return True
        return self.verify

    def effective_error_stop(self) -> bool:
        """In move mode we always stop on error for safety."""
        if self.mode == "move":
            return True
        return not self.nonstop


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
@dataclass
class CopyResult:
    """Outcome of a FastCopy operation."""

    return_code: int = -1
    success: bool = False
    elapsed_seconds: float = 0.0
    output_lines: List[str] = field(default_factory=list)
    command: str = ""

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
        """Translate config into a FastCopy CLI argument list."""
        cfg = self.config
        cmd: List[str] = [str(self._exe)]

        # --- mode ---
        if cfg.dry_run:
            # /listing performs a real scan but writes nothing
            cmd.append("/listing")
        else:
            if cfg.mode == "move":
                cmd.append("/cmd=move")
            else:
                cmd.append("/cmd=diff")

        # --- verify ---
        if not cfg.dry_run and cfg.effective_verify():
            cmd.append("/verify")

        # --- error handling ---
        if not cfg.dry_run:
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
        """Convenience: force dry-run regardless of config and execute."""
        original = self.config.dry_run
        self.config.dry_run = True
        try:
            return self.run(on_output=on_output)
        finally:
            self.config.dry_run = original
