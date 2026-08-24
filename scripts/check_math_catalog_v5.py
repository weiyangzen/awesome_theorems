#!/usr/bin/env python3
"""Independent verifier for the Stage5 mathematics catalog releases.

This module intentionally does not import the Stage5 generator or any source
extractor.  It rebuilds the release sets, hashes, source slices, numbering,
migration coverage, and theorem/open projections from the checked-in
authorities and pinned source assets.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
from typing import Any, Iterable, Mapping, Sequence
import unicodedata

try:
    import jsonschema
except ImportError:  # pragma: no cover - CI/repository environments provide it.
    jsonschema = None


CONTRACT_PATH = Path("Docs/catalog/v5/Stage5_Math_Expansion_Contract_v5.json")
SCHEMA_PATH = Path("Docs/catalog/v5/Math_Claim_Record_Schema_v5.json")
SOURCE_REGISTRY_PATH = Path("Docs/catalog/v5/Math_Source_Registry_v5.json")
V4_IMPORT_RECEIPT_PATH = Path("Docs/catalog/v5/V4_Import_Receipt_v5.json")
V4_CATALOG_PATH = Path("Docs/catalog/v4/Claim_Catalog_v4.json")
V4_REGISTRY_PATH = Path("Docs/catalog/v4/Claim_ID_Registry_v4.json")
V4_SOURCE_RECORDS_PATH = Path("Docs/catalog/v4/Source_Records_v4.json")
V4_STAGE_REGISTRY_PATH = Path("Docs/catalog/v4/Stage4_Claim_ID_Registry_v4.json")
V5_ROOT = Path("Docs/catalog/v5")

RELEASES = ("5.0", "5.1")
RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"

PARENT_HIGH_WATERMARK = 3484
PARENT_FAMILY_HIGH_WATERMARK = 3254
FIRST_STAGE5_ORDINAL = 3485
PINNED_CANDIDATE_COUNT = 2778
PINNED_EXTRACTION_JSONL_SHA256 = (
    "7ec09ebc21475a41b62127fb05eb48aff90577c65b1f6b85c5ebfb11680ce2f7"
)
PINNED_FORMAL_SOURCE_ID = "SRC-MATH-V5-FORMAL-CONJECTURES-2270D31E"
PINNED_FORMAL_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"
REVIEW_DATE = "2026-08-10"
FORMAL_SOURCE_REPOSITORY = "https://github.com/google-deepmind/formal-conjectures"
FORMAL_SOURCE_SCHEMA_VERSION = "awesome-theorems/formal-conjectures-source-block/5.0"
FORMAL_SELECTED_CATEGORIES = {"research open", "research solved", "textbook"}
MSC2020_TOP_LEVEL = {
    "00", "01", "03", "05", "06", "08", "11", "12", "13", "14",
    "15", "16", "17", "18", "19", "20", "22", "26", "28", "30",
    "31", "32", "33", "34", "35", "37", "39", "40", "41", "42",
    "43", "44", "45", "46", "47", "49", "51", "52", "53", "54",
    "55", "57", "58", "60", "62", "65", "68", "70", "74", "76",
    "78", "80", "81", "82", "83", "85", "86", "90", "91", "92",
    "93", "94", "97",
}
MINIMUMS = {
    "5.0": {"theorem": 1000, "open": 1000},
    "5.1": {"theorem": 500, "open": 0},
}

ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
ATO_RE = re.compile(r"^ATO-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
ATS_RE = re.compile(r"^ATS-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
QUALIFIED_NAME_RE = re.compile(r"^[^\s].*[^\s]$|^[^\s]$")
FORMAL_DECLARATION_RE = re.compile(r"\b(theorem|lemma)\b")
FORMAL_SCOPE_RE = re.compile(
    r"(?m)^[ \t]*(?:(noncomputable)[ \t]+)?(namespace|section|end)\b([^\n]*)"
)
FORMAL_IMPORT_RE = re.compile(r"(?m)^[ \t]*import[ \t]+([^\s]+)")
FORMAL_MODIFIER_RE = re.compile(
    r"(?:(?:private|protected|noncomputable|unsafe)\s*)*\Z"
)
FORMAL_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_']*")

THEOREM_KINDS = {
    "theorem",
    "lemma",
    "corollary",
    "proposition",
    "result",
    "identity",
    "inequality",
    "complexity_result",
    "impossibility_result",
    "undecidability_result",
}
OPEN_KINDS = {"conjecture", "hypothesis", "open_problem", "assumption"}
OPEN_STATUSES = {"open", "partial", "independent", "conditional", "disputed"}

MANIFEST_FIELDS = {
    "schema_version",
    "release",
    "parent_release",
    "parent_release_root_sha256",
    "release_root_sha256",
    "artifacts",
    "counts",
    "authority_sha256",
}
MANIFEST_ARTIFACT_FIELDS = {"path", "sha256", "size_bytes", "row_count"}


class CheckFailure(RuntimeError):
    """Raised for malformed input that prevents meaningful continuation."""


@dataclass(frozen=True)
class FormalSourceFile:
    relative_path: str
    data: bytes
    archive_member: str


@dataclass(frozen=True)
class FormalSnapshot:
    commit: str
    source_files: tuple[FormalSourceFile, ...]
    license_bytes: bytes
    readme_bytes: bytes


@dataclass(frozen=True)
class FormalCommentRange:
    start: int
    end: int
    is_doc: bool


@dataclass(frozen=True)
class FormalAttributeRange:
    start: int
    end: int


@dataclass(frozen=True)
class FormalScopeEvent:
    start: int
    action: str
    name: str | None


class Checker:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []
        self.notes: list[str] = []
        self._asset_bytes: dict[Path, bytes] = {}
        self._tar_members: dict[tuple[Path, str], bytes] = {}
        self._tar_archives: dict[Path, tuple[io.BytesIO, tarfile.TarFile]] = {}
        self._formal_candidates: tuple[dict[str, Any], ...] | None = None

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def path(self, relative: str | Path) -> Path:
        value = Path(relative)
        if value.is_absolute() or ".." in value.parts:
            raise CheckFailure(f"unsafe repository path: {relative!r}")
        resolved = (self.root / value).resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as error:
            raise CheckFailure(f"path escapes repository: {relative!r}") from error
        return resolved

    def load_json(self, relative: str | Path) -> dict[str, Any]:
        path = self.path(relative)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as error:
            raise CheckFailure(f"missing JSON authority: {relative}") from error
        except (UnicodeError, json.JSONDecodeError) as error:
            raise CheckFailure(f"invalid JSON authority {relative}: {error}") from error
        if not isinstance(value, dict):
            raise CheckFailure(f"{relative} must contain one JSON object")
        return value

    def asset_bytes(self, relative: str | Path) -> bytes:
        path = self.path(relative)
        if path not in self._asset_bytes:
            try:
                self._asset_bytes[path] = path.read_bytes()
            except OSError as error:
                raise CheckFailure(f"cannot read pinned asset {relative}: {error}") from error
        return self._asset_bytes[path]

    def tar_member(self, relative: str | Path, member: str) -> bytes:
        path = self.path(relative)
        normalized = normalize_member_path(member)
        cache_key = (path, normalized)
        if cache_key in self._tar_members:
            return self._tar_members[cache_key]
        try:
            if path not in self._tar_archives:
                buffer = io.BytesIO(self.asset_bytes(relative))
                self._tar_archives[path] = (
                    buffer,
                    tarfile.open(fileobj=buffer, mode="r:*"),
                )
            archive = self._tar_archives[path][1]
            selected = archive.getmember(normalized)
            if not selected.isfile():
                raise CheckFailure(f"archive locator is not a regular file: {member}")
            stream = archive.extractfile(selected)
            if stream is None:
                raise CheckFailure(f"cannot extract archive member: {member}")
            payload = stream.read()
        except (KeyError, tarfile.TarError) as error:
            raise CheckFailure(
                f"archive member {member!r} is absent from {relative}"
            ) from error
        self._tar_members[cache_key] = payload
        return payload


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_document_sha256(document: Mapping[str, Any], field: str) -> str:
    body = {key: value for key, value in document.items() if key != field}
    return sha256_bytes(canonical_json_bytes(body))


def normalize_member_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise CheckFailure(f"unsafe archive member path: {value!r}")
    return str(path)


def normalized_text(value: str) -> str:
    return unicodedata.normalize("NFC", " ".join(value.split())).casefold()


def formal_candidate_key(record: Mapping[str, Any]) -> str:
    """Return the stable source key used by both release ledgers."""

    return (
        f"formal-conjectures:{record['source_file']}#"
        f"{record['qualified_name']}"
    )


def formal_contextual_statement_sha256(record: Mapping[str, Any]) -> str:
    return sha256_bytes(
        canonical_json_bytes(
            {
                "module": record["module"],
                "namespace": record["namespace"],
                "source_statement_sha256": record["statement_sha256"],
            }
        )
    )


def _formal_mask_comments_and_strings(
    text: str, *, mask_strings: bool = True
) -> tuple[str, list[FormalCommentRange]]:
    """Build a same-length Lean syntax mask without using the extractor."""

    chars = list(text)
    comments: list[FormalCommentRange] = []
    length = len(text)
    index = 0

    def blank(start: int, end: int) -> None:
        for offset in range(start, end):
            if chars[offset] not in "\r\n":
                chars[offset] = " "

    while index < length:
        if text.startswith("--", index):
            end = text.find("\n", index + 2)
            end = length if end < 0 else end
            blank(index, end)
            index = end
            continue
        if text.startswith("/-", index):
            start = index
            is_doc = text.startswith("/--", index) and not text.startswith(
                "/---", index
            )
            depth = 1
            index += 2
            while index < length and depth:
                if text.startswith("/-", index):
                    depth += 1
                    index += 2
                elif text.startswith("-/", index):
                    depth -= 1
                    index += 2
                else:
                    index += 1
            if depth:
                raise CheckFailure(
                    f"unterminated Lean block comment at character offset {start}"
                )
            comments.append(FormalCommentRange(start, index, is_doc))
            blank(start, index)
            continue
        if text[index] == '"':
            start = index
            index += 1
            escaped = False
            while index < length:
                char = text[index]
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    index += 1
                    break
                index += 1
            else:
                raise CheckFailure(
                    f"unterminated Lean string at character offset {start}"
                )
            if mask_strings:
                blank(start, index)
            continue
        index += 1
    return "".join(chars), comments


def _formal_attribute_ranges(mask: str) -> list[FormalAttributeRange]:
    ranges: list[FormalAttributeRange] = []
    index = 0
    while True:
        start = mask.find("@[", index)
        if start < 0:
            return ranges
        depth = 1
        cursor = start + 2
        while cursor < len(mask) and depth:
            if mask[cursor] == "[":
                depth += 1
            elif mask[cursor] == "]":
                depth -= 1
            cursor += 1
        if depth:
            raise CheckFailure(
                f"unterminated Lean attribute at character offset {start}"
            )
        ranges.append(FormalAttributeRange(start, cursor))
        index = cursor


def _formal_associated_attributes(
    mask: str,
    declaration_start: int,
    ranges: Sequence[FormalAttributeRange],
) -> tuple[list[FormalAttributeRange], int]:
    preceding = [item for item in ranges if item.end <= declaration_start]
    if not preceding:
        return [], declaration_start
    chosen: list[FormalAttributeRange] = []
    cursor = declaration_start
    for item in reversed(preceding):
        gap = mask[item.end:cursor]
        if not chosen:
            if FORMAL_MODIFIER_RE.fullmatch(gap.strip()) is None:
                break
        elif gap.strip():
            break
        chosen.append(item)
        cursor = item.start
    chosen.reverse()
    return chosen, cursor


def _formal_categories(attribute_texts: Sequence[str]) -> list[str]:
    pattern = re.compile(
        r"\bcategory\s+(research\s+(?:open|solved)|textbook)\b"
    )
    return [
        match.group(1)
        for text in attribute_texts
        for match in pattern.finditer(text)
    ]


def _formal_ams_codes(attribute_texts: Sequence[str]) -> list[str]:
    codes: list[str] = []
    for text in attribute_texts:
        for match in re.finditer(r"\bAMS\b", text):
            suffix = text[match.end():]
            values = re.match(r"(?:\s+[0-9]{1,2})+", suffix)
            if values is not None:
                codes.extend(
                    f"{int(value):02d}"
                    for value in re.findall(r"[0-9]+", values.group(0))
                )
    return codes


def _formal_qualified_name(namespaces: Sequence[str], local_name: str) -> str:
    if local_name.startswith("_root_."):
        return local_name[len("_root_."):]
    prefix = ".".join(namespaces)
    return f"{prefix}.{local_name}" if prefix else local_name


def _formal_proofs(
    attribute_texts: Sequence[str], namespaces: Sequence[str]
) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"\b(?:(conditional)\s+)?formal_proof\s+using\s+"
        r"(formal_conjectures|lean4|other_system)\s+at\s+"
        r'("(?:\\.|[^"\\])*")'
        r"(?:\s+assuming\s+([^,\]]+))?",
        re.DOTALL,
    )
    result: list[dict[str, Any]] = []
    for text in attribute_texts:
        for match in pattern.finditer(text):
            try:
                link = ast.literal_eval(match.group(3))
            except (SyntaxError, ValueError) as error:
                raise CheckFailure(
                    f"malformed formal_proof link {match.group(3)!r}"
                ) from error
            if not isinstance(link, str):
                raise CheckFailure("formal_proof link is not a string")
            conditional = match.group(1) is not None
            raw_conditions = match.group(4)
            conditions = raw_conditions.split() if raw_conditions else []
            if conditional and not conditions:
                raise CheckFailure(
                    "conditional formal_proof attribute has no assumptions"
                )
            if not conditional and conditions:
                raise CheckFailure(
                    "formal_proof assumptions lack the conditional modifier"
                )
            result.append(
                {
                    "kind": match.group(2),
                    "link": link,
                    "conditional": conditional,
                    "proof_conditions": [
                        _formal_qualified_name(namespaces, condition)
                        for condition in conditions
                    ],
                }
            )
    return result


def _formal_answer_kinds(result_mask: str) -> list[str]:
    result: list[str] = []
    index = 0
    while True:
        match = re.search(r"\banswer\s*\(", result_mask[index:])
        if match is None:
            return result
        start = index + match.start()
        open_paren = index + match.end() - 1
        depth = 1
        cursor = open_paren + 1
        while cursor < len(result_mask) and depth:
            if result_mask[cursor] == "(":
                depth += 1
            elif result_mask[cursor] == ")":
                depth -= 1
            cursor += 1
        if depth:
            raise CheckFailure("unbalanced answer(...) expression")
        inner = result_mask[open_paren + 1:cursor - 1].strip()
        before = result_mask[:start].rstrip()
        after = result_mask[cursor:].lstrip()
        prop_context = (
            inner in {"True", "False"}
            or after.startswith(("↔", "→"))
            or before.endswith(("↔", "→", "¬"))
            or (not before.strip(" ()") and not after.strip(" ()"))
        )
        result.append("Prop" if prop_context else "non-Prop")
        index = cursor


def _formal_parse_name(mask: str, start: int) -> tuple[str, int]:
    cursor = start
    while cursor < len(mask) and mask[cursor].isspace():
        cursor += 1
    name_start = cursor
    quoted = False
    while cursor < len(mask):
        char = mask[cursor]
        if char == "«":
            quoted = True
        elif char == "»":
            quoted = False
        elif not quoted and (char.isspace() or char in "([{:"):
            break
        cursor += 1
    name = mask[name_start:cursor]
    if not name or quoted:
        raise CheckFailure(f"malformed declaration name near offset {start}")
    return name, cursor


def _formal_line_indentation(mask: str, offset: int) -> int:
    line_start = mask.rfind("\n", 0, offset) + 1
    width = 0
    for char in mask[line_start:offset]:
        if char == " ":
            width += 1
        elif char == "\t":
            width += 8 - width % 8
        else:
            break
    return width


def _formal_after_layout_block(
    mask: str, start: int, boundary: int, parent_indentation: int
) -> int:
    line_start = mask.find("\n", start, boundary)
    if line_start < 0:
        return boundary
    line_start += 1
    while line_start < boundary:
        line_end = mask.find("\n", line_start, boundary)
        if line_end < 0:
            line_end = boundary
        token_start = line_start
        while token_start < line_end and mask[token_start] in " \t\r":
            token_start += 1
        if (
            token_start < line_end
            and _formal_line_indentation(mask, token_start) <= parent_indentation
        ):
            return token_start
        line_start = line_end + 1
    return boundary


def _formal_signature_end(mask: str, start: int, boundary: int) -> tuple[int, int]:
    stack: list[str] = []
    matching = {")": "(", "]": "[", "}": "{"}
    colon = -1
    pending_lets: list[int] = []
    index = start
    while index < boundary:
        char = mask[index]
        if char in "([{":
            stack.append(char)
            index += 1
            continue
        if char in ")]}:":
            # The colon is handled below; this branch only owns closers.
            if char != ":":
                if not stack or stack[-1] != matching[char]:
                    raise CheckFailure(
                        f"unbalanced delimiter near character offset {index}"
                    )
                stack.pop()
                index += 1
                continue
        if not stack:
            word = FORMAL_WORD_RE.match(mask, index)
            if word is not None:
                if word.group(0) in {"let", "letI"} and colon >= 0:
                    pending_lets.append(
                        _formal_line_indentation(mask, word.start())
                    )
                index = word.end()
                continue
            if char == ":" and not mask.startswith(":=", index) and colon < 0:
                colon = index
            if mask.startswith(":=", index) and colon >= 0:
                if pending_lets:
                    let_indentation = pending_lets.pop()
                    index += 2
                    rhs_start = index
                    while rhs_start < boundary and mask[rhs_start].isspace():
                        rhs_start += 1
                    rhs_word = FORMAL_WORD_RE.match(mask, rhs_start)
                    if rhs_word is not None and rhs_word.group(0) == "by":
                        index = _formal_after_layout_block(
                            mask, rhs_word.end(), boundary, let_indentation
                        )
                    continue
                return index, colon
        index += 1
    raise CheckFailure("declaration has no complete top-level body separator")


def _formal_line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _formal_normalized_statement(
    text: str, name_end: int, separator: int
) -> str:
    comment_mask, _comments = _formal_mask_comments_and_strings(
        text[name_end:separator], mask_strings=False
    )
    return " ".join(comment_mask.split())


def _formal_scope_events(mask: str) -> list[FormalScopeEvent]:
    result: list[FormalScopeEvent] = []
    for match in FORMAL_SCOPE_RE.finditer(mask):
        action = match.group(2)
        tail = match.group(3).strip()
        if action == "namespace":
            name = tail.split()[0] if tail else None
            if name is None:
                raise CheckFailure(
                    f"namespace command has no name at offset {match.start()}"
                )
            result.append(FormalScopeEvent(match.start(), action, name))
        elif action == "section":
            result.append(
                FormalScopeEvent(
                    match.start(), action, tail.split()[0] if tail else None
                )
            )
        else:
            result.append(FormalScopeEvent(match.start(), action, None))
    return result


def _formal_namespaces_at(
    declarations: Sequence[re.Match[str]], events: Sequence[FormalScopeEvent]
) -> dict[int, tuple[str, ...]]:
    output: dict[int, tuple[str, ...]] = {}
    stack: list[tuple[str, str | None]] = []
    event_index = 0
    for declaration in declarations:
        while (
            event_index < len(events)
            and events[event_index].start < declaration.start()
        ):
            event = events[event_index]
            if event.action in {"namespace", "section"}:
                stack.append((event.action, event.name))
            elif event.action == "end":
                if not stack:
                    raise CheckFailure(
                        f"unmatched end command at offset {event.start}"
                    )
                stack.pop()
            event_index += 1
        output[declaration.start()] = tuple(
            name
            for kind, name in stack
            if kind == "namespace" and name is not None
        )
    return output


def _formal_module_name(relative_path: str) -> str:
    return ".".join(PurePosixPath(relative_path).with_suffix("").parts)


def _load_formal_snapshot(
    checker: Checker, source: Mapping[str, Any]
) -> FormalSnapshot:
    archive_info = require_dict(source.get("archive"), "formal source.archive")
    asset_path = require_string(
        archive_info.get("local_path"), "formal source.archive.local_path"
    )
    root_prefix = require_string(
        archive_info.get("root_prefix"), "formal source.archive.root_prefix"
    ).rstrip("/")
    revision = require_dict(source.get("revision"), "formal source.revision")
    commit = require_string(revision.get("value"), "formal source.revision.value")
    if commit != PINNED_FORMAL_COMMIT or not root_prefix.endswith(commit):
        raise CheckFailure("formal-conjectures source is not at the pinned commit")

    regular: dict[str, bytes] = {}
    prefixes: set[str] = set()
    try:
        with tarfile.open(
            fileobj=io.BytesIO(checker.asset_bytes(asset_path)), mode="r:*"
        ) as archive:
            for member in archive.getmembers():
                normalized = normalize_member_path(member.name)
                member_path = PurePosixPath(normalized)
                if member.issym() or member.islnk():
                    raise CheckFailure(
                        f"formal-conjectures archive contains a link: {normalized}"
                    )
                if not member.isfile():
                    continue
                if "FormalConjectures" in member_path.parts:
                    position = member_path.parts.index("FormalConjectures")
                    if position != 1:
                        raise CheckFailure(
                            f"unexpected formal source archive root: {normalized}"
                        )
                    prefixes.add(member_path.parts[0])
                stream = archive.extractfile(member)
                if stream is None:
                    raise CheckFailure(f"cannot read archive member {normalized}")
                if normalized in regular:
                    raise CheckFailure(f"duplicate archive member {normalized}")
                regular[normalized] = stream.read()
    except tarfile.TarError as error:
        raise CheckFailure(f"cannot parse pinned formal source tar: {error}") from error

    if prefixes != {root_prefix}:
        raise CheckFailure(
            f"formal source archive root differs from registry: {sorted(prefixes)!r}"
        )
    source_prefix = root_prefix + "/FormalConjectures/"
    files = tuple(
        FormalSourceFile(
            name[len(root_prefix) + 1:], payload, name
        )
        for name, payload in sorted(regular.items())
        if name.startswith(source_prefix) and name.endswith(".lean")
    )
    if not files:
        raise CheckFailure("pinned archive contains no FormalConjectures/*.lean files")
    try:
        license_bytes = regular[root_prefix + "/LICENSE"]
        readme_bytes = regular[root_prefix + "/README.md"]
        license_text = license_bytes.decode("utf-8", errors="strict")
        readme_text = readme_bytes.decode("utf-8", errors="strict")
    except (KeyError, UnicodeError) as error:
        raise CheckFailure("formal source LICENSE/README is missing or invalid") from error
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        raise CheckFailure("formal source LICENSE is not Apache-2.0")
    if "Creative Commons Attribution 4.0" not in readme_text:
        raise CheckFailure("formal source README lacks its materials license")
    return FormalSnapshot(commit, files, license_bytes, readme_bytes)


def _extract_formal_file(
    source: FormalSourceFile, snapshot: FormalSnapshot
) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        text = source.data.decode("utf-8", errors="strict")
    except UnicodeError as error:
        raise CheckFailure(
            f"{source.relative_path} is not strict UTF-8"
        ) from error
    try:
        mask, comments = _formal_mask_comments_and_strings(text)
        attributes = _formal_attribute_ranges(mask)
        declarations = list(FORMAL_DECLARATION_RE.finditer(mask))
        namespaces = _formal_namespaces_at(
            declarations, _formal_scope_events(mask)
        )
    except CheckFailure as error:
        raise CheckFailure(f"{source.relative_path}: {error}") from error

    doc_comments = [comment for comment in comments if comment.is_doc]
    imports = sorted(set(FORMAL_IMPORT_RE.findall(mask)))
    source_sha = sha256_bytes(source.data)
    license_info = {
        "code_spdx": "Apache-2.0",
        "license_file": "LICENSE",
        "license_file_sha256": sha256_bytes(snapshot.license_bytes),
        "repository_materials_spdx": "CC-BY-4.0",
        "repository_readme_sha256": sha256_bytes(snapshot.readme_bytes),
    }
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for declaration_index, declaration in enumerate(declarations):
        associated, attribute_start = _formal_associated_attributes(
            mask, declaration.start(), attributes
        )
        attribute_texts = [text[item.start:item.end] for item in associated]
        categories = _formal_categories(attribute_texts)
        selected = [
            category
            for category in categories
            if category in FORMAL_SELECTED_CATEGORIES
        ]
        if not selected:
            continue
        location = (
            f"{source.relative_path}:"
            f"{_formal_line_number(text, declaration.start())}"
        )
        if len(categories) != 1 or len(selected) != 1:
            errors.append(f"{location}: expected exactly one selected category")
            continue
        ams_codes = _formal_ams_codes(attribute_texts)
        if not ams_codes:
            errors.append(f"{location}: selected declaration has no AMS class")
            continue
        if len(ams_codes) != len(set(ams_codes)):
            errors.append(f"{location}: selected declaration repeats an AMS class")
            continue
        invalid_ams = sorted(set(ams_codes) - MSC2020_TOP_LEVEL)
        if invalid_ams:
            errors.append(f"{location}: invalid AMS classes {invalid_ams!r}")
            continue

        docs = [comment for comment in doc_comments if comment.end <= attribute_start]
        doc = docs[-1] if docs else None
        if doc is None or mask[doc.end:attribute_start].strip():
            errors.append(f"{location}: no adjacent docstring")
            continue
        doc_raw = text[doc.start:doc.end]
        doc_text = doc_raw[3:-2]
        if not doc_text.strip():
            errors.append(f"{location}: empty docstring")
            continue

        try:
            local_name, name_end = _formal_parse_name(mask, declaration.end())
            boundary = (
                declarations[declaration_index + 1].start()
                if declaration_index + 1 < len(declarations)
                else len(mask)
            )
            separator, colon = _formal_signature_end(mask, name_end, boundary)
        except CheckFailure as error:
            errors.append(f"{location}: {error}")
            continue
        if not mask[colon + 1:separator].strip():
            errors.append(f"{location}: empty declaration result type")
            continue

        modifier_gap = (
            mask[associated[-1].end:declaration.start()] if associated else ""
        )
        modifier_match = re.search(
            r"(?:private|protected|noncomputable|unsafe)"
            r"(?:\s+(?:private|protected|noncomputable|unsafe))*\s*$",
            modifier_gap,
        )
        declaration_start = (
            associated[-1].end + modifier_match.start()
            if modifier_match is not None and associated
            else declaration.start()
        )
        signature_end = separator
        while (
            signature_end > declaration_start
            and text[signature_end - 1].isspace()
        ):
            signature_end -= 1
        declaration_statement = text[declaration_start:signature_end]
        if not declaration_statement.strip():
            errors.append(f"{location}: empty declaration statement")
            continue
        source_block = text[doc.start:signature_end]
        byte_start = len(text[:doc.start].encode("utf-8"))
        byte_end = len(text[:signature_end].encode("utf-8"))
        if source.data[byte_start:byte_end] != source_block.encode("utf-8"):
            errors.append(f"{location}: inconsistent UTF-8 byte offsets")
            continue
        statement_payload = _formal_normalized_statement(
            text, name_end, separator
        )
        if not statement_payload:
            errors.append(f"{location}: empty normalized statement")
            continue
        namespace = namespaces[declaration.start()]
        qualified_name = _formal_qualified_name(namespace, local_name)
        try:
            formal_proofs = _formal_proofs(attribute_texts, namespace)
            answer_kinds = _formal_answer_kinds(mask[colon + 1:separator])
        except CheckFailure as error:
            errors.append(f"{location}: {error}")
            continue
        effective_proof = formal_proofs[-1] if formal_proofs else None
        next_doc_start = min(
            (
                comment.start
                for comment in doc_comments
                if separator < comment.start < boundary
            ),
            default=boundary,
        )
        proof_mask = mask[separator:next_doc_start]
        has_sorry_free_proof = re.search(r"\bsorry\b", proof_mask) is None
        modifier_words = re.findall(
            r"\b(?:private|protected|noncomputable|unsafe)\b",
            text[declaration_start:declaration.start()],
        )
        records.append(
            {
                "schema_version": FORMAL_SOURCE_SCHEMA_VERSION,
                "source_repository": FORMAL_SOURCE_REPOSITORY,
                "source_commit": snapshot.commit,
                "category": selected[0],
                "ams": ams_codes,
                "declaration_kind": declaration.group(1),
                "declaration_modifiers": modifier_words,
                "namespace": ".".join(namespace),
                "local_name": local_name,
                "qualified_name": qualified_name,
                "theorem": qualified_name,
                "subjects": [str(int(code)) for code in ams_codes],
                "statement": text[name_end:separator].strip(),
                "statement_policy": "unelaborated Lean source after declaration name",
                "docstring": doc_text,
                "docstring_raw": doc_raw,
                "formalProofKind": (
                    effective_proof["kind"] if effective_proof else None
                ),
                "formalProofLink": (
                    effective_proof["link"] if effective_proof else None
                ),
                "hasSorryFreeProof": has_sorry_free_proof,
                "hasSorryFreeProofPolicy": (
                    "no source-level sorry token before the next documented declaration"
                ),
                "answerKinds": answer_kinds,
                "answerKindsPolicy": (
                    "static source-context inference; compare to Lean elaboration"
                ),
                "proofConditions": (
                    effective_proof["proof_conditions"] if effective_proof else []
                ),
                "formal_proofs": formal_proofs,
                "declaration_statement": declaration_statement,
                "declaration_sha256": sha256_bytes(
                    declaration_statement.encode("utf-8")
                ),
                "statement_sha256": sha256_bytes(
                    statement_payload.encode("utf-8")
                ),
                "statement_hash_policy": (
                    "comments-and-strings-masked signature after declaration name; "
                    "whitespace collapsed"
                ),
                "source_block": source_block,
                "source_block_sha256": sha256_bytes(source_block.encode("utf-8")),
                "source_file": source.relative_path,
                "archive_member": source.archive_member,
                "source_file_sha256": source_sha,
                "source_block_byte_start": byte_start,
                "source_block_byte_end_exclusive": byte_end,
                "source_line_start": _formal_line_number(text, doc.start),
                "source_line_end": _formal_line_number(text, signature_end),
                "declaration_line_start": _formal_line_number(
                    text, declaration_start
                ),
                "declaration_line_end": _formal_line_number(text, signature_end),
                "module": _formal_module_name(source.relative_path),
                "module_imports": imports,
                "license": license_info,
            }
        )
    return records, errors


def rebuild_formal_candidates(
    checker: Checker, sources: Mapping[str, Mapping[str, Any]]
) -> tuple[dict[str, Any], ...]:
    """Independently rebuild and receipt-bind all 2,778 pinned candidates."""

    if checker._formal_candidates is not None:
        return checker._formal_candidates
    source = sources.get(PINNED_FORMAL_SOURCE_ID)
    if source is None:
        raise CheckFailure(
            f"source registry omits {PINNED_FORMAL_SOURCE_ID}"
        )
    snapshot = _load_formal_snapshot(checker, source)
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for source_file in snapshot.source_files:
        extracted, file_errors = _extract_formal_file(source_file, snapshot)
        records.extend(extracted)
        errors.extend(file_errors)
    if errors:
        preview = "; ".join(errors[:12])
        raise CheckFailure(
            f"independent formal extraction rejected {len(errors)} declarations: "
            f"{preview}"
        )
    records.sort(
        key=lambda row: (
            row["qualified_name"],
            row["source_file"],
            row["declaration_line_start"],
        )
    )
    names = [str(row["qualified_name"]) for row in records]
    duplicate_names = sorted(
        name for name, count in Counter(names).items() if count != 1
    )
    if duplicate_names:
        raise CheckFailure(
            f"independent formal extraction found duplicate names: "
            f"{duplicate_names[:8]!r}"
        )
    if len(records) != PINNED_CANDIDATE_COUNT:
        raise CheckFailure(
            f"independent formal extraction rebuilt {len(records)} candidates; "
            f"expected {PINNED_CANDIDATE_COUNT}"
        )
    jsonl = b"".join(canonical_json_bytes(record) + b"\n" for record in records)
    digest = sha256_bytes(jsonl)
    if digest != PINNED_EXTRACTION_JSONL_SHA256:
        raise CheckFailure(
            "independent formal extraction digest drifted: "
            f"observed {digest}, expected {PINNED_EXTRACTION_JSONL_SHA256}"
        )
    checker._formal_candidates = tuple(records)
    return checker._formal_candidates


def formal_source_locator(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_id": PINNED_FORMAL_SOURCE_ID,
        "revision": PINNED_FORMAL_COMMIT,
        "member_path": candidate["source_file"],
        "file_sha256": candidate["source_file_sha256"],
        "byte_start": candidate["source_block_byte_start"],
        "byte_end_exclusive": candidate["source_block_byte_end_exclusive"],
        "line_start": candidate["source_line_start"],
        "line_end": candidate["source_line_end"],
        "raw_block_sha256": candidate["source_block_sha256"],
    }


def ordinal(identifier: str, pattern: re.Pattern[str]) -> int:
    match = pattern.fullmatch(identifier)
    if match is None:
        raise CheckFailure(f"malformed identifier: {identifier!r}")
    return int(match.group(1))


def require_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CheckFailure(f"{label} must be an object")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CheckFailure(f"{label} must be an array")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckFailure(f"{label} must be a non-empty string")
    return value


def require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise CheckFailure(f"{label} must be a lowercase SHA-256 digest")
    return value


def exact_unique_strings(
    checker: Checker,
    values: Iterable[Any],
    label: str,
    pattern: re.Pattern[str] | None = None,
) -> set[str]:
    observed: list[str] = []
    for value in values:
        if not isinstance(value, str) or (pattern is not None and pattern.fullmatch(value) is None):
            checker.fail(f"{label} contains malformed value {value!r}")
            continue
        observed.append(value)
    duplicates = sorted(key for key, count in Counter(observed).items() if count != 1)
    if duplicates:
        checker.fail(f"{label} contains duplicates: {duplicates[:8]!r}")
    return set(observed)


def canonical_row_multiset(values: Iterable[Any], label: str) -> Counter[bytes]:
    rows: list[bytes] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise CheckFailure(f"{label}[{index}] must be an object")
        rows.append(canonical_json_bytes(value))
    return Counter(rows)


def release_dir(release: str) -> Path:
    if release not in RELEASES:
        raise CheckFailure(f"unsupported release {release!r}")
    return V5_ROOT / "releases" / release


def artifact_rows(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    for key in (
        "records",
        "variants",
        "mappings",
        "migrations",
        "historical_bindings",
        "entries",
        "rows",
        "candidate_dispositions",
    ):
        value = document.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
    return []


def artifact_row_count(path: str, document: Mapping[str, Any]) -> int:
    """Return the contract row count without trusting declared count metadata."""

    if path == "Coverage_Ledger.json":
        candidates = require_list(
            document.get("candidate_dispositions"),
            "Coverage_Ledger.candidate_dispositions",
        )
        msc_rows = require_list(
            document.get("msc_coverage"), "Coverage_Ledger.msc_coverage"
        )
        return len(candidates) + len(msc_rows)
    if path in {"Theorem_List.json", "Open_Claim_List.json"}:
        return len(projection_ids(document))
    for key in (
        "records",
        "variants",
        "mappings",
        "migrations",
        "historical_bindings",
        "entries",
        "rows",
    ):
        value = document.get(key)
        if isinstance(value, list):
            return len(value)
    raise CheckFailure(f"{path} has no contract row array")


def record_variant_id(row: Mapping[str, Any]) -> str | None:
    for key in ("variant_id", "atv_id", "canonical_variant_id"):
        value = row.get(key)
        if isinstance(value, str):
            return value
    return None


def record_stage_id(row: Mapping[str, Any]) -> str | None:
    for key in ("stage_claim_id", "stage_id", "s5_id"):
        value = row.get(key)
        if isinstance(value, str):
            return value
    return None


def claim_kind(row: Mapping[str, Any]) -> str:
    value = row.get("current_claim_kind", row.get("claim_kind", ""))
    return value.strip().casefold() if isinstance(value, str) else ""


def material_status(row: Mapping[str, Any]) -> str:
    value = row.get("material_status", row.get("status", ""))
    if isinstance(value, dict):
        value = value.get("status", value.get("value", ""))
    return value.strip().casefold() if isinstance(value, str) else ""


def is_active_claim(row: Mapping[str, Any]) -> bool:
    lifecycle = row.get("lifecycle", "active")
    if isinstance(lifecycle, dict):
        lifecycle = lifecycle.get("state")
    truth = row.get("truth_apt", True)
    atomicity = row.get("atomicity", "atomic")
    role = row.get("record_role", "claim")
    return (
        lifecycle in {"active", "current"}
        and truth in {True, "true", "truth_apt", "yes"}
        and atomicity == "atomic"
        and role == "claim"
    )


def is_theorem(row: Mapping[str, Any]) -> bool:
    return is_active_claim(row) and claim_kind(row) in THEOREM_KINDS and material_status(row) == "proved"


def is_open_claim(row: Mapping[str, Any]) -> bool:
    return (
        is_active_claim(row)
        and claim_kind(row) in OPEN_KINDS
        and material_status(row) in OPEN_STATUSES
    )


def is_quota_theorem(row: Mapping[str, Any]) -> bool:
    return (
        is_theorem(row)
        and row.get("origin_stage") == "Stage5"
        and row.get("category") == "theorem"
        and row.get("declaration_kind") == "theorem"
        and claim_kind(row) == "theorem"
    )


def is_quota_open_claim(row: Mapping[str, Any]) -> bool:
    return (
        is_active_claim(row)
        and row.get("origin_stage") == "Stage5"
        and row.get("category") == "open_claim"
        and row.get("declaration_kind") == "theorem"
        and claim_kind(row) in {"conjecture", "hypothesis", "open_problem"}
        and material_status(row) in {"open", "partial", "independent", "disputed"}
        and row.get("raw_category") == "research open"
    )


def origin_release(row: Mapping[str, Any]) -> str | None:
    value = row.get("origin_release", row.get("entry_origin_release"))
    if value in {"5.0", "5.1"}:
        return str(value)
    aliases = {
        "stage5_0": "5.0",
        "stage5.0": "5.0",
        "stage5_1": "5.1",
        "stage5.1": "5.1",
    }
    return aliases.get(str(value).casefold())


def statement_digest(statement: Any) -> str:
    if isinstance(statement, dict):
        statement = {
            key: value for key, value in statement.items() if key != "statement_sha256"
        }
    return sha256_bytes(canonical_json_bytes(statement))


def mathematical_statement(row: Mapping[str, Any]) -> Any:
    return row.get("statement", row.get("mathematical_statement"))


def mathematical_statement_sha256(row: Mapping[str, Any]) -> Any:
    if isinstance(row.get("statement_sha256"), str):
        return row["statement_sha256"]
    statement = row.get("mathematical_statement")
    if isinstance(statement, dict):
        return statement.get("statement_sha256")
    return row.get("statement_sha256")


def formal_statement(row: Mapping[str, Any]) -> Mapping[str, Any]:
    value = row.get("formal_statement")
    return value if isinstance(value, dict) else {}


def record_source_id(row: Mapping[str, Any]) -> Any:
    if isinstance(row.get("source_id"), str):
        return row["source_id"]
    locator = formal_statement(row).get("locator")
    if isinstance(locator, dict) and isinstance(locator.get("source_id"), str):
        return locator["source_id"]
    return row.get("source_id")


def record_qualified_name(row: Mapping[str, Any]) -> Any:
    if isinstance(row.get("qualified_name"), str):
        return row["qualified_name"]
    value = formal_statement(row).get("qualified_declaration")
    return value if isinstance(value, str) else row.get("qualified_name")


def record_declaration(row: Mapping[str, Any]) -> Any:
    if isinstance(row.get("formal_declaration"), str):
        return row["formal_declaration"]
    value = formal_statement(row).get("declaration_text")
    return value if isinstance(value, str) else row.get("formal_declaration")


def record_docstring(row: Mapping[str, Any]) -> Any:
    if isinstance(row.get("formal_docstring"), str):
        return row["formal_docstring"]
    value = formal_statement(row).get("docstring")
    return value if isinstance(value, str) else row.get("formal_docstring")


def record_locator(row: Mapping[str, Any]) -> Mapping[str, Any]:
    value = row.get("locator")
    if isinstance(value, dict):
        return value
    value = formal_statement(row).get("locator")
    if isinstance(value, dict):
        return value
    return {}


def contextual_statement_sha256(row: Mapping[str, Any]) -> str:
    dedupe = require_dict(row.get("dedupe"), "record.dedupe")
    source_statement = require_sha256(
        dedupe.get("source_statement_sha256"),
        "record.dedupe.source_statement_sha256",
    )
    module = require_string(row.get("module"), "record.module")
    namespace = row.get("namespace")
    if not isinstance(namespace, str):
        raise CheckFailure("record.namespace must be a string")
    payload = {
        "module": module,
        "namespace": namespace,
        "source_statement_sha256": source_statement,
    }
    return sha256_bytes(canonical_json_bytes(payload))


def quota_duplicate_keys(row: Mapping[str, Any]) -> tuple[Any, Any, Any]:
    """Rebuild the three scoped non-credit keys from record content."""

    source_id = require_string(record_source_id(row), "record.source_id")
    qualified = require_string(record_qualified_name(row), "record.qualified_name")
    declaration = require_string(record_declaration(row), "record.formal_declaration")
    module = require_string(row.get("module"), "record.module")
    namespace = row.get("namespace")
    if not isinstance(namespace, str):
        raise CheckFailure("record.namespace must be a string")
    return (
        (source_id, normalized_text(qualified)),
        contextual_statement_sha256(row),
        (module, namespace, normalized_text(declaration)),
    )


def release_inventory(root: Path, release: str) -> list[dict[str, Any]]:
    base = root / release_dir(release)
    inventory: list[dict[str, Any]] = []
    for name in RELEASE_FILES:
        path = base / name
        if not path.is_file():
            raise CheckFailure(f"release {release} is missing {name}")
        inventory.append(
            {
                "path": name,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return sorted(inventory, key=lambda row: row["path"])


def release_root_sha256(inventory: Sequence[Mapping[str, Any]]) -> str:
    normalized = [
        {
            "path": require_string(row.get("path"), "release inventory path"),
            "sha256": require_sha256(row.get("sha256"), "release inventory sha256"),
            "size_bytes": row.get("size_bytes"),
        }
        for row in sorted(inventory, key=lambda item: str(item.get("path", "")))
    ]
    if any(not isinstance(row["size_bytes"], int) or row["size_bytes"] < 0 for row in normalized):
        raise CheckFailure("release inventory size_bytes must be non-negative integers")
    return sha256_bytes(canonical_json_bytes(normalized))


def check_sealed_document(checker: Checker, label: str, document: Mapping[str, Any]) -> None:
    for field in ("authority_sha256", "document_sha256"):
        if field not in document:
            continue
        try:
            observed = require_sha256(document[field], f"{label}.{field}")
        except CheckFailure as error:
            checker.fail(str(error))
            return
        expected = canonical_document_sha256(document, field)
        if observed != expected:
            checker.fail(f"{label}.{field} is stale")
        return


def check_v4_import_receipt(
    checker: Checker,
    receipt: Mapping[str, Any],
    parent_v4_ids: set[str],
) -> None:
    v4_registry = checker.load_json(V4_REGISTRY_PATH)
    v4_source_records = checker.load_json(V4_SOURCE_RECORDS_PATH)
    v4_stage_registry = checker.load_json(V4_STAGE_REGISTRY_PATH)
    observed = receipt.get("authority_sha256")
    expected = canonical_document_sha256(receipt, "authority_sha256")
    if observed != expected:
        checker.fail("V4 import receipt authority_sha256 is stale")
    bindings = require_list(
        receipt.get("authoritative_sources"), "V4 receipt authoritative_sources"
    )
    for index, row in enumerate(bindings):
        row = require_dict(row, f"V4 receipt source[{index}]")
        path = require_string(row.get("path"), f"V4 receipt source[{index}].path")
        resolved = checker.path(path)
        if not resolved.is_file():
            checker.fail(f"V4 import receipt source is missing: {path}")
            continue
        if row.get("size_bytes") != resolved.stat().st_size:
            checker.fail(f"V4 import receipt source size drifted: {path}")
        if row.get("sha256") != sha256_file(resolved):
            checker.fail(f"V4 import receipt source hash drifted: {path}")
    identity = require_dict(receipt.get("identity_import"), "V4 receipt identity_import")
    rows = require_list(
        identity.get("variant_stage_crosswalk"), "V4 receipt variant_stage_crosswalk"
    )
    pairs: list[tuple[str, str]] = []
    for index, row in enumerate(rows):
        row = require_dict(row, f"V4 crosswalk[{index}]")
        atv = row.get("variant_id", row.get("atv_id"))
        s4 = row.get("stage_claim_id", row.get("s4_claim_id"))
        if not isinstance(atv, str) or not isinstance(s4, str):
            checker.fail(f"V4 crosswalk[{index}] lacks ATV/S4 identifiers")
            continue
        try:
            if ordinal(atv, ATV_RE) != ordinal(s4, re.compile(r"^S4-CLM-([0-9]{8})$")):
                checker.fail(f"V4 receipt ordinal mismatch for {atv}")
        except CheckFailure as error:
            checker.fail(str(error))
            continue
        pairs.append((atv, s4))
    domain = exact_unique_strings(
        checker, (atv for atv, _ in pairs), "V4 receipt ATV domain", ATV_RE
    )
    if domain != parent_v4_ids or len({stage for _, stage in pairs}) != len(parent_v4_ids):
        checker.fail("V4 import receipt is not a bijection over all 3484 variants")
    stage_rows = require_list(
        v4_stage_registry.get("mappings"), "V4 Stage4 registry mappings"
    )
    expected_stage_by_atv: dict[str, str] = {}
    for index, value in enumerate(stage_rows):
        value = require_dict(value, f"V4 Stage4 mapping[{index}]")
        atv = require_string(value.get("variant_id"), f"V4 Stage4 mapping[{index}].variant_id")
        stage = require_string(
            value.get("stage_claim_id", value.get("stage_id")),
            f"V4 Stage4 mapping[{index}].stage_claim_id",
        )
        if atv in expected_stage_by_atv:
            checker.fail(f"V4 Stage4 registry duplicates {atv}")
        expected_stage_by_atv[atv] = stage
    if dict(pairs) != expected_stage_by_atv:
        checker.fail("V4 import receipt ATV/S4 crosswalk differs from Stage4 authority")

    counts = require_dict(receipt.get("counts"), "V4 receipt counts")
    identity_counts = {
        "atv_variants": len(parent_v4_ids),
        "stage_claim_mappings": len(rows),
    }
    for key, expected_count in identity_counts.items():
        if counts.get(key) != expected_count:
            checker.fail(f"V4 import receipt count {key} is stale")

    aliases = require_list(
        identity.get("historical_thm_alias_crosswalk"),
        "V4 receipt historical_thm_alias_crosswalk",
    )
    expected_aliases: list[dict[str, Any]] = []
    for index, value in enumerate(
        require_list(v4_registry.get("legacy_aliases"), "V4 registry legacy_aliases")
    ):
        value = require_dict(value, f"V4 legacy alias[{index}]")
        target = require_string(
            value.get("target_variant_id"), f"V4 legacy alias[{index}].target_variant_id"
        )
        expected_aliases.append(
            {
                "thm_alias_id": value.get("alias_id"),
                "historical_atv_id": target,
                "historical_s4_claim_id": expected_stage_by_atv.get(target),
                "rebound": False,
            }
        )
    if canonical_row_multiset(aliases, "V4 receipt alias") != canonical_row_multiset(
        expected_aliases, "V4 expected alias"
    ):
        checker.fail("V4 import receipt does not conserve all 3262 historical aliases")
    if counts.get("historical_thm_aliases") != len(expected_aliases):
        checker.fail("V4 import receipt historical alias count is stale")

    folded = require_list(
        identity.get("folded_occurrence_ids"), "V4 receipt folded_occurrence_ids"
    )
    folded_set = exact_unique_strings(
        checker, folded, "V4 receipt folded occurrence IDs", ATO_RE
    )
    expected_folded = set(
        require_list(
            v4_source_records.get("folded_occurrence_ids"),
            "V4 source records folded_occurrence_ids",
        )
    )
    if folded_set != expected_folded:
        checker.fail("V4 import receipt does not conserve all 76 folded occurrences")
    if counts.get("folded_occurrences") != len(expected_folded):
        checker.fail("V4 import receipt folded occurrence count is stale")

    graph: defaultdict[str, set[str]] = defaultdict(set)
    for receipt_key, registry_key, count_key, expected_number in (
        ("redirects", "redirects", "redirects", 8),
        ("splits", "splits", "splits", 4),
    ):
        actual_relation_rows = require_list(
            identity.get(receipt_key), f"V4 receipt {receipt_key}"
        )
        expected_relation_rows = require_list(
            v4_registry.get(registry_key), f"V4 registry {registry_key}"
        )
        if canonical_row_multiset(
            actual_relation_rows, f"V4 receipt {receipt_key}"
        ) != canonical_row_multiset(
            expected_relation_rows, f"V4 registry {registry_key}"
        ):
            checker.fail(f"V4 import receipt does not exactly conserve {receipt_key}")
        if len(actual_relation_rows) != expected_number or counts.get(count_key) != expected_number:
            checker.fail(f"V4 import receipt {receipt_key} cardinality is stale")
        for index, value in enumerate(actual_relation_rows):
            value = require_dict(value, f"V4 receipt {receipt_key}[{index}]")
            source = require_string(
                value.get("source_variant_id"),
                f"V4 receipt {receipt_key}[{index}].source_variant_id",
            )
            targets = (
                [value.get("target_variant_id")]
                if receipt_key == "redirects"
                else require_list(
                    value.get("child_variant_ids"),
                    f"V4 receipt splits[{index}].child_variant_ids",
                )
            )
            if receipt_key == "splits" and len(targets) < 2:
                checker.fail(f"V4 receipt split {source} has fewer than two children")
            if value.get("default_child") is not None or value.get("default_child_id") is not None:
                checker.fail(f"V4 receipt {receipt_key} {source} chooses a default child")
            if value.get("evidence_inherited") is not False:
                checker.fail(f"V4 receipt {receipt_key} {source} inherits evidence")
            for target in targets:
                if not isinstance(target, str) or target not in parent_v4_ids:
                    checker.fail(f"V4 receipt {receipt_key} {source} has invalid target {target!r}")
                    continue
                graph[source].add(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise CheckFailure(f"V4 redirect/split graph contains a cycle at {node}")
        if node in visited:
            return
        visiting.add(node)
        for child in graph.get(node, set()):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    try:
        for node in graph:
            visit(node)
    except CheckFailure as error:
        checker.fail(str(error))

    set_digests = identity.get("set_digests")
    if isinstance(set_digests, dict):
        digest_fields = {
            "variant_stage_crosswalk_sha256": rows,
            "historical_thm_alias_crosswalk_sha256": aliases,
            "folded_occurrence_ids_sha256": folded,
            "redirect_rows_sha256": identity.get("redirects"),
            "split_rows_sha256": identity.get("splits"),
        }
        for field, value in digest_fields.items():
            if set_digests.get(field) != sha256_bytes(canonical_json_bytes(value)):
                checker.fail(f"V4 import receipt {field} is stale")


def check_contract(checker: Checker, contract: Mapping[str, Any]) -> None:
    parent = contract.get("parent_variant_high_watermark")
    if parent is None:
        parent = require_dict(contract.get("identity_policy", {}), "contract.identity_policy").get(
            "parent_variant_high_watermark"
        )
    if parent != PARENT_HIGH_WATERMARK:
        checker.fail("Stage5 contract parent ATV high-watermark is not 3484")
    thresholds = contract.get("minimum_counts", contract.get("release_minimums"))
    if isinstance(thresholds, dict):
        for release, expected in MINIMUMS.items():
            row = thresholds.get(release, {})
            if not isinstance(row, dict):
                checker.fail(f"contract has no minimum-count object for {release}")
                continue
            theorem = row.get("origin_theorems", row.get("new_theorems", row.get("theorem", 0)))
            open_count = row.get("origin_open_claims", row.get("new_open_claims", row.get("open", 0)))
            if not isinstance(theorem, int) or theorem < expected["theorem"]:
                checker.fail(f"contract weakens {release} theorem minimum")
            if not isinstance(open_count, int) or open_count < expected["open"]:
                checker.fail(f"contract weakens {release} open-claim minimum")
    for field, expected_path, digest_field in (
        ("record_schema", SCHEMA_PATH, "sha256"),
        ("source_registry", SOURCE_REGISTRY_PATH, "sha256"),
    ):
        binding = require_dict(contract.get(field), f"contract.{field}")
        if binding.get("path") != str(expected_path):
            checker.fail(f"contract.{field} path is not canonical")
        path = checker.path(expected_path)
        if not path.is_file() or binding.get(digest_field) != sha256_file(path):
            checker.fail(f"contract.{field} file hash is stale")
    parent_binding = require_dict(contract.get("parent"), "contract.parent")
    if parent_binding.get("import_receipt_path") != str(V4_IMPORT_RECEIPT_PATH):
        checker.fail("contract parent import-receipt path is not canonical")
    receipt_path = checker.path(V4_IMPORT_RECEIPT_PATH)
    if parent_binding.get("import_receipt_file_sha256") != sha256_file(receipt_path):
        checker.fail("contract parent import-receipt file hash is stale")
    layout = require_dict(contract.get("release_layout"), "contract.release_layout")
    expected_artifacts = {MANIFEST_NAME, *RELEASE_FILES}
    if set(layout.get("artifact_names", [])) != expected_artifacts:
        checker.fail("contract release artifact set is not exact")
    coverage_contract = require_dict(
        contract.get("coverage_ledger_contract"), "contract.coverage_ledger_contract"
    )
    dispositions = set(coverage_contract.get("candidate_disposition_enum", []))
    if "already_allocated_noncredit" not in dispositions:
        checker.fail("contract omits already_allocated_noncredit carry disposition")
    msc_policy = require_dict(
        contract.get("msc_coverage_policy"), "contract.msc_coverage_policy"
    )
    msc_classes = msc_policy.get("top_level_classes")
    if not isinstance(msc_classes, list) or len(msc_classes) != 63 or len(set(msc_classes)) != 63:
        checker.fail("contract does not freeze exactly 63 unique MSC top classes")
    category_mapping = category_map(contract)
    if category_mapping.get("research open") != "open_claim":
        checker.fail("contract research-open category mapping is not canonical")
    status_mapping = status_map(contract)
    if status_mapping.get("research open") != "open":
        checker.fail("contract research-open status mapping is not canonical")
    check_sealed_document(checker, str(CONTRACT_PATH), contract)


def source_rows(registry: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = registry.get("sources", registry.get("records"))
    if not isinstance(rows, list):
        raise CheckFailure("Math_Source_Registry_v5.json has no sources array")
    if not all(isinstance(row, dict) for row in rows):
        raise CheckFailure("source registry contains a non-object row")
    return list(rows)


def check_source_registry(
    checker: Checker, registry: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    source_contract = require_dict(
        registry.get("source_record_contract"), "source registry contract"
    )
    required_source_fields = set(
        require_list(
            source_contract.get("required_fields"),
            "source registry contract.required_fields",
        )
    )
    for index, row in enumerate(source_rows(registry)):
        label = f"source[{index}]"
        try:
            missing = sorted(required_source_fields - set(row))
            if missing:
                raise CheckFailure(f"{label} misses source-contract fields: {missing!r}")
            if source_contract.get("additional_fields_allowed") is False:
                extra = sorted(set(row) - required_source_fields)
                if extra:
                    raise CheckFailure(f"{label} has undeclared source fields: {extra!r}")
            source_id = require_string(row.get("source_id"), f"{label}.source_id")
            archive = require_dict(row.get("archive"), f"{label}.archive")
            asset_path = require_string(archive.get("local_path"), f"{label}.archive.local_path")
            expected_asset_sha = require_sha256(
                archive.get("sha256"), f"{label}.archive.sha256"
            )
            revision = require_dict(row.get("revision"), f"{label}.revision")
            pin_value = require_string(revision.get("value"), f"{label}.revision.value")
            if not re.fullmatch(r"[a-f0-9]{40,64}", pin_value):
                raise CheckFailure(f"{label}.revision.value is not an immutable digest")
            license_info = require_dict(row.get("rights"), f"{label}.rights")
            axes = require_list(license_info.get("axes"), f"{label}.rights.axes")
            if not axes:
                raise CheckFailure(f"{label}.rights.axes is empty")
            for axis_index, axis in enumerate(axes):
                axis = require_dict(axis, f"{label}.rights.axes[{axis_index}]")
                require_string(axis.get("asset_class"), f"{label}.rights.axes asset_class")
                require_string(axis.get("status"), f"{label}.rights.axes status")
                require_string(axis.get("scope_note"), f"{label}.rights.axes scope_note")
            require_dict(license_info.get("policy_locator"), f"{label}.rights.policy_locator")
            if source_id in output:
                raise CheckFailure(f"duplicate source_id {source_id}")
            asset = checker.path(asset_path)
            if not asset.is_file():
                raise CheckFailure(f"{label} pinned asset is missing: {asset_path}")
            if sha256_file(asset) != expected_asset_sha:
                raise CheckFailure(f"{label} pinned asset hash drifted: {asset_path}")
            if isinstance(archive.get("size_bytes"), int) and asset.stat().st_size != archive["size_bytes"]:
                raise CheckFailure(f"{label} pinned asset size drifted")
            content_facts = row.get("content_facts")
            if isinstance(content_facts, dict):
                for key, member_path in content_facts.items():
                    if not key.endswith("_path") or not isinstance(member_path, str):
                        continue
                    digest_key = key[:-5] + "_sha256"
                    expected_member_sha = content_facts.get(digest_key)
                    if not isinstance(expected_member_sha, str):
                        continue
                    full_member = str(archive.get("root_prefix", "")) + member_path
                    if sha256_bytes(checker.tar_member(asset_path, full_member)) != expected_member_sha:
                        raise CheckFailure(f"{label} pinned archive fact {key} drifted")
            output[source_id] = row
        except CheckFailure as error:
            checker.fail(str(error))
    check_sealed_document(checker, str(SOURCE_REGISTRY_PATH), registry)
    counts = registry.get("counts")
    if isinstance(counts, dict) and counts.get("source_records") != len(output):
        checker.fail("source registry counts.source_records is stale")
    return output


def category_map(contract: Mapping[str, Any]) -> Mapping[str, Any]:
    for key in ("category_mapping", "category_map", "source_category_mapping"):
        value = contract.get(key)
        if isinstance(value, dict):
            return value
    mappings = contract.get("mappings")
    return mappings.get("categories", {}) if isinstance(mappings, dict) else {}


def status_map(contract: Mapping[str, Any]) -> Mapping[str, Any]:
    for key in ("status_mapping", "status_map", "source_status_mapping"):
        value = contract.get(key)
        if isinstance(value, dict):
            return value
    mappings = contract.get("mappings")
    return mappings.get("statuses", {}) if isinstance(mappings, dict) else {}


def mapping_value(mapping: Mapping[str, Any], source_id: str, raw: str) -> str | None:
    scoped = mapping.get(source_id)
    if isinstance(scoped, dict):
        value = scoped.get(raw)
    else:
        value = mapping.get(raw)
    if isinstance(value, dict):
        value = value.get("canonical", value.get("value"))
    return value if isinstance(value, str) else None


def locator_payload(
    checker: Checker,
    source: Mapping[str, Any],
    locator: Mapping[str, Any],
    label: str,
) -> bytes:
    archive = require_dict(source.get("archive"), f"{label}.source archive")
    asset_path = require_string(archive.get("local_path"), f"{label}.source archive.local_path")
    member = require_string(
        locator.get("member_path", locator.get("archive_member_path")),
        f"{label}.locator.member_path",
    )
    root_prefix = archive.get("root_prefix", "")
    if isinstance(root_prefix, str) and root_prefix and not member.startswith(root_prefix):
        member = root_prefix + member
    file_payload = checker.tar_member(asset_path, member)
    expected_file = require_sha256(
        locator.get("file_sha256", locator.get("archive_member_sha256")),
        f"{label}.locator.file_sha256",
    )
    if sha256_bytes(file_payload) != expected_file:
        raise CheckFailure(f"{label} locator file hash drifted")
    start = locator.get("byte_start")
    end = locator.get("byte_end_exclusive")
    if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end <= len(file_payload)):
        raise CheckFailure(f"{label} has an invalid exact byte range")
    block = file_payload[start:end]
    expected_block = require_sha256(
        locator.get("raw_block_sha256", locator.get("source_slice_sha256")),
        f"{label}.locator.raw_block_sha256",
    )
    if sha256_bytes(block) != expected_block:
        raise CheckFailure(f"{label} raw block hash drifted")
    revision = source.get("revision", {})
    if isinstance(revision, dict) and locator.get("revision") != revision.get("value"):
        raise CheckFailure(f"{label} locator revision differs from source pin")
    start_line = file_payload[:start].count(b"\n") + 1
    end_line = file_payload[: max(start, end - 1)].count(b"\n") + 1
    if locator.get("line_start") != start_line or locator.get("line_end") != end_line:
        raise CheckFailure(f"{label} locator line range differs from byte range")
    return block


def validate_record_schema(
    checker: Checker, schema: Mapping[str, Any], records: Sequence[Mapping[str, Any]]
) -> None:
    if jsonschema is None:
        checker.fail("jsonschema is required to validate Math_Claim_Record_Schema_v5.json")
        return
    candidate: Mapping[str, Any] = schema
    definitions = schema.get("$defs")
    if isinstance(definitions, dict):
        for key in ("claim_record", "math_claim_record", "record"):
            if key in definitions:
                candidate = {
                    "$schema": schema.get("$schema", "https://json-schema.org/draft/2020-12/schema"),
                    "$defs": definitions,
                    "$ref": f"#/$defs/{key}",
                }
                break
    try:
        jsonschema.Draft202012Validator.check_schema(candidate)
        validator = jsonschema.Draft202012Validator(candidate)
    except jsonschema.SchemaError as error:
        checker.fail(f"invalid Stage5 record schema: {error.message}")
        return
    failures = 0
    for index, record in enumerate(records):
        for error in validator.iter_errors(record):
            checker.fail(f"catalog record[{index}] schema error: {error.message}")
            failures += 1
            if failures >= 20:
                checker.fail("catalog schema errors truncated after 20 failures")
                return


def check_record_content(
    checker: Checker,
    release: str,
    records: Sequence[dict[str, Any]],
    contract: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    candidates: Sequence[Mapping[str, Any]] | None = None,
) -> None:
    rebuilt_candidates = (
        tuple(candidates)
        if candidates is not None
        else rebuild_formal_candidates(checker, sources)
    )
    candidates_by_key = {
        formal_candidate_key(candidate): candidate
        for candidate in rebuilt_candidates
    }
    allocations = expected_formal_allocations(rebuilt_candidates)
    allocations_by_atv = {
        str(identity["variant_id"]): identity
        for identity in allocations.values()
        if identity["origin_release"] == "5.0" or release == "5.1"
    }
    expected_aliases: defaultdict[str, list[str]] = defaultdict(list)
    for duplicate_key, (winner, _reason) in _formal_duplicate_map(
        rebuilt_candidates
    ).items():
        duplicate = candidates_by_key[duplicate_key]
        expected_aliases[formal_candidate_key(winner)].append(
            str(duplicate["qualified_name"])
        )
    for values in expected_aliases.values():
        values.sort()
    if len(candidates_by_key) != PINNED_CANDIDATE_COUNT:
        checker.fail("independent formal candidate keys are not unique and complete")
    categories = category_map(contract)
    statuses = status_map(contract)
    msc_policy = require_dict(
        contract.get("msc_coverage_policy"), "contract.msc_coverage_policy"
    )
    msc_top_classes = set(
        require_list(msc_policy.get("top_level_classes"), "contract MSC top classes")
    )
    qualified_seen: dict[Any, str] = {}
    statement_seen: dict[Any, str] = {}
    declaration_seen: dict[Any, str] = {}
    candidate_seen: dict[str, str] = {}
    normalized_formal_types: dict[str, str] = {}
    for index, row in enumerate(records):
        label = f"release {release} catalog record[{index}]"
        atv = record_variant_id(row)
        if atv is None:
            checker.fail(f"{label} lacks variant_id")
            continue
        try:
            ordinal(atv, ATV_RE)
            stage = require_string(record_stage_id(row), f"{label}.stage_claim_id")
            if ordinal(atv, ATV_RE) != ordinal(stage, S5_RE):
                raise CheckFailure(f"{label} ATV/S5 ordinal mismatch")
            # The 3,484 inherited rows are governed by exact migration and
            # identity conservation below.  Stage5 source pins, raw locators,
            # and formal declaration/docstring contracts apply to additions.
            if origin_release(row) not in RELEASES:
                continue
            statement = require_dict(mathematical_statement(row), f"{label}.statement")
            if statement in (None, "", {}, []):
                raise CheckFailure(f"{label} has an empty semantic statement")
            observed_statement_hash = require_sha256(
                row.get("statement_sha256"), f"{label}.statement_sha256"
            )
            if observed_statement_hash != statement_digest(statement):
                raise CheckFailure(f"{label} semantic statement hash is stale")
            nested_statement = require_dict(
                row.get("mathematical_statement"), f"{label}.mathematical_statement"
            )
            nested_statement_hash = require_sha256(
                nested_statement.get("statement_sha256"),
                f"{label}.mathematical_statement.statement_sha256",
            )
            if nested_statement_hash != statement_digest(nested_statement):
                raise CheckFailure(f"{label} nested mathematical statement hash is stale")
            nested_projection = {
                key: value
                for key, value in nested_statement.items()
                if key != "statement_sha256"
            }
            if nested_projection != statement:
                raise CheckFailure(
                    f"{label} flat/nested mathematical statement projection drifted"
                )
            if nested_statement_hash != observed_statement_hash:
                raise CheckFailure(f"{label} flat/nested statement hashes differ")
            dedupe = require_dict(row.get("dedupe"), f"{label}.dedupe")
            normalized_formal = require_sha256(
                dedupe.get("normalized_statement_sha256"),
                f"{label}.dedupe.normalized_statement_sha256",
            )
            expected_normalized_formal = contextual_statement_sha256(row)
            if normalized_formal != expected_normalized_formal:
                raise CheckFailure(f"{label} contextual normalized statement hash is stale")
            semantic_payload = {
                "record_role": row.get("record_role"),
                "atomicity": row.get("atomicity"),
                "truth_apt": row.get("truth_apt"),
                "normalized_formal_statement_sha256": normalized_formal,
                "mathematical_statement_sha256": nested_statement_hash,
            }
            if require_sha256(
                row.get("semantic_payload_sha256"), f"{label}.semantic_payload_sha256"
            ) != sha256_bytes(canonical_json_bytes(semantic_payload)):
                raise CheckFailure(f"{label} semantic payload hash is stale")
            source_id = require_string(record_source_id(row), f"{label}.formal source_id")
            if source_id not in sources:
                raise CheckFailure(f"{label} cites unknown source {source_id}")
            qualified_name = require_string(
                record_qualified_name(row), f"{label}.formal_statement.qualified_declaration"
            )
            if QUALIFIED_NAME_RE.fullmatch(qualified_name) is None:
                raise CheckFailure(f"{label} has malformed qualified_name")
            locator = require_dict(record_locator(row), f"{label}.formal_statement.locator")
            if locator.get("source_id") != source_id or row.get("source_id") != source_id:
                raise CheckFailure(f"{label} flat/nested locator source_id drifted")
            member_path = require_string(
                locator.get("member_path"), f"{label}.locator.member_path"
            )
            candidate_key = (
                f"formal-conjectures:{member_path}#{qualified_name}"
            )
            candidate = candidates_by_key.get(candidate_key)
            if candidate is None:
                raise CheckFailure(
                    f"{label} is not an independently rebuilt pinned candidate: "
                    f"{candidate_key}"
                )
            expected_identity = allocations_by_atv.get(atv)
            if expected_identity is None:
                raise CheckFailure(
                    f"{label} has no independently selected allocation at {atv}"
                )
            if expected_identity["candidate_key"] != candidate_key:
                raise CheckFailure(
                    f"{label} candidate/ordinal binding differs from independent "
                    "selection and allocation"
                )
            previous_candidate_atv = candidate_seen.get(candidate_key)
            if previous_candidate_atv is not None and previous_candidate_atv != atv:
                raise CheckFailure(
                    f"{label} reallocates pinned candidate already used by "
                    f"{previous_candidate_atv}"
                )
            candidate_seen[candidate_key] = atv
            block = locator_payload(checker, sources[source_id], locator, label)
            declaration = require_string(
                record_declaration(row), f"{label}.formal_statement.declaration_text"
            )
            docstring = require_string(
                record_docstring(row), f"{label}.formal_statement.docstring"
            )
            formal = require_dict(row.get("formal_statement"), f"{label}.formal_statement")
            expected_raw_category = str(candidate["category"])
            expected_category = mapping_value(
                categories, source_id, expected_raw_category
            )
            expected_status = mapping_value(
                statuses, source_id, expected_raw_category
            )
            compact_declaration = "".join(
                str(candidate["declaration_statement"]).split()
            )
            answer_placeholder = "answer(sorry)" in compact_declaration
            expected_claim_kind = (
                "theorem"
                if expected_raw_category in {"research solved", "textbook"}
                else ("open_problem" if answer_placeholder else "conjecture")
            )
            expected_statement = {
                "completeness": "source_docstring_plus_exact_formal",
                "component_extraction_status": "not_separately_parsed",
                "language": "en",
                "natural_language": str(candidate["docstring"]).strip(),
                "hypotheses": [],
                "conclusion": None,
                "scope": None,
                "formal_type": candidate["statement"],
            }
            if statement != expected_statement:
                raise CheckFailure(
                    f"{label} mathematical statement differs from source-derived record"
                )
            source_bindings = {
                "schema_version": (
                    row.get("schema_version"),
                    "awesome-theorems/stage5-math-claim-record/5.0",
                ),
                "origin_stage": (row.get("origin_stage"), "Stage5"),
                "curation_key": (
                    row.get("curation_key"),
                    "formal-conjectures/"
                    + sha256_bytes(candidate_key.encode("utf-8"))[:40],
                ),
                "display_name": (
                    row.get("display_name"), candidate["qualified_name"]
                ),
                "aliases": (
                    row.get("aliases"), expected_aliases.get(candidate_key, [])
                ),
                "owner_domain": (row.get("owner_domain"), "mathematics"),
                "membership_domains": (
                    row.get("membership_domains"), ["mathematics"]
                ),
                "record_role": (row.get("record_role"), "claim"),
                "atomicity": (row.get("atomicity"), "atomic"),
                "truth_apt": (row.get("truth_apt"), True),
                "lifecycle": (row.get("lifecycle"), "active"),
                "lineage": (row.get("lineage"), []),
                "source_id": (source_id, PINNED_FORMAL_SOURCE_ID),
                "raw_category": (row.get("raw_category"), expected_raw_category),
                "raw_status": (row.get("raw_status"), expected_raw_category),
                "category": (row.get("category"), expected_category),
                "material_status": (
                    material_status(row),
                    expected_status.casefold() if isinstance(expected_status, str) else None,
                ),
                "claim_kind": (row.get("claim_kind"), expected_claim_kind),
                "current_claim_kind": (
                    row.get("current_claim_kind"), expected_claim_kind
                ),
                "historical_kind": (
                    row.get("historical_kind"), expected_claim_kind
                ),
                "origin_release": (
                    origin_release(row), expected_identity["origin_release"]
                ),
                "release_id": (
                    row.get("release_id"), expected_identity["origin_release"]
                ),
                "occurrence ID": (
                    row.get("occurrence_id"), expected_identity["occurrence_id"]
                ),
                "family ID": (
                    row.get("family_id"), expected_identity["family_id"]
                ),
                "sense ID": (
                    row.get("sense_id"), expected_identity["sense_id"]
                ),
                "stage ID": (stage, expected_identity["stage_claim_id"]),
                "declaration_kind": (
                    row.get("declaration_kind"), candidate["declaration_kind"]
                ),
                "formal_shape": (
                    row.get("formal_shape"),
                    "answer_placeholder" if answer_placeholder else "direct_prop",
                ),
                "classification_status": (
                    row.get("classification_status"),
                    "source_curated_machine_extracted",
                ),
                "qualified_name": (qualified_name, candidate["qualified_name"]),
                "module": (row.get("module"), candidate["module"]),
                "namespace": (row.get("namespace"), candidate["namespace"]),
                "formal declaration": (
                    declaration, candidate["declaration_statement"]
                ),
                "formal type": (row.get("formal_type"), candidate["statement"]),
                "formal docstring": (docstring, candidate["docstring_raw"]),
                "AMS classes": (row.get("ams"), candidate["ams"]),
                "primary AMS class": (
                    row.get("primary_ams_class"), candidate["ams"][0]
                ),
                "declaration name": (
                    formal.get("declaration_name"), candidate["local_name"]
                ),
                "natural-language statement": (
                    mathematical_statement(row).get("natural_language"),
                    str(candidate["docstring"]).strip(),
                ),
                "source statement hash": (
                    require_dict(row.get("dedupe"), f"{label}.dedupe").get(
                        "source_statement_sha256"
                    ),
                    candidate["statement_sha256"],
                ),
                "source locator/range": (
                    locator, formal_source_locator(candidate)
                ),
            }
            for field, (observed, expected) in source_bindings.items():
                if observed != expected:
                    raise CheckFailure(
                        f"{label} {field} differs from independently parsed source"
                    )
            expected_sorry_free = bool(candidate.get("hasSorryFreeProof"))
            if (
                formal.get("sorry_free") is not expected_sorry_free
                or formal.get("axioms")
                != ([] if expected_sorry_free else ["sorryAx"])
            ):
                raise CheckFailure(
                    f"{label} proof metadata differs from independently parsed source"
                )
            for field, payload in (
                ("formal_declaration_sha256", declaration),
                ("formal_type_sha256", require_string(row.get("formal_type"), f"{label}.formal_type")),
                ("formal_docstring_sha256", docstring),
            ):
                if require_sha256(row.get(field), f"{label}.{field}") != sha256_bytes(payload.encode("utf-8")):
                    raise CheckFailure(f"{label} {field} is stale")
            redundant_pairs = {
                "locator": locator,
                "module": row.get("module"),
                "namespace": row.get("namespace"),
                "qualified_declaration": qualified_name,
                "declaration_kind": row.get("declaration_kind"),
                "declaration_text": declaration,
                "declaration_sha256": row.get("formal_declaration_sha256"),
                "declaration_type": row.get("formal_type"),
                "declaration_type_sha256": row.get("formal_type_sha256"),
                "docstring": docstring,
                "docstring_sha256": row.get("formal_docstring_sha256"),
            }
            for key, expected in redundant_pairs.items():
                if formal.get(key) != expected:
                    raise CheckFailure(f"{label} flat/formal_statement {key} drifted")
            if dedupe.get("formal_type_sha256") != row.get("formal_type_sha256"):
                raise CheckFailure(f"{label} dedupe/formal type hash drifted")
            expected_dedupe_fixed = {
                "source_statement_sha256": candidate["statement_sha256"],
                "normalized_statement_sha256": (
                    formal_contextual_statement_sha256(candidate)
                ),
                "qualified_name_key": normalized_text(qualified_name),
                "candidate_atv_ids": [],
                "verdict": "unique_exact_source_declaration",
                "validation_status": "machine_validated_exact",
                "duplicate_grants_quota": False,
                "no_evidence_or_status_inheritance": True,
            }
            if any(
                dedupe.get(key) != expected
                for key, expected in expected_dedupe_fixed.items()
            ):
                raise CheckFailure(
                    f"{label} dedupe metadata differs from independent source truth"
                )
            expected_qualified_key = normalized_text(qualified_name)
            if dedupe.get("qualified_name_key") != expected_qualified_key:
                raise CheckFailure(f"{label} dedupe qualified-name key is stale")
            previous_formal_type = normalized_formal_types.get(normalized_formal)
            if previous_formal_type is not None and previous_formal_type != dedupe.get("formal_type_sha256"):
                raise CheckFailure(
                    f"{label} normalized-statement hash collides across unequal formal types"
                )
            normalized_formal_types[normalized_formal] = str(dedupe.get("formal_type_sha256"))
            identity_payload = {
                "formal_type_sha256": dedupe.get("formal_type_sha256"),
                "normalized_statement_sha256": normalized_formal,
            }
            if dedupe.get("identity_payload_sha256") != sha256_bytes(
                canonical_json_bytes(identity_payload)
            ):
                raise CheckFailure(f"{label} dedupe identity payload hash is stale")
            allocation = require_dict(row.get("allocation"), f"{label}.allocation")
            for field, expected in {
                "family_action": "new_family",
                "append_only": True,
            }.items():
                if allocation.get(field) != expected:
                    raise CheckFailure(
                        f"{label} allocation.{field} differs from source allocation policy"
                    )
            if allocation.get("transaction_id") != expected_identity["transaction_id"]:
                raise CheckFailure(
                    f"{label} allocation transaction differs from independent ordinal"
                )
            allocation_payload = {
                "origin_release": row.get("origin_release"),
                "source_id": source_id,
                "qualified_name": qualified_name,
                "formal_type_sha256": row.get("formal_type_sha256"),
                "statement_sha256": observed_statement_hash,
                "dedupe.verdict": dedupe.get("verdict"),
                "allocation.family_action": allocation.get("family_action"),
            }
            if allocation.get("allocation_request_sha256") != sha256_bytes(
                canonical_json_bytes(allocation_payload)
            ):
                raise CheckFailure(f"{label} allocation request hash is stale")
            decoded = block.decode("utf-8", errors="strict")
            if declaration not in decoded:
                raise CheckFailure(f"{label} declaration is not contained in its raw block")
            if docstring not in decoded:
                raise CheckFailure(f"{label} docstring is not contained in its raw block")
            local_name = require_string(
                formal.get("declaration_name"), f"{label}.formal_statement.declaration_name"
            )
            if local_name not in declaration:
                raise CheckFailure(f"{label} local declaration name is absent from declaration")
            expected_module = member_path[:-5].replace("/", ".") if member_path.endswith(".lean") else ""
            if row.get("module") != expected_module:
                raise CheckFailure(f"{label} module does not match source member context")
            proof_state = row.get("formal_proof_state")
            nested_proof_state = formal.get("elaboration_status")
            if (
                proof_state != "source_asserted_not_replayed"
                or nested_proof_state != "source_repository_statement"
            ):
                raise CheckFailure(
                    f"{label} overstates the non-replayed source proof state"
                )
            if proof_state == "kernel_checked_sorry_free" and (
                formal.get("sorry_free") is not True
                or re.search(r"\bsorry\b", decoded) is not None
            ):
                raise CheckFailure(f"{label} falsely claims kernel-checked sorry-free proof")
            if re.search(r"\btype_of%", declaration):
                raise CheckFailure(f"{label} is a type_of% pointer and cannot grant quota")

            raw_category = require_string(row.get("raw_category"), f"{label}.raw_category")
            canonical_category = require_string(row.get("category"), f"{label}.category")
            expected_category = mapping_value(categories, source_id, raw_category)
            if expected_category is None or canonical_category != expected_category:
                raise CheckFailure(f"{label} category mapping is not contract-derived")
            raw_status = require_string(row.get("raw_status"), f"{label}.raw_status")
            expected_status = mapping_value(statuses, source_id, raw_status)
            if expected_status is None or material_status(row) != expected_status.casefold():
                raise CheckFailure(f"{label} status mapping is not contract-derived")
            if re.search(r"\banswer\s*\(\s*sorry\s*\)", declaration) and claim_kind(row) != "open_problem":
                raise CheckFailure(f"{label} answer(sorry) must be typed open_problem")
            ams_classes = require_list(row.get("ams"), f"{label}.ams")
            primary_ams = require_string(
                row.get("primary_ams_class"), f"{label}.primary_ams_class"
            )
            if primary_ams not in msc_top_classes:
                raise CheckFailure(f"{label} primary MSC class is outside MSC2020")
            if not ams_classes or any(
                not isinstance(value, str) or value[:2] not in msc_top_classes
                for value in ams_classes
            ):
                raise CheckFailure(f"{label} has malformed MSC classifications")
            if primary_ams not in {str(value)[:2] for value in ams_classes}:
                raise CheckFailure(f"{label} primary MSC class is not represented in ams")
            rights = require_dict(row.get("rights"), f"{label}.rights")
            source_spdx = {
                axis.get("spdx_expression")
                for axis in sources[source_id].get("rights", {}).get("axes", [])
                if isinstance(axis, dict) and isinstance(axis.get("spdx_expression"), str)
            }
            if rights.get("formal_code_terms") not in source_spdx:
                raise CheckFailure(f"{label} formal-code license is not source-authorized")
            if rights.get("status") in {"restricted"} or rights.get("redistribution_mode") == "excluded":
                raise CheckFailure(f"{label} has non-releasable rights status")
            if source_id not in rights.get("source_refs", []):
                raise CheckFailure(f"{label} rights record omits formal source")
            expected_rights = {
                "formal_code_terms": "Apache-2.0",
                "docstring_terms": (
                    "source-specific terms preserved; not independently cleared"
                ),
                "status": "source_terms_preserved_not_independently_cleared",
                "redistribution_mode": (
                    "source_terms_preserved_in_repository_inventory"
                ),
                "attribution": [
                    "The Formal Conjectures Authors",
                    candidate_key,
                ],
                "source_refs": [PINNED_FORMAL_SOURCE_ID],
                "not_independently_cleared": True,
            }
            if rights != expected_rights:
                raise CheckFailure(
                    f"{label} rights differ from the pinned source policy"
                )
            expected_status_detail = {
                "status_as_of": REVIEW_DATE,
                "basis": (
                    f"Pinned Formal Conjectures category {expected_raw_category!r} "
                    "is preserved as a source assertion; no independent truth or "
                    "proof replay is claimed."
                ),
                "source_refs": [PINNED_FORMAL_SOURCE_ID],
                "evidence_level": "source_asserted_as_of",
                "resolution_criterion": (
                    None
                    if expected_claim_kind == "theorem"
                    else "Resolve the exact Lean proposition by proof or counterexample."
                ),
                "known_special_cases": [],
            }
            if row.get("status_detail") != expected_status_detail:
                raise CheckFailure(
                    f"{label} status evidence overstates the source assertion"
                )
            expected_conditionality = {
                "mode": "none",
                "assumption_variant_ids": [],
                "implication_proof_status": "not_applicable",
                "antecedent_status": "not_applicable",
                "consequent_standalone_status": "not_applicable",
                "no_status_inheritance": True,
            }
            if row.get("conditionality") != expected_conditionality:
                raise CheckFailure(
                    f"{label} conditionality differs from source-derived policy"
                )
            provenance = require_dict(row.get("provenance"), f"{label}.provenance")
            expected_provenance = {
                "formal_source_ref": PINNED_FORMAL_SOURCE_ID,
                "source_refs": [PINNED_FORMAL_SOURCE_ID],
                "extraction_mode": "source_curated_machine_extracted",
                "extractor_version": FORMAL_SOURCE_SCHEMA_VERSION,
                "extraction_receipt_sha256": PINNED_EXTRACTION_JSONL_SHA256,
                "source_assertion_not_independent_truth_review": True,
            }
            if provenance != expected_provenance:
                raise CheckFailure(
                    f"{label} provenance is not exactly bound to the independent extraction"
                )
            expected_frontier = {
                "class": (
                    "source_asserted_solved"
                    if expected_claim_kind == "theorem"
                    else "source_asserted_open_frontier"
                ),
                "as_of": REVIEW_DATE,
                "basis": (
                    f"Formal Conjectures source category {expected_raw_category!r} "
                    "at the pinned commit."
                ),
                "source_refs": [PINNED_FORMAL_SOURCE_ID],
                "evidence_level": "source_category_signal",
            }
            if row.get("frontier") != expected_frontier:
                raise CheckFailure(
                    f"{label} frontier evidence overstates the source signal"
                )
            expected_importance = {
                "tier": "unranked_research_level",
                "basis": "source_category_signal_only",
                "rationale": (
                    "No independent per-record importance ranking was performed."
                ),
                "evidence_level": "unranked",
            }
            if row.get("importance") != expected_importance:
                raise CheckFailure(
                    f"{label} importance overstates independent review"
                )

            if origin_release(row) in RELEASES:
                qualified_key, statement_key, declaration_key = quota_duplicate_keys(row)
                for seen, key, kind in (
                    (qualified_seen, qualified_key, "qualified name"),
                    (statement_seen, statement_key, "statement"),
                    (declaration_seen, declaration_key, "declaration"),
                ):
                    previous = seen.get(key)
                    if previous is not None and previous != atv:
                        checker.fail(
                            f"{label} duplicates {kind} of {previous}; duplicates cannot grant quota"
                        )
                    else:
                        seen[key] = atv
        except (CheckFailure, UnicodeError) as error:
            checker.fail(str(error))


def check_quota_duplicates(
    checker: Checker, release: str, records: Sequence[Mapping[str, Any]]
) -> None:
    """Reject duplicate credit keys without consulting generator metadata."""

    indexes: tuple[tuple[str, dict[Any, str]], ...] = (
        ("qualified name", {}),
        ("statement", {}),
        ("declaration", {}),
    )
    for row in records:
        if origin_release(row) not in RELEASES:
            continue
        atv = record_variant_id(row)
        if not isinstance(atv, str):
            continue
        try:
            keys = quota_duplicate_keys(row)
        except CheckFailure as error:
            checker.fail(f"release {release} {atv} cannot rebuild duplicate keys: {error}")
            continue
        for (kind, seen), key in zip(indexes, keys):
            previous = seen.get(key)
            if previous is not None and previous != atv:
                checker.fail(
                    f"release {release} {atv} duplicates {kind} of {previous}; "
                    "duplicates cannot grant quota"
                )
            else:
                seen[key] = atv


def check_declared_catalog_counts(
    checker: Checker,
    release: str,
    catalog: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
) -> tuple[set[str], set[str]]:
    origin = [row for row in records if origin_release(row) == release]
    theorems = {
        value
        for row in origin
        if is_quota_theorem(row) and isinstance((value := record_variant_id(row)), str)
    }
    open_claims = {
        value
        for row in origin
        if is_quota_open_claim(row) and isinstance((value := record_variant_id(row)), str)
    }
    counts = catalog.get("counts")
    if isinstance(counts, dict):
        for key, expected in {
            "records": len(records),
            "origin_theorems": len(theorems),
            "origin_open_claims": len(open_claims),
        }.items():
            if key in counts and counts[key] != expected:
                checker.fail(f"release {release} catalog count {key} is not recomputed truth")
    return theorems, open_claims


def check_catalog_allocation_suffixes(
    checker: Checker, release: str, records: Sequence[Mapping[str, Any]]
) -> None:
    contracts = (
        ("occurrence_id", ATO_RE, PARENT_HIGH_WATERMARK),
        ("family_id", ATF_RE, PARENT_FAMILY_HIGH_WATERMARK),
        ("sense_id", ATS_RE, PARENT_HIGH_WATERMARK),
        ("variant_id", ATV_RE, PARENT_HIGH_WATERMARK),
    )
    for field, pattern, highwater in contracts:
        values = [row.get(field) for row in records]
        observed = exact_unique_strings(
            checker, values, f"release {release} catalog {field}", pattern
        )
        try:
            ordinals = sorted(ordinal(value, pattern) for value in observed)
        except CheckFailure as error:
            checker.fail(str(error))
            continue
        expected = list(range(highwater + 1, highwater + len(records) + 1))
        if ordinals != expected:
            checker.fail(
                f"release {release} {field} allocations are not the contiguous "
                f"append-only suffix after {highwater}"
            )
    for row in records:
        allocation = row.get("allocation")
        if not isinstance(allocation, dict) or allocation.get("family_action") != "new_family":
            checker.fail(
                f"release {release} accepted {record_variant_id(row)} does not allocate a new family"
            )


def load_release_documents(checker: Checker, release: str) -> dict[str, dict[str, Any]]:
    result = {MANIFEST_NAME: checker.load_json(release_dir(release) / MANIFEST_NAME)}
    for name in RELEASE_FILES:
        result[name] = checker.load_json(release_dir(release) / name)
    return result


def manifest_artifacts(manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = manifest.get("artifacts")
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise CheckFailure("release manifest has no artifact inventory")
    return list(value)


def check_manifest(
    checker: Checker,
    release: str,
    manifest: Mapping[str, Any],
    documents: Mapping[str, Mapping[str, Any]],
) -> str:
    if set(manifest) != MANIFEST_FIELDS:
        checker.fail(
            f"release {release} manifest fields are not exact: "
            f"missing={sorted(MANIFEST_FIELDS-set(manifest))!r}, "
            f"extra={sorted(set(manifest)-MANIFEST_FIELDS)!r}"
        )
    if manifest.get("release") != release:
        checker.fail(f"release {release} manifest release label drifted")
    if not isinstance(manifest.get("schema_version"), str):
        checker.fail(f"release {release} manifest schema_version is malformed")
    if not isinstance(manifest.get("counts"), dict):
        checker.fail(f"release {release} manifest counts is not an object")
    actual = release_inventory(checker.root, release)
    actual_by_path = {row["path"]: row for row in actual}
    rows = manifest_artifacts(manifest)
    observed_paths = exact_unique_strings(
        checker,
        (row.get("path") for row in rows),
        f"release {release} manifest artifact paths",
    )
    if observed_paths != set(RELEASE_FILES):
        checker.fail(f"release {release} manifest artifact set is not exact")
    for row in rows:
        if set(row) != MANIFEST_ARTIFACT_FIELDS:
            checker.fail(
                f"release {release} manifest artifact row fields are not exact for "
                f"{row.get('path')!r}"
            )
        path = row.get("path")
        if path not in actual_by_path:
            continue
        actual_row = actual_by_path[path]
        if row.get("sha256") != actual_row["sha256"]:
            checker.fail(f"release {release} manifest hash drifted for {path}")
        if row.get("size_bytes") != actual_row["size_bytes"]:
            checker.fail(f"release {release} manifest size drifted for {path}")
        expected_count = artifact_row_count(str(path), documents[path])
        if row.get("row_count") != expected_count:
            checker.fail(f"release {release} manifest row_count drifted for {path}")
    root = release_root_sha256(actual)
    if manifest.get("release_root_sha256") != root:
        checker.fail(f"release {release} release_root_sha256 is stale")
    check_sealed_document(checker, f"release {release} manifest", manifest)
    return root


def registry_variant_ids(document: Mapping[str, Any]) -> list[str]:
    values = document.get("variants")
    if not isinstance(values, list):
        raise CheckFailure("Claim_ID_Registry.json has no variants array")
    output: list[str] = []
    for row in values:
        if isinstance(row, str):
            output.append(row)
        elif isinstance(row, dict) and isinstance(record_variant_id(row), str):
            output.append(str(record_variant_id(row)))
        else:
            raise CheckFailure("Claim_ID_Registry variants contains malformed row")
    return output


def check_numbering_and_migration(
    checker: Checker,
    release: str,
    documents: Mapping[str, Mapping[str, Any]],
    catalog_ids: set[str],
    parent_v4_ids: set[str],
) -> tuple[set[str], dict[str, str]]:
    registry_ids = exact_unique_strings(
        checker,
        registry_variant_ids(documents["Claim_ID_Registry.json"]),
        f"release {release} registry variants",
        ATV_RE,
    )
    expected_registry = parent_v4_ids | catalog_ids
    if registry_ids != expected_registry:
        checker.fail(
            f"release {release} registry is not exactly v4 history plus Stage5 catalog"
        )

    mappings = artifact_rows(documents["Stage5_Claim_ID_Registry.json"])
    pairs: list[tuple[str, str]] = []
    for row in mappings:
        atv = record_variant_id(row)
        stage = record_stage_id(row)
        if not isinstance(atv, str) or not isinstance(stage, str):
            checker.fail(f"release {release} numbering row lacks ATV/S5 IDs")
            continue
        try:
            if ordinal(atv, ATV_RE) != ordinal(stage, S5_RE):
                checker.fail(f"release {release} numbering ordinal mismatch: {atv}/{stage}")
        except CheckFailure as error:
            checker.fail(str(error))
            continue
        pairs.append((atv, stage))
    atv_domain = exact_unique_strings(
        checker, (atv for atv, _ in pairs), f"release {release} numbering ATV domain", ATV_RE
    )
    stage_range = exact_unique_strings(
        checker, (stage for _, stage in pairs), f"release {release} numbering S5 range", S5_RE
    )
    if atv_domain != registry_ids or len(stage_range) != len(registry_ids):
        checker.fail(f"release {release} ATV↔S5 map is not a total bijection")
    mapping = dict(pairs)

    migrations = artifact_rows(documents["Migration_v4_to_v5.json"])
    migration_document = documents["Migration_v4_to_v5.json"]
    receipt = checker.load_json(V4_IMPORT_RECEIPT_PATH)
    receipt_binding = require_dict(
        migration_document.get("v4_import_receipt"),
        f"release {release} migration v4_import_receipt",
    )
    receipt_path = checker.path(V4_IMPORT_RECEIPT_PATH)
    if (
        receipt_binding.get("path") != str(V4_IMPORT_RECEIPT_PATH)
        or receipt_binding.get("sha256") != sha256_file(receipt_path)
        or receipt_binding.get("authority_sha256") != receipt.get("authority_sha256")
    ):
        checker.fail(f"release {release} migration V4 receipt binding is stale")
    authoritative_inputs = require_list(
        migration_document.get("authoritative_inputs"),
        f"release {release} migration authoritative_inputs",
    )
    expected_input_paths = {
        str(V4_CATALOG_PATH),
        str(V4_REGISTRY_PATH),
        str(V4_STAGE_REGISTRY_PATH),
        str(CONTRACT_PATH),
        str(SCHEMA_PATH),
        str(SOURCE_REGISTRY_PATH),
        str(V4_IMPORT_RECEIPT_PATH),
    }
    input_paths = exact_unique_strings(
        checker,
        (
            row.get("path") if isinstance(row, dict) else None
            for row in authoritative_inputs
        ),
        f"release {release} migration authoritative input paths",
    )
    if input_paths != expected_input_paths:
        checker.fail(f"release {release} migration input path set is not exact")
    if [row.get("path") for row in authoritative_inputs if isinstance(row, dict)] != sorted(
        input_paths
    ):
        checker.fail(f"release {release} migration inputs are not path-sorted")
    for index, value in enumerate(authoritative_inputs):
        value = require_dict(value, f"release {release} migration input[{index}]")
        if set(value) != {"path", "sha256", "size_bytes"}:
            checker.fail(f"release {release} migration input[{index}] fields are not exact")
            continue
        path_value = require_string(value.get("path"), f"migration input[{index}].path")
        resolved = checker.path(path_value)
        if (
            not resolved.is_file()
            or value.get("sha256") != sha256_file(resolved)
            or value.get("size_bytes") != resolved.stat().st_size
        ):
            checker.fail(f"release {release} migration input binding drifted: {path_value}")

    v4_catalog = checker.load_json(V4_CATALOG_PATH)
    v4_by_atv = {
        str(row.get("variant_id")): row
        for row in require_list(v4_catalog.get("records"), "V4 catalog records")
        if isinstance(row, dict) and isinstance(row.get("variant_id"), str)
    }
    receipt_crosswalk = {
        str(row.get("atv_id")): row
        for row in require_list(
            require_dict(receipt.get("identity_import"), "V4 receipt identity_import").get(
                "variant_stage_crosswalk"
            ),
            "V4 receipt variant_stage_crosswalk",
        )
        if isinstance(row, dict) and isinstance(row.get("atv_id"), str)
    }
    required_migration_fields = {
        "ordinal",
        "variant_id",
        "v4_variant_id",
        "s4_claim_id",
        "stage_claim_id",
        "migration_action",
        "predecessor_record_sha256",
        "current_resolution",
    }
    required_resolution_fields = {
        "kind",
        "terminal_atv_ids",
        "terminal_s5_ids",
        "default_child",
        "evidence_inherited",
    }
    migration_ids: list[str] = []
    historical: list[str] = []
    for index, value in enumerate(migrations):
        label = f"release {release} migration[{index}]"
        try:
            row = require_dict(value, label)
            if set(row) != required_migration_fields:
                raise CheckFailure(f"{label} fields are not exact")
            target = require_string(record_variant_id(row), f"{label}.variant_id")
            stage = require_string(record_stage_id(row), f"{label}.stage_claim_id")
            if target not in registry_ids or mapping.get(target) != stage:
                raise CheckFailure(f"{label} is outside the release ATV/S5 registry")
            target_ordinal = ordinal(target, ATV_RE)
            if row.get("ordinal") != target_ordinal or ordinal(stage, S5_RE) != target_ordinal:
                raise CheckFailure(f"{label} ordinal is stale")
            migration_ids.append(target)
            resolution = require_dict(row.get("current_resolution"), f"{label}.current_resolution")
            if set(resolution) != required_resolution_fields:
                raise CheckFailure(f"{label}.current_resolution fields are not exact")
            if resolution.get("default_child") is not None:
                raise CheckFailure(f"{label} current resolution chooses a default child")
            if resolution.get("evidence_inherited") is not False:
                raise CheckFailure(f"{label} current resolution inherits evidence")

            if target in parent_v4_ids:
                historical.append(target)
                if row.get("v4_variant_id") != target:
                    raise CheckFailure(f"{label} rebinds historical ATV {target}")
                expected_s4 = f"S4-CLM-{target_ordinal:08d}"
                if row.get("s4_claim_id") != expected_s4:
                    raise CheckFailure(f"{label} rebinds historical S4 ID")
                predecessor = v4_by_atv.get(target)
                if predecessor is None or row.get("predecessor_record_sha256") != sha256_bytes(
                    canonical_json_bytes(predecessor)
                ):
                    raise CheckFailure(f"{label} predecessor record hash is stale")
                if row.get("migration_action") != "historical_binding_preserved":
                    raise CheckFailure(f"{label} historical migration action is wrong")
                crosswalk = require_dict(
                    receipt_crosswalk.get(target), f"{label} receipt crosswalk"
                )
                receipt_resolution = require_dict(
                    crosswalk.get("current_resolution"), f"{label} receipt resolution"
                )
                target_s4_ids = require_list(
                    receipt_resolution.get("target_stage_claim_ids"),
                    f"{label} receipt target_stage_claim_ids",
                )
                terminal_ordinals = [
                    ordinal(str(item), re.compile(r"^S4-CLM-([0-9]{8})$"))
                    for item in target_s4_ids
                ]
                expected_kind = receipt_resolution.get("kind")
                expected_terminal_atv = [f"ATV-{number:08d}" for number in terminal_ordinals]
                expected_terminal_s5 = [f"S5-CLM-{number:08d}" for number in terminal_ordinals]
            else:
                if any(
                    row.get(field) is not None
                    for field in ("v4_variant_id", "s4_claim_id", "predecessor_record_sha256")
                ):
                    raise CheckFailure(f"{label} new allocation claims historical identity")
                if row.get("migration_action") != "new_stage5_allocation":
                    raise CheckFailure(f"{label} new migration action is wrong")
                expected_kind = "current"
                expected_terminal_atv = [target]
                expected_terminal_s5 = [stage]
            if resolution.get("kind") != expected_kind:
                raise CheckFailure(f"{label} current-resolution kind drifted")
            if resolution.get("terminal_atv_ids") != expected_terminal_atv:
                raise CheckFailure(f"{label} terminal ATV resolution drifted")
            if resolution.get("terminal_s5_ids") != expected_terminal_s5:
                raise CheckFailure(f"{label} terminal S5 resolution drifted")
        except CheckFailure as error:
            checker.fail(str(error))
    migration_set = exact_unique_strings(
        checker, migration_ids, f"release {release} migration ATV domain", ATV_RE
    )
    if migration_set != registry_ids:
        checker.fail(f"release {release} migration is not total over its registry")
    historical_set = exact_unique_strings(
        checker, historical, f"release {release} v4 migration domain", ATV_RE
    )
    if historical_set != parent_v4_ids:
        checker.fail(f"release {release} does not migrate all 3484 historical ATV IDs")
    return registry_ids, mapping


def projection_ids(document: Mapping[str, Any]) -> list[str]:
    values = document.get("stage_claim_ids", document.get("ids"))
    if isinstance(values, list):
        return [value for value in values if isinstance(value, str)]
    return [
        value
        for row in artifact_rows(document)
        if isinstance((value := record_stage_id(row)), str)
    ]


def check_projections(
    checker: Checker,
    release: str,
    documents: Mapping[str, Mapping[str, Any]],
    catalog_by_atv: Mapping[str, Mapping[str, Any]],
    stage_by_atv: Mapping[str, str],
) -> tuple[set[str], set[str]]:
    theorem_expected = {
        stage_by_atv[atv]
        for atv, row in catalog_by_atv.items()
        if is_quota_theorem(row)
    }
    open_expected = {
        stage_by_atv[atv]
        for atv, row in catalog_by_atv.items()
        if is_quota_open_claim(row)
    }
    theorem_observed = exact_unique_strings(
        checker,
        projection_ids(documents["Theorem_List.json"]),
        f"release {release} theorem projection",
        S5_RE,
    )
    open_observed = exact_unique_strings(
        checker,
        projection_ids(documents["Open_Claim_List.json"]),
        f"release {release} open projection",
        S5_RE,
    )
    by_statement: defaultdict[str, list[tuple[str, Mapping[str, Any]]]] = defaultdict(list)
    for atv, row in catalog_by_atv.items():
        dedupe = row.get("dedupe")
        digest = (
            dedupe.get("normalized_statement_sha256")
            if isinstance(dedupe, dict)
            else None
        )
        if isinstance(digest, str):
            by_statement[digest].append((atv, row))
    for digest, members in by_statement.items():
        source_categories = {row.get("raw_category") for _atv, row in members}
        if "research solved" in source_categories or "textbook" in source_categories:
            forbidden = {
                stage_by_atv[atv]
                for atv, row in members
                if row.get("raw_category") == "research open"
            }
            if forbidden & open_observed:
                checker.fail(
                    f"release {release} Open_List includes lower-priority open duplicate "
                    f"of solved statement {digest}"
                )
    if theorem_observed != theorem_expected:
        checker.fail(f"release {release} theorem projection is not catalog set-equal")
    if open_observed != open_expected:
        checker.fail(f"release {release} open projection is not catalog set-equal")
    if theorem_observed & open_observed:
        checker.fail(f"release {release} theorem/open projections overlap")
    return theorem_expected, open_expected


def _formal_is_pointer(candidate: Mapping[str, Any]) -> bool:
    return "type_of%" in str(candidate["declaration_statement"])


def _formal_is_answer_placeholder(candidate: Mapping[str, Any]) -> bool:
    compact = "".join(str(candidate["declaration_statement"]).split())
    return "answer(sorry)" in compact


def _formal_duplicate_map(
    candidates: Sequence[Mapping[str, Any]],
) -> dict[str, tuple[Mapping[str, Any], str]]:
    priority = {"research solved": 0, "textbook": 1, "research open": 2}
    eligible = [
        candidate for candidate in candidates if not _formal_is_pointer(candidate)
    ]
    eligible.sort(
        key=lambda candidate: (
            priority[str(candidate["category"])],
            formal_candidate_key(candidate),
        )
    )
    winners: dict[str, Mapping[str, Any]] = {}
    duplicates: dict[str, tuple[Mapping[str, Any], str]] = {}
    for candidate in eligible:
        digest = formal_contextual_statement_sha256(candidate)
        winner = winners.get(digest)
        if winner is None:
            winners[digest] = candidate
        else:
            duplicates[formal_candidate_key(candidate)] = (
                winner,
                "contextual_exact_statement",
            )
    return duplicates


def _formal_source_collection(candidate: Mapping[str, Any]) -> str:
    parts = str(candidate["source_file"]).split("/")
    return parts[1] if len(parts) > 2 else "root"


def _formal_round_robin(
    candidates: Iterable[Mapping[str, Any]], count: int
) -> list[Mapping[str, Any]]:
    buckets: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        buckets[(str(candidate["ams"][0]), _formal_source_collection(candidate))].append(
            candidate
        )
    for values in buckets.values():
        values.sort(
            key=lambda candidate: (
                formal_contextual_statement_sha256(candidate),
                candidate["qualified_name"],
                formal_candidate_key(candidate),
            )
        )
    keys = sorted(buckets)
    offsets = {key: 0 for key in keys}
    selected: list[Mapping[str, Any]] = []
    while len(selected) < count:
        advanced = False
        for key in keys:
            offset = offsets[key]
            values = buckets[key]
            if offset >= len(values):
                continue
            selected.append(values[offset])
            offsets[key] += 1
            advanced = True
            if len(selected) == count:
                break
        if not advanced:
            break
    if len(selected) != count:
        raise CheckFailure(
            f"independent round-robin selected {len(selected)} of {count} rows"
        )
    return selected


def expected_formal_allocations(
    candidates: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Independently select releases and freeze every candidate-to-ID binding."""

    priority = {"research solved": 0, "textbook": 1, "research open": 2}
    eligible = [
        candidate for candidate in candidates if not _formal_is_pointer(candidate)
    ]
    eligible.sort(
        key=lambda candidate: (
            priority[str(candidate["category"])],
            formal_candidate_key(candidate),
        )
    )
    winners: dict[str, Mapping[str, Any]] = {}
    for candidate in eligible:
        winners.setdefault(
            formal_contextual_statement_sha256(candidate), candidate
        )
    unique = sorted(winners.values(), key=formal_candidate_key)
    literal_theorems = [
        candidate
        for candidate in unique
        if candidate["declaration_kind"] == "theorem"
        and not (
            candidate["category"] in {"research solved", "textbook"}
            and _formal_is_answer_placeholder(candidate)
        )
    ]
    solved = [
        candidate
        for candidate in literal_theorems
        if candidate["category"] == "research solved"
    ]
    textbook = [
        candidate
        for candidate in literal_theorems
        if candidate["category"] == "textbook"
    ]
    open_rows = [
        candidate
        for candidate in literal_theorems
        if candidate["category"] == "research open"
    ]
    direct_open = [
        candidate
        for candidate in open_rows
        if not _formal_is_answer_placeholder(candidate)
    ]
    problem_open = [
        candidate
        for candidate in open_rows
        if _formal_is_answer_placeholder(candidate)
    ]

    selected_solved_50 = _formal_round_robin(solved, 1000)
    solved_50_keys = {
        formal_candidate_key(candidate) for candidate in selected_solved_50
    }
    remaining_solved = [
        candidate
        for candidate in solved
        if formal_candidate_key(candidate) not in solved_50_keys
    ]
    selected_direct = (
        _formal_round_robin(direct_open, 1000)
        if len(direct_open) > 1000
        else sorted(direct_open, key=formal_candidate_key)
    )
    selected_problem = _formal_round_robin(
        problem_open, 1000 - len(selected_direct)
    )
    selected_50 = sorted(
        selected_solved_50 + selected_direct + selected_problem,
        key=formal_candidate_key,
    )
    solved_51_count = min(len(remaining_solved), 500)
    selected_solved_51 = _formal_round_robin(
        remaining_solved, solved_51_count
    )
    selected_textbook_51 = _formal_round_robin(
        textbook, 500 - solved_51_count
    )
    selected_51 = sorted(
        selected_solved_51 + selected_textbook_51,
        key=formal_candidate_key,
    )
    if len(selected_50) != 2000 or len(selected_51) != 500:
        raise CheckFailure("independent release-selection cardinalities drifted")
    combined = selected_50 + selected_51
    if len({formal_candidate_key(candidate) for candidate in combined}) != 2500:
        raise CheckFailure("independent release selections overlap")

    output: dict[str, dict[str, Any]] = {}
    for index, candidate in enumerate(combined):
        atv_ordinal = PARENT_HIGH_WATERMARK + index + 1
        family_ordinal = PARENT_FAMILY_HIGH_WATERMARK + index + 1
        key = formal_candidate_key(candidate)
        output[key] = {
            "candidate_key": key,
            "origin_release": "5.0" if index < len(selected_50) else "5.1",
            "ordinal": atv_ordinal,
            "variant_id": f"ATV-{atv_ordinal:08d}",
            "occurrence_id": f"ATO-{atv_ordinal:08d}",
            "sense_id": f"ATS-{atv_ordinal:08d}",
            "family_id": f"ATF-{family_ordinal:08d}",
            "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
            "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        }
    return output


def expected_candidate_dispositions(
    release: str,
    candidates: Sequence[Mapping[str, Any]],
    catalog_by_atv: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Recompute every credit and noncredit row from source plus catalog IDs."""

    identities = expected_formal_allocations(candidates)
    duplicate_map = _formal_duplicate_map(candidates)
    result: list[dict[str, Any]] = []
    for candidate in sorted(candidates, key=formal_candidate_key):
        key = formal_candidate_key(candidate)
        identity = identities.get(key)
        identity_visible = (
            identity
            if identity is not None
            and (
                identity.get("origin_release") == "5.0"
                or release == "5.1"
            )
            else None
        )
        duplicate = duplicate_map.get(key)
        target_variant: str | None = None
        target_stage: str | None = None
        duplicate_of_variant: str | None = None
        accepted = (
            identity is not None
            and identity.get("origin_release") == release
        )
        if accepted:
            disposition = "accepted_new_claim"
            grants = True
            target_variant = str(identity["variant_id"])
            target_stage = str(identity["stage_claim_id"])
            reason_code = "deterministic_round_robin_quota_selection"
        elif (
            identity_visible is not None
            and identity_visible.get("origin_release") != release
        ):
            disposition = "already_allocated_noncredit"
            grants = False
            target_variant = str(identity_visible["variant_id"])
            target_stage = str(identity_visible["stage_claim_id"])
            reason_code = "allocated_in_parent_release"
        elif _formal_is_pointer(candidate):
            disposition = "pointer_noncredit"
            grants = False
            reason_code = "type_of_pointer_no_identity_credit"
        elif duplicate is not None:
            grants = False
            winner_identity = identities.get(formal_candidate_key(duplicate[0]))
            winner_visible = (
                winner_identity
                if winner_identity is not None
                and (
                    winner_identity.get("origin_release") == "5.0"
                    or release == "5.1"
                )
                else None
            )
            if winner_visible is not None:
                disposition = "duplicate_noncredit"
                duplicate_of_variant = str(winner_visible["variant_id"])
                reason_code = duplicate[1]
            else:
                disposition = "excluded_by_source_policy"
                reason_code = "duplicate_winner_not_allocated_in_release"
        elif candidate["declaration_kind"] != "theorem":
            disposition = "excluded_by_source_policy"
            grants = False
            reason_code = "literal_theorem_only_quota"
        elif (
            candidate["category"] in {"research solved", "textbook"}
            and _formal_is_answer_placeholder(candidate)
        ):
            disposition = "status_blocked"
            grants = False
            reason_code = "solved_answer_placeholder_quarantined"
        elif (
            candidate["category"] == "research open"
            and identity_visible is None
        ):
            disposition = "open_reserve_noncredit"
            grants = False
            reason_code = "deterministic_open_reserve_not_allocated"
        else:
            disposition = "excluded_by_source_policy"
            grants = False
            reason_code = "deterministic_theorem_reserve_not_allocated"

        result.append(
            {
                "candidate_key": key,
                "source_id": PINNED_FORMAL_SOURCE_ID,
                "qualified_name": candidate["qualified_name"],
                "source_statement_sha256": candidate["statement_sha256"],
                "normalized_statement_sha256": (
                    formal_contextual_statement_sha256(candidate)
                ),
                "disposition": disposition,
                "reason_code": reason_code,
                "target_variant_id": target_variant,
                "target_s5_id": target_stage,
                "duplicate_of_variant_id": duplicate_of_variant,
                "grants_quota": grants,
                "origin_release": (
                    str(identity_visible["origin_release"])
                    if identity_visible is not None
                    else release
                ),
                "evidence_locator_sha256": sha256_bytes(
                    canonical_json_bytes(formal_source_locator(candidate))
                ),
            }
        )
    return result


def check_coverage_ledger(
    checker: Checker,
    release: str,
    ledger: Mapping[str, Any],
    catalog_by_atv: Mapping[str, Mapping[str, Any]],
    contract: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    candidates: Sequence[Mapping[str, Any]] | None = None,
) -> None:
    rebuilt_candidates = (
        tuple(candidates)
        if candidates is not None
        else rebuild_formal_candidates(checker, sources)
    )
    source_candidates_by_key = {
        formal_candidate_key(candidate): candidate
        for candidate in rebuilt_candidates
    }
    expected_dispositions = expected_candidate_dispositions(
        release, rebuilt_candidates, catalog_by_atv
    )
    expected_by_key = {
        str(row["candidate_key"]): row for row in expected_dispositions
    }
    coverage_contract = require_dict(
        contract.get("coverage_ledger_contract"), "contract.coverage_ledger_contract"
    )
    required_top = set(
        require_list(
            coverage_contract.get("top_level_required_fields"),
            "coverage contract top_level_required_fields",
        )
    )
    if set(ledger) != required_top:
        checker.fail(
            f"release {release} coverage top-level fields are not exact: "
            f"missing={sorted(required_top-set(ledger))!r}, "
            f"extra={sorted(set(ledger)-required_top)!r}"
        )
    if ledger.get("release") != release:
        checker.fail(f"release {release} coverage release label drifted")

    candidate_required = set(
        require_list(
            coverage_contract.get("candidate_disposition_required_fields"),
            "coverage contract candidate_disposition_required_fields",
        )
    )
    dispositions = set(
        require_list(
            coverage_contract.get("candidate_disposition_enum"),
            "coverage contract candidate_disposition_enum",
        )
    )
    rows = require_list(
        ledger.get("candidate_dispositions"),
        f"release {release} coverage candidate_dispositions",
    )
    if len(rows) != PINNED_CANDIDATE_COUNT:
        checker.fail(
            f"release {release} coverage has {len(rows)} candidates; "
            f"pinned source universe has {PINNED_CANDIDATE_COUNT}"
        )
    observed_order = [
        row.get("candidate_key") if isinstance(row, dict) else None
        for row in rows
    ]
    expected_order = [row["candidate_key"] for row in expected_dispositions]
    if observed_order != expected_order:
        checker.fail(
            f"release {release} coverage candidate order/universe differs from "
            "the independently rebuilt source universe"
        )
    accepted: list[str] = []
    already_allocated: list[str] = []
    candidate_keys: list[str] = []
    reserve_by_key: dict[str, Mapping[str, Any]] = {}
    candidate_by_key: dict[str, Mapping[str, Any]] = {}
    for index, value in enumerate(rows):
        label = f"release {release} coverage candidate[{index}]"
        try:
            row = require_dict(value, label)
            if set(row) != candidate_required:
                raise CheckFailure(
                    f"{label} fields are not exact: "
                    f"missing={sorted(candidate_required-set(row))!r}, "
                    f"extra={sorted(set(row)-candidate_required)!r}"
                )
            key = require_string(row.get("candidate_key"), f"{label}.candidate_key")
            candidate_keys.append(key)
            candidate_by_key[key] = row
            expected_row = expected_by_key.get(key)
            if expected_row is None:
                raise CheckFailure(
                    f"{label} is a forged or unknown non-source candidate {key!r}"
                )
            for field in candidate_required:
                if row.get(field) != expected_row.get(field):
                    raise CheckFailure(
                        f"{label}.{field} differs from independently rebuilt "
                        "candidate/disposition truth"
                    )
            source_id = require_string(row.get("source_id"), f"{label}.source_id")
            if source_id not in sources:
                raise CheckFailure(f"{label} cites unknown source {source_id}")
            qualified_name = require_string(
                row.get("qualified_name"), f"{label}.qualified_name"
            )
            source_hash = require_sha256(
                row.get("source_statement_sha256"),
                f"{label}.source_statement_sha256",
            )
            normalized_hash = require_sha256(
                row.get("normalized_statement_sha256"),
                f"{label}.normalized_statement_sha256",
            )
            require_sha256(
                row.get("evidence_locator_sha256"),
                f"{label}.evidence_locator_sha256",
            )
            require_string(row.get("reason_code"), f"{label}.reason_code")
            disposition = row.get("disposition")
            if disposition not in dispositions:
                raise CheckFailure(f"{label} has unknown disposition {disposition!r}")
            grants = row.get("grants_quota")
            if grants is not (disposition == "accepted_new_claim"):
                raise CheckFailure(f"{label} grants_quota disagrees with disposition")
            target = row.get("target_variant_id")
            target_s5 = row.get("target_s5_id")
            duplicate_of = row.get("duplicate_of_variant_id")
            if disposition == "duplicate_noncredit":
                if target is not None or target_s5 is not None:
                    raise CheckFailure(f"{label} duplicate allocates target IDs")
                if not isinstance(duplicate_of, str) or ATV_RE.fullmatch(duplicate_of) is None:
                    raise CheckFailure(f"{label} duplicate lacks duplicate_of_variant_id")
            elif duplicate_of is not None:
                raise CheckFailure(f"{label} nonduplicate carries duplicate_of_variant_id")

            target_row: Mapping[str, Any] | None = None
            if disposition in {"accepted_new_claim", "already_allocated_noncredit"}:
                if not isinstance(target, str) or ATV_RE.fullmatch(target) is None:
                    raise CheckFailure(f"{label} lacks a valid target ATV")
                if not isinstance(target_s5, str) or S5_RE.fullmatch(target_s5) is None:
                    raise CheckFailure(f"{label} lacks a valid target S5 ID")
                if ordinal(target, ATV_RE) != ordinal(target_s5, S5_RE):
                    raise CheckFailure(f"{label} target ATV/S5 ordinal mismatch")
                target_row = catalog_by_atv.get(target)
                if target_row is None or record_stage_id(target_row) != target_s5:
                    raise CheckFailure(f"{label} target is absent from the catalog mapping")
                expected_origin = release if disposition == "accepted_new_claim" else "5.0"
                if origin_release(target_row) != expected_origin:
                    raise CheckFailure(f"{label} target has wrong origin release")
                if row.get("origin_release") != expected_origin:
                    raise CheckFailure(f"{label} candidate origin release drifted")
                if disposition == "already_allocated_noncredit":
                    if release != "5.1":
                        raise CheckFailure(f"{label} carry disposition is only legal in 5.1")
                    already_allocated.append(target)
                else:
                    accepted.append(target)
            elif target is not None or target_s5 is not None:
                raise CheckFailure(f"{label} nonallocation disposition carries target IDs")

            if disposition == "open_reserve_noncredit":
                if row.get("origin_release") not in RELEASES:
                    raise CheckFailure(f"{label} reserve lacks a release assignment")
                reserve_by_key[key] = row

            if target_row is not None:
                target_dedupe = require_dict(target_row.get("dedupe"), f"{label} target.dedupe")
                if row.get("source_id") != record_source_id(target_row):
                    raise CheckFailure(f"{label} source_id drifts from catalog target")
                if qualified_name != record_qualified_name(target_row):
                    raise CheckFailure(f"{label} qualified name drifts from catalog target")
                if source_hash != target_dedupe.get("source_statement_sha256"):
                    raise CheckFailure(f"{label} source-statement hash drifts from target")
                if normalized_hash != target_dedupe.get("normalized_statement_sha256"):
                    raise CheckFailure(f"{label} normalized-statement hash drifts from target")
                expected_locator_hash = sha256_bytes(
                    canonical_json_bytes(record_locator(target_row))
                )
                if row.get("evidence_locator_sha256") != expected_locator_hash:
                    raise CheckFailure(f"{label} evidence-locator hash drifts from target")
                if re.search(r"\btype_of%", str(record_declaration(target_row))):
                    raise CheckFailure(f"{label} type_of% pointer grants or retains allocation")
        except CheckFailure as error:
            checker.fail(str(error))

    exact_unique_strings(
        checker, candidate_keys, f"release {release} coverage candidate keys"
    )
    accepted_set = exact_unique_strings(
        checker, accepted, f"release {release} accepted coverage targets", ATV_RE
    )
    expected = {
        atv for atv, row in catalog_by_atv.items() if origin_release(row) == release
    }
    if accepted_set != expected:
        checker.fail(f"release {release} coverage ledger accepted set differs from origin catalog set")
    already_set = exact_unique_strings(
        checker,
        already_allocated,
        f"release {release} already-allocated coverage targets",
        ATV_RE,
    )
    expected_already = (
        {atv for atv, row in catalog_by_atv.items() if origin_release(row) == "5.0"}
        if release == "5.1"
        else set()
    )
    if already_set != expected_already:
        checker.fail(
            f"release {release} already-allocated set differs from carried 5.0 catalog"
        )

    msc_policy = require_dict(
        contract.get("msc_coverage_policy"), "contract.msc_coverage_policy"
    )
    top_classes = require_list(
        msc_policy.get("top_level_classes"), "contract MSC top_level_classes"
    )
    scarcity_enum = set(
        require_list(msc_policy.get("scarcity_enum"), "contract MSC scarcity_enum")
    )
    msc_required = set(
        require_list(
            coverage_contract.get("msc_coverage_required_fields"),
            "coverage contract msc_coverage_required_fields",
        )
    )
    msc_rows = require_list(
        ledger.get("msc_coverage"), f"release {release} coverage msc_coverage"
    )
    observed_top = [
        row.get("msc_top_class") if isinstance(row, dict) else None for row in msc_rows
    ]
    if observed_top != top_classes:
        checker.fail(f"release {release} MSC rows are not the exact ordered 63-class set")

    stage_to_row = {
        str(record_stage_id(row)): row
        for row in catalog_by_atv.values()
        if isinstance(record_stage_id(row), str)
    }
    all_reserve_keys: list[str] = []
    id_fields = (
        "current_theorem_s5_ids",
        "current_open_s5_ids",
        "origin_theorem_s5_ids",
        "origin_open_s5_ids",
    )
    count_fields = {
        "current_theorems": "current_theorem_s5_ids",
        "current_open": "current_open_s5_ids",
        "origin_theorems": "origin_theorem_s5_ids",
        "origin_open": "origin_open_s5_ids",
        "open_reserve": "open_reserve_candidate_keys",
    }
    for index, value in enumerate(msc_rows):
        label = f"release {release} MSC row[{index}]"
        try:
            row = require_dict(value, label)
            if set(row) != msc_required:
                raise CheckFailure(f"{label} fields are not exact")
            top = require_string(row.get("msc_top_class"), f"{label}.msc_top_class")
            arrays: dict[str, list[str]] = {}
            for field in (*id_fields, "open_reserve_candidate_keys", "source_ids"):
                values = require_list(row.get(field), f"{label}.{field}")
                if not all(isinstance(item, str) and item for item in values):
                    raise CheckFailure(f"{label}.{field} contains a malformed value")
                if values != sorted(set(values)):
                    raise CheckFailure(f"{label}.{field} is not sorted and unique")
                arrays[field] = list(values)
            for field in id_fields:
                if any(S5_RE.fullmatch(item) is None for item in arrays[field]):
                    raise CheckFailure(f"{label}.{field} contains a malformed S5 ID")
            expected_current_theorem = sorted(
                stage
                for stage, catalog_row in stage_to_row.items()
                if catalog_row.get("primary_ams_class") == top
                and is_quota_theorem(catalog_row)
            )
            expected_current_open = sorted(
                stage
                for stage, catalog_row in stage_to_row.items()
                if catalog_row.get("primary_ams_class") == top
                and is_quota_open_claim(catalog_row)
            )
            expected_origin_theorem = sorted(
                stage
                for stage in expected_current_theorem
                if origin_release(stage_to_row[stage]) == release
            )
            expected_origin_open = sorted(
                stage
                for stage in expected_current_open
                if origin_release(stage_to_row[stage]) == release
            )
            expected_arrays = {
                "current_theorem_s5_ids": expected_current_theorem,
                "current_open_s5_ids": expected_current_open,
                "origin_theorem_s5_ids": expected_origin_theorem,
                "origin_open_s5_ids": expected_origin_open,
            }
            for field, expected_values in expected_arrays.items():
                if arrays[field] != expected_values:
                    raise CheckFailure(f"{label}.{field} is not the recomputed catalog query")
            for key in arrays["open_reserve_candidate_keys"]:
                if key not in reserve_by_key:
                    raise CheckFailure(f"{label} lists non-reserve candidate {key}")
            expected_class_reserve = sorted(
                key
                for key in reserve_by_key
                if key in source_candidates_by_key
                and source_candidates_by_key[key].get("ams", [None])[0] == top
            )
            if arrays["open_reserve_candidate_keys"] != expected_class_reserve:
                raise CheckFailure(
                    f"{label}.open_reserve_candidate_keys differs from "
                    "independently parsed primary AMS classes"
                )
            all_reserve_keys.extend(arrays["open_reserve_candidate_keys"])

            contributor_sources = {
                str(record_source_id(stage_to_row[stage]))
                for field in ("current_theorem_s5_ids", "current_open_s5_ids")
                for stage in arrays[field]
            }
            contributor_sources.update(
                str(reserve_by_key[key].get("source_id"))
                for key in arrays["open_reserve_candidate_keys"]
            )
            if arrays["source_ids"] != sorted(contributor_sources):
                raise CheckFailure(f"{label}.source_ids is not contributor-derived")

            counts = require_dict(row.get("counts"), f"{label}.counts")
            if set(counts) != set(count_fields):
                raise CheckFailure(f"{label}.counts fields are not exact")
            for count_field, array_field in count_fields.items():
                if counts.get(count_field) != len(arrays[array_field]):
                    raise CheckFailure(f"{label}.counts.{count_field} is stale")
            basis = require_dict(
                row.get("classification_basis_counts"),
                f"{label}.classification_basis_counts",
            )
            basis_fields = {"source_annotation", "machine_crosswalk", "independent_review"}
            if set(basis) != basis_fields or any(
                not isinstance(item, int) or isinstance(item, bool) or item < 0
                for item in basis.values()
            ):
                raise CheckFailure(f"{label}.classification_basis_counts is malformed")
            population = (
                len(arrays["current_theorem_s5_ids"])
                + len(arrays["current_open_s5_ids"])
                + len(arrays["open_reserve_candidate_keys"])
            )
            expected_basis = {
                "source_annotation": population,
                "machine_crosswalk": 0,
                "independent_review": 0,
            }
            if basis != expected_basis:
                raise CheckFailure(
                    f"{label} classification basis is not source-annotation derived"
                )
            scarcity = row.get("scarcity")
            if scarcity not in scarcity_enum:
                raise CheckFailure(f"{label} scarcity value is not contractual")
            expected_scarcity: str
            expected_reason: str
            if population == 0:
                expected_scarcity = "zero"
                expected_reason = (
                    "No current or open-reserve member has this primary source annotation."
                )
            elif population < 10:
                expected_scarcity = "thin"
                expected_reason = (
                    "Fewer than ten current-plus-reserve members have this primary class."
                )
            else:
                expected_scarcity = "adequate_in_source_inventory"
                expected_reason = (
                    "At least ten current-plus-reserve members have this primary class."
                )
            if (
                scarcity != expected_scarcity
                or row.get("scarcity_reason") != expected_reason
            ):
                raise CheckFailure(
                    f"{label} scarcity/reason is not recomputed from source members"
                )
        except CheckFailure as error:
            checker.fail(str(error))

    observed_reserve = exact_unique_strings(
        checker,
        all_reserve_keys,
        f"release {release} MSC reserve candidate keys",
    )
    if observed_reserve != set(reserve_by_key):
        checker.fail(f"release {release} MSC rows do not partition the open reserve")

    counts = require_dict(ledger.get("counts"), f"release {release} coverage counts")
    expected_counts = {
        "candidate_dispositions": len(rows),
        "msc_coverage": len(msc_rows),
        "accepted_new_claims": len(accepted_set),
        "open_reserve_noncredit": len(reserve_by_key),
    }
    if counts != expected_counts:
        checker.fail(f"release {release} coverage top-level counts are stale")


def check_release_data(
    checker: Checker,
    release: str,
    documents: Mapping[str, Mapping[str, Any]],
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    parent_v4_ids: set[str],
    candidates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    extraction_bound_artifacts = {
        "Claim_Catalog.json",
        "Claim_ID_Registry.json",
        "Stage5_Claim_ID_Registry.json",
        "Theorem_List.json",
        "Open_Claim_List.json",
    }
    for name in RELEASE_FILES:
        if name not in documents:
            raise CheckFailure(f"release {release} decoded documents omit {name}")
        check_sealed_document(checker, f"release {release}/{name}", documents[name])
        inputs = documents[name].get("authoritative_inputs")
        if name in extraction_bound_artifacts and (
            not isinstance(inputs, dict)
            or inputs.get("extractor_records_jsonl_sha256")
            != PINNED_EXTRACTION_JSONL_SHA256
        ):
            checker.fail(
                f"release {release}/{name} is not bound to the independently "
                "recomputed extraction digest"
            )
    records = artifact_rows(documents["Claim_Catalog.json"])
    validate_record_schema(checker, schema, records)
    by_atv: dict[str, dict[str, Any]] = {}
    for row in records:
        atv = record_variant_id(row)
        if not isinstance(atv, str) or ATV_RE.fullmatch(atv) is None:
            checker.fail(f"release {release} catalog has malformed ATV ID {atv!r}")
            continue
        if atv in by_atv:
            checker.fail(f"release {release} catalog duplicates {atv}")
        by_atv[atv] = row
    if set(by_atv) & parent_v4_ids:
        checker.fail(f"release {release} catalog republishes inherited v4 rows")
    expected_allocations = expected_formal_allocations(candidates)
    expected_catalog_ids = {
        str(identity["variant_id"])
        for identity in expected_allocations.values()
        if identity["origin_release"] == "5.0" or release == "5.1"
    }
    if set(by_atv) != expected_catalog_ids:
        checker.fail(
            f"release {release} catalog allocation set differs from the "
            "independent source selection"
        )
    check_catalog_allocation_suffixes(checker, release, records)
    check_record_content(
        checker, release, records, contract, sources, candidates
    )
    check_quota_duplicates(checker, release, records)
    registry_ids, stage_by_atv = check_numbering_and_migration(
        checker, release, documents, set(by_atv), parent_v4_ids
    )
    theorem_ids, open_ids = check_projections(
        checker, release, documents, by_atv, stage_by_atv
    )
    check_coverage_ledger(
        checker,
        release,
        documents["Coverage_Ledger.json"],
        by_atv,
        contract,
        sources,
        candidates,
    )

    origin_theorems, origin_open = check_declared_catalog_counts(
        checker, release, documents["Claim_Catalog.json"], records
    )
    if len(origin_theorems) < MINIMUMS[release]["theorem"]:
        checker.fail(
            f"release {release} has only {len(origin_theorems)} origin theorems; "
            f"minimum is {MINIMUMS[release]['theorem']}"
        )
    if len(origin_open) < MINIMUMS[release]["open"]:
        checker.fail(
            f"release {release} has only {len(origin_open)} origin open claims; "
            f"minimum is {MINIMUMS[release]['open']}"
        )
    return {
        "records": records,
        "by_atv": by_atv,
        "registry_ids": registry_ids,
        "stage_by_atv": stage_by_atv,
        "theorem_ids": theorem_ids,
        "open_ids": open_ids,
        "origin_theorems": origin_theorems,
        "origin_open": origin_open,
    }


def expected_suffix(values: Iterable[str], start: int) -> list[int]:
    observed = sorted(ordinal(value, ATV_RE) for value in values if ordinal(value, ATV_RE) >= start)
    if not observed:
        return []
    expected = list(range(start, observed[-1] + 1))
    if observed != expected:
        raise CheckFailure(
            f"append-only ATV suffix is not contiguous from {start}: "
            f"observed head={observed[:8]!r}"
        )
    return observed


def check_parent_chain(
    checker: Checker,
    contract: Mapping[str, Any],
    manifests: Mapping[str, Mapping[str, Any]],
    roots: Mapping[str, str],
) -> None:
    first = manifests["5.0"]
    if first.get("parent_release") is not None:
        checker.fail("release 5.0 unexpectedly declares a parent release")
    if first.get("parent_release_root_sha256") is not None:
        checker.fail("release 5.0 unexpectedly declares a parent release root")
    child = manifests["5.1"]
    parent_release = child.get("parent_release")
    parent_root = child.get("parent_release_root_sha256")
    if parent_release != "5.0":
        checker.fail("release 5.1 parent release is not 5.0")
    if parent_root != roots["5.0"]:
        checker.fail("release 5.1 parent release-root digest does not match 5.0 bytes")
    lock = contract.get("release_5_0_lock", contract.get("s5_0_lock"))
    if isinstance(lock, dict):
        if lock.get("release_root_sha256") != roots["5.0"]:
            checker.fail("contract's immutable 5.0 release-root lock drifted")
        actual_manifest_sha = sha256_file(
            checker.path(release_dir("5.0") / MANIFEST_NAME)
        )
        if "manifest_sha256" in lock and lock.get("manifest_sha256") != actual_manifest_sha:
            checker.fail("contract's immutable 5.0 manifest lock drifted")


def run(checker: Checker) -> None:
    contract = checker.load_json(CONTRACT_PATH)
    schema = checker.load_json(SCHEMA_PATH)
    source_registry = checker.load_json(SOURCE_REGISTRY_PATH)
    v4_receipt = checker.load_json(V4_IMPORT_RECEIPT_PATH)
    v4_registry = checker.load_json(V4_REGISTRY_PATH)
    check_contract(checker, contract)
    sources = check_source_registry(checker, source_registry)
    candidates = rebuild_formal_candidates(checker, sources)
    parent_v4_ids = exact_unique_strings(
        checker,
        (row.get("variant_id") for row in require_list(v4_registry.get("variants"), "v4 variants")),
        "v4 parent variant IDs",
        ATV_RE,
    )
    if parent_v4_ids != {f"ATV-{value:08d}" for value in range(1, 3485)}:
        checker.fail("Stage5 parent variant universe is not the exact 1..3484 set")
    check_v4_import_receipt(checker, v4_receipt, parent_v4_ids)

    documents: dict[str, dict[str, dict[str, Any]]] = {}
    roots: dict[str, str] = {}
    results: dict[str, dict[str, Any]] = {}
    for release in RELEASES:
        documents[release] = load_release_documents(checker, release)
        roots[release] = check_manifest(
            checker, release, documents[release][MANIFEST_NAME], documents[release]
        )
        results[release] = check_release_data(
            checker,
            release,
            documents[release],
            contract,
            schema,
            sources,
            parent_v4_ids,
            candidates,
        )

    try:
        suffix_50 = expected_suffix(results["5.0"]["registry_ids"] - parent_v4_ids, FIRST_STAGE5_ORDINAL)
        suffix_51 = expected_suffix(results["5.1"]["registry_ids"] - parent_v4_ids, FIRST_STAGE5_ORDINAL)
        if not suffix_50:
            checker.fail("release 5.0 allocated no ATV IDs after 3484")
        if not set(results["5.0"]["registry_ids"]) <= set(results["5.1"]["registry_ids"]):
            checker.fail("release 5.1 drops one or more 5.0 ATV allocations")
        if suffix_50 and suffix_51 and suffix_51[: len(suffix_50)] != suffix_50:
            checker.fail("release 5.1 does not preserve the exact 5.0 ATV suffix")
    except CheckFailure as error:
        checker.fail(str(error))
    rows_50 = {
        atv: canonical_json_bytes(row)
        for atv, row in results["5.0"]["by_atv"].items()
    }
    rows_51 = {
        atv: canonical_json_bytes(row)
        for atv, row in results["5.1"]["by_atv"].items()
    }
    if not set(rows_50) <= set(rows_51):
        checker.fail("release 5.1 cumulative catalog drops one or more 5.0 additions")
    changed = sorted(atv for atv in set(rows_50) & set(rows_51) if rows_50[atv] != rows_51[atv])
    if changed:
        checker.fail(f"release 5.1 mutates carried 5.0 catalog rows: {changed[:8]!r}")
    check_parent_chain(
        checker,
        contract,
        {release: documents[release][MANIFEST_NAME] for release in RELEASES},
        roots,
    )
    checker.note(
        f"pinned formal candidates={len(candidates)}; extraction digest="
        f"{PINNED_EXTRACTION_JSONL_SHA256}; S5.0 origin theorem/open="
        f"{len(results['5.0']['origin_theorems'])}/{len(results['5.0']['origin_open'])}; "
        f"S5.1 new theorem={len(results['5.1']['origin_theorems'])}; "
        f"final variants={len(results['5.1']['registry_ids'])}"
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: inferred from this script)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    checker = Checker(args.root)
    try:
        run(checker)
    except (CheckFailure, OSError, TypeError, ValueError) as error:
        checker.fail(f"unhandled verification input error: {error}")
    if checker.errors:
        print(f"FAIL check_math_catalog_v5 ({len(checker.errors)} errors)")
        for error in checker.errors:
            print(f"- {error}")
        for note in checker.notes:
            print(f"NOTE {note}")
        return 1
    print("PASS check_math_catalog_v5")
    for note in checker.notes:
        print(f"NOTE {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
