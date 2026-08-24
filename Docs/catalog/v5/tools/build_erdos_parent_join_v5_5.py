#!/usr/bin/env python3
"""Build a pinned Erdős Problems ↔ awesome-theorems 5.4 exact join.

This is an audit asset only.  It never edits the release.  Problem-level status
is joined by the exact decimal problem number encoded in both the parent module
and qualified declaration name.  Credit remains declaration/identity-level:
an open problem page does not turn theorem subclaims or unoriented questions
into strict conjecture credits.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import tarfile
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[4]
ERDOS_COMMIT = "af90db960021ff3247f0374e015dae97b5125ff6"
ERDOS_TREE = "931fc5b8a230485d49f095b59bbd30e6a0466455"
ERDOS_ARCHIVE_SHA256 = "a9125786b0ccf2da2c5411b0eb9c80f6b2cd2717d140606e136314e76bc0be58"
ERDOS_PROBLEMS_SHA256 = "14007c54a9ad0a9560966bd782f3303db898c6387df02754219dc585ef8b989d"
ERDOS_LICENSE_SHA256 = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
ERDOS_SNAPSHOT_SHA256 = "5425b13a9d77ac3136cdea0f52d754f5f11ae8bff74943577f1b45c3bb665956"
ERDOS_SNAPSHOT_AUTHORITY = "8aeeda4f44f36240fc2ca752df5baae2ac30c31747b7c22d568edcae75e02601"
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_CATALOG_AUTHORITY = "f52d1634a2e65add6835856d7043a1723cb9669538d4435b51ef5d1776942f4d"
PARENT_LEDGER_SHA256 = "52ba1ccf06462741bcc48028fb121e5e30d1e7b56128cfeb910dc56a2e1a83a3"
PARENT_LEDGER_AUTHORITY = "466190eecfc997f7b92729c79623537137283b818f13ecead3ff6cd4b8f0322e"
PARENT_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
PARENT_MANIFEST_AUTHORITY = "3e4e2bf258bfec3e7247d755522aba402c4b1e28c25cc1c93c681e66793dcf3d"
SOURCE_REPOSITORY = "https://github.com/teorth/erdosproblems"
SCHEMA_VERSION = "awesome-theorems/erdos-parent-exact-join-audit/5.5"
DEFAULT_ARCHIVE = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz"
DEFAULT_SNAPSHOT = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
DEFAULT_RELEASE_ROOT = REPO_ROOT / "Docs/catalog/v5/releases/5.4"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "Docs/catalog/v5/curation/erdos_parent_join_v5_5"

RESOLVED_STATES = {"proved", "disproved", "solved"}
FINITE_OR_LOGICALLY_CLASSIFIED_UNRESOLVED = {
    "falsifiable",
    "verifiable",
    "decidable",
    "not provable",
    "not disprovable",
    "independent",
}
UNRESOLVED_STATES = {"open"} | FINITE_OR_LOGICALLY_CLASSIFIED_UNRESOLVED

DATA_ARTIFACTS = [
    "source-problems.jsonl",
    "parent-erdos-join.jsonl",
    "problem-groups.jsonl",
    "current-open-identities.jsonl",
    "existing-strict-credits.jsonl",
    "polarity-review-backlog.jsonl",
    "new-credit-review-candidates.jsonl",
    "status-conflicts.jsonl",
    "resolved-theorem-rows.jsonl",
    "resolved-theorem-file-capacity.jsonl",
    "resolved-theorem-max2-selected.jsonl",
    "research-solved-upstream-open-drift.jsonl",
    "summary.json",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def canonical_line(value: Any) -> bytes:
    return canonical_bytes(value) + b"\n"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_line(value))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    payload = b"".join(canonical_line(row) for row in rows)
    path.write_bytes(payload)


def require_file_sha(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    actual = sha256_bytes(data)
    if actual != expected:
        raise SystemExit(f"SHA-256 mismatch for {path}: {actual} != {expected}")
    return data


def hash_without(value: dict[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha256_bytes(canonical_bytes({key: item for key, item in value.items() if key not in ignored}))


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as error:
        raise SystemExit(f"authority path escapes repository: {path}") from error


def verify_archive(archive_path: Path) -> None:
    require_file_sha(archive_path, ERDOS_ARCHIVE_SHA256)
    with tarfile.open(archive_path, "r:gz") as stream:
        members = stream.getmembers()
        if [member.name for member in members] != ["LICENSE", "data", "data/problems.yaml"]:
            raise SystemExit("unexpected pinned Erdős archive inventory")
        extracted: dict[str, bytes] = {}
        for member in members:
            if member.isdir():
                continue
            if not member.isfile() or member.name.startswith("/") or ".." in Path(member.name).parts:
                raise SystemExit(f"unsafe pinned archive member: {member.name}")
            handle = stream.extractfile(member)
            if handle is None:
                raise SystemExit(f"cannot read archive member: {member.name}")
            extracted[member.name] = handle.read()
    if sha256_bytes(extracted["data/problems.yaml"]) != ERDOS_PROBLEMS_SHA256:
        raise SystemExit("archived problems.yaml digest mismatch")
    if sha256_bytes(extracted["LICENSE"]) != ERDOS_LICENSE_SHA256:
        raise SystemExit("archived LICENSE digest mismatch")


def complete_truth_apt(record: dict[str, Any]) -> bool:
    statement = record.get("mathematical_statement") or {}
    return bool(
        record.get("truth_apt") is True
        and isinstance(statement.get("natural_language"), str)
        and statement["natural_language"].strip()
        and isinstance(statement.get("formal_type"), str)
        and statement["formal_type"].strip()
        and statement.get("completeness") not in {None, "incomplete"}
    )


def semantic_role(problem_number: int, qualified_name: str) -> str:
    if qualified_name == f"Erdos{problem_number}.erdos_{problem_number}":
        return "base"
    if any(token in qualified_name for token in (".variants.", ".variant.", ".varaints.")):
        return "variant"
    if ".parts." in qualified_name:
        return "part"
    return "other_subclaim"


def current_status_relation(source_state: str, parent_material_status: str) -> str:
    if source_state == "open" and parent_material_status == "open":
        return "aligned_current_open"
    if source_state == "open" and parent_material_status == "proved":
        return "problem_open_but_declaration_is_proved_subclaim"
    if source_state in RESOLVED_STATES and parent_material_status == "open":
        return "parent_open_conflicts_with_current_problem_resolution"
    if source_state in RESOLVED_STATES and parent_material_status == "proved":
        return "aligned_resolved_or_proved_subclaim"
    if source_state in FINITE_OR_LOGICALLY_CLASSIFIED_UNRESOLVED and parent_material_status == "open":
        return "current_unresolved_but_not_exact_open"
    if source_state in FINITE_OR_LOGICALLY_CLASSIFIED_UNRESOLVED and parent_material_status == "proved":
        return "classified_problem_with_proved_subclaim"
    return "other_status_combination"


def fixed_problem_page_binding(number: int, source: dict[str, Any]) -> dict[str, Any]:
    """Return stable numeric-page locators plus the pinned status authority.

    erdosproblems.com page bodies are live, so the pinned teorth record—not the
    HTML pointer—is the fixity authority for current status.  The numeric page,
    history, LaTeX, bibliography container, and remarks selectors are recorded
    as locators rather than silently treated as immutable content.
    """
    page = f"https://www.erdosproblems.com/{number}"
    return {
        "bibliography_locator": {
            "citation_key_links_css_selector": "#problem_id a[href^='#bib-container']",
            "container_anchor": f"{page}#bib-container{number}",
            "dynamic_bibliography_endpoint_template": "https://www.erdosproblems.com/bibs/{citation_key}",
            "fixity": "live_pointer",
        },
        "current_status_locator": {
            "derived_status": source["status"],
            "informal_status": source["informal_status"],
            "pinned_archive_path": "Docs/catalog/v5/sources/erdosproblems-af90db96-source.tar.gz",
            "pinned_archive_sha256": ERDOS_ARCHIVE_SHA256,
            "pinned_problem_number": str(number),
            "pinned_snapshot_authority_sha256": ERDOS_SNAPSHOT_AUTHORITY,
            "pinned_snapshot_path": "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json",
            "pinned_source_record_sha256": source["row_sha256"],
            "status_page_css_selector": ".problem-text[id] #prize",
        },
        "history_locator": f"https://www.erdosproblems.com/history/{number}",
        "latex_source_locator": f"https://www.erdosproblems.com/latex/{number}",
        "page_fixity_boundary": (
            "Numeric page/history/LaTeX are stable locators but live content. Current-status fixity comes from the "
            "pinned teorth commit and record hash."
        ),
        "problem_page_url": page,
        "remarks_locator": {
            "css_selector": ".problem-additional-text",
            "history_url": f"https://www.erdosproblems.com/history/{number}",
            "latex_url": f"https://www.erdosproblems.com/latex/{number}",
            "page_url": page,
        },
    }


def credit_assessment(
    *,
    existing_credit: bool,
    source_state: str,
    parent_record: dict[str, Any],
    complete: bool,
) -> tuple[str, bool]:
    if existing_credit:
        return "existing_strict_credit", False
    if parent_record["current_claim_kind"] == "theorem":
        return "theorem_subclaim_not_conjecture_credit", False
    if source_state in RESOLVED_STATES:
        return "current_problem_resolved_no_new_credit", False
    if source_state != "open":
        return "not_exact_current_open_no_new_credit", False
    if parent_record["material_status"] != "open" or not complete:
        return "parent_open_or_statement_gate_not_met", False
    if parent_record["current_claim_kind"] == "open_problem":
        return "question_has_no_asserted_conjectural_direction", False
    if parent_record["current_claim_kind"] == "conjecture":
        return "uncredited_asserted_conjecture_requires_independent_strict_review", True
    return "unsupported_claim_kind", False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--release-root", type=Path, default=DEFAULT_RELEASE_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    archive_path = args.archive.resolve()
    snapshot_path = args.snapshot.resolve()
    args.release_root = args.release_root.resolve()
    args.output_dir = args.output_dir.resolve()
    repo_relative(archive_path, repo_root)
    repo_relative(snapshot_path, repo_root)
    repo_relative(args.release_root, repo_root)
    repo_relative(args.output_dir, repo_root)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    catalog_path = args.release_root / "Claim_Catalog.json"
    ledger_path = args.release_root / "Strict_Conjecture_Ledger.json"
    manifest_path = args.release_root / "Release_Manifest.json"

    verify_archive(archive_path)
    snapshot_bytes = require_file_sha(snapshot_path, ERDOS_SNAPSHOT_SHA256)
    catalog_bytes = require_file_sha(catalog_path, PARENT_CATALOG_SHA256)
    ledger_bytes = require_file_sha(ledger_path, PARENT_LEDGER_SHA256)
    manifest_bytes = require_file_sha(manifest_path, PARENT_MANIFEST_SHA256)

    snapshot = json.loads(snapshot_bytes)
    if snapshot_bytes != canonical_line(snapshot):
        raise SystemExit("noncanonical pinned Erdős status snapshot")
    if snapshot.get("schema_version") != "awesome-theorems/erdosproblems-status-snapshot/1.0":
        raise SystemExit("pinned Erdős snapshot schema mismatch")
    if snapshot.get("authority_sha256") != ERDOS_SNAPSHOT_AUTHORITY:
        raise SystemExit("pinned Erdős snapshot authority mismatch")
    if hash_without(snapshot, "authority_sha256") != ERDOS_SNAPSHOT_AUTHORITY:
        raise SystemExit("pinned Erdős snapshot authority does not replay")
    expected_source_binding = {
        "archive_sha256": ERDOS_ARCHIVE_SHA256,
        "commit": ERDOS_COMMIT,
        "license_sha256": ERDOS_LICENSE_SHA256,
        "problems_sha256": ERDOS_PROBLEMS_SHA256,
        "tree": ERDOS_TREE,
    }
    for field, expected in expected_source_binding.items():
        if snapshot["source"].get(field) != expected:
            raise SystemExit(f"pinned Erdős snapshot source binding mismatch: {field}")
    source_raw = snapshot.get("records")
    if not isinstance(source_raw, list) or len(source_raw) != 1217:
        raise SystemExit("Erdős status snapshot must contain 1217 records")
    source_by_number: dict[int, dict[str, Any]] = {}
    source_rows: list[dict[str, Any]] = []
    for expected_source_index, source_record in enumerate(source_raw):
        number = source_record.get("problem_number")
        if not isinstance(number, int) or number <= 0:
            raise SystemExit(f"invalid snapshot problem number: {number}")
        if source_record.get("source_index") != expected_source_index:
            raise SystemExit(f"snapshot source index mismatch for problem {number}")
        if hash_without(source_record, "row_sha256") != source_record.get("row_sha256"):
            raise SystemExit(f"snapshot row digest mismatch for problem {number}")
        if number in source_by_number:
            raise SystemExit(f"duplicate source problem number: {number}")
        source_by_number[number] = source_record
        informal = source_record.get("informal_status") or {}
        derived = source_record.get("status") or {}
        row = {
            "derived_status": derived,
            "formal_status": source_record.get("formal_status"),
            "formalized_statement": source_record.get("formalized"),
            "has_monetary_prize": bool(source_record.get("prize") and source_record.get("prize") != "no"),
            "informal_status": informal,
            "is_current_exact_open": informal.get("state") == "open",
            "is_current_unresolved_broad": informal.get("state") in UNRESOLVED_STATES,
            "last_update": derived.get("last_update"),
            "oeis": source_record.get("oeis_raw", []),
            "prize": source_record.get("prize"),
            "problem_number": number,
            "problem_number_text": str(number),
            "problem_url": source_record["upstream_page"],
            "schema_version": SCHEMA_VERSION,
            "source_commit": ERDOS_COMMIT,
            "source_index": expected_source_index,
            "source_record_sha256": source_record["row_sha256"],
            "source_snapshot_authority_sha256": ERDOS_SNAPSHOT_AUTHORITY,
            "tags": source_record.get("tags", []),
        }
        source_rows.append(row)

    catalog = json.loads(catalog_bytes)
    ledger = json.loads(ledger_bytes)
    manifest = json.loads(manifest_bytes)
    if catalog.get("release") != "5.4" or ledger.get("release") != "5.4" or manifest.get("release") != "5.4":
        raise SystemExit("parent release mismatch")
    if catalog.get("authority_sha256") != PARENT_CATALOG_AUTHORITY:
        raise SystemExit("parent catalog authority mismatch")
    if ledger.get("authority_sha256") != PARENT_LEDGER_AUTHORITY:
        raise SystemExit("parent ledger authority mismatch")
    if manifest.get("authority_sha256") != PARENT_MANIFEST_AUTHORITY:
        raise SystemExit("parent manifest authority mismatch")

    effective_credit_rows = {
        row["stage_claim_id"]: row
        for row in ledger["strict_credits"]
        if row.get("grants_strict_conjecture_credit") is True
    }
    for correction in ledger.get("credit_corrections", []):
        if correction.get("grants_strict_conjecture_credit") is False:
            effective_credit_rows.pop(correction["stage_claim_id"], None)

    parent_erdos: list[tuple[int, int, dict[str, Any]]] = []
    for catalog_index, record in enumerate(catalog["records"]):
        module_match = re.fullmatch(r"FormalConjectures\.ErdosProblems\.(\d+)", record.get("module", ""))
        if not module_match:
            continue
        qname_match = re.match(r"^Erdos(\d+)\.", record.get("qualified_name", ""))
        if not qname_match or qname_match.group(1) != module_match.group(1):
            raise SystemExit(f"module/qname problem-number mismatch for {record['stage_claim_id']}")
        number = int(module_match.group(1))
        if number not in source_by_number:
            raise SystemExit(f"parent problem number missing from source: {number}")
        parent_erdos.append((catalog_index, number, record))

    identity_groups: dict[str, list[str]] = collections.defaultdict(list)
    for _, _, record in parent_erdos:
        identity_groups[record["dedupe"]["identity_payload_sha256"]].append(record["stage_claim_id"])

    join_rows: list[dict[str, Any]] = []
    for catalog_index, number, record in parent_erdos:
        source = source_by_number[number]
        informal = source["informal_status"]
        derived = source["status"]
        complete = complete_truth_apt(record)
        credit_row = effective_credit_rows.get(record["stage_claim_id"])
        assessment, review_candidate = credit_assessment(
            existing_credit=credit_row is not None,
            source_state=informal["state"],
            parent_record=record,
            complete=complete,
        )
        identity_hash = record["dedupe"]["identity_payload_sha256"]
        row = {
            "credit": {
                "assessment": assessment,
                "existing_strict_credit": credit_row is not None,
                "existing_strict_credit_row": credit_row,
                "grants_new_credit_from_this_audit": False,
                "new_credit_review_candidate": review_candidate,
                "problem_presence_grants_credit": False,
            },
            "exact_join": {
                "key": str(number),
                "method": "decimal_problem_number_equal_in_source_module_and_qualified_name",
                "module_problem_number": number,
                "qualified_name_problem_number": number,
                "source_problem_number": number,
            },
            "identity": {
                "dedupe_verdict": record["dedupe"]["verdict"],
                "exact_identity_duplicate_group_size": len(identity_groups[identity_hash]),
                "exact_identity_duplicate_stage_claim_ids": identity_groups[identity_hash],
                "identity_payload_sha256": identity_hash,
                "role_within_problem": semantic_role(number, record["qualified_name"]),
                "semantic_identity_key": f"formal-conjectures-parent-identity/{identity_hash}",
                "semantic_payload_sha256": record["semantic_payload_sha256"],
            },
            "parent": {
                "atomicity": record["atomicity"],
                "catalog_index": catalog_index,
                "current_claim_kind": record["current_claim_kind"],
                "dedupe": record["dedupe"],
                "family_id": record["family_id"],
                "formal_type_sha256": record["formal_type_sha256"],
                "locator": record["locator"],
                "material_status": record["material_status"],
                "mathematical_statement": record["mathematical_statement"],
                "module": record["module"],
                "origin_release": record["origin_release"],
                "qualified_name": record["qualified_name"],
                "raw_status": record["raw_status"],
                "sense_id": record["sense_id"],
                "stage_claim_id": record["stage_claim_id"],
                "truth_apt": record["truth_apt"],
                "variant_id": record["variant_id"],
            },
            "schema_version": SCHEMA_VERSION,
            "source_problem": {
                "derived_status": derived,
                "formal_status": source.get("formal_status"),
                "informal_status": informal,
                "is_current_exact_open": informal["state"] == "open",
                "is_current_unresolved_broad": informal["state"] in UNRESOLVED_STATES,
                "last_update": derived.get("last_update"),
                "prize": source.get("prize"),
                "problem_number": number,
                "problem_url": f"https://www.erdosproblems.com/{number}",
                "source_record_sha256": source["row_sha256"],
                "source_snapshot_authority_sha256": ERDOS_SNAPSHOT_AUTHORITY,
                "tags": source.get("tags", []),
            },
            "statement_gate": {
                "complete_truth_apt": complete,
                "completeness": record["mathematical_statement"].get("completeness"),
                "truth_apt": record["truth_apt"],
            },
            "status_relation": current_status_relation(informal["state"], record["material_status"]),
        }
        join_rows.append(row)

    groups: list[dict[str, Any]] = []
    rows_by_problem: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in join_rows:
        rows_by_problem[row["source_problem"]["problem_number"]].append(row)
    for number in sorted(rows_by_problem):
        rows = rows_by_problem[number]
        source = rows[0]["source_problem"]
        roles: dict[str, list[str]] = collections.defaultdict(list)
        for row in rows:
            roles[row["identity"]["role_within_problem"]].append(row["parent"]["stage_claim_id"])
        groups.append(
            {
                "current_open_identity_stage_claim_ids": [
                    row["parent"]["stage_claim_id"]
                    for row in rows
                    if source["is_current_exact_open"]
                    and row["parent"]["material_status"] == "open"
                    and row["statement_gate"]["complete_truth_apt"]
                ],
                "existing_strict_credit_stage_claim_ids": [
                    row["parent"]["stage_claim_id"] for row in rows if row["credit"]["existing_strict_credit"]
                ],
                "problem_number": number,
                "problem_url": source["problem_url"],
                "role_stage_claim_ids": dict(sorted(roles.items())),
                "row_count": len(rows),
                "schema_version": SCHEMA_VERSION,
                "source_derived_status": source["derived_status"],
                "source_informal_status": source["informal_status"],
                "source_prize": source["prize"],
                "source_tags": source["tags"],
            }
        )

    current_open = [
        row
        for row in join_rows
        if row["source_problem"]["is_current_exact_open"]
        and row["parent"]["material_status"] == "open"
        and row["statement_gate"]["complete_truth_apt"]
    ]
    existing_credits = [row for row in join_rows if row["credit"]["existing_strict_credit"]]
    polarity_backlog = [
        row
        for row in current_open
        if not row["credit"]["existing_strict_credit"]
        and row["parent"]["current_claim_kind"] == "open_problem"
    ]
    new_credit_candidates = [row for row in join_rows if row["credit"]["new_credit_review_candidate"]]
    status_conflicts = [
        row
        for row in join_rows
        if row["status_relation"] == "parent_open_conflicts_with_current_problem_resolution"
    ]
    research_solved_theorem_rows = [
        row
        for row in join_rows
        if row["parent"]["current_claim_kind"] == "theorem"
        and row["parent"]["raw_status"] == "research solved"
    ]
    resolved_theorem_rows = [
        row
        for row in research_solved_theorem_rows
        if row["source_problem"]["informal_status"]["state"] in RESOLVED_STATES
    ]
    resolved_by_file: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in resolved_theorem_rows:
        resolved_by_file[row["parent"]["locator"]["member_path"]].append(row)
    resolved_file_capacity = []
    resolved_theorem_selected = []
    for member_path in sorted(resolved_by_file):
        rows = sorted(resolved_by_file[member_path], key=lambda item: item["parent"]["catalog_index"])
        selected = rows[:2]
        number = rows[0]["source_problem"]["problem_number"]
        resolved_file_capacity.append(
            {
                "available_row_count": len(rows),
                "max2_available_count": len(selected),
                "member_path": member_path,
                "problem_number": number,
                "schema_version": SCHEMA_VERSION,
                "selected_stage_claim_ids": [row["parent"]["stage_claim_id"] for row in selected],
                "source_problem_binding": fixed_problem_page_binding(number, source_by_number[number]),
            }
        )
        for rank, row in enumerate(selected, 1):
            selected_row = dict(row)
            selected_row["theorem_selection"] = {
                "eligible_after_upstream_resolved_filter": True,
                "file_available_row_count": len(rows),
                "frontier_credit_allowed_from_problem_status_alone": False,
                "max_per_formal_conjectures_file": 2,
                "rank_within_file": rank,
                "source_problem_binding": fixed_problem_page_binding(number, source_by_number[number]),
            }
            resolved_theorem_selected.append(selected_row)
    research_solved_upstream_open_drift = []
    for row in research_solved_theorem_rows:
        if row["source_problem"]["informal_status"]["state"] != "open":
            continue
        drift_row = dict(row)
        number = row["source_problem"]["problem_number"]
        drift_row["theorem_status_drift"] = {
            "classification": "parent_research_solved_but_upstream_problem_current_open",
            "frontier_credit_allowed": False,
            "frontier_credit_prohibition_reason": (
                "Problem-level upstream status remains open. A solved subclaim may still be valid, but the problem page "
                "cannot be used as resolved-frontier evidence or as an additional theorem/conjecture credit."
            ),
            "source_problem_binding": fixed_problem_page_binding(number, source_by_number[number]),
        }
        research_solved_upstream_open_drift.append(drift_row)

    role_counts = collections.Counter(row["identity"]["role_within_problem"] for row in current_open)
    source_status_counts = collections.Counter(row["informal_status"]["state"] for row in source_rows)
    source_derived_status_counts = collections.Counter(row["derived_status"]["state"] for row in source_rows)
    parent_kind_counts = collections.Counter(row["parent"]["current_claim_kind"] for row in join_rows)
    parent_material_counts = collections.Counter(row["parent"]["material_status"] for row in join_rows)
    represented_problem_status_counts = collections.Counter(
        source_by_number[number]["informal_status"]["state"] for number in rows_by_problem
    )
    credit_status_counts = collections.Counter(
        row["source_problem"]["informal_status"]["state"] for row in existing_credits
    )
    current_open_kind_counts = collections.Counter(row["parent"]["current_claim_kind"] for row in current_open)
    exact_duplicate_groups = [members for members in identity_groups.values() if len(members) > 1]
    current_open_identity_keys = {row["identity"]["semantic_identity_key"] for row in current_open}

    summary = {
        "credit_accounting": {
            "existing_erdos_strict_credits": len(existing_credits),
            "existing_erdos_strict_credits_by_current_problem_status": dict(sorted(credit_status_counts.items())),
            "existing_credits_current_exact_open": sum(
                row["source_problem"]["is_current_exact_open"] for row in existing_credits
            ),
            "existing_credits_current_finite_or_logically_classified": sum(
                row["source_problem"]["informal_status"]["state"]
                in FINITE_OR_LOGICALLY_CLASSIFIED_UNRESOLVED
                for row in existing_credits
            ),
            "existing_credits_current_resolved_conflict": sum(
                row["source_problem"]["informal_status"]["state"] in RESOLVED_STATES
                for row in existing_credits
            ),
            "grants_new_credit_from_audit": 0,
            "mechanically_addable_new_credit": 0,
            "new_credit_review_candidates_with_asserted_conjecture_kind": len(new_credit_candidates),
            "polarity_review_backlog_open_problem_identities": len(polarity_backlog),
            "policy_boundary": (
                "Problem-page existence/status never grants credit. An uncredited open_problem question lacks an "
                "asserted conjectural direction; the join cannot convert it into strict conjecture credit."
            ),
        },
        "current_open_identity_inventory": {
            "by_parent_current_claim_kind": dict(sorted(current_open_kind_counts.items())),
            "by_role_within_problem": dict(sorted(role_counts.items())),
            "complete_truth_apt_distinct_identities": len(current_open_identity_keys),
            "exact_identity_duplicate_groups": len(exact_duplicate_groups),
            "exact_identity_duplicate_rows": sum(len(group) for group in exact_duplicate_groups),
            "existing_strict_credit": sum(row["credit"]["existing_strict_credit"] for row in current_open),
            "selection_rule": (
                "source informal_status.state == open AND parent material_status == open AND exact complete "
                "truth-apt statement; distinct by parent dedupe.identity_payload_sha256"
            ),
            "uncredited": sum(not row["credit"]["existing_strict_credit"] for row in current_open),
        },
        "join_counts": {
            "complete_truth_apt_parent_rows": sum(row["statement_gate"]["complete_truth_apt"] for row in join_rows),
            "parent_current_claim_kind": dict(sorted(parent_kind_counts.items())),
            "parent_erdos_records": len(join_rows),
            "parent_material_status": dict(sorted(parent_material_counts.items())),
            "represented_problem_informal_status": dict(sorted(represented_problem_status_counts.items())),
            "represented_source_problem_numbers": len(rows_by_problem),
            "status_conflict_parent_open_source_resolved_rows": len(status_conflicts),
        },
        "research_solved_theorem_inventory": {
            "filter_rule": (
                "parent current_claim_kind == theorem AND raw_status == research solved; eligible resolved lane also "
                "requires pinned upstream informal_status.state in {proved, disproved, solved}"
            ),
            "max2_per_file_available_count": len(resolved_theorem_selected),
            "resolved_filtered_distinct_formal_files": len(resolved_by_file),
            "resolved_filtered_distinct_problem_numbers": len(
                {row["source_problem"]["problem_number"] for row in resolved_theorem_rows}
            ),
            "resolved_filtered_by_derived_status_including_lean": dict(
                sorted(
                    collections.Counter(
                        row["source_problem"]["derived_status"]["state"] for row in resolved_theorem_rows
                    ).items()
                )
            ),
            "resolved_filtered_by_informal_status": dict(
                sorted(
                    collections.Counter(
                        row["source_problem"]["informal_status"]["state"] for row in resolved_theorem_rows
                    ).items()
                )
            ),
            "resolved_filtered_rows": len(resolved_theorem_rows),
            "research_solved_rows_before_upstream_filter": len(research_solved_theorem_rows),
            "upstream_open_drift_distinct_formal_files": len(
                {row["parent"]["locator"]["member_path"] for row in research_solved_upstream_open_drift}
            ),
            "upstream_open_drift_distinct_problem_numbers": len(
                {row["source_problem"]["problem_number"] for row in research_solved_upstream_open_drift}
            ),
            "upstream_open_drift_frontier_credit_allowed": False,
            "upstream_open_drift_rows": len(research_solved_upstream_open_drift),
        },
        "release_mutation": False,
        "schema_version": SCHEMA_VERSION,
        "source_counts": {
            "derived_status": dict(sorted(source_derived_status_counts.items())),
            "formalized_statement_yes": sum(
                (row.get("formalized_statement") or {}).get("state") == "yes" for row in source_rows
            ),
            "informal_status": dict(sorted(source_status_counts.items())),
            "problems": len(source_rows),
            "current_exact_open": sum(row["is_current_exact_open"] for row in source_rows),
            "current_unresolved_broad": sum(row["is_current_unresolved_broad"] for row in source_rows),
        },
        "status_semantics": {
            "current_exact_open_uses": "informal_status.state == open",
            "derived_status_is_preserved": True,
            "problem_level_status_does_not_override_declaration_level_kind_or_material_status": True,
        },
    }

    write_jsonl(args.output_dir / "source-problems.jsonl", source_rows)
    write_jsonl(args.output_dir / "parent-erdos-join.jsonl", join_rows)
    write_jsonl(args.output_dir / "problem-groups.jsonl", groups)
    write_jsonl(args.output_dir / "current-open-identities.jsonl", current_open)
    write_jsonl(args.output_dir / "existing-strict-credits.jsonl", existing_credits)
    write_jsonl(args.output_dir / "polarity-review-backlog.jsonl", polarity_backlog)
    write_jsonl(args.output_dir / "new-credit-review-candidates.jsonl", new_credit_candidates)
    write_jsonl(args.output_dir / "status-conflicts.jsonl", status_conflicts)
    write_jsonl(args.output_dir / "resolved-theorem-rows.jsonl", resolved_theorem_rows)
    write_jsonl(args.output_dir / "resolved-theorem-file-capacity.jsonl", resolved_file_capacity)
    write_jsonl(args.output_dir / "resolved-theorem-max2-selected.jsonl", resolved_theorem_selected)
    write_jsonl(
        args.output_dir / "research-solved-upstream-open-drift.jsonl",
        research_solved_upstream_open_drift,
    )
    write_json(args.output_dir / "summary.json", summary)

    artifact_inventory = []
    for name in DATA_ARTIFACTS:
        path = args.output_dir / name
        data = path.read_bytes()
        artifact_inventory.append(
            {
                "file_sha256": sha256_bytes(data),
                "line_count": len(data.splitlines()),
                "path": repo_relative(path, repo_root),
                "size_bytes": len(data),
            }
        )
    script_paths = [
        repo_root / "Docs/catalog/v5/tools/build_erdos_parent_join_v5_5.py",
        repo_root / "Docs/catalog/v5/tools/check_erdos_parent_join_v5_5.py",
        repo_root / "Docs/catalog/v5/tools/test_erdos_parent_join_v5_5.py",
    ]
    for path in script_paths:
        data = path.read_bytes()
        artifact_inventory.append(
            {
                "file_sha256": sha256_bytes(data),
                "line_count": len(data.splitlines()),
                "path": repo_relative(path, repo_root),
                "size_bytes": len(data),
            }
        )

    receipt_without_authority = {
        "artifact_inventory": artifact_inventory,
        "build_command": "python3 Docs/catalog/v5/tools/build_erdos_parent_join_v5_5.py",
        "credit_boundary": summary["credit_accounting"],
        "output_root": repo_relative(args.output_dir, repo_root),
        "parent_release": {
            "catalog_authority_sha256": PARENT_CATALOG_AUTHORITY,
            "catalog_file_sha256": PARENT_CATALOG_SHA256,
            "ledger_authority_sha256": PARENT_LEDGER_AUTHORITY,
            "ledger_file_sha256": PARENT_LEDGER_SHA256,
            "manifest_authority_sha256": PARENT_MANIFEST_AUTHORITY,
            "manifest_file_sha256": PARENT_MANIFEST_SHA256,
            "release": "5.4",
        },
        "release_mutation": False,
        "schema_version": SCHEMA_VERSION,
        "source_snapshot": {
            "archive_path": repo_relative(archive_path, repo_root),
            "archive_sha256": ERDOS_ARCHIVE_SHA256,
            "commit": ERDOS_COMMIT,
            "commit_timestamp": snapshot["source"]["commit_timestamp"],
            "license_file_sha256": ERDOS_LICENSE_SHA256,
            "license_spdx": "Apache-2.0",
            "problems_file_sha256": ERDOS_PROBLEMS_SHA256,
            "repository": SOURCE_REPOSITORY,
            "status_snapshot_authority_sha256": ERDOS_SNAPSHOT_AUTHORITY,
            "status_snapshot_file_sha256": ERDOS_SNAPSHOT_SHA256,
            "status_snapshot_path": repo_relative(snapshot_path, repo_root),
            "tree": ERDOS_TREE,
        },
        "summary_sha256": sha256_bytes((args.output_dir / "summary.json").read_bytes()),
        "validation_command": "python3 Docs/catalog/v5/tools/check_erdos_parent_join_v5_5.py",
        "mutation_test_command": "python3 Docs/catalog/v5/tools/test_erdos_parent_join_v5_5.py",
    }
    receipt = dict(receipt_without_authority)
    receipt["authority_sha256"] = sha256_bytes(canonical_bytes(receipt_without_authority))
    write_json(args.output_dir / "receipt.json", receipt)
    print(
        canonical_bytes(
            {"receipt": repo_relative(args.output_dir / "receipt.json", repo_root), "summary": summary}
        ).decode()
    )


if __name__ == "__main__":
    main()
