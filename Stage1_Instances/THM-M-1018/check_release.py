#!/usr/bin/env python3
"""Fail-closed, integration-replayable checker for the THM-M-1018 release decision."""

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


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1018"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-1018-RELEASE"
THEOREM = "THM-M-1018"
BASE_REVISION = "3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58"
BASE_TREE = "e8837f7e0722548e2b35e901d9d974797097635e"
EXPRESSION_SHA256 = "c897cb4f129790bbefbb22e4500310d827ae75b914808fd8260916c315e2d964"
DENOMINATOR_SHA256 = "c5662da4255541baea4a76c8de113b36bfb571e2b65376597ad2bcc8cf13d6c2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
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
    "intake.json": "fad10c47d732195988f57137636bda863ef432e2112487074ccf6c0058ce18f4",
    "source_statement_crosswalk.md": "bcdadc5c7f2d3e397c75f2d8f6285491c434a62de7213937f22b0543762028fb",
    "Statement.lean": "88009a0b2e20577d7a007df22f94e79c1e03fb51f062291cb6b23bf5741efdd7",
    "AnchorAudit.lean": "ae91373f97ebc5c864c8fa95e8efd3821252cd5241f835c7ae0e1a5d074a5fe9",
    "anchor-audit.json": "44e089c4ee30a02b8675b85d54515aaac295923363a9581f1ffd0ae6066bee99",
    "obligation-registry.json": "14938dc0eb568813794896c3643545c834ac9f14523529e9c45b1c7d353afb95",
    "typed-graphs.json": "0ab510940f92808e16bc1528c9d7c9d02ebc9d26befe1da14588d543a795fba2",
    "ObligationTree.lean": "2df4f358a5612a779f0c8cbc05e5d4c760629bacfd9cf2a5b0955fbf1ca7055e",
    "Proof.lean": "2d147de6d7d67985a8eec90f0f3e2f6bf5dfe7db10aa62ec00322e54a18e4334",
    PROOF_RECEIPT: "a2d12bf0d7d5ecf95bbd50b2c04f4fcaad374e61933392e92a8bebc1eac07a2d",
    "Validation.lean": "a125ed1ce0d8acb48442b884d483ba557cf68071bba004fafe34c94b7f5b04e4",
    "validation-spec.json": "59ba4b2b882b2958163bafee7ad16329dc745621586652468ffdcc0813065407",
    "validation-receipt.json": "26f757b97d6b45ab0dcffd712d54e7aa6b519396668e74dc696734f1bdaf9b4e",
    "validation-phase.md": "95b42883ca3a97ff58a43ad01b0375db701de51d1f0bc8393c9e1928e9715ec9",
    "check_validation.py": "d1d3649a28de0e604628f94475d0ee31b015655d637cb102fe60ac47c31287be",
}
AUTHORITY_SNAPSHOT = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c584bb1f4c87c725a2f9b96a7370a5a3d0ff706047bf2784db0fcd6d979c507e",
    "Docs/Stage1_Blueprint_rev-5.6.md": "eb12ec6581509195079e6f899ff04e1a803600d60aadc13049e0ce82c3049295",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
ALL_IDS = [
    "M1018-ROOT", "M1018-S-EXACT", "M1018-S-KERNEL", "M1018-S-BOUNDARY",
    "M1018-S-TRANSPORT", "M1018-S-FOUNDATION", "M1018-N-FUBINI",
    "M1018-N-SCALE", "M1018-B-POSITION", "M1018-C-APPROX",
    "M1018-L-DIRICHLET", "M1018-L-INTEGRAL-LIMIT", "M1018-L-ENDPOINTS",
    "M1018-T-ANALYTIC", "M1018-T-ASSEMBLE", "M1018-X-SOURCE",
    "M1018-X-PROVENANCE",
]
CLOSED_IDS = [
    "M1018-S-BOUNDARY", "M1018-S-EXACT", "M1018-S-KERNEL",
    "M1018-S-TRANSPORT", "M1018-T-ASSEMBLE",
]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("root_compose",),
    "Proof.lean": (
        "frontier_Ioc_null", "tendsto_Ioc_mass_of_tendsto",
        "measureReal_Icc_eq_Ioc", "measureReal_Ioo_eq_Ioc",
        "interval_mass_of_weak_limit",
    ),
    "Validation.lean": (
        "frontier_Ioc_null_direct", "tendsto_Ioc_mass_of_tendsto_direct",
        "conditionalCanonicalBridge",
    ),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
KNOWN_FAILURES = [
    "S56-M-1018-VALIDATION remains provisional [_], blocked, nonrelease, and not master-accepted.",
    "No premise-free local or pinned declaration inhabits LevyInversionTarget; M1018-T-ANALYTIC remains the root cut and M1018-L-DIRICHLET is the first missing mathematical package.",
    "The predecessor validation recipe is not replayable after integration because its checker requires an ephemeral predecessor self-test packet, old HEAD, and old dirty change set.",
    "Primary-source H0, complete accepted inventory/source-boundary classification, independent R0 review, and AUDIT-Z are absent.",
    "Complete transitive provenance, foundation, TCB, SBOM, license, cold empty-cache/offline restoration, and deterministic bundle evidence is absent.",
    "No second signed clean runner, independently implemented minimal release verifier, protected release CI, THEOREM-Z, release acceptance, or master acceptance exists.",
    "This packet self-tests only a truthful negative release decision; it supplies no accepted E0/E1, M0 root, AUDIT-Z, THEOREM-Z, theorem completion, or release.",
]
SUMMARY_LINES = (
    "PASS release inputs: target, dependency, receipts, registry, graph, and immutable base hashes agree",
    "PASS fresh Lean replay: exact statement, conditional composition, five partial bodies, and three probes elaborate at trust zero",
    "PASS trust boundary: observed axioms are exactly propext, Classical.choice, and Quot.sound; source hygiene passes",
    "PASS fail-closed root: accepted vector H2/M3/R4; M1018-T-ANALYTIC open; accepted receipts 0",
    "PASS validation freshness audit: predecessor recorded recipe is snapshot-coupled and not current release evidence",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE and M1018-L-DIRICHLET.kernel_closure",
    "verdict=blocked audit_complete=false theorem_complete=false release_grade=false",
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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout.strip()


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60)


def base_blob_sha256(path: str) -> str:
    data = subprocess.check_output(["git", "show", f"{BASE_REVISION}:{path}"], cwd=ROOT)
    return hashlib.sha256(data).hexdigest()


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
    pattern = re.compile(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)]",
        flags=re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, (declaration, output)
    return {
        part.strip() for part in matches[0].replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def replay_lean() -> None:
    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env))
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env))
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env)
    bwrap_name = shutil.which("bwrap")
    assert lean.is_file() and lake.is_file() and bwrap_name is not None
    bwrap = Path(bwrap_name)
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert "Lean (version 4.29.0" in run([str(lean), "--version"], env=fixed_env)

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1018-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        home = tmp / "home"
        home.mkdir()
        for name in LEAN_MODULES:
            shutil.copy2(HERE / name, tmp / name)
        common = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(home),
            "--setenv", "ELAN_TOOLCHAIN", "leanprover/lean4:v4.29.0",
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
            "--chdir", str(tmp), str(lean), "--trust=0", "-t0", "--root", str(tmp),
        ]

        def isolated(args: list[str], *, local: bool = False) -> str:
            path = f"{tmp}:{lean_path}" if local else lean_path
            command = common.copy()
            insert_at = command.index("--chdir")
            command[insert_at:insert_at] = ["--setenv", "LEAN_PATH", path]
            return run(command + args, env=fixed_env, timeout=300)

        outputs["Statement.lean"] = isolated(["-o", "Statement.olean", "Statement.lean"])
        outputs["ObligationTree.lean"] = isolated(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"]
        )
        outputs["Proof.lean"] = isolated(["-o", "Proof.olean", "Proof.lean"], local=True)
        outputs["Validation.lean"] = isolated(
            ["-o", "Validation.olean", "Validation.lean"], local=True
        )
        outputs["AnchorAudit.lean"] = isolated(["AnchorAudit.lean"])

    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[module], declaration) == EXPECTED_AXIOMS
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 3
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    intake = load(HERE / "intake.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / PROOF_RECEIPT)
    validation_spec = load(HERE / "validation-spec.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", BASE_REVISION) == BASE_REVISION
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    run(["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"], timeout=60)
    for name, expected in AUTHORITY_SNAPSHOT.items():
        assert base_blob_sha256(name) == expected, f"base authority drifted: {name}"
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert {k: v for k, v in decision["authority_snapshot"].items() if k != "classification"} == AUTHORITY_SNAPSHOT

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 494 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1018-VALIDATION"
    )
    invariant = {k: v for k, v in release_item.items() if k not in {"state", "attempts"}}
    assert invariant == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 494,
        "phase": "release", "layer": 6,
        "depends_on": ["S56-M-1018-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "children": [],
    }
    assert release_item["state"] in {"[ ]", "[_]"}
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert intake["canonical_formal_target"]["elaborated_expression_hash"].startswith(
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert anchor["machine_classification"] == "M3"
    assert anchor["terminal_candidate_found"] is anchor["audit_complete"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == ALL_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == CLOSED_IDS
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1018-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H2", "M3", "R4",
    ]

    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]
    assert validation["verdict"] == "blocked"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]
    assert validation_spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]
    old_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert 'BASE_REVISION = "718e166c56e53c552ebb861ee01427f9a606fc72"' in old_checker
    assert 'packet = load(ROOT / ".stage1-worker-selftest.json")' in old_checker
    assert "actual_changes == changed_paths" in old_checker

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["recorded_recipe_currently_replayable"] is False
    assert decision["verdict"] == "blocked" and decision["release_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    assert decision["root_vector"]["accepted_before"] == ["H2", "M3", "R4"]
    assert decision["root_vector"]["accepted_after"] == ["H2", "M3", "R4"]
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_theorem_gate"]["gate_id"] == "M1018-L-DIRICHLET.kernel_closure"
    assert decision["first_failed_release_specific_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert decision["known_failures"] == KNOWN_FAILURES
    assert decision["evidence_reconciliation"]["root_kernel_closed"] is False
    assert decision["evidence_reconciliation"]["minimal_open_root_cut_set"] == [
        "M1018-T-ANALYTIC",
    ]
    for key in (
        "validation_recorded_recipe_currently_replayable",
        "audit_inventory_and_source_boundaries_accepted",
        "pinpoint_h0_and_independent_source_review", "independent_r0_review",
        "complete_transitive_provenance_foundation_tcb", "immutable_clean_release_input",
        "hermetic_empty_cache_cold_build", "offline_archive_restoration",
        "sbom_license_archive_closure", "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_required_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1018-VALIDATION", "M1018-L-DIRICHLET", "M1018-T-ANALYTIC",
        "AUDIT-Z", "H0 primary-source", "R0 node-by-node",
        "replayable structured validation", "empty-cache network-denied cold build",
        "SBOM and license", "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut, fragment

    assert spec["recipe_id"] == "S56-M-1018-RELEASE-NARROW-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == ALL_IDS

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["base_revision"] == decision["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == decision["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked" and receipt["accepted_receipt_ids"] == []
    assert receipt["known_failures"] == KNOWN_FAILURES
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["first_failed_theorem_gate"] == "M1018-L-DIRICHLET.kernel_closure"
    for name, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / name) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    semantic_output = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(semantic_output.encode()).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES), "exit_code": 0,
    }

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
    proof_source = source_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    validation_source = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "LevyInversionTarget" not in proof_source
    assert "import Proof" not in validation_source
    assert "(analytic : forall" in validation_source
    assert "ObligationTree.InversionFor mu a b" in validation_source
    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    assert "cannot support `H0`" in crosswalk and "Primary edition/theorem/page" in crosswalk

    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_pin["rev"] == mathlib_pin["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    replay_lean()
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == KNOWN_FAILURES
        assert packet["output_summary"] == list(SUMMARY_LINES)
        status = git(
            "status", "--short", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        )
        actual_changes = {line[3:] for line in status.splitlines() if line}
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)
    handoff = " ".join((HERE / "release-validation.md").read_text(encoding="utf-8").split())
    for fragment in (
        "`S56-M-1018-RELEASE` is **blocked**", "`[H2, M3, R4]`",
        "`audit_complete`", "`theorem_complete`", "M1018-T-ANALYTIC",
        "not replayable at integrated HEAD", "acceptance all remain false",
    ):
        assert fragment in handoff, fragment

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
