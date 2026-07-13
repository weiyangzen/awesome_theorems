#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1009-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1009"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1009-RELEASE"
THEOREM = "THM-M-1009"
BASE_REVISION = "a7c34044268bf5745e40c011134b447dd1e7cd0f"
BASE_TREE = "7808aabc33d7bad66b0b6ad394f3e5e9835d462b"
EXPRESSION_SHA256 = "5933a50ff097d2de1336a67d4671b3caf7add728d2be6f8be22f95a0385dec1f"
DENOMINATOR_SHA256 = "24570f903e38e644cc31fc4f8725224e3551ab48325fedc9a072fdedb4c1b93d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "intake.json": "e5aa5b69351c06302c392b20105c1187c3a3437619743c752697aa7e599be833",
    "README.md": "962cfa92cd7fd63bcbb1250d9c12f5e8e31f6195d9264d58a595cfab8db2529c",
    "source_statement_crosswalk.md": "6a8366776fae6ee0165b0c3903e9139603d13f62bd6758638834642b36f77cc3",
    "Statement.lean": "9906d8bf53b69bff68246b938627f5f117611fbdf95e2e54f01758c28ce5d831",
    "statement.json": "621c47d483467acd98eb0370930050e61b1818d68fbca29aed714111db1c67fe",
    "anchor-audit.json": "4182164ae4b6951d635fd90f70c85add5bbd26b66c4756bccafe7d8a798447f9",
    "obligation-registry.json": "0baaf6dd25fc4222d849fdfaa2240a537c6bd4ca81f9e18ecb8bab8f112e3fb0",
    "typed-graphs.json": "9fcd990adf7edf38e8cf2465b54d3c2ece7b82cc6638396679a34a8781e99f2a",
    "ObligationTree.lean": "9481f4c7c973a04eab69c35c7e27de90f6fef79ad2de6615994993c6e312cdae",
    "Proof.lean": "0e498dbd2d3c0f4d8def2a305388605fe571d3d77aa2033bb4e3edd633ef4fde",
    "proof-receipt.json": "bb201c531dfd646758b97ac0b12f645b2051cda87cad8d3dd2b4b2053f704272",
    "proof-status.json": "9259715f5b5249f8eec5d5e34fdb40303639fbc757191442c987ed7a04a56056",
    "Validation.lean": "e20e3637ef4c5f3ebf9fe3e4ba1d453f604126c6e2d6a3d2cced37483ee9ab1e",
    "validation-spec.json": "4e08d0d2a983b9b7cbffe309223813e16302a6c5e1ab4749ffaa267a757a59cc",
    "validation-receipt.json": "f86f9bf089ec9f6315ef45f6d66e4c032a16ec4131611feae169fa90c4068570",
    "validation-phase.md": "f9e6eec0dbcab39070685466127f6badee514073cd89c288aa96718d9fe2ceea",
    "check_validation.py": "161e5e5b173132c636fdfdbab7497382f29f6ae8a6e274237c211d09647044b8",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "6d7e70f4f7b6fdbd0ce89c747e9c29a87bf66421493e86c1b34332975a8bc625",
    "Docs/Stage1_Blueprint_rev-5.6.md": "ec4cd8a897ae20c4d7c940fbb5be8d5a814377baeed1ebf7982d98c1d9eaeac0",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
ALL_OBLIGATIONS = {
    "M1009-ROOT",
    "M1009-S-EVENTS",
    "M1009-S-DIVERGE",
    "M1009-B-ZERO",
    "M1009-N-COUNT",
    "M1009-L-SECOND-MOMENT",
    "M1009-L-TAIL",
    "M1009-L-RATIO",
    "M1009-L-CONTINUITY",
    "M1009-T-ASSEMBLE",
    "M1009-X-SOURCE",
    "M1009-X-ANCHOR",
    "M1009-X-TCB",
    "M1009-D-READABLE",
    "M1009-W-VALIDATE",
}
MACHINE_CUT = {
    "M1009-L-SECOND-MOMENT",
    "M1009-L-TAIL",
    "M1009-L-RATIO",
    "M1009-L-CONTINUITY",
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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=420,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}",
    )
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed checking")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    proof_status = load(HERE / "proof-status.json")
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

    target = next(
        (row for row in targets["targets"] if row["theorem_id"] == THEOREM), None
    )
    require(target is not None, "target absent from manifest")
    require(target["execution_rank"] == 289, "execution rank drifted")
    require(
        target["baseline"] == "L0" and target["rework_required"] is True,
        "uniform L0 baseline drifted",
    )
    require(target["lifecycle_mode"] == "planned", "target lifecycle drifted")
    require(target["theorem_complete"] is False, "target authority claims completion")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1009-VALIDATION"),
        None,
    )
    expected_release_item = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 289,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1009-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    require(release_item == expected_release_item, "release execution item drifted")
    require(
        validation_item is not None and validation_item["state"] == "[_]",
        "validation dependency is not provisional [_]",
    )
    require(validation_item["attempts"] == 1, "validation attempt count drifted")

    accepted_vector = {"human": "H1", "machine": "M3", "readability": "R3"}
    require(intake["lifecycle_mode"] == "planned", "intake lifecycle drifted")
    require(intake["root_vector"] == accepted_vector, "accepted intake vector drifted")
    require(intake["theorem_complete"] is False, "intake claims theorem completion")
    require(
        intake["canonical_formal_target"]["gate_state"] == "open_pending_statement_phase",
        "intake legacy boundary drifted",
    )
    require(
        intake["canonical_formal_target"]["elaborated_expression_hash"] is None,
        "intake was silently reconciled",
    )
    require(
        statement["canonical_formal_target"]["elaborated_expression_sha256"]
        == EXPRESSION_SHA256,
        "canonical target expression drifted",
    )
    require(statement["statement_elaborated"] is True, "statement lost elaboration")
    require(statement["theorem_complete"] is False, "statement claims completion")
    require(anchor["root_vector_after"] == accepted_vector, "anchor vector drifted")
    require(anchor["theorem_complete"] is False, "anchor claims completion")
    require(registry["denominator_sha256"] == DENOMINATOR_SHA256, "registry drifted")
    require(
        {row["obligation_id"] for row in registry["obligations"]} == ALL_OBLIGATIONS,
        "registry obligation universe drifted",
    )
    require(
        {row["obligation_id"] for row in graphs["nodes"]} == ALL_OBLIGATIONS,
        "typed graph obligation universe drifted",
    )
    require(
        graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
        "graph/registry denominator drifted",
    )
    require(
        all(
            (row["human_debt"], row["machine_debt"], row["readability_debt"])
            == ("H1", "M3", "R3")
            and row["evidence_ids"] == []
            for row in graphs["nodes"]
        ),
        "frozen graph no longer records the accepted H1/M3/R3 boundary",
    )
    boundary = graphs["closure_boundary"]
    require(boundary["closed_obligations"] == [], "graph has accepted closure")
    require(boundary["root_closed"] is False, "frozen graph claims root closure")
    require(boundary["audit_complete"] is False, "graph claims audit completion")
    require(boundary["theorem_complete"] is False, "graph claims theorem completion")
    require(
        set(boundary["remaining_root_cut_set"]) == MACHINE_CUT,
        "authoritative machine cut drifted",
    )

    require(proof["support_state"] == "provisional_worker_selftest", "proof support drifted")
    require(proof["accepted"] is False, "proof receipt became accepted")
    require(proof["result"]["root_kernel_closed"] is True, "local proof root was lost")
    require(
        proof["result"]["accepted_root_closed"] is False,
        "proof receipt claims accepted root",
    )
    require(proof["result"]["theorem_complete"] is False, "proof claims completion")
    require(proof_status["root_kernel_closed"] is True, "proof status lost local root")
    require(proof_status["root_accepted"] is False, "proof status claims acceptance")
    require(proof_status["theorem_complete"] is False, "proof status claims completion")
    require(
        validation["support_state"] == "provisional_worker_selftest",
        "validation support drifted",
    )
    require(validation["accepted"] is False, "validation became accepted")
    require(validation["release_grade"] is False, "validation became release grade")
    result = validation["result"]
    require(result["root_kernel_replay"] == "pass", "validation lost kernel replay")
    require(result["root_accepted"] is False, "validation claims accepted root")
    require(
        result["structured_state_freshness"]
        == "fail_closed_preproof_graph_records_root_open_M3",
        "validation silently reconciled structured state",
    )
    require(result["hermetic_release_gate"] == "fail_closed", "hermetic gate cleared")
    require(result["independent_runner_gate"] == "fail_closed", "independent gate cleared")
    require(
        result["audit_complete"] is False and result["theorem_complete"] is False,
        "validation claims terminal completion",
    )

    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "release decision identity drifted")
    require(
        decision["verdict"] == "blocked" and decision["release_accepted"] is False,
        "release decision is not blocked",
    )
    require(
        decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
        "blocked release advanced lifecycle",
    )
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    require(
        decision["terminal_decisions"]
        == {
            "audit_complete": False,
            "theorem_complete": False,
            "audit_z": "blocked",
            "theorem_z": "blocked",
        },
        "terminal decisions are not fail-closed",
    )
    require(
        decision["root_vector"]["accepted_before"] == ["H1", "M3", "R3"]
        and decision["root_vector"]["accepted_after"] == ["H1", "M3", "R3"],
        "release silently changed the accepted vector",
    )
    require(
        decision["first_failed_gate"]["gate_id"]
        == "S56-10.2-DEPENDENCY-ACCEPTANCE",
        "first failed node gate drifted",
    )
    require(
        decision["first_failed_release_gate"]["gate_id"]
        == "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
        "first failed release gate drifted",
    )
    require(
        decision["first_failed_reproduction_gate"]["gate_id"]
        == "S56-10.6-HERMETIC-COLD-BUILD",
        "first reproduction gate drifted",
    )
    require(
        set(decision["authoritative_open_obligation_ids"]) == ALL_OBLIGATIONS,
        "decision open obligation projection drifted",
    )
    require(
        set(decision["authoritative_remaining_machine_cut_set"]) == MACHINE_CUT,
        "decision machine cut drifted",
    )
    for key in (
        "authoritative_graph_reconciled",
        "structured_state_fresh",
        "audit_inventory_complete_and_accepted",
        "pinpoint_h0_and_independent_source_review",
        "independent_r0_review",
        "complete_transitive_provenance_foundation_tcb",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_required_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False, f"release cleared {key}")

    require(spec["item_id"] == receipt["item_id"] == ITEM, "recipe/receipt item drifted")
    require(spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "recipe/receipt theorem drifted")
    require(
        spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "release recipe argv drifted",
    )
    require(
        spec["cwd"] == "." and spec["network_policy"] == "denied",
        "release recipe policy drifted",
    )
    require(
        spec["timeout_seconds"] == 420 and spec["expected_exit"] == 0,
        "release recipe resource contract drifted",
    )
    require(
        set(spec["covered_obligation_ids"]) == ALL_OBLIGATIONS,
        "release recipe misses a frozen obligation",
    )
    require(receipt["support_state"] == "provisional_worker_selftest",
            "release receipt support drifted")
    require(
        receipt["release_grade"] is False and receipt["accepted"] is False,
        "release receipt falsely claims acceptance",
    )
    require(receipt["master_accepted"] is False, "worker claims master acceptance")
    require(receipt["dependency"] == decision["dependency"], "dependency ledgers disagree")
    require(receipt["known_failures"] == decision["known_failures"], "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS, "changed paths drifted")
    for name, expected in receipt["inputs"].items():
        require(digest(ROOT / name) == expected, f"receipt input drifted: {name}")
    require(receipt["authority_inputs"] == AUTHORITY_INPUTS, "authority ledger drifted")
    require(receipt["decision_id"] == decision["decision_id"], "wrong decision ID")
    require(
        receipt["base_revision"] == decision["base_revision"] == BASE_REVISION,
        "release base revision drifted",
    )
    require(
        receipt["base_tree"] == decision["base_tree"] == BASE_TREE,
        "release base tree drifted",
    )
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "release decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "release specification hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "release checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "release projection hash drifted")
    require(receipt["result"]["verdict"] == decision["verdict"] == "blocked",
            "receipt/decision verdict mismatch")
    require(receipt["result"]["audit_complete"] is False,
            "release receipt claims audit completion")
    require(receipt["result"]["theorem_complete"] is False,
            "release receipt claims theorem completion")
    require(receipt["result"]["accepted_receipt_ids"] == [],
            "release receipt contains accepted receipts")
    require(receipt["retry_condition"] == decision["retry_condition"],
            "release retry conditions disagree")

    require(selftest["item_id"] == ITEM, "worker packet belongs to another item")
    require(selftest["theorem_id"] == THEOREM, "worker packet theorem drifted")
    require(selftest["state"] == "[_]", "worker packet proposes an illegal state")
    require(selftest["base_revision"] == BASE_REVISION, "worker packet base drifted")
    require(selftest["base_tree"] == BASE_TREE, "worker packet tree drifted")
    require(set(selftest["changed_paths"]) == CHANGED_PATHS,
            "worker packet changed paths drifted")
    require(selftest["known_failures"], "worker packet hides all failures")
    require(
        "verdict is blocked" in selftest["output_summary"]
        and "audit_complete=false" in selftest["output_summary"]
        and "theorem_complete=false" in selftest["output_summary"],
        "worker packet omits the exact negative result",
    )
    actual_changes = {
        line[3:]
        for line in git(
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            f"Stage1_Instances/{THEOREM}",
            ".stage1-worker-selftest.json",
        ).splitlines()
        if line
    }
    require(actual_changes == CHANGED_PATHS, "actual scoped changes differ from handoff")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = without_comments((HERE / name).read_text(encoding="utf-8"))
        require(prohibited.search(source) is None, f"prohibited Lean construct in {name}")

    require(MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drifted")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "pinned mathlib worktree is dirty before replay")
    validation_env = os.environ.copy()
    validation_env.update({"LC_ALL": "C", "TZ": "UTC", "PYTHONOPTIMIZE": "0"})
    validation_output = run(
        ["python3", "-B", str(HERE / "check_validation.py")], env=validation_env
    )
    for fragment in (
        "PASS THM-M-1009 narrow validation",
        "kernel: exact frozen root and frozen composition replayed from temporary source copies",
        "trust: both root paths report exactly propext, Classical.choice, Quot.sound; hygiene passed",
        "blocked: proof master acceptance, graph reconciliation, cold offline hermetic replay, and distinct-runner verification",
    ):
        require(fragment in validation_output, f"validation output lost {fragment!r}")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "pinned mathlib worktree changed during replay")

    handoff = " ".join((HERE / "release-validation.md").read_text(encoding="utf-8").split())
    for fragment in (
        "`blocked`",
        "`[H1, M3, R3]`",
        "`AUDIT-Z`",
        "`THEOREM-Z`",
        "release_grade=false",
        "accepts no receipt",
    ):
        require(fragment in handoff, f"handoff omits {fragment!r}")
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n"), f"missing final newline: {relative}")
        require(b"\r" not in data and b"\x00" not in data, f"invalid byte in {relative}")
        require(
            all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
            f"trailing whitespace in {relative}",
        )

    print("PASS release inputs: target, DAG dependency, receipts, registry, graphs, and hashes agree")
    print("PASS current Lean replay: exact root and differential composition; axioms " + str(EXPECTED_AXIOMS))
    print("PASS fail-closed state: lifecycle planned; accepted root H1/M3/R3; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
