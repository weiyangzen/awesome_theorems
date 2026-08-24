#!/usr/bin/env python3
"""Fail-closed runner for Stage5 BOOT candidate validation commands.

This module deliberately has no unsandboxed fallback.  It copies every
declared repository input into a content-addressed snapshot and executes the
frozen command plan in a transient user service.  The snapshot is mounted
read-only, the live repository and home are hidden, temporary state is
private, Internet address families are denied, and systemd owns the complete
candidate cgroup so a timeout also removes detached descendants.

The bootstrap manager is expected to pin the returned manifest, command and
suite authorities in its signed receipts.  Producer tests are supplemental:
``run_suite`` first runs a module-owned isolation probe and validates its exact
semantic result before any candidate command is admitted.
"""

from __future__ import annotations

import base64
from collections.abc import Iterable, Mapping, Sequence
import ctypes
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import secrets
import shutil
import signal
import stat
import subprocess
import tempfile
import time
from typing import Any


class SandboxError(RuntimeError):
    """A closed validation or sandbox failure, optionally with closed evidence."""

    def __init__(self, message: str, *, evidence: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.evidence = dict(evidence) if evidence is not None else None


SNAPSHOT_SCHEMA = "awesome-theorems/stage5-boot-input-snapshot/1.0"
COMMAND_SCHEMA = "awesome-theorems/stage5-boot-command/1.0"
RESULT_SCHEMA = "awesome-theorems/stage5-boot-command-result/1.0"
SUITE_SCHEMA = "awesome-theorems/stage5-boot-command-suite/1.0"
SANDBOX_POLICY_SCHEMA = "awesome-theorems/stage5-boot-systemd-sandbox/1.0"
MANAGER_CONFORMANCE_ID = "stage5-boot-manager-conformance-v1"

SYSTEMD_RUN = Path("/usr/bin/systemd-run")
SYSTEMCTL = Path("/usr/bin/systemctl")
ENV = Path("/usr/bin/env")
PROBE_PYTHON = Path("/usr/bin/python3.12")

# Reviewed host-tool pins.  A distribution update must be accepted as a
# manager/module migration; learning a new digest at runtime is forbidden.
PINNED_HOST_TOOLS = {
    SYSTEMD_RUN.as_posix(): "dbc8b988a849d5c9d7ef2de7068a6f107021bc6c11e0d7864c73f373eef726a7",
    SYSTEMCTL.as_posix(): "e0d3d0e9444da1b2b58c792c3f5028b69f049b77d5ca17b3ec0d09f89117225b",
    ENV.as_posix(): "0aefff8f912fb75716c5d4de3b6acde93edbe8fa280fc8ee895c1226d3e373ef",
    PROBE_PYTHON.as_posix(): "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,95}$")
MAX_TIMEOUT_SECONDS = 900
MAX_OUTPUT_BYTES = 16 * 1024 * 1024
CONTROL_TIMEOUT_SECONDS = 10
TERMINATION_GRACE_SECONDS = 2.0

BASE_ENVIRONMENT = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PYTHONDONTWRITEBYTECODE": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_OPTIONAL_LOCKS": "0",
}


def _control_environment() -> dict[str, str]:
    """Return only the local user-manager transport needed by systemd clients.

    These values are consumed by ``systemd-run``/``systemctl`` themselves.
    They are deliberately not inherited by the candidate process; the service
    hides both buses and starts the candidate through ``env -i``.
    """

    runtime = f"/run/user/{os.geteuid()}"
    return {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "XDG_RUNTIME_DIR": runtime,
        "DBUS_SESSION_BUS_ADDRESS": f"unix:path={runtime}/bus",
    }

_MANIFEST_FIELDS = {
    "schema_version", "source_root", "entries", "tools",
    "entries_sha256", "tools_sha256", "authority_sha256",
}
_ENTRY_FIELDS = {"path", "kind", "mode", "size", "sha256"}
_TOOL_FIELDS = {"path", "mode", "size", "uid", "gid", "sha256"}
_COMMAND_FIELDS = {
    "schema_version", "command_id", "argv", "cwd", "shell", "stdin",
    "timeout_seconds", "max_output_bytes", "conformance_id",
    "snapshot_manifest_sha256", "tool_bindings_sha256",
    "sandbox_policy_sha256", "authority_sha256",
}
_CHILD_CONFIG_SCHEMA = "awesome-theorems/stage5-boot-landlock-child/1.0"
_CHILD_CONFIG_FIELDS = {
    "schema_version", "snapshot", "source_root", "private_root", "argv",
    "environment", "read_paths", "launcher_sha256", "authority_sha256",
}

# Linux UAPI values.  This runner is intentionally host-specific and refuses
# another architecture or an older Landlock ABI instead of silently weakening
# isolation.
_PR_SET_NO_NEW_PRIVS = 38
_LANDLOCK_CREATE_RULESET_VERSION = 1
_LANDLOCK_RULE_PATH_BENEATH = 1
_LANDLOCK_ACCESS_FS_EXECUTE = 1 << 0
_LANDLOCK_ACCESS_FS_WRITE_FILE = 1 << 1
_LANDLOCK_ACCESS_FS_READ_FILE = 1 << 2
_LANDLOCK_ACCESS_FS_READ_DIR = 1 << 3
_LANDLOCK_ACCESS_FS_REMOVE_DIR = 1 << 4
_LANDLOCK_ACCESS_FS_REMOVE_FILE = 1 << 5
_LANDLOCK_ACCESS_FS_MAKE_CHAR = 1 << 6
_LANDLOCK_ACCESS_FS_MAKE_DIR = 1 << 7
_LANDLOCK_ACCESS_FS_MAKE_REG = 1 << 8
_LANDLOCK_ACCESS_FS_MAKE_SOCK = 1 << 9
_LANDLOCK_ACCESS_FS_MAKE_FIFO = 1 << 10
_LANDLOCK_ACCESS_FS_MAKE_BLOCK = 1 << 11
_LANDLOCK_ACCESS_FS_MAKE_SYM = 1 << 12
_LANDLOCK_ACCESS_FS_REFER = 1 << 13
_LANDLOCK_ACCESS_FS_TRUNCATE = 1 << 14
_LANDLOCK_READ = (
    _LANDLOCK_ACCESS_FS_EXECUTE
    | _LANDLOCK_ACCESS_FS_READ_FILE
    | _LANDLOCK_ACCESS_FS_READ_DIR
)
_LANDLOCK_WRITE = (
    _LANDLOCK_ACCESS_FS_WRITE_FILE
    | _LANDLOCK_ACCESS_FS_REMOVE_DIR
    | _LANDLOCK_ACCESS_FS_REMOVE_FILE
    | _LANDLOCK_ACCESS_FS_MAKE_CHAR
    | _LANDLOCK_ACCESS_FS_MAKE_DIR
    | _LANDLOCK_ACCESS_FS_MAKE_REG
    | _LANDLOCK_ACCESS_FS_MAKE_SOCK
    | _LANDLOCK_ACCESS_FS_MAKE_FIFO
    | _LANDLOCK_ACCESS_FS_MAKE_BLOCK
    | _LANDLOCK_ACCESS_FS_MAKE_SYM
    | _LANDLOCK_ACCESS_FS_REFER
    | _LANDLOCK_ACCESS_FS_TRUNCATE
)


class _LandlockRulesetAttr(ctypes.Structure):
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


class _LandlockPathBeneathAttr(ctypes.Structure):
    _fields_ = [
        ("allowed_access", ctypes.c_uint64),
        ("parent_fd", ctypes.c_int32),
        ("reserved", ctypes.c_uint32),
    ]


def canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SandboxError("value is not canonical JSON") from exc


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result["authority_sha256"] = sha256_bytes(canonical_json(result))
    return result


def _verify_seal(value: Mapping[str, Any], label: str) -> None:
    authority = value.get("authority_sha256")
    unsigned = dict(value)
    unsigned.pop("authority_sha256", None)
    if (
        not isinstance(authority, str)
        or not SHA256_RE.fullmatch(authority)
        or sha256_bytes(canonical_json(unsigned)) != authority
    ):
        raise SandboxError(f"{label} authority seal mismatch")


def _safe_root(root: Path | str) -> Path:
    path = Path(root)
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise SandboxError("snapshot source root must be an absolute real directory")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise SandboxError("snapshot source root cannot be resolved") from exc
    if resolved != path:
        raise SandboxError("snapshot source root contains a symlink or alias")
    if path == Path("/"):
        raise SandboxError("filesystem root cannot be a snapshot source")
    return path


def _safe_relative(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        raise SandboxError(f"{label} is not a non-empty POSIX relative path")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or value != pure.as_posix()
        or value.startswith("./")
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise SandboxError(f"{label} is not canonical and repository-relative")
    return value


def _read_regular(path: Path, label: str) -> tuple[bytes, os.stat_result]:
    try:
        before = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise SandboxError(f"{label} is unavailable") from exc
    if not stat.S_ISREG(before.st_mode) or path.is_symlink():
        raise SandboxError(f"{label} is not a regular non-symlink file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise SandboxError(f"{label} cannot be opened safely") from exc
    try:
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
        ):
            raise SandboxError(f"{label} changed before open")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        identity_before = (
            opened.st_dev, opened.st_ino, opened.st_mode, opened.st_uid,
            opened.st_gid, opened.st_nlink, opened.st_size,
            opened.st_mtime_ns, opened.st_ctime_ns,
        )
        identity_after = (
            after.st_dev, after.st_ino, after.st_mode, after.st_uid,
            after.st_gid, after.st_nlink, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        )
        if identity_before != identity_after:
            raise SandboxError(f"{label} changed while reading")
        data = b"".join(chunks)
        if len(data) != after.st_size:
            raise SandboxError(f"{label} size changed while reading")
        return data, after
    finally:
        os.close(descriptor)


def _validate_absolute_tool(path_text: Any, expected_sha: Any, label: str) -> dict[str, Any]:
    if (
        not isinstance(path_text, str)
        or "\x00" in path_text
        or not Path(path_text).is_absolute()
        or not isinstance(expected_sha, str)
        or not SHA256_RE.fullmatch(expected_sha)
    ):
        raise SandboxError(f"{label} binding is malformed")
    path = Path(path_text)
    try:
        if path.resolve(strict=True) != path:
            raise SandboxError(f"{label} path is not canonical or contains a symlink")
    except OSError as exc:
        raise SandboxError(f"{label} path cannot be resolved") from exc
    data, observed = _read_regular(path, label)
    digest = sha256_bytes(data)
    if digest != expected_sha:
        raise SandboxError(f"{label} SHA-256 drift")
    mode = stat.S_IMODE(observed.st_mode)
    if not mode & 0o111 or mode & 0o022:
        raise SandboxError(f"{label} executable mode is unsafe")
    return {
        "path": path.as_posix(),
        "mode": mode,
        "size": observed.st_size,
        "uid": observed.st_uid,
        "gid": observed.st_gid,
        "sha256": digest,
    }


def _validate_host_tools() -> None:
    for path, digest in PINNED_HOST_TOOLS.items():
        binding = _validate_absolute_tool(path, digest, f"pinned host tool {path}")
        if binding["uid"] != 0 or binding["gid"] != 0:
            raise SandboxError(f"pinned host tool {path} is not root-owned")


def _walk_declared(root: Path, relatives: Iterable[str]) -> list[dict[str, Any]]:
    requested = sorted({_safe_relative(value, "snapshot input") for value in relatives})
    if not requested:
        raise SandboxError("snapshot input set is empty")
    records: dict[str, dict[str, Any]] = {}
    for relative in requested:
        path = root / relative
        try:
            if path.resolve(strict=True) != path:
                raise SandboxError(f"snapshot input {relative} contains a symlink")
        except OSError as exc:
            raise SandboxError(f"snapshot input {relative} is unavailable") from exc
        candidates = [path]
        if path.is_dir():
            candidates.extend(sorted(path.rglob("*")))
        for candidate in candidates:
            child_relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink():
                raise SandboxError(f"snapshot input {child_relative} is a symlink")
            observed = candidate.stat(follow_symlinks=False)
            mode = stat.S_IMODE(observed.st_mode)
            if stat.S_ISDIR(observed.st_mode):
                row = {
                    "path": child_relative, "kind": "directory", "mode": mode,
                    "size": None, "sha256": None,
                }
            elif stat.S_ISREG(observed.st_mode):
                raw, stable = _read_regular(candidate, f"snapshot input {child_relative}")
                row = {
                    "path": child_relative, "kind": "file",
                    "mode": stat.S_IMODE(stable.st_mode), "size": stable.st_size,
                    "sha256": sha256_bytes(raw),
                }
            else:
                raise SandboxError(f"snapshot input {child_relative} has a special type")
            previous = records.get(child_relative)
            if previous is not None and previous != row:
                raise SandboxError(f"snapshot input {child_relative} is inconsistent")
            records[child_relative] = row
    return [records[key] for key in sorted(records)]


def seal_snapshot_manifest(
    root: Path | str,
    relative_paths: Iterable[str],
    *,
    executable_paths: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Seal the exact repository files and already-reviewed executable pins."""

    source_root = _safe_root(root)
    entries = _walk_declared(source_root, relative_paths)
    tools = [
        _validate_absolute_tool(path, digest, f"candidate tool {path}")
        for path, digest in sorted((executable_paths or {}).items())
    ]
    if not tools:
        raise SandboxError("snapshot manifest has no pinned candidate executable")
    return _seal({
        "schema_version": SNAPSHOT_SCHEMA,
        "source_root": source_root.as_posix(),
        "entries": entries,
        "tools": tools,
        "entries_sha256": sha256_bytes(canonical_json(entries)),
        "tools_sha256": sha256_bytes(canonical_json(tools)),
    })


def _validate_manifest(value: Any, *, expected_root: Path | None = None) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _MANIFEST_FIELDS:
        raise SandboxError("snapshot manifest fields are not closed")
    _verify_seal(value, "snapshot manifest")
    if value.get("schema_version") != SNAPSHOT_SCHEMA:
        raise SandboxError("snapshot manifest schema differs")
    root = _safe_root(value.get("source_root"))
    if expected_root is not None and root != expected_root:
        raise SandboxError("snapshot manifest source root differs")
    entries = value.get("entries")
    tools = value.get("tools")
    if not isinstance(entries, list) or not entries or not isinstance(tools, list) or not tools:
        raise SandboxError("snapshot manifest entries/tools are empty or malformed")
    paths: list[str] = []
    for row in entries:
        if not isinstance(row, dict) or set(row) != _ENTRY_FIELDS:
            raise SandboxError("snapshot entry fields are not closed")
        relative = _safe_relative(row.get("path"), "snapshot entry")
        paths.append(relative)
        mode = row.get("mode")
        if not isinstance(mode, int) or isinstance(mode, bool) or not 0 <= mode <= 0o7777:
            raise SandboxError("snapshot entry mode is malformed")
        if row.get("kind") == "directory":
            if row.get("size") is not None or row.get("sha256") is not None:
                raise SandboxError("snapshot directory binding is malformed")
        elif row.get("kind") == "file":
            if (
                not isinstance(row.get("size"), int)
                or isinstance(row.get("size"), bool)
                or row["size"] < 0
                or not isinstance(row.get("sha256"), str)
                or not SHA256_RE.fullmatch(row["sha256"])
            ):
                raise SandboxError("snapshot file binding is malformed")
        else:
            raise SandboxError("snapshot entry kind is unsupported")
    if paths != sorted(set(paths)):
        raise SandboxError("snapshot entry order/identity is not canonical")
    observed_tools: list[dict[str, Any]] = []
    tool_paths: list[str] = []
    for row in tools:
        if not isinstance(row, dict) or set(row) != _TOOL_FIELDS:
            raise SandboxError("snapshot tool fields are not closed")
        observed = _validate_absolute_tool(
            row.get("path"), row.get("sha256"), f"candidate tool {row.get('path')}",
        )
        if observed != row:
            raise SandboxError(f"candidate tool metadata drift: {row.get('path')}")
        observed_tools.append(observed)
        tool_paths.append(observed["path"])
    if tool_paths != sorted(set(tool_paths)):
        raise SandboxError("snapshot tool order/identity is not canonical")
    if (
        value.get("entries_sha256") != sha256_bytes(canonical_json(entries))
        or value.get("tools_sha256") != sha256_bytes(canonical_json(observed_tools))
    ):
        raise SandboxError("snapshot manifest aggregate digest mismatch")
    return value


def sandbox_policy() -> dict[str, Any]:
    policy = {
        "schema_version": SANDBOX_POLICY_SCHEMA,
        "runner": SYSTEMD_RUN.as_posix(),
        "runner_sha256": PINNED_HOST_TOOLS[SYSTEMD_RUN.as_posix()],
        "control": SYSTEMCTL.as_posix(),
        "control_sha256": PINNED_HOST_TOOLS[SYSTEMCTL.as_posix()],
        "clearenv": ENV.as_posix(),
        "clearenv_sha256": PINNED_HOST_TOOLS[ENV.as_posix()],
        "probe_python": PROBE_PYTHON.as_posix(),
        "probe_python_sha256": PINNED_HOST_TOOLS[PROBE_PYTHON.as_posix()],
        "repository_view": "content-addressed-read-only-snapshot-through-landlock",
        "live_repository_view": "landlock-denied",
        "home": "landlock-private-writable-root",
        "tmp": "landlock-private-writable-root",
        "network": "systemd-seccomp-AF_INET-and-AF_INET6-denied",
        "process_cleanup": "systemd-cgroup-KillMode-control-group-TERM-then-KILL",
        "environment": dict(BASE_ENVIRONMENT),
        "max_output_bytes_per_channel": MAX_OUTPUT_BYTES,
        "max_timeout_seconds": MAX_TIMEOUT_SECONDS,
        "manager_conformance_id": MANAGER_CONFORMANCE_ID,
        "manager_probe_sha256": sha256_bytes(_PROBE_CODE.encode("utf-8")),
        "trusted_child_launcher_sha256": sha256_bytes(Path(__file__).read_bytes()),
    }
    return _seal(policy)


def make_command_spec(
    snapshot_manifest: Mapping[str, Any],
    *,
    command_id: str,
    argv: Sequence[str],
    timeout_seconds: int | float,
    conformance_id: str,
) -> dict[str, Any]:
    manifest = _validate_manifest(dict(snapshot_manifest))
    if not isinstance(command_id, str) or not ID_RE.fullmatch(command_id):
        raise SandboxError("BOOT command ID is malformed")
    if (
        not isinstance(argv, (list, tuple))
        or not argv
        or any(not isinstance(part, str) or not part or "\x00" in part for part in argv)
    ):
        raise SandboxError("BOOT command argv is malformed")
    tools = {row["path"] for row in manifest["tools"]}
    if argv[0] not in tools:
        raise SandboxError("BOOT command executable is not digest-bound")
    if "-c" in argv[1:]:
        raise SandboxError("BOOT candidate command may not contain inline executable code")
    if "-m" in argv[1:]:
        module_indexes = [index for index, value in enumerate(argv[1:], start=1) if value == "-m"]
        if (
            len(module_indexes) != 1
            or module_indexes[0] + 1 >= len(argv)
            or argv[module_indexes[0] + 1] != "py_compile"
        ):
            raise SandboxError("BOOT candidate module execution is not the pinned py_compile route")
    entry_paths = {row["path"] for row in manifest["entries"] if row["kind"] == "file"}
    for index, argument in enumerate(argv[1:], start=1):
        if argument.startswith("/") and argument not in tools:
            raise SandboxError(f"BOOT command argv[{index}] contains an unbound absolute path")
        if (
            not argument.startswith("-")
            and ("/" in argument or argument.endswith((".py", ".json", ".toml", ".lean")))
            and not Path(argument).is_absolute()
            and argument not in entry_paths
        ):
            raise SandboxError(f"BOOT command argv[{index}] names an undeclared snapshot input")
    if (
        not isinstance(timeout_seconds, (int, float))
        or isinstance(timeout_seconds, bool)
        or not 0 < float(timeout_seconds) <= MAX_TIMEOUT_SECONDS
    ):
        raise SandboxError("BOOT command timeout is outside the closed bound")
    if conformance_id != MANAGER_CONFORMANCE_ID:
        raise SandboxError("BOOT command lacks the manager-pinned conformance ID")
    policy = sandbox_policy()
    return _seal({
        "schema_version": COMMAND_SCHEMA,
        "command_id": command_id,
        "argv": list(argv),
        "cwd": ".",
        "shell": False,
        "stdin": "devnull",
        "timeout_seconds": float(timeout_seconds),
        "max_output_bytes": MAX_OUTPUT_BYTES,
        "conformance_id": conformance_id,
        "snapshot_manifest_sha256": manifest["authority_sha256"],
        "tool_bindings_sha256": manifest["tools_sha256"],
        "sandbox_policy_sha256": policy["authority_sha256"],
    })


def _validate_command(value: Any, manifest: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _COMMAND_FIELDS:
        raise SandboxError("BOOT command fields are not closed")
    _verify_seal(value, "BOOT command")
    if (
        value.get("schema_version") != COMMAND_SCHEMA
        or value.get("cwd") != "."
        or value.get("shell") is not False
        or value.get("stdin") != "devnull"
        or value.get("conformance_id") != MANAGER_CONFORMANCE_ID
        or value.get("snapshot_manifest_sha256") != manifest["authority_sha256"]
        or value.get("tool_bindings_sha256") != manifest["tools_sha256"]
        or value.get("sandbox_policy_sha256") != sandbox_policy()["authority_sha256"]
        or value.get("max_output_bytes") != MAX_OUTPUT_BYTES
    ):
        raise SandboxError("BOOT command authority binding differs")
    rebuilt = make_command_spec(
        manifest,
        command_id=value.get("command_id"),
        argv=value.get("argv"),
        timeout_seconds=value.get("timeout_seconds"),
        conformance_id=value.get("conformance_id"),
    )
    if rebuilt != value:
        raise SandboxError("BOOT command is not the canonical closed specification")
    return value


def _capture_snapshot(root: Path, manifest: Mapping[str, Any], destination: Path) -> None:
    directories = [row for row in manifest["entries"] if row["kind"] == "directory"]
    files = [row for row in manifest["entries"] if row["kind"] == "file"]
    destination.mkdir(mode=0o700)
    for row in sorted(directories, key=lambda item: (len(PurePosixPath(item["path"]).parts), item["path"])):
        target = destination / row["path"]
        target.mkdir(parents=True, exist_ok=True, mode=0o700)
    for row in files:
        source = root / row["path"]
        raw, observed = _read_regular(source, f"snapshot input {row['path']}")
        if (
            len(raw) != row["size"]
            or sha256_bytes(raw) != row["sha256"]
            or stat.S_IMODE(observed.st_mode) != row["mode"]
        ):
            raise SandboxError(f"snapshot input drift before spawn: {row['path']}")
        target = destination / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        descriptor = os.open(
            target,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
            0o600,
        )
        try:
            view = memoryview(raw)
            while view:
                written = os.write(descriptor, view)
                view = view[written:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        target.chmod(0o555 if row["mode"] & 0o111 else 0o444)
    for path in sorted(
        (candidate for candidate in destination.rglob("*") if candidate.is_dir()),
        key=lambda candidate: len(candidate.parts), reverse=True,
    ):
        path.chmod(0o555)
    destination.chmod(0o555)
    observed_rows = []
    for row in manifest["entries"]:
        path = destination / row["path"]
        if row["kind"] == "directory":
            if not path.is_dir() or path.is_symlink():
                raise SandboxError(f"materialized snapshot directory missing: {row['path']}")
        else:
            raw, observed = _read_regular(path, f"materialized snapshot {row['path']}")
            if len(raw) != row["size"] or sha256_bytes(raw) != row["sha256"]:
                raise SandboxError(f"materialized snapshot digest differs: {row['path']}")
        observed_rows.append(row)
    if sha256_bytes(canonical_json(observed_rows)) != manifest["entries_sha256"]:
        raise SandboxError("materialized snapshot manifest differs")


def _systemd_properties(
    *, unit: str, snapshot: Path, source_root: Path, timeout_seconds: float,
) -> list[str]:
    properties = [
        "KillMode=control-group",
        "SendSIGKILL=yes",
        f"TimeoutStopSec={TERMINATION_GRACE_SECONDS}s",
        f"RuntimeMaxSec={timeout_seconds}s",
        "PrivateNetwork=no",
        "PrivateTmp=no",
        "PrivateIPC=no",
        "ProtectSystem=no",
        "ProtectHome=no",
        "ProtectKernelTunables=yes",
        "ProtectControlGroups=yes",
        "ProtectProc=default",
        "NoNewPrivileges=yes",
        "RestrictSUIDSGID=yes",
        "RestrictRealtime=yes",
        "RestrictNamespaces=yes",
        "RestrictAddressFamilies=AF_UNIX",
        "LockPersonality=yes",
        "MemoryDenyWriteExecute=no",
        "RemoveIPC=yes",
        "SystemCallArchitectures=native",
        "KeyringMode=private",
        "UMask=0077",
        "TasksMax=256",
        "MemoryMax=2147483648",
        "LimitNOFILE=1024",
        "LimitCORE=0",
        "SystemCallErrorNumber=EPERM",
        "SystemCallFilter=~kill tkill tgkill pidfd_send_signal ptrace process_vm_readv process_vm_writev ioprio_set setpriority sched_setattr sched_setparam sched_setscheduler",
        "WorkingDirectory=/",
    ]
    return properties


def _sandbox_environment(private_root: str) -> dict[str, str]:
    private = private_root
    environment = {
        **BASE_ENVIRONMENT,
        # The candidate is a read-only content-addressed BOOT snapshot.  This
        # explicit marker lets the repository manager distinguish that sealed
        # validation view from an unreviewed arbitrary relocation.
        "STAGE5_BOOT_SANDBOX": "1",
        # The canonical repository root and its checked-in authority remain
        # the manager's identity even while Python runs from the sealed
        # snapshot.  Validators use this reviewed binding for root checks.
        "STAGE5_BOOT_CANONICAL_ROOT": "/home/sansha/Github/awesome_theorems",
        "STAGE5_BOOT_AUTH": f"{private}/boot-auth.json",
        "STAGE5_BOOT_CONFIG": f"{private}/boot-config.toml",
        "HOME": f"{private}/home",
        "TMPDIR": f"{private}/tmp",
        "TMP": f"{private}/tmp",
        "TEMP": f"{private}/tmp",
        "XDG_CACHE_HOME": f"{private}/cache",
        "XDG_CONFIG_HOME": f"{private}/config",
        "XDG_DATA_HOME": f"{private}/data",
    }
    return dict(sorted(environment.items()))


def _tool_read_roots(manifest: Mapping[str, Any]) -> list[str]:
    roots = {"/usr", "/bin", "/lib", "/lib64", "/etc/ld.so.cache"}
    for row in manifest["tools"]:
        path = Path(row["path"])
        roots.add(path.as_posix())
        roots.add(path.parent.as_posix())
    resolved = set()
    for value in roots:
        path = Path(value)
        if path.exists():
            resolved.add(path.resolve(strict=True).as_posix())
    return sorted(resolved)


def _make_child_config(
    *, snapshot: Path, source_root: Path, private_root: Path,
    manifest: Mapping[str, Any], command_argv: Sequence[str], launcher: Path,
) -> dict[str, Any]:
    private_root.mkdir(mode=0o700)
    for child in ("home", "tmp", "cache", "config", "data"):
        (private_root / child).mkdir(mode=0o700)
    (private_root / "boot-auth.json").write_text("{}\n", encoding="utf-8")
    (private_root / "boot-config.toml").write_text(
        '[model_providers.sub2api]\nname = "sub2api"\nbase_url = "http://127.0.0.1"\nwire_api = "responses"\n',
        encoding="utf-8",
    )
    return _seal({
        "schema_version": _CHILD_CONFIG_SCHEMA,
        "snapshot": snapshot.as_posix(),
        "source_root": source_root.as_posix(),
        "private_root": private_root.as_posix(),
        "argv": list(command_argv),
        "environment": _sandbox_environment(private_root.as_posix()),
        "read_paths": _tool_read_roots(manifest),
        "launcher_sha256": sha256_bytes(launcher.read_bytes()),
    })


def _validate_child_config(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _CHILD_CONFIG_FIELDS:
        raise SandboxError("Landlock child config fields are not closed")
    _verify_seal(value, "Landlock child config")
    if value.get("schema_version") != _CHILD_CONFIG_SCHEMA:
        raise SandboxError("Landlock child config schema differs")
    for field in ("snapshot", "source_root", "private_root"):
        text = value.get(field)
        if not isinstance(text, str) or not Path(text).is_absolute() or "\x00" in text:
            raise SandboxError(f"Landlock child {field} is malformed")
        path = Path(text)
        if path.resolve(strict=True) != path or path.is_symlink():
            raise SandboxError(f"Landlock child {field} is not a real canonical path")
    argv = value.get("argv")
    if (
        not isinstance(argv, list)
        or not argv
        or any(not isinstance(part, str) or not part or "\x00" in part for part in argv)
        or not Path(argv[0]).is_absolute()
    ):
        raise SandboxError("Landlock child argv is malformed")
    environment = value.get("environment")
    if environment != _sandbox_environment(value["private_root"]):
        raise SandboxError("Landlock child environment differs")
    read_paths = value.get("read_paths")
    if (
        not isinstance(read_paths, list)
        or read_paths != sorted(set(read_paths))
        or any(not isinstance(path, str) or not Path(path).is_absolute() for path in read_paths)
    ):
        raise SandboxError("Landlock child read paths differ")
    if value.get("launcher_sha256") != sha256_bytes(Path(__file__).read_bytes()):
        raise SandboxError("Landlock trusted child launcher drift")
    return value


def _syscall(number: int, *arguments: Any) -> int:
    libc = ctypes.CDLL(None, use_errno=True)
    result = int(libc.syscall(number, *arguments))
    if result < 0:
        observed_errno = ctypes.get_errno()
        raise OSError(observed_errno, os.strerror(observed_errno))
    return result


def _landlock_add_path(ruleset_fd: int, path: Path, allowed: int) -> None:
    observed = path.stat(follow_symlinks=False)
    if stat.S_ISREG(observed.st_mode):
        allowed &= (
            _LANDLOCK_ACCESS_FS_EXECUTE
            | _LANDLOCK_ACCESS_FS_WRITE_FILE
            | _LANDLOCK_ACCESS_FS_READ_FILE
            | _LANDLOCK_ACCESS_FS_TRUNCATE
        )
    parent_fd = os.open(path, os.O_PATH | os.O_CLOEXEC | os.O_NOFOLLOW)
    try:
        attribute = _LandlockPathBeneathAttr(allowed, parent_fd, 0)
        try:
            _syscall(445, ruleset_fd, 1, ctypes.byref(attribute), 0)
        except OSError as exc:
            raise OSError(exc.errno, f"{exc.strerror}: {path} access={allowed:#x}") from exc
    finally:
        os.close(parent_fd)


def _restrict_with_landlock(config: Mapping[str, Any]) -> None:
    try:
        abi = _syscall(444, 0, 0, _LANDLOCK_CREATE_RULESET_VERSION)
    except OSError as exc:
        raise SandboxError("Landlock ABI query failed; no sandbox fallback exists") from exc
    if abi < 3:
        raise SandboxError(f"Landlock ABI {abi} lacks required truncate/refer controls")
    abi_handled = _LANDLOCK_READ | _LANDLOCK_WRITE
    if abi < 2:
        abi_handled &= ~_LANDLOCK_ACCESS_FS_REFER
    if abi < 3:
        abi_handled &= ~_LANDLOCK_ACCESS_FS_TRUNCATE
    # Filesystems may reject optional rights even when the running kernel
    # advertises a newer ABI (notably overlay/snap configurations).  Build the
    # strongest ruleset the kernel accepts, but never omit the read/write/make
    # rights needed to protect the canonical tree.
    required = (
        _LANDLOCK_ACCESS_FS_EXECUTE
        | _LANDLOCK_ACCESS_FS_WRITE_FILE
        | _LANDLOCK_ACCESS_FS_READ_FILE
        | _LANDLOCK_ACCESS_FS_READ_DIR
        | _LANDLOCK_ACCESS_FS_REMOVE_DIR
        | _LANDLOCK_ACCESS_FS_REMOVE_FILE
        | _LANDLOCK_ACCESS_FS_MAKE_DIR
        | _LANDLOCK_ACCESS_FS_MAKE_REG
        | _LANDLOCK_ACCESS_FS_MAKE_SYM
    )
    candidates = [abi_handled]
    for optional in (
        _LANDLOCK_ACCESS_FS_TRUNCATE,
        _LANDLOCK_ACCESS_FS_REFER,
        _LANDLOCK_ACCESS_FS_MAKE_BLOCK,
        _LANDLOCK_ACCESS_FS_MAKE_CHAR,
        _LANDLOCK_ACCESS_FS_MAKE_SOCK,
        _LANDLOCK_ACCESS_FS_MAKE_FIFO,
    ):
        candidates.append(candidates[-1] & ~optional)
    handled = 0
    ruleset_fd = -1
    for candidate in candidates:
        if candidate & required != required:
            continue
        attribute = _LandlockRulesetAttr(candidate)
        try:
            ruleset_fd = _syscall(444, ctypes.byref(attribute), ctypes.sizeof(attribute), 0)
            handled = candidate
            break
        except OSError as exc:
            if exc.errno not in {errno.EINVAL, errno.ENOMSG, errno.EOPNOTSUPP}:
                raise SandboxError("Landlock ruleset creation failed") from exc
    if ruleset_fd < 0 or not handled:
        raise SandboxError("Landlock cannot enforce the mandatory filesystem rights")
    try:
        read_paths = [Path(config["snapshot"]), *(Path(path) for path in config["read_paths"])]
        for path in read_paths:
            if path.exists():
                _landlock_add_path(ruleset_fd, path, _LANDLOCK_READ & handled)
        _landlock_add_path(
            ruleset_fd, Path(config["private_root"]),
            (_LANDLOCK_READ | _LANDLOCK_WRITE) & handled,
        )
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
            observed_errno = ctypes.get_errno()
            raise OSError(observed_errno, os.strerror(observed_errno))
        _syscall(446, ruleset_fd, 0)
    except OSError as exc:
        raise SandboxError(f"Landlock rule installation failed: {exc}") from exc
    finally:
        os.close(ruleset_fd)


def _landlock_child(config_path: Path) -> None:
    raw, _ = _read_regular(config_path, "Landlock child config")
    try:
        config = _validate_child_config(json.loads(raw))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SandboxError("Landlock child config is not canonical JSON") from exc
    if raw != canonical_json(config):
        raise SandboxError("Landlock child config bytes are not canonical")
    os.environ.clear()
    os.environ.update(config["environment"])
    os.chdir(config["snapshot"])
    _restrict_with_landlock(config)
    try:
        os.execve(config["argv"][0], config["argv"], config["environment"])
    except OSError as exc:
        raise SandboxError("Landlock child could not exec the sealed command") from exc


def _systemd_argv(
    *, unit: str, snapshot: Path, source_root: Path, timeout_seconds: float,
    manifest: Mapping[str, Any], child_config: Path, launcher: Path,
) -> list[str]:
    argv = [
        SYSTEMD_RUN.as_posix(), "--user", "--quiet", "--wait", "--pipe",
        "--service-type=exec", f"--unit={unit}",
    ]
    for prop in _systemd_properties(
        unit=unit, snapshot=snapshot, source_root=source_root,
        timeout_seconds=timeout_seconds,
    ):
        argv.extend(["--property", prop])
    argv.extend([
        "--", PROBE_PYTHON.as_posix(), "-I", "-B", launcher.as_posix(),
        "--landlock-child", child_config.as_posix(),
    ])
    return argv


def _trusted_launcher_copy(destination_root: Path) -> Path:
    raw, _ = _read_regular(Path(__file__), "trusted Landlock launcher")
    destination = destination_root / f"launcher-{sha256_bytes(raw)}.py"
    if not destination.exists():
        descriptor = os.open(
            destination,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
            0o400,
        )
        try:
            view = memoryview(raw)
            while view:
                written = os.write(descriptor, view)
                view = view[written:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    observed, _ = _read_regular(destination, "copied Landlock launcher")
    if observed != raw:
        raise SandboxError("trusted Landlock launcher copy differs")
    return destination


def _signal_process_group(process: subprocess.Popen[bytes], signum: int) -> None:
    try:
        os.killpg(process.pid, signum)
    except ProcessLookupError:
        pass


def _run_control(argv: Sequence[str], *, check: bool = False) -> subprocess.CompletedProcess[bytes]:
    try:
        completed = subprocess.run(
            list(argv), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=_control_environment(),
            timeout=CONTROL_TIMEOUT_SECONDS, check=False, start_new_session=True,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SandboxError("systemd control command failed or timed out") from exc
    if check and completed.returncode != 0:
        raise SandboxError(
            f"systemd control command failed exit={completed.returncode}: {argv[1:3]}"
        )
    return completed


def _unit_properties(unit: str) -> dict[str, str]:
    completed = _run_control([
        SYSTEMCTL.as_posix(), "--user", "show", f"{unit}.service", "--no-pager",
        "--property=LoadState", "--property=ActiveState", "--property=SubState",
        "--property=Result", "--property=ExecMainStatus",
    ])
    if completed.returncode != 0:
        return {"LoadState": "not-found"}
    result: dict[str, str] = {}
    try:
        for line in completed.stdout.decode("utf-8", "strict").splitlines():
            key, separator, value = line.partition("=")
            if separator and key in {"LoadState", "ActiveState", "SubState", "Result", "ExecMainStatus"}:
                result[key] = value
    except UnicodeDecodeError as exc:
        raise SandboxError("systemd returned non-UTF-8 unit state") from exc
    return result


def _cleanup_unit(unit: str) -> tuple[dict[str, str], bool]:
    before = _unit_properties(unit)
    if before.get("ActiveState") not in {None, "inactive", "failed"}:
        _run_control([
            SYSTEMCTL.as_posix(), "--user", "kill", "--kill-whom=all",
            "--signal=SIGTERM", f"{unit}.service",
        ])
        deadline = time.monotonic() + TERMINATION_GRACE_SECONDS
        while time.monotonic() < deadline:
            if _unit_properties(unit).get("ActiveState") in {None, "inactive", "failed"}:
                break
            time.sleep(0.02)
        state = _unit_properties(unit)
        if state.get("ActiveState") not in {None, "inactive", "failed"}:
            _run_control([
                SYSTEMCTL.as_posix(), "--user", "kill", "--kill-whom=all",
                "--signal=SIGKILL", f"{unit}.service",
            ])
    _run_control([SYSTEMCTL.as_posix(), "--user", "stop", f"{unit}.service"])
    _run_control([SYSTEMCTL.as_posix(), "--user", "reset-failed", f"{unit}.service"])
    deadline = time.monotonic() + TERMINATION_GRACE_SECONDS
    after: dict[str, str] = {}
    while time.monotonic() < deadline:
        after = _unit_properties(unit)
        if after.get("LoadState") in {None, "not-found"}:
            return before, True
        time.sleep(0.02)
    return before, False


def _communicate_bounded(
    process: subprocess.Popen[bytes], *, deadline: float,
) -> tuple[bytes, bytes, bool, bool]:
    if process.stdout is None or process.stderr is None:
        raise SandboxError("sandbox output pipes were not created")
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    overflow = False
    timed_out = False
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            events = selector.select(min(remaining, 0.1))
            if not events and process.poll() is not None:
                events = [(key, 0) for key in list(selector.get_map().values())]
            for key, _ in events:
                try:
                    chunk = os.read(key.fd, 65536)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                buffer = buffers[key.data]
                if len(buffer) + len(chunk) > MAX_OUTPUT_BYTES:
                    remaining_bytes = max(0, MAX_OUTPUT_BYTES - len(buffer))
                    buffer.extend(chunk[:remaining_bytes])
                    overflow = True
                    return bytes(buffers["stdout"]), bytes(buffers["stderr"]), timed_out, overflow
                buffer.extend(chunk)
        return bytes(buffers["stdout"]), bytes(buffers["stderr"]), timed_out, overflow
    finally:
        selector.close()


def _closed_result(
    *, command_id: str, command_authority: str, command_argv: Sequence[str],
    unit: str, exit_code: int | None, systemd_result: str, timed_out: bool,
    overflow: bool, duration_ms: int, stdout: bytes, stderr: bytes,
    descendants_absent: bool, manifest: Mapping[str, Any],
) -> dict[str, Any]:
    return _seal({
        "schema_version": RESULT_SCHEMA,
        "command_id": command_id,
        "command_authority_sha256": command_authority,
        "argv": list(command_argv),
        "snapshot_manifest_sha256": manifest["authority_sha256"],
        "tool_bindings_sha256": manifest["tools_sha256"],
        "sandbox_policy_sha256": sandbox_policy()["authority_sha256"],
        "conformance_id": MANAGER_CONFORMANCE_ID,
        "sandbox_unit": unit,
        "systemd_result": systemd_result,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "output_overflow": overflow,
        "duration_ms": duration_ms,
        "stdout_base64": base64.b64encode(stdout).decode("ascii"),
        "stdout_size": len(stdout),
        "stdout_sha256": sha256_bytes(stdout),
        "stdout_complete": not overflow,
        "stderr_base64": base64.b64encode(stderr).decode("ascii"),
        "stderr_size": len(stderr),
        "stderr_sha256": sha256_bytes(stderr),
        "stderr_complete": not overflow,
        "descendants_absent": descendants_absent,
    })


def _run_one(
    *, source_root: Path, snapshot: Path, manifest: Mapping[str, Any],
    command_id: str, command_authority: str, argv: Sequence[str],
    timeout_seconds: float,
) -> dict[str, Any]:
    unit = f"stage5-boot-{os.getpid()}-{secrets.token_hex(8)}"
    control_root = snapshot.parent
    private_root = control_root / f"private-{unit}"
    launcher = _trusted_launcher_copy(control_root)
    child_config = _make_child_config(
        snapshot=snapshot,
        source_root=source_root,
        private_root=private_root,
        manifest=manifest,
        command_argv=argv,
        launcher=launcher,
    )
    child_config_path = control_root / f"config-{unit}.json"
    config_raw = canonical_json(child_config)
    descriptor = os.open(
        child_config_path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
        0o400,
    )
    try:
        view = memoryview(config_raw)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    systemd_argv = _systemd_argv(
        unit=unit, snapshot=snapshot, source_root=source_root,
        timeout_seconds=timeout_seconds, manifest=manifest,
        child_config=child_config_path, launcher=launcher,
    )
    started = time.monotonic_ns()
    try:
        process = subprocess.Popen(
            systemd_argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=_control_environment(),
            shell=False, close_fds=True, start_new_session=True,
        )
    except OSError as exc:
        raise SandboxError("systemd sandbox could not be spawned") from exc
    stdout = b""
    stderr = b""
    timed_out = False
    overflow = False
    state: dict[str, str] = {}
    descendants_absent = False
    try:
        stdout, stderr, timed_out, overflow = _communicate_bounded(
            process,
            deadline=time.monotonic() + timeout_seconds + TERMINATION_GRACE_SECONDS + 2.0,
        )
        if timed_out or overflow:
            _signal_process_group(process, signal.SIGTERM)
        try:
            process.wait(timeout=TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            _signal_process_group(process, signal.SIGKILL)
            try:
                process.wait(timeout=TERMINATION_GRACE_SECONDS)
            except subprocess.TimeoutExpired as exc:
                raise SandboxError("systemd-run process group did not terminate") from exc
    finally:
        state, descendants_absent = _cleanup_unit(unit)
        if process.poll() is None:
            _signal_process_group(process, signal.SIGKILL)
            process.wait(timeout=TERMINATION_GRACE_SECONDS)
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
    duration_ms = (time.monotonic_ns() - started) // 1_000_000
    systemd_result = state.get("Result", "unknown")
    timed_out = timed_out or systemd_result == "timeout"
    result = _closed_result(
        command_id=command_id,
        command_authority=command_authority,
        command_argv=argv,
        unit=unit,
        exit_code=process.returncode,
        systemd_result=systemd_result,
        timed_out=timed_out,
        overflow=overflow,
        duration_ms=duration_ms,
        stdout=stdout,
        stderr=stderr,
        descendants_absent=descendants_absent,
        manifest=manifest,
    )
    if not descendants_absent:
        raise SandboxError("sandbox cgroup/descendants remain after command", evidence=result)
    if overflow:
        raise SandboxError("BOOT command exceeded the complete-output bound", evidence=result)
    if timed_out:
        raise SandboxError("BOOT command timed out", evidence=result)
    if process.returncode != 0 or systemd_result not in {"success", "unknown"}:
        raise SandboxError(
            f"BOOT command failed exit={process.returncode} result={systemd_result}",
            evidence=result,
        )
    return result


_PROBE_CODE = r'''import errno,json,os,socket,sys
workspace,live_root,tmp_marker,parent_pid,expected_home=sys.argv[1:]
def denied_write(path):
    try:
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd);return False
    except OSError as exc:return exc.errno in {errno.EACCES,errno.EROFS,errno.ENOENT}
def denied_family(family):
    try:s=socket.socket(family,socket.SOCK_STREAM);s.close();return False
    except OSError as exc:return exc.errno in {errno.EAFNOSUPPORT,errno.EPERM,errno.EACCES}
def denied_read(path):
    try:fd=os.open(path,os.O_RDONLY);os.close(fd);return False
    except OSError as exc:return exc.errno in {errno.EACCES,errno.EPERM,errno.ENOENT}
def denied_signal(pid):
    try:os.kill(int(pid),0);return False
    except OSError as exc:return exc.errno in {errno.EPERM,errno.ESRCH}
home=os.environ.get("HOME","")
os.makedirs(home,exist_ok=True)
home_probe=os.path.join(home,"probe")
with open(home_probe,"w",encoding="utf-8") as stream:stream.write("private")
with open(tmp_marker,"w",encoding="utf-8") as stream:stream.write("private")
result={
 "cwd":os.getcwd()==workspace,
 "workspace_readable":os.path.isdir(workspace),
 "workspace_read_only":denied_write(os.path.join(workspace,".manager-write-probe")),
 "live_root_read_denied":denied_read(live_root),
 "home_private":home==expected_home and os.path.isfile(home_probe),
 "tmp_private":os.path.isfile(tmp_marker),
 "inet_denied":denied_family(socket.AF_INET),
 "inet6_denied":denied_family(socket.AF_INET6),
 "host_process_read_denied":denied_read("/proc/%s/status"%parent_pid),
 "host_signal_denied":denied_signal(parent_pid),
}
print(json.dumps(result,sort_keys=True,separators=(",",":")))
'''


def _run_manager_probe(root: Path, snapshot: Path, manifest: Mapping[str, Any]) -> None:
    marker_name = f"stage5-boot-host-tmp-probe-{os.getpid()}-{secrets.token_hex(8)}"
    host_marker = Path("/tmp") / marker_name
    # _run_one chooses the unit name, so construct the same operation locally
    # with a dedicated path that reports its actual HOME instead of trusting a
    # producer-controlled value.
    probe_code = _PROBE_CODE.replace(
        "home==expected_home", "home.endswith('/home') and 'private-stage5-boot-' in home"
    ).replace(
        'with open(tmp_marker,"w",encoding="utf-8") as stream:stream.write("private")',
        'tmp_denied=denied_write(tmp_marker)',
    ).replace(
        '"tmp_private":os.path.isfile(tmp_marker),',
        '"host_tmp_denied":tmp_denied,\n "private_tmp_writable":denied_write(os.path.join(os.environ["TMPDIR"],"probe")) is False,',
    )
    argv = [
        PROBE_PYTHON.as_posix(), "-I", "-B", "-c", probe_code,
        snapshot.as_posix(), root.as_posix(), f"/tmp/{marker_name}", str(os.getpid()),
        "__PRIVATE_HOME__",
    ]
    result = _run_one(
        source_root=root,
        snapshot=snapshot,
        manifest=manifest,
        command_id="manager-isolation-probe",
        command_authority=sha256_bytes(canonical_json({
            "probe_sha256": sha256_bytes(_PROBE_CODE.encode("utf-8")),
            "policy_sha256": sandbox_policy()["authority_sha256"],
        })),
        argv=argv,
        timeout_seconds=15.0,
    )
    if host_marker.exists():
        raise SandboxError("PrivateTmp probe escaped into host /tmp", evidence=result)
    try:
        stdout = base64.b64decode(result["stdout_base64"], validate=True)
        semantic = json.loads(stdout)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SandboxError("manager isolation probe output is malformed", evidence=result) from exc
    expected_keys = {
        "cwd", "workspace_readable", "workspace_read_only", "live_root_read_denied",
        "home_private", "host_tmp_denied", "private_tmp_writable", "inet_denied", "inet6_denied",
        "host_process_read_denied",
        "host_signal_denied",
    }
    if set(semantic) != expected_keys or any(value is not True for value in semantic.values()):
        raise SandboxError(
            f"manager isolation probe did not prove every boundary: {semantic}",
            evidence=result,
        )


def run_suite(
    root: Path | str,
    snapshot_manifest: Mapping[str, Any],
    command_specs: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Execute one frozen suite and return closed, receipt-ready evidence.

    All manifest/spec/tool checks and snapshot capture happen before the first
    candidate spawn.  Any sandbox setup, timeout, output, cleanup, command or
    conformance failure raises ``SandboxError``; no bare-process fallback is
    present.
    """

    source_root = _safe_root(root)
    _validate_host_tools()
    manifest = _validate_manifest(dict(snapshot_manifest), expected_root=source_root)
    if not isinstance(command_specs, (list, tuple)) or not command_specs:
        raise SandboxError("BOOT command suite is empty or malformed")
    commands = [_validate_command(dict(command), manifest) for command in command_specs]
    command_ids = [row["command_id"] for row in commands]
    if command_ids != list(dict.fromkeys(command_ids)):
        raise SandboxError("BOOT command IDs are duplicated")

    temporary = Path(tempfile.mkdtemp(prefix="stage5-boot-snapshot-", dir="/tmp"))
    snapshot = temporary / manifest["authority_sha256"]
    results: list[dict[str, Any]] = []
    try:
        _capture_snapshot(source_root, manifest, snapshot)
        # Recheck tools after potentially expensive capture and before spawn.
        _validate_manifest(manifest, expected_root=source_root)
        _run_manager_probe(source_root, snapshot, manifest)
        for command in commands:
            results.append(_run_one(
                source_root=source_root,
                snapshot=snapshot,
                manifest=manifest,
                command_id=command["command_id"],
                command_authority=command["authority_sha256"],
                argv=command["argv"],
                timeout_seconds=command["timeout_seconds"],
            ))
        _validate_manifest(manifest, expected_root=source_root)
        suite = _seal({
            "schema_version": SUITE_SCHEMA,
            "snapshot_manifest_sha256": manifest["authority_sha256"],
            "sandbox_policy_sha256": sandbox_policy()["authority_sha256"],
            "commands": results,
            "suite_conformance_id": MANAGER_CONFORMANCE_ID,
            "side_effects_absent": True,
        })
        return suite
    finally:
        try:
            snapshot.chmod(0o700) if snapshot.exists() else None
            for directory in sorted(
                (path for path in snapshot.rglob("*") if path.is_dir()) if snapshot.exists() else (),
                key=lambda path: len(path.parts), reverse=True,
            ):
                directory.chmod(0o700)
            for file_path in snapshot.rglob("*") if snapshot.exists() else ():
                if file_path.is_file():
                    file_path.chmod(0o600)
            shutil.rmtree(temporary)
        except OSError as exc:
            raise SandboxError("content-addressed snapshot cleanup failed") from exc


__all__ = [
    "BASE_ENVIRONMENT", "COMMAND_SCHEMA", "MANAGER_CONFORMANCE_ID",
    "MAX_OUTPUT_BYTES", "MAX_TIMEOUT_SECONDS", "RESULT_SCHEMA",
    "SANDBOX_POLICY_SCHEMA", "SNAPSHOT_SCHEMA", "SUITE_SCHEMA",
    "SandboxError", "canonical_json", "make_command_spec", "run_suite",
    "sandbox_policy", "seal_snapshot_manifest", "sha256_bytes",
]


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landlock-child", type=Path)
    arguments = parser.parse_args()
    if arguments.landlock_child is None:
        parser.error("this module is not an ordinary command-line runner")
    try:
        _landlock_child(arguments.landlock_child)
    except SandboxError as exc:
        print(f"SANDBOX ERROR: {exc}", file=__import__("sys").stderr)
        return 125
    raise AssertionError("execve unexpectedly returned")


if __name__ == "__main__":
    raise SystemExit(_main())
