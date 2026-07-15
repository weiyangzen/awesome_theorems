#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0162-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0162"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0162-RELEASE"
THEOREM = "THM-M-0162"
BASE_REVISION = "dafb8b51c4561eee5fcf162a8d5ee49555584bdb"
BASE_TREE = "cca569d6bbc491441652aae678232353fb385a74"
VALIDATION_BASE = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
DENOMINATOR_SHA256 = "28db67d8555342a82bfb4d209445a5c10be82fe50e7b8f2763bdebdb54ca23ff"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0162-ROOT",
    "M0162-S-PREMISES",
    "M0162-S-FOUNDATION",
    "M0162-F-ORTHONORMAL",
    "M0162-D-INNER",
    "M0162-A-DECOMPOSE",
    "M0162-E-TANGENT",
    "M0162-C-NORMAL-T",
    "M0162-C-NORMAL-N",
    "M0162-C-NORMAL-B",
    "M0162-E-NORMAL",
    "M0162-D-CROSS",
    "M0162-C-BINORMAL",
    "M0162-E-BINORMAL",
    "M0162-T-ASSEMBLE",
    "M0162-X-SOURCE",
    "M0162-X-PROVENANCE",
]
OPEN_ROOT_CUT = ["M0162-E-TANGENT", "M0162-E-NORMAL", "M0162-E-BINORMAL"]
TRUST_DECLARATIONS = [
    "Stage1Instances.THM_M_0162.tangentEquation",
    "Stage1Instances.THM_M_0162.normalEquation",
    "Stage1Instances.THM_M_0162.binormalEquation",
    "Stage1Instances.THM_M_0162.frenetSerret",
]
EXPECTED_OLEANS = {
    "Statement.olean": "600c5c2245299aab10f2b06d7c5e265b13645ea765535b4eb6cd5bcdacb740cb",
    "ObligationTree.olean": "49337fdb13e00d360fc326802d5b9d130ccd4b0ca2b0a75c3868127fe702714e",
    "Proof.olean": "d05074e8f9cbfcdf27e08aa7195c4e5d8ea3eca6e96871abcd5d0a35d10b7984",
    "Validation.olean": "8753f976886261190656a942cdd16023af5285548e1ef09a0b365a05fabce75c",
}
EXPECTED_INPUTS = {
    "README.md": "d1dad7f137e2828d313c441c08635b3f8df0339ae98c0d5a1b19fa7ec8f5979e",
    "Statement.lean": "a3b7283df516fbba35412815a954b6d9ad4acb1e79b2c33fe473ac3da50073c2",
    "ObligationTree.lean": "a4bbed3b1777b7c24c7abf1e7a75e421158b95f8edc0d876ccdfa930aa8b1a3a",
    "Proof.lean": "968d9933bf08d4b315d54ef9bdf8215a5fd4b41b51f168541f2135d1213d09b9",
    "Validation.lean": "e2f441f72d3b7b02ff4a79d58d89f8b7050d797e4c000213e9b42fb9b0563674",
    "instance.json": "e83350773c05af46aa441854f259f4778040845c18003f8d70806b14c7bc8433",
    "statement.json": "510eaa244250add3617bb8d239e0eb9802b5538da203a6614bff6228baad6754",
    "anchor-audit.json": "97233583a43cca9f53b0397cc3cbf66eae4c31dbdb926e42ee6133571a99047d",
    "obligation-registry.json": "5efb429c678746fbad8e8767a5e2ebcfaf44dc4bae5195be5e7943fb4d93994d",
    "typed-graphs.json": "79efc75d0aa3dc7b126648ad8f135c9e3e69806f365dda23c832fd54ebf43abe",
    "validation-specs.json": "dfac58e3cda47c11ef822befa96b8b078a407552ac70129af1321b6d6b63757c",
    "proof-receipt.json": "3c1bf3f58d0e0f598e3c69540f581afc5bcbad2bef58514ed8a6ebec1e44fd34",
    "validation-receipt.json": "f58c55f70dc2b5a19314521f1d9e2a455dd2e77da740e5a239626944d71a3c7a",
    "validation-spec.json": "8f6ef9e92f0fe2c32ecd1fab8127fb2fcd7dc37f4206c1ef3c1697c9ada6e733",
    "source-statement-crosswalk.md": "52964a0a40810440530a0a62c032389c884715d7a8b4d5b0d692265c2d2922fd",
    "validation-phase.md": "3172bbf453b37ffcab9c99b1363ff6da0510e67a5b6969fd0e6eb8d00f378782",
    "check_validation.py": "761c2fe9600775e51853810c73a2f31e742a2a4ccbcc3ae5e72b6a27fa69312b",
    "check_validation.sh": "c77fd32158a4cf870c4e823b5ebce665a6932ced746cd1cf4354197cc22756f3",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "40fe3749690b1d3d0ea9adcfc63448e672a182ef5d94b07966937a3475d6e78e",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a361708e7b8cafd63616efb760c0cf65d450ecfb87270c54b0cf37926ebb5b25",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_OUTPUTS = {
    "release-spec.json": "48200dc5578531bad96ece78b73fd787c6be7ad3a9733cd1a869fc90fb322338",
    "release-decision.json": "1e67632c133cd44dea8bff2b74ae89e3803830dbdb1a64e529638b8b5e69a875",
    "release-validation.md": "7d3d83a7ea2e973d9d2283b4e69db17bc925aa417ddfec7ca7e76e43dd852208",
}
RELEASE_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_NAMES),
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact root and three equation packages are sorry-free at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED authority: provisional H1/M3/R4 unchanged; frozen graph remains root-open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


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
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output, declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 661 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    assert instance["theorem_complete"] is False and instance["accepted_proof_state"] == []
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 661,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0162-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0162-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS
    assert statement["declaration"] == "Stage1Instances.THM_M_0162.FrenetSerretTarget"
    assert statement["statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0162-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["audit_complete"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0162-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H1", "M3", "R4"
    ]
    assert all(row["evidence_ids"] == [] for row in graphs["nodes"])

    assert proof["accepted"] is False and proof["support_state"] == "provisional_worker_selftest"
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert set(proof["result"]["axioms"]) == EXPECTED_AXIOMS
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["result"]["provisional_root_kernel_closed"] is True
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "S56-M-0162-VALIDATION-PREREQUISITE-NOT-ACCEPTED"
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in (HERE / "check_validation.py").read_text()

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0162-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-AUTHORITATIVE-ROOT-ACCEPTANCE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    disagreement = decision["authority_disagreement"]
    assert disagreement["frozen_structured_projection"] == ["H1", "M3", "R4"]
    assert disagreement["best_provisional_kernel_projection"] == ["H1", "M0-L", "R4"]
    assert disagreement["typed_graph_root_closed"] is False
    assert disagreement["validation_provisional_root_kernel_closed"] is True
    assert disagreement["reconciled"] is False
    for key in (
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
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
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0162-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert receipt["result"]["remaining_root_cut_set"] == OPEN_ROOT_CUT
    expected_bindings = {
        **{f"Stage1_Instances/{THEOREM}/{name}": digest for name, digest in EXPECTED_INPUTS.items()},
        **EXPECTED_AUTHORITY_INPUTS,
    }
    assert receipt["input_bindings"] == expected_bindings
    for relative, expected in expected_bindings.items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    expected_release_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": digest
        for name, digest in EXPECTED_RELEASE_OUTPUTS.items()
    }
    expected_release_bindings[f"Stage1_Instances/{THEOREM}/check_release.py"] = sha256(
        Path(__file__).resolve()
    )
    assert receipt["release_output_bindings"] == expected_release_bindings
    for relative, expected in expected_release_bindings.items():
        assert sha256(ROOT / relative) == expected, f"release output drifted: {relative}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    mathlib = lake_link / "packages" / "mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    # Other isolated workers share the canonical cache and may briefly create
    # untracked scratch directories; tracked source drift still fails closed.
    assert git("status", "--porcelain=v1", "--untracked-files=no", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_ORIGIN
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    replay = run(["bash", str(HERE / "check_validation.sh")]).stdout
    assert "PASS network-denied trust-zero fresh-output replay" in replay
    assert replay.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    for declaration in TRUST_DECLARATIONS:
        assert reported_axioms(replay, declaration) == EXPECTED_AXIOMS
    for name, digest in EXPECTED_OLEANS.items():
        assert f"{name} sha256: {digest}" in replay
    assert "sorryAx" not in replay and "error:" not in replay

    tree = run(["python3", "-I", "-B", str(HERE / "check_obligation_tree.py")]).stdout
    assert "PASS THM-M-0162 obligation tree: 17 obligations, 49 typed edges" in tree
    assert "root closure: open (M3)" in tree

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_NAMES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
