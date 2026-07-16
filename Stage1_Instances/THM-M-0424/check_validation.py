#!/usr/bin/env python3
"""Semantic validation blocker for S56-M-0424-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0424"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
ITEM = "S56-M-0424-VALIDATION"
THEOREM = "THM-M-0424"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "f6c5258e1d42d3812d7d616b9a9135ed71401872573195920e5bf8aa56d99683"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLR_TREE = "32c9eace926573a9981787ae97643e520353c893"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BRAUER_SOURCE_SHA256 = "ab3a4ef1b8c38b799b25430e9a4ec638aa3aad5e1f7012ae3a71c9c1d9c7668c"
BRAUER_SOURCE_BLOB = "8b82a886f653dd788670a2098d0f45ba2e0541f9"
BRAUER_OLEAN_SHA256 = "d3a91e4ae4753622d8ed96c9bc34fed15c1bf3256efc9585db3d97b5811bcca9"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = "62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8"
DENOMINATOR_SHA256 = "83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "e6ee85656ac5bf9576546f2d56ab6e9ff20eb85452be4a9be4ea6a06a55ae7e9",
    "ObligationTree.lean": "f5a825653aabeb9365b86ab7c1c91a2291291258a5ba7131cab2027127ec10cb",
    "UniverseCounterexample-2026-07-14-head-5753c6ed.lean":
        "2b7580c0ccb344736e3643522f4b96b0efeb66db4d310b90cb0745a2dad9e5e8",
    "obligation-registry.json": "2886ccb997b40e63b7bee6241954eaca770db39a71ce9a701af890f600a0f6f5",
    "typed-graphs.json": "079c3176794bd6caf665cd0bcac2cb14fcf8b6a1c99a39256728d5fb16df69cd",
    "anchor-audit.json": "7b2941e9728a1a0913168ae4ae336bdfd009d53181bc9f5f537d591c3b9adc60",
    "validation-specs.json": "2fea3704a2dd481c07801e4456d378d6b7096c17da8630cc11bf78c872fca4cc",
    "proof-receipt.json": "3e2e7c50b6cf4450c6d74bdccd3c3c3d9c0433e54b75f436c3cf48a7516cb5c2",
    "check_proof.py": "f93f1e10528b399540aa33c996f0943e80a5a568c5c0ab5a2ca47e715c7ecdc1",
}
EXPECTED_BLOBS = {
    "Statement.lean": "a2e445f9fedcf5523c1831eae701ee121fefbecb",
    "ObligationTree.lean": "40149a45f58e0b258e3686dfee01f23a24a5e9d7",
    "UniverseCounterexample-2026-07-14-head-5753c6ed.lean":
        "1624ed83e6215131c57f4f9ba35dd8766679eaa1",
    "obligation-registry.json": "afd4d37670e601e0bdc237b546862c125a9d69de",
    "typed-graphs.json": "44d89678d93fcd52c45d30ca34da515749876d64",
    "anchor-audit.json": "14154e43807f682a10d45f51751dafcd1a566b6f",
    "validation-specs.json": "136db5049ac70627b81885a7e871ecabe822aa34",
    "proof-receipt.json": "6c9e196063ced2079737bcb60f730f818ea50ec6",
    "check_proof.py": "3614a37545a381c8c643b695c2834c80b3241b59",
}
AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "2a5bc7d397e03969aac1a9f8f21b437152b8ef63ef453055acf67857ced628b5",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "fe70128eba4e3878fbc58625bc7f602be4020e5e2edd6b94b134436568086d65",
    "skills/execute-stage1-rev56/SKILL.md":
        "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
}
AUTHORITY_BLOBS = {
    "Docs/Stage1_Blueprint_v2.md": "aff0509a6a1d50b429f28aa3fb603f8da3347114",
    "Docs/Stage1_Blueprint_rev-5.6.md": "00b304bc44f3d1c52f3723cf1553bb13a2ad4018",
    "Docs/Stage1_Phase_Acceptance_Contracts.json":
        "84b92df9eaf457ab954b652c3f20f4d513cf0a88",
    "Docs/Stage1_Theorem_DAG_v2.json": "db66431477ee26a5577f8a239d29985d59b32543",
    "Docs/Stage1_Targets_rev-5.6.json": "3c85586d3060c219bad5462121b85717360a0665",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "c62ea44cc32f86e77fb4b7ef998464ea48accd9e",
    "skills/execute-stage1-rev56/SKILL.md": "9b1a2dd279ea94d9b4ca840b063cc8d7fc0d6a49",
}
SHARED_GROUPS = [
    "SHARED-MODULE-1e1e801c1afdcc1f",
    "SHARED-MODULE-6e79d52d6da9de82",
    "SHARED-MODULE-d1f653e354a315e1",
]
SHARED_PROVIDERS = {
    "SHARED-MODULE-1e1e801c1afdcc1f": (
        "THM-M-0039",
        {
            "Stage1_Instances/THM-M-0039/IntakeProbe.lean":
                "d7c4c9e201164f66fc3ef4aac7cdbf7830f1aded53a4236a6ca6b9ef6f56aed7",
            "Stage1_Instances/THM-M-0039/instance.json":
                "84e7922423ede59acfe79bde5bb7b75e742aa782d039d732a92826fc7c671786",
        },
    ),
    "SHARED-MODULE-6e79d52d6da9de82": (
        "THM-M-0037",
        {
            "Stage1_Instances/THM-M-0037/IntakeProbe.lean":
                "9693c4ec79ad5df88504f187819dd0857954d1c9d9ec43630d1b9e0b9ce32bf6",
            "Stage1_Instances/THM-M-0037/instance.json":
                "732f8a2df1df5ac8323ec93e01232c8d1d3109c9aee771a4dc3b9b6fc1e437cd",
        },
    ),
    "SHARED-MODULE-d1f653e354a315e1": (
        "THM-M-0038",
        {
            "Stage1_Instances/THM-M-0038/IntakeProbe.lean":
                "ceac8a1ffaa8adafb317a912413a5939bacd18a88fe7362072a9a6fd07bf81ec",
            "Stage1_Instances/THM-M-0038/instance.json":
                "26e2a46f2a0fd38d0a4ad2c204b1bcaae47b188cde8d01414c788279f88852f9",
        },
    ),
}
OPEN_IDS = {
    "M0424-ROOT", "M0424-S-TARGET", "M0424-S-BOUNDARY",
    "M0424-S-FOUNDATION", "M0424-C-TENSOR-ALG", "M0424-C-TENSOR-CSA",
    "M0424-C-TENSOR-CONGR", "M0424-C-ONE", "M0424-C-OPPOSITE",
    "M0424-L-DESCENT", "M0424-L-ASSOC", "M0424-L-COMM",
    "M0424-L-UNIT", "M0424-L-INVERSE", "M0424-T-LAWDATA",
    "M0424-T-COMPOSE", "M0424-X-SOURCE", "M0424-X-PROVENANCE",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )


def checked_output(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    preserve_whitespace: bool = False,
) -> str:
    result = run(argv, cwd=cwd, env=env)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout if preserve_whitespace else result.stdout.strip()


def git(*argv: str, cwd: Path = ROOT) -> str:
    return checked_output(["/usr/bin/git", *argv], cwd=cwd)


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            index += 1
        else:
            output.append(source[index])
            index += 1
    if depth or in_string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        re.DOTALL,
    )
    if match is None:
        raise ValueError(f"missing axiom report for {declaration}")
    return {
        item.strip()
        for item in match.group(1).replace("\n", "").split(",")
        if item.strip()
    }


def validate_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema mismatch")
    if ledger.get("consumer_theorem_id") != THEOREM:
        raise ValueError("dependency ledger theorem mismatch")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding is stale")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding is stale")
    if ledger.get("repository_revision") != BASE_REVISION:
        raise ValueError("dependency ledger repository binding is stale")
    for key in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "inspections", "unresolved_compatibility_obligations",
    ):
        if ledger.get(key) != []:
            raise ValueError(f"dependency ledger field {key} is not the audited empty closure")
    if ledger.get("shared_group_ids") != SHARED_GROUPS:
        raise ValueError("dependency ledger shared-group context is incomplete")
    closure = ledger.get("closure_audit")
    if not isinstance(closure, dict):
        raise ValueError("dependency ledger lacks its closure audit")
    if closure.get("parent_inspection_order") != [] or closure.get("inspected_parent_ids") != []:
        raise ValueError("dependency ledger invents a hard-parent inspection")
    if closure.get("status") != "empty_hard_parent_closure_inspected":
        raise ValueError("dependency ledger does not record the empty closure audit")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or len(decisions) != len(SHARED_GROUPS):
        raise ValueError("dependency ledger does not decide every shared group exactly once")
    if [row.get("source_id") for row in decisions] != SHARED_GROUPS:
        raise ValueError("dependency ledger shared-group decision order changed")
    for row in decisions:
        source_id = row["source_id"]
        provider, artifacts = SHARED_PROVIDERS[source_id]
        if row.get("provider_theorem_id") != provider or row.get("decision") != "not_applicable":
            raise ValueError("shared-module hint was improperly credited as proof reuse")
        if row.get("context_digest") != CONTEXT_SHA256 or not row.get("non_reuse_reason"):
            raise ValueError("shared-module decision lacks context or non-reuse reason")
        if row.get("inspected_member_artifacts") != artifacts:
            raise ValueError("shared-module inspected artifact set changed")
        for relative, expected in artifacts.items():
            if sha256(ROOT / relative) != expected:
                raise ValueError(f"shared-module inspected artifact drifted: {relative}")


def replay_counterexample() -> tuple[str, str, str, str]:
    lean = Path(checked_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lake = Path(checked_output(["lake", "env", "which", "lake"], cwd=LEAN_ROOT))
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        raise ValueError("pinned Lean or Lake executable digest mismatch")
    if LEAN_COMMIT not in checked_output([str(lean), "--version"], cwd=LEAN_ROOT):
        raise ValueError("pinned Lean executable identity mismatch")
    base_path = checked_output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    fixed_env = {
        **os.environ,
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": base_path,
    }
    with tempfile.TemporaryDirectory(prefix="m0424-validation-", dir="/tmp") as raw:
        scratch = Path(raw)
        statement = scratch / "Statement.lean"
        obligation = scratch / "ObligationTree.lean"
        counterexample = scratch / "Counterexample.lean"
        statement.write_bytes((HERE / "Statement.lean").read_bytes())
        obligation.write_bytes((HERE / "ObligationTree.lean").read_bytes())
        counterexample.write_bytes(
            (HERE / "UniverseCounterexample-2026-07-14-head-5753c6ed.lean").read_bytes()
        )
        statement_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Statement.olean"), str(statement)],
            cwd=LEAN_ROOT,
            env=fixed_env,
        )
        if statement_result.returncode:
            raise ValueError(f"statement replay failed\n{statement_result.stdout}")
        local_env = {**fixed_env, "LEAN_PATH": f"{scratch}:{base_path}"}
        obligation_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "ObligationTree.olean"), str(obligation)],
            cwd=LEAN_ROOT,
            env=local_env,
        )
        if obligation_result.returncode:
            raise ValueError(f"conditional composition replay failed\n{obligation_result.stdout}")
        counter_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Counterexample.olean"), str(counterexample)],
            cwd=LEAN_ROOT,
            env=local_env,
        )
        if counter_result.returncode:
            raise ValueError(f"counterexample replay failed\n{counter_result.stdout}")
        for declaration in (
            "Stage1Instances.THM_M_0424.brauerGroupStatement_of_lawData",
        ):
            if printed_axioms(obligation_result.stdout, declaration) != EXPECTED_AXIOMS:
                raise ValueError(f"unexpected axiom profile for {declaration}")
        for declaration in (
            "Stage1Instances.THM_M_0424.UniverseCounterexample.small_of_one_rep_equiv",
            "Stage1Instances.THM_M_0424.UniverseCounterexample.no_small_base_representative",
            "Stage1Instances.THM_M_0424.UniverseCounterexample.no_law_data_at_unrelated_universes",
            "Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement",
        ):
            if printed_axioms(counter_result.stdout, declaration) != EXPECTED_AXIOMS:
                raise ValueError(f"unexpected axiom profile for {declaration}")
        if "this : ¬BrauerGroupStatement" not in counter_result.stdout:
            raise ValueError("counterexample did not recheck the negated exact target")
        return (
            hashlib.sha256(statement_result.stdout.encode()).hexdigest(),
            hashlib.sha256(obligation_result.stdout.encode()).hexdigest(),
            hashlib.sha256(counter_result.stdout.encode()).hexdigest(),
            sha256(scratch / "Counterexample.olean"),
        )


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base revision or tree drifted")
    for relative, expected in AUTHORITY_HASHES.items():
        path = ROOT / relative
        if sha256(path) != expected or git("hash-object", str(path)) != AUTHORITY_BLOBS[relative]:
            raise ValueError(f"authority input drifted: {relative}")
    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        raise ValueError("Lean toolchain file drifted")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        raise ValueError("Lake manifest drifted")
    for name, expected in EXPECTED_HASHES.items():
        path = HERE / name
        if sha256(path) != expected or git("hash-object", str(path)) != EXPECTED_BLOBS[name]:
            raise ValueError(f"owned validation input drifted: {name}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 78 or target.get("lifecycle_mode") != "planned":
        raise ValueError("target manifest identity or lifecycle drifted")
    if target.get("theorem_complete") is not False:
        raise ValueError("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    items = {row["phase"]: row for row in execution["items"] if row.get("theorem_id") == THEOREM}
    if set(items) != {
        "intake", "statement", "anchor_audit", "obligation_tree", "proof",
        "validation", "release",
    }:
        raise ValueError("target does not have the exact seven phase items")
    validation_item = items["validation"]
    if validation_item.get("state") != "[ ]" or validation_item.get("attempts") != 0:
        raise ValueError("validation item no longer matches the claimed open state")
    if validation_item.get("depends_on") != ["S56-M-0424-PROOF"]:
        raise ValueError("validation prerequisite identity changed")
    if items["proof"].get("state") != "[_]" or items["proof"].get("attempts") != 1:
        raise ValueError("proof prerequisite observation changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 304 or node.get("topological_layer") != 0:
        raise ValueError("v2 claim order changed")
    for field in ("direct_hard_parents", "transitive_hard_ancestors", "direct_reuse_hint_ids"):
        if node.get(field) != []:
            raise ValueError(f"unexpected dependency context in {field}")
    if node.get("shared_lemma_group_ids") != SHARED_GROUPS:
        raise ValueError("shared-group context changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context digest changed")
    validate_ledger()

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    validation_contracts = [
        row for row in contract.get("phases", [])
        if isinstance(row, dict) and row.get("phase") == "validation"
    ]
    if len(validation_contracts) != 1:
        raise ValueError("HEAD phase contract lacks exactly one validation row")
    validation_contract = validation_contracts[0]
    if validation_contract.get("intent") != "validate" or validation_contract.get("layer") != 5:
        raise ValueError("validation phase contract intent or layer changed")
    if validation_contract.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        raise ValueError("validation negative-result policy changed")
    candidates = validation_contract.get("validator_candidates")
    if [row.get("path_pattern") for row in candidates] != [
        "Stage1_Instances/{theorem_id}/check_validation.py",
        "Stage1_Instances/{theorem_id}/check_validation.sh",
    ]:
        raise ValueError("validation validator candidate contract changed")
    existing_candidates = [
        pattern.format(theorem_id=THEOREM)
        for pattern in (row["path_pattern"] for row in candidates)
        if (ROOT / pattern.format(theorem_id=THEOREM)).is_file()
    ]
    if existing_candidates != ["Stage1_Instances/THM-M-0424/check_validation.py"]:
        raise ValueError("validation validator candidate selection is not exact")

    receipt = load(HERE / "validation-receipt.json")
    required_receipt_fields = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "recipe", "result", "trust",
        "provenance", "independent_validation",
    }
    if not required_receipt_fields <= set(receipt):
        raise ValueError("validation receipt lacks a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        raise ValueError("validation receipt schema mismatch")
    if receipt.get("item_id") != ITEM or receipt.get("theorem_id") != THEOREM:
        raise ValueError("validation receipt identity mismatch")
    if receipt.get("phase") != "validation" or receipt.get("intent") != "validate":
        raise ValueError("validation receipt phase or intent mismatch")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        raise ValueError("validation receipt base binding mismatch")
    if receipt.get("support_state") != "provisional_worker_selftest":
        raise ValueError("validation receipt support state mismatch")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        raise ValueError("validation receipt improperly claims master acceptance")
    if receipt.get("verdict") != "blocked" or receipt.get("selftest_status") != "passed":
        raise ValueError("validation receipt does not preserve the self-tested blocked verdict")
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        raise ValueError("validation receipt self-test exit is not successful")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        raise ValueError("validation receipt lacks exact self-test commands")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("validation receipt overstates a terminal decision")
    if receipt.get("result") != {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "audit_complete": False,
        "theorem_complete": False,
        "root_closed": False,
        "open_obligations": len(OPEN_IDS),
        "proof_dependency_master_acceptance": "fail_closed",
        "kernel_replay": "pass_trust_zero_for_statement_conditional_composition_and_exact_negative_counterexample",
        "hermetic_release_gate": "fail_closed",
        "independent_distinct_runner_gate": "fail_closed",
    }:
        raise ValueError("validation receipt semantic result mismatch")

    proof_binding = receipt.get("inputs", {}).get("proof_receipt")
    if proof_binding != {
        "path": "Stage1_Instances/THM-M-0424/proof-receipt.json",
        "sha256": EXPECTED_HASHES["proof-receipt.json"],
        "git_blob": EXPECTED_BLOBS["proof-receipt.json"],
        "receipt_id": "S56-M-0424-PROOF-blocked-2dc5a410b68e-20260717",
        "authoritative_state_observed": "[_]",
        "master_accepted": False,
    }:
        raise ValueError("validation receipt proof dependency binding mismatch")
    if receipt.get("inputs", {}).get("consumer_validation_receipts") != []:
        raise ValueError("validation receipt invents a hard-edge consumer receipt")
    if receipt.get("inputs", {}).get("validation_sources") != []:
        raise ValueError("validation receipt invents an independent validation source")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        raise ValueError("worker self-test packet schema mismatch")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        raise ValueError("worker self-test packet identity or state mismatch")
    if packet.get("base_revision") != BASE_REVISION:
        raise ValueError("worker self-test packet base mismatch")
    if packet.get("commands") != commands:
        raise ValueError("worker packet and receipt command evidence disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet and receipt known failures disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0424/check_validation.py",
        "Stage1_Instances/THM-M-0424/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0424/validation-phase.md",
        "Stage1_Instances/THM-M-0424/validation-receipt.json",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        raise ValueError("worker self-test packet changed-path scope mismatch")
    status = checked_output(
        ["/usr/bin/git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        preserve_whitespace=True,
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != expected_changed:
        raise ValueError("worktree delta escapes or omits the declared target scope")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    rows = registry.get("obligations")
    if not isinstance(rows, list) or {row.get("obligation_id") for row in rows} != OPEN_IDS:
        raise ValueError("frozen obligation denominator identity changed")
    if registry.get("root_obligation_id") != "M0424-ROOT":
        raise ValueError("frozen root identity changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("frozen obligation denominator digest changed")
    recorded_bodies = {
        row.get("obligation_id"): row.get("terminal_proof_body_id")
        for row in rows if row.get("terminal_proof_body_id") is not None
    }
    if recorded_bodies != {
        "M0424-T-COMPOSE":
            "local:Stage1_Instances/THM-M-0424/ObligationTree.lean#"
            "brauerGroupStatement_of_lawData"
    }:
        raise ValueError("registry terminal-body inventory changed")
    closure = graphs.get("closure_boundary")
    if not isinstance(closure, dict) or closure.get("root_closed") is not False:
        raise ValueError("typed graph unexpectedly closes the root")
    if closure.get("distinct_terminal_proof_bodies") != []:
        raise ValueError("typed graph unexpectedly credits a terminal proof body")

    proof_receipt = load(HERE / "proof-receipt.json")
    if proof_receipt.get("item_id") != "S56-M-0424-PROOF":
        raise ValueError("proof receipt identity changed")
    if proof_receipt.get("support_state") != "provisional_worker_selftest":
        raise ValueError("proof receipt support state changed")
    if proof_receipt.get("accepted") is not False or proof_receipt.get("verdict") != "blocked":
        raise ValueError("proof receipt unexpectedly gained acceptance")
    if proof_receipt.get("closed_obligation_ids") != []:
        raise ValueError("proof receipt unexpectedly closes an obligation")
    if proof_receipt.get("result", {}).get("phase_accepted") is not False:
        raise ValueError("proof receipt unexpectedly claims its phase predicate")
    if proof_receipt.get("result", {}).get("root_closed") is not False:
        raise ValueError("proof receipt unexpectedly closes the root")

    for name in (
        "Statement.lean", "ObligationTree.lean",
        "UniverseCounterexample-2026-07-14-head-5753c6ed.lean",
    ):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            raise ValueError(f"prohibited proof construct found in {name}")

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row.get("name") == "mathlib")
    if mathlib_entry.get("rev") != MATHLIB_REVISION:
        raise ValueError("manifest mathlib revision drifted")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("mathlib tree drifted")
    if git("status", "--porcelain=v1", cwd=MATHLIB) != "":
        raise ValueError("mathlib checkout is dirty")
    if git("rev-parse", "HEAD", cwd=FLR) != FLR_REVISION:
        raise ValueError("flt-regular revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=FLR) != FLR_TREE:
        raise ValueError("flt-regular tree drifted")
    if git("status", "--porcelain=v1", cwd=FLR) != "":
        raise ValueError("flt-regular checkout is dirty")
    brauer_source = MATHLIB / "Mathlib/Algebra/BrauerGroup/Defs.lean"
    brauer_olean = (
        MATHLIB / ".lake/build/lib/lean/Mathlib/Algebra/BrauerGroup/Defs.olean"
    )
    if sha256(brauer_source) != BRAUER_SOURCE_SHA256:
        raise ValueError("pinned Brauer-group source drifted")
    if git("rev-parse", "HEAD:Mathlib/Algebra/BrauerGroup/Defs.lean", cwd=MATHLIB) != BRAUER_SOURCE_BLOB:
        raise ValueError("pinned Brauer-group source Git blob drifted")
    if sha256(brauer_olean) != BRAUER_OLEAN_SHA256:
        raise ValueError("pinned Brauer-group compiled object drifted")
    if sha256(MATHLIB / "LICENSE") != MATHLIB_LICENSE_SHA256:
        raise ValueError("pinned mathlib license drifted")
    definitions = brauer_source.read_text(encoding="utf-8")
    if "Prove that the Brauer group is an abelian group" not in definitions:
        raise ValueError("pinned Brauer-group implementation boundary changed")
    if re.search(r"instance\b[^\n]*CommGroup[^\n]*BrauerGroup", definitions):
        raise ValueError("pinned Brauer-group source unexpectedly gained the missing instance")

    statement_hash, obligation_hash, counter_hash, counter_olean_hash = replay_counterexample()
    replay = receipt.get("kernel_evidence")
    if replay != {
        "statement_stdout_sha256": statement_hash,
        "conditional_composition_stdout_sha256": obligation_hash,
        "counterexample_stdout_sha256": counter_hash,
        "counterexample_olean_sha256": counter_olean_hash,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "trust_level": 0,
        "network": "not_used",
    }:
        raise ValueError("validation receipt kernel evidence is stale")


def semantic_result(*, verified: bool, error: str | None = None) -> dict[str, Any]:
    message = (
        "The validation replay confirms the proof prerequisite is unaccepted and the exact "
        "frozen target is refuted at universe specialization {1,0}; all positive validation "
        "gates therefore remain blocked."
        if verified else f"Validation blocker replay failed: {error}"
    )
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "validation",
        "status": "blocked" if verified else "failed",
        "verdict": "blocked" if verified else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "V01-ARTIFACTS/dependency.S56-M-0424-PROOF.master_acceptance"
            if verified else "V01-ARTIFACTS"
        ),
        "open_obligations": len(OPEN_IDS),
        "stale_inputs": [],
        "blocked": verified,
        "message": message,
    }


def main() -> int:
    try:
        verify()
    except Exception as exc:
        result = semantic_result(verified=False, error=str(exc))
        code = 1
    else:
        result = semantic_result(verified=True)
        code = 0
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
