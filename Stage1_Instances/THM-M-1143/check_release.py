#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1143-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1143"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1143-RELEASE"
THEOREM = "THM-M-1143"
BASE_REVISION = "4990a9d6fa09beb7747e6822c6543c6123ca7504"
BASE_TREE = "b74497bc09c004757aa3974f3bb0622d77e20106"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "e05a7b951bf36aedbc370a3f6ad2950c86b63b4d3a8af1d0e031290b62701610"
DENOMINATOR_SHA256 = "af64903cdbdaa77c2ffcbbbf20f444870b91f6e032643c3994d35d2688c20eb7"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1143-ROOT", "M1143-S-STATEMENT", "M1143-S-FOUNDATION",
    "M1143-N-BOUND", "M1143-L-GRADIENT", "M1143-L-LIMIT",
    "M1143-T-VANISH", "M1143-L-CONSTANT", "M1143-T-ASSEMBLE",
    "M1143-X-PLANE", "M1143-X-SOURCE", "M1143-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "a4ed1193c0c91ec8ba4237e46e2dbee38da52d143919f549f96616c2e05589bd",
    "ObligationTree.lean": "75ab2460c3f80b62566b8751d57c92e2d46f49c776c2c82cc05a2373e1a25991",
    "Proof.lean": "3dd0bab66a89e6408534ef0aa48eb712b3b1cd8c92fc420c7508ac2e97f24d11",
    "Validation.lean": "ff55ed6d6b8a5c5d58cd3314b871a641a14788df1bba4093f88694c825cc408d",
    "instance.json": "7408ab5fb7af6b5acc90d171b9b0ceeba2d9d7e07155c45d8d2ccf348bd36406",
    "task-dag.json": "c6b22e03f97c8f9aae26fb232d9e37e5c4446b0a52568ee38d6bb8f7b9837671",
    "statement.json": "e88420bb218e8a2ade2c43028dea16d14619c685bf939ccf0a3000f456d2a71f",
    "scope-map.md": "f379aea0cc5f7c07e5c4e5af6fe9e02639a19e1135643bb4c296ab16d9a4f9a8",
    "source-statement-crosswalk.md": "cde4fa9d954301008cb17a1ac264a383ab1a45af0f1b3add2b6f4c20e26fe2f2",
    "anchor-audit.json": "18436db648ceaf7e83be659af50cc18c6daa3fcc01abaa54539889e0805834df",
    "obligation-registry.json": "20e66e86a932c2e56fe73373a62707b32a869a37930c9c2ffa7986e7350927fd",
    "typed-graphs.json": "62416cc42ed04fe300b3ae4a90674f6301f6c2d8bbe6f7c4f1690dd863cbf414",
    "validation-specs.json": "cf7643db42ea0863211941fa8918c478fdbe14a3da3324fcfec40a9379edadb9",
    "proof-receipt.json": "2d1263e1b503891a6df959d745b884e68a10efcbb44c85f75bfe799d793e2910",
    "proof-blocker.json": "720e734c0362fa258388c3bf748e181d1b341a2734e6c84ba72c8ad0441337a3",
    "proof-validation.md": "666c27c3643cd632c302198a644da27c0b6b8d8dbbb1194a3cb197fd6ab17973",
    "validation-spec.json": "885e4e4e2f2500f4f3957d03ef57f7eeebde71a22d5a3efdf942563c3cf39184",
    "validation-receipt.json": "937edef379e768a98c164254e22ebec7bf3a53bd462950876fb55687779f0d08",
    "validation-blocker.json": "89d6974f851235b0d38f952b5704f81c3466330fe3d02a359b6755fb1a19e2ab",
    "validation-phase.md": "8931f363752824a1711e15ee5f5fd5c0553e55e9c8dae4b8663fb263e1a3d61f",
    "check_validation.py": "da0c6bf054b2481a93159517d62d5fb2b90d29da25675d14ba8b1b87021ef24e",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SUMMARY_LINES = [
    "release-decision: ok (blocked at validation dependency acceptance)",
    "narrow Lean replay: ok (warm-cache trust-zero; exact root remains open M3)",
    "authoritative vector: H4/M4/R4 unchanged; best provisional vector: H4/M3/R4",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]",
    "first mathematical cut: M1143-L-GRADIENT",
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
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output, flags=re.DOTALL,
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
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=60)

    with tempfile.TemporaryDirectory(prefix="m1143-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN,
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]
        run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0",
            "-o", "Statement.olean", "Statement.lean",
        ], timeout=300)
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean",
        ], timeout=300)
        proof_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "Proof.olean", "Proof.lean",
        ], timeout=300)
        validation_output = run(base + module_env + [
            str(lean), "--trust=0", "Validation.lean",
        ], timeout=300)

    assert "sorryAx" not in obligation_output + proof_output + validation_output
    for declaration in (
        "exists_uniform_abs_bound",
        "exists_nonnegative_uniform_abs_bound",
        "continuousLinearMap_eq_zero_of_norm_le_div",
        "vanishingDerivativePackage_of_interiorGradientEstimate",
        "zeroDerivativeConstantPackage",
        "root_of_vanishingDerivativePackage",
        "root_of_interiorGradientEstimate",
    ):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in ("uniformAbsBoundDirect", "continuousLinearMapEqZeroDirect"):
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    validation_blocker = load(HERE / "validation-blocker.json")
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
    assert target["execution_rank"] == 348 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 348,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1143-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1143-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert statement["printed_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert proof["result"]["root_closed"] is False
    assert proof["first_unavailable_substantive_leaf"] == "M1143-L-GRADIENT"
    assert proof_blocker["first_unavailable_substantive_leaf"] == "M1143-L-GRADIENT"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["results"]["exact_root"] == "open_M3"
    assert validation["audit_complete"] is validation["theorem_complete"] is False
    assert validation_blocker["root_kernel_gate"]["state"] == "open_M3"
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H4", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

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
    assert (
        result["authoritative_recorded_root_vector_before"]
        == result["authoritative_recorded_root_vector_after"]
        == [
        "H4", "M4", "R4"
        ]
    )
    assert result["best_provisional_root_vector"] == ["H4", "M3", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_substantive_gate"]["obligation_id"] == "M1143-X-SOURCE"
    assert result["first_failed_root_kernel_gate"]["obligation_id"] == "M1143-L-GRADIENT"
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("assert_no_sorry", "")
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    replay_lean()

    assert spec["recipe_id"] == "S56-M-1143-RELEASE-NARROW-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["inputs"]["release_validation_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["inputs"]["check_release_sha256"] == sha256(HERE / "check_release.py")

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
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

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
