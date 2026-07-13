#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0626-VALIDATION."""

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


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0626"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0626-VALIDATION"
THEOREM = "THM-M-0626"
BASE_REVISION = "48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0"
BASE_TREE = "0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPRESSION_SHA256 = "5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231"
DENOMINATOR_SHA256 = "9c6e54699269263a82e13f7b771daf802103b4a4e0114d1c6a76a98918487270"
EXPECTED_INPUTS = {
    "Statement.lean": "eb03b777ac803b993a4787a8b58bd3f8f132218bda961bec4b4d1445a88bcca6",
    "AnchorAudit.lean": "791df6f8ed5ce37e75b7a7f431de69e5a5e28587015f3726003e027da20ab76b",
    "anchor-audit.json": "007066e76f0bfde71bfcbecafa34d0ffc6d00808037a8a91394a5b680abaddc8",
    "ObligationTree.lean": "8fbab093179985a82443e342fc90b172a9341ce90b3b6784a325aa3a0be6da3c",
    "Proof.lean": "218bc7aa1465996a3edb8aea41bd0598f48f1f432c3737396803e57c502ef115",
    "proof-receipt.json": "a4c10934c7e3697b32057216d21aab4aa4719dcdea3c5d317bc9a23cfd73560d",
    "obligation-registry.json": "9d2b1ee334d5403dce7cf9c0c435dc852808ab09f06c1c37a9c73c3450e6eef0",
    "typed-graphs.json": "b92113c2bdc30f9919ae968efcf7c13e52947a0c61792fc938aa94528413189a",
    "validation-specs.json": "ff3dec27d5f7488ba42fbfd650f7f9451f0335152294632d1f69ca06781e6033",
    "Validation.lean": "c998787b09a37730cebb47e18c39aac1deb634ed92164a3cd493e42956f37d41",
    "validation-spec.json": "406bfbfe7779e69f4314223094bb1e6e458e84332e096cac491a8a6fbda480bc",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE_SHA256 = "929f0e1c789b8c0ed10c3164aa174e369b9b250317c525a8ad2f2dcca2a65e9c"
TERMINAL_SOURCE_BLOB = "d3fdb9332b203fe7bb9e932a5136c7c6c9824f82"
TERMINAL_BODY_SHA256 = "52cd1c84042b3e3cce16ea0209bf323e7d976bcf1b4f4b2cba629345711b4d9e"
TERMINAL_OLEAN_SHA256 = "1e39b129af65d5c03040959a3edc75fa5090a872682059600ae99d1994b0b757"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
PROVISIONAL_CLOSED = {
    "M0626-ROOT",
    "M0626-S-GLOBAL-LOCAL",
    "M0626-N-IMAGE-COVER-TO-SOURCE",
    "M0626-N-SEPARATION-GOAL",
    "M0626-C-RELATIVE-PREIMAGES",
    "M0626-N-WITNESS-PULLBACK",
    "M0626-L-SOURCE-INTERSECTION",
    "M0626-T-INTERSECTION-PUSHFORWARD",
    "M0626-L-IMAGE-PRECONNECTED",
    "M0626-L-IMAGE-NONEMPTY",
    "M0626-A-ISCONNECTED-IMAGE",
    "M0626-T-LOCAL-COMPOSE",
    "M0626-T-ASSEMBLE",
}
OPEN_MACHINE = {
    "M0626-S-INTERFACE",
    "M0626-S-CONNECTEDNESS",
    "M0626-S-BOUNDARY",
    "M0626-S-FOUNDATION",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1320,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0626-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    proof_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0626-PROOF"
    )
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0626-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == PROVISIONAL_CLOSED

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0626.ConnectedImageTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["obligation_tree_sha256"] == EXPECTED_INPUTS["ObligationTree.lean"]
    assert proof_receipt["inputs"]["obligation_registry_sha256"] == EXPECTED_INPUTS["obligation-registry.json"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert set(proof_receipt["provisionally_closed_proof_obligation_ids"]) == PROVISIONAL_CLOSED
    assert set(proof_receipt["required_machine_open_ids"]) == OPEN_MACHINE
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = [registry["root_obligation_id"]]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert reachable == {
        "M0626-ROOT",
        "M0626-T-ASSEMBLE",
        "M0626-S-GLOBAL-LOCAL",
        "M0626-A-ISCONNECTED-IMAGE",
    }
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    independent = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.connectedImage",
        "root_of_localConnectedImage", "connectedImage_via_components",
    ):
        assert forbidden not in independent, forbidden
    assert "exact hs.image f hf.continuousOn" in independent

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / "Mathlib/Topology/Connected/Basic.lean"
    terminal_olean = (
        MATHLIB / ".lake/build/lib/lean/Mathlib/Topology/Connected/Basic.olean"
    )
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert git(
        "rev-parse", "HEAD:Mathlib/Topology/Connected/Basic.lean", cwd=MATHLIB
    ) == TERMINAL_SOURCE_BLOB
    body = terminal_source.read_bytes().splitlines(keepends=True)[272:297]
    assert hashlib.sha256(b"".join(body)).hexdigest() == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_text = b"".join(body).decode("utf-8")
    assert prohibited.search(code_without_comments(terminal_text)) is None

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied Lean replay"
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    with tempfile.TemporaryDirectory(prefix="m0626-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_command = [
            bwrap,
            "--bind", "/", "/",
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--chdir", str(tmp),
        ]
        statement_env = ["--setenv", "LEAN_PATH", lean_path]
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        statement_output = run(
            base_command + statement_env + [lean, "-o", "Statement.olean", "Statement.lean"]
        )
        obligation_output = run(
            base_command + module_env + [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"]
        )
        proof_output = run(base_command + module_env + [lean, "Proof.lean"])
        validation_output = run(base_command + module_env + [lean, "Validation.lean"])

    assert "ConnectedImageTarget" in statement_output
    for declaration in (
        "IsPreconnected.image",
        "IsConnected.image",
        "Stage1Instances.THM_M_0626.Proof.relativePreimages",
        "Stage1Instances.THM_M_0626.Proof.separationEngine",
        "Stage1Instances.THM_M_0626.Proof.localConnectedImage_components",
        "Stage1Instances.THM_M_0626.Proof.localConnectedImage_mathlib",
        "Stage1Instances.THM_M_0626.Proof.connectedImage",
        "Stage1Instances.THM_M_0626.Proof.connectedImage_via_components",
        "Stage1Instances.THM_M_0626.Proof.connectedImage_via_exactAssembly",
    ):
        assert_axioms(proof_output, declaration)
    assert_axioms(validation_output, "IsPreconnected.image")
    assert_axioms(validation_output, "IsConnected.image")
    assert_axioms(
        validation_output,
        "Stage1Instances.THM_M_0626.Validation.differentialConnectedImage",
    )
    assert proof_output.count("Declarations are sorry-free!") == 15
    assert validation_output.count("Declarations are sorry-free!") == 3
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["release_grade"] is receipt["accepted"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_0626.ConnectedImageTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["provenance"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["provenance"]["terminal_source_blob"] == TERMINAL_SOURCE_BLOB
    assert receipt["provenance"]["terminal_body_sha256"] == TERMINAL_BODY_SHA256
    assert receipt["provenance"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["provenance"]["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    result = receipt["result"]
    assert result["exact_root_kernel_closed"] is True
    assert result["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_closed_obligations"] == []
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0626-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0626 narrow validation")
    print("PASS network-isolated kernel replay: exact target, frozen composition, proof roots, and differential root elaborated")
    print("PASS trust observation: checked declarations report exactly propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: frozen hashes, terminal source/body/olean, clean mathlib pin, remote, and license agree")
    print("PASS hygiene and architecture: Lean assert_no_sorry, local scan, and frozen proof reachability agree")
    print("FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R4")
    print("FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or full TCB/SBOM closure")
    print("FAIL CLOSED independent release: differential probe used this worker/shared cache, not a distinct signed runner")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
