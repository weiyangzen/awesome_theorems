#!/usr/bin/env python3
"""Check structural invariants of the Stage1 assurance standard and generated queue."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
STANDARD = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
QUEUE = ROOT / "Docs" / "Stage1_Blueprint.md"
APPLICABLE = ROOT / "Docs" / "Stage1_Blueprint_Applicable_Theorems.md"
TARGET_MANIFEST = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
EXECUTION_SKILL = ROOT / "skills" / "execute-stage1-rev56" / "SKILL.md"
EXECUTION_TOOL = ROOT / "scripts" / "stage1_target.py"
V2_BLUEPRINT = ROOT / "Docs" / "Stage1_Blueprint_v2.md"
V2_THEOREM_DAG = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
V2_VALIDATOR = ROOT / "Docs" / "tools" / "check_stage1_theorem_dag_v2.py"
V2_LEDGER_TEST = ROOT / "scripts" / "test_stage1_execution_cron.py"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_stage1_blueprint as stage1  # noqa: E402

FEATURE_GROUPS = {
    "lifecycle": ("lifecycle mode", "audit_complete=true", "theorem_complete=false"),
    "statement": ("elaborated_expression_hash", "Lean 4 Statement Gate"),
    "obligations": ("Canonical Obligation Registry", "obligation_registry_hash"),
    "typed_graphs": ("Typed Graph Contract", "proof_requires", "workflow_depends_on"),
    "composition": ("Parent Closure and Composition Certificate",),
    "provenance": ("terminal_proof_body_id", "Formal Candidate and Provenance Audit"),
    "foundation_tcb": ("Lean 4 Trust and Foundation Profile", "TCB profile"),
    "computation": ("certificate_replayed_by_kernel", "experiment_only"),
    "metrics": ("Coverage and Anti-Goodhart Metrics", "minimal open root cut sets"),
    "readability_human": ("Human-Source `H0` Contract", "reader or domain-review receipt"),
    "receipts": ("Evidence Receipt and Bundle Contract", "content-addressed"),
    "reproduction": ("Hermetic Lean 4 Reproduction", "network denied"),
    "independence_ci": ("Independent Verification and CI", "independently implemented verifier"),
    "maintenance": ("Maintenance, Revocation, and Upgrade Rehearsal",),
    "genericity": ("Required Generic Conformance Fixtures", "second materially different prover adapter"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"check_stage1_standard: {message}")


def main() -> None:
    standard = STANDARD.read_text(encoding="utf-8")
    queue = QUEUE.read_text(encoding="utf-8")
    applicable = APPLICABLE.read_text(encoding="utf-8")
    target_manifest = json.loads(TARGET_MANIFEST.read_text(encoding="utf-8"))
    execution_skill = EXECUTION_SKILL.read_text(encoding="utf-8")

    require(V2_BLUEPRINT.is_file(), "v2 orchestration blueprint is missing")
    require(V2_THEOREM_DAG.is_file(), "v2 theorem dependency DAG is missing")
    require(V2_VALIDATOR.is_file(), "v2 theorem DAG validator is missing")
    require(V2_LEDGER_TEST.is_file(), "v2 dependency ledger regression gate is missing")
    v2_blueprint = V2_BLUEPRINT.read_text(encoding="utf-8")
    v2_requirements = (
        "Stage1 v2 Theorem Dependency and Reuse Blueprint",
        "all and only the 1546",
        "direct and transitive parent context",
        "dependency-reuse-ledger.json",
        "stage1-dependency-reuse-ledger/1.1",
        "dependency_context_sha256",
        "shared_lemma_groups",
        "v2_execution_rank",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "[_]",
        "[x]",
    )
    require(
        all(needle in v2_blueprint for needle in v2_requirements),
        "v2 orchestration blueprint is missing coverage, reuse, order, or compatibility requirements",
    )

    missing = {
        group: [needle for needle in needles if needle not in standard]
        for group, needles in FEATURE_GROUPS.items()
    }
    missing = {group: needles for group, needles in missing.items() if needles}
    require(not missing, f"missing assurance requirements: {missing}")

    legacy = re.findall(
        r"^- \[([ _xX])\] `(S56-M0387-[A-Z0-9]+)`", standard, re.MULTILINE
    )
    require(len(legacy) == 41, f"expected 41 retained legacy checklist rows, found {len(legacy)}")
    require(len({item_id for _, item_id in legacy}) == 41, "duplicate legacy checklist ids")

    items = re.findall(r"^### S1-M-(\d{3}) / (THM-[^ ]+) ", queue, re.MULTILINE)
    require(len(items) == 300, f"expected 300 generated Stage1 items, found {len(items)}")
    require(
        [int(number) for number, _ in items] == list(range(1, 301)),
        "generated Stage1 item numbering is not contiguous",
    )
    queue_requirements = (
        "canonical Lean 4 target",
        "typed proof/refinement/provenance/trust/workflow graphs",
        "independently implemented minimal verifier",
        "audit 与 theorem completion 分开决定",
    )
    require(
        all(needle in queue for needle in queue_requirements),
        "generated queue does not carry the generalized assurance header",
    )
    skill_requirements = (
        "execute-stage1-rev56",
        "Docs/Stage1_Targets_rev-5.6.json",
        "intake",
        "audit",
        "prove",
        "validate",
        "release",
        "accepted_audit_only",
        "theorem_complete",
        "first_failed_gate",
        "remaining_root_cut_set",
        "Docs/Stage1_Blueprint_v2.md",
        "Docs/Stage1_Theorem_DAG_v2.json",
        "dependency-reuse-ledger.json",
        "stage1-dependency-reuse-ledger/1.1",
        "dependency_context_sha256",
        "transitive ancestors",
        "v2_execution_rank",
    )
    require(
        all(needle in execution_skill for needle in skill_requirements),
        "execution skill is missing required intents, verdicts, or handoff fields",
    )
    require(EXECUTION_TOOL.is_file(), "deterministic Stage1 target inspection tool is missing")
    target_rows = re.findall(
        r"^\| (\d+) \| (S1-M-\d{3}|-) \| `(THM-M-\d{4})` \|", applicable, re.MULTILINE
    )
    applicable_items = [theorem_id for _, _, theorem_id in target_rows]
    require(len(applicable_items) == 1546, "covered target list must contain exactly 1546 rows")
    require(len(set(applicable_items)) == 1546, "covered target list contains duplicate theorem ids")
    require(
        [int(rank) for rank, _, _ in target_rows] == list(range(1, 1547)),
        "covered target execution ranks are not contiguous from 1 through 1546",
    )
    all_items, _ = stage1.load_stage0_items()
    expected_items = [item for item in all_items if stage1.is_stage1_eligible(item)]
    expected_ids = {item.uid for item in expected_items}
    require(
        set(applicable_items) == expected_ids,
        "covered target IDs disagree with the Stage1 eligibility predicate",
    )
    target_set_payload = "\n".join(sorted(expected_ids)) + "\n"
    expected_hash = hashlib.sha256(target_set_payload.encode("utf-8")).hexdigest()
    require(
        f"Canonical sorted target-ID set SHA-256: `{expected_hash}`" in applicable,
        "covered target-set digest is missing or stale",
    )
    require(
        target_manifest.get("schema_version") == "stage1-target-set/5.6.2",
        "target manifest schema version is missing or stale",
    )
    manifest_targets = target_manifest.get("targets")
    require(isinstance(manifest_targets, list), "target manifest targets must be a list")
    require(len(manifest_targets) == 1546, "target manifest must contain exactly 1546 targets")
    require(
        [target.get("execution_rank") for target in manifest_targets] == list(range(1, 1547)),
        "target manifest execution ranks are not contiguous",
    )
    require(
        [target.get("theorem_id") for target in manifest_targets] == applicable_items,
        "target manifest and Markdown projection disagree on ordered target IDs",
    )
    require(
        all(target.get("theorem_complete") is False for target in manifest_targets),
        "generated target manifest must not manufacture theorem completion",
    )
    require(
        all(
            target.get("baseline") == "L0"
            and target.get("rework_required") is True
            and target.get("legacy_artifacts_accepted") is False
            and "assurance_level" not in target
            and "priority_slot" not in target
            for target in manifest_targets
        ),
        "all targets must share the L0 rework baseline without inherited assurance",
    )
    manifest_scope = target_manifest.get("scope", {})
    require(manifest_scope.get("covered_targets") == 1546, "manifest covered-target count is stale")
    require(manifest_scope.get("excluded_mathematics_records") == 55, "manifest exclusion count is stale")
    require(manifest_scope.get("uniform_l0_targets") == 1546, "uniform L0 count is stale")
    require(
        manifest_scope.get("canonical_sorted_target_id_set_sha256") == expected_hash,
        "target manifest ID-set digest is stale",
    )
    require(
        "all and only the `1546` covered theorem IDs" in applicable,
        "covered target list does not declare its closed 1546-ID scope",
    )
    require(
        "The 55 non-eligible mathematical records are not covered" in applicable,
        "covered target list does not fail closed on the 55 exclusions",
    )
    selected_rows = re.findall(
        r"^\| \d+ \| S1-M-(\d{3}) \| `(THM-M-\d{4})` \|", applicable, re.MULTILINE
    )
    require(len(selected_rows) == 300, "full mathematical list must identify 300 priority slots")
    require(
        sorted(selected_rows, key=lambda row: int(row[0])) == items,
        "priority slots in full list disagree with generated queue",
    )
    v2_check = subprocess.run(
        [sys.executable, str(V2_VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(
        v2_check.returncode == 0,
        "v2 theorem DAG validator failed: " + (v2_check.stderr or v2_check.stdout).strip(),
    )
    ledger_check = subprocess.run(
        [sys.executable, "-m", "unittest", "scripts/test_stage1_execution_cron.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(
        ledger_check.returncode == 0,
        "v2 dependency ledger regression gate failed: "
        + (ledger_check.stderr or ledger_check.stdout).strip(),
    )

    print(
        "check_stage1_standard: ok "
        f"({len(FEATURE_GROUPS)} assurance groups, 41 legacy rows, "
        "300 legacy slots, 1546 uniform-L0 Lean 4 targets, v2 theorem DAG, execution skill present)"
    )


if __name__ == "__main__":
    main()
