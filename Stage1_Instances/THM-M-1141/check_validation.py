#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1141-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1141"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1141-VALIDATION"
THEOREM = "THM-M-1141"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
DENOMINATOR_SHA256 = "6f4e5fa64e6d8750ab7592a5b54a269a3b0759b480fae5c802c9740e5daef2d1"
SOURCE_PDF_SHA256 = "4e64124f7e36993ee784e575a024505f99d484ccf959d2d3864eae9232af8bf1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "07b60266780d55e9a3edda48f46d4c6fc38200f133636c62eebf979f1640ea22",
    "ObligationTree.lean": "cdc326dfb76fd6152bdfae157121554dac52590338adf371fa3d78bbb9a86700",
    "Proof.lean": "595c2853af2d99906b009d778a36bdb88e0e8b6f6f2ca44fd08700815f97647d",
    "Validation.lean": "8c6d5ace89ee884290bf14cd0c9ddd984463c82bf174cbccbe3944b1a4053e73",
    "anchor-audit.json": "63e24ee90613f872c4fd07407f81952dcd6a4ffe9a5881927f64c15ca62a9283",
    "obligation-registry.json": "70a9e0f9948086bbb9c7559ac2298fe9b375162d21f1d7dbb18143d0c15e3b3a",
    "typed-graphs.json": "e53722ede3a729b0ed135d684a861f359ad392e820142a512dffabe337660a6d",
    "validation-specs.json": "51b4f09fd1b194446c027fa1df42eb2be81f8f9bfcc487474f60ca03cb715dae",
    "task-dag.json": "ea35e682a42bb793c41728bf3625593ab0a604a1cd29ee3b7ed83b00ca374530",
    "instance.json": "3dd3731592ae2a48ab3406a3b34eab3feb56acbbdc5641c66d8011d4361423da",
    "scope-map.md": "80ac8fceea544dd1c24cbe0437f557d397fd8af9b2ec3305cced936b49d888dd",
    "source-statement-crosswalk.md": "c599c3b451cb3a25790e0e10e36453c3239a4eb0e2291754854f87aa6f629bfc",
    "proof-validation.md": "75416e8b5c5d45fc8f43fb13d2b68237d4b971047d19c67658af0e265cf4f96c",
    "validation-spec.json": "39db19d5819f7dc7fec431a19b62f76e5aeeaeb4a8dc3f5700dfeea777534bdf",
}
OPEN_ROOT_CUT = [
    "source statement: add 2 <= n or check a low-dimensional extension",
    "M1141-L-LOCAL",
    "M1141-C-COVER",
    "M1141-C-CHAIN",
    "M1141-T-UNIFORM",
    "M1141-X-TRUST",
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
    "PASS narrow kernel replay: statement, conditional composition, proof-phase packages, and import-dependent probes elaborated at trust zero",
    "PASS trust observation: five unique declarations across seven reports have exactly propext, Classical.choice, and Quot.sound",
    "PASS local provenance: frozen hashes, denominator, toolchain pins, and clean pinned mathlib revision agree",
    "FAIL CLOSED exact source identity: the selected source fixes n > 1, but Statement.lean quantifies every n : Nat",
    "OPEN exact root: local analytic Harnack, compact cover/chain, and uniform comparison remain unproved at M3",
    "FAIL CLOSED release gates: shared warm .lake, incomplete TCB/SBOM provenance, and no distinct independent runner",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=360,
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
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 346 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 346,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1141-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1141-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_proof = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-1141-PROOF"
    )
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == ITEM
    )
    assert local_proof["state"] == local_validation["state"] == "open"

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert frozen_specs["item_id"] == "S56-M-1141-OBLIGATION_TREE"
    assert all(
        row["state"] == "open"
        for row in frozen_specs["recipes"]
        if row["obligation_id"] in {"M1141-L-POSITIVE", "M1141-L-PROPAGATE"}
    )
    assert not (HERE / "proof-receipt.json").exists()

    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    scope_map = (HERE / "scope-map.md").read_text(encoding="utf-8")
    assert "forall (n : Nat)" in statement_source or "\u2200 (n : Nat)" in statement_source
    assert "arbitrary `n`" in scope_map and "zero-dimensional" in scope_map
    assert SOURCE_PDF_SHA256 in (HERE / "source-statement-crosswalk.md").read_text(
        encoding="utf-8"
    )

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
    validation_source = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert validation_source.startswith("import Proof\n")
    assert "positiveDenominatorsDirect" in validation_source
    assert "comparisonChainEndpointDirect" in validation_source
    assert "UniformValueComparison" not in re.sub(
        r"#check UniformValueComparison", "", validation_source
    ).replace("harnackInequality_of_analytic_package", "")

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    assert LEAN_COMMIT in run([str(lean), "--version"])
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"])

    with tempfile.TemporaryDirectory(prefix="m1141-validation-", dir=LEAN_ROOT) as tmp_name:
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
            "--clearenv",
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN,
            "--chdir", str(tmp),
        ]
        run(base_command + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0",
            "-o", "Statement.olean", "Statement.lean",
        ])
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base_command + module_env + [
            str(lean), "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean",
        ])
        proof_output = run(base_command + module_env + [
            str(lean), "--trust=0", "-o", "Proof.olean", "Proof.lean",
        ])
        validation_output = run(base_command + module_env + [
            str(lean), "--trust=0", "Validation.lean",
        ])

    assert printed_axioms(
        obligation_output, "harnackInequality_of_uniformValueComparison"
    ) == EXPECTED_AXIOMS
    for declaration in (
        "positive_denominators_on_compact",
        "ComparisonChain.endpoint",
        "harnackInequality_of_analytic_package",
    ):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "positiveDenominatorsDirect",
        "comparisonChainEndpointDirect",
        "harnackInequality_of_analytic_package",
    ):
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 360
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == {
        "M1141-L-POSITIVE", "M1141-L-PROPAGATE", "M1141-T-RATIO"
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["depends_on"] == ["S56-M-1141-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt["debt_vector_change_proposed"] is False
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_1141.HarnackInequality",
        "statement_sha256": EXPECTED_INPUTS["Statement.lean"],
        "elaborated_expression_fingerprint": "missing_from_predecessor_statement_phase",
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "source_statement_identity": "fail_closed_dimension_scope_mismatch",
    }
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(Path(bwrap).resolve())
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    result = receipt["result"]
    assert result["declaration_kernel_replay"] == "pass"
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["source_statement_identity_gate"] == "fail_closed"
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "S56-5.1-EXACT-SOURCE-STATEMENT-IDENTITY"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["recipe"] == spec
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
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    status = git(
        "status", "--short", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert receipt["hygiene"]["direct_changed_file_scan"] == "pass"
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
