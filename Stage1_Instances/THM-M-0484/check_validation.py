#!/usr/bin/env python3
"""Fail-closed local validation for S56-M-0484-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0484"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0484-VALIDATION"
THEOREM = "THM-M-0484"
BASE_REVISION = "27400857bccc93638c97e9c65859ddf5d5b5f4da"
BASE_TREE = "3762537e0e5ae46cd70b086da49a69e2fd7b275c"
EXPRESSION_SHA256 = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
DENOMINATOR_SHA256 = "af0c1b5d7bfd4da0a7f1b982646906d20217976af4c5805295d37e43d0b39edf"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
TERMINAL_SOURCE_BLOB = "36af70028d43c613055738999815ed2e88e84bd4"
TERMINAL_SOURCE_SHA256 = "6321c156165f59d49954c0e6e47706e765c0277df20b97a20333ceba29e8bead"
TERMINAL_OLEAN_SHA256 = "c02832844a7c1605945cf05750cbcc0909909124ea7ba45f335888bae0157844"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TERMINAL_BODY_IDS = (
    "8ec5fa60da0232f21b8a79ca9a7a846be51b71ed8b5bae0016943f880599efaf",
    "8f45e13a6d27e866e46e24320d770ad4c0a4e1b01412b2c32e708c00a29d01dd",
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase-spec.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


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
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 240,
) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def replay() -> dict[str, object]:
    fixed_env = os.environ.copy()
    fixed_env.update(
        {
            "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
        }
    )
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
    assert sha256(lean) == LEAN_EXECUTABLE_SHA256
    assert sha256(lake) == LAKE_EXECUTABLE_SHA256
    version = run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    assert "4.29.0" in version and LEAN_COMMIT in version
    lake_version = run([str(lake), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    assert "5.0.0" in lake_version and "4.29.0" in lake_version

    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).strip()
    base_module_env = fixed_env.copy()
    base_module_env["LEAN_PATH"] = lean_path

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0484-validation-", dir=LEAN_ROOT))
    try:
        for name in (
            "Statement.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean", "AnchorAudit.lean",
        ):
            (tmp / name).write_bytes((HERE / name).read_bytes())

        statement_output = run(
            [
                "lake", "env", "lean", "--trust=0", "-o", str(tmp / "Statement.olean"),
                str(tmp / "Statement.lean"),
            ],
            cwd=LEAN_ROOT,
            env=base_module_env,
        )
        module_env = base_module_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [
                "lake", "env", "lean", "--trust=0", "-o",
                str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean"),
            ],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        proof_output = run(
            ["lake", "env", "lean", "--trust=0", str(tmp / "Proof.lean")],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        validation_output = run(
            ["lake", "env", "lean", "--trust=0", str(tmp / "Validation.lean")],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        anchor_output = run(
            ["lake", "env", "lean", "--trust=0", str(tmp / "AnchorAudit.lean")],
            cwd=LEAN_ROOT,
            env=base_module_env,
        )
    finally:
        for path in sorted(tmp.iterdir(), reverse=True):
            path.unlink()
        tmp.rmdir()

    for output in (proof_output, validation_output, anchor_output):
        assert "Declarations are sorry-free!" in output
        assert "sorryAx" not in output

    for declaration in (
        "lucas_lehmer_sufficiency",
        "lucas_lehmer_necessity",
        "Stage1Instances.THM_M_0484.Proof.pinnedSufficiency",
        "Stage1Instances.THM_M_0484.Proof.pinnedNecessity",
        "Stage1Instances.THM_M_0484.Proof.assembledRoot",
        "Stage1Instances.THM_M_0484.Proof.lucasLehmerCriterion",
    ):
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "lucas_lehmer_sufficiency",
        "lucas_lehmer_necessity",
        "Stage1Instances.THM_M_0484.Validation.differentialResidueCriterion",
        "Stage1Instances.THM_M_0484.Validation.differentialLucasLehmerCriterion",
    ):
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "lucas_lehmer_sufficiency",
        "lucas_lehmer_necessity",
        "Stage1Instances.THM_M_0484.AnchorAudit.exactTarget_mathlib_candidate",
    ):
        assert reported_axioms(anchor_output, declaration) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THM_M_0484.ObligationTree.root_of_directions",
        "Stage1Instances.THM_M_0484.ObligationTree.root_of_terminal",
    ):
        assert reported_axioms(obligation_output, declaration) == {
            "propext", "Quot.sound"
        }

    closure = re.search(
        r"ANCHOR_CLOSURE declarations=(\d+) modules=(\d+)", anchor_output
    )
    assert closure is not None
    assert (int(closure.group(1)), int(closure.group(2))) == (35389, 1243)
    assert "ANCHOR_CLOSURE bodyless_nonaxioms=[]" in anchor_output
    assert "ANCHOR_CLOSURE unsafe=[]" in anchor_output
    assert all("error:" not in output for output in (
        statement_output, obligation_output, proof_output, validation_output, anchor_output
    ))

    outputs = {
        "statement": statement_output,
        "obligation_tree": obligation_output,
        "proof": proof_output,
        "validation": validation_output,
        "anchor_audit": anchor_output,
    }
    return {
        "output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "anchor_closure_declarations": 35389,
        "anchor_closure_modules": 1243,
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "composition_axioms": ["Quot.sound", "propext"],
    }


def check_static(receipt: dict, spec: dict) -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    anchor_receipt = load(HERE / "anchor-audit-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION == receipt["base_revision"]
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE == receipt["base_tree"]
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1365,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0484-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0484-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_item = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_item["state"] == "open" and local_item["evidence_ids"] == []
    assert local_dag["accepted_states"] == []

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0484-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 300
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert receipt["recipe"] == recipe
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["content_addressed"] is False

    paths = {
        "lean-toolchain": LEAN_ROOT / "lean-toolchain",
        "lake-manifest.json": LEAN_ROOT / "lake-manifest.json",
    }
    paths.update({name: HERE / name for name in receipt["inputs"] if name not in paths})
    for name, expected in receipt["inputs"].items():
        assert sha256(paths[name]) == expected, f"stale validation input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0484-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert len(graphs["unverified_decomposition_plans"]) == 17
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-0484-PROOF"
    assert proof_receipt["proposed_state"] == "[_]" and proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert proof_receipt["result"]["root_kernel_declaration_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["internal_composition_boundary"][
        "unverified_internal_composition_count"
    ] == 17
    assert anchor_receipt["candidate_result"]["trust_zero"] is True
    assert anchor_receipt["candidate_result"]["transitive_declaration_count"] == 35389
    assert anchor_receipt["candidate_result"]["bodyless_nonaxioms"] == []
    assert anchor_receipt["candidate_result"]["unsafe_declarations"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited construct in {name}"
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert re.search(
        r"^[ \t]*import[ \t]+(?:Proof|ObligationTree)\b",
        validation_source,
        re.MULTILINE,
    ) is None
    for fragment in (
        "theorem differentialResidueCriterion : LucasLehmerResidueTarget",
        "lucas_lehmer_sufficiency p (by omega) hresidue",
        "lucas_lehmer_necessity p hp hprime",
        "lucasLehmerTestTarget_iff_residueTarget.mpr differentialResidueCriterion",
        "assert_no_sorry differentialLucasLehmerCriterion",
        "#print axioms differentialLucasLehmerCriterion",
    ):
        assert fragment in validation_source, fragment

    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_record = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_record["rev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink(), "canonical worker .lake symlink is missing"
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    terminal_rel = Path("Mathlib/NumberTheory/LucasLehmer.lean")
    terminal_source = mathlib / terminal_rel
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/NumberTheory/LucasLehmer.olean"
    assert git("rev-parse", f"HEAD:{terminal_rel}", cwd=mathlib) == TERMINAL_SOURCE_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert terminal_olean.stat().st_size == 516240
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    source_lines = terminal_source.read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(source_lines[580:591])).hexdigest() == TERMINAL_BODY_IDS[0]
    assert hashlib.sha256(b"".join(source_lines[592:608])).hexdigest() == TERMINAL_BODY_IDS[1]
    terminal_code = code_without_comments(terminal_source.read_text(encoding="utf-8"))
    assert prohibited.search(terminal_code) is None
    for fragment in (
        "theorem lucas_lehmer_sufficiency",
        "theorem lucas_lehmer_necessity",
        "have h\u2081 := order_ineq p' t",
        "have := X.\u03c9_pow_trace",
    ):
        assert fragment in terminal_code, fragment

    result = receipt["result"]
    assert result["exact_root_kernel_closed_locally"] is True
    assert result["differential_wrapper_route_checked"] is True
    assert result["distinct_terminal_proof_body_checked"] is False
    assert result["complete_transitive_trust_and_provenance"] == "fail_closed"
    assert result["accepted_foundation_and_tcb_policy"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is False and result["theorem_complete"] is False


def check_worker_packet(receipt: dict, path: Path) -> None:
    packet = load(path.resolve())
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"]
    assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]

    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    observation = replay()
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    receipt = load(HERE / "validation-receipt.json")
    spec = load(HERE / "validation-phase-spec.json")
    check_static(receipt, spec)
    assert receipt["result"]["lean_output_sha256"] == observation["output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["composition_axioms"] == observation["composition_axioms"]
    assert receipt["result"]["terminal_closure"] == {
        "declarations": observation["anchor_closure_declarations"],
        "modules": observation["anchor_closure_modules"],
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }
    if args.worker_packet is not None:
        check_worker_packet(receipt, args.worker_packet)

    for relative in CHANGED_PATHS[1:]:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS S56-M-0484-VALIDATION: exact root and differential residue route kernel-replayed")
    print("PASS trust observation: exact classical trio; terminal bodyless and unsafe scans are empty")
    print("PASS direct provenance: source bodies, olean, clean pin/tree, remote, and license agree")
    print("FAIL CLOSED authority: proof receipt and root state await master acceptance/reconciliation")
    print("FAIL CLOSED transitive trust/TCB: serialized closure, executables, SBOM, and policy are incomplete")
    print("FAIL CLOSED hermetic gate: shared warm cache is not a cold empty-cache offline replay")
    print("FAIL CLOSED independent gate: same-worker probe is not a distinct signed runner/verifier")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
