#!/usr/bin/env python3
"""Generate the lossless Stage2 claim catalog and identity registries.

The three files in ``Docs/researches`` are untrusted source pools.  In
particular, a source label such as ``已验证`` is preserved verbatim and is
never converted into mathematical, formal-system, repository, or benchmark
credit by this generator.

Identity is deliberately conservative:

* ATO identifies a source occurrence.
* ATF is a lexical discovery family.  Membership does not assert equivalence.
* ATS is a provisional sense, one per occurrence until human review.
* ATV is a provisional statement variant, one per occurrence until review.

The old Stage0 six-field equality is emitted only as an unreviewed relation.
It never creates an alias, redirect, shared ATS, or shared ATV.  Historical
``THM-*`` IDs are snapshot aliases to the 3,262 Stage0 survivors and nothing
more.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import sys
import unicodedata
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / "Docs" / "researches"
CATALOG_DIR = ROOT / "Docs" / "catalog"

SOURCE_RECORDS_PATH = CATALOG_DIR / "Source_Records_v2.json"
ID_REGISTRY_PATH = CATALOG_DIR / "Claim_ID_Registry_v2.json"
RELATIONS_PATH = CATALOG_DIR / "Claim_Relations_v2.json"
CATALOG_JSON_PATH = CATALOG_DIR / "Claim_Catalog_v2.json"
CATALOG_MD_PATH = CATALOG_DIR / "Claim_Catalog_v2.md"
REPAIRS_DIR = CATALOG_DIR / "repairs"

STAGE0_PATH = ROOT / "Docs" / "Stage0_Blueprint.md"
SCHEMA_REF = "Docs/catalog/Claim_Record_Schema_v2.json"

BOOTSTRAP_OCCURRENCES = 3338
BOOTSTRAP_LEGACY_ALIASES = 3262
BOOTSTRAP_EXACT_CLUSTERS = 74
BOOTSTRAP_EXACT_EXTRAS = 76
BOOTSTRAP_TIMESTAMP = "2026-08-10T00:00:00+08:00"
ID_PATTERN = re.compile(r"^AT[OFSV]-[0-9]{8}$")
LEGACY_UNSEALED_SOURCE_SHA256 = "192c626f951f4e8862f4a46ef323b9a12bc49266c59cab8d32578b882e4aef76"
LEGACY_UNSEALED_REGISTRY_SHA256 = "60a61efa1394285288af09d8f743003bc1863b16748889707897a74d929f28fd"

LIST_SOURCES = (
    {
        "path": RESEARCH_DIR / "math_theorems.md",
        "discipline": "数学",
        "ignore_h2": {"概述", "目录"},
    },
    {
        "path": RESEARCH_DIR / "physics_theorems.md",
        "discipline": "物理",
        "ignore_h2": {"概述", "统计信息", "定理列表"},
    },
)
TABLE_SOURCE = {
    "path": RESEARCH_DIR / "cs_theorems.md",
    "discipline": "计算机科学",
    "ignore_h2": {"目录", "统计信息", "参考文献"},
}

DISCIPLINE_PREFIX = {"数学": "M", "物理": "P", "计算机科学": "C"}
DISCIPLINE_PRIORITY = {"数学": 0, "物理": 1, "计算机科学": 2}

H2_RE = re.compile(r"^##\s+(.*)$")
H3_RE = re.compile(r"^###\s+(.*)$")
THEOREM_RE = re.compile(r"^\*\*(.+?)\*\*$")
LIST_FIELD_RE = re.compile(r"^\s*-\s*(?:\*\*)?([^:*：]+?)(?:\*\*)?\s*[:：]\s*(.*)\s*$")


class CatalogError(RuntimeError):
    """A fail-closed catalog generation error."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_digest(namespace: str, payload: Any) -> str:
    return sha256_bytes(namespace.encode("utf-8") + b"\0" + canonical_json_bytes(payload))


def authority_digest(namespace: str, document: dict[str, Any]) -> str:
    body = {key: value for key, value in document.items() if key != "authority_sha256"}
    return stable_digest(namespace, body)


def seal_authority(namespace: str, document: dict[str, Any]) -> dict[str, Any]:
    document["authority_sha256"] = authority_digest(namespace, document)
    return document


def verify_authority(namespace: str, document: dict[str, Any], label: str) -> None:
    observed = document.get("authority_sha256")
    expected = authority_digest(namespace, document)
    if not isinstance(observed, str) or observed != expected:
        raise CatalogError(f"{label} authority digest is missing or stale")


def relation_id(prefix: str, namespace: str, payload: Any) -> tuple[str, str]:
    digest = stable_digest(namespace, payload)
    return f"{prefix}-{digest[:24].upper()}", digest


def parse_registry_ordinal(identifier: str, prefix: str) -> int:
    match = re.fullmatch(rf"{re.escape(prefix)}-([0-9]{{8}})", identifier)
    if match is None:
        raise CatalogError(f"invalid {prefix} registry ID: {identifier!r}")
    return int(match.group(1))


def next_registry_id(prefix: str, next_ordinal: int) -> str:
    if not 1 <= next_ordinal <= 99_999_999:
        raise CatalogError(f"{prefix} registry exhausted its eight-digit namespace")
    return f"{prefix}-{next_ordinal:08d}"


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip()
    return re.sub(r"\s+", " ", value)


def normalize_title_key(value: str) -> str:
    return normalize_text(value).casefold()


def strip_numeric_prefix(text: str) -> str:
    # This intentionally reproduces the historical Stage0 behavior, including
    # the leading dot left by headings such as ``2. 复杂性理论``.
    return re.sub(r"^\d+(?:\.\d+)?\s*", "", text).strip()


def normalize_title(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^\*\*(.+)\*\*$", r"\1", text)
    text = re.sub(r"^\d+\.\s*", "", text)
    return text.strip()


def normalize_subcategory(parent: str, child: str) -> str:
    parent = strip_numeric_prefix(parent)
    child = strip_numeric_prefix(child)
    if child.startswith(parent + "-"):
        leaf = child[len(parent) + 1 :].strip()
        return f"{parent} / {leaf}"
    if child.startswith(parent + " / "):
        return child
    return f"{parent} / {child}"


def normalize_field_key(key: str) -> str:
    return key.strip().replace(" ", "")


def split_lines_with_byte_offsets(data: bytes) -> tuple[list[str], list[int], list[int]]:
    byte_lines = data.splitlines(keepends=True)
    if not byte_lines and data == b"":
        return [], [], []
    if data and (not byte_lines or sum(map(len, byte_lines)) != len(data)):
        raise CatalogError("source line splitting lost bytes")
    lines: list[str] = []
    starts: list[int] = []
    ends: list[int] = []
    cursor = 0
    for raw in byte_lines:
        starts.append(cursor)
        cursor += len(raw)
        ends.append(cursor)
        lines.append(raw.decode("utf-8").rstrip("\r\n"))
    return lines, starts, ends


@dataclass
class Candidate:
    discipline: str
    subcategory: str
    name: str
    proposer: str
    proposed_time: str
    statement: str
    importance: str
    formal_status: str
    source_file: str
    parser: str
    raw_section_path: list[str]
    source_domain: str = ""
    source_label: str = ""
    source_record_ordinal: int = 0
    section_record_ordinal: int = 0
    global_source_ordinal: int = 0
    line_start: int = 0
    line_end: int = 0
    byte_start: int = 0
    byte_end_exclusive: int = 0
    raw_text: str = ""
    occurrence_key_sha256: str = ""
    occurrence_anchor_sha256: str = ""
    occurrence_id: str = ""
    birth_locator: dict[str, Any] = field(default_factory=dict)
    current_locator: dict[str, Any] = field(default_factory=dict)

    def raw_fields(self) -> dict[str, str]:
        return {
            "discipline": self.discipline,
            "subcategory": self.subcategory,
            "name": self.name,
            "proposer": self.proposer,
            "proposed_time": self.proposed_time,
            "statement": self.statement,
            "importance": self.importance,
            "formal_status": self.formal_status,
            "source_domain": self.source_domain,
        }

    def legacy_exact_signature(self) -> tuple[str, str, str, str, str, str]:
        return (
            self.name,
            self.statement,
            self.proposer,
            self.proposed_time,
            self.importance,
            self.formal_status,
        )


def _finalize_list_candidate(
    current: dict[str, Any] | None,
    output: list[Candidate],
    data: bytes,
) -> None:
    if current is None:
        return
    byte_start = current.pop("byte_start")
    byte_end = current.pop("byte_end_exclusive")
    current["raw_text"] = data[byte_start:byte_end].decode("utf-8")
    current["byte_start"] = byte_start
    current["byte_end_exclusive"] = byte_end
    current["source_record_ordinal"] = len(output) + 1
    output.append(Candidate(**current))


def parse_list_source(path: Path, discipline: str, ignore_h2: set[str]) -> list[Candidate]:
    data = path.read_bytes()
    lines, starts, ends = split_lines_with_byte_offsets(data)
    output: list[Candidate] = []
    current_h2: str | None = None
    current_h3: str | None = None
    raw_h2: str | None = None
    raw_h3: str | None = None
    current: dict[str, Any] | None = None

    for index, line in enumerate(lines):
        h2_match = H2_RE.match(line)
        if h2_match:
            _finalize_list_candidate(current, output, data)
            current = None
            heading = h2_match.group(1).strip()
            if heading in ignore_h2:
                current_h2 = current_h3 = raw_h2 = raw_h3 = None
                continue
            current_h2 = heading
            current_h3 = None
            raw_h2 = heading
            raw_h3 = None
            continue

        h3_match = H3_RE.match(line)
        if h3_match:
            _finalize_list_candidate(current, output, data)
            current = None
            if current_h2 is None:
                continue
            raw_h3 = h3_match.group(1).strip()
            current_h3 = normalize_subcategory(current_h2, raw_h3)
            continue

        theorem_match = THEOREM_RE.match(line.strip())
        if theorem_match and current_h2 is not None:
            _finalize_list_candidate(current, output, data)
            theorem_label = theorem_match.group(1)
            theorem_name = normalize_title(theorem_label)
            if theorem_name.startswith("定理数量"):
                current = None
                continue
            current = {
                "discipline": discipline,
                "subcategory": current_h3 or strip_numeric_prefix(current_h2),
                "name": theorem_name,
                "proposer": "待补充",
                "proposed_time": "待补充",
                "statement": "待补充",
                "importance": "待补充",
                "formal_status": "待补充",
                "source_file": str(path.relative_to(ROOT)),
                "parser": "markdown_list/v2",
                "raw_section_path": [x for x in (raw_h2, raw_h3) if x is not None],
                "source_label": theorem_label,
                "line_start": index + 1,
                "line_end": index + 1,
                "byte_start": starts[index],
                "byte_end_exclusive": ends[index],
            }
            continue

        if current is None:
            continue
        field_match = LIST_FIELD_RE.match(line)
        if not field_match:
            continue
        key = normalize_field_key(field_match.group(1))
        value = field_match.group(2).strip() or "待补充"
        destination = {
            "提出者": "proposer",
            "时间": "proposed_time",
            "陈述": "statement",
            "重要性": "importance",
            "形式化状态": "formal_status",
        }.get(key)
        if destination is not None:
            current[destination] = value
            current["line_end"] = index + 1
            current["byte_end_exclusive"] = ends[index]

    _finalize_list_candidate(current, output, data)
    return output


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and not re.match(r"^\|\s*-", stripped)


def parse_table_source(path: Path, discipline: str, ignore_h2: set[str]) -> list[Candidate]:
    data = path.read_bytes()
    lines, starts, ends = split_lines_with_byte_offsets(data)
    output: list[Candidate] = []
    current_h2: str | None = None
    current_h3: str | None = None
    raw_h2: str | None = None
    raw_h3: str | None = None

    for index, line in enumerate(lines):
        h2_match = H2_RE.match(line)
        if h2_match:
            heading = h2_match.group(1).strip()
            if heading in ignore_h2:
                current_h2 = current_h3 = raw_h2 = raw_h3 = None
                continue
            current_h2 = strip_numeric_prefix(heading)
            current_h3 = None
            raw_h2 = heading
            raw_h3 = None
            continue
        h3_match = H3_RE.match(line)
        if h3_match:
            if current_h2 is None:
                continue
            raw_h3 = h3_match.group(1).strip()
            current_h3 = normalize_subcategory(current_h2, raw_h3)
            continue
        if current_h2 is None or current_h3 is None or not is_table_row(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        if cells[0] in {"序号", "重要性级别", "形式化状态", "分支"}:
            continue
        if not re.match(r"^\d+(?:\.\d+)*$", cells[0]):
            continue
        raw_text = data[starts[index] : ends[index]].decode("utf-8")
        output.append(
            Candidate(
                discipline=discipline,
                subcategory=current_h3,
                name=normalize_title(cells[1]),
                source_domain=cells[2],
                proposer=cells[3] or "待补充",
                proposed_time=cells[4] or "待补充",
                statement=cells[5] or "待补充",
                importance=cells[6] or "待补充",
                formal_status=cells[7] or "待补充",
                source_file=str(path.relative_to(ROOT)),
                parser="markdown_table/v2",
                raw_section_path=[x for x in (raw_h2, raw_h3) if x is not None],
                source_label=cells[0],
                source_record_ordinal=len(output) + 1,
                line_start=index + 1,
                line_end=index + 1,
                byte_start=starts[index],
                byte_end_exclusive=ends[index],
                raw_text=raw_text,
            )
        )
    return output


def source_snapshot() -> dict[str, Any]:
    paths = [source["path"] for source in LIST_SOURCES] + [TABLE_SOURCE["path"]]
    files = [
        {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }
        for path in paths
    ]
    return {
        "files": files,
        "aggregate_sha256": stable_digest("awesome-theorems/source-snapshot/v2", files),
    }


def parse_all_sources() -> list[Candidate]:
    candidates: list[Candidate] = []
    for source in LIST_SOURCES:
        candidates.extend(
            parse_list_source(source["path"], source["discipline"], source["ignore_h2"])
        )
    candidates.extend(
        parse_table_source(
            TABLE_SOURCE["path"],
            TABLE_SOURCE["discipline"],
            TABLE_SOURCE["ignore_h2"],
        )
    )

    source_counters: Counter[str] = Counter()
    section_counters: Counter[tuple[str, str]] = Counter()
    title_groups: defaultdict[str, list[Candidate]] = defaultdict(list)
    for global_ordinal, candidate in enumerate(candidates, start=1):
        source_counters[candidate.source_file] += 1
        # Parsers already assign this, but recomputing makes the invariant explicit.
        if candidate.source_record_ordinal != source_counters[candidate.source_file]:
            raise CatalogError(f"non-contiguous source ordinal in {candidate.source_file}")
        section_key = (candidate.source_file, candidate.subcategory)
        section_counters[section_key] += 1
        candidate.section_record_ordinal = section_counters[section_key]
        candidate.global_source_ordinal = global_ordinal
        candidate.current_locator = {
            "path": candidate.source_file,
            "parser": candidate.parser,
            "raw_section_path": candidate.raw_section_path,
            "normalized_subcategory": candidate.subcategory,
            "source_label": candidate.source_label,
            "source_record_ordinal": candidate.source_record_ordinal,
            "section_record_ordinal": candidate.section_record_ordinal,
            "global_source_ordinal": candidate.global_source_ordinal,
            "line_start": candidate.line_start,
            "line_end": candidate.line_end,
            "byte_start": candidate.byte_start,
            "byte_end_exclusive": candidate.byte_end_exclusive,
            "raw_block_sha256": sha256_bytes(candidate.raw_text.encode("utf-8")),
        }
        title_anchor = {
            "source_path": candidate.source_file,
            "parser": candidate.parser,
            "normalized_title": normalize_title_key(candidate.name),
        }
        title_groups[stable_digest("awesome-theorems/occurrence-title-anchor/v2", title_anchor)].append(candidate)

    for title_anchor_sha256, title_group in title_groups.items():
        for candidate in title_group:
            candidate.occurrence_anchor_sha256 = title_anchor_sha256
        if len(title_group) == 1:
            title_group[0].occurrence_key_sha256 = stable_digest(
                "awesome-theorems/occurrence-key/v3",
                {"title_anchor_sha256": title_anchor_sha256},
            )
            continue

        disambiguated: defaultdict[str, list[Candidate]] = defaultdict(list)
        for candidate in title_group:
            # Mutable catalog metadata (importance, raw status, category and
            # line/order locators) is deliberately absent.  A status edit must
            # update the occurrence in place and must not mint new ATO/ATS/ATV
            # IDs.  Statement/attribution fields disambiguate genuine homonyms.
            disambiguator = {
                "statement": normalize_text(candidate.statement),
                "proposer": normalize_text(candidate.proposer),
                "proposed_time": normalize_text(candidate.proposed_time),
                "source_domain": normalize_text(candidate.source_domain),
            }
            disambiguator_sha256 = stable_digest(
                "awesome-theorems/occurrence-disambiguator/v3", disambiguator
            )
            disambiguated[disambiguator_sha256].append(candidate)

        for disambiguator_sha256, group in disambiguated.items():
            if len(group) == 1:
                group[0].occurrence_key_sha256 = stable_digest(
                    "awesome-theorems/occurrence-key/v3",
                    {
                        "title_anchor_sha256": title_anchor_sha256,
                        "disambiguator_sha256": disambiguator_sha256,
                    },
                )
                continue
            category_groups: defaultdict[str, list[Candidate]] = defaultdict(list)
            for candidate in group:
                category_anchor = normalize_text(candidate.subcategory).casefold()
                category_groups[category_anchor].append(candidate)
            for category_anchor, category_group in category_groups.items():
                category_group.sort(key=lambda candidate: candidate.global_source_ordinal)
                for duplicate_slot, candidate in enumerate(category_group, start=1):
                    candidate.occurrence_key_sha256 = stable_digest(
                        "awesome-theorems/occurrence-key/v3",
                        {
                            "title_anchor_sha256": title_anchor_sha256,
                            "disambiguator_sha256": disambiguator_sha256,
                            "category_anchor": category_anchor,
                            "duplicate_slot": duplicate_slot,
                        },
                    )
    return candidates


def read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CatalogError(f"{path.relative_to(ROOT)} is not a JSON object")
    return value


def compatible_previous_source_records(value: dict[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    records = value.get("records")
    if (
        value.get("schema_version") != "awesome-theorems/source-records/2.0"
        or value.get("identity_policy", {}).get("occurrence_key_version") != "v3-status-stable"
        or not isinstance(records, list)
    ):
        raise CatalogError("existing Source_Records_v2.json has an unsupported authority schema")
    if not all(re.fullmatch(r"ATO-[0-9]{8}", str(row.get("occurrence_id"))) for row in records):
        raise CatalogError("existing Source_Records_v2.json contains invalid occurrence IDs")
    if "authority_sha256" in value:
        verify_authority(
            "awesome-theorems/source-records-authority/v2",
            value,
            "Source_Records_v2.json",
        )
    elif sha256_bytes(pretty_json(value).encode("utf-8")) != LEGACY_UNSEALED_SOURCE_SHA256:
        raise CatalogError("unsealed Source_Records_v2.json is not the reviewed migration input")
    return value


def compatible_previous_registry(value: dict[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    if (
        value.get("schema_version") != "awesome-theorems/claim-id-registry/2.0"
        or value.get("allocation_policy", {}).get("occurrence_key_version") != "v3-status-stable"
    ):
        raise CatalogError("existing Claim_ID_Registry_v2.json has an unsupported authority schema")
    groups = (("families", "family_id", "ATF"), ("senses", "sense_id", "ATS"), ("variants", "variant_id", "ATV"))
    for group, field, prefix in groups:
        rows = value.get(group)
        if not isinstance(rows, list) or not all(
            re.fullmatch(rf"{prefix}-[0-9]{{8}}", str(row.get(field))) for row in rows
        ):
            raise CatalogError(f"existing Claim_ID_Registry_v2.json contains invalid {prefix} IDs")
    if "authority_sha256" in value:
        verify_authority(
            "awesome-theorems/claim-id-registry-authority/v2",
            value,
            "Claim_ID_Registry_v2.json",
        )
    elif sha256_bytes(pretty_json(value).encode("utf-8")) != LEGACY_UNSEALED_REGISTRY_SHA256:
        raise CatalogError("unsealed Claim_ID_Registry_v2.json is not the reviewed migration input")
    return value


def build_source_records(
    candidates: list[Candidate], snapshot: dict[str, Any], previous: dict[str, Any] | None
) -> dict[str, Any]:
    previous_by_key: dict[str, dict[str, Any]] = {}
    previous_ids: set[str] = set()
    if previous is not None:
        if previous.get("schema_version") != "awesome-theorems/source-records/2.0":
            raise CatalogError("existing Source_Records_v2.json has an unsupported schema")
        for record in previous.get("records", []):
            key = record.get("occurrence_key_sha256")
            occurrence_id = record.get("occurrence_id")
            if (
                not isinstance(key, str)
                or key in previous_by_key
                or not isinstance(occurrence_id, str)
                or re.fullmatch(r"ATO-[0-9]{8}", occurrence_id) is None
                or occurrence_id in previous_ids
                or record.get("idempotency_request_sha256") != key
            ):
                raise CatalogError("existing source occurrence keys are missing or duplicated")
            anchor = record.get("occurrence_anchor_sha256")
            if "authority_sha256" in previous and (
                not isinstance(anchor, str) or re.fullmatch(r"[0-9a-f]{64}", anchor) is None
            ):
                raise CatalogError("sealed source occurrence has no valid immutable title anchor")
            previous_by_key[key] = record
            previous_ids.add(occurrence_id)

    def old_anchor(record: dict[str, Any]) -> str:
        anchor = record.get("occurrence_anchor_sha256")
        if isinstance(anchor, str):
            return anchor
        locator = record.get("birth_locator") or record.get("current_locator") or {}
        fields = record.get("raw_fields") or {}
        return stable_digest(
            "awesome-theorems/occurrence-title-anchor/v2",
            {
                "source_path": locator.get("path"),
                "parser": locator.get("parser"),
                "normalized_title": normalize_title_key(str(fields.get("name", ""))),
            },
        )

    # Reconcile duplicate-title groups as a set.  Mutable status/category data
    # is used only as a matching hint; it is never encoded in the allocated ID.
    # This preserves identities when rows are reordered or one mutable field is
    # edited, while a new member still receives max+1.
    matched_old_by_candidate: dict[int, dict[str, Any]] = {}
    if previous_by_key:
        old_groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        current_groups: defaultdict[str, list[int]] = defaultdict(list)
        for record in previous_by_key.values():
            old_groups[old_anchor(record)].append(record)
        for index, candidate in enumerate(candidates):
            current_groups[candidate.occurrence_anchor_sha256].append(index)
            collision = previous_by_key.get(candidate.occurrence_key_sha256)
            if collision is not None and old_anchor(collision) != candidate.occurrence_anchor_sha256:
                raise CatalogError(
                    "occurrence-key collision has unequal immutable title anchors: "
                    + candidate.occurrence_key_sha256
                )

        # Exact-content landmarks make insertions observable without putting a
        # mutable line number into identity.  They are used only to decide
        # which member of an otherwise byte-identical duplicate bucket is the
        # pre-existing occurrence.  A unique row before/after an insertion
        # supplies the source-record ordinal shift; if no unique optimum exists
        # we fail closed instead of silently moving an old ATO to a new row.
        global_current_by_raw: defaultdict[tuple[str, str, bytes], list[int]] = defaultdict(list)
        global_old_by_raw: defaultdict[tuple[str, str, bytes], list[dict[str, Any]]] = defaultdict(list)
        for index, candidate in enumerate(candidates):
            locator = candidate.current_locator
            global_current_by_raw[
                (
                    str(locator.get("path", "")),
                    str(locator.get("parser", "")),
                    canonical_json_bytes(candidate.raw_fields()),
                )
            ].append(index)
        for row in previous_by_key.values():
            locator = row.get("current_locator") or {}
            if not locator:
                continue
            global_old_by_raw[
                (
                    str(locator.get("path", "")),
                    str(locator.get("parser", "")),
                    canonical_json_bytes(row["raw_fields"]),
                )
            ].append(row)
        landmarks: defaultdict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
        for raw_key in set(global_current_by_raw) & set(global_old_by_raw):
            current_bucket = global_current_by_raw[raw_key]
            old_bucket = global_old_by_raw[raw_key]
            if len(current_bucket) != 1 or len(old_bucket) != 1:
                continue
            current_locator = candidates[current_bucket[0]].current_locator
            old_locator = old_bucket[0].get("current_locator") or {}
            current_ordinal = current_locator.get("source_record_ordinal")
            old_ordinal = old_locator.get("source_record_ordinal")
            if isinstance(current_ordinal, int) and isinstance(old_ordinal, int):
                landmarks[(raw_key[0], raw_key[1])].append(
                    (old_ordinal, current_ordinal)
                )
        for rows in landmarks.values():
            rows.sort()

        def expected_source_ordinal(row: dict[str, Any]) -> int | None:
            locator = row.get("current_locator") or {}
            old_ordinal = locator.get("source_record_ordinal")
            if not isinstance(old_ordinal, int):
                return None
            source_key = (str(locator.get("path", "")), str(locator.get("parser", "")))
            source_landmarks = landmarks.get(source_key, [])
            following = next(
                (pair for pair in source_landmarks if pair[0] > old_ordinal),
                None,
            )
            if following is not None:
                return old_ordinal + (following[1] - following[0])
            preceding = next(
                (pair for pair in reversed(source_landmarks) if pair[0] < old_ordinal),
                None,
            )
            if preceding is not None:
                return old_ordinal + (preceding[1] - preceding[0])
            return None

        def pair_exact_raw_bucket(
            current_bucket: list[int], old_bucket: list[dict[str, Any]]
        ) -> list[tuple[int, dict[str, Any]]]:
            current_bucket = sorted(
                current_bucket,
                key=lambda index: (
                    candidates[index].current_locator.get("source_record_ordinal", 0),
                    candidates[index].current_locator.get("global_source_ordinal", 0),
                ),
            )
            old_bucket = sorted(
                old_bucket,
                key=lambda row: (
                    (row.get("current_locator") or {}).get("source_record_ordinal", 0),
                    row["occurrence_id"],
                ),
            )
            if len(current_bucket) == len(old_bucket):
                return list(zip(current_bucket, old_bucket))
            if len(current_bucket) < len(old_bucket):
                raise CatalogError(
                    "ambiguous deletion inside a byte-identical occurrence bucket; "
                    "retain an explicit source occurrence identifier or review the tombstone"
                )
            expected = [expected_source_ordinal(row) for row in old_bucket]
            if any(value is None for value in expected):
                raise CatalogError(
                    "byte-identical insertion has no unique neighboring landmark; "
                    "refusing to rebind an existing occurrence"
                )
            ranked: list[tuple[int, tuple[int, ...]]] = []
            for selected in combinations(current_bucket, len(old_bucket)):
                score = sum(
                    abs(
                        int(candidates[index].current_locator["source_record_ordinal"])
                        - int(target)
                    )
                    for index, target in zip(selected, expected)
                )
                ranked.append((score, selected))
            best_score = min(score for score, _ in ranked)
            best = [selected for score, selected in ranked if score == best_score]
            if len(best) != 1:
                raise CatalogError(
                    "byte-identical insertion admits multiple equally plausible old-ID bindings"
                )
            return list(zip(best[0], old_bucket))

        for anchor, candidate_indexes in current_groups.items():
            old_rows = old_groups.get(anchor, [])
            if not old_rows:
                continue
            remaining_current = set(candidate_indexes)
            remaining_old = {row["occurrence_id"]: row for row in old_rows}

            current_by_raw: defaultdict[bytes, list[int]] = defaultdict(list)
            old_by_raw: defaultdict[bytes, list[dict[str, Any]]] = defaultdict(list)
            for index in candidate_indexes:
                current_by_raw[canonical_json_bytes(candidates[index].raw_fields())].append(index)
            for row in old_rows:
                old_by_raw[canonical_json_bytes(row["raw_fields"])].append(row)
            for raw_key in sorted(set(current_by_raw) & set(old_by_raw)):
                for index, row in pair_exact_raw_bucket(
                    current_by_raw[raw_key], old_by_raw[raw_key]
                ):
                    matched_old_by_candidate[index] = row
                    remaining_current.discard(index)
                    remaining_old.pop(row["occurrence_id"], None)

            old_by_locator: dict[tuple[Any, ...], dict[str, Any]] = {}
            for row in remaining_old.values():
                locator = row.get("current_locator") or {}
                key = (
                    locator.get("path"),
                    locator.get("parser"),
                    locator.get("source_record_ordinal"),
                )
                if key not in old_by_locator:
                    old_by_locator[key] = row
            for index in sorted(remaining_current):
                locator = candidates[index].current_locator
                key = (locator.get("path"), locator.get("parser"), locator.get("source_record_ordinal"))
                row = old_by_locator.get(key)
                if row is None or row["occurrence_id"] not in remaining_old:
                    continue
                matched_old_by_candidate[index] = row
                remaining_current.discard(index)
                remaining_old.pop(row["occurrence_id"], None)

            for index in sorted(
                remaining_current,
                key=lambda value: (
                    candidates[value].occurrence_key_sha256,
                    candidates[value].current_locator["global_source_ordinal"],
                ),
            ):
                same_key = previous_by_key.get(candidates[index].occurrence_key_sha256)
                if same_key is None or same_key["occurrence_id"] not in remaining_old:
                    continue
                matched_old_by_candidate[index] = same_key
                remaining_old.pop(same_key["occurrence_id"])

            remaining_current = {
                index for index in remaining_current if index not in matched_old_by_candidate
            }
            if remaining_current and remaining_old:
                raise CatalogError(
                    "ambiguous same-title reconciliation would rebind an existing occurrence"
                )

        # A correction may legitimately change the title anchor itself.  Once
        # all exact content/key/locator matches have been consumed, a single
        # one-field revision in a source is still identifiable.  More complex
        # replacements remain review-required and fail closed.
        used_old_ids = {
            row["occurrence_id"] for row in matched_old_by_candidate.values()
        }
        unmatched_current_by_source: defaultdict[tuple[str, str], list[int]] = defaultdict(list)
        unmatched_old_by_source: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for index, candidate in enumerate(candidates):
            if index in matched_old_by_candidate:
                continue
            locator = candidate.current_locator
            unmatched_current_by_source[
                (str(locator.get("path", "")), str(locator.get("parser", "")))
            ].append(index)
        for row in previous_by_key.values():
            if row["occurrence_id"] in used_old_ids or row.get("lifecycle") == "retired":
                continue
            locator = row.get("current_locator") or {}
            unmatched_old_by_source[
                (str(locator.get("path", "")), str(locator.get("parser", "")))
            ].append(row)

        def changed_raw_fields(candidate: Candidate, row: dict[str, Any]) -> int:
            current = candidate.raw_fields()
            old = row["raw_fields"]
            return sum(current.get(key) != old.get(key) for key in set(current) | set(old))

        for source_key in set(unmatched_current_by_source) & set(unmatched_old_by_source):
            current_rows = unmatched_current_by_source[source_key]
            old_rows = unmatched_old_by_source[source_key]
            edges: list[tuple[int, str, dict[str, Any]]] = []
            for index in current_rows:
                for row in old_rows:
                    current_ordinal = candidates[index].current_locator.get(
                        "source_record_ordinal"
                    )
                    expected_ordinal = expected_source_ordinal(row)
                    old_ordinal = (row.get("current_locator") or {}).get(
                        "source_record_ordinal"
                    )
                    locator_agrees = (
                        current_ordinal == expected_ordinal
                        if expected_ordinal is not None
                        else current_ordinal == old_ordinal
                    )
                    if (
                        changed_raw_fields(candidates[index], row) == 1
                        and locator_agrees
                    ):
                        edges.append((index, row["occurrence_id"], row))
            while edges:
                current_counts = Counter(index for index, _, _ in edges)
                old_counts = Counter(old_id for _, old_id, _ in edges)
                forced = next(
                    (
                        edge
                        for edge in edges
                        if current_counts[edge[0]] == 1 and old_counts[edge[1]] == 1
                    ),
                    None,
                )
                if forced is None:
                    raise CatalogError(
                        "one-field occurrence corrections are ambiguous within a source"
                    )
                index, old_id, row = forced
                matched_old_by_candidate[index] = row
                edges = [
                    edge for edge in edges if edge[0] != index and edge[1] != old_id
                ]

            used_now = {
                row["occurrence_id"] for row in matched_old_by_candidate.values()
            }
            for index in current_rows:
                if index in matched_old_by_candidate:
                    continue
                current_locator = candidates[index].current_locator
                for row in old_rows:
                    if row["occurrence_id"] in used_now:
                        continue
                    old_locator = row.get("current_locator") or {}
                    if (
                        current_locator.get("source_record_ordinal")
                        == old_locator.get("source_record_ordinal")
                    ):
                        raise CatalogError(
                            "multi-field replacement at an existing source locator requires review"
                        )

    observed_max_ordinal = max(
        (parse_registry_ordinal(record["occurrence_id"], "ATO") for record in previous_by_key.values()),
        default=0,
    )
    previous_high_watermark = observed_max_ordinal
    if previous is not None and "namespace_high_watermark" in previous:
        previous_high_watermark = previous["namespace_high_watermark"]
        if (
            not isinstance(previous_high_watermark, int)
            or isinstance(previous_high_watermark, bool)
            or previous_high_watermark < observed_max_ordinal
        ):
            raise CatalogError("ATO namespace high-water mark is invalid or below an allocated ID")
    next_ordinal = previous_high_watermark + 1

    current_keys: set[str] = set()
    records: list[dict[str, Any]] = []
    for candidate_index, candidate in enumerate(candidates):
        old = matched_old_by_candidate.get(candidate_index)
        if old is not None:
            candidate.occurrence_key_sha256 = old["occurrence_key_sha256"]
            candidate.occurrence_anchor_sha256 = old_anchor(old)
        key = candidate.occurrence_key_sha256
        if key in current_keys:
            raise CatalogError(f"duplicate current occurrence key: {key}")
        current_keys.add(key)
        if old is None:
            candidate.occurrence_id = next_registry_id("ATO", next_ordinal)
            next_ordinal += 1
        else:
            candidate.occurrence_id = old["occurrence_id"]
        birth_locator = candidate.current_locator if old is None else old.get("birth_locator")
        first_seen = (
            snapshot["aggregate_sha256"]
            if old is None
            else old.get("first_seen_source_snapshot_sha256")
        )
        if not isinstance(birth_locator, dict) or not isinstance(first_seen, str):
            raise CatalogError(f"invalid birth data for {candidate.occurrence_id}")
        candidate.birth_locator = birth_locator
        records.append(
            {
                "occurrence_id": candidate.occurrence_id,
                "occurrence_key_sha256": key,
                "occurrence_anchor_sha256": candidate.occurrence_anchor_sha256,
                "idempotency_request_sha256": key,
                "lifecycle": "current",
                "first_seen_source_snapshot_sha256": first_seen,
                "birth_locator": birth_locator,
                "current_locator": candidate.current_locator,
                "raw_fields": candidate.raw_fields(),
                "raw_text": candidate.raw_text,
                "raw_text_sha256": sha256_bytes(candidate.raw_text.encode("utf-8")),
                "source_status_authority": "untrusted_raw_label_only",
            }
        )

    for key, old in previous_by_key.items():
        if key in current_keys:
            continue
        retired = dict(old)
        retired["lifecycle"] = "retired"
        retired["current_locator"] = None
        records.append(retired)

    records.sort(key=lambda row: row["occurrence_id"])
    counts = Counter(
        row["raw_fields"]["discipline"] for row in records if row["lifecycle"] == "current"
    )
    document = {
        "schema_version": "awesome-theorems/source-records/2.0",
        "catalog_schema_ref": SCHEMA_REF,
        "generated_by": "Docs/tools/generate_claim_catalog_v2.py",
        "source_snapshot": snapshot,
        "identity_policy": {
            "namespace": "ATO",
            "occurrence_key_version": "v3-status-stable",
            "allocation": "append-only eight-digit registry; idempotency key is content-derived but is not the ID",
            "append_only": True,
            "existing_ids_survive_reorder_and_insertion": True,
            "new_ids_use_max_plus_one": True,
            "birth_locator_immutable": True,
            "current_locator_refreshable": True,
            "source_order_or_line_number_in_identity": False,
            "byte_identical_insertion_reconciliation": "use unique neighboring content landmarks to preserve old occurrences; ambiguous bindings fail closed",
            "single_field_correction_reconciliation": "preserve the old occurrence only when the one-field source revision is uniquely matchable",
            "ambiguous_reconciliation": "fail_closed_without_rebinding_or_allocation",
            "raw_status_is_evidence": False,
            "authority_digest": "sha256 over canonical JSON excluding authority_sha256",
        },
        "namespace_high_watermark": max(
            previous_high_watermark,
            max(
                (parse_registry_ordinal(record["occurrence_id"], "ATO") for record in records),
                default=0,
            ),
        ),
        "counts": {
            "allocated_occurrences": len(records),
            "current_occurrences": sum(row["lifecycle"] == "current" for row in records),
            "retired_occurrences": sum(row["lifecycle"] == "retired" for row in records),
            "current_by_discipline": dict(sorted(counts.items())),
        },
        "records": records,
    }
    return seal_authority("awesome-theorems/source-records-authority/v2", document)


def build_allocations(
    source_records: dict[str, Any], previous_registry: dict[str, Any] | None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, str]]]:
    previous_families: dict[str, dict[str, Any]] = {}
    previous_senses: dict[str, dict[str, Any]] = {}
    previous_variants: dict[str, dict[str, Any]] = {}
    previous_family_ids: set[str] = set()
    previous_sense_ids: set[str] = set()
    previous_variant_ids: set[str] = set()
    record_occurrence_ids = {row["occurrence_id"] for row in source_records["records"]}
    if previous_registry is not None:
        for row in previous_registry.get("families", []):
            family_id = row.get("family_id")
            title_key = row.get("lexical_title_key")
            if (
                re.fullmatch(r"ATF-[0-9]{8}", str(family_id)) is None
                or not isinstance(title_key, str)
                or family_id in previous_family_ids
                or row.get("idempotency_request_sha256")
                != stable_digest(
                    "awesome-theorems/idempotency/family/v2",
                    {"lexical_title_key": title_key},
                )
            ):
                raise CatalogError("existing family allocation is invalid")
            if title_key in previous_families:
                raise CatalogError(f"duplicate existing family key: {title_key!r}")
            previous_families[title_key] = row
            previous_family_ids.add(family_id)
        for row in previous_registry.get("senses", []):
            sense_id = row.get("sense_id")
            occurrence_id = row.get("bootstrap_occurrence_id")
            if (
                re.fullmatch(r"ATS-[0-9]{8}", str(sense_id)) is None
                or not isinstance(occurrence_id, str)
                or sense_id in previous_sense_ids
                or occurrence_id in previous_senses
                or row.get("idempotency_request_sha256")
                != stable_digest(
                    "awesome-theorems/idempotency/sense/v2",
                    {"bootstrap_occurrence_id": occurrence_id},
                )
            ):
                raise CatalogError("existing sense allocation is invalid")
            previous_senses[occurrence_id] = row
            previous_sense_ids.add(sense_id)
        for row in previous_registry.get("variants", []):
            variant_id = row.get("variant_id")
            occurrence_id = row.get("bootstrap_occurrence_id")
            if (
                re.fullmatch(r"ATV-[0-9]{8}", str(variant_id)) is None
                or not isinstance(occurrence_id, str)
                or variant_id in previous_variant_ids
                or occurrence_id in previous_variants
                or row.get("idempotency_request_sha256")
                != stable_digest(
                    "awesome-theorems/idempotency/variant/v2",
                    {"bootstrap_occurrence_id": occurrence_id},
                )
            ):
                raise CatalogError("existing variant allocation is invalid")
            previous_variants[occurrence_id] = row
            previous_variant_ids.add(variant_id)
        if (
            set(previous_senses) != set(previous_variants)
            or not set(previous_senses) <= record_occurrence_ids
        ):
            raise CatalogError("append-only registry/source-record occurrence coverage is inconsistent")

    observed_family_max = max(
        (parse_registry_ordinal(row["family_id"], "ATF") for row in previous_families.values()),
        default=0,
    )
    observed_sense_max = max(
        (parse_registry_ordinal(row["sense_id"], "ATS") for row in previous_senses.values()),
        default=0,
    )
    observed_variant_max = max(
        (parse_registry_ordinal(row["variant_id"], "ATV") for row in previous_variants.values()),
        default=0,
    )
    high_watermarks = {
        "ATF": observed_family_max,
        "ATS": observed_sense_max,
        "ATV": observed_variant_max,
    }
    if previous_registry is not None and "namespace_high_watermarks" in previous_registry:
        stored = previous_registry["namespace_high_watermarks"]
        if not isinstance(stored, dict):
            raise CatalogError("registry namespace high-water marks are not an object")
        for prefix, observed in tuple(high_watermarks.items()):
            value = stored.get(prefix)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < observed
            ):
                raise CatalogError(f"{prefix} namespace high-water mark is invalid")
            high_watermarks[prefix] = value
    next_family = high_watermarks["ATF"] + 1
    next_sense = high_watermarks["ATS"] + 1
    next_variant = high_watermarks["ATV"] + 1
    family_members: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    family_keys: dict[str, str] = {}
    family_by_title: dict[str, str] = {
        title_key: row["family_id"] for title_key, row in previous_families.items()
    }
    previous_family_by_id = {
        row["family_id"]: row for row in previous_families.values()
    }
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    by_occurrence: dict[str, dict[str, str]] = {}

    for record in sorted(source_records["records"], key=lambda row: row["occurrence_id"]):
        occurrence_id = record["occurrence_id"]
        title_key = normalize_title_key(record["raw_fields"]["name"])
        family_id = family_by_title.get(title_key)
        if family_id is None:
            family_id = next_registry_id("ATF", next_family)
            next_family += 1
            family_by_title[title_key] = family_id
        family_keys[family_id] = title_key

        old_sense = previous_senses.get(occurrence_id)
        sense_id = old_sense["sense_id"] if old_sense else next_registry_id("ATS", next_sense)
        if old_sense is None:
            next_sense += 1
        old_variant = previous_variants.get(occurrence_id)
        variant_id = old_variant["variant_id"] if old_variant else next_registry_id("ATV", next_variant)
        if old_variant is None:
            next_variant += 1

        family_members[family_id].append(record)
        by_occurrence[occurrence_id] = {
            "family_id": family_id,
            "sense_id": sense_id,
            "variant_id": variant_id,
        }
        senses.append(
            {
                "sense_id": sense_id,
                "idempotency_request_sha256": stable_digest(
                    "awesome-theorems/idempotency/sense/v2",
                    {"bootstrap_occurrence_id": occurrence_id},
                ),
                "family_id": family_id,
                "bootstrap_occurrence_id": occurrence_id,
                "lifecycle": record["lifecycle"],
                "identity_state": "provisional_one_occurrence_unreviewed",
            }
        )
        variants.append(
            {
                "variant_id": variant_id,
                "idempotency_request_sha256": stable_digest(
                    "awesome-theorems/idempotency/variant/v2",
                    {"bootstrap_occurrence_id": occurrence_id},
                ),
                "sense_id": sense_id,
                "bootstrap_occurrence_id": occurrence_id,
                "lifecycle": record["lifecycle"],
                "identity_state": "provisional_one_occurrence_unreviewed",
            }
        )
    # A title correction moves the current occurrence to a new lexical family,
    # but it must not erase the prior ATF allocation.  Preserve an orphaned
    # family as a retired tombstone with its historical membership evidence.
    for title_key, row in previous_families.items():
        family_id = row["family_id"]
        family_keys.setdefault(family_id, title_key)
        family_members.setdefault(family_id, [])
    families: list[dict[str, Any]] = []
    for family_id, members in family_members.items():
        current = [member for member in members if member["lifecycle"] == "current"]
        previous_family = previous_family_by_id.get(family_id)
        display_titles = (
            sorted({member["raw_fields"]["name"] for member in members})
            if members
            else list(previous_family.get("display_titles", []))
            if previous_family is not None
            else []
        )
        member_occurrence_ids = sorted(
            member["occurrence_id"] for member in members
        )
        prior_historical_members = (
            previous_family.get(
                "historical_member_occurrence_ids",
                previous_family.get("member_occurrence_ids", []),
            )
            if previous_family is not None
            else []
        )
        historical_member_occurrence_ids = sorted(
            set(prior_historical_members) | set(member_occurrence_ids)
        )
        families.append(
            {
                "family_id": family_id,
                "idempotency_request_sha256": stable_digest(
                    "awesome-theorems/idempotency/family/v2",
                    {"lexical_title_key": family_keys[family_id]},
                ),
                "lexical_title_key": family_keys[family_id],
                "display_titles": display_titles,
                "lifecycle": "current" if current else "retired",
                "member_occurrence_ids": member_occurrence_ids,
                "historical_member_occurrence_ids": historical_member_occurrence_ids,
                "identity_state": "lexical_discovery_family_only",
                "semantic_equivalence_asserted": False,
            }
        )
    families.sort(key=lambda row: row["family_id"])
    senses.sort(key=lambda row: row["sense_id"])
    variants.sort(key=lambda row: row["variant_id"])
    return families, senses, variants, by_occurrence


def stage0_legacy_bootstrap(
    candidates: list[Candidate],
    by_occurrence: dict[str, dict[str, str]],
    snapshot_sha256: str,
) -> list[dict[str, Any]]:
    kept: dict[tuple[str, str, str, str, str, str], tuple[int, Candidate]] = {}
    for index, candidate in enumerate(candidates):
        signature = candidate.legacy_exact_signature()
        current = kept.get(signature)
        if current is None:
            kept[signature] = (index, candidate)
            continue
        kept_index, kept_candidate = current
        candidate_key = (DISCIPLINE_PRIORITY[candidate.discipline], index)
        kept_key = (DISCIPLINE_PRIORITY[kept_candidate.discipline], kept_index)
        if candidate_key < kept_key:
            kept[signature] = (index, candidate)

    survivors = [pair[1] for pair in sorted(kept.values(), key=lambda pair: pair[0])]
    counters: Counter[str] = Counter()
    aliases: list[dict[str, Any]] = []
    stage0_sha = sha256_file(STAGE0_PATH) if STAGE0_PATH.is_file() else None
    for survivor in survivors:
        prefix = DISCIPLINE_PREFIX[survivor.discipline]
        counters[prefix] += 1
        legacy_id = f"THM-{prefix}-{counters[prefix]:04d}"
        target = by_occurrence[survivor.occurrence_id]
        aliases.append(
            {
                "alias_id": legacy_id,
                "alias_kind": "legacy_stage0_snapshot_id",
                "target_variant_id": target["variant_id"],
                "target_occurrence_id": survivor.occurrence_id,
                "status": "active",
                "resolution_cardinality": 1,
                "birth_source_snapshot_sha256": snapshot_sha256,
                "legacy_stage0_sha256": stage0_sha,
                "semantic_equivalence_reviewed": False,
                "scope_note": "historical pointer to the Stage0 survivor; not proof or equivalence credit",
            }
        )
    aliases.sort(key=lambda row: row["alias_id"])
    return aliases


def load_or_bootstrap_aliases(
    previous_registry: dict[str, Any] | None,
    candidates: list[Candidate],
    by_occurrence: dict[str, dict[str, str]],
    snapshot_sha256: str,
) -> list[dict[str, Any]]:
    if previous_registry is None:
        return stage0_legacy_bootstrap(candidates, by_occurrence, snapshot_sha256)
    if previous_registry.get("schema_version") != "awesome-theorems/claim-id-registry/2.0":
        raise CatalogError("existing Claim_ID_Registry_v2.json has an unsupported schema")
    aliases = previous_registry.get("legacy_aliases")
    if not isinstance(aliases, list) or not aliases:
        raise CatalogError("existing ID registry has no immutable legacy aliases")
    aliases = [dict(alias) for alias in aliases]
    aliases.sort(key=lambda row: row["alias_id"])
    return aliases


def validate_redirects(redirects: Any, allocated_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(redirects, list):
        raise CatalogError("existing redirects are not a list")
    required = {
        "redirect_id",
        "source_id",
        "target_id",
        "relation_type",
        "review_state",
        "reviewed_at",
        "reviewer",
        "evidence_refs",
        "reason",
        "evidence_inherited",
    }
    redirect_ids: set[str] = set()
    by_source: dict[str, str] = {}
    validated: list[dict[str, Any]] = []
    for row in redirects:
        if not isinstance(row, dict) or set(row) != required:
            raise CatalogError("redirect does not match the closed reviewed-redirect schema")
        redirect_id = row["redirect_id"]
        source = row["source_id"]
        target = row["target_id"]
        evidence = row["evidence_refs"]
        if (
            re.fullmatch(r"ATD-[A-F0-9]{24}", str(redirect_id)) is None
            or redirect_id in redirect_ids
            or source in by_source
            or source not in allocated_ids
            or target not in allocated_ids
            or source == target
            or row["relation_type"] != "reviewed_merge_redirect"
            or row["review_state"] != "accepted"
            or not isinstance(row["reviewed_at"], str)
            or not row["reviewed_at"]
            or not isinstance(row["reviewer"], str)
            or not row["reviewer"]
            or not isinstance(evidence, list)
            or not evidence
            or not all(isinstance(ref, str) and ref.startswith("EVID-") for ref in evidence)
            or not isinstance(row["reason"], str)
            or not row["reason"]
            or row["evidence_inherited"] is not False
        ):
            raise CatalogError("redirect is malformed, unreviewed, dangling, or inherits evidence")
        expected_id, _ = relation_id(
            "ATD",
            "awesome-theorems/reviewed-redirect/v2",
            {"source_id": source, "target_id": target, "evidence_refs": evidence},
        )
        if redirect_id != expected_id:
            raise CatalogError("redirect ID is not content-bound to its reviewed edge")
        redirect_ids.add(redirect_id)
        by_source[source] = target
        validated.append(dict(row))

    for source, target in by_source.items():
        if target in by_source:
            raise CatalogError(
                f"redirect {source} -> {target} is not one-hop or participates in a cycle"
            )
    return sorted(validated, key=lambda row: row["redirect_id"])


def validate_splits(splits: Any, allocated_ids: set[str]) -> list[dict[str, Any]]:
    if not isinstance(splits, list):
        raise CatalogError("existing splits are not a list")
    required = {
        "split_id",
        "parent_id",
        "child_ids",
        "review_state",
        "reviewed_at",
        "reviewer",
        "evidence_refs",
        "default_child",
        "evidence_inherited",
    }
    seen_ids: set[str] = set()
    seen_parents: set[str] = set()
    validated: list[dict[str, Any]] = []
    for row in splits:
        if not isinstance(row, dict) or set(row) != required:
            raise CatalogError("split does not match the closed reviewed-split schema")
        children = row["child_ids"]
        evidence = row["evidence_refs"]
        if (
            re.fullmatch(r"ATX-[A-F0-9]{24}", str(row["split_id"])) is None
            or row["split_id"] in seen_ids
            or row["parent_id"] in seen_parents
            or row["parent_id"] not in allocated_ids
            or not isinstance(children, list)
            or len(children) < 2
            or len(children) != len(set(children))
            or not set(children) <= allocated_ids
            or row["parent_id"] in children
            or row["review_state"] != "accepted"
            or not isinstance(row["reviewed_at"], str)
            or not row["reviewed_at"]
            or not isinstance(row["reviewer"], str)
            or not row["reviewer"]
            or not isinstance(evidence, list)
            or not evidence
            or not all(isinstance(ref, str) and ref.startswith("EVID-") for ref in evidence)
            or row["default_child"] is not None
            or row["evidence_inherited"] is not False
        ):
            raise CatalogError("split is malformed, dangling, selects a default, or inherits evidence")
        expected_id, _ = relation_id(
            "ATX",
            "awesome-theorems/reviewed-split/v2",
            {
                "parent_id": row["parent_id"],
                "child_ids": sorted(children),
                "evidence_refs": evidence,
            },
        )
        if row["split_id"] != expected_id:
            raise CatalogError("split ID is not content-bound to its reviewed edge")
        seen_ids.add(row["split_id"])
        seen_parents.add(row["parent_id"])
        validated.append(dict(row))
    return sorted(validated, key=lambda row: row["split_id"])


def build_id_registry(
    snapshot: dict[str, Any],
    source_records: dict[str, Any],
    families: list[dict[str, Any]],
    senses: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    aliases: list[dict[str, Any]],
    previous_registry: dict[str, Any] | None,
) -> dict[str, Any]:
    occurrence_ids = {row["occurrence_id"] for row in source_records["records"]}
    family_ids = {row["family_id"] for row in families}
    sense_ids = {row["sense_id"] for row in senses}
    variant_ids = {row["variant_id"] for row in variants}
    allocated_ids = occurrence_ids | family_ids | sense_ids | variant_ids
    variant_by_occurrence = {
        row["bootstrap_occurrence_id"]: row["variant_id"] for row in variants
    }
    alias_ids: set[str] = set()
    for alias in aliases:
        if alias.get("alias_id") in alias_ids:
            raise CatalogError(f"duplicate legacy alias: {alias.get('alias_id')}")
        alias_ids.add(alias["alias_id"])
        if alias.get("target_variant_id") not in variant_ids:
            raise CatalogError(f"legacy alias has missing target: {alias.get('alias_id')}")
        if variant_by_occurrence.get(alias.get("target_occurrence_id")) != alias.get("target_variant_id"):
            raise CatalogError(f"legacy alias occurrence/variant target mismatch: {alias.get('alias_id')}")
        if alias.get("resolution_cardinality") != 1:
            raise CatalogError(f"legacy alias is not single-target: {alias.get('alias_id')}")

    redirects = validate_redirects(
        previous_registry.get("redirects", []) if previous_registry is not None else [],
        allocated_ids,
    )
    splits = validate_splits(
        previous_registry.get("splits", []) if previous_registry is not None else [],
        allocated_ids,
    )

    observed_high_watermarks = {
        "ATO": max((parse_registry_ordinal(value, "ATO") for value in occurrence_ids), default=0),
        "ATF": max((parse_registry_ordinal(value, "ATF") for value in family_ids), default=0),
        "ATS": max((parse_registry_ordinal(value, "ATS") for value in sense_ids), default=0),
        "ATV": max((parse_registry_ordinal(value, "ATV") for value in variant_ids), default=0),
    }
    namespace_high_watermarks = dict(observed_high_watermarks)
    if previous_registry is not None and "namespace_high_watermarks" in previous_registry:
        stored = previous_registry["namespace_high_watermarks"]
        if not isinstance(stored, dict):
            raise CatalogError("registry namespace high-water marks are malformed")
        for prefix, observed in observed_high_watermarks.items():
            value = stored.get(prefix)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise CatalogError(f"{prefix} namespace high-water mark is malformed")
            # `observed` may legitimately exceed the previous authority when
            # this generation appended new IDs.  Earlier validation in
            # build_source_records/build_allocations already proves the stored
            # mark was not below any prior allocation.
            namespace_high_watermarks[prefix] = max(value, observed)

    current_occurrences = source_records["counts"]["current_occurrences"]
    document = {
        "schema_version": "awesome-theorems/claim-id-registry/2.0",
        "catalog_schema_ref": SCHEMA_REF,
        "generated_by": "Docs/tools/generate_claim_catalog_v2.py",
        "source_snapshot_sha256": snapshot["aggregate_sha256"],
        "source_records_authority_sha256": source_records["authority_sha256"],
        "namespace_high_watermarks": namespace_high_watermarks,
        "identity_model": {
            "ATO": "immutable source occurrence",
            "ATF": "lexical discovery family; no semantic identity assertion",
            "ATS": "provisional claim sense; bootstrap is one per occurrence",
            "ATV": "provisional statement variant; bootstrap is one per occurrence",
            "legacy_alias": "single-target historical Stage0 pointer",
            "redirect": "human-reviewed append-only migration edge; none at bootstrap",
            "split": "human-reviewed one-to-many edge with no default child or inherited evidence",
        },
        "allocation_policy": {
            "append_only": True,
            "occurrence_key_version": "v3-status-stable",
            "order_independent_after_bootstrap": True,
            "source_insertion_independent_after_bootstrap": True,
            "allocation": "persisted idempotency key lookup, then namespace-local max plus one",
            "idempotency_digest": "sha256",
            "id_encodes_mutable_metadata": False,
            "collision_policy": "idempotency-key collision or duplicate registry ordinal fails closed; existing IDs are never renumbered",
            "deletion_policy": "retain the allocation and mark it retired",
            "merge_policy": "retain both IDs and add a reviewed redirect; never recycle",
            "split_policy": "retain the old ID as a reviewed umbrella/deprecated node and append new IDs; never retarget silently",
            "authority_digest": "sha256 over canonical JSON excluding authority_sha256",
        },
        "counts": {
            "occurrences_allocated": source_records["counts"]["allocated_occurrences"],
            "occurrences_current": current_occurrences,
            "families_allocated": len(families),
            "families_current": sum(row["lifecycle"] == "current" for row in families),
            "senses_allocated": len(senses),
            "senses_current": sum(row["lifecycle"] == "current" for row in senses),
            "variants_allocated": len(variants),
            "variants_current": sum(row["lifecycle"] == "current" for row in variants),
            "legacy_aliases": len(aliases),
            "redirects": len(redirects),
            "splits": len(splits),
        },
        "families": families,
        "senses": senses,
        "variants": variants,
        "legacy_aliases": aliases,
        "redirects": redirects,
        "splits": splits,
    }
    return seal_authority("awesome-theorems/claim-id-registry-authority/v2", document)


def raw_signature_from_record(record: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    fields = record["raw_fields"]
    return (
        fields["name"],
        fields["statement"],
        fields["proposer"],
        fields["proposed_time"],
        fields["importance"],
        fields["formal_status"],
    )


def build_relations(
    snapshot: dict[str, Any],
    source_records: dict[str, Any],
    by_occurrence: dict[str, dict[str, str]],
    aliases: list[dict[str, Any]],
) -> dict[str, Any]:
    records = source_records["records"]
    aliases_by_occurrence = {
        alias["target_occurrence_id"]: alias["alias_id"] for alias in aliases
    }
    exact_groups: defaultdict[tuple[str, str, str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    title_groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        exact_groups[raw_signature_from_record(record)].append(record)
        title_groups[normalize_title_key(record["raw_fields"]["name"])].append(record)

    exact_clusters: list[dict[str, Any]] = []
    for signature, members in exact_groups.items():
        if len(members) <= 1:
            continue
        signature_payload = {
            "name": signature[0],
            "statement": signature[1],
            "proposer": signature[2],
            "proposed_time": signature[3],
            "importance": signature[4],
            "formal_status": signature[5],
        }
        cluster_id, cluster_digest = relation_id(
            "ATX", "awesome-theorems/relation/legacy-exact/v2", signature_payload
        )
        members = sorted(
            members,
            key=lambda row: (
                row["birth_locator"].get("global_source_ordinal", sys.maxsize),
                row["occurrence_id"],
            ),
        )
        survivor = next(
            (member for member in members if member["occurrence_id"] in aliases_by_occurrence),
            min(
                members,
                key=lambda row: (
                    DISCIPLINE_PRIORITY[row["raw_fields"]["discipline"]],
                    row["birth_locator"].get("global_source_ordinal", sys.maxsize),
                    row["occurrence_id"],
                ),
            ),
        )
        member_rows = [
            {
                "occurrence_id": member["occurrence_id"],
                "variant_id": by_occurrence[member["occurrence_id"]]["variant_id"],
                "legacy_alias_id": aliases_by_occurrence.get(member["occurrence_id"]),
                "discipline": member["raw_fields"]["discipline"],
                "subcategory": member["raw_fields"]["subcategory"],
                "lifecycle": member["lifecycle"],
                "birth_locator": member["birth_locator"],
                "current_locator": member["current_locator"],
            }
            for member in members
        ]
        exact_clusters.append(
            {
                "cluster_id": cluster_id,
                "cluster_id_full_sha256": cluster_digest,
                "relation_type": "legacy_six_field_exact_match_candidate",
                "legacy_signature": signature_payload,
                "review_state": "unreviewed",
                "review_required": True,
                "identity_assertion": False,
                "redirect_created": False,
                "canonicalization_effect": "none",
                "member_count": len(members),
                "extra_count": len(members) - 1,
                "cross_discipline": len({member["raw_fields"]["discipline"] for member in members}) > 1,
                "legacy_survivor_occurrence_id": survivor["occurrence_id"],
                "legacy_survivor_alias_id": aliases_by_occurrence.get(survivor["occurrence_id"]),
                "members": member_rows,
                "adversarial_note": "Equal mutable metadata is a discovery signal only; members retain distinct ATS and ATV IDs until reviewed.",
            }
        )
    exact_clusters.sort(key=lambda row: row["cluster_id"])

    same_name_clusters: list[dict[str, Any]] = []
    for title_key, members in title_groups.items():
        signature_count = len({raw_signature_from_record(member) for member in members})
        if signature_count <= 1:
            continue
        cluster_id, cluster_digest = relation_id(
            "ATN", "awesome-theorems/relation/same-title/v2", {"lexical_title_key": title_key}
        )
        same_name_clusters.append(
            {
                "cluster_id": cluster_id,
                "cluster_id_full_sha256": cluster_digest,
                "relation_type": "same_normalized_title_multiple_raw_claims",
                "lexical_title_key": title_key,
                "display_titles": sorted({member["raw_fields"]["name"] for member in members}),
                "review_state": "unreviewed",
                "review_required": True,
                "semantic_relation_asserted": False,
                "raw_signature_count": signature_count,
                "member_occurrence_ids": sorted(member["occurrence_id"] for member in members),
                "member_variant_ids": sorted(
                    by_occurrence[member["occurrence_id"]]["variant_id"] for member in members
                ),
                "disciplines": sorted({member["raw_fields"]["discipline"] for member in members}),
            }
        )
    same_name_clusters.sort(key=lambda row: row["cluster_id"])

    hamming = [
        cluster
        for cluster in exact_clusters
        if normalize_title_key(cluster["legacy_signature"]["name"]) == normalize_title_key("Hamming界")
    ]
    if len(hamming) != 1:
        raise CatalogError("expected exactly one Hamming界 legacy-exact cluster")
    hamming_domains = {member["discipline"] for member in hamming[0]["members"]}
    if hamming_domains != {"数学", "计算机科学"} or len(hamming[0]["members"]) != 2:
        raise CatalogError("Hamming界 dual provenance was lost")

    aliases_by_id = {alias["alias_id"]: alias for alias in aliases}
    stage1_identity_members: list[dict[str, Any]] = []
    for legacy_id in ("THM-M-0133", "THM-M-0387"):
        alias = aliases_by_id.get(legacy_id)
        if alias is None:
            raise CatalogError(f"missing required legacy identity audit member: {legacy_id}")
        statement_path = ROOT / "Stage1_Instances" / legacy_id / "statement.json"
        lean_path = ROOT / "Stage1_Instances" / legacy_id / "Statement.lean"
        if not statement_path.is_file() or not lean_path.is_file():
            raise CatalogError(f"missing Stage1 statement identity evidence for {legacy_id}")
        statement_document = json.loads(statement_path.read_text(encoding="utf-8"))
        target = statement_document.get("canonical_formal_target", {})
        declared_fingerprint = target.get("elaborated_expression_sha256")
        stage1_identity_members.append(
            {
                "legacy_alias_id": legacy_id,
                "occurrence_id": alias["target_occurrence_id"],
                "variant_id": alias["target_variant_id"],
                "canonical_statement": statement_document.get("canonical_statement"),
                "declared_elaborated_expression_sha256": declared_fingerprint,
                "declared_fingerprint_well_formed": isinstance(declared_fingerprint, str)
                and re.fullmatch(r"[a-f0-9]{64}", declared_fingerprint) is not None,
                "formal_target": target,
                "evidence": [
                    {
                        "path": str(statement_path.relative_to(ROOT)),
                        "sha256": sha256_file(statement_path),
                    },
                    {
                        "path": str(lean_path.relative_to(ROOT)),
                        "sha256": sha256_file(lean_path),
                    },
                ],
            }
        )
    identity_payload = {
        "legacy_alias_ids": [member["legacy_alias_id"] for member in stage1_identity_members],
        "canonical_statement_sha256": [
            sha256_bytes(str(member["canonical_statement"]).encode("utf-8"))
            for member in stage1_identity_members
        ],
    }
    identity_cluster_id, identity_cluster_digest = relation_id(
        "ATQ", "awesome-theorems/relation/stage1-statement-collision/v2", identity_payload
    )
    stage1_identity_collision_candidates = [
        {
            "cluster_id": identity_cluster_id,
            "cluster_id_full_sha256": identity_cluster_digest,
            "relation_type": "stage1_statement_identity_collision_candidate",
            "review_state": "unreviewed",
            "review_required": True,
            "identity_assertion": False,
            "redirect_created": False,
            "canonical_statement_text_equal": len(
                {member["canonical_statement"] for member in stage1_identity_members}
            )
            == 1,
            "declared_formal_fingerprint_equal": len(
                {member["declared_elaborated_expression_sha256"] for member in stage1_identity_members}
            )
            == 1,
            "all_declared_fingerprints_well_formed": all(
                member["declared_fingerprint_well_formed"] for member in stage1_identity_members
            ),
            "members": stage1_identity_members,
            "required_resolution": "Human identity review must decide whether THM-M-0133 is a proof-event/history record for the THM-M-0387 claim, a distinct scoped claim, or a reviewed redirect. Current malformed/disagreeing fingerprint metadata grants no merge.",
        }
    ]

    return {
        "schema_version": "awesome-theorems/claim-relations/2.0",
        "catalog_schema_ref": SCHEMA_REF,
        "generated_by": "Docs/tools/generate_claim_catalog_v2.py",
        "source_snapshot_sha256": snapshot["aggregate_sha256"],
        "relation_policy": {
            "legacy_exact_is_identity": False,
            "same_title_is_identity": False,
            "unreviewed_relation_can_redirect": False,
            "reviewed_merge_requires_evidence": True,
            "split_merge_preserves_all_old_ids": True,
        },
        "counts": {
            "legacy_exact_clusters": len(exact_clusters),
            "legacy_exact_extra_occurrences": sum(row["extra_count"] for row in exact_clusters),
            "legacy_exact_cross_discipline_clusters": sum(row["cross_discipline"] for row in exact_clusters),
            "same_title_multiple_signature_clusters": len(same_name_clusters),
            "stage1_statement_identity_collision_candidates": len(
                stage1_identity_collision_candidates
            ),
            "reviewed_identity_relations": 0,
        },
        "legacy_exact_match_clusters": exact_clusters,
        "same_title_candidate_clusters": same_name_clusters,
        "stage1_statement_identity_collision_candidates": stage1_identity_collision_candidates,
        "reviewed_relations": [],
        "hamming_dual_provenance_audit": {
            "passed": True,
            "cluster_id": hamming[0]["cluster_id"],
            "disciplines": sorted(hamming_domains),
            "occurrence_ids": [member["occurrence_id"] for member in hamming[0]["members"]],
            "variant_ids": [member["variant_id"] for member in hamming[0]["members"]],
            "legacy_alias_ids": [
                member["legacy_alias_id"]
                for member in hamming[0]["members"]
                if member["legacy_alias_id"] is not None
            ],
            "semantic_merge_performed": False,
        },
    }


def machine_triage(fields: dict[str, str]) -> dict[str, Any]:
    name = fields["name"]
    discipline = fields["discipline"]
    status = fields["formal_status"]
    open_hint = any(token in status for token in ("未解决", "待解决", "待证明", "待研究", "开放"))
    kind = "unknown"
    confidence = 0.35
    matched_rule = "domain_generic_fallback"

    common_rules = (
        ("猜想", "conjecture"),
        ("假说", "hypothesis"),
        ("假设", "hypothesis"),
        ("引理", "lemma"),
    )
    for token, candidate_kind in common_rules:
        if token in name:
            kind = candidate_kind
            confidence = 0.74
            matched_rule = f"title_contains:{token}"
            break
    else:
        if "问题" in name or "难题" in name:
            kind = "open_problem" if open_hint else "unknown"
            confidence = 0.66 if open_hint else 0.48
            matched_rule = "title_problem_plus_raw_status_hint"
        elif discipline == "数学":
            rules = (
                ("定理", "theorem"),
                ("不等式", "unknown"),
                ("恒等式", "unknown"),
                ("公式", "unknown"),
                ("方程", "equation"),
                ("算法", "algorithm"),
                ("原理", "principle"),
            )
            kind = "unknown"
            for token, candidate_kind in rules:
                if token in name:
                    kind, confidence, matched_rule = candidate_kind, 0.68, f"title_contains:{token}"
                    break
        elif discipline == "物理":
            rules = (
                ("定律", "law"),
                ("原理", "principle"),
                ("方程", "equation"),
                ("模型", "model"),
                ("效应", "effect"),
                ("机制", "method"),
                ("理论", "framework"),
                ("关系", "empirical_relation"),
            )
            kind = "unknown"
            for token, candidate_kind in rules:
                if token in name:
                    kind, confidence, matched_rule = candidate_kind, 0.70, f"title_contains:{token}"
                    break
        elif discipline == "计算机科学":
            rules = (
                ("定理", "theorem"),
                ("算法", "algorithm"),
                ("协议", "protocol"),
                ("不可判定", "undecidability_result"),
                ("不可解", "impossibility_result"),
                ("界", "complexity_result"),
                ("构造", "method"),
            )
            kind = "unknown"
            for token, candidate_kind in rules:
                if token in name:
                    kind, confidence, matched_rule = candidate_kind, 0.68, f"title_contains:{token}"
                    break

    return {
        "value": kind,
        "assessment_method": "machine_triage",
        "confidence": round(confidence, 2),
        "review_required": True,
        "matched_rule": matched_rule,
        "status_label_used_only_as_hint": open_hint,
    }


def repair_rows(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list):
        return [row for row in document if isinstance(row, dict)]
    if not isinstance(document, dict):
        return []
    for key in ("reviews", "claim_reviews", "repairs", "records"):
        value = document.get(key)
        if isinstance(value, list):
            return [row for row in value if isinstance(row, dict)]
    return []


def load_repair_overlays(
    variant_ids: set[str], aliases: list[dict[str, Any]], by_occurrence: dict[str, dict[str, str]]
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], str | None]:
    if not REPAIRS_DIR.is_dir():
        return {}, [], None
    paths = sorted(REPAIRS_DIR.glob("*.json"))
    if not paths:
        return {}, [], None
    alias_targets = {alias["alias_id"]: alias["target_variant_id"] for alias in aliases}
    occurrence_targets = {
        occurrence_id: allocation["variant_id"] for occurrence_id, allocation in by_occurrence.items()
    }
    overlays: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    manifest: list[dict[str, Any]] = []
    allowed_patch_keys = {
        "canonical_title",
        "claim_kind",
        "exact_statement",
        "human_mathematical_status",
        "external_formal_status",
        "repository_status",
        "benchmark_status",
        "provenance",
        "license",
        "notes",
    }
    for path in paths:
        raw = path.read_bytes()
        document = json.loads(raw)
        rows = repair_rows(document)
        manifest.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256_bytes(raw),
                "row_count": len(rows),
            }
        )
        for index, row in enumerate(rows):
            target = row.get("target_id") or row.get("variant_id") or row.get("legacy_id") or row.get("occurrence_id")
            if target in variant_ids:
                variant_id = target
            elif target in alias_targets:
                variant_id = alias_targets[target]
            elif target in occurrence_targets:
                variant_id = occurrence_targets[target]
            else:
                raise CatalogError(f"unknown repair target {target!r} in {path.relative_to(ROOT)}")
            patch = row.get("patch", {})
            if not isinstance(patch, dict):
                raise CatalogError(f"repair patch is not an object in {path.relative_to(ROOT)}")
            unknown = set(patch) - allowed_patch_keys
            if unknown:
                raise CatalogError(f"unsafe repair keys {sorted(unknown)} in {path.relative_to(ROOT)}")
            review = row.get("review") if isinstance(row.get("review"), dict) else {}
            review = dict(review)
            for field_name in ("reviewer", "reviewed_at", "evidence", "decision", "confidence", "rationale"):
                if field_name not in review and field_name in row:
                    review[field_name] = row[field_name]
            reviewer = review.get("reviewer")
            reviewed_at = review.get("reviewed_at")
            evidence = review.get("evidence")
            decision = review.get("decision")
            qualified = (
                decision == "accepted"
                and isinstance(reviewer, str)
                and bool(reviewer.strip())
                and isinstance(reviewed_at, str)
                and bool(reviewed_at.strip())
                and isinstance(evidence, list)
                and bool(evidence)
                and all(
                    isinstance(ref, str) and re.fullmatch(r"EVID-[A-Za-z0-9._:-]+", ref)
                    for ref in evidence
                )
            )
            overlays[variant_id].append(
                {
                    "source": str(path.relative_to(ROOT)),
                    "row_index": index,
                    "review": review,
                    "patch": patch,
                    "qualified_human_review": qualified,
                    "review_required": not qualified,
                    "application": "applied_as_human_review" if qualified else "proposal_only_not_applied",
                }
            )
    manifest_digest = stable_digest("awesome-theorems/repair-manifest/v2", manifest)
    return dict(overlays), manifest, manifest_digest


def discipline_tags(records: list[dict[str, Any]]) -> list[str]:
    mapping = {
        "数学": "mathematics",
        "物理": "physics",
        "计算机科学": "computer_science",
    }
    tags = {mapping.get(record["raw_fields"]["discipline"], "other") for record in records}
    if len(tags) > 1:
        tags.add("cross_domain")
    return sorted(tags)


def exact_statement_surface(text: str | None, completeness: str = "source_prose") -> dict[str, Any]:
    return {
        "completeness": completeness,
        "language": "zh-Hans",
        "natural_language": text,
        "binders": [],
        "hypotheses": [],
        "conclusion": None,
        "scope": None,
        "formal_surfaces": [],
        "statement_sha256": sha256_bytes(text.encode("utf-8")) if text is not None else None,
    }


def unknown_status_axes(scope_note: str) -> dict[str, Any]:
    return {
        "human_truth": {
            "status": "unknown",
            "answer_polarity": "unknown",
            "as_of": None,
            "resolved_at": None,
            "scope_note": scope_note,
            "source_refs": [],
            "refutation": None,
            "independence": None,
        },
        "empirical": {
            "status": "unknown",
            "as_of": None,
            "regime_ref": None,
            "observable": None,
            "uncertainty_or_error_model": None,
            "data_refs": [],
            "source_refs": [],
        },
        "external_formalization": {
            "status": "unknown",
            "as_of": None,
            "source_refs": [],
            "artifacts": [],
        },
        "repo_integration": {
            "status": "unknown",
            "as_of": None,
            "repository_revision": None,
            "evidence_refs": [],
            "receipt_refs": [],
        },
    }


def raw_status_rows(
    records: list[dict[str, Any]], source_blob_by_path: dict[str, str]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        source_path = record["birth_locator"]["path"]
        for field_name in ("formal_status", "importance"):
            rows.append(
                {
                    "occurrence_id": record["occurrence_id"],
                    "field_name": field_name,
                    "raw_value": record["raw_fields"][field_name],
                    "raw_language": "zh-Hans",
                    "source_blob_sha256": source_blob_by_path[source_path],
                }
            )
    return rows


def base_schema_record(
    *,
    record_type: str,
    record_id: str,
    preferred_label: str,
    member_sources: list[dict[str, Any]],
    idempotency_request_sha256: str,
    registry_revision: str,
    legacy_ids: list[str],
    current_kind: str,
    atomicity: str,
    truth_apt: str,
    statement: dict[str, Any],
    confidence: float,
    confidence_method: str,
    rationale: str,
    relations: list[dict[str, Any]],
    family_split_group: str | None,
    source_blob_by_path: dict[str, str],
) -> dict[str, Any]:
    lifecycle = "active" if any(row["lifecycle"] == "current" for row in member_sources) else "retired"
    labels = sorted({row["raw_fields"]["name"] for row in member_sources})
    return {
        "schema_version": "claim-record/2.0",
        "record_type": record_type,
        "record_id": record_id,
        "registry_revision": registry_revision,
        "lifecycle": lifecycle,
        "identity": {
            "preferred_label": preferred_label,
            "labels": [
                {"text": label, "language": "zh-Hans", "role": "source_raw"}
                for label in labels
            ],
            "legacy_ids": sorted(legacy_ids),
            "discipline_tags": discipline_tags(member_sources),
            "allocation_basis": "append_only_registry",
            "idempotency_request_sha256": idempotency_request_sha256,
            "redirect_to": None,
            "split_children": [],
        },
        "claim_kind": {
            "historical_kind": "unreviewed",
            "current_kind": current_kind,
            "atomicity": atomicity,
            "truth_apt": truth_apt,
        },
        "exact_statement": statement,
        "source_status_raw": raw_status_rows(member_sources, source_blob_by_path),
        "statuses": unknown_status_axes(
            "Unreviewed source metadata was preserved verbatim and was not interpreted as truth or proof evidence."
        ),
        "conditionality": {
            "mode": "unknown",
            "assumptions": [],
            "consequent_status_note": "Conditionality has not been reviewed.",
        },
        "historical_status": {
            "classification": "unreviewed",
            "historical_names": [],
            "proposed_at": None,
            "resolved_at": None,
            "resolution_kind": "unknown",
            "source_refs": [],
        },
        "provenance": {
            "status": "missing",
            "evidence_refs": [],
        },
        "license": {
            "status": "unknown",
            "spdx_expression": None,
            "redistribution_scope": "License and redistribution scope have not been reviewed.",
            "evidence_refs": [],
        },
        "status_history": [],
        "classification_review": {
            "status": "machine_triage",
            "reviewed_at": None,
            "reviewer_role": None,
            "confidence": confidence,
            "confidence_method": confidence_method,
            "rationale": f"review_required=true; {rationale}",
            "source_refs": [],
        },
        "benchmark_eligibility": {
            "status": "not_evaluated",
            "assessed_as_of": None,
            "policy_version": "catalog-bootstrap-v2/unreleased",
            "review_ref": None,
            "allowed_tracks": [],
            "blocking_reasons": [
                "identity_unresolved",
                "kind_unreviewed",
                "statement_inexact",
                "scope_incomplete",
                "provenance_incomplete",
                "rights_unresolved",
                "contamination_unresolved",
            ],
            "family_split_group": family_split_group,
            "contamination_status": "unknown",
        },
        "relations": relations,
        "created_at": BOOTSTRAP_TIMESTAMP,
        "updated_at": BOOTSTRAP_TIMESTAMP,
    }


def relation_edge(relation_type: str, target_id: str) -> dict[str, Any]:
    return {
        "relation_type": relation_type,
        "target_id": target_id,
        "review_status": "machine_candidate",
        "source_refs": [],
    }


def apply_reviewed_schema_overlays(
    record: dict[str, Any], overlays: list[dict[str, Any]]
) -> None:
    """Apply only qualified, schema-bounded review fields.

    Unqualified repairs remain visible in the catalog-level overlay audit but
    cannot affect a schema record.  Raw status rows and registry identity are
    never overwritten.
    """

    allowed_kinds = {
        "unknown", "theorem", "lemma", "conjecture", "hypothesis", "open_problem",
        "axiom", "thesis", "definition", "equation", "model", "law", "principle",
        "effect", "empirical_relation", "observation", "algorithm", "protocol",
        "complexity_result", "impossibility_result", "undecidability_result",
        "proof_event", "method", "framework", "device", "dataset", "claim_family",
        "claim_sense", "source_occurrence", "aggregate", "non_claim",
    }
    for overlay in overlays:
        if not overlay["qualified_human_review"]:
            continue
        patch = overlay["patch"]
        if isinstance(patch.get("canonical_title"), str) and patch["canonical_title"].strip():
            record["identity"]["preferred_label"] = patch["canonical_title"].strip()
        claim_kind = patch.get("claim_kind")
        if claim_kind is not None:
            if claim_kind not in allowed_kinds:
                raise CatalogError(f"reviewed claim_kind is outside schema: {claim_kind!r}")
            record["claim_kind"]["current_kind"] = claim_kind
        exact_statement = patch.get("exact_statement")
        if isinstance(exact_statement, str) and exact_statement.strip():
            record["exact_statement"] = exact_statement_surface(
                exact_statement.strip(), "normalized_prose"
            )
        elif isinstance(exact_statement, dict):
            record["exact_statement"] = exact_statement
        axis_patches = {
            "human_mathematical_status": ("statuses", "human_truth"),
            "external_formal_status": ("statuses", "external_formalization"),
            "repository_status": ("statuses", "repo_integration"),
            "benchmark_status": ("benchmark_eligibility", None),
            "provenance": ("provenance", None),
            "license": ("license", None),
        }
        for patch_key, (container, child) in axis_patches.items():
            value = patch.get(patch_key)
            if value is None:
                continue
            if not isinstance(value, dict):
                raise CatalogError(
                    f"reviewed {patch_key} must be a complete schema object in {overlay['source']}"
                )
            if child is None:
                record[container] = value
            else:
                record[container][child] = value
        review = overlay["review"]
        reviewed_at = review.get("reviewed_at")
        if not isinstance(reviewed_at, str) or not reviewed_at:
            raise CatalogError(
                f"qualified repair {overlay['source']} row {overlay['row_index']} lacks reviewed_at"
            )
        record["classification_review"] = {
            "status": "human_reviewed",
            "reviewed_at": reviewed_at,
            "reviewer_role": str(review.get("reviewer")),
            "confidence": float(review.get("confidence", 1.0)),
            "confidence_method": "manual_review",
            "rationale": str(review.get("rationale", "accepted repair overlay")),
            "source_refs": [
                ref for ref in review.get("evidence", [])
                if isinstance(ref, str) and re.fullmatch(r"EVID-[A-Za-z0-9._:-]+", ref)
            ],
        }
        if isinstance(patch.get("notes"), str) and patch["notes"].strip():
            record["classification_review"]["rationale"] += "; " + patch["notes"].strip()


def build_catalog(
    snapshot: dict[str, Any],
    source_records: dict[str, Any],
    registry: dict[str, Any],
    relations: dict[str, Any],
    by_occurrence: dict[str, dict[str, str]],
) -> dict[str, Any]:
    records_by_occurrence = {record["occurrence_id"]: record for record in source_records["records"]}
    aliases_by_variant: defaultdict[str, list[str]] = defaultdict(list)
    for alias in registry["legacy_aliases"]:
        aliases_by_variant[alias["target_variant_id"]].append(alias["alias_id"])
    overlays, repair_manifest, repair_manifest_sha = load_repair_overlays(
        {row["variant_id"] for row in registry["variants"]},
        registry["legacy_aliases"],
        by_occurrence,
    )
    source_blob_by_path = {
        row["path"]: row["sha256"] for row in snapshot["files"]
    }
    registry_revision = "sha256:" + sha256_bytes(pretty_json(registry).encode("utf-8"))
    aliases_by_occurrence = {
        alias["target_occurrence_id"]: alias["alias_id"] for alias in registry["legacy_aliases"]
    }
    family_allocations = {row["family_id"]: row for row in registry["families"]}
    sense_allocations = {row["sense_id"]: row for row in registry["senses"]}

    schema_records: list[dict[str, Any]] = []
    for occurrence_id in sorted(records_by_occurrence):
        source = records_by_occurrence[occurrence_id]
        ids = by_occurrence[occurrence_id]
        fields = source["raw_fields"]
        locator = source["current_locator"] or source["birth_locator"]
        ato = base_schema_record(
            record_type="ATO",
            record_id=occurrence_id,
            preferred_label=fields["name"],
            member_sources=[source],
            idempotency_request_sha256=source["idempotency_request_sha256"],
            registry_revision=registry_revision,
            legacy_ids=[aliases_by_occurrence[occurrence_id]] if occurrence_id in aliases_by_occurrence else [],
            current_kind="source_occurrence",
            atomicity="entity",
            truth_apt="no",
            statement=exact_statement_surface(fields["statement"]),
            confidence=1.0,
            confidence_method="schema_heuristic",
            rationale="The parser structurally identified one source occurrence; semantic identity remains unreviewed.",
            relations=[
                relation_edge("family_member", ids["family_id"]),
                relation_edge("source_occurrence_of", ids["variant_id"]),
                relation_edge("needs_review", ids["sense_id"]),
            ],
            family_split_group=ids["family_id"],
            source_blob_by_path=source_blob_by_path,
        )
        ato["occurrence"] = {
            "source_path": locator["path"],
            "source_blob_sha256": source_blob_by_path[locator["path"]],
            "raw_block_sha256": locator["raw_block_sha256"],
            "byte_start": locator["byte_start"],
            "byte_end": locator["byte_end_exclusive"],
            "section_path": locator["raw_section_path"],
            "source_ordinal": locator["source_record_ordinal"],
            "raw_name": fields["name"],
            "raw_statement": fields["statement"],
            "candidate_record_ids": [ids["family_id"], ids["sense_id"], ids["variant_id"]],
        }
        schema_records.append(ato)

    for family_id in sorted(family_allocations):
        allocation = family_allocations[family_id]
        members = [
            records_by_occurrence[occurrence_id]
            for occurrence_id in allocation["member_occurrence_ids"]
        ]
        evidence_members = members or [
            records_by_occurrence[occurrence_id]
            for occurrence_id in allocation.get(
                "historical_member_occurrence_ids", []
            )
        ]
        member_senses = sorted(by_occurrence[row["occurrence_id"]]["sense_id"] for row in members)
        legacy_ids = sorted(
            alias for row in evidence_members
            if (alias := aliases_by_occurrence.get(row["occurrence_id"])) is not None
        )
        atf = base_schema_record(
            record_type="ATF",
            record_id=family_id,
            preferred_label=allocation["display_titles"][0],
            member_sources=evidence_members,
            idempotency_request_sha256=allocation["idempotency_request_sha256"],
            registry_revision=registry_revision,
            legacy_ids=legacy_ids,
            current_kind="claim_family",
            atomicity="aggregate",
            truth_apt="unknown",
            statement=exact_statement_surface(None, "not_applicable"),
            confidence=1.0,
            confidence_method="schema_heuristic",
            rationale="Lexical normalization formed a discovery family only; member equivalence is not asserted.",
            relations=[relation_edge("family_member", sense_id) for sense_id in member_senses],
            family_split_group=family_id,
            source_blob_by_path=source_blob_by_path,
        )
        atf["lifecycle"] = (
            "active" if allocation["lifecycle"] == "current" else "retired"
        )
        atf["family"] = {
            "member_ids": member_senses,
            "leakage_component_key": family_id,
            "scope_note": "Lexical-title family used to prevent silent loss and benchmark leakage; it is not a semantic equivalence class.",
            "identity_rationale": "Machine bootstrap grouped Unicode-NFKC and whitespace-normalized equal titles; human review is required.",
        }
        schema_records.append(atf)

    for sense_id in sorted(sense_allocations):
        allocation = sense_allocations[sense_id]
        occurrence_id = allocation["bootstrap_occurrence_id"]
        source = records_by_occurrence[occurrence_id]
        ids = by_occurrence[occurrence_id]
        fields = source["raw_fields"]
        ats = base_schema_record(
            record_type="ATS",
            record_id=sense_id,
            preferred_label=fields["name"],
            member_sources=[source],
            idempotency_request_sha256=allocation["idempotency_request_sha256"],
            registry_revision=registry_revision,
            legacy_ids=[aliases_by_occurrence[occurrence_id]] if occurrence_id in aliases_by_occurrence else [],
            current_kind="claim_sense",
            atomicity="unknown",
            truth_apt="unknown",
            statement=exact_statement_surface(fields["statement"]),
            confidence=1.0,
            confidence_method="schema_heuristic",
            rationale="One provisional sense was allocated per source occurrence; same-name and equivalence review remains open.",
            relations=[
                relation_edge("family_member", ids["family_id"]),
                relation_edge("sense_member", ids["variant_id"]),
                relation_edge("needs_review", occurrence_id),
            ],
            family_split_group=ids["family_id"],
            source_blob_by_path=source_blob_by_path,
        )
        ats["sense"] = {
            "family_id": ids["family_id"],
            "disambiguator": f"unreviewed source occurrence {occurrence_id} in {fields['subcategory']}",
            "member_variant_ids": [ids["variant_id"]],
            "same_name_collision_reviewed": False,
        }
        schema_records.append(ats)

    for allocation in sorted(registry["variants"], key=lambda row: row["variant_id"]):
        occurrence_id = allocation["bootstrap_occurrence_id"]
        source = records_by_occurrence[occurrence_id]
        ids = by_occurrence[occurrence_id]
        fields = source["raw_fields"]
        triage = machine_triage(fields)
        atv = base_schema_record(
            record_type="ATV",
            record_id=allocation["variant_id"],
            preferred_label=fields["name"],
            member_sources=[source],
            idempotency_request_sha256=allocation["idempotency_request_sha256"],
            registry_revision=registry_revision,
            legacy_ids=aliases_by_variant[allocation["variant_id"]],
            current_kind=triage["value"],
            atomicity="unknown",
            truth_apt="unknown",
            statement=exact_statement_surface(fields["statement"]),
            confidence=triage["confidence"],
            confidence_method="lexical_heuristic",
            rationale=f"{triage['matched_rule']}; raw status was used only as a non-authoritative hint={triage['status_label_used_only_as_hint']}.",
            relations=[
                relation_edge("family_member", ids["family_id"]),
                relation_edge("sense_member", ids["sense_id"]),
                relation_edge("source_occurrence_of", occurrence_id),
            ],
            family_split_group=ids["family_id"],
            source_blob_by_path=source_blob_by_path,
        )
        atv["variant"] = {
            "sense_id": ids["sense_id"],
            "source_occurrence_ids": [occurrence_id],
            "variant_revision": 1,
            "supersedes_variant_ids": [],
        }
        apply_reviewed_schema_overlays(atv, overlays.get(allocation["variant_id"], []))
        schema_records.append(atv)

    prefix_order = {"ATO": 0, "ATF": 1, "ATS": 2, "ATV": 3}
    schema_records.sort(key=lambda row: (prefix_order[row["record_type"]], row["record_id"]))

    return {
        "schema_version": "awesome-theorems/claim-catalog/2.0",
        "catalog_schema_ref": SCHEMA_REF,
        "generated_by": "Docs/tools/generate_claim_catalog_v2.py",
        "source_snapshot_sha256": snapshot["aggregate_sha256"],
        "authoritative_inputs": {
            "source_records": "Docs/catalog/Source_Records_v2.json",
            "id_registry": "Docs/catalog/Claim_ID_Registry_v2.json",
            "relations": "Docs/catalog/Claim_Relations_v2.json",
            "repairs": repair_manifest,
            "repair_manifest_sha256": repair_manifest_sha,
        },
        "trust_boundary": {
            "source_statuses_preserved_verbatim": True,
            "source_statuses_grant_formal_proof_credit": False,
            "machine_classification_is_triage_only": True,
            "every_machine_classification_requires_review": True,
            "legacy_exact_clusters_are_unreviewed_relations_only": True,
            "license_is_independent_from_provenance": True,
            "unknown_license_blocks_benchmark_derivation": True,
        },
        "counts": {
            "source_occurrences_allocated": source_records["counts"]["allocated_occurrences"],
            "source_occurrences_current": source_records["counts"]["current_occurrences"],
            "families_allocated": len(registry["families"]),
            "families_current": sum(row["lifecycle"] == "current" for row in registry["families"]),
            "senses_allocated": len(registry["senses"]),
            "senses_current": sum(row["lifecycle"] == "current" for row in registry["senses"]),
            "variants_allocated": len(registry["variants"]),
            "variants_current": sum(row["lifecycle"] == "current" for row in registry["variants"]),
            "schema_records": len(schema_records),
            "legacy_aliases": len(registry["legacy_aliases"]),
            "legacy_exact_clusters": relations["counts"]["legacy_exact_clusters"],
            "legacy_exact_extra_occurrences": relations["counts"]["legacy_exact_extra_occurrences"],
            "qualified_human_repair_overlays": sum(
                overlay["qualified_human_review"]
                for rows in overlays.values()
                for overlay in rows
            ),
        },
        "registry_revision": registry_revision,
        "record_schema": {
            "path": SCHEMA_REF,
            "sha256": sha256_file(ROOT / SCHEMA_REF) if (ROOT / SCHEMA_REF).is_file() else None,
            "validation_scope": "every element of records",
        },
        "repair_overlay_audit": [
            {"variant_id": variant_id, "overlays": rows}
            for variant_id, rows in sorted(overlays.items())
        ],
        "records": schema_records,
    }


def markdown_escape(value: Any) -> str:
    if value is None or value == "":
        return "—"
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_catalog_markdown(
    catalog: dict[str, Any], registry: dict[str, Any], relations: dict[str, Any]
) -> str:
    counts = catalog["counts"]
    ato_by_id = {
        row["record_id"]: row for row in catalog["records"] if row["record_type"] == "ATO"
    }
    sense_family = {
        row["record_id"]: row["sense"]["family_id"]
        for row in catalog["records"]
        if row["record_type"] == "ATS"
    }
    variant_records = [row for row in catalog["records"] if row["record_type"] == "ATV"]
    lines = [
        "# Claim Catalog v2",
        "",
        "> Generated by `Docs/tools/generate_claim_catalog_v2.py`. Do not edit this projection by hand.",
        "",
        "## Trust boundary",
        "",
        "All source labels, including `已验证`, are untrusted raw metadata. They grant no mathematical-proof, external-formal-proof, repository-replay, or benchmark-release credit. Every automatic claim-kind label is `machine_triage`, carries a confidence value, and remains `review_required`.",
        "",
        "The bootstrap keeps one ATS and one ATV per ATO. Historical six-field equality appears only as an unreviewed relation: it creates no semantic merge, alias, redirect, or shared proof credit.",
        "",
        "Bibliographic provenance and license are independent top-level contracts. An unknown license retains `rights_unresolved` and cannot authorize benchmark task derivation.",
        "",
        "## Counts",
        "",
        "| Surface | Count |",
        "|---|---:|",
        f"| Current source occurrences (ATO) | {counts['source_occurrences_current']} |",
        f"| Lexical families (ATF) | {counts['families_current']} |",
        f"| Provisional senses (ATS) | {counts['senses_current']} |",
        f"| Provisional variants (ATV) | {counts['variants_current']} |",
        f"| Historical THM aliases | {counts['legacy_aliases']} |",
        f"| Legacy exact-match clusters | {counts['legacy_exact_clusters']} |",
        f"| Extra occurrences retained in those clusters | {counts['legacy_exact_extra_occurrences']} |",
        "",
        "## Identity model",
        "",
        "- `ATO`: immutable source occurrence with an immutable birth locator and refreshable current locator.",
        "- `ATF`: lexical discovery family; common spelling does not assert a common claim.",
        "- `ATS`: provisional sense; bootstrap allocation is one per occurrence.",
        "- `ATV`: provisional statement variant; bootstrap allocation is one per occurrence.",
        "- `THM-*`: immutable single-target alias to a Stage0 survivor, not a truth or equivalence assertion.",
        "",
        "## Hamming dual-provenance audit",
        "",
    ]
    hamming = relations["hamming_dual_provenance_audit"]
    lines.extend(
        [
            f"The audit passed: `{hamming['cluster_id']}` retains distinct mathematics and computer-science occurrences (`{'`, `'.join(hamming['occurrence_ids'])}`), with no semantic merge.",
            "",
            "## THM-M-0133 / THM-M-0387 identity collision",
            "",
        ]
    )
    identity_collision = relations["stage1_statement_identity_collision_candidates"][0]
    lines.extend(
        [
            f"`{identity_collision['cluster_id']}` records the equal Stage1 canonical statement text as an unreviewed collision candidate. Declared formal fingerprints are equal: `{str(identity_collision['declared_formal_fingerprint_equal']).lower()}`; all are well formed: `{str(identity_collision['all_declared_fingerprints_well_formed']).lower()}`. No alias or redirect was created.",
            "",
            "## Legacy exact-match candidate clusters",
            "",
            "| Cluster | Name | Members | Extras | Cross-discipline | Review |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    for cluster in relations["legacy_exact_match_clusters"]:
        lines.append(
            "| {cluster} | {name} | {members} | {extras} | {cross} | unreviewed |".format(
                cluster=cluster["cluster_id"],
                name=markdown_escape(cluster["legacy_signature"]["name"]),
                members=cluster["member_count"],
                extras=cluster["extra_count"],
                cross="yes" if cluster["cross_discipline"] else "no",
            )
        )

    lines.extend(
        [
            "",
            "## Complete provisional variant projection",
            "",
            "| ATV | Legacy | ATO | ATF | ATS | Title | Discipline | Subcategory | Machine triage | Confidence | Raw status |",
            "|---|---|---|---|---|---|---|---|---|---:|---|",
        ]
    )
    for variant in variant_records:
        occurrence_id = variant["variant"]["source_occurrence_ids"][0]
        occurrence = ato_by_id[occurrence_id]
        classification = variant["classification_review"]
        raw_status = next(
            row["raw_value"]
            for row in variant["source_status_raw"]
            if row["field_name"] == "formal_status"
        )
        lines.append(
            "| {variant_id} | {legacy} | {occurrence} | {family} | {sense} | {title} | {discipline} | {subcategory} | {kind} | {confidence:.2f} | {status} |".format(
                variant_id=variant["record_id"],
                legacy=",".join(variant["identity"]["legacy_ids"]) or "—",
                occurrence=occurrence_id,
                family=sense_family[variant["variant"]["sense_id"]],
                sense=variant["variant"]["sense_id"],
                title=markdown_escape(variant["identity"]["preferred_label"]),
                discipline=markdown_escape(",".join(variant["identity"]["discipline_tags"])),
                subcategory=markdown_escape(" / ".join(occurrence["occurrence"]["section_path"])),
                kind=markdown_escape(variant["claim_kind"]["current_kind"]),
                confidence=float(classification.get("confidence", 1.0)),
                status=markdown_escape(raw_status),
            )
        )
    lines.extend(
        [
            "",
            "## Human repair overlays",
            "",
            "Optional `Docs/catalog/repairs/*.json` files may contain a `reviews` (or `claim_reviews`, `repairs`, `records`) array. A row targets an ATV, ATO, or legacy ID and supplies a `patch`. Semantic fields are applied only when the row records `decision: accepted`, a nonempty reviewer, and nonempty evidence; otherwise it is retained as a proposal requiring review. Raw source fields and IDs are never overwritten.",
            "",
        ]
    )
    return "\n".join(lines)


def validate_bootstrap(
    candidates: list[Candidate],
    source_records: dict[str, Any],
    registry: dict[str, Any],
    relations: dict[str, Any],
    had_previous_registry: bool,
) -> None:
    if not had_previous_registry:
        checks = {
            "source occurrences": (len(candidates), BOOTSTRAP_OCCURRENCES),
            "legacy aliases": (len(registry["legacy_aliases"]), BOOTSTRAP_LEGACY_ALIASES),
            "legacy exact clusters": (
                relations["counts"]["legacy_exact_clusters"],
                BOOTSTRAP_EXACT_CLUSTERS,
            ),
            "legacy exact extras": (
                relations["counts"]["legacy_exact_extra_occurrences"],
                BOOTSTRAP_EXACT_EXTRAS,
            ),
        }
        failures = [f"{name}: got {actual}, expected {expected}" for name, (actual, expected) in checks.items() if actual != expected]
        if failures:
            raise CatalogError("bootstrap population mismatch: " + "; ".join(failures))
    if len({row["occurrence_id"] for row in source_records["records"]}) != len(source_records["records"]):
        raise CatalogError("duplicate ATO IDs")
    if len({row["alias_id"] for row in registry["legacy_aliases"]}) != len(registry["legacy_aliases"]):
        raise CatalogError("duplicate legacy aliases")
    if any(cluster["review_state"] != "unreviewed" or cluster["identity_assertion"] for cluster in relations["legacy_exact_match_clusters"]):
        raise CatalogError("legacy exact equality was upgraded beyond an unreviewed relation")


def validate_catalog_records_against_schema(catalog: dict[str, Any]) -> None:
    schema_path = ROOT / SCHEMA_REF
    if not schema_path.is_file():
        raise CatalogError(f"record schema is missing: {SCHEMA_REF}")
    try:
        import jsonschema
    except ImportError as error:  # pragma: no cover - release environment gate
        raise CatalogError("python package jsonschema is required for catalog generation") from error
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    type_definitions = {"ATO": "ato_record", "ATF": "atf_record", "ATS": "ats_record", "ATV": "atv_record"}
    validators = {
        record_type: jsonschema.Draft202012Validator(
            {
                "$schema": schema["$schema"],
                "$id": f"urn:awesome-theorems:schema:claim-record:v2:{record_type.lower()}",
                "$defs": schema["$defs"],
                "$ref": f"#/$defs/{definition}",
            },
            format_checker=jsonschema.FormatChecker(),
        )
        for record_type, definition in type_definitions.items()
    }
    for index, record in enumerate(catalog["records"]):
        validator = validators.get(record.get("record_type"))
        if validator is None:
            raise CatalogError(f"unknown catalog record type at index {index}")
        errors = sorted(validator.iter_errors(record), key=lambda error: list(error.absolute_path))
        if errors:
            first = errors[0]
            location = "/".join(str(part) for part in first.absolute_path) or "<root>"
            raise CatalogError(
                f"schema-invalid catalog record {index} {record.get('record_id')} at {location}: {first.message}"
            )


def build_all() -> dict[Path, str]:
    snapshot = source_snapshot()
    candidates = parse_all_sources()
    raw_previous_source_records = read_json_if_present(SOURCE_RECORDS_PATH)
    raw_previous_registry = read_json_if_present(ID_REGISTRY_PATH)
    previous_source_records = compatible_previous_source_records(raw_previous_source_records)
    previous_registry = compatible_previous_registry(raw_previous_registry)
    if (previous_source_records is None) != (previous_registry is None):
        raise CatalogError(
            "append-only Source_Records and Claim_ID_Registry authorities must bootstrap or migrate together"
        )
    if previous_source_records is not None and previous_registry is not None:
        source_sealed = "authority_sha256" in previous_source_records
        registry_sealed = "authority_sha256" in previous_registry
        if source_sealed != registry_sealed:
            raise CatalogError("source and registry authorities cannot mix sealed and unsealed revisions")
        if source_sealed and (
            previous_registry.get("source_records_authority_sha256")
            != previous_source_records["authority_sha256"]
        ):
            raise CatalogError("registry is not bound to the current source-record authority revision")
    source_records = build_source_records(candidates, snapshot, previous_source_records)
    families, senses, variants, by_occurrence = build_allocations(source_records, previous_registry)
    aliases = load_or_bootstrap_aliases(
        previous_registry,
        candidates,
        by_occurrence,
        snapshot["aggregate_sha256"],
    )
    registry = build_id_registry(
        snapshot,
        source_records,
        families,
        senses,
        variants,
        aliases,
        previous_registry,
    )
    relations = build_relations(snapshot, source_records, by_occurrence, aliases)
    catalog = build_catalog(snapshot, source_records, registry, relations, by_occurrence)
    validate_catalog_records_against_schema(catalog)
    markdown = render_catalog_markdown(catalog, registry, relations)
    validate_bootstrap(
        candidates,
        source_records,
        registry,
        relations,
        previous_registry is not None,
    )
    return {
        SOURCE_RECORDS_PATH: pretty_json(source_records),
        ID_REGISTRY_PATH: pretty_json(registry),
        RELATIONS_PATH: pretty_json(relations),
        CATALOG_JSON_PATH: pretty_json(catalog),
        CATALOG_MD_PATH: markdown,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated outputs differ; do not write",
    )
    args = parser.parse_args(argv)
    outputs = build_all()
    if args.check:
        stale = [path for path, text in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != text]
        if stale:
            for path in stale:
                print(f"STALE {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print(
            f"PASS catalog deterministic check: {len(outputs)} outputs, "
            f"sha256={sha256_bytes(canonical_json_bytes({str(path.relative_to(ROOT)): sha256_bytes(text.encode('utf-8')) for path, text in outputs.items()}))}"
        )
        return 0

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
        print(f"WROTE {path.relative_to(ROOT)} sha256={sha256_bytes(text.encode('utf-8'))}")
    catalog = json.loads(outputs[CATALOG_JSON_PATH])
    counts = catalog["counts"]
    print(
        "COUNTS "
        f"ATO={counts['source_occurrences_current']} "
        f"ATF={counts['families_current']} "
        f"ATS={counts['senses_current']} "
        f"ATV={counts['variants_current']} "
        f"legacy_aliases={counts['legacy_aliases']} "
        f"exact_clusters={counts['legacy_exact_clusters']} "
        f"exact_extras={counts['legacy_exact_extra_occurrences']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CatalogError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
