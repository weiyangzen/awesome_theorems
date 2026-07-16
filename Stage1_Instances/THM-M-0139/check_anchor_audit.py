#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0139-ANCHOR_AUDIT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM_ID = "S56-M-0139-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0139"
PHASE = "anchor_audit"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "0b6e07779b4c252c9d254520bcdd89f3d3c41f94b8a76a1ab4b040333a3df455"
EVIDENCE_SHA256 = "124fa2d2782cb43b77c04b8c6901e788cbd5905356fa8e7ed7d0a41c9f7fb6d4"
AUDIT_SHA256 = "8a18e248d01c7ad558b69f7d680e45f0d0df1ec0aab657a3a35a80b2df4eaf0b"
LEDGER_SHA256 = "00450fcc6455a80e4ba0517833133a82e7ba396bf13ad48466a4a8671e84af0f"
PROBE_SHA256 = "90cb23e91b9c5dc7551a3e48c442c12e901581f392d6fc27aa3c1d1c87d86b49"
VALIDATION_SHA256 = "6dac98466f33be0e73eba3099c246d7fe6bb340df812a00ce3bf7f00418ed4c7"
STATEMENT_SHA256 = "59e3ef74de584eba3fc6b623f3a90a7bac2f8529bc4ca707a505c80edbec64b3"
STATEMENT_RECORD_SHA256 = "2e53b0d9fa3decf09a86122cf7a9db1b357f56cc8a60b06806bd3699fde4f50d"
STATEMENT_RECEIPT_SHA256 = "24b7b5dc3ad13a37933cf883e04571dd427b1e4b02ce946d1e71c5b72fc559b7"
LEGACY_SHA256 = "e1a5e161d9fdd2c5dbbb0c744696eeb3d63fa9e239478ab97aaee88a73f283cb"
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
MATHLIB_QUERIES = (
    "Kazhdan",
    "Lusztig",
    "KazhdanLusztig",
    "BGG category",
    "Verma module",
    "compositionMultiplicity",
    "VermaMultiplicity",
    "HeckeAlgebra",
)
PROHIBITED_PROBE = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} is not a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, timeout=60).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalize_classification(value: str) -> str:
    for state in sorted(MACHINE_STATES, key=len, reverse=True):
        if value == state or value.startswith(state + "_") or value.startswith(state + " "):
            return state
    raise AssertionError(f"unsupported classification {value!r}")


def resolve_git_blob(relative: str) -> str:
    prefix = "Formalizations/Lean/.lake/packages/mathlib/"
    if relative.startswith(prefix):
        return output("git", "rev-parse", f"HEAD:{relative.removeprefix(prefix)}", cwd=MATHLIB)
    tracked = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{relative}"],
        cwd=ROOT,
        capture_output=True,
        timeout=20,
        check=False,
    )
    if tracked.returncode == 0:
        return output("git", "rev-parse", f"HEAD:{relative}")
    return git_blob(ROOT / relative)


def validate_authority(contract: dict, theorem_dag: dict) -> None:
    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256,
            "phase contract drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256,
            "theorem DAG drift")

    targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 55, "target execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "target assurance baseline drift")

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 289 and node["topological_layer"] == 0,
            "v2 claim order drift")
    require(node["phase_states"][PHASE] == "[ ]", "authoritative phase is not unclaimed")
    require(node["phase_attempts"][PHASE] == 0, "authoritative attempt count drift")
    require(node["phase_states"]["statement"] == "[_]", "statement predecessor state drift")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        require(node[field] == [], f"declared empty theorem context drift at {field}")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")

    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    require(phase_contract["layer"] == 2, "anchor phase layer drift")
    require(phase_contract["classified_negative_findings_may_satisfy_deliverable"] is True,
            "negative classification contract drift")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase_contract["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    require(validators == ["Stage1_Instances/THM-M-0139/check_anchor_audit.py"],
            "validator candidate selection is not exactly one declared path")


def validate_ledger(ledger: dict) -> None:
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "wrong dependency ledger schema")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "ledger owner drift")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "ledger graph mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger revision mismatch")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 289,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "ledger claim order mismatch")
    require("independence" not in ledger["closure_audit"]["boundary"].lower()
            or "does not assert" in ledger["closure_audit"]["boundary"].lower(),
            "empty closure is misreported as independence")
    for field in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        require(ledger[field] == [], f"declared empty dependency closure drift at {field}")
    closure = ledger["closure_audit"]
    require(closure["parent_inspection_order"] == [], "parent inspection order drift")
    require(closure["item_id"] == ITEM_ID and closure["phase"] == PHASE,
            "ledger phase identity drift")


def validate_artifact(path: str, expected_sha: str) -> None:
    target = ROOT / path
    require(target.is_file() and not target.is_symlink(), f"artifact missing or symlinked: {path}")
    require(sha256(target) == expected_sha, f"artifact SHA drift: {path}")


def validate_output_git_blob(path: str, expected_blob: str) -> None:
    target = ROOT / path
    require(git_blob(target) == expected_blob, f"worker-output Git blob drift: {path}")


def validate_protocol_and_evidence(protocol: dict, evidence: dict) -> None:
    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity mismatch")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order mismatch")
    require(protocol["canonical_target_boundary"]["declaration"] is None,
            "protocol invents a canonical target")
    protocol_inventory = protocol["inventory_version"]

    require(evidence["schema_version"] == "stage1-anchor-discovery-evidence/1.0",
            "wrong discovery evidence schema")
    require(evidence["item_id"] == ITEM_ID and evidence["theorem_id"] == THEOREM_ID,
            "evidence identity mismatch")
    require(evidence["network_used_for_replay"] is False, "offline replay used network")
    require(evidence["inventory_version"] == protocol_inventory,
            "protocol/evidence inventory version mismatch")
    lane_results = evidence["ordered_lane_results"]
    require([row["lane"] for row in lane_results] == ORDERED_LANES,
            "evidence lane order mismatch")
    for row in lane_results:
        require(all(row.get(field) for field in (
            "query_or_source", "revision", "result", "normalized_match",
            "machine_classification", "trust_boundary", "access_boundary", "reopen_condition"
        )), f"incomplete lane result: {row['lane']}")
        require(normalize_classification(row["machine_classification"]) in MACHINE_STATES,
                f"lane machine classification invalid: {row['lane']}")
        require(isinstance(row.get("evidence"), list) and row["evidence"],
                f"unbound lane result: {row['lane']}")
        for artifact in row["evidence"]:
            path = artifact["path"]
            validate_artifact(path, artifact["sha256"])
            require(resolve_git_blob(path) == artifact["git_blob"],
                    f"evidence Git blob drift: {path}")


def validate_audit(audit: dict) -> None:
    require(audit["schema_version"] == "stage1-anchor-audit/1.0", "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity mismatch")
    require(audit["phase"] == PHASE and audit["execution_rank"] == 55,
            "audit execution identity drift")
    require(audit["v2_execution_rank"] == 289 and audit["phase_layer"] == 2,
            "audit claim order mismatch")
    require(audit["canonical_statement_file_sha256"] == STATEMENT_SHA256,
            "audit statement binding mismatch")
    require(audit["canonical_expression_sha256"] is None,
            "audit invents a canonical expression fingerprint")
    require(audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256,
            "audit protocol binding mismatch")
    require(audit["discovery_protocol"]["inventory_version"] ==
            "M0139-anchor-inventory-2026-07-17-1", "audit inventory version drift")
    require(audit["search_order_completed"] == ORDERED_LANES, "audit search order mismatch")

    candidates = audit["candidates"]
    require(len(candidates) == 4, "candidate inventory size drift")
    require(len({candidate["id"] for candidate in candidates}) == len(candidates),
            "duplicate candidate identity")
    for candidate in candidates:
        require(normalize_classification(candidate["classification"]) in MACHINE_STATES,
                f"candidate classification missing: {candidate['id']}")
        require(all(candidate.get(field) for field in (
            "revision", "exact_type", "normalized_match", "toolchain",
            "dependency_feasibility", "proof_body", "placeholder_axiom_unsafe_oracle_status",
            "blocker", "reopen_event",
        )), f"candidate provenance/trust classification incomplete: {candidate['id']}")
        require(candidate["completion_credit"] is False,
                f"candidate improperly receives proof credit: {candidate['id']}")
    coxeter4 = next(candidate for candidate in candidates
                    if candidate["id"] == "M0139-C03-COXETER4-IMMUTABLE-INFRASTRUCTURE")
    require(coxeter4["revision"] == "881d4302d008284eff8d945990387a3b162cf542",
            "coxeter4 revision drift")
    require(coxeter4["classification"] == "M5", "placeholder candidate is not M5")
    require("active proof placeholders" in coxeter4["proof_body"],
            "coxeter4 placeholder boundary drift")

    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 4,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] == coverage["prescribed_lane_count"] == 7,
            "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "inventory version is not completely classified")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["exact_terminal_candidate_found"] is False,
            "audit contradicts exact-candidate boundary")
    require(audit["root_machine_classification"] == "M4", "root M state drift")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor phase overclaims terminal completion")
    require(audit["accepted_receipt_ids"] == [], "audit invents accepted receipts")
    mathlib = next(candidate for candidate in candidates
                   if candidate["id"] == "M0139-C02-PINNED-MATHLIB-SUBSTRATE")
    require(mathlib["machine_axioms"] == {
        "CoxeterSystem.length": ["propext", "Classical.choice", "Quot.sound"],
        "CoxeterSystem.IsLeftDescent": ["propext", "Classical.choice", "Quot.sound"],
        "CoxeterSystem.IsRightInversion": ["propext", "Classical.choice", "Quot.sound"],
        "Polynomial.eval": ["propext", "Quot.sound"],
        "CategoryTheory.Simple": [],
        "CategoryTheory.IsArtinianObject": [
            "propext", "Classical.choice", "Quot.sound"
        ],
        "CategoryTheory.IsNoetherianObject": [
            "propext", "Classical.choice", "Quot.sound"
        ],
    }, "pinned substrate axiom inventory drift")
    require("sorry-free" in mathlib["machine_sorry_check"],
            "pinned substrate sorry boundary drift")


def validate_pinned_sources_and_probe() -> None:
    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(output("git", "status", "--short", cwd=MATHLIB) == "",
            "mathlib worktree is dirty")

    for query in MATHLIB_QUERIES:
        result = subprocess.run(
            ["rg", "-l", "-F", "-i", "--glob", "*.lean", query, "Mathlib"],
            cwd=MATHLIB,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        require(result.returncode == 1 and result.stdout == "",
                f"pinned mathlib query gained a hit: {query}")

    legacy_path = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_055.lean"
    require(sha256(legacy_path) == LEGACY_SHA256, "legacy audit source drift")
    legacy = legacy_path.read_text(encoding="utf-8")
    for marker in (
        "def StatementShape : Prop",
        "∀ D : KazhdanLusztigDatum",
        "881d4302d008284eff8d945990387a3b162cf542",
        "query result: total_count = 0",
        "active proof placeholders",
        "leanprover/lean4:v4.6.0-rc1",
        "no LICENSE, COPYING, NOTICE",
    ):
        require(marker in legacy, f"legacy content-bound evidence changed: {marker}")

    probe_path = HERE / "AnchorAudit.lean"
    require(sha256(probe_path) == PROBE_SHA256, "anchor probe source drift")
    probe = probe_path.read_text(encoding="utf-8")
    require(not PROHIBITED_PROBE.search(probe), "anchor probe contains prohibited trust syntax")
    checks = re.findall(r"^#check ([^\s]+)$", probe, re.MULTILINE)
    require(checks == [
        "CoxeterSystem.length",
        "CoxeterSystem.IsLeftDescent",
        "CoxeterSystem.IsRightInversion",
        "Polynomial.eval",
        "CategoryTheory.Simple",
        "CategoryTheory.IsArtinianObject",
        "CategoryTheory.IsNoetherianObject",
    ], "anchor probe declaration inventory drift")
    axiom_checks = re.findall(r"^#print axioms ([^\s]+)$", probe, re.MULTILINE)
    sorry_checks = re.findall(r"^#print sorries ([^\s]+)$", probe, re.MULTILINE)
    require(axiom_checks == checks, "anchor probe axiom inventory drift")
    require(sorry_checks == checks, "anchor probe sorry inventory drift")


def validate_receipt(receipt: dict, contract: dict) -> None:
    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    for pointer in phase_contract["phase_receipt_required_fields"]:
        parts = pointer.removeprefix("/").split("/")
        value = receipt
        for part in parts:
            require(isinstance(value, dict) and part in value,
                    f"receipt missing required field {pointer}")
            value = value[part]

    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "wrong receipt schema")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "receipt identity mismatch")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "receipt phase or intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "receipt base mismatch")
    require(receipt["claim_order"] == {
        "v2_execution_rank": 289,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "receipt claim order mismatch")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt claims acceptance")
    require(receipt["verdict"] == "no_state_change", "unexpected worker verdict")
    require(receipt["selftest_status"] == "passed", "receipt lacks passed self-test")
    require(receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"], "receipt self-test result incomplete")
    require(receipt["inputs"]["parent_inspection_order"] == [],
            "receipt parent inspection order drift")
    require(receipt["inputs"]["provider_acceptance_inherited"] is False,
            "receipt transfers provider acceptance")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding mismatch")
    inventory = receipt["candidate_inventory_result"]
    require(inventory["classification_complete"] is True
            and inventory["ordered_lanes_complete"] is True,
            "receipt phase predicate incomplete")
    require(inventory["root_proof_credit"] is False,
            "receipt improperly claims proof credit")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["first_failed_gate"]
            and receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary or freshness data missing")

    expected_bindings = {
        "anchor_inventory": ("Stage1_Instances/THM-M-0139/anchor-audit.json", AUDIT_SHA256),
        "discovery_evidence": (
            "Stage1_Instances/THM-M-0139/discovery-evidence.json", EVIDENCE_SHA256
        ),
        "anchor_probe_source": (
            "Stage1_Instances/THM-M-0139/AnchorAudit.lean", PROBE_SHA256
        ),
    }
    for role, (path, expected_sha) in expected_bindings.items():
        binding = receipt["artifact_bindings"][role]
        require(binding["role"] == role and binding["path"] == path,
                f"receipt role binding path drift: {role}")
        require(binding["sha256"] == expected_sha, f"receipt role SHA drift: {role}")
        require(binding["git_blob"] == git_blob(ROOT / path),
                f"receipt role Git blob drift: {role}")
    phase_binding = receipt["artifact_bindings"]["phase_receipt"]
    require(phase_binding["role"] == "phase_receipt"
            and phase_binding["path"] ==
            "Stage1_Instances/THM-M-0139/anchor-audit-receipt.json",
            "receipt self-binding path drift")
    require(phase_binding["sha256"] is None and phase_binding["git_blob"] is None,
            "receipt self-binding must remain acyclic")

    validator = receipt["validator_binding"]
    require(validator["path"] ==
            "Stage1_Instances/THM-M-0139/check_anchor_audit.py",
            "validator binding path drift")
    require(validator["sha256"] == sha256(HERE / "check_anchor_audit.py")
            and validator["git_blob"] == git_blob(HERE / "check_anchor_audit.py"),
            "validator binding bytes drift")
    require(validator["declared_argv"] == [
        "/usr/bin/python3", "-I", "-B",
        "Stage1_Instances/THM-M-0139/check_anchor_audit.py",
    ], "validator argv drift")
    require(validator["stdout_schema"] ==
            "stage1-validator-semantic-result/1.0", "validator stdout schema drift")

    packet = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }, "worker packet field inventory drift")
    require(packet["item_id"] == ITEM_ID and packet["state"] == "[_]",
            "worker packet identity or state drift")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drift")
    require(packet["commands"] == receipt["selftest_result"]["commands"],
            "worker packet commands differ from receipt")
    require(packet["known_failures"] == receipt["known_failures"],
            "worker packet known failures differ from receipt")
    require(packet["changed_paths"] == [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0139/AnchorAudit.lean",
        "Stage1_Instances/THM-M-0139/anchor-audit-receipt.json",
        "Stage1_Instances/THM-M-0139/anchor-audit-validation.md",
        "Stage1_Instances/THM-M-0139/anchor-audit.json",
        "Stage1_Instances/THM-M-0139/check_anchor_audit.py",
        "Stage1_Instances/THM-M-0139/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0139/discovery-evidence.json",
        "Stage1_Instances/THM-M-0139/discovery-protocol.json",
    ], "worker packet changed-path inventory drift")


def validate() -> None:
    contract = json.loads((ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json").read_text())
    theorem_dag = json.loads((ROOT / "Docs/Stage1_Theorem_DAG_v2.json").read_text())
    protocol = load("discovery-protocol.json")
    evidence = load("discovery-evidence.json")
    audit = load("anchor-audit.json")
    ledger = load("dependency-reuse-ledger.json")
    receipt = load("anchor-audit-receipt.json")

    validate_authority(contract, theorem_dag)
    validate_artifact("Stage1_Instances/THM-M-0139/Statement.lean", STATEMENT_SHA256)
    validate_artifact("Stage1_Instances/THM-M-0139/statement.json", STATEMENT_RECORD_SHA256)
    validate_artifact(
        "Stage1_Instances/THM-M-0139/statement-receipt.json", STATEMENT_RECEIPT_SHA256
    )
    validate_artifact("Stage1_Instances/THM-M-0139/discovery-protocol.json", PROTOCOL_SHA256)
    validate_output_git_blob(
        "Stage1_Instances/THM-M-0139/discovery-protocol.json",
        "0c3e3aa6303805e4c3ccddc4e8516901295390ab",
    )
    validate_artifact("Stage1_Instances/THM-M-0139/discovery-evidence.json", EVIDENCE_SHA256)
    validate_output_git_blob(
        "Stage1_Instances/THM-M-0139/discovery-evidence.json",
            "724e6aaef66171df85577dc2c800cc921ff4e571",
    )
    validate_artifact("Stage1_Instances/THM-M-0139/anchor-audit.json", AUDIT_SHA256)
    validate_output_git_blob(
        "Stage1_Instances/THM-M-0139/anchor-audit.json",
        "11cc7c8b0fddb806fd9eb126bc64cc380d0e26e3",
    )
    validate_artifact("Stage1_Instances/THM-M-0139/dependency-reuse-ledger.json", LEDGER_SHA256)
    validate_output_git_blob(
        "Stage1_Instances/THM-M-0139/dependency-reuse-ledger.json",
        "d4904beb6e2b40e9f1ab6722007c1aea4ea5ef9d",
    )
    validate_artifact("Stage1_Instances/THM-M-0139/AnchorAudit.lean", PROBE_SHA256)
    validate_output_git_blob(
        "Stage1_Instances/THM-M-0139/AnchorAudit.lean",
        "958ffc1423a87ef42e5817db635f0a52aa9e15a3",
    )
    validate_artifact(
        "Stage1_Instances/THM-M-0139/anchor-audit-validation.md", VALIDATION_SHA256
    )
    validate_output_git_blob(
        "Stage1_Instances/THM-M-0139/anchor-audit-validation.md",
        "eb62b819bda7fc02c0a91fd339f718163d3344a8",
    )
    validate_ledger(ledger)
    validate_protocol_and_evidence(protocol, evidence)
    validate_audit(audit)
    validate_pinned_sources_and_probe()
    validate_receipt(receipt, contract)


def semantic_result(*, passed: bool, message: str) -> dict:
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
        print(json.dumps(semantic_result(passed=False, message=str(exc)), sort_keys=True,
                         separators=(",", ":")))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            "A01-A03 proven for four content-bound candidate groups and all seven ordered lanes; "
            "the exact empty parent closure is audited without reuse or proof-credit transfer."
        ),
    ), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
