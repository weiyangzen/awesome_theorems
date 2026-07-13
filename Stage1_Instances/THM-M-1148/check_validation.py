#!/usr/bin/env python3
"""Fail-closed validation packet checker for S56-M-1148-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1148"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1148-VALIDATION"
THEOREM = "THM-M-1148"
BASE_REVISION = "2d334dfd1443fdb9dbdf08b9d53d6c67399ec7af"
BASE_TREE = "1e9faa0af7424ddabe787898ee4534051a4cc145"
PROOF_BASE_REVISION = "0afbf514f9bd5f339943542106f6b811869fe572"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "4631cdf8cf607ec85b6c0e053d81966f967247daf9952a6edcbdfee6ac4016d8"
DENOMINATOR_SHA256 = "a19a68e6b87e8cca5d75a8d15555442289d8760b83f206ab64fc440a189ad243"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "7e17ed32e812a1b846ff168947684ac8930bbffe3c0f410ea4bea558c22ad25d",
    "statement.json": "ae749b5cdb83b6f00ce7ec0d1c94c807d774746aeee5c56e1d163b767710bb8a",
    "PoissonUnitDisk.lean": "9b2ee14db077d868340268cbb5504072adf7a5148425e57a5510dd2ce63cbcc8",
    "Proof.lean": "c8eb5a4dba0328d86dcd45c74a2c753b683e051be24806dc31570e92e211b18a",
    "ObligationTree.lean": "e21d471125e7798030a67d4f01da7be98fc057fe6aba0aeec0f26c56660cac2d",
    "obligation-registry.json": "1a8431015181de7259f2b70eb449c9aafb4f08a454e2a81aafed58eb761208bc",
    "typed-graphs.json": "79d1e08b15d38375bda31652915553f6d17571b279a284e26263ac745c62067c",
    "task-dag.json": "aad299b4c6141204c48bd7abecfe80c54088f7a3484074278a46b11393efd765",
    "instance.json": "7d4317063f6d1bb168c1b2637cfdacdee206eeab01331ff5dbb742134353b1d7",
    "proof-receipt.json": "6711ad4cfd6043b69c5341049e9dd203ad7bd2f32f9a2c9557af335ca15b4fe3",
    "proof-validation.md": "c91deccc0fb19034a0808dcd4ca339eeaaccd09ae6b4b02713a881c67b0b0ccb",
    "check_proof.py": "3f404185a3bc121de45c0e4296c03cb363515e018fae6fbc78a21a6172e67b44",
    "check_proof.sh": "86fad532afc81f3cf7f88d717017d3a9c7a5e6d59d1a17fd30fbb89c11b5ef5c",
    "ATLAS-LICENSE": "289dc0e96c537ecc7883cd94c3f65e2b691ac0fd6f4372fc01604531cbbf1abc",
}
EXPECTED_REPO_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "c43af2ed89fb2d44bfce10abbbf85233fa0ff289bb1d712c3f06db9a65bbefb4",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
UNIT_DECLARATIONS = (
    "poissonIntegral_eq_re_herglotzIntegral",
    "herglotzIntegral_differentiableOn",
    "poissonIntegral_harmonic",
    "unitDiskExtension_harmonic",
    "unitDiskExtension_eqOn_sphere",
    "unitDiskExtension_continuousOn",
    "unitKernelMass",
    "unitPoissonKernel_nonneg",
    "boundaryData_uniformContinuousOn",
    "continuous_extension_of_sphere",
    "invMobiusAngle_mobiusTransform_core",
    "poissonIntegral_eq_circleAverage_mobiusTransform",
    "mobiusTransform_tendsto_on_circle",
    "circleAverage_mobiusTransform_tendsto",
    "poissonIntegral_tendsto_boundary",
    "bounded_continuous_extension_of_sphere",
    "unitDiskConstruction",
    "harmonicOnNhd_affine_pullback",
    "continuousOn_affine_pullback",
    "eqOn_affine_pullback",
    "generalDiskConstruction",
)
PROOF_DECLARATIONS = (
    "interiorFormula_of_harmonicContOnCl_of_eqOn",
    "dirichletExtension_to_root",
    "rootTarget_to_frozen",
    "dirichletExtension_to_frozen",
    "dirichletExtension",
    "poissonIntegralFormula",
    "unitDiskConstruction_of_boundaryConvergence",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = [
    "PASS network-isolated trust-zero kernel replay: exact statement, implemented proof root, and separately reconstructed local root elaborated",
    "PASS trust observation: 29 selected declarations report exactly propext, Classical.choice, and Quot.sound",
    "PASS narrow provenance: frozen source hashes, proof receipt, ATLAS license, clean mathlib pin, and tool identities agree",
    "FAIL CLOSED dependency and state freshness: proof is provisional, its receipt is stale at current HEAD, and frozen structured state remains open",
    "FAIL CLOSED complete provenance and hermetic release: ATLAS source is not vendored, license compatibility is unreviewed, and the shared dependency cache is warm",
    "FAIL CLOSED independent verification: the differential proof shares this worker, checkout, Lean binary, and dependency cache",
    "audit_complete=false; theorem_complete=false",
]


if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")


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
    timeout: int = 60,
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


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*\.{re.escape(declaration)}' depends on axioms:\s*\[(.*?)]",
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
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 353
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 353,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1148-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1148-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert next(row for row in local_dag["tasks"] if row["id"] == "S56-M-1148-PROOF")["state"] == "open"
    assert local_dag["accepted_states"] == []
    assert instance["lifecycle"] == "planned"
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for relative, expected in EXPECTED_REPO_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"stale repository input: {relative}"
    assert statement["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_machine_debt": "M4",
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1148-C", "M1148-L1", "M1148-B", "M1148-N3"],
    }
    assert proof_receipt["base_revision"] == PROOF_BASE_REVISION
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof_receipt["root_evidence"]["accepted_root_closed"] is False
    assert proof_receipt["root_evidence"]["internal_per_node_composition_credit"] is False
    assert proof_receipt["proof_bodies"][0]["license_compatibility"] == "unreviewed_blocker"
    assert proof_receipt["result"]["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "PoissonUnitDisk.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation_source = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in validation_source
    assert "independent" not in validation_source.lower()
    assert "theorem reconstructedPoissonIntegralFormula" in validation_source
    assert "generalDiskConstruction c R hR g hg" in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == (
        "https://github.com/leanprover-community/mathlib4.git"
    )
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
    lake = lean.with_name("lake")
    assert lean.is_file() and lake.is_file()
    lean_version = run([str(lean), "--version"])
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_dirs = [
        LEAN_ROOT / ".lake" / "packages" / name / ".lake" / "build" / "lib" / "lean"
        for name in (
            "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
            "LeanSearchClient", "plausible",
        )
    ] + [
        MATHLIB / ".lake" / "build" / "lib" / "lean",
        LEAN_ROOT / ".lake" / "build" / "lib" / "lean",
        lean.parents[1] / "lib" / "lean",
    ]
    assert all(path.is_dir() for path in lean_dirs)
    lean_path = ":".join(str(path) for path in lean_dirs)
    bwrap = shutil.which("bwrap")
    assert bwrap is not None
    with tempfile.TemporaryDirectory(prefix="m1148-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "PoissonUnitDisk.lean", "Proof.lean", "Validation.lean"):
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
            "--setenv", "PATH", f"{lean.parent}:/usr/bin:/bin",
            "--chdir", str(tmp),
        ]
        run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lake), "env", "lean", "--trust=0",
            "-o", "Statement.olean", "Statement.lean",
        ], timeout=180)
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        unit_output = run(base + module_env + [
            str(lake), "env", "lean", "--trust=0", "-o", "PoissonUnitDisk.olean",
            "PoissonUnitDisk.lean",
        ], timeout=420)
        proof_output = run(base + module_env + [
            str(lake), "env", "lean", "--trust=0", "Proof.lean",
        ], timeout=420)
        validation_output = run(base + module_env + [
            str(lake), "env", "lean", "--trust=0", "Validation.lean",
        ], timeout=420)

    for declaration in UNIT_DECLARATIONS:
        assert printed_axioms(unit_output, declaration) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "reconstructedPoissonIntegralFormula") == EXPECTED_AXIOMS
    assert "sorryAx" not in unit_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1"
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied"
    assert spec["network_policy_scope"] == (
        "Lean subrecipes only; this is not a recipe-level hermetic network guarantee"
    )
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == ["M1148-ROOT", "M1148-X", "M1148-T"]
    expected_covered_declarations = [
        *(f"Stage1Instances.THM_M_1148.PoissonUnitDisk.{name}" for name in UNIT_DECLARATIONS),
        *(f"Stage1Instances.THM_M_1148.Proof.{name}" for name in PROOF_DECLARATIONS),
        "Stage1Instances.THM_M_1148.Validation.reconstructedPoissonIntegralFormula",
    ]
    assert spec["covered_declarations"] == expected_covered_declarations

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["started_at"] == "2026-07-14T04:27:30+08:00"
    assert receipt["finished_at"] == receipt["validated_at"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["repository_state"]["release_clean"] is False
    assert receipt["repository_state"]["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    input_payload = [
        {"path": name, "sha256": sha256(HERE / name)}
        for name in ("Validation.lean", "check_validation.py", "validation-phase.md", "validation-spec.json")
    ]
    assert receipt["repository_state"]["untracked_input_sha256"] == hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert receipt["content_addressing"]["receipt_content_addressed"] is False
    assert receipt["content_addressing"]["recipe_content_addressed"] is False
    assert receipt["content_addressing"]["release_bundle_id"] is None
    assert receipt["invalidation_inputs"]
    assert receipt["supersession_state"] and receipt["revocation_state"]
    assert receipt["incident_path"].endswith("S56-M-1148-VALIDATION")
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1148-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["remaining_root_cut_set"] == [
        "S56-M-1148-PROOF master acceptance",
        "ATLAS license and upstream-source provenance review",
        "frozen internal composition reconciliation",
        "complete transitive foundation and TCB closure",
        "cold empty-cache offline replay",
        "distinct signed independent verifier",
    ]
    assert receipt["results"]["kernel_replay"] == "pass_network_isolated_trust_zero_warm_cache"
    assert receipt["results"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["results"]["exact_root_kernel_closed"] is True
    assert receipt["results"]["accepted_root_closed"] is False
    assert receipt["results"]["accepted_closed_obligation_ids"] == []
    assert receipt["results"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["results"]["independent_verification_gate"] == "fail_closed"
    assert receipt["results"]["differential_root_kernel_closed"] is True
    assert "shares this worker" in receipt["output_summary"][5]
    assert "independent local root" not in "\n".join(receipt["output_summary"]).lower()
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation_source_sha256"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation_phase_sha256"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["check_validation_sha256"] == sha256(HERE / "check_validation.py")
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for relative, expected in EXPECTED_REPO_INPUTS.items():
        assert receipt["inputs"][relative] == expected
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_policy_scope", "network_enforcement", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations", "coverage_boundary",
    ):
        assert receipt["recipe"][key] == spec[key]
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(Path(sys.executable).resolve())
    assert environment["git_executable_sha256"] == sha256(Path(shutil.which("git") or "").resolve())
    assert environment["bash_executable_sha256"] == sha256(Path(shutil.which("bash") or "").resolve())
    assert environment["bubblewrap_executable_sha256"] == sha256(Path(bwrap).resolve())
    assert environment["platform"] == f"{platform.system()} {platform.machine()}"
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == receipt["known_failures"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
    summary_bytes = "".join(f"{line}\n" for line in SUMMARY_LINES).encode()
    assert receipt["output_evidence"]["recorded_summary_sha256"] == hashlib.sha256(
        summary_bytes
    ).hexdigest()

    status = git("status", "--porcelain=v1", "--untracked-files=all")
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
        if (line[3:] if line[:2] == "??" else line[2:].lstrip()) != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        public_text = path.read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
