#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0414-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0414"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0414-RELEASE"
THEOREM = "THM-M-0414"
BASE_REVISION = "0afbf514f9bd5f339943542106f6b811869fe572"
BASE_TREE = "adbd9c80e360931a3e7c51cae73dda809b5bed65"
EXPRESSION_SHA256 = "de0c201f670ebcc5d4da370f9d5871c131e333652cff7a4dfb903d75e245b005"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "instance.json": "61c5ecdf6c1eb18b38d8ecd4be7b1bcada31ed6a60631ea50b0f9cbc605624df",
    "task-dag.json": "541089998c3273abdda8b7673412ec225ee50f2f5a7b6903ab4c52c4c5bac424",
    "Statement.lean": "7fe066774a7105731721a651a959cf67312763e9ed089be248866dc49c9c486d",
    "statement.json": "f179056b013a84212e917d8cf4df21c653826c83ccb7f8d9f8e0d766fd64d53c",
    "source-statement-crosswalk.md": "34874c8a165f343004fff0d58105a21e15065b5d1931c822355f0254a4103b01",
    "scope-map.md": "1d57006994e25f6e094d3aed89c923ef908431457b319c12bb4514da87c5278e",
    "anchor-audit.json": "5a4684932fd4d8ad0a2cef83f94594c8acd0b49e77b876f4e527c459a1a13b57",
    "obligation-registry.json": "441286a90669b8da023fdf1d4167306df19010c5eec1d371ff0ae072329cdfba",
    "typed-graphs.json": "81df7d3a7871a3a6eb2ec15b98f24d9d432501536c6bd7c7f587e3e8f6da8b86",
    "proof-units.json": "aa8721e5bce677ec448020a3a3870bae2903d38af2a60cd295e70a4a65557f8d",
    "ObligationTree.lean": "a90129d8ce1293e658ff04e09c689142d1fd04fe2a04729572ad7320c766c413",
    "Proof.lean": "8d462642b07638e85c67710ed20782b9f45d3705b40898ae78223151bc1a8afd",
    "proof-receipt.json": "cd97c59c827f08a9e26fa288cba685b5949111006b2594c9e0c1cf94770f44da",
    "Validation.lean": "d4a84f52bda0c357660b0ec59434cafec21179482e450879617a3988d8cd0ed5",
    "validation-spec.json": "ea57fe27b8957ba61e48613bf41ebbcd4593706306948c226b4342b05aa38432",
    "validation-receipt.json": "e18dd4f2b574cea74e71e3e2ba5a26c02d8fa34b2c7ecd70bdf5938117d3b4ed",
    "validation-phase.md": "1edf70a6350a9eb8efc890bb311cd8f73c01837047127a02791ebf1eff858def",
    "check_validation.py": "791d043c827de340b2a9f1703ec69a49e14beeb14ed92650c68c9bff94119e0d",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c698d4d0336848b0042136a7ae84c15ba1496adfefc2925577af273509bf83cc",
    "Docs/Stage1_Blueprint_rev-5.6.md": "a6d5ee1af1191aca7bad0354265d1b56435cc7108bdee3aa81e9d73bc4e644a9",
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
OPEN_OBLIGATIONS = {
    "THM-M-0414-ROOT",
    "THM-M-0414-UFM",
    "THM-M-0414-FINPROD",
    "THM-M-0414-TRUST",
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
            timeout=300,
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
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
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

    target = next(
        (row for row in targets["targets"] if row["theorem_id"] == THEOREM), None
    )
    require(target is not None, "target absent from manifest")
    require(target["execution_rank"] == 69, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned", "target lifecycle drifted")
    require(target["theorem_complete"] is False, "target authority claims completion")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-0414-VALIDATION"),
        None,
    )
    expected_release_item = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 69,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0414-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    require(release_item == expected_release_item, "release execution item drifted")
    require(validation_item is not None and validation_item["state"] == "[_]",
            "validation dependency is not provisional [_]")
    require(validation_item["attempts"] == 1, "validation attempt count drifted")

    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-0414-VALIDATION"
    )
    require(local_release["state"] == local_validation["state"] == "open",
            "local task authority no longer records open validation and release")
    require(local_dag["accepted_states"] == [], "local task authority has accepted state")

    accepted_vector = {"H": "H2", "M": "M3", "R": "R3"}
    require(instance["lifecycle"] == "planned", "instance lifecycle drifted")
    require(instance["root_vector"] == accepted_vector, "accepted vector drifted")
    require(instance["accepted_proof_state"] == [], "instance has accepted proof state")
    require(instance["audit_complete"] is False, "instance claims audit completion")
    require(instance["theorem_complete"] is False, "instance claims theorem completion")
    require(
        statement["canonical_formal_target"]["elaborated_expression_sha256"]
        == EXPRESSION_SHA256,
        "canonical target expression drifted",
    )
    require(statement["theorem_complete"] is False, "statement claims completion")
    require(anchor["audit_result"]["human_debt"] == "H1", "anchor H proposal drifted")
    require(anchor["audit_result"]["readability_debt"] == "R4", "anchor R proposal drifted")
    require(set(graphs["nodes"]) == OPEN_OBLIGATIONS, "typed graph nodes drifted")
    require(
        {row["obligation_id"] for row in registry["obligations"]} == OPEN_OBLIGATIONS,
        "registry denominator drifted",
    )
    require(registry["audit_complete"] is False, "registry claims audit completion")
    require(registry["theorem_complete"] is False, "registry claims theorem completion")
    trust_edge = next(
        edge
        for edge in graphs["trust_graph"]["edges"]
        if edge["from"] == "THM-M-0414-ROOT" and edge["to"] == "THM-M-0414-TRUST"
    )
    require(trust_edge["status"] == "open_release_gate", "release trust edge closed")
    evidence_sources = {edge["from"] for edge in graphs["evidence_graph"]["edges"]}
    require("proof-receipt.json" not in evidence_sources, "old graph unexpectedly reconciled proof")
    require("validation-receipt.json" not in evidence_sources,
            "old graph unexpectedly reconciled validation")

    require(proof["support_state"] == "provisional_worker_selftest",
            "proof receipt support drifted")
    require(proof["result"]["root_closed"] is True, "provisional exact root was lost")
    require(proof["result"]["theorem_complete"] is False,
            "proof receipt claims theorem completion")
    require(validation["support_state"] == "provisional_worker_selftest",
            "validation receipt support drifted")
    require(validation["release_grade"] is False, "validation became release grade")
    require(validation["result"]["provisional_root_kernel_closed"] is True,
            "validation lost provisional root closure")
    require(validation["result"]["accepted_closed_obligation_ids"] == [],
            "validation receipt has accepted obligations")
    for gate in (
        "structured_state_freshness",
        "provenance_closure_gate",
        "tcb_closure_gate",
        "hermetic_release_gate",
        "independent_verification_gate",
    ):
        require(validation["result"][gate] == "fail_closed", f"validation cleared {gate}")
    require(validation["result"]["audit_complete"] is False,
            "validation claims audit completion")
    require(validation["result"]["theorem_complete"] is False,
            "validation claims theorem completion")

    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "release decision identity drifted")
    require(decision["verdict"] == "blocked" and decision["release_accepted"] is False,
            "release decision is not blocked")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    terminal = decision["terminal_decisions"]
    require(terminal == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions are not fail-closed")
    require(decision["root_vector"]["accepted_before"] == ["H2", "M3", "R3"],
            "decision before vector drifted")
    require(decision["root_vector"]["accepted_after"] == ["H2", "M3", "R3"],
            "decision silently changed vector")
    require(decision["first_failed_gate"]["gate_id"] ==
            "S56-10.2-DEPENDENCY-ACCEPTANCE", "first failed gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first failed release gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "reproduction gate drifted")
    require(set(decision["authoritative_open_obligation_ids"]) == OPEN_OBLIGATIONS,
            "open obligation projection drifted")

    require(spec["item_id"] == receipt["item_id"] == ITEM, "recipe/receipt item drifted")
    require(spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "recipe/receipt theorem drifted")
    require(spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
            "release recipe argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied",
            "release recipe policy drifted")
    require(spec["timeout_seconds"] == 300 and spec["expected_exit"] == 0,
            "release recipe resource contract drifted")
    require(set(spec["covered_obligation_ids"]) == OPEN_OBLIGATIONS,
            "release recipe misses a frozen obligation")
    require(receipt["support_state"] == "provisional_worker_selftest",
            "release receipt support drifted")
    require(receipt["release_grade"] is False and receipt["accepted"] is False,
            "release receipt falsely claims acceptance")
    require(receipt["master_accepted"] is False, "worker claims master acceptance")
    require(receipt["dependency"] == decision["dependency"], "dependency ledgers disagree")
    require(receipt["known_failures"] == decision["known_failures"],
            "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "release receipt changed paths drifted")
    for name, expected in receipt["inputs"].items():
        require(digest(ROOT / name) == expected, f"receipt input drifted: {name}")
    require(receipt["authority_inputs"] == AUTHORITY_INPUTS,
            "receipt authority input map drifted")
    require(receipt["decision_id"] == decision["decision_id"],
            "release receipt identifies the wrong decision")
    require(receipt["base_revision"] == decision["base_revision"] == BASE_REVISION,
            "release base revision drifted")
    require(receipt["base_tree"] == decision["base_tree"] == BASE_TREE,
            "release base tree drifted")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "release decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "release specification hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "release checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "release public projection hash drifted")
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
        "PASS THM-M-0414 narrow validation",
        "kernel: exact statement, conditional composition, proof root, and differential root elaborated",
        "trust: checked local and terminal declarations report only propext, Classical.choice, Quot.sound",
        "blocked: THM-M-0414-TRUST lacks complete transitive TCB and compiled-import closure",
        "blocked: shared warm .lake is not cold hermetic replay; same worker is not independent verification",
    ):
        require(fragment in validation_output, f"validation output lost {fragment!r}")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "pinned mathlib worktree changed during replay")

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    normalized_handoff = " ".join(handoff.split())
    for fragment in (
        "`blocked`",
        "`[H2, M3, R3]`",
        "`AUDIT-Z`",
        "`THEOREM-Z`",
        "release_grade=false",
        "accepts no receipt",
    ):
        require(fragment in normalized_handoff, f"handoff omits {fragment!r}")
    durable_changed_paths = CHANGED_PATHS - {".stage1-worker-selftest.json"}
    for relative in durable_changed_paths:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n"), f"missing final newline: {relative}")
        require(b"\r" not in data and b"\x00" not in data,
                f"invalid byte in {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
                f"trailing whitespace in {relative}")

    print("PASS release inputs: target, DAG dependency, receipts, registry, graphs, and hashes agree")
    print("PASS current Lean replay: exact root and differential route; axioms " + str(EXPECTED_AXIOMS))
    print("PASS fail-closed state: lifecycle planned; accepted root H2/M3/R3; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE: THM-M-0414-TRUST is open")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
