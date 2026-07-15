#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0861-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("check_release.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0861"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0861-RELEASE"
THEOREM = "THM-M-0861"
BASE_REVISION = "705caafffbcdaf43757a4468b018716da692307d"
BASE_TREE = "ee88e7872fd1a00bc7c906f6deeb99ecdf7e1a64"
EXPRESSION_SHA256 = "4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197"
DENOMINATOR_SHA256 = "1272c7806d6c29040abda962a5fd83037c2f57a04631ddd5507b6e84c46af230"
VALIDATION_RECEIPT_SHA256 = "bfaca214dd8f9141d446190fd096377243470f745ea14c7b200393e7e158af8b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
OPEN_ROOT_CUT = ["M0861-T-UPPER"]
PROVISIONAL_CLOSED = [
    "M0861-L-DEGREE-LE-MAX",
    "M0861-L-INCIDENCE-FIN",
    "M0861-L-COLOR-INJECTIVE",
    "M0861-L-SUP-LOWER",
    "M0861-T-LOWER",
    "M0861-B-SMALL-EDGE-COUNT",
    "M0861-L-SMALL-PALETTE-EMBED",
]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0861_Proof.degree_le_maxDegree",
    "Stage1Instances.THM_M_0861_Proof.incidenceSet_finite",
    "Stage1Instances.THM_M_0861_Proof.incidentColor_injective",
    "Stage1Instances.THM_M_0861_Proof.maxDegree_le_of_degree_le",
    "Stage1Instances.THM_M_0861_Proof.lowerBound",
    "Stage1Instances.THM_M_0861_Proof.edgePaletteEmbedding",
    "Stage1Instances.THM_M_0861_Proof.edgeColorable_of_edge_ncard_le",
    "Stage1Instances.THM_M_0861_Proof.upperBound_of_boundedSatzC",
    "Stage1Instances.THM_M_0861_Proof.konigEdgeColoring_of_boundedSatzC",
)
DIFFERENTIAL_DECLARATION = (
    "Stage1Instances.THM_M_0861_Validation.rootFromBoundedSatzC"
)
EXPECTED_INPUTS = {
    "README.md": "6e6e55e838121c6ff3650d9e6b2f87db961698814920eb3f4a838833b49402d0",
    "Statement.lean": "a6ce9ee3edd720d38fa9306324e38b48d5f0430a8b9513b9207e7808ea1b380d",
    "AnchorAudit.lean": "d109f2336caa28e017313e05572986ec1e1e2311d267b486789fb240552628e6",
    "ObligationTree.lean": "066fe4c9e401d6a5c45fe7699cfca3278661f77b32404d4eb7151dfe5b8aa5be",
    "Proof.lean": "fc9fab5aadcf161926b3f1efee51e6e0f47fb638cf940f91a4d0945edd3244db",
    "Validation.lean": "36aaddaa58e1bdda28795a437bd38a803a16469cb8c820391da95f92be8262fb",
    "statement.json": "af40ef59543ec155fe465f78fc3d3393aa651952f108f70ea36a27366401fb3d",
    "anchor-audit.json": "3adb7aaf96cc2fa6959da59a6a4556a9447505ee6f4be4078e73db7e17bd1c34",
    "obligation-registry.json": "44f0fcb20dce6ed0c1d60302a41e0f58aa86d2c5c91bc6821e5ccb14e87629d3",
    "typed-graphs.json": "dc170c799a1fc6f9711befe8daf5b5629d7b600a851db130e8525a8372e83ea5",
    "validation-specs.json": "f315c8f6fe4e3514ab6c13266333e67e4b0440690a9b6b96684dea287b08b11a",
    "instance.json": "6a4f30bd9aef94ec6416130d7cf3ff7ec35e9e13657a64099cef17f442d06418",
    "task-dag.json": "6c802c333cd0e8529e0b7f97b78a9eb2d2ec3b939ab3d0e995c794541a42cdc3",
    "intake-receipt.json": "d9419e3b41eccacc80596b379e4b49b92eb64cd18da2f20838b45c2a33740c78",
    "statement-receipt.json": "02031cc500ddb47ef1d08de1b084e72f7ac2dba16cf1d9b77717f57b4f3e7956",
    "anchor-audit-receipt.json": "b018ce0b793a9587133a6ce0a4905e1481655fc68e97ee7c72e1f1b3f37c41be",
    "obligation-tree-receipt.json": "8307fc193c9b7e81270d91887ae81458641482ab3dbc3e8508cd770c2e3aacc0",
    "proof-receipt.json": "8cc938ba3d65f43f691b2a4b28794cd371f90f544662de51a6494593e59891aa",
    "proof-blocker.json": "08e546a93f3f1ac4da1f9c597b4d4146d08b6596da63d6e32a198b9c383f31f4",
    "validation-spec.json": "5b7bf7f458f643f38c75bfb96a1f279e353d6d4ed9330bffc0b4f34036e8a555",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-blocker.json": "d7717f586874c92b61c2f024a8ca3ff782816ba7be4157beff69ca14b121bc07",
    "check_validation.py": "288fc7a215f27d941550916b146119e87e8760304f213567da24a56c64bfba2e",
    "validation-phase.md": "de9a67455ca2067211ec87b9a461b1ca7d5558afc10bf721f1d18da66db3e6d8",
}
EXPECTED_AUTHORITIES = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "0083f3e7f384cd6e70fb105b8c551d2968f63db8ec8aedcbc37ecc28172e7f7a",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "aee0a15c743fbfd08a904892874753db21b540dd56dea3a1f42347d68e4ff4db",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, authorities, and hashes agree",
    "PASS narrow Lean replay: partial bodies and conditional root are sorry-free at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: BoundedSatzCTarget is unproved and M0861-T-UPPER remains open",
    "BLOCKED audit/release: H0/R0, cold offline bundle, TCB/SBOM, and independent verifier are absent",
    "verdict=blocked lifecycle=planned root_vector=H1/M4/R4 audit_complete=false theorem_complete=false",
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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).strip()


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def compiled_roots() -> list[Path]:
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    local = (LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve()
    if local.is_dir():
        roots.append(local)
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0861-release-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
            "Proof.lean", "Validation.lean",
        ):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        dependency_path = ":".join(str(path) for path in compiled_roots())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, env={"PATH": "/usr/bin:/bin"})

        old_umask = os.umask(0o022)
        try:
            return {
                "statement": lean_run("Statement.lean", False, True),
                "anchor_audit": lean_run("AnchorAudit.lean", True, False),
                "obligation_tree": lean_run("ObligationTree.lean", True, True),
                "proof": lean_run("Proof.lean", True, True),
                "validation": lean_run("Validation.lean", True, False),
            }
        finally:
            os.umask(old_umask)


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    transitive_receipts = [
        load(HERE / name)
        for name in (
            "intake-receipt.json", "statement-receipt.json",
            "anchor-audit-receipt.json", "obligation-tree-receipt.json",
        )
    ]
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1415 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1415,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0861-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0861-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0861-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITIES.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert receipt["input_bindings"] == {
        f"Stage1_Instances/{THEOREM}/{name}": expected
        for name, expected in EXPECTED_INPUTS.items()
    } | EXPECTED_AUTHORITIES
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0861.KonigEdgeColoringTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0861-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    inventory = registry["frozen_denominators"]["inventory"]
    assert len(inventory) == len(registry["obligations"]) == 54
    assert spec["covered_obligation_ids"] == inventory

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["accepted_states"] == []
    assert all(row["state"] == "open" for row in local_dag["tasks"])
    expected_transitive = [
        ("S56-M-0861-INTAKE", "S56-M-0861-INTAKE-WORKER-20260713"),
        ("S56-M-0861-STATEMENT", "S56-M-0861-STATEMENT-WORKER-4E7919ED"),
        ("S56-M-0861-ANCHOR_AUDIT", "S56-M-0861-ANCHOR-AUDIT-WORKER-20260713"),
        ("S56-M-0861-OBLIGATION_TREE", "S56-M-0861-OBLIGATION_TREE-worker-b243ebc0"),
    ]
    assert [
        (row["item_id"], row["receipt_id"]) for row in transitive_receipts
    ] == expected_transitive
    assert all(row["theorem_id"] == THEOREM for row in transitive_receipts)
    assert all(row["proposed_state"] == "[_]" for row in transitive_receipts)
    assert all(row["accepted"] is False for row in transitive_receipts)
    assert decision["provisional_receipt_ids_inspected"] == [
        *(receipt_id for _, receipt_id in expected_transitive),
        proof["receipt_id"], validation["receipt_id"],
    ]
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["authoritative_root_vector"] == VECTOR
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_CLOSED
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-0861-PROOF.master_acceptance"
    )
    assert validation_blocker["root_kernel_closed"] is False
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is receipt["content_addressed_release_evidence"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert set(decision["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == VECTOR
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0861-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_mathematical_gate"]["gate_id"] == "M0861-T-SATZ-C"
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-0861-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_mathematical_gate"] == "M0861-T-SATZ-C"

    for gate in (
        "exact_unconditional_upper_and_root_kernel_closure",
        "authoritative_instance_task_registry_graph_reconciliation",
        "node_specific_proof_and_composition_acceptance",
        "accepted_h0_primary_source_review",
        "independently_reviewed_r0_reconstruction",
        "accepted_foundation_and_complete_transitive_tcb",
        "complete_provenance_sbom_and_license_archive",
        "immutable_clean_cold_offline_reproduction",
        "deterministic_content_addressed_release_bundle",
        "distinct_signed_independent_runners",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][gate] == "missing", gate

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert set(receipt["release_artifacts"]) == {
        "check_release.py", "release-decision.json", "release-spec.json",
        "release-validation.md",
    }
    for name, expected in receipt["release_artifacts"].items():
        assert sha256(HERE / name) == expected, f"release artifact drifted: {name}"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "Proof.lean", "Validation.lean",
    ):
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    proof_source = code_without_comments_and_strings((HERE / "Proof.lean").read_text())
    validation_source = code_without_comments_and_strings((HERE / "Validation.lean").read_text())
    assert proof_source.count("(satzC : BoundedSatzCTarget") == 2
    assert "(satzC : BoundedSatzCTarget" in validation_source
    assert "theorem konigEdgeColoringTarget_proof" not in proof_source + validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    tool_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/python3").resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"])
    assert TOOLCHAIN == (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()

    outputs = sandboxed_replay(lean, bwrap)
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert printed_axioms(outputs["validation"], DIFFERENTIAL_DECLARATION) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None
    assert tuple(map(int, closure_match.groups())) == (10, 6519, 275)
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    expected_output_hashes = {
        "statement": "6b80a3cfac8567914519f94b1cf01c86a011335f754040101bf75a8cad0d26d6",
        "anchor_audit": "015cf7091d852e2453c600ea0f5d4ab6c5c4785f9707584b32401fcb3a6bec9d",
        "obligation_tree": "fc7ec02361f27f46d5b8f06632424a6acff1bd96a26405190d6a8e3a132ff5db",
        "proof": "18b0409eae4b70ee9d967f1c25f5cab5ac263210447c0571094ccc1ea44e780d",
        "validation": "4931d16d8ccfb0a35c9a7fc233d89ee1250b1f902b78c8b019e2df5df925dd53",
    }
    assert {
        name: hashlib.sha256(output.encode()).hexdigest()
        for name, output in outputs.items()
    } == expected_output_hashes
    assert receipt["result"]["lean_output_sha256"] == expected_output_hashes

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
    assert packet["known_failures"] == decision["known_failures"]
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == SUMMARY_LINES
    assert all(
        set(row) == {"command", "exit_code", "result"}
        and isinstance(row["exit_code"], int)
        and isinstance(row["result"], str)
        and row["result"]
        for row in packet["commands"]
    )
    command_results = {row["command"]: row["exit_code"] for row in packet["commands"]}
    assert command_results[
        f"/usr/bin/python3 -I -B Stage1_Instances/{THEOREM}/check_release.py"
    ] == 0
    assert command_results[
        f"/usr/bin/python3 -O -I -B Stage1_Instances/{THEOREM}/check_release.py"
    ] == 1

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no", "release_grade=false", "M0861-T-SATZ-C",
    ):
        assert fragment in handoff, fragment
    for path in (
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
