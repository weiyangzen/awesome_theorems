#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0814-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0814"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0814-RELEASE"
THEOREM = "THM-M-0814"
BASE_REVISION = "118d66d1986768cd9a00e661ccf6447c26a53efb"
BASE_TREE = "e31babc8fcb7426673e5d6c0a4a884af2cd737e8"
EXPRESSION_SHA256 = "f9fc7813f437ebcd4b2b7327373dd76134d651c1624d2a06f689e84ec571a21e"
DENOMINATOR_SHA256 = "f0ff554fe8facfa66bbdcbe9f036f7de20ebbe738b1d2cc9b4c06a899d673d7b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BASH_EXECUTABLE_SHA256 = "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
LEAN_MODULES = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
MACHINE_CUT = ["M0814-L-MAX-ATTAIN", "M0814-T-EQUAL-CUT"]
PROVISIONAL_IDS = ["M0814-L-WEAK-DUALITY"]
PARTIAL_IDS = ["M0814-B-NO-CHAIN"]
CONDITIONAL_IDS = ["M0814-T-CUT-CERT", "M0814-T-ASSEMBLE"]
INVENTORY_IDS = [
    "M0814-ROOT", "M0814-S-TARGET", "M0814-S-CHAIN", "M0814-S-FLOW-CUT",
    "M0814-S-BOUNDARY", "M0814-S-TRANSPORT", "M0814-S-FOUNDATION",
    "M0814-N-CHAIN-ENUM", "M0814-N-FLOW-COORD", "M0814-B-NO-CHAIN",
    "M0814-B-HAS-CHAIN", "M0814-B-MERGE", "M0814-C-FEASIBLE-POLYTOPE",
    "M0814-L-MAX-ATTAIN", "M0814-L-MAX-CONVEX", "M0814-C-SATURATED-CORE",
    "M0814-L-S-DISCONNECTS", "M0814-L-REROUTE-BASIC", "M0814-L-S-ORIENTATION",
    "M0814-C-LEFT-ARCS", "M0814-L-L-DISCONNECTS", "M0814-L-L-AT-MOST-ONE",
    "M0814-L-L-EXACTLY-ONE", "M0814-L-WEAK-DUALITY", "M0814-L-COUNT-ONCE",
    "M0814-T-EQUAL-CUT", "M0814-T-CUT-CERT", "M0814-T-ASSEMBLE",
    "M0814-X-SOURCE", "M0814-X-PROVENANCE", "M0814-X-TRUST",
    "M0814-X-READABLE", "M0814-X-WORKFLOW",
]
KERNEL_REPLAYED_IDS = [
    "M0814-S-TARGET", "M0814-B-NO-CHAIN", "M0814-L-WEAK-DUALITY",
    "M0814-T-CUT-CERT", "M0814-T-ASSEMBLE",
]
AXIOM_DECLARATIONS = {
    "Statement.lean": ("maxFlowMinCutTarget_iff_expanded",),
    "ObligationTree.lean": ("cutCertificate_compose", "compose_root", "root_of_terminal"),
    "Proof.lean": (
        "weakDuality_proof", "noChain_case", "cutCertificate_of_equalCut",
        "root_of_maximalFlowAttainment_and_equalCut",
    ),
    "Validation.lean": (
        "weakDuality_proof", "noChain_case", "cutCertificate_of_equalCut",
        "root_of_maximalFlowAttainment_and_equalCut",
    ),
}
EXPECTED_INPUTS = {
    "Statement.lean": "e2493ef46f9bdd5c8d0b30069efaf27b7ad0f69781d4c4c7317b94a63a06755b",
    "ObligationTree.lean": "bca977e826adfc22fe9e3b3fe583445ff42cfe57f66da706d2827a2f1d62a69d",
    "Proof.lean": "b7f4d1e28d4e9add0ca9f21943bb104b1dd450106a217b9b8298013afe250e76",
    "Validation.lean": "1d2412bbf5e056c6a34865e2b66b5d355ee1614d1b9870c7bf4d181153fbdf36",
    "instance.json": "726dc6f09f476c7060a90ae449e591693a7bbb2e10da4893e525a61e7fafaf8f",
    "task-dag.json": "b68cd92d256cf50cd6780f3536763543f8f8ea2548a5c790da843512516f9644",
    "statement.json": "ed7b955159e8bc250fe051cc69ad5b067c7f0901a3a401e0ae4890414adda4b0",
    "anchor-audit.json": "4add5128314497037bd14a8cb009edc94f66e78b8a690eb43632477a5e8d191a",
    "obligation-registry.json": "1b771d946118867c69834923a5e107934526d6dd638dd78e31fac2cb6094e63e",
    "typed-graphs.json": "d970a886c6f727962d7dfb3e37d6b9475125d48d7d786f9e9f91b583b201e2fc",
    "source-statement-crosswalk.md": "a179f8cea8cf7578092f95f15579db8a5fca9bd9f3b359eda5271d24778d9659",
    "intake-receipt.json": "f23f12c0421cdb89232e3453a885a9d6dcfc7e91e0879f329d173109bae50f61",
    "statement-receipt.json": "5703ba64b8d52390f77e4afa6840ad7261d842a24563bbfedefc9f652b1a165d",
    "anchor-audit-receipt.json": "8de30be5fadfe488a31b1907a6b4ac9c94684c86db79dd0df8cb35e5a381b72d",
    "obligation-tree-receipt.json": "90ae69221fa31612f5818bb705ecda1492282398dcfcd875a7f02829e737227f",
    "proof-receipt.json": "d91e637c09b92f21f92d8005d004014912eb1f04ff9fc10ca7a2643291825c8a",
    "proof-blocker.json": "6e4a2aed3868fce77f1368a678b87afcd0bc21346cc62d062c7282de1549ce23",
    "validation-spec.json": "03f6a2cfc8c717d34671baf217f938909240c28e3b0246477d632d3d187dc1f0",
    "validation-receipt.json": "f24c5733601161c44e83b5725403f39d6921487ce8aa66d8755bb397e0a67802",
    "validation-blocker.json": "4b85c1a2984a505a8e4dc24f77bcdcfcd961d4793130f8cfcb5c49ff53741213",
    "check_validation.py": "fb6d758c521109a84d77bcda9ba8b23c34338732b92002f151ef2437214777d9",
    "validation-phase.md": "e91c641864ec2a566ae1af2ef9f83d5848bfa966f5023dce1c591fd7fe42796f",
    "release-spec.json": "25ce73fe735c98508dbb54be17312a6202812a53f6769a1543a78ab4b4b5325f",
    "release-decision.json": "519e0d360ddfb49b79429a036ce5fc18c1fd6a01f9dfc4ee55b565aac6ec34b3",
    "release-validation.md": "9b09c32369543da24f57775eff878156829ee40e94e4429bdb61361b1a253cc2",
}
EXPECTED_REPO_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "fe817cc9dd778a4126a999ca75ffe36f0389162db5c2fe28d747348f8aabaf8b",
    "Docs/Stage1_Blueprint_rev-5.6.md": "2f08864346f8f074318ea8d27d6076e0a473b4045387796504fca28860750d52",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SUMMARY_LINES = [
    "PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree",
    "PASS narrow Lean replay: exact statement and conditional declarations are sorry-free at trust zero with only allowed axioms",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted obligations and receipts remain empty",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED exact root and release assurance: attainment, equal cut, H0/R0, TCB/SBOM, clean cold/offline, independent verifier, and bundle gates remain open",
    "verdict=blocked audit_complete=false theorem_complete=false",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


if not __debug__ or sys.flags.optimize:
    raise SystemExit("release-decision: FAIL: Python assertions are disabled")


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).strip()


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.escape(f".{declaration}' depends on axioms: [") + r"(.*?)]"
    matches = re.findall(pattern, output, flags=re.DOTALL)
    assert len(matches) == 1, (declaration, len(matches))
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def replay_lean(lean: Path, lean_path: str, bwrap: Path) -> dict[str, str]:
    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m0814-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_MODULES:
            shutil.copy2(HERE / name, tmp / name)
        home = tmp / "home"
        home.mkdir()
        sandbox = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(home), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def replay(name: str, include_local: bool) -> str:
            module_path = f"{tmp}:{lean_path}" if include_local else lean_path
            return run(
                sandbox + [
                    "--setenv", "LEAN_PATH", module_path, str(lean), "--root", str(tmp),
                    "--trust=0", "-t0", "-o", str(tmp / Path(name).with_suffix(".olean")),
                    str(tmp / name),
                ],
                timeout=300,
            )

        outputs["Statement.lean"] = replay("Statement.lean", False)
        outputs["ObligationTree.lean"] = replay("ObligationTree.lean", True)
        outputs["Proof.lean"] = replay("Proof.lean", True)
        outputs["Validation.lean"] = replay("Validation.lean", True)
        for name in LEAN_MODULES:
            assert (tmp / Path(name).with_suffix(".olean")).is_file()
    return outputs


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1373 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1373,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0814-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0814-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-0814-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0814-VALIDATION"]
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
        assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/{name}"] == expected
    for relative, expected in EXPECTED_REPO_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"repository input drifted: {relative}"
        assert receipt["input_bindings"][relative] == expected
    assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/check_release.py"] == sha256(
        HERE / "check_release.py"
    )
    assert decision["reconciled_inputs"] == {
        name: expected for name, expected in EXPECTED_INPUTS.items()
        if name not in {"intake-receipt.json", "statement-receipt.json", "anchor-audit-receipt.json",
                        "obligation-tree-receipt.json", "check_validation.py", "validation-phase.md",
                        "release-decision.json", "release-validation.md"}
    }

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0814.MaxFlowMinCutTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert anchor["audit_result"]["exact_proof_candidate_located"] is False
    assert registry["root_obligation_id"] == "M0814-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["result"]["root_kernel_closed"] is False
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["remaining_machine_root_cut_set"] == MACHINE_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["provisionally_validated_obligation_ids"] == PROVISIONAL_IDS
    assert validation["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert validation["conditional_composition_ids"] == CONDITIONAL_IDS
    assert validation["accepted_closed_obligation_ids"] == validation["accepted_receipt_ids"] == []
    assert validation["remaining_machine_root_cut_set"] == MACHINE_CUT
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation_blocker["remaining_machine_root_cut_set"] == MACHINE_CUT
    assert validation_blocker["root_closed"] is validation_blocker["theorem_complete"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["intent"] == "release" and decision["proposed_state"] == "[_]"
    assert decision["release_grade"] is decision["release_accepted"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert decision["root_vector_before"] == decision["root_vector_after"] == vector
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0814-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_accepted"] is dependency["receipt_release_grade"] is False
    assert dependency["master_accepted"] is False
    terminal = decision["terminal_decisions"]
    assert terminal["verdict"] == "blocked"
    assert terminal["root_vector_before"] == terminal["root_vector_after"] == vector
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0814-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "proof.M0814-L-MAX-ATTAIN"
    assert decision["next_failed_theorem_gate"]["gate_id"] == "proof.M0814-T-EQUAL-CUT"
    assert decision["remaining_machine_root_cut_set"] == MACHINE_CUT
    expected_cut_scope = (
        "Provisional top-spine exact-interface cut exposed by the proof and validation "
        "proposals; this is not the frozen typed graph's unreconciled proof_leaf_cut_set."
    )
    assert decision["remaining_machine_root_cut_set_scope"] == expected_cut_scope
    assert decision["frozen_graph_proof_leaf_cut_set"] == boundary["proof_leaf_cut_set"]
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0814-VALIDATION", "M0814-L-MAX-ATTAIN", "M0814-T-EQUAL-CUT",
        "H0", "R0", "AUDIT-Z", "empty-cache", "two signed", "minimal release verifier",
        "deterministic", "THEOREM-Z",
    ):
        assert fragment in cut, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == decision["release_recipe_id"]
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["env_allowlist"] == {
        "PATH": "runner-provided only for hash-checked Lake, Bubblewrap, and Git discovery",
        "HOME": "runner-provided only for the pinned Elan toolchain selected by Lake",
    }
    assert spec["network_policy"] == "denied"
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["kernel_replayed_obligation_ids"] == KERNEL_REPLAYED_IDS

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["decision_id"] == decision["decision_id"]
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == KERNEL_REPLAYED_IDS
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert set(result["observed_axioms"]) == ALLOWED_AXIOMS
    assert result["conditional_root_kernel_replay"] is True
    assert result["premise_free_root_kernel_closed"] is result["accepted_root_closed"] is False
    assert result["accepted_receipt_ids"] == result["accepted_closed_obligations"] == []
    assert result["remaining_machine_root_cut_set"] == MACHINE_CUT
    assert result["remaining_machine_root_cut_set_scope"] == expected_cut_scope
    assert result["frozen_graph_proof_leaf_cut_set"] == boundary["proof_leaf_cut_set"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(
            ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
        ).hexdigest(),
        "expected_line_count": 6,
        "exit_code": 0,
    }
    assert receipt["recipe"]["recipe_id"] == spec["recipe_id"]
    for key in (
        "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_enforcement", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "kernel_replayed_obligation_ids", "covered_declarations", "covered_decisions",
    ):
        assert receipt["recipe"][key] == spec[key], key

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac|oracle|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    lake_name = shutil.which("lake")
    bwrap_name = shutil.which("bwrap")
    git_name = shutil.which("git")
    assert lake_name is not None and bwrap_name is not None and git_name is not None
    lake = Path(lake_name).resolve()
    bwrap = Path(bwrap_name).resolve()
    lean = Path(run([str(lake), "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lean_path = run(
        ["/usr/bin/env", "-u", "LEAN_PATH", str(lake), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT, timeout=60,
    ).strip()
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_EXECUTABLE_SHA256
    assert sha256(Path(sys.executable).resolve()) == PYTHON_EXECUTABLE_SHA256
    assert sha256(Path(git_name).resolve()) == GIT_EXECUTABLE_SHA256
    assert sha256(Path("/usr/bin/bash")) == BASH_EXECUTABLE_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=30)
    outputs = replay_lean(lean, lean_path, bwrap)
    report_count = 0
    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[module], declaration) == ALLOWED_AXIOMS
            report_count += 1
    assert report_count == 12
    validation_output = outputs["Validation.lean"]
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE unexpected_bodyless=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", combined)

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == [row["argv"] for row in receipt["commands_and_results"]]
    assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (
        HERE / "release-decision.json", HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        public_text = path.read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
