#!/usr/bin/env python3
"""Fail-closed integrity checks for the THM-M-1056 Oseledets vendor closure."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_vendor.py must not run with assertions disabled")


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "vendor-manifest.json"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, ("duplicate JSON key", key)
        value[key] = item
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_lean_comments_and_strings(source: str) -> str:
    """Erase nested comments, line comments, and string/character contents."""
    out: list[str] = []
    i = 0
    block_depth = 0
    in_string = False
    in_char = False
    escaped = False
    while i < len(source):
        pair = source[i : i + 2]
        char = source[i]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                i += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
            continue
        if in_string or in_char:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif in_string and char == '"':
                in_string = False
            elif in_char and char == "'":
                in_char = False
            i += 1
            continue
        if pair == "/-":
            block_depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            end = source.find("\n", i)
            if end == -1:
                out.extend(" " * (len(source) - i))
                i = len(source)
            else:
                out.extend(" " * (end - i))
                i = end
        elif char == '"':
            in_string = True
            out.append(" ")
            i += 1
        elif char == "'" and i + 2 < len(source) and source[i + 2] == "'":
            in_char = True
            out.append(" ")
            i += 1
        else:
            out.append(char)
            i += 1
    assert block_depth == 0 and not in_string and not in_char
    return "".join(out)


manifest = json.loads(
    MANIFEST_PATH.read_text(encoding="utf-8"),
    object_pairs_hook=reject_duplicate_keys,
)
assert manifest["schema_version"] == "stage1-vendored-source-closure/1.0"
assert manifest["item_id"] == "S56-M-1056-PROOF"
assert manifest["theorem_id"] == "THM-M-1056"

vendor = HERE / manifest["vendor_root"]
source_root = vendor / "ErgodicTheory"
expected_support = {
    "LICENSE",
    "lean429-port-complete.patch",
    "order.txt",
    "port-completion-report.md",
    "provenance-pins.tsv",
    "source-olean-hashes.tsv",
}
expected_sources = {row["path"] for row in manifest["files"]}
actual_sources = {
    path.relative_to(vendor).as_posix() for path in source_root.rglob("*.lean")
}
assert actual_sources == expected_sources, (actual_sources ^ expected_sources)
actual_files = {
    path.relative_to(vendor).as_posix()
    for path in vendor.rglob("*")
    if path.is_file()
}
assert actual_files == expected_sources | expected_support, actual_files ^ (
    expected_sources | expected_support
)

for name, expected in manifest["support_files"].items():
    assert sha256(vendor / name) == expected, name

order = (vendor / "order.txt").read_text(encoding="utf-8").splitlines()
assert order == manifest["build_order"]
assert len(order) == len(set(order)) == manifest["closure"]["module_count"] == 62
assert [row["module"] for row in manifest["files"]] == order

total_bytes = 0
total_lines = 0
for row in manifest["files"]:
    expected_path = row["module"].replace(".", "/") + ".lean"
    assert row["path"] == expected_path
    path = vendor / row["path"]
    assert sha256(path) == row["vendored_sha256"], row["path"]
    assert path.stat().st_size == row["vendored_bytes"], row["path"]
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    total_bytes += len(data)
    total_lines += len(data.splitlines())

    stripped = strip_lean_comments_and_strings(data.decode("utf-8"))
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    match = forbidden.search(stripped)
    assert match is None, (row["path"], match.group(0) if match else None)

closure = manifest["closure"]
assert closure["vendored_bytes"] == total_bytes
assert closure["vendored_lines"] == total_lines

with (vendor / "source-olean-hashes.tsv").open(encoding="utf-8", newline="") as stream:
    ledger = list(csv.DictReader(stream, delimiter="\t"))
assert len(ledger) == 62
for row, evidence in zip(manifest["files"], ledger, strict=True):
    assert int(evidence["index"]) == row["index"]
    assert evidence["module"] == row["module"]
    assert evidence["source_sha256"] == row["vendored_sha256"]
    assert int(evidence["source_bytes"]) == row["vendored_bytes"]
    assert evidence["olean_sha256"] == row["prior_validation_olean_sha256"]
    assert int(evidence["olean_bytes"]) == row["prior_validation_olean_bytes"]

pins: dict[str, str] = {}
for line in (vendor / "provenance-pins.tsv").read_text(encoding="utf-8").splitlines():
    key, value = line.split("\t", 1)
    assert key not in pins
    pins[key] = value
for key, expected in manifest["provenance_pins"].items():
    assert pins[key] == expected, key

# Reversing the checked compatibility patch must reconstruct the upstream bytes
# of exactly the 62 imported modules, without requiring a network checkout.
with tempfile.TemporaryDirectory(prefix="m1056-vendor-reverse-") as tmp_name:
    tmp = Path(tmp_name)
    for row in manifest["files"]:
        source = vendor / row["path"]
        target = tmp / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
    subprocess.run(
        ["patch", "-R", "-p1", "--batch", "--fuzz=0", "--input", str(vendor / "lean429-port-complete.patch")],
        cwd=tmp,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    for row in manifest["files"]:
        assert sha256(tmp / row["path"]) == row["upstream_sha256"], row["path"]

patch = (vendor / "lean429-port-complete.patch").read_text(encoding="utf-8")
patched_paths = [line.removeprefix("--- a/") for line in patch.splitlines() if line.startswith("--- a/")]
assert patched_paths == manifest["compatibility_port"]["modified_paths"]
assert len(patched_paths) == len(set(patched_paths)) == 26

if "--check-upstream" in sys.argv:
    upstream = Path(sys.argv[sys.argv.index("--check-upstream") + 1]).resolve()
    for row in manifest["files"]:
        assert sha256(upstream / row["path"]) == row["upstream_sha256"], row["path"]

print(
    "PASS THM-M-1056 vendor closure: "
    f"{len(order)} modules, {total_bytes} bytes, reversible 26-file port"
)
