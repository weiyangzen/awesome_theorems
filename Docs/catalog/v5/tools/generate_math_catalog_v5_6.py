#!/usr/bin/env python3
"""Build append-only Stage5 release 5.6 from the sealed mathlib reserve.

The transaction preserves every 5.5 release array as an exact prefix and
allocates exactly 1,000 new theorem records.  The source denominator is the
1,561-row qualified mathlib ledger: 1,092 mechanically ready rows and 469
semantic-signal quarantine rows.  Selection first admits every ready row with
an individual declaration docstring (511), then performs a deterministic
module-root round-robin for 489 further rows.  The remaining 92 ready rows and
all 469 quarantine rows receive terminal, non-credit dispositions.

``--selection-only`` materializes the closed mathlib operand without granting
credit or allocating IDs.  The full transaction derives a separate, sealed
release-allocation ledger from that operand, allocates exactly 1,000 identities,
and leaves every Putnam seed, formal variant, and relation edge at zero catalog
credit.  Putnam benchmark curation is therefore an independent follow-on and
cannot block this release or be counted as theorem inventory.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable, Mapping, Sequence


REPO = Path(__file__).resolve().parents[4]
V5 = REPO / "Docs/catalog/v5"
PARENT_DIR = V5 / "releases/5.5"
RELEASE_DIR = V5 / "releases/5.6"
READABLE_DIR = V5 / "readable/5.6"
RESERVE_DIR = V5 / "curation/mathlib_reserve_v5_6"
FULL_SOURCE = RESERVE_DIR / "mathlib-verified-theorems-8a178386-full.json"
QUALIFIED_LEDGER = RESERVE_DIR / "Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl"
QUALIFIED_INVENTORY = RESERVE_DIR / "Mathlib_Qualified_Batch_Inventory_v5_6.json"
ACCEPTED_SET = RESERVE_DIR / "Mathlib_Generator_Accepted_Set_v5_6.jsonl"
GENERATOR_ACCEPTANCE_RECEIPT = RESERVE_DIR / "Mathlib_Generator_Acceptance_Receipt_v5_6.json"
SELECTION_PATH = RESERVE_DIR / "Mathlib_Release_Selection_v5_6.json"
ALLOCATION_PATH = RESERVE_DIR / "Mathlib_Release_Allocation_v5_6.json"
CONTRACT_PATH = V5 / "Stage5_Math_Expansion_Contract_v5_6.json"
SCHEMA_PATH = V5 / "Math_Claim_Record_Schema_v5_6.json"
SOURCE_REGISTRY_PATH = V5 / "Math_Source_Registry_v5_6.json"
PARENT_RECEIPT_PATH = V5 / "V5_5_Parent_Receipt_v5_6.json"
BASE_SCHEMA_PATH = V5 / "Math_Claim_Record_Schema_v5_4.json"
LEGACY_CONSTRUCTOR_PATH = REPO / "Docs/tools/generate_math_catalog_v5_3.py"
CURRENT_PATH = V5 / "Current_Release.json"
LOCK_PATH = V5 / ".Current_Release.lock"

RELEASE = "5.6"
PARENT_RELEASE = "5.5"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386-FULL"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
FULL_SOURCE_SHA = "7075e0bb151182ae4ba01cd34945657969be4bc60f7ee4ae6a62fc518f5386c3"
FULL_SOURCE_SIZE = 10_473_933
FULL_SOURCE_CONTENT_DIGEST = "cd54f6600e733f780153ba8d5f0d08994cb13cdd0ece1d63697f33e4eddf2ece"
QUALIFIED_LEDGER_SHA = "b03a2a3df17165b7f1e4bff7e2de80a8ecea6060a115b0fed66975827fb0f039"
QUALIFIED_INVENTORY_SHA = "669ad0d5b3f7d4b26000ffc36c153f5d415fdce4f7824f85177d999a80d34ab9"
QUALIFIED_INVENTORY_AUTHORITY = "879111d857fc5ce18a4baaf1cc1e98a3aee524f9c7dd5a7736dbd2ca61d370e1"
ACCEPTED_SET_SHA = "7943e8f473aaac523d617a8debd1dda5d589187bf62844933af684172570ab86"
GENERATOR_RECEIPT_SHA = "cc3236b5b91976d9ec876548ee7de6289313c7737d1ffeee019ba1f16916a7a4"
GENERATOR_RECEIPT_AUTHORITY = "c528aba0e081b912c4102e1fea1c54e5adda49662c0bde9a94c994bddb27ebe5"
PARENT_ROOT = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"
PARENT_MANIFEST_SHA = "773253c2afad3a91c1b14cc9b5f60b51ec9b7e258d1619f0168dd23c9c4b0a43"
PARENT_CATALOG_SHA = "9d6dc79b1cbdee401f2f022ee027557a04331fa9605dc7f443fdc09a62b029b4"
PARENT_REGISTRY_AUTHORITY = "c19b24eee38ecba5634b1420da3f737694bce4a0732f3b5ca7a5cc9f9f40d203"
PARENT_CURRENT_SHA = "d7237b2877787fb18068b0d8b9504e90cc81ad0d58806b413b10dfb12d9cacce"
PARENT_ATV_HIGH = 8_009
PARENT_ATF_HIGH = 7_779
LAST_ATV = 9_009
LAST_ATF = 8_779
READY_ROWS = 1_092
QUARANTINE_ROWS = 469
QUALIFIED_ROWS = 1_561
NEW_ROWS = 1_000
INDIVIDUAL_ROWS = 511
BALANCED_ROWS = 489
TERMINAL_UNSELECTED_ROWS = 92

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
    "Strict_Conjecture_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"
ALL_RELEASE_FILES = frozenset((*RELEASE_FILES, MANIFEST_NAME))
AUTHORITY_POLICY = (
    "sha256 over UTF-8 json.dumps(value, ensure_ascii=False, sort_keys=True, "
    "separators=(',', ':')) after removing only the top-level authority_sha256 field"
)
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")


class GenerationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GenerationError(message)


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise GenerationError(f"value is not canonical JSON: {error}") from error


def document_bytes(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha_bytes(canonical({key: item for key, item in value.items() if key not in omitted}))


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def verify_seal(value: Mapping[str, Any], label: str) -> None:
    require(value.get("authority_sha256") == hash_without(value, "authority_sha256"), f"{label} seal is stale")


def set_digest(values: Iterable[str]) -> str:
    return sha_bytes(canonical(sorted(values)))


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        pairs_seen: list[str] = []

        def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise GenerationError(f"duplicate JSON key {key!r} in {path}")
                result[key] = value
                pairs_seen.append(key)
            return result

        value = json.loads(text, object_pairs_hook=no_duplicates, parse_constant=lambda x: (_ for _ in ()).throw(GenerationError(f"non-finite JSON {x}")))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GenerationError(f"cannot load {path}: {error}") from error
    require(isinstance(value, dict), f"{path} is not a JSON object")
    return value


def load_jsonl(path: Path, expected_sha: str, expected_rows: int) -> list[dict[str, Any]]:
    payload = path.read_bytes()
    require(sha_bytes(payload) == expected_sha, f"{path.name} SHA-256 drifted")
    rows: list[dict[str, Any]] = []
    for number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"{path.name} line {number} is blank")
        try:
            row = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise GenerationError(f"invalid {path.name} line {number}: {error}") from error
        require(isinstance(row, dict), f"{path.name} line {number} is not an object")
        require(raw == canonical(row), f"{path.name} line {number} is not canonical JSON")
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"{path.name} line {number} row seal is stale")
        rows.append(row)
    require(len(rows) == expected_rows, f"{path.name} row count drifted")
    return rows


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def write_immutable(path: Path, payload: bytes, check: bool) -> None:
    if check:
        require(path.is_file() and path.read_bytes() == payload, f"missing or stale artifact: {relative(path)}")
    elif path.exists():
        require(path.read_bytes() == payload, f"refusing to rewrite unequal immutable artifact: {relative(path)}")
    else:
        atomic_write(path, payload)


def artifact_binding(path: Path, document: Mapping[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": relative(path),
        "file_sha256": sha_file(path),
        "size_bytes": path.stat().st_size,
    }
    if document is not None:
        result["authority_sha256"] = document["authority_sha256"]
        result["schema_version"] = document.get("schema_version")
    return result


def load_parent() -> dict[str, dict[str, Any]]:
    require(sha_file(PARENT_DIR / MANIFEST_NAME) == PARENT_MANIFEST_SHA, "5.5 manifest bytes drifted")
    require(sha_file(PARENT_DIR / "Claim_Catalog.json") == PARENT_CATALOG_SHA, "5.5 catalog bytes drifted")
    result: dict[str, dict[str, Any]] = {}
    for name in ALL_RELEASE_FILES:
        value = load_json(PARENT_DIR / name)
        verify_seal(value, f"5.5 {name}")
        result[name] = value
    manifest = result[MANIFEST_NAME]
    require(manifest.get("release_root_sha256") == PARENT_ROOT, "5.5 release root drifted")
    for binding in manifest.get("artifacts", []):
        path = PARENT_DIR / binding["path"]
        require(sha_file(path) == binding["sha256"] and path.stat().st_size == binding["size_bytes"], f"5.5 artifact drifted: {path.name}")
    registry = result["Claim_ID_Registry.json"]
    require(registry.get("authority_sha256") == PARENT_REGISTRY_AUTHORITY, "5.5 registry authority drifted")
    require(registry.get("namespace_high_watermarks") == {"ATF": PARENT_ATF_HIGH, "ATO": PARENT_ATV_HIGH, "ATS": PARENT_ATV_HIGH, "ATV": PARENT_ATV_HIGH}, "5.5 high-watermarks drifted")
    return result


def load_source() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    require(sha_file(FULL_SOURCE) == FULL_SOURCE_SHA and FULL_SOURCE.stat().st_size == FULL_SOURCE_SIZE, "full mathlib source drifted")
    document = load_json(FULL_SOURCE)
    require(document.get("content_digest_before_self_field") == FULL_SOURCE_CONTENT_DIGEST, "full source content digest drifted")
    require(document.get("source_snapshot", {}).get("commit") == MATHLIB_COMMIT, "mathlib commit drifted")
    rows = document.get("records")
    require(isinstance(rows, list) and len(rows) == 2_566 and all(isinstance(row, dict) for row in rows), "full source denominator drifted")
    index = {row["source_record_id"]: row for row in rows}
    require(len(index) == len(rows), "full source IDs are not unique")
    return document, rows, index


def load_candidate_inputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    ready = load_jsonl(ACCEPTED_SET, ACCEPTED_SET_SHA, READY_ROWS)
    qualified = load_jsonl(QUALIFIED_LEDGER, QUALIFIED_LEDGER_SHA, QUALIFIED_ROWS)
    require(sha_file(QUALIFIED_INVENTORY) == QUALIFIED_INVENTORY_SHA, "qualified inventory bytes drifted")
    inventory = load_json(QUALIFIED_INVENTORY)
    verify_seal(inventory, "qualified inventory")
    require(inventory.get("authority_sha256") == QUALIFIED_INVENTORY_AUTHORITY, "qualified inventory authority drifted")
    require([row.get("acceptance_rank") for row in ready] == list(range(1, READY_ROWS + 1)), "ready ranks are not dense")
    require([row.get("candidate_index") for row in qualified] == list(range(1, QUALIFIED_ROWS + 1)), "qualified indexes are not dense")
    q_by_key = {row["candidate_key"]: row for row in qualified}
    require(len(q_by_key) == QUALIFIED_ROWS, "qualified candidate keys are not unique")
    for row in ready:
        source = q_by_key.get(row["candidate_key"])
        require(source is not None, "ready row is absent from qualified denominator")
        require(source.get("row_sha256") == row.get("qualified_candidate_row_sha256"), "ready-to-qualified row binding drifted")
        require(source.get("generator_lane") == "provisional_generator_admission" and source.get("generator_admission_qualified") is True, "ready row is not in provisional lane")
    require(sum(row.get("generator_lane") == "provisional_generator_admission" for row in qualified) == READY_ROWS, "ready qualified count drifted")
    require(sum(row.get("generator_lane") == "semantic_variant_review_quarantine" for row in qualified) == QUARANTINE_ROWS, "quarantine count drifted")
    return ready, qualified, inventory


def selected_ready_rows(ready: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    individualized = sorted(
        (row for row in ready if row.get("documentation_status") == "individual_declaration_docstring"),
        key=lambda row: (row["acceptance_rank"], row["candidate_key"]),
    )
    require(len(individualized) == INDIVIDUAL_ROWS, "individual-docstring count drifted")
    module_rows = [row for row in ready if row.get("documentation_status") == "module_main_result_description"]
    require(len(module_rows) == READY_ROWS - INDIVIDUAL_ROWS, "module-description count drifted")
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in module_rows:
        buckets[str(row["module_root"])].append(row)
    for rows in buckets.values():
        rows.sort(key=lambda row: (row["acceptance_rank"], row["candidate_key"]))
    offsets = {root: 0 for root in buckets}
    balanced: list[dict[str, Any]] = []
    while len(balanced) < BALANCED_ROWS:
        advanced = False
        for root in sorted(buckets):
            offset = offsets[root]
            if offset >= len(buckets[root]):
                continue
            balanced.append(buckets[root][offset])
            offsets[root] += 1
            advanced = True
            if len(balanced) == BALANCED_ROWS:
                break
        require(advanced, "module-root sweep exhausted before quota")
    selected = individualized + balanced
    selected_keys = {row["candidate_key"] for row in selected}
    terminal = [row for row in ready if row["candidate_key"] not in selected_keys]
    require(len(selected) == NEW_ROWS and len(terminal) == TERMINAL_UNSELECTED_ROWS, "selection cardinality drifted")
    require(len(selected_keys) == NEW_ROWS, "selected candidate keys are not unique")
    require(Counter(row["source_syntax_kind"] for row in selected) == Counter({"theorem": 629, "lemma": 371}), "selected source-syntax partition drifted")
    require(Counter(row["module_root"] for row in terminal) == Counter({"Analysis": 15, "RingTheory": 77}), "terminal ready distribution drifted")
    return selected, terminal


def load_generator_receipt(
    ready: Sequence[dict[str, Any]], qualified: Sequence[dict[str, Any]], inventory: Mapping[str, Any]
) -> dict[str, Any]:
    require(sha_file(GENERATOR_ACCEPTANCE_RECEIPT) == GENERATOR_RECEIPT_SHA, "generator acceptance receipt bytes drifted")
    receipt = load_json(GENERATOR_ACCEPTANCE_RECEIPT)
    verify_seal(receipt, "generator acceptance receipt")
    require(receipt.get("authority_sha256") == GENERATOR_RECEIPT_AUTHORITY, "generator acceptance receipt authority drifted")
    counts = receipt.get("counts", {})
    require(counts.get("machine_qualified_accepted_set") == len(ready) == READY_ROWS, "generator receipt ready count drifted")
    require(counts.get("semantic_variant_review_quarantine") == QUARANTINE_ROWS, "generator receipt quarantine count drifted")
    require(counts.get("unadmitted_canonical_candidates") == len(qualified) == QUALIFIED_ROWS, "generator receipt qualified count drifted")
    require(counts.get("theorem_credits_granted_by_receipt") == 0 and receipt.get("release_mutation_authorized_or_performed") is False, "candidate receipt crossed release boundary")
    require(receipt.get("inputs", {}).get("qualified_batch_inventory", {}).get("sha256") == QUALIFIED_INVENTORY_SHA and inventory.get("authority_sha256") == QUALIFIED_INVENTORY_AUTHORITY, "generator receipt inventory binding drifted")
    require(receipt.get("output", {}).get("sha256") == ACCEPTED_SET_SHA and receipt.get("output", {}).get("rows") == READY_ROWS, "generator receipt accepted-set binding drifted")
    return receipt


def build_selection(ready: Sequence[dict[str, Any]], qualified: Sequence[dict[str, Any]]) -> dict[str, Any]:
    selected, terminal = selected_ready_rows(ready)
    selected_rank = {row["candidate_key"]: rank for rank, row in enumerate(selected, 1)}
    individual_keys = {row["candidate_key"] for row in selected[:INDIVIDUAL_ROWS]}
    terminal_keys = {row["candidate_key"] for row in terminal}
    ready_by_key = {row["candidate_key"]: row for row in ready}
    dispositions: list[dict[str, Any]] = []
    for qualified_row in qualified:
        key = qualified_row["candidate_key"]
        ready_row = ready_by_key.get(key)
        rank = selected_rank.get(key)
        if rank is not None:
            phase = "individual_declaration_docstring_priority" if key in individual_keys else "module_root_round_robin"
            reason = "all_individual_declaration_docstrings_first" if key in individual_keys else "domain_balanced_module_root_sweep"
            disposition = "selected_for_joint_5_6_release_transaction"
            selected_for_joint = True
            grants = False
            target_variant = None
            target_s5 = None
        elif key in terminal_keys:
            phase = None
            reason = "release_cap_reached_after_documentation_priority_and_balanced_sweep"
            disposition = "terminal_ready_unselected_in_5_6"
            selected_for_joint = False
            grants = False
            target_variant = None
            target_s5 = None
        else:
            require(qualified_row.get("generator_lane") == "semantic_variant_review_quarantine", "non-ready row escaped quarantine")
            phase = None
            reason = "semantic_alias_or_family_signal_requires_human_review"
            disposition = "preserved_semantic_variant_review_quarantine"
            selected_for_joint = False
            grants = False
            target_variant = None
            target_s5 = None
        binding = qualified_row["source_binding"]
        row = {
            "candidate_key": key,
            "qualified_candidate_index": qualified_row["candidate_index"],
            "qualified_candidate_row_sha256": qualified_row["row_sha256"],
            "ready_acceptance_rank": ready_row["acceptance_rank"] if ready_row is not None else None,
            "ready_candidate_row_sha256": ready_row["row_sha256"] if ready_row is not None else None,
            "source_index": binding["source_index_zero_based"],
            "source_record_id": binding["source_record_id"],
            "source_record_sha256": binding["source_record_sha256"],
            "declaration": qualified_row["declaration"],
            "source_syntax_kind": qualified_row["source_syntax_kind"],
            "theorem_record_kind": qualified_row["theorem_record_kind"],
            "formal_type_sha256": qualified_row["formal_type_sha256"],
            "normalized_formal_type_sha256": qualified_row["normalized_formal_type_sha256"],
            "module": qualified_row["module"],
            "module_root": qualified_row["module_root"],
            "documentation_status": qualified_row["documentation_status"],
            "generator_lane": qualified_row["generator_lane"],
            "semantic_alias_evidence_sha256": sha_bytes(canonical(qualified_row["semantic_alias_evidence"])),
            "disposition": disposition,
            "reason_code": reason,
            "selection_phase": phase,
            "accepted_rank": rank,
            "selected_for_joint_release_transaction": selected_for_joint,
            "semantic_key": "mathlib-theorem-semantic/" + qualified_row["formal_type_sha256"],
            "target_variant_id": target_variant,
            "target_s5_id": target_s5,
            "grants_catalog_entry": grants,
            "grants_theorem_credit": grants,
            "row_sha256": None,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        dispositions.append(row)
    counts = Counter(row["disposition"] for row in dispositions)
    selected_rows = sorted((row for row in dispositions if row["selected_for_joint_release_transaction"]), key=lambda row: row["accepted_rank"])
    require([row["accepted_rank"] for row in selected_rows] == list(range(1, NEW_ROWS + 1)), "release ranks are not dense")
    require(counts == Counter({"selected_for_joint_5_6_release_transaction": 1_000, "terminal_ready_unselected_in_5_6": 92, "preserved_semantic_variant_review_quarantine": 469}), "selection disposition counts drifted")
    return seal({
        "schema_version": "awesome-theorems/mathlib-release-selection/5.6",
        "artifact": SELECTION_PATH.name,
        "release": RELEASE,
        "parent_release_root_sha256": PARENT_ROOT,
        "candidate_denominator_closed": True,
        "release_credit_granted_here": False,
        "ids_allocated_here": False,
        "inputs": {
            "generator_acceptance_receipt": {"path": relative(GENERATOR_ACCEPTANCE_RECEIPT), "file_sha256": GENERATOR_RECEIPT_SHA, "authority_sha256": GENERATOR_RECEIPT_AUTHORITY},
            "accepted_set": {"path": relative(ACCEPTED_SET), "file_sha256": ACCEPTED_SET_SHA, "rows": READY_ROWS},
            "qualified_ledger": {"path": relative(QUALIFIED_LEDGER), "file_sha256": QUALIFIED_LEDGER_SHA, "rows": QUALIFIED_ROWS},
            "qualified_inventory": {"path": relative(QUALIFIED_INVENTORY), "file_sha256": QUALIFIED_INVENTORY_SHA, "authority_sha256": QUALIFIED_INVENTORY_AUTHORITY},
            "full_source": {"path": relative(FULL_SOURCE), "file_sha256": FULL_SOURCE_SHA, "records": 2_566, "mathlib_commit": MATHLIB_COMMIT},
        },
        "selection_policy": {
            "release_cap": NEW_ROWS,
            "phase_1": "Select every ready row with documentation_status == individual_declaration_docstring, ordered by (ready acceptance_rank, candidate_key).",
            "phase_1_rows": INDIVIDUAL_ROWS,
            "phase_2": "Bucket remaining ready rows by module_root; order each bucket by (ready acceptance_rank, candidate_key); visit module roots in Unicode byte order repeatedly until 489 rows are selected.",
            "phase_2_rows": BALANCED_ROWS,
            "hidden_truncation": False,
            "ready_unselected_terminal": True,
            "quarantine_preserved": True,
        },
        "quality_boundary": {
            "formal_truth": "All selected rows are Lean ConstantInfo.thmInfo declarations at the pinned commit and the batch axiom union excludes sorryAx.",
            "identity": "The credit unit is one canonical formal proposition identity after exact/normalized formal-type and full-declaration-name gates.",
            "semantic_limit": "No listed alias/family signal is not proof of distinct human-level theorem identity; exhaustive proposition-level semantic review was not performed.",
            "importance_limit": "Selection is supported by individual declaration docstrings or module Main-result signals, not by an independent universal landmark ranking.",
            "source_syntax": "Lean theorem and lemma commands both elaborate to thmInfo; source syntax is retained and never presented as a separate credit.",
        },
        "counts": {
            "qualified_denominator": QUALIFIED_ROWS,
            "ready_denominator": READY_ROWS,
            "selected": NEW_ROWS,
            "selected_individual_declaration_docstring": INDIVIDUAL_ROWS,
            "selected_module_main_result_description": BALANCED_ROWS,
            "selected_source_syntax_theorem": 629,
            "selected_source_syntax_lemma": 371,
            "terminal_ready_unselected": TERMINAL_UNSELECTED_ROWS,
            "terminal_ready_unselected_analysis": 15,
            "terminal_ready_unselected_ring_theory": 77,
            "preserved_quarantine": QUARANTINE_ROWS,
        },
        "set_digests": {
            "all_disposition_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in dispositions),
            "selected_candidate_key_set_sha256": set_digest(row["candidate_key"] for row in selected_rows),
            "selected_formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in selected_rows),
            "selected_source_record_id_set_sha256": set_digest(row["source_record_id"] for row in selected_rows),
            "selected_acceptance_rank_set_sha256": set_digest(str(row["accepted_rank"]) for row in selected_rows),
            "terminal_ready_candidate_key_set_sha256": set_digest(row["candidate_key"] for row in dispositions if row["disposition"] == "terminal_ready_unselected_in_5_6"),
            "quarantine_candidate_key_set_sha256": set_digest(row["candidate_key"] for row in dispositions if row["disposition"] == "preserved_semantic_variant_review_quarantine"),
        },
        "candidate_dispositions": dispositions,
    })


def build_release_allocation(selection: Mapping[str, Any]) -> dict[str, Any]:
    """Allocate release identities without rewriting the non-credit selection.

    The selection artifact records a candidate decision and deliberately has
    no catalog credit or IDs.  This second ledger is the authenticated join
    between that decision and release 5.6.  Its credit is effective only when
    the matching release manifest is accepted and published.
    """

    verify_seal(selection, "mathlib release selection")
    selected = sorted(
        (
            row
            for row in selection["candidate_dispositions"]
            if row.get("selected_for_joint_release_transaction") is True
        ),
        key=lambda row: row["accepted_rank"],
    )
    require(len(selected) == NEW_ROWS, "release-allocation source count drifted")
    require(
        [row["accepted_rank"] for row in selected] == list(range(1, NEW_ROWS + 1)),
        "release-allocation ranks are not dense",
    )
    accepted_rows: list[dict[str, Any]] = []
    for row in selected:
        rank = int(row["accepted_rank"])
        atv = f"ATV-{PARENT_ATV_HIGH + rank:08d}"
        stage = f"S5-CLM-{PARENT_ATV_HIGH + rank:08d}"
        accepted = {
            "candidate_key": row["candidate_key"],
            "selection_row_sha256": row["row_sha256"],
            "qualified_candidate_row_sha256": row["qualified_candidate_row_sha256"],
            "ready_candidate_row_sha256": row["ready_candidate_row_sha256"],
            "source_index": row["source_index"],
            "source_record_id": row["source_record_id"],
            "source_record_sha256": row["source_record_sha256"],
            "declaration": row["declaration"],
            "source_syntax_kind": row["source_syntax_kind"],
            "formal_type_sha256": row["formal_type_sha256"],
            "semantic_key": row["semantic_key"],
            "selection_phase": row["selection_phase"],
            "reason_code": row["reason_code"],
            "accepted_rank": rank,
            "transition_from_disposition": row["disposition"],
            "disposition": "accepted_new_kernel_checked_formal_theorem",
            "target_family_id": f"ATF-{PARENT_ATF_HIGH + rank:08d}",
            "target_occurrence_id": f"ATO-{PARENT_ATV_HIGH + rank:08d}",
            "target_sense_id": f"ATS-{PARENT_ATV_HIGH + rank:08d}",
            "target_variant_id": atv,
            "target_s5_id": stage,
            "grants_catalog_entry": True,
            "grants_theorem_credit": True,
            "credit_effective_boundary": "authenticated_published_stage5_release_5_6_only",
            "row_sha256": None,
        }
        accepted["row_sha256"] = hash_without(accepted, "row_sha256")
        accepted_rows.append(accepted)
    require(
        len({row["candidate_key"] for row in accepted_rows}) == NEW_ROWS
        and len({row["formal_type_sha256"] for row in accepted_rows}) == NEW_ROWS,
        "release-allocation identities are not unique",
    )
    return seal({
        "schema_version": "awesome-theorems/mathlib-release-allocation/5.6",
        "artifact": ALLOCATION_PATH.name,
        "release": RELEASE,
        "parent_release_root_sha256": PARENT_ROOT,
        "selection_binding": {
            "path": relative(SELECTION_PATH),
            "file_sha256": sha_file(SELECTION_PATH),
            "authority_sha256": selection["authority_sha256"],
            "selected_rows": NEW_ROWS,
        },
        "allocation_policy": {
            "append_only": True,
            "one_formal_identity_per_credit": True,
            "parent_prefix_rewrite_forbidden": True,
            "putnam_seed_variant_relation_credit": 0,
            "credit_effective_boundary": "authenticated_published_stage5_release_5_6_only",
        },
        "counts": {
            "accepted_rows": NEW_ROWS,
            "theorem_credits": NEW_ROWS,
            "catalog_entries": NEW_ROWS,
            "putnam_credits": 0,
        },
        "ranges": {
            "ATF": [PARENT_ATF_HIGH + 1, LAST_ATF],
            "ATO": [PARENT_ATV_HIGH + 1, LAST_ATV],
            "ATS": [PARENT_ATV_HIGH + 1, LAST_ATV],
            "ATV": [PARENT_ATV_HIGH + 1, LAST_ATV],
            "S5_CLM": [PARENT_ATV_HIGH + 1, LAST_ATV],
        },
        "set_digests": {
            "accepted_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in accepted_rows),
            "candidate_key_set_sha256": set_digest(row["candidate_key"] for row in accepted_rows),
            "formal_type_sha256_set_sha256": set_digest(row["formal_type_sha256"] for row in accepted_rows),
            "variant_id_set_sha256": set_digest(row["target_variant_id"] for row in accepted_rows),
            "stage_claim_id_set_sha256": set_digest(row["target_s5_id"] for row in accepted_rows),
        },
        "accepted_rows": accepted_rows,
    })


def build_schema() -> dict[str, Any]:
    schema = copy.deepcopy(load_json(BASE_SCHEMA_PATH))
    schema.pop("authority_sha256", None)
    schema["$id"] = "https://example.invalid/awesome-theorems/stage5/math-claim-record-5.6.schema.json"
    schema["title"] = "Closed Stage5 release 5.6 mathlib formal-theorem claim record"
    schema["description"] = "Exact closed schema for only the 1,000 origin-5.6 formal theorem records; inherited 5.5 records retain their original schemas."
    schema["authority_hash_policy"] = AUTHORITY_POLICY
    props = schema["properties"]
    props["schema_version"] = {"const": "awesome-theorems/stage5-math-claim-record/5.6"}
    props["release_id"] = {"const": RELEASE}
    props["origin_release"] = {"const": RELEASE}
    props["source_id"] = {"const": SOURCE_ID}
    allocation = schema["$defs"]["allocation"]["properties"]
    allocation["parent_registry_authority_sha256"] = {"const": PARENT_REGISTRY_AUTHORITY}
    allocation["parent_release_root_sha256"] = {"const": PARENT_ROOT}
    curator = schema["$defs"]["curator_disposition"]["properties"]
    curator["accepted_rank"]["maximum"] = NEW_ROWS
    curator["curation_ledger_path"] = {"const": relative(ALLOCATION_PATH)}
    curator["disposition"] = {"const": "accepted_new_kernel_checked_formal_theorem"}
    curator["reason_code"] = {"enum": ["all_individual_declaration_docstrings_first", "domain_balanced_module_root_sweep"]}
    curator["source_index"]["maximum"] = 2_565
    dedupe = schema["$defs"]["dedupe"]["properties"]
    dedupe["parent_catalog_file_sha256"] = {"const": PARENT_CATALOG_SHA}
    dedupe["verdict"] = {"const": "unique_formal_identity_after_parent_and_batch_exact_gates"}
    dedupe["validation_status"] = {"const": "exact_identity_and_alias_signal_screened_not_exhaustive_human_semantic_dedup"}
    formal = schema["$defs"]["formal_statement"]["properties"]
    formal["declaration_kind"] = {"enum": ["theorem", "lemma"]}
    formal["source_syntax_kind"] = {"enum": ["theorem", "lemma"]}
    provenance = schema["$defs"]["provenance"]["properties"]
    provenance["formal_source_ref"] = {"const": SOURCE_ID}
    provenance["source_asset_sha256"] = {"const": FULL_SOURCE_SHA}
    locator = schema["$defs"]["source_locator"]["properties"]
    locator["artifact_path"] = {"const": relative(FULL_SOURCE)}
    locator["artifact_sha256"] = {"const": FULL_SOURCE_SHA}
    locator["artifact_size_bytes"] = {"const": FULL_SOURCE_SIZE}
    locator["record_index"]["maximum"] = 2_565
    locator["source_id"] = {"const": SOURCE_ID}
    schema["$defs"]["source_ref_array"]["items"] = {"const": SOURCE_ID}
    selection = schema["$defs"]["theorem_selection"]["properties"]
    selection["phase_rank"]["maximum"] = NEW_ROWS
    selection["selection_rank"]["maximum"] = 2_566
    selection["selection_phase"] = {"enum": ["individual_declaration_docstring_priority", "module_root_round_robin"]}
    return seal(schema)


def build_parent_receipt(parent: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    manifest = parent[MANIFEST_NAME]
    inventory = []
    for name in sorted(ALL_RELEASE_FILES):
        path = PARENT_DIR / name
        inventory.append({"path": relative(path), "file_sha256": sha_file(path), "size_bytes": path.stat().st_size, "authority_sha256": parent[name]["authority_sha256"]})
    return seal({
        "schema_version": "awesome-theorems/stage5-parent-receipt/5.6",
        "artifact": PARENT_RECEIPT_PATH.name,
        "parent_release": PARENT_RELEASE,
        "parent_release_root_sha256": PARENT_ROOT,
        "parent_manifest_file_sha256": PARENT_MANIFEST_SHA,
        "parent_manifest_authority_sha256": manifest["authority_sha256"],
        "parent_registry_authority_sha256": PARENT_REGISTRY_AUTHORITY,
        "parent_counts": copy.deepcopy(manifest["counts"]),
        "parent_namespace_high_watermarks": copy.deepcopy(parent["Claim_ID_Registry.json"]["namespace_high_watermarks"]),
        "artifacts": inventory,
        "verification": "All nine 5.5 release files, top-level seals, manifest inventory bindings, and release root were replayed before 5.6 construction.",
    })


def build_source_registry(
    selection: Mapping[str, Any], allocation: Mapping[str, Any], receipt: Mapping[str, Any]
) -> dict[str, Any]:
    return seal({
        "schema_version": "awesome-theorems/stage5-math-source-registry/5.6",
        "registry_status": "closed_pinned_mathlib_full_source_for_exact_5_6_transaction",
        "reviewed_as_of": "2026-08-10",
        "authority_hash_policy": AUTHORITY_POLICY,
        "additional_sources_allowed": False,
        "source_record_contract": {
            "additional_fields_allowed": False,
            "source_record_required_fields": ["declaration", "declaration_docstring", "declaration_kind", "display_label", "exact_curated_summary", "formal_docstring", "formal_docstring_origin", "formal_docstring_sha256", "formal_proof_state", "formal_type", "formal_type_sha256", "importance_signals", "material_status", "msc2020", "proof_evidence", "raw_category", "raw_status", "rights", "selection_cohort", "selection_rank", "source", "source_record_id", "source_syntax_kind"],
            "release_join_fields": ["source_record_id", "source_record_sha256", "formal_type_sha256", "declaration", "source.module"],
            "unknown_source_facts_grant_credit": False,
        },
        "sources": [{
            "source_id": SOURCE_ID,
            "title": "Pinned full mathlib verified theorem source at 8a178386",
            "source_type": "formal_library_runtime_extraction",
            "source_roles": ["formal_statement", "proof_state", "documentation_signal", "classification_hint"],
            "authority": "Lean compiled ConstantInfo.thmInfo plus collectAxioms at the pinned commit",
            "release_eligibility": "only rows selected by the sealed 5.6 release-selection ledger",
            "asset": {"path": relative(FULL_SOURCE), "file_sha256": FULL_SOURCE_SHA, "size_bytes": FULL_SOURCE_SIZE, "content_digest_before_self_field": FULL_SOURCE_CONTENT_DIGEST, "records": 2_566},
            "snapshot": {"repository": "https://github.com/leanprover-community/mathlib4.git", "commit": MATHLIB_COMMIT, "license": "Apache-2.0", "license_sha256": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"},
            "selection_binding": {"path": relative(SELECTION_PATH), "file_sha256": sha_file(SELECTION_PATH), "authority_sha256": selection["authority_sha256"], "selected": NEW_ROWS, "terminal_ready_unselected": TERMINAL_UNSELECTED_ROWS, "quarantine": QUARANTINE_ROWS},
            "release_allocation_binding": {"path": relative(ALLOCATION_PATH), "file_sha256": sha_file(ALLOCATION_PATH), "authority_sha256": allocation["authority_sha256"], "accepted": NEW_ROWS},
            "generator_acceptance_binding": {"path": relative(GENERATOR_ACCEPTANCE_RECEIPT), "file_sha256": sha_file(GENERATOR_ACCEPTANCE_RECEIPT), "authority_sha256": receipt["authority_sha256"], "ready": READY_ROWS},
            "truth_boundary": "Pinned formal truth only; later commits are not inferred.",
            "importance_boundary": "Documentation/Main-result signal, not independent universal ranking.",
            "semantic_identity_boundary": "Formal identity and alias-signal screening, not exhaustive human semantic equivalence review.",
            "rights": {"formal_code_and_docstrings": "Apache-2.0 with mathlib attribution", "optional_1000_plus_metadata": "Unlicense where present", "catalog_relicenses_source": False},
        }],
        "counts": {"sources": 1, "asset_records": 2_566, "qualified_candidates": QUALIFIED_ROWS, "ready_candidates": READY_ROWS, "selected_release_rows": NEW_ROWS, "terminal_ready_unselected": TERMINAL_UNSELECTED_ROWS, "quarantine_preserved": QUARANTINE_ROWS},
    })


def build_contract(
    schema: Mapping[str, Any],
    registry: Mapping[str, Any],
    parent_receipt: Mapping[str, Any],
    selection: Mapping[str, Any],
    allocation: Mapping[str, Any],
    generator_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    return seal({
        "schema_version": "awesome-theorems/stage5-math-expansion-contract/5.6",
        "contract_status": "normative_closed_exact_1000_mathlib_formal_theorem_append",
        "stage": "Stage5",
        "release": RELEASE,
        "review_date": "2026-08-10",
        "authority_hash_policy": AUTHORITY_POLICY,
        "parent": {"release": PARENT_RELEASE, "release_root_sha256": PARENT_ROOT, "manifest_file_sha256": PARENT_MANIFEST_SHA, "catalog_records": 4_525, "theorem_records": 2_500, "open_claim_records": 2_025, "effective_strict_conjecture_credits": 1_425, "variant_high_watermark": PARENT_ATV_HIGH, "family_high_watermark": PARENT_ATF_HIGH},
        "quantity_gates": {"origin_theorems_exact": NEW_ROWS, "cumulative_theorems_exact": 3_500, "catalog_records_exact": 5_525, "open_claims_conserved": 2_025, "strict_conjectures_conserved": 1_425, "dynamic_theorem_expansion_bound": [500, 1_000]},
        "selection_gates": {"qualified_denominator": QUALIFIED_ROWS, "ready_denominator": READY_ROWS, "selected": NEW_ROWS, "individual_docstring_priority": INDIVIDUAL_ROWS, "module_root_round_robin": BALANCED_ROWS, "terminal_ready_unselected": TERMINAL_UNSELECTED_ROWS, "quarantine_preserved": QUARANTINE_ROWS, "formal_variants_or_relation_edges_grant_theorem_credit": False, "putnam_problem_seeds_grant_theorem_credit": False},
        "identity_allocation": {"append_only": True, "parent_prefix_rewrite_forbidden": True, "ATF": [7_780, 8_779], "ATO": [8_010, 9_009], "ATS": [8_010, 9_009], "ATV": [8_010, 9_009], "S5_CLM": [8_010, 9_009], "one_formal_identity_per_credit": True},
        "quality_gates": {"kernel_checked_sorry_free_exact": NEW_ROWS, "selected_individual_declaration_docstring": INDIVIDUAL_ROWS, "selected_module_main_result_description": BALANCED_ROWS, "source_syntax_theorem": 629, "source_syntax_lemma": 371, "human_semantic_uniqueness_claimed": False, "independent_universal_importance_ranking_claimed": False, "quality_limit_must_be_reported": True},
        "release_layout": {"root": relative(RELEASE_DIR), "manifest_name": MANIFEST_NAME, "manifest_excluded_from_release_root": True, "non_manifest_artifacts": list(RELEASE_FILES), "release_root_formula": "sha256(canonical_json(sorted([{path,sha256,size_bytes}], key=path)))"},
        "publication": {"write_does_not_publish": True, "compare_and_swap_parent_pointer_file_sha256": PARENT_CURRENT_SHA, "publish_current_requires_exact_5_5_or_idempotent_5_6": True, "independent_checker_required": True, "independent_acceptance_receipt_path": "Docs/catalog/v5/receipts/V5_6_Independent_Acceptance_Receipt.json"},
        "versioned_authorities": {
            "record_schema": artifact_binding(SCHEMA_PATH, schema),
            "source_registry": artifact_binding(SOURCE_REGISTRY_PATH, registry),
            "parent_receipt": artifact_binding(PARENT_RECEIPT_PATH, parent_receipt),
            "release_selection": artifact_binding(SELECTION_PATH, selection),
            "release_allocation": artifact_binding(ALLOCATION_PATH, allocation),
            "generator_acceptance_receipt": artifact_binding(GENERATOR_ACCEPTANCE_RECEIPT, generator_receipt),
        },
        "acceptance_commands": [
            "python3 Docs/catalog/v5/curation/mathlib_reserve_v5_6/build_mathlib_generator_accepted_set_v5_6.py",
            "python3 Docs/catalog/v5/tools/generate_math_catalog_v5_6.py --check",
            "python3 Docs/catalog/v5/tools/check_math_catalog_v5_6.py --prepublish",
            "python3 -m unittest Docs.catalog.v5.tests.test_math_catalog_v5_6",
            "python3 Docs/catalog/v5/tools/render_math_catalog_v5_6.py --check",
        ],
    })


def materialize_pre_release_authorities(parent: Mapping[str, Mapping[str, Any]], ready: Sequence[dict[str, Any]], qualified: Sequence[dict[str, Any]], inventory: Mapping[str, Any], check: bool) -> dict[str, dict[str, Any]]:
    receipt = load_generator_receipt(ready, qualified, inventory)
    selection = build_selection(ready, qualified)
    write_immutable(SELECTION_PATH, document_bytes(selection), check)
    allocation = build_release_allocation(selection)
    write_immutable(ALLOCATION_PATH, document_bytes(allocation), check)
    schema = build_schema()
    write_immutable(SCHEMA_PATH, document_bytes(schema), check)
    parent_receipt = build_parent_receipt(parent)
    write_immutable(PARENT_RECEIPT_PATH, document_bytes(parent_receipt), check)
    registry = build_source_registry(selection, allocation, receipt)
    write_immutable(SOURCE_REGISTRY_PATH, document_bytes(registry), check)
    contract = build_contract(schema, registry, parent_receipt, selection, allocation, receipt)
    write_immutable(CONTRACT_PATH, document_bytes(contract), check)
    return {"generator_receipt": receipt, "selection": selection, "allocation": allocation, "schema": schema, "parent_receipt": parent_receipt, "source_registry": registry, "contract": contract}


def load_record_constructor() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_v56_record_constructor", LEGACY_CONSTRUCTOR_PATH)
    require(spec is not None and spec.loader is not None, "cannot load legacy record constructor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.RELEASE = RELEASE
    module.PARENT_RELEASE = PARENT_RELEASE
    module.PARENT_DIR = PARENT_DIR
    module.CURATION_PATH = SELECTION_PATH
    module.SOURCE_PATH = FULL_SOURCE
    module.SOURCE_ID = SOURCE_ID
    module.SOURCE_FILE_SHA256 = FULL_SOURCE_SHA
    module.SOURCE_FILE_SIZE = FULL_SOURCE_SIZE
    module.MATHLIB_COMMIT = MATHLIB_COMMIT
    module.PARENT_ATV_HIGH_WATERMARK = PARENT_ATV_HIGH
    module.PARENT_ATF_HIGH_WATERMARK = PARENT_ATF_HIGH
    module.LAST_ATV_ORDINAL = LAST_ATV
    module.LAST_ATF_ORDINAL = LAST_ATF
    module.NEW_ROWS = NEW_ROWS
    module.validate_schema_instance = lambda *_args, **_kwargs: None
    return module


def build_new_records(parent: Mapping[str, Mapping[str, Any]], source_rows: Sequence[dict[str, Any]], source_index: Mapping[str, dict[str, Any]], authorities: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    allocation = authorities["allocation"]
    accepted = sorted(allocation["accepted_rows"], key=lambda row: row["accepted_rank"])
    require(len(accepted) == NEW_ROWS, "accepted release selection count drifted")
    constructor = load_record_constructor()
    result: list[dict[str, Any]] = []
    for ledger in accepted:
        source = source_index.get(ledger["source_record_id"])
        require(source is not None, "selected source record is missing")
        require(source_rows[ledger["source_index"]] == source, "selected source index binding drifted")
        require(sha_bytes(canonical(source)) == ledger["source_record_sha256"], "selected source row SHA drifted")
        require(source["formal_type_sha256"] == ledger["formal_type_sha256"], "selected formal type binding drifted")
        row = constructor.build_claim_row(ledger, source, PARENT_REGISTRY_AUTHORITY, PARENT_ROOT, allocation["authority_sha256"], load_json(BASE_SCHEMA_PATH))
        row["schema_version"] = "awesome-theorems/stage5-math-claim-record/5.6"
        row["theorem_selection"]["selection_phase"] = ledger["selection_phase"]
        row["theorem_selection"]["phase_rank"] = (
            ledger["accepted_rank"] if ledger["selection_phase"] == "individual_declaration_docstring_priority" else ledger["accepted_rank"] - INDIVIDUAL_ROWS
        )
        row["curator_disposition"]["curation_ledger_path"] = relative(ALLOCATION_PATH)
        row["curator_disposition"]["curation_ledger_file_sha256"] = sha_file(ALLOCATION_PATH)
        row["curator_disposition"]["curation_ledger_authority_sha256"] = allocation["authority_sha256"]
        row["dedupe"]["parent_catalog_file_sha256"] = PARENT_CATALOG_SHA
        row["dedupe"]["verdict"] = "unique_formal_identity_after_parent_and_batch_exact_gates"
        row["dedupe"]["validation_status"] = "exact_identity_and_alias_signal_screened_not_exhaustive_human_semantic_dedup"
        row["source_payload_sha256"] = sha_bytes(canonical({"source_locator": row["source_locator"], "theorem_selection": row["theorem_selection"], "provenance": row["provenance"]}))
        require(row["formal_statement"]["declaration_kind"] in {"theorem", "lemma"}, "new runtime theorem has unsupported source syntax")
        require(row["proof_evidence"]["formal_proof_state"] == "kernel_checked_sorry_free" and row["proof_evidence"]["uses_sorry"] is False and "sorryAx" not in row["proof_evidence"]["batch_axiom_dependency_union"], "new theorem proof gate failed")
        require(row["variant_id"] == ledger["target_variant_id"] and row["stage_claim_id"] == ledger["target_s5_id"], "new theorem allocation binding drifted")
        require(set(row) == set(authorities["schema"]["required"]) == set(authorities["schema"]["properties"]), "new theorem top-level schema closure drifted")
        result.append(row)
    require([row["variant_id"] for row in result] == [f"ATV-{ordinal:08d}" for ordinal in range(PARENT_ATV_HIGH + 1, LAST_ATV + 1)], "new ATV range is not dense")
    require([row["family_id"] for row in result] == [f"ATF-{ordinal:08d}" for ordinal in range(PARENT_ATF_HIGH + 1, LAST_ATF + 1)], "new ATF range is not dense")
    require(len({row["formal_statement"]["formal_type_sha256"] for row in result}) == NEW_ROWS, "selected formal types are not unique")
    return result


def authoritative_inputs(authorities: Mapping[str, Mapping[str, Any]], parent: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "contract": artifact_binding(CONTRACT_PATH, authorities["contract"]),
        "record_schema": artifact_binding(SCHEMA_PATH, authorities["schema"]),
        "source_registry": artifact_binding(SOURCE_REGISTRY_PATH, authorities["source_registry"]),
        "parent_receipt": artifact_binding(PARENT_RECEIPT_PATH, authorities["parent_receipt"]),
        "release_selection": artifact_binding(SELECTION_PATH, authorities["selection"]),
        "release_allocation": artifact_binding(ALLOCATION_PATH, authorities["allocation"]),
        "generator_acceptance_receipt": artifact_binding(GENERATOR_ACCEPTANCE_RECEIPT, authorities["generator_receipt"]),
        "accepted_set": {"path": relative(ACCEPTED_SET), "file_sha256": ACCEPTED_SET_SHA, "size_bytes": ACCEPTED_SET.stat().st_size, "rows": READY_ROWS},
        "qualified_inventory": {"path": relative(QUALIFIED_INVENTORY), "file_sha256": QUALIFIED_INVENTORY_SHA, "size_bytes": QUALIFIED_INVENTORY.stat().st_size, "authority_sha256": QUALIFIED_INVENTORY_AUTHORITY},
        "qualified_ledger": {"path": relative(QUALIFIED_LEDGER), "file_sha256": QUALIFIED_LEDGER_SHA, "size_bytes": QUALIFIED_LEDGER.stat().st_size, "rows": QUALIFIED_ROWS},
        "full_mathlib_source": {"path": relative(FULL_SOURCE), "file_sha256": FULL_SOURCE_SHA, "size_bytes": FULL_SOURCE_SIZE, "records": 2_566, "content_digest_before_self_field": FULL_SOURCE_CONTENT_DIGEST, "mathlib_commit": MATHLIB_COMMIT},
        "parent_release": {"release": PARENT_RELEASE, "release_root_sha256": PARENT_ROOT, "manifest_file_sha256": PARENT_MANIFEST_SHA, "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"], "registry_authority_sha256": PARENT_REGISTRY_AUTHORITY},
    }


def new_registry_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append({"family_id": row["family_id"], "curation_key": row["curation_key"], "display_titles": list(dict.fromkeys([row["display_name"], *row["aliases"]])), "member_occurrence_ids": [row["occurrence_id"]], "historical_member_occurrence_ids": [row["occurrence_id"]], "idempotency_request_sha256": request, "identity_state": "stage5_mathlib_formal_identity_family", "lifecycle": "current", "semantic_equivalence_asserted": False})
        senses.append({"sense_id": row["sense_id"], "family_id": row["family_id"], "bootstrap_occurrence_id": row["occurrence_id"], "curation_key": row["curation_key"], "idempotency_request_sha256": request, "identity_state": "stage5_mathlib_formal_identity_sense_without_exhaustive_human_semantic_claim", "lifecycle": "current"})
        variants.append({"variant_id": row["variant_id"], "sense_id": row["sense_id"], "bootstrap_occurrence_id": row["occurrence_id"], "curation_key": row["curation_key"], "idempotency_request_sha256": request, "semantic_payload_sha256": row["semantic_payload_sha256"], "identity_state": "stage5_mathlib_exact_formal_type_variant", "lifecycle": "current"})
    return families, senses, variants


def build_artifacts(parent: Mapping[str, Mapping[str, Any]], new_rows: Sequence[dict[str, Any]], inputs: Mapping[str, Any], authorities: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    parent_catalog = parent["Claim_Catalog.json"]
    records = copy.deepcopy(parent_catalog["records"]) + copy.deepcopy(list(new_rows))
    quality_qualification = {
        "inherited_5_5": copy.deepcopy(parent[MANIFEST_NAME]["quality_qualification"]),
        "origin_5_6": {
            "accepted_kernel_checked_sorry_free_formal_identities": NEW_ROWS,
            "selected_individual_declaration_docstring": INDIVIDUAL_ROWS,
            "selected_module_main_result_description": BALANCED_ROWS,
            "source_syntax_theorem": 629,
            "source_syntax_lemma": 371,
            "selection_authority_sha256": authorities["selection"]["authority_sha256"],
            "allocation_authority_sha256": authorities["allocation"]["authority_sha256"],
            "unsupported_formal_truth_credit": 0,
            "human_semantic_uniqueness_claimed": False,
            "independent_universal_importance_ranking_claimed": False,
        },
    }
    catalog = seal({
        "schema_version": "awesome-theorems/stage5-claim-catalog/5.6", "artifact": "Claim_Catalog.json", "release": RELEASE,
        "catalog_scope": parent_catalog["catalog_scope"], "authoritative_inputs": copy.deepcopy(inputs),
        "counts": {"records": 5_525, "origin_theorems": 1_000, "origin_open_claims": 0, "origin_strict_conjectures": 0, "cumulative_theorems": 3_500, "cumulative_open_claims": 2_025, "effective_strict_conjectures": 1_425},
        "quality_qualification": quality_qualification,
        "origin_5_6_closed_schema": {"closed": True, "origin_records": NEW_ROWS, "schema_path": relative(SCHEMA_PATH), "schema_authority_sha256": authorities["schema"]["authority_sha256"], "record_keys": sorted(authorities["schema"]["required"]), "parent_records_rewritten": False},
        "records": records,
    })
    parent_registry = parent["Claim_ID_Registry.json"]
    families, senses, variants = new_registry_rows(new_rows)
    allocation_policy = copy.deepcopy(parent_registry["allocation_policy"])
    allocation_policy.update({"release_5_6_first_new_atv_ordinal": PARENT_ATV_HIGH + 1, "release_5_6_new_family_first_atf_ordinal": PARENT_ATF_HIGH + 1, "release_5_6_credit_unit": "canonical_formal_proposition_identity_not_asserted_human_semantic_landmark"})
    registry = seal({
        "schema_version": "awesome-theorems/claim-id-registry/5.6", "artifact": "Claim_ID_Registry.json", "release": RELEASE,
        "parent_registry_authority_sha256": PARENT_REGISTRY_AUTHORITY, "baseline_registry_authority_sha256": parent_registry["baseline_registry_authority_sha256"], "authoritative_inputs": copy.deepcopy(inputs), "allocation_policy": allocation_policy,
        "namespace_high_watermarks": {"ATF": LAST_ATF, "ATO": LAST_ATV, "ATS": LAST_ATV, "ATV": LAST_ATV},
        "families": copy.deepcopy(parent_registry["families"]) + families, "senses": copy.deepcopy(parent_registry["senses"]) + senses, "variants": copy.deepcopy(parent_registry["variants"]) + variants,
        "legacy_aliases": copy.deepcopy(parent_registry["legacy_aliases"]), "redirects": copy.deepcopy(parent_registry["redirects"]), "splits": copy.deepcopy(parent_registry["splits"]), "family_membership_extensions": copy.deepcopy(parent_registry["family_membership_extensions"]),
        "counts": {"families": 8_779, "senses": 9_009, "variants": 9_009, "stage4_variants": parent_registry["counts"]["stage4_variants"], "stage5_additions": 5_525, "legacy_aliases": len(parent_registry["legacy_aliases"]), "redirects": len(parent_registry["redirects"]), "splits": len(parent_registry["splits"])},
    })
    parent_stage = parent["Stage5_Claim_ID_Registry.json"]
    mappings = copy.deepcopy(parent_stage["mappings"]) + [{"ordinal": PARENT_ATV_HIGH + rank, "variant_id": row["variant_id"], "predecessor_stage_claim_id": None, "stage_claim_id": row["stage_claim_id"], "lifecycle": "current"} for rank, row in enumerate(new_rows, 1)]
    stage = seal({"schema_version": "awesome-theorems/stage5-claim-id-registry/5.6", "artifact": "Stage5_Claim_ID_Registry.json", "release": RELEASE, "authoritative_inputs": copy.deepcopy(inputs), "numbering_policy": parent_stage["numbering_policy"], "counts": {"mappings": 9_009}, "mappings": mappings})
    parent_migration = parent["Migration_v4_to_v5.json"]
    migrations = copy.deepcopy(parent_migration["migrations"]) + [{"ordinal": PARENT_ATV_HIGH + rank, "variant_id": row["variant_id"], "v4_variant_id": None, "s4_claim_id": None, "stage_claim_id": row["stage_claim_id"], "migration_action": "new_stage5_allocation", "predecessor_record_sha256": None, "current_resolution": {"kind": "current", "terminal_atv_ids": [row["variant_id"]], "terminal_s5_ids": [row["stage_claim_id"]], "default_child": None, "evidence_inherited": False}} for rank, row in enumerate(new_rows, 1)]
    migration = seal({"schema_version": "awesome-theorems/migration-v4-to-v5/5.6", "artifact": "Migration_v4_to_v5.json", "release": RELEASE, "authoritative_inputs": copy.deepcopy(inputs), "v4_import_receipt": copy.deepcopy(parent_migration["v4_import_receipt"]), "counts": {"historical_bindings": parent_migration["counts"]["historical_bindings"], "new_allocations": 5_525, "migrations": 9_009}, "migrations": migrations})
    theorem_rows = copy.deepcopy(parent["Theorem_List.json"]["records"]) + copy.deepcopy(list(new_rows))
    theorem_ids = copy.deepcopy(parent["Theorem_List.json"]["stage_claim_ids"]) + [row["stage_claim_id"] for row in new_rows]
    theorem = seal({"schema_version": "awesome-theorems/stage5-query-projection/5.6", "artifact": "Theorem_List.json", "release": RELEASE, "authoritative_inputs": copy.deepcopy(inputs), "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically", "stage_claim_ids": theorem_ids, "counts": {"records": 3_500}, "records": theorem_rows})
    open_list = seal({"schema_version": "awesome-theorems/stage5-query-projection/5.6", "artifact": "Open_Claim_List.json", "release": RELEASE, "authoritative_inputs": copy.deepcopy(inputs), "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically", "stage_claim_ids": copy.deepcopy(parent["Open_Claim_List.json"]["stage_claim_ids"]), "counts": {"records": 2_025}, "records": copy.deepcopy(parent["Open_Claim_List.json"]["records"])})
    parent_coverage = parent["Coverage_Ledger.json"]
    coverage_additions = []
    allocated_by_key = {
        row["candidate_key"]: row for row in authorities["allocation"]["accepted_rows"]
    }
    for row in authorities["selection"]["candidate_dispositions"]:
        accepted = allocated_by_key.get(row["candidate_key"])
        effective = accepted if accepted is not None else row
        coverage_additions.append({"candidate_key": row["candidate_key"], "source_id": SOURCE_ID, "source_index": row["source_index"], "source_record_id": row["source_record_id"], "source_record_sha256": row["source_record_sha256"], "declaration": row["declaration"], "source_syntax_kind": row["source_syntax_kind"], "formal_type_sha256": row["formal_type_sha256"], "semantic_key": row["semantic_key"], "generator_lane": row["generator_lane"], "disposition": effective["disposition"], "reason_code": row["reason_code"], "accepted_rank": row["accepted_rank"], "target_variant_id": effective["target_variant_id"], "target_s5_id": effective["target_s5_id"], "grants_catalog_entry": effective["grants_catalog_entry"], "grants_theorem_credit": effective["grants_theorem_credit"], "origin_release": RELEASE, "curation_row_sha256": effective["row_sha256"], "qualified_candidate_row_sha256": row["qualified_candidate_row_sha256"], "ready_candidate_row_sha256": row["ready_candidate_row_sha256"], "supersedes_candidate_key": None, "transition_from_disposition": accepted["transition_from_disposition"] if accepted is not None else "qualified_candidate_only"})
    candidates = copy.deepcopy(parent_coverage["candidate_dispositions"]) + coverage_additions
    by_code: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in new_rows:
        by_code[str(row["classification"]["msc2020_code"])].append(row)
    msc_rows = []
    for old in parent_coverage["msc_coverage"]:
        row = copy.deepcopy(old)
        additions = by_code.pop(str(row["msc_top_class"]), [])
        ids = [item["stage_claim_id"] for item in additions]
        row["current_theorem_s5_ids"] = [*row["current_theorem_s5_ids"], *ids]
        row["origin_theorem_s5_ids"] = ids
        row["origin_open_s5_ids"] = []
        if additions:
            row["source_ids"] = sorted(set(row["source_ids"]) | {SOURCE_ID})
        exact = sum(item["classification"]["basis"] == "1000_plus_curated" for item in additions)
        row["classification_basis_counts"]["source_annotation"] += exact
        row["classification_basis_counts"]["machine_crosswalk"] += len(additions) - exact
        row["counts"]["current_theorems"] = len(row["current_theorem_s5_ids"])
        row["counts"]["current_open"] = len(row["current_open_s5_ids"])
        row["counts"]["origin_theorems"] = len(ids)
        row["counts"]["origin_open"] = 0
        row["counts"]["open_reserve"] = len(row["open_reserve_candidate_keys"])
        classified = row["counts"]["current_theorems"] + row["counts"]["current_open"] + row["counts"]["open_reserve"]
        row["scarcity"] = "zero" if classified == 0 else "thin" if classified < 10 else "adequate_in_source_inventory"
        row["scarcity_reason"] = "No current or open-reserve member has this primary source annotation." if classified == 0 else "Fewer than ten current-plus-reserve members have this primary class." if classified < 10 else "At least ten current-plus-reserve members have this primary class."
        msc_rows.append(row)
    require(not by_code, f"unknown MSC codes in new rows: {sorted(by_code)}")
    coverage = seal({"schema_version": "awesome-theorems/stage5-coverage-ledger/5.6", "release": RELEASE, "authoritative_inputs": copy.deepcopy(inputs), "effective_state_policy": {"identity_fields": ["source_id", "source_record_id"], "historical_parent_rows_are_immutable": True, "origin_5_6_candidate_denominator_closed": True, "release_selection_dispositions_terminal": ["accepted_new_kernel_checked_formal_theorem", "terminal_ready_unselected_in_5_6", "preserved_semantic_variant_review_quarantine"]}, "candidate_dispositions": candidates, "msc_coverage": msc_rows, "counts": {"candidate_dispositions": len(candidates), "msc_coverage": len(msc_rows), "origin_5_6_candidates": QUALIFIED_ROWS, "origin_5_6_accepted_new_theorems": NEW_ROWS, "origin_5_6_terminal_ready_unselected": TERMINAL_UNSELECTED_ROWS, "origin_5_6_quarantine_preserved": QUARANTINE_ROWS}})
    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    strict = seal({"schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.6", "release": RELEASE, "parent_release_root_sha256": PARENT_ROOT, "parent_strict_ledger_file_sha256": sha_file(PARENT_DIR / "Strict_Conjecture_Ledger.json"), "parent_strict_ledger_authority_sha256": parent_strict["authority_sha256"], "strict_credits": copy.deepcopy(parent_strict["strict_credits"]), "credit_corrections": copy.deepcopy(parent_strict["credit_corrections"]), "counts": copy.deepcopy(parent_strict["counts"]), "set_digests": copy.deepcopy(parent_strict["set_digests"]), "origin_5_6_change": {"strict_credits_added": 0, "strict_credits_removed": 0, "credit_corrections_added": 0}})
    return {"Claim_Catalog.json": catalog, "Claim_ID_Registry.json": registry, "Stage5_Claim_ID_Registry.json": stage, "Migration_v4_to_v5.json": migration, "Theorem_List.json": theorem, "Open_Claim_List.json": open_list, "Coverage_Ledger.json": coverage, "Strict_Conjecture_Ledger.json": strict}


def row_count(name: str, document: Mapping[str, Any]) -> int:
    if name == "Coverage_Ledger.json":
        return len(document["candidate_dispositions"]) + len(document["msc_coverage"])
    if name == "Strict_Conjecture_Ledger.json":
        return len(document["strict_credits"]) + len(document["credit_corrections"])
    key = {"Claim_Catalog.json": "records", "Claim_ID_Registry.json": "variants", "Stage5_Claim_ID_Registry.json": "mappings", "Migration_v4_to_v5.json": "migrations", "Theorem_List.json": "records", "Open_Claim_List.json": "records"}[name]
    return len(document[key])


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    return sha_bytes(canonical(sorted(({"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]} for row in inventory), key=lambda row: row["path"])))


def build_manifest(artifacts: Mapping[str, Mapping[str, Any]], inputs: Mapping[str, Any], authorities: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    inventory = []
    for name in sorted(RELEASE_FILES):
        payload = document_bytes(artifacts[name])
        inventory.append({"path": name, "sha256": sha_bytes(payload), "size_bytes": len(payload), "row_count": row_count(name, artifacts[name])})
    root = release_root(inventory)
    selection = authorities["selection"]
    return seal({
        "schema_version": "awesome-theorems/stage5-release-manifest/5.6", "release": RELEASE, "parent_release": PARENT_RELEASE, "parent_release_root_sha256": PARENT_ROOT, "release_root_sha256": root,
        "authoritative_inputs": copy.deepcopy(inputs), "artifacts": inventory,
        "counts": {"non_manifest_artifacts": 8, "catalog_records": 5_525, "origin_theorems": 1_000, "origin_open_claims": 0, "origin_strict_conjectures": 0, "cumulative_theorems": 3_500, "cumulative_open_claims": 2_025, "effective_strict_conjecture_credits": 1_425, "net_strict_increase_after_5_0": 1_024, "variants": 9_009, "canonical_variants": 9_009, "terminal_ready_unselected": 92, "preserved_quarantine": 469},
        "quality_qualification": copy.deepcopy(artifacts["Claim_Catalog.json"]["quality_qualification"]),
        "accepted_set_digests": copy.deepcopy(selection["set_digests"]),
        "release_allocation_digests": copy.deepcopy(authorities["allocation"]["set_digests"]),
        "strict_credit_binding": {"effective_credits": 1_425, "new_credits": 0, "strict_ledger_authority_sha256": artifacts["Strict_Conjecture_Ledger.json"]["authority_sha256"], "strict_credit_set_sha256": artifacts["Strict_Conjecture_Ledger.json"]["set_digests"].get("effective_strict_credit_set_sha256", artifacts["Strict_Conjecture_Ledger.json"]["set_digests"])},
        "publication": {"current_release_not_mutated_by_build": True, "cas_parent_pointer_file_sha256": PARENT_CURRENT_SHA, "independent_acceptance_receipt_required": "Docs/catalog/v5/receipts/V5_6_Independent_Acceptance_Receipt.json"},
    })


def validate_artifacts(artifacts: Mapping[str, Mapping[str, Any]], parent: Mapping[str, Mapping[str, Any]], new_rows: Sequence[Mapping[str, Any]], authorities: Mapping[str, Mapping[str, Any]]) -> None:
    require(set(artifacts) == set(RELEASE_FILES), "release artifact set drifted")
    for name, value in artifacts.items():
        verify_seal(value, name)
        require(value.get("release") == RELEASE, f"{name} release marker drifted")
    require(artifacts["Claim_Catalog.json"]["records"][:4_525] == parent["Claim_Catalog.json"]["records"], "catalog parent prefix changed")
    require(artifacts["Claim_Catalog.json"]["records"][4_525:] == list(new_rows), "catalog suffix differs from new rows")
    require(artifacts["Theorem_List.json"]["records"][:2_500] == parent["Theorem_List.json"]["records"], "theorem parent prefix changed")
    require(artifacts["Theorem_List.json"]["records"][2_500:] == list(new_rows), "theorem suffix differs from catalog suffix")
    require(artifacts["Open_Claim_List.json"]["records"] == parent["Open_Claim_List.json"]["records"], "open claims changed")
    for name, key in (("Claim_ID_Registry.json", "families"), ("Claim_ID_Registry.json", "senses"), ("Claim_ID_Registry.json", "variants"), ("Stage5_Claim_ID_Registry.json", "mappings"), ("Migration_v4_to_v5.json", "migrations"), ("Coverage_Ledger.json", "candidate_dispositions"), ("Strict_Conjecture_Ledger.json", "strict_credits"), ("Strict_Conjecture_Ledger.json", "credit_corrections")):
        require(artifacts[name][key][:len(parent[name][key])] == parent[name][key], f"{name}.{key} parent prefix changed")
    require(artifacts["Claim_ID_Registry.json"]["namespace_high_watermarks"] == {"ATF": LAST_ATF, "ATO": LAST_ATV, "ATS": LAST_ATV, "ATV": LAST_ATV}, "new high-watermarks drifted")
    dispositions = artifacts["Coverage_Ledger.json"]["candidate_dispositions"][-QUALIFIED_ROWS:]
    require(Counter(row["disposition"] for row in dispositions) == Counter({"accepted_new_kernel_checked_formal_theorem": 1_000, "terminal_ready_unselected_in_5_6": 92, "preserved_semantic_variant_review_quarantine": 469}), "coverage terminal disposition counts drifted")
    require(artifacts["Strict_Conjecture_Ledger.json"]["strict_credits"] == parent["Strict_Conjecture_Ledger.json"]["strict_credits"], "strict credits changed")


def materialize_release(artifacts: Mapping[str, Mapping[str, Any]], manifest: Mapping[str, Any], check: bool) -> None:
    for name in RELEASE_FILES:
        write_immutable(RELEASE_DIR / name, document_bytes(artifacts[name]), check)
    write_immutable(RELEASE_DIR / MANIFEST_NAME, document_bytes(manifest), check)


def pointer_for(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return seal({"schema_version": "awesome-theorems/stage5-current-release/5.6", "release": RELEASE, "manifest_path": "releases/5.6/Release_Manifest.json", "manifest_sha256": sha_file(RELEASE_DIR / MANIFEST_NAME), "release_root_sha256": manifest["release_root_sha256"]})


def publish_current(manifest: Mapping[str, Any]) -> None:
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current_bytes = CURRENT_PATH.read_bytes()
        wanted = document_bytes(pointer_for(manifest))
        if current_bytes == wanted:
            return
        require(sha_bytes(current_bytes) == PARENT_CURRENT_SHA, "Current_Release compare-and-swap parent mismatch")
        current = json.loads(current_bytes.decode("utf-8"))
        require(current.get("release") == PARENT_RELEASE and current.get("release_root_sha256") == PARENT_ROOT and current.get("manifest_sha256") == PARENT_MANIFEST_SHA, "Current_Release is not authenticated 5.5")
        receipt = V5 / "receipts/V5_6_Independent_Acceptance_Receipt.json"
        require(receipt.is_file(), "independent 5.6 acceptance receipt is required before publication")
        receipt_doc = load_json(receipt)
        verify_seal(receipt_doc, "5.6 acceptance receipt")
        require(receipt_doc.get("release_root_sha256") == manifest["release_root_sha256"] and receipt_doc.get("manifest_file_sha256") == sha_file(RELEASE_DIR / MANIFEST_NAME), "acceptance receipt does not bind staged release")
        atomic_write(CURRENT_PATH, wanted)


def run(*, check: bool, publish: bool) -> dict[str, Any]:
    parent = load_parent()
    _source, source_rows, source_index = load_source()
    ready, qualified, inventory = load_candidate_inputs()
    authorities = materialize_pre_release_authorities(
        parent, ready, qualified, inventory, check
    )
    inputs = authoritative_inputs(authorities, parent)
    new_rows = build_new_records(parent, source_rows, source_index, authorities)
    artifacts = build_artifacts(parent, new_rows, inputs, authorities)
    validate_artifacts(artifacts, parent, new_rows, authorities)
    manifest = build_manifest(artifacts, inputs, authorities)
    verify_seal(manifest, "Release_Manifest.json")
    materialize_release(artifacts, manifest, check)
    if publish:
        require(not check, "--check and --publish-current are mutually exclusive")
        publish_current(manifest)
    return {
        "authorities": authorities,
        "new_rows": new_rows,
        "artifacts": artifacts,
        "manifest": manifest,
    }


def run_selection_only(*, check: bool) -> dict[str, Any]:
    parent = load_parent()
    load_source()
    ready, qualified, inventory = load_candidate_inputs()
    receipt = load_generator_receipt(ready, qualified, inventory)
    selection = build_selection(ready, qualified)
    write_immutable(SELECTION_PATH, document_bytes(selection), check)
    return {"selection": selection, "generator_receipt": receipt}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify all files byte-for-byte without writing")
    parser.add_argument("--selection-only", action="store_true", help="materialize/check only the non-credit mathlib operand")
    parser.add_argument("--publish-current", action="store_true", help="CAS-publish after an exact check and independent receipt")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.selection_only:
            require(not args.publish_current, "selection-only mode cannot publish")
            result = run_selection_only(check=args.check)
            selection = result["selection"]
            print(
                f"PASS Stage5 5.6 mathlib operand mode={'check' if args.check else 'write'} "
                f"authority={selection['authority_sha256']} selected=1000 ready_unselected=92 "
                "quarantine=469 release_credit=0 ids=0"
            )
            return 0
        result = run(check=args.check, publish=args.publish_current)
        manifest = result["manifest"]
        print(f"PASS Stage5 release 5.6 mode={'check' if args.check else 'write'} root={manifest['release_root_sha256']} catalog=5525 theorem=3500 open=2025 strict=1425 origin_theorem=1000 ready_unselected=92 quarantine=469 published={args.publish_current}")
        return 0
    except (GenerationError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL Stage5 release 5.6: {error}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
