#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0958-VALIDATION."""

from __future__ import annotations

import argparse
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
HERE = ROOT / "Stage1_Instances" / "THM-M-0958"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0958-VALIDATION"
THEOREM = "THM-M-0958"
BASE_REVISION = "51c2828e82ffb19860830f78b771f80e13ad7dff"
BASE_TREE = "4655b8b40829513de6fb5661344b33fc7cd17cd1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
DENOMINATOR_SHA256 = "a66280599ad67d6daac4bea5c3e08484e1b6c1aa0d75223a5d3aaf428c383e5b"
EXPRESSION_SHA256 = "bc0d841038cdbcd4960581583c4ddfb7004d7ad38cf6432ab4803e9908f8f59c"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PARTIAL_IDS = [
    "M0958-C-DIGIT-EMBED",
    "M0958-L-DIGIT-INJECTIVE",
    "M0958-L-NO-CARRY",
    "M0958-L-PROGRESSION-FREE",
    "M0958-L-EMBED-RANGE",
]
INPUT_HASHES = {
    "Statement.lean": "765d13f4b2fc0bc8bdf0a1211039b62ed6269148819857795aac0c7a42dc40e6",
    "ObligationTree.lean": "c52b448dfaa236834207a048c5d26208e6b4db8b39830eaf620b398497a64394",
    "Proof.lean": "60def65f51836f174a4d0c10fb782b6c10158184183d6bbc05eb7a1b578fd3be",
    "proof-receipt.json": "4ba570039727a924a5d650bf1948f50b7b145e0e292f78d1162c7f85c052e4e5",
    "proof-blocker.json": "7cc75b4698b15ba892f3742ed4205866d93b63e758636762ac9198645bf21e83",
    "statement.json": "2e48944da988922ac8b4c9a0b56f13795c6dad8536464d29f64e449ed6920500",
    "anchor-audit.json": "eba38a4e3bb2530ffb45bc9560be6b667823a4b3ff9e19fdedc802fc6190224d",
    "obligation-registry.json": "53433fb10301f4166c0500b9872f04f0f31839117f4c54457d448458712287d2",
    "typed-graphs.json": "c6f40a4fa5d20d0b0ca88d17222d71e87ad292d29a8218ecdac17f0ddaa4f62a",
    "instance.json": "28dd5b490a3e83306ea10985feeba58904b5d1193fa605eb53f27990413b8990",
    "task-dag.json": "31e963bdb84f105e66071ea2c8af769f205d00ecb945d0fbcc2b671ef77f2faa",
    "validation-specs.json": "4bf073c4863f525b072288cf65f18703fabb2ac39d91308d6a7398418562a188",
}
SELECTED_PROVENANCE = {
    "Mathlib/Combinatorics/Additive/AP/Three/Defs.lean": {
        "source_sha256": "b325fb632a5398208995fa5beae71c47798086e588f98e46679aa81b923b28e3",
        "git_blob": "534177a2aa83fa462689226e248953fe38f2e1cc",
        "olean_sha256": "19cbfd0bcf347073590f8f60d2aa288874a3fbe3f7c73fda5ade9b1b702bee8c",
    },
    "Mathlib/Analysis/SpecialFunctions/Log/Base.lean": {
        "source_sha256": "585f502f8c45eaac27a8d18548104a6125b0738d2e9e6c7c0e4eaa62f2c4366a",
        "git_blob": "3fd5c28ef8a6d38def7410c01258250655ccbbd3",
        "olean_sha256": "ceccdb798c506c7f7d68b27542a00fbc3770f87e473ff703fa1d907f4abf9941",
    },
    "Mathlib/Combinatorics/Additive/AP/Three/Behrend.lean": {
        "source_sha256": "1f8c1813a75c722ee4d62d63185c53d0b52d27691e531c05e0ecb6c10c15cf65",
        "git_blob": "7d3eb0e603040dcd72fe35e39c82f4d615b3e254",
        "olean_sha256": "620e1ce9b071dd2049ce734f4e58bc1e2bbdb6fb9bf9f6e17f1b39ad34bb720f",
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0958.Proof.map_injOn_digit_box",
    "Stage1Instances.THM_M_0958.Proof.map_add_eq",
    "Stage1Instances.THM_M_0958.Proof.map_image_threeAPFree",
    "Stage1Instances.THM_M_0958.Proof.card_map_image",
    "Stage1Instances.THM_M_0958.Proof.map_image_lt_pow",
    "Stage1Instances.THM_M_0958.Proof.oneBasedDigitImage_subset",
    "Stage1Instances.THM_M_0958.Proof.card_oneBasedDigitImage",
    "Stage1Instances.THM_M_0958.Proof.oneBasedDigitImage_progressionFree",
    "Stage1Instances.THM_M_0958.Proof.digitEmbeddingPackage_checked",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_0958.ObligationTree.checkedWitnessToRootTransport",
    "Stage1Instances.THM_M_0958.ObligationTree.rootComposition_checked",
    "Stage1Instances.THM_M_0958.ObligationTree.root_of_terminal_packages",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0958.Validation.digitEmbeddingPackage_validation",
    "Stage1Instances.THM_M_0958.Validation.conditionalRoot_validation",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
EXPECTED_SUMMARY = (
    "PASS S56-M-0958-VALIDATION narrow network-isolated validation\n"
    "kernel: exact statement, three conditional composition declarations, nine partial proof declarations, and two differential declarations replayed with trust zero\n"
    "trust: all checked proof-bearing declarations are sorry-free; observed axioms are propext, Classical.choice, and Quot.sound; differential closure has no bodyless nonaxiom or unsafe declaration\n"
    "provenance: frozen local hashes, clean pinned mathlib, three selected source/blob/olean identities, license, and tool digests agree\n"
    "blocked: proof master acceptance and M0958-T-WITNESS root closure fail; zero frozen obligations are accepted\n"
    "release: complete TCB/provenance, cold empty-cache replay, H0/R0 review, and distinct-runner independent verification fail closed\n"
)

if not __debug__:
    raise RuntimeError("validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


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


def reported_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def validate_static(worker_packet: Path | None) -> None:
    spec = load(HERE / "validation-spec.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    statement = load(HERE / "statement.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    old_specs = load(HERE / "validation-specs.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1492,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0958-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0958-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 600
    assert spec["covered_obligation_ids"] == []
    assert spec["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_0958.ElkinConstructionTarget",
        *COMPOSITION_DECLARATIONS,
        *PROOF_DECLARATIONS,
        *VALIDATION_DECLARATIONS,
    }

    for name, expected in INPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == INPUT_HASHES["Statement.lean"]
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["minimal_open_machine_proof_cut_sets"] == [["M0958-T-WITNESS"]]

    assert proof_receipt["item_id"] == "S56-M-0958-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["verdict"] == "no_state_change"
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == ["M0958-T-WITNESS"]
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    local_proof = next(row for row in local_dag["tasks"] if row["id"] == "S56-M-0958-PROOF")
    local_validation = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_proof["state"] == local_validation["state"] == "open"
    assert old_specs["item_id"] == "S56-M-0958-OBLIGATION_TREE"
    assert len(old_specs["recipes"]) == 64
    assert {tuple(recipe["argv"]) for recipe in old_specs["recipes"]} == {
        ("python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }

    lean_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|proof_wanted)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(lean_source) is None
    imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifacts are unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, record in SELECTED_PROVENANCE.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / relative.replace(".lean", ".olean")
        assert sha256(source) == record["source_sha256"]
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == record["git_blob"]
        assert sha256(olean) == record["olean_sha256"]

    if worker_packet is not None:
        receipt = load(HERE / "validation-receipt.json")
        packet = load(worker_packet)
        assert packet["item_id"] == receipt["item_id"] == ITEM
        assert packet["state"] == receipt["proposed_state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert receipt["inputs"]["validation_lean_sha256"] == sha256(HERE / "Validation.lean")
        assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
        assert receipt["inputs"]["validator_sha256"] == sha256(HERE / "check_validation.py")
        assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
            EXPECTED_SUMMARY.encode("utf-8")
        ).hexdigest()
        assert receipt["result"]["root_closed"] is receipt["result"]["theorem_complete"] is False
        assert receipt["result"]["accepted_closed_obligation_ids"] == []
        assert receipt["first_failed_gate"].startswith("dependency.S56-M-0958-PROOF.master_acceptance")
        status = git("status", "--short", "--untracked-files=all")
        changed = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert changed == CHANGED_PATHS, (changed, CHANGED_PATHS)

    for path in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        full = ROOT / path
        if full.exists():
            data = full.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def replay() -> dict:
    bwrap = Path(shutil.which("bwrap") or "")
    assert bwrap.is_file() and sha256(bwrap) == BWRAP_SHA256
    python = Path("/usr/bin/python3")
    assert sha256(python) == PYTHON_SHA256
    lean_override = os.environ.get("STAGE1_LEAN_BIN")
    if lean_override:
        lean = Path(lean_override).resolve()
    else:
        lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()).resolve()
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()).resolve()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    version = run([str(lean), "--version"])
    assert "4.29.0" in version and LEAN_COMMIT in version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()

    with tempfile.TemporaryDirectory(prefix="m0958-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc",
            "--unshare-net", "--die-with-parent", "--setenv", "HOME", "/tmp/home",
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp),
        ]
        outputs: dict[str, str] = {}
        hashes: dict[str, str] = {}
        for name in ("Statement", "ObligationTree", "Proof", "Validation"):
            module_path = lean_path if name == "Statement" else f"{tmp}:{lean_path}"
            output = run(base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--root", str(tmp),
                "--trust=0", "-o", f"{name}.olean", f"{name}.lean",
            ])
            outputs[name] = output
            hashes[f"{name}.log"] = hashlib.sha256(output.encode("utf-8")).hexdigest()
            hashes[f"{name}.olean"] = sha256(tmp / f"{name}.olean")

    assert outputs["Statement"].count("depends on axioms") == 9
    assert outputs["ObligationTree"].count("depends on axioms") == 3
    assert outputs["Proof"].count("depends on axioms") == 9
    assert outputs["Validation"].count("depends on axioms") == 2
    for declaration in (*COMPOSITION_DECLARATIONS, *PROOF_DECLARATIONS, *VALIDATION_DECLARATIONS):
        module = (
            "ObligationTree" if declaration in COMPOSITION_DECLARATIONS
            else "Proof" if declaration in PROOF_DECLARATIONS
            else "Validation"
        )
        assert reported_axioms(outputs[module], declaration) <= ALLOWED_AXIOMS
    observed = set().union(*(
        reported_axioms(outputs["Proof"], declaration) for declaration in PROOF_DECLARATIONS
    ))
    assert observed == ALLOWED_AXIOMS
    assert outputs["Validation"].count("Declarations are sorry-free!") == 2
    assert "VALIDATION_CLOSURE declarations=17070 modules=672" in outputs["Validation"]
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["Validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["Validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["Validation"]
    assert all("sorryAx" not in output and "error:" not in output for output in outputs.values())
    return {"lean_output_sha256": hashes}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    worker_packet = args.worker_packet.resolve() if args.worker_packet else None
    validate_static(None if args.probe else worker_packet)
    replay()
    sys.stdout.write(EXPECTED_SUMMARY)


if __name__ == "__main__":
    main()
