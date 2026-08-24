#!/usr/bin/env python3
"""Freeze rights-cleared PutnamBench metadata and formal declaration assets."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
import tempfile
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR_REL = Path("Docs/catalog/v5/curation/putnambench_v5_6")
INVENTORY_REL = OUTPUT_DIR_REL / "PutnamBench_Source_Inventory_v5_6.json"
PROBLEMS_REL = OUTPUT_DIR_REL / "PutnamBench_Source_Problems_v5_6.jsonl"
VARIANTS_REL = OUTPUT_DIR_REL / "PutnamBench_Formal_Variants_v5_6.jsonl"
FORMAL_ASSET_REL = OUTPUT_DIR_REL / "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl"
FORBIDDEN_FULL_ARCHIVE_RELS = (
    Path("Docs/catalog/v5/sources/putnambench-dfb0a47a-source.tar.gz"),
    Path("Docs/catalog/v5/sources/putnambench-dfb0a47-source.tar.gz"),
)

UPSTREAM_REPOSITORY = "https://github.com/trishullab/PutnamBench"
UPSTREAM_COMMIT = "dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c"
UPSTREAM_TREE_SHA1 = "609c8623a81281f5442c0c4dc7e82dc015e97ed9"
EXTERNAL_ARCHIVE_URL = f"{UPSTREAM_REPOSITORY}/archive/{UPSTREAM_COMMIT}.tar.gz"
ARCHIVE_SHA256 = "843911c7eb432c0ce96ac1e6494f9675336a9be935884cd5b6de4575db042c30"
ARCHIVE_BYTE_LENGTH = 988_321
ARCHIVE_ROOT = f"PutnamBench-{UPSTREAM_COMMIT}"
SOURCE_SNAPSHOT_ID = f"putnambench:{UPSTREAM_COMMIT}"

EXPECTED_ARCHIVE_FILE_COUNT = 1_764
EXPECTED_COUNTS = {
    "all_problem_key_union": 675,
    "informal_records": 673,
    "informal_problem_key_union": 673,
    "formal_variants": 1_724,
    "formal_problem_key_union": 674,
    "lean4_variants": 672,
    "isabelle_variants": 640,
    "coq_variants": 412,
}
EXPECTED_INFORMAL_ONLY = ("putnam_1997_a1",)
EXPECTED_FORMAL_ONLY = ("putnam_1987_a3", "putnam_1996_a1")
EXPECTED_DECLARATION_NAME_MISMATCHES = {
    ("isabelle", "putnam_1980_b3"): "putnam_1980_a3",
    ("coq", "putnam_1968_a1"): "putnam_1968_b1",
    ("coq", "putnam_1970_b5"): "putnam_1970_b5_solution",
    ("coq", "putnam_1979_a6"): "putnam_1979_b6",
    ("coq", "putnam_1994_b3"): "putnam_1993_b3",
}
EXPECTED_PROOF_HOLE_COUNTS = {"lean4": 1_018, "isabelle": 641, "coq": 412}
EXPECTED_FILES_WITH_MULTIPLE_HOLES = {"lean4": 346, "isabelle": 1, "coq": 0}

EXPECTED_SOURCE_FILE_SHA256 = {
    "README.md": "6a157e86321ea08a11766c18e20d28b6204a73cd5a96285fffc918120c976758",
    "informal/README.md": "b25188d7fb6aaaacf979bf6d22333b4e4dc045ef6a6a948cdb763e6b831d7b03",
    "informal/putnam.json": "b2be6223c8790076e50735ef8f99e5b31c3ec9fe60d87dee00cec820b0a9c7d1",
    "lean4/LICENSE": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
    "isabelle/LICENSE": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
    "coq/LICENSE": "3b827918f5519d5f01e0197eedf478049de5cb21bbd91771f60f761fc08b0f0d",
}
MAA_PERMISSION_ASSERTION_LINE = 11
MAA_PERMISSION_ASSERTION_LINE_SHA256 = "0cbaa7aa0ac003cef8a3486534136cfc29f25b224c75c3251e5077e922fd265d"

PROBLEM_KEY_RE = re.compile(r"^putnam_(?P<year>[0-9]{4})_(?P<section>[ab])(?P<number>[1-6])$")
FORMAL_SOURCE_PATTERNS = {
    "lean4": re.compile(r"^lean4/src/(?P<key>putnam_[0-9]{4}_[ab][1-6])\.lean$"),
    "isabelle": re.compile(r"^isabelle/(?P<key>putnam_[0-9]{4}_[ab][1-6])\.thy$"),
    "coq": re.compile(r"^coq/src/(?P<key>putnam_[0-9]{4}_[ab][1-6])\.v$"),
}
DECLARATION_PATTERNS = {
    "lean4": re.compile(
        r"(?m)^[ \t]*(?:(?:private|protected)[ \t]+)?"
        r"(?P<kind>theorem|lemma)[ \t]+(?P<name>[A-Za-z_][A-Za-z0-9_']*)\b"
    ),
    "isabelle": re.compile(
        r"(?m)^[ \t]*(?P<kind>theorem|lemma)[ \t]+"
        r"(?P<name>[A-Za-z_][A-Za-z0-9_']*)[ \t]*:"
    ),
    "coq": re.compile(
        r"(?mi)^[ \t]*(?P<kind>Theorem|Lemma|Proposition|Corollary|Fact|Remark)[ \t]+"
        r"(?P<name>[A-Za-z_][A-Za-z0-9_']*)\b"
    ),
}
HOLE_PATTERNS = {
    "lean4": re.compile(r"\bsorry\b"),
    "isabelle": re.compile(r"\bsorry\b"),
    "coq": re.compile(r"\bAdmitted\s*\.", re.IGNORECASE),
}
LANGUAGE_ORDER = {"lean4": 0, "isabelle": 1, "coq": 2}
RIGHTS_IDS = {
    "lean4": "putnambench-lean4-apache-2.0",
    "isabelle": "putnambench-isabelle-apache-2.0",
    "coq": "putnambench-coq-mit",
    "informal": "putnambench-informal-maa-permission-no-license-assertion",
}


class FreezeError(RuntimeError):
    """Raised when a source or generated invariant fails closed."""


@dataclass(frozen=True)
class SourceFile:
    relative_path: str
    archive_member_path: str
    data: bytes
    git_mode: str


@dataclass(frozen=True)
class FrozenArchive:
    files: Mapping[str, SourceFile]
    archive_file_count: int
    git_tree_sha1: str


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FreezeError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def encoded_json(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def encoded_jsonl(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha256(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: Iterable[str]) -> str:
    return sha256(canonical(sorted(values)))


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise FreezeError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> Any:
    raise FreezeError(f"non-finite JSON number: {value}")


def strict_json_loads(payload: bytes, source: str) -> Any:
    try:
        text = payload.decode("utf-8", errors="strict")
        return json.loads(
            text,
            object_pairs_hook=strict_object,
            parse_constant=reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FreezeError(f"invalid strict JSON in {source}: {error}") from error


def git_object_sha1(kind: bytes, payload: bytes) -> bytes:
    header = kind + b" " + str(len(payload)).encode("ascii") + b"\0"
    return hashlib.sha1(header + payload).digest()  # noqa: S324 - Git object identity is SHA-1.


def git_blob_sha1(payload: bytes) -> str:
    return git_object_sha1(b"blob", payload).hex()


def reconstruct_git_tree_sha1(files: Mapping[str, SourceFile]) -> str:
    blob_ids = {path: git_object_sha1(b"blob", source.data) for path, source in files.items()}
    directories = {""}
    for path in files:
        parts = path.split("/")
        for index in range(1, len(parts)):
            directories.add("/".join(parts[:index]))

    tree_ids: dict[str, bytes] = {}
    ordered_directories = sorted(
        directories,
        key=lambda item: len(item.split("/")) if item else 0,
        reverse=True,
    )
    for directory in ordered_directories:
        prefix = f"{directory}/" if directory else ""
        entries: list[tuple[str, bool, str, bytes]] = []
        for path, blob_id in blob_ids.items():
            if not path.startswith(prefix):
                continue
            remainder = path[len(prefix) :]
            if "/" not in remainder:
                entries.append((remainder, False, files[path].git_mode, blob_id))
        for child in directories:
            if not child or not child.startswith(prefix):
                continue
            remainder = child[len(prefix) :]
            if "/" not in remainder:
                require(child in tree_ids, f"tree reconstruction order failed at {child}")
                entries.append((remainder, True, "40000", tree_ids[child]))
        entries.sort(key=lambda entry: entry[0].encode("utf-8") + (b"/" if entry[1] else b""))
        payload = b"".join(
            mode.encode("ascii") + b" " + name.encode("utf-8") + b"\0" + object_id
            for name, _is_directory, mode, object_id in entries
        )
        tree_ids[directory] = git_object_sha1(b"tree", payload)
    return tree_ids[""].hex()


def load_archive(path: Path) -> FrozenArchive:
    require(path.is_file(), f"pinned archive is missing: {path}")
    actual_archive_size = path.stat().st_size
    require(actual_archive_size == ARCHIVE_BYTE_LENGTH, f"archive byte length drifted: {actual_archive_size}")
    actual_archive_sha = file_sha256(path)
    require(actual_archive_sha == ARCHIVE_SHA256, f"archive SHA-256 drifted: {actual_archive_sha}")

    files: dict[str, SourceFile] = {}
    seen_members: set[str] = set()
    explicit_directories: set[str] = set()
    try:
        with tarfile.open(path, mode="r:gz") as archive:
            for member in archive.getmembers():
                pure = PurePosixPath(member.name)
                require(not pure.is_absolute(), f"absolute archive member: {member.name}")
                require(".." not in pure.parts, f"parent traversal archive member: {member.name}")
                require(pure.parts and pure.parts[0] == ARCHIVE_ROOT, f"unexpected archive root: {member.name}")
                normalized = pure.as_posix()
                require(normalized not in seen_members, f"duplicate archive member: {normalized}")
                seen_members.add(normalized)
                if len(pure.parts) == 1:
                    require(member.isdir(), "archive root is not a directory")
                    continue
                relative = PurePosixPath(*pure.parts[1:]).as_posix()
                if member.isdir():
                    explicit_directories.add(relative)
                    continue
                if member.isfile():
                    stream = archive.extractfile(member)
                    require(stream is not None, f"cannot read archive member: {normalized}")
                    data = stream.read()
                    git_mode = "100755" if member.mode & 0o111 else "100644"
                elif member.issym():
                    data = member.linkname.encode("utf-8")
                    git_mode = "120000"
                else:
                    raise FreezeError(f"unsupported archive member type: {normalized}")
                require(relative not in files, f"duplicate source path: {relative}")
                files[relative] = SourceFile(relative, normalized, data, git_mode)
    except tarfile.TarError as error:
        raise FreezeError(f"invalid tar archive: {error}") from error

    require(len(files) == EXPECTED_ARCHIVE_FILE_COUNT, f"archive file count drifted: {len(files)}")
    inferred_directories: set[str] = set()
    for relative in files:
        parts = relative.split("/")
        for index in range(1, len(parts)):
            inferred_directories.add("/".join(parts[:index]))
    require(
        explicit_directories <= inferred_directories,
        f"archive contains empty/unrepresented directories: {sorted(explicit_directories - inferred_directories)}",
    )

    tree_sha1 = reconstruct_git_tree_sha1(files)
    require(tree_sha1 == UPSTREAM_TREE_SHA1, f"reconstructed Git tree SHA-1 drifted: {tree_sha1}")
    for relative, expected in EXPECTED_SOURCE_FILE_SHA256.items():
        require(relative in files, f"required source file missing: {relative}")
        actual = sha256(files[relative].data)
        require(actual == expected, f"required source file drifted: {relative} ({actual})")
    require("LICENSE" not in files, "unexpected repository-root LICENSE appeared")
    require("informal/LICENSE" not in files, "unexpected informal-scoped LICENSE appeared")
    return FrozenArchive(files=files, archive_file_count=len(files), git_tree_sha1=tree_sha1)


def byte_position(payload: bytes, offset: int) -> tuple[int, int]:
    require(0 <= offset <= len(payload), f"byte offset outside payload: {offset}")
    line = payload.count(b"\n", 0, offset) + 1
    previous_newline = payload.rfind(b"\n", 0, offset)
    column = offset + 1 if previous_newline < 0 else offset - previous_newline
    return line, column


def span(payload: bytes, start: int, end: int) -> dict[str, int]:
    require(0 <= start <= end <= len(payload), f"invalid byte span: {start}:{end}")
    start_line, start_column = byte_position(payload, start)
    end_line, end_column = byte_position(payload, end)
    return {
        "start_byte": start,
        "end_byte_exclusive": end,
        "start_line": start_line,
        "start_column_utf8_byte": start_column,
        "end_line": end_line,
        "end_column_utf8_byte_exclusive": end_column,
    }


def full_file_binding(source: SourceFile) -> dict[str, Any]:
    return {
        "archive_member_path": source.archive_member_path,
        "upstream_relative_path": source.relative_path,
        "file_sha256": sha256(source.data),
        "byte_length": len(source.data),
        "git_blob_sha1": git_blob_sha1(source.data),
        "git_mode": source.git_mode,
    }


def top_level_array_element_spans(payload: bytes) -> list[tuple[int, int]]:
    whitespace = b" \t\r\n"
    length = len(payload)
    index = 0

    def skip_space(position: int) -> int:
        while position < length and payload[position] in whitespace:
            position += 1
        return position

    index = skip_space(index)
    require(index < length and payload[index] == ord("["), "informal JSON root is not an array")
    index = skip_space(index + 1)
    spans: list[tuple[int, int]] = []
    if index < length and payload[index] == ord("]"):
        index = skip_space(index + 1)
        require(index == length, "trailing bytes after informal JSON array")
        return spans

    while True:
        require(index < length and payload[index] == ord("{"), f"informal row is not an object at byte {index}")
        start = index
        depth = 0
        in_string = False
        escaped = False
        while index < length:
            byte = payload[index]
            if in_string:
                if escaped:
                    escaped = False
                elif byte == ord("\\"):
                    escaped = True
                elif byte == ord('"'):
                    in_string = False
            else:
                if byte == ord('"'):
                    in_string = True
                elif byte in (ord("{"), ord("[")):
                    depth += 1
                elif byte in (ord("}"), ord("]")):
                    depth -= 1
                    require(depth >= 0, f"unbalanced informal JSON at byte {index}")
                    if depth == 0:
                        index += 1
                        break
            index += 1
        require(depth == 0 and not in_string, "unterminated informal JSON row")
        spans.append((start, index))
        index = skip_space(index)
        require(index < length, "unterminated informal JSON array")
        if payload[index] == ord(","):
            index = skip_space(index + 1)
            continue
        require(payload[index] == ord("]"), f"expected comma or array end at byte {index}")
        index = skip_space(index + 1)
        require(index == length, "trailing bytes after informal JSON array")
        return spans


def char_byte_offsets(text: str) -> list[int]:
    offsets = [0]
    total = 0
    for character in text:
        total += len(character.encode("utf-8"))
        offsets.append(total)
    return offsets


def byte_span_from_match(
    payload: bytes,
    offsets: Sequence[int],
    start_character: int,
    end_character: int,
) -> tuple[dict[str, int], bytes]:
    start = offsets[start_character]
    end = offsets[end_character]
    return span(payload, start, end), payload[start:end]


def coordinate(problem_key: str) -> dict[str, Any]:
    match = PROBLEM_KEY_RE.fullmatch(problem_key)
    require(match is not None, f"invalid Putnam problem key: {problem_key}")
    return {
        "competition": "William Lowell Putnam Mathematical Competition",
        "year": int(match.group("year")),
        "section": match.group("section").upper(),
        "problem_number": int(match.group("number")),
    }


def seal(row: dict[str, Any]) -> dict[str, Any]:
    row["row_sha256"] = hash_without(row, "row_sha256")
    return row


def build_rights(archive: FrozenArchive) -> dict[str, Any]:
    rights: dict[str, Any] = {}
    for language, license_relative, expression in (
        ("lean4", "lean4/LICENSE", "Apache-2.0"),
        ("isabelle", "isabelle/LICENSE", "Apache-2.0"),
        ("coq", "coq/LICENSE", "MIT"),
    ):
        source = archive.files[license_relative]
        rights[language] = {
            "rights_id": RIGHTS_IDS[language],
            "scope": f"PutnamBench {language} formal source subtree only",
            "license_expression": expression,
            "attribution": {
                "upstream_repository": UPSTREAM_REPOSITORY,
                "upstream_commit": UPSTREAM_COMMIT,
                "source_subtree": {"lean4": "lean4", "isabelle": "isabelle", "coq": "coq"}[language],
            },
            "license_binding": {
                **full_file_binding(source),
                "full_file_span": span(source.data, 0, len(source.data)),
                "license_text_utf8": source.data.decode("utf-8", errors="strict"),
            },
            "applies_to_informal_statements": False,
        }

    readme = archive.files["README.md"]
    readme_lines = readme.data.splitlines(keepends=True)
    require(len(readme_lines) >= MAA_PERMISSION_ASSERTION_LINE, "README permission line disappeared")
    assertion = readme_lines[MAA_PERMISSION_ASSERTION_LINE - 1]
    require(
        sha256(assertion) == MAA_PERMISSION_ASSERTION_LINE_SHA256,
        "README MAA permission assertion line drifted",
    )
    assertion_start = sum(len(line) for line in readme_lines[: MAA_PERMISSION_ASSERTION_LINE - 1])
    assertion_end = assertion_start + len(assertion)
    rights["informal"] = {
        "rights_id": RIGHTS_IDS["informal"],
        "scope": "upstream README permission assertion for PutnamBench informal_statement fields only",
        "license_expression": "NOASSERTION",
        "informal_statement_permission_status": "upstream_repository_readme_asserts_MAA_permission",
        "informal_solution_permission_status": "not_established_by_the_bound_README_assertion",
        "permission_assertion_is_not_a_license": True,
        "repository_root_license_file_present": False,
        "informal_scoped_license_file_present": False,
        "inherits_lean4_isabelle_or_coq_license": False,
        "permission_assertion_binding": {
            "archive_member_path": readme.archive_member_path,
            "upstream_relative_path": readme.relative_path,
            "file_sha256": sha256(readme.data),
            "line_number": MAA_PERMISSION_ASSERTION_LINE,
            "line_span": span(readme.data, assertion_start, assertion_end),
            "line_sha256": sha256(assertion),
        },
        "derived_problem_rows_embed_exact_statement_or_solution_text": False,
    }
    return rights


def build_informal_bindings(archive: FrozenArchive) -> dict[str, dict[str, Any]]:
    source = archive.files["informal/putnam.json"]
    document = strict_json_loads(source.data, source.relative_path)
    require(isinstance(document, list), "informal JSON root is not a list")
    raw_spans = top_level_array_element_spans(source.data)
    require(len(document) == len(raw_spans) == EXPECTED_COUNTS["informal_records"], "informal denominator drifted")

    bindings: dict[str, dict[str, Any]] = {}
    for index, (record, (start, end)) in enumerate(zip(document, raw_spans, strict=True)):
        require(isinstance(record, dict), f"informal row {index} is not an object")
        require(
            set(record) == {"problem_name", "informal_statement", "informal_solution", "tags"},
            f"informal row field set drifted at index {index}",
        )
        problem_key = record.get("problem_name")
        require(isinstance(problem_key, str), f"informal row lacks problem_name at index {index}")
        coordinate(problem_key)
        require(problem_key not in bindings, f"duplicate informal problem_name: {problem_key}")
        require(isinstance(record.get("informal_statement"), str), f"informal statement is not text: {problem_key}")
        require(isinstance(record.get("informal_solution"), str), f"informal solution is not text: {problem_key}")
        tags = record.get("tags")
        require(isinstance(tags, list) and all(isinstance(tag, str) for tag in tags), f"informal tags invalid: {problem_key}")
        raw_record = source.data[start:end]
        reparsed = strict_json_loads(raw_record, f"{source.relative_path}#/{index}")
        require(reparsed == record, f"informal raw span does not replay: {problem_key}")
        base_pointer = f"/{index}"
        bindings[problem_key] = {
            **full_file_binding(source),
            "record_index": index,
            "json_pointer": base_pointer,
            "record_span": span(source.data, start, end),
            "record_raw_sha256": sha256(raw_record),
            "record_canonical_sha256": sha256(canonical(record)),
            "problem_name_pointer": f"{base_pointer}/problem_name",
            "problem_name_value_sha256": sha256(canonical(problem_key)),
            "statement_pointer": f"{base_pointer}/informal_statement",
            "statement_value_sha256": sha256(canonical(record["informal_statement"])),
            "solution_pointer": f"{base_pointer}/informal_solution",
            "solution_value_sha256": sha256(canonical(record["informal_solution"])),
            "tags_pointer": f"{base_pointer}/tags",
            "tags_value_sha256": sha256(canonical(tags)),
            "tag_count": len(tags),
            "rights_id": RIGHTS_IDS["informal"],
            "exact_statement_or_solution_text_embedded": False,
        }
    return bindings


def formal_sources(archive: FrozenArchive) -> dict[str, dict[str, SourceFile]]:
    result: dict[str, dict[str, SourceFile]] = {language: {} for language in LANGUAGE_ORDER}
    for relative, source in archive.files.items():
        for language, pattern in FORMAL_SOURCE_PATTERNS.items():
            match = pattern.fullmatch(relative)
            if match is None:
                continue
            problem_key = match.group("key")
            coordinate(problem_key)
            require(problem_key not in result[language], f"duplicate {language} problem key: {problem_key}")
            result[language][problem_key] = source
            break
    for language, count_key in (
        ("lean4", "lean4_variants"),
        ("isabelle", "isabelle_variants"),
        ("coq", "coq_variants"),
    ):
        require(len(result[language]) == EXPECTED_COUNTS[count_key], f"{language} source denominator drifted")
    return result


def formal_variant_id(language: str, problem_key: str) -> str:
    return f"putnambench::{UPSTREAM_COMMIT}::{problem_key}::{language}"


def build_formal_variant(language: str, problem_key: str, source: SourceFile) -> dict[str, Any]:
    try:
        text = source.data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise FreezeError(f"formal source is not UTF-8: {source.relative_path}") from error
    offsets = char_byte_offsets(text)
    declaration_matches = list(DECLARATION_PATTERNS[language].finditer(text))
    require(len(declaration_matches) == 1, f"expected one declaration in {source.relative_path}: {len(declaration_matches)}")
    declaration = declaration_matches[0]
    declared_name = declaration.group("name")
    kind = declaration.group("kind").lower()
    declaration_start = declaration.start("kind")

    hole_matches = list(HOLE_PATTERNS[language].finditer(text))
    require(hole_matches, f"no proof hole in {source.relative_path}")
    principal_candidates = [match for match in hole_matches if match.start() > declaration_start]
    require(
        len(principal_candidates) == 1,
        f"principal declaration proof-hole ambiguity in {source.relative_path}: {len(principal_candidates)}",
    )
    principal_hole = principal_candidates[0]
    principal_hole_index = hole_matches.index(principal_hole)

    if language == "lean4":
        prefix = text[declaration_start : principal_hole.start()]
        delimiters = list(re.finditer(r":=", prefix))
        require(delimiters, f"Lean declaration proof delimiter missing: {source.relative_path}")
        delimiter = delimiters[-1]
        header_end = declaration_start + delimiter.start()
        introducer_start = header_end
        introducer_end = principal_hole.start()
        introducer_text = text[introducer_start:introducer_end]
        require(
            re.fullmatch(r":=[ \t\r\n]*(?:by[ \t\r\n]*)?", introducer_text) is not None,
            f"unexpected Lean proof introducer: {source.relative_path}",
        )
    elif language == "isabelle":
        header_end = principal_hole.start()
        introducer_start = introducer_end = principal_hole.start()
    else:
        prefix = text[declaration_start : principal_hole.start()]
        proof_matches = list(re.finditer(r"\bProof\s*\.", prefix, re.IGNORECASE))
        require(len(proof_matches) == 1, f"Coq Proof delimiter ambiguity: {source.relative_path}")
        proof_match = proof_matches[0]
        header_end = declaration_start + proof_match.start()
        introducer_start = header_end
        introducer_end = principal_hole.start()

    header_span, header_payload = byte_span_from_match(
        source.data,
        offsets,
        declaration_start,
        header_end,
    )
    full_span, full_payload = byte_span_from_match(
        source.data,
        offsets,
        declaration_start,
        principal_hole.end(),
    )
    proof_introducer: dict[str, Any] | None
    if introducer_start == introducer_end:
        proof_introducer = None
    else:
        introducer_span, introducer_payload = byte_span_from_match(
            source.data,
            offsets,
            introducer_start,
            introducer_end,
        )
        proof_introducer = {"span": introducer_span, "sha256": sha256(introducer_payload)}

    proof_holes: list[dict[str, Any]] = []
    for index, hole in enumerate(hole_matches):
        hole_span, hole_payload = byte_span_from_match(source.data, offsets, hole.start(), hole.end())
        proof_holes.append(
            {
                "hole_index": index,
                "hole_kind": {
                    "lean4": "lean_sorry",
                    "isabelle": "isabelle_sorry",
                    "coq": "coq_admitted",
                }[language],
                "span": hole_span,
                "token_sha256": sha256(hole_payload),
                "is_principal_declaration_hole": index == principal_hole_index,
            }
        )

    mismatch_key = (language, problem_key)
    observed_mismatch = declared_name != problem_key
    expected_declared_name = EXPECTED_DECLARATION_NAME_MISMATCHES.get(mismatch_key)
    if expected_declared_name is None:
        require(not observed_mismatch, f"unregistered declaration-name mismatch: {source.relative_path} -> {declared_name}")
        anomaly_codes: list[str] = []
    else:
        require(observed_mismatch, f"registered mismatch disappeared: {source.relative_path}")
        require(declared_name == expected_declared_name, f"registered mismatch changed: {source.relative_path} -> {declared_name}")
        anomaly_codes = [f"{language}_declared_name_mismatch"]

    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/putnambench-formal-variant/5.6",
        "variant_id": formal_variant_id(language, problem_key),
        "problem_key": problem_key,
        "language": language,
        "source_binding": full_file_binding(source),
        "principal_declaration": {
            "kind": kind,
            "declared_name": declared_name,
            "expected_name": problem_key,
            "name_matches_problem_key": not observed_mismatch,
            "header_span": header_span,
            "header_sha256": sha256(header_payload),
            "proof_introducer_binding": proof_introducer,
            "full_declaration_span": full_span,
            "full_declaration_sha256": sha256(full_payload),
            "principal_hole_index": principal_hole_index,
            "source_proof_state": "placeholder_with_proof_hole",
        },
        "proof_holes": proof_holes,
        "rights_id": RIGHTS_IDS[language],
        "anomaly_codes": anomaly_codes,
    }
    return seal(row)


def bytes_at_span(payload: bytes, binding: Mapping[str, int]) -> bytes:
    start = binding["start_byte"]
    end = binding["end_byte_exclusive"]
    require(isinstance(start, int) and not isinstance(start, bool), "span start is not an integer")
    require(isinstance(end, int) and not isinstance(end, bool), "span end is not an integer")
    require(0 <= start <= end <= len(payload), f"span outside payload: {start}:{end}")
    return payload[start:end]


def build_formal_asset_row(variant: Mapping[str, Any], source: SourceFile) -> dict[str, Any]:
    language = variant["language"]
    declaration = variant["principal_declaration"]
    header_payload = bytes_at_span(source.data, declaration["header_span"])
    header_text = header_payload.decode("utf-8", errors="strict")
    require(sha256(header_payload) == declaration["header_sha256"], "formal asset header binding drifted")
    require(
        header_text.lstrip().lower().startswith(declaration["kind"]),
        f"formal asset header does not start at its declaration: {variant['variant_id']}",
    )
    if language == "lean4":
        require("/--" not in header_text, f"Lean docstring leaked into formal asset: {variant['variant_id']}")

    introducer_binding = declaration["proof_introducer_binding"]
    if introducer_binding is None:
        introducer_asset = None
    else:
        introducer_payload = bytes_at_span(source.data, introducer_binding["span"])
        require(sha256(introducer_payload) == introducer_binding["sha256"], "proof introducer binding drifted")
        introducer_asset = {
            "source_span": introducer_binding["span"],
            "sha256": introducer_binding["sha256"],
            "utf8": introducer_payload.decode("utf-8", errors="strict"),
        }

    hole_assets: list[dict[str, Any]] = []
    for hole in variant["proof_holes"]:
        hole_payload = bytes_at_span(source.data, hole["span"])
        require(sha256(hole_payload) == hole["token_sha256"], "proof-hole binding drifted")
        hole_assets.append(
            {
                "hole_index": hole["hole_index"],
                "hole_kind": hole["hole_kind"],
                "is_principal_declaration_hole": hole["is_principal_declaration_hole"],
                "source_span": hole["span"],
                "token_sha256": hole["token_sha256"],
                "token_utf8": hole_payload.decode("utf-8", errors="strict"),
            }
        )

    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/putnambench-formal-declaration-asset/5.6",
        "variant_id": variant["variant_id"],
        "problem_key": variant["problem_key"],
        "language": language,
        "external_source_binding": variant["source_binding"],
        "declaration_header": {
            "source_span": declaration["header_span"],
            "sha256": declaration["header_sha256"],
            "utf8": header_text,
        },
        "proof_introducer": introducer_asset,
        "proof_holes": hole_assets,
        "rights": {
            "rights_id": variant["rights_id"],
            "license_expression": {"lean4": "Apache-2.0", "isabelle": "Apache-2.0", "coq": "MIT"}[language],
            "attribution_ref": f"{INVENTORY_REL.as_posix()}#/rights/{language}",
        },
        "exclusions": {
            "full_source_file_included": False,
            "docstring_included": False,
            "informal_statement_included": False,
            "informal_solution_included": False,
            "supporting_definition_source_included": False,
        },
    }
    return seal(row)


def build(
    archive_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    archive = load_archive(archive_path)
    rights = build_rights(archive)
    informal = build_informal_bindings(archive)
    sources = formal_sources(archive)

    variants = [
        build_formal_variant(language, problem_key, source)
        for language in LANGUAGE_ORDER
        for problem_key, source in sources[language].items()
    ]
    variants.sort(key=lambda row: (row["problem_key"], LANGUAGE_ORDER[row["language"]]))
    require(len(variants) == EXPECTED_COUNTS["formal_variants"], "formal variant denominator drifted")
    formal_assets = [
        build_formal_asset_row(variant, sources[variant["language"]][variant["problem_key"]])
        for variant in variants
    ]
    require(len(formal_assets) == EXPECTED_COUNTS["formal_variants"], "formal asset denominator drifted")

    informal_document = strict_json_loads(
        archive.files["informal/putnam.json"].data,
        "informal/putnam.json",
    )
    require(isinstance(informal_document, list), "informal source ceased to be a list")
    formal_asset_code = "\n".join(
        piece
        for asset in formal_assets
        for piece in (
            asset["declaration_header"]["utf8"],
            asset["proof_introducer"]["utf8"] if asset["proof_introducer"] is not None else "",
            *(hole["token_utf8"] for hole in asset["proof_holes"]),
        )
    )
    for index, record in enumerate(informal_document):
        require(isinstance(record, dict), f"informal source row is not an object: {index}")
        for field in ("informal_statement", "informal_solution"):
            prose = record.get(field)
            require(isinstance(prose, str) and prose, f"informal prose field invalid: {index}/{field}")
            require(prose not in formal_asset_code, f"informal prose leaked into formal asset: {index}/{field}")

    formal_keys = set().union(*(set(by_key) for by_key in sources.values()))
    informal_keys = set(informal)
    all_keys = informal_keys | formal_keys
    require(len(formal_keys) == EXPECTED_COUNTS["formal_problem_key_union"], "formal key union drifted")
    require(len(informal_keys) == EXPECTED_COUNTS["informal_problem_key_union"], "informal key union drifted")
    require(len(all_keys) == EXPECTED_COUNTS["all_problem_key_union"], "all-component key union drifted")
    require(tuple(sorted(informal_keys - formal_keys)) == EXPECTED_INFORMAL_ONLY, "informal-only set drifted")
    require(tuple(sorted(formal_keys - informal_keys)) == EXPECTED_FORMAL_ONLY, "formal-only set drifted")

    variants_by_problem: dict[str, list[dict[str, Any]]] = {key: [] for key in all_keys}
    for variant in variants:
        variants_by_problem[variant["problem_key"]].append(variant)

    problems: list[dict[str, Any]] = []
    for problem_key in sorted(all_keys):
        problem_variants = variants_by_problem[problem_key]
        languages = {variant["language"] for variant in problem_variants}
        anomaly_codes: list[str] = []
        if problem_key in informal_keys - formal_keys:
            anomaly_codes.append("informal_only_no_formal_variant")
        if problem_key in formal_keys - informal_keys:
            anomaly_codes.append("formal_only_no_informal_record")
        if any(variant["anomaly_codes"] for variant in problem_variants):
            anomaly_codes.append("formal_declaration_name_mismatch")
        row = {
            "schema_version": "awesome-theorems/putnambench-source-problem/5.6",
            "problem_key": problem_key,
            "coordinate": coordinate(problem_key),
            "presence": {
                "informal": problem_key in informal,
                "lean4": "lean4" in languages,
                "isabelle": "isabelle" in languages,
                "coq": "coq" in languages,
            },
            "informal_binding": informal.get(problem_key),
            "formal_variant_ids": [variant["variant_id"] for variant in problem_variants],
            "anomaly_codes": anomaly_codes,
        }
        problems.append(seal(row))
    require(len(problems) == EXPECTED_COUNTS["all_problem_key_union"], "problem row denominator drifted")

    observed_mismatches = {
        (variant["language"], variant["problem_key"]): variant["principal_declaration"]["declared_name"]
        for variant in variants
        if not variant["principal_declaration"]["name_matches_problem_key"]
    }
    require(observed_mismatches == EXPECTED_DECLARATION_NAME_MISMATCHES, "declaration mismatch ledger drifted")
    proof_hole_counts = Counter()
    multiple_hole_counts = Counter()
    for variant in variants:
        language = variant["language"]
        proof_hole_counts[language] += len(variant["proof_holes"])
        multiple_hole_counts[language] += len(variant["proof_holes"]) > 1
    require(dict(proof_hole_counts) == EXPECTED_PROOF_HOLE_COUNTS, "proof-hole counts drifted")
    require(dict(multiple_hole_counts) == EXPECTED_FILES_WITH_MULTIPLE_HOLES, "multiple-hole file counts drifted")

    problems_payload = encoded_jsonl(problems)
    variants_payload = encoded_jsonl(variants)
    formal_assets_payload = encoded_jsonl(formal_assets)
    relevant_formal_files = [variant["source_binding"]["upstream_relative_path"] for variant in variants]
    known_anomalies = {
        "informal_only_problem_keys": list(EXPECTED_INFORMAL_ONLY),
        "formal_only_problem_keys": list(EXPECTED_FORMAL_ONLY),
        "declaration_name_mismatches": [
            {
                "language": language,
                "problem_key": problem_key,
                "declared_name": declared_name,
                "source_path": sources[language][problem_key].relative_path,
            }
            for (language, problem_key), declared_name in sorted(EXPECTED_DECLARATION_NAME_MISMATCHES.items())
        ],
    }
    inventory: dict[str, Any] = {
        "schema_version": "awesome-theorems/putnambench-source-inventory/5.6",
        "source_snapshot": {
            "source_snapshot_id": SOURCE_SNAPSHOT_ID,
            "upstream_repository": UPSTREAM_REPOSITORY,
            "upstream_commit": UPSTREAM_COMMIT,
            "upstream_git_tree_sha1": UPSTREAM_TREE_SHA1,
            "reconstructed_git_tree_sha1": archive.git_tree_sha1,
            "archive_sha256": ARCHIVE_SHA256,
            "archive_byte_length": ARCHIVE_BYTE_LENGTH,
            "external_archive_url": EXTERNAL_ARCHIVE_URL,
            "archive_root": ARCHIVE_ROOT,
            "archive_file_count": archive.archive_file_count,
            "archive_embedded_in_repository": False,
            "catalog_distributes_full_source_archive": False,
            "operator_supplied_external_archive_required_for_full_replay": True,
        },
        "span_convention": {
            "byte_offsets": "zero_based_half_open_UTF-8_bytes",
            "line_numbers": "one_based",
            "columns": "one_based_UTF-8_byte_columns",
            "end_positions": "exclusive",
        },
        "rights": rights,
        "outputs": {
            "problems": {
                "path": PROBLEMS_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(problems),
                "sha256": sha256(problems_payload),
            },
            "formal_variants": {
                "path": VARIANTS_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(variants),
                "sha256": sha256(variants_payload),
            },
            "formal_declaration_asset": {
                "path": FORMAL_ASSET_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(formal_assets),
                "sha256": sha256(formal_assets_payload),
            },
        },
        "counts": {
            **EXPECTED_COUNTS,
            "formal_variants_by_language": {
                language: sum(variant["language"] == language for variant in variants)
                for language in LANGUAGE_ORDER
            },
            "proof_holes_by_language": dict(sorted(proof_hole_counts.items())),
            "files_with_multiple_proof_holes_by_language": dict(sorted(multiple_hole_counts.items())),
            "declaration_name_mismatches_by_language": dict(
                sorted(Counter(language for language, _problem_key in observed_mismatches).items())
            ),
            "rights_cleared_formal_declaration_asset_rows": len(formal_assets),
        },
        "coverage": {
            "problem_key_union_is_complete_for_all_four_components": True,
            "every_formal_file_has_exactly_one_principal_declaration": True,
            "every_formal_principal_declaration_has_exactly_one_principal_proof_hole": True,
            "every_informal_record_has_exact_file_record_span_and_json_pointer_binding": True,
            "exact_informal_statement_or_solution_text_reproduced_in_derived_rows": False,
            "full_informal_source_replay_available_without_external_archive": False,
            "formal_asset_excludes_docstrings_supporting_definitions_and_full_source_files": True,
            "formal_source_file_count": len(relevant_formal_files),
        },
        "known_anomalies": known_anomalies,
        "set_digests": {
            "all_problem_keys_sha256": set_digest(all_keys),
            "informal_problem_keys_sha256": set_digest(informal_keys),
            "formal_problem_keys_sha256": set_digest(formal_keys),
            "formal_variant_ids_sha256": set_digest(variant["variant_id"] for variant in variants),
            "formal_source_paths_sha256": set_digest(relevant_formal_files),
            "problem_row_seals_sha256": set_digest(problem["row_sha256"] for problem in problems),
            "formal_variant_row_seals_sha256": set_digest(variant["row_sha256"] for variant in variants),
            "formal_asset_row_seals_sha256": set_digest(asset["row_sha256"] for asset in formal_assets),
        },
    }
    inventory["authority_sha256"] = hash_without(inventory, "authority_sha256")
    return inventory, problems, variants, formal_assets


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def output_payloads(
    inventory: Mapping[str, Any],
    problems: Sequence[Mapping[str, Any]],
    variants: Sequence[Mapping[str, Any]],
    formal_assets: Sequence[Mapping[str, Any]],
) -> dict[Path, bytes]:
    return {
        INVENTORY_REL: encoded_json(inventory),
        PROBLEMS_REL: encoded_jsonl(problems),
        VARIANTS_REL: encoded_jsonl(variants),
        FORMAL_ASSET_REL: encoded_jsonl(formal_assets),
    }


def require_exact_keys(value: Any, expected: set[str], label: str) -> Mapping[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    actual = set(value)
    require(actual == expected, f"{label} field set drifted: missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    return value


def require_nonnegative_int(value: Any, label: str) -> int:
    require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"{label} is not a nonnegative integer")
    return value


def check_sha256(value: Any, label: str) -> str:
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None, f"{label} is not SHA-256")
    return value


def load_jsonl_output(path: Path, label: str) -> tuple[list[dict[str, Any]], bytes]:
    require(path.is_file(), f"missing frozen output: {path}")
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), f"{label} lacks final newline")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(payload.splitlines(), start=1):
        require(line, f"blank JSONL row: {label}:{line_number}")
        row = strict_json_loads(line, f"{label}:{line_number}")
        require(isinstance(row, dict), f"non-object JSONL row: {label}:{line_number}")
        require(canonical(row) == line, f"noncanonical JSONL row: {label}:{line_number}")
        rows.append(row)
    return rows, payload


def validate_span_schema(value: Any, label: str) -> Mapping[str, Any]:
    source_span = require_exact_keys(
        value,
        {
            "start_byte",
            "end_byte_exclusive",
            "start_line",
            "start_column_utf8_byte",
            "end_line",
            "end_column_utf8_byte_exclusive",
        },
        label,
    )
    start = require_nonnegative_int(source_span["start_byte"], f"{label}.start_byte")
    end = require_nonnegative_int(source_span["end_byte_exclusive"], f"{label}.end_byte_exclusive")
    require(start <= end, f"{label} is reversed")
    for field in ("start_line", "start_column_utf8_byte", "end_line", "end_column_utf8_byte_exclusive"):
        require(require_nonnegative_int(source_span[field], f"{label}.{field}") >= 1, f"{label}.{field} is not positive")
    return source_span


def validate_source_binding(value: Any, label: str) -> Mapping[str, Any]:
    binding = require_exact_keys(
        value,
        {"archive_member_path", "upstream_relative_path", "file_sha256", "byte_length", "git_blob_sha1", "git_mode"},
        label,
    )
    require(isinstance(binding["archive_member_path"], str) and binding["archive_member_path"].startswith(f"{ARCHIVE_ROOT}/"), f"{label} member path drifted")
    require(isinstance(binding["upstream_relative_path"], str) and binding["upstream_relative_path"], f"{label} relative path invalid")
    check_sha256(binding["file_sha256"], f"{label}.file_sha256")
    require_nonnegative_int(binding["byte_length"], f"{label}.byte_length")
    require(isinstance(binding["git_blob_sha1"], str) and re.fullmatch(r"[0-9a-f]{40}", binding["git_blob_sha1"]) is not None, f"{label}.git_blob_sha1 invalid")
    require(binding["git_mode"] in {"100644", "100755", "120000"}, f"{label}.git_mode invalid")
    return binding


def validate_repo_only(repository_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    for relative in FORBIDDEN_FULL_ARCHIVE_RELS:
        require(not (repository_root / relative).exists(), f"full upstream archive must not be distributed: {relative}")

    inventory_path = repository_root / INVENTORY_REL
    require(inventory_path.is_file(), f"missing frozen output: {INVENTORY_REL}")
    inventory_payload = inventory_path.read_bytes()
    inventory = strict_json_loads(inventory_payload, INVENTORY_REL.as_posix())
    inventory = dict(
        require_exact_keys(
            inventory,
            {
                "schema_version",
                "source_snapshot",
                "span_convention",
                "rights",
                "outputs",
                "counts",
                "coverage",
                "known_anomalies",
                "set_digests",
                "authority_sha256",
            },
            "inventory",
        )
    )
    require(encoded_json(inventory) == inventory_payload, "inventory is not canonical JSON")
    require(inventory["schema_version"] == "awesome-theorems/putnambench-source-inventory/5.6", "inventory schema drifted")
    require(inventory["authority_sha256"] == hash_without(inventory, "authority_sha256"), "inventory authority mismatch")

    problems, problems_payload = load_jsonl_output(repository_root / PROBLEMS_REL, "problems")
    variants, variants_payload = load_jsonl_output(repository_root / VARIANTS_REL, "formal variants")
    formal_assets, formal_assets_payload = load_jsonl_output(repository_root / FORMAL_ASSET_REL, "formal assets")
    outputs = require_exact_keys(inventory["outputs"], {"problems", "formal_variants", "formal_declaration_asset"}, "inventory.outputs")
    for key, relative, rows, payload in (
        ("problems", PROBLEMS_REL, problems, problems_payload),
        ("formal_variants", VARIANTS_REL, variants, variants_payload),
        ("formal_declaration_asset", FORMAL_ASSET_REL, formal_assets, formal_assets_payload),
    ):
        descriptor = require_exact_keys(outputs[key], {"path", "media_type", "row_count", "sha256"}, f"inventory.outputs.{key}")
        require(descriptor["path"] == relative.as_posix(), f"output path drifted: {key}")
        require(descriptor["media_type"] == "application/x-ndjson", f"output media type drifted: {key}")
        require(descriptor["row_count"] == len(rows), f"output row count drifted: {key}")
        require(descriptor["sha256"] == sha256(payload), f"output digest drifted: {key}")

    source_snapshot = require_exact_keys(
        inventory["source_snapshot"],
        {
            "source_snapshot_id",
            "upstream_repository",
            "upstream_commit",
            "upstream_git_tree_sha1",
            "reconstructed_git_tree_sha1",
            "archive_sha256",
            "archive_byte_length",
            "external_archive_url",
            "archive_root",
            "archive_file_count",
            "archive_embedded_in_repository",
            "catalog_distributes_full_source_archive",
            "operator_supplied_external_archive_required_for_full_replay",
        },
        "inventory.source_snapshot",
    )
    require(source_snapshot["upstream_commit"] == UPSTREAM_COMMIT, "source commit drifted")
    require(source_snapshot["upstream_git_tree_sha1"] == UPSTREAM_TREE_SHA1, "source tree drifted")
    require(source_snapshot["reconstructed_git_tree_sha1"] == UPSTREAM_TREE_SHA1, "reconstructed tree drifted")
    require(source_snapshot["archive_sha256"] == ARCHIVE_SHA256, "source archive digest drifted")
    require(source_snapshot["archive_byte_length"] == ARCHIVE_BYTE_LENGTH, "source archive size drifted")
    require(source_snapshot["external_archive_url"] == EXTERNAL_ARCHIVE_URL, "external archive URL drifted")
    require(source_snapshot["archive_embedded_in_repository"] is False, "inventory falsely embeds full archive")
    require(source_snapshot["catalog_distributes_full_source_archive"] is False, "inventory falsely distributes full archive")
    require(source_snapshot["operator_supplied_external_archive_required_for_full_replay"] is True, "external replay boundary drifted")

    rights = require_exact_keys(inventory["rights"], {"lean4", "isabelle", "coq", "informal"}, "inventory.rights")
    for language, expression in (("lean4", "Apache-2.0"), ("isabelle", "Apache-2.0"), ("coq", "MIT")):
        entry = rights[language]
        require(entry["license_expression"] == expression, f"formal license drifted: {language}")
        require(entry["applies_to_informal_statements"] is False, f"formal license leaked to informal: {language}")
        license_binding = entry["license_binding"]
        license_text = license_binding["license_text_utf8"]
        require(isinstance(license_text, str), f"embedded license text missing: {language}")
        require(sha256(license_text.encode("utf-8")) == license_binding["file_sha256"], f"embedded license text drifted: {language}")
    informal_rights = rights["informal"]
    require(informal_rights["license_expression"] == "NOASSERTION", "informal license overclaim")
    require(informal_rights["informal_solution_permission_status"] == "not_established_by_the_bound_README_assertion", "informal solution permission overclaim")
    require(informal_rights["inherits_lean4_isabelle_or_coq_license"] is False, "informal license inheritance overclaim")

    problem_keys: set[str] = set()
    variant_ids: set[str] = set()
    variants_by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(problems):
        row = dict(require_exact_keys(row, {"schema_version", "problem_key", "coordinate", "presence", "informal_binding", "formal_variant_ids", "anomaly_codes", "row_sha256"}, f"problem[{index}]"))
        require(row["schema_version"] == "awesome-theorems/putnambench-source-problem/5.6", f"problem schema drifted: {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"problem row seal mismatch: {index}")
        problem_key = row["problem_key"]
        require(isinstance(problem_key, str) and problem_key not in problem_keys, f"duplicate/invalid problem key: {problem_key}")
        problem_keys.add(problem_key)
        require(row["coordinate"] == coordinate(problem_key), f"problem coordinate drifted: {problem_key}")
        require_exact_keys(row["presence"], {"informal", "lean4", "isabelle", "coq"}, f"problem presence: {problem_key}")
        require(all(isinstance(value, bool) for value in row["presence"].values()), f"problem presence type drifted: {problem_key}")
        require(isinstance(row["formal_variant_ids"], list) and all(isinstance(item, str) for item in row["formal_variant_ids"]), f"problem variant IDs invalid: {problem_key}")
        binding = row["informal_binding"]
        if binding is not None:
            binding = require_exact_keys(
                binding,
                {
                    "archive_member_path", "upstream_relative_path", "file_sha256", "byte_length", "git_blob_sha1", "git_mode",
                    "record_index", "json_pointer", "record_span", "record_raw_sha256", "record_canonical_sha256",
                    "problem_name_pointer", "problem_name_value_sha256", "statement_pointer", "statement_value_sha256",
                    "solution_pointer", "solution_value_sha256", "tags_pointer", "tags_value_sha256", "tag_count",
                    "rights_id", "exact_statement_or_solution_text_embedded",
                },
                f"informal binding: {problem_key}",
            )
            validate_source_binding({key: binding[key] for key in ("archive_member_path", "upstream_relative_path", "file_sha256", "byte_length", "git_blob_sha1", "git_mode")}, f"informal source: {problem_key}")
            record_index = require_nonnegative_int(binding["record_index"], f"informal record index: {problem_key}")
            base = f"/{record_index}"
            require(binding["json_pointer"] == base, f"informal base pointer drifted: {problem_key}")
            require(binding["problem_name_pointer"] == f"{base}/problem_name", f"problem name pointer drifted: {problem_key}")
            require(binding["statement_pointer"] == f"{base}/informal_statement", f"statement pointer drifted: {problem_key}")
            require(binding["solution_pointer"] == f"{base}/informal_solution", f"solution pointer drifted: {problem_key}")
            require(binding["tags_pointer"] == f"{base}/tags", f"tags pointer drifted: {problem_key}")
            require(binding["problem_name_value_sha256"] == sha256(canonical(problem_key)), f"problem name value hash drifted: {problem_key}")
            validate_span_schema(binding["record_span"], f"record span: {problem_key}")
            for field in ("record_raw_sha256", "record_canonical_sha256", "statement_value_sha256", "solution_value_sha256", "tags_value_sha256"):
                check_sha256(binding[field], f"{problem_key}.{field}")
            require(binding["exact_statement_or_solution_text_embedded"] is False, f"informal prose embedding overclaim: {problem_key}")

    for index, row in enumerate(variants):
        row = dict(require_exact_keys(row, {"schema_version", "variant_id", "problem_key", "language", "source_binding", "principal_declaration", "proof_holes", "rights_id", "anomaly_codes", "row_sha256"}, f"variant[{index}]"))
        require(row["schema_version"] == "awesome-theorems/putnambench-formal-variant/5.6", f"variant schema drifted: {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"variant row seal mismatch: {index}")
        variant_id = row["variant_id"]
        require(isinstance(variant_id, str) and variant_id not in variant_ids, f"duplicate/invalid variant ID: {variant_id}")
        variant_ids.add(variant_id)
        variants_by_id[variant_id] = row
        require(row["problem_key"] in problem_keys, f"variant problem missing: {variant_id}")
        require(row["language"] in LANGUAGE_ORDER, f"variant language invalid: {variant_id}")
        validate_source_binding(row["source_binding"], f"variant source: {variant_id}")
        declaration = require_exact_keys(
            row["principal_declaration"],
            {"kind", "declared_name", "expected_name", "name_matches_problem_key", "header_span", "header_sha256", "proof_introducer_binding", "full_declaration_span", "full_declaration_sha256", "principal_hole_index", "source_proof_state"},
            f"variant declaration: {variant_id}",
        )
        validate_span_schema(declaration["header_span"], f"variant header span: {variant_id}")
        validate_span_schema(declaration["full_declaration_span"], f"variant full span: {variant_id}")
        check_sha256(declaration["header_sha256"], f"variant header hash: {variant_id}")
        check_sha256(declaration["full_declaration_sha256"], f"variant declaration hash: {variant_id}")
        if declaration["proof_introducer_binding"] is not None:
            intro = require_exact_keys(declaration["proof_introducer_binding"], {"span", "sha256"}, f"variant proof intro: {variant_id}")
            validate_span_schema(intro["span"], f"variant proof intro span: {variant_id}")
            check_sha256(intro["sha256"], f"variant proof intro hash: {variant_id}")
        require(isinstance(row["proof_holes"], list) and row["proof_holes"], f"variant proof holes missing: {variant_id}")
        for hole_index, hole in enumerate(row["proof_holes"]):
            hole = require_exact_keys(hole, {"hole_index", "hole_kind", "span", "token_sha256", "is_principal_declaration_hole"}, f"variant hole: {variant_id}/{hole_index}")
            require(hole["hole_index"] == hole_index, f"variant hole index drifted: {variant_id}/{hole_index}")
            validate_span_schema(hole["span"], f"variant hole span: {variant_id}/{hole_index}")
            check_sha256(hole["token_sha256"], f"variant hole hash: {variant_id}/{hole_index}")

    asset_ids: set[str] = set()
    for index, row in enumerate(formal_assets):
        row = dict(require_exact_keys(row, {"schema_version", "variant_id", "problem_key", "language", "external_source_binding", "declaration_header", "proof_introducer", "proof_holes", "rights", "exclusions", "row_sha256"}, f"asset[{index}]"))
        require(row["schema_version"] == "awesome-theorems/putnambench-formal-declaration-asset/5.6", f"asset schema drifted: {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"asset row seal mismatch: {index}")
        variant_id = row["variant_id"]
        require(variant_id in variants_by_id and variant_id not in asset_ids, f"asset variant ID invalid: {variant_id}")
        asset_ids.add(variant_id)
        variant = variants_by_id[variant_id]
        require(row["problem_key"] == variant["problem_key"] and row["language"] == variant["language"], f"asset identity mismatch: {variant_id}")
        require(row["external_source_binding"] == variant["source_binding"], f"asset source mismatch: {variant_id}")
        header = require_exact_keys(row["declaration_header"], {"source_span", "sha256", "utf8"}, f"asset header: {variant_id}")
        require(header["source_span"] == variant["principal_declaration"]["header_span"], f"asset header span mismatch: {variant_id}")
        require(header["sha256"] == variant["principal_declaration"]["header_sha256"], f"asset header binding mismatch: {variant_id}")
        require(isinstance(header["utf8"], str) and sha256(header["utf8"].encode("utf-8")) == header["sha256"], f"asset header content mismatch: {variant_id}")
        require(header["utf8"].lstrip().lower().startswith(variant["principal_declaration"]["kind"]), f"asset header boundary drifted: {variant_id}")
        require("/--" not in header["utf8"], f"docstring leaked into asset: {variant_id}")
        variant_intro = variant["principal_declaration"]["proof_introducer_binding"]
        if variant_intro is None:
            require(row["proof_introducer"] is None, f"asset proof intro appeared: {variant_id}")
        else:
            asset_intro = require_exact_keys(row["proof_introducer"], {"source_span", "sha256", "utf8"}, f"asset proof intro: {variant_id}")
            require(asset_intro["source_span"] == variant_intro["span"] and asset_intro["sha256"] == variant_intro["sha256"], f"asset proof intro binding mismatch: {variant_id}")
            require(sha256(asset_intro["utf8"].encode("utf-8")) == asset_intro["sha256"], f"asset proof intro content mismatch: {variant_id}")
        require(len(row["proof_holes"]) == len(variant["proof_holes"]), f"asset hole count mismatch: {variant_id}")
        for asset_hole, variant_hole in zip(row["proof_holes"], variant["proof_holes"], strict=True):
            asset_hole = require_exact_keys(asset_hole, {"hole_index", "hole_kind", "is_principal_declaration_hole", "source_span", "token_sha256", "token_utf8"}, f"asset hole: {variant_id}")
            require(asset_hole["hole_index"] == variant_hole["hole_index"], f"asset hole index mismatch: {variant_id}")
            require(asset_hole["hole_kind"] == variant_hole["hole_kind"], f"asset hole kind mismatch: {variant_id}")
            require(asset_hole["source_span"] == variant_hole["span"], f"asset hole span mismatch: {variant_id}")
            require(asset_hole["token_sha256"] == variant_hole["token_sha256"], f"asset hole hash mismatch: {variant_id}")
            require(sha256(asset_hole["token_utf8"].encode("utf-8")) == asset_hole["token_sha256"], f"asset hole content mismatch: {variant_id}")
            expected_token = "Admitted." if row["language"] == "coq" else "sorry"
            require(asset_hole["token_utf8"] == expected_token, f"asset hole token drifted: {variant_id}")
        exclusions = require_exact_keys(row["exclusions"], {"full_source_file_included", "docstring_included", "informal_statement_included", "informal_solution_included", "supporting_definition_source_included"}, f"asset exclusions: {variant_id}")
        require(all(value is False for value in exclusions.values()), f"asset exclusion flag drifted: {variant_id}")
        asset_rights = require_exact_keys(row["rights"], {"rights_id", "license_expression", "attribution_ref"}, f"asset rights: {variant_id}")
        require(asset_rights["rights_id"] == variant["rights_id"], f"asset rights ID mismatch: {variant_id}")
    require(asset_ids == variant_ids, "formal asset does not cover every variant exactly once")

    counts = inventory["counts"]
    require(len(problems) == counts["all_problem_key_union"] == EXPECTED_COUNTS["all_problem_key_union"], "problem denominator drifted")
    require(len(variants) == counts["formal_variants"] == EXPECTED_COUNTS["formal_variants"], "variant denominator drifted")
    require(len(formal_assets) == counts["rights_cleared_formal_declaration_asset_rows"], "formal asset denominator drifted")
    set_digests = inventory["set_digests"]
    require(set_digests["all_problem_keys_sha256"] == set_digest(problem_keys), "problem key set digest drifted")
    require(set_digests["formal_variant_ids_sha256"] == set_digest(variant_ids), "variant ID set digest drifted")
    require(set_digests["problem_row_seals_sha256"] == set_digest(row["row_sha256"] for row in problems), "problem seal set digest drifted")
    require(set_digests["formal_variant_row_seals_sha256"] == set_digest(row["row_sha256"] for row in variants), "variant seal set digest drifted")
    require(set_digests["formal_asset_row_seals_sha256"] == set_digest(row["row_sha256"] for row in formal_assets), "asset seal set digest drifted")
    return inventory, problems, variants, formal_assets


def compare_full_rebuild(repository_root: Path, archive_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    inventory, problems, variants, formal_assets = build(archive_path)
    payloads = output_payloads(inventory, problems, variants, formal_assets)
    for relative, expected in payloads.items():
        output = repository_root / relative
        require(output.is_file(), f"missing frozen output: {relative}")
        require(output.read_bytes() == expected, f"frozen output is not a deterministic full-source rebuild: {relative}")
    validate_repo_only(repository_root)
    return inventory, problems, variants, formal_assets


def run(args: argparse.Namespace) -> int:
    repository_root = args.repo_root.resolve()
    if args.write:
        require(args.source_archive is not None, "--write requires --source-archive PATH")
        inventory, problems, variants, formal_assets = build(args.source_archive.resolve())
        for relative, payload in output_payloads(inventory, problems, variants, formal_assets).items():
            atomic_write(repository_root / relative, payload)
        validate_repo_only(repository_root)
        action = "WROTE"
    elif args.check:
        require(args.source_archive is None, "--check is repository-only and does not accept --source-archive")
        inventory, problems, variants, formal_assets = validate_repo_only(repository_root)
        action = "PASS"
    else:
        require(args.audit_source_archive is not None, "audit archive path missing")
        require(args.source_archive is None, "--audit-source-archive does not accept --source-archive")
        inventory, problems, variants, formal_assets = compare_full_rebuild(
            repository_root,
            args.audit_source_archive.resolve(),
        )
        action = "AUDIT PASS"
    print(
        f"{action} PutnamBench source freeze problems={len(problems)} informal={EXPECTED_COUNTS['informal_records']} "
        f"formal_variants={len(variants)} formal_assets={len(formal_assets)} "
        f"formal_keys={EXPECTED_COUNTS['formal_problem_key_union']} authority={inventory['authority_sha256']}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the four rights-cleared frozen outputs")
    mode.add_argument("--check", action="store_true", help="validate the repository-only rights-cleared outputs")
    mode.add_argument(
        "--audit-source-archive",
        type=Path,
        metavar="PATH",
        help="read-only full replay against an operator-supplied pinned tar.gz",
    )
    parser.add_argument("--source-archive", type=Path, help="operator-supplied pinned tar.gz required by --write")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="repository root for output paths")
    args = parser.parse_args()
    try:
        return run(args)
    except (FreezeError, OSError, ValueError) as error:
        print(f"FAIL PutnamBench source freeze: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
