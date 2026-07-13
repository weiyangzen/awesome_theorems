#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1246-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1246"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1246-VALIDATION"
THEOREM = "THM-M-1246"
BASE_REVISION = "18ff7447208231633bf2e01e8aad3111af56531a"
BASE_TREE = "9ea9aab30253e72b62ef25c80e17b575356fb7b6"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
DENOMINATOR_SHA256 = "dd6e6ca1fc734ea8f477095e77a99601a3387cd914de7e599c9343b874ae2d6d"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "0388e86c4661e59d1cebd5d54c854bad1184b6b7d2ae2a83e12fc3c3dabddf41",
    "ObligationTree.lean": "794d7584a46ae138d071b1958bd1fa82da1fa11db763f696e16f6b4a14e1aac6",
    "RegularizedIBP.lean": "7af35645a8afbc1e61f3bf44b8cdabb7ad244097cd6a7c27829e9876adf84936",
    "SharpEstimate.lean": "6f839807e9c76117edccc734fa79f99f68b3edb86211be78222a1ec1e48a9093",
    "HardyLimit.lean": "2cb9fea444cc720976838b285c06026b8a6a60ba5c9e9e9c413a46771bb59b53",
    "Proof.lean": "fa5b3bf6cb5dbd63f597f0428d9d490baccb5c41005cb6d2145c0a6ebc39388b",
    "ProofAudit.lean": "253e11a86327d30feee6402d37b47e40e41574596301da1d08964f7a1ab01f5b",
    "Validation.lean": "488e771788870293aed54f5a9bd6c6b847856f9470d903400b93cd2f3b49af64",
    "statement.json": "48ca0afb1db7651526500b03e47c73e25ceae54bc6f2b0a288c454ee6829d237",
    "anchor-audit.json": "5688f27403172094e3ba47a076310f73f1677bc09d7cfb504a032bc7c79f035f",
    "obligation-registry.json": "55abd985d8dae0c29fa16cde7df11f83979cda152bea30bc9df5a1143ab2fd2e",
    "typed-graphs.json": "3af40d84c9b5a91b33b2de6b12a11d65e2b5dab1f98d9a563b770d56ad1e4920",
    "validation-specs.json": "02e2833d927194ebbb2250661467acfec1321bebd24829b46074b25f62e05785",
    "proof-receipt.json": "34b95ea1376a363cee1dc6d1a4e6a28f14332fda3c93abe261238beba30e3d87",
    "check_validation.sh": "8daeb99f8a64d8cbb650b29b2a59f9cfd861d1449c5a179b7acfbe96daeb5edd",
    "validation-spec.json": "65751e8dd3fb838345597f80e66eee359cbdc53124d25d797ff76af1201d148f",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SELECTED_MATHLIB = {
    "Mathlib/Analysis/Calculus/LineDeriv/IntegrationByParts.lean": {
        "blob": "e17ed658c074d670e1b5cbe3ec4169986c129275",
        "source_sha256": "4d99d4d640519f84d26b2893e62300f2abf73c30db53dfece2748abd1f59c0ce",
        "olean_sha256": "44218f82fc5b9f6f8782556844fdbe62652f3ce5ddfc9480ff33a0292a26ad04",
    },
    "Mathlib/MeasureTheory/Constructions/HaarToSphere.lean": {
        "blob": "4ce707c09bcbb019767436392092c7a131605b42",
        "source_sha256": "c851e9bad3ea822d33933f4bf0312cb4ba31d4300ce1678cc75519500bdedb2f",
        "olean_sha256": "a9d4fb47b02b422119491a93ac81276e196e72849dd0a4e1e744eca4f0cc3b4d",
    },
    "Mathlib/MeasureTheory/Integral/DominatedConvergence.lean": {
        "blob": "3aeb4ace15863cef3af283800c10f7d670c3727c",
        "source_sha256": "967aff89500aeff8a1a94358c79bb3200c4e77bdfabe1e6481d2beeda67f6191",
        "olean_sha256": "32b03944f8d8944801e31f10f0e8687975f5d39f0c0b4f8adab077cdd3bc8cfd",
    },
}
EXPECTED_TOOL_HASHES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bwrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ProofAudit.lean",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1246 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, composition, proof terminal/root, and no-Proof-module replay elaborated",
    "PASS hygiene: kernel recursive sorry checks and comment-stripped prohibited-construct scan passed",
    "PASS trust observation: all six checked declarations use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin/tree/remote, selected source/olean hashes, license, and tools agree",
    "FAIL CLOSED authority/state: proof is provisional and the frozen graph remains M3/open pending master architecture reconciliation",
    "FAIL CLOSED hermetic/trust: shared warm .lake is not an empty-cache offline replay or complete transitive TCB/SBOM bundle",
    "FAIL CLOSED independence/readability/source: mirrored same-worker replay is not independent verification; H0 and R0 reviews remain open",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


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


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    predecessor_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 426 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 426,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1246-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1246-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        "07f1c030325dfe8d02e99a0af1a00c5241a312e6195aa4a9e2967822960048f1"
    )
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert predecessor_specs["item_id"] == "S56-M-1246-OBLIGATION_TREE"
    assert len(predecessor_specs["recipes"]) == 15
    assert all(
        row["argv"] == ["python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
        for row in predecessor_specs["recipes"]
    )

    assert proof_receipt["item_id"] == "S56-M-1246-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert "M1246-N-CUTOFF" in proof_receipt["open_proof_or_release_boundaries"]
    assert graphs["closure_boundary"] == {
        "closed_obligations": ["M1246-S-DEFINITIONS", "M1246-T-ROOT-TRANSPORT"],
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1246-T-ANALYTIC"],
        "root_machine_debt": "M3",
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "RegularizedIBP.lean",
        "SharpEstimate.lean", "HardyLimit.lean", "Proof.lean", "ProofAudit.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation_header = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import Proof" not in validation_header
    validation_code = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert re.search(r"(?<![A-Za-z0-9_])hardyTerminal(?![A-Za-z0-9_])", validation_code) is None
    assert "independentlyReconstructedHardyTerminal" in validation_code
    assert "assert_no_sorry independentlyReconstructedHardyInequality" in validation_code

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    for source_name, expected in SELECTED_MATHLIB.items():
        source = MATHLIB / source_name
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / source_name.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    python = Path(os.path.realpath(os.sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    tools = {"lean": lean, "lake": lake, "python": python, "git": git_path, "bwrap": bwrap}
    for name, path in tools.items():
        assert path.is_file() and sha256(path) == EXPECTED_TOOL_HASHES[name], (name, path)
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], cwd=LEAN_ROOT)

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    runner_bytes = runner_output.encode("utf-8")
    assert hashlib.sha256(runner_bytes).hexdigest() == receipt["result"]["kernel_output_sha256"]
    assert len(runner_bytes) == receipt["result"]["kernel_output_bytes"]
    assert runner_output.count("Declarations are sorry-free!") == 6
    assert "PASS axiom profile: six exact declarations" in runner_output
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    # Recheck the shared cache after replay to detect dependency races.
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    for source_name, expected in SELECTED_MATHLIB.items():
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / source_name.replace(".lean", ".olean")
        assert sha256(MATHLIB / source_name) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["env_allowlist"] == {}
    assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
    assert spec["covered_obligation_ids"] == [
        "M1246-ROOT", "M1246-T-ANALYTIC", "M1246-T-ROOT-TRANSPORT"
    ]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED summary from the hash-bound validator",
        "semantic_sha256": "69a146f1821082a68f2fd55e9bbd2fb7661ba00592887bbf8eb4296e98a4f842",
        "bytes": 926,
    }]
    assert len(spec["covered_declarations"]) == 6
    for field in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][field] == spec[field], field

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["inputs"] == {**EXPECTED_INPUTS, "check_validation.py": sha256(Path(__file__).resolve())}
    assert receipt["locally_checked_obligation_ids"] == [
        "M1246-ROOT", "M1246-T-ANALYTIC", "M1246-T-ROOT-TRANSPORT"
    ]
    assert receipt["provisionally_closed_obligation_ids"] == [
        "M1246-ROOT", "M1246-T-ANALYTIC", "M1246-T-ROOT-TRANSPORT"
    ]
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["result"]["axiom_report_count"] == 6
    assert receipt["result"]["placeholder_and_unsafe_scan"] == "pass"
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"]["typed_state_and_architecture_reconciliation"] == "fail_closed"
    assert receipt["result"]["complete_provenance_and_tcb"] == "fail_closed"
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == {
        "human": "H2", "machine": "M3", "readability": "R4"
    }
    assert receipt["root_vector_after_worker_selftest"] == {
        "human": "H2", "machine": "M3_with_provisional_exact_root_replay",
        "readability": "R4",
    }
    assert receipt["first_failed_gate"] == "dependency.S56-M-1246-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_exit_codes"]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    summary_bytes = ("\n".join(packet["output_summary"]) + "\n").encode("utf-8")
    assert hashlib.sha256(summary_bytes).hexdigest() == "69a146f1821082a68f2fd55e9bbd2fb7661ba00592887bbf8eb4296e98a4f842"
    assert packet["known_failures"] == receipt["known_failures"]

    public_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("validation-phase.md", "validation-receipt.json")
    )
    assert "/home/" not in public_text and ".cron/" not in public_text
    assert '"theorem_complete": true' not in public_text
    changed = set(
        git(
            "status", "--porcelain=v1", "-uall", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            "Formalizations/Lean/.lake",
        ).splitlines()
    )
    allowed_status = {f"?? {path}" for path in CHANGED_PATHS}
    allowed_status.add("?? Formalizations/Lean/.lake")
    assert changed == allowed_status, (changed, allowed_status)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert platform.system() == "Linux"
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
