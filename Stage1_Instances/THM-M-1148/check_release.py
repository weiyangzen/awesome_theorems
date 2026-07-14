#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1148-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1148"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1148-RELEASE"
THEOREM = "THM-M-1148"
BASE_REVISION = "99cd22cccebeb1f25106f5bdb86b82a536ae1a68"
BASE_TREE = "ac469ca91938094c2987a47d19fc2a457a0d3a97"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "4631cdf8cf607ec85b6c0e053d81966f967247daf9952a6edcbdfee6ac4016d8"
DENOMINATOR_SHA256 = "a19a68e6b87e8cca5d75a8d15555442289d8760b83f206ab64fc440a189ad243"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1148-ROOT", "M1148-S", "M1148-S1", "M1148-S2", "M1148-S3",
    "M1148-S4", "M1148-N", "M1148-N1", "M1148-N2", "M1148-N3",
    "M1148-B", "M1148-B1", "M1148-B2", "M1148-B3", "M1148-C",
    "M1148-C1", "M1148-C2", "M1148-C3", "M1148-L", "M1148-L1",
    "M1148-L2", "M1148-L3", "M1148-L4", "M1148-L5", "M1148-X",
    "M1148-T",
]
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
EXPECTED_INPUTS = {
    "Statement.lean": "7e17ed32e812a1b846ff168947684ac8930bbffe3c0f410ea4bea558c22ad25d",
    "PoissonUnitDisk.lean": "9b2ee14db077d868340268cbb5504072adf7a5148425e57a5510dd2ce63cbcc8",
    "Proof.lean": "c8eb5a4dba0328d86dcd45c74a2c753b683e051be24806dc31570e92e211b18a",
    "Validation.lean": "0ae64091d1ef92bbbc412598425087cf02b2f95d3b7ab7f2a2f5645c06c8d15d",
    "instance.json": "7d4317063f6d1bb168c1b2637cfdacdee206eeab01331ff5dbb742134353b1d7",
    "task-dag.json": "aad299b4c6141204c48bd7abecfe80c54088f7a3484074278a46b11393efd765",
    "statement.json": "ae749b5cdb83b6f00ce7ec0d1c94c807d774746aeee5c56e1d163b767710bb8a",
    "scope-map.md": "9c0f6bed0faced4c171a138fe9470490e8f9fc818d1eced01810ee5d666477ec",
    "source-statement-crosswalk.md": "eaad8ca35ae1f1c55660f1da07e58313dcbc223152f55c9d37e598fb2f153254",
    "anchor-audit.json": "88fa518e73db2a8b0b89a45f4c7499aea468be40d271dacb046799e29fcae108",
    "obligation-registry.json": "1a8431015181de7259f2b70eb449c9aafb4f08a454e2a81aafed58eb761208bc",
    "typed-graphs.json": "79d1e08b15d38375bda31652915553f6d17571b279a284e26263ac745c62067c",
    "proof-receipt.json": "6711ad4cfd6043b69c5341049e9dd203ad7bd2f32f9a2c9557af335ca15b4fe3",
    "proof-validation.md": "c91deccc0fb19034a0808dcd4ca339eeaaccd09ae6b4b02713a881c67b0b0ccb",
    "validation-spec.json": "c97fca7f44577f43aac133e59e060985808abc344fee1b12f617348c4999bab7",
    "validation-receipt.json": "40c0472362bfc14195fe4a21dd62ebc76dde888d1e33ecde8a712add9cc56abb",
    "validation-phase.md": "413daeee3b97b70438404bb6aeddcbe972c3148fae7b9b9b9f8f152918199536",
    "check_validation.py": "b3315a7fdd21b2114d1a08df00f5c230b34a1d900cdeb948e9d9831821266776",
    "ATLAS-LICENSE": "289dc0e96c537ecc7883cd94c3f65e2b691ac0fd6f4372fc01604531cbbf1abc",
    "release-decision.json": "a1855409e06592f7119dfcc517ab087c772d9796c6f1068b553c07dcce5316bb",
    "release-spec.json": "b164d6967aa03ea34e3487e4500b449c5fb81b1a52fe47a7b4dcf7e15fa0ca88",
    "release-validation.md": "d7de4db7635ea72831f3ef499c01eebe3dbdd9705c4cb03d30aa5196128b60d6",
}
EXPECTED_REPO_INPUTS = {
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3e7913dbcfa5096fb9a9a4c07410a5af8c83dd48d6a9fbef9615b57ed514ceca",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0c2dffccab35acb05f1c6619d3172815dcfb6b6011651e596b7a360a9dcf6c4b",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
SUMMARY_LINES = [
    "release-decision: ok (blocked at validation dependency acceptance)",
    "narrow Lean replay: ok (29 declarations, trust-zero, network-isolated, warm-cache)",
    "accepted boundary: H2/M4/R4 unchanged; instance H2/M3/R4 conflict remains open",
    "accepted root=false; frozen cut=M1148-C,M1148-L1,M1148-B,M1148-N3",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]",
    "release assurance: immutable-clean, cold-offline, source-license, H0/R0, TCB, independent-verifier, CI, and deterministic-bundle gates open",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
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
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 600,
    env: dict[str, str] | None = None,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False, env=env,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


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


def replay_lean() -> None:
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied replay"
    discovery_env = os.environ.copy()
    discovery_env.pop("LEAN_PATH", None)
    lean = Path(run(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=120,
        env=discovery_env,
    ).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, timeout=120,
        env=discovery_env,
    ).strip()
    lake = lean.with_name("lake")
    assert lean.is_file() and lake.is_file()
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=60)

    with tempfile.TemporaryDirectory(prefix="m1148-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "PoissonUnitDisk.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN,
            "--setenv", "LEAN_NUM_THREADS", "1", "--setenv", "PATH",
            f"{lean.parent}:/usr/bin:/bin", "--chdir", str(tmp),
        ]
        run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lake), "env", "lean",
            "--trust=0", "-o", "Statement.olean", "Statement.lean",
        ], timeout=300)
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

    assert "sorryAx" not in unit_output + proof_output + validation_output
    for declaration in UNIT_DECLARATIONS:
        assert printed_axioms(unit_output, declaration) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    assert printed_axioms(
        validation_output, "reconstructedPoissonIntegralFormula"
    ) == EXPECTED_AXIOMS


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 353 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 353,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1148-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1148-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-1148-VALIDATION"
    )["state"] == "open"
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

    assert statement["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_machine_debt": "M4",
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1148-C", "M1148-L1", "M1148-B", "M1148-N3"],
    }
    root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1148-ROOT")
    assert [
        root_node["human_debt"], root_node["machine_debt"], root_node["readability_debt"]
    ] == ["H2", "M4", "R4"]
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert proof["accepted"] is False and proof["content_addressed"] is False
    assert proof["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof["root_evidence"]["accepted_root_closed"] is False
    assert proof["root_evidence"]["internal_per_node_composition_credit"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["proof_bodies"][0]["license_compatibility"] == "unreviewed_blocker"
    assert validation["item_id"] == "S56-M-1148-VALIDATION"
    assert validation["verdict"] == "blocked"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["root_vector_before"] == validation["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }
    assert validation["results"]["exact_root_kernel_closed"] is True
    assert validation["results"]["accepted_root_closed"] is False
    assert validation["results"]["accepted_closed_obligation_ids"] == []
    assert validation["audit_complete"] is validation["theorem_complete"] is False

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
    assert "generalDiskConstruction c R hR g hg" in validation_source

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["intent"] == "release" and decision["proposed_state"] == "[_]"
    assert decision["release_grade"] is False and decision["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_substantive_gate"]["gate_id"] == (
        "S56-M1148-STRUCTURED-STATE-RECONCILIATION"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    cut = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1148-VALIDATION", "M1148-C", "ATLAS", "transitive declaration",
        "primary-source", "R0", "AUDIT-Z", "empty-cache", "two signed",
        "minimal release verifier", "deterministic", "THEOREM-Z",
    ):
        assert fragment in cut, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1148-RELEASE-NARROW-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    expected_declarations = [
        "Stage1Instances.THM_M_1148.PoissonIntegralFormula",
        *(f"Stage1Instances.THM_M_1148.PoissonUnitDisk.{name}" for name in UNIT_DECLARATIONS),
        *(f"Stage1Instances.THM_M_1148.Proof.{name}" for name in PROOF_DECLARATIONS),
        "Stage1Instances.THM_M_1148.Validation.reconstructedPoissonIntegralFormula",
    ]
    assert spec["covered_declarations"] == expected_declarations

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H2", "M4", "R4"
    ]
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    replay_lean()

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == SUMMARY_LINES == receipt["output_summary"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "release-decision.json", HERE / "release-receipt.json", HERE / "release-validation.md"):
        public_text = path.read_text(encoding="utf-8")
        assert "/home/" not in public_text and ".cron/" not in public_text
        assert "theorem_complete=true" not in public_text

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
