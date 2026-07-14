#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1018-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1018"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1018-VALIDATION"
THEOREM = "THM-M-1018"
BASE_REVISION = "718e166c56e53c552ebb861ee01427f9a606fc72"
BASE_TREE = "f2e15921b967c6f80b9e964361b684b5f9a011d9"
EXPRESSION_SHA256 = "c897cb4f129790bbefbb22e4500310d827ae75b914808fd8260916c315e2d964"
DENOMINATOR_SHA256 = "c5662da4255541baea4a76c8de113b36bfb571e2b65376597ad2bcc8cf13d6c2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"

PROOF_RECEIPT = "proof-receipt-2026-07-15-head-00f98378.json"
LEAN_MODULES = (
    "Statement.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "AnchorAudit.lean",
    "Validation.lean",
)
EXPECTED_INPUTS = {
    "Statement.lean": "88009a0b2e20577d7a007df22f94e79c1e03fb51f062291cb6b23bf5741efdd7",
    "ObligationTree.lean": "2df4f358a5612a779f0c8cbc05e5d4c760629bacfd9cf2a5b0955fbf1ca7055e",
    "Proof.lean": "2d147de6d7d67985a8eec90f0f3e2f6bf5dfe7db10aa62ec00322e54a18e4334",
    "AnchorAudit.lean": "ae91373f97ebc5c864c8fa95e8efd3821252cd5241f835c7ae0e1a5d074a5fe9",
    "Validation.lean": "a125ed1ce0d8acb48442b884d483ba557cf68071bba004fafe34c94b7f5b04e4",
    "intake.json": "fad10c47d732195988f57137636bda863ef432e2112487074ccf6c0058ce18f4",
    "anchor-audit.json": "44e089c4ee30a02b8675b85d54515aaac295923363a9581f1ffd0ae6066bee99",
    "obligation-registry.json": "14938dc0eb568813794896c3643545c834ac9f14523529e9c45b1c7d353afb95",
    "typed-graphs.json": "0ab510940f92808e16bc1528c9d7c9d02ebc9d26befe1da14588d543a795fba2",
    "validation-specs.json": "92681bbd6305f93e9c239b09b3bbf19735da20de655511ff159b334c7b4490ee",
    PROOF_RECEIPT: "a2d12bf0d7d5ecf95bbd50b2c04f4fcaad374e61933392e92a8bebc1eac07a2d",
    "source_statement_crosswalk.md": "bcdadc5c7f2d3e397c75f2d8f6285491c434a62de7213937f22b0543762028fb",
    "check_obligation_tree.py": "c740a7e63277ab42faa9feee95ce07e779412e33e075d8bc229485adc19b37e8",
    "validation-spec.json": "59ba4b2b882b2958163bafee7ad16329dc745621586652468ffdcc0813065407",
}

PINNED_TERMINALS = {
    "Mathlib/MeasureTheory/Measure/Portmanteau.lean": {
        "source_sha256": "5bc8fe09f6b0d40f62f4cad062092e031e34b1bfaba10889d160c0b79d4e9674",
        "git_blob": "411291e6e0e0dcf015ff33fc67adf9aeb702cf56",
        "olean_sha256": "9a9efaee35509086bbad2a91b61ce735cc7cc4039efbac7788fad4d175795df8",
    },
    "Mathlib/Topology/Order/DenselyOrdered.lean": {
        "source_sha256": "0c49d8488019c1ff076e92121e331d4bfeff137ca3fb50aa3f6bb1b31ab412c4",
        "git_blob": "75d95df016df2dc40aa5725d93d01052edba3e2d",
        "olean_sha256": "a6c1f76d9d11cadbc7db38b5ef4a3886f5875d9115c2ab3be8816f7ea3af9e50",
    },
    "Mathlib/MeasureTheory/OuterMeasure/Basic.lean": {
        "source_sha256": "9e739a4d20704494cc92d11be380512d956500fbc365b2eb3a9221f41a724fc1",
        "git_blob": "07673b5e3114e94fd1cb8a4b7ce1f856570ec72d",
        "olean_sha256": "9f741aa7de6fb64efb037b325a62ef9999c77e420d2e37e2f1dace991e7a1b14",
    },
    "Mathlib/MeasureTheory/Measure/Real.lean": {
        "source_sha256": "73d4563de66b47351874859ba7b693c9f8dc3d6f6e6d1007623ad2b02e291d75",
        "git_blob": "b7889e340cdb39fd9cf21a8b46b5eeea9da39243",
        "olean_sha256": "3723f4db6a450fbf228aac1af79a901dc2622ad6103fb06e8eb09d6aa9fb589c",
    },
    "Mathlib/Topology/Instances/ENNReal/Lemmas.lean": {
        "source_sha256": "4517f4bb30716616fe0fef9495a6585d13b2b569164ca0e3a2ff3d6683251ec2",
        "git_blob": "07b49e50a2e945c5538fb661921549521f6556aa",
        "olean_sha256": "64910f5e78d272eb7ff9117f0db475fb314619f989d631ce0696d5d420461751",
    },
}

AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("root_compose",),
    "Proof.lean": (
        "frontier_Ioc_null",
        "tendsto_Ioc_mass_of_tendsto",
        "measureReal_Icc_eq_Ioc",
        "measureReal_Ioo_eq_Ioc",
        "interval_mass_of_weak_limit",
    ),
    "Validation.lean": (
        "frontier_Ioc_null_direct",
        "tendsto_Ioc_mass_of_tendsto_direct",
        "conditionalCanonicalBridge",
    ),
}

SUMMARY_LINES = (
    "PASS network-isolated trust-zero replay of the frozen statement, conditional composition, five partial proof bodies, and three validation probes",
    "PASS observed axioms: exactly propext, Classical.choice, and Quot.sound; every validation probe is sorry-free and no output contains sorryAx",
    "PASS frozen hashes, open-root graph boundary, clean mathlib pin, selected direct source/blob/olean provenance, and owned-source hygiene",
    "FAIL CLOSED authority and exact root: the proof predecessor is not master-accepted and no declaration inhabits LevyInversionTarget without the open analytic premise",
    "FAIL CLOSED complete trust/provenance and cold hermetic replay: the dependency cache is shared and warm, and no accepted complete TCB or offline-restorable closure exists",
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
    timeout: int = 300,
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
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


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
    intake = load(HERE / "intake.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / PROOF_RECEIPT)

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 494 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 494,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1018-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1018-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    assert intake["canonical_formal_target"]["elaborated_expression_hash"].startswith(
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1018-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [
        "M1018-S-BOUNDARY",
        "M1018-S-EXACT",
        "M1018-S-KERNEL",
        "M1018-S-TRANSPORT",
        "M1018-T-ASSEMBLE",
    ]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]
    assert closure["composition_certificates"] == [
        "Stage1Instances.THM_M_1018.ObligationTree.root_compose"
    ]

    assert proof_receipt["accepted"] is False
    assert proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert anchor["terminal_candidate_found"] is anchor["audit_complete"] is False
    assert anchor["machine_classification"] == "M3"

    # The frozen recipes are architecture checks only; they cannot close open math obligations.
    assert frozen_specs["item_id"] == "S56-M-1018-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 17
    assert {tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]} == {
        ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    flt_pin = next(row for row in manifest["packages"] if "flt-regular" in row["name"])
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert flt_pin["rev"] == flt_pin["inputRev"] == FLT_REGULAR_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    olean_root = MATHLIB / ".lake" / "build" / "lib" / "lean"
    for relative, expected in PINNED_TERMINALS.items():
        source = MATHLIB / relative
        olean = olean_root / relative.replace(".lean", ".olean")
        assert sha256(source) == expected["source_sha256"]
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["git_blob"]
        assert sha256(olean) == expected["olean_sha256"]

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
    assert "import Proof" not in validation
    for marker in (
        "theorem frontier_Ioc_null_direct",
        "theorem tendsto_Ioc_mass_of_tendsto_direct",
        "theorem conditionalCanonicalBridge",
    ):
        assert marker in validation

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert "Lean (version 4.29.0" in run([str(lean), "--version"])
    bwrap_name = shutil.which("bwrap")
    assert bwrap_name is not None, "bubblewrap is required to enforce network denial"
    bwrap = Path(bwrap_name)
    assert sha256(bwrap) == BWRAP_SHA256

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1018-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_MODULES:
            shutil.copy2(HERE / name, tmp / name)
        base = [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(tmp),
            "--setenv", "ELAN_TOOLCHAIN", "leanprover/lean4:v4.29.0",
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp),
            str(lean), "--trust=0", "-t0", "--root", str(tmp),
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"
        outputs["Statement.lean"] = run(
            base + ["-o", "Statement.olean", "Statement.lean"], timeout=300
        )
        outputs["ObligationTree.lean"] = run(
            base + ["-o", "ObligationTree.olean", "ObligationTree.lean"], timeout=300
        )
        outputs["Proof.lean"] = run(
            local + ["-o", "Proof.olean", "Proof.lean"], timeout=300
        )
        outputs["Validation.lean"] = run(
            local + ["-o", "Validation.olean", "Validation.lean"], timeout=300
        )
        outputs["AnchorAudit.lean"] = run(base + ["AnchorAudit.lean"], timeout=300)

    allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
    for name, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[name], declaration) == allowed_axioms
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 3
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output and "error:" not in all_output

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
    assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"]))

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
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation_verifier_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_release_verification_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1018-PROOF.master_acceptance"

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
        line[3:] for line in status.splitlines()
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
