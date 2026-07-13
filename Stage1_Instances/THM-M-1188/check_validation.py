#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-1188-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1188"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLT_REGULAR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
ITEM = "S56-M-1188-VALIDATION"
THEOREM = "THM-M-1188"
BASE_REVISION = "4d2c77230343716176b4192dc38e26f4c20c7547"
BASE_TREE = "9eebdfdfda6b289fea0b6e778fae8e13327395b2"
EXPRESSION_SHA256 = "0564abe47c982ec2eea57b707d8e761b8f00999b3d35fc307f18e406c163ffd8"
DENOMINATOR_SHA256 = "2c191411ea8f03dd1a2dcd2e206e72315fb39f01c51f6e6c146efbbe93b55ffd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLT_REGULAR_TREE = "32c9eace926573a9981787ae97643e520353c893"
FLT_REGULAR_REMOTE = "https://github.com/leanprover-community/flt-regular.git"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_TOOL_HASHES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
    "python3": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
EXPECTED_INPUTS = {
    "Statement.lean": "1e84c9edaec0f86f93e7f8ad8e0eca243fa5ba0efa3c3cb8bfc329bff9d0a4b0",
    "ObligationTree.lean": "ae204448fee6a75acf367b43874ae3d5bb6b026d759ccabae4f04594b074b959",
    "Proof.lean": "0043ed68df3928c41f7ed189b48c970581c2aaf9c6ab4108374848ff7bde1a97",
    "Validation.lean": "cb784237e3b7e47598cadec4614a028b64ad1bf63da2c58671064690a1790e8e",
    "statement.json": "5b47a6e4c1e86be177945dd151a0b903bf46dd9d467bf7340cfa6683ee7f7d6a",
    "intake.json": "bdd4fbea5dd89223eff75ddd9f26d21c7b1534b3dd9919f21e6e5021e64aeaf7",
    "anchor-audit.json": "84fe65f23a0c34421b25e04aaab8c85bbb71d56543b15f0fb355a9ebfdbaab86",
    "obligation-registry.json": "2edda82e85a548d5a756aaf757b9de7c9a813e4aabeea84d84e5933d7c6fa608",
    "typed-graphs.json": "02fc0a5882f0415aa8f9847fff723b556a56bddfb52b1d4c9b9921581925dda6",
    "validation-specs.json": "67871c7863cd3b43606095ecaa2c3bdd1994f86e56352119b4baa64a903058e7",
    "proof-receipt.json": "97269855a03efccc85cf372d3e2a330a1eafcda9f1eb301969dfd4ec53679388",
    "check_validation.sh": "50eafa1e2d35630885dd6521cc1e71a8f9040874b59d4fcea9b11d53e94535a4",
    "validation-spec.json": "300dc2327845d8eb8cd9f7264a1da6a8b8b831d714059544fb01e84448d1f4ae",
    "validation-phase.md": "aad93d83d71bf99f1c12b61f880e723de980ab77b66cd14198978b3a562486d0",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1188/Validation.lean",
    "Stage1_Instances/THM-M-1188/check_validation.py",
    "Stage1_Instances/THM-M-1188/check_validation.sh",
    "Stage1_Instances/THM-M-1188/validation-phase.md",
    "Stage1_Instances/THM-M-1188/validation-receipt.json",
    "Stage1_Instances/THM-M-1188/validation-spec.json",
}
SUMMARY = (
    "PASS THM-M-1188 narrow validation",
    "PASS network-isolated lake env lean --trust=0 fresh-output replay: exact statement, proof root, frozen composition, and same-worker adapters elaborated",
    "PASS trust observation: 19 reports; checked roots and composition use exactly propext, Classical.choice, and Quot.sound",
    "PASS hygiene and selected provenance: source hashes, clean mathlib pin/tree/remote/license, compiled import artifacts, and tool identities agree",
    "FAIL CLOSED authority/state: proof prerequisite lacks master acceptance and the pre-proof graph has no proof evidence or node-specific closure reconciliation",
    "FAIL CLOSED provenance/TCB: foundation, source, complete transitive provenance, compiled closure, SBOM, and offline archive remain open",
    "FAIL CLOSED hermetic replay: read-only shared warm cache and current checkout are not a clean-checkout empty-cache offline cold build",
    "FAIL CLOSED independent verification: wrappers reuse Proof.lean in this worker; no distinct signed runner or independently implemented verifier exists",
    "audit_complete=false; theorem_complete=false",
)

if not __debug__:
    raise RuntimeError("validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


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


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 383 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-1188-PROOF"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1188-PROOF")
    assert predecessor["state"] == "[_]"
    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False

    canonical = statement["canonical_formal_target"]
    assert canonical["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1188-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(spec["covered_obligation_ids"]) == set(
        proof_receipt["provisionally_closed_obligation_ids"]
    )
    assert set(proof_receipt["open_proof_or_release_boundaries"]) == {
        "M1188-S-FOUNDATION", "M1188-X-SOURCE", "M1188-X-PROVENANCE",
    }
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["base_revision"] != BASE_REVISION
    old_proof = subprocess.run(
        ["git", "cat-file", "-e", f'{proof_receipt["base_revision"]}:Stage1_Instances/THM-M-1188/Proof.lean'],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    assert old_proof.returncode != 0

    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1188-ROOT")
    assert root["machine_debt"] == "M3" and root["evidence_ids"] == []
    assert root["provenance_id"] == "none" and root["owned_sources"] == []
    for oid in ("M1188-S-FOUNDATION", "M1188-X-SOURCE", "M1188-X-PROVENANCE"):
        node = next(node for node in graphs["nodes"] if node["obligation_id"] == oid)
        assert node["evidence_ids"] == [] and node["validity"]["revocation_state"] == "open"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale input: {name}"
        assert receipt["inputs"].get(name) == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected
        assert receipt["inputs"][name] == expected

    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert FLT_REGULAR.is_dir()
    assert git("rev-parse", "HEAD", cwd=FLT_REGULAR) == FLT_REGULAR_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=FLT_REGULAR) == FLT_REGULAR_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=FLT_REGULAR) == ""
    assert git("remote", "get-url", "origin", cwd=FLT_REGULAR) == FLT_REGULAR_REMOTE
    root_lake = subprocess.run(
        [str(Path.home() / ".elan/bin/lake"), "env", "lean", "--version"],
        cwd=LEAN_ROOT, env={**os.environ, "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, check=False,
    )
    assert root_lake.returncode == 0 and "Lean (version 4.29.0" in root_lake.stdout

    executable_paths = {
        "lean": Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean",
        "lake": Path.home() / ".elan/bin/lake",
        "python3": Path(os.path.realpath(shutil.which("python3") or "")),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bwrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
    }
    for name, path in executable_paths.items():
        assert path.is_file() and sha256(path) == EXPECTED_TOOL_HASHES[name], (name, path)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe|opaque|extern)\b|"
        r"\bimplemented_by\b|\bnative_decide\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(source_without_comments((HERE / name).read_text(encoding="utf-8"))) is None
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
    ):
        assert receipt["recipe"][key] == spec[key]
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["first_failed_gate"] == "dependency.S56-M-1188-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert set(result["observed_axioms"]) == EXPECTED_AXIOMS
    assert result["axiom_report_count"] == 19
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["complete_provenance_and_tcb"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=600)
    assert "PASS axiom profile: 19 reports" in replay
    assert replay.count("Declarations are sorry-free!") == 2
    assert "error:" not in replay and "sorryAx" not in replay
    assert platform.system() == "Linux"
    print("\n".join(SUMMARY))


if __name__ == "__main__":
    main()
