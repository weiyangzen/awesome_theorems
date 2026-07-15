#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0527-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0527"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0527-RELEASE"
THEOREM = "THM-M-0527"
BASE_REVISION = "a9274bb02f984e5c74d2c97339044c6db8eb14f9"
BASE_TREE = "c72a5af07dd4ab3f7088c516c74235e794a6de09"
VALIDATION_BASE = "874745ff39044c1e45ed30a04111d3d84aa0e348"
EXPRESSION_SHA256 = "4c7a7d4c54edb4a2d46091dda31f20a26664f005b20495012be1425dd625f55d"
DENOMINATOR_SHA256 = "3b54d00ce59d2dba93b119edf669c1bf39c3f402e5e0d7dcb7139f013f135df1"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_CUT = ["M0527-EX-COVER", "M0527-EX-RANGE"]
FIBER_IDS = [
    "M0527-FIB", "M0527-FIB-FWD", "M0527-FIB-LIFT-PQ",
    "M0527-FIB-LIFT-QP", "M0527-FIB-INVERSE", "M0527-FIB-HOME",
    "M0527-FIB-OVER", "M0527-FIB-REV", "M0527-FIB-REV-MAP",
    "M0527-FIB-REV-RANGE",
]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0527.locPathConnectedSpace_of_isLocalHomeomorph",
    "Stage1Instances.THM_M_0527.covering_locPathConnectedSpace",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.comparisonLift",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.inducedSubgroup_eq_of_isomorphic",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.inducedMap_naturality",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.inducedMap_surjective",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.range_eq_of_comp_eq_of_surjective",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.inducedSubgroup_eq_of_naturality",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.inducedSubgroup_eq_of_isomorphic_via_naturality",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.comparisonMaps_mutualInverse",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.comparisonHomeomorph",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.isomorphic_of_comparisonMaps",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.isomorphic_of_inducedSubgroup_eq",
    "Stage1Instances.THM_M_0527.PointedConnectedCover.inducedSubgroup_eq_iff_isomorphic",
)
RECONCILED_INPUTS = {
    "Statement.lean": "00d2308cc4275b3ca7958961bc0ffc2c06651a64eff06773960f8aac94251327",
    "Proof.lean": "a279182be283228fd51f46d15dc5a9f80522d6e367cd1aff111c87af62e41467",
    "Validation.lean": "e6395dc99a61421c294831058d3ba22aace7637dc8857a9e839c8c9ae35a1e50",
    "statement.json": "d2c3b10b7c65129e4ac74bc07c53d4631800efdf78ca0d3a28699bcda4adfb8b",
    "anchor-audit.json": "420dde0497bdb408774de281cd9188a2ba48d626312932a73fa1d123f68e76ee",
    "obligation-registry.json": "8d63fae58b561e019f54fd213b37c6e055a4f5e96a33b8233128e938c5eab80b",
    "typed-graphs.json": "f152d6bb427c32658bf62750cb6eca0655575577d297cb17e90bfae27c65d87b",
    "obligation-tree-receipt.json": "7b8a69c13592e24f5566a924cf135d5b4248a383ae008d6ee1b25f7bd423908a",
    "proof-receipt.json": "6095c0fe7042c28add83dd77e85d56ed367296dddb304d9dabcb07c1071e0a2e",
    "proof-blocker.json": "a69b275041b2b0afd09e08bfa2056c4b26be09210116348e88ff178a4ea60d0b",
    "validation-spec.json": "47ad04785d486455cbb6484bea5efc5b03c2d5b5b6b56d5f404249c5b2f38286",
    "validation-receipt.json": "7ebdf6ed617ba9f11bb85e15f7cd377d2544e341a88698688290fc3ff7effa90",
    "check_validation.py": "661e22ac6a8e029a6a96a70a0949f1dc4a11b81d3fc61cc14d289c25f1e45a9c",
    "source_statement_crosswalk.md": "1dc8b8bab884748ec76b69912036d1bd8c655538782b180ea4c6481f6aaad049",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "4f5335b6a1724a2856bb155e3147debd858e7fc1cf07d4b70c757e6515f5dd23"
    ),
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, predecessor receipts, registry, graphs, and input hashes agree",
    "PASS narrow Lean replay: exact statement and fourteen partial fiber declarations checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H1/M3/R3 unchanged; M0527-EX-COVER and M0527-EX-RANGE remain open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def narrow_lean_replay() -> dict[str, object]:
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink(), "canonical pinned .lake symlink is unavailable"
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    mathlib = lake_link / "packages" / "mathlib"
    assert mathlib.is_dir() and git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).stdout.strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).stdout.strip()
    assert lean.is_file() and LEAN_COMMIT in run([str(lean), "--version"]).stdout

    with tempfile.TemporaryDirectory(prefix="stage1-m0527-release-", dir="/tmp") as name:
        temp = Path(name).resolve()
        for source in ("Statement.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / source, temp / source)

        def lean_run(source: str, module_path: str, emit_olean: bool) -> str:
            argv = [str(lean), "--trust=0", "-t0", "-R", str(temp)]
            if emit_olean:
                argv += ["-o", str(temp / source.replace(".lean", ".olean"))]
            argv.append(str(temp / source))
            env = {**fixed_env, "HOME": str(temp), "LEAN_PATH": module_path}
            return run(argv, cwd=LEAN_ROOT, env=env).stdout

        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "proof": lean_run("Proof.lean", f"{temp}:{lean_path}", True),
            "validation": lean_run("Validation.lean", f"{temp}:{lean_path}", False),
        }

    assert "Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget" in outputs["statement"]
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    semantic = {
        "statement_target_printed": True,
        "proof_axiom_reports": len(PROOF_DECLARATIONS),
        "validation_axiom_reports": len(PROOF_DECLARATIONS),
        "validation_sorry_free_report": True,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
    }
    return semantic


def main() -> None:
    if not __debug__:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 584 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 584,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0527-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0527-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0527-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == spec["covered_obligation_ids"]
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0527-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H1", "M3", "R3"
    ]
    assert graphs["closure_boundary"] == {
        "closed_obligations": [], "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M0527-EX-COVER", "M0527-EX-RANGE", "M0527-FIB"],
        "composition_certificates_checked": [], "theorem_complete": False,
    }
    assert anchor["exact_external_closure_found"] is False
    assert proof["accepted"] is False and proof["supported_obligation_ids"] == []
    assert proof["partial_progress_toward_obligation_ids"] == FIBER_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is proof["result"]["theorem_complete"] is False

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0527-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False
    assert validation["base_revision"] == VALIDATION_BASE != BASE_REVISION
    assert validation["release_grade"] is validation["accepted"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["remaining_root_cut_set"] == ROOT_CUT
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R3"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == ROOT_CUT
    for key in (
        "accepted_exact_root_kernel_closure", "audit_z_accepted", "pinpoint_h0_review",
        "independent_r0_review", "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "sbom_license_archive_closure", "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "not_used" and spec["expected_exit"] == 0
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget", *PROOF_DECLARATIONS,
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    lean_hashes = narrow_lean_replay()

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0527-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["input_bindings"] == {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": digest
            for name, digest in RECONCILED_INPUTS.items()
        },
        **AUTHORITY_INPUTS,
    }
    assert receipt["release_input_sha256"] == {
        "release-spec.json": sha256(HERE / "release-spec.json"),
        "release-decision.json": sha256(HERE / "release-decision.json"),
        "release-phase.md": sha256(HERE / "release-phase.md"),
        "check_release.py": sha256(Path(__file__).resolve()),
    }
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
        )
    }
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H1", "M3", "R3"
    ]
    assert receipt["result"]["remaining_root_cut_set"] == ROOT_CUT
    assert receipt["result"]["current_release_lean_output_sha256"] == lean_hashes
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    if os.environ.get("STAGE1_BOOTSTRAP") == "1":
        print("\n".join(SUMMARY_LINES))
        return

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in (
        "release-spec.json", "release-decision.json", "release-receipt.json", "release-phase.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
