#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0063-VALIDATION."""

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
import time
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0063"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0063-VALIDATION"
THEOREM = "THM-M-0063"
BASE_REVISION = "1944ddb6f503b699293e82f18d19efe0f32b4380"
BASE_TREE = "e5004bc50d7e6fae75e8332fb00748a57e3bf622"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a"
DENOMINATOR_SHA256 = "384a00c490054109773a2b786763af466971bd50c093a6facd39b614133b74a1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_STDOUT_SHA256 = "a7e628ab6f1a55ba1976e2b1cfa01a5e17aed40e1e3a260b8e091747262d35cf"
EXPECTED_INPUTS = {
    "Statement.lean": "37e52256a1a3d1e5e56a00888309b208d7f2c2ee1b45932ac761c5f01e3bf950",
    "ObligationTree.lean": "c6bd361bb9e2436b5dc078d742eda496f2b81d522c264375fd17adaf865d4e56",
    "Proof.lean": "3da42810ad8e78c3e61b0e8d2f1686f77ace2f637c15522228b09dad757917cf",
    "proof-receipt.json": "200db9b33a8e75ebf48731ae0f0b06d39815f4be294270fe434bfd1257eceb9f",
    "statement.json": "c816af26ce58a3828d874932f26d7291348e0261582fdd99fc329a3433e40e36",
    "obligation-registry.json": "d8bf96eb607d40b8cf7291ff5c0b807d4c51bd6ec1a99905c7bf2246284a26fc",
    "typed-graphs.json": "0787dd3457c91abe17460ee8cfbbdf6e8572e71461acef8ad7a972698c77486f",
    "validation-specs.json": "780facf7b2264880a459b1afff3eacd863b39c1182b9c245d465bb7ee18f7434",
    "anchor-audit.json": "8be880b75b3cfbcb97f20b96dd146a11d9bf79c1df00df78eaf46e9206debe03",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SOURCE_BOUNDARY = {
    "Mathlib/GroupTheory/Perm/Subgroup.lean": (
        "31512df634de3801bcc4802599139c5e90b84ff1",
        "342a5720c959ad335a6f8598ab52f2c12f2a6690f17dc64bfab7157929decd12",
        "941dcc68de2feed36e53da99a67ce1fd50a24228c05d32c606a0b8d82c995c3b",
    ),
    "Mathlib/Algebra/Group/Action/Basic.lean": (
        "af1f28cd06a114fb4e8c787c073a5c8277fa0a75",
        "ccdaa363f6e34addf9fb62664cc61795c32cee351569a205aba66c07363210ee",
        "68483445396f689fe3be014945dddf54aa42b86407a553cd1bba6987f3ffcc10",
    ),
    "Mathlib/Algebra/Group/Action/Faithful.lean": (
        "e64797f425d890654714b1dfefe59cb914ed3e28",
        "ca3171aea3a733052c36cb9d0883dce81bdd665a037f18ca8f50af9174f1e09a",
        "18a1fabd43071c3cc3d82d8feb10a6d1044b959c982316a813a87aa8e203de11",
    ),
    "Mathlib/Algebra/Group/Subgroup/Ker.lean": (
        "752cf3f7138cea3e653f3764cea5dcb6736293e0",
        "9269396e790bc8dcb0105cfb87897bff48fca981d62dd43e8c6840187217bfa1",
        "3417d59b00deaccd9a51e675da1dd4627a6f56e04d7080940eda7807d3e461ce",
    ),
    "Mathlib/Algebra/Group/Action/End.lean": (
        "8fde4399617920870a00a9feb595162da049a1f8",
        "befe42ad32661f6f92d22a27e876403849d8044e439c362e745c8d64ff142bda",
        "2f80b76aedab20f51417344cf0fbdc20db8619488d5ec28f7b3b9d6e9d2efedf",
    ),
}
PROOF_IDS = [
    "M0063-ROOT",
    "M0063-N-REGULAR",
    "M0063-C-PERM-HOM",
    "M0063-L-POINTWISE",
    "M0063-L-REGULAR-FAITHFUL",
    "M0063-L-INJECTIVE",
    "M0063-C-LEFT-INVERSE",
    "M0063-C-MRANGE-EQUIV",
    "M0063-N-MRANGE-RANGE",
    "M0063-T-GENERAL",
    "M0063-T-ASSEMBLE",
]
PROOF_DECLARATIONS = (
    "pointwiseFaithfulness",
    "regularFaithfulness",
    "permutationHomConstructor",
    "genericToPermInjectivity",
    "leftInverseConstructor",
    "mrangeEquivFromLeftInverse",
    "mrangeToRange",
    "generalFaithfulActionPackage",
    "regularSpecialization",
    "exactAssembly",
    "cayleyTheorem",
    "cayleyTheorem_pinned",
)
COMPOSITION_DECLARATIONS = (
    "genericInjectivity_of_pointwiseFaithfulness",
    "mrangeToRangeTransport",
    "generalPackage_of_components",
    "exactTarget_of_generalFaithfulAction",
    "exactAssembly_of_components",
    "root_of_exactAssembly",
)
TERMINAL_BODY_SHA256 = "ab83db4a51a8ac5e9f645c00385828f2cb1727ffec6dc2be542071ea583814e8"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0063 narrow validation",
    "PASS kernel replay: exact statement, all proof declarations, frozen compositions, two proof roots, and alternate exact-root adapter elaborated",
    "PASS trust observation: checked declarations depend only on propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, five source/blob/olean boundaries, clean mathlib pin, remote, license, and tool identities agree",
    "PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed",
    "FAIL CLOSED authority: proof master acceptance and structured state reconciliation are pending; accepted root remains H1/M3/R4",
    "FAIL CLOSED trust: M0063-S-FOUNDATION, an accepted theorem-specific foundation policy, and complete transitive declaration/TCB/SBOM closure remain open",
    "FAIL CLOSED hermetic/independent: shared warm .lake and same-worker adapter are neither cold offline replay nor distinct signed verification",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 180.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 180-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]",
        re.DOTALL,
    )
    match = pattern.search(output)
    if match is None:
        no_axioms = re.search(
            rf"'[^'\n]*{re.escape(declaration)}' does not depend on any axioms",
            output,
        )
        assert no_axioms is not None, declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


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
    proof_receipt = load(HERE / "proof-receipt.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1094 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1094,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0063-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0063-PROOF")
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0063-PROOF"]

    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_classification"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert proof_receipt["required_machine_open_ids"] == ["M0063-S-FOUNDATION"]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["accepted"] is False

    assert frozen_specs["item_id"] == "S56-M-0063-OBLIGATION_TREE"
    assert all(row["closure_credit"] is False for row in frozen_specs["recipes"])
    assert any(
        any(arg.endswith("check_obligation_tree.py") for arg in row["argv"])
        for row in frozen_specs["recipes"]
    )
    assert any(
        any(arg.endswith("build_obligation_artifacts.py") for arg in row["argv"])
        for row in frozen_specs["recipes"]
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in ("import Proof", "import ObligationTree", "Proof.", "cayleyTheorem_pinned"):
        assert forbidden not in differential, forbidden
    assert "MulEquiv.ofLeftInverse' (MulAction.toPermHom G G)" in differential
    assert "assert_no_sorry independentlyReconstructedTarget" in differential

    manifest_record = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest_record["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.is_dir(), "pinned mathlib artifacts are unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    for source_name, (blob_hash, source_hash, olean_hash) in SOURCE_BOUNDARY.items():
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == blob_hash
        assert sha256(MATHLIB / source_name) == source_hash, source_name
        olean_name = source_name.removesuffix(".lean") + ".olean"
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / olean_name
        assert sha256(olean) == olean_hash

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    assert git_path is not None
    git_executable = Path(os.path.realpath(git_path))
    assert LEAN_COMMIT in run([lean, "--version"])
    assert "5.0.0-src+98dc76e" in run([lake, "--version"])
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(git_executable) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"

    with tempfile.TemporaryDirectory(prefix="m0063-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_env = {
            "HOME": os.environ.get("HOME", ""),
            "PATH": os.environ.get("PATH", ""),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_PATH": lean_path,
        }
        run([lean, "-t", "0", "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=base_env)
        module_env = dict(base_env)
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-t", "0", "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run([lean, "-t", "0", "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "-t", "0", "Validation.lean"], cwd=tmp, env=module_env)

    for declaration in COMPOSITION_DECLARATIONS:
        assert printed_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "Equiv.Perm.subgroupOfMulAction") == EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "independentlyReconstructedTarget") == EXPECTED_AXIOMS
    assert proof_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "cannot provision a kernel network namespace" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == PROOF_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]
    covered_declarations = spec["covered_declarations"]
    assert covered_declarations == [
        "Stage1Instances.THM_M_0063.CayleyTheoremTarget",
        *(f"Stage1Instances.THM_M_0063.ObligationTree.{name}" for name in COMPOSITION_DECLARATIONS),
        *(f"Stage1Instances.THM_M_0063.Proof.{name}" for name in PROOF_DECLARATIONS),
        "Equiv.Perm.subgroupOfMulAction",
        "Stage1Instances.THM_M_0063.Validation.independentlyReconstructedTarget",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0063-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    started_at = datetime.fromisoformat(receipt["started_at"])
    ended_at = datetime.fromisoformat(receipt["ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at.tzinfo is not None and ended_at.tzinfo is not None
    assert started_at <= ended_at == validated_at
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"] == PROOF_IDS
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    origin = provenance["origin"]
    owning_source = "Mathlib/GroupTheory/Perm/Subgroup.lean"
    assert provenance["terminal_declaration"] == "Equiv.Perm.subgroupOfMulAction"
    assert provenance["terminal_proof_body_id"] == f"sha256:{TERMINAL_BODY_SHA256}"
    assert origin["remote"] == MATHLIB_REMOTE
    assert origin["revision"] == MATHLIB_REVISION and origin["tree_hash"] == MATHLIB_TREE
    assert origin["file"] == owning_source
    assert [origin["source_blob"], origin["source_sha256"], origin["olean_sha256"]] == list(
        SOURCE_BOUNDARY[owning_source]
    )
    source_lines = (MATHLIB / owning_source).read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(source_lines[67:73])).hexdigest() == TERMINAL_BODY_SHA256
    assert provenance["selected_source_blob_olean_triples"] == {
        name: list(values) for name, values in SOURCE_BOUNDARY.items() if name != owning_source
    }
    assert provenance["license_sha256"] == sha256(MATHLIB / "LICENSE")
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id",
            "cwd",
            "argv",
            "env_allowlist",
            "timeout_seconds",
            "network_policy",
            "expected_exit",
            "expected_outputs",
            "covered_obligation_ids",
            "covered_declarations",
        )
    }
    assert receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert receipt["result"]["kernel_replay"] == "provisional_pass"
    assert receipt["result"]["placeholder_and_unsafe_scan"] == "pass"
    assert receipt["result"]["selected_provenance"] == "pass"
    assert receipt["result"]["foundation_and_complete_trust_closure"] == "fail_closed"
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert hashlib.sha256(expected_stdout.encode("utf-8")).hexdigest() == EXPECTED_STDOUT_SHA256
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": EXPECTED_STDOUT_SHA256,
        "stdout_bytes": len(expected_stdout.encode("utf-8")),
        "stdout_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
        "log_boundary": "Canonical nine-line semantic summary; full temporary Lean output was parsed in memory and was not retained as release evidence.",
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-0063-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "theorem completion is false" in phase_notes
    assert "same-worker" in phase_notes and "cold empty-cache" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
