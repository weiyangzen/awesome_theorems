#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1083-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1083"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1083-RELEASE"
THEOREM = "THM-M-1083"
BASE_REVISION = "d01e5d7daab630d25a32f781a754be9af1b82761"
BASE_TREE = "32894fb5c2ce690dc4959f6964ed4c745d26a1ec"
EXPRESSION_SHA256 = "fb7209158513f98f9692a12449560573c5009e1a2366ed34eb8e61f9cae7c58a"
DENOMINATOR_SHA256 = "06ca47d90b0a7af9d99c935d0c7766cea3df5e722f08b563d226d7736baf6a50"
VALIDATION_RECEIPT_ID = "S56-M-1083-VALIDATION-network-isolated-20260715T081308+0800"
VALIDATION_RECEIPT_SHA256 = "b478a6d20e9b07affc4250583cd548f4e7ee0c2f487e7e2a76a51e90d5954194"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H2", "M": "M4", "R": "R4"}
INVENTORY_IDS = [
    "M1083-ROOT", "M1083-S-DEFINITIONS", "M1083-S-BOUNDARY",
    "M1083-S-FOUNDATION", "M1083-N-KOLMOGOROV", "M1083-N-COVERING",
    "M1083-B-SCALES", "M1083-C-NETS", "M1083-L-MARKOV",
    "M1083-L-BOREL-CANTELLI", "M1083-L-CAUCHY", "M1083-C-MODIFICATION",
    "M1083-L-HOLDER-NET", "M1083-L-HOLDER-EXTEND", "M1083-T-ONE-GAMMA",
    "M1083-T-MODIFICATION", "M1083-T-COMPOSE", "M1083-X-EXTERNAL",
    "M1083-X-SOURCE", "M1083-X-PROVENANCE",
]
RECONCILED_INPUTS = {
    "instance.json": "3a3d364b600c565fdc8d703d8ecdd9dff5ecb28c9d6a0ceb320f7054087cfaca",
    "task-dag.json": "f13656697985b3342e31abd924dd988b160dfa21013326f47f4528aa9bd3cbd3",
    "statement.json": "3bf4b61d578d08961021ca4bab5d9efef3d5db63b323a07e29124463c7215cb4",
    "Statement.lean": "2b9c25f6eec19a8d8366850aa868f7ea13921827859f11e268c69b1149ab3c04",
    "anchor-audit.json": "718f29d7e35b729cd9d71ef2ff6dce15c00e6e6a62d32016b9810b55385c3a1e",
    "AnchorAudit.lean": "9d14f30c91c3db27fe19219030431e9e17148f3c5521f1ecba174b3701e21fbe",
    "obligation-registry.json": "5f768dabf5986ffc5e92b5697233e2721c28d5fcdc69f60d65d0f899004ab6ad",
    "typed-graphs.json": "fffb2de52e626df799ca5c785ce4382f1c002a65d86356b1550e173bf3a9ec2f",
    "ObligationTree.lean": "3f6337cdfbac95d6bc78d68728fa074219cc54d0f600eeb10dd5447d01731008",
    "Proof.lean": "5bd5472e7170dc88b579d739194b4704c3f44c872d61187612c32117be76db3d",
    "Validation.lean": "00e53b13109bbf26ce31091f6c22bf04554aa774d78c963ab23c5e08b9e7a9ab",
    "proof-execution.json": "1a0384e6fef08540fe2246a76c231f87e905043e56c972e95f67c5e9dbbaae53",
    "proof-receipt.json": "f07912715f97d9d5328028d3fbfa3b788e73898be8035f0bbc11d3ac4c7d9952",
    "validation-spec.json": "6462268c12c523515d1393b167460bf487ad3cc2066fd2638b7344178d3ae28a",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "abe198c67ec4730571693fd564e575150495a4166bf51f2fc19302c8ed04cd2d",
    "check_validation.sh": "da502295455923bab7547666195c289dc868189248114211cd899bd5ee805b38",
    "validation-specs.json": "e865040d2ed76113c298988587c3fb2ac3954d7d87177c4cf1c98bb8a9f9c561",
    "validation-phase.md": "ed5c9091c23f749bebfeb2cd65c591d2c59af9ac5fe7ce2d388f05b20abdaf42",
    "check_obligation_tree.py": "1064c0b3de3adc10809a48e9f91f537b36690d46d920d781a4e9ec6b11c752ea",
    "source-statement-crosswalk.md": "e8d9e7e4c0bc8db32c184197154a44dd6ac9d0bf4b98c69bb35d224853b0580e",
    "PORT_PROVENANCE.md": "415ee4435783be70d48dcce833bca327200e0fae916cd41d5aae7815a26823c7",
    "Vendor/LICENSE": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    "Vendor/README.md": "5bace4c6c3cd3953f478690cda3ec1a13b1a927051dd0a866fbcd6d4d99b0997",
}
SOURCE_ROWS = {
    "Auxiliary/Algebra.lean": "9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3",
    "Auxiliary/ENNReal.lean": "108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6",
    "Auxiliary/FiniteInf.lean": "042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a",
    "Auxiliary/MeanInequalities.lean": "67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d",
    "Auxiliary/MeasureTheory.lean": "3df7b5faa5795bda61419b864048349d2ae32d8381a4376bac0a337089b383e6",
    "Auxiliary/Metric.lean": "13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e",
    "Auxiliary/Nat.lean": "43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae",
    "Auxiliary/Topology.lean": "ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6",
    "Continuity/Chaining.lean": "75e88c2b7800ebf9f0f3b3f52538444e3323a30f0cbfd603847d2874e3db87bc",
    "Continuity/CoveringNumber.lean": "1d4cad9147985c271cd58fc90bc60a8697933258db6b8228a85a0e2f125f543b",
    "Continuity/HasBoundedInternalCoveringNumber.lean": "688b05f9a645d3d87f8e5cab131b3d2b1723cac32b44703c8b54d92d45cd29e8",
    "Continuity/IsKolmogorovProcess.lean": "62f9ae5b726aba8f36db7a0cb92f9b446ba62e5b583804707aa2ae18b3378a02",
    "Continuity/KolmogorovChentsov.lean": "8c60d137ebb5918ebde96e5158867ff5a7e25b9711ef68cbcb9cb4626df9360b",
    "Continuity/KolmogorovChentsovInequality.lean": "0d8fd8b5bcd66770c79337fbc2ba9dcac7a888c9703f40ac665cef1504a30576",
    "Gaussian/StochasticProcesses.lean": "c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81",
}
MODULES = [
    "Auxiliary/Algebra.lean", "Auxiliary/ENNReal.lean", "Auxiliary/FiniteInf.lean",
    "Auxiliary/MeanInequalities.lean", "Auxiliary/Metric.lean",
    "Auxiliary/MeasureTheory.lean", "Auxiliary/Nat.lean", "Auxiliary/Topology.lean",
    "Continuity/Chaining.lean", "Continuity/CoveringNumber.lean",
    "Continuity/HasBoundedInternalCoveringNumber.lean",
    "Continuity/IsKolmogorovProcess.lean",
    "Continuity/KolmogorovChentsovInequality.lean",
    "Gaussian/StochasticProcesses.lean", "Continuity/KolmogorovChentsov.lean",
]
SUMMARY_LINES = [
    "PASS S56-M-1083-RELEASE negative reconciliation",
    "PASS fresh trust-zero network-isolated replay: 15 vendored modules, exact statement, conditional composition, and exact proof root",
    "BLOCKED dependency: S56-M-1083-VALIDATION is provisional and not master-accepted",
    "BLOCKED graph: alternate proof route lacks an accepted registry delta and typed-graph reconciliation",
    "BLOCKED assurance: H0/R0/foundation/TCB/cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H2/M4/R4 audit_complete=false theorem_complete=false",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
RECIPE_DEADLINE_SECONDS = 1800
STARTED_MONOTONIC = time.monotonic()
SAFE_ENV = {
    "HOME": os.environ.get("HOME", "/nonexistent"),
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
    "PYTHONOPTIMIZE": "0",
    "PATH": "/home/sansha-2/.local/bin:/home/sansha-2/.elan/bin:/usr/bin:/bin",
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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int | None = None) -> str:
    remaining = RECIPE_DEADLINE_SECONDS - (time.monotonic() - STARTED_MONOTONIC)
    assert remaining > 0, "global release recipe deadline exceeded"
    effective_timeout = min(float(timeout) if timeout is not None else remaining, remaining)
    result = subprocess.run(
        argv, cwd=cwd, env=SAFE_ENV, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=effective_timeout, check=False,
    )
    if result.returncode:
        raise AssertionError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=120).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def observed_axioms(output: str, declaration: str) -> set[str]:
    if f"'{declaration}' does not depend on any axioms" in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    if sys.flags.optimize:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 525 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 525,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1083-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1083-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in tasks["tasks"] if row["id"] == "S56-M-1083-VALIDATION"
    )
    assert local_release == {
        "id": ITEM, "depends_on": ["S56-M-1083-VALIDATION"], "state": "open"
    }
    assert local_validation["state"] == "open" and tasks["accepted_states"] == []

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert instance["lifecycle_mode"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == {
        "human": "H2", "machine": "M4", "readability": "R4"
    }
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1083.Statement"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M1083-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [], "root_machine_debt": "M3"
    }
    assert registry["append_only_delta"] == []
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1083-ROOT")
    assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
        "H1", "M3", "R4"
    )
    assert root["evidence_ids"] == []

    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["exact_root_kernel_closed"] is True
    assert proof["exact_root_frozen_graph_closed"] is False
    assert proof["foundation_open_ids"] == ["M1083-S-FOUNDATION"]
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["decision_id"] == "S56-M-1083-RELEASE-local-20260715T101231+0800"
    assert decision["decided_at"] == "2026-07-15T10:12:31+08:00"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert decision["root_vector"]["accepted_before"] == VECTOR
    assert decision["root_vector"]["accepted_after"] == VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1083-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "M1083-REGISTRY-ALTERNATE-ROUTE-DELTA"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for key in (
        "audit_inventory_reconciliation", "human_source_acceptance",
        "readability_acceptance", "foundation_and_trust_closure",
        "hermetic_release_reproduction", "supply_chain_closure",
        "independent_release_verification", "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key
    assert decision["evidence_reconciliation"]["frozen_graph_reconciliation"].startswith(
        "failed"
    )

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1083-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["cwd"] == "." and spec["timeout_seconds"] == RECIPE_DEADLINE_SECONDS
    assert set(spec["env_allowlist"]) == set(SAFE_ENV)
    assert spec["env_allowlist"]["PATH"].startswith("sanitized variable;")
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_paths = [
        HERE / "Statement.lean", HERE / "AnchorAudit.lean",
        HERE / "ObligationTree.lean", HERE / "Proof.lean", HERE / "Validation.lean",
        *sorted((HERE / "Vendor/BrownianMotion").rglob("*.lean")),
    ]
    assert len(lean_paths) == 20
    for path in lean_paths:
        source = code_without_comments(path.read_text(encoding="utf-8"))
        if path.name == "Validation.lean":
            source = re.sub(
                r"^import Mathlib\.Util\.(?:AssertNoSorry|PrintSorries)$", "", source,
                flags=re.MULTILINE,
            )
            source = re.sub(
                r"^\s*(?:assert_no_sorry|#print sorries)\b.*$", "", source,
                flags=re.MULTILINE,
            )
        assert prohibited.search(source) is None, f"prohibited source construct in {path}"
    for name, expected in SOURCE_ROWS.items():
        assert sha256(HERE / "Vendor/BrownianMotion" / name) == expected, name

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib["rev"] == mathlib["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=120).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, timeout=120).strip())
    python = Path(os.path.realpath(sys.executable))
    git_path = shutil.which("git")
    bwrap_path = shutil.which("bwrap")
    assert git_path is not None and bwrap_path is not None
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=120)
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(
        Path(os.path.realpath(git_path))
    )
    assert environment["bubblewrap_executable_sha256"] == sha256(
        Path(os.path.realpath(bwrap_path))
    )
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_license_sha256"] == sha256(MATHLIB / "LICENSE")

    runner = run(["/usr/bin/bash", str(HERE / "check_validation.sh")])
    assert runner.splitlines() == [
        "PASS THM-M-1083 network-isolated narrow kernel replay",
        "PASS exact root, vendored terminal, bridges, and frozen composition trust probes",
        "PASS transitive sorry check and observed axiom boundary: propext, Classical.choice, Quot.sound",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-1083-RELEASE-local-20260715T101612+0800"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1083-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert datetime.fromisoformat(decision["decided_at"]) <= datetime.fromisoformat(
        receipt["output_evidence"]["started_at"]
    )
    assert datetime.fromisoformat(receipt["output_evidence"]["started_at"]) <= (
        datetime.fromisoformat(receipt["output_evidence"]["finished_at"])
    )
    assert datetime.fromisoformat(receipt["output_evidence"]["finished_at"]) <= (
        datetime.fromisoformat(receipt["validated_at"])
    )
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-1083-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == (
        "M1083-REGISTRY-ALTERNATE-ROUTE-DELTA"
    )
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    output_evidence = receipt["output_evidence"]
    assert output_evidence["exit_code"] == 0
    assert output_evidence["stdout_sha256"] == (
        "b2d8bd86b6dcf4af52a13cca4f0eafab974c89a2ee66dd0e9f7b6164691d6e10"
    )
    assert output_evidence["stdout_line_count"] == len(SUMMARY_LINES)
    assert output_evidence["timestamp_boundary"] == (
        "Execution timestamps are written by the worker after the immutable checker returns and "
        "are not checker-authenticated; the stdout digest and current checker digest bind the "
        "reproducible result."
    )
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(
        HERE / "release-decision.json"
    )
    assert receipt["inputs"]["release_validation_sha256"] == sha256(
        HERE / "release-validation.md"
    )
    assert receipt["inputs"]["check_release_sha256"] == sha256(Path(__file__))
    for name, expected in RECONCILED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "evidence_records", "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["commands"][4]["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    records = packet["evidence_records"]
    assert records["node_ids"] == [ITEM]
    assert records["exact_statement_delta"] == "none"
    assert records["debt_vector_delta"] == "none; H2/M4/R4 -> H2/M4/R4"
    assert records["statement_fingerprint"] == decision["statement_fingerprint"]
    assert records["typed_graph_delta"] == "none"
    assert records["recipe_id"] == spec["recipe_id"]
    assert records["receipt_id"] == receipt["receipt_id"]
    assert records["actual_source_ownership"] == receipt["actual_source_ownership"]
    assert records["declaration_ownership"] == receipt["declaration_ownership"]
    assert records["readable_ownership"] == receipt["readable_ownership"]
    assert records["change_impact_set"] == receipt["change_impact_set"]
    assert receipt["known_failures"] == packet["known_failures"]
    assert receipt["retry_condition"] == decision["retry_condition"]
    status = run([
        "git", "status", "--porcelain=v1", "-z", "--untracked-files=all"
    ])
    actual_changed = {
        entry[3:] for entry in status.split("\0") if entry
        if entry[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    obligation_output = run(["python3", "-B", str(HERE / "check_obligation_tree.py")])
    assert "root closure: open (M3); no proof or theorem completion claimed" in obligation_output
    public = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in (
            "release-decision.json", "release-receipt.json", "release-spec.json",
            "release-validation.md",
        )
    )
    assert "/home/" not in public and ".cron/" not in public
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
