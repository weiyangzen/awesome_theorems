#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0276-VALIDATION."""

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


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0276"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0276-VALIDATION"
THEOREM = "THM-M-0276"
BASE_REVISION = "dc600635160cace0916df5234bf8808c39dc656d"
BASE_TREE = "8ee34b31ec38be1ef067aaab38c9a4cb4935b75a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPRESSION_SHA256 = "0cfb9796471903d081ad67551a3f9c2c3414cce1f7adbf79394d364a467c82fa"
DENOMINATOR_SHA256 = "1437a03a1fa4badc07b730dd8fb72bc6e2783c1205a2d842479b573cfde710c8"
EXPECTED_INPUTS = {
    "Statement.lean": "ede62e0c7bbf3804f6a81c2f1115643048c69ced4750453af7e8ebd845c6aeea",
    "AnchorAudit.lean": "370b505369246ac2e1ccc5336a3ae0e75cd26d5028ae5e4a536a749f46b38a0b",
    "anchor-audit.json": "d84027b9f12d99c5617d719f7ce48bb1b34917a90414f476589e53c17934b906",
    "ObligationTree.lean": "e5757cdf296ba2c12b52658dd7e8231decf8de61a0ff97718139b7a864ab2a76",
    "Proof.lean": "6db08255c52f0314a059858270bdfb9949faec3e56c300affc1032fe7ba8c608",
    "proof-receipt.json": "cbd0b7e696e2a9637e1be53d9a0d30f352d1f7c85e645518adc771a53748719b",
    "obligation-registry.json": "0a5df1dbb570e1ec995f609e6e75e6fe0e1e33e306f7f180eeb3a2a139647004",
    "typed-graphs.json": "853fc1e01fe0abc25bc0d8ab82a2b1013562b21a7d277215930fa86359ed4ea3",
    "validation-specs.json": "18d146c8cfa420b914fa2970987bc1fda939f4060af27d57bcc501840f494bd0",
    "Validation.lean": "14bb1e0cbf014f7fb866ffd698b81526c28f76c30eb775d1f3e47fa536eca8b0",
    "validation-spec.json": "64ad64351125a17c872caa12bf0d543bb1c830e262b7f63a9cdacf887086d841",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE_SHA256 = "b046e38a239014c32e2313b4a216edd89198e57351d9c6068a3de7811680bf6c"
TERMINAL_SOURCE_BLOB = "8d4361a5bdf07bb8b7e2214ee59340f9931422bd"
TERMINAL_OLEAN_SHA256 = "3a1f5d8a584421c9878fdd8401429e3b44847122efd4e944fd7e9d2133528224"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TERMINAL_BODY_HASHES = {
    "approximate_preimage": "e3ffd09433a0872ba4c06b126b79935162ba63dbb1857a904f3d3d6996653f30",
    "exact_preimage": "46005221da6ab656dc9d2f7711c1608d700132bf194a91905885adab896f911a",
    "open_map": "ade0fccdfbd624537071f03d746974a6dbf31a498dfeae90ec0fc26c26b69a63",
}
MAPPED_PROOF_IDS = {
    "M0276-ROOT", "M0276-N-SAME-FIELD", "M0276-T-ASSEMBLE",
    "M0276-T-ADAPTER", "M0276-T-UPSTREAM", "M0276-B-REAL",
    "M0276-B-COMPLEX", "M0276-T-ISOPENMAP", "M0276-L-LOCAL-OPEN-BALL",
    "M0276-L-EXACT-PREIMAGE", "M0276-C-APPROX-SELECTION",
    "M0276-L-RESIDUAL-GEOMETRIC", "M0276-L-SUMMABLE-SERIES",
    "M0276-L-TELESCOPE", "M0276-L-LIMIT-IMAGE", "M0276-L-APPROX-PREIMAGE",
    "M0276-C-BAIRE-COVER", "M0276-L-BAIRE-INTERIOR",
    "M0276-L-RESCALE-SHELL", "M0276-C-CLOSURE-PAIR",
}
RECIPE_COVERED_IDS = {
    "M0276-ROOT", "M0276-N-SAME-FIELD", "M0276-T-ASSEMBLE",
    "M0276-T-ADAPTER", "M0276-T-UPSTREAM", "M0276-B-REAL",
    "M0276-B-COMPLEX", "M0276-T-ISOPENMAP", "M0276-L-EXACT-PREIMAGE",
    "M0276-L-APPROX-PREIMAGE",
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
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=180, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        output, re.DOTALL,
    )
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
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1282,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0276-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-0276-PROOF")
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0276-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == RECIPE_COVERED_IDS

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0276.BanachOpenMappingTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["obligationtree_lean_sha256"] == EXPECTED_INPUTS["ObligationTree.lean"]
    assert proof_receipt["inputs"]["obligation_registry_json_sha256"] == EXPECTED_INPUTS["obligation-registry.json"]
    assert proof_receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof_receipt["root_evidence"]["accepted_root_closed"] is False
    assert set(proof_receipt["root_evidence"]["mapped_proof_graph_ids"]) == MAPPED_PROOF_IDS
    assert proof_receipt["root_evidence"]["unverified_internal_composition_count"] == 14
    assert proof_receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b", re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in ("import Proof", "import ObligationTree", "Proof.banachOpenMapping", "compose_root"):
        assert forbidden not in differential, forbidden
    assert differential.count("exact ContinuousLinearMap.isOpenMap f surj") == 2

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / "Mathlib/Analysis/Normed/Operator/Banach.lean"
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Analysis/Normed/Operator/Banach.olean"
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert git("rev-parse", "HEAD:Mathlib/Analysis/Normed/Operator/Banach.lean", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    source_lines = terminal_source.read_bytes().splitlines(keepends=True)
    body_hashes = {
        "approximate_preimage": hashlib.sha256(b"".join(source_lines[84:153])).hexdigest(),
        "exact_preimage": hashlib.sha256(b"".join(source_lines[159:225])).hexdigest(),
        "open_map": hashlib.sha256(b"".join(source_lines[226:248])).hexdigest(),
    }
    assert body_hashes == TERMINAL_BODY_HASHES == proof_receipt["proof_body"]["terminal_body_sha256"]
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    with tempfile.TemporaryDirectory(prefix="m0276-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc",
            "--unshare-net", "--die-with-parent", "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--chdir", str(tmp),
        ]
        statement_output = run(base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-o", "Statement.olean", "Statement.lean"])
        anchor_output = run(base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "AnchorAudit.lean"])
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base + module_env + [str(lean), "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean"])
        proof_output = run(base + module_env + [str(lean), "--trust=0", "Proof.lean"])
        validation_output = run(base + module_env + [str(lean), "--trust=0", "Validation.lean"])

    assert "BanachOpenMappingTarget" in statement_output
    assert "ANCHOR_CLOSURE declarations=17187 modules=654" in anchor_output
    assert "ANCHOR_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in anchor_output
    assert "ANCHOR_CLOSURE bodyless_nonaxioms=[]" in anchor_output
    assert "ANCHOR_CLOSURE unsafe=[]" in anchor_output
    assert "ExactRoot" in obligation_output
    upstream = (
        "ContinuousLinearMap.exists_approx_preimage_norm_le",
        "ContinuousLinearMap.exists_preimage_norm_le",
        "ContinuousLinearMap.isOpenMap",
    )
    local = (
        "pinnedApproximatePreimage", "pinnedExactPreimage", "pinnedOpenMap",
        "pinnedMathlibTerminal", "realOpenMapping", "complexOpenMapping",
        "banachOpenMapping_direct", "banachOpenMapping_via_frozen_composition",
        "expandedBanachOpenMapping",
    )
    for declaration in upstream:
        assert_axioms(proof_output, declaration)
        assert_axioms(validation_output, declaration)
    for declaration in local:
        assert_axioms(proof_output, f"Stage1Instances.THM_M_0276.Proof.{declaration}")
    assert_axioms(validation_output, "Stage1Instances.THM_M_0276.Validation.differentialBanachOpenMapping")
    assert proof_output.count("Declarations are sorry-free!") == 12
    assert validation_output.count("Declarations are sorry-free!") == 4
    assert "sorryAx" not in anchor_output + obligation_output + proof_output + validation_output

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["release_grade"] is receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_0276.BanachOpenMappingTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["python_executable_sha256"] == sha256(Path(sys.executable).resolve())
    assert receipt["environment"]["git_executable_sha256"] == sha256(Path(shutil.which("git") or "").resolve())
    assert receipt["environment"]["bash_executable_sha256"] == sha256(Path(shutil.which("bash") or "").resolve())
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(Path(bwrap).resolve())
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["provenance"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["provenance"]["terminal_source_blob"] == TERMINAL_SOURCE_BLOB
    assert receipt["provenance"]["terminal_body_sha256"] == TERMINAL_BODY_HASHES
    assert receipt["provenance"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["provenance"]["license_sha256"] == LICENSE_SHA256
    assert receipt["provenance"]["machine_replayed_transitive_closure"] == {
        "declarations": 17187,
        "modules": 654,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    result = receipt["result"]
    assert result["exact_root_kernel_closed"] is True
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_closed_obligations"] == []
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["same_worker_differential_probe"] == "pass"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["complete_tcb_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0276-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert receipt["known_failures"] == packet["known_failures"]
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
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    print("PASS THM-M-0276 narrow validation: exact root and differential wrapper kernel-check under network isolation")
    print("PASS trust/provenance observations: 12 proof declarations and four validation declarations are sorry-free with the selected classical trio")
    print("PASS pinned inputs: target, denominator, source/body/olean/license, toolchain, mathlib revision/tree/remote, and clean dependency agree")
    print("OPEN accepted state: PROOF is provisional; accepted H2/M3/R4, zero accepted obligations, and 14 uncredited internal compositions remain")
    print("BLOCKED release gates: shared warm cache, incomplete transitive provenance/TCB, and no distinct signed independent verifier")


if __name__ == "__main__":
    main()
