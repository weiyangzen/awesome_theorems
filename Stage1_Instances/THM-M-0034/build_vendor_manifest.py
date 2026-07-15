#!/usr/bin/env python3
"""Fail-closed verification of the reversible THM-M-0034 compatibility port."""

from __future__ import annotations

import hashlib
import json
from difflib import unified_diff
from pathlib import Path


HERE = Path(__file__).resolve().parent
VENDOR = HERE / "Vendor"
MANIFEST = HERE / "vendor-manifest.json"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(
    data: bytes, old: bytes, new: bytes, label: str, expected_count: int = 1
) -> bytes:
    assert data.count(old) == expected_count, (label, data.count(old), expected_count)
    return data.replace(old, new, 1)


manifest = json.loads(
    MANIFEST.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
)
assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert manifest["item_id"] == "S56-M-0034-PROOF"
assert manifest["theorem_id"] == "THM-M-0034"
assert [row["path"] for row in manifest["files"]] == sorted(
    row["path"] for row in manifest["files"]
)

expected_sources = {row["path"] for row in manifest["files"]}
actual_sources = {
    path.relative_to(VENDOR).as_posix() for path in VENDOR.rglob("*.lean")
}
actual_files = {
    path.relative_to(VENDOR).as_posix()
    for path in VENDOR.rglob("*")
    if path.is_file()
}
assert actual_sources == expected_sources
assert actual_files == expected_sources | {"LICENSE"}
assert digest((VENDOR / "LICENSE").read_bytes()) == manifest["license"]["sha256"]

canonical_operations = bytearray()
normalized_diff: list[str] = []
total_bytes = 0
total_lines = 0
internal_import_edges = 0

for row in manifest["files"]:
    name = row["path"]
    path = VENDOR / name
    vendored = path.read_bytes()
    assert digest(vendored) == row["vendored_sha256"], name
    assert len(vendored) == row["vendored_bytes"], name
    assert vendored.endswith(b"\n") and b"\r" not in vendored and b"\x00" not in vendored
    total_bytes += len(vendored)
    total_lines += len(vendored.splitlines())
    internal_import_edges += vendored.count(
        b"import \xc2\xabStage1_Instances\xc2\xbb.\xc2\xabTHM-M-0034\xc2\xbb.Vendor.QuillenSuslin."
    )

    upstream = vendored
    for operation in row["compatibility_operations"]:
        kind = operation["kind"]
        if kind == "replace_once":
            before = operation["from"].encode("utf-8")
            after = operation["to"].encode("utf-8")
            upstream = replace_once(
                upstream, after, before, name, operation.get("expected_to_count", 1)
            )
        elif kind == "insert_once_after":
            anchor = operation["anchor"].encode("utf-8")
            addition = operation["bytes"].encode("utf-8")
            assert upstream.count(anchor + addition) == 1, name
            upstream = upstream.replace(anchor + addition, anchor, 1)
        else:
            raise AssertionError((name, kind))
    assert digest(upstream) == row["upstream_sha256"], name
    assert len(upstream) == row["upstream_bytes"], name
    assert row["modified"] is (upstream != vendored), name

    for operation in row["compatibility_operations"]:
        encoded = json.dumps(
            {"path": name, **operation},
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
        canonical_operations.extend(encoded + b"\n")
    if upstream != vendored:
        semantic = vendored
        for operation in row["compatibility_operations"]:
            if operation["kind"] == "insert_once_after":
                anchor = operation["anchor"].encode("utf-8")
                addition = operation["bytes"].encode("utf-8")
                assert semantic.count(anchor + addition) == 1, name
                semantic = semantic.replace(anchor + addition, anchor, 1)
            elif operation.get("scope") == "localization":
                before = operation["from"].encode("utf-8")
                after = operation["to"].encode("utf-8")
                semantic = replace_once(
                    semantic, after, before, name, operation.get("expected_to_count", 1)
                )
        normalized_diff.extend(
            unified_diff(
                upstream.decode("utf-8").splitlines(keepends=True),
                semantic.decode("utf-8").splitlines(keepends=True),
                fromfile=f"a/{name}",
                tofile=f"b/{name}",
                n=3,
                lineterm="\n",
            )
        )

closure = manifest["closure"]
assert closure["module_count"] == len(manifest["files"])
assert closure["internal_import_edges"] == internal_import_edges
assert closure["vendored_bytes"] == total_bytes
assert closure["vendored_lines"] == total_lines
patch_sha = digest(bytes(canonical_operations))
semantic_sha = digest("".join(normalized_diff).encode("utf-8"))
assert closure["normalized_compatibility_patch_sha256"] == patch_sha
assert closure["semantic_diff_sha256"] == semantic_sha

print(
    "PASS THM-M-0034 vendor closure: "
    f"{len(manifest['files'])} modules, {total_lines} lines, {total_bytes} bytes"
)
print(f"normalized compatibility patch sha256: {patch_sha}")
print(f"normalized semantic diff sha256: {semantic_sha}")
