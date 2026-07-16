#!/usr/bin/env python3
"""Content-address the frozen Stage1 claim ledger and worker deltas.

This utility is deliberately outside the scheduler mutation path.  It never
changes claims, workspaces, the blueprint, or pause markers.  A written archive
contains only Git deltas and untracked entries, not another copy of each clone.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
from typing import Any, NoReturn


SCHEMA = "stage1-frozen-runtime-archive/1.0"
WORKSPACE_SCHEMA = "stage1-frozen-workspace-delta/1.0"
RETIREMENT_SCHEMA = "stage1-frozen-claim-retirement/1.0"
SHA256_RE_LENGTH = 64
ITEM_RE = re.compile(r"^S56-M-([0-9]{4})-[A-Z_]+$")
THEOREM_RE = re.compile(r"^THM-M-([0-9]{4})$")
CLAIM_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}$")


class ArchiveError(RuntimeError):
    """The frozen runtime cannot be archived without weakening its binding."""


def fail(message: str) -> NoReturn:
    raise ArchiveError(message)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def content_address(value: dict[str, Any], field: str) -> dict[str, Any]:
    if field in value:
        fail(f"content-address field already exists: {field}")
    result = dict(value)
    result[field] = sha256_bytes(canonical_json(value))
    return result


def run_bytes(cwd: Path, argv: list[str]) -> bytes:
    result = subprocess.run(
        argv,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        fail(f"command failed ({' '.join(argv)}): {detail}")
    return result.stdout


def git_text(cwd: Path, *argv: str) -> str:
    return run_bytes(cwd, ["git", *argv]).decode("ascii", "strict").strip()


def nul_paths(value: bytes, label: str) -> list[str]:
    if value and not value.endswith(b"\0"):
        fail(f"{label} is not NUL-terminated")
    result: list[str] = []
    for raw in value.split(b"\0"):
        if not raw:
            continue
        try:
            relative = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ArchiveError(f"{label} contains a non-UTF-8 path") from exc
        pure = PurePosixPath(relative)
        if (
            not relative
            or pure.is_absolute()
            or pure.as_posix() != relative
            or any(part in {"", ".", ".."} for part in pure.parts)
        ):
            fail(f"{label} contains an unsafe path")
        result.append(relative)
    if len(result) != len(set(result)):
        fail(f"{label} contains duplicate paths")
    return sorted(result)


def read_untracked_entry(workspace: Path, relative: str) -> dict[str, Any]:
    """Read one untracked leaf without following a symlink in any component."""

    parts = PurePosixPath(relative).parts
    descriptor = os.open(workspace, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in parts[:-1]:
            child = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = child
        metadata = os.stat(parts[-1], dir_fd=descriptor, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode):
            target = os.readlink(parts[-1], dir_fd=descriptor)
            return {
                "path": relative,
                "kind": "symlink",
                "mode": stat.S_IMODE(metadata.st_mode),
                "target": target,
                "target_sha256": sha256_bytes(os.fsencode(target)),
            }
        if not stat.S_ISREG(metadata.st_mode):
            fail(f"untracked entry is neither a regular file nor symlink: {relative}")
        opened = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=descriptor)
        try:
            before = os.fstat(opened)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(opened, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            after = os.fstat(opened)
        finally:
            os.close(opened)
        identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        if identity != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            fail(f"untracked entry changed while archived: {relative}")
        data = b"".join(chunks)
        return {
            "path": relative,
            "kind": "regular",
            "mode": stat.S_IMODE(before.st_mode),
            "size": len(data),
            "sha256": sha256_bytes(data),
            "content_base64": base64.b64encode(data).decode("ascii"),
        }
    except OSError as exc:
        raise ArchiveError(f"cannot safely read untracked entry: {relative}") from exc
    finally:
        os.close(descriptor)


def canonical_workspace(root: Path, runtime: Path, value: Any, slot: Any) -> Path:
    if not isinstance(slot, int) or isinstance(slot, bool) or slot < 1:
        fail("claim slot is malformed")
    expected = runtime / "workers" / f"slot{slot}"
    if not isinstance(value, str) or Path(value).absolute() != expected.absolute():
        fail("claim workspace is not the canonical slot path")
    if not expected.absolute().is_relative_to(root.absolute()):
        fail("claim workspace escapes the repository")
    return expected


def claim_metadata_state(claim: dict[str, Any], slot: int) -> str:
    item = claim.get("item_id")
    theorem = claim.get("theorem_id")
    claim_id = claim.get("claim_id")
    workspace = claim.get("workspace")
    item_match = ITEM_RE.fullmatch(item) if isinstance(item, str) else None
    theorem_match = THEOREM_RE.fullmatch(theorem) if isinstance(theorem, str) else None
    complete = (
        item_match is not None
        and theorem_match is not None
        and item_match.group(1) == theorem_match.group(1)
        and isinstance(claim_id, str)
        and CLAIM_ID_RE.fullmatch(claim_id) is not None
        and isinstance(workspace, str)
        and isinstance(claim.get("status"), str)
        and isinstance(claim.get("owned_paths"), list)
    )
    if not complete:
        return "incomplete"
    return "internally_consistent"


def owned_path_classification(
    claim: dict[str, Any], changed: list[str]
) -> tuple[list[str], list[str], list[str]]:
    owned = claim.get("owned_paths")
    prefixes = (
        [f"{row.rstrip('/')}/" for row in owned if isinstance(row, str) and row]
        if isinstance(owned, list)
        else []
    )
    evidence_exact = {".stage1-worker-selftest.json"}
    infrastructure_exact = {"Formalizations/Lean/.lake"}
    in_scope = [
        path
        for path in changed
        if path in evidence_exact or any(path.startswith(prefix) for prefix in prefixes)
    ]
    infrastructure = [path for path in changed if path in infrastructure_exact]
    classified = set(in_scope) | set(infrastructure)
    return in_scope, infrastructure, [path for path in changed if path not in classified]


def workspace_delta(
    root: Path,
    runtime: Path,
    claim: dict[str, Any],
    *,
    claim_index: int,
    claims_sha256: str,
) -> dict[str, Any]:
    workspace = canonical_workspace(root, runtime, claim.get("workspace"), claim.get("slot"))
    identity = {
        "claim_index": claim_index,
        "claim_id": claim.get("claim_id"),
        "item_id": claim.get("item_id"),
        "theorem_id": claim.get("theorem_id"),
        "slot": claim.get("slot"),
        "ledger_status": claim.get("status"),
        "claims_sha256": claims_sha256,
        "workspace": str(workspace.relative_to(root)),
        "claim_metadata_state": claim_metadata_state(claim, int(claim["slot"])),
    }
    if not workspace.exists():
        return content_address(
            {
                "schema_version": WORKSPACE_SCHEMA,
                **identity,
                "workspace_state": "missing",
                "head_revision": None,
                "head_tree": None,
                "tracked_paths": [],
                "tracked_patch_sha256": sha256_bytes(b""),
                "tracked_patch_base64": "",
                "untracked_entries": [],
                "claim_owned_changed_paths": [],
                "scheduler_infrastructure_paths": [],
                "out_of_claim_changed_paths": [],
            },
            "archive_sha256",
        )
    if workspace.is_symlink() or not workspace.resolve().is_relative_to(runtime.resolve()):
        fail("worker workspace is a symlink or escapes runtime storage")
    if git_text(workspace, "rev-parse", "--is-inside-work-tree") != "true":
        fail("worker workspace is not a Git worktree")
    head = git_text(workspace, "rev-parse", "HEAD^{commit}")
    tree = git_text(workspace, "rev-parse", "HEAD^{tree}")
    tracked = nul_paths(
        run_bytes(workspace, ["git", "diff", "--name-only", "-z", "HEAD", "--"]),
        "tracked delta",
    )
    untracked = nul_paths(
        run_bytes(
            workspace,
            ["git", "ls-files", "--others", "--exclude-standard", "-z", "--"],
        ),
        "untracked delta",
    )
    patch = run_bytes(
        workspace,
        ["git", "diff", "--binary", "--full-index", "--no-ext-diff", "HEAD", "--"],
    )
    entries = [read_untracked_entry(workspace, relative) for relative in untracked]
    changed = sorted(set(tracked) | set(untracked))
    in_scope, infrastructure, out_of_scope = owned_path_classification(claim, changed)
    return content_address(
        {
            "schema_version": WORKSPACE_SCHEMA,
            **identity,
            "workspace_state": "dirty" if changed else "clean",
            "head_revision": head,
            "head_tree": tree,
            "tracked_paths": tracked,
            "tracked_patch_sha256": sha256_bytes(patch),
            "tracked_patch_base64": base64.b64encode(patch).decode("ascii"),
            "untracked_entries": entries,
            "claim_owned_changed_paths": in_scope,
            "scheduler_infrastructure_paths": infrastructure,
            "out_of_claim_changed_paths": out_of_scope,
        },
        "archive_sha256",
    )


def load_claims(path: Path) -> tuple[bytes, list[dict[str, Any]]]:
    if path.is_symlink() or not path.is_file():
        fail("claim ledger is missing or unsafe")
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    if (before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ):
        fail("claim ledger changed while it was read")
    try:
        value = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ArchiveError("claim ledger is not valid UTF-8 JSON") from exc
    claims = value.get("claims") if isinstance(value, dict) else None
    if not isinstance(claims, list) or any(not isinstance(row, dict) for row in claims):
        fail("claim ledger has no exact claims array")
    return data, claims


def build_archive(root: Path, runtime: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root = root.absolute()
    runtime = runtime.absolute()
    if not (root / ".git").exists():
        fail("repository root is not a Git checkout")
    if runtime.is_symlink() or not runtime.is_relative_to(root):
        fail("runtime root is unsafe")
    claims_path = runtime / "claims.json"
    claims_bytes, claims = load_claims(claims_path)
    claims_digest = sha256_bytes(claims_bytes)
    pause_paths = [runtime / "PAUSED", root / ".cron" / "stage1-rev56" / "PAUSED"]
    if any(path.is_symlink() or not path.is_file() for path in pause_paths):
        fail("both Stage1 pause markers must exist before frozen archival")
    deltas = [
        workspace_delta(
            root, runtime, claim, claim_index=index,
            claims_sha256=claims_digest,
        )
        for index, claim in enumerate(claims)
    ]
    blueprint = root / "Docs" / "Stage1_Blueprint_v2.md"
    if blueprint.is_symlink() or not blueprint.is_file():
        fail("Stage1 blueprint is missing or unsafe")
    manifest = content_address(
        {
            "schema_version": SCHEMA,
            "repository_head": git_text(root, "rev-parse", "HEAD^{commit}"),
            "repository_tree": git_text(root, "rev-parse", "HEAD^{tree}"),
            "blueprint_sha256": sha256_bytes(blueprint.read_bytes()),
            "claims_path": str(claims_path.relative_to(root)),
            "claims_sha256": claims_digest,
            "pause_marker_sha256s": {
                str(path.relative_to(root)): sha256_bytes(path.read_bytes())
                for path in pause_paths
            },
            "workspace_archives": [
                {
                    "claim_index": row["claim_index"],
                    "claim_id": row["claim_id"],
                    "slot": row["slot"],
                    "workspace_state": row["workspace_state"],
                    "archive_sha256": row["archive_sha256"],
                }
                for row in deltas
            ],
        },
        "manifest_sha256",
    )
    return manifest, deltas


def write_exclusive_or_verify(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    except FileExistsError:
        if path.is_symlink() or path.read_bytes() != data:
            fail(f"content-addressed archive collision: {path}")
        return
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def write_archive(runtime: Path, manifest: dict[str, Any], deltas: list[dict[str, Any]]) -> Path:
    destination = runtime / "frozen-archives"
    for row in deltas:
        digest = row.get("archive_sha256")
        if not isinstance(digest, str) or len(digest) != SHA256_RE_LENGTH:
            fail("workspace archive digest is malformed")
        write_exclusive_or_verify(destination / "workspaces" / f"{digest}.json", canonical_json(row) + b"\n")
    manifest_digest = manifest.get("manifest_sha256")
    if not isinstance(manifest_digest, str) or len(manifest_digest) != SHA256_RE_LENGTH:
        fail("archive manifest digest is malformed")
    path = destination / f"{manifest_digest}.json"
    write_exclusive_or_verify(path, canonical_json(manifest) + b"\n")
    return path


def retire_archived_claims(
    root: Path,
    runtime: Path,
    manifest: dict[str, Any],
    deltas: list[dict[str, Any]],
) -> Path:
    """Replace the frozen ledger with an empty cursor after exact archival.

    Workspaces are intentionally retained. Their content-addressed deltas and
    the old ledger digest remain recoverable through the immutable manifest.
    """
    rebuilt, repeated = build_archive(root, runtime)
    if rebuilt != manifest or repeated != deltas:
        fail("frozen runtime changed after archival; refuse claim retirement")
    manifest_path = runtime / "frozen-archives" / f"{manifest['manifest_sha256']}.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        fail("claim retirement requires the persisted archive manifest")
    expected_manifest = canonical_json(manifest) + b"\n"
    if manifest_path.read_bytes() != expected_manifest:
        fail("persisted archive manifest differs from the verified frozen runtime")
    claims_path = runtime / "claims.json"
    claims_bytes, claims = load_claims(claims_path)
    if sha256_bytes(claims_bytes) != manifest.get("claims_sha256"):
        fail("claim ledger changed before retirement")
    retirement = content_address(
        {
            "schema_version": RETIREMENT_SCHEMA,
            "archive_manifest_sha256": manifest["manifest_sha256"],
            "claims_sha256": manifest["claims_sha256"],
            "retired_claim_count": len(claims),
            "retired_claim_ids": [claim.get("claim_id") for claim in claims],
            "workspaces_retained": True,
            "pause_markers_retained": True,
        },
        "retirement_sha256",
    )
    retirement_path = (
        runtime
        / "frozen-archives"
        / "retirements"
        / f"{retirement['retirement_sha256']}.json"
    )
    write_exclusive_or_verify(retirement_path, canonical_json(retirement) + b"\n")
    empty = json.dumps(
        {
            "claims": [],
            "retired_archive_manifest_sha256": manifest["manifest_sha256"],
            "retirement_sha256": retirement["retirement_sha256"],
        },
        ensure_ascii=True,
        sort_keys=True,
        indent=2,
    ).encode("ascii") + b"\n"
    temporary = runtime / ".claims.json.retiring"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(empty)
            handle.flush()
            os.fsync(handle.fileno())
        if claims_path.is_symlink() or claims_path.read_bytes() != claims_bytes:
            fail("claim ledger changed during retirement")
        os.replace(temporary, claims_path)
        directory = os.open(runtime, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return retirement_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--runtime", type=Path)
    parser.add_argument("--write", action="store_true", help="persist content-addressed private archives")
    parser.add_argument(
        "--retire-claims",
        action="store_true",
        help="after --write, replace the archived frozen claim ledger with an empty cursor",
    )
    parser.add_argument("--output", type=Path, help="optional report destination")
    args = parser.parse_args()
    root = args.root.absolute()
    runtime = (args.runtime or root / ".cron" / "stage1-v2-app-server").absolute()
    manifest, deltas = build_archive(root, runtime)
    if args.write:
        archive_path = write_archive(runtime, manifest, deltas)
        print(f"archive={archive_path}")
        if args.retire_claims:
            retirement_path = retire_archived_claims(root, runtime, manifest, deltas)
            print(f"retirement={retirement_path}")
    elif args.retire_claims:
        fail("--retire-claims requires --write")
    report = {
        **manifest,
        "counts": {
            "claims": len(deltas),
            "dirty": sum(row["workspace_state"] == "dirty" for row in deltas),
            "clean": sum(row["workspace_state"] == "clean" for row in deltas),
            "missing": sum(row["workspace_state"] == "missing" for row in deltas),
            "ownership_mismatch": sum(bool(row["out_of_claim_changed_paths"]) for row in deltas),
            "incomplete_claim_metadata": sum(
                row["claim_metadata_state"] == "incomplete" for row in deltas
            ),
        },
    }
    rendered = json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="ascii")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
