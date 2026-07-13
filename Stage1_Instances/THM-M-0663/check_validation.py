#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0663-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0663"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0663-VALIDATION"
THEOREM = "THM-M-0663"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
BASE_TREE = "ca999baf360c6ce2440bbc2c01aeb8d519269a90"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
STATEMENT_EXPRESSION_SHA256 = "2d5a051f2bc932f2b637928aaf63f6795621670cb9d9f13264e139dfe1074fbd"
DENOMINATOR_SHA256 = "0e54d5483488181af11d415bb6e29860b351fce14b297a02bd45d9ee269faf53"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "c0c75f33c97b50eac9d225fb75dc841819ab721690d2ae880b10ae591b31aa40",
    "ObligationTree.lean": "9ff6f3b60885a8df62b9a2679c41c284ca0f3b2fcff2c02c7c8841a7f6fffc76",
    "Proof.lean": "5f17bf17801abaaac0ac80acb037a8293759ec9ba6b235ee8e29e0400fc65704",
    "statement.json": "cbad8f956f3c32ac253b46f2025932964178552bf27b6689b6643c0e33131086",
    "anchor-audit.json": "28fff486624d15ece90074d871a34dfb1ca85257fcedf5068c40208fde6f8b27",
    "obligation-registry.json": "128eb58b83f86922775ffbc83df0553159beb35b1eede52e872c5359cfdd4541",
    "typed-graphs.json": "d464b63227b1019e13a8f652224d9f74e95301ab168851ea06c8640c38584a65",
    "validation-specs.json": "40a8ec6015985ae040f32d54efa2a812343e8f82735fb646e10e1133221cb63c",
    "proof-validation.md": "6c5658509ed424608074ba66553af8004f7fecad5940af147ee4bc89533e88a1",
}
OPEN_ROOT_CUT = [
    "M0663-N-DOMAIN",
    "M0663-L-LOCAL-CONT",
    "M0663-L-LOCAL-ORDER",
    "M0663-L-FINITENESS",
    "M0663-X-SOURCE",
    "M0663-X-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = [
    "PASS kernel replay: exact statement boundary, conditional identity, proof-phase declarations, and same-worker direct reconstruction elaborated",
    "PASS trust observation: five checked declarations report exactly propext, Classical.choice, and Quot.sound",
    "PASS local provenance: frozen hashes, denominator, toolchain pins, and clean pinned mathlib agree; no proof receipt exists",
    "OPEN exact root and node identity: the monotonicity root is M3, and the frozen degenerate obligation exceeds the two checked declarations",
    "FAIL CLOSED release gates: shared warm .lake, incomplete TCB/SBOM provenance, and no distinct independent runner",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms: \[(.*?)\]",
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 707 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 707,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0663-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0663-PROOF")
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0663-PROOF"]

    assert instance["root_vector"] == {"H": "H3", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure == {
        "root_closed": False,
        "machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": OPEN_ROOT_CUT,
    }

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256

    degenerate = next(
        row for row in registry["obligations"]
        if row["obligation_id"] == "M0663-B-DEGENERATE"
    )
    assert degenerate["statement_fingerprint"].startswith("planned:v1:")
    assert degenerate["terminal_proof_body_id"] is None
    degenerate_node = next(
        row for row in graphs["nodes"]
        if row["obligation_id"] == "M0663-B-DEGENERATE"
    )
    assert "nondegenerate branch split exhaustive" in degenerate_node["human_statement"]
    assert degenerate_node["formal_target"].endswith("emptyDomainPartition")
    assert degenerate_node["evidence_ids"] == []
    assert not (HERE / "proof-receipt.json").exists()
    assert frozen_specs["item_id"] == "S56-M-0663-OBLIGATION_TREE"
    frozen_recipe = next(
        row for row in frozen_specs["recipes"]
        if row["obligation_id"] == "M0663-B-DEGENERATE"
    )
    assert frozen_recipe["state"] == "provisional" and "argv" not in frozen_recipe

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in differential and "import ObligationTree" not in differential
    assert "partitionOfSubsingletonDirect" in differential

    manifest_record = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest_record["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    assert LEAN_COMMIT in run([str(lean), "--version"])
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"])

    with tempfile.TemporaryDirectory(prefix="m0663-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_command = [
            bwrap,
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN,
            "--chdir", str(tmp),
        ]
        run(
            base_command + ["--setenv", "LEAN_PATH", lean_path, str(lean),
                            "-t", "0", "-o", "Statement.olean", "Statement.lean"]
        )
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(
            base_command + module_env + [str(lean), "-t", "0", "ObligationTree.lean"]
        )
        proof_output = run(
            base_command + module_env + [str(lean), "-t", "0", "Proof.lean"]
        )
        validation_output = run(
            base_command + module_env + [str(lean), "-t", "0", "Validation.lean"]
        )

    assert printed_axioms(obligation_output, "root_of_partition_package") == EXPECTED_AXIOMS
    for declaration in ("partition_of_subsingleton", "partition_empty"):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in ("partitionOfSubsingletonDirect", "partitionEmptyDirect"):
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == ["M0663-B-DEGENERATE"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0663-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(Path(bwrap).resolve())
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    result = receipt["result"]
    assert result["declaration_kernel_replay"] == "pass"
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_kernel_closed"] is False
    assert result["root_machine_classification"] == "M3"
    assert result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0663-PROOF.master_acceptance"
    assert receipt["first_failed_mathematical_gate"] == "proof.node_exact_identity_and_root_kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["recipe"]["argv"] == spec["argv"]
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
