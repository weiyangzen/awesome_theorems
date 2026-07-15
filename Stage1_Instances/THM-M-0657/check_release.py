#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0657-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0657"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0657-RELEASE"
THEOREM = "THM-M-0657"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
VALIDATION_BASE = "8b9311952b6b4186c774d25758d16597a7c10a8b"
EXPRESSION_SHA256 = "95c7d92148fe7e9375ef83729de47149f0cdecec4ce440308515ddae33442fc2"
DENOMINATOR_SHA256 = "22647d29b16c9d77f04719fe51238e427dab88b5fd6c57dfab8ac599c627ce44"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROVISIONAL_IDS = ["M0657-L-COMPLETENESS", "M0657-C-EXISTENCE"]
ROOT_CUT = [
    "M0657-C-MORLEY-RANK",
    "M0657-L-STABILITY",
    "M0657-L-SATURATION",
    "M0657-L-SATURATED-ISO",
    "M0657-T-TARGET-CAT",
    "M0657-ROOT",
]
INVENTORY_IDS = [
    "M0657-ROOT",
    "M0657-S-ENCODING",
    "M0657-N-SOURCE-SHAPE",
    "M0657-L-COMPLETENESS",
    "M0657-C-MORLEY-RANK",
    "M0657-L-STABILITY",
    "M0657-L-SATURATION",
    "M0657-C-EXISTENCE",
    "M0657-L-SATURATED-ISO",
    "M0657-T-TARGET-CAT",
    "M0657-T-ASSEMBLE",
    "M0657-X-SOURCE",
    "M0657-X-FOUNDATION",
    "M0657-X-PROVENANCE",
]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0657.hasModelCardinality_of_uncountably_categorical",
    "Stage1Instances.THM_M_0657.infinitePart_categorical",
    "Stage1Instances.THM_M_0657.infinitePart_isComplete",
    "Stage1Instances.THM_M_0657.categoricalWithExistence_of_categorical",
    "Stage1Instances.THM_M_0657.morleyCategoricityTarget_of_categoricalTransfer",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0657.Validation.differentialHasModelCardinality",
    "Stage1Instances.THM_M_0657.Validation.differentialInfinitePartCategorical",
    "Stage1Instances.THM_M_0657.Validation.differentialInfinitePartIsComplete",
    "Stage1Instances.THM_M_0657.Validation.differentialConditionalRoot",
)
RECONCILED_INPUTS = {
    "Statement.lean": "e70540498a70b7836ef9d70446a69753d3610088ab93669281f05a3ea1286131",
    "AnchorAudit.lean": "465a3d008c98d98934172a4df533d275487b36671fa16c98ae33d52d7a53b856",
    "ObligationTree.lean": "82128d51e2340be71d7838e7b4ffb82a40cfd1b16114f85390a9af98b0d6a911",
    "Proof.lean": "ea6b3cd2b96f0ae1b4901f69fcb22d091da92dcb0777ea86793ba871b21cfaf7",
    "Validation.lean": "ac683858be3f18b8b8beaa632d70351108797c57dfbf1c8c6ade421958ad53ba",
    "intake.json": "5a5ee7bc34011f014f6f87f183769054b1b64a2cdb83012c2a3004d4a3e6be62",
    "statement.json": "830a54a7ebe87d5c97d836afebd4150a3b34d1f4a5946629f62a29cf4a17c00e",
    "anchor-audit.json": "77632635737306a02f378d8350ff956fbcfd1cdb5b0c6865fccefa64d17c0fe0",
    "obligation-registry.json": "cb15499b200bf207bf71ce172a8e227e44bff5dddec58d24fb37a35d60b5babb",
    "typed-graphs.json": "0eeb5ba818108ff6f25271c17472a512d269492175b9895e7d8594a56c47695c",
    "validation-specs.json": "317e0959e7fdd4b1c431b4b8c0b997ee0a0617edc1312ee24a482e6e78e5abc1",
    "source-statement-crosswalk.md": "f81e3aa169b740dd620b994200ab56e99b519a33fea27871a50f476648bc899f",
    "proof-receipt.json": "1625fd89c397b4445e8cc01b7c23cdf1bf687c139fe821c90b0d94bf3aad8fbc",
    "proof-blocker.json": "65e0f2092ad9380525d6dfcc25d7f0eff7fa91fd0718c33511fc8e13077a87a6",
    "validation-spec.json": "b9d7d7f8285702bb3a63c5836a5dc87a3b61dfe667e71eb9a8ee08cb94c9f83e",
    "validation-receipt.json": "e4e29ef33ca68616d92d89e58b2a793291ea2e3cb6b530ad75fc98a80a9065f4",
    "check_validation.py": "180c29a4739365dbbb9efff9f68f5a5bbaa6d4d63d03a329480ad4e26eb563e3",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_OUTPUT_SHA256 = {
    "statement": "26288775ba2bc4e82046c5d0faca5e4c3c6e21f8f65847b004b1871be59abc3a",
    "obligation_tree": "fcc37be564856b1289be23afc923c3743659f95facbd552f5db13f07a1c576ea",
    "proof": "5f011c0a59f43dfd49e6a8d2481ff6c0e09f92f526dae936b32072e99b7990e8",
    "validation": "6fedfdb3296ee032306c7ae4141f327428e3c69b2f667d93572da4a7bc1c4f64",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and bound inputs agree",
    "PASS narrow Lean replay: exact statement, two partial bodies, and conditional compositions checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H1/M3/R3 unchanged; Morley rank, stability, saturation, uniqueness, and root remain open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}


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
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).stdout.strip()


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
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def pinned_lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([
        *(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean"),
    ])


def narrow_lean_replay() -> dict[str, object]:
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink(), "canonical pinned .lake symlink is unavailable"
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    mathlib = (lake_link / "packages" / "mathlib").resolve()
    assert mathlib.is_dir() and git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    home = Path(os.environ["HOME"])
    lean = home / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    assert lean.is_file()
    assert sha256(lean) == LEAN_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=60).stdout
    bwrap = Path("/usr/bin/bwrap")
    assert bwrap.is_file()
    assert sha256(bwrap) == BWRAP_SHA256
    lean_path = pinned_lean_path(lean)

    with tempfile.TemporaryDirectory(prefix="stage1-m0657-release-", dir="/tmp") as name:
        temp = Path(name).resolve()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / source, temp / source)
        (temp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(temp), str(temp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(temp / "home"),
            "--setenv", "TMPDIR", str(temp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(temp),
        ]

        def lean_run(source: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, timeout=600).stdout

        module_path = f"{temp}:{lean_path}"
        outputs = {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run("ObligationTree.lean", module_path, True),
            "proof": lean_run("Proof.lean", module_path, False),
            "validation": lean_run("Validation.lean", module_path, False),
        }

    actual_hashes = {
        key: hashlib.sha256(value.encode()).hexdigest() for key, value in outputs.items()
    }
    assert actual_hashes == LEAN_OUTPUT_SHA256
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined
    observed_axioms: set[str] = set()
    for declaration in PROOF_DECLARATIONS:
        axioms = reported_axioms(outputs["proof"], declaration)
        assert axioms <= EXPECTED_AXIOMS
        observed_axioms |= axioms
    for declaration in VALIDATION_DECLARATIONS:
        axioms = reported_axioms(outputs["validation"], declaration)
        assert axioms <= EXPECTED_AXIOMS
        observed_axioms |= axioms
    assert observed_axioms == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 4
    assert "VALIDATION_CLOSURE declarations=9214 modules=356" in outputs["validation"]
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    return {
        "lean_output_sha256": actual_hashes,
        "observed_axioms": sorted(observed_axioms),
        "sorry_free_differential_declarations": 4,
        "closure_declarations": 9214,
        "closure_modules": 356,
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert set(spec) == {
        "schema_version", "recipe_id", "item_id", "theorem_id", "cwd", "argv",
        "env_allowlist", "timeout_seconds", "network_policy", "network_enforcement",
        "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations", "covered_decisions", "scope_boundary",
    }
    assert set(decision) == {
        "schema_version", "decision_id", "item_id", "theorem_id", "execution_rank",
        "phase", "intent", "base_revision", "base_tree", "decided_at", "support_state",
        "proposed_state", "release_grade", "canonical_target",
        "canonical_target_expression_sha256", "reconciled_inputs", "authority_inputs",
        "tool_inputs", "dependency", "accepted_receipt_ids",
        "provisional_receipt_ids_inspected", "evidence_reconciliation", "decision",
        "known_failures", "retry_condition", "status_boundary",
    }
    assert set(receipt) == {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "depends_on", "base_revision", "base_tree", "validated_at",
        "validation_started_at", "validation_ended_at", "attestor", "owner", "reviewer",
        "support_state", "proposed_state", "accepted", "release_grade",
        "content_addressed_release_evidence", "master_accepted", "decision_id",
        "accepted_receipt_ids", "dependency", "input_bindings", "release_input_sha256",
        "recipe", "canonical_obligation_ids", "result", "commands",
        "commands_and_results", "output_summary", "output_evidence", "known_failures",
        "retry_condition", "freshness", "invalidation_inputs", "changed_paths",
        "status_boundary",
    }

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for relative, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / relative) == expected, f"tool input drifted: {relative}"
    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    assert decision["tool_inputs"] == {
        **TOOL_INPUTS,
        "lean_toolchain": TOOLCHAIN,
        "lean_commit": LEAN_COMMIT,
        "mathlib_revision": MATHLIB_REVISION,
    }

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 702 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0657-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 702,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0657-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0657.MorleyCategoricityTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == RECONCILED_INPUTS["Statement.lean"]
    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3",
    }
    assert intake["audit_complete"] is intake["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0657-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == (
        DENOMINATOR_SHA256
    )
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0657-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H1", "M3", "R3",
    ]
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"
    assert sum(len(graph["edges"]) for graph in graphs["graphs"].values()) == 56
    assert len(graphs["graphs"]["proof"]["edges"]) == 16
    assert anchor["classification"]["machine"] == "M3"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False

    assert proof["accepted"] is False and proof["support_state"] == (
        "provisional_worker_selftest"
    )
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
    assert blocker["provisional_remaining_machine_cut"] == ROOT_CUT
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0657-VALIDATION"
    assert dependency["worker_projection"] == validation_item["state"] == "[_]"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"] == (
        "provisional_worker_selftest"
    )
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_base_revision"] == validation["base_revision"] == VALIDATION_BASE
    assert dependency["historical_recipe_currently_replayable"] is False
    assert git("merge-base", "--is-ancestor", VALIDATION_BASE, BASE_REVISION) == ""
    assert validation["result"]["validated_provisional_obligation_ids"] == PROVISIONAL_IDS
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["open_root_cut_set"] == ROOT_CUT
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["decision_id"] == "S56-M-0657-RELEASE-local-20260715T132000+0800"
    assert decision["decided_at"] == "2026-07-15T13:20:00+08:00"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["execution_rank"] == 702
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["canonical_target"] == formal["declaration_or_expression"]
    assert decision["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert decision["accepted_receipt_ids"] == []
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"],
    ]
    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H1", "M3", "R3",
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert result["remaining_root_cut_set"] == ROOT_CUT
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", str(HERE.relative_to(ROOT) / "check_release.py")]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_0657.MorleyCategoricityTarget",
        "Stage1Instances.THM_M_0657.morleyCategoricityTarget_iff_existentialSourceShape",
        *PROOF_DECLARATIONS,
        *VALIDATION_DECLARATIONS,
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean",
        )
    )
    assert prohibited.search(all_source) is None
    replay = narrow_lean_replay()

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-0657-RELEASE-BLOCKED-local-20260715T132000+0800"
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["attestor"] == "stage1-rev56-worker-slot8"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0657-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validation_ended_at"] == receipt["validated_at"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["dependency"] == dependency
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["exit_code"] == 0
    assert receipt["result"]["root_vector_before"] == (
        receipt["result"]["root_vector_after"]
    ) == ["H1", "M3", "R3"]
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["validated_provisional_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["result"]["remaining_root_cut_set"] == ROOT_CUT
    assert receipt["result"]["audit_z"] == receipt["result"]["theorem_z"] == "blocked"
    assert receipt["result"]["release_accepted"] is False
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["first_failed_theorem_gate"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert receipt["result"]["current_release_narrow_lean_replay"] == replay
    assert receipt["output_summary"] == SUMMARY_LINES
    summary_bytes = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        summary_bytes
    ).hexdigest()
    assert receipt["output_evidence"]["stdout_bytes"] == len(summary_bytes)
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["output_evidence"]["exit_code"] == 0
    assert receipt["output_evidence"]["raw_logs_retained"] is False
    assert receipt["output_evidence"]["raw_log_sha256"] is None
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["status_boundary"] == decision["status_boundary"]
    assert receipt["changed_paths"] == sorted(CHANGED_PATHS)
    command_results = receipt["commands_and_results"]
    assert len(command_results) == 11
    assert [row["exit_code"] for row in command_results] == [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
    assert command_results[4]["argv"][-1] == "--probe"
    assert command_results[5]["cwd"] == "Formalizations/Lean"
    assert "no validation credit" in command_results[5]["result"]
    assert receipt["freshness"]["support_state"] == "provisional_nonrelease_worker_evidence"
    assert receipt["freshness"]["supersession_state"] == "current_worker_proposal"
    assert receipt["freshness"]["revocation_state"] == "unaccepted"
    assert receipt["freshness"]["incident_path"]
    assert len(receipt["invalidation_inputs"]) == 7
    assert receipt["input_bindings"] == {
        **{f"Stage1_Instances/{THEOREM}/{name}": value for name, value in RECONCILED_INPUTS.items()},
        **AUTHORITY_INPUTS,
        **{f"Formalizations/Lean/{name}": value for name, value in TOOL_INPUTS.items()},
    }
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    assert receipt["release_input_sha256"] == {
        "release-spec.json": sha256(HERE / "release-spec.json"),
        "release-decision.json": sha256(HERE / "release-decision.json"),
        "release-phase.md": sha256(HERE / "release-phase.md"),
        "check_release.py": sha256(Path(__file__).resolve()),
    }
    assert replay["lean_output_sha256"] == validation["result"]["lean_output_sha256"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "covered_decisions", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"]

    base_target_diff = git("diff", "--binary", "HEAD", "--", str(HERE))
    assert base_target_diff == "", "owned target was dirty before release outputs"
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for path in (HERE / "release-decision.json", HERE / "release-receipt.json", HERE / "release-phase.md"):
        public = path.read_text(encoding="utf-8")
        assert "/home/" not in public and ".cron/" not in public
        assert "theorem_complete=true" not in public
    phase = (HERE / "release-phase.md").read_text(encoding="utf-8")
    for fragment in (
        "The release verdict is `blocked`",
        "`theorem_complete=false`",
        "`S56-10.2-DEPENDENCY-ACCEPTANCE`",
        "M0657-C-MORLEY-RANK",
        "M0657-ROOT",
        "It grants no `H0`, `M0`, `E0/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`",
    ):
        assert fragment in phase, fragment

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
