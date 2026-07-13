#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0912-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0912-VALIDATION"
THEOREM = "THM-M-0912"
BASE_REVISION = "4a10a7a4ddff88e302d5a303b16dd687d9468f63"
BASE_TREE = "730de242597680b39a7087d3204dfd1e6c41c60e"
EXPRESSION_SHA256 = "b322549a05e57fbf466b60eb8ff89f4a08c6ee3b68ea5bf3ff3bf86d99521776"
DENOMINATOR_SHA256 = "c66f1840e6d1bcc7b0a64f7ecdc24ee2f13adc10098ca8467cd238c649f7432b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
BASIC_SOURCE = Path("Mathlib/Data/Nat/Choose/Basic.lean")
BASIC_BLOB = "15a5c95dae82b6fc0ae14eebe85215f89853f7ee"
BASIC_SHA256 = "b3c40f47d39427428d70518b48adaaf16d3622698b32406fa7745749f1387170"
BASIC_OLEAN_SHA256 = "057f7b9cc9a9d24c4d1e2d7fcdec76cf6909fd0ee0439bbe59c25a823efcbf10"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
PROOF_OUTPUT_SHA256 = "c992e4e246af412dc7a18bf35e90239c8c91607c7905916109f87a42e27f2726"
EXPECTED_AXIOMS = {"propext"}
PROOF_OBLIGATION_IDS = [
    "M0912-ROOT",
    "M0912-T-ROOT-COMPOSE",
    "M0912-N-POSITIVE-ROW",
    "M0912-T-PREDECESSOR-COMPOSE",
    "M0912-L-CHOOSE-SUCC-RIGHT",
    "M0912-L-POSITIVE-COLUMN-REINDEX",
    "M0912-N-SUMMAND-ORDER",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase-spec.json",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def run(
    argv: list[str], *, cwd: Path, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def observed_axioms(output: str, declaration: str) -> set[str]:
    qualified = re.escape(declaration)
    match = re.search(
        rf"'{qualified}' depends on axioms: \[(.*?)\]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {value.strip() for value in match.group(1).split(",") if value.strip()}


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    spec = load(HERE / "validation-phase-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    anchor = load(HERE / "anchor-audit.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1454,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0912-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert len(spec["recipes"]) == 3
    for recipe in spec["recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert 0 < recipe["timeout_seconds"] <= 180
        assert recipe["expected_outputs"]
        assert recipe["covered_obligation_ids"]
        assert recipe["covered_declarations"]

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0912-ROOT"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROOF_OBLIGATION_IDS
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == ["propext"]
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["accepted"] is False
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}

    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is False
    assert closure["theorem_complete"] is False

    expected_inputs = {
        "Statement.lean": sha256(HERE / "Statement.lean"),
        "ObligationTree.lean": sha256(HERE / "ObligationTree.lean"),
        "Proof.lean": sha256(HERE / "Proof.lean"),
        "Validation.lean": sha256(HERE / "Validation.lean"),
        "statement.json": sha256(HERE / "statement.json"),
        "obligation-registry.json": sha256(HERE / "obligation-registry.json"),
        "typed-graphs.json": sha256(HERE / "typed-graphs.json"),
        "proof-receipt.json": sha256(HERE / "proof-receipt.json"),
        "anchor-audit.json": sha256(HERE / "anchor-audit.json"),
        "validation-specs.json": sha256(HERE / "validation-specs.json"),
        "validation-phase-spec.json": sha256(HERE / "validation-phase-spec.json"),
        "check_validation.py": sha256(HERE / "check_validation.py"),
    }
    assert receipt["inputs"] == expected_inputs
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["depends_on"] == ["S56-M-0912-PROOF"]
    assert receipt["intent"] == "validate"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["observed_axioms"] == ["propext"]
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0912-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "hermetic.cold_empty_cache_offline_replay"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited mechanism in {name}"
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    imports = [
        line.removeprefix("import ")
        for line in validation_source.splitlines()
        if line.startswith("import ")
    ]
    assert imports == ["Statement", "Mathlib.Util.AssertNoSorry", "Mathlib.Util.PrintSorries"]
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "theorem pascalIdentityTarget_independent_local : PascalIdentityTarget := by" in validation_source
    assert "Nat.choose_eq_choose_pred_add hm hn" in validation_source

    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifacts are missing"
    assert git_output("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=MATHLIB) == ""
    basic = MATHLIB / BASIC_SOURCE
    basic_olean = MATHLIB / ".lake/build/lib/lean" / BASIC_SOURCE.with_suffix(".olean")
    assert git_output("rev-parse", f"HEAD:{BASIC_SOURCE}", cwd=MATHLIB) == BASIC_BLOB
    assert sha256(basic) == BASIC_SHA256
    assert sha256(basic_olean) == BASIC_OLEAN_SHA256
    basic_text = without_comments(basic.read_text(encoding="utf-8"))
    assert prohibited.search(basic_text) is None
    for marker in (
        "def choose :",
        "theorem choose_succ_right",
        "theorem choose_eq_choose_pred_add",
        "Nat.exists_eq_add_of_le'",
        "Nat.add_one_sub_one",
    ):
        assert marker in basic_text

    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).stdout.strip()
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).stdout.strip()
    assert sha256(Path(lean)) == LEAN_EXECUTABLE_SHA256
    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="stage1-m0912-validation-") as directory:
        temporary = Path(directory)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (temporary / name).write_bytes((HERE / name).read_bytes())
        environment = os.environ.copy()
        environment.update(
            {
                "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
                "LANG": "C",
                "LC_ALL": "C",
                "NO_COLOR": "1",
                "TZ": "UTC",
                "LEAN_PATH": lean_path,
            }
        )
        outputs["Statement.lean"] = run(
            [lean, "-o", str(temporary / "Statement.olean"), str(temporary / "Statement.lean")],
            cwd=temporary,
            env=environment,
        ).stdout
        environment["LEAN_PATH"] = f"{temporary}:{lean_path}"
        outputs["ObligationTree.lean"] = run(
            [lean, "-o", str(temporary / "ObligationTree.olean"), str(temporary / "ObligationTree.lean")],
            cwd=temporary,
            env=environment,
        ).stdout
        outputs["Proof.lean"] = run(
            [lean, str(temporary / "Proof.lean")], cwd=temporary, env=environment
        ).stdout
        outputs["Validation.lean"] = run(
            [lean, str(temporary / "Validation.lean")], cwd=temporary, env=environment
        ).stdout

    proof_declarations = (
        "Nat.choose_succ_right",
        "Nat.choose_eq_choose_pred_add",
        "Stage1Instances.THM_M_0912.Proof.positiveColumnReindex_proof",
        "Stage1Instances.THM_M_0912.Proof.chooseSuccRight_proof",
        "Stage1Instances.THM_M_0912.Proof.predecessorRecurrence_from_frozen_children",
        "Stage1Instances.THM_M_0912.Proof.predecessorRecurrence_pinned",
        "Stage1Instances.THM_M_0912.Proof.root_via_pinned_composition",
        "Stage1Instances.THM_M_0912.Proof.root_via_frozen_children",
        "Stage1Instances.THM_M_0912.Proof.pascalIdentityTarget_proof",
        "Stage1Instances.THM_M_0912.Proof.pascalIdentityTarget_via_frozen_children",
    )
    validation_declarations = (
        "Nat.choose_eq_choose_pred_add",
        "Stage1Instances.THM_M_0912.Validation.pascalIdentityTarget_independent_local",
    )
    for declaration in proof_declarations:
        assert observed_axioms(outputs["Proof.lean"], declaration) == EXPECTED_AXIOMS
    for declaration in validation_declarations:
        assert observed_axioms(outputs["Validation.lean"], declaration) == EXPECTED_AXIOMS
    assert outputs["Proof.lean"].count("Declarations are sorry-free!") == 10
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in outputs["Proof.lean"] + outputs["Validation.lean"]
    assert "error:" not in "".join(outputs.values())

    local_provenance = receipt["provenance"]
    assert local_provenance["terminal_source_sha256"] == sha256(basic)
    assert local_provenance["terminal_olean_sha256"] == sha256(basic_olean)
    assert local_provenance["dependency_revision"] == MATHLIB_REVISION
    assert local_provenance["dependency_tree"] == MATHLIB_TREE
    closure_payload = {
        "terminal_declarations": local_provenance["terminal_declarations"],
        "direct_dependencies": local_provenance["direct_dependencies"],
        "origins": local_provenance["origins"],
        "observed_axioms": receipt["result"]["observed_axioms"],
        "terminal_source_sha256": local_provenance["terminal_source_sha256"],
        "terminal_olean_sha256": local_provenance["terminal_olean_sha256"],
    }
    assert local_provenance["direct_trust_observation_sha256"] == canonical_sha256(closure_payload)
    assert local_provenance["transitive_trust_closure_sha256"] is None

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["commands_and_results"],
        "output_summary": receipt["output_summary"],
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS
    for path in (ROOT / relative for relative in CHANGED_PATHS):
        check_text_file(path)

    print(
        "PASS THM-M-0912 validation: exact warm kernel, trust observation, "
        "and pinned local provenance"
    )
    print("PASS differential exact root: separately written local probe reports only propext")
    print(
        "BLOCKED node acceptance: proof prerequisite lacks master acceptance and "
        "the authoritative graph remains M3"
    )
    print(
        "BLOCKED release gates: no cold offline empty-cache replay, complete transitive "
        "TCB/SBOM, or distinct independent runner"
    )


if __name__ == "__main__":
    main()
