#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0651-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0651"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0651-RELEASE"
THEOREM = "THM-M-0651"
BASE_REVISION = "51c2828e82ffb19860830f78b771f80e13ad7dff"
BASE_TREE = "4655b8b40829513de6fb5661344b33fc7cd17cd1"
VALIDATION_BASE = "9254a0ec0d0c71b346ae15a911721409e3ab3139"
EXPRESSION_SHA256 = "789c281a89ba5947476cb2189ae3e216de0eeaa0b5d016549489d8c1553d8c43"
DENOMINATOR_SHA256 = "e739a3f3ee963205d34582d0879d767e928e26670f557de0871addcc176f3805"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
PYTHON = Path("/usr/bin/python3")
GIT = Path("/usr/bin/git")
ROOT_VECTOR = ["H1", "M4", "R3"]
OPEN_ROOT_CUT = [
    "M0651-L-ENUM",
    "M0651-L-DENSE",
    "M0651-L-HENKIN",
    "M0651-L-OMIT",
]
PARTIAL_IDS = ["M0651-L-ENUM", "M0651-L-DENSE", "M0651-B-ARITY0"]
INVENTORY_IDS = [
    "M0651-ROOT",
    "M0651-S-EXACT",
    "M0651-L-ENUM",
    "M0651-L-DENSE",
    "M0651-L-HENKIN",
    "M0651-L-OMIT",
    "M0651-T-ASSEMBLE",
    "M0651-B-ARITY0",
    "M0651-X-ANCHOR",
    "M0651-X-SOURCE",
    "M0651-X-TCB",
]
EXPECTED_INPUTS = {
    "instance.json": "a4829af9d1331524e186d3e54ad90dfdfead7fda371e85ad345c956406c6a945",
    "Statement.lean": "39b09536792acdd585eb62dc09917eca50eff8717211a764bca58d96645d38ea",
    "ObligationTree.lean": "2317873fba80bc681a10267eaba79f13828a35f156950168a388b565f9c8c2df",
    "ProofLemmas.lean": "47b5cb564dba6793cc10b3b9cf3cd50cd565441a8b2cd97cc346462928e089dc",
    "Validation.lean": "ab820ad99f8c5fb6cc479db9b51215635155b5eb8bf1b85931da97105d7ee121",
    "statement.json": "cf4e441e06d3309f010c975b2da9efea08ed805a66627797b7400bae6e503c5b",
    "anchor-audit.json": "17fc3419e05444401a36b0146562a552179c663c6a92606f1a05add44b21111c",
    "obligation-registry.json": "9a87b090025b80fde991e80c2eec07a9f67ae84a269802288d30c7ec572d142f",
    "typed-graphs.json": "7ae5e1d811de7c88799746b29a6d89d277f0954ab1b131c499f807cb47548900",
    "proof-receipt.json": "92501ac511409d61a3303884b0d25ba4024fdaf936eb38855a85866644113ee2",
    "proof-blocker.json": "3e937b90d7746c5b13afb72ab953c729a7041a725a2266649ebba86f49b48f80",
    "validation-spec.json": "20aca0002013580471feeba96f87fb56cd932a1acbba16c2a3cb8f71f3887e58",
    "validation-receipt.json": "2b60783463f1ea127f7bb36d9ead24204d6baa9ab4798735686612f9c5246c46",
    "validation-phase.md": "78345101ec585b7e6b87b63228336f020aac9a3370a13dcc99f9325a62cc67a8",
    "check_validation.py": "a5203246340d90c8f9e337151de5e440947cc713525f5cb78a99c4ab46768dab",
    "check_statement.py": "85a2c4896fb40fe87353d2000a5c9c7e2ab1c9a2182a8fa901cbd183683fc978",
    "check_obligation_tree.py": "9a71a865cd55045f999dd29b8964c0a6af60981130d1457ea5d1946492df08fa",
    "check_proof.sh": "bdf2e00cdfa7a632c6fb36e3b0597330366034130d1bb4d32b08a146743f0d95",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "7d07d22e5b04fa9f630545d72f0e3adde1de3012ba517fc4831820a75458c8da",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "e7c5ba72eaeb0010eb43f348ca6489c29a9dd99d503a9c9c8e9982911c92036c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_OUTPUTS = {
    "release-spec.json": "65020b1d56511a76d3ed49b3ab95155aaf079018c2901f5047a1a5d322ad8127",
    "release-decision.json": "f769594acc47bd49fb21114728ae6b3a23fa439fe6483aebb4b1009e1b40a4f1",
    "release-phase.md": "241ee96376639e7c27635787c0ab7aaa704b87929ab49e2bb197544b0b8e9a4c",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional composition, and eight partial bodies checked",
    "BLOCKED dependency acceptance and freshness: validation is provisional, unaccepted, and snapshot-stale",
    "BLOCKED exact root: H1/M4/R3 unchanged; zero frozen obligations accepted closed",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600,
    env: dict[str, str] | None = None,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run([str(GIT), *args], cwd=cwd, timeout=60).strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
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
            quoted = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not quoted
    return "".join(output)


def check_historical_validation(validation: dict) -> None:
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    assert validation["root_vector_before"] == validation["root_vector_after"] == {
        "H": "H1", "M": "M4", "R": "R3"
    }
    result = validation["result"]
    assert result["supported_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert validation["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert validation["independent_validation"]["decision"] == "fail_closed"
    checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in checker
    assert VALIDATION_BASE != BASE_REVISION


def narrow_replay() -> None:
    launcher = Path.home() / ".elan" / "bin" / "lake"
    assert sha256(launcher) == ELAN_LAUNCHER_SHA256
    fixed_env = {
        "HOME": str(Path.home()),
        "PATH": f"{launcher.parent}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean = Path(run(
        [str(launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env
    ).strip())
    lake = Path(run(
        [str(launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env
    ).strip())
    assert sha256(lake) == LAKE_SHA256 and sha256(lean) == LEAN_SHA256
    assert "98dc76e3c0a9b856c9b98726b713fb04fab16740" in run(
        [str(lean), "--version"], env=fixed_env
    )
    statement_output = run(
        [str(PYTHON), f"Stage1_Instances/{THEOREM}/check_statement.py"],
        timeout=180,
        env=fixed_env,
    )
    statement = json.loads(statement_output)
    assert statement["expression_sha256"] == EXPRESSION_SHA256
    assert statement["killed_mutations"] == [
        "MutationProbes.WithoutNonprincipality",
        "MutationProbes.OneTuplePerType",
    ]
    tree_output = run(
        [str(PYTHON), f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
        timeout=180,
        env=fixed_env,
    )
    assert "11 obligations, 21 typed edges" in tree_output
    assert "root remains open at M4" in tree_output
    lean_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).strip()
    with tempfile.TemporaryDirectory(prefix="stage1-m0651-release-", dir="/tmp") as name:
        tmp = Path(name)
        for source in ("Statement.lean", "ObligationTree.lean", "ProofLemmas.lean"):
            shutil.copy2(HERE / source, tmp / source)
        outputs: dict[str, str] = {}
        for module in ("Statement", "ObligationTree", "ProofLemmas"):
            module_path = lean_path if module == "Statement" else f"{tmp}:{lean_path}"
            output = run(
                [
                    str(lean), "--trust=0", "-t0", "--root", str(tmp),
                    "-o", str(tmp / f"{module}.olean"), str(tmp / f"{module}.lean"),
                ],
                cwd=tmp,
                timeout=420,
                env={
                    "HOME": str(tmp), "TMPDIR": str(tmp), "LANG": "C.UTF-8",
                    "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
                    "LEAN_PATH": module_path,
                },
            )
            assert (tmp / f"{module}.olean").is_file()
            outputs[module] = output
    proof_output = "\n".join(outputs.values())
    assert "'Stage1Instances.THM_M_0651.ObligationTree.root_compose' depends on axioms: [propext, Quot.sound]" in proof_output
    for declaration in (
        "countable_symbols",
        "countable_finite_arity_syntax",
        "exists_surjective_formula_schedule",
        "countable_avoidance_requirements",
        "zero_arity_formula_requirement_inhabited",
        "zero_arity_tuple_requirement_inhabited",
        "exists_surjective_avoidance_schedule",
        "exists_consistent_avoidance_extension",
    ):
        assert f"Stage1Instances.THM_M_0651.ProofLemmas.{declaration}" in proof_output
    assert "sorryAx" not in proof_output and "error:" not in proof_output.lower()


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")
    assert sha256(PYTHON) == PYTHON_SHA256 and sha256(GIT) == GIT_SHA256

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 697 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 697,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0651-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0651-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in EXPECTED_RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, f"release output drifted: {name}"

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0651-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_debt"] == "M4"
    assert boundary["remaining_root_cut_set"] == OPEN_ROOT_CUT
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0651-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == ROOT_VECTOR

    assert proof["accepted"] is False
    assert proof["supported_obligation_ids"] == proof["accepted_closed_obligation_ids"] == []
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["result"]["root_kernel_closed"] is proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert blocker["architecture_issue"].startswith("The frozen AvoidanceInterface quantifies over every Candidate")
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    check_historical_validation(validation)

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0651-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["root_vector"] == {"before": ROOT_VECTOR, "after": ROOT_VECTOR}
    terminal = decision["terminal_decisions"]
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert terminal["release_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE-AND-FRESH-REPLAY"
    )
    assert decision["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-READABILITY-RECONCILIATION"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert decision["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["remaining_root_cut_set"] == OPEN_ROOT_CUT
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["validated_partial_progress_toward_obligations"] == PARTIAL_IDS
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    recipe = spec["recipe"]
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["depends_on"] == ["S56-M-0651-VALIDATION"]
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == INVENTORY_IDS
    assert recipe["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    covered_declarations = recipe["covered_declarations"]
    assert len(covered_declarations) == 11 == len(set(covered_declarations))
    assert covered_declarations[0] == "Stage1Instances.THM_M_0651.OmittingTypesTarget"
    assert covered_declarations[2] == "Stage1Instances.THM_M_0651.ObligationTree.root_compose"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0651-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["review_due"] == "before master acceptance and after any invalidation input changes"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["root_vector_before"] == result["root_vector_after"] == ROOT_VECTOR
    assert result["accepted_closed_obligations"] == []
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE-AND-FRESH-REPLAY"
    assert result["first_failed_audit_gate"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-READABILITY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"] == "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    assert result["first_failed_release_specific_gate"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert receipt["dependency_receipt"]["receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["freshness"] == {
        "support_state": "provisional_nonrelease_worker_evidence",
        "supersession_state": "current_worker_proposal",
        "revocation_state": "unaccepted",
        "incident_path": "Revoke this receipt and rerun release reconciliation after any invalidation input changes.",
    }
    assert len(receipt["invalidation_inputs"]) == 7

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    mathlib = lake_link / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == LEAN_SHA256
    assert environment["lake_executable_sha256"] == LAKE_SHA256
    assert environment["elan_launcher_sha256"] == ELAN_LAUNCHER_SHA256
    assert environment["python_executable_sha256"] == PYTHON_SHA256
    assert environment["git_executable_sha256"] == GIT_SHA256

    lean_sources = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "ProofLemmas.lean", "Validation.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(lean_sources) is None
    narrow_replay()

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in (
        "release-spec.json", "release-decision.json", "release-receipt.json",
        "release-phase.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
