#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1141-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1141"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1141-RELEASE"
THEOREM = "THM-M-1141"
BASE_REVISION = "055d2986f15165228f00094a7de24a77795055a2"
BASE_TREE = "0fced52df7813bdc38ea71f4d649a788bb895512"
VALIDATION_BASE = "c45f3c7090cb4adf616d45e5414985f956e807b2"
DENOMINATOR_SHA256 = "6f4e5fa64e6d8750ab7592a5b54a269a3b0759b480fae5c802c9740e5daef2d1"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "07b60266780d55e9a3edda48f46d4c6fc38200f133636c62eebf979f1640ea22",
    "AnchorAudit.lean": "edd0c79b595f2f944d7dc0f7f84366ebe02e23d3623f9620ddbe914b6be91bc3",
    "ObligationTree.lean": "cdc326dfb76fd6152bdfae157121554dac52590338adf371fa3d78bbb9a86700",
    "Proof.lean": "595c2853af2d99906b009d778a36bdb88e0e8b6f6f2ca44fd08700815f97647d",
    "Validation.lean": "8c6d5ace89ee884290bf14cd0c9ddd984463c82bf174cbccbe3944b1a4053e73",
    "instance.json": "3dd3731592ae2a48ab3406a3b34eab3feb56acbbdc5641c66d8011d4361423da",
    "task-dag.json": "ea35e682a42bb793c41728bf3625593ab0a604a1cd29ee3b7ed83b00ca374530",
    "scope-map.md": "80ac8fceea544dd1c24cbe0437f557d397fd8af9b2ec3305cced936b49d888dd",
    "source-statement-crosswalk.md": "c599c3b451cb3a25790e0e10e36453c3239a4eb0e2291754854f87aa6f629bfc",
    "anchor-audit.json": "63e24ee90613f872c4fd07407f81952dcd6a4ffe9a5881927f64c15ca62a9283",
    "obligation-registry.json": "70a9e0f9948086bbb9c7559ac2298fe9b375162d21f1d7dbb18143d0c15e3b3a",
    "typed-graphs.json": "e53722ede3a729b0ed135d684a861f359ad392e820142a512dffabe337660a6d",
    "validation-specs.json": "51b4f09fd1b194446c027fa1df42eb2be81f8f9bfcc487474f60ca03cb715dae",
    "proof-validation.md": "75416e8b5c5d45fc8f43fb13d2b68237d4b971047d19c67658af0e265cf4f96c",
    "validation-spec.json": "39db19d5819f7dc7fec431a19b62f76e5aeeaeb4a8dc3f5700dfeea777534bdf",
    "validation-receipt.json": "422a571c7b46b96cc337d0885cb5b362a92764e0e36d88b55f900706a3379a25",
    "check_validation.py": "e8aeb3609976fcece281b2e100c99b49c47b135b9e9992270653c93f2170db1f",
}
EXPECTED_RELEASE_INPUTS = {
    "release-spec.json": "4f0ad9c2541120fe83aa1dc4537a11be36ce97462374c5aecc6a4c6a973fb80d",
    "release-decision.json": "d21e3505675cc85a286c125827df0f8bf405768ccc68fa217e3d7c59ff63c6f2",
    "release-validation.md": "3e7f7394545a4493cd39321f0120210ead34ab34ca7db642df7e59c9d63bdf8d",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M1141-ROOT", "M1141-L-LOCAL", "M1141-L-POSITIVE",
    "M1141-C-COVER", "M1141-C-CHAIN", "M1141-L-PROPAGATE",
    "M1141-T-UNIFORM", "M1141-T-RATIO", "M1141-X-SOURCE",
    "M1141-X-TRUST", "M1141-X-PROVENANCE",
]
OPEN_ROOT_CUT = [
    "source statement: add 2 <= n or check a low-dimensional extension",
    "M1141-L-LOCAL", "M1141-C-COVER", "M1141-C-CHAIN",
    "M1141-T-UNIFORM", "M1141-X-TRUST",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
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


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=360, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output, flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def replay_lean() -> None:
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    assert LEAN_COMMIT in run([str(lean), "--version"])

    with tempfile.TemporaryDirectory(prefix="m1141-release-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN, "--chdir", str(tmp),
        ]
        run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0",
            "-o", "Statement.olean", "Statement.lean",
        ])
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "ObligationTree.olean", "ObligationTree.lean",
        ])
        proof_output = run(base + module_env + [
            str(lean), "--trust=0", "-o", "Proof.olean", "Proof.lean",
        ])
        validation_output = run(base + module_env + [
            str(lean), "--trust=0", "Validation.lean",
        ])

    assert printed_axioms(
        obligation_output, "harnackInequality_of_uniformValueComparison"
    ) == EXPECTED_AXIOMS
    for declaration in (
        "positive_denominators_on_compact",
        "ComparisonChain.endpoint",
        "harnackInequality_of_analytic_package",
    ):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "positiveDenominatorsDirect",
        "comparisonChainEndpointDirect",
        "harnackInequality_of_analytic_package",
    ):
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert "sorryAx" not in obligation_output + proof_output + validation_output


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 346
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1141-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 346,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1141-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-1141-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert registry["root_obligation_id"] == "M1141-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert frozen_specs["item_id"] == "S56-M-1141-OBLIGATION_TREE"
    assert all(
        row["state"] == "open"
        for row in frozen_specs["recipes"]
        if row["obligation_id"] in {"M1141-L-POSITIVE", "M1141-L-PROPAGATE"}
    )

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["intent"] == "release" and decision["execution_rank"] == 346
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1141-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed_release_evidence"] is False
    assert dependency["master_accepted"] is False
    assert decision["provisional_receipt_ids_inspected"] == [validation["receipt_id"]]

    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["result"]["source_statement_identity_gate"] == "fail_closed"
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M3"
    assert validation["result"]["open_root_cut_set"] == OPEN_ROOT_CUT
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "S56-5.1-EXACT-SOURCE-STATEMENT-IDENTITY"
    assert not (HERE / "proof-receipt.json").exists()

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 360 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert "bubblewrap" in spec["network_enforcement"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-1141-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["dependency_receipt"]["receipt_id"] == validation["receipt_id"]
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["canonical_statement"]["elaborated_expression_fingerprint"] == (
        "missing_from_predecessor_statement_phase"
    )
    assert receipt["proof_body_locations"]["exact_root"] is None
    for name, expected in receipt["input_bindings"].items():
        path = ROOT / name
        assert sha256(path) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H1", "M3", "R3"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_substantive_gate"]["gate_id"] == (
        "S56-5.1-EXACT-SOURCE-STATEMENT-IDENTITY"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == [
        "M1141-L-LOCAL", "M1141-C-COVER", "M1141-C-CHAIN",
        "M1141-L-PROPAGATE", "M1141-T-UNIFORM", "M1141-X-TRUST",
    ]

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "exact_root_kernel_closed", "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled", "proof_receipt_present",
        "historical_validation_recipe_currently_replayable", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates", "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["source_statement_identity"] == "failed_dimension_scope_mismatch"
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]

    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1141-VALIDATION", "source identity", "M1141-L-LOCAL",
        "M1141-C-COVER", "M1141-C-CHAIN", "M1141-T-UNIFORM",
        "M1141-X-TRUST", "H0", "R0", "AUDIT-Z", "empty-cache",
        "two signed attestations", "minimal verifier", "deterministic",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    proof_source = code_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    assert "UniformValueComparison" in proof_source
    assert "harnackInequality_of_analytic_package" in proof_source
    assert re.search(r"\btheorem\s+harnackInequality\s*[:(]", proof_source) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    replay_lean()

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git(
        "status", "--short", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    normalized_handoff = " ".join(handoff.split())
    for fragment in (
        "`blocked`", "`[H1, M3, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "accepted=false", "release_grade=false", "This worker accepts no receipt",
    ):
        assert fragment in normalized_handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (
        HERE / "release-decision.json", HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    print("PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree")
    print("PASS current Lean replay: conditional and local packages are trust-zero and placeholder-free")
    print("PASS axiom observation: propext, Classical.choice, and Quot.sound")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE and exact source/root closure")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
