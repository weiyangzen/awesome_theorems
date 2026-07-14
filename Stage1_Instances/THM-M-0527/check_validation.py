#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0527-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import pwd
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0527"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0527-VALIDATION"
THEOREM = "THM-M-0527"
BASE_REVISION = "874745ff39044c1e45ed30a04111d3d84aa0e348"
BASE_TREE = "6e4fd01c84ebee3b7e65ad42efcfe307b2f88fc4"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "4c7a7d4c54edb4a2d46091dda31f20a26664f005b20495012be1425dd625f55d"
)
DENOMINATOR_SHA256 = "3b54d00ce59d2dba93b119edf669c1bf39c3f402e5e0d7dcb7139f013f135df1"
EXPECTED_INPUT_HASHES = {
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
    "source_statement_crosswalk.md": "1dc8b8bab884748ec76b69912036d1bd8c655538782b180ea4c6481f6aaad049",
    "validation-spec.json": "47ad04785d486455cbb6484bea5efc5b03c2d5b5b6b56d5f404249c5b2f38286",
}
SELECTED_PROVENANCE = {
    "Mathlib/Topology/Covering/Basic.lean": (
        "1172bafdcd01889d475dde04af1f6bf1fb8486b3",
        "c9f48cf15f3740dea92c17c6943bf718865d9e4d28410433f4cf219f17843890",
        "24f220addb5c422a90b954236031b6736a508ac4cb2fa0cc242b07fd4f2f7af0",
    ),
    "Mathlib/Topology/Homotopy/Lifting.lean": (
        "4e1bc1f865f88a9fd2680b3271e56ceb5ac68eef",
        "e47671e27a60b6e7f3699df8b2ba1a3c40bc2c939971e972c8d6acb7bfc73291",
        "3aa2db189f9f52a75808b6389e7df787ba8bef40438bbbee78939716d56e692c",
    ),
    "Mathlib/Topology/Connected/LocPathConnected.lean": (
        "d884aaee656e28af9a3fe9aa3cfeaa01fc0269f0",
        "3227bb1d0f8ef455d2109196638be7ff1c2a27585b2d9219ff4f61fd4a5ea912",
        "6acd1a7396942024965b9ad27ce8885dfc73f0d581d4f0058666d39cfa607aad",
    ),
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
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
FIBER_IDS = [
    "M0527-FIB", "M0527-FIB-FWD", "M0527-FIB-LIFT-PQ",
    "M0527-FIB-LIFT-QP", "M0527-FIB-INVERSE", "M0527-FIB-HOME",
    "M0527-FIB-OVER", "M0527-FIB-REV", "M0527-FIB-REV-MAP",
    "M0527-FIB-REV-RANGE",
]
ROOT_CUT = ["M0527-EX-COVER", "M0527-EX-RANGE"]
RECIPE_PATH = "/usr/bin:/bin"
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
    "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net",
    "--die-with-parent", "--clearenv", "--setenv", "HOME", "/tmp",
    "--setenv", "PATH", RECIPE_PATH, "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1", "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


if not __debug__:
    raise RuntimeError("validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).rstrip()


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
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    obligation_receipt = load(HERE / "obligation-tree-receipt.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    receipt_path = HERE / "validation-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    verify_outputs = os.environ.get("STAGE1_SKIP_OUTPUT_CHECK") != "1"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 584,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "覆盖空间理论",
        "category": "拓扑学 / 代数拓扑",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 132,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 584,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0527-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0527-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == RECIPE_ARGV and spec["cwd"] == "."
    assert spec["env_allowlist"] == {
        "HOME": "/tmp", "PATH": RECIPE_PATH, "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert spec["timeout_seconds"] == 720 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert len(spec["expected_outputs"]) == 1
    assert spec["expected_outputs"][0]["path_or_stream"] == "stdout"
    obligation_ids = [row["obligation_id"] for row in registry["obligations"]]
    assert spec["covered_obligation_ids"] == obligation_ids
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget",
        *PROOF_DECLARATIONS,
    }

    for name, expected in EXPECTED_INPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
    canonical = statement["canonical_formal_target"]
    assert canonical["statement_file_sha256"] == EXPECTED_INPUT_HASHES["Statement.lean"]
    assert canonical["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0527-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert obligation_receipt["outputs"]["denominator_sha256"] == DENOMINATOR_SHA256
    assert obligation_receipt["outputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": [], "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M0527-EX-COVER", "M0527-EX-RANGE", "M0527-FIB"],
        "composition_certificates_checked": [], "theorem_complete": False,
    }
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0527-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == {"H": "H1", "M": "M3", "R": "R3"}
    assert anchor["exact_external_closure_found"] is False
    assert anchor["machine_status"] == "M3" and anchor["theorem_complete"] is False
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["proposed_state"] == "[_]" and proof_receipt["accepted"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUT_HASHES["Proof.lean"]
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == FIBER_IDS
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == ROOT_CUT
    assert proof_blocker["remaining_root_cut_set"] == ROOT_CUT
    assert proof_blocker["root_closed"] is False and proof_blocker["theorem_complete"] is False

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
    validation_source = source_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert re.search(r"^(?:theorem|def|abbrev|instance)\b", validation_source, re.MULTILINE) is None
    assert validation_source.count("assert_no_sorry ") == len(PROOF_DECLARATIONS)

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for source_name, (blob_hash, source_hash, olean_hash) in SELECTED_PROVENANCE.items():
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == blob_hash
        assert sha256(MATHLIB / source_name) == source_hash
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / source_name.replace(
            ".lean", ".olean"
        )
        assert sha256(olean) == olean_hash
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

    toolchain_bin = (
        Path(pwd.getpwuid(os.getuid()).pw_dir)
        / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    )
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    bwrap = Path("/usr/bin/bwrap")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    fixed_env = {
        "HOME": os.environ["HOME"], "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert {key: os.environ[key] for key in spec["env_allowlist"]} == spec["env_allowlist"]
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    lean_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).strip()

    temp_root = Path(tempfile.mkdtemp(prefix="stage1-m0527-validation-", dir="/tmp"))
    try:
        target_dir = temp_root / "Stage1_Instances" / THEOREM
        target_dir.mkdir(parents=True)
        for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, target_dir / name)
        (temp_root / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            path = f"{target_dir}:{lean_path}" if module_path else lean_path
            return run(
                [str(lake), "env", "lean", "--trust=0", "-t0", "-R", str(target_dir), *args],
                cwd=LEAN_ROOT,
                env={**fixed_env, "HOME": str(temp_root / "home"), "LEAN_PATH": path},
                timeout=600,
            )

        statement_output = isolated_lean([
            "-o", str(target_dir / "Statement.olean"), str(target_dir / "Statement.lean")
        ])
        proof_output = isolated_lean([
            "-o", str(target_dir / "Proof.olean"), str(target_dir / "Proof.lean")
        ], module_path=True)
        validation_output = isolated_lean([
            str(target_dir / "Validation.lean")
        ], module_path=True)
    finally:
        shutil.rmtree(temp_root)

    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    combined = "\n".join((statement_output, proof_output, validation_output))
    assert "Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget" in statement_output
    assert validation_output.count("Declarations are sorry-free!") == 1
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined

    if receipt is not None and verify_outputs:
        assert receipt["schema_version"] == "stage1-node-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
        assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
        assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
        for key, name in (
            ("statement_source_sha256", "Statement.lean"),
            ("proof_source_sha256", "Proof.lean"),
            ("validation_probe_sha256", "Validation.lean"),
            ("validation_spec_sha256", "validation-spec.json"),
            ("validator_sha256", "check_validation.py"),
            ("statement_record_sha256", "statement.json"),
            ("anchor_audit_sha256", "anchor-audit.json"),
            ("obligation_registry_sha256", "obligation-registry.json"),
            ("typed_graphs_sha256", "typed-graphs.json"),
            ("obligation_tree_receipt_sha256", "obligation-tree-receipt.json"),
            ("proof_receipt_sha256", "proof-receipt.json"),
            ("proof_blocker_sha256", "proof-blocker.json"),
            ("source_crosswalk_sha256", "source_statement_crosswalk.md"),
        ):
            assert receipt["inputs"][key] == sha256(HERE / name), key
        assert receipt["recipe"] == {
            key: spec[key] for key in (
                "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
                "network_policy", "network_enforcement", "expected_exit",
            )
        }
        assert receipt["repository_state"]["base_owned_patch_sha256"] == (
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
        assert receipt["repository_state"]["pre_existing_untracked_symlink_text_sha256"] == (
            "e7d8a6bce8b934a5b0dc162324c830c4f26e1146c65bb31e8063491a3f47bfcc"
        )
        result = receipt["result"]
        assert result["revalidated_partial_progress_ids"] == FIBER_IDS
        assert result["accepted_closed_obligation_ids"] == []
        assert result["root_kernel_closed"] is False
        assert result["root_vector_before"] == result["root_vector_after"] == {
            "H": "H1", "M": "M3", "R": "R3"
        }
        assert result["remaining_root_cut_set"] == ROOT_CUT
        assert result["complete_transitive_provenance_gate"] == "fail_closed"
        assert result["complete_transitive_tcb_gate"] == "fail_closed"
        assert result["hermetic_release_gate"] == "fail_closed"
        assert result["independent_verification_gate"] == "fail_closed"
        assert result["audit_complete"] is False and result["theorem_complete"] is False
        assert receipt["first_failed_gate"] == "dependency.S56-M-0527-PROOF.master_acceptance"
        assert receipt["remaining_root_cut_set"] == ROOT_CUT
        assert set(receipt["changed_paths"]) == CHANGED_PATHS

    if verify_outputs:
        packet = load(ROOT / ".stage1-worker-selftest.json")
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
        assert isinstance(packet["known_failures"], list) and packet["known_failures"]
        actual_changes = {
            line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        }
        actual_changes.discard("Formalizations/Lean/.lake")
        assert actual_changes == CHANGED_PATHS
        for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
            assert_text_hygiene(ROOT / relative)

    assert platform.system() == "Linux"
    print("PASS THM-M-0527 network-isolated trust-zero fresh-output replay")
    print("PASS exact statement and all fourteen proof-phase declarations elaborated; Lean reports them sorry-free")
    print("PASS observed axioms are exactly propext, Classical.choice, and Quot.sound")
    print("PASS frozen inputs and selected pinned mathlib source, blob, olean, origin, license, and tool identities agree")
    print("OPEN proof master acceptance, arbitrary-subgroup cover construction, complete trust/provenance, cold hermetic replay, and distinct-runner verification")


if __name__ == "__main__":
    main()
