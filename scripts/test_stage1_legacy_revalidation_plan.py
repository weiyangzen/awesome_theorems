#!/usr/bin/env python3
"""Tests for the read-only Stage1 legacy revalidation planning lane."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage1_legacy_migration_inventory as inventory  # noqa: E402
import stage1_legacy_revalidation_plan as planner  # noqa: E402


def run(root: Path, *argv: str) -> str:
    result = subprocess.run(
        argv,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(argv)}\n{result.stderr}"
        )
    return result.stdout.strip()


def contract() -> dict[str, object]:
    return {
        "schema_version": "stage1-phase-acceptance-contracts/1.0",
        "task_state_authority": planner.BLUEPRINT_PATH,
        "phase_order": list(planner.PHASES),
        "state_protocol": {
            "worker_self_tested": "[_]",
            "master_accepted": "[x]",
        },
        "phases": [
            {
                "phase": phase,
                "item_suffix": planner.PHASE_SUFFIXES[phase],
                "required_artifact_roles": [
                    {
                        "role": "phase_receipt",
                        "requirement": "required",
                        "cardinality": "exactly_one",
                        "resolution": "path_candidates",
                        "path_candidates": [
                            "Stage1_Instances/{theorem_id}/missing-receipt.json"
                        ],
                    }
                ],
                "phase_receipt_required_fields": [],
                "validator_authorities": [],
                "superseded_validator_sources": [],
            }
            for phase in planner.PHASES
        ],
    }


class Fixture:
    def __init__(self, *, tracked_contract: bool = True) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        run(self.root, "git", "init", "-q", "-b", "main")
        run(self.root, "git", "config", "user.name", "Plan Tests")
        run(self.root, "git", "config", "user.email", "plan@example.invalid")
        docs = self.root / "Docs"
        docs.mkdir()
        self.contract_path = docs / "Stage1_Phase_Acceptance_Contracts.json"
        self.contract_path.write_text(json.dumps(contract()) + "\n", encoding="utf-8")

        self.theorems: list[dict[str, object]] = []
        checklist: list[str] = [planner.CHECKLIST_BEGIN]
        for rank in range(1, 10):
            theorem_id = f"THM-M-{rank:04d}"
            states = {
                phase: ("[_]" if not (rank == 4 and phase == "release") else "[ ]")
                for phase in planner.PHASES
            }
            attempts = {phase: int(states[phase] == "[_]") for phase in planner.PHASES}
            context = hashlib.sha256(f"context:{theorem_id}".encode()).hexdigest()
            self.theorems.append(
                {
                    "theorem_id": theorem_id,
                    "v2_execution_rank": rank,
                    "phase_states": states,
                    "phase_attempts": attempts,
                    "dependency_context_sha256": context,
                }
            )
            for phase in planner.PHASES:
                item_id = (
                    f"S56-{theorem_id.removeprefix('THM-')}-"
                    f"{planner.PHASE_SUFFIXES[phase]}"
                )
                checklist.append(
                    f"- {states[phase]} `{item_id}` / `{theorem_id}` / `{phase}`: "
                    f"fixture {{attempts={attempts[phase]}}}"
                )
        checklist.append(planner.CHECKLIST_END)
        self.blueprint_path = docs / "Stage1_Blueprint_v2.md"
        self.blueprint_path.write_text("\n".join(checklist) + "\n", encoding="utf-8")

        blueprint_sha = hashlib.sha256(self.blueprint_path.read_bytes()).hexdigest()
        state_counts = Counter(
            state
            for theorem in self.theorems
            for state in theorem["phase_states"].values()  # type: ignore[union-attr]
        )
        theorem_dag = {
            "schema_version": "stage1-theorem-dag/2.0",
            "requirements_source": planner.BLUEPRINT_PATH,
            "blueprint_state_snapshot": {
                "authoritative_blueprint": planner.BLUEPRINT_PATH,
                "authoritative_blueprint_sha256": blueprint_sha,
                "item_count": sum(state_counts.values()),
                "item_state_counts": dict(sorted(state_counts.items())),
            },
            "theorems": self.theorems,
        }
        self.dag_path = docs / "Stage1_Theorem_DAG_v2.json"
        self.dag_path.write_text(json.dumps(theorem_dag) + "\n", encoding="utf-8")
        run(self.root, "git", "add", ".")
        if not tracked_contract:
            run(
                self.root,
                "git",
                "reset",
                "-q",
                "Docs/Stage1_Phase_Acceptance_Contracts.json",
            )
        run(self.root, "git", "commit", "-qm", "fixture")
        self.inventory_path = self.root.parent / f"{self.root.name}-inventory.json"
        self.write_inventory(
            candidate_contract=self.contract_path if not tracked_contract else None
        )

    def write_inventory(self, *, candidate_contract: Path | None = None) -> None:
        value = inventory.build_inventory(
            self.root, candidate_contract=candidate_contract
        )
        self.inventory_path.write_text(json.dumps(value) + "\n", encoding="utf-8")

    def load_inventory(self) -> dict[str, object]:
        return json.loads(self.inventory_path.read_text(encoding="utf-8"))

    def store_inventory(self, value: dict[str, object]) -> None:
        self.inventory_path.write_text(json.dumps(value) + "\n", encoding="utf-8")

    def close(self) -> None:
        self.inventory_path.unlink(missing_ok=True)
        self.temp.cleanup()


class RevalidationPlanTests(unittest.TestCase):
    def test_head_owned_contract_is_required_by_default(self) -> None:
        fixture = Fixture(tracked_contract=False)
        self.addCleanup(fixture.close)
        with self.assertRaisesRegex(planner.PlanError, "not tracked"):
            planner.build_plan(fixture.root, fixture.inventory_path)

    def test_candidate_contract_is_explicit_non_authoritative_preflight(self) -> None:
        fixture = Fixture(tracked_contract=False)
        self.addCleanup(fixture.close)
        plan = planner.build_plan(
            fixture.root,
            fixture.inventory_path,
            candidate_contract=fixture.contract_path,
        )
        self.assertEqual(plan["authority_mode"], "candidate_preflight")
        self.assertFalse(plan["head_owned_contract"])
        self.assertFalse(plan["authoritative_for_acceptance"])
        self.assertEqual(plan["state_transition"], "none")

    def test_stratifies_all_phases_and_uses_canonical_order(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        plan = planner.build_plan(fixture.root, fixture.inventory_path)
        self.assertEqual(planner.MAX_SAMPLES, 50)
        self.assertEqual(plan["selected_item_count"], planner.MAX_SAMPLES)
        self.assertEqual(plan["selection_policy"]["hard_max_samples"], 50)
        self.assertEqual(plan["selection_policy"]["requested_limit"], 50)
        self.assertEqual(
            plan["selected_phase_counts"],
            {
                "intake": 8,
                "statement": 7,
                "anchor_audit": 7,
                "obligation_tree": 7,
                "proof": 7,
                "validation": 7,
                "release": 7,
            },
        )
        keys = [
            (lane["phase_layer"], lane["v2_execution_rank"], lane["item_id"])
            for lane in plan["lanes"]
        ]
        self.assertEqual(keys, sorted(keys))
        self.assertTrue(all(lane["authoritative_state"] == "[_]" for lane in plan["lanes"]))
        self.assertTrue(all("M-0004-RELEASE" not in lane["item_id"] for lane in plan["lanes"]))

    def test_lanes_require_fresh_evidence_and_never_promote(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        plan = planner.build_plan(fixture.root, fixture.inventory_path, limit=7)
        self.assertEqual(plan["required_steps"], list(planner.REQUIRED_STEPS))
        self.assertFalse(plan["executes_validators"])
        self.assertFalse(plan["launches_workers"])
        self.assertFalse(plan["mutates_repository"])
        self.assertFalse(plan["writes_ssot"])
        for lane in plan["lanes"]:
            self.assertEqual(lane["required_steps"], list(planner.REQUIRED_STEPS))
            self.assertEqual(
                lane["step_outcomes"],
                {step: "unknown" for step in planner.REQUIRED_STEPS},
            )
            self.assertEqual(lane["state_transition"], "none")
            self.assertFalse(lane["acceptance_claimed"])
            self.assertFalse(lane["promotes_to_master_accepted"])

    def test_required_items_are_included_without_exceeding_the_plan_bound(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        required = "S56-M-0009-RELEASE"
        default_ids = {
            lane["item_id"]
            for lane in planner.build_plan(
                fixture.root, fixture.inventory_path
            )["lanes"]
        }
        self.assertNotIn(required, default_ids)
        plan = planner.build_plan(
            fixture.root,
            fixture.inventory_path,
            required_item_ids=[required],
        )
        self.assertEqual(plan["selected_item_count"], planner.MAX_SAMPLES)
        self.assertEqual(plan["required_item_ids"], [required])
        self.assertIn(required, {lane["item_id"] for lane in plan["lanes"]})

    def test_required_items_must_be_unique_authoritative_rows_within_limit(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        required = "S56-M-0009-RELEASE"
        for required_ids, message in (
            ([required, required], "malformed, duplicated"),
            (["S56-M-0004-RELEASE"], "not an authoritative"),
            (["S56-M-0008-RELEASE", required], "exceed the plan limit"),
        ):
            with self.subTest(required_ids=required_ids), self.assertRaisesRegex(
                planner.PlanError, message
            ):
                planner.build_plan(
                    fixture.root,
                    fixture.inventory_path,
                    limit=1 if message == "exceed the plan limit" else 50,
                    required_item_ids=required_ids,
                )

    def test_plan_and_lane_digests_are_recomputable_and_deterministic(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        first = planner.build_plan(fixture.root, fixture.inventory_path)
        second = planner.build_plan(fixture.root, fixture.inventory_path)
        self.assertEqual(first, second)
        for original in first["lanes"]:
            lane = dict(original)
            claimed = lane.pop("lane_sha256")
            self.assertEqual(
                claimed, inventory.sha256_bytes(inventory.canonical_json(lane))
            )
        unsigned = dict(first)
        claimed = unsigned.pop("plan_sha256")
        self.assertEqual(
            claimed, inventory.sha256_bytes(inventory.canonical_json(unsigned))
        )

    def test_build_is_read_only_for_authorities_and_runtime_state(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        runtime = fixture.root / ".cron" / "stage1-v2-app-server"
        runtime.mkdir(parents=True)
        protected = {
            fixture.blueprint_path: fixture.blueprint_path.read_bytes(),
            fixture.dag_path: fixture.dag_path.read_bytes(),
            fixture.contract_path: fixture.contract_path.read_bytes(),
            runtime / "claims.json": b'{"claims":["sentinel"]}\n',
            runtime / "PAUSED": b"sentinel-pause\n",
            fixture.root / "todos_20990101.md": b"sentinel todo\n",
        }
        for path, data in protected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        planner.build_plan(fixture.root, fixture.inventory_path)
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        self.assertEqual(before, after)

    def test_tampered_inventory_or_item_digest_fails_closed(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        value = fixture.load_inventory()
        value["items"][0]["attempts"] = 99  # type: ignore[index]
        fixture.store_inventory(value)
        with self.assertRaisesRegex(planner.PlanError, "does not bind its content"):
            planner.build_plan(fixture.root, fixture.inventory_path)

        fixture.write_inventory()
        value = fixture.load_inventory()
        item = value["items"][0]  # type: ignore[index]
        item["attempts"] = 99  # type: ignore[index]
        unsigned_item = dict(item)  # type: ignore[arg-type]
        unsigned_item.pop("item_sha256")
        item["item_sha256"] = inventory.sha256_bytes(  # type: ignore[index]
            inventory.canonical_json(unsigned_item)
        )
        unsigned_inventory = dict(value)
        unsigned_inventory.pop("inventory_sha256")
        value["inventory_sha256"] = inventory.sha256_bytes(
            inventory.canonical_json(unsigned_inventory)
        )
        fixture.store_inventory(value)
        with self.assertRaisesRegex(planner.PlanError, "inconsistent attempts"):
            planner.build_plan(fixture.root, fixture.inventory_path)

    def test_stale_theorem_dag_projection_fails_closed(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        dag = json.loads(fixture.dag_path.read_text(encoding="utf-8"))
        dag["theorems"][0]["phase_states"]["proof"] = "[x]"
        fixture.dag_path.write_text(json.dumps(dag) + "\n", encoding="utf-8")
        run(
            fixture.root,
            "git",
            "add",
            "Docs/Stage1_Theorem_DAG_v2.json",
        )
        run(fixture.root, "git", "commit", "-qm", "stale projection")
        fixture.write_inventory()
        with self.assertRaisesRegex(planner.PlanError, "does not exactly project"):
            planner.build_plan(fixture.root, fixture.inventory_path)

    def test_limit_is_bounded_and_output_inside_repo_is_rejected(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        with self.assertRaisesRegex(planner.PlanError, "between 1 and 50"):
            planner.build_plan(fixture.root, fixture.inventory_path, limit=51)
        with self.assertRaisesRegex(planner.PlanError, "outside the repository"):
            planner._write_external_output(
                fixture.root, fixture.root / "plan.json", b"{}\n"
            )


if __name__ == "__main__":
    unittest.main()
