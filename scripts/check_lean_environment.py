#!/usr/bin/env python3
"""Fail-closed preflight for the repository's pinned Lean environment.

The check deliberately runs Lean and Lake through ``elan run <toolchain>`` so
that an unrelated default toolchain cannot make a validation receipt pass.
It emits one JSON document on both success and failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "awesome-theorems-lean-preflight/1.0"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_ELAN_VERSION = "4.2.3"
EXPECTED_LEAN_VERSION = "4.29.0"
EXPECTED_LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_LAKE_VERSION = "5.0.0-src+98dc76e"
EXPECTED_ROOT_PINS = {
    "mathlib": "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    "flt-regular": "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
}
SHA256 = re.compile(r"^[0-9a-f]{40}$")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path, *, timeout_seconds: int = 30) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "argv": argv,
            "exit_code": None,
            "stdout": (exc.stdout or "").strip(),
            "stderr": (exc.stderr or "").strip(),
            "timed_out": True,
            "timeout_seconds": timeout_seconds,
        }
    except OSError as exc:
        return {
            "argv": argv,
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc),
            "timed_out": False,
            "timeout_seconds": timeout_seconds,
        }
    return {
        "argv": argv,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "timed_out": False,
        "timeout_seconds": timeout_seconds,
    }


def package_dir_name(manifest_name: str) -> str:
    return manifest_name.removeprefix("«").removesuffix("»")


def find_elan(explicit: str | None) -> tuple[Path | None, str]:
    if explicit:
        return Path(explicit).expanduser().resolve(), "--elan"
    elan_home = os.environ.get("ELAN_HOME")
    if elan_home:
        return Path(elan_home).expanduser().resolve() / "bin" / "elan", "ELAN_HOME"
    candidate = shutil.which("elan")
    if candidate:
        return Path(candidate).resolve(), "PATH"
    return None, "unresolved"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lean-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "Formalizations" / "Lean",
        help="Lean project root (defaults to this repository's tracked project)",
    )
    parser.add_argument(
        "--elan",
        help="exact elan executable; otherwise ELAN_HOME/bin/elan, then PATH",
    )
    args = parser.parse_args()

    lean_root = args.lean_root.expanduser().resolve()
    toolchain_path = lean_root / "lean-toolchain"
    manifest_path = lean_root / "lake-manifest.json"
    diagnostics: list[dict[str, str]] = []
    commands: dict[str, dict[str, Any]] = {}
    dependencies: list[dict[str, Any]] = []

    def issue(code: str, message: str, action: str) -> None:
        diagnostics.append({"code": code, "message": message, "action": action})

    toolchain: str | None = None
    manifest: dict[str, Any] | None = None
    if not toolchain_path.is_file():
        issue(
            "missing_toolchain_file",
            f"missing {toolchain_path}",
            "restore the tracked Formalizations/Lean/lean-toolchain file",
        )
    else:
        toolchain = toolchain_path.read_text(encoding="utf-8").strip()
        if toolchain != EXPECTED_TOOLCHAIN:
            issue(
                "toolchain_pin_mismatch",
                f"tracked toolchain is {toolchain!r}, expected {EXPECTED_TOOLCHAIN!r}",
                "review the pin change; do not validate THM-M-0387 against a different toolchain",
            )

    if not manifest_path.is_file():
        issue(
            "missing_lake_manifest",
            f"missing {manifest_path}",
            "materialize the committed lake-manifest.json without regenerating its pins",
        )
    else:
        try:
            loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict) or not isinstance(loaded.get("packages"), list):
                raise ValueError("top-level packages is not an array")
            manifest = loaded
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issue(
                "invalid_lake_manifest",
                f"cannot parse {manifest_path}: {exc}",
                "restore the committed manifest and rerun the preflight",
            )

    elan, elan_source = find_elan(args.elan)
    if elan is None or not elan.is_file() or not os.access(elan, os.X_OK):
        shown = str(elan) if elan is not None else "elan"
        issue(
            "missing_elan",
            f"official elan executable is unavailable at {shown} (resolution={elan_source})",
            "install elan 4.2.3 or set ELAN_HOME to its writable installation root",
        )
    else:
        commands["elan_version"] = run([str(elan), "--version"], lean_root)
        elan_output = commands["elan_version"]["stdout"]
        if commands["elan_version"]["exit_code"] != 0 or not elan_output.startswith(
            f"elan {EXPECTED_ELAN_VERSION} "
        ):
            issue(
                "elan_version_mismatch",
                f"observed elan version output is {elan_output!r}",
                f"install official elan {EXPECTED_ELAN_VERSION} and select it with ELAN_HOME or --elan",
            )

        if toolchain == EXPECTED_TOOLCHAIN:
            commands["lean_version"] = run(
                [str(elan), "run", toolchain, "lean", "--version"], lean_root
            )
            commands["lake_version"] = run(
                [str(elan), "run", toolchain, "lake", "--version"], lean_root
            )
            lean_output = commands["lean_version"]["stdout"]
            if (
                commands["lean_version"]["exit_code"] != 0
                or f"version {EXPECTED_LEAN_VERSION}," not in lean_output
                or f"commit {EXPECTED_LEAN_COMMIT}," not in lean_output
            ):
                issue(
                    "lean_version_mismatch",
                    f"observed Lean version output is {lean_output!r}",
                    f"run `elan toolchain install {EXPECTED_TOOLCHAIN}` and retry",
                )
            lake_output = commands["lake_version"]["stdout"]
            if (
                commands["lake_version"]["exit_code"] != 0
                or not lake_output.startswith(f"Lake version {EXPECTED_LAKE_VERSION} ")
                or f"Lean version {EXPECTED_LEAN_VERSION}" not in lake_output
            ):
                issue(
                    "lake_version_mismatch",
                    f"observed Lake version output is {lake_output!r}",
                    f"reinstall the exact {EXPECTED_TOOLCHAIN} toolchain and retry",
                )

    manifest_names: set[str] = set()
    if manifest is not None:
        for entry in manifest["packages"]:
            if not isinstance(entry, dict):
                issue(
                    "invalid_package_entry",
                    "lake-manifest.json contains a non-object package entry",
                    "restore the committed lake-manifest.json",
                )
                continue
            raw_name = entry.get("name")
            revision = entry.get("rev")
            package_type = entry.get("type")
            if not isinstance(raw_name, str) or not isinstance(revision, str):
                issue(
                    "invalid_package_entry",
                    f"manifest package entry lacks string name/rev: {entry!r}",
                    "restore the committed lake-manifest.json",
                )
                continue
            name = package_dir_name(raw_name)
            manifest_names.add(name)
            record: dict[str, Any] = {
                "name": name,
                "manifest_revision": revision,
                "type": package_type,
            }
            package_path = lean_root / ".lake" / "packages" / name
            record["path"] = str(package_path)
            if package_type != "git":
                record["observed_revision"] = None
                record["match"] = None
                dependencies.append(record)
                continue
            if not SHA256.fullmatch(revision):
                issue(
                    "invalid_package_revision",
                    f"{name} has a non-commit revision {revision!r}",
                    "restore or intentionally review the committed Lake lockfile",
                )
            if not package_path.is_dir():
                issue(
                    "missing_package",
                    f"manifest package {name} is absent at {package_path}",
                    "run `lake update` only if it preserves every committed revision, then fetch caches",
                )
                record["observed_revision"] = None
                record["match"] = False
                dependencies.append(record)
                continue
            observed = run(["git", "rev-parse", "HEAD"], package_path)
            record["observed_revision"] = observed["stdout"] or None
            record["match"] = observed["exit_code"] == 0 and observed["stdout"] == revision
            if not record["match"]:
                issue(
                    "package_revision_mismatch",
                    f"{name} is at {observed['stdout']!r}, expected {revision}",
                    "materialize the exact committed package revision; do not rewrite lake-manifest.json",
                )
            observed_tree = run(["git", "rev-parse", "HEAD^{tree}"], package_path)
            tracked_status = run(
                ["git", "status", "--porcelain=v1", "--untracked-files=no"], package_path
            )
            record["observed_tree"] = observed_tree["stdout"] or None
            record["tracked_tree_clean"] = (
                observed_tree["exit_code"] == 0
                and tracked_status["exit_code"] == 0
                and tracked_status["stdout"] == ""
            )
            if not record["tracked_tree_clean"]:
                issue(
                    "package_tracked_tree_dirty",
                    f"{name} has tracked changes or its commit tree cannot be resolved",
                    "restore the exact package commit without deleting ignored build/cache artifacts",
                )
            dependencies.append(record)

        for name, expected in EXPECTED_ROOT_PINS.items():
            matching = [row for row in dependencies if row["name"] == name]
            if len(matching) != 1 or matching[0]["manifest_revision"] != expected:
                issue(
                    "root_pin_mismatch",
                    f"root dependency {name} is not pinned exactly to {expected}",
                    "restore lakefile.lean and lake-manifest.json to the reviewed revisions",
                )

    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed" if not diagnostics else "failed",
        "lean_root": str(lean_root),
        "toolchain": {
            "tracked": toolchain,
            "expected": EXPECTED_TOOLCHAIN,
            "lean_version": EXPECTED_LEAN_VERSION,
            "lean_commit": EXPECTED_LEAN_COMMIT,
            "lake_version": EXPECTED_LAKE_VERSION,
        },
        "elan": {
            "path": str(elan) if elan is not None else None,
            "resolution": elan_source,
            "expected_version": EXPECTED_ELAN_VERSION,
        },
        "inputs": {
            "lean_toolchain_sha256": digest(toolchain_path) if toolchain_path.is_file() else None,
            "lake_manifest_sha256": digest(manifest_path) if manifest_path.is_file() else None,
        },
        "commands": commands,
        "dependencies": dependencies,
        "diagnostics": diagnostics,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not diagnostics else 1


if __name__ == "__main__":
    sys.exit(main())
