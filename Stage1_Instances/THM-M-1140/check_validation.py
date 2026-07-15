#!/usr/bin/env python3
"""Fail-closed validator for S56-M-1140-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import pwd
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1140"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1140-VALIDATION"
THEOREM = "THM-M-1140"
BASE_REVISION = "557b928b377b386864527c9fb4831d45857837aa"
BASE_TREE = "e677879a6eb4cb9d6795ba1bd78726af06ab9465"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "541e5716657e39b56e24f220a7118beecc0fc4f2a196312b7f278af92302b3b4"
DENOMINATOR_SHA256 = "355cbcf3b25f5e8ac67d3d814a268744dbe8ba8ae8afaec651199e64d6520bee"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_INPUTS = {
    "Statement.lean": "c0f7ef8b8c003598b09d5984804630ca3d47bfde472c7748e5ee2035e6ef418a",
    "ObligationTree.lean": "ed5fb3a36f248104c0f66458270fc362233a1634b46586cb33b2f006bc9f504b",
    "Proof.lean": "998609dc7186a333fbf3ae6220e6b7f63bd1b5c22995af1bd752a9d2d7de98ae",
    "Validation.lean": "c18f1f895224b991c5f11acee5edade11cd11af8a1d2fbcc3618bb09cb82241e",
    "intake.json": "7dbdd20f4813f3b6e63c397482b485336630512eb154a57644caa8ea464a092d",
    "statement.json": "57a7ddf69672b1b2bfb5be53d0752572c9b07b5915b7205da399e4b714ec1379",
    "anchor-audit.json": "7f37819dc454ae67b7e0363ea50d85ac378b377bda58806f1b2eeff1fd1ffdfc",
    "obligation-registry.json": "14dc0bf5e61a29063a530b3510c6b59f21be8d989c94ac2c13d31af481c90826",
    "typed-graphs.json": "6e99d7b827544e1cd78a882a84a8bd28fb8e1eaa66d33f49feec55b21d2b7477",
    "validation-specs.json": "bf0ff6ca61da45ca67a600a756b68505ddee03f06f79b71185f9b82b0c31b20b",
    "proof-receipt.json": "4f2f07e773b2ef59ea2cb01584d40d463a14384e3dcc22f7024f50a9bc880fbd",
    "proof-validation.md": "980e16fbe13285481b4481aabef2b1aebc740f792d9ba05e676242f1e0f7b82c",
    "check_proof.sh": "fbff95b1fb7389eab5475a402599d566230ffa8d0e5ef2890024c0895b7979df",
    "validation-spec.json": "08bdd99c41d3d73698f791169ce83b6ada56e97b7d359415ccfe30b2bdecf20d",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TOOL_SHA256 = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python3": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
SOURCE_PROVENANCE = {
    "Mathlib/Analysis/InnerProductSpace/Harmonic/Basic.lean": (
        "39aefbe7fac2fae9017f3c47ee4c0baea8f6ac64cf1511a4776fc6c917ae16ea",
        "f96c43dbb5796b9ff5fd71831fdc9ef6cc5d60b1",
        "5cfcc289af8bfa1af7235a44628037cf1468e61681f4207c246ca5f09b432241",
    ),
    "Mathlib/Analysis/Calculus/DerivativeTest.lean": (
        "4d89b7883a04a373e0dc4d73b0163a7542a690249d9316509701e96074fb7dbb",
        "de697940d455520137948b48e506e2377b14f5a3",
        "e16cab82cfcf4ca5b58c533ee745886cfd088b745aca3efb4231cb58ad731a8a",
    ),
    "Mathlib/Analysis/InnerProductSpace/Calculus.lean": (
        "695878ec0ba211d9027445a28f4474ed5716237a1bf960d34375f7233b4906e5",
        "efec86444df931af495584ae8a6f4a39e9abe9b1",
        "3582d6dae6ed23f5a39cb31d8c61530a6e3d6a6300deaa474ba6d8b70237ff24",
    ),
    "Mathlib/Analysis/InnerProductSpace/PiL2.lean": (
        "4df49dd497992b022f3d18ee79ea0ae5536be7a452779b4c2400b1d136b7a2bb",
        "1809daf0493b8bbfde55c8f4d1bdcb2eb3feda7a",
        "b421e082ec7b4bfab92f0fd05c51968deb0933812e975beec781bdab0a826ea4",
    ),
    "Mathlib/Analysis/InnerProductSpace/Harmonic/HarmonicContOnCl.lean": (
        "33aefdda3bea8d84225fa77525ab4b4a84751f7492d261a2920c517022f32278",
        "d885a8372fc7e1116d0bce17d29371ec1c9fdc56",
        "0c40b3ba1110b09488512b7ec89dcab5db90898f53838563fbff9155c90415d4",
    ),
    "Mathlib/Topology/Connected/Clopen.lean": (
        "41977a3ba127bb92d2fe8099836fb72330c1f91986ce0a9e905af9b454abad7b",
        "1f9dafd93b92a9deb9f4b898c532e46787e17f38",
        "eca19fae13a3183a1336f169e1c8fa6a1941e5760888a6107c9df1606ebcad03",
    ),
    "Mathlib/Analysis/SpecialFunctions/ExpDeriv.lean": (
        "7678c4712458f4129eb9b29ea7eb332467501cc8a6688547d1ed1b25f8849722",
        "65e0c15f2921a9dfd6bea14c06d2b46699dccc2a",
        "b5f7634f3db34e8116ca98ad81a4045561f10f22345e34ecf6db900da4e89de2",
    ),
    "Mathlib/Analysis/Normed/Affine/AddTorsor.lean": (
        "abe2c3faf41cddfc541a808366edfe90b777bed5b20b753a20d4e1b7e617caf8",
        "0beb28f923ee47b2627b89c16c1e161fb9bdbeb9",
        "9f35188e21006005e75443a8978979c0a9eb1f24f605e1c526a72405d86adef4",
    ),
}

MACHINE_IDS = {
    "M1140-ROOT", "M1140-S-DEFINITIONS", "M1140-S-DOMAIN",
    "M1140-S-BOUNDARY", "M1140-S-FOUNDATION", "M1140-N-MAX-LEVEL",
    "M1140-L-MEAN-VALUE", "M1140-L-CONTINUITY", "M1140-L-LEVEL-CLOSED",
    "M1140-L-LEVEL-OPEN", "M1140-L-CONNECTED", "M1140-T-LOCAL-PACKAGE",
    "M1140-T-PROPAGATION-PACKAGE", "M1140-T-ASSEMBLE",
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
    "PASS THM-M-1140 network-isolated trust-zero replay: exact statement, frozen composition, repo-local proof root, and same-worker probes elaborated from fresh outputs",
    "PASS trust observation: root/package/probe declarations are sorry-free and use exactly propext, Classical.choice, and Quot.sound; transitive probe closure reports no bodyless nonaxioms or unsafe declarations",
    "PASS selected provenance: local input hashes, clean pinned mathlib revision/tree/origin/license, eight theorem/proof direct-import source blobs, and their oleans agree",
    "FAIL CLOSED authority: proof master acceptance and Gaussian-barrier-to-frozen-bridge architecture reconciliation remain open; accepted graph stays H2/M3/R3",
    "FAIL CLOSED provenance/TCB: accepted foundation policy, complete transitive source/body/compiled-object/toolchain/SBOM closure, and offline archive remain open",
    "FAIL CLOSED hermetic replay: network is denied and outputs are fresh, but shared warm pinned oleans are not a new-checkout empty-cache cold build",
    "FAIL CLOSED independent verification: the probes import Proof.lean in this worker; no distinct signed runner or independently implemented verifier exists",
    "audit_complete=false; theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 900.0

if sys_flags := __import__("sys").flags:
    if sys_flags.optimize:
        raise SystemExit("validation failed: Python optimization disables assertions")


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: float | None = None,
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    effective_timeout = min(remaining, timeout) if timeout is not None else remaining
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=effective_timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=30).rstrip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = depth = 0
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
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, (declaration, len(matches))
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def main() -> None:
    assert "STAGE1_SKIP_OUTPUT_CHECK" not in os.environ, (
        "the canonical validation recipe does not permit bypassing receipt checks"
    )
    os.umask(0o022)
    spec = load(HERE / "validation-spec.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    receipt_path = HERE / "validation-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 345 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 345,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-1140-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1140-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    canonical = statement["canonical_formal_target"]
    assert canonical["declaration"] == (
        "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1140-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(registry["frozen_denominators"]["required_machine"]) == MACHINE_IDS

    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == [
        "M1140-T-LOCAL-PACKAGE", "M1140-T-PROPAGATION-PACKAGE",
    ]
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1140-ROOT")
    foundation_node = next(
        row for row in graphs["nodes"] if row["obligation_id"] == "M1140-S-FOUNDATION"
    )
    provenance_node = next(
        row for row in graphs["nodes"] if row["obligation_id"] == "M1140-X-PROVENANCE"
    )
    assert root_node["machine_debt"] == "M3" and root_node["human_debt"] == "H2"
    assert root_node["readability_debt"] == "R3" and root_node["evidence_ids"] == []
    assert foundation_node["machine_debt"] == provenance_node["machine_debt"] == "M4"
    assert "policy-audit-pending" in foundation_node["foundation_profile"]
    assert "transitive-closure-pending" in provenance_node["tcb_profile"]

    assert frozen_specs["item_id"] == "S56-M-1140-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 16
    assert {tuple(row["argv"]) for row in frozen_specs["recipes"]} == {
        ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }
    assert "no analytic package closure" in frozen_specs["status_boundary"]
    mean_value = next(
        row for row in registry["obligations"] if row["obligation_id"] == "M1140-L-MEAN-VALUE"
    )
    assert mean_value["kind"] == "bridge" and mean_value["machine_eligibility"] == "required"

    assert proof_receipt["item_id"] == "S56-M-1140-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert set(proof_receipt["provisionally_closed_obligation_ids"]) == MACHINE_IDS
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert "Gaussian barrier" in proof_receipt["architecture_reconciliation"]
    assert "master review" in proof_receipt["architecture_reconciliation"].lower()

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_source = source_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" in validation_source
    assert "theorem exactRootProbe : HarmonicStrongMaximumPrinciple" in validation_source
    assert "theorem exactCompositionProbe : HarmonicStrongMaximumPrinciple" in validation_source
    theorem_imports: set[str] = set()
    for name in ("Statement.lean", "Proof.lean"):
        theorem_imports.update(
            re.findall(r"^import (Mathlib\.[^\s]+)$", (HERE / name).read_text(), re.MULTILINE)
        )
    assert theorem_imports == {path.removesuffix(".lean").replace("/", ".") for path in SOURCE_PROVENANCE}

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
        "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent",
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]
    assert spec["env_allowlist"] == {}
    assert "rejects STAGE1_SKIP_OUTPUT_CHECK" in spec["orchestration_environment_boundary"]
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "entire structured Python recipe" in spec["network_policy_boundary"]
    assert set(spec["covered_obligation_ids"]) == MACHINE_IDS | {"M1140-X-PROVENANCE"}
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple",
        "Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple_of_packages",
        "Stage1Instances.THM_M_1140.interiorLocalRigidity",
        "Stage1Instances.THM_M_1140.connectedLevelPropagation",
        "Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple",
        "Stage1Instances.THM_M_1140.Validation.exactRootProbe",
        "Stage1Instances.THM_M_1140.Validation.exactCompositionProbe",
    }

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, (source_digest, blob, olean_digest) in SOURCE_PROVENANCE.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / relative.replace(
            ".lean", ".olean"
        )
        assert sha256(source) == source_digest
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(olean) == olean_digest

    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_bin = account_home / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    tools = {
        "lean": toolchain_bin / "lean",
        "lake": toolchain_bin / "lake",
        "python3": Path("/usr/bin/python3").resolve(),
        "git": Path("/usr/bin/git").resolve(),
        "bwrap": Path("/usr/bin/bwrap").resolve(),
    }
    for name, path in tools.items():
        assert path.is_file() and sha256(path) == TOOL_SHA256[name], (name, path)
    assert LEAN_COMMIT in run([str(tools["lean"]), "--version"], cwd=LEAN_ROOT)
    assert "Lake version 5.0.0" in run([str(tools["lake"]), "--version"], cwd=LEAN_ROOT)

    fixed_env = {
        "HOME": str(account_home),
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run(
        [str(tools["lake"]), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT, env=fixed_env, timeout=30,
    ).strip()
    project_build = str((LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve())
    lean_path_entries = [
        entry for entry in lean_path.split(":")
        if entry and str(Path(entry).resolve()) != project_build
    ]
    assert project_build not in {str(Path(entry).resolve()) for entry in lean_path_entries}
    assert all("/tmp/" not in entry for entry in lean_path_entries)
    lean_path = ":".join(lean_path_entries)

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1140-validation-", dir="/tmp"))
    outputs: dict[str, str] = {}
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(name: str, *, module_path: bool) -> str:
            path = f"{tmp}:{lean_path}" if module_path else lean_path
            args = [str(tools["lean"]), "--trust=0", "-j1", "-t0"]
            if name != "Validation.lean":
                args += ["-o", str(tmp / name.replace(".lean", ".olean"))]
            args.append(name)
            lean_env = dict(fixed_env)
            lean_env["HOME"] = str(tmp / "home")
            lean_env["LEAN_PATH"] = path
            return run(args, cwd=tmp, env=lean_env)

        outputs["statement"] = isolated_lean("Statement.lean", module_path=False)
        outputs["obligation"] = isolated_lean("ObligationTree.lean", module_path=True)
        outputs["proof"] = isolated_lean("Proof.lean", module_path=True)
        outputs["validation"] = isolated_lean("Validation.lean", module_path=True)
    finally:
        shutil.rmtree(tmp)

    all_output = "\n".join(outputs.values())
    assert hashlib.sha256(outputs["statement"].encode("utf-8")).hexdigest() == EXPRESSION_SHA256
    assert "error:" not in all_output and "declaration uses 'sorry'" not in all_output
    assert "sorryAx" not in all_output
    declarations = {
        "obligation": [
            "Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple_of_packages",
        ],
        "proof": [
            "Stage1Instances.THM_M_1140.interiorLocalRigidity",
            "Stage1Instances.THM_M_1140.connectedLevelPropagation",
            "Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple",
        ],
        "validation": [
            "Stage1Instances.THM_M_1140.Validation.exactRootProbe",
            "Stage1Instances.THM_M_1140.Validation.exactCompositionProbe",
        ],
    }
    for stream, names in declarations.items():
        for declaration in names:
            assert reported_axioms(outputs[stream], declaration) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 3
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure_match is not None
    assert receipt is not None
    assert receipt["provenance"]["transitive_probe_observation"] == (
        f"{closure_match.group(1)} declarations across {closure_match.group(2)} modules; "
        "axioms [propext, Classical.choice, Quot.sound]; bodyless_nonaxioms []; unsafe []"
    )

    assert receipt is not None and packet is not None
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation-spec.json"] == EXPECTED_INPUTS["validation-spec.json"]
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["recipe"] == spec
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["recipe_output"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    assert receipt["recipe_output"]["stdout_bytes"] == len(expected_stdout.encode("utf-8"))
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert set(result["observed_axioms"]) == EXPECTED_AXIOMS
    assert result["kernel_sorry_reachable_unsafe_and_supplemental_source_scan"] == "pass"
    assert result["accepted_root_closed"] is False
    assert result["complete_provenance_and_tcb"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["first_failed_gate"] == "dependency.S56-M-1140-PROOF.master_acceptance"
    assert receipt["known_failures"] == packet["known_failures"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    receipt_status_input = receipt["nonrelease_input_set"]
    canonical_status = "\n".join(
        line for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    ) + "\n"
    assert receipt_status_input["git_status_sha256_excluding_preexisting_lake"] == (
        hashlib.sha256(canonical_status.encode("utf-8")).hexdigest()
    )
    assert receipt_status_input["tracked_patch_sha256"] == hashlib.sha256(
        subprocess.check_output(
            ["/usr/bin/git", "diff", "--binary", "--", "."], cwd=ROOT
        )
    ).hexdigest()
    assert receipt_status_input["lake_symlink_target_sha256"] == hashlib.sha256(
        (os.readlink(LEAN_ROOT / ".lake") + "\n").encode("utf-8")
    ).hexdigest()
    assert receipt_status_input["preexisting_untracked_input"] == (
        "Formalizations/Lean/.lake symlink to the automation-provided canonical dependency closure"
    )
    assert receipt_status_input["worker_selftest_sha256"] == sha256(packet_path)
    assert receipt["environment"]["locale_timezone_threads_umask"] == (
        "C.UTF-8 / UTC / 1 / 0022"
    )

    for relative in CHANGED_PATHS:
        path = ROOT / relative
        if path.exists():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path
    assert platform.system() == "Linux"
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
