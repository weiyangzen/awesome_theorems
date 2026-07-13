#!/usr/bin/env python3
"""Fail-closed verdict checker for S56-M-1016-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1016"
THEOREM = "THM-M-1016"
ITEM = "S56-M-1016-RELEASE"
BASE_REVISION = "8c4a58ee73da7fa8dce7a9f9bfcc0ec5fd713588"
BASE_TREE = "3fa6104e948efe18f95dcfc23e9d2bf7f3dad150"
EXPRESSION_SHA256 = "9cdb0281811565d62d5b8a7cc2933f27facd49e39aff10c29fe1d7702797dbee"
DENOMINATOR_SHA256 = "a0552dc7b546e055218200f066ebeb2cce448a60ac46a162949c1a57647fcef4"
EXPECTED_INPUTS = {
    "instance.json": "1e2a72aec53c73e5d407a355781aafd147305b1414515a8fd65761e1c5429c80",
    "task-dag.json": "10ba187bf8314e9541ec2fd8ac050f3fbd3c46ede3c63f24e6326855b4a73b4a",
    "README.md": "d819de2aac31698a9f25aa923a63b5af44f9bf6e3ea6e92d0270187d9092766c",
    "source-statement-crosswalk.md": "282065aa0a6156868e052ad6f65e03135b781166288579a5501ef3279a50dc53",
    "Statement.lean": "75d7800ccedfe5499e997adb68acbb9f7bef828815cdf2802b4735babaa5f011",
    "statement.json": "d13f68e5c331537b1f701ddb6aeac63329a2194b04ae47e4b4ca695b55b13c81",
    "anchor-audit.json": "0fc50ec020adcd90b00e12e75e083bf9f785a02df13f3ff22480bb9da4d4a829",
    "obligation-registry.json": "5f0efabd00ce7236b0319b8800f38230404495fc01481d6c23d993d651d6a8cc",
    "typed-graphs.json": "c5a024eac21553cb02848024d7e7957ca80a2c095e920e4578313fc5677d1f68",
    "ObligationTree.lean": "4e740dd14d4efa9440ea7bb48803b9cd664e41e1dbe2eb7422b01eb6e85694cd",
    "Proof.lean": "64af1c77d3819ed735f7953b8ac62c2b43e77c4acc82f1af2fae839499393bac",
    "proof-receipt.json": "05045132b311970ba0d7eb9cd96fe36e3e072c5cfb2fd277cad3d96bc1a3409f",
    "Validation.lean": "ddd214e7013a802f5d5f3a498a40bd46d2f8afd8831fd525ba4c9d6998f9b448",
    "validation-spec.json": "60654897c290ad7c84e891a9f2cbc6f4a6b3066d0e40755a4f5dce5eee9e31af",
    "validation-receipt.json": "e6baff984e92e075e033e114d05743768ecead8aa6f073416c34249561d4b86f",
    "validation-phase.md": "a62f17e126c0ad7a18fa80730740cca766d359ef9f5c49ae2a83c1828b444cab",
    "check_validation.py": "98d362ce2820acdcbd1c98b366fc279b12bab4bb04e365998076fbb165fcc4e1",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "ecec74713a007e34d80bde119074fa56f83862f84c14bf8e0bbefb5a46c4be9c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "19bcc19b4d07132dc2ee163df61d665eaa4205866d12e0d19ce2cfc409d1220c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
ALL_OBLIGATIONS = {
    "M1016-ROOT", "M1016-S-DEFINITIONS", "M1016-S-BOUNDARIES",
    "M1016-S-FOUNDATION", "M1016-N-TIGHTNESS", "M1016-N-CONCENTRATION",
    "M1016-C-REMAINDER", "M1016-L-LITTLE-O", "M1016-L-PRODUCT",
    "M1016-L-LINEAR-MAP", "M1016-T-REMAINDER", "M1016-T-ASSEMBLE",
    "M1016-X-SOURCE", "M1016-X-PROVENANCE",
}
FROZEN_LOCAL_CLOSED = {
    "M1016-S-DEFINITIONS", "M1016-S-BOUNDARIES",
    "M1016-L-LINEAR-MAP", "M1016-T-ASSEMBLE",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            argv, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=120, check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")


def git(*args: str) -> str:
    result = run(["git", *args])
    require(result.returncode == 0, f"git command failed: {args!r}\n{result.stdout}")
    return result.stdout.strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed checking")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    for name, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / name) == expected, f"reconciled input drifted: {name}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for name, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / name) == expected, f"authority input drifted: {name}")

    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    require(target is not None and target["execution_rank"] == 295, "target/rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "target authority no longer records planned/incomplete")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1016-VALIDATION"), None
    )
    expected_release_item = {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 295,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1016-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    require(release_item == expected_release_item, "release execution item drifted")
    require(validation_item is not None and validation_item["state"] == "[_]",
            "validation dependency is not provisional [_]")

    planned_vector = {"H": "H2", "M": "M4", "R": "R4"}
    require(instance["lifecycle"] == "planned", "instance lifecycle drifted")
    require(instance["root_vector"] == planned_vector, "planned root vector drifted")
    require(instance["accepted_proof_state"] == [], "instance has accepted proof state")
    require(instance["audit_complete"] is False and instance["theorem_complete"] is False,
            "instance claims terminal completion")
    require(task_dag["lifecycle"] == "planned" and task_dag["accepted_states"] == [],
            "target-local task authority advanced")
    require(all(row["state"] == "open" for row in task_dag["tasks"]),
            "target-local task DAG no longer records the open boundary")
    require(statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical target expression drifted")
    require(statement["statement_elaborated"] is True and statement["theorem_proved"] is False,
            "statement boundary drifted")
    require(anchor["audit_complete"] is False and anchor["theorem_complete"] is False,
            "anchor phase claims terminal completion")
    require(registry["denominator_sha256"] == DENOMINATOR_SHA256, "registry drifted")
    require({row["obligation_id"] for row in registry["obligations"]} == ALL_OBLIGATIONS,
            "obligation universe drifted")
    require({row["obligation_id"] for row in graphs["nodes"]} == ALL_OBLIGATIONS,
            "typed graph obligation universe drifted")
    require(all(row["evidence_ids"] == [] for row in graphs["nodes"]),
            "frozen graph gained accepted evidence IDs")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is False and boundary["audit_complete"] is False
            and boundary["theorem_complete"] is False, "frozen graph claims terminal closure")
    require(boundary["remaining_root_cut_set"] == ["M1016-T-REMAINDER"],
            "frozen machine cut drifted")

    require(proof["support_state"] == "provisional_worker_selftest", "proof support drifted")
    require(proof["result"]["root_closed"] is True, "provisional proof lost local root")
    require(proof["result"]["theorem_complete"] is False, "proof claims completion")
    require(validation["support_state"] == "provisional_worker_selftest", "validation support drifted")
    require(validation["accepted"] is False and validation["release_grade"] is False,
            "validation became accepted or release grade")
    require(validation["content_addressed_release_evidence"] is False,
            "validation became content-addressed release evidence")
    vresult = validation["result"]
    require(vresult["provisional_root_kernel_closed"] is True, "prior local validation root lost")
    require(vresult["accepted_closed_obligation_ids"] == [], "validation claims accepted obligations")
    require(vresult["structured_state_freshness"] == "fail_closed_stale_pre_proof_typed_graph",
            "validation silently reconciled structured state")
    require(vresult["foundation_and_complete_tcb_gate"] == "fail_closed",
            "foundation/TCB gate cleared")
    require(vresult["hermetic_release_gate"] == "fail_closed"
            and vresult["independent_distinct_runner_gate"] == "fail_closed",
            "release validation gate cleared")
    require(vresult["audit_complete"] is False and vresult["theorem_complete"] is False,
            "validation claims terminal completion")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by)\b|^[ \t]*(?:axiom|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        require(prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None,
                f"prohibited mechanism in {name}")

    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "release decision identity drifted")
    require(decision["verdict"] == "blocked" and decision["release_accepted"] is False,
            "release decision is not blocked")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == []
            and decision["accepted_closed_obligation_ids"] == [],
            "worker accepted evidence")
    require(decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
    }, "terminal decisions are not fail-closed")
    require(decision["root_vector"]["authoritative_planned_before"] == ["H2", "M4", "R4"]
            and decision["root_vector"]["authoritative_planned_after"] == ["H2", "M4", "R4"],
            "release silently changed the planned structured vector")
    require(decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE",
            "first node gate drifted")
    require(decision["failed_release_assurance_gate"]["gate_id"]
            == "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "recorded failed assurance gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"]
            == "S56-10.6-HERMETIC-COLD-BUILD", "first reproduction gate drifted")
    require(set(decision["frozen_locally_closed_but_not_master_accepted_obligation_ids"])
            == FROZEN_LOCAL_CLOSED, "decision frozen local closure projection drifted")
    require(set(decision["frozen_not_locally_closed_obligation_ids"])
            == ALL_OBLIGATIONS - FROZEN_LOCAL_CLOSED,
            "decision frozen non-closure projection drifted")
    require(decision["frozen_preproof_machine_cut_set"] == ["M1016-T-REMAINDER"],
            "decision frozen cut drifted")
    for key in (
        "authoritative_graph_reconciled", "structured_state_fresh",
        "audit_inventory_complete_and_accepted", "pinpoint_h0_and_independent_source_review",
        "independent_r0_review", "complete_transitive_provenance_foundation_tcb",
        "immutable_clean_release_input", "shared_dependency_cache_remained_unmodified_during_worker_run",
        "predecessor_recipe_replay_currently_passes",
        "hermetic_cold_offline_replay", "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_required_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False, f"release cleared {key}")
    require(any("corrected structured predecessor recipe" in row
                for row in decision["remaining_root_cut_set"]), "cut set omits replay repair")
    require(any("no-.lake-mutation constraint" in row for row in decision["known_failures"]),
            "decision omits the forbidden shared-cache mutation")

    replay = decision["predecessor_recipe_replay"]
    require(replay["exit_code"] == 1 and replay["result"] == "blocked_before_lean_replay",
            "predecessor replay was misclassified")
    require("No such file or directory: 'lake'" in replay["failure"],
            "predecessor failure boundary drifted")
    validation_source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    require('set(os.environ) == {"LC_CTYPE"}' in validation_source,
            "predecessor no longer enforces its env-cleared contract")
    require('["lake", "env", "printenv", "LEAN_PATH"]' in validation_source,
            "predecessor no longer invokes bare lake")
    require(shutil.which("lake", path=os.defpath) is None,
            "lake became resolvable in platform default path; replay record is stale")

    require(spec["item_id"] == receipt["item_id"] == ITEM, "recipe/receipt item drifted")
    require(spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "recipe/receipt theorem drifted")
    require(spec["argv"] == ["/usr/bin/python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
            "release recipe argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied",
            "release recipe policy drifted")
    require(spec["timeout_seconds"] == 120 and spec["expected_exit"] == 0,
            "release recipe resource contract drifted")
    require(set(spec["covered_obligation_ids"]) == ALL_OBLIGATIONS,
            "release recipe misses a frozen obligation")
    require(spec["covered_declarations"] == [],
            "negative release recipe falsely claims declaration coverage")
    require(receipt["support_state"] == "provisional_worker_selftest",
            "release receipt support drifted")
    require(receipt["accepted"] is False and receipt["release_grade"] is False
            and receipt["master_accepted"] is False, "release receipt claims acceptance")
    require(receipt["dependency"] == decision["dependency"], "dependency ledgers disagree")
    require(receipt["result"]["verdict"] == "blocked"
            and receipt["result"]["theorem_complete"] is False,
            "release receipt result drifted")
    require(receipt["result"]["accepted_receipt_ids"] == [], "receipt accepts evidence")
    require(receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE",
            "receipt first gate drifted")
    require(any("no-.lake-mutation constraint" in row for row in receipt["known_failures"]),
            "receipt omits the forbidden shared-cache mutation")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "receipt decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "receipt spec hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "receipt checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "receipt public projection hash drifted")

    require(set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }, "worker self-test schema drifted")
    require(selftest["item_id"] == ITEM and selftest["state"] == "[_]",
            "worker self-test identity/state drifted")
    require(selftest["base_revision"] == BASE_REVISION, "self-test base drifted")
    require(set(selftest["changed_paths"]) == CHANGED_PATHS, "changed-path ledger drifted")
    require(any("no-.lake-mutation constraint" in row for row in selftest["known_failures"]),
            "self-test omits the forbidden shared-cache mutation")
    require(all(row["exit_code"] == 0 for row in selftest["commands"]
                if row.get("expected") == "pass"), "self-test records a failed pass command")
    blocked_commands = [row for row in selftest["commands"] if row.get("expected") == "blocked"]
    require(len(blocked_commands) == 1 and blocked_commands[0]["exit_code"] == 1,
            "self-test predecessor blocker drifted")

    print("release-decision: PASS (blocked; dependency unaccepted; planned H2/M4/R4 unchanged)")
    print("predecessor replay: BLOCKED before Lean (bare lake unresolved under exact cleared env)")
    print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
    print("status: provisional [_] negative release reconciliation; release_grade=false")


if __name__ == "__main__":
    main()
