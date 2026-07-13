#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1184-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1184"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1184-RELEASE"
THEOREM = "THM-M-1184"
BASE_REVISION = "a7c34044268bf5745e40c011134b447dd1e7cd0f"
BASE_TREE = "7808aabc33d7bad66b0b6ad394f3e5e9835d462b"
VALIDATION_REVISION = "3bb4cb3ae15dff8b48c93242019edec3bf858e48"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "edb496494c51e51e63988c1b32c3fd639f1c911af60db1557a364968ff01cc29"
DENOMINATOR_SHA256 = "4626bc02bb751442b67f842fd1e77a79210940bdd405134d5b14c41f1ff07e27"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
OPEN_STRONG_IDS = [
    "M1184-S-SEPARATION",
    "M1184-C-POTENTIALS",
    "M1184-L-GAP",
    "M1184-W-REVERSE",
    "M1184-T-STRONG",
]
PROVISIONAL_WEAK_IDS = [
    "M1184-C-PRODUCT",
    "M1184-C-CONSTANT",
    "M1184-W-INTEGRATE",
    "M1184-W-ORDER",
    "M1184-T-WEAK",
]
INVENTORY_IDS = [
    "M1184-ROOT",
    "M1184-S-DEFINITIONS",
    "M1184-S-FOUNDATION",
    "M1184-C-PRODUCT",
    "M1184-C-CONSTANT",
    "M1184-W-INTEGRATE",
    "M1184-W-ORDER",
    "M1184-T-WEAK",
    "M1184-S-SEPARATION",
    "M1184-C-POTENTIALS",
    "M1184-L-GAP",
    "M1184-W-REVERSE",
    "M1184-T-STRONG",
    "M1184-T-ASSEMBLE",
    "M1184-X-SOURCE",
    "M1184-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "e9f16cca64ccfd408080d8165c852d8b31fe547c6be121e98a2cba931319fbb2",
    "ObligationTree.lean": "5cf473b0376dc8b49eb498dac0f587a119b72dd9ed366de267c8d599bbfd3f2b",
    "Proof.lean": "84313d9f50b96009a524d3fdf310422496208e99c3359e5c6066773875187d30",
    "Validation.lean": "eb6f6d2a0d28561dc76780e99dcf224e3e527842026b5010412d34ae72435b61",
    "README.md": "796c9685add09073e8bba7771fa37af54f9ddd83ee33ea020083255aa2966ed2",
    "source_statement_crosswalk.md": "386346d047b86cf7f0f997ffc7de1c2bf949fc591d2da4a124beedcfd412633b",
    "intake.json": "bd6f8589672248662a319a55cfc63e5e20e1923087454134749acf1ebe156b5f",
    "statement.json": "8abb0cebb99b319af29bb8cd3fd77919ffa2c83bb162db51ce25a6f98a295a0e",
    "anchor-audit.json": "c37a2248bf810b313bbe34572abf91cf7391ec6c7572f375d3ceaf59681740a5",
    "obligation-registry.json": "0572a71422d4ea4c5cba91e6511ddc49a4dd2144f9e12648a21654351954ee16",
    "typed-graphs.json": "a8367dd3f4cf8d0077700035489c9b894636af500d0fcec1e5f6c1b63e1f3316",
    "proof-receipt.json": "708bbdecd869190f660ab7892cf592f4243d800978f2a3fa30d7abbdf7fa0242",
    "validation-spec.json": "d2f185ffb9f1da243195cb2a68e4129f10f89f747d65f4abe7e033438c4f8958",
    "validation-receipt.json": "e679b9d07b9713929ce38985288a4fb737e118613a5e14cccc5c8d95115f7c31",
    "check_validation.py": "17d55a657bfd77b54341b36579e07aa01bb821c6010c6fe460537a5df6e8b116",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "ec4cd8a897ae20c4d7c940fbb5be8d5a814377baeed1ebf7982d98c1d9eaeac0",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "6d7e70f4f7b6fdbd0ce89c747e9c29a87bf66421493e86c1b34332975a8bc625",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_RELEASE_INPUTS = {
    "ReleaseCheck.lean": "01e67d5e8120af39e5e00e2517c26cb514bcd9497b04d303cd903cd88abb803f",
    "release-spec.json": "c61532ec781af511a53c88ccce49a1d443beada36208489f0e7a51a3765d7496",
    "release-decision.json": "1974c4e8ca1370273cb62cb5d91a5b8d12482c0852a16e938e19a170cd7d12ee",
    "release-validation.md": "d0f86419d89bbfbb0db44bc455431ade482120ca0266e9397ea27966ece18f96",
}


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
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 180,
    check: bool = True,
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
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def source_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_narrow_lean_replay() -> None:
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).stdout.strip())
    version = run([str(lean), "--version"], cwd=LEAN_ROOT).stdout
    assert "4.29.0" in version and LEAN_COMMIT in version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).stdout.strip()
    fixed_env = os.environ.copy()
    fixed_env.update(
        {
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
            "LEAN_PATH": lean_path,
        }
    )
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap network isolation is unavailable"

    with tempfile.TemporaryDirectory(prefix="stage1-m1184-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name)
        (tmp / "home").mkdir()
        for name in (
            "Statement.lean",
            "ObligationTree.lean",
            "Proof.lean",
            "Validation.lean",
            "ReleaseCheck.lean",
        ):
            shutil.copy2(HERE / name, tmp / name)

        def isolated_lean(args: list[str], *, modules: bool = False) -> str:
            module_path = f"{tmp}:{lean_path}" if modules else lean_path
            return run(
                [
                    bwrap,
                    "--ro-bind", "/", "/",
                    "--bind", str(tmp), str(tmp),
                    "--dev", "/dev",
                    "--proc", "/proc",
                    "--unshare-net",
                    "--die-with-parent",
                    "--setenv", "HOME", str(tmp / "home"),
                    "--setenv", "LANG", "C.UTF-8",
                    "--setenv", "LC_ALL", "C.UTF-8",
                    "--setenv", "TZ", "UTC",
                    "--setenv", "LEAN_NUM_THREADS", "1",
                    "--setenv", "LEAN_PATH", module_path,
                    "--chdir", str(tmp),
                    str(lean),
                    "--trust=0",
                    *args,
                ],
                cwd=ROOT,
                env=fixed_env,
            ).stdout

        isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], modules=True
        )
        proof_output = isolated_lean(["-o", "Proof.olean", "Proof.lean"], modules=True)
        validation_output = isolated_lean(
            ["-o", "Validation.olean", "Validation.lean"], modules=True
        )
        release_output = isolated_lean(["ReleaseCheck.lean"], modules=True)

    for declaration in (
        "Stage1Instances.THM_M_1184.root_of_duality_packages",
    ):
        assert reported_axioms(obligation_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_1184.productCoupling",
        "Stage1Instances.THM_M_1184.integral_fst_of_coupling",
        "Stage1Instances.THM_M_1184.integral_snd_of_coupling",
        "Stage1Instances.THM_M_1184.dualValue_le_primalValue",
        "Stage1Instances.THM_M_1184.constantDualPair_nonempty",
        "Stage1Instances.THM_M_1184.objectiveRanges_wellFounded",
        "Stage1Instances.THM_M_1184.weakDuality",
        "Stage1Instances.THM_M_1184.kantorovichDuality_of_reverse",
    ):
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    assert reported_axioms(
        validation_output,
        "Stage1Instances.THM_M_1184.Validation.differentialWeakDuality",
    ) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_1184.ReleaseCheck.localWeakDuality",
        "Stage1Instances.THM_M_1184.ReleaseCheck.differentialWeakDuality",
        "Stage1Instances.THM_M_1184.ReleaseCheck.conditionalRoot",
    ):
        assert reported_axioms(release_output, declaration) == EXPECTED_AXIOMS
    assert release_output.count("Declarations are sorry-free!") == 3
    assert "sorryAx" not in release_output


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    intake = load(HERE / "intake.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 169
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1184-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 169,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1184-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1184-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1184-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    for name, expected in receipt["inputs"].items():
        path = LEAN_ROOT / name if name in {"lean-toolchain", "lake-manifest.json"} else HERE / name
        assert sha256(path) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == "planned"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == ["H3", "M2", "R4"]
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["accepted_closed_obligation_ids"] == []
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["remaining_mathematical_root_cut_set"] == OPEN_STRONG_IDS

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1184-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "root_vector": ["H3", "M2", "R4"],
        "reason": "Both exact inequality packages and all release overlays remain unaccepted.",
    }
    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False

    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_WEAK_IDS
    assert proof["remaining_root_cut_set"] == OPEN_STRONG_IDS
    assert proof["result"]["weak_package_kernel_closed"] is True
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_vector"] == ["H3", "M2", "R4"]
    assert validation["result"]["remaining_root_cut_set"] == OPEN_STRONG_IDS
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["result"]["complete_transitive_provenance_and_tcb"] == "fail_closed"
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_verification_gate"] == "fail_closed"

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H3", "M2", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_theorem_gate"]["gate_id"] == "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    assert result["first_failed_release_assurance_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert result["remaining_mathematical_root_cut_set"] == OPEN_STRONG_IDS

    reconciliation = decision["evidence_reconciliation"]
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
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["historical_validation_recipe_replay"] == (
        "stale_at_current_head_and_preserved_as_nonrelease_historical_evidence"
    )

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean", "ReleaseCheck.lean",
        )
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""

    old_recipe = load(HERE / "validation-spec.json")
    assert old_recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    old_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_REVISION}"' in old_checker
    assert VALIDATION_REVISION != BASE_REVISION
    stale = run(old_recipe["argv"], check=False)
    assert stale.returncode != 0
    assert "AssertionError" in stale.stdout

    assert_narrow_lean_replay()

    print("PASS release inputs: manifest, DAG, receipts, frozen registry, graphs, and hashes agree")
    print("PASS narrow Lean replay: statement, conditional composition, weak proof, and differential weak proof are sorry-free at --trust=0")
    print("PASS fail-closed reconciliation: root H3/M2/R4 remains open; accepted receipts=[]; AUDIT-Z=false; THEOREM-Z=false")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted")
    print("BLOCKED exact root: reverse-duality cut remains open; stale validation recipe and every release-assurance gate stay visible")
    print("verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
