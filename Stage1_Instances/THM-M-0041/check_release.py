#!/usr/bin/env python3
"""Self-test the fail-closed release decision for THM-M-0041."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0041"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0041-RELEASE"
THEOREM = "THM-M-0041"
BASE_REVISION = "2bfb272c83b2089e9b285d48dce2c30616ff6c36"
BASE_TREE = "f44853226ddecdf2a2b462fd6c85e770bbffbaa3"
EXPRESSION_SHA256 = "5aad8415af4578ca43d0ec58eee038ed4470dce17896766215d3bf9f49d8e711"
DENOMINATOR_SHA256 = "c854b50bfd112e0e20a94f25fc6db6f4fda74e248e61b647ffd93d93977c33dc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
TERMINAL_SOURCE_SHA256 = "9e22d8fdace32c7bb8304335027b95ccb4cca18b5d430076ac4f87b2d76ca3f2"
TERMINAL_SOURCE_BLOB = "f9f5b9423cbc597a427c6da31f42ad6466c2940b"
TERMINAL_BODY_SHA256 = "427ef4b3af84b4d5f1445bf4b7cadc44af97aca88833bbc30307661b7915c7cd"
TERMINAL_OLEAN_SHA256 = "882236875a32debd61e2ca5cdb3026350a01240abe7eb5d6c5a93863c5b591aa"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "instance.json": "1ab6e19a003f2c0f6da30e8f62f2b0289f00cc6d2808f82617c776807a7575a1",
    "task-dag.json": "cad7969266852634a08a293e22a760553c9ffe86d65d7d729f34f00d8a1d38d9",
    "statement.json": "f247195d6c3693d8371b145f1e53092af0c3ebc9277061cccddb50d334d88351",
    "source-statement-crosswalk.md": "112b62ef0e95a10e73233afbdc1f562e3237e9690010697b08d6785d3c2bf78b",
    "obligation-registry.json": "7d8f26df395fa73ca9dacb9f20fe9564f8f3232491c62976f57c86ee12936cac",
    "typed-graphs.json": "8bb7d50066c36b84935880b240d79091e964ce53a0599f90ebdf6a408c5c84b1",
    "intake-receipt.json": "c6e413bc576cd18a242919c0ff0d3bb2e13b8643edfb2956a1c5e6dd76e13008",
    "statement-receipt.json": "88f8bf833dd041aff111d8ebd679a89114d8b494b12fd14fb824b609e555a8cd",
    "anchor-audit-receipt.json": "6126d28f4943207668935dd06aa4b40df591a31b1cd77eae86ab1f0faae824ef",
    "obligation-tree-receipt.json": "876001bcedec4c709e4b4cf6dc2ab0660e759d5d8af9cbde622d315a53895e2e",
    "proof-receipt.json": "5443de832daf6f4f3c76f07e8ea6936cdf2f0448bcc057141fd1640b4968e2d9",
    "validation-receipt.json": "5a5212d49e67c6b6f1f441e8e16cee37cab73e6b7cbffc98ed6438143cb51801",
    "Statement.lean": "3b218c1a96922399bb8ed2d852d556422a92901dca10efdd431a677eaefd2b0b",
    "Proof.lean": "051ac9b2030db4c21edece622b80820a82a41a5f444912570b736d5f5e688506",
    "Validation.lean": "cfb78c37b4ef84a9c7609918047c328dcdab6abaabeb616ab8fd6307b603dccc",
    "validation-spec.json": "c5e667aaa9f0729ac2e61e07d915ee9364579b3513518294957b752589488c4f",
}
REMAINING_CUT = {
    "M0041-T-CHARPOLY",
    "M0041-A-MATHLIB-ANCHOR",
    "M0041-X-SOURCE",
    "M0041-S-FOUNDATION",
    "M0041-X-PROVENANCE",
    "M0041-X-TRUST",
    "M0041-X-READABLE",
    "M0041-X-WORKFLOW",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
EXPECTED_COMMANDS = [
    "python3 Docs/tools/check_stage1_standard.py",
    "python3 scripts/stage1_target.py check",
    "python3 scripts/stage1_target.py show THM-M-0041",
    "python3 -B Stage1_Instances/THM-M-0041/check_release.py",
    "python3 -m json.tool Stage1_Instances/THM-M-0041/release-spec.json",
    "python3 -m json.tool Stage1_Instances/THM-M-0041/release-receipt.json",
    "python3 -m json.tool .stage1-worker-selftest.json",
    "PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0041-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0041/check_release.py",
    "rg -n -i --glob '*.lean' '\\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0041/Statement.lean Stage1_Instances/THM-M-0041/Proof.lean Stage1_Instances/THM-M-0041/Validation.lean",
    "git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json",
]
EXPECTED_SUMMARY = (
    "Release-node self-test passed: the exact statement and differential root elaborated in /tmp "
    "with the pinned Lean executable, were sorry-free, and reported exactly propext, "
    "Classical.choice, and Quot.sound. Evidence reconciliation truthfully returned blocked: "
    "lifecycle planned, vector H1/M3/R3, AUDIT-Z=false because required "
    "classification/reconciliation is unaccepted, THEOREM-Z=false, no accepted receipts, "
    "release_grade=false."
)
EXPECTED_STDOUT_SHA256 = "ff6775b5e53e89ab520a943dd04a89be936acd251f322da7767075cef95897a0"
EXPECTED_STDOUT_LINES = [
    "PASS THM-M-0041 release reconciliation",
    "PASS exact-root temporary Lean replay: sorry-free; axioms propext, Classical.choice, Quot.sound",
    "BLOCKED dependency: S56-M-0041-VALIDATION is provisional and not master-accepted",
    "BLOCKED AUDIT-Z: source/readability/trust classification and graph reconciliation are unaccepted",
    "BLOCKED THEOREM-Z: cold/offline, SBOM, independent-verifier, bundle, and master gates remain open",
    "verdict=blocked; lifecycle=planned; audit_complete=false; theorem_complete=false",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def replay_exact_root() -> tuple[Path, Path]:
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="thm-m-0041-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "Validation.lean"):
            shutil.copyfile(HERE / name, tmp / name)
        statement_env = env.copy()
        statement_env["LEAN_PATH"] = lean_path
        run([lean, "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=statement_env)
        validation_env = env.copy()
        validation_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        output = run([lean, "Validation.lean"], cwd=tmp, env=validation_env)
    assert output.count("Declarations are sorry-free!") == 2, output
    assert_axioms(output, "Matrix.aeval_self_charpoly")
    assert_axioms(
        output,
        "Stage1Instances.THM_M_0041.Validation.differentialCayleyHamilton",
    )
    return Path(lean), Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale release input: {name}"

    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1081
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1081,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0041-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    dependency_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0041-VALIDATION"
    )
    assert dependency_item["state"] == "[_]"
    local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open"
    assert local_item["depends_on"] == ["S56-M-0041-VALIDATION"]

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["root_closed"] is False
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert set(boundary["remaining_root_cut_set"]) == REMAINING_CUT

    receipt_names = (
        "intake-receipt.json",
        "statement-receipt.json",
        "anchor-audit-receipt.json",
        "obligation-tree-receipt.json",
        "proof-receipt.json",
        "validation-receipt.json",
    )
    predecessor_ids = []
    for name in receipt_names:
        predecessor = load(HERE / name)
        assert predecessor["proposed_state"] == "[_]", name
        assert predecessor["accepted"] is False, name
        predecessor_ids.append(predecessor["receipt_id"])
    assert proof["result"]["root_closed_by_kernel"] is True
    assert proof["result"]["theorem_complete"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert validation["release_grade"] is False and validation["accepted"] is False
    assert validation["result"]["exact_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_closed_obligations"] == []
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "did not provision a kernel network namespace" in spec["network_enforcement"]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": f"sha256:{EXPECTED_STDOUT_SHA256}",
    }]
    assert spec["covered_obligation_ids"] == ["M0041-ROOT"]
    assert set(spec["reconciled_open_obligation_ids"]) == REMAINING_CUT
    assert set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_0041.CayleyHamiltonTarget",
        "Matrix.aeval_self_charpoly",
        "Stage1Instances.THM_M_0041.Validation.differentialCayleyHamilton",
    }
    assert "Only M0041-ROOT receives a fresh provisional Lean replay" in spec["scope_boundary"]
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"].startswith("S56-M-0041-RELEASE-local-")
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["depends_on"] == ["S56-M-0041-VALIDATION"]
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["owner"] == receipt["attestor"] == "stage1-rev56-worker-slot1"
    assert receipt["acceptance_authority"] == "Stage1 integration lane"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["release-spec.json"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["check_release.py"] == sha256(HERE / "check_release.py")
    for key in (
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "network_enforcement",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "reconciled_open_obligation_ids",
        "covered_declarations",
        "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key]

    decision = receipt["decision"]
    assert receipt["verdict"] == decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    expected_vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert decision["root_vector_before"] == decision["root_vector_after"] == expected_vector
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["audit_z"] == decision["theorem_z"] == "blocked"
    assert decision["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["worker_release_item_self_tested"] is True
    assert decision["master_acceptance_pending"] is True
    assert receipt["dependency"] == {
        "item_id": "S56-M-0041-VALIDATION",
        "worker_projection": "[_]",
        "master_accepted": False,
        "receipt_id": validation["receipt_id"],
        "receipt_sha256": EXPECTED_INPUTS["validation-receipt.json"],
        "support_state": validation["support_state"],
        "release_grade": validation["release_grade"],
    }
    assert receipt["provisional_receipt_ids_inspected"] == predecessor_ids
    assert receipt["first_failed_gate"]["gate_id"] == "dependency.S56-M-0041-VALIDATION.master_acceptance"
    assert receipt["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["remaining_root_cut_set"]) == REMAINING_CUT
    required_false = {
        "authoritative_graph_reconciled",
        "accepted_root_m0_e1",
        "audit_z_accepted",
        "accepted_source_boundary_classification",
        "accepted_readability_classification",
        "accepted_transitive_provenance_foundation_tcb",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    }
    evidence = receipt["evidence_reconciliation"]
    assert all(evidence[name] is False for name in required_false)
    assert evidence["exact_root_kernel_replay"] == "provisional_pass"
    assert evidence["provisional_observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert evidence["provisional_placeholder_and_unsafe_scan"] == "pass"

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    lean, lake = replay_exact_root()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["environment"]["lean_toolchain"] == "leanprover/lean4:v4.29.0"
    assert receipt["environment"]["lean_version"].endswith(LEAN_COMMIT)
    assert receipt["environment"]["network"] == "not_used"
    assert "not an immutable clean checkout" in receipt["environment"]["reproduction_boundary"]
    terminal_source = MATHLIB / "Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean"
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.olean"
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert git(
        "rev-parse", "HEAD:Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean", cwd=MATHLIB
    ) == TERMINAL_SOURCE_BLOB
    body = terminal_source.read_bytes().splitlines(keepends=True)[210:231]
    assert hashlib.sha256(b"".join(body)).hexdigest() == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    provenance = receipt["provisional_provenance"]
    assert provenance == {
        "terminal_declaration": "Matrix.aeval_self_charpoly",
        "terminal_source_sha256": TERMINAL_SOURCE_SHA256,
        "terminal_source_blob": TERMINAL_SOURCE_BLOB,
        "terminal_body_sha256": TERMINAL_BODY_SHA256,
        "terminal_olean_sha256": TERMINAL_OLEAN_SHA256,
        "license_sha256": LICENSE_SHA256,
        "transitive_trust_status": "incomplete_fail_closed",
    }

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == EXPECTED_COMMANDS
    assert packet["output_summary"] == EXPECTED_SUMMARY
    commands = receipt["commands_and_exit_codes"]
    assert [row["command"] for row in commands] == EXPECTED_COMMANDS
    assert [row["exit_code"] for row in commands] == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    assert receipt["execution"]["exit_code"] == 0
    assert receipt["execution"]["stdout_sha256"] == EXPECTED_STDOUT_SHA256
    assert receipt["execution"]["started_at"] < receipt["execution"]["ended_at"]
    assert receipt["validated_at"] == receipt["execution"]["ended_at"]
    assert receipt["public_projection"] == {
        "path": "Stage1_Instances/THM-M-0041/release-phase.md",
        "sha256": sha256(HERE / "release-phase.md"),
        "audit_complete": False,
        "theorem_complete": False,
        "verdict": "blocked",
    }
    dirty = receipt["dirty_inputs"]
    assert dirty["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert git("diff", "--binary", "HEAD", "--", f"Stage1_Instances/{THEOREM}") == ""
    assert dirty["pre_existing_untracked"] == {
        "path": "Formalizations/Lean/.lake",
        "kind": "symlink",
        "target_string_sha256": hashlib.sha256(
            os.readlink(LEAN_ROOT / ".lake").encode()
        ).hexdigest(),
    }
    for relative in CHANGED_PATHS - {f"Stage1_Instances/{THEOREM}/release-receipt.json"}:
        assert dirty["owned_untracked_sha256"][relative] == sha256(ROOT / relative)
    assert "self-referential" in dirty["hash_boundary"]
    assert "theorem completion" in receipt["status_boundary"]
    assert "fully classify and reconcile the audit inventory" in receipt["retry_condition"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    stdout = "\n".join(EXPECTED_STDOUT_LINES) + "\n"
    assert hashlib.sha256(stdout.encode()).hexdigest() == EXPECTED_STDOUT_SHA256
    print(stdout, end="")


if __name__ == "__main__":
    main()
