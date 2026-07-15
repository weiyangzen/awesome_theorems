#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0819-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0819"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0819-VALIDATION"
THEOREM = "THM-M-0819"
BASE_REVISION = "9d50d838c8132b2aaf005a4863baeb5385e52a97"
BASE_TREE = "ef268baf236c1fe55806a57847c7f78ed6587b9d"
EXPRESSION_SHA256 = "bdf0aa8f8adac4be9bf2080951be62eac168872b8c589a804ac8587c1878bb19"
STATEMENT_BUNDLE_SHA256 = "df437e79e306cbbdca0f9344a6a953a7f27886a197db7c614b995c846f8a2195"
DENOMINATOR_SHA256 = "3e19428b16575891198438f798957373f440bf15623c22c44df4c1f69239742c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_IDS = [
    "M0819-ROOT",
    "M0819-S-TRANSPORT",
    "M0819-N-FINITE-RESTRICTION",
    "M0819-N-COLORING",
    "M0819-B-WIDTH-ZERO",
    "M0819-B-WIDTH-POSITIVE",
    "M0819-C-LOCAL-COLORINGS",
    "M0819-L-FINITE-DILWORTH",
    "M0819-B-FINITE-INDUCTION",
    "M0819-C-ADJOIN-ELEMENT",
    "M0819-L-LOW-WIDTH-INDEX",
    "M0819-L-DUAL-INDEX",
    "M0819-X-FINITE-TAIL",
    "M0819-L-FINITE-EXACTNESS",
    "M0819-L-RADO-SELECTION",
    "M0819-C-GLOBAL-COLORING",
    "M0819-L-GLOBAL-PROPER",
    "M0819-C-COLOR-CLASSES",
    "M0819-L-FIBERS-CHAIN",
    "M0819-L-UNIQUE-MEMBERSHIP",
    "M0819-T-POSITIVE-ASSEMBLE",
    "M0819-T-WIDTH-BRANCHES",
    "M0819-T-ROOT-ASSEMBLE",
]
TRUST_DECLARATIONS = [
    "minAntichainPartition_eq_chainHeight",
    "minChainPartition_eq_antichainWidth",
    "Stage1Instances.THM_M_0819_Proof.dilworthPrimary",
]
VALIDATED_DECLARATIONS = [
    "Stage1Instances.THM_M_0819.DilworthPrimaryTarget",
    *TRUST_DECLARATIONS,
]
EXPECTED_INPUTS = {
    "Statement.lean": "c3e600a4a5c2b48686bf244915aea79972e4537a2d89120ad739018716056b52",
    "FiniteDilworth.lean": "825275407850c60f8fe1417a2cee408fb262b60f26eaa9ab30662ea46829e2c1",
    "Proof.lean": "c64e830b6c1a8770319bdaf9549dcd0a8a557da6710272c127560a931da8cd22",
    "LICENSE": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    "statement.json": "56d8c2af848287eab330da7497ad4fb5039a6305d4584e68415863cc6e0edf7c",
    "instance.json": "5e15e8b602d128fe9e525b36449b8b11de806127a0aff119fbe81b2c0b91f935",
    "task-dag.json": "7fd03c20aa1a8a9e0290047013529431e24aaceb76dfd204ddbe27b0f35007e6",
    "anchor-audit.json": "a97aa82bbe42e49bee4a689d477ed9d574bbf8680b15feedf2c12fb508da85b1",
    "obligation-tree.md": "b4b8ea59b87792094976bb5852472a6cf283f18a67ec1bd22a13e3d82da96ccd",
    "obligation-registry.json": "4ef75dba4309a4c59e46a6394c0eb9345ebfd0e90b483cee8eaeb73760667554",
    "typed-graphs.json": "1397445ffb49c0e099c5bc76c40a2c000edeea6ebfcf9da3191f3e846f5ba2d6",
    "validation-specs.json": "97b2d4f5fc07dfd514646bb6139a83cbe7df8ea1d1eda2abeb572a6c3df7d0aa",
    "source-statement-crosswalk.md": "906ef72ea36e0474348984a13ebaf8e98ca9c47ee60c52e6f3c2c1c4d5d09777",
    "proof-receipt.json": "266eae1986ace9ef8bb38bd8e13e3a929fe774aa660cd06cf167f64132453c56",
    "proof-validation.md": "b61cf67288d0c48d2bc6dc96de42d3f523c527e7b656a21ea95a59e12913bb75",
    "check_proof.py": "cdc11dc64ab9bef0ed3a63e531e5365a09c969dab295630f3024312a3ee29f97",
    "check_proof.sh": "252ce7e823e9ea7673859d8b9e2966bd8d38ccd347136844b77b68b263d80e67",
    "Validation.lean": "e997194630e857d27b38730ea5c1164c8a29ea06392234a885b9e8b67f168c39",
    "check_validation.sh": "58cc39e16c46e290d30dbc9d3babc4cd2cab75be6acb06162a9f6187795394ae",
    "validation-spec.json": "2fa93fe93ae061168e19b07cb056cb65a3174a307f7497706bb22fc2e4ac59d1",
    "validation-phase.md": "d7f881fc937543c172f84af54c50cafda68da1797a5149e7e1e435b6595e4936",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_POLICY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "c91cc845ae0a11e05c29fb0369e1f22fcb87280d2d1694529a72c14e2dce9b1b",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "42901f12234b012cad2a9c66eb251b26a67836304f68f1bfd1222abf14282e10",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0819 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact statement, finite proof, arbitrary-poset root, and proof-only trust probe elaborated",
    "PASS hygiene: Lean transitive sorry collectors and a nested-comment-aware prohibited-construct scan passed",
    "PASS selected provenance: frozen local hashes, proof-body identity, finite port/license, Rado source/olean, clean mathlib pin, and tool identities agree",
    "FAIL CLOSED authority: proof is provisional and instance/task/registry/graph authorities are unreconciled; accepted root remains H1/M3/R3",
    "FAIL CLOSED node coverage: planned fingerprints, missing terminal body/evidence links, and absent accepted composition require master reconciliation",
    "FAIL CLOSED foundation/trust: observed axioms are unaccepted and complete transitive declaration, compiled-artifact, and TCB closure are absent",
    "FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache clean-checkout offline replay or deterministic bundle",
    "FAIL CLOSED independent release: trust-only probe shares this worker, checkout, kernel, and cache; no distinct signed runner or minimal verifier exists",
    "audit_complete=false; theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def elan_binary(name: str) -> Path:
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    result = subprocess.run(
        ["elan", "which", name],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"cannot resolve pinned {name}: {result.stdout}")
    path = Path(result.stdout.strip())
    assert path.is_file(), f"pinned {name} executable missing"
    return path


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1377 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1377
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0819-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Run hermetic kernel, trust, provenance, and independent validation gates."
    )
    assert item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )
    assert item["attempts"] == 0 and item["children"] == []
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0819-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    for name, expected in EXPECTED_POLICY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"changed policy input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0819.DilworthPrimaryTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_bundle_sha256"] == STATEMENT_BUNDLE_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert "M0819-X-TRUST" in closure["remaining_release_cut_set"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    # The intake-era authorities intentionally remain unreconciled and therefore fail closed.
    assert instance["canonical_formal_target"]["declaration_or_expression"] is None
    assert instance["obligation_registry_hash"] is None
    assert instance["theorem_complete"] is False
    assert all(row["state"] == "open" for row in task_dag["tasks"])

    assert proof_receipt["item_id"] == "S56-M-0819-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["provisionally_closed_obligation_ids"] == MACHINE_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["root_source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["finite_source_sha256"] == EXPECTED_INPUTS["FiniteDilworth.lean"]
    assert proof_receipt["proof_body"]["license_sha256"] == EXPECTED_INPUTS["LICENSE"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert any(
        row["statement_fingerprint"].startswith("planned:v1:")
        for row in registry["obligations"]
    )
    graph_nodes = graphs["nodes"]
    assert all(not node["evidence_ids"] for node in graph_nodes)
    assert next(
        node for node in graph_nodes if node["obligation_id"] == "M0819-X-TRUST"
    )["machine_debt"] == "M4"
    assert frozen_specs["item_id"] == "S56-M-0819-OBLIGATION_TREE"

    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "yet justify `H0`" in crosswalk and "no independent" in crosswalk
    proof_notes = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "independently accepted R0" in proof_notes

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "FiniteDilworth.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" in validation
    assert "theorem " not in validation and "def " not in validation
    for declaration in TRUST_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation
        assert f"#print sorries {declaration}" in validation
        assert f"#print axioms {declaration}" in validation

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    compactness = "Mathlib/Combinatorics/Compactness.lean"
    assert git("rev-parse", f"HEAD:{compactness}", cwd=MATHLIB) == (
        "a605b18dd914ece8c37f60356c138feead87ccc4"
    )
    assert sha256(MATHLIB / compactness) == (
        "743f441a1a18edb0a56b7b7d50def3a9ab9916ad14716f859a91ca43563a16a9"
    )
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/Compactness.olean"
    ) == "d0c938cfb1412f09f901012db4d2906cd6ae7f87830b31d1025fbd28ca672b67"
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = elan_binary("lean")
    lake = elan_binary("lake")
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    lake_version = run([str(lake), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    tools = {
        "lean": lean,
        "lake": lake,
        "elan": Path(os.path.realpath(shutil.which("elan") or "")),
        "python": Path(os.path.realpath(sys.executable)),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bash": Path(os.path.realpath(shutil.which("bash") or "")),
        "bubblewrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
        "timeout": Path(os.path.realpath(shutil.which("timeout") or "")),
    }
    expected_tools = {
        "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        "elan": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
        "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
        "timeout": "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0",
    }
    assert {name: sha256(path) for name, path in tools.items()} == expected_tools

    kernel_output = run(["bash", str(HERE / "check_validation.sh")])
    assert kernel_output.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    assert "declaration uses 'sorry'" not in kernel_output
    assert "sorryAx" not in kernel_output and "error:" not in kernel_output
    for declaration in TRUST_DECLARATIONS:
        assert observed_axioms(kernel_output, declaration) == EXPECTED_AXIOMS
    assert hashlib.sha256(kernel_output.encode()).hexdigest() == (
        "5ce0375f67c0df938040d573b58b9f705dd90f1524a74c67ccc2570787d4ddb3"
    )
    assert len(kernel_output.encode()) == 943 and len(kernel_output.splitlines()) == 13

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert set(spec["env_allowlist"]) == {
        "PATH", "HOME", "PYTHONPATH", "LANG", "LC_ALL", "TZ", "LEAN_NUM_THREADS"
    }
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["covered_declarations"] == VALIDATED_DECLARATIONS
    assert receipt["recipe"] == spec

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0819-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["canonical_target"]["statement_bundle_sha256"] == STATEMENT_BUNDLE_SHA256
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["validated_declarations"] == VALIDATED_DECLARATIONS
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert receipt["inputs"][f"Formalizations/Lean/{name}"] == expected, name
    for name, expected in EXPECTED_POLICY_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    untracked_hashes = receipt["environment"]["worktree_state"][
        "untracked_input_sha256"
    ]
    assert set(untracked_hashes) == CHANGED_PATHS - {
        f"Stage1_Instances/{THEOREM}/validation-receipt.json"
    }
    for relative, expected in untracked_hashes.items():
        assert sha256(ROOT / relative) == expected, relative
    result = receipt["result"]
    assert result["kernel_output_sha256"] == hashlib.sha256(kernel_output.encode()).hexdigest()
    assert result["kernel_output_bytes"] == len(kernel_output.encode()) == 943
    assert result["kernel_output_lines"] == len(kernel_output.splitlines()) == 13
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["selected_provenance"] == "pass_with_incomplete_transitive_closure"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["instance_and_task_authority_reconciliation"] == "fail_closed"
    assert result["node_specific_proof_body_and_composition_mapping"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0819-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["trust"]["machine_reported_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["tcb_gate"] == "fail_closed"
    assert receipt["provenance"]["upstream_source_bytes_retained_in_dossier"] is False
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    independent = receipt["independent_validation"]
    assert independent["same_worker_trust_probe"] == "pass"
    assert independent["proof_independent_exact_root_probe"] is False
    assert independent["distinct_runner"] is independent["distinct_verifier_identity"] is False
    assert independent["release_gate"] == "fail_closed"
    assert receipt["root_vector_before"] == receipt[
        "root_vector_after_worker_selftest"
    ] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["freshness"]["revocation_state"] == "not_revoked"
    assert receipt["status_boundary"].startswith("Self-tested blocked validation-node evidence")

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"] == list(SUMMARY_LINES)
    assert receipt["known_failures"] == packet["known_failures"]

    link_target = os.readlink(LEAN_ROOT / ".lake").encode("utf-8")
    assert hashlib.sha256(link_target).hexdigest() == receipt["environment"][
        "worktree_state"
    ]["preexisting_untracked_link_target_sha256"]
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
