#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0134-ANCHOR_AUDIT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
PACKAGES = LEAN_ROOT / ".lake" / "packages"
MATHLIB = PACKAGES / "mathlib"

ITEM_ID = "S56-M-0134-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0134"
PHASE = "anchor_audit"
BASE_REVISION = "778c2db4855d48868391ea236f702e592067e798"
BASE_TREE = "27abf0ec82dad50561a14d1db471126fb7ac8665"
GRAPH_SHA256 = "9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "317857104cffa67e2a18ac260fcf0351951cd0f4c391e14caefb6be1f834e3b4"
EVIDENCE_SHA256 = "9db97217acc801f86c176a50eef7d19d8c332aa13fecb281a29d7ef90d687136"
AUDIT_SHA256 = "1672bcf6413056097547a219995ae199838a86a260b42cd4ebf1a2d470bb24d2"
LEDGER_SHA256 = "37e777540c769b35f8a2ea3bbc5db268ef0691a2d0b9b5c6bbc67d2798483167"
STATEMENT_INFRA_SHA256 = "d30389978ec093562f4bcda48c6be2d2da1cf6180b59ed9de43a198427428cb2"
LEGACY_SHA256 = "f36dd089b105c6557adcc4acdd25f64dc6133791972aab0830faf9551a6ca6bd"
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
EXPECTED_OUTPUTS = {
    "anchor-discovery-protocol.json": PROTOCOL_SHA256,
    "anchor-discovery-evidence.json": EVIDENCE_SHA256,
    "anchor-audit.json": AUDIT_SHA256,
    "dependency-reuse-ledger.json": LEDGER_SHA256,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalized_machine_state(value: str) -> str:
    for state in sorted(MACHINE_STATES, key=len, reverse=True):
        if value == state or value.startswith(state + "_") or value.startswith(state + " "):
            return state
    raise AssertionError(f"unsupported classification {value!r}")


def validate_contract(contract: dict) -> None:
    phase = next(row for row in contract["phases"] if row["phase"] == PHASE)
    require(phase["layer"] == 2 and phase["item_suffix"] == "ANCHOR_AUDIT",
            "anchor phase contract identity drift")
    require(phase["classified_negative_findings_may_satisfy_deliverable"] is True,
            "negative-classification phase rule drift")
    gates = {row["gate_id"] for row in phase["semantic_gates"]}
    require(gates == {"A01-ARTIFACTS", "A02-DISCOVERY", "A03-CLASSIFICATION"},
            "anchor semantic gate set drift")
    candidates = [row["path_pattern"] for row in phase["validator_candidates"]]
    require(candidates == [
        "Stage1_Instances/{theorem_id}/check_anchor_audit.py",
        "Stage1_Instances/{theorem_id}/check_anchor.py",
    ], "validator candidate paths drift")


def validate_repository_state(theorem_dag: dict, targets: dict) -> None:
    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 50, "legacy execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform assurance baseline drift")
    require(target["legacy_artifacts_accepted"] is False and target["theorem_complete"] is False,
            "legacy or completion boundary drift")

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 284, "v2 execution rank drift")
    require(node["phase_states"][PHASE] == "[ ]", "authoritative phase state drift")
    require(node["phase_states"]["statement"] == "[_]", "statement predecessor state drift")
    require(node["direct_hard_parents"] == [] and node["transitive_hard_ancestors"] == [],
            "hard-parent closure is no longer empty")
    require(node["direct_reuse_hint_ids"] == [] and node["shared_lemma_group_ids"] == [],
            "hint or shared-group closure is no longer empty")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256,
            "dependency context digest drift")


def validate_dependency_ledger(ledger: dict) -> None:
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "wrong dependency ledger schema")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "wrong ledger owner")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "ledger graph mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger revision mismatch")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 284,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "claim order mismatch")
    for field in (
        "parent_inspection_order", "direct_parent_ids", "transitive_ancestor_ids",
        "hard_edge_ids", "reuse_hint_ids", "shared_group_ids", "inspections",
        "reuse_decisions", "unresolved_compatibility_obligations",
    ):
        require(ledger[field] == [], f"audited empty dependency field drift: {field}")


def validate_discovery(protocol: dict, evidence: dict, audit: dict) -> None:
    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(evidence["schema_version"] == "stage1-anchor-discovery-evidence/1.0",
            "wrong discovery evidence schema")
    require(audit["schema_version"] == "stage1-anchor-audit/1.0",
            "wrong anchor inventory schema")
    for value in (protocol, evidence, audit):
        require(value["item_id"] == ITEM_ID and value["theorem_id"] == THEOREM_ID,
                "anchor artifact identity mismatch")
    version = protocol["inventory_version"]
    require(version == evidence["inventory_version"] == audit["inventory_version"],
            "inventory version mismatch")
    require(protocol["precommitted_before_replay"] is True,
            "discovery protocol is not precommitted")
    require(protocol["frozen_at_utc"] < protocol["cutoff_utc"],
            "discovery protocol time order invalid")
    require(protocol["saturation_claim"] is False, "discovery overclaims saturation")
    protocol_lanes = [row["lane"] for row in protocol["ordered_search_lanes"]]
    evidence_lanes = [row["lane"] for row in evidence["ordered_lane_results"]]
    require(protocol_lanes == ORDERED_LANES, "protocol lane order drift")
    require(evidence_lanes == ORDERED_LANES, "evidence lane order drift")
    require(len(evidence_lanes) == len(set(evidence_lanes)) == 7,
            "discovery lane traversal is not exactly once")
    require(evidence["network_used_for_replay"] is False,
            "validator evidence unexpectedly claims network use")
    require(evidence["lane_order_complete"] is True, "lane replay is incomplete")
    for lane in evidence["ordered_lane_results"]:
        for field in ("query_or_source", "revision", "result", "evidence",
                      "access_boundary", "reopen_condition"):
            require(field in lane and lane[field] not in (None, ""),
                    f"incomplete discovery evidence: {lane['lane']}.{field}")
        require(isinstance(lane["evidence"], list) and lane["evidence"],
                f"discovery lane lacks evidence: {lane['lane']}")
        for artifact in lane["evidence"]:
            path = ROOT / artifact["path"]
            require(path.is_file() and not path.is_symlink(),
                    f"missing or symlinked lane evidence: {path}")
            require(sha256(path) == artifact["sha256"], f"lane evidence SHA drift: {path}")
            if path.is_relative_to(MATHLIB):
                relative = path.relative_to(MATHLIB).as_posix()
                require(output("git", "rev-parse", f"HEAD:{relative}", cwd=MATHLIB)
                        == artifact["git_blob"], f"mathlib evidence blob drift: {path}")
            else:
                require(output("git", "rev-parse", f"HEAD:{artifact['path']}")
                        == artifact["git_blob"], f"repository evidence blob drift: {path}")

    candidates = audit["candidates"]
    ids = [row["candidate_id"] for row in candidates]
    require(len(ids) == len(set(ids)) == 6, "candidate inventory is not a six-row bijection")
    require([normalized_machine_state(row["classification"]) for row in candidates]
            == ["M4", "M2", "M4", "M5", "M5", "M4"],
            "candidate M classifications drift")
    require(all(row["terminal_proof_body"] is None or
                row["candidate_id"] == "M0134-C02-REPO-CONDITIONAL-PROOF-PACKAGE"
                for row in candidates), "unexpected terminal proof body")
    require(all(not row["classification"].startswith(("M0", "M1")) for row in candidates),
            "inventory incorrectly credits a closed or integration-ready root")
    coverage = audit["classification_coverage"]
    require(coverage == {
        "classified": 6,
        "inventory_size": 6,
        "complete_for_inventory_version": True,
        "ordered_lanes_complete": True,
        "discovery_saturation_claimed": False,
        "external_exact_proof_candidate_found": False,
        "canonical_statement_available": False,
    }, "classification coverage drift")
    require(audit["canonical_target"] is None, "canonical target was invented")
    require(audit["dependency_context"]["parent_inspection_order"] == [],
            "parent inspection order drift")
    require(audit["dependency_context"]["closure_traversed_exactly_once"] is True,
            "empty dependency closure was not audited")
    require(audit["root_vector_before"] == audit["root_vector_after_proposed"]
            == {"H": "H4", "M": "M4", "R": "R4"},
            "root debt vector changed without evidence")
    decision = audit["root_decision"]
    require(decision["classification_before"] == decision["classification_after_proposed"]
            == "M4", "root machine classification drift")
    require(decision["kernel_closed"] is False and decision["root_proof_credit"] is False,
            "root decision overclaims proof closure")
    require(audit["inventory_complete"] is True and audit["theorem_proved"] is False,
            "inventory or proof boundary drift")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor inventory overclaims terminal completion")
    require(audit["accepted_receipt_ids"] == [], "worker inventory accepts a receipt")


def validate_pinned_sources(audit: dict) -> None:
    environment = audit["immutable_environment"]
    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "materialized mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "materialized mathlib tree drift")
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    require(len(manifest["packages"]) == environment["package_count"] == 11,
            "pinned package count drift")
    for package in manifest["packages"]:
        name = package["name"].strip("«»")
        directory = PACKAGES / name
        require(output("git", "rev-parse", "HEAD", cwd=directory) == package["rev"],
                f"package revision drift: {name}")
        require(output("git", "status", "--short", "--untracked-files=no", cwd=directory) == "",
                f"package tracked worktree dirty: {name}")
    require(sha256(MATHLIB / "LICENSE") == environment["mathlib_license_sha256"],
            "mathlib license drift")

    expected_mathlib = {
        "Mathlib/Combinatorics/Enumerative/Partition/Basic.lean":
            "365f49db37156830a0c14cf5740024dcd8bea923175d4479ee2e370fdf833a09",
        "Mathlib/Combinatorics/Young/YoungDiagram.lean":
            "e58dfb68e18aedad3c0ba34dfc2ca07b72fbbb587d506b52cd1e004f30d02e5b",
        "Mathlib/Combinatorics/Young/SemistandardTableau.lean":
            "06e741f9bf34b69ff6a56229652fb50906b3ec115283a8118e5b2df2f41e86cc",
        "Mathlib/GroupTheory/Perm/Fin.lean":
            "3cf255a32be19160c0f8b94047271f3a57137ebdb81b346aeea610f94e56950f",
        "Mathlib/RepresentationTheory/Rep/Basic.lean":
            "a85f06f969682a338aa788a5b96e7cf9ae2f1eb234ab5ec5ecc60e33eaa3e948",
        "Mathlib/RepresentationTheory/Irreducible.lean":
            "6c94c6476ca26e443d0ec5fe0314deeeb3c01e3beae70247a1d96e3ca0a5c195",
    }
    for relative, digest in expected_mathlib.items():
        require(sha256(MATHLIB / relative) == digest, f"pinned support source drift: {relative}")

    docs = (MATHLIB / "docs/1000.yaml").read_text(encoding="utf-8")
    marker = "Q7574438:\n  title: Specht's theorem"
    require(marker in docs, "mathlib Specht documentation row drift")
    row_start = docs.index("Q7574438:")
    row_end = docs.find("\nQ", row_start + 1)
    row = docs[row_start:] if row_end == -1 else docs[row_start:row_end]
    require("decl:" not in row and "decls:" not in row,
            "Specht documentation row unexpectedly gained a declaration")

    exact_topic = re.compile(
        r"burnside[ _-]?young|young[ _-]?burnside|specht(?:module| module)|"
        r"youngmodule|young module|(?:^|[^a-z])standardtableau|standard tableau|tabloid|"
        r"irreducible representations? of the symmetric group|"
        r"symmetric group irreducible representations?",
        re.IGNORECASE,
    )
    hits: list[str] = []
    for package in manifest["packages"]:
        name = package["name"].strip("«»")
        directory = PACKAGES / name
        for path in directory.rglob("*.lean"):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if exact_topic.search(line):
                    hits.append(f"{name}/{path.relative_to(directory)}:{number}:{line}")
    require(hits == [], "pinned package closure gained an exact-topic hit:\n" + "\n".join(hits))


def validate_repo_sources() -> None:
    infrastructure = HERE / "StatementInfrastructure.lean"
    legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_050.lean"
    require(sha256(infrastructure) == STATEMENT_INFRA_SHA256,
            "candidate statement infrastructure drift")
    require(sha256(legacy) == LEGACY_SHA256, "legacy discovery source drift")
    text = legacy.read_text(encoding="utf-8")
    for marker in (
        "def StatementShape : Prop",
        "structure BurnsideYoungProofPackage where",
        "noncomputable def equivalence (P : BurnsideYoungProofPackage)",
        "theorem statementShape_of_proofPackage (P : BurnsideYoungProofPackage)",
        "no inhabitant of BurnsideYoungProofPackage is available",
        "def primaryLeanRepoSearchRows",
        "primaryLeanRepoSearchRows_noTerminalTheorem",
    ):
        require(marker in text, f"legacy audit marker drift: {marker}")
    forbidden = re.compile(
        r"^\s*(?:sorry|admit|axiom|constant|opaque|unsafe\s+(?:def|theorem))\b|"
        r"\bsorryAx\b|\bimplemented_by\b|\bnative_decide\b",
        re.MULTILINE,
    )
    require(forbidden.search(text) is None, "prohibited construct in legacy discovery module")
    require(forbidden.search(infrastructure.read_text(encoding="utf-8")) is None,
            "prohibited construct in target-owned infrastructure probe")


def validate_receipt(receipt: dict) -> None:
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "wrong phase receipt schema")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "phase receipt identity mismatch")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "phase receipt phase or intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "phase receipt base mismatch")
    require(receipt["support_state"] == "provisional_worker_selftest",
            "receipt support state drift")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt overclaims acceptance")
    require(receipt["verdict"] == "no_state_change", "worker verdict drift")
    require(receipt["selftest_status"] == "passed"
            and receipt["selftest_result"]["exit_code"] == 0,
            "self-test receipt is not passed")
    require(isinstance(receipt["selftest_result"]["commands"], list)
            and receipt["selftest_result"]["commands"], "self-test command list missing")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    semantic = receipt["semantic_result"]
    require(semantic == semantic_result(
        passed=True,
        message=(
            "A01-A03 are proven for the content-bound six-candidate inventory and all seven "
            "ordered lanes; the empty dependency closure is audited without reuse or "
            "acceptance transfer."
        ),
    ), "receipt semantic result drift")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding drift")
    validator = receipt["validator_binding"]
    validator_path = ROOT / validator["path"]
    require(validator_path.resolve() == Path(__file__).resolve(), "receipt selects another validator")
    require(sha256(validator_path) == validator["sha256"], "validator SHA binding drift")
    require(output("git", "hash-object", validator["path"]) == validator["git_blob"],
            "validator worker Git blob binding drift")
    require(validator["declared_argv"] == [
        "/usr/bin/python3", "-I", "-B", "Stage1_Instances/THM-M-0134/check_anchor_audit.py"
    ], "validator argv binding drift")
    result = receipt["candidate_inventory_result"]
    require(result["classified"] == result["inventory_size"] == 6,
            "receipt inventory count drift")
    require(result["classification_complete"] is True
            and result["ordered_lanes_complete"] is True,
            "receipt phase predicate incomplete")
    require(result["discovery_saturation_claimed"] is False
            and result["exact_terminal_candidate_found"] is False
            and result["canonical_statement_available"] is False,
            "receipt overclaims discovery, candidate, or statement")
    require(result["accepted_root_machine_state"] == "M4"
            and result["root_proof_credit"] is False,
            "receipt root boundary drift")
    for collection in (receipt["inputs"]["anchor_inventory"],
                       receipt["inputs"]["discovery_evidence"]):
        for artifact in collection:
            path = ROOT / artifact["path"]
            require(path.is_file() and not path.is_symlink(),
                    f"receipt input missing or symlinked: {path}")
            require(sha256(path) == artifact["sha256"], f"receipt SHA drift: {path}")
            require(output("git", "hash-object", artifact["path"]) == artifact["git_blob"],
                    f"receipt worker Git blob drift: {path}")

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        require(packet["item_id"] == ITEM_ID and packet["state"] == "[_]",
                "worker packet identity/state mismatch")
        require(packet["base_revision"] == BASE_REVISION, "worker packet base mismatch")
        require(set(packet["changed_paths"]) == set(receipt["changed_paths"]),
                "worker packet changed-path mismatch")
        require(packet["known_failures"] == receipt["known_failures"],
                "worker packet failure-boundary mismatch")
        require(packet["commands"] == receipt["selftest_result"]["commands"],
                "worker packet command mismatch")

    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0134/anchor-audit-receipt.json",
        "Stage1_Instances/THM-M-0134/anchor-audit-validation.md",
        "Stage1_Instances/THM-M-0134/anchor-audit.json",
        "Stage1_Instances/THM-M-0134/anchor-discovery-evidence.json",
        "Stage1_Instances/THM-M-0134/anchor-discovery-protocol.json",
        "Stage1_Instances/THM-M-0134/check_anchor_audit.py",
        "Stage1_Instances/THM-M-0134/dependency-reuse-ledger.json",
    }
    require(set(receipt["changed_paths"]) == expected_changed,
            "receipt changed-path inventory drift")
    actual_changed = set(output(
        "git", "diff", "--name-only", "HEAD", "--", "Stage1_Instances/THM-M-0134"
    ).splitlines())
    actual_changed.update(output(
        "git", "ls-files", "--others", "--exclude-standard", "--",
        "Stage1_Instances/THM-M-0134"
    ).splitlines())
    require(actual_changed == expected_changed - {".stage1-worker-selftest.json"},
            "owned Git delta differs from the handoff inventory")


def validate() -> None:
    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    dag_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    require(sha256(contract_path) == CONTRACT_SHA256, "phase contract digest drift")
    require(sha256(dag_path) == GRAPH_SHA256, "theorem DAG digest drift")
    for name, digest in EXPECTED_OUTPUTS.items():
        require(sha256(HERE / name) == digest, f"worker output drift: {name}")

    contract = load(contract_path)
    theorem_dag = load(dag_path)
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    evidence = load(HERE / "anchor-discovery-evidence.json")
    audit = load(HERE / "anchor-audit.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    receipt = load(HERE / "anchor-audit-receipt.json")

    validate_contract(contract)
    validate_repository_state(theorem_dag, targets)
    validate_dependency_ledger(ledger)
    validate_discovery(protocol, evidence, audit)
    validate_pinned_sources(audit)
    validate_repo_sources()
    validate_receipt(receipt)


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
    except Exception as exc:  # Always emit exactly one typed semantic result.
        print(json.dumps(semantic_result(passed=False, message=str(exc)), sort_keys=True))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            "A01-A03 proven for the content-bound six-candidate inventory and all seven "
            "ordered lanes; the empty dependency closure is audited without reuse or "
            "acceptance transfer."
        ),
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
