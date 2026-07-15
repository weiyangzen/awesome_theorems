#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0339-RELEASE."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0339"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0339-RELEASE"
THEOREM = "THM-M-0339"
BASE_REVISION = "e90521b4b150b98d81c4dca2462ad36b64d4673e"
BASE_TREE = "f12951f481d2b51f33d6d300dc2874b3c49ed0e0"
VALIDATION_BASE = "e4c6d32d1eb44bab8a06b606e6f2274e442d7f45"
VALIDATION_RECEIPT_SHA256 = (
    "841c227eaa384fc0ff4b1e1aee5348b8efe181107f2e06337c77f2cb745f8356"
)
EXPRESSION_SHA256 = "65f33abcebfa3d3c007b923852d0f89d71c3250f72b95b8645546178813503dc"
DENOMINATOR_SHA256 = "29ab54f13bdf31d2d84b7eb0ac2a07fe21a19ac12587dae5e5e58d97374c4b62"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FROZEN_ROOT_CUT = ["M0339-L-THEOREM14"]
EXPANDED_ROOT_CUT = [
    "M0339-C-RANDOM",
    "M0339-C-MCP",
    "M0339-L-REALROOTED",
    "M0339-L-INTERLACING",
    "M0339-L-BARRIER",
    "M0339-L-THEOREM14",
]
INVENTORY_IDS = [
    "M0339-ROOT",
    "M0339-S-EXACT",
    "M0339-S-PARTITION",
    "M0339-S-BOUNDARY",
    "M0339-S-FOUNDATION",
    "M0339-N-OPERATORS",
    "M0339-B-RONE",
    "M0339-B-RMANY",
    "M0339-C-RANDOM",
    "M0339-C-MCP",
    "M0339-L-REALROOTED",
    "M0339-L-INTERLACING",
    "M0339-L-BARRIER",
    "M0339-L-THEOREM14",
    "M0339-T-COR15",
    "M0339-T-ASSEMBLE",
    "M0339-X-UPSTREAM",
    "M0339-X-SOURCE",
    "M0339-X-TCB",
]
PARTIAL_IDS = [
    "M0339-S-BOUNDARY",
    "M0339-B-RONE",
    "M0339-B-RMANY",
    "M0339-T-COR15",
    "M0339-T-ASSEMBLE",
]
PROOF_DECLARATIONS = (
    "Stage1.THM_M_0339.Proof.one_part",
    "Stage1.THM_M_0339.Proof.zero_dimension",
    "Stage1.THM_M_0339.Proof.empty_family",
    "Stage1.THM_M_0339.Proof.enough_colors",
    "Stage1.THM_M_0339.Proof.constant_color_large_bound",
    "Stage1.THM_M_0339.Proof.delta_ge_one",
    "Stage1.THM_M_0339.Proof.zero_delta",
    "Stage1.THM_M_0339.Proof.mssPartitionStatement_of_hardRegimeEngine",
)
EXPECTED_REPLAY_HASHES = {
    "statement": "65f33abcebfa3d3c007b923852d0f89d71c3250f72b95b8645546178813503dc",
    "proof": "943d78a1ce73e8330409c40263ede94e2c902ded1931d90494e315d10ee6cbfa",
    "validation": "a8820bf11872eceacbee42866c601186aa7749dbd159b19482fb9c9791e89a84",
}
EXPECTED_INPUTS = {
    "README.md": "dc0da99f5d4eb68fbdbaa42f64fcd2669b355d80b3e077db74ecbafe55369678",
    "instance.json": "073704317907a3e923ea925577d250cf6971bd55d388438678184a4d70f04675",
    "task-dag.json": "7b4427d5ddc061c47e58f476f7f51487bec7c25506e85d5b2e4cd59ed94aab27",
    "Statement.lean": "b906c95d7778f7d908a4f2e1373f2256786fcb62094be72b79920a558f3679fd",
    "Proof.lean": "6656a0d0b433069e149a583d053d98cfcdd42bcddfb374ad68428f513d379ccd",
    "Validation.lean": "0724a0464dd045471f539a33887292448a28cf2fc454ffc04606179406dbffe3",
    "ObligationTree.lean": "9722eb3711877516e30d040d30fcb6c998d28244d72cbb4342034e25c9881323",
    "anchor-audit.json": "ee53efba48e877cbe76508602952ddd03b6ba18fd7c5dd003513f2870d37e8a9",
    "obligation-registry.json": "e61f9b1e4146bde5fbe0c3beec92663cac3645d26a12c616af7b7f79a2b383c0",
    "typed-graphs.json": "6700d71b249d3405dbe251589a6f662c6ba3454dbba7dbec34d7b43a4d728046",
    "source-statement-crosswalk.md": "6b16fd0285d90a04362272be8221381fbfcc36b8ee82daacbab704f76087c6c3",
    "proof-receipt.json": "551a1f9dc6f454d142ef3a15e3a6cd7c33b3f39b7b68b89ce271a35d1f97711a",
    "proof-blocker.json": "a68f7411396d8cfe7f5b8e06522ed5230725170c5be3bd808a67fdea84f6b1a7",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-spec.json": "bd62ec1774c4a9fa16532bb5d9dd70306ce651fe5ea6e5c803ab4ce7c8b4cff4",
    "validation-phase.md": "0ce5ecc778fce64de0276925d4ea101805b60f7f849473aebee41e2c31991ef3",
    "check_validation.py": "dd3ba75f98d27dce9f4ec1ff9ec631cbe5008031428c8407342c4c4ea49a824f",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "58044e507bed529c809f8f5d4d9680ba86dc8812e4f614836d474fa6375f624e",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5ed9edc880c295fe4df0d419b72e4489e0aa9e0cbe18163b64c177104d7e264c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUT_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, historical receipts, registry, graphs, and hashes agree",
    "PASS current narrow replay: exact statement, seven elementary bodies, and conditional composition checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: HardRegimeEngine is unproved; H1/M4/R4 unchanged and zero frozen obligations closed",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


if not __debug__:
    raise RuntimeError("release validation requires Python assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600,
    env: dict[str, str] | None = None, expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exit {result.returncode}, expected {expected_exit}: {argv!r}\n"
            f"{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def reported_axioms(output: str, declaration: str) -> set[str]:
    matches = re.findall(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def current_narrow_replay() -> dict[str, object]:
    validator_path = HERE / "check_validation.py"
    module_spec = importlib.util.spec_from_file_location("m0339_historical_validator", validator_path)
    assert module_spec is not None and module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    lean = Path(os.environ["HOME"]) / (
        ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    )
    bwrap = Path("/usr/bin/bwrap")
    assert lean.is_file() and bwrap.is_file()
    assert sha256(lean) == module.LEAN_SHA256
    assert sha256(bwrap) == module.BWRAP_SHA256
    assert module.LEAN_COMMIT in run([str(lean), "--version"], env=module.BASE_ENV).stdout

    outputs = module.isolated_replay(lean, bwrap, module.pinned_lean_path(lean))
    hashes = {
        name: hashlib.sha256(output.encode()).hexdigest()
        for name, output in outputs.items()
    }
    assert hashes == EXPECTED_REPLAY_HASHES
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined
    assert all("error:" not in output.lower() for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 8
    closure = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unexpected_bodyless=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        "output_sha256": hashes,
        "sorry_free_reports": 8,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "closure": {
            "declarations": int(closure.group(1)),
            "modules": int(closure.group(2)),
            "unexpected_bodyless": [],
            "unsafe": [],
        },
    }


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 832 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 832,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0339-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0339-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"

    for filename, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / filename) == expected, f"release input drifted: {filename}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert registry["root_obligation_id"] == "M0339-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_closed": False,
        "root_machine_debt": "M4",
        "remaining_root_cut_set": FROZEN_ROOT_CUT,
        "composition_certificates_checked": [
            "Stage1.THM_M_0339.ObligationTree.root_compose"
        ],
        "audit_complete": False,
        "theorem_complete": False,
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0339-ROOT")
    assert {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    } == ROOT_VECTOR

    assert proof["accepted"] is False
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["supported_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == EXPANDED_ROOT_CUT
    assert blocker["remaining_root_cut_set"] == EXPANDED_ROOT_CUT
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    assert validation["root_vector_before"] == validation["root_vector_after"] == ROOT_VECTOR
    assert validation["result"]["supported_obligation_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M4"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert validation["independent_validation"]["decision"] == "fail_closed"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == receipt["proposed_state"] == packet["state"] == "[_]"
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["current_snapshot_recipe_replay"] is False

    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["authoritative_remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert decision["expanded_remaining_root_cut_set"] == EXPANDED_ROOT_CUT
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0339-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["node_gate"] == "M0339-L-THEOREM14"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    for key in (
        "premise_free_exact_root_kernel_closure",
        "integrated_validation_recipe_current",
        "normal_lake_resolution_current",
        "dependency_master_acceptance",
        "audit_inventory_reconciliation",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_profile",
        "complete_provenance_trust_tcb_and_sbom",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "independent_signed_runner_attestations",
        "independent_minimal_verifier",
        "protected_ci_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key
    assert decision["evidence_reconciliation"]["validated_frozen_obligation_count"] == 0

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert set(spec["covered_declarations"]) == {
        "Stage1.THM_M_0339.MSSPartitionStatement", *PROOF_DECLARATIONS
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["release_accepted"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["result"]["root_vector_before"] == ROOT_VECTOR
    assert receipt["result"]["root_vector_after"] == ROOT_VECTOR
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["remaining_root_cut_set"] == EXPANDED_ROOT_CUT
    assert receipt["dependency"] == dependency
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    for relative, expected in receipt["release_artifact_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"release artifact drifted: {relative}"
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id",
            "cwd",
            "argv",
            "env_allowlist",
            "timeout_seconds",
            "network_policy",
            "network_enforcement",
            "expected_exit",
            "expected_outputs",
            "covered_obligation_ids",
            "covered_declarations",
        )
    }

    observed = current_narrow_replay()
    assert receipt["current_narrow_replay"] == observed
    assert observed["output_sha256"] == EXPECTED_REPLAY_HASHES

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == decision["known_failures"]
    actual = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`",
        "`[H1, M4, R4]`",
        "`HardRegimeEngine`",
        "`AUDIT-Z`",
        "`THEOREM-Z`",
        "accepts no",
    ):
        assert fragment in handoff, fragment

    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["repository_state"]["release_clean"] is False
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
