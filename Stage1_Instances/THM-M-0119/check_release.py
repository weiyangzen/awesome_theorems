#!/usr/bin/env python3
"""Fail-closed reconciliation and narrow replay for S56-M-0119-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


if not __debug__:
    raise RuntimeError("release checking requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0119"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0119-RELEASE"
THEOREM = "THM-M-0119"
BASE_REVISION = "50db6284742415b7da294d323c820bf4b224711d"
BASE_TREE = "bb477aa021efaf69c84ee3a98f486f4ba407bae2"
ROOT_VECTOR = ["H4", "M3", "R4"]
FROZEN_CUT = [
    "M0119-X-APIS",
    "M0119-N-RESOLUTION",
    "M0119-L-SMOOTH",
    "M0119-C-PUSH",
]
INVALIDATION_BOUNDARY = [
    "S56-M-0119-STATEMENT",
    "M0119-S-DATA",
    "M0119-S-HYP",
    "M0119-ROOT",
]
EXPECTED_OUTPUT_HASHES = {
    "statement": "e7402bc1bb4f1bc6255436b7d7635869788000c47450782fa75cf8272dac644b",
    "obligation": "f2ba3ac92c0cdff043432949d1445d9b85aa8114a413fa9392b7982e801c7f5b",
    "proof": "c6b29f07f5d9175a9aa2439c336d176a5cb200801d6a2769f0fa01754003eb42",
    "validation": "98f89fafdfe3f9c0c604c2f22e0a3909204b3127eaf508a1f3f1e2a004cd58a8",
}
EXPECTED_OLEAN_HASH = "01729724a41a4bee420c56a7f3fbcd0d4dd681ba039a7633d3739c2239919e0b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SUMMARY_LINES = [
    "PASS S56-M-0119-RELEASE reconciliation",
    "PASS current trust-zero Lean replay: exact statement, conditional composition, Int countermodel, and no-Proof-import ZMod 2 countermodel",
    "verdict=blocked lifecycle=planned root_vector=H4/M3/R4",
    "AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0",
    "first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE",
    "first_failed_theorem_gate=S56-5.1-EXACT-TARGET-CONSISTENCY",
    "first_failed_release_gate=S56-10.6-HERMETIC-COLD-EMPTY-CACHE",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
]


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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
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
    assert result.returncode == 0, f"command failed: {argv!r}\n{result.stdout}"
    return result


def git(*args: str) -> str:
    return run(["/usr/bin/git", *args]).stdout.strip()


def source_without_comments_or_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth == 0 and not in_string and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif not in_string and source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string and source[index] == "\\" and index + 1 < len(source):
            output.extend("  ")
            index += 2
        elif in_string:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, declaration
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def lean_replay() -> None:
    base_env = {
        "HOME": os.environ.get("HOME", str(Path.home())),
        "PATH": f"{os.environ.get('HOME', str(Path.home()))}/.elan/bin:/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=base_env
    ).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="stage1-m0119-release-", dir="/tmp") as name:
        tmp = Path(name)
        for source_name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / source_name).write_bytes((HERE / source_name).read_bytes())

        outputs: dict[str, str] = {}
        commands = (
            ("statement", "Statement.lean", lean_path, True),
            ("obligation", "ObligationTree.lean", lean_path, False),
            ("proof", "Proof.lean", f"{tmp}:{lean_path}", False),
            ("validation", "Validation.lean", f"{tmp}:{lean_path}", False),
        )
        for key, source_name, module_path, emit_object in commands:
            argv = ["lake", "env", "lean", "--trust=0", "-t0", f"--root={tmp}"]
            if emit_object:
                argv.extend(["-o", str(tmp / "Statement.olean")])
            argv.append(str(tmp / source_name))
            env = {**base_env, "LEAN_PATH": module_path}
            outputs[key] = run(argv, cwd=LEAN_ROOT, env=env).stdout

        actual = {
            key: hashlib.sha256(value.encode()).hexdigest()
            for key, value in outputs.items()
        }
        assert actual == EXPECTED_OUTPUT_HASHES
        assert sha256(tmp / "Statement.olean") == EXPECTED_OLEAN_HASH
        proof_decl = "Stage1Instances.THMM0119.not_kawamataViehwegVanishingTarget"
        validation_decl = (
            "Stage1Instances.THMM0119.Validation.independent_root_countermodel"
        )
        assert reported_axioms(outputs["proof"], proof_decl) == EXPECTED_AXIOMS
        assert reported_axioms(outputs["validation"], validation_decl) == EXPECTED_AXIOMS
        for declaration in (
            "Stage1Instances.THMM0119.ObligationTree.positive_degrees_compose",
            "Stage1Instances.THMM0119.ObligationTree.implication_compose",
        ):
            assert f"'{declaration}' does not depend on any axioms" in outputs["obligation"]
        assert "Declarations are sorry-free!" in outputs["validation"]
        assert "VALIDATION_CLOSURE declarations=15934 modules=589" in outputs["validation"]
        assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
        assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    decision = load(HERE / "release-decision.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    proof = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 38
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0119-VALIDATION"
    )
    assert release_item["state"] == "[ ]" and release_item["depends_on"] == [validation_item["id"]]
    assert validation_item["state"] == "[_]"
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_release = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in task_dag["tasks"] if row["id"] == validation_item["id"]
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_release["accepted_receipt_ids"] == local_validation["accepted_receipt_ids"] == []
    assert task_dag["accepted_state"] == []

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["intent"] == "release" and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]"
    assert decision["accepted"] is decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    for relative, expected in decision["authority_inputs"].items():
        assert sha256(ROOT / relative) == expected, relative
    for relative, expected in decision["reconciled_inputs"].items():
        assert sha256(ROOT / relative if relative.startswith("Formalizations/") else HERE / relative) == expected, relative

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_support_state"] == validation["support_state"]
    assert dependency["receipt_accepted"] is validation["accepted"] is False
    assert dependency["receipt_release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False

    assurance = instance["assurance"]
    assert assurance["human_debt"] == "H4"
    assert assurance["machine_debt"] == "M3"
    assert assurance["readability_debt"] == "R4"
    assert assurance["accepted_evidence_ids"] == []
    assert assurance["audit_complete"] is assurance["theorem_complete"] is False
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    terminal = decision["terminal_decisions"]
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert terminal["release_accepted"] is False

    boundary = graphs["closure_boundary"]
    assert registry["root_obligation_id"] == "M0119-ROOT"
    assert boundary["closed_obligations"] == []
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["remaining_root_cut_set"] == FROZEN_CUT
    assert boundary["theorem_complete"] is False
    assert decision["frozen_graph_remaining_root_cut_set"] == FROZEN_CUT
    assert decision["proposed_invalidation_and_retry_boundary"] == INVALIDATION_BOUNDARY
    assert proof["verdict"] == "blocked" and proof["canonical_target_refuted"] is True
    assert proof["root_closed"] is proof["theorem_complete"] is False
    result = validation["result"]
    assert result["validated_blocker_obligation_ids"] == [
        "M0119-S-DATA", "M0119-S-HYP", "M0119-ROOT"
    ]
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["positive_exact_root_gate"] == "fail_closed_checked_countermodels"

    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_theorem_gate"]["gate_id"] == "S56-5.1-EXACT-TARGET-CONSISTENCY"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["positive_exact_root_kernel_closure"] == "failed_checked_countermodels"
    for key in (
        "audit_inventory_reconciliation",
        "accepted_foundation_and_complete_provenance_tcb_closure",
        "immutable_current_snapshot_receipt",
        "hermetic_cold_offline_reproduction",
        "sbom_and_license_closure",
        "independent_release_verification",
        "protected_adversarial_ci",
        "deterministic_signed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] == "missing", key
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "statement fields",
        "kernel closure of the repaired exact root",
        "AUDIT-Z",
        "H0 primary-source",
        "R0 node-by-node",
        "foundation and axiom",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "two signed attestations",
        "minimal release verifier",
        "mutation, differential, and metamorphic",
        "deterministic signed content-addressed release bundle",
    ):
        assert fragment in cut, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_or_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in validation_source
    assert "ZMod 2" in validation_source
    lean_replay()

    for relative in CHANGED_PATHS[1:]:
        assert_text_hygiene(ROOT / relative)
    if args.worker_packet is not None:
        packet = load(args.worker_packet)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
        assert packet["output_summary"] == SUMMARY_LINES
        assert packet["known_failures"] == decision["known_failures"]
        assert_text_hygiene(args.worker_packet)
        actual_changed = {
            line[3:]
            for line in git("status", "--short", "--untracked-files=all").splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changed == set(CHANGED_PATHS), actual_changed

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
