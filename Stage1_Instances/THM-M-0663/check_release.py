#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0663-RELEASE."""

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
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0663"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM = "S56-M-0663-RELEASE"
THEOREM = "THM-M-0663"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
VALIDATION_RECEIPT_SHA256 = "c0e0196b84b0d8fd292260cb6121de3fda4bb0cc2322d26595ea8b39e132d3c4"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
STATEMENT_EXPRESSION_SHA256 = "2d5a051f2bc932f2b637928aaf63f6795621670cb9d9f13264e139dfe1074fbd"
DENOMINATOR_SHA256 = "0e54d5483488181af11d415bb6e29860b351fce14b297a02bd45d9ee269faf53"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "c0c75f33c97b50eac9d225fb75dc841819ab721690d2ae880b10ae591b31aa40",
    "ObligationTree.lean": "9ff6f3b60885a8df62b9a2679c41c284ca0f3b2fcff2c02c7c8841a7f6fffc76",
    "Proof.lean": "5f17bf17801abaaac0ac80acb037a8293759ec9ba6b235ee8e29e0400fc65704",
    "Validation.lean": "6e2cf1753d284cca6b91bbda6f040672db4ddff3f6bf4f19fe2bbad7d1976ab0",
    "instance.json": "71b0a050bbce47d9941b29064acf578bfd97173a91c587732e092d9278ee6683",
    "task-dag.json": "828c81729fd9424b304c771b56fd3c230de97871029432250f170fc8316fa993",
    "statement.json": "cbad8f956f3c32ac253b46f2025932964178552bf27b6689b6643c0e33131086",
    "anchor-audit.json": "28fff486624d15ece90074d871a34dfb1ca85257fcedf5068c40208fde6f8b27",
    "obligation-registry.json": "128eb58b83f86922775ffbc83df0553159beb35b1eede52e872c5359cfdd4541",
    "typed-graphs.json": "d464b63227b1019e13a8f652224d9f74e95301ab168851ea06c8640c38584a65",
    "validation-specs.json": "40a8ec6015985ae040f32d54efa2a812343e8f82735fb646e10e1133221cb63c",
    "validation-spec.json": "e6045201b69ef3b0026f8cf421abfbeb40f6e10e5ae2caa8524e823aa737fb8a",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "7a421bef43694be1be6418a259cf6837fdee6464b5a57f2aaa9dded81f696298",
    "proof-validation.md": "6c5658509ed424608074ba66553af8004f7fecad5940af147ee4bc89533e88a1",
    "README.md": "e40715cd4bcd3940bfd9a0acec38640eb8cad9a5c7efbec61b0d6a77c11dee99",
    "scope-map.md": "5d2f9ce18e69ce337679e007b6d22a6a3a6e535a6643fe4d0d6e692eeb0198a0",
    "source-statement-crosswalk.md": "162852c50ea6c81543edd5a2a83629480a55c43062d2b0e215acb0a2593501eb",
    "obligation-tree.md": "97ab8f5056ea68a640fab87df220073b56978e896543f68100537fe59c0f4741",
    "validation-phase.md": "836773a3139ae5cd73daf96cde2af899ca71bf02fe2e32306a8faef9b7ffd7e5",
    "statement-validation.md": "9bff09d378860aac8894240cd5f699c9731325860de8fd374725a2166d24c461",
    "anchor-audit-validation.md": "6a6ee0027ed20624d84824d9579ff9f53d6c2e4353127479f078a912ebb91279",
    "obligation-tree-validation.md": "3a7367261b80ed41721f3ed44fa5b2a9445bbdecda1ab1f6e63dbd030f05de85",
    "validation.md": "8d96707c5a459bba95610be6d6f87c9728cc96618763f9b90834bab729af6aa6",
}
INVENTORY_IDS = [
    "M0663-ROOT",
    "M0663-S-ENCODING",
    "M0663-N-DOMAIN",
    "M0663-B-DEGENERATE",
    "M0663-C-EXCEPTIONAL",
    "M0663-L-LOCAL-CONT",
    "M0663-L-LOCAL-ORDER",
    "M0663-L-FINITENESS",
    "M0663-T-PARTITION",
    "M0663-T-ASSEMBLE",
    "M0663-X-SOURCE",
    "M0663-X-FOUNDATION",
    "M0663-X-PROVENANCE",
    "M0663-X-READABLE",
]
OPEN_ROOT_CUT = [
    "M0663-N-DOMAIN",
    "M0663-L-LOCAL-CONT",
    "M0663-L-LOCAL-ORDER",
    "M0663-L-FINITENESS",
    "M0663-X-SOURCE",
    "M0663-X-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG dependency, validation receipt, graph, and hashes agree",
    "PASS current Lean replay: statement, conditional identity, and partial branch declarations elaborate without placeholders",
    "PASS fail-closed state: lifecycle planned; accepted root H3/M4/R4; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED exact root, audit, cold/offline, trust, source/readability, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def replay_lean() -> None:
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    assert LEAN_COMMIT in run([str(lean), "--version"])

    with tempfile.TemporaryDirectory(prefix="m0663-release-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap,
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN,
            "--chdir", str(tmp),
        ]
        run(
            base + ["--setenv", "LEAN_PATH", lean_path, str(lean),
                    "-t", "0", "-o", "Statement.olean", "Statement.lean"]
        )
        module_env = ["--setenv", "LEAN_PATH", f"{tmp}:{lean_path}"]
        obligation_output = run(
            base + module_env + [str(lean), "-t", "0", "ObligationTree.lean"]
        )
        proof_output = run(
            base + module_env + [str(lean), "-t", "0", "Proof.lean"]
        )
        validation_output = run(
            base + module_env + [str(lean), "-t", "0", "Validation.lean"]
        )

    assert printed_axioms(
        obligation_output,
        "Stage1Instances.THM_M_0663.root_of_partition_package",
    ) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_0663.partition_of_subsingleton",
        "Stage1Instances.THM_M_0663.partition_empty",
    ):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_0663.Validation.partitionOfSubsingletonDirect",
        "Stage1Instances.THM_M_0663.Validation.partitionEmptyDirect",
    ):
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    combined = obligation_output + proof_output + validation_output
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined


def main() -> None:
    if sys.flags.optimize != 0 or os.environ.get("PYTHONOPTIMIZE"):
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 707
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 707,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0663-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0663-VALIDATION"
    )
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0663-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 707 and decision["intent"] == "release"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0663-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "."
    assert set(spec["env_allowlist"]) == {"PATH", "HOME", "LANG", "LC_ALL", "TZ"}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == [
        "M0663-ROOT", "M0663-B-DEGENERATE", "M0663-T-ASSEMBLE"
    ]
    assert spec["reconciled_inventory_ids"] == INVENTORY_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0663-VALIDATION"]
    assert receipt["accepted"] is receipt["master_accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in receipt["input_bindings"].items():
        assert "PLACEHOLDER" not in expected
        path = ROOT / name if name.startswith(".") or name.startswith("Stage1_") else LEAN_ROOT / name
        assert sha256(path) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["recipe"]["reconciled_inventory_ids"] == INVENTORY_IDS
    assert receipt["recipe"]["coverage_semantics"] == spec["coverage_semantics"]

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H3", "M4", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_mathematical_gate"]["gate_id"] == "proof.exact_root_kernel_closure"
    assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["mathematical_open_root_cut"] == OPEN_ROOT_CUT
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked" and receipt_result["exit_code"] == 0
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H3", "M4", "R4"
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_mathematical_gate"] == "proof.exact_root_kernel_closure"
    assert receipt_result["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["statement_fingerprint"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == []
    assert receipt["remaining_root_cut_set"] == result["remaining_root_cut_set"]
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H3", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    statement = load(HERE / "statement.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        STATEMENT_EXPRESSION_SHA256
    )
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    boundary = graphs["closure_boundary"]
    assert boundary == {
        "root_closed": False,
        "machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": OPEN_ROOT_CUT,
    }
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert not (HERE / "proof-receipt.json").exists()

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["current_narrow_kernel_replay"] == "provisional_pass_network_isolated_warm_cache"
    assert reconciliation["accepted_instance_root_vector"] == ["H3", "M4", "R4"]
    assert reconciliation["graph_discovery_boundary"] == "M3_root_open"
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_independent_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_evidence",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    bwrap = Path(shutil.which("bwrap") or "")
    assert bwrap.is_file(), "bubblewrap is unavailable"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"])
    replay_lean()

    assert receipt["actual_source_ownership"] == {
        "release_proof_sources_changed": [],
        "inspected_sources": [
            f"Stage1_Instances/{THEOREM}/Statement.lean",
            f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
            f"Stage1_Instances/{THEOREM}/Proof.lean",
            f"Stage1_Instances/{THEOREM}/Validation.lean",
        ],
    }
    assert receipt["declaration_ownership"]["new_or_changed_declarations"] == []
    assert receipt["readable_ownership"]["changed_public_surfaces"] == [
        f"Stage1_Instances/{THEOREM}/release-validation.md"
    ]
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["change_impact_set"] == [ITEM]
    assert receipt["nonrelease_snapshot_binding"]["base_revision"] == BASE_REVISION
    assert receipt["nonrelease_snapshot_binding"]["base_tree"] == BASE_TREE
    assert receipt["nonrelease_snapshot_binding"]["binding_policy"] == (
        "individual SHA-256 bindings for every changed artifact except this receipt, "
        "plus all reconciled theorem inputs; the receipt is self-excluded"
    )
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    started_at = datetime.fromisoformat(receipt["timing"]["started_at"])
    ended_at = datetime.fromisoformat(receipt["timing"]["ended_at"])
    assert started_at <= ended_at == validated_at
    assert all(value.tzinfo is not None for value in (started_at, ended_at, validated_at))
    assert receipt["timing"]["exit_code"] == 0
    assert receipt["freshness"]["supersession_state"] == "current provisional worker proposal"
    assert receipt["freshness"]["support_window"] == (
        "valid only for master inspection of the recorded base snapshot; never release-grade"
    )

    assert decision["known_failures"] == receipt["known_failures"]
    assert set(decision["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    status = git(
        "status", "--short", "--untracked-files=all", "--",
        ".stage1-worker-selftest.json", f"Stage1_Instances/{THEOREM}",
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H3, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
