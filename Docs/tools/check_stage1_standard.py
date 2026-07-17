#!/usr/bin/env python3
"""Check the Stage1 assurance standard, target manifest, and sole blueprint."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
STANDARD = ROOT / "Docs" / "Stage1_Assurance_Standard_rev-5.6.md"
TARGET_MANIFEST = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
EXECUTION_SKILL = ROOT / "skills" / "execute-stage1-rev56" / "SKILL.md"
EXECUTION_TOOL = ROOT / "scripts" / "stage1_target.py"
V2_BLUEPRINT = ROOT / "Docs" / "Stage1_Blueprint_v2.md"
V2_THEOREM_DAG = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
V2_VALIDATOR = ROOT / "Docs" / "tools" / "check_stage1_theorem_dag_v2.py"
V2_LEDGER_TEST = ROOT / "scripts" / "test_stage1_execution_cron.py"
PHASE_ACCEPTANCE_CONTRACT = ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json"
PHASE_ACCEPTANCE_VALIDATOR = (
    ROOT / "Docs" / "tools" / "check_stage1_phase_acceptance_contracts.py"
)
CHECKLIST_SHA256 = "8ffdc57f4002d3e70a7c53984b441ab22bec9a1ecf7141fe740e94608db9fe62"

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
    target_manifest = json.loads(TARGET_MANIFEST.read_text(encoding="utf-8"))
    execution_skill = EXECUTION_SKILL.read_text(encoding="utf-8")

    require(V2_BLUEPRINT.is_file(), "v2 orchestration blueprint is missing")
    require(V2_THEOREM_DAG.is_file(), "v2 theorem dependency DAG is missing")
    require(V2_VALIDATOR.is_file(), "v2 theorem DAG validator is missing")
    require(V2_LEDGER_TEST.is_file(), "v2 dependency ledger regression gate is missing")
    require(PHASE_ACCEPTANCE_CONTRACT.is_file(), "phase acceptance contract is missing")
    require(PHASE_ACCEPTANCE_VALIDATOR.is_file(), "phase acceptance contract validator is missing")
    tracked_blueprints = subprocess.check_output(
        ["git", "ls-files", "Docs/Stage1_Blueprint*.md"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    require(
        tracked_blueprints == ["Docs/Stage1_Blueprint_v2.md"],
        "Docs must track exactly one Stage1 blueprint: Docs/Stage1_Blueprint_v2.md; "
        f"found {tracked_blueprints}",
    )
    physical_blueprints = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "Docs").glob("Stage1_Blueprint*.md")
        if path.is_file()
    )
    require(
        physical_blueprints == ["Docs/Stage1_Blueprint_v2.md"],
        "Docs must contain exactly one physical Stage1 blueprint: "
        "Docs/Stage1_Blueprint_v2.md; "
        f"found {physical_blueprints}",
    )
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
        "Requirements and phase-state SSOT",
        "STAGE1-EXECUTION-CHECKLIST:BEGIN",
        "[_]",
        "[x]",
    )
    require(
        all(needle in v2_blueprint for needle in v2_requirements),
        "v2 orchestration blueprint is missing coverage, reuse, order, or compatibility requirements",
    )
    v2_states = re.findall(
        r"^- (\[[_x ]\]) `(S56-M-\d{4}-(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE))`"
        r" / `THM-M-\d{4}` / `[a-z_]+`: .+ \{attempts=\d+\}$",
        v2_blueprint,
        re.MULTILINE,
    )
    require(len(v2_states) == 10822, "v2 SSOT must contain exactly 10822 phase-state rows")
    require(len({item_id for _, item_id in v2_states}) == 10822, "v2 SSOT contains duplicate phase IDs")
    checklist_begin = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
    checklist_end = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
    require(
        v2_blueprint.count(checklist_begin) == 1 and v2_blueprint.count(checklist_end) == 1,
        "v2 SSOT must contain exactly one checklist marker pair",
    )
    checklist_body = v2_blueprint.split(checklist_begin, 1)[1].split(checklist_end, 1)[0]
    require(
        hashlib.sha256(checklist_body.encode("utf-8")).hexdigest() == CHECKLIST_SHA256,
        "v2 SSOT checklist body differs from the frozen 7521/3300/1 migration cursor",
    )
    state_counts = {state: sum(row_state == state for row_state, _ in v2_states) for state in ("[ ]", "[_]", "[x]")}
    require(
        state_counts == {"[ ]": 7521, "[_]": 3300, "[x]": 1},
        f"v2 SSOT checklist counts changed: {state_counts}",
    )
    require(
        "STAGE1-EXECUTION-CHECKLIST:BEGIN" not in standard
        and not re.search(r"^[-] \[[_x ]\] `S56-M-\d{4}-(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE)`", standard, re.MULTILINE),
        "rev-5.6 assurance blueprint must not retain a second live phase-state checklist",
    )

    missing = {
        group: [needle for needle in needles if needle not in standard]
        for group, needles in FEATURE_GROUPS.items()
    }
    missing = {group: needles for group, needles in missing.items() if needles}
    require(not missing, f"missing assurance requirements: {missing}")

    legacy = re.findall(
        r"^- Historically (checked|open): `(S56-M0387-[A-Z0-9]+)`",
        standard,
        re.MULTILINE | re.IGNORECASE,
    )
    require(len(legacy) == 41, f"expected 41 retained historical rows, found {len(legacy)}")
    require(len({item_id for _, item_id in legacy}) == 41, "duplicate historical record ids")
    require(
        not re.search(r"^- \[[ _xX]\] `S56-M0387-", standard, re.MULTILINE),
        "assurance standard must not contain a competing checkbox cursor",
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
    all_items, _ = stage1.load_stage0_items()
    expected_items = [item for item in all_items if stage1.is_stage1_eligible(item)]
    expected_ids = {item.uid for item in expected_items}
    require(
        {target.get("theorem_id") for target in target_manifest.get("targets", [])}
        == expected_ids,
        "target manifest IDs disagree with the Stage1 eligibility predicate",
    )
    target_set_payload = "\n".join(sorted(expected_ids)) + "\n"
    expected_hash = hashlib.sha256(target_set_payload.encode("utf-8")).hexdigest()
    require(
        target_manifest.get("schema_version") == "stage1-target-set/5.6.2",
        "target manifest schema version is missing or stale",
    )
    require(
        target_manifest.get("standard") == "Docs/Stage1_Assurance_Standard_rev-5.6.md",
        "target manifest assurance-standard reference is stale",
    )
    require(
        target_manifest.get("task_state_authority") == "Docs/Stage1_Blueprint_v2.md",
        "target manifest task-state authority is stale",
    )
    require(
        "generated_projection" not in target_manifest,
        "target manifest must not name a retired Markdown projection",
    )
    manifest_targets = target_manifest.get("targets")
    require(isinstance(manifest_targets, list), "target manifest targets must be a list")
    require(len(manifest_targets) == 1546, "target manifest must contain exactly 1546 targets")
    require(
        [target.get("execution_rank") for target in manifest_targets] == list(range(1, 1547)),
        "target manifest execution ranks are not contiguous",
    )
    require(
        len({target.get("theorem_id") for target in manifest_targets}) == 1546,
        "target manifest contains duplicate theorem IDs",
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
    selected_rows = [
        (target.get("legacy_priority_slot"), target.get("theorem_id"))
        for target in manifest_targets
        if target.get("legacy_priority_slot") is not None
    ]
    require(len(selected_rows) == 300, "target manifest must identify 300 legacy priority slots")
    require(
        [slot for slot, _ in selected_rows] == [f"S1-M-{rank:03d}" for rank in range(1, 301)],
        "target manifest legacy priority slots are not contiguous",
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
    phase_acceptance_check = subprocess.run(
        [sys.executable, str(PHASE_ACCEPTANCE_VALIDATOR)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    require(
        phase_acceptance_check.returncode == 0,
        "phase acceptance contract validator failed: "
        + (phase_acceptance_check.stderr or phase_acceptance_check.stdout).strip(),
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
        f"({len(FEATURE_GROUPS)} assurance groups, 41 historical non-checkbox rows, "
        "300 legacy slots in the manifest, 1546 uniform-L0 Lean 4 targets, sole v2 blueprint, "
        "seven-phase acceptance contract, execution skill present)"
    )


if __name__ == "__main__":
    main()
