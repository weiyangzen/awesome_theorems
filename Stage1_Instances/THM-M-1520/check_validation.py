#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1520-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1520"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1520-VALIDATION"
THEOREM = "THM-M-1520"
BASE_REVISION = "ed9e08c4aa5d18cb58fa54e74867f38999a92a14"
BASE_TREE = "41384c2a54f3f02cffd5aa5c92555706fc748659"
EXPRESSION_SHA256 = "547fe7d61d57e7ea242aaff7a97763a769275f0c6f1c64d03ca5db45e82a012b"
DENOMINATOR_SHA256 = "3e5ecbc29279547f4e05323bfea6cdbda08b8e69545cffba35df81df8b460e4c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"

LEAN_MODULES = (
    "Statement.lean",
    "Proof.lean",
    "FlowAlgebra.lean",
    "JacobianBridge.lean",
    "VectorFieldRegularity.lean",
    "ChangeOfVariables.lean",
    "ObligationTree.lean",
    "AnchorAudit.lean",
    "Validation.lean",
)

EXPECTED_INPUTS = {
    "Statement.lean": "0b3bb7e3410047f58ca7790fd4640c547604bbf8b2e715b0bf46c32634ce2ef0",
    "Proof.lean": "24fe83d637e32fba4339836b621d973364b3aa216d309026919209184d4958ac",
    "FlowAlgebra.lean": "fd042ca5dd5521eb31070b1dc58edf918998754f84df546c1e8b05a3cbdf5075",
    "JacobianBridge.lean": "47c55fa46e82f5eb5f26034351f28625b33b7b16b14946f2308c743b33e96589",
    "VectorFieldRegularity.lean": "1f7c8bc12e51b81fba8f55bda63699936f6c198500422f297a37bcb0fcc1adea",
    "ChangeOfVariables.lean": "bd1afc515434ab31955de36fdb60f6549d678a0896846b94aad10c9919b4056a",
    "ObligationTree.lean": "e73e0e967957fe57d94dba19206bd7f23e5499f54149e19ca693787500e4d4d0",
    "AnchorAudit.lean": "52166d5b009f1ec2747e778a162170f2e8695c9107fba5cc1cbe4d04966d8691",
    "Validation.lean": "5851fe985eb77ff846a8ff687dbf70998b2990ad4fb692af707d0d770aba5d63",
    "intake.json": "fe1f419b89de7b5f7da97a0c0e6855ddf058a3d843ef8d54cc95d84dd257304e",
    "obligation-registry.json": "705f92d2c5a61eb289f27aef71ff454d4afc397f7039e57044498af825cad851",
    "typed-graphs.json": "e4116a46fa9a193b332bc30be1c3c025d258fa2318d328e53b3e7fb1fe866a90",
    "proof-receipt.json": "26dab222a908b9b94a79a060a820931ddaad11b694fa8cb5c301c9cdcfe5b301",
    "source_statement_crosswalk.md": "a0acd0ac603b566b732f6ac2f767ad15357004413e5aee4479ee08d68c361f97",
    "anchor_audit.md": "da7dc36cb1b07bc2bade0d3a0adff0a1840a4fb101e763b763179020d3bf73b8",
    "check_obligation_tree.py": "e035b6c693027fdbabeae149404845622cb0cbef0f762a7d53b790e5d8b6be10",
    "validation-spec.json": "a642405bbf507e18e5323e1889e9b83b3451c6ba41d3dce8b29c2c550a3cf58e",
}

PINNED_TERMINALS = {
    "Mathlib/Analysis/Calculus/ContDiff/Comp.lean": {
        "sha256": "681ad595de1071027a0af86aafa30694907c9878455fedeed7818c7b01a36279",
        "blob": "ddbf59b18f85f0fdea44b50bc74d09782604a219",
        "olean": "Mathlib/Analysis/Calculus/ContDiff/Comp.olean",
        "olean_sha256": "35e0932e6dfdf799b1566fb7d72b6c7b32c6a75a3b7f6ecf4bca447c0ea8b009",
    },
    "Mathlib/Analysis/Calculus/ContDiff/WithLp.lean": {
        "sha256": "2a6f678a6a6ef69c002204bf38a0684fc0492e3f992e6afab667fb7139bd31db",
        "blob": "48f0c2c7b8e0f2e98c3045b825ae284fff548854",
        "olean": "Mathlib/Analysis/Calculus/ContDiff/WithLp.olean",
        "olean_sha256": "775e2307aec9e98012324109a34f087b9af5aece465b5f5f22fa47417610d8b3",
    },
    "Mathlib/MeasureTheory/Function/Jacobian.lean": {
        "sha256": "8ef05ea1f035e9281c768c453536cfeb9e6bdc205657563628ebc81ee6de6c33",
        "blob": "262b0739135ae11eb54b9ab0b953e89d0bacc75f",
        "olean": "Mathlib/MeasureTheory/Function/Jacobian.olean",
        "olean_sha256": "21222dc7ba4286c223cbf9d755c93a9fd53d0ec9a02252c2e54c0ab334ff4030",
    },
}

AXIOM_DECLARATIONS = {
    "Proof.lean": (
        "timeZero_measurePreserving",
        "zeroDimension_measurePreserving",
    ),
    "FlowAlgebra.lean": ("timeMap_bijective",),
    "JacobianBridge.lean": ("measurePreserving_of_det_fderiv_eq_one",),
    "VectorFieldRegularity.lean": ("hamiltonianVectorField_contDiff_one",),
    "ChangeOfVariables.lean": (
        "timeMap_measurePreserving_of_differentiable_det_eq_one",
        "allTimeMaps_measurePreserving_of_differentiable_det_eq_one",
    ),
    "ObligationTree.lean": ("liouvilleStatement_of_analyticPackage",),
    "Validation.lean": (
        "timeZero_measurePreserving_direct",
        "timeMap_bijective_direct",
    ),
}

SUMMARY_LINES = (
    "PASS trust-zero network-isolated replay of nine copied Lean modules and ten local declarations",
    "PASS observed axioms: exactly propext, Classical.choice, and Quot.sound; no sorryAx",
    "PASS frozen hashes, graph invariants, clean mathlib pin, direct terminal source/blob/olean provenance, and source hygiene",
    "FAIL CLOSED exact root: LiouvilleAnalyticPackage has no inhabitant and M1520-T-ALL-TIMES remains open",
    "FAIL CLOSED complete trust/provenance and cold hermetic replay: the dependency cache is shared, warm, mutable, and not an offline-restorable release closure",
    "FAIL CLOSED independent verification: same-workspace probes are not a second signed clean runner or independently implemented release verifier",
)


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
) -> str:
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
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout.strip()


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd)


def source_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 189 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 189,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1520-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1520-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256

    assert intake["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert registry["root_obligation_id"] == "M1520-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == ["M1520-T-ASSEMBLE"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1520-T-ALL-TIMES"]
    assert closure["composition_certificates"] == [
        "Stage1.THM_M_1520.liouvilleStatement_of_analyticPackage"
    ]
    assert proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_pin = next(row for row in manifest["packages"] if "flt-regular" in row["name"])
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert flt_pin["rev"] == flt_pin["inputRev"] == FLT_REGULAR_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == (
        "https://github.com/leanprover-community/mathlib4.git"
    )
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )

    olean_root = MATHLIB / ".lake" / "build" / "lib" / "lean"
    for relative, expected in PINNED_TERMINALS.items():
        source = MATHLIB / relative
        assert sha256(source) == expected["sha256"]
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(olean_root / expected["olean"]) == expected["olean_sha256"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"

    validation = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert validation.startswith("import Statement\n")
    assert "import Proof" not in validation and "import ObligationTree" not in validation
    for marker in (
        "theorem timeZero_measurePreserving_direct",
        "theorem timeMap_bijective_direct",
        "#check LiouvilleStatement",
    ):
        assert marker in validation

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert "Lean (version 4.29.0" in run([str(lean), "--version"])
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required to enforce network denial"

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1520-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_MODULES:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap,
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(tmp),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp),
            str(lean), "--trust=0", "-t0",
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"

        outputs["Statement.lean"] = run(
            base + ["-o", "Statement.olean", "Statement.lean"], timeout=300
        )
        outputs["JacobianBridge.lean"] = run(
            base + ["-o", "JacobianBridge.olean", "JacobianBridge.lean"], timeout=300
        )
        for name in (
            "Proof.lean",
            "FlowAlgebra.lean",
            "VectorFieldRegularity.lean",
            "ChangeOfVariables.lean",
            "ObligationTree.lean",
            "Validation.lean",
        ):
            outputs[name] = run(local + ["-o", name[:-5] + ".olean", name], timeout=300)
        outputs["AnchorAudit.lean"] = run(base + ["AnchorAudit.lean"], timeout=300)

    allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
    for name, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[name], declaration) == allowed_axioms
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output
    for name in (
        "FlowAlgebra.lean",
        "JacobianBridge.lean",
        "VectorFieldRegularity.lean",
        "ChangeOfVariables.lean",
        "Validation.lean",
    ):
        assert "Declarations are sorry-free!" in outputs[name]

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_release_verification_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M1520-T-ALL-TIMES"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1520-PROOF.master_acceptance"

    changed_paths = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    }
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == changed_paths
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == changed_paths, (actual_changes, changed_paths)

    for path in [ROOT / path for path in changed_paths]:
        assert_text_hygiene(path)
    for line in SUMMARY_LINES:
        print(line)
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
