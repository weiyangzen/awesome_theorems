#!/usr/bin/env python3
"""Tests for the read-only Stage5.1 activation fence."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_1_activation_fence.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("stage5_1_activation_fence_tests_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def seal(value: dict) -> dict:
    value = dict(value)
    value["authority_sha256"] = hashlib.sha256(checker._canonical(value)).hexdigest()
    return value


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def reseal_json(path: Path, mutate) -> None:
    value = json.loads(path.read_text())
    value.pop("authority_sha256", None)
    mutate(value)
    write_json(path, seal(value))


def blueprint(program: str, *, boot: str = " ") -> str:
    title = "Theorems" if program == "theorems" else "Conjectures"
    prefix = "S51THM" if program == "theorems" else "S51CON"
    prompt = f"Docs/evidence/stage5_1_{program}/operator-concurrency-prompt.json"
    runtime = f".ops/stage5-1-{program}-execution-v1"
    marker = program.upper()
    specification = {
        "program": program,
        "activation_state": "materialized_unaccepted_missing_concurrency_prompt",
        "concurrency_prompt_contract": {
            "required_dimensions": sorted(checker.CONCURRENCY_FIELDS),
            "required_policy_fields": sorted(checker.PROMPT_POLICY_FIELDS),
            "required_replacement_policy_fields": sorted(checker.REPLACEMENT_POLICY_FIELDS),
            "required_prompt_fields": sorted(
                checker.AUTHORITY_PROMPT_FIELDS | checker.ROUTE_FIELDS
                | checker.PROMPT_POLICY_FIELDS | {"schema_version", "concurrency"}
            ),
            "required_route_fields": sorted(checker.ROUTE_FIELDS),
            "required_authority_fields": sorted(checker.AUTHORITY_PROMPT_FIELDS),
            "value_source": "explicit_execution_prompt_only",
            "missing_policy": "fail_closed_before_reservation_or_launch",
            "defaults_forbidden": True,
            "prompt_path": prompt,
        },
        "activation_contract": {
            "runtime_root": runtime,
            "controller_path": f"scripts/stage5_1_{program}_execution_cron.py",
            "cron_marker_begin": f"# BEGIN AWESOME_THEOREMS_STAGE5_1_{marker}_EXECUTION_V1",
            "cron_marker_end": f"# END AWESOME_THEOREMS_STAGE5_1_{marker}_EXECUTION_V1",
            "prompt_path": prompt,
            "predecessor_fence_receipt_path": str(checker.PREDECESSOR_FENCE_RECEIPT),
            "required_side_effect_absence": [
                "runtime_root", "claims", "reservations", "task_roots", "tmux_sockets",
                "processes", "request_leases", "turn_leases", "requests", "cron_marker",
            ],
        },
    }
    return (
        f"# Stage5.1 {title} Blueprint\n\n"
        "```json\n" + json.dumps(specification, sort_keys=True, indent=2) + "\n```\n\n"
        f"- [{boot}] `{prefix}-BOOT-001` new BOOT | depends_on=- | owned_paths=- | gate=new review\n"
        f"- [ ] `{prefix}-00000001-TARGET` member | depends_on={prefix}-BOOT-001 | owned_paths=x | gate=member\n"
    )


def prompt(program: str) -> dict:
    vector = {field: 1 for field in checker.CONCURRENCY_FIELDS}
    vector["service_records"] = "not_applicable"
    vector["exact_path_conflicts"] = 0
    return seal({
        "schema_version": "awesome-theorems/stage5.1-concurrency-prompt/1.0",
        "program": program,
        "policy_epoch": f"stage5.1-{program}-fixture-current-operator",
        "source": "explicit current operator prompt; defaults forbidden; inheritance forbidden",
        "concurrency": vector,
        "request_window_seconds": 60,
        "lifecycle_mode": "bounded",
        "replacement_policy": {
            "replacement_limit": 2,
            "startup_deadline_seconds": 60,
            "tick_time_budget_seconds": 120,
        },
        "route": "fixture-provider-route",
        "model": "fixture-model",
        "reasoning_effort": "fixture-effort",
        "service_tier": "fixture-tier",
    })


def make_fixture(root: Path, *, prompts: bool = True, boots: bool = False,
                 state: bool = False, queues: bool = False,
                 predecessor_receipt: bool = True,
                 activation_receipt: bool | None = None) -> None:
    (root / "Docs/tools").mkdir(parents=True, exist_ok=True)
    # evaluate() imports this interface; the fixture keeps release semantics out
    # of lifecycle-focused unit tests.
    (root / "Docs/tools/check_stage5_1_organization_release.py").write_text(
        "def audit_release(root, release, rebuild=True, cursor_mode='initial_blank', activation_receipt=None):\n"
        "    assert rebuild is True\n"
        "    return {'members': 19790, 'legacy_rows': 20197, 'subjects': 1, 'relations': 0, 'hard_edges': 0}\n"
    )
    (root / "Docs/tools/check_stage5_1_activation_fence.py").write_bytes(
        CHECKER_PATH.read_bytes()
    )
    for program in checker.PROGRAMS:
        controller = root / f"scripts/stage5_1_{program}_execution_cron.py"
        controller.parent.mkdir(parents=True, exist_ok=True)
        controller.write_text("# fixture successor controller\n")
    write_json(root / "Docs/catalog/v5/Current_Release.json", seal({
        "schema_version": "awesome-theorems/stage5-current-release/5.6",
        "release": "5.6",
        "manifest_path": "releases/5.6/Release_Manifest.json",
        "manifest_sha256": "0" * 64,
        "release_root_sha256": "1" * 64,
    }))
    bp_rows = []
    for program in checker.PROGRAMS:
        bp_path = root / checker.PROGRAMS[program]["blueprint"]
        bp_path.parent.mkdir(parents=True, exist_ok=True)
        initial_raw = blueprint(program, boot=" ").encode()
        raw = blueprint(program, boot="x" if boots else " ").encode()
        bp_path.write_bytes(raw)
        gantt_path = bp_path.with_name(bp_path.name.replace("_Blueprint.md", "_Gantt.md"))
        gantt_path.write_text(
            f"| Item ID | Title | State |\n|---|---|---|\n"
            f"| `{'S51THM' if program == 'theorems' else 'S51CON'}-BOOT-001` | BOOT | "
            f"{'master_accepted' if boots else 'not_done'} |\n"
        )
        bp_rows.append({
            "path": bp_path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(initial_raw).hexdigest(),
            "gantt_path": gantt_path.relative_to(root).as_posix(),
            "gantt_sha256": hashlib.sha256(gantt_path.read_bytes()).hexdigest(),
        })
        if prompts:
            write_json(
                root / f"Docs/evidence/stage5_1_{program}/operator-concurrency-prompt.json",
                prompt(program),
            )
    manifest_path = root / "Docs/catalog/stage5_1_organization/releases/1.0/Organization_Manifest.json"
    manifest = seal({
        "schema_version": "awesome-theorems/stage5_1-organization/manifest/1.0",
        "organization_release": "1.0", "blueprint_revision": "Stage5.1",
        "base_catalog_release": "5.6", "not_catalog_release_5_1": True,
        "activation": {
            "status": "blocked",
            "requires_explicit_operator_concurrency_prompt": True,
            "concurrency_defaults_present": False,
            "fence_receipt_path": str(checker.FENCE_RECEIPT),
            "preconditions": [
                "predecessor_admission_stopped", "predecessor_handoffs_dispositioned",
                "predecessor_live_generations_zero", "predecessor_cron_markers_absent",
                "stage51_boot_accepted", "complete_current_operator_concurrency_prompt_accepted",
            ],
        },
    })
    write_json(manifest_path, manifest)
    pointer = seal({
        "schema_version": "awesome-theorems/stage5_1-organization/current-release/1.0",
        "organization_release": "1.0", "base_catalog_release": "5.6",
        "blueprint_revision": "Stage5.1", "not_catalog_release_5_1": True,
        "manifest": {
            "path": manifest_path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "authority_sha256": manifest["authority_sha256"],
        },
        "blueprints": dict(zip(checker.PROGRAMS, bp_rows)),
        "migration": {"path": "Docs/catalog/stage5_1_organization/migrations/fixture.json",
                      "sha256": "2" * 64, "authority_sha256": "3" * 64},
        "activation": {"status": "blocked", "reason_codes": ["fixture_blocked"]},
    })
    write_json(root / checker.CURRENT, pointer)
    for program, policy in checker.PROGRAMS.items():
        write_json(root / policy["runtime"] / "state/controller-state.json", seal({
            "claims": {}, "reservations": [], "schema_version": f"fixture-{program}",
        }))
    if queues:
        for program, policy in checker.PROGRAMS.items():
            q = root / policy["runtime"] / "integration/pending.json"
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text("{}\n")
    if predecessor_receipt:
        predecessor = seal({
            "schema_version": "awesome-theorems/stage5-1-predecessor-fence/1.0",
            "organization_release": "1.0", "status": "accepted",
            "evidence_as_of": "2026-08-21T09:00:00Z",
            "manifest_sha256": pointer["manifest"]["sha256"],
            "crontab_sha256": hashlib.sha256(b"").hexdigest(),
            "checker": {
                "path": "Docs/tools/check_stage5_1_activation_fence.py",
                "sha256": hashlib.sha256(
                    (root / "Docs/tools/check_stage5_1_activation_fence.py").read_bytes()
                ).hexdigest(),
            },
            "reviewer_id": "fixture-independent-reviewer",
            "review_receipt_sha256": "9" * 64,
            "prompt_digests": {
                program: hashlib.sha256(
                    (root / f"Docs/evidence/stage5_1_{program}/operator-concurrency-prompt.json").read_bytes()
                ).hexdigest() if prompts else "0" * 64
                for program in checker.PROGRAMS
            },
            "predecessors": {
                program: {
                    "runtime_root": str(policy["runtime"]),
                    "state_sha256": hashlib.sha256(
                        (root / policy["runtime"] / "state/controller-state.json").read_bytes()
                    ).hexdigest(),
                    "admission_fenced": True, "live_generations_zero": True,
                    "reservations_zero": True, "queues_dispositioned": True,
                    "owner_processes_zero": True, "tmux_sockets_zero": True,
                    "leases_released": True,
                    "queue_inventory_sha256": checker._queue_inventory(
                        root, policy["runtime"]
                    )[1],
                }
                for program, policy in checker.PROGRAMS.items()
            },
        })
        predecessor_path = root / checker.PREDECESSOR_FENCE_RECEIPT
        write_json(predecessor_path, predecessor)
        if activation_receipt is None:
            activation_receipt = boots
        if activation_receipt:
            activation = seal({
                "schema_version": "awesome-theorems/stage5-1-activation-fence/1.0",
                "organization_release": "1.0", "status": "accepted",
                "predecessor_fence": {
                    "path": str(checker.PREDECESSOR_FENCE_RECEIPT),
                    "sha256": hashlib.sha256(predecessor_path.read_bytes()).hexdigest(),
                    "authority_sha256": predecessor["authority_sha256"],
                },
                "boot_acceptance": {
                    program: {
                        "item_id": f"{'S51THM' if program == 'theorems' else 'S51CON'}-BOOT-001",
                        "pre_blueprint_sha256": pointer["blueprints"][program]["sha256"],
                        "post_blueprint_sha256": hashlib.sha256(
                            (root / checker.PROGRAMS[program]["blueprint"]).read_bytes()
                        ).hexdigest(),
                        "post_gantt_sha256": hashlib.sha256(
                            (root / pointer["blueprints"][program]["gantt_path"]).read_bytes()
                        ).hexdigest(),
                        "review_receipt_sha256": "8" * 64,
                    }
                    for program in checker.PROGRAMS
                },
            })
            write_json(root / checker.FENCE_RECEIPT, activation)


def snapshot(root: Path) -> dict[str, tuple]:
    result = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        result[relative] = (info.st_mode, info.st_size, info.st_mtime_ns, info.st_ino, digest)
    return result


class Stage51ActivationFenceTests(unittest.TestCase):
    def test_ready_fixture_has_three_distinct_phases(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root)
            before = snapshot(root)
            boot = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            member = checker.evaluate(root, phase="member", crontab_text="", process_rows=[])
            self.assertTrue(boot["axes"]["materialization_valid"])
            self.assertTrue(boot["axes"]["ready_for_boot_reacceptance"])
            self.assertFalse(boot["axes"]["ready_for_member_admission"])
            self.assertTrue(boot["ready"])
            self.assertFalse(member["ready"])
            self.assertIn("STAGE51_BOOT_NOT_ACCEPTED", {row["code"] for row in member["reasons"]})
            self.assertEqual(before, snapshot(root))

    def test_member_ready_requires_new_boot_x(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, boots=True)
            report = checker.evaluate(root, phase="member", crontab_text="", process_rows=[])
            self.assertTrue(report["ready"])
            self.assertEqual(report["status"], "ready")
            self.assertEqual(report["reasons"], [])

    def test_boot_phase_does_not_require_prompt_controller_or_activation_receipt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, prompts=False, activation_receipt=False)
            (root / "scripts/stage5_1_theorems_execution_cron.py").unlink()
            report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            self.assertTrue(report["ready"])
            self.assertTrue(report["axes"]["ready_for_boot_reacceptance"])
            self.assertFalse(report["axes"]["ready_for_member_admission"])

    def test_receipt_digests_are_rebound_to_current_evidence(self) -> None:
        mutations = (
            lambda root: reseal_json(
                root / checker.PREDECESSOR_FENCE_RECEIPT,
                lambda value: value.__setitem__("crontab_sha256", "a" * 64),
            ),
            lambda root: reseal_json(
                root / checker.PREDECESSOR_FENCE_RECEIPT,
                lambda value: value["predecessors"]["theorems"].__setitem__(
                    "state_sha256", "b" * 64,
                ),
            ),
            lambda root: reseal_json(
                root / checker.PREDECESSOR_FENCE_RECEIPT,
                lambda value: value["predecessors"]["conjectures"].__setitem__(
                    "queue_inventory_sha256", "c" * 64,
                ),
            ),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory(
                prefix="stage51-fence-"
            ) as temporary:
                root = Path(temporary)
                make_fixture(root, activation_receipt=False)
                mutate(root)
                report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
                self.assertFalse(report["ready"])
                self.assertIn(
                    "PREDECESSOR_FENCE_RECEIPT_STALE",
                    {row["code"] for row in report["reasons"]},
                )

    def test_prompt_digest_rebinds_only_at_member_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, boots=True)
            reseal_json(
                root / checker.PREDECESSOR_FENCE_RECEIPT,
                lambda value: value["prompt_digests"].__setitem__("theorems", "d" * 64),
            )
            # Rebind activation receipt to the newly sealed predecessor receipt
            # so this mutation isolates the current prompt-digest check.
            predecessor = json.loads((root / checker.PREDECESSOR_FENCE_RECEIPT).read_text())
            reseal_json(
                root / checker.FENCE_RECEIPT,
                lambda value: value["predecessor_fence"].update({
                    "sha256": hashlib.sha256(
                        (root / checker.PREDECESSOR_FENCE_RECEIPT).read_bytes()
                    ).hexdigest(),
                    "authority_sha256": predecessor["authority_sha256"],
                }),
            )
            boot = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            member = checker.evaluate(root, phase="member", crontab_text="", process_rows=[])
            self.assertTrue(boot["ready"])
            self.assertFalse(member["ready"])
            self.assertIn(
                "PREDECESSOR_FENCE_PROMPT_BINDING_STALE",
                {row["code"] for row in member["reasons"]},
            )

    def test_handoff_ready_is_terminal_evidence_not_unknown_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, activation_receipt=False)
            policy = checker.PROGRAMS["conjectures"]
            write_json(root / policy["runtime"] / "state/controller-state.json", seal({
                "schema_version": "fixture-conjectures", "reservations": [],
                "claims": {"C": {"status": "handoff_ready", "item_id": "S5CON-X", "run_id": "r-x"}},
            }))
            report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            self.assertNotIn("STATE_UNKNOWN_STATUS", {row["code"] for row in report["reasons"]})
            self.assertIn("PREDECESSOR_FENCE_RECEIPT_STALE", {row["code"] for row in report["reasons"]})

    def test_missing_and_partial_prompt_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, prompts=False)
            report = checker.evaluate(root, phase="member", crontab_text="", process_rows=[])
            self.assertIn("CONCURRENCY_PROMPT_REQUIRED", {row["code"] for row in report["reasons"]})
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root)
            path = root / "Docs/evidence/stage5_1_theorems/operator-concurrency-prompt.json"
            value = json.loads(path.read_text())
            value["concurrency"].pop("hard_cap")
            write_json(path, seal({key: child for key, child in value.items() if key != "authority_sha256"}))
            report = checker.evaluate(root, phase="member", crontab_text="", process_rows=[])
            self.assertIn("CONCURRENCY_PROMPT_INVALID", {row["code"] for row in report["reasons"]})

    def test_legacy_marker_active_claim_transport_descendant_and_lease_block(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, state=True)
            policy = checker.PROGRAMS["theorems"]
            runtime = root / policy["runtime"]
            task = runtime / "tasks/C/r-1"
            task.mkdir(parents=True)
            state = seal({
                "schema_version": "fixture", "claims": {"C": {
                    "status": "live", "item_id": "S5THM-00000001-TARGET",
                    "run_id": "r-1", "pane_pid": 91, "pane_pid_start_ticks": 92,
                    "task_root": str(task),
                }},
            })
            write_json(runtime / "state/controller-state.json", state)
            lease = {"lease_id": "l-1", "status": "leased", "run_id": "r-1"}
            ledger = runtime / "ledgers/request-leases.jsonl"
            ledger.parent.mkdir(parents=True, exist_ok=True)
            ledger.write_text(json.dumps(lease) + "\n")
            cron = policy["cron_begin"] + "\n* * * * * old\n" + policy["cron_end"] + "\n"
            processes = [{"pid": 91, "start_ticks": 92, "argv": "codex", "cwd": str(task), "codex_home": str(task / "codex-home")}]
            report = checker.evaluate(root, phase="boot", crontab_text=cron, process_rows=processes)
            codes = {row["code"] for row in report["reasons"]}
            self.assertTrue({"LEGACY_CRON_PRESENT", "LEGACY_ACTIVE_CLAIM",
                             "LEGACY_DESCENDANT_PROCESS_LIVE", "LEGACY_LEASE_UNRELEASED"}.issubset(codes))
            self.assertFalse(report["ready"])

    def test_queue_requires_explicit_disposition_but_handoff_archive_alone_does_not(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, state=True)
            archive = root / checker.PROGRAMS["theorems"]["runtime"] / "handoffs/archive/result.json"
            archive.parent.mkdir(parents=True)
            archive.write_text("{}\n")
            report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            self.assertNotIn("LEGACY_QUEUE_DISPOSITION_REQUIRED", {row["code"] for row in report["reasons"]})
            queue = root / checker.PROGRAMS["theorems"]["runtime"] / "integration/pending.json"
            queue.parent.mkdir(parents=True)
            queue.write_text("{}\n")
            report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            self.assertIn("LEGACY_QUEUE_DISPOSITION_REQUIRED", {row["code"] for row in report["reasons"]})

    def test_lock_path_alone_is_not_a_blocker(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, state=True)
            lock = root / checker.PROGRAMS["theorems"]["runtime"] / "scheduler.lock"
            lock.parent.mkdir(parents=True, exist_ok=True)
            lock.write_text("")
            report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            self.assertNotIn("LEGACY_CONTROLLER_LOCK_HELD", {row["code"] for row in report["reasons"]})

    def test_release_audit_failure_is_typed_invalid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root)
            (root / "Docs/tools/check_stage5_1_organization_release.py").write_text(
                "def audit_release(root, release, rebuild=True):\n    raise RuntimeError('drift')\n"
            )
            report = checker.evaluate(root, phase="materialization", crontab_text="", process_rows=[])
            self.assertEqual(report["status"], "invalid")
            self.assertIn("STAGE51_AUTHORITY_INVALID", {row["code"] for row in report["reasons"]})

    def test_successor_side_effect_before_ready_blocks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, prompts=False)
            report = checker.evaluate(
                root, phase="boot",
                crontab_text="# BEGIN AWESOME_THEOREMS_STAGE5_1_THEOREMS_EXECUTION_V1\n",
                process_rows=[],
            )
            self.assertIn("ACTIVATION_SIDE_EFFECT_BEFORE_READY", {row["code"] for row in report["reasons"]})

    def test_missing_successor_controller_blocks_boot_not_materialization(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root)
            controller = root / "scripts/stage5_1_theorems_execution_cron.py"
            controller.unlink()
            materialization = checker.evaluate(
                root, phase="materialization", crontab_text="", process_rows=[],
            )
            boot = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            member = checker.evaluate(root, phase="member", crontab_text="", process_rows=[])
            self.assertTrue(materialization["ready"])
            self.assertTrue(boot["ready"])
            self.assertFalse(member["ready"])
            self.assertIn("STAGE51_CONTROLLER_MISSING", {row["code"] for row in member["reasons"]})

    def test_inactive_predecessor_operator_goal_does_not_break_read_only_audit(self) -> None:
        # The activation fence never authenticates or resumes the predecessor
        # root goal.  An inactive goal must leave concrete drain reasons visible.
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, state=True)
            policy = checker.PROGRAMS["theorems"]
            write_json(root / policy["runtime"] / "state/controller-state.json", seal({
                "schema_version": "fixture", "operator_goal_status": "blocked",
                "claims": {"C": {"status": "live", "item_id": "S5THM-00000001-TARGET", "run_id": "r-1"}},
            }))
            report = checker.evaluate(root, phase="boot", crontab_text="", process_rows=[])
            codes = {row["code"] for row in report["reasons"]}
            self.assertIn("LEGACY_ACTIVE_CLAIM", codes)
            self.assertNotIn("OBSERVATION_FAILED", codes)

    def test_cli_json_and_check_are_read_only_and_nonzero_when_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage51-fence-") as temporary:
            root = Path(temporary)
            make_fixture(root, prompts=False)
            before = snapshot(root)
            json_run = subprocess.run(
                [sys.executable, "-B", str(CHECKER_PATH), "--root", str(root), "--json", "--phase", "member"],
                cwd="/", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(json_run.returncode, 1)
            value = json.loads(json_run.stdout)
            self.assertFalse(value["ready"])
            self.assertEqual(json_run.stderr, "")
            check_run = subprocess.run(
                [sys.executable, "-B", str(CHECKER_PATH), "--root", str(root), "--check", "--phase", "member"],
                cwd="/", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(check_run.returncode, 1)
            self.assertIn(value["reasons"][0]["code"], check_run.stdout)
            self.assertEqual(before, snapshot(root))
            self.assertFalse((root / "__pycache__").exists())

    def test_cli_requires_exactly_one_output_mode(self) -> None:
        no_mode = subprocess.run([sys.executable, "-B", str(CHECKER_PATH)], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, check=False)
        both = subprocess.run([sys.executable, "-B", str(CHECKER_PATH), "--check", "--json"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        write = subprocess.run([sys.executable, "-B", str(CHECKER_PATH), "--write"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        self.assertEqual((no_mode.returncode, both.returncode, write.returncode), (2, 2, 2))

    def test_current_repository_is_blocked_and_read_only(self) -> None:
        touched = [CHECKER_PATH, ROOT / "Docs/catalog/stage5_1_organization/Current_Release.json"]
        before = {str(path): (path.exists(), hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None)
                  for path in touched}
        run = subprocess.run(
            [sys.executable, "-B", str(CHECKER_PATH), "--json", "--phase", "member"],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        self.assertEqual(run.returncode, 1)
        report = json.loads(run.stdout)
        self.assertFalse(report["ready"])
        self.assertTrue(report["reasons"])
        after = {str(path): (path.exists(), hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None)
                 for path in touched}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
