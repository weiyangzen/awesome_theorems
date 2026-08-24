#!/usr/bin/env python3
"""Deterministic Stage5.1 subject-classification overlay builder.

This module is deliberately a *pure materializer*: it reads frozen Stage5
catalog/pool inputs plus a caller-pinned MSC CSV and returns taxonomy nodes and
one assignment for every Stage5.1 execution member.  It never writes release
artifacts and never upgrades a heuristic to an accepted classification.

Accepted classifications are limited to the depth explicitly asserted by a
source record (for example an exact two-digit AMS class remains two-digit).
Module roots, titles, statements and local rules produce candidates only.  In
particular, a five-character MSC leaf is never inferred from a broader code.

The public entry point is :func:`build_stage5_1_subject_classification`.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import tarfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "awesome-theorems/stage5.1-subject-classification-bundle/1.0"
NODE_SCHEMA_VERSION = "awesome-theorems/stage5.1-subject-node/1.0"
ASSIGNMENT_SCHEMA_VERSION = "awesome-theorems/stage5.1-subject-assignment/1.0"
EXPECTED_COUNTS = {"theorem": 3_500, "strict_conjecture": 1_425, "occurrence": 14_865}
EXPECTED_TOTAL = sum(EXPECTED_COUNTS.values())

MSC_CODE_RE = re.compile(
    r"^(?:[0-9]{2}|[0-9]{2}[A-Z]|[0-9]{2}[A-Z][0-9]{2}|[0-9]{2}-[0-9]{2})$"
)
S5_ID_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
POOL_ID_RE = re.compile(r"^S5POOL-([0-9]{8})$")

ROOT_NODE_ID = "S51-SUBJ-MATH"
NATIVE_ROOT_ID = "S51-SUBJ-SOURCE-VOCABULARY"
SENTINEL_ROOT_ID = "S51-SUBJ-SENTINEL"
SENTINELS = {
    "UNCLASSIFIED": "S51-SUBJ-SENTINEL-UNCLASSIFIED",
    "AMBIGUOUS": "S51-SUBJ-SENTINEL-AMBIGUOUS",
    "OTHER": "S51-SUBJ-SENTINEL-OTHER",
    "OUT_OF_SCOPE": "S51-SUBJ-SENTINEL-OUT-OF-SCOPE",
}

# These rules only propose broad MSC candidates.  They never populate an
# accepted membership or descend to a five-character leaf.
TITLE_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (r"\b(graph|hypergraph|ramsey|colour|coloring|matching|matroid)\b", ("05",)),
    (r"\b(prime|diophantine|integer|divisor|congruence|fermat|goldbach)\b", ("11",)),
    (r"\b(group|cayley|subgroup|lie group)\b", ("20",)),
    (r"\b(ring|ideal|module|algebra)\b", ("16",)),
    (r"\b(field|galois|polynomial)\b", ("12",)),
    (r"\b(probability|random|stochastic|martingale)\b", ("60",)),
    (r"\b(topolog|compact|continuous|homotop)\b", ("54",)),
    (r"\b(knot|manifold|embedding|cobord)\b", ("57",)),
    (r"\b(measure|integral|almost everywhere)\b", ("28",)),
    (r"\b(complex analysis|holomorphic|entire function)\b", ("30",)),
    (r"\b(functional analysis|banach|hilbert space|operator)\b", ("46",)),
    (r"\b(logic|model theory|set theory|computab)\b", ("03",)),
    (r"\b(algorithm|complexity|automata|computer)\b", ("68",)),
    (r"\b(dynamical|ergodic|orbit)\b", ("37",)),
    (r"\b(geometry|convex|polytope|distance set)\b", ("52",)),
)

NON_SUBJECT_TAG_RE = re.compile(
    r"^(?:difficulty:|set:|secondary-aggregation$|background-|problem-number-|"
    r"status$|statement$|current-status$|exact-|primary-source-|kourovka-main$)",
    re.IGNORECASE,
)
KNOWN_PROVENANCE_TAGS = {
    "Arxiv", "Books", "ErdosProblems", "GreensOpenProblems", "Mathoverflow",
    "OEIS", "Paper", "Wikipedia", "WrittenOnTheWallII",
}


class ClassificationError(RuntimeError):
    """A fail-closed input, authority, or classification invariant error."""


@dataclass(frozen=True)
class InputPaths:
    """Filesystem inputs consumed by the classifier."""

    msc_csv: Path
    theorem_list: Path
    claim_catalog: Path
    strict_ledger: Path
    pool_occurrences: Path
    pool_source_tar: Path


def default_input_paths(repo_root: Path, msc_csv: Path) -> InputPaths:
    base = repo_root / "Docs/catalog/v5"
    return InputPaths(
        msc_csv=msc_csv,
        theorem_list=base / "releases/5.6/Theorem_List.json",
        claim_catalog=base / "releases/5.6/Claim_Catalog.json",
        strict_ledger=base / "releases/5.6/Strict_Conjecture_Ledger.json",
        pool_occurrences=base / "pools/conjecturebench-357bcb1a/Source_Occurrence_Pool.jsonl",
        pool_source_tar=base / "sources/conjecturebench-357bcb1a-full-source.tar.gz",
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def bytes_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ClassificationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClassificationError(f"{label}: invalid UTF-8 JSON: {exc}") from exc


def read_json(path: Path) -> Any:
    if path.is_symlink() or not path.is_file():
        raise ClassificationError(f"missing regular JSON input: {path}")
    return strict_json_bytes(path.read_bytes(), str(path))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if path.is_symlink() or not path.is_file():
        raise ClassificationError(f"missing regular JSONL input: {path}")
    rows: list[dict[str, Any]] = []
    with path.open("rb") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                raise ClassificationError(f"{path}:{line_no}: blank JSONL row")
            value = strict_json_bytes(raw, f"{path}:{line_no}")
            if not isinstance(value, dict):
                raise ClassificationError(f"{path}:{line_no}: expected object")
            rows.append(value)
    return rows


def normalize_msc_code(value: Any) -> str | None:
    """Normalize common official-CSV renderings without changing depth."""

    if not isinstance(value, str):
        return None
    text = re.sub(r"\s+", "", value).upper()
    if re.fullmatch(r"[0-9]{2}-[A-Z]{2}", text):
        text = text[:2]
    elif re.fullmatch(r"[0-9]{2}-[0-9]{2}", text):
        return text
    elif re.fullmatch(r"[0-9]{2}[A-Z][X]{2}", text):
        text = text[:3]
    if MSC_CODE_RE.fullmatch(text):
        return text
    match = re.search(r"(?<![0-9A-Z])([0-9]{2}(?:[A-Z](?:[0-9]{2})?)?)(?![0-9A-Z])", text)
    return match.group(1) if match and MSC_CODE_RE.fullmatch(match.group(1)) else None


def msc_rank(code: str) -> str:
    return "msc_cross_reference" if "-" in code else {
        2: "msc_top", 3: "msc_section", 5: "msc_topic"
    }[len(code)]


def msc_node_id(code: str) -> str:
    return f"S51-SUBJ-MSC2020-{code}"


def _base_nodes(msc_sha256: str) -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {
        ROOT_NODE_ID: {
            "schema_version": NODE_SCHEMA_VERSION,
            "node_id": ROOT_NODE_ID,
            "scheme": "awesome-theorems",
            "edition": "Stage5.1",
            "notation": "MATH",
            "label": "Mathematics",
            "rank": "domain",
            "parent_node_id": None,
            "status": "structural",
            "source_sha256": msc_sha256,
        },
        NATIVE_ROOT_ID: {
            "schema_version": NODE_SCHEMA_VERSION,
            "node_id": NATIVE_ROOT_ID,
            "scheme": "awesome-theorems",
            "edition": "Stage5.1",
            "notation": "SOURCE_VOCABULARY",
            "label": "Source-native subject vocabularies",
            "rank": "source_vocabulary_root",
            "parent_node_id": ROOT_NODE_ID,
            "status": "structural_not_msc_equivalence",
            "source_sha256": msc_sha256,
        },
        SENTINEL_ROOT_ID: {
            "schema_version": NODE_SCHEMA_VERSION,
            "node_id": SENTINEL_ROOT_ID,
            "scheme": "awesome-theorems",
            "edition": "Stage5.1",
            "notation": "SENTINEL",
            "label": "Classification state sentinels",
            "rank": "sentinel_root",
            "parent_node_id": ROOT_NODE_ID,
            "status": "structural",
            "source_sha256": msc_sha256,
        },
    }
    sentinel_labels = {
        "UNCLASSIFIED": "Evidence insufficient for a reliable subject",
        "AMBIGUOUS": "Multiple subjects without an evidence-backed primary",
        "OTHER": "Mathematical content outside the current controlled vocabulary",
        "OUT_OF_SCOPE": "Not presently classifiable as an exact mathematical proposition",
    }
    for notation, node_id in SENTINELS.items():
        nodes[node_id] = {
            "schema_version": NODE_SCHEMA_VERSION,
            "node_id": node_id,
            "scheme": "awesome-theorems",
            "edition": "Stage5.1",
            "notation": notation,
            "label": sentinel_labels[notation],
            "rank": "sentinel",
            "parent_node_id": SENTINEL_ROOT_ID,
            "status": "sentinel",
            "source_sha256": msc_sha256,
        }
    return nodes


def parse_msc_csv(raw: bytes, expected_sha256: str) -> dict[str, dict[str, Any]]:
    """Parse a caller-pinned MSC CSV and return closed taxonomy nodes.

    Column names are intentionally tolerant because official exports differ;
    the code cell itself is not.  Parent nodes absent from the CSV are created
    only as structural prefix nodes, never as item-classification evidence.
    """

    actual = bytes_sha256(raw)
    if not re.fullmatch(r"[a-f0-9]{64}", expected_sha256) or actual != expected_sha256:
        raise ClassificationError(f"MSC CSV SHA-256 differs: expected {expected_sha256}, got {actual}")
    try:
        # The official MSC2020 file is named `.csv` but the pinned bytes are
        # ISO-8859-1 and tab-delimited.  Preserve/hash the raw bytes and decode
        # only for parsing.
        text = raw.decode("iso-8859-1")
    except UnicodeDecodeError as exc:
        raise ClassificationError(f"MSC CSV is not ISO-8859-1: {exc}") from exc
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    if not reader.fieldnames:
        raise ClassificationError("MSC CSV has no header")
    rows = list(reader)
    if not rows:
        raise ClassificationError("MSC CSV has no data rows")

    normalized_headers = {re.sub(r"[^a-z0-9]", "", h.lower()): h for h in reader.fieldnames}
    code_column = next(
        (normalized_headers[name] for name in ("code", "msc", "msc2020", "classification", "id")
         if name in normalized_headers),
        None,
    )
    if code_column is None:
        scored = [(sum(normalize_msc_code(row.get(header)) is not None for row in rows), header)
                  for header in reader.fieldnames]
        score, code_column = max(scored)
        if score == 0:
            raise ClassificationError("MSC CSV has no recognizable code column")
    label_column = next(
        (normalized_headers[name] for name in ("description", "label", "title", "name", "text")
         if name in normalized_headers),
        None,
    )

    labels: dict[str, str] = {}
    for line_no, row in enumerate(rows, 2):
        code = normalize_msc_code(row.get(code_column))
        if code is None:
            continue
        label = str(row.get(label_column) or code).strip() if label_column else code
        if code in labels and labels[code] != label:
            raise ClassificationError(f"MSC CSV line {line_no}: conflicting label for {code}")
        labels[code] = label
    if not labels:
        raise ClassificationError("MSC CSV yielded no MSC codes")

    # Close structural prefixes without pretending the CSV asserted their label.
    for code in list(labels):
        if len(code) == 5:
            labels.setdefault(code[:3], code[:3])
            labels.setdefault(code[:2], code[:2])
        elif len(code) == 3:
            labels.setdefault(code[:2], code[:2])

    nodes = _base_nodes(actual)
    for code in sorted(labels, key=lambda item: (len(item), item)):
        parent = (
            ROOT_NODE_ID
            if len(code) == 2
            else msc_node_id(code[:2] if len(code) == 3 or "-" in code else code[:3])
        )
        nodes[msc_node_id(code)] = {
            "schema_version": NODE_SCHEMA_VERSION,
            "node_id": msc_node_id(code),
            "scheme": "MSC",
            "edition": "2020",
            "notation": code,
            "label": labels[code],
            "rank": msc_rank(code),
            "parent_node_id": parent,
            "status": "active" if labels[code] != code else "structural_prefix_inferred",
            "source_sha256": actual,
        }
    return nodes


def load_msc_taxonomy(path: Path, expected_sha256: str) -> dict[str, dict[str, Any]]:
    if path.is_symlink() or not path.is_file():
        raise ClassificationError(f"missing regular MSC CSV: {path}")
    return parse_msc_csv(path.read_bytes(), expected_sha256)


class TaxonomyBuilder:
    def __init__(self, msc_nodes: Mapping[str, Mapping[str, Any]]) -> None:
        self.nodes = {key: dict(value) for key, value in msc_nodes.items()}
        self.msc_sha256 = str(self.nodes[ROOT_NODE_ID]["source_sha256"])
        self._native: dict[tuple[str, str, str | None], str] = {}
        self._scheme_roots: dict[str, str] = {}

    def require_msc(self, code: str) -> str:
        node_id = msc_node_id(code)
        if node_id not in self.nodes:
            raise ClassificationError(f"source references MSC {code}, absent from pinned CSV")
        return node_id

    def native_node(self, scheme: str, label: str, rank: str, parent_node_id: str | None = None) -> str:
        scheme = scheme.strip()
        label = label.strip()
        if not scheme or not label:
            raise ClassificationError("empty source-native scheme or label")
        if scheme not in self._scheme_roots:
            digest = hashlib.sha256(scheme.encode("utf-8")).hexdigest()[:16].upper()
            root_id = f"S51-SUBJ-SOURCE-SCHEME-{digest}"
            self._scheme_roots[scheme] = root_id
            self.nodes[root_id] = {
                "schema_version": NODE_SCHEMA_VERSION,
                "node_id": root_id,
                "scheme": scheme,
                "edition": "source-pinned",
                "notation": scheme,
                "label": scheme,
                "rank": "source_scheme",
                "parent_node_id": NATIVE_ROOT_ID,
                "status": "source_vocabulary_not_msc_equivalence",
                "source_sha256": self.msc_sha256,
            }
        parent = parent_node_id or self._scheme_roots[scheme]
        key = (scheme, label, parent)
        if key in self._native:
            return self._native[key]
        digest = hashlib.sha256(canonical_json(key).encode("utf-8")).hexdigest()[:20].upper()
        node_id = f"S51-SUBJ-SOURCE-{digest}"
        self._native[key] = node_id
        self.nodes[node_id] = {
            "schema_version": NODE_SCHEMA_VERSION,
            "node_id": node_id,
            "scheme": scheme,
            "edition": "source-pinned",
            "notation": label,
            "label": label,
            "rank": rank,
            "parent_node_id": parent,
            "status": "source_exact_at_native_granularity_not_msc_equivalence",
            "source_sha256": self.msc_sha256,
        }
        return node_id


def _raw_label(scheme: str, value: str, path: str, role: str = "source_label") -> dict[str, str]:
    return {"scheme": scheme, "value": value, "path": path, "role": role}


def _membership(node_id: str, scheme: str, value: str, path: str, *,
                priority: int, primary_claim: bool, basis: str) -> dict[str, Any]:
    return {
        "subject_id": node_id,
        "scheme": scheme,
        "raw_value": value,
        "evidence_path": path,
        "priority": priority,
        "source_primary_claim": primary_claim,
        "assertion_state": "source_exact",
        "evidence_tier": basis,
    }


def _candidate(node_id: str | None, scheme: str, value: str, path: str, basis: str) -> dict[str, Any]:
    return {
        "subject_id": node_id,
        "scheme": scheme,
        "raw_value": value,
        "evidence_path": path,
        "assertion_state": "candidate_only",
        "basis": basis,
    }


def _dedupe_dicts(values: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {canonical_json(value): value for value in values}
    return [by_key[key] for key in sorted(by_key)]


def _statement_text(record: Mapping[str, Any]) -> str:
    mathematical = record.get("mathematical_statement") or {}
    statement = record.get("statement") or {}
    if isinstance(statement, str):
        return statement
    values = (
        mathematical.get("natural_language"), mathematical.get("plain_text"),
        mathematical.get("semantic_summary"), mathematical.get("exact_claim_text"),
        mathematical.get("body_tex"), statement.get("natural_language") if isinstance(statement, dict) else None,
        statement.get("formal_type") if isinstance(statement, dict) else None,
        record.get("formal_type"),
    )
    return "\n".join(value for value in values if isinstance(value, str))


def _rule_candidates(builder: TaxonomyBuilder, title: str, statement: str, path: str) -> list[dict[str, Any]]:
    haystack = f"{title}\n{statement}".lower()
    candidates: list[dict[str, Any]] = []
    for pattern, codes in TITLE_RULES:
        if re.search(pattern, haystack, re.IGNORECASE):
            for code in codes:
                node_id = msc_node_id(code)
                if node_id in builder.nodes:
                    candidates.append(_candidate(node_id, "MSC", code, path, "title_statement_rule"))
    return _dedupe_dicts(candidates)


def _finalize_assignment(
    *,
    member_id: str,
    member_kind: str,
    legacy_binding: dict[str, Any],
    accepted: Iterable[dict[str, Any]],
    candidates: Iterable[dict[str, Any]],
    raw_labels: Iterable[dict[str, str]],
    review_flags: Iterable[str],
    conflicts: Iterable[dict[str, Any]],
    out_of_scope: bool = False,
    explicit_other: bool = False,
) -> dict[str, Any]:
    accepted_rows = _dedupe_dicts(accepted)
    candidate_rows = _dedupe_dicts(candidates)
    raw_rows = _dedupe_dicts(raw_labels)
    flags = sorted(set(str(flag) for flag in review_flags if str(flag)))
    conflict_rows = _dedupe_dicts(conflicts)

    primary_claims = sorted(
        {row["subject_id"] for row in accepted_rows if row["source_primary_claim"]},
    )
    accepted_ids = sorted({row["subject_id"] for row in accepted_rows})
    candidate_ids = sorted({row["subject_id"] for row in candidate_rows if row["subject_id"]})
    if out_of_scope:
        primary = SENTINELS["OUT_OF_SCOPE"]
        primary_state = "out_of_scope"
    elif len(primary_claims) == 1:
        primary = primary_claims[0]
        primary_state = "source_exact"
    elif len(primary_claims) > 1 or (not primary_claims and len(accepted_ids) > 1):
        primary = SENTINELS["AMBIGUOUS"]
        primary_state = "ambiguous_source_exact_memberships"
        flags.append("multiple_source_labels_primary_review")
    elif len(accepted_ids) == 1:
        primary = accepted_ids[0]
        primary_state = "source_exact"
    elif explicit_other:
        primary = SENTINELS["OTHER"]
        primary_state = "source_explicit_other"
    elif len(candidate_ids) > 1:
        primary = SENTINELS["AMBIGUOUS"]
        primary_state = "ambiguous_candidates_only"
    else:
        primary = SENTINELS["UNCLASSIFIED"]
        primary_state = "unclassified_candidates_do_not_grant_assignment" if candidate_ids else "unclassified"

    secondary = sorted(subject_id for subject_id in accepted_ids if subject_id != primary)
    body = {
        "schema_version": ASSIGNMENT_SCHEMA_VERSION,
        "member_id": member_id,
        "member_kind": member_kind,
        "legacy_binding": legacy_binding,
        "primary_subject_id": primary,
        "primary_assertion_state": primary_state,
        "secondary_subject_ids": secondary,
        "accepted_memberships": accepted_rows,
        "candidate_subjects": candidate_rows,
        "raw_labels": raw_rows,
        "conflicts": conflict_rows,
        "review_flags": sorted(set(flags)),
        "fine_msc_inference_forbidden": True,
    }
    body["assignment_id"] = "S51SUB-" + canonical_sha256(body)[:24].upper()
    body["record_sha256"] = canonical_sha256(body)
    return body


def _claim_member(stage_claim_id: str, kind: str) -> tuple[str, str]:
    match = S5_ID_RE.fullmatch(stage_claim_id)
    if not match:
        raise ClassificationError(f"invalid Stage5 claim ID: {stage_claim_id!r}")
    ordinal = match.group(1)
    if kind == "theorem":
        return f"S51-THM-{ordinal}", f"S5THM-{ordinal}-TARGET"
    return f"S51-CON-{ordinal}", f"S5CON-{ordinal}-TARGET"


def _add_exact_msc(
    builder: TaxonomyBuilder,
    accepted: list[dict[str, Any]],
    raw: list[dict[str, str]],
    code_value: Any,
    path: str,
    *,
    priority: int,
    primary: bool,
    basis: str,
) -> None:
    code = normalize_msc_code(code_value)
    if code is None:
        raise ClassificationError(f"{path}: malformed source-exact MSC code {code_value!r}")
    node_id = builder.require_msc(code)
    raw.append(_raw_label("MSC", str(code_value), path, "source_exact"))
    accepted.append(_membership(node_id, "MSC", code, path, priority=priority,
                                primary_claim=primary, basis=basis))


def classify_theorem_records(
    theorem_records: Sequence[Mapping[str, Any]], builder: TaxonomyBuilder
) -> list[dict[str, Any]]:
    assignments: list[dict[str, Any]] = []
    for record in theorem_records:
        stage_id = str(record.get("stage_claim_id", ""))
        member_id, legacy_item = _claim_member(stage_id, "theorem")
        accepted: list[dict[str, Any]] = []
        candidates: list[dict[str, Any]] = []
        raw: list[dict[str, str]] = []
        flags: list[str] = []
        conflicts: list[dict[str, Any]] = []
        title = str(record.get("display_name") or "")
        statement = _statement_text(record)

        if isinstance(record.get("ams"), list):
            primary_code = normalize_msc_code(record.get("primary_ams_class"))
            for index, value in enumerate(record["ams"]):
                code = normalize_msc_code(value)
                _add_exact_msc(builder, accepted, raw, value, f"records[{stage_id}].ams[{index}]",
                               priority=10 if code == primary_code else 20,
                               primary=code == primary_code,
                               basis="formal_conjectures_source_ams")

        classification = record.get("classification") or {}
        if isinstance(classification, dict) and classification.get("msc2020_code") is not None:
            value = classification["msc2020_code"]
            code = normalize_msc_code(value)
            basis = str(classification.get("basis") or classification.get("status") or "")
            path = f"records[{stage_id}].classification.msc2020_code"
            raw.append(_raw_label("MSC", str(value), path,
                                  "source_exact" if basis in {"1000_plus_curated", "source_curated_exact"} else "machine_signal"))
            if code is None:
                raise ClassificationError(f"{path}: malformed MSC code")
            node_id = builder.require_msc(code)
            if basis in {"1000_plus_curated", "source_curated_exact"}:
                accepted.append(_membership(node_id, "MSC", code, path, priority=10,
                                            primary_claim=True, basis="source_curated_exact"))
            else:
                candidates.append(_candidate(node_id, "MSC", code, path, "machine_module_root_crosswalk"))
                flags.append("coarse_module_root_only")
        module = record.get("module") or (record.get("formal_statement") or {}).get("module")
        if isinstance(module, str) and module:
            raw.append(_raw_label("LEAN_MODULE", module, f"records[{stage_id}].module", "machine_signal"))
        candidates.extend(_rule_candidates(builder, title, statement, f"records[{stage_id}].title_statement"))

        if len({row["subject_id"] for row in accepted}) > 1:
            flags.append("multiple_source_subjects")
        assignments.append(_finalize_assignment(
            member_id=member_id,
            member_kind="theorem",
            legacy_binding={
                "stage5_claim_id": stage_id,
                "stage5_item_id": legacy_item,
                "variant_id": record.get("variant_id"),
                "source_record_sha256": canonical_sha256(record),
            },
            accepted=accepted,
            candidates=candidates,
            raw_labels=raw,
            review_flags=flags,
            conflicts=conflicts,
        ))
    return assignments


def classify_strict_conjectures(
    strict_credits: Sequence[Mapping[str, Any]],
    claim_records_by_id: Mapping[str, Mapping[str, Any]],
    builder: TaxonomyBuilder,
) -> list[dict[str, Any]]:
    assignments: list[dict[str, Any]] = []
    for credit in strict_credits:
        stage_id = str(credit.get("stage_claim_id", ""))
        if stage_id not in claim_records_by_id:
            raise ClassificationError(f"strict credit missing Claim_Catalog record: {stage_id}")
        record = claim_records_by_id[stage_id]
        member_id, legacy_item = _claim_member(stage_id, "strict_conjecture")
        accepted: list[dict[str, Any]] = []
        candidates: list[dict[str, Any]] = []
        raw: list[dict[str, str]] = []
        flags: list[str] = []
        conflicts: list[dict[str, Any]] = []
        title = str(record.get("display_name") or "")
        statement = _statement_text(record)

        if isinstance(record.get("ams"), list):
            primary_code = normalize_msc_code(record.get("primary_ams_class"))
            for index, value in enumerate(record["ams"]):
                code = normalize_msc_code(value)
                _add_exact_msc(builder, accepted, raw, value, f"records[{stage_id}].ams[{index}]",
                               priority=10 if code == primary_code else 20,
                               primary=code == primary_code,
                               basis="formal_conjectures_source_ams")

        classification = record.get("classification") or {}
        if isinstance(classification, dict):
            msc_codes = classification.get("msc_codes") or []
            if not isinstance(msc_codes, list):
                raise ClassificationError(f"{stage_id}: classification.msc_codes is not an array")
            for index, value in enumerate(msc_codes):
                _add_exact_msc(builder, accepted, raw, value,
                               f"records[{stage_id}].classification.msc_codes[{index}]",
                               priority=10 if index == 0 else 20, primary=index == 0,
                               basis="source_or_review_metadata")

            for field_name in ("source_categories", "source_areas"):
                values = classification.get(field_name) or []
                if not isinstance(values, list):
                    continue
                primary_value = str(classification.get("source_primary_category") or "")
                for index, value in enumerate(values):
                    if not isinstance(value, str) or not value.strip():
                        continue
                    scheme = "ARXIV" if field_name == "source_categories" else "SOURCE_AREA"
                    node_id = builder.native_node(scheme, value, "source_category")
                    path = f"records[{stage_id}].classification.{field_name}[{index}]"
                    raw.append(_raw_label(scheme, value, path, "source_exact"))
                    accepted.append(_membership(node_id, scheme, value, path, priority=30,
                                                primary_claim=value == primary_value,
                                                basis="source_exact_native_category"))
            if classification.get("classification_status") == "source_metadata_missing":
                flags.append("missing_standard_class")

        candidates.extend(_rule_candidates(builder, title, statement, f"records[{stage_id}].title_statement"))
        if not accepted:
            flags.append("missing_standard_class")
        assignments.append(_finalize_assignment(
            member_id=member_id,
            member_kind="strict_conjecture",
            legacy_binding={
                "stage5_claim_id": stage_id,
                "stage5_item_id": legacy_item,
                "variant_id": credit.get("variant_id"),
                "credit_row_sha256": credit.get("row_sha256"),
                "source_record_sha256": canonical_sha256(record),
            },
            accepted=accepted,
            candidates=candidates,
            raw_labels=raw,
            review_flags=flags,
            conflicts=conflicts,
        ))
    return assignments


def _safe_tar_members(archive: tarfile.TarFile) -> dict[str, tarfile.TarInfo]:
    members: dict[str, tarfile.TarInfo] = {}
    for member in archive.getmembers():
        path = PurePosixPath(member.name)
        if path.is_absolute() or not path.parts or ".." in path.parts:
            raise ClassificationError(f"unsafe tar path: {member.name!r}")
        if member.issym() or member.islnk():
            raise ClassificationError(f"tar link forbidden: {member.name!r}")
        if member.name in members:
            raise ClassificationError(f"duplicate tar member: {member.name!r}")
        members[member.name] = member
    return members


def _pool_raw_records(
    occurrences: Sequence[Mapping[str, Any]], source_tar: Path
) -> dict[str, dict[str, Any]]:
    if source_tar.is_symlink() or not source_tar.is_file():
        raise ClassificationError(f"missing regular pool source archive: {source_tar}")
    required_paths = {str(row.get("record_path")) for row in occurrences}
    result: dict[str, dict[str, Any]] = {}
    with tarfile.open(source_tar, "r:*") as archive:
        members = _safe_tar_members(archive)
        roots = {PurePosixPath(name).parts[0] for name in members if PurePosixPath(name).parts}
        if len(roots) != 1:
            raise ClassificationError(f"pool archive must have one top-level root, got {sorted(roots)}")
        root = next(iter(roots))
        payload_cache: dict[str, Any] = {}
        for relative in sorted(required_paths):
            full_name = f"{root}/{relative}"
            member = members.get(full_name)
            if member is None or not member.isfile():
                raise ClassificationError(f"pool archive lacks regular member: {relative}")
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ClassificationError(f"cannot read pool archive member: {relative}")
            payload_cache[relative] = strict_json_bytes(extracted.read(), relative)
        for row in occurrences:
            pool_id = str(row.get("pool_id", ""))
            relative = str(row.get("record_path", ""))
            payload = payload_cache[relative]
            if row.get("kind") == "family":
                index = row.get("family_container_index")
                records = payload.get("records") if isinstance(payload, dict) else None
                if not isinstance(index, int) or not isinstance(records, list) or not (0 <= index < len(records)):
                    raise ClassificationError(f"{pool_id}: invalid family container index")
                record = records[index]
            else:
                record = payload
            if not isinstance(record, dict):
                raise ClassificationError(f"{pool_id}: raw source record is not an object")
            if record.get("id") != row.get("source_native_id"):
                raise ClassificationError(f"{pool_id}: source-native ID differs")
            if canonical_sha256(record) != row.get("canonical_record_sha256"):
                raise ClassificationError(f"{pool_id}: canonical raw record digest differs")
            result[pool_id] = record
    return result


def _pool_statement(record: Mapping[str, Any]) -> str:
    statement = record.get("statement")
    if isinstance(statement, str):
        return statement
    if isinstance(statement, dict) and isinstance(statement.get("text"), str):
        return statement["text"]
    return ""


def _subject_tag(tag: str) -> bool:
    return bool(tag and tag not in KNOWN_PROVENANCE_TAGS and not NON_SUBJECT_TAG_RE.search(tag))


def classify_pool_occurrences(
    occurrences: Sequence[Mapping[str, Any]],
    raw_by_pool_id: Mapping[str, Mapping[str, Any]],
    builder: TaxonomyBuilder,
) -> list[dict[str, Any]]:
    assignments: list[dict[str, Any]] = []
    for occurrence in occurrences:
        pool_id = str(occurrence.get("pool_id", ""))
        match = POOL_ID_RE.fullmatch(pool_id)
        if not match or pool_id not in raw_by_pool_id:
            raise ClassificationError(f"invalid or unjoined pool ID: {pool_id!r}")
        record = raw_by_pool_id[pool_id]
        member_id = f"S51-OCC-{match.group(1)}"
        accepted: list[dict[str, Any]] = []
        candidates: list[dict[str, Any]] = []
        raw: list[dict[str, str]] = []
        flags = list(occurrence.get("review_flags") or [])
        conflicts: list[dict[str, Any]] = []
        title = str(occurrence.get("title") or "")
        statement = _pool_statement(record)

        field = record.get("field")
        field_node: str | None = None
        if isinstance(field, str) and field.strip():
            field_node = builder.native_node("CONJECTUREBENCH_FIELD", field, "source_field")
            path = f"{occurrence.get('record_path')}#/field"
            raw.append(_raw_label("CONJECTUREBENCH_FIELD", field, path, "source_exact"))
            accepted.append(_membership(field_node, "CONJECTUREBENCH_FIELD", field, path,
                                        priority=30, primary_claim=not record.get("class"),
                                        basis="source_exact_native_field"))
        source_class = record.get("class")
        if isinstance(source_class, str) and source_class.strip():
            class_node = builder.native_node("CONJECTUREBENCH_CLASS", source_class,
                                             "source_subfield", field_node)
            path = f"{occurrence.get('record_path')}#/class"
            raw.append(_raw_label("CONJECTUREBENCH_CLASS", source_class, path, "source_exact"))
            accepted.append(_membership(class_node, "CONJECTUREBENCH_CLASS", source_class, path,
                                        priority=20, primary_claim=True,
                                        basis="source_exact_native_class"))

        tags = (record.get("provenance") or {}).get("tags") or record.get("tags") or []
        if not isinstance(tags, list):
            raise ClassificationError(f"{pool_id}: tags are not an array")
        explicit_primary_count = 0
        for index, value in enumerate(tags):
            if not isinstance(value, str) or not value.strip():
                continue
            path = f"{occurrence.get('record_path')}#/provenance/tags/{index}"
            raw.append(_raw_label("SOURCE_TAG", value, path,
                                  "source_subject_signal" if _subject_tag(value) else "source_metadata"))
            ams_match = re.fullmatch(r"AMS-([0-9]{2})", value, re.IGNORECASE)
            if ams_match:
                code = ams_match.group(1)
                node_id = builder.require_msc(code)
                accepted.append(_membership(node_id, "MSC", code, path, priority=20,
                                            primary_claim=False, basis="source_exact_ams_tag"))
            elif value.lower().startswith("category:"):
                category = value.split(":", 1)[1].strip()
                if category.lower() == "miscellaneous":
                    flags.append("source_category_miscellaneous")
                    continue
                node_id = builder.native_node("SOURCE_CATEGORY", category, "source_category")
                accepted.append(_membership(node_id, "SOURCE_CATEGORY", category, path, priority=30,
                                            primary_claim=True, basis="source_exact_category_tag"))
                explicit_primary_count += 1
            elif _subject_tag(value):
                node_id = builder.native_node("SOURCE_TOPIC_TAG", value, "source_topic")
                accepted.append(_membership(node_id, "SOURCE_TOPIC_TAG", value, path, priority=40,
                                            primary_claim=False, basis="source_exact_topic_tag"))

        candidates.extend(_rule_candidates(builder, title, statement,
                                           f"{occurrence.get('record_path')}#/title_statement"))
        placeholder = bool(occurrence.get("contains_placeholder"))
        vacuous_true = bool(re.search(r"(?m):\s*True\s*(?::=|$)", statement))
        if placeholder:
            flags.append("placeholder_statement")
        if vacuous_true:
            flags.append("vacuous_true_false_negative")
        if occurrence.get("statement_presence") == "pointer":
            flags.append("pointer_requires_dereference")
        for flag in list(flags):
            if flag in {"category-conflict", "source-category-conflict"}:
                conflicts.append({"kind": "source_category_conflict", "source_flag": flag})
        if explicit_primary_count > 1:
            conflicts.append({"kind": "multiple_source_primary_categories",
                              "count": explicit_primary_count})

        assignments.append(_finalize_assignment(
            member_id=member_id,
            member_kind="occurrence",
            legacy_binding={
                "pool_id": pool_id,
                "stage5_item_id": f"S5CON-POOL-{match.group(1)}-INTAKE",
                "stable_source_key": occurrence.get("stable_source_key"),
                "occurrence_authority_sha256": occurrence.get("authority_sha256"),
                "canonical_record_sha256": occurrence.get("canonical_record_sha256"),
            },
            accepted=accepted,
            candidates=candidates,
            raw_labels=raw,
            review_flags=flags,
            conflicts=conflicts,
            out_of_scope=placeholder or vacuous_true,
            explicit_other=("source_category_miscellaneous" in flags and not accepted),
        ))
    return assignments


def _input_authority(paths: InputPaths) -> dict[str, dict[str, Any]]:
    return {
        name: {"path": str(path), "sha256": file_sha256(path), "size_bytes": path.stat().st_size}
        for name, path in (
            ("msc_csv", paths.msc_csv),
            ("theorem_list", paths.theorem_list),
            ("claim_catalog", paths.claim_catalog),
            ("strict_ledger", paths.strict_ledger),
            ("pool_occurrences", paths.pool_occurrences),
            ("pool_source_tar", paths.pool_source_tar),
        )
    }


def build_stage5_1_subject_classification(
    paths: InputPaths, *, msc_csv_sha256: str
) -> dict[str, Any]:
    """Return taxonomy nodes and exactly 19,790 deterministic assignments."""

    nodes = load_msc_taxonomy(paths.msc_csv, msc_csv_sha256)
    builder = TaxonomyBuilder(nodes)
    theorem_doc = read_json(paths.theorem_list)
    claim_doc = read_json(paths.claim_catalog)
    strict_doc = read_json(paths.strict_ledger)
    if not isinstance(theorem_doc, dict) or not isinstance(theorem_doc.get("records"), list):
        raise ClassificationError("Theorem_List.records is missing")
    if not isinstance(claim_doc, dict) or not isinstance(claim_doc.get("records"), list):
        raise ClassificationError("Claim_Catalog.records is missing")
    if not isinstance(strict_doc, dict) or not isinstance(strict_doc.get("strict_credits"), list):
        raise ClassificationError("Strict_Conjecture_Ledger.strict_credits is missing")
    claim_by_id: dict[str, Mapping[str, Any]] = {}
    for record in claim_doc["records"]:
        stage_id = record.get("stage_claim_id") if isinstance(record, dict) else None
        if not isinstance(stage_id, str) or stage_id in claim_by_id:
            raise ClassificationError(f"invalid/duplicate Claim_Catalog stage ID: {stage_id!r}")
        claim_by_id[stage_id] = record

    occurrences = read_jsonl(paths.pool_occurrences)
    raw_by_pool_id = _pool_raw_records(occurrences, paths.pool_source_tar)
    theorem_assignments = classify_theorem_records(theorem_doc["records"], builder)
    strict_assignments = classify_strict_conjectures(strict_doc["strict_credits"], claim_by_id, builder)
    pool_assignments = classify_pool_occurrences(occurrences, raw_by_pool_id, builder)
    assignments = sorted(theorem_assignments + strict_assignments + pool_assignments,
                         key=lambda row: row["member_id"])
    taxonomy_nodes = sorted(builder.nodes.values(), key=lambda row: row["node_id"])
    authority = _input_authority(paths)
    body = {
        "schema_version": SCHEMA_VERSION,
        "blueprint_revision": "Stage5.1",
        "catalog_parent_release": "5.6",
        "not_catalog_release_5_1": True,
        "policy": {
            "source_exact_only_to_asserted_depth": True,
            "machine_module_title_and_rule_are_candidate_only": True,
            "five_character_msc_without_exact_source_evidence_forbidden": True,
            "unknown_is_not_independence_or_completion": True,
        },
        "inputs": authority,
        "taxonomy_nodes": taxonomy_nodes,
        "assignments": assignments,
    }
    body["taxonomy_set_sha256"] = canonical_sha256(taxonomy_nodes)
    body["assignment_set_sha256"] = canonical_sha256(assignments)
    body["authority_sha256"] = canonical_sha256(body)
    self_check_bundle(body)
    return body


def self_check_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]:
    nodes = bundle.get("taxonomy_nodes")
    assignments = bundle.get("assignments")
    if not isinstance(nodes, list) or not isinstance(assignments, list):
        raise ClassificationError("bundle lacks taxonomy_nodes or assignments")
    by_node = {row.get("node_id"): row for row in nodes if isinstance(row, dict)}
    if len(by_node) != len(nodes):
        raise ClassificationError("duplicate or malformed taxonomy node")
    for required in (ROOT_NODE_ID, NATIVE_ROOT_ID, SENTINEL_ROOT_ID, *SENTINELS.values()):
        if required not in by_node:
            raise ClassificationError(f"missing required taxonomy node: {required}")
    for node_id, node in by_node.items():
        parent = node.get("parent_node_id")
        if parent is not None and parent not in by_node:
            raise ClassificationError(f"taxonomy orphan: {node_id} -> {parent}")
        seen = {node_id}
        cursor = parent
        while cursor is not None:
            if cursor in seen:
                raise ClassificationError(f"taxonomy cycle at {node_id}")
            seen.add(cursor)
            cursor = by_node[cursor].get("parent_node_id")

    ids = [row.get("member_id") for row in assignments if isinstance(row, dict)]
    if len(assignments) != EXPECTED_TOTAL or len(set(ids)) != EXPECTED_TOTAL:
        raise ClassificationError(f"assignment cardinality/uniqueness differs: {len(assignments)}")
    counts = Counter(row.get("member_kind") for row in assignments)
    if dict(counts) != EXPECTED_COUNTS:
        raise ClassificationError(f"assignment kind counts differ: {dict(counts)}")
    for row in assignments:
        primary = row.get("primary_subject_id")
        if primary not in by_node:
            raise ClassificationError(f"{row.get('member_id')}: unknown primary subject {primary}")
        for subject_id in row.get("secondary_subject_ids", []):
            if subject_id not in by_node:
                raise ClassificationError(f"{row.get('member_id')}: unknown secondary subject")
        for membership in row.get("accepted_memberships", []):
            subject_id = membership.get("subject_id")
            if subject_id not in by_node or membership.get("assertion_state") != "source_exact":
                raise ClassificationError(f"{row.get('member_id')}: invalid accepted membership")
            node = by_node[subject_id]
            if node.get("scheme") == "MSC" and len(str(node.get("notation"))) == 5:
                raw_code = normalize_msc_code(membership.get("raw_value"))
                if raw_code != node.get("notation"):
                    raise ClassificationError(
                        f"{row.get('member_id')}: inferred five-character MSC forbidden"
                    )
        for candidate in row.get("candidate_subjects", []):
            if candidate.get("assertion_state") != "candidate_only":
                raise ClassificationError(f"{row.get('member_id')}: candidate upgraded")
    if canonical_sha256(nodes) != bundle.get("taxonomy_set_sha256"):
        raise ClassificationError("taxonomy set digest differs")
    if canonical_sha256(assignments) != bundle.get("assignment_set_sha256"):
        raise ClassificationError("assignment set digest differs")
    return {
        "status": "ok",
        "assignments": len(assignments),
        "taxonomy_nodes": len(nodes),
        "counts": dict(sorted(counts.items())),
    }


def summarize_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]:
    assignments = bundle["assignments"]
    primary_states = Counter(row["primary_assertion_state"] for row in assignments)
    sentinels = Counter(
        next((name for name, node_id in SENTINELS.items() if row["primary_subject_id"] == node_id), "NONE")
        for row in assignments
    )
    accepted_five = sum(
        1
        for row in assignments
        for membership in row["accepted_memberships"]
        if membership["scheme"] == "MSC" and len(membership["raw_value"]) == 5
    )
    return {
        "schema_version": "awesome-theorems/stage5.1-subject-classification-summary/1.0",
        "self_check": self_check_bundle(bundle),
        "taxonomy_nodes": len(bundle["taxonomy_nodes"]),
        "assignments": len(assignments),
        "primary_assertion_states": dict(sorted(primary_states.items())),
        "primary_sentinels": dict(sorted(sentinels.items())),
        "accepted_five_character_msc_with_exact_raw_evidence": accepted_five,
        "taxonomy_set_sha256": bundle["taxonomy_set_sha256"],
        "assignment_set_sha256": bundle["assignment_set_sha256"],
        "authority_sha256": bundle["authority_sha256"],
    }


def _parser() -> argparse.ArgumentParser:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--msc-csv", type=Path, required=True,
                        help="caller-pinned MSC CSV (never downloaded by this tool)")
    parser.add_argument("--msc-sha256", required=True,
                        help="mandatory expected SHA-256 of --msc-csv")
    parser.add_argument("--theorem-list", type=Path,
                        default=repo_root / "Docs/catalog/v5/releases/5.6/Theorem_List.json")
    parser.add_argument("--claim-catalog", type=Path,
                        default=repo_root / "Docs/catalog/v5/releases/5.6/Claim_Catalog.json")
    parser.add_argument("--strict-ledger", type=Path,
                        default=repo_root / "Docs/catalog/v5/releases/5.6/Strict_Conjecture_Ledger.json")
    parser.add_argument("--pool-occurrences", type=Path,
                        default=repo_root / "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Source_Occurrence_Pool.jsonl")
    parser.add_argument("--pool-source-tar", type=Path,
                        default=repo_root / "Docs/catalog/v5/sources/conjecturebench-357bcb1a-full-source.tar.gz")
    parser.add_argument("--emit", choices=("summary", "bundle", "taxonomy", "assignments"),
                        default="summary")
    parser.add_argument("--self-check", action="store_true",
                        help="run all invariants; summary output includes the result")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    paths = InputPaths(
        msc_csv=args.msc_csv,
        theorem_list=args.theorem_list,
        claim_catalog=args.claim_catalog,
        strict_ledger=args.strict_ledger,
        pool_occurrences=args.pool_occurrences,
        pool_source_tar=args.pool_source_tar,
    )
    try:
        bundle = build_stage5_1_subject_classification(paths, msc_csv_sha256=args.msc_sha256)
        if args.self_check:
            self_check_bundle(bundle)
        value: Any
        if args.emit == "bundle":
            value = bundle
        elif args.emit == "taxonomy":
            value = bundle["taxonomy_nodes"]
        elif args.emit == "assignments":
            value = bundle["assignments"]
        else:
            value = summarize_bundle(bundle)
        sys.stdout.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        return 0
    except (ClassificationError, OSError, tarfile.TarError) as exc:
        print(f"classification error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
