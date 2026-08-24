#!/usr/bin/env python3
"""Independent verifier for the non-credit 5.6 mathlib selection operand."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping, Sequence
import unicodedata


REPO_DEFAULT = Path(__file__).resolve().parents[4]
SELECTION_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Release_Selection_v5_6.json")
SELECTION_RECEIPT_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Release_Selection_Acceptance_Receipt_v5_6.json")
READY_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Generator_Accepted_Set_v5_6.jsonl")
QUALIFIED_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl")
INVENTORY_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Qualified_Batch_Inventory_v5_6.json")
RECEIPT_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Generator_Acceptance_Receipt_v5_6.json")
SOURCE_REL = Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/mathlib-verified-theorems-8a178386-full.json")
PARENT_MANIFEST_REL = Path("Docs/catalog/v5/releases/5.5/Release_Manifest.json")
PARENT_CATALOG_REL = Path("Docs/catalog/v5/releases/5.5/Claim_Catalog.json")

READY_SHA = "7943e8f473aaac523d617a8debd1dda5d589187bf62844933af684172570ab86"
QUALIFIED_SHA = "b03a2a3df17165b7f1e4bff7e2de80a8ecea6060a115b0fed66975827fb0f039"
INVENTORY_SHA = "669ad0d5b3f7d4b26000ffc36c153f5d415fdce4f7824f85177d999a80d34ab9"
INVENTORY_AUTHORITY = "879111d857fc5ce18a4baaf1cc1e98a3aee524f9c7dd5a7736dbd2ca61d370e1"
RECEIPT_SHA = "cc3236b5b91976d9ec876548ee7de6289313c7737d1ffeee019ba1f16916a7a4"
RECEIPT_AUTHORITY = "c528aba0e081b912c4102e1fea1c54e5adda49662c0bde9a94c994bddb27ebe5"
SOURCE_SHA = "7075e0bb151182ae4ba01cd34945657969be4bc60f7ee4ae6a62fc518f5386c3"
SOURCE_SIZE = 10_473_933
PARENT_MANIFEST_SHA = "773253c2afad3a91c1b14cc9b5f60b51ec9b7e258d1619f0168dd23c9c4b0a43"
PARENT_CATALOG_SHA = "9d6dc79b1cbdee401f2f022ee027557a04331fa9605dc7f443fdc09a62b029b4"
PARENT_ROOT = "fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0"
QUALIFIED_ROWS = 1_561
READY_ROWS = 1_092
SELECTED_ROWS = 1_000
INDIVIDUAL_ROWS = 511
BALANCED_ROWS = 489
UNSELECTED_ROWS = 92
QUARANTINE_ROWS = 469


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CheckError(f"not canonical JSON: {error}") from error


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha(canonical({key: item for key, item in value.items() if key not in omitted}))


def set_digest(values: Iterable[str]) -> str:
    return sha(canonical(sorted(values)))


def normalized_type_sha(value: str) -> str:
    return sha(" ".join(value.split()).encode("utf-8"))


def normalized_name_sha(value: str) -> str:
    return sha(unicodedata.normalize("NFKC", value).casefold().strip().encode("utf-8"))


def safe_file(root: Path, relative: Path) -> Path:
    require(not relative.is_absolute() and ".." not in relative.parts, f"unsafe path: {relative}")
    root = root.resolve()
    path = root / relative
    require(path.is_file() and not path.is_symlink(), f"missing or symlinked input: {relative}")
    require(path.resolve().is_relative_to(root), f"input escapes repository: {relative}")
    return path


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    def reject_constant(value: str) -> None:
        raise CheckError(f"non-finite number in {label}: {value}")

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key {key!r} in {label}")
            result[key] = value
        return result

    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=no_duplicates, parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CheckError(f"invalid JSON in {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def load_json(root: Path, relative: Path, *, canonical_file: bool = True) -> dict[str, Any]:
    path = safe_file(root, relative)
    payload = path.read_bytes()
    value = parse_json_bytes(payload, str(relative))
    if canonical_file:
        require(payload == canonical(value) + b"\n", f"{relative} is not canonical one-line JSON")
    return value


def load_jsonl(root: Path, relative: Path, expected_sha: str, expected_rows: int) -> list[dict[str, Any]]:
    path = safe_file(root, relative)
    payload = path.read_bytes()
    require(sha(payload) == expected_sha, f"{relative} SHA drifted")
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(payload.splitlines(), 1):
        require(bool(raw), f"blank line {line_number} in {relative}")
        row = parse_json_bytes(raw, f"{relative}:{line_number}")
        require(raw == canonical(row), f"noncanonical row {line_number} in {relative}")
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"stale row seal {line_number} in {relative}")
        rows.append(row)
    require(len(rows) == expected_rows, f"{relative} count drifted")
    return rows


def verify_seal(value: Mapping[str, Any], label: str) -> None:
    require(value.get("authority_sha256") == hash_without(value, "authority_sha256"), f"{label} authority seal is stale")


def select_independently(ready: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    individualized = sorted((row for row in ready if row.get("documentation_status") == "individual_declaration_docstring"), key=lambda row: (row["acceptance_rank"], row["candidate_key"]))
    require(len(individualized) == INDIVIDUAL_ROWS, "individual-docstring denominator drifted")
    module_rows = [row for row in ready if row.get("documentation_status") == "module_main_result_description"]
    require(len(module_rows) == READY_ROWS - INDIVIDUAL_ROWS, "module-description denominator drifted")
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in module_rows:
        buckets[str(row["module_root"])].append(row)
    for bucket in buckets.values():
        bucket.sort(key=lambda row: (row["acceptance_rank"], row["candidate_key"]))
    offsets = {root: 0 for root in buckets}
    balanced: list[dict[str, Any]] = []
    while len(balanced) < BALANCED_ROWS:
        advanced = False
        for module_root in sorted(buckets):
            offset = offsets[module_root]
            if offset >= len(buckets[module_root]):
                continue
            balanced.append(buckets[module_root][offset])
            offsets[module_root] += 1
            advanced = True
            if len(balanced) == BALANCED_ROWS:
                break
        require(advanced, "balanced sweep exhausted early")
    selected = individualized + balanced
    selected_keys = {row["candidate_key"] for row in selected}
    terminal = [row for row in ready if row["candidate_key"] not in selected_keys]
    require(len(selected) == SELECTED_ROWS and len(terminal) == UNSELECTED_ROWS, "selection counts drifted")
    require(Counter(row["source_syntax_kind"] for row in selected) == Counter({"theorem": 629, "lemma": 371}), "selected syntax-kind partition drifted")
    require(Counter(row["module_root"] for row in terminal) == Counter({"Analysis": 15, "RingTheory": 77}), "terminal distribution drifted")
    return selected, terminal


def expected_selection(ready: Sequence[dict[str, Any]], qualified: Sequence[dict[str, Any]]) -> dict[str, Any]:
    selected, terminal = select_independently(ready)
    selected_rank = {row["candidate_key"]: rank for rank, row in enumerate(selected, 1)}
    individual_keys = {row["candidate_key"] for row in selected[:INDIVIDUAL_ROWS]}
    terminal_keys = {row["candidate_key"] for row in terminal}
    ready_by_key = {row["candidate_key"]: row for row in ready}
    dispositions: list[dict[str, Any]] = []
    for source in qualified:
        key = source["candidate_key"]
        ready_row = ready_by_key.get(key)
        rank = selected_rank.get(key)
        if rank is not None:
            individual = key in individual_keys
            disposition = "selected_for_joint_5_6_release_transaction"
            reason = "all_individual_declaration_docstrings_first" if individual else "domain_balanced_module_root_sweep"
            phase = "individual_declaration_docstring_priority" if individual else "module_root_round_robin"
            selected_for_joint = True
        elif key in terminal_keys:
            disposition = "terminal_ready_unselected_in_5_6"
            reason = "release_cap_reached_after_documentation_priority_and_balanced_sweep"
            phase = None
            selected_for_joint = False
        else:
            require(source.get("generator_lane") == "semantic_variant_review_quarantine", "non-ready row escaped quarantine")
            disposition = "preserved_semantic_variant_review_quarantine"
            reason = "semantic_alias_or_family_signal_requires_human_review"
            phase = None
            selected_for_joint = False
        binding = source["source_binding"]
        row = {
            "candidate_key": key,
            "qualified_candidate_index": source["candidate_index"],
            "qualified_candidate_row_sha256": source["row_sha256"],
            "ready_acceptance_rank": ready_row["acceptance_rank"] if ready_row is not None else None,
            "ready_candidate_row_sha256": ready_row["row_sha256"] if ready_row is not None else None,
            "source_index": binding["source_index_zero_based"],
            "source_record_id": binding["source_record_id"],
            "source_record_sha256": binding["source_record_sha256"],
            "declaration": source["declaration"],
            "source_syntax_kind": source["source_syntax_kind"],
            "theorem_record_kind": source["theorem_record_kind"],
            "formal_type_sha256": source["formal_type_sha256"],
            "normalized_formal_type_sha256": source["normalized_formal_type_sha256"],
            "module": source["module"],
            "module_root": source["module_root"],
            "documentation_status": source["documentation_status"],
            "generator_lane": source["generator_lane"],
            "semantic_alias_evidence_sha256": sha(canonical(source["semantic_alias_evidence"])),
            "disposition": disposition,
            "reason_code": reason,
            "selection_phase": phase,
            "accepted_rank": rank,
            "selected_for_joint_release_transaction": selected_for_joint,
            "semantic_key": "mathlib-theorem-semantic/" + source["formal_type_sha256"],
            "target_variant_id": None,
            "target_s5_id": None,
            "grants_catalog_entry": False,
            "grants_theorem_credit": False,
            "row_sha256": None,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        dispositions.append(row)
    selected_rows = sorted((row for row in dispositions if row["selected_for_joint_release_transaction"]), key=lambda row: row["accepted_rank"])
    return {
        "schema_version": "awesome-theorems/mathlib-release-selection/5.6",
        "artifact": "Mathlib_Release_Selection_v5_6.json",
        "release": "5.6",
        "parent_release_root_sha256": PARENT_ROOT,
        "candidate_denominator_closed": True,
        "release_credit_granted_here": False,
        "ids_allocated_here": False,
        "inputs": {
            "generator_acceptance_receipt": {"path": RECEIPT_REL.as_posix(), "file_sha256": RECEIPT_SHA, "authority_sha256": RECEIPT_AUTHORITY},
            "accepted_set": {"path": READY_REL.as_posix(), "file_sha256": READY_SHA, "rows": READY_ROWS},
            "qualified_ledger": {"path": QUALIFIED_REL.as_posix(), "file_sha256": QUALIFIED_SHA, "rows": QUALIFIED_ROWS},
            "qualified_inventory": {"path": INVENTORY_REL.as_posix(), "file_sha256": INVENTORY_SHA, "authority_sha256": INVENTORY_AUTHORITY},
            "full_source": {"path": SOURCE_REL.as_posix(), "file_sha256": SOURCE_SHA, "records": 2_566, "mathlib_commit": "8a178386ffc0f5fef0b77738bb5449d50efeea95"},
        },
        "selection_policy": {
            "release_cap": SELECTED_ROWS,
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
            "selected": SELECTED_ROWS,
            "selected_individual_declaration_docstring": INDIVIDUAL_ROWS,
            "selected_module_main_result_description": BALANCED_ROWS,
            "selected_source_syntax_theorem": 629,
            "selected_source_syntax_lemma": 371,
            "terminal_ready_unselected": UNSELECTED_ROWS,
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
    }


def verify(root: Path, *, selection_override: Mapping[str, Any] | None = None) -> dict[str, Any]:
    root = root.resolve()
    require(root.is_dir(), "repository root is missing")
    require(sha_file(safe_file(root, PARENT_MANIFEST_REL)) == PARENT_MANIFEST_SHA, "parent manifest drifted")
    require(sha_file(safe_file(root, PARENT_CATALOG_REL)) == PARENT_CATALOG_SHA, "parent catalog drifted")
    parent_catalog = load_json(root, PARENT_CATALOG_REL)
    parent_manifest = load_json(root, PARENT_MANIFEST_REL)
    require(parent_manifest.get("release_root_sha256") == PARENT_ROOT, "parent release root drifted")
    require(sha_file(safe_file(root, SOURCE_REL)) == SOURCE_SHA and safe_file(root, SOURCE_REL).stat().st_size == SOURCE_SIZE, "full source drifted")
    source_document = load_json(root, SOURCE_REL, canonical_file=False)
    source_rows = source_document.get("records")
    require(isinstance(source_rows, list) and len(source_rows) == 2_566, "source row denominator drifted")
    ready = load_jsonl(root, READY_REL, READY_SHA, READY_ROWS)
    qualified = load_jsonl(root, QUALIFIED_REL, QUALIFIED_SHA, QUALIFIED_ROWS)
    require(sha_file(safe_file(root, INVENTORY_REL)) == INVENTORY_SHA, "qualified inventory drifted")
    inventory = load_json(root, INVENTORY_REL, canonical_file=False)
    verify_seal(inventory, "qualified inventory")
    require(inventory.get("authority_sha256") == INVENTORY_AUTHORITY, "qualified inventory authority drifted")
    require(sha_file(safe_file(root, RECEIPT_REL)) == RECEIPT_SHA, "qualification receipt drifted")
    receipt = load_json(root, RECEIPT_REL, canonical_file=False)
    verify_seal(receipt, "qualification receipt")
    require(receipt.get("authority_sha256") == RECEIPT_AUTHORITY, "qualification receipt authority drifted")
    require(receipt.get("release_mutation_authorized_or_performed") is False and receipt.get("counts", {}).get("theorem_credits_granted_by_receipt") == 0, "qualification receipt crossed credit boundary")
    require([row["acceptance_rank"] for row in ready] == list(range(1, READY_ROWS + 1)), "ready ranks are not dense")
    require([row["candidate_index"] for row in qualified] == list(range(1, QUALIFIED_ROWS + 1)), "qualified indexes are not dense")
    source_by_id = {row["source_record_id"]: (index, row) for index, row in enumerate(source_rows)}
    require(len(source_by_id) == 2_566, "source record IDs are not unique")
    qualified_by_key = {row["candidate_key"]: row for row in qualified}
    require(len(qualified_by_key) == QUALIFIED_ROWS, "qualified keys are not unique")
    for row in qualified:
        binding = row["source_binding"]
        source_index, source = source_by_id[binding["source_record_id"]]
        require(source_index == binding["source_index_zero_based"], "qualified source index binding drifted")
        require(sha(canonical(source)) == binding["source_record_sha256"], "qualified source row binding drifted")
        require(source["formal_type_sha256"] == row["formal_type_sha256"], "qualified formal type binding drifted")
        require(source.get("formal_proof_state") == "kernel_checked_sorry_free", "qualified source is not kernel-checked sorry-free")
        proof = source.get("proof_evidence", {})
        require(proof.get("uses_sorry") is False and "sorryAx" not in proof.get("batch_axiom_dependency_union", []), "qualified source proof evidence admits sorry")
        require(normalized_type_sha(source["formal_type"]) == row["normalized_formal_type_sha256"], "qualified normalized formal type drifted")
        require(normalized_name_sha(source["declaration"]) == row["normalized_declaration_name_sha256"], "qualified normalized declaration name drifted")
    for row in ready:
        qualified_row = qualified_by_key.get(row["candidate_key"])
        require(qualified_row is not None and qualified_row["row_sha256"] == row["qualified_candidate_row_sha256"], "ready-to-qualified binding drifted")
        require(qualified_row["generator_lane"] == "provisional_generator_admission" and qualified_row["generator_admission_qualified"] is True, "ready row is not machine-qualified")
    expected = expected_selection(ready, qualified)
    expected["authority_sha256"] = hash_without(expected, "authority_sha256")
    observed = copy.deepcopy(selection_override) if selection_override is not None else load_json(root, SELECTION_REL)
    verify_seal(observed, "mathlib release selection")
    require(observed == expected, "selection differs from independent reconstruction")
    require(all(row["grants_catalog_entry"] is False and row["grants_theorem_credit"] is False and row["target_variant_id"] is None and row["target_s5_id"] is None for row in observed["candidate_dispositions"]), "selection grants credit or IDs before joint release")
    selected = [row for row in observed["candidate_dispositions"] if row["selected_for_joint_release_transaction"]]
    require(len({row["formal_type_sha256"] for row in selected}) == SELECTED_ROWS, "selected exact formal types are not unique")
    require(len({row["normalized_formal_type_sha256"] for row in selected}) == SELECTED_ROWS, "selected normalized formal types are not unique")
    parent_exact_types: set[str] = set()
    parent_normalized_types: set[str] = set()
    parent_normalized_names: set[str] = set()
    for parent_row in parent_catalog.get("records", []):
        formal = parent_row.get("formal_statement", {}) if isinstance(parent_row.get("formal_statement"), dict) else {}
        for digest in (parent_row.get("formal_type_sha256"), formal.get("formal_type_sha256"), formal.get("declaration_type_sha256"), parent_row.get("mathematical_statement", {}).get("formal_type_sha256") if isinstance(parent_row.get("mathematical_statement"), dict) else None):
            if isinstance(digest, str):
                parent_exact_types.add(digest)
        for statement in (parent_row.get("formal_type"), formal.get("formal_type"), formal.get("declaration_type"), parent_row.get("mathematical_statement", {}).get("formal_type") if isinstance(parent_row.get("mathematical_statement"), dict) else None):
            if isinstance(statement, str):
                parent_normalized_types.add(normalized_type_sha(statement))
        for declaration in (parent_row.get("formal_declaration"), parent_row.get("qualified_name"), formal.get("declaration"), formal.get("declaration_name"), formal.get("qualified_declaration")):
            if isinstance(declaration, str):
                parent_normalized_names.add(normalized_name_sha(declaration))
    require(not ({row["formal_type_sha256"] for row in selected} & parent_exact_types), "selected exact formal type collides with parent")
    require(not ({row["normalized_formal_type_sha256"] for row in selected} & parent_normalized_types), "selected normalized formal type collides with parent")
    selected_name_hashes = {qualified_by_key[row["candidate_key"]]["normalized_declaration_name_sha256"] for row in selected}
    require(len(selected_name_hashes) == SELECTED_ROWS and not (selected_name_hashes & parent_normalized_names), "selected normalized declaration name collides internally or with parent")
    return {"selection": observed, "ready": ready, "qualified": qualified, "source": source_document, "receipt": receipt}


def acceptance_receipt(root: Path, result: Mapping[str, Any]) -> dict[str, Any]:
    selection = result["selection"]
    document = {
        "schema_version": "awesome-theorems/mathlib-release-selection-acceptance/5.6",
        "artifact": SELECTION_RECEIPT_REL.name,
        "as_of": "2026-08-10",
        "decision": "accept_noncredit_mathlib_operand_for_later_joint_5_6_transaction",
        "parent_release_root_sha256": PARENT_ROOT,
        "selection_path": SELECTION_REL.as_posix(),
        "selection_file_sha256": sha_file(safe_file(root, SELECTION_REL)),
        "selection_authority_sha256": selection["authority_sha256"],
        "qualification_receipt_path": RECEIPT_REL.as_posix(),
        "qualification_receipt_file_sha256": RECEIPT_SHA,
        "qualification_receipt_authority_sha256": RECEIPT_AUTHORITY,
        "checker_path": Path(__file__).resolve().relative_to(root.resolve()).as_posix(),
        "checker_file_sha256": sha_file(Path(__file__).resolve()),
        "counts": copy.deepcopy(selection["counts"]),
        "credit_boundary": {
            "release_credit_granted": False,
            "catalog_entries_granted": 0,
            "theorem_credits_granted": 0,
            "ids_allocated": 0,
            "joint_putnam_mathlib_release_required": True,
        },
        "quality_boundary": copy.deepcopy(selection["quality_boundary"]),
        "findings": [],
        "authority_sha256": None,
    }
    document["authority_sha256"] = hash_without(document, "authority_sha256")
    return document


def atomic_write(path: Path, payload: bytes) -> None:
    import os
    import tempfile

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_DEFAULT)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--check-receipt", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = verify(args.repo_root)
        expected_receipt = acceptance_receipt(args.repo_root.resolve(), result)
        receipt_path = args.repo_root.resolve() / SELECTION_RECEIPT_REL
        if args.write_receipt:
            atomic_write(receipt_path, canonical(expected_receipt) + b"\n")
        if args.check_receipt:
            observed_receipt = load_json(args.repo_root.resolve(), SELECTION_RECEIPT_REL)
            require(observed_receipt == expected_receipt, "selection acceptance receipt differs from independent reconstruction")
        if not args.quiet:
            selection = result["selection"]
            print(f"PASS independent mathlib 5.6 selection authority={selection['authority_sha256']} selected=1000 ready_unselected=92 quarantine=469 release_credit=0 ids=0")
        return 0
    except (CheckError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL independent mathlib 5.6 selection: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
