#!/usr/bin/env python3
"""Fail-closed validation packet checker for S56-M-1143-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1143"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLT_REGULAR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"

ITEM = "S56-M-1143-VALIDATION"
THEOREM = "THM-M-1143"
BASE_REVISION = "53dced5833f17a55f667239e756fc93c99810c44"
BASE_TREE = "f0c4bdb31a84f0b4221b8392c9c95be1441914dc"
EXPRESSION_SHA256 = "e05a7b951bf36aedbc370a3f6ad2950c86b63b4d3a8af1d0e031290b62701610"
DENOMINATOR_SHA256 = "af64903cdbdaa77c2ffcbbbf20f444870b91f6e032643c3994d35d2688c20eb7"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
LEAN_PATH_ENTRIES = [
    "Cli/.lake/build/lib/lean",
    "batteries/.lake/build/lib/lean",
    "Qq/.lake/build/lib/lean",
    "aesop/.lake/build/lib/lean",
    "proofwidgets/.lake/build/lib/lean",
    "importGraph/.lake/build/lib/lean",
    "LeanSearchClient/.lake/build/lib/lean",
    "plausible/.lake/build/lib/lean",
    "checkdecls/.lake/build/lib/lean",
    "mathlib/.lake/build/lib/lean",
]
EXPECTED_INPUTS = {
    "Statement.lean": "a4ed1193c0c91ec8ba4237e46e2dbee38da52d143919f549f96616c2e05589bd",
    "ObligationTree.lean": "75ab2460c3f80b62566b8751d57c92e2d46f49c776c2c82cc05a2373e1a25991",
    "Proof.lean": "3dd0bab66a89e6408534ef0aa48eb712b3b1cd8c92fc420c7508ac2e97f24d11",
    "anchor-audit.json": "18436db648ceaf7e83be659af50cc18c6daa3fcc01abaa54539889e0805834df",
    "obligation-registry.json": "20e66e86a932c2e56fe73373a62707b32a869a37930c9c2ffa7986e7350927fd",
    "typed-graphs.json": "62416cc42ed04fe300b3ae4a90674f6301f6c2d8bbe6f7c4f1690dd863cbf414",
    "validation-specs.json": "cf7643db42ea0863211941fa8918c478fdbe14a3da3324fcfec40a9379edadb9",
    "task-dag.json": "c6b22e03f97c8f9aae26fb232d9e37e5c4446b0a52568ee38d6bb8f7b9837671",
    "instance.json": "7408ab5fb7af6b5acc90d171b9b0ceeba2d9d7e07155c45d8d2ccf348bd36406",
    "statement.json": "e88420bb218e8a2ade2c43028dea16d14619c685bf939ccf0a3000f456d2a71f",
    "scope-map.md": "f379aea0cc5f7c07e5c4e5af6fe9e02639a19e1135643bb4c296ab16d9a4f9a8",
    "source-statement-crosswalk.md": "cde4fa9d954301008cb17a1ac264a383ab1a45af0f1b3add2b6f4c20e26fe2f2",
    "proof-receipt.json": "2d1263e1b503891a6df959d745b884e68a10efcbb44c85f75bfe799d793e2910",
    "proof-blocker.json": "720e734c0362fa258388c3bf748e181d1b341a2734e6c84ba72c8ad0441337a3",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = [
    "PASS network-isolated trust-zero replay: statement, conditional composition, seven proof declarations, and two import-dependent probes elaborated",
    "PASS trust observation: nine unique local declarations use exactly propext, Classical.choice, and Quot.sound",
    "PASS validation packet structure, frozen hashes, manifest/source pins, source hygiene, and negative gate decisions",
    "FAIL CLOSED source identity and exact root: H4 source evidence and M1143-L-GRADIENT remain open",
    "FAIL CLOSED complete trust/provenance and cold hermetic replay: shared canonical .lake is warm, mutable, and incomplete",
    "FAIL CLOSED independent verification: no second signed clean runner or independently implemented minimal verifier",
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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 60) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


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


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 348 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 348,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1143-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1143-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert local_dag["accepted_states"] == []
    assert instance["lifecycle"] == "planned"
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert statement["printed_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1143-ROOT")
    assert root_node["machine_debt"] == "M3"
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == ["M1143-T-VANISH"]
    assert proof_blocker["first_unavailable_substantive_leaf"] == "M1143-L-GRADIENT"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_pin = next(row for row in manifest["packages"] if row["name"] == "«flt-regular»")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert flt_pin["rev"] == flt_pin["inputRev"] == FLT_REGULAR_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert FLT_REGULAR.is_dir()

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
    validation = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert validation.startswith("import Proof\n")
    for fragment in (
        "theorem uniformAbsBoundDirect",
        "theorem continuousLinearMapEqZeroDirect",
        "#check BoundedHarmonicIsConstant",
        "#check root_of_interiorGradientEstimate",
    ):
        assert fragment in validation

    lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
    assert lean.is_file()
    lean_path = ":".join(
        [str(LEAN_ROOT / ".lake" / "packages" / relative) for relative in LEAN_PATH_ENTRIES]
        + [str(LEAN_ROOT / ".lake" / "build" / "lib" / "lean"), str(lean.parents[1] / "lib" / "lean")]
    )
    bwrap = shutil.which("bwrap")
    assert bwrap is not None
    with tempfile.TemporaryDirectory(prefix="m1143-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
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
            "--chdir", str(tmp),
        ]
        run(base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-o", "Statement.olean", "Statement.lean"], timeout=180)
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base + module_env + [str(lean), "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean"], timeout=180)
        proof_output = run(base + module_env + [str(lean), "--trust=0", "-o", "Proof.olean", "Proof.lean"], timeout=180)
        validation_output = run(base + module_env + [str(lean), "--trust=0", "Validation.lean"], timeout=180)

    allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
    for declaration in (
        "exists_uniform_abs_bound",
        "exists_nonnegative_uniform_abs_bound",
        "continuousLinearMap_eq_zero_of_norm_le_div",
        "vanishingDerivativePackage_of_interiorGradientEstimate",
        "zeroDerivativeConstantPackage",
        "root_of_vanishingDerivativePackage",
        "root_of_interiorGradientEstimate",
    ):
        assert printed_axioms(proof_output, declaration) == allowed_axioms
    for declaration in ("uniformAbsBoundDirect", "continuousLinearMapEqZeroDirect"):
        assert printed_axioms(validation_output, declaration) == allowed_axioms
    assert printed_axioms(validation_output, "root_of_interiorGradientEstimate") == allowed_axioms
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == {
        "M1143-S-STATEMENT", "M1143-N-BOUND", "M1143-L-LIMIT",
        "M1143-L-CONSTANT", "M1143-T-ASSEMBLE",
    }

    if os.environ.get("STAGE1_VALIDATION_CHILD") == "1":
        for line in SUMMARY_LINES:
            print(line)
        return

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H4", "M": "M3", "R": "R4"
    }
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "S56-M1143-X-SOURCE-IDENTITY"
    assert receipt["remaining_root_cut_set"] == ["M1143-X-SOURCE", "M1143-L-GRADIENT"]
    assert receipt["results"]["kernel_replay"] == "pass_network_isolated_trust_zero_warm_cache"
    assert receipt["results"]["kernel_output_sha256"] == {
        "Statement.lean": "e05a7b951bf36aedbc370a3f6ad2950c86b63b4d3a8af1d0e031290b62701610",
        "ObligationTree.lean": "20d57a1ee980c0bcacd9bebf504d97940b6f315f9f6b05b3d8449ec9eb719d44",
        "Proof.lean": "2de4c5bbaaf5a8df0fb2db760876fe6e9d6be995a300c419d6f16d58682c90cb",
        "Validation.lean": "1fc4284a5b25f79a13719937f30a1604b081c00bfc247d6b18b550c9caf40ce2",
    }
    assert receipt["results"]["exact_root"] == "open_M3"
    assert receipt["results"]["independent_verification"] == "fail_closed"
    assert receipt["recipe"]["argv"] == spec["argv"]
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation_source_sha256"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation_blocker_sha256"] == sha256(HERE / "validation-blocker.json")
    assert receipt["inputs"]["validation_phase_sha256"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["check_validation_sha256"] == sha256(HERE / "check_validation.py")
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected

    assert blocker["item_id"] == ITEM and blocker["outcome"] == "validation_self_tested_gates_blocked"
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == receipt["known_failures"]

    replay_env = os.environ.copy()
    replay_env["STAGE1_VALIDATION_CHILD"] = "1"
    replay = subprocess.run(
        spec["argv"],
        cwd=ROOT / spec["cwd"],
        env=replay_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=spec["timeout_seconds"],
        check=False,
    )
    assert replay.returncode == spec["expected_exit"], replay.stdout
    assert replay.stdout == "".join(f"{line}\n" for line in SUMMARY_LINES)

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
