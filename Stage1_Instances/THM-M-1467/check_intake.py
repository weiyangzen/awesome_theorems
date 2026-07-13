#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1467 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1467"
ITEM_ID = "S56-M-1467-INTAKE"
RANK = 1144
BASE_REVISION = "521bd42e5ab5e30513a3c2b7377ea4a1516c0d16"
BASE_TREE = "6f3d9fcf297fe5251a1dc839c1e67930001a86fc"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "statement-blocker.md",
    "task-dag.json",
    "validation.md",
}
TASK_PHASES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
TASK_DELIVERABLES = [
    "Elaborate the exact Lean 4 target with the minimal pinned imports.",
    "Audit mathlib and external Lean 4 candidates at immutable revisions.",
    "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
    "Implement or pin/import the required proof bodies without placeholders.",
    "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "Reconcile evidence and decide the exact theorem-completion verdict.",
]
PROBE_DECLARATIONS = [
    "IsCoercive.continuousLinearEquivOfBilin",
    "IsCoercive.unique_continuousLinearEquivOfBilin",
    "Submodule.orthogonalProjection",
    "Submodule.starProjection_minimal",
    "Polynomial.Chebyshev.T",
    "Polynomial.Chebyshev.integral_eval_T_real_mul_eval_T_real_measureT_of_ne",
    "Polynomial.Chebyshev.sumZeroes",
    "Polynomial.Chebyshev.integral_eq_sumZeroes",
]
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "eccd63e0df13dd5acacd67b5cef26c376189185e8e530adaff0a9d56744f9c1d"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "451bd6661dc5445b0429f55d3131d0c1ded0dd83a3e1f2d5c8e947f72d50976f"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
    "Docs/Blueprint_Guidelines.md": (
        "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535"
    ),
    "Docs/researches/math_theorems.md": (
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29"
    ),
    "Docs/Stage0_Blueprint.md": (
        "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f"
    ),
    "Formalizations/Lean/lean-toolchain": (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    ),
    "Formalizations/Lean/lake-manifest.json": (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    ),
}
MATHLIB_HASHES = {
    "mathlib_lax_milgram_source_sha256": (
        "Mathlib/Analysis/InnerProductSpace/LaxMilgram.lean",
        "79643570d2052a66114e0f87f7b284e2dc72f79638b3c6c962ba18300a9abc6d",
    ),
    "mathlib_projection_source_sha256": (
        "Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean",
        "0457835f43221940112a96509aa2d33386cf1043ef5cc28e54fd609df66c44e4",
    ),
    "mathlib_chebyshev_orthogonality_source_sha256": (
        "Mathlib/Analysis/SpecialFunctions/Trigonometric/Chebyshev/Orthogonality.lean",
        "f9fe36661815f38aaa6469a055ba7944680542be0057d11d6d9d84fc448ad7c0",
    ),
    "mathlib_chebyshev_gauss_source_sha256": (
        "Mathlib/Analysis/SpecialFunctions/Trigonometric/Chebyshev/ChebyshevGauss.lean",
        "b1c9c90e9d3c6c3d3a521f7f5dc7409654ed9aa39be011824cd28e63e5c005fd",
    ),
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode()).hexdigest()


def check_authorities(instance: dict) -> None:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "谱元法",
        "category": "其他重要领域 / 数值分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    assert target["execution_rank"] == instance["execution_rank"]
    assert target["name"] == instance["name_zh"]
    assert target["category"] == instance["category"]

    nodes = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    scoped = sorted(
        (node for node in nodes if node["theorem_id"] == THEOREM_ID),
        key=lambda node: node["layer"],
    )
    assert len(scoped) == 7
    intake = scoped[0]
    assert intake["id"] == ITEM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["execution_rank"] == RANK and instance["intake_score"] == 86
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["source_status_untrusted"] == "已验证"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "does_not_select_a_stable_truth_valued_proposition" in instance[
        "canonical_claim_status"
    ]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert formal["backend"] == "lean4"
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert "does not refute" in instance["status_boundary"]
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-1460",
        "THM-M-1461",
        "THM-M-1462",
        "THM-M-1463",
        "THM-M-1464",
        "THM-M-1468",
    }

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10707, 10712) == (
        revisions["repository_record_excerpt_sha256"]
    ) == "9dea58e986908ddfe99e5146f68c0aac08f80f31aea5645132b7519e97032a22"
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 39892, 39917) == (
        revisions["stage0_projection_excerpt_sha256"]
    ) == "dc00953de5de471decce2f103a760e87536e6f8c57e5cd1e4e1b26d86559512e"
    revision_fields = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
        "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
        "repository_math_source_sha256": "Docs/researches/math_theorems.md",
        "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    }
    for field, path in revision_fields.items():
        assert revisions[field] == SOURCE_HASHES[path]
        assert sha256(ROOT / path) == SOURCE_HASHES[path], f"changed input: {path}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == (
        revisions["mathlib_tree"]
    ) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, (path, expected) in MATHLIB_HASHES.items():
        assert revisions[field] == expected
        assert sha256(mathlib / path) == expected, f"changed pinned mathlib input: {path}"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for literal in (
        "**谱元法**",
        "- 提出者: Anthony Patera",
        "- 时间: 1984",
        "- 陈述: 谱方法与有限元的结合",
    ):
        assert literal in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1467 谱元法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0


def check_task_dag(dag: dict) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6

    authorities = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    authorities = {
        node["id"]: node for node in authorities if node["theorem_id"] == THEOREM_ID
    }
    prior = ITEM_ID
    for layer, (task, phase, deliverable) in enumerate(
        zip(dag["tasks"], TASK_PHASES, TASK_DELIVERABLES), start=1
    ):
        expected_id = f"S56-M-1467-{phase}"
        assert task["id"] == expected_id and task["phase"] == phase.lower()
        assert task["depends_on"] == [prior]
        assert task["state"] == "open" and task["layer"] == layer
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == deliverable
        assert task["completion_gate"] == (
            "rev-5.6 node-specific receipt and master acceptance"
        )
        assert task["evidence_ids"] == []
        authority = authorities[expected_id]
        assert authority["state"] == "[ ]"
        for field in (
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[field] == authority[field]
        prior = expected_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    for key in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["lean_probe_output_sha256"] == (
        "ffb52430462d2a45217887343544d376d5209ea87ff526291ccf00b144b4ab94"
    )
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
    }
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert recipes[0]["env_allowlist"] == {}
    assert recipes[1]["env_allowlist"] == {"LC_ALL": "C", "TZ": "UTC"}
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    assert recipes[0]["covered_declarations"] == []
    assert recipes[1]["covered_declarations"] == PROBE_DECLARATIONS


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_lean_probe(receipt: dict) -> None:
    lean_root = ROOT / "Formalizations/Lean"
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "TZ": "UTC"})
    result = subprocess.run(
        [
            "lake",
            "env",
            "lean",
            "../../Stage1_Instances/THM-M-1467/IntakeProbe.lean",
        ],
        cwd=lean_root,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout.decode(errors="replace")
    assert hashlib.sha256(result.stdout).hexdigest() == receipt[
        "lean_probe_output_sha256"
    ]


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected artifact inventory: {sorted(actual)}"
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "statement-blocker.md",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        forbidden = ("/" + "home/", "." + "cron/", "theorem_complete=" + "true")
        assert all(fragment not in text for fragment in forbidden)
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    for declaration in (
        "IsCoercive.unique_continuousLinearEquivOfBilin",
        "Submodule.starProjection_minimal",
        "Polynomial.Chebyshev.integral_eq_sumZeroes",
    ):
        assert f"#print axioms {declaration}" in probe


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    check_authorities(instance)
    check_instance(instance)
    check_task_dag(dag)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    check_lean_probe(receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-1467 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
