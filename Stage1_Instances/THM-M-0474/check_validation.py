#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0474-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0474"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0474-VALIDATION"
THEOREM = "THM-M-0474"
BASE_REVISION = "7a489588a59dbd7cca44de7e3b8c3bafcb7448f5"
BASE_TREE = "54d558bf8ed3ea71536ff6a7e6ac7ee67cccfe98"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
DENOMINATOR_SHA256 = "28dd518db2fe79a5006cbeb3fdd51b379f67cf388960c3f5fafdf2a7ad8b6a9e"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
CLOSED_IDS = {
    "M0474-ROOT",
    "M0474-T-COMPOSE",
    "M0474-L-NAT",
    "M0474-N-NAT-INT",
    "M0474-N-COPRIME",
    "M0474-L-INT",
    "M0474-C-ZMOD-NONZERO",
    "M0474-T-INT-ZMOD",
    "M0474-L-ZMOD",
    "M0474-T-ZMOD-CARD",
    "M0474-L-FINITE-FIELD",
    "M0474-C-UNIT",
    "M0474-L-GROUP-CARD",
}
VALIDATION_FILES = {
    "Validation.lean",
    "check_validation.py",
    "validation-spec.json",
    "validation-receipt.json",
    "validation-phase.md",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *{f"Stage1_Instances/{THEOREM}/{name}" for name in VALIDATION_FILES},
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM}/check_intake.py",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_statement.py",
    f"Stage1_Instances/{THEOREM}/instance.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if completed.returncode:
        raise SystemExit(
            f"validation command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def axiom_reports(output: str) -> list[set[str]]:
    blocks = re.findall(r"depends on axioms: \[(.*?)\]", output, flags=re.DOTALL)
    return [
        {name.strip() for name in block.split(",") if name.strip()}
        for block in blocks
    ]


def main() -> None:
    spec = load("validation-spec.json")
    receipt = load("validation-receipt.json")
    statement = load("statement.json")
    registry = load("obligation-registry.json")
    graphs = load("typed-graphs.json")
    proof_receipt = load("proof-receipt.json")
    instance = load("instance.json")
    dag = load("task-dag.json")
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
    )
    selftest = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 938,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0474-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and dag["accepted_states"] == []
    assert spec["item_id"] == receipt["item_id"] == selftest["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == selftest["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(selftest) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert selftest["state"] == "[_]"
    assert selftest["commands"] and selftest["output_summary"].startswith("PASS:")
    assert set(selftest["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS

    recipe = spec["recipes"]
    assert len(recipe) == 1
    recipe = recipe[0]
    assert receipt["recipe"] == recipe
    assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
    assert recipe["argv"] == ["python3", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["timeout_seconds"] == 120
    assert set(recipe["covered_obligation_ids"]) == CLOSED_IDS

    expected_inputs = {
        "Statement.lean": "67c859e7999fa793cdeb74493ff1ca2d3473174de5d2021786f0549bee254c43",
        "ObligationTree.lean": "4eba971fb779598d6678ce2f28d8c24b00d4266c1a4e7fa840b6d36c2b251e7e",
        "Proof.lean": "5862ada21b6c84ccd2c3c67a53419178b6bce2e15198a2a6a1727e65720c1ce8",
        "proof-receipt.json": "438a1a799141faa808ec17ccc780440889d3404b7ad8c59f913ff6f5daa650c0",
        "obligation-registry.json": "c5df064b9a9d2ab47034cb1b6e4b24adb59cd9351e0f4adceac7db965593fd3b",
        "typed-graphs.json": "5e26e72ba6129349ac39dcf7a7dccce050e8ef356c233b85c19985e69df87df8",
    }
    for name, expected in expected_inputs.items():
        assert digest(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"][name] == expected
    for name in ("Validation.lean", "validation-spec.json", "check_validation.py"):
        assert receipt["inputs"][name] == digest(HERE / name)

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
        HERE / "Statement.lean"
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(proof_receipt["closed_obligation_ids"]) == CLOSED_IDS
    assert proof_receipt["result"]["root_closed"] is True
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["accepted"] is False
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_debt"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited mechanism in {name}"
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "Nat.ModEq.pow_card_sub_one_eq_one" not in validation_source
    assert "Nat.ModEq.pow_totient" in validation_source
    assert "Nat.totient_prime hp" in validation_source

    assert digest(LEAN_ROOT / "lean-toolchain") == (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    )
    assert digest(LEAN_ROOT / "lake-manifest.json") == (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    )
    env = os.environ.copy()
    env.update(recipe["env_allowlist"])
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
    assert digest(lean) == LEAN_SHA256
    version = run([str(lean), "--version"], cwd=LEAN_ROOT, env=env)
    assert "4.29.0" in version and LEAN_COMMIT in version
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
    assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_REVISION
    assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=MATHLIB).strip() == MATHLIB_TREE
    assert run(["git", "status", "--porcelain=v1"], cwd=MATHLIB) == ""

    provenance = receipt["provenance"]
    provenance_files = {
        "Mathlib/FieldTheory/Finite/Basic.lean": (
            "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44",
            "fb3668d594f865e52f20c8af45e91e7e3b1eebd8",
        ),
        "Mathlib/GroupTheory/OrderOfElement.lean": (
            "42bef2580b87cd0fa6367cd2d57d30fb25fce373576a856cc84d27dad23fae23",
            "c2ac8b615cb093b89142094270478683ef67f1dc",
        ),
        "Mathlib/Data/Nat/Totient.lean": (
            "bc3be754c653d34785636ed734355fc5e976719b4eddf3cb7f37175265f1c20f",
            "107862af492eaf86037c3b62121e687b69d1e183",
        ),
    }
    for relative, (expected_sha, expected_blob) in provenance_files.items():
        source = MATHLIB / relative
        assert digest(source) == expected_sha
        assert run(["git", "hash-object", relative], cwd=MATHLIB).strip() == expected_blob
        assert provenance["sources"][relative] == {
            "sha256": expected_sha,
            "git_blob": expected_blob,
        }
    olean_files = {
        "Mathlib/FieldTheory/Finite/Basic.olean": "4cede73b3c7f85692307990d9cdaf819b5ac61dc50272e31586b7899d9f32119",
        "Mathlib/GroupTheory/OrderOfElement.olean": "33d0d5970b2ec79349ee6335e9f76842ff648e8594994ddd3da18ca8941c2858",
        "Mathlib/Data/Nat/Totient.olean": "e0f0c983aed45dd95fab75f06773eb7afe69f7ed1769071234b476a778bf69c6",
    }
    for relative, expected in olean_files.items():
        path = MATHLIB / ".lake/build/lib/lean" / relative
        assert digest(path) == expected
        assert provenance["oleans"][relative] == expected

    lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m0474-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name)
        for name in lean_files:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_env = env.copy()
        base_env["LEAN_PATH"] = lean_path
        outputs["Statement.lean"] = run(
            [str(lean), "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
            cwd=LEAN_ROOT,
            env=base_env,
        )
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        for name in lean_files[1:]:
            argv = [str(lean)]
            if name == "ObligationTree.lean":
                argv.extend(["-o", str(tmp / "ObligationTree.olean")])
            argv.append(str(tmp / name))
            outputs[name] = run(argv, cwd=LEAN_ROOT, env=module_env)

    proof_reports = axiom_reports(outputs["Proof.lean"])
    validation_reports = axiom_reports(outputs["Validation.lean"])
    assert len(proof_reports) == 18 and all(report <= EXPECTED_AXIOMS for report in proof_reports)
    assert len(validation_reports) == 3
    assert validation_reports[0] == EXPECTED_AXIOMS
    assert validation_reports[1] == EXPECTED_AXIOMS
    assert validation_reports[2] == EXPECTED_AXIOMS
    combined = "".join(outputs.values())
    assert combined.count("Declarations are sorry-free!") == 21
    assert "declaration uses 'sorry'" not in combined and "sorryAx" not in combined

    assert receipt["result"]["exit_code"] == 0
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["result"]["same_worker_differential_probe"] == (
        "pass_via_Nat_ModEq_pow_totient_without_importing_Proof_or_ObligationTree"
    )
    assert receipt["result"]["proof_dependency_master_accepted"] is False
    assert receipt["result"]["authoritative_graph_root_closed"] is False
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "validation.proof_dependency_master_acceptance"
    assert receipt["freshness"] == {
        "review_due": "before master acceptance and upon any invalidation input change",
        "supersession_state": "current provisional worker receipt",
        "revocation_state": "not_revoked",
        "incident_path": "master integration lane",
    }
    assert receipt["invalidation_inputs"]
    assert receipt["retry_condition"]
    assert receipt["status_boundary"].startswith("Self-tested worker evidence")
    assert receipt["known_failures"] == selftest["known_failures"]

    assert set(instance["owned_artifacts"]) == {path.name for path in HERE.iterdir() if path.is_file()}
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    semantic_output = "\n".join(
        (
            "PASS S56-M-0474-VALIDATION: exact proof root, frozen composition, and totient differential root kernel-replayed",
            "PASS trust observation: all checked proof routes are sorry-free and use only propext, Classical.choice, and Quot.sound",
            "PASS local provenance: frozen hashes, clean mathlib pin/tree, terminal sources, and oleans agree",
            "STALE authoritative graph: pre-proof M3 root awaits dependency-ordered master reconciliation",
            "BLOCKED proof dependency: S56-M-0474-PROOF is provisional rather than master-accepted",
            "BLOCKED hermetic gate: shared warm canonical .lake is not a cold empty-cache offline replay",
            "BLOCKED independent gate: differential source ran in this worker and shared cache, not a distinct signed runner",
        )
    )
    assert receipt["result"]["semantic_output_sha256"] == hashlib.sha256(
        semantic_output.encode("utf-8")
    ).hexdigest()
    print(semantic_output)


if __name__ == "__main__":
    main()
