#!/usr/bin/env python3
"""Independent, read-only checker for the Stage 5.5 frontier qualification.

This checker intentionally does not import the qualification builder.  It
replays the two frozen candidate universes, every human-review row, all four
coverage lanes, the parent/important-set boundary, and the complete emitted
qualification document.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping


CATALOG_REL = Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json")
MANIFEST_REL = Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json")
IMPORTANT_REL = Path(
    "Docs/catalog/v5/curation/theorem_quality_v5_5/"
    "mathlib-important-inventory-1000.json"
)
ERDOS_PRIMARY_REL = Path(
    "Docs/catalog/v5/curation/erdos_parent_join_v5_5/"
    "resolved-theorem-max2-selected.jsonl"
)
ERDOS_SUPPLEMENTAL_REL = Path(
    "Docs/catalog/v5/curation/erdos_parent_join_v5_5/"
    "resolved-theorem-supplemental.jsonl"
)
NONERDOS_PRIMARY_REL = Path(
    "Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"
)
NONERDOS_SUPPLEMENTAL_REL = Path(
    "Docs/catalog/v5/curation/Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"
)
REVIEW_DIR_REL = Path(
    "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"
)
QUALIFICATION_REL = Path(
    "Docs/catalog/v5/curation/Frontier_Theorem_Qualification_v5_5.json"
)

FIXED_FILE_SHA256 = {
    CATALOG_REL: "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709",
    MANIFEST_REL: "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9",
    IMPORTANT_REL: "a3db9bcd31feb8f2ea4ac07c0b60076446af25b3e4045c2938851440fb974f92",
    ERDOS_PRIMARY_REL: "a65f8e9841dd415894cbfc5f032283fa05e4bd1161c6bd4c8a4ae3e9e0e64cae",
    ERDOS_SUPPLEMENTAL_REL: "6d31bf21d1182e3d1dd908fa27d552340fcb6169636541b04fbf26ea1a7e65a7",
    NONERDOS_PRIMARY_REL: "b3b28b81cfcd9fe4dbf002d2bb8d9bedaa8094656396e224abb5c6221530b2fc",
    NONERDOS_SUPPLEMENTAL_REL: "78c2d8e1e4068d59bf0471ecca9071fc139bb3300525df0aab8348718cbdc135",
}
FIXED_REVIEW_SHA256 = {
    "erdos_000_094.jsonl": "3ab25dfcdf8da43fe2b58b3171d27960ede98667f906c551a9ce8544d5b8f7ac",
    "erdos_095_189.jsonl": "f4030d1ded1b7107fb269c8eaf698f8bcdb209d5e9bdc49a9a18b7415a770567",
    "erdos_190_284.jsonl": "0c9b52d84b9aea6a6bffd3a9817e50ae5b62304cd2199e2ddc767f58a4e596a9",
    "erdos_285_320.jsonl": "d0551bc6bbefd03e4ac0068dcd83ec70514e86e91fc9d9535a9073f82e20fb61",
    "erdos_321_350.jsonl": "a34206115d68cc2e016845dc15bfc713a0346e0ec69ab954b40efed0938d5807",
    "erdos_351_378.jsonl": "f5f71b4fb1073c7cc81d1461d10d3bde83b6b2ad7e51224424aaedf570c40cc2",
    "erdos_supplemental_000_083.jsonl": "dd5e442ba9edb127505b2125a314438c855812de93d5c42b7e8ff8ef37d385da",
    "erdos_supplemental_084_166.jsonl": "59ec02d694720d97636dd7a6ed4f3e37ebada006faf7347504a8088f3be80fae",
    "nonerdos_001_085.jsonl": "a07d59318c6eb150fa475b4c654e0aa811d23d6e3e7fb68d9e7edd24748295f5",
    "nonerdos_086_170.jsonl": "f70fed52ad70bddd881d00ed38c33a856377c311cf1cc1a940c8bbf1b035c765",
    "nonerdos_171_254.jsonl": "984ac32dace39d251f0f450ec776f539ac3c56943b95b0e11aff3ca989b8f7e8",
    "nonerdos_supplemental_001_059.jsonl": "17da2a497653cee6b676f620b717b8d13561e901693c9fcd848c59f021640e76",
    "nonerdos_supplemental_060_117.jsonl": "b4c0aa46d9099b8f6df7d663b66604d544b7c4980e19c79703d10e3fdda31887",
}
PARENT_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
IMPORTANT_AUTHORITY = "0b4d7c43f91e3c57104665c579fabf7b8a27282b10d95670dea9ccb3bbaf11d2"
NONERDOS_PRIMARY_AUTHORITY = "375ca73546293f74fdc966209d4be0d184ad5e28273c70aecc7a12a601548133"
NONERDOS_SUPPLEMENTAL_AUTHORITY = "d382e4c9b6851150257fea50ab597051b6258085a24b04d43e517a81094c547c"
MIN_CREDITS = 500
MAX_CREDITS = 1_000

ERDOS_GATES = {
    "exact_statement_scope",
    "current_upstream_status",
    "primary_resolution",
    "importance_frontier",
    "semantic_dedupe",
    "rights",
}
NONERDOS_BOOLEAN_GATES = {
    "complete_proved_theorem_statement",
    "documented_open_problem_or_frontier_main_result",
    "primary_resolution_reference_fixed",
    "proved_status_verified_as_of_2026_08_10",
    "rights_review_complete_for_existing_credit",
    "scope_matches_reference",
    "semantic_dedupe_complete",
    "semantic_dedupe_passed",
}
NONERDOS_OBJECT_GATES = {
    "complete_proved_statement",
    "primary_reference",
    "scope_match",
    "current_proved_status",
    "frontier_or_documented_resolution",
    "rights",
    "semantic_dedupe",
}
LANE_ORDER = {
    "erdos_primary": 0,
    "erdos_supplemental": 1,
    "nonerdos_primary": 2,
    "nonerdos_supplemental": 3,
}
REVIEW_NAME = re.compile(
    r"^(erdos|nonerdos)(?:_(supplemental))?_(\d{3})_(\d{3})\.jsonl$"
)


class CheckError(RuntimeError):
    """A fail-closed qualification validation error."""


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def set_digest(values: Iterable[str]) -> str:
    return digest(canonical(sorted(values)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def strict_int(value: Any, message: str) -> int:
    require(type(value) is int, message)
    return value


def reject_constant(token: str) -> None:
    raise CheckError(f"non-finite JSON token: {token}")


def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def safe_path(root: Path, relative: Path) -> Path:
    require(not relative.is_absolute() and ".." not in relative.parts, f"unsafe path: {relative}")
    path = (root / relative).resolve(strict=True)
    require(path.is_relative_to(root), f"path escapes repository root: {relative}")
    return path


def parse_json(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload,
            object_pairs_hook=closed_object,
            parse_constant=reject_constant,
        )
    except UnicodeDecodeError as error:
        raise CheckError(f"{label}: invalid UTF-8: {error}") from error
    require(isinstance(value, dict), f"{label}: JSON root is not an object")
    return value


def load_fixed_json(root: Path, relative: Path) -> tuple[dict[str, Any], bytes]:
    path = safe_path(root, relative)
    payload = path.read_bytes()
    require(
        digest(payload) == FIXED_FILE_SHA256[relative],
        f"fixed input file hash drifted: {relative}",
    )
    return parse_json(payload, relative.as_posix()), payload


def load_fixed_jsonl(root: Path, relative: Path) -> tuple[list[dict[str, Any]], bytes]:
    path = safe_path(root, relative)
    payload = path.read_bytes()
    require(
        digest(payload) == FIXED_FILE_SHA256[relative],
        f"fixed input file hash drifted: {relative}",
    )
    return parse_jsonl(payload, relative.as_posix()), payload


def parse_jsonl(payload: bytes, label: str) -> list[dict[str, Any]]:
    require(payload.endswith(b"\n"), f"{label}: JSONL lacks terminal LF")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(payload.splitlines(), start=1):
        require(line, f"{label}:{line_number}: blank JSONL row")
        rows.append(parse_json(line, f"{label}:{line_number}"))
    return rows


def ranges(values: set[int]) -> str:
    if not values:
        return "none"
    ordered = sorted(values)
    groups: list[str] = []
    first = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + 1:
            previous = value
            continue
        groups.append(str(first) if first == previous else f"{first}-{previous}")
        first = previous = value
    groups.append(str(first) if first == previous else f"{first}-{previous}")
    return ",".join(groups)


def authority_is_valid(document: Mapping[str, Any], label: str) -> None:
    require(
        document.get("authority_sha256") == hash_without(document, "authority_sha256"),
        f"{label}: authority hash mismatch",
    )


def validate_parent_candidate(
    candidate: Mapping[str, Any],
    catalog_by_id: Mapping[str, Mapping[str, Any]],
    label: str,
) -> tuple[str, str]:
    parent = candidate.get("parent", candidate)
    identity = candidate.get("identity")
    if isinstance(identity, dict):
        stage_id = parent.get("stage_claim_id")
        variant_id = parent.get("variant_id")
        semantic = identity.get("semantic_identity_key")
        require(
            semantic == "formal-conjectures-parent-identity/" + str(identity.get("identity_payload_sha256")),
            f"{label}: candidate semantic identity malformed",
        )
        require(
            parent.get("dedupe", {}).get("identity_payload_sha256")
            == identity.get("identity_payload_sha256"),
            f"{label}: candidate identity payload mismatch",
        )
    else:
        stage_id = candidate.get("stage_claim_id")
        variant_id = candidate.get("variant_id")
        semantic = candidate.get("semantic_key")
        require(
            semantic
            == "normalized-statement-sha256/"
            + str(candidate.get("semantic_key", "")).split("/", 1)[-1],
            f"{label}: candidate semantic key malformed",
        )
    require(
        isinstance(stage_id, str) and re.fullmatch(r"S5-CLM-\d{8}", stage_id) is not None,
        f"{label}: bad stage ID",
    )
    require(
        isinstance(variant_id, str) and re.fullmatch(r"ATV-\d{8}", variant_id) is not None,
        f"{label}: bad variant ID",
    )
    require(isinstance(semantic, str) and semantic, f"{label}: missing semantic key")
    require(
        re.fullmatch(
            r"(?:formal-conjectures-parent-identity|normalized-statement-sha256)/[0-9a-f]{64}",
            semantic,
        )
        is not None,
        f"{label}: semantic key format malformed",
    )
    claim = catalog_by_id.get(stage_id)
    require(claim is not None, f"{label}: candidate absent from parent catalog: {stage_id}")
    require(
        claim.get("current_claim_kind") == "theorem" and claim.get("material_status") == "proved",
        f"{label}: candidate parent is not a proved theorem: {stage_id}",
    )
    require(claim.get("variant_id") == variant_id, f"{label}: parent variant binding mismatch")
    require(claim.get("family_id") == parent.get("family_id"), f"{label}: parent family binding mismatch")
    require(
        claim.get("formal_type_sha256") == parent.get("formal_type_sha256"),
        f"{label}: parent formal type binding mismatch",
    )
    if isinstance(identity, dict):
        require(
            claim.get("dedupe", {}).get("identity_payload_sha256")
            == identity.get("identity_payload_sha256"),
            f"{label}: catalog identity binding mismatch",
        )
    else:
        require(
            claim.get("dedupe", {}).get("normalized_statement_sha256")
            == semantic.split("/", 1)[1],
            f"{label}: catalog semantic binding mismatch",
        )
    return stage_id, semantic


def validate_nonerdos_queue(
    document: dict[str, Any],
    *,
    supplemental: bool,
    catalog_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[int, dict[str, Any]]:
    label = "non-Erdos supplemental queue" if supplemental else "non-Erdos primary queue"
    authority_is_valid(document, label)
    expected_authority = (
        NONERDOS_SUPPLEMENTAL_AUTHORITY if supplemental else NONERDOS_PRIMARY_AUTHORITY
    )
    require(document.get("authority_sha256") == expected_authority, f"{label}: authority constant drifted")
    rows = document.get("records")
    expected_count = 117 if supplemental else 254
    require(isinstance(rows, list) and len(rows) == expected_count, f"{label}: denominator drifted")
    expected_ranks = list(range(255, 372)) if supplemental else list(range(1, 255))
    require([row.get("candidate_rank") for row in rows] == expected_ranks, f"{label}: rank order drifted")
    result: dict[int, dict[str, Any]] = {}
    for position, row in enumerate(rows):
        require(isinstance(row, dict), f"{label}:{position + 1}: row is not object")
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"{label}:{position + 1}: row hash mismatch")
        rank = strict_int(row.get("candidate_rank"), f"{label}:{position + 1}: rank malformed")
        if supplemental:
            require(row.get("supplemental_rank") == rank - 254, f"{label}:{position + 1}: supplemental rank mismatch")
        validate_parent_candidate(row, catalog_by_id, f"{label}:{position + 1}")
        result[rank] = row
    require(len(result) == expected_count, f"{label}: duplicate rank")
    return result


def discover_reviews(root: Path) -> list[tuple[Path, Path, bytes, list[dict[str, Any]], re.Match[str]]]:
    directory = safe_path(root, REVIEW_DIR_REL)
    paths = sorted(directory.glob("*.jsonl"), key=lambda path: path.name.encode("utf-8"))
    require(paths, "no frontier review ledgers found")
    result: list[tuple[Path, Path, bytes, list[dict[str, Any]], re.Match[str]]] = []
    for path in paths:
        resolved = path.resolve(strict=True)
        require(resolved.is_relative_to(directory), f"review path escapes review directory: {path}")
        match = REVIEW_NAME.fullmatch(path.name)
        require(match is not None, f"unexpected frontier review ledger name: {path.name}")
        payload = path.read_bytes()
        require(path.name in FIXED_REVIEW_SHA256, f"unfixed frontier review ledger: {path.name}")
        require(
            digest(payload) == FIXED_REVIEW_SHA256[path.name],
            f"fixed review ledger hash drifted: {path.name}",
        )
        rows = parse_jsonl(payload, path.relative_to(root).as_posix())
        require(rows, f"empty frontier review ledger: {path.name}")
        result.append((path, path.relative_to(root), payload, rows, match))
    return result


def lane_from_match(match: re.Match[str]) -> str:
    return f"{match.group(1)}_{'supplemental' if match.group(2) else 'primary'}"


def builder_index(lane: str, row: Mapping[str, Any], label: str) -> int:
    if lane.startswith("erdos_"):
        source = row.get("source_binding")
        require(isinstance(source, dict), f"{label}: source binding missing")
        if lane == "erdos_supplemental" and "supplemental_index" in row:
            value = row.get("supplemental_index")
        elif lane == "erdos_supplemental" and "supplemental_rank" in row:
            value = row.get("supplemental_rank")
        else:
            value = source.get("zero_based_row")
    else:
        value = row.get("candidate_rank")
    return strict_int(value, f"{label}: candidate index malformed")


def gates_pass(gates: Mapping[str, Any]) -> bool:
    if not gates:
        return False
    for gate in gates.values():
        if type(gate) is bool:
            if gate is not True:
                return False
        elif isinstance(gate, dict):
            if gate.get("pass") is True or gate.get("verdict") == "pass":
                continue
            return False
        else:
            return False
    return True


def validate_erdos_review(
    row: dict[str, Any],
    candidate: dict[str, Any],
    *,
    lane: str,
    actual_index: int,
    emitted_index: int,
    source_relative: Path,
    label: str,
) -> None:
    require(row.get("schema_version") == "awesome-theorems/frontier-theorem-row-review/5.5", f"{label}: schema mismatch")
    source = row.get("source_binding")
    identity = row.get("identity")
    require(isinstance(source, dict) and isinstance(identity, dict), f"{label}: identity/source malformed")
    require(source.get("path") == source_relative.as_posix(), f"{label}: source path mismatch")
    require(source.get("full_file_sha256") == FIXED_FILE_SHA256[source_relative], f"{label}: source file hash mismatch")
    require(source.get("zero_based_row") == actual_index, f"{label}: source row index mismatch")
    if source.get("row_sha256") is not None:
        require(source.get("row_sha256") == digest(canonical(candidate)), f"{label}: source row hash mismatch")
    expected_identity = candidate["identity"]
    expected_parent = candidate["parent"]
    for key, expected in (
        ("problem_number", candidate["source_problem"]["problem_number"]),
        ("stage_claim_id", expected_parent["stage_claim_id"]),
        ("variant_id", expected_parent["variant_id"]),
        ("qualified_name", expected_parent["qualified_name"]),
        ("role", expected_identity["role_within_problem"]),
        ("semantic_identity_key", expected_identity["semantic_identity_key"]),
        ("identity_payload_sha256", expected_identity["identity_payload_sha256"]),
    ):
        require(identity.get(key) == expected, f"{label}: identity field mismatch: {key}")
    statement = row.get("statement_binding")
    locator = expected_parent.get("locator", {})
    mathematical = expected_parent.get("mathematical_statement", {})
    require(isinstance(statement, dict), f"{label}: statement binding missing")
    expected_statement = {
        "member_path": locator.get("member_path"),
        "source_revision": locator.get("revision"),
        "line_start": locator.get("line_start"),
        "line_end": locator.get("line_end"),
        "raw_block_sha256": locator.get("raw_block_sha256"),
        "formal_type_sha256": expected_parent.get("formal_type_sha256"),
        "statement_sha256": mathematical.get("statement_sha256"),
    }
    require(statement == expected_statement, f"{label}: statement binding mismatch")
    gates = row.get("gates")
    require(isinstance(gates, dict) and set(gates) == ERDOS_GATES, f"{label}: gate set mismatch")
    verdicts: list[str] = []
    for name, gate in gates.items():
        require(isinstance(gate, dict), f"{label}: gate is not object: {name}")
        verdict = gate.get("verdict")
        require(verdict in {"pass", "pending", "fail"}, f"{label}: bad gate verdict: {name}")
        require(isinstance(gate.get("evidence"), str) and gate["evidence"].strip(), f"{label}: empty gate evidence: {name}")
        verdicts.append(verdict)
    require(gates["rights"]["verdict"] == "pass", f"{label}: rights gate did not pass")
    primary = gates["primary_resolution"]
    require(isinstance(primary.get("citation_evidence"), str) and primary["citation_evidence"].strip(), f"{label}: primary citation evidence missing")
    decision = row.get("decision")
    expected_decision = "accept" if all(value == "pass" for value in verdicts) else "reject" if "fail" in verdicts else "pending"
    require(decision == expected_decision, f"{label}: decision does not follow gate verdicts")
    all_pass = all(value == "pass" for value in verdicts)
    require(type(row.get("all_gates_pass")) is bool and row["all_gates_pass"] is all_pass, f"{label}: all_gates_pass mismatch")
    credit = row.get("credit")
    require(
        credit
        == {
            "frontier_theorem_credit_granted": False,
            "new_theorem_credit_granted": False,
            "release_modified": False,
        },
        f"{label}: review credit boundary escalated",
    )
    rights = row.get("rights_boundary")
    require(isinstance(rights, dict), f"{label}: rights boundary missing")
    require(rights.get("third_party_text_reused") is False, f"{label}: third-party text boundary failed")
    require(rights.get("metadata_and_locator_only") is True, f"{label}: metadata-only boundary failed")
    if lane == "erdos_supplemental":
        # emitted_index may be either a zero-based supplemental_index or a
        # one-based supplemental_rank, but it must bind the same source row.
        require(emitted_index in {actual_index, actual_index + 1}, f"{label}: supplemental convention mismatch")


def validate_nonerdos_review(
    row: dict[str, Any],
    candidate: dict[str, Any],
    *,
    supplemental: bool,
    label: str,
) -> None:
    schema = row.get("schema_version")
    require(
        schema
        in {
            "awesome-theorems/frontier-existing-credit-review/5.5",
            "awesome-theorems/frontier-theorem-human-review/5.5",
        },
        f"{label}: schema mismatch",
    )
    for key in ("candidate_rank", "stage_claim_id", "variant_id", "family_id", "semantic_key"):
        require(row.get(key) == candidate.get(key), f"{label}: candidate binding mismatch: {key}")
    if supplemental:
        require(row.get("supplemental_rank") == candidate.get("supplemental_rank"), f"{label}: supplemental rank mismatch")
    declared_candidate_hash = row.get("queue_row_sha256", row.get("source_row_sha256"))
    require(declared_candidate_hash == candidate.get("row_sha256"), f"{label}: queue row hash mismatch")
    declared_field = "review_row_sha256" if "review_row_sha256" in row else "row_sha256"
    require(row.get(declared_field) == hash_without(row, declared_field), f"{label}: review row hash mismatch")
    gates = row.get("gates")
    require(isinstance(gates, dict) and gates, f"{label}: gates missing")
    if set(gates) == NONERDOS_BOOLEAN_GATES:
        require(all(type(value) is bool for value in gates.values()), f"{label}: boolean gate malformed")
        require(gates["rights_review_complete_for_existing_credit"] is True, f"{label}: rights gate did not pass")
    else:
        require(set(gates) == NONERDOS_OBJECT_GATES, f"{label}: gate set mismatch")
        for name, gate in gates.items():
            require(isinstance(gate, dict), f"{label}: gate is not object: {name}")
            require(type(gate.get("pass")) is bool, f"{label}: gate pass is not boolean: {name}")
            evidence = gate.get("evidence")
            require(
                isinstance(evidence, list)
                and evidence
                and all(isinstance(item, str) and item.strip() for item in evidence),
                f"{label}: gate evidence missing: {name}",
            )
        require(gates["rights"]["pass"] is True, f"{label}: rights gate did not pass")
    all_pass = gates_pass(gates)
    accepted = row.get("decision") == "eligible_existing_frontier_credit"
    require(row.get("decision") in {"eligible_existing_frontier_credit", "pending", "reject"}, f"{label}: bad decision")
    require(accepted is all_pass, f"{label}: decision does not follow all gates")
    require(row.get("grants_new_theorem_credit") is False, f"{label}: new-theorem credit escalation")
    if supplemental:
        require(row.get("review_eligible_frontier_credit") is accepted, f"{label}: supplemental eligibility flag mismatch")
        require(row.get("grants_frontier_credit") is False, f"{label}: supplemental review grants formal credit")
    else:
        require(row.get("grants_frontier_credit") is accepted, f"{label}: frontier eligibility flag mismatch")
    references = row.get("primary_references", row.get("primary_resolution_references", []))
    require(isinstance(references, list), f"{label}: primary references malformed")
    if accepted:
        require(references, f"{label}: accepted row lacks primary reference")
    for reference in references:
        require(isinstance(reference, dict) and reference, f"{label}: primary reference is empty")
    parent_binding = row.get("parent_binding")
    if parent_binding is not None:
        require(isinstance(parent_binding, dict), f"{label}: parent binding malformed")
        require(parent_binding.get("parent_release") == "5.4", f"{label}: parent release mismatch")
        require(parent_binding.get("parent_stage_claim_id") == candidate["stage_claim_id"], f"{label}: parent stage mismatch")
        require(parent_binding.get("parent_variant_id") == candidate["variant_id"], f"{label}: parent variant mismatch")
        require(parent_binding.get("exact_parent_occurrences") == 1, f"{label}: parent occurrence mismatch")
        require(parent_binding.get("parent_catalog_sha256") == FIXED_FILE_SHA256[CATALOG_REL], f"{label}: parent catalog hash mismatch")


def collect_and_validate_reviews(
    root: Path,
    *,
    catalog_by_id: Mapping[str, Mapping[str, Any]],
    erdos_primary: list[dict[str, Any]],
    erdos_supplemental: list[dict[str, Any]],
    nonerdos_primary: Mapping[int, dict[str, Any]],
    nonerdos_supplemental: Mapping[int, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    files = discover_reviews(root)
    raw_rows: list[dict[str, Any]] = []
    file_inputs: list[dict[str, Any]] = []
    observed: dict[str, list[int]] = {lane: [] for lane in LANE_ORDER}
    erdos_supplemental_offsets: set[int] = set()
    for path, relative, payload, rows, match in files:
        lane = lane_from_match(match)
        start, end = int(match.group(3)), int(match.group(4))
        require(start <= end, f"{path.name}: reversed filename range")
        indices: list[int] = []
        for line_number, row in enumerate(rows, start=1):
            label = f"{relative}:{line_number}"
            index = builder_index(lane, row, label)
            indices.append(index)
            observed[lane].append(index)
            if lane == "erdos_supplemental":
                source_index = strict_int(row.get("source_binding", {}).get("zero_based_row"), f"{label}: source index malformed")
                erdos_supplemental_offsets.add(index - source_index)
            raw_rows.append(
                {
                    "lane": lane,
                    "candidate_index": index,
                    "row": row,
                    "path": path,
                    "relative": relative,
                    "payload": payload,
                    "line_number": line_number,
                }
            )
        if lane == "nonerdos_supplemental":
            expected_file_indices = list(range(start + 254, end + 255))
        else:
            expected_file_indices = list(range(start, end + 1))
        require(indices == expected_file_indices, f"{path.name}: filename range does not equal ordered row indices")
        file_inputs.append(
            {
                "path": relative.as_posix(),
                "file_sha256": digest(payload),
                "size_bytes": len(payload),
                "rows": len(rows),
            }
        )

    require(
        erdos_supplemental_offsets <= {0} or erdos_supplemental_offsets <= {1},
        "Erdos supplemental reviews mix zero- and one-based index conventions",
    )
    erdos_supp_offset = next(iter(erdos_supplemental_offsets), 0)
    expected = {
        "erdos_primary": set(range(379)),
        "erdos_supplemental": set(range(erdos_supp_offset, erdos_supp_offset + 167)),
        "nonerdos_primary": set(range(1, 255)),
        "nonerdos_supplemental": set(range(255, 372)),
    }
    coverage_errors: list[str] = []
    for lane, wanted in expected.items():
        values = observed[lane]
        missing = wanted - set(values)
        unexpected = set(values) - wanted
        duplicates = sorted(value for value, count in Counter(values).items() if count != 1)
        if missing or unexpected or duplicates or len(values) != len(wanted):
            detail = f"{lane} missing={ranges(missing)}"
            if unexpected:
                detail += f" unexpected={ranges(unexpected)}"
            if duplicates:
                detail += f" duplicate={ranges(set(duplicates))}"
            coverage_errors.append(detail)
    require(not coverage_errors, "review coverage incomplete: " + "; ".join(coverage_errors))

    normalized: list[dict[str, Any]] = []
    for item in raw_rows:
        lane = item["lane"]
        emitted_index = item["candidate_index"]
        row = item["row"]
        label = f"{item['relative']}:{item['line_number']}"
        if lane == "erdos_primary":
            actual_index = emitted_index
            candidate = erdos_primary[actual_index]
            source_relative = ERDOS_PRIMARY_REL
            validate_erdos_review(
                row,
                candidate,
                lane=lane,
                actual_index=actual_index,
                emitted_index=emitted_index,
                source_relative=source_relative,
                label=label,
            )
            identity = row["identity"]
            decision = row["decision"]
            accepted = decision == "accept" and row["all_gates_pass"] is True and gates_pass(row["gates"])
            rights = row.get("rights_boundary")
            references = [row["gates"]["primary_resolution"]["evidence"]]
            stage_id = identity["stage_claim_id"]
            variant_id = identity["variant_id"]
            semantic = identity["semantic_identity_key"]
        elif lane == "erdos_supplemental":
            actual_index = emitted_index - erdos_supp_offset
            candidate = erdos_supplemental[actual_index]
            source_relative = ERDOS_SUPPLEMENTAL_REL
            validate_erdos_review(
                row,
                candidate,
                lane=lane,
                actual_index=actual_index,
                emitted_index=emitted_index,
                source_relative=source_relative,
                label=label,
            )
            identity = row["identity"]
            decision = row["decision"]
            accepted = decision == "accept" and row["all_gates_pass"] is True and gates_pass(row["gates"])
            rights = row.get("rights_boundary")
            references = [row["gates"]["primary_resolution"]["evidence"]]
            stage_id = identity["stage_claim_id"]
            variant_id = identity["variant_id"]
            semantic = identity["semantic_identity_key"]
        else:
            supplemental = lane == "nonerdos_supplemental"
            candidate = (nonerdos_supplemental if supplemental else nonerdos_primary)[emitted_index]
            validate_nonerdos_review(row, candidate, supplemental=supplemental, label=label)
            decision = row["decision"]
            accepted = decision == "eligible_existing_frontier_credit" and gates_pass(row["gates"])
            rights = {
                "review_finding": row.get("rights_finding"),
                "gate": row["gates"].get("rights"),
            }
            references = row.get("primary_references", row.get("primary_resolution_references", []))
            stage_id = row["stage_claim_id"]
            variant_id = row["variant_id"]
            semantic = row["semantic_key"]
        claim = catalog_by_id.get(stage_id)
        require(claim is not None, f"{label}: review parent absent from catalog")
        require(claim.get("variant_id") == variant_id, f"{label}: review variant/catalog mismatch")
        normalized.append(
            {
                "lane": lane,
                "candidate_index": emitted_index,
                "stage_claim_id": stage_id,
                "variant_id": variant_id,
                "semantic_key": semantic,
                "decision": decision,
                "accepted": accepted,
                "all_gates_pass": gates_pass(row["gates"])
                and row.get("all_gates_pass", True) is True,
                "rights_evidence": rights,
                "primary_references": references,
                "review_binding": {
                    "path": item["relative"].as_posix(),
                    "file_sha256": digest(item["payload"]),
                    "line_number": item["line_number"],
                    "review_row_sha256": digest(canonical(row)),
                },
            }
        )
    return normalized, file_inputs


def validate_actual_qualification(
    document: dict[str, Any],
    *,
    root: Path,
    important_ids: set[str],
    parent_theorems: Mapping[str, Mapping[str, Any]],
) -> None:
    authority_is_valid(document, "frontier qualification")
    require(document.get("schema_version") == "awesome-theorems/frontier-theorem-qualification/5.5", "qualification schema mismatch")
    counts = document.get("counts")
    require(isinstance(counts, dict), "qualification counts is not an object")
    require(
        set(counts)
        == {
            "review_rows",
            "review_accepted_before_global_dedupe",
            "accepted_additional_frontier_theorems",
            "accepted_distinct_important_landmarks",
            "new_theorem_identity_credits",
            "unsupported_importance_or_frontier_credit",
            "pending_not_credited",
            "rejected_not_credited",
        }
        and all(type(value) is int for value in counts.values()),
        "qualification count fields are not closed strict integers",
    )
    credits = document.get("accepted_credits")
    require(isinstance(credits, list), "qualification accepted credits is not a list")
    require(MIN_CREDITS <= len(credits) <= MAX_CREDITS, "qualification credit count misses 500-1000 gate")
    stage_ids: list[str] = []
    variant_ids: list[str] = []
    semantic_keys: list[str] = []
    row_hashes: list[str] = []
    for position, row in enumerate(credits, start=1):
        require(isinstance(row, dict), f"qualification credit {position} is not object")
        require(row.get("accepted_rank") == position, f"qualification credit rank mismatch: {position}")
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"qualification credit row hash mismatch: {position}")
        stage_id = row.get("stage_claim_id")
        variant_id = row.get("variant_id")
        semantic = row.get("semantic_key")
        require(stage_id in parent_theorems, f"qualification credit is not a parent theorem: {stage_id}")
        require(stage_id not in important_ids, f"qualification credit overlaps important inventory: {stage_id}")
        require(parent_theorems[stage_id].get("variant_id") == variant_id, f"qualification parent variant mismatch: {stage_id}")
        require(row.get("decision") == "accept" and row.get("all_gates_pass") is True, f"qualification credit lacks passed decision: {stage_id}")
        require(row.get("grants_frontier_theorem_credit") is True, f"qualification frontier credit missing: {stage_id}")
        require(row.get("grants_new_theorem_identity_credit") is False, f"qualification new theorem credit escalation: {stage_id}")
        binding = row.get("review_binding")
        require(isinstance(binding, dict), f"qualification review binding malformed: {stage_id}")
        relative = Path(str(binding.get("path")))
        review_path = safe_path(root, relative)
        require(file_digest(review_path) == binding.get("file_sha256"), f"qualification review file hash mismatch: {stage_id}")
        stage_ids.append(stage_id)
        variant_ids.append(variant_id)
        semantic_keys.append(semantic)
        row_hashes.append(row["row_sha256"])
    require(len(set(stage_ids)) == len(stage_ids), "qualification stage identity duplicate")
    require(len(set(variant_ids)) == len(variant_ids), "qualification variant identity duplicate")
    require(len(set(semantic_keys)) == len(semantic_keys), "qualification semantic duplicate")
    require(
        document.get("set_digests")
        == {
            "accepted_stage_claim_id_set_sha256": set_digest(stage_ids),
            "accepted_variant_id_set_sha256": set_digest(variant_ids),
            "accepted_semantic_key_set_sha256": set_digest(semantic_keys),
            "accepted_row_sha256_set_sha256": set_digest(row_hashes),
        },
        "qualification set digests mismatch",
    )
    review_inputs = document.get("inputs", {}).get("review_ledgers")
    require(isinstance(review_inputs, list), "qualification review input inventory malformed")
    for item in review_inputs:
        require(isinstance(item, dict), "qualification review input is not object")
        relative = Path(str(item.get("path")))
        path = safe_path(root, relative)
        payload = path.read_bytes()
        require(item.get("file_sha256") == digest(payload), f"qualification review ledger file hash mismatch: {relative}")
        require(item.get("size_bytes") == len(payload), f"qualification review ledger byte count mismatch: {relative}")
        require(item.get("rows") == len(payload.splitlines()), f"qualification review ledger row count mismatch: {relative}")
    candidate_inputs = document.get("inputs", {}).get("candidate_queues")
    require(isinstance(candidate_inputs, list), "qualification candidate queue inventory malformed")
    expected_candidate_rows = {
        ERDOS_PRIMARY_REL: 379,
        ERDOS_SUPPLEMENTAL_REL: 167,
        NONERDOS_PRIMARY_REL: 254,
        NONERDOS_SUPPLEMENTAL_REL: 117,
    }
    require(len(candidate_inputs) == 4, "qualification candidate queue inventory denominator drifted")
    for item in candidate_inputs:
        require(isinstance(item, dict), "qualification candidate queue input is not object")
        relative = Path(str(item.get("path")))
        require(relative in expected_candidate_rows, f"qualification unexpected candidate queue: {relative}")
        path = safe_path(root, relative)
        require(item.get("file_sha256") == file_digest(path), f"qualification candidate queue file hash mismatch: {relative}")
        require(item.get("rows") == expected_candidate_rows[relative], f"qualification candidate queue row count mismatch: {relative}")


def expected_document(
    *,
    normalized: list[dict[str, Any]],
    review_inputs: list[dict[str, Any]],
    important: dict[str, Any],
    parent_theorems: Mapping[str, Mapping[str, Any]],
    important_ids: set[str],
) -> dict[str, Any]:
    accepted = [row for row in normalized if row["accepted"]]
    accepted.sort(
        key=lambda row: (
            LANE_ORDER[row["lane"]],
            row["candidate_index"],
            row["stage_claim_id"],
        )
    )
    seen_stage: set[str] = set()
    seen_variant: set[str] = set()
    seen_semantic: set[str] = set()
    credits: list[dict[str, Any]] = []
    for source in accepted:
        stage_id = source["stage_claim_id"]
        variant_id = source["variant_id"]
        semantic = source["semantic_key"]
        require(stage_id in parent_theorems, f"accepted review is not parent theorem: {stage_id}")
        require(stage_id not in important_ids, f"accepted review overlaps important inventory: {stage_id}")
        require(stage_id not in seen_stage, f"accepted stage identity duplicate: {stage_id}")
        require(variant_id not in seen_variant, f"accepted variant identity duplicate: {variant_id}")
        require(semantic not in seen_semantic, f"accepted semantic duplicate: {semantic}")
        row = {
            "accepted_rank": len(credits) + 1,
            "stage_claim_id": stage_id,
            "variant_id": variant_id,
            "semantic_key": semantic,
            "source_lane": source["lane"],
            "source_candidate_index": source["candidate_index"],
            "decision": "accept",
            "all_gates_pass": True,
            "rights_evidence": source["rights_evidence"],
            "primary_references": source["primary_references"],
            "review_binding": source["review_binding"],
            "grants_frontier_theorem_credit": True,
            "grants_new_theorem_identity_credit": False,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        credits.append(row)
        seen_stage.add(stage_id)
        seen_variant.add(variant_id)
        seen_semantic.add(semantic)
    require(MIN_CREDITS <= len(credits) <= MAX_CREDITS, f"replayed accepted frontier count {len(credits)} misses 500-1000 gate")
    document: dict[str, Any] = {
        "schema_version": "awesome-theorems/frontier-theorem-qualification/5.5",
        "review_as_of": "2026-08-10",
        "parent": {
            "release": "5.4",
            "release_root_sha256": PARENT_ROOT,
            "claim_catalog_sha256": FIXED_FILE_SHA256[CATALOG_REL],
            "release_manifest_sha256": FIXED_FILE_SHA256[MANIFEST_REL],
        },
        "scope": {
            "existing_parent_theorem_quality_credit_only": True,
            "creates_new_theorem_identities": False,
            "important_and_frontier_quota_sets_disjoint": True,
            "candidate_or_pending_rows_receive_credit": False,
        },
        "inputs": {
            "review_ledgers": review_inputs,
            "candidate_queues": [
                {
                    "path": relative.as_posix(),
                    "file_sha256": FIXED_FILE_SHA256[relative],
                    "rows": rows,
                }
                for relative, rows in (
                    (ERDOS_PRIMARY_REL, 379),
                    (ERDOS_SUPPLEMENTAL_REL, 167),
                    (NONERDOS_PRIMARY_REL, 254),
                    (NONERDOS_SUPPLEMENTAL_REL, 117),
                )
            ],
            "important_inventory": {
                "path": IMPORTANT_REL.as_posix(),
                "file_sha256": FIXED_FILE_SHA256[IMPORTANT_REL],
                "authority_sha256": important["authority_sha256"],
                "rows": 1_000,
            },
        },
        "accepted_credits": credits,
        "counts": {
            "review_rows": len(normalized),
            "review_accepted_before_global_dedupe": len(accepted),
            "accepted_additional_frontier_theorems": len(credits),
            "accepted_distinct_important_landmarks": 1_000,
            "new_theorem_identity_credits": 0,
            "unsupported_importance_or_frontier_credit": 0,
            "pending_not_credited": sum(row["decision"] == "pending" for row in normalized),
            "rejected_not_credited": sum(row["decision"] == "reject" for row in normalized),
        },
        "set_digests": {
            "accepted_stage_claim_id_set_sha256": set_digest(row["stage_claim_id"] for row in credits),
            "accepted_variant_id_set_sha256": set_digest(row["variant_id"] for row in credits),
            "accepted_semantic_key_set_sha256": set_digest(row["semantic_key"] for row in credits),
            "accepted_row_sha256_set_sha256": set_digest(row["row_sha256"] for row in credits),
        },
    }
    document["authority_sha256"] = hash_without(document, "authority_sha256")
    return document


def verify(repo_root: Path, qualification_relative: Path = QUALIFICATION_REL) -> dict[str, Any]:
    root = repo_root.resolve(strict=True)
    catalog, _ = load_fixed_json(root, CATALOG_REL)
    manifest, _ = load_fixed_json(root, MANIFEST_REL)
    important, _ = load_fixed_json(root, IMPORTANT_REL)
    erdos_primary, _ = load_fixed_jsonl(root, ERDOS_PRIMARY_REL)
    erdos_supplemental, _ = load_fixed_jsonl(root, ERDOS_SUPPLEMENTAL_REL)
    nonerdos_primary_doc, _ = load_fixed_json(root, NONERDOS_PRIMARY_REL)
    nonerdos_supplemental_doc, _ = load_fixed_json(root, NONERDOS_SUPPLEMENTAL_REL)

    require(manifest.get("release_root_sha256") == PARENT_ROOT, "parent release root drifted")
    catalog_rows = catalog.get("records")
    require(isinstance(catalog_rows, list) and len(catalog_rows) == 4_100, "parent catalog denominator drifted")
    catalog_by_id = {row.get("stage_claim_id"): row for row in catalog_rows if isinstance(row, dict)}
    require(len(catalog_by_id) == 4_100 and None not in catalog_by_id, "parent catalog IDs are not unique")
    parent_theorems = {
        stage_id: row
        for stage_id, row in catalog_by_id.items()
        if row.get("current_claim_kind") == "theorem" and row.get("material_status") == "proved"
    }
    require(len(parent_theorems) == 2_500, "parent theorem denominator drifted")

    authority_is_valid(important, "important inventory")
    require(important.get("authority_sha256") == IMPORTANT_AUTHORITY, "important inventory authority constant drifted")
    important_rows = important.get("records")
    require(isinstance(important_rows, list) and len(important_rows) == 1_000, "important inventory denominator drifted")
    important_ids = {row.get("stage_claim_id") for row in important_rows if isinstance(row, dict)}
    require(len(important_ids) == 1_000 and None not in important_ids, "important inventory IDs are not unique")

    require(len(erdos_primary) == 379, "Erdos primary candidate denominator drifted")
    require(len(erdos_supplemental) == 167, "Erdos supplemental candidate denominator drifted")
    nonerdos_primary = validate_nonerdos_queue(
        nonerdos_primary_doc,
        supplemental=False,
        catalog_by_id=catalog_by_id,
    )
    nonerdos_supplemental = validate_nonerdos_queue(
        nonerdos_supplemental_doc,
        supplemental=True,
        catalog_by_id=catalog_by_id,
    )
    candidate_identities: list[tuple[str, str, str]] = []
    for index, candidate in enumerate(erdos_primary):
        stage, semantic = validate_parent_candidate(candidate, catalog_by_id, f"Erdos primary candidate {index}")
        candidate_identities.append((stage, candidate["parent"]["variant_id"], semantic))
    for index, candidate in enumerate(erdos_supplemental):
        stage, semantic = validate_parent_candidate(candidate, catalog_by_id, f"Erdos supplemental candidate {index}")
        candidate_identities.append((stage, candidate["parent"]["variant_id"], semantic))
    for candidate in [*nonerdos_primary.values(), *nonerdos_supplemental.values()]:
        candidate_identities.append(
            (candidate["stage_claim_id"], candidate["variant_id"], candidate["semantic_key"])
        )
    require(len(candidate_identities) == 917, "frontier candidate union denominator drifted")
    require(len({item[0] for item in candidate_identities}) == 917, "frontier candidate stage identity duplicate")
    require(len({item[1] for item in candidate_identities}) == 917, "frontier candidate variant identity duplicate")
    require(len({item[2] for item in candidate_identities}) == 917, "frontier candidate semantic identity duplicate")
    require(not ({item[0] for item in candidate_identities} & important_ids), "frontier candidates overlap important inventory")

    normalized, review_inputs = collect_and_validate_reviews(
        root,
        catalog_by_id=catalog_by_id,
        erdos_primary=erdos_primary,
        erdos_supplemental=erdos_supplemental,
        nonerdos_primary=nonerdos_primary,
        nonerdos_supplemental=nonerdos_supplemental,
    )
    expected = expected_document(
        normalized=normalized,
        review_inputs=review_inputs,
        important=important,
        parent_theorems=parent_theorems,
        important_ids=important_ids,
    )
    try:
        qualification_path = safe_path(root, qualification_relative)
    except FileNotFoundError as error:
        raise CheckError(f"qualification artifact missing: {qualification_relative}") from error
    payload = qualification_path.read_bytes()
    actual = parse_json(payload, qualification_relative.as_posix())
    validate_actual_qualification(
        actual,
        root=root,
        important_ids=important_ids,
        parent_theorems=parent_theorems,
    )
    require(actual == expected, "qualification document differs from independent full replay")
    require(payload == canonical(expected) + b"\n", "qualification bytes are not canonical or lack terminal LF")
    return actual


def acceptance_receipt(
    document: dict[str, Any],
    *,
    root: Path,
    qualification_relative: Path,
    checker_path: Path,
) -> dict[str, Any]:
    qualification_path = safe_path(root, qualification_relative)
    reviews = document["inputs"]["review_ledgers"]
    receipt: dict[str, Any] = {
        "schema_version": "awesome-theorems/frontier-theorem-qualification-acceptance-receipt/5.5",
        "review_as_of": "2026-08-10",
        "qualification": {
            "path": qualification_relative.as_posix(),
            "file_sha256": file_digest(qualification_path),
            "authority_sha256": document["authority_sha256"],
        },
        "checker": {
            "path": checker_path.resolve(strict=True).relative_to(root).as_posix(),
            "file_sha256": file_digest(checker_path.resolve(strict=True)),
            "independent_from_builder": True,
            "read_only": True,
        },
        "review_manifest": {
            "files": len(reviews),
            "rows": sum(item["rows"] for item in reviews),
            "manifest_sha256": digest(canonical(reviews)),
            "file_sha256_set_sha256": set_digest(
                item["file_sha256"] for item in reviews
            ),
            "entries": reviews,
        },
        "counts": document["counts"],
        "findings": [],
    }
    receipt["authority_sha256"] = hash_without(receipt, "authority_sha256")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--qualification", type=Path, default=QUALIFICATION_REL)
    parser.add_argument(
        "--receipt-json",
        action="store_true",
        help="emit a canonical acceptance receipt to stdout after full validation",
    )
    args = parser.parse_args()
    try:
        document = verify(args.repo_root, args.qualification)
        receipt = (
            acceptance_receipt(
                document,
                root=args.repo_root.resolve(strict=True),
                qualification_relative=args.qualification,
                checker_path=Path(__file__),
            )
            if args.receipt_json
            else None
        )
    except (
        CheckError,
        OSError,
        ValueError,
        json.JSONDecodeError,
        KeyError,
        IndexError,
        TypeError,
    ) as error:
        print(f"FAIL frontier theorem qualification: {error}")
        return 1
    if args.receipt_json:
        assert receipt is not None
        print(canonical(receipt).decode("utf-8"))
        return 0
    print(
        "PASS frontier theorem qualification "
        f"reviewed={document['counts']['review_rows']} "
        f"accepted={document['counts']['accepted_additional_frontier_theorems']} "
        f"authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
