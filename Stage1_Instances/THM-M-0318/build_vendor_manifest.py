#!/usr/bin/env python3
"""Verify the reversible THM-M-0318 Brouwer compatibility port."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "vendor-manifest.json"
VENDOR = HERE / "Vendor"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


manifest = json.loads(
    MANIFEST_PATH.read_text(encoding="utf-8"),
    object_pairs_hook=reject_duplicate_keys,
)
assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert manifest["item_id"] == "S56-M-0318-PROOF"
assert manifest["theorem_id"] == "THM-M-0318"

expected_sources = {row["path"] for row in manifest["files"]}
actual_sources = {
    path.relative_to(VENDOR).as_posix() for path in VENDOR.rglob("*.lean")
}
assert actual_sources == expected_sources, (actual_sources, expected_sources)
actual_files = {
    path.relative_to(VENDOR).as_posix()
    for path in VENDOR.rglob("*")
    if path.is_file()
}
assert actual_files == expected_sources | {"LICENSE"}, actual_files

assert sha256((VENDOR / "LICENSE").read_bytes()) == manifest["license"]["sha256"]

patch_stream = bytearray()
total_bytes = 0
total_lines = 0
for row in manifest["files"]:
    path = VENDOR / row["path"]
    data = path.read_bytes()
    assert sha256(data) == row["vendored_sha256"], row["path"]
    assert len(data) == row["vendored_bytes"], row["path"]
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    total_bytes += len(data)
    total_lines += len(data.splitlines())

    upstream = data
    for operation in reversed(row["compatibility_operations"]):
        kind = operation["kind"]
        if kind == "replace_once":
            old = operation["from"].encode("utf-8")
            new = operation["to"].encode("utf-8")
            assert upstream.count(new) == 1, (row["path"], new)
            upstream = upstream.replace(new, old, 1)
        elif kind == "append_once":
            addition = operation["bytes"].encode("utf-8").decode("unicode_escape").encode()
            upstream += addition
        else:
            raise AssertionError((row["path"], kind))
    assert sha256(upstream) == row["upstream_sha256"], row["path"]

    for operation in row["compatibility_operations"]:
        canonical = json.dumps(
            {"path": row["path"], **operation},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        patch_stream.extend(canonical.encode("ascii") + b"\n")

closure = manifest["closure"]
assert closure["module_count"] == len(manifest["files"])
assert closure["vendored_bytes"] == total_bytes
assert closure["vendored_lines"] == total_lines
patch_sha = sha256(bytes(patch_stream))
assert closure["normalized_compatibility_patch_sha256"] == patch_sha

print(
    "PASS THM-M-0318 vendor closure: "
    f"{len(manifest['files'])} modules, {total_bytes} bytes, reversible patch {patch_sha}"
)
