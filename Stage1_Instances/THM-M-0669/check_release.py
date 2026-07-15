#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0669-RELEASE."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0669"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0669-RELEASE"
THEOREM = "THM-M-0669"
BASE_REVISION = "8d6ac2078d37dc107d80c38c020de01c6f9affce"
BASE_TREE = "a9332226f35fa562b7dbbe9feab5f5a2da80d013"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_EXPRESSION_SHA256 = (
    "91efc0e7986951efbb4f667a73f31de3eae2f0221d397c37c13a303f3769badd"
)
DENOMINATOR_SHA256 = "9ec85645aa13399fb7dd6255e1cb66f90fc3694c536f6a282a6b30f19173afb4"
ROOT_VECTOR = ["H1", "M3", "R3"]
PROVISIONAL_IDS = ["M0669-C-BOOLEAN"]
PARTIAL_IDS = ["M0669-C-ATOMIC", "M0669-I-FORMULA", "M0669-T-ASSEMBLE"]
OPEN_ROOT_CUT = [
    "M0669-E-ONE-VAR",
    "M0669-E-SIGN",
    "M0669-E-ROOTS",
    "M0669-E-PROJECT",
    "M0669-E-SEMANTICS",
    "M0669-I-FORMULA",
    "M0669-T-ASSEMBLE",
    "M0669-ROOT",
]
INVENTORY_IDS = [
    "M0669-ROOT",
    "M0669-S-THEORY",
    "M0669-C-ATOMIC",
    "M0669-C-BOOLEAN",
    "M0669-E-ONE-VAR",
    "M0669-E-SIGN",
    "M0669-E-ROOTS",
    "M0669-E-PROJECT",
    "M0669-E-SEMANTICS",
    "M0669-I-FORMULA",
    "M0669-T-ASSEMBLE",
    "M0669-X-SOURCE",
    "M0669-X-FOUNDATION",
    "M0669-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "instance.json": "adb5aac9b4a28627d65933a8d875ec5fd69704cd2e8390cd163c23e17af2c6ea",
    "task-dag.json": "fe40a10c7e39615246da3fd177db152c611be8e10bd95a93855e21357a3b4e41",
    "statement.json": "c6db83b8be055f729b3c01079c08515a120b417cf61db286fd59d34afe11c0fe",
    "scope-map.md": "2c8794b8c45513524deb1bebfc889036574b47708d42863101dc4a91a887764a",
    "source-statement-crosswalk.md": "93484f91b05cfdf9728dab42adeeca522f40fdfc329e30bf0e32da0940535416",
    "anchor-audit.json": "ff03d190345cf872b4bd401f1286537120a8057e4bc0fe6b2eb8c67fb1e82af3",
    "obligation-registry.json": "305e5f67aad487e60f74aa076e63a69d65db599a112b81a21ea909d5b24b9bcb",
    "typed-graphs.json": "ca58a855e548c6f6cf377853c231a95664095c21a875b1a887b3dbe525ee23f8",
    "Statement.lean": "09836be630efcb735336dc3d18c2e74e83ec73b5c6237c13be1b8b8fa85f2a7a",
    "ObligationTree.lean": "ff86db4e034849d69e37b6d42683f7a21f64238455f4f8cc41bf622fb25ada4d",
    "Proof.lean": "23e739dcbc773c25d4536360fad54e27d0625bcd416875e73cc2210eb6bd2f58",
    "proof-receipt.json": "51139b89515843ce137ed0b9a8219d2e9d7551fa1c7d4957cff2f72a1b0c6e18",
    "proof-blocker.json": "477e6ade1f847397cd6aad67ff779363ebdeb57e20568d79c968457e44f43993",
    "Validation.lean": "4b749e634675c3f9151bc8dbc85d59dd68840d2b572bf47da94b68c2cdbe138e",
    "validation-spec.json": "f9b8da45eb75f09cf0de09f2be2a76f3646d6a6eaea54a5e2d8ab1cc20f00192",
    "validation-receipt.json": "ef32d8e0c16398780be291f205c18f412d4c2b7d26bcf87a811bad4fb6896c97",
    "check_validation.py": "13427afb5ef565315e6609e72efeffd75f7d9b294194a26e7ae44538b4636a35",
    "lean-toolchain": TOOLCHAIN_SHA256,
    "lake-manifest.json": MANIFEST_SHA256,
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
]
SUMMARY_LINES = [
    "PASS current narrow replay: exact statement and all partial or conditional proof and differential declarations elaborated at trust zero with matching hashes",
    "PASS scoped trust observation: twelve declarations are sorry-free, use only the recorded standard axioms, and the differential closure has no bodyless nonaxiom or unsafe declaration",
    "OPEN exact root: M0669-E-ONE-VAR and its sign, roots, projection, and semantics chain remain absent, so accepted closure is empty and the root remains M3",
    "BLOCKED AUDIT-Z and THEOREM-Z: source, readability, graph, evidence, foundation, provenance, trust, and exact-root acceptance gates remain open",
    "FAIL CLOSED release protocol: no clean cold offline build, SBOM/archive closure, distinct signed runners, minimal verifier, protected CI, or deterministic bundle exists",
    "VERDICT blocked: lifecycle planned and root vector H1/M3/R3 are unchanged; theorem_complete=false and no receipt is accepted",
]

if not __debug__:
    raise RuntimeError("release reconciliation requires Python assertions")


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": f"{os.environ['HOME']}/.elan/bin:/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
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
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def import_validation_helper():
    helper_path = HERE / "check_validation.py"
    spec = importlib.util.spec_from_file_location("thm_m_0669_validation_helper", helper_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    release_spec = load(HERE / "release-spec.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0669-VALIDATION"
    )
    assert target["execution_rank"] == release_item["execution_rank"] == 713
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert release_item["phase"] == "release" and release_item["state"] == "[ ]"
    assert release_item["depends_on"] == [validation_item["id"]]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_item["state"] == "[_]"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == receipt["item_id"] == release_spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["support_state"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is dependency["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert validation["accepted"] is False
    assert validation.get("master_accepted") in (None, False)

    for name, expected in EXPECTED_INPUTS.items():
        path = LEAN_ROOT / name if name in {"lean-toolchain", "lake-manifest.json"} else HERE / name
        assert sha256(path) == expected, f"stale reconciled input: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    for relative, expected in receipt["input_bindings"].items():
        if relative == "lean-toolchain":
            path = LEAN_ROOT / relative
        elif relative == "lake-manifest.json":
            path = LEAN_ROOT / relative
        else:
            path = ROOT / relative
        assert sha256(path) == expected, f"stale release receipt input: {relative}"

    assert instance["lifecycle"] == task_dag["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == task_dag["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == (
        graphs["registry_denominator_sha256"]
    ) == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is boundary["theorem_complete"] is False
    assert boundary["root_machine_classification"] == "M3"
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0669-ROOT")
    assert [root[key] for key in ("human_debt", "machine_debt", "readability_debt")] == (
        ROOT_VECTOR
    )
    assert root["evidence_ids"] == []

    assert proof["accepted"] is False and proof.get("master_accepted") in (None, False)
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0669-PROOF.master_acceptance"
    assert validation["first_failed_theorem_gate"] == "M0669-E-ONE-VAR.root_closure"

    terminal = decision["terminal_decisions"]
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert terminal["release_accepted"] is False
    assert decision["root_vector"]["accepted_before"] == (
        decision["root_vector"]["accepted_after"]
    ) == ROOT_VECTOR
    assert decision["first_failed_gate"]["gate_id"] == (
        "dependency.S56-M-0669-VALIDATION.master_acceptance"
    )
    assert decision["nested_validation_first_failed_gate"]["gate_id"] == (
        "dependency.S56-M-0669-PROOF.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "M0669-E-ONE-VAR.root_closure"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    for key in (
        "exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "audit_inventory_reconciled",
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
        assert decision["evidence_reconciliation"][key] is False, key

    assert release_spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert release_spec["recipe_id"] == receipt["recipe"]["recipe_id"] == (
        "S56-M-0669-RELEASE-NARROW-v1"
    )
    assert release_spec["argv"] == receipt["recipe"]["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    for key in (
        "cwd",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "network_enforcement",
        "environment_boundary",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
        "reconciled_inventory_ids",
        "coverage_semantics",
        "scope_boundary",
    ):
        assert release_spec[key] == receipt["recipe"][key], key

    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE

    helper = import_validation_helper()
    lean = Path(os.environ["HOME"]) / ".elan/toolchains" / (
        TOOLCHAIN.replace("/", "--").replace(":", "---")
    ) / "bin/lean"
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(lean) == LEAN_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/python3").resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git").resolve()) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"])
    outputs = helper.isolated_replay(lean, bwrap, helper.pinned_lean_path(lean))
    output_hashes = {
        name: hashlib.sha256(output.encode()).hexdigest()
        for name, output in outputs.items()
    }
    assert output_hashes == validation["result"]["lean_output_sha256"]
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in value for value in outputs.values())
    for declaration in helper.PROOF_DECLARATIONS:
        assert helper.reported_axioms(outputs["proof"], declaration) <= helper.EXPECTED_AXIOMS
    for declaration in helper.VALIDATION_DECLARATIONS:
        assert helper.reported_axioms(outputs["validation"], declaration) <= helper.EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 5
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]

    historical_probe = subprocess.run(
        [
            "/usr/bin/python3", "-I", "-B",
            str(HERE / "check_validation.py"), "--probe",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    assert historical_probe.returncode != 0
    assert "AssertionError" in historical_probe.stdout

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "release" and receipt["depends_on"] == [validation["item_id"]]
    assert receipt["accepted"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["root_vector_before"] == (
        receipt["result"]["root_vector_after"]
    ) == ROOT_VECTOR
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_receipt_ids"] == []
    assert receipt["result"]["current_lean_output_sha256"] == output_hashes
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"] == CHANGED_PATHS
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    started = datetime.fromisoformat(receipt["timing"]["started_at"])
    ended = datetime.fromisoformat(receipt["timing"]["ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated_at
    assert started.utcoffset() is not None and ended.utcoffset() is not None
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git(
            "status", "--short", "--untracked-files=all", "--",
            ".stage1-worker-selftest.json", f"Stage1_Instances/{THEOREM}",
        )
        actual = {line[3:] for line in status.splitlines()}
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M3, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
