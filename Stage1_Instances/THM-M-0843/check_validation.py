#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0843-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0843"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0843-VALIDATION"
THEOREM = "THM-M-0843"
BASE_REVISION = "d750776142c633e42858cebfc67c5c2664d419d7"
BASE_TREE = "7e62c62f1939b5cb668e56590b709f71f6e676b5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
STATEMENT_EXPRESSION_SHA256 = (
    "3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "5373c66a953b356d53f3849d2b3d2cb9657189e38b458964f992817b66751f06"
)
EXPECTED_INPUTS = {
    "Statement.lean": "6afd11f23d5245eaa4c487ad4484249b517f6fcf4f99373a2f437d5307aee9ec",
    "AnchorAudit.lean": "73c9657416ddab7fc9997eaf32e5e9d488e250f592e448fd15eb91e382504482",
    "anchor-audit.json": "8c581b2d671b928481cd73876bf71c3ea0a3b4f1a06c2021946401741f814d20",
    "ObligationTree.lean": "59b179eeb8b7cdc9f96f131fd52c50e51a4400f7c50625acd9af7e0277ebf417",
    "Proof.lean": "03d47b0be61e4e75cbcd4320ad413a98e5014abbd592c5998172cc28e73c8229",
    "proof-receipt.json": "4b1a91cca81d2b7abaa266247a3ae431d5b86b0082af34d9b846b6fe4de2db22",
    "obligation-registry.json": "43ff3a49c316a51636a9972ef62ee9d37101b5d8e88ca4e68e42cb12b16bb2ce",
    "typed-graphs.json": "ca4d7c16e81e5e0dc4fd84f7a99ae03fae7426523b0c45ee4dabb07d4cb384de",
    "Validation.lean": "47aa8748007d0b5853f805b8d3a584cb0593270ab164331a9ac0bda99c896eba",
    "validation-spec.json": "bdee88fbd87aeca4c123ec63aadc03a60bd64f5a8da50226951b3b205cd6c8bc",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
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
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
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


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1032,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0843-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0843-PROOF"]
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", str(HERE.relative_to(ROOT) / "check_validation.py")]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert len(spec["expected_outputs"]) == 1
    assert spec["covered_obligation_ids"] == [
        "M0843-ROOT", "M0843-T-UPSTREAM", "M0843-T-ADAPTER"
    ]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        STATEMENT_EXPRESSION_SHA256
    )
    assert statement["canonical_formal_target"]["statement_file_sha256"] == (
        EXPECTED_INPUTS["Statement.lean"]
    )
    assert anchor["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert anchor["canonical_statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["obligation_tree_sha256"] == EXPECTED_INPUTS["ObligationTree.lean"]
    assert proof_receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    independent = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.szemerediRegularity",
        "pinnedTerminal", "terminal_adapter", "compose_root",
    ):
        assert forbidden not in independent, forbidden
    assert "exact _root_.szemeredi_regularity G hEpsilon hCard" in independent

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain", cwd=MATHLIB) == ""

    candidate = next(row for row in anchor["candidates"] if row["candidate_id"] == "M0843-C01")
    assert sha256(MATHLIB / candidate["file"]) == candidate["file_sha256"]
    for boundary in candidate["regularity_source_boundary"]:
        assert sha256(MATHLIB / boundary["file"]) == boundary["file_sha256"]
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/SimpleGraph/Regularity/Lemma.olean"
    assert sha256(terminal_olean) == proof_receipt["proof_body"]["terminal_olean_sha256"]
    assert sha256(MATHLIB / "LICENSE") == anchor["immutable_environment"]["license_sha256"]

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in version and LEAN_COMMIT in version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    base_env = os.environ.copy()
    base_env.update({
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_PATH": lean_path,
    })
    with tempfile.TemporaryDirectory(prefix="m0843-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        run([lean, "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=LEAN_ROOT, env=base_env)
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        proof_output = run([lean, str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=module_env)
        validation_output = run([lean, str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=module_env)

    assert_axioms(obligation_output, "szemeredi_regularity")
    assert_axioms(obligation_output, "Stage1Instances.THM_M_0843_Obligations.terminal_adapter")
    assert_axioms(obligation_output, "Stage1Instances.THM_M_0843_Obligations.compose_root")
    for declaration in (
        "szemeredi_regularity",
        "Stage1Instances.THM_M_0843.Proof.pinnedTerminal",
        "Stage1Instances.THM_M_0843.Proof.szemerediRegularity_via_frozen_composition",
        "Stage1Instances.THM_M_0843.Proof.szemerediRegularity",
    ):
        assert_axioms(proof_output, declaration)
    assert_axioms(validation_output, "szemeredi_regularity")
    assert_axioms(
        validation_output,
        "Stage1Instances.THM_M_0843.Validation.differentialSzemerediRegularity",
    )
    assert proof_output.count("Declarations are sorry-free!") == 4
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0843-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert len(reachable) == 38
    assert len(graphs["unverified_decomposition_plans"]) == 18
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_0843.SzemerediRegularityTarget",
        "elaborated_expression_sha256": STATEMENT_EXPRESSION_SHA256,
        "registry_denominator_sha256": REGISTRY_DENOMINATOR_SHA256,
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["provenance"]["terminal_source_sha256"] == candidate["file_sha256"]
    assert receipt["provenance"]["terminal_olean_sha256"] == sha256(terminal_olean)
    assert receipt["provenance"]["license_sha256"] == sha256(MATHLIB / "LICENSE")
    for boundary in candidate["regularity_source_boundary"]:
        name = Path(boundary["file"]).name
        assert receipt["provenance"]["regularity_support_sources"][name] == boundary["file_sha256"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "covered_obligation_ids",
        "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    assert receipt["result"]["exact_root_kernel_closed"] is True
    assert receipt["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["proof_reachable_obligation_count"] == len(reachable)
    assert receipt["result"]["unverified_internal_composition_count"] == 18
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0843-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS narrow kernel replay: exact terminal, frozen composition, proof roots, and differential exact root elaborated")
    print("PASS trust observation: all checked declarations report only propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: frozen hashes, regularity sources, terminal olean, clean mathlib pin, and license agree")
    print("PASS hygiene and architecture: no prohibited construct; 38 reachable IDs and 18 unverified compositions preserved")
    print("FAIL CLOSED authoritative state: prerequisite proof/master reconciliation is pending; accepted root remains H1/M3/R4")
    print("FAIL CLOSED hermetic release: the shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive")
    print("FAIL CLOSED independent release: the differential probe ran in this worker/shared cache, not a distinct signed runner")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
