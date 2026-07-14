#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0559-VALIDATION."""

from __future__ import annotations

from datetime import datetime
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


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0559"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0559-VALIDATION"
THEOREM = "THM-M-0559"
BASE_REVISION = "6cf20c1ab97fcd6970455baa23022062ebc14fe1"
BASE_TREE = "5fa65edc9a9b91b49f7f925ad524ec374328e14c"
STATEMENT_SHA256 = "f6db49c559ac718c96eb566d83e69748ae2d3fd0a1e95396465cbfa1e7328f1c"
STATEMENT_RECORD_SHA256 = "6d7925c9f37f5b2506f403b1fbda81a200e1e37edac1579a6c8bac1c0a4da1a4"
STATEMENT_OUTPUT_SHA256 = "ceed321b7234e4250269966bf4c6583e6f62b9305361da2ec910973e62c083be"
STATEMENT_OUTPUT_BYTES = 465
DENOMINATOR_SHA256 = "040c9f0d06a8432b0cf5768d43391f143d820754686514252ce484f53d3446fc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
LEAN_MODULES = ("Statement.lean", "Proof.lean", "Validation.lean")

PROOF_DECLARATIONS = (
    "joined_of_component_eq",
    "exists_preimage_joined",
    "joined_of_map_joined",
    "components_surjective_iff",
    "components_injective_iff",
    "components_bijective_iff",
    "nonempty_zerothHomotopy_iff",
    "nonempty_iff_of_components_bijective",
    "empty_branch",
)
DIFFERENTIAL_DECLARATION = "empty_branch_direct"
CUT = ["M0559-N-COMPONENTS", "M0559-T-FORWARD"]
DIRECT_COVERED_IDS = [
    "M0559-S-DEFINITIONS",
    "M0559-S-TRANSPORT",
]
OBSERVATIONAL_COVERED_IDS = ["M0559-X-PROVENANCE", "M0559-X-TRUST"]
PARTIAL_COVERED_IDS = ["M0559-N-COMPONENTS", "M0559-B-EMPTY"]
VALIDATED_DECLARATIONS = [
    "Stage1Instances.THM_M_0559.WhiteheadTarget",
    "Stage1Instances.THM_M_0559.whiteheadTarget_iff_expandedSourceShape",
    *[
        f"Stage1Instances.THM_M_0559.Proof.{declaration}"
        for declaration in PROOF_DECLARATIONS
    ],
    "Stage1Instances.THM_M_0559.Validation.empty_branch_direct",
]

EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "ObligationTree.lean": "471cea10d3c2d18632dbd7aafcb13e63fa7876eefef7e86359a7d2b1b1b6985c",
    "Proof.lean": "f0b1ec9ac606a8943e2aaaf711f2704caf628a33532d71709b0ff370f454b660",
    "Validation.lean": "fed617a1585f602720fab7065ffd9fc0fab8455557e08a965a5f98d5f87ebe84",
    "instance.json": "9230796550017250686ffc137f97e087936358a6cf82ef718b735001476f181e",
    "task-dag.json": "f21cda9d050bdceaf17e018d98b6da79edb0c5b346ba5ab46f616059fc22aa71",
    "statement.json": STATEMENT_RECORD_SHA256,
    "anchor-audit-receipt.json": "1eaaf9b8509815a4017083eaff581fc62f37125673e32ec1c992ba2c42cb97fb",
    "obligation-registry.json": "9a07086c9d49e00ff8100e18064d50578d253f5c6f6976cce5ae1e186bf6b9b6",
    "typed-graphs.json": "5cd995d027f4dd1dc5c54e7d6c0bf0c29985a50ab1a9701d21daa967fea2c411",
    "proof-receipt.json": "aba8729230ab01409ce50e61980fab266b0875aaf3adb11141d4b78d3279ec86",
    "proof-blocker.json": "9970ae61a7de898f34a2d7f6d55e47ff868f69883363f4ac91db4b5f1cd4b171",
    "source-statement-crosswalk.md": "7b818de32e06143405946b9fbf53658cd7e3a92b91386accb45979df0b942359",
    "check_obligation_tree.py": "676ff2cb4bbc0e6d4e745649fb5b711e5a1949c87d9b77c6b7c75bebedb271a7",
}

PINNED_IMPORTS = {
    "Mathlib/Topology/CWComplex/Classical/Basic.lean": {
        "source_blob": "562737853db77f0cf82cb34600efc19f0f8ec278",
        "source_sha256": "90f8848cdf8d82b0d0fc17108de9b769410f13c7d3a8b99c092e0bd051b9bd94",
        "olean_sha256": "27b14992d67f2dcc8794005786ea5219369d8b5dc6bb3c3241652e71cb1a7c0d",
    },
    "Mathlib/Topology/Homotopy/Equiv.lean": {
        "source_blob": "e2483ec51a00c190eda1ac0a481b02527da380b7",
        "source_sha256": "ae10cc95ccfd5a28d540fa2701b50ca852ec7979c34093e56d982b6a0fe037a3",
        "olean_sha256": "698b1e3c9a88a9ad58bcf11d95663c88377820eec929c4ef2d5ce8d04f65abf6",
    },
    "Mathlib/Topology/Homotopy/HomotopyGroup.lean": {
        "source_blob": "02446f9239282c4353dba6bcb50655767d91e3f0",
        "source_sha256": "0233597af0b0db82315ec206cacf9b88d62ae7d2cd05a099a8e4c36b17c39104",
        "olean_sha256": "e28af21c8704d2792d260f5c3dc219860f4c88e66248ad492a17bd8ce409a25c",
    },
    "Mathlib/Topology/Homeomorph/Defs.lean": {
        "source_blob": "eb1d9c5da67c10c77d0b746fc14ad48433e94312",
        "source_sha256": "fa07e3709be98fd676277ae1cfd8585d6f3e145246589b123ea5dedaee2b4ffb",
        "olean_sha256": "97c6199e1c9e18d98d87c25c48418d1b8bc37b4c71b290f136a93bd8bce7d3e6",
    },
}

SUMMARY_LINES = (
    "PASS THM-M-0559 narrow validation",
    "PASS network-isolated trust-zero replay: frozen statement, nine partial proof declarations, and differential empty branch elaborated",
    "PASS hygiene: kernel sorry checks and a comment-aware prohibited-construct scan passed for the hash-bound Lean sources",
    "PASS trust observation: ten proof declarations use exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: target hashes, denominator, clean mathlib pin/tree/remote, four source/blob/olean identities, license, and tool hashes agree",
    "FAIL CLOSED authority/root: proof predecessor is provisional and unaccepted; the exact Whitehead root has no proof body and remains H3/M4/R4",
    "FAIL CLOSED node mapping: B-EMPTY is only a planned-fingerprint implementation candidate and the component/nonempty/forward cut remains open",
    "FAIL CLOSED complete trust/hermeticity: selected imports and a shared warm cache are not a transitive TCB/SBOM closure or cold offline replay",
    "FAIL CLOSED independence: the differential branch ran in this worker checkout and cache, not on a distinct signed independent runner",
    "audit_complete=false; theorem_complete=false",
)

REQUIRED_COMMANDS = [
    ["python3", "Docs/tools/check_stage1_standard.py"],
    ["python3", "scripts/stage1_target.py", "check"],
    ["python3", "scripts/stage1_target.py", "show", "THM-M-0559"],
    ["python3", "Stage1_Instances/THM-M-0559/check_obligation_tree.py"],
    ["bash", "Stage1_Instances/THM-M-0559/check_proof.sh"],
    ["python3", "-I", "-B", "Stage1_Instances/THM-M-0559/check_validation.py"],
    ["python3", "-m", "json.tool", "Stage1_Instances/THM-M-0559/validation-spec.json"],
    ["python3", "-m", "json.tool", "Stage1_Instances/THM-M-0559/validation-receipt.json"],
    ["python3", "-m", "json.tool", ".stage1-worker-selftest.json"],
    [
        "PYTHONPYCACHEPREFIX=/tmp/stage1-m0559-validation-pycache",
        "python3", "-m", "py_compile",
        "Stage1_Instances/THM-M-0559/check_validation.py",
    ],
    [
        "git", "diff", "--check", "--",
        ".stage1-worker-selftest.json", "Stage1_Instances/THM-M-0559",
    ],
]
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0

KNOWN_FAILURES = (
    "S56-M-0559-PROOF is only provisionally self-tested [_], not master-accepted, and its receipt accepts no closed obligation.",
    "WhiteheadTarget has no proof body. M0559-N-COMPONENTS and M0559-T-FORWARD remain the frozen root cut; the nonempty cellular, skeleton, extension, colimit, recomposition, and exact-forward packages are open.",
    "M0559-B-EMPTY has only a planned registry fingerprint, so both checked implementations remain candidates pending master exact-statement mapping; no M0-L or accepted closed-obligation status is claimed.",
    "The frozen graph remains H3/M4/R4. Its S-TRANSPORT and T-ASSEMBLE entries are conditional interfaces, not a proof of the missing DirectWhiteheadCore or canonical root.",
    "The external jzxia Whitehead theorem is anchor-only at incompatible Lean/mathlib pins and a different CW representation, universe/nonempty scope, and weak-equivalence predicate; no checked bridge exists.",
    "The frozen target omits T2Space although pinned CWComplex permits non-Hausdorff spaces; validation cannot silently add Hausdorffness or substitute a narrower theorem.",
    "Primary theorem/page/assumption/errata review, H0, independently reviewed R0, a complete transitive provenance/SBOM, and an accepted foundation/TCB profile remain open.",
    "The replay used the automation-provided shared warm .lake cache. Network was denied and sources were copied to a fresh directory, but this is not a clean checkout, empty-cache cold build, offline-restored archive, or deterministic release bundle.",
    "Validation.lean imports only Statement and independently reconstructs the empty branch, but it ran under this worker identity, checkout, kernel, and shared cache; it is not a second signed independent runner or minimal release verifier.",
    "AUDIT-Z, THEOREM-Z, E0/E1, M0 root closure, release, theorem completion, and master acceptance remain false.",
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
    timeout: int = 180,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    assert remaining > 0, "validation recipe exceeded its 600-second wall-clock bound"
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=min(timeout, remaining),
        check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


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
    qualified = re.escape(declaration)
    match = re.search(
        rf"'[^']*{qualified}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_sorry_free(output: str, declaration: str) -> None:
    diagnostic = re.compile(
        rf"declaration uses 'sorry': '[^']*{re.escape(declaration)}'"
    )
    assert diagnostic.search(output) is None, (declaration, output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 607 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 607,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0559-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0559-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"][name] == expected, f"misreported receipt input: {name}"
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["lean-toolchain"] == LEAN_TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == LAKE_MANIFEST_SHA256
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256

    assert instance["lifecycle"] == local_dag["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H3", "M": "M4", "R": "R4"}
    assert instance["theorem_complete"] is False and local_dag["accepted_states"] == []
    assert all(row["state"] == "open" for row in local_dag["tasks"])
    assert statement["canonical_declaration"] == "Stage1Instances.THM_M_0559.WhiteheadTarget"
    assert statement["source_sha256"] == STATEMENT_SHA256
    assert statement["proof_claimed"] is statement["theorem_complete"] is False

    assert registry["root_obligation_id"] == "M0559-ROOT"
    assert registry["frozen_against_statement_sha256"] == STATEMENT_RECORD_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == ["M0559-S-TRANSPORT", "M0559-T-ASSEMBLE"]
    assert closure["root_machine_debt"] == "M4"
    assert closure["remaining_root_cut_set"] == CUT
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert all(node["obligation_id"] != "M0559-ROOT" or node["machine_debt"] == "M4" for node in graphs["nodes"])

    fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in registry["obligations"]}
    assert fingerprints["M0559-B-EMPTY"].startswith("planned:v1:sha256:")
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["provisionally_implemented_obligation_ids"] == ["M0559-B-EMPTY"]
    assert proof_receipt["obligation_statement_fingerprints"]["M0559-B-EMPTY"] == fingerprints["M0559-B-EMPTY"]
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof_blocker["remaining_root_cut_set"] == CUT
    assert proof_blocker["accepted_receipt_ids"] == []

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    olean_root = MATHLIB / ".lake" / "build" / "lib" / "lean"
    for relative, expected in PINNED_IMPORTS.items():
        source = MATHLIB / relative
        olean = olean_root / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["source_blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
    selected_sources = receipt["selected_dependency_provenance"]["selected_sources"]
    assert {row["file"]: {key: value for key, value in row.items() if key != "file"} for row in selected_sources} == PINNED_IMPORTS
    assert receipt["selected_dependency_provenance"]["revision"] == MATHLIB_REVISION
    assert receipt["selected_dependency_provenance"]["tree"] == MATHLIB_TREE
    assert receipt["selected_dependency_provenance"]["remote"] == MATHLIB_REMOTE
    assert receipt["selected_dependency_provenance"]["license_sha256"] == LICENSE_SHA256

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
    imports = re.findall(r"^import[ \t]+([^\n]+)$", validation, flags=re.MULTILINE)
    assert imports == ["Stage1_Instances.«THM-M-0559».Statement"]
    assert "empty_branch" not in validation.replace("empty_branch_direct", "")
    for marker in (
        "theorem empty_branch_direct",
        "hf.1.2",
        "Homeomorph.empty",
        "h.toHomotopyEquiv",
    ):
        assert marker in validation

    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    progress = (HERE / "proof-progress.md").read_text(encoding="utf-8")
    assert "not `H0` evidence" in crosswalk
    assert "no `T2Space` assumptions" in progress

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    assert lean.is_file() and sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert "Lean (version 4.29.0" in run([str(lean), "--version"])
    assert platform.system() == "Linux" and platform.machine() == "x86_64"
    python = Path(sys.executable).resolve()
    lake = Path(shutil.which("lake") or "").resolve()
    git_executable = Path(shutil.which("git") or "").resolve()
    bwrap_path = Path(shutil.which("bwrap") or "").resolve()
    assert python.is_file() and sha256(python) == PYTHON_EXECUTABLE_SHA256
    assert lake.is_file() and sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert git_executable.is_file() and sha256(git_executable) == GIT_EXECUTABLE_SHA256
    assert bwrap_path.is_file() and sha256(bwrap_path) == BWRAP_EXECUTABLE_SHA256

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m0559-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        module_dir = tmp / "Stage1_Instances" / THEOREM
        module_dir.mkdir(parents=True)
        for name in LEAN_MODULES:
            (module_dir / name).write_bytes((HERE / name).read_bytes())
        base = [
            str(bwrap_path),
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
            str(lean), "--trust=0", "-t0", "-R", ".",
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"
        relative = f"Stage1_Instances/{THEOREM}"
        outputs["Statement.lean"] = run(
            base + ["-o", f"{relative}/Statement.olean", f"{relative}/Statement.lean"],
            timeout=300,
        )
        outputs["Proof.lean"] = run(local + [f"{relative}/Proof.lean"], timeout=300)
        outputs["Validation.lean"] = run(local + [f"{relative}/Validation.lean"], timeout=300)

    statement_bytes = outputs["Statement.lean"].encode("utf-8")
    assert (hashlib.sha256(statement_bytes).hexdigest(), len(statement_bytes)) == (
        STATEMENT_OUTPUT_SHA256,
        STATEMENT_OUTPUT_BYTES,
    )
    assert "def Stage1Instances.THM_M_0559.WhiteheadTarget" in outputs["Statement.lean"]
    assert "ContinuousMap.HomotopyEquiv.toFun" in outputs["Statement.lean"]
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(outputs["Proof.lean"], declaration) == EXPECTED_AXIOMS
        assert_sorry_free(outputs["Proof.lean"], declaration)
    assert printed_axioms(outputs["Validation.lean"], DIFFERENTIAL_DECLARATION) == EXPECTED_AXIOMS
    assert_sorry_free(outputs["Validation.lean"], DIFFERENTIAL_DECLARATION)
    all_output = "\n".join(outputs.values())
    assert "sorryAx" not in all_output and "error:" not in all_output
    assert outputs["Proof.lean"].count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 1
    kernel_bytes = all_output.encode("utf-8")
    actual_kernel_result = (hashlib.sha256(kernel_bytes).hexdigest(), len(kernel_bytes))
    assert actual_kernel_result == (
        receipt["result"]["kernel_output_sha256"],
        receipt["result"]["kernel_output_bytes"],
    ), actual_kernel_result
    output_fields = {
        "Statement.lean": ("statement_output_sha256", "statement_output_bytes"),
        "Proof.lean": ("proof_output_sha256", "proof_output_bytes"),
        "Validation.lean": ("differential_output_sha256", "differential_output_bytes"),
    }
    for name, (digest_field, bytes_field) in output_fields.items():
        data = outputs[name].encode("utf-8")
        assert receipt["result"][digest_field] == hashlib.sha256(data).hexdigest()
        assert receipt["result"][bytes_field] == len(data)

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == DIRECT_COVERED_IDS
    assert spec["observationally_covered_obligation_ids"] == OBSERVATIONAL_COVERED_IDS
    assert spec["partially_covered_obligation_ids"] == PARTIAL_COVERED_IDS
    assert spec["covered_declarations"] == receipt["validated_declarations"] == VALIDATED_DECLARATIONS
    recipe_fields = {key: value for key, value in spec.items() if key not in {"schema_version", "item_id", "theorem_id"}}
    assert receipt["recipe"] == recipe_fields

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"]["statement_source_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target"]["elaborated_expression_output_sha256"] == STATEMENT_OUTPUT_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == DIRECT_COVERED_IDS
    assert receipt["observationally_covered_obligation_ids"] == OBSERVATIONAL_COVERED_IDS
    assert receipt["partially_covered_obligation_ids"] == PARTIAL_COVERED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["placeholder_and_unsafe_scan"] == "pass"
    assert receipt["result"]["selected_direct_provenance"] == "pass"
    assert receipt["result"]["proof_dependency_master_accepted"] is False
    assert receipt["result"]["accepted_root_machine_debt"] == "M4"
    assert receipt["result"]["complete_transitive_trust_and_provenance"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_release_verification_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0559-PROOF.master_acceptance"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["debt_vector_delta"] == {
        "before": {"H": "H3", "M": "M4", "R": "R4"},
        "after_worker_selftest": {"H": "H3", "M": "M4", "R": "R4"},
        "changed": False,
    }
    assert receipt["known_failures"] == list(KNOWN_FAILURES)
    started_at = datetime.fromisoformat(receipt["started_at"])
    ended_at = datetime.fromisoformat(receipt["ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at.tzinfo is not None and ended_at.tzinfo is not None
    assert started_at <= ended_at == validated_at <= datetime.now().astimezone()
    assert (ended_at - started_at).total_seconds() <= spec["timeout_seconds"]
    assert receipt["environment"]["platform"] == "Linux 7.0.0-27-generic x86_64"
    assert receipt["environment"]["locale"] == "LANG=C.UTF-8; LC_ALL=C.UTF-8"
    assert receipt["environment"]["timezone"] == "UTC"
    assert receipt["environment"]["lean_executable_sha256"] == LEAN_EXECUTABLE_SHA256
    assert receipt["environment"]["lake_executable_sha256"] == LAKE_EXECUTABLE_SHA256
    assert receipt["environment"]["python_executable_sha256"] == PYTHON_EXECUTABLE_SHA256
    assert receipt["environment"]["git_executable_sha256"] == GIT_EXECUTABLE_SHA256
    assert receipt["environment"]["bubblewrap_executable_sha256"] == BWRAP_EXECUTABLE_SHA256
    assert receipt["nonrelease_worktree"]["tracked_patch_sha256"] == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert receipt["nonrelease_worktree"]["pre_existing_untracked_path"] == "Formalizations/Lean/.lake"
    assert receipt["commands_and_exit_codes"] == [
        {"argv": row["argv"], "exit_code": row["exit_code"]} for row in packet["commands"]
    ]
    assert [row["argv"] for row in receipt["commands_and_exit_codes"]] == REQUIRED_COMMANDS
    assert all(row["exit_code"] == 0 for row in receipt["commands_and_exit_codes"])
    stdout_bytes = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["result"]["stdout_sha256"] == hashlib.sha256(stdout_bytes).hexdigest()
    assert receipt["result"]["stdout_bytes"] == len(stdout_bytes)

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
    assert packet["known_failures"] == receipt["known_failures"] == list(KNOWN_FAILURES)
    status = git("status", "--short", "--untracked-files=all")
    status_rows = [line for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"]
    assert {line[3:] for line in status_rows} == changed_paths, (status_rows, changed_paths)
    assert all(line.startswith("?? ") for line in status_rows), status_rows
    assert git("diff", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json")) == ""
    assert git("diff", "--cached", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json")) == ""
    assert receipt["nonrelease_worktree"]["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    untracked_hashes = receipt["nonrelease_worktree"]["owned_untracked_sha256"]
    assert set(untracked_hashes) == changed_paths - {f"Stage1_Instances/{THEOREM}/validation-receipt.json"}
    for relative, expected in untracked_hashes.items():
        assert sha256(ROOT / relative) == expected, relative

    for path in [ROOT / path for path in changed_paths]:
        assert_text_hygiene(path)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
