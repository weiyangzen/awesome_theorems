#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0760 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0760"
ITEM_ID = "S56-M-0760-INTAKE"
RANK = 1346
BASE_REVISION = "d05520867fab3367a9b61b9544c3e12241204f54"
BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
MATH_SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
CS_SOURCE_BLOB = "0a87065663fa7966305127495f50a61c22e57066"
MATH_RECORD_SHA256 = "454ca6a27b47d5306785d00995df182f23af9cad916e73c744f256b902221c85"
CS_RECORD_SHA256 = "0ef7ac791e88a8d958b84d7212660e24abf0885eb41265f8dd8c690563944c73"
STAGE0_BLOCK_SHA256 = "088c7d51c2069e77b61b437f247c23bdbeb56bab0b3cb9afef270fccc8a99c50"
CS_STAGE0_BLOCK_SHA256 = "ecfa47127e5c22166dd1de6fbf574c86a841a080d516cddcd80647a9b07d54a7"
MANIFEST_ENTRY_SHA256 = "06d38f513b2fd6a4bcbf12631a30c60e4ea702306e37f1d6e2d8d339ae1595aa"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "3f57df84d5d9781f66f1880399a6ca1563c91f63"
LAKE_SYMLINK_TARGET_SHA256 = "e7d8a6bce8b934a5b0dc162324c830c4f26e1146c65bb31e8063491a3f47bfcc"
ROOT_VECTOR = {"H": "H5", "M": "M3", "R": "R4"}
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "validation.md",
}
PRIVATE_REFERENCE = re.compile(
    r"(?:/home/|[.]cron/|slot" + "58|runtime" + " ledger)", re.I
)
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "58f0fe34e1443dd92bc0f587793dcba33c9e03931fa08df3af7d587919537b64",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5279ae201a4642841cd6bda73600a6e979d402e1ef3fe059c226ecd3602cd7e9",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/cs_theorems.md": "32cc0824d326427cc66457b8eaed333a20b82df3269e019d52caa9fb1fccbc1e",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCE_HASHES = {
    "Mathlib/Computability/MyhillNerode.lean": "c5e64f8def4527f5e1049d8fa5949fd004b7356326685931a91043d2983eea5e",
    "Mathlib/Computability/DFA.lean": "d311736c5c10a198822373cddf98947a208f4870758c7148ec4ee3bab6c7d021",
    "Mathlib/Computability/Language.lean": "f4c3964d5713b752c02906354e5366a8367b94804b4dcdac9b07964c36bb8d2e",
}
PROBE_DECLARATIONS = [
    "Language",
    "DFA",
    "Language.IsRegular",
    "Language.leftQuotient",
    "Language.mem_leftQuotient",
    "Language.IsRegular.finite_range_leftQuotient",
    "Language.toDFA",
    "Language.accepts_toDFA",
    "Language.IsRegular.of_finite_range_leftQuotient",
    "Language.isRegular_iff_finite_range_leftQuotient",
]


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def canonical_manifest_entry(target: dict) -> str:
    encoded = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def check_authorities(instance: dict, *, worker_mode: bool) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["scope"]["covered_targets"] == 1546
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "Myhill-Nerode定理",
            "category": "数理逻辑 / 递归论",
            "source_status_untrusted": "已验证",
            "baseline": "L0",
            "rework_required": True,
            "legacy_artifacts_accepted": False,
            "target_lane": "hard_statement_first_partial_verification",
            "intake_score": 86,
            "lifecycle_mode": "planned",
            "theorem_complete": False,
        }
    ]
    target = matches[0]
    assert canonical_manifest_entry(target) == MANIFEST_ENTRY_SHA256
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake["theorem_id"] == THEOREM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] in {"[ ]", "[_]", "[x]"} and intake["depends_on"] == []
    assert isinstance(intake["attempts"], int) and intake["attempts"] >= 0
    if worker_mode:
        assert intake["state"] == "[ ]" and intake["attempts"] == 0
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    assert intake["children"] == []
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "minimal_dfa" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    assert formal["module"] is None
    assert formal["candidate_module"] == "Mathlib.Computability.MyhillNerode"
    assert formal["candidate_declaration"] == (
        "Language.isRegular_iff_finite_range_leftQuotient"
    )
    for field in ("declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[field] is None
    assert "blocked" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "No canonical mathematical or Lean proposition" in instance["status_boundary"]
    assert instance["source_status"].startswith("H5_")

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    assert revisions["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == MATH_SOURCE_BLOB
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/cs_theorems.md") == CS_SOURCE_BLOB
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 5598, 5603) == MATH_RECORD_SHA256
    assert excerpt_sha256(ROOT / "Docs/researches/cs_theorems.md", 233, 233) == CS_RECORD_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 20758, 20783) == STAGE0_BLOCK_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 85150, 85175) == CS_STAGE0_BLOCK_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION
    assert revisions["mathlib_tree"] == MATHLIB_TREE
    assert revisions["mathlib_candidate_origin_commit"] == MATHLIB_ORIGIN
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"stale source hash: {relative}"
    for relative, expected in MATHLIB_SOURCE_HASHES.items():
        assert sha256(mathlib / relative) == expected, f"stale mathlib hash: {relative}"


def check_dag(dag: dict, authority_items: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert dag["accepted_states"] == []
    assert len(dag["tasks"]) == len(TASK_SUFFIXES)
    for index, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES, strict=True), 1):
        task_id = f"S56-M-0760-{suffix}"
        assert task["id"] == task_id and task["layer"] == index
        expected_dependency = ITEM_ID if index == 1 else dag["tasks"][index - 2]["id"]
        assert task["depends_on"] == [expected_dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        authority = next(row for row in authority_items if row["id"] == task_id)
        for field in ("phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field]


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["covered_task_ids"] == [ITEM_ID]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
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
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"] == (
        "master acceptance of the provisional self-tested intake receipt"
    )
    assert "exact source statement identity" in receipt["first_failed_theorem_gate"]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == [
        "Formalizations/Lean/.lake"
    ]
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    lake_target_hash = hashlib.sha256((str(lake.readlink()) + "\n").encode()).hexdigest()
    assert lake_target_hash == receipt["worker_input_hashes"][
        "lake_symlink_target_line_sha256"
    ] == LAKE_SYMLINK_TARGET_SHA256
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()
    }

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    for recipe in recipes:
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
    assert recipes[0]["argv"] == [
        "python3",
        "-B",
        "Stage1_Instances/THM-M-0760/check_intake.py",
    ]
    assert recipes[0]["covered_declarations"] == []
    assert recipes[1]["argv"] == [
        "lake",
        "env",
        "lean",
        "../../Stage1_Instances/THM-M-0760/IntakeProbe.lean",
    ]
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
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected owned artifact inventory: {sorted(actual)}"
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = set(expected_changed) - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(hashes) == expected_hashed
    for relative, expected in hashes.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
        whitespace = subprocess.run(
            ["git", "diff", "--no-index", "--check", "/dev/null", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert whitespace.returncode in {0, 1} and not whitespace.stdout, whitespace.stdout

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in HERE.iterdir()
        if path.is_file() and path.name != "check_intake.py"
    )
    assert not PRIVATE_REFERENCE.search(combined)
    lean = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", lean
    )
    assert not re.search(r"\b(theorem|lemma|example)\b", lean)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authorities = check_authorities(instance, worker_mode=args.worker_packet is not None)
    check_instance(instance)
    check_dag(dag, authorities)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("THM-M-0760 intake self-check: ok (planned H5/M3/R4; no proof credit)")


if __name__ == "__main__":
    main()
