#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1271-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1271"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1271-VALIDATION"
THEOREM = "THM-M-1271"
BASE_REVISION = "557b928b377b386864527c9fb4831d45857837aa"
BASE_TREE = "e677879a6eb4cb9d6795ba1bd78726af06ab9465"
STATEMENT_SHA256 = "984ec64013fa92caf23696c39017a28b7c8a908224ae8e1018a156734469f70c"
EXPRESSION_SHA256 = "686a7f777a77c3f91504e4c48cd3d0fab19ef802ce3df1751dc4288e62592d7b"
DENOMINATOR_SHA256 = "2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "ObligationTree.lean": "8877433688d159ad88c07307d59cb8e6bad9d0c54b97cbae739609bf5a69602e",
    "Proof.lean": "707249895e0dfca3638f1fb8f94ae907d0e55a4ffeb1c07cb7e4697000e4b9ae",
    "AnchorAudit.lean": "3f2ed9d48513168e33323b09a21e977fcfa10301255c744cbc6d65b6ad89574b",
    "Validation.lean": "e072ad47b44d45245b7397c841706bee577d93345ecb28ed689e3444d73d8480",
    "statement.json": "1af288978c86bf3bf24bdc627fef502a15df88b919e7926a0c79d63afa263362",
    "anchor-audit.json": "a653c9c9a230ad26d3160905542831fa716ed6135ea5eb2f1f676f62dd3c6dbf",
    "obligation-registry.json": "1310ad818e169b8d56d1a5dfcd75294756051d5b834979bc996daadce1a58bef",
    "typed-graphs.json": "93b9f4757d1739dd78bfd914ffe98f4ab45c4e86ac0308e2b942dd53e1e98f77",
    "validation-specs.json": "0dd4e5771731cebf9811dc3671d04bc940465affadec79f58b1808ec0e15404a",
    "proof-receipt.json": "ff8dc94634474ec113721a57cc48ed46ee6c6a4fdaea4cbfdf82b96db131f368",
    "proof-blocker.json": "5f53ba41386360b0b673bc2e493989c485f12ab81a8951930077ce53a219dea2",
    "source-statement-crosswalk.md": "598260f0cdd29500e3a43e0384a5970292930985fe72363e88c1755f7747cfac",
    "check_obligation_tree.py": "652786aa63e9918b4cb59da081a0b52690003890a8b0b5495d48a89e50349667",
    "validation-spec.json": "f883e4650e1c1041c7fe7f52f89b9cdb54a243a6dd80cd158547c3a94c282b52",
}
PINNED_TERMINALS = {
    "Mathlib/Topology/Order/IntermediateValue.lean": {
        "source_sha256": "cfa4c897696242691c5545e03d4b9794a1aa8e35c3e7abf9b36b30dfd666f260",
        "git_blob": "9f4f44f8fa483b14dd372d2d76a7a649215518ad",
        "olean_sha256": "332e81a58dc1e4b1cc5be8d42b6c3d79ab86bda43030c422b360072ff58bd277",
    },
    "Mathlib/Topology/Order/Compact.lean": {
        "source_sha256": "bf00e5c54860bc821e8310f4901ff38071f41099c274d5a34ab9ef46e7ff6ac1",
        "git_blob": "3cc7cd919769ab22afecfde178c0a16367ef0aa5",
        "olean_sha256": "4d3dc8974d03302b48630e83f414a0a704653c14cab11e2e0dbc2e90da0e34f7",
    },
    "Mathlib/Topology/Sequences.lean": {
        "source_sha256": "4f49427b838a566edb7c480fc0419cb49d3521790c32d002a176de234225e3a9",
        "git_blob": "342292cb09a8db8b1ed552db63d6865a58f9713c",
        "olean_sha256": "f2b71c9fc990babadd181bbadad1d705164c30b8819b7b162f11248890ad51ad",
    },
    "Mathlib/Analysis/Calculus/ContDiff/Basic.lean": {
        "source_sha256": "c3da4bad51dbed2870e5a92284953176992b5a04bc959a4c3284f63411ad52d4",
        "git_blob": "e0ad3b97537a731639b45d1a0d47bacff40a5129",
        "olean_sha256": "b2d73b6e964ed930bc8db763568dea3578ba0b60808a6f59b8b8055e6ec66b1e",
    },
}
LEAN_MODULES = (
    "Statement.lean", "ObligationTree.lean", "Proof.lean", "AnchorAudit.lean", "Validation.lean"
)
AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("root_of_barrier_and_critical_packages",),
    "Proof.lean": (
        "admissiblePath_meets_sphere",
        "alpha_le_pathHeight",
        "pathHeight_attained",
        "mountainPassBarrierPackage",
        "exists_valueSequence_at_mountainPassLevel",
        "exists_criticalPoint_of_psSequence",
        "mountainPassCriticalPackage_of_psSequence",
    ),
    "Validation.lean": (
        "directAdmissiblePath_meets_sphere",
        "directAlpha_le_pathHeight",
        "directAlpha_le_mountainPassLevel",
        "directConditionalRoot",
    ),
}
EXPECTED_COVERED_OBLIGATIONS = {
    "M1271-C-PATH-MAX",
    "M1271-L-SPHERE-CROSSING",
    "M1271-T-BARRIER",
    "M1271-C-PS-SEQUENCE",
    "M1271-L-PS-COMPACT",
    "M1271-L-LIMIT-PASSAGE",
    "M1271-T-ASSEMBLE",
}
EXPECTED_COVERED_DECLARATIONS = {
    "Stage1Instances.THM_M_1271.root_of_barrier_and_critical_packages",
    *{
        f"Stage1Instances.THM_M_1271.{name}"
        for name in AXIOM_DECLARATIONS["Proof.lean"]
    },
    *{
        f"Stage1Instances.THM_M_1271.Validation.{name}"
        for name in AXIOM_DECLARATIONS["Validation.lean"]
    },
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1271 narrow validation",
    "PASS network-isolated trust-zero replay: frozen statement, conditional composition, seven partial proof declarations, anchor probe, and four differential probes elaborated",
    "PASS hygiene and trust observation: twelve axiom reports contain exactly propext, Classical.choice, and Quot.sound; prohibited proof devices and sorryAx are absent",
    "PASS selected provenance: frozen local hashes, clean mathlib pin, four source/blob/olean identities, license, and tool identities agree",
    "OPEN exact root: derivative-small Palais-Smale sequence M1271-C-PS-SEQUENCE is absent; M1271-T-CRITICAL and M1271-ROOT remain open",
    "FAIL CLOSED authority: S56-M-1271-PROOF is worker-provisional and not master-accepted",
    "FAIL CLOSED release: complete trust/provenance, cold empty-cache offline replay, and a distinct signed independent verifier are absent",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

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
    timeout: float | None = None,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
    limit = remaining if timeout is None else min(remaining, timeout)
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=limit,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


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
    if match is None:
        assert re.search(
            rf"'[^']*{re.escape(declaration)}' does not depend on any axioms", output
        ), declaration
        return set()
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
    os.umask(0o022)
    os.environ["LANG"] = "C.UTF-8"
    os.environ["LC_ALL"] = "C.UTF-8"
    os.environ["TZ"] = "UTC"

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 164
    assert target["target_lane"] == "hard_mathlib_anchor_and_wrapper"
    assert target["baseline"] == "L0" and target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 164,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1271-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1271-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1271.MountainPassTarget"
    )
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1271-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 13
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["theorem_complete"] is False
    assert closure["first_open_cut_set"] == ["M1271-T-BARRIER", "M1271-T-CRITICAL"]
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1271-ROOT")
    assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
        "H3", "M3", "R4"
    )
    assert graphs["graphs"]["evidence"]["edges"] == []

    assert proof_receipt["item_id"] == "S56-M-1271-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_receipt["closed_obligation_ids"] == ["M1271-C-PATH-MAX"]
    assert proof_receipt["partial_progress"] == {
        "obligation_id": "M1271-C-PS-SEQUENCE",
        "obligation_closed": False,
        "checked_component": "functional_value_convergence_only",
    }
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == [
        "M1271-C-PS-SEQUENCE", "M1271-T-CRITICAL", "M1271-ROOT"
    ]
    assert proof_blocker["first_failed_gate"].startswith("M1271-C-PS-SEQUENCE")
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert anchor["root_decision"]["kernel_closed"] is False

    # The frozen recipes predate proof work. Open nodes call a structural checker,
    # while the root recipe checks only conditional composition, not an inhabitant.
    assert frozen_specs["item_id"] == "S56-M-1271-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 13
    assert {tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]} == {
        ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"),
        ("python3", f"Stage1_Instances/{THEOREM}/check_lean_composition.py"),
    }

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
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
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in (
        "import Proof", "import ObligationTree", "root_of_barrier_and_critical_packages",
        "admissiblePath_meets_sphere hgamma", "mountainPassBarrierPackage",
    ):
        assert forbidden not in validation, forbidden
    for marker in (
        "theorem directAdmissiblePath_meets_sphere",
        "theorem directAlpha_le_pathHeight",
        "theorem directAlpha_le_mountainPassLevel",
        "theorem directConditionalRoot",
        "(critical :",
    ):
        assert marker in validation
    proof_source = source_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    assert "(produce :" in proof_source
    assert not re.search(r"^theorem\s+\w+\s*:\s*MountainPassTarget", proof_source, re.MULTILINE)
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    lake_name = shutil.which("lake")
    bwrap_name = shutil.which("bwrap")
    assert lake_name is not None and bwrap_name is not None
    lake = Path(lake_name).resolve()
    bwrap = Path(bwrap_name).resolve()
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    lean = Path(run([str(lake), "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lean_path = run(
        ["env", "-u", "LEAN_PATH", str(lake), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
        timeout=60,
    ).strip()
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    version = run([str(lean), "--version"], timeout=30)
    assert "Lean (version 4.29.0" in version and LEAN_COMMIT in version
    assert "Lake version 5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, timeout=30)

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1271-validation-", dir="/tmp") as tmp_name:
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
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp),
            str(lean), "--trust=0", "--root", str(tmp),
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"
        outputs["Statement.lean"] = run(
            base + ["-o", "Statement.olean", "Statement.lean"], timeout=300
        )
        outputs["ObligationTree.lean"] = run(
            local + ["-o", "ObligationTree.olean", "ObligationTree.lean"], timeout=300
        )
        outputs["Proof.lean"] = run(
            local + ["-o", "Proof.olean", "Proof.lean"], timeout=300
        )
        outputs["Validation.lean"] = run(
            local + ["-o", "Validation.olean", "Validation.lean"], timeout=300
        )
        outputs["AnchorAudit.lean"] = run(base + ["AnchorAudit.lean"], timeout=300)

    report_count = 0
    for name, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[name], declaration) == ALLOWED_AXIOMS
            report_count += 1
    assert report_count == 12
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output and "error:" not in all_output
    module_hashes = {
        name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
    }
    kernel_output_sha256 = hashlib.sha256(
        "\n".join(outputs[name] for name in LEAN_MODULES).encode()
    ).hexdigest()

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == EXPECTED_COVERED_OBLIGATIONS
    assert set(spec["covered_declarations"]) == EXPECTED_COVERED_DECLARATIONS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    canonical = receipt["canonical_target"]
    assert canonical["statement_file_sha256"] == STATEMENT_SHA256
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["validation_spec"] == {
        "path": f"Stage1_Instances/{THEOREM}/validation-spec.json",
        "sha256": sha256(HERE / "validation-spec.json"),
    }
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["worktree"]["tracked_changes"] == []
    assert receipt["worktree"]["pre_existing_untracked"] == ["Formalizations/Lean/.lake"]
    assert receipt["worktree"]["validation_untracked_sha256"] == {
        relative: sha256(ROOT / relative)
        for relative in sorted(CHANGED_PATHS - {f"Stage1_Instances/{THEOREM}/validation-receipt.json"})
    }
    assert receipt["worktree"]["self_referential_receipt_hash"] == "not_applicable"
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["validation_verifier_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["lean-toolchain"] == LEAN_TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == LAKE_MANIFEST_SHA256
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == LEAN_EXECUTABLE_SHA256
    assert environment["lake_launcher_sha256"] == LAKE_EXECUTABLE_SHA256
    assert environment["bubblewrap_sha256"] == BWRAP_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    receipt_terminals = receipt["provenance"]["selected_mathlib_sources"]
    for relative, expected in PINNED_TERMINALS.items():
        assert receipt_terminals[relative] == expected
    assert receipt["execution"]["kernel_output_sha256"] == kernel_output_sha256
    assert receipt["execution"]["per_module_output_sha256"] == module_hashes
    assert receipt["execution"]["started_at"] < receipt["execution"]["ended_at"]
    assert isinstance(receipt["execution"]["duration_seconds"], int)
    assert receipt["execution"]["duration_seconds"] > 0
    result = receipt["result"]
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["axiom_report_count"] == 12
    assert set(result["observed_axioms"]) == ALLOWED_AXIOMS
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_closed_obligation_ids"] == []
    assert result["provisionally_observed_obligation_ids"] == [
        "M1271-C-PATH-MAX", "M1271-L-SPHERE-CROSSING", "M1271-T-BARRIER",
        "M1271-L-PS-COMPACT", "M1271-L-LIMIT-PASSAGE", "M1271-T-ASSEMBLE",
    ]
    assert result["partially_observed_obligation_ids"] == ["M1271-C-PS-SEQUENCE"]
    assert result["complete_foundation_tcb_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [
        "M1271-C-PS-SEQUENCE", "M1271-T-CRITICAL", "M1271-ROOT"
    ]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1271-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == "proof.M1271-C-PS-SEQUENCE.kernel_closure"
    assert receipt["first_failed_release_gate"] == "S56-7.3-TRANSITIVE-PROVENANCE-CLOSURE"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == {
        "H": "H3", "M": "M3", "R": "R4"
    }
    assert receipt["debt_vector_delta"] == "none"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == [row["command"] for row in receipt["commands"]]
    assert {row["exit_code"] for row in receipt["commands"]} == {0}
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["execution"]["stdout_sha256"] == hashlib.sha256(stdout.encode()).hexdigest()
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
