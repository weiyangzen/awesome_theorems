#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0600-VALIDATION."""

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
import time


if not __debug__:
    raise SystemExit("validation requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0600"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0600-VALIDATION"
THEOREM = "THM-M-0600"
BASE_REVISION = "7348dc646fd6babfe2b82c35b4c03a9ed5921f8e"
BASE_TREE = "ddd6941316b5d4a9d6574d9532212c24de6fe516"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_SHA256 = "40dced107b293e5045af83deaabd2f898bdf16c4b6f4bced61b6a9fbef2b97dc"
EXPRESSION_SHA256 = "6ba927d7712fa05ea04ff656eefe32d16a57a2c45f4aa49a30695b263b04911d"
DENOMINATOR_SHA256 = "071b084403b89cd9fb084d9fe7167cad1738e115f6353aaeabfab4516e93f981"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "ObligationTree.lean": "6e01acd6107af26a9b969495c97edd2d1e3f73ad3e1c78e78765fe81bdb6bb97",
    "Proof.lean": "cfc2225e6c236608ddda93b7038e8a6f584a4164a11e5a093ed375e51e04cf55",
    "AnchorAudit.lean": "bbdd2e32bad8571517658f6ef718d58c06388b15555b991870f95fd39b2a88af",
    "Validation.lean": "957beb3a3a5679e1bcca15c263772d9ea82c3e27b44e5496fd0b2cbeae641341",
    "instance.json": "dc647bcc3af5bf6889f49064f5ab23f730b43db06c1d6e4109820f6863fe070d",
    "task-dag.json": "a97ff34ab5b065d4f5b8908a5524ea902a17e517efe3e66c70608b56f127d458",
    "statement.json": "fb5b2919203752f6ee859e934df2233002362454a0b9a56d8626e31b89a43cd9",
    "anchor-audit.json": "31ac00c0831b22a587c74f0c7572256cdd153447cbeb34fc25c7823d5624ae7b",
    "obligation-registry.json": "3746b457df4c0f011582f59aac375739f6d28b02f6dc55c68155d8e8cd4deff0",
    "typed-graphs.json": "38970e70e2007054cc2bb7a27ef6e421c1645f96a8d1653b10d3a0d9cdf28160",
    "validation-specs.json": "4f1b05f38d8a07e8dea9d050af533c01595ee09404e7e9fcf4fef75de1f973bb",
    "proof-receipt.json": "286c8b9f6256331e0743922be4c5c55e32040e6dcb1420d578f3341990175de1",
    "proof-blocker.json": "f6e44c023a8c4223f5071d9393afcf12e3724e1bb205e2b4b3588b6f2592485b",
    "source-statement-crosswalk.md": "f781ede12f33e77e28f0f48a8f3065db8fe52a8464405f3a2c8f0d9f48711567",
    "check_obligation_tree.py": "bc5cd01f81b5855d60ea7125536e6be96655ff3a094823164b46829a589c84cd",
    "validation-spec.json": "ece868df0301ed8a1ca093f5a8a396e83bdf4885bfd0514310345867c938e560",
}

PINNED_IMPORTS = {
    "Mathlib/Geometry/Manifold/ContMDiff/NormedSpace.lean": {
        "source_sha256": "243c5fa029893428942c9edb1b7e0f9f7506134d924a67b9840c0bb7911afb58",
        "git_blob": "5ecafad9772f7a5355317a8e81e18ed5a6b0ff8c",
        "olean_sha256": "cb6410930734ab2db4fac3a013ee1530b031edfa4b0472d6f61f93c04ddb8b7e",
    },
    "Mathlib/LinearAlgebra/QuadraticForm/Real.lean": {
        "source_sha256": "8d4bdfbacc438e038e075271d19d693fa9678436f12df1dc65a3c47e87375138",
        "git_blob": "9cc35276c8a4d782fca61451df21fc5f6c06fa26",
        "olean_sha256": "6a72eb5d458c97804b70813047217a07d89df6e5f6b5fbcb3a237691951d772a",
    },
    "Mathlib/LinearAlgebra/QuadraticForm/Signature.lean": {
        "source_sha256": "ae8e916c6c797ac394bedff7bf74ebd9f18a1968c2f9b8b612efec0f65f39ccb",
        "git_blob": "a853d78a5c77a3784fd9a37463a09373591b2519",
        "olean_sha256": "9c5ba5ffc5209ae5d8660cd7be5758e8e36ea9345bb8a985f77654f49ad5dd75",
    },
    "Mathlib/Analysis/Calculus/ImplicitContDiff.lean": {
        "source_sha256": "2d2be297f5e817f9eed9b79b35339d7b502f2d7e4f2c8861dac2ec3c23c17324",
        "git_blob": "bb4287f60ddb9450daa46db1b56602df09262d1c",
        "olean_sha256": "ab5ab883b05530f9191721caa931b11363c4c7f038070cc08f8dc445b864ed59",
    },
}

AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("root_of_morseNormalFormEngine",),
    "Proof.lean": (
        "zeroDimensionBranch",
        "morseNormalFormEngine_of_positiveDimension",
        "morseLemmaTarget_of_positiveDimension",
    ),
    "Validation.lean": ("zeroDimensionBranchDirect", "conditionalRootDirect"),
}
EXPECTED_COVERED_OBLIGATIONS = {"M0600-S-DEFINITIONS", "M0600-T-ASSEMBLE"}
EXPECTED_OBSERVED_OBLIGATIONS = {"M0600-S-FOUNDATION", "M0600-X-PROVENANCE"}
EXPECTED_PARTIAL_OBLIGATIONS = {"M0600-S-DIMZERO", "M0600-T-ENGINE"}
EXPECTED_DECLARATIONS = {
    "Stage1Instances.THM_M_0600.MorseLemmaTarget",
    "Stage1Instances.THM_M_0600.morseLemmaTarget_iff_expandedTarget",
    "Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine",
    "Stage1Instances.THM_M_0600.zeroDimensionBranch",
    "Stage1Instances.THM_M_0600.morseNormalFormEngine_of_positiveDimension",
    "Stage1Instances.THM_M_0600.morseLemmaTarget_of_positiveDimension",
    "Stage1Instances.THM_M_0600.Validation.zeroDimensionBranchDirect",
    "Stage1Instances.THM_M_0600.Validation.conditionalRootDirect",
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
    "PASS THM-M-0600 narrow validation",
    "PASS network-isolated trust-zero replay: statement, conditional composition, partial proof, anchor probes, and differential probes elaborated",
    "PASS hygiene: kernel sorry checks and a nested-comment-aware prohibited-device scan passed for all five hash-bound Lean modules",
    "PASS trust observation: six proof and differential declarations use exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: local inputs, clean mathlib pin/tree/remote, four source/blob/olean identities, license, and tool hashes agree",
    "OPEN exact root: M0600-T-ENGINE has no premise-free proof body and MorseLemmaTarget remains H1/M3/R3",
    "FAIL CLOSED authority: S56-M-0600-PROOF is worker-provisional and not master-accepted",
    "FAIL CLOSED release: complete trust/provenance, cold empty-cache offline replay, and a distinct signed independent verifier are absent",
    "audit_complete=false; theorem_complete=false",
)
SUMMARY_BYTES = ("\n".join(SUMMARY_LINES) + "\n").encode()
SUMMARY_SHA256 = "6d5689f08b4c4e810d3a3a6a8032dbb68f0a148707fcb33fbbd4554f95c27349"
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: float | None = None,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    assert remaining > 0, "validation recipe exceeded its 600-second wall-clock bound"
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
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                index += 1
            continue
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index + 2)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        flags=re.DOTALL,
    )
    matches = pattern.findall(output)
    no_axioms = re.findall(
        rf"'[^']*{re.escape(declaration)}' does not depend on any axioms", output
    )
    assert len(matches) + len(no_axioms) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def isolated_lean(
    bwrap: Path,
    lean: Path,
    lean_path: str,
    tmp: Path,
    args: list[str],
    *,
    module_path: bool,
) -> str:
    module_search = f"{tmp}:{lean_path}" if module_path else lean_path
    clean_env = {
        "PATH": "/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    return run(
        [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", module_search,
            "--chdir", str(tmp),
            str(lean),
            "--trust=0",
            "-t0",
            *args,
        ],
        cwd=ROOT,
        env=clean_env,
        timeout=300,
    )


def main() -> None:
    os.umask(0o022)
    os.environ.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})

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
    assert target == {
        "execution_rank": 638,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "莫尔斯引理",
        "category": "拓扑学 / 微分拓扑",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 132,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 638,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0600-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0600-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0600.MorseLemmaTarget"
    )
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"] == formal["declaration_or_expression"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0600-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 18
    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": ["M0600-S-DEFINITIONS", "M0600-T-ASSEMBLE"],
        "root_closed": False,
        "root_machine_debt": "M3",
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M0600-T-ENGINE"],
        "composition_certificates": [
            "Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine"
        ],
        "reason": "The final composition is conditional; MorseNormalFormEngine has no proof body.",
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0600-ROOT")
    assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
        "H1", "M3", "R3"
    )
    assert graphs["graphs"]["evidence"]["edges"] == []
    assert frozen_specs["item_id"] == "S56-M-0600-OBLIGATION_TREE"

    assert proof_receipt["item_id"] == "S56-M-0600-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_receipt["provisionally_closed_obligation_ids"] == [
        "M0600-S-DIMZERO"
    ]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set_after"] == ["M0600-T-ENGINE"]
    assert proof_blocker["machine_classification"] == "M3"
    assert proof_blocker["remaining_root_cut_set"] == ["M0600-T-ENGINE"]
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["argv"] == ["python3", "-I", "-B", str(Path(__file__).relative_to(ROOT))]
    assert spec["timeout_seconds"] == 600 and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == EXPECTED_COVERED_OBLIGATIONS
    assert set(spec["observationally_covered_obligation_ids"]) == EXPECTED_OBSERVED_OBLIGATIONS
    assert set(spec["partially_covered_obligation_ids"]) == EXPECTED_PARTIAL_OBLIGATIONS
    assert set(spec["covered_declarations"]) == EXPECTED_DECLARATIONS

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "AnchorAudit.lean", "Validation.lean",
        )
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split(
        "/-!", 1
    )[0]
    assert "import Proof" not in validation_imports
    assert "import ObligationTree" not in validation_imports

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in PINNED_IMPORTS.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(source) == expected["source_sha256"]
        assert git("hash-object", relative, cwd=MATHLIB) == expected["git_blob"]
        assert sha256(olean) == expected["olean_sha256"]

    fixed_env = os.environ.copy()
    fixed_env.update({
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).strip()
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_EXECUTABLE_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0600-validation-", dir="/tmp"))
    try:
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "AnchorAudit.lean", "Validation.lean",
        ):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        statement_output = isolated_lean(
            bwrap, lean, lean_path, tmp,
            ["-o", "Statement.olean", "Statement.lean"], module_path=False,
        )
        obligation_output = isolated_lean(
            bwrap, lean, lean_path, tmp,
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True,
        )
        proof_output = isolated_lean(
            bwrap, lean, lean_path, tmp,
            ["-o", "Proof.olean", "Proof.lean"], module_path=True,
        )
        anchor_output = isolated_lean(
            bwrap, lean, lean_path, tmp, ["AnchorAudit.lean"], module_path=True,
        )
        validation_output = isolated_lean(
            bwrap, lean, lean_path, tmp, ["Validation.lean"], module_path=True,
        )
    finally:
        shutil.rmtree(tmp)

    outputs = {
        "ObligationTree.lean": obligation_output,
        "Proof.lean": proof_output,
        "Validation.lean": validation_output,
    }
    observed = []
    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            axioms = printed_axioms(outputs[module], declaration)
            assert axioms == ALLOWED_AXIOMS, (declaration, axioms)
            observed.append((declaration, axioms))
    assert len(observed) == 6
    assert proof_output.count("Declarations are sorry-free!") == 3
    assert validation_output.count("Declarations are sorry-free!") == 2
    for fragment in (
        "QuadraticForm.equivalent_one_neg_one_weighted_sum_squared",
        "QuadraticForm.sigPos_add_sigNeg_add_radical",
        "hf.to_localInverse hf' hn",
    ):
        assert fragment in (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    combined = "\n".join(
        (statement_output, obligation_output, proof_output, anchor_output, validation_output)
    )
    assert "sorryAx" not in combined
    assert "declaration uses 'sorry'" not in combined
    assert "error:" not in combined

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["depends_on"] == ["S56-M-0600-PROOF"]
    assert receipt["root_vector_after"] == receipt["root_vector_after_worker_selftest"]
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation_checker_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids",
            "observationally_covered_obligation_ids",
            "partially_covered_obligation_ids", "covered_declarations", "scope_boundary",
        )
    }
    result = receipt["result"]
    assert result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["accepted_closed_obligation_ids"] == []
    assert result["provisionally_observed_obligation_ids"] == ["M0600-S-DIMZERO"]
    assert result["complete_transitive_trust_and_provenance"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_release_verification_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert hashlib.sha256(SUMMARY_BYTES).hexdigest() == SUMMARY_SHA256
    assert receipt["execution"]["stdout_sha256"] == SUMMARY_SHA256
    assert receipt["execution"]["stdout_bytes"] == len(SUMMARY_BYTES) == 926
    assert receipt["execution"]["stdout_line_count"] == len(SUMMARY_LINES) == 9
    assert receipt["first_failed_gate"] == "dependency.S56-M-0600-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == ["M0600-T-ENGINE"]
    assert receipt["accepted_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:]
        for line in run(["git", "status", "--short", "--untracked-files=all"]).splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
