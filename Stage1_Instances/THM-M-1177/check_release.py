#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1177-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1177"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1177-RELEASE"
THEOREM = "THM-M-1177"
BASE_REVISION = "499a718cc7926abaf61e9721fe0d7485059403e6"
BASE_TREE = "ed2a23c0266f4d921ad97562392226015eee80be"
VALIDATION_BASE = "ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
EXPRESSION_SHA256 = "bb3ff2384920048fe79eb0bad3c47a32db31bdaf4e4595898cbd5c7dbfb6ac41"
DENOMINATOR_SHA256 = "fdee2b8bae43f9b17436d494feaf781196712daef92e93a3aa062129f2108ef1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1177-ROOT",
    "M1177-S-DATA",
    "M1177-S-FOUNDATION",
    "M1177-B-SPLIT",
    "M1177-B-DEGENERATE",
    "M1177-B-POSITIVE",
    "M1177-C-CONTACT",
    "M1177-L-SLOPE-BALL",
    "M1177-L-GRADIENT-IMAGE",
    "M1177-L-AREA",
    "M1177-L-HESSIAN",
    "M1177-L-DET-TRACE",
    "M1177-L-OPERATOR",
    "M1177-L-INTEGRAL",
    "M1177-L-BALL-VOLUME",
    "M1177-L-SUP",
    "M1177-T-POSITIVE",
    "M1177-T-ASSEMBLE",
    "M1177-X-SOURCE",
    "M1177-X-PROVENANCE",
    "M1177-X-TCB",
]
EXPECTED_INPUTS = {
    "Statement.lean": "d7512549ee50d7e7fcfd6e17dc19fdc96bea00cd32504659b4e11491505afe1d",
    "ObligationTree.lean": "155f1fc892ef8ad52b4ddadb948f6d30975b2547e03c28b89d5b9dcb71404fc6",
    "Proof.lean": "aaf7f1e17f07d4665aba005aea7d4226257c6ba04ede5eeb1be035ea788e10be",
    "Validation.lean": "ed1bd70f8d978d0dd794261709925457b5a622eea4961032355cc86634b24557",
    "README.md": "b4c55c037714f1e76f7ebd32af8ffbdfa26328848316f3b087623efc61087dc8",
    "source_statement_crosswalk.md": "3b4d9b4fae54a547de4dbd7180a5c473525077954f08303e274d654b75f9fe06",
    "intake.json": "45deb2f83195d8866ee4a855bf13f795143b0d419728a3153e40a440d569a230",
    "statement.json": "ae71f3c101d778735b644482eba9840d3f146f87469acf54e098982477b780bc",
    "anchor-audit.json": "75cba1d70253e927ee9f0e1d1dc7503ddbf9c9cdce20cd48fc3383771a68a280",
    "obligation-registry.json": "4d6f3d4002647fcb9ad9de5d7ca2c5672eb60e525c560c9da273ebded891a240",
    "typed-graphs.json": "11405b3e54e0152b7e120f6fd93b871ef4ca57c4124f0dae5a844dd93760db56",
    "proof-receipt.json": "751469505a5b93e1e6e6dfb47f0725b85e77dd683757b07e7fdb805c23d86fbc",
    "validation-spec.json": "fee1883242b93c87cbe999b649438a5407c4ea6dba39efdd13c16337649f5701",
    "validation-receipt.json": "10f875d7933caec5cbb32875604992f777ed7ca7919904ec204e288215de9a57",
    "check_validation.py": "2040e3ab1a3a0e95bf932832b33202993ba63e9ebbd2f186c76ea76ea4cd4f54",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "4164a1f7d548dc405a1c2a3f4a705650bc65c8fdc66df8091c7b0648ba4fd06c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "60660bd599c047e2c78187b34cad672c559d16eaab3017c2e32fb404e07a2bbd",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_RELEASE_INPUTS = {
    "ReleaseCheck.lean": "b3827ab31ce096b5e8f5cad813c837c17e06c6d8e30e35cad5444df19b2b47c3",
    "release-spec.json": "2b41326d9cc9f87f03c1ec1cb6ae5724b22ffa1738900e2786ec49a1a885daa0",
    "release-decision.json": "e861f22fe073cc285855ecbbf21e9b4400d4e4d42d8f598cf1eb2aa831a25c52",
    "release-validation.md": "7d0e530513ce26f4ac5609ecf9846c64a871cab0569163e13b895a7aeae92bab",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ReleaseCheck.lean",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG, receipts, frozen registry, graphs, and hashes agree",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M4/R3; accepted receipts 0",
    "PASS historical evidence integrity: validation input and semantic-output hashes agree; recipe is stale at current HEAD",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root and release gates: M1177-T-POSITIVE is open; narrow replay is warm and same-worker",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 360,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


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
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {
        part.strip() for part in match.group("axioms").split(",") if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def historical_validation_integrity(receipt: dict) -> None:
    mapping = {
        "Statement.lean": "Statement.lean",
        "ObligationTree.lean": "ObligationTree.lean",
        "Proof.lean": "Proof.lean",
        "Validation.lean": "Validation.lean",
        "statement.json": "statement.json",
        "anchor-audit.json": "anchor-audit.json",
        "obligation-registry.json": "obligation-registry.json",
        "typed-graphs.json": "typed-graphs.json",
        "proof-receipt.json": "proof-receipt.json",
        "check_proof.py": "check_proof.py",
        "validation_spec_sha256": "validation-spec.json",
        "validator_sha256": "check_validation.py",
        "validation_probe_sha256": "Validation.lean",
    }
    for field, name in mapping.items():
        assert receipt["inputs"][field] == sha256(HERE / name), field
    summary = (
        "PASS S56-M-1177-VALIDATION: trust-zero network-isolated fresh-output replay "
        "checked the exact statement, conditional composition, local degenerate branch, "
        "and same-worker differential degenerate branch; observed axioms are exactly "
        "propext, Classical.choice, and Quot.sound; accepted root remains M4 and the "
        "positive branch remains open; complete TCB/provenance, cold empty-cache, and "
        "distinct-runner gates fail closed"
    )
    assert hashlib.sha256(summary.encode()).hexdigest() == receipt["result"][
        "stdout_semantic_sha256"
    ]


def pinned_artifacts_usable(manifest: dict) -> tuple[bool, str]:
    lake_link = LEAN_ROOT / ".lake"
    flt = lake_link / "packages" / "flt-regular"
    mathlib = lake_link / "packages" / "mathlib"
    if not lake_link.exists() or not flt.is_dir() or not mathlib.is_dir():
        return False, "missing pinned .lake, flt-regular, or mathlib directory"
    flt_head = run(
        ["git", "rev-parse", "HEAD"], cwd=flt, check=False, timeout=30
    )
    if flt_head.returncode != 0 or flt_head.stdout.strip() != FLT_REGULAR_REVISION:
        return False, "pinned flt-regular artifact has no resolvable manifest revision"
    mathlib_head = run(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, check=False, timeout=30
    )
    mathlib_tree = run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, check=False, timeout=30
    )
    if (
        mathlib_head.returncode != 0
        or mathlib_head.stdout.strip() != MATHLIB_REVISION
        or mathlib_tree.returncode != 0
        or mathlib_tree.stdout.strip() != MATHLIB_TREE
    ):
        return False, "pinned mathlib artifact does not match its recorded revision/tree"
    packages = {row["name"].strip("«»"): row for row in manifest["packages"]}
    if packages["flt-regular"]["rev"] != FLT_REGULAR_REVISION:
        return False, "lake manifest flt-regular revision drifted"
    if packages["mathlib"]["rev"] != MATHLIB_REVISION:
        return False, "lake manifest mathlib revision drifted"
    return True, "usable"


def narrow_lean_replay() -> None:
    fixed_env = os.environ.copy()
    fixed_env.update(
        {
            "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        }
    )
    lean_result = run(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env
    )
    lake_result = run(
        ["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env
    )
    path_result = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    )
    lean = Path(lean_result.stdout.strip())
    lake = Path(lake_result.stdout.strip())
    bwrap = Path(shutil.which("bwrap") or "")
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert bwrap.is_file() and sha256(bwrap) == BWRAP_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env).stdout
    lean_path = path_result.stdout.strip()

    with tempfile.TemporaryDirectory(prefix="stage1-m1177-release-", dir="/tmp") as name:
        tmp = Path(name)
        (tmp / "home").mkdir()
        for source in (
            "Statement.lean",
            "ObligationTree.lean",
            "Proof.lean",
            "Validation.lean",
            "ReleaseCheck.lean",
        ):
            shutil.copy2(HERE / source, tmp / source)

        def isolated_lean(args: list[str], *, modules: bool = False) -> str:
            module_path = f"{tmp}:{lean_path}" if modules else lean_path
            return run(
                [
                    str(bwrap),
                    "--ro-bind", "/", "/",
                    "--bind", str(tmp), str(tmp),
                    "--dev", "/dev",
                    "--proc", "/proc",
                    "--unshare-net",
                    "--die-with-parent",
                    "--clearenv",
                    "--setenv", "HOME", str(tmp / "home"),
                    "--setenv", "LANG", "C.UTF-8",
                    "--setenv", "LC_ALL", "C.UTF-8",
                    "--setenv", "TZ", "UTC",
                    "--setenv", "LEAN_NUM_THREADS", "1",
                    "--setenv", "LEAN_PATH", module_path,
                    "--chdir", str(tmp),
                    str(lean),
                    "--trust=0",
                    *args,
                ],
                env=fixed_env,
            ).stdout

        isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], modules=True
        )
        isolated_lean(["-o", "Proof.olean", "Proof.lean"], modules=True)
        isolated_lean(["-o", "Validation.olean", "Validation.lean"], modules=True)
        output = isolated_lean(["ReleaseCheck.lean"], modules=True)

    assert "Declarations are sorry-free!" in output
    for declaration in (
        "Stage1Instances.THM_M_1177.ReleaseCheck.localDegenerateMaximumPackage",
        "Stage1Instances.THM_M_1177.ReleaseCheck.differentialDegenerateMaximumPackage",
        "Stage1Instances.THM_M_1177.ReleaseCheck.conditionalRoot",
    ):
        assert reported_axioms(output, declaration) == EXPECTED_AXIOMS


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 377
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 377,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1177-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1177-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1177-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 360 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1177-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["accepted_receipt_ids"] == []

    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1177-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "root_machine_debt": "M4",
        "audit_complete": False,
        "theorem_complete": False,
        "minimal_open_root_cut_set": ["M1177-B-DEGENERATE", "M1177-T-POSITIVE"],
    }
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == ["M1177-B-DEGENERATE"]
    assert proof["remaining_root_cut_set"] == ["M1177-T-POSITIVE"]
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["accepted_root_vector"] == ["H1", "M4", "R3"]
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert validation["independent_validation"]["decision"] == "fail_closed"
    historical_validation_integrity(validation)

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M4", "R3"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_theorem_gate"]["gate_id"] == "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["accepted_remaining_root_cut_set"] == [
        "M1177-B-DEGENERATE", "M1177-T-POSITIVE"
    ]
    assert result["proposed_remaining_root_cut_set_after_proof_acceptance"] == [
        "M1177-T-POSITIVE"
    ]

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["historical_validation_recipe_replay"] == (
        "stale_at_current_head_and_preserved_as_nonrelease_historical_evidence"
    )

    old_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in old_checker
    assert VALIDATION_BASE != BASE_REVISION

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean", "ReleaseCheck.lean",
        )
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    for name in EXPECTED_RELEASE_INPUTS:
        assert_text_hygiene(HERE / name)
    assert_text_hygiene(Path(__file__).resolve())

    usable, reason = pinned_artifacts_usable(manifest)
    if not usable:
        raise RuntimeError(
            f"pinned dependency artifact unavailable; do not fetch or update it: {reason}"
        )
    narrow_lean_replay()
    replay_result = (
        "provisional_pass_trust_zero_network_isolated_fresh_output_for_statement_"
        "conditional_composition_two_degenerate_routes_and_conditional_root"
    )
    assert reconciliation["current_release_narrow_lean_replay"] == replay_result
    assert receipt["result"]["current_release_narrow_lean_replay"] == replay_result

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
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
