#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0137-ANCHOR_AUDIT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0137"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM_ID = "S56-M-0137-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0137"
PHASE = "anchor_audit"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "8d67fa7c42700d4411760f8d5eb8dc634a6ded3b3cde1e03eb8cb0f1d5ff2727"
EVIDENCE_SHA256 = "60d4c7e4290c9c8944b4cdce323db885a6cc7307c8ffa7673fcf60a80d60ecc3"
ACCESS_SHA256 = "53014368def1ba48f7b61fc924fe2c550a934e2fe30af583af745db541f3d599"
LEDGER_SHA256 = "636a36efa2afad9535be9c3c90a6eb28a24316577e1033f36f8c3737edb7e1b0"
AUDIT_SHA256 = "904012d1dc71217a142cf1271965d8eba38137782209502ce4e10fe895ec8c5d"
STATEMENT_SHA256 = "654d6cf907e8ac4fcca037a06cfbf5e0be94828217a941feced1f93243eb809e"
LEGACY_SHA256 = "0a16ee0be2a18b0bfb5baff0b686620895995404bb2a83c6da0e3cfdb9c7d184"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"

ORDERED_LANES = [
    "repo_local",
    "pinned_mathlib",
    "official_primary_projects",
    "other_immutable_public_projects",
    "statement_only_collections",
    "historical_or_other_provers",
    "primary_human_sources",
]
MACHINE_STATES = {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md":
        "2a5bc7d397e03969aac1a9f8f21b437152b8ef63ef453055acf67857ced628b5",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "fe70128eba4e3878fbc58625bc7f602be4020e5e2edd6b94b134436568086d65",
    "skills/execute-stage1-rev56/SKILL.md":
        "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/Blueprint_Guidelines.md":
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
REPOSITORY_EVIDENCE = {
    "Stage1_Instances/THM-M-0137/Statement.lean":
        (STATEMENT_SHA256, "389bd2090e5ee4bad617585ed794ff48314897a2"),
    "Stage1_Instances/THM-M-0137/statement.json":
        ("aa6dde3c6d9195e4bb451747bbf22ca71b5589d4840ea7e7fd69e0e81a621755",
         "ea86bd3010e0b923d31827ef67a0badbd3b15590"),
    "Stage1_Instances/THM-M-0137/statement-receipt.json":
        ("553b52b30179779b74c440fed2445a2866c78ba831a8a3d04ee080ee8437cf64",
         "ef02fedbc40fedf91e29e531a1dc3ab54a9eca1e"),
    "Stage1_Instances/THM-M-0137/source-statement-crosswalk.md":
        ("0b28e21a021c57bdea92fa90049cdcf190bfdfbf6fa140c8d402df5f2f3c034e",
         "54b4d3fb50725682e76dc872f8237203d4c81159"),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_053.lean":
        (LEGACY_SHA256, "f577a38de4f07b7d9bbc50d8e15ff71bf833137a"),
}
MATHLIB_EVIDENCE = {
    "Mathlib/Algebra/Lie/Loop.lean":
        ("162ef308149a6f2548d93c8089a7862cfdb8be7e3f78e030a9921fefd9b8ba98",
         "c449a7b2c04e4e11233399c0ab77de8333c9dfd9"),
    "Mathlib/Algebra/Lie/Character.lean":
        ("8ff9ff21e8ae5968d639956ddc2ddf314222ab83382b7f755299dc706afca845",
         "c7876c8c359af7793c0bbb9a108e7645d39a6bcb"),
    "Mathlib/Algebra/Lie/Weights/Basic.lean":
        ("6bcd8c0161bdaea99c48ec5904cd66d266c9e81ee6a2d8cd9010253874b5aaf4",
         "f0179d1949eca9e01abdc74e8ff340fd6f360fd2"),
    "Mathlib/LinearAlgebra/RootSystem/WeylGroup.lean":
        ("60bf2ce6c6ff8eca569881d95e203cbf1b7ef66bb97d1123412e99b568f9a53b",
         "498d75ac45eb281353dfd8ac0271a9d7e293d4ec"),
    "Mathlib/Algebra/MonoidAlgebra/Basic.lean":
        ("cda5df6bc20f161fcc5e7bad9efdee908b284d260e92c471ad53362eec559420",
         "c5c8989adcd602a7a592cd4c9a0dadefb6241262"),
    "Mathlib/RingTheory/HahnSeries/Basic.lean":
        ("e90074cd841e051ad4d99053253d82bc80a672ecf9c2f6e5632483a5e6d00f45",
         "ab3d2de2bfdf0db22ae4c61cdcbda5cf648805eb"),
    "Mathlib/LinearAlgebra/RootSystem/RootPositive.lean":
        ("fff50ab953e9d7f1e5a98df2c6e5becb4951c3ca45a0268772474d7b37cd43e7",
         "ce49a7138e2d4258d41c255b887dbce62763c0a8"),
    "LICENSE":
        ("b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
         "8dada3edaf50dbc082c9a125058f25def75e625a"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            require(key not in value, f"duplicate JSON key {key!r} in {path}")
            value[key] = child
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"{path} is not a JSON object")
    return value


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, capture_output=True, text=True, timeout=30
    )
    require(result.returncode == 0, f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalize_machine_state(value: Any) -> str:
    require(isinstance(value, str), "candidate classification is not a string")
    for state in sorted(MACHINE_STATES, key=len, reverse=True):
        if value == state or value.startswith(state + "_") or value.startswith(state + " "):
            return state
    raise AssertionError(f"unsupported machine classification {value!r}")


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for part in raw.removeprefix("/").split("/"):
        require(isinstance(value, dict) and part in value, f"receipt field {raw} is missing")
        value = value[part]
    return value


def validate_authority() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(git("rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "repository base tree drift")
    for relative, expected in AUTHORITY_HASHES.items():
        require(digest(ROOT / relative) == expected, f"authority input drift: {relative}")
    for relative, (expected_digest, expected_blob) in REPOSITORY_EVIDENCE.items():
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), f"repository evidence missing: {relative}")
        require(digest(path) == expected_digest, f"repository evidence SHA drift: {relative}")
        require(git("rev-parse", f"HEAD:{relative}") == expected_blob,
                f"repository evidence Git blob drift: {relative}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 53, "manifest execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "manifest assurance baseline drift")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "manifest lifecycle boundary drift")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    require(item == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 53,
        "phase": PHASE,
        "layer": 2,
        "state": "[ ]",
        "depends_on": ["S56-M-0137-STATEMENT"],
        "owned_paths": ["Stage1_Instances/THM-M-0137"],
        "deliverable": "Audit mathlib and external Lean 4 candidates at immutable revisions.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "execution manifest item drift")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 287 and node["topological_layer"] == 0,
            "v2 claim order drift")
    require(node["phase_states"][PHASE] == "[ ]" and node["phase_attempts"][PHASE] == 0,
            "authoritative anchor state drift")
    require(node["phase_states"]["statement"] == "[_]", "statement predecessor state drift")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        require(node[field] == [], f"dependency field {field} is no longer empty")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == PHASE)
    require(phase["layer"] == 2 and phase["intent"] == "audit", "phase contract drift")
    require([gate["gate_id"] for gate in phase["semantic_gates"]] == [
        "A01-ARTIFACTS", "A02-DISCOVERY", "A03-CLASSIFICATION"
    ], "anchor semantic gates drift")
    validator_paths = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    require(validator_paths == ["Stage1_Instances/THM-M-0137/check_anchor_audit.py"],
            "validator candidate selection is not exactly one path")
    return node, phase, item


def validate_dependency_ledger(node: dict[str, Any]) -> None:
    path = HERE / "dependency-reuse-ledger.json"
    require(digest(path) == LEDGER_SHA256, "dependency ledger drift")
    ledger = load(path)
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "dependency ledger schema drift")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "dependency ledger owner drift")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "ledger graph drift")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context drift")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger base drift")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 287,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "ledger claim order drift")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        require(ledger[field] == [], f"empty dependency closure drift: {field}")
    closure = ledger["closure_audit"]
    require(closure["parent_inspection_order"] == [], "parent inspection order drift")
    require(closure["status"] == "empty_complete_closure_audited",
            "empty closure was not marked completely audited")
    require(node["direct_hard_parents"] == closure["parent_inspection_order"],
            "ledger inspection order disagrees with the exact closure")


def validate_mathlib() -> None:
    require(MATHLIB.is_dir(), "pinned mathlib source artifact is missing")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "", "mathlib tree is dirty")
    for relative, (expected_digest, expected_blob) in MATHLIB_EVIDENCE.items():
        path = MATHLIB / relative
        require(path.is_file() and not path.is_symlink(), f"mathlib evidence missing: {relative}")
        require(digest(path) == expected_digest, f"mathlib source SHA drift: {relative}")
        require(git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected_blob,
                f"mathlib Git blob drift: {relative}")
    loop = (MATHLIB / "Mathlib/Algebra/Lie/Loop.lean").read_text(encoding="utf-8")
    for marker in (
        "* Construction of central extensions from invariant forms.",
        "* Positive energy representations induced from a fixed central character",
    ):
        require(marker in loop, "mathlib affine infrastructure boundary drift")


def validate_protocol_and_evidence() -> tuple[dict[str, Any], dict[str, Any]]:
    protocol_path = HERE / "anchor-discovery-protocol.json"
    evidence_path = HERE / "anchor-discovery-evidence.json"
    access_path = HERE / "anchor-search-access.json"
    require(digest(protocol_path) == PROTOCOL_SHA256, "discovery protocol drift")
    require(digest(evidence_path) == EVIDENCE_SHA256, "discovery evidence drift")
    require(digest(access_path) == ACCESS_SHA256, "search-access observation drift")
    protocol = load(protocol_path)
    evidence = load(evidence_path)
    access = load(access_path)

    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "discovery protocol identity drift")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order drift")
    canonical = protocol["canonical_target"]
    require(canonical["declaration"] is None
            and canonical["elaborated_expression_sha256"] is None,
            "protocol invents a canonical target")
    require(canonical["status"] == "blocked_on_primary_source_disambiguation",
            "canonical-target ambiguity boundary drift")
    require(len(canonical["candidate_interpretations"]) == 2,
            "source ambiguity no longer names both candidate families")

    require(evidence["schema_version"] == "stage1-anchor-discovery-evidence/1.0",
            "wrong discovery evidence schema")
    require(evidence["item_id"] == ITEM_ID and evidence["theorem_id"] == THEOREM_ID,
            "discovery evidence identity drift")
    require(evidence["inventory_version"] == protocol["inventory_version"],
            "inventory version disagreement")
    require(evidence["network_used_for_replay"] is False, "semantic replay used network")
    lanes = evidence["ordered_lane_results"]
    require([row["lane"] for row in lanes] == ORDERED_LANES, "evidence lane order drift")
    for row in lanes:
        for field in ("query_or_source", "revision", "result", "access_boundary", "reopen_condition"):
            require(isinstance(row.get(field), str) and bool(row[field].strip()),
                    f"incomplete lane field {field}: {row.get('lane')}")
        require(isinstance(row.get("evidence"), list) and row["evidence"],
                f"unbound lane evidence: {row['lane']}")
        for binding in row["evidence"]:
            relative = binding["path"]
            if relative.startswith("Formalizations/Lean/.lake/packages/mathlib/"):
                package_relative = relative.removeprefix(
                    "Formalizations/Lean/.lake/packages/mathlib/"
                )
                path = MATHLIB / package_relative
                actual_blob = git("rev-parse", f"HEAD:{package_relative}", cwd=MATHLIB)
            elif relative == "Stage1_Instances/THM-M-0137/anchor-search-access.json":
                path = ROOT / relative
                actual_blob = None
            else:
                path = ROOT / relative
                actual_blob = git("rev-parse", f"HEAD:{relative}")
            require(path.is_file() and not path.is_symlink(), f"lane evidence missing: {relative}")
            require(digest(path) == binding["sha256"], f"lane evidence SHA drift: {relative}")
            if actual_blob is None:
                require(binding.get("git_blob") is None, "untracked access evidence claims a blob")
            else:
                require(binding.get("git_blob") == actual_blob,
                        f"lane evidence Git blob drift: {relative}")

    require(access["schema_version"] == "stage1-search-access-observation/1.0",
            "wrong access-observation schema")
    require(access["item_id"] == ITEM_ID and access["theorem_id"] == THEOREM_ID,
            "access-observation identity drift")
    require(access["exit_code"] == 6 and access["stdout_size"] == 0,
            "access failure observation drift")
    require(access["result_classification"] == "access_failed_no_search_result",
            "network failure was not classified as access failure")
    require(access["absence_claimed"] is False, "access failure was upgraded to absence")
    return protocol, evidence


def validate_audit(protocol: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    audit_path = HERE / "anchor-audit.json"
    require(digest(audit_path) == AUDIT_SHA256, "anchor audit drift")
    audit = load(audit_path)
    require(audit["schema_version"] == "stage1-anchor-audit/1.0", "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity drift")
    require(audit["phase"] == PHASE and audit["intent"] == "audit",
            "audit phase or intent drift")
    require(audit["execution_rank"] == 53 and audit["v2_execution_rank"] == 287
            and audit["phase_layer"] == 2, "audit claim order drift")
    require(audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE,
            "audit base drift")
    require(audit["inventory_version"] == protocol["inventory_version"]
            == evidence["inventory_version"], "audit inventory version drift")
    require(audit["canonical_target"] is None
            and audit["canonical_target_expression_sha256"] is None,
            "audit invents a canonical proposition")
    require(audit["canonical_target_status"] == "blocked_on_primary_source_disambiguation",
            "audit ambiguity boundary drift")
    require(audit["canonical_statement_file_sha256"] == STATEMENT_SHA256,
            "audit statement boundary binding drift")
    require(audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256,
            "audit protocol binding drift")
    require(audit["discovery_evidence"]["sha256"] == EVIDENCE_SHA256,
            "audit evidence binding drift")
    require(audit["search_order_completed"] == ORDERED_LANES,
            "audit search order drift")

    candidates = audit["candidates"]
    require(len(candidates) == 6, "candidate inventory size drift")
    require(len({row["candidate_id"] for row in candidates}) == 6,
            "duplicate candidate identity")
    expected_states = {
        "M0137-C01-REPO-LOCAL-BOUNDARY-PROBE": "M4",
        "M0137-C02-LEGACY-STATEMENT-SHAPE": "M5",
        "M0137-C03-MATHLIB-AFFINE-SUBSTRATE": "M3",
        "M0137-C04-MATHLIB-FORMAL-SERIES-SUBSTRATE": "M3",
        "M0137-C05-PUBLIC-PROJECT-DISCOVERY": "M4",
        "M0137-C06-PRIMARY-SOURCE-ROOT-BOUNDARY": "M4",
    }
    require({row["candidate_id"]: normalize_machine_state(row["classification"])
             for row in candidates} == expected_states, "candidate classification drift")
    required_candidate_fields = (
        "type", "normalized_match", "checked_wrapper_or_conclusion", "toolchain",
        "dependency_feasibility", "proof_body_location",
        "placeholder_bodyless_unsafe_oracle_status", "blocker", "reopen_condition",
    )
    for candidate in candidates:
        for field in required_candidate_fields:
            require(isinstance(candidate.get(field), str) and bool(candidate[field].strip()),
                    f"candidate {candidate['candidate_id']} lacks {field}")
        require(candidate["completion_credit"] is False,
                f"candidate {candidate['candidate_id']} improperly receives proof credit")
    legacy = next(row for row in candidates if row["candidate_id"].endswith("STATEMENT-SHAPE"))
    require(legacy["file_sha256"] == LEGACY_SHA256, "legacy source binding drift")
    require("CharacterEqualsKacPetersonFormula" in legacy["type"],
            "legacy circular-input diagnosis drift")
    local_probe = next(
        row for row in candidates if row["candidate_id"].endswith("BOUNDARY-PROBE")
    )
    require(local_probe["module"] == "Stage1_Instances/THM-M-0137/AnchorAudit.lean",
            "target-owned anchor probe path drift")
    require(local_probe["file_sha256"] ==
            "6980b47270521ab1f37e1ec201ce73c1ecaf3c8b3e45c82c46ee3739db1506af",
            "target-owned anchor probe SHA drift")
    require(local_probe["file_git_blob"] ==
            "ab9f35e7e9acaddf89c2d40303d444733812b11f",
            "target-owned anchor probe Git blob drift")

    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 6,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] == coverage["prescribed_lane_count"] == 7,
            "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "frozen inventory classification is incomplete")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["canonical_target_frozen"] is False
            and coverage["exact_terminal_candidate_found"] is False,
            "audit contradicts its source/candidate boundary")
    require(coverage["root_proof_credit"] is False, "audit grants root proof credit")
    require(audit["root_machine_classification"] == "M4"
            and audit["root_evidence_grade"] == "E5", "root debt boundary drift")
    require(audit["accepted_receipt_ids"] == [] and audit["reused_declaration_ids"] == [],
            "audit invents accepted evidence or reuse")
    require(audit["provider_acceptance_inherited"] is False,
            "audit transfers provider acceptance")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor phase overclaims terminal completion")
    return audit


def validate_sources() -> None:
    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    probe_source = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    legacy_source = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_053.lean"
    ).read_text(encoding="utf-8")
    require("deliberately declares no canonical target" in statement_source,
            "statement source ambiguity marker drift")
    require("intentionally declares no canonical" in probe_source,
            "anchor probe ambiguity marker drift")
    checks = re.findall(r"^#check ([^\s]+)$", probe_source, flags=re.MULTILINE)
    require(checks == [
        "AddMonoidAlgebra", "HahnSeries", "LieAlgebra.loopAlgebra",
        "LieAlgebra.LieCharacter", "LieModule.weightSpace", "RootPairing.weylGroup",
    ], "anchor probe interface set drift")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b", flags=re.MULTILINE
    )
    source_without_comments = re.sub(r"/-.*?-/|--.*", "", probe_source, flags=re.DOTALL)
    require(prohibited.search(source_without_comments) is None,
            "anchor probe contains a prohibited construct")
    for marker in (
        "structure KacPetersonCharacterFormulaInput",
        "CharacterEqualsKacPetersonFormula : Prop",
        "def StatementShape : Prop :=",
        "X.CharacterFormulaWellFormed →\n    X.CharacterEqualsKacPetersonFormula",
        "theorem statementShape_iff",
    ):
        require(marker in legacy_source, "legacy circular interface marker drift")


def validate_receipt(phase_contract: dict[str, Any]) -> dict[str, Any]:
    receipt = load(HERE / "anchor-audit-receipt.json")
    for raw in phase_contract["phase_receipt_required_fields"]:
        pointer(receipt, raw)
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "wrong phase receipt schema")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "phase receipt identity drift")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "phase receipt phase or intent drift")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "phase receipt base drift")
    require(receipt["claim_order"] == {
        "v2_execution_rank": 287,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "phase receipt claim order drift")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt claims master acceptance")
    require(receipt["verdict"] == "no_state_change", "unexpected worker verdict")
    require(receipt["selftest_status"] == "passed", "receipt self-test is not passed")
    require(receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"], "receipt self-test result is incomplete")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding drift")
    result = receipt["candidate_inventory_result"]
    require(result["classified"] == result["inventory_size"] == 6,
            "receipt candidate inventory coverage drift")
    require(result["classification_complete"] is True
            and result["ordered_lanes_complete"] is True,
            "receipt phase predicate is incomplete")
    require(result["root_proof_credit"] is False,
            "receipt improperly grants root proof credit")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["first_failed_gate"]
            and receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary/freshness data is incomplete")
    discovery = receipt["inputs"]["discovery_evidence"]
    required_discovery = {
        "Stage1_Instances/THM-M-0137/anchor-discovery-protocol.json": PROTOCOL_SHA256,
        "Stage1_Instances/THM-M-0137/anchor-discovery-evidence.json": EVIDENCE_SHA256,
        "Stage1_Instances/THM-M-0137/anchor-search-access.json": ACCESS_SHA256,
        "Stage1_Instances/THM-M-0137/dependency-reuse-ledger.json": LEDGER_SHA256,
    }
    require({row["path"]: row["sha256"] for row in discovery} == required_discovery,
            "receipt discovery evidence binding drift")
    require(receipt["inputs"]["parent_inspection_order"] == []
            and receipt["inputs"]["inspected_parent_ids"] == [],
            "receipt parent inspection closure drift")
    require(receipt["inputs"]["provider_acceptance_inherited"] is False,
            "receipt transfers provider acceptance")
    require(receipt["inputs"]["anchor_probe_source"] == [{
        "path": "Stage1_Instances/THM-M-0137/AnchorAudit.lean",
        "sha256": "6980b47270521ab1f37e1ec201ce73c1ecaf3c8b3e45c82c46ee3739db1506af",
        "git_blob": "ab9f35e7e9acaddf89c2d40303d444733812b11f",
    }], "receipt anchor-probe input binding drift")
    bindings = receipt["artifact_bindings"]
    require(bindings["anchor_inventory"] == {
        "role": "anchor_inventory",
        "path": "Stage1_Instances/THM-M-0137/anchor-audit.json",
        "sha256": AUDIT_SHA256,
        "git_blob": "92d6c978b1ca2276e212329612706e6846a942ce",
        "tracking_state": "worker_output_to_be_HEAD_bound_by_integration",
    }, "receipt anchor-inventory role binding drift")
    require(bindings["discovery_evidence"] == {
        "role": "discovery_evidence",
        "path": "Stage1_Instances/THM-M-0137/anchor-discovery-evidence.json",
        "sha256": EVIDENCE_SHA256,
        "git_blob": "7360b378931fb6ae4b03239fabf524d682be83ae",
        "tracking_state": "worker_output_to_be_HEAD_bound_by_integration",
    }, "receipt discovery-evidence role binding drift")
    require(bindings["anchor_probe_source"] == {
        "role": "anchor_probe_source",
        "path": "Stage1_Instances/THM-M-0137/AnchorAudit.lean",
        "sha256": "6980b47270521ab1f37e1ec201ce73c1ecaf3c8b3e45c82c46ee3739db1506af",
        "git_blob": "ab9f35e7e9acaddf89c2d40303d444733812b11f",
        "tracking_state": "worker_output_to_be_HEAD_bound_by_integration",
    }, "receipt anchor-probe role binding drift")
    require(receipt["artifact_bindings"]["phase_receipt"]["sha256"] is None
            and receipt["artifact_bindings"]["phase_receipt"]["git_blob"] is None,
            "receipt embeds a cyclic self-binding")
    validator = receipt["validator_binding"]
    validator_path = HERE / "check_anchor_audit.py"
    require(validator["path"] == "Stage1_Instances/THM-M-0137/check_anchor_audit.py",
            "receipt validator path drift")
    require(validator["sha256"] == digest(validator_path), "receipt validator SHA drift")
    require(validator["git_blob"] == git("hash-object", "--no-filters", str(validator_path)),
            "receipt validator Git-blob binding drift")
    require(validator["declared_argv"] == [
        "/usr/bin/python3", "-I", "-B",
        "Stage1_Instances/THM-M-0137/check_anchor_audit.py",
    ], "receipt validator argv drift")
    return receipt


def validate_worker_packet(receipt: dict[str, Any]) -> None:
    packet_path = ROOT / ".stage1-worker-selftest.json"
    if not packet_path.exists():
        return
    require(packet_path.is_file() and not packet_path.is_symlink(),
            "worker self-test packet is missing or unsafe")
    packet = load(packet_path)
    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }, "worker packet field set drift")
    require(packet["item_id"] == ITEM_ID and packet["state"] == "[_]",
            "worker packet identity or state drift")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drift")
    require(packet["commands"] == receipt["selftest_result"]["commands"],
            "worker packet commands differ from the phase receipt")
    require(packet["output_summary"] == receipt["selftest_result"]["output_summary"],
            "worker packet output summary differs from the phase receipt")
    require(packet["known_failures"] == receipt["known_failures"],
            "worker packet known failures differ from the phase receipt")
    expected = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0137/AnchorAudit.lean",
        "Stage1_Instances/THM-M-0137/anchor-audit-receipt.json",
        "Stage1_Instances/THM-M-0137/anchor-audit-validation.md",
        "Stage1_Instances/THM-M-0137/anchor-audit.json",
        "Stage1_Instances/THM-M-0137/anchor-discovery-evidence.json",
        "Stage1_Instances/THM-M-0137/anchor-discovery-protocol.json",
        "Stage1_Instances/THM-M-0137/anchor-search-access.json",
        "Stage1_Instances/THM-M-0137/check_anchor_audit.py",
        "Stage1_Instances/THM-M-0137/dependency-reuse-ledger.json",
    }
    require(set(packet["changed_paths"]) == expected, "worker packet path inventory drift")
    tracked = git("diff", "--name-only", "HEAD", "--", "Stage1_Instances/THM-M-0137")
    untracked = git(
        "ls-files", "--others", "--exclude-standard", "--",
        "Stage1_Instances/THM-M-0137",
    )
    actual = set(filter(None, (tracked + "\n" + untracked).splitlines()))
    require(actual == expected - {".stage1-worker-selftest.json"},
            "worker packet does not exactly cover the owned Git delta")


def validate_worktree_boundary() -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    require(result.returncode == 0, "could not inspect worker worktree status")
    expected = {
        ".stage1-worker-selftest.json",
        "Formalizations/Lean/.lake",
        "Stage1_Instances/THM-M-0137/AnchorAudit.lean",
        "Stage1_Instances/THM-M-0137/anchor-audit-receipt.json",
        "Stage1_Instances/THM-M-0137/anchor-audit-validation.md",
        "Stage1_Instances/THM-M-0137/anchor-audit.json",
        "Stage1_Instances/THM-M-0137/anchor-discovery-evidence.json",
        "Stage1_Instances/THM-M-0137/anchor-discovery-protocol.json",
        "Stage1_Instances/THM-M-0137/anchor-search-access.json",
        "Stage1_Instances/THM-M-0137/check_anchor_audit.py",
        "Stage1_Instances/THM-M-0137/dependency-reuse-ledger.json",
    }
    changed = {line[3:] for line in result.stdout.splitlines() if len(line) > 3}
    require(changed == expected, "worker worktree contains an undeclared or missing delta")
    lake = LEAN_ROOT / ".lake"
    require(lake.is_symlink(), "automation-provided .lake artifact is not a symlink")
    require((lake / "packages" / "mathlib").resolve() == MATHLIB.resolve(),
            "automation-provided .lake artifact does not resolve to the audited mathlib tree")


def validate() -> None:
    node, phase_contract, _item = validate_authority()
    validate_dependency_ledger(node)
    validate_mathlib()
    protocol, evidence = validate_protocol_and_evidence()
    validate_audit(protocol, evidence)
    validate_sources()
    receipt = validate_receipt(phase_contract)
    validate_worker_packet(receipt)
    validate_worktree_boundary()


def semantic_result(*, passed: bool, message: str) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": PHASE,
        "status": "passed" if passed else "failed",
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": None if passed else "ANCHOR-AUDIT-SEMANTIC-CHECK",
        "open_obligations": 0 if passed else 1,
        "stale_inputs": [],
        "blocked": False,
        "message": message,
    }


def main() -> int:
    try:
        validate()
    except Exception as exc:
        result = semantic_result(passed=False, message=f"anchor-audit validation failed: {exc}")
    else:
        result = semantic_result(
            passed=True,
            message=(
                "A01-A03 proven for six content-bound classifications and all seven ordered "
                "lanes; source ambiguity, no root proof credit, and the empty reuse closure are "
                "preserved."
            ),
        )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["phase_accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
