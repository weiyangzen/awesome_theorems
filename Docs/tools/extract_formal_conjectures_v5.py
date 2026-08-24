#!/usr/bin/env python3
"""Extract typed Lean declarations from a pinned formal-conjectures snapshot.

The extractor is deliberately independent of Lean and of the upstream project.
It uses only Python's standard library, accepts either a source checkout/archive
directory or a tar archive, and emits deterministic canonical JSONL (or a JSON
envelope).  It extracts only ``theorem`` and ``lemma`` declarations carrying one
of these upstream categories:

* ``research open``
* ``research solved``
* ``textbook``

An extracted declaration must have a non-empty immediately preceding Lean
docstring, at least one valid top-level MSC2020 ``AMS`` code, and a complete
signature ending at the declaration's proof/body separator.  Proof bodies are
never included.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import re
import sys
import tarfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


PINNED_COMMIT = "2270d31e8dd611521f979de6d86da364930b7669"
SOURCE_REPOSITORY = "https://github.com/google-deepmind/formal-conjectures"
SCHEMA_VERSION = "awesome-theorems/formal-conjectures-source-block/5.0"
SUMMARY_SCHEMA_VERSION = "awesome-theorems/formal-conjectures-extraction-summary/5.0"

SELECTED_CATEGORIES = {"research open", "research solved", "textbook"}
MSC2020_TOP_LEVEL = {
    "00", "01", "03", "05", "06", "08", "11", "12", "13", "14",
    "15", "16", "17", "18", "19", "20", "22", "26", "28", "30",
    "31", "32", "33", "34", "35", "37", "39", "40", "41", "42",
    "43", "44", "45", "46", "47", "49", "51", "52", "53", "54",
    "55", "57", "58", "60", "62", "65", "68", "70", "74", "76",
    "78", "80", "81", "82", "83", "85", "86", "90", "91", "92",
    "93", "94", "97",
}

DECLARATION_RE = re.compile(r"\b(theorem|lemma)\b")
SCOPE_RE = re.compile(
    r"(?m)^[ \t]*(?:(noncomputable)[ \t]+)?(namespace|section|end)\b([^\n]*)"
)
IMPORT_RE = re.compile(r"(?m)^[ \t]*import[ \t]+([^\s]+)")
MODIFIER_RE = re.compile(r"(?:(?:private|protected|noncomputable|unsafe)\s*)*\Z")
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_']*")


class ExtractionError(RuntimeError):
    """A fail-closed source, syntax, metadata, or uniqueness error."""


@dataclass(frozen=True)
class SourceFile:
    relative_path: str
    data: bytes
    archive_member: str | None


@dataclass(frozen=True)
class Snapshot:
    commit: str
    source_files: tuple[SourceFile, ...]
    license_bytes: bytes
    readme_bytes: bytes


@dataclass(frozen=True)
class CommentRange:
    start: int
    end: int
    is_doc: bool


@dataclass(frozen=True)
class AttributeRange:
    start: int
    end: int


@dataclass(frozen=True)
class ScopeEvent:
    start: int
    action: str
    name: str | None


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def canonical_jsonl(records: Iterable[Mapping[str, Any]]) -> str:
    rows = [canonical_json(record) for record in records]
    return "".join(row + "\n" for row in rows)


def _safe_member_path(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ExtractionError(f"unsafe tar member path: {name!r}")
    return path


def _tar_snapshot(path: Path, expected_commit: str | None) -> Snapshot:
    try:
        archive_bytes = path.read_bytes()
        archive = tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:*")
    except (OSError, tarfile.TarError) as exc:
        raise ExtractionError(f"cannot read tar archive {path}: {exc}") from exc

    regular: dict[str, bytes] = {}
    prefixes: set[str] = set()
    try:
        for member in archive.getmembers():
            member_path = _safe_member_path(member.name)
            if member.issym() or member.islnk():
                raise ExtractionError(
                    f"tar archive contains unsupported link: {member.name!r}"
                )
            if not member.isfile():
                continue
            parts = member_path.parts
            if "FormalConjectures" in parts:
                index = parts.index("FormalConjectures")
                if index != 1:
                    raise ExtractionError(
                        f"unexpected archive root for {member.name!r}"
                    )
                prefixes.add(parts[0])
            stream = archive.extractfile(member)
            if stream is None:
                raise ExtractionError(f"cannot read tar member {member.name!r}")
            if member.name in regular:
                raise ExtractionError(f"duplicate tar member: {member.name!r}")
            regular[member.name] = stream.read()
    finally:
        archive.close()

    if len(prefixes) != 1:
        raise ExtractionError(
            f"archive must contain exactly one FormalConjectures root, got {sorted(prefixes)!r}"
        )
    prefix = next(iter(prefixes))
    if expected_commit is not None and not prefix.endswith(expected_commit):
        raise ExtractionError(
            f"archive root {prefix!r} does not identify pinned commit {expected_commit}"
        )
    commit = expected_commit or _commit_from_archive_prefix(prefix)
    source_prefix = prefix + "/FormalConjectures/"
    files = tuple(
        SourceFile(name[len(prefix) + 1 :], data, name)
        for name, data in sorted(regular.items())
        if name.startswith(source_prefix) and name.endswith(".lean")
    )
    if not files:
        raise ExtractionError("archive contains no FormalConjectures/*.lean source files")
    try:
        license_bytes = regular[prefix + "/LICENSE"]
        readme_bytes = regular[prefix + "/README.md"]
    except KeyError as exc:
        raise ExtractionError(f"archive is missing required repository file: {exc}") from exc
    _validate_license(license_bytes, readme_bytes)
    return Snapshot(commit, files, license_bytes, readme_bytes)


def _commit_from_archive_prefix(prefix: str) -> str:
    match = re.search(r"([0-9a-f]{40})$", prefix)
    if match is None:
        raise ExtractionError(
            "archive root does not end in a 40-character source commit"
        )
    return match.group(1)


def _git_dir(root: Path) -> Path | None:
    marker = root / ".git"
    if marker.is_dir():
        return marker
    if marker.is_file():
        try:
            text = marker.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise ExtractionError(f"cannot read {marker}: {exc}") from exc
        if text.startswith("gitdir:"):
            target = Path(text.split(":", 1)[1].strip())
            return (root / target).resolve() if not target.is_absolute() else target
    return None


def _git_head(root: Path) -> str | None:
    git_dir = _git_dir(root)
    if git_dir is None:
        return None
    try:
        head = (git_dir / "HEAD").read_text(encoding="ascii").strip()
    except OSError as exc:
        raise ExtractionError(f"cannot read Git HEAD in {root}: {exc}") from exc
    if re.fullmatch(r"[0-9a-f]{40}", head):
        return head
    if not head.startswith("ref: "):
        raise ExtractionError(f"malformed Git HEAD in {root}: {head!r}")
    ref = head[5:]
    loose = git_dir / ref
    if loose.is_file():
        value = loose.read_text(encoding="ascii").strip()
        if re.fullmatch(r"[0-9a-f]{40}", value):
            return value
    packed = git_dir / "packed-refs"
    if packed.is_file():
        for line in packed.read_text(encoding="ascii").splitlines():
            if line.startswith("#") or line.startswith("^"):
                continue
            fields = line.split(" ", 1)
            if len(fields) == 2 and fields[1] == ref:
                if re.fullmatch(r"[0-9a-f]{40}", fields[0]):
                    return fields[0]
    raise ExtractionError(f"cannot resolve Git HEAD reference {ref!r} in {root}")


def _directory_snapshot(path: Path, expected_commit: str | None) -> Snapshot:
    source = path.resolve()
    if (source / "FormalConjectures").is_dir():
        root = source
    elif source.name == "FormalConjectures" and source.is_dir():
        root = source.parent
    else:
        raise ExtractionError(
            f"source directory {path} does not contain FormalConjectures/"
        )

    observed_commit = _git_head(root)
    if observed_commit is None:
        suffix = re.search(r"([0-9a-f]{40})$", root.name)
        observed_commit = suffix.group(1) if suffix is not None else None
    if expected_commit is not None and observed_commit != expected_commit:
        raise ExtractionError(
            f"source directory identifies commit {observed_commit!r}, expected {expected_commit}"
        )
    commit = expected_commit or observed_commit
    if commit is None:
        raise ExtractionError("source directory has no verifiable 40-character commit")

    files: list[SourceFile] = []
    for file_path in sorted((root / "FormalConjectures").rglob("*.lean")):
        if file_path.is_symlink() or not file_path.is_file():
            raise ExtractionError(f"unsupported source path: {file_path}")
        relative = file_path.relative_to(root).as_posix()
        files.append(SourceFile(relative, file_path.read_bytes(), None))
    if not files:
        raise ExtractionError("source directory contains no FormalConjectures/*.lean files")
    try:
        license_bytes = (root / "LICENSE").read_bytes()
        readme_bytes = (root / "README.md").read_bytes()
    except OSError as exc:
        raise ExtractionError(f"source directory lacks LICENSE/README.md: {exc}") from exc
    _validate_license(license_bytes, readme_bytes)
    return Snapshot(commit, tuple(files), license_bytes, readme_bytes)


def load_snapshot(path: Path, expected_commit: str | None = PINNED_COMMIT) -> Snapshot:
    if path.is_dir():
        return _directory_snapshot(path, expected_commit)
    if not path.is_file():
        raise ExtractionError(f"source does not exist: {path}")
    return _tar_snapshot(path, expected_commit)


def _validate_license(license_bytes: bytes, readme_bytes: bytes) -> None:
    try:
        license_text = license_bytes.decode("utf-8")
        readme_text = readme_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ExtractionError(f"LICENSE/README.md is not strict UTF-8: {exc}") from exc
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        raise ExtractionError("repository LICENSE is not identifiable as Apache-2.0")
    if "Creative Commons Attribution 4.0" not in readme_text:
        raise ExtractionError("README.md lacks the repository materials license statement")


def mask_comments_and_strings(
    text: str, *, mask_strings: bool = True
) -> tuple[str, list[CommentRange]]:
    """Return a same-length syntax mask and all block-comment ranges.

    Comment and string contents become spaces while newlines are preserved.
    Lean block comments nest; unterminated comments/strings fail closed.
    """

    chars = list(text)
    comments: list[CommentRange] = []
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
            is_doc = text.startswith("/--", index) and not text.startswith("/---", index)
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
                raise ExtractionError(
                    f"unterminated block comment at character offset {start}"
                )
            comments.append(CommentRange(start, index, is_doc))
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
                raise ExtractionError(
                    f"unterminated string literal at character offset {start}"
                )
            if mask_strings:
                blank(start, index)
            continue
        index += 1
    return "".join(chars), comments


def find_attribute_ranges(mask: str) -> list[AttributeRange]:
    ranges: list[AttributeRange] = []
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
            raise ExtractionError(
                f"unterminated attribute block at character offset {start}"
            )
        ranges.append(AttributeRange(start, cursor))
        index = cursor


def _associated_attributes(
    mask: str, declaration_start: int, ranges: Sequence[AttributeRange]
) -> tuple[list[AttributeRange], int]:
    preceding = [item for item in ranges if item.end <= declaration_start]
    if not preceding:
        return [], declaration_start
    chosen: list[AttributeRange] = []
    cursor = declaration_start
    for item in reversed(preceding):
        gap = mask[item.end:cursor]
        if not chosen:
            if MODIFIER_RE.fullmatch(gap.strip()) is None:
                break
        elif gap.strip():
            break
        chosen.append(item)
        cursor = item.start
    chosen.reverse()
    return chosen, cursor


def _categories(attribute_texts: Sequence[str]) -> list[str]:
    found: list[str] = []
    pattern = re.compile(r"\bcategory\s+(research\s+(?:open|solved)|textbook)\b")
    for text in attribute_texts:
        found.extend(match.group(1) for match in pattern.finditer(text))
    return found


def _ams_codes(attribute_texts: Sequence[str]) -> list[str]:
    codes: list[str] = []
    for text in attribute_texts:
        for match in re.finditer(r"\bAMS\b", text):
            suffix = text[match.end():]
            values = re.match(r"(?:\s+[0-9]{1,2})+", suffix)
            if values is None:
                continue
            codes.extend(f"{int(value):02d}" for value in re.findall(r"[0-9]+", values.group(0)))
    return codes


def _lean_string_value(token: str) -> str:
    """Decode the ordinary quoted strings accepted by the attribute syntax."""

    try:
        value = ast.literal_eval(token)
    except (SyntaxError, ValueError) as exc:
        raise ExtractionError(f"malformed formal_proof link string: {token!r}") from exc
    if not isinstance(value, str):
        raise ExtractionError(f"formal_proof link is not a string: {token!r}")
    return value


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
            conditional = match.group(1) is not None
            raw_conditions = match.group(4)
            conditions = raw_conditions.split() if raw_conditions else []
            if conditional and not conditions:
                raise ExtractionError(
                    "conditional formal_proof attribute has no assumed declarations"
                )
            if not conditional and conditions:
                raise ExtractionError(
                    "formal_proof assuming clause lacks the conditional modifier"
                )
            result.append(
                {
                    "kind": match.group(2),
                    "link": _lean_string_value(match.group(3)),
                    "conditional": conditional,
                    "proof_conditions": [
                        _qualified_name(namespaces, condition) for condition in conditions
                    ],
                }
            )
    return result


def _answer_kinds(result_mask: str) -> list[str]:
    """Infer source-level answer kinds for comparison with Lean elaboration.

    ``answer`` arguments next to proposition connectives, literal ``True`` or
    ``False``, or occupying the whole result are classified as ``Prop``.  Other
    occurrences are classified as ``non-Prop``.  The record states this static
    policy explicitly; the upstream elaborator remains authoritative.
    """

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
            raise ExtractionError("unbalanced answer(...) expression in declaration result")
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


def _parse_name(mask: str, start: int) -> tuple[str, int]:
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
        raise ExtractionError(f"malformed declaration name near offset {start}")
    return name, cursor


def _line_indentation(mask: str, offset: int) -> int:
    """Return the visual indentation of the line containing ``offset``."""

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


def _after_layout_block(
    mask: str, start: int, boundary: int, parent_indentation: int
) -> int:
    """Find the next token after a ``by`` block owned by a local ``let``.

    Comments and strings are spaces in ``mask``, so a nonblank line indented no
    farther than the owning ``let`` is the first token outside the tactic RHS.
    """

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
        if token_start < line_end:
            indentation = _line_indentation(mask, token_start)
            if indentation <= parent_indentation:
                return token_start
        line_start = line_end + 1
    return boundary


def _signature_end(mask: str, start: int, boundary: int) -> tuple[int, int]:
    """Return ``(separator_start, first_top_level_colon)``.

    A top-level ``:=`` belonging to a top-level ``let`` in the proposition is
    skipped.  The next top-level assignment is the declaration body separator.
    """

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
        if char in ")]}":
            if not stack or stack[-1] != matching[char]:
                raise ExtractionError(
                    f"unbalanced delimiter near character offset {index}"
                )
            stack.pop()
            index += 1
            continue
        if not stack:
            word = WORD_RE.match(mask, index)
            if word is not None:
                # Lean's term-level local bindings are ``let`` and ``letI``.
                # The assignment that introduces either binding belongs to
                # the result type; it is not the declaration proof separator.
                if word.group(0) in {"let", "letI"} and colon >= 0:
                    pending_lets.append(_line_indentation(mask, word.start()))
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
                    rhs_word = WORD_RE.match(mask, rhs_start)
                    if rhs_word is not None and rhs_word.group(0) == "by":
                        index = _after_layout_block(
                            mask, rhs_word.end(), boundary, let_indentation
                        )
                    continue
                return index, colon
        index += 1
    raise ExtractionError("declaration has no complete top-level body separator")


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _normalized_statement_payload(text: str, name_end: int, separator: int) -> str:
    comment_mask, _comments = mask_comments_and_strings(
        text[name_end:separator], mask_strings=False
    )
    return " ".join(comment_mask.split())


def _scope_events(mask: str) -> list[ScopeEvent]:
    result: list[ScopeEvent] = []
    for match in SCOPE_RE.finditer(mask):
        action = match.group(2)
        tail = match.group(3).strip()
        if action == "namespace":
            name = tail.split()[0] if tail else None
            if name is None:
                raise ExtractionError(
                    f"namespace command has no name at character offset {match.start()}"
                )
            result.append(ScopeEvent(match.start(), action, name))
        elif action == "section":
            name = tail.split()[0] if tail else None
            result.append(ScopeEvent(match.start(), action, name))
        else:
            result.append(ScopeEvent(match.start(), action, None))
    return result


def _namespaces_at(
    declarations: Sequence[re.Match[str]], events: Sequence[ScopeEvent]
) -> dict[int, tuple[str, ...]]:
    output: dict[int, tuple[str, ...]] = {}
    stack: list[tuple[str, str | None]] = []
    event_index = 0
    for declaration in declarations:
        while event_index < len(events) and events[event_index].start < declaration.start():
            event = events[event_index]
            if event.action in {"namespace", "section"}:
                stack.append((event.action, event.name))
            elif event.action == "end":
                if not stack:
                    raise ExtractionError(
                        f"unmatched end command at character offset {event.start}"
                    )
                stack.pop()
            event_index += 1
        output[declaration.start()] = tuple(
            name for kind, name in stack if kind == "namespace" and name is not None
        )
    return output


def _qualified_name(namespaces: Sequence[str], local_name: str) -> str:
    if local_name.startswith("_root_."):
        return local_name[len("_root_."):]
    prefix = ".".join(namespaces)
    return f"{prefix}.{local_name}" if prefix else local_name


def _module_name(relative_path: str) -> str:
    path = PurePosixPath(relative_path)
    return ".".join(path.with_suffix("").parts)


def _license_object(snapshot: Snapshot) -> dict[str, str]:
    return {
        "code_spdx": "Apache-2.0",
        "license_file": "LICENSE",
        "license_file_sha256": sha256_bytes(snapshot.license_bytes),
        "repository_materials_spdx": "CC-BY-4.0",
        "repository_readme_sha256": sha256_bytes(snapshot.readme_bytes),
    }


def extract_file(
    source: SourceFile, snapshot: Snapshot
) -> tuple[list[dict[str, Any]], list[str]]:
    try:
        text = source.data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ExtractionError(f"{source.relative_path} is not strict UTF-8: {exc}") from exc
    try:
        mask, comments = mask_comments_and_strings(text)
        attributes = find_attribute_ranges(mask)
    except ExtractionError as exc:
        raise ExtractionError(f"{source.relative_path}: {exc}") from exc

    declarations = list(DECLARATION_RE.finditer(mask))
    namespaces = _namespaces_at(declarations, _scope_events(mask))
    doc_comments = [comment for comment in comments if comment.is_doc]
    imports = sorted(set(IMPORT_RE.findall(mask)))
    source_sha = sha256_bytes(source.data)
    license_info = _license_object(snapshot)
    records: list[dict[str, Any]] = []
    errors: list[str] = []

    for declaration_index, declaration in enumerate(declarations):
        associated, attribute_start = _associated_attributes(
            mask, declaration.start(), attributes
        )
        attribute_texts = [text[item.start:item.end] for item in associated]
        categories = _categories(attribute_texts)
        selected = [value for value in categories if value in SELECTED_CATEGORIES]
        if not selected:
            continue
        location = f"{source.relative_path}:{_line_number(text, declaration.start())}"
        if len(categories) != 1 or len(selected) != 1:
            errors.append(f"{location}: declaration must have exactly one selected category")
            continue
        ams_codes = _ams_codes(attribute_texts)
        if not ams_codes:
            errors.append(f"{location}: selected declaration has no AMS classification")
            continue
        if len(ams_codes) != len(set(ams_codes)):
            errors.append(f"{location}: selected declaration has duplicate AMS codes")
            continue
        invalid_ams = sorted(set(ams_codes) - MSC2020_TOP_LEVEL)
        if invalid_ams:
            errors.append(f"{location}: invalid top-level MSC2020 codes {invalid_ams!r}")
            continue

        docs = [comment for comment in doc_comments if comment.end <= attribute_start]
        doc = docs[-1] if docs else None
        if doc is None or mask[doc.end:attribute_start].strip():
            errors.append(f"{location}: selected declaration has no adjacent docstring")
            continue
        doc_raw = text[doc.start:doc.end]
        doc_text = doc_raw[3:-2]
        if not doc_text.strip():
            errors.append(f"{location}: selected declaration has an empty docstring")
            continue

        try:
            local_name, name_end = _parse_name(mask, declaration.end())
            boundary = (
                declarations[declaration_index + 1].start()
                if declaration_index + 1 < len(declarations)
                else len(mask)
            )
            separator, colon = _signature_end(mask, name_end, boundary)
        except ExtractionError as exc:
            errors.append(f"{location}: {exc}")
            continue
        if not mask[colon + 1:separator].strip():
            errors.append(f"{location}: declaration has an empty result type")
            continue

        # Preserve declaration modifiers such as ``private``/``protected``.
        modifier_gap = mask[associated[-1].end:declaration.start()] if associated else ""
        modifier_match = re.search(
            r"(?:private|protected|noncomputable|unsafe)(?:\s+(?:private|protected|noncomputable|unsafe))*\s*$",
            modifier_gap,
        )
        declaration_start = (
            associated[-1].end + modifier_match.start()
            if modifier_match is not None and associated
            else declaration.start()
        )
        signature_end = separator
        while signature_end > declaration_start and text[signature_end - 1].isspace():
            signature_end -= 1
        declaration_statement = text[declaration_start:signature_end]
        if not declaration_statement.strip():
            errors.append(f"{location}: declaration statement is empty")
            continue
        source_block = text[doc.start:signature_end]
        source_block_byte_start = len(text[:doc.start].encode("utf-8"))
        source_block_byte_end = len(text[:signature_end].encode("utf-8"))
        if source.data[source_block_byte_start:source_block_byte_end] != source_block.encode("utf-8"):
            errors.append(f"{location}: UTF-8 source-block byte offsets are inconsistent")
            continue
        statement_payload = _normalized_statement_payload(text, name_end, separator)
        if not statement_payload:
            errors.append(f"{location}: normalized declaration payload is empty")
            continue
        namespace = namespaces[declaration.start()]
        qualified_name = _qualified_name(namespace, local_name)
        try:
            formal_proofs = _formal_proofs(attribute_texts, namespace)
            answer_kinds = _answer_kinds(mask[colon + 1:separator])
        except ExtractionError as exc:
            errors.append(f"{location}: {exc}")
            continue
        effective_formal_proof = formal_proofs[-1] if formal_proofs else None
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
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "source_repository": SOURCE_REPOSITORY,
            "source_commit": snapshot.commit,
            "category": selected[0],
            "ams": ams_codes,
            "declaration_kind": declaration.group(1),
            "declaration_modifiers": modifier_words,
            "namespace": ".".join(namespace),
            "local_name": local_name,
            "qualified_name": qualified_name,
            # Names matching scripts/extract_names.lean are intentionally kept
            # at top level so a caller can diff this static source extraction
            # against upstream elaborated metadata.
            "theorem": qualified_name,
            "subjects": [str(int(code)) for code in ams_codes],
            "statement": text[name_end:separator].strip(),
            "statement_policy": "unelaborated Lean source after declaration name",
            "docstring": doc_text,
            "docstring_raw": doc_raw,
            "formalProofKind": (
                effective_formal_proof["kind"] if effective_formal_proof else None
            ),
            "formalProofLink": (
                effective_formal_proof["link"] if effective_formal_proof else None
            ),
            "hasSorryFreeProof": has_sorry_free_proof,
            "hasSorryFreeProofPolicy": (
                "no source-level sorry token before the next documented declaration"
            ),
            "answerKinds": answer_kinds,
            "answerKindsPolicy": "static source-context inference; compare to Lean elaboration",
            "proofConditions": (
                effective_formal_proof["proof_conditions"]
                if effective_formal_proof else []
            ),
            "formal_proofs": formal_proofs,
            "declaration_statement": declaration_statement,
            "declaration_sha256": sha256_bytes(declaration_statement.encode("utf-8")),
            "statement_sha256": sha256_bytes(statement_payload.encode("utf-8")),
            "statement_hash_policy": (
                "comments-and-strings-masked signature after declaration name; whitespace collapsed"
            ),
            "source_block": source_block,
            "source_block_sha256": sha256_bytes(source_block.encode("utf-8")),
            "source_file": source.relative_path,
            "archive_member": source.archive_member,
            "source_file_sha256": source_sha,
            "source_block_byte_start": source_block_byte_start,
            "source_block_byte_end_exclusive": source_block_byte_end,
            "source_line_start": _line_number(text, doc.start),
            "source_line_end": _line_number(text, signature_end),
            "declaration_line_start": _line_number(text, declaration_start),
            "declaration_line_end": _line_number(text, signature_end),
            "module": _module_name(source.relative_path),
            "module_imports": imports,
            "license": license_info,
        }
        records.append(record)
    return records, errors


def extract_snapshot(snapshot: Snapshot) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for source in snapshot.source_files:
        extracted, file_errors = extract_file(source, snapshot)
        records.extend(extracted)
        errors.extend(file_errors)
    if errors:
        preview = "\n".join(f"- {message}" for message in errors[:30])
        remainder = "" if len(errors) <= 30 else f"\n- ... {len(errors) - 30} more"
        raise ExtractionError(
            f"rejected {len(errors)} incomplete/invalid selected declarations:\n{preview}{remainder}"
        )
    records.sort(
        key=lambda row: (
            row["qualified_name"],
            row["source_file"],
            row["declaration_line_start"],
        )
    )
    by_name: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_name[record["qualified_name"]].append(record)
    duplicate_names = {
        name: rows for name, rows in by_name.items() if len(rows) > 1
    }
    if duplicate_names:
        details = "; ".join(
            f"{name}: {[row['source_file'] for row in rows]!r}"
            for name, rows in sorted(duplicate_names.items())[:20]
        )
        raise ExtractionError(
            f"duplicate qualified declaration names ({len(duplicate_names)} groups): {details}"
        )
    return records


def extraction_summary(
    snapshot: Snapshot, records: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    by_statement: defaultdict[str, list[str]] = defaultdict(list)
    for record in records:
        by_statement[str(record["statement_sha256"])].append(
            str(record["qualified_name"])
        )
    duplicate_groups = [
        {"statement_sha256": digest, "qualified_names": sorted(names)}
        for digest, names in sorted(by_statement.items())
        if len(names) > 1
    ]
    category_counts = Counter(str(record["category"]) for record in records)
    kind_counts = Counter(str(record["declaration_kind"]) for record in records)
    formal_proof_counts = Counter(
        str(record["formalProofKind"])
        for record in records
        if record["formalProofKind"] is not None
    )
    answer_kind_counts: Counter[str] = Counter()
    for record in records:
        answer_kind_counts.update(str(kind) for kind in record["answerKinds"])
    ams_counts: Counter[str] = Counter()
    for record in records:
        ams_counts.update(str(code) for code in record["ams"])
    jsonl = canonical_jsonl(records)
    return {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": snapshot.commit,
        "source_files_scanned": len(snapshot.source_files),
        "source_files_with_records": len({record["source_file"] for record in records}),
        "candidate_declarations": len(records),
        "unique_qualified_names": len({record["qualified_name"] for record in records}),
        "unique_statement_hashes": len(by_statement),
        "duplicate_statement_hash_groups": len(duplicate_groups),
        "duplicate_statement_declarations": sum(
            len(group["qualified_names"]) for group in duplicate_groups
        ),
        "duplicate_statements": duplicate_groups,
        "category_counts": dict(sorted(category_counts.items())),
        "declaration_kind_counts": dict(sorted(kind_counts.items())),
        "formal_proof_kind_counts": dict(sorted(formal_proof_counts.items())),
        "records_with_formal_proof": sum(
            record["formalProofKind"] is not None for record in records
        ),
        "records_with_proof_conditions": sum(
            bool(record["proofConditions"]) for record in records
        ),
        "source_inferred_sorry_free_proofs": sum(
            record["hasSorryFreeProof"] is True for record in records
        ),
        "answer_kind_counts": dict(sorted(answer_kind_counts.items())),
        "ams_membership_counts": dict(sorted(ams_counts.items())),
        "records_jsonl_sha256": sha256_bytes(jsonl.encode("utf-8")),
    }


def _write_output(path: Path | None, content: str) -> None:
    if path is None:
        sys.stdout.write(content)
        return
    path.write_text(content, encoding="utf-8", newline="")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        type=Path,
        help="pinned formal-conjectures checkout/archive directory or tar archive",
    )
    parser.add_argument("--output", "-o", type=Path, help="output path (default: stdout)")
    parser.add_argument(
        "--format",
        choices=("jsonl", "json"),
        default="jsonl",
        help="record output format (default: jsonl)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="also write a canonical extraction summary to stderr",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="write only the canonical extraction summary to stdout/output",
    )
    parser.add_argument(
        "--expected-commit",
        default=PINNED_COMMIT,
        help=f"required source commit (default: {PINNED_COMMIT})",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if re.fullmatch(r"[0-9a-f]{40}", args.expected_commit) is None:
            raise ExtractionError("--expected-commit must be 40 lowercase hexadecimal characters")
        snapshot = load_snapshot(args.source, args.expected_commit)
        records = extract_snapshot(snapshot)
        summary = extraction_summary(snapshot, records)
        if args.summary_only:
            content = canonical_json(summary) + "\n"
        elif args.format == "jsonl":
            content = canonical_jsonl(records)
        else:
            envelope = {
                "schema_version": "awesome-theorems/formal-conjectures-source-blocks/5.0",
                "summary": summary,
                "records": records,
            }
            content = canonical_json(envelope) + "\n"
        _write_output(args.output, content)
        if args.summary and not args.summary_only:
            sys.stderr.write(canonical_json(summary) + "\n")
    except (ExtractionError, OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL extract_formal_conjectures_v5: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
