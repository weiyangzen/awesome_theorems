#!/usr/bin/env python3
"""Materialize the all-blank 14,865-occurrence Stage5 conjecture successor.

This is a one-way successor preparer, not BOOT acceptance and not controller
activation.  It preserves the historical v2 runtime and handoff archives, but
does not reinterpret their accepted bytes.  The generated successor resets
BOOT and every execution row to blank so a reviewed BOOT bridge/reacceptance is
required before any launch.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_conjectures_blueprint.py"
BLUEPRINT = ROOT / "Docs/Stage5_Conjectures_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Conjectures_Gantt.md"
ANCESTOR_RECEIPT = ROOT / "Docs/evidence/stage5_conjectures/pool-expansion-correction-v5.json"
PREDECESSOR_RECEIPT = ROOT / "Docs/evidence/stage5_conjectures/pool-expansion-correction-v6.json"
RECEIPT = ROOT / "Docs/evidence/stage5_conjectures/pool-expansion-correction-v7.json"
RUNTIME = ROOT / ".ops/stage5-conjectures-execution-v2"
SUCCESSOR_RUNTIME = RUNTIME / "epochs/stage5-conjecture-occurrence-pool-v2"
CODE_PATHS = (
    MANAGER_PATH,
    CHECKER_PATH,
    ROOT / "Docs/tools/generate_stage5_conjectures_gantt.py",
    ROOT / "Docs/tools/materialize_stage5_conjecture_pool_expansion.py",
    ROOT / "Docs/catalog/v5/tools/build_stage5_conjecture_occurrence_pool.py",
    ROOT / "scripts/stage5_conjectures_execution_cron_v2.py",
    ROOT / "scripts/test_stage5_conjectures_execution_cron_v2.py",
    ROOT / "scripts/check_stage5_conjecture_claim.py",
    ROOT / "scripts/test_stage5_conjecture_claim.py",
    ROOT / "scripts/stage5_boot_schema_contract.py",
    ROOT / "scripts/test_stage5_boot_schema_contract.py",
    ROOT / "scripts/stage5_conjecture_handoff_transition.py",
    ROOT / "scripts/test_stage5_conjecture_handoff_transition.py",
)


class MigrationError(RuntimeError):
    pass


def load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise MigrationError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def runtime_boundary() -> dict[str, Any]:
    state_path = RUNTIME / "state/controller-state.json"
    if not state_path.is_file():
        return {"state_sha256": None, "active": [], "reserved": [], "claims": {}, "integration": []}
    value = json.loads(state_path.read_text(encoding="utf-8"))
    claims = value.get("claims", {}) if isinstance(value, dict) else {}
    if not isinstance(claims, dict):
        raise MigrationError("historical controller claims are malformed")
    active = sorted(
        item_id for item_id, record in claims.items()
        if isinstance(record, dict) and record.get("status") in {"materialized", "goal_submitted", "live"}
    )
    reservations = value.get("reservations", [])
    reserved = [row for row in reservations if isinstance(row, dict) and row.get("status") == "reserved"] if isinstance(reservations, list) else ["malformed"]
    integrations = [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path.read_bytes()), "disposition": "historical_predecessor_only"}
        for path in sorted((RUNTIME / "integration").glob("*.json"))
        if path.is_file() and not path.is_symlink()
    ] if (RUNTIME / "integration").is_dir() else []
    return {
        "state_sha256": digest(state_path.read_bytes()),
        "active": active,
        "reserved": reserved,
        "claims": {key: record.get("status") for key, record in sorted(claims.items()) if isinstance(record, dict)},
        "integration": integrations,
        "handoff_file_set_sha256": (
            digest(canonical(sorted(
                [
                    [path.relative_to(ROOT).as_posix(), digest(path.read_bytes())]
                    for path in (RUNTIME / "handoffs").rglob("*")
                    if path.is_file() and not path.is_symlink()
                ]
            ))) if (RUNTIME / "handoffs").is_dir() else None
        ),
        "repair_entries": sorted(path.name for path in (RUNTIME / "repair").glob("*") if path.is_file()) if (RUNTIME / "repair").is_dir() else [],
        "checkpoint_entries": sorted(path.name for path in (RUNTIME / "checkpoints").glob("*") if path.is_file()) if (RUNTIME / "checkpoints").is_dir() else [],
    }


def successor_runtime_boundary() -> dict[str, Any]:
    state_path = SUCCESSOR_RUNTIME / "state/controller-state.json"
    if not SUCCESSOR_RUNTIME.exists():
        return {"root_exists": False, "state_sha256": None, "active": [], "reserved": [], "queue_entries": []}
    if SUCCESSOR_RUNTIME.is_symlink() or not SUCCESSOR_RUNTIME.is_dir():
        raise MigrationError("successor runtime root is not a real directory")
    value = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}
    claims = value.get("claims", {}) if isinstance(value, dict) else {}
    reservations = value.get("reservations", []) if isinstance(value, dict) else []
    active = sorted(
        item_id for item_id, record in claims.items()
        if isinstance(record, dict) and record.get("status") in {
            "materialized", "goal_submitted", "live", "generation_retire_required", "handoff_ready",
        }
    ) if isinstance(claims, dict) else ["malformed"]
    reserved = [row for row in reservations if isinstance(row, dict) and row.get("status") == "reserved"] if isinstance(reservations, list) else ["malformed"]
    queues = []
    for name in ("handoffs", "integration", "repair", "checkpoints"):
        root = SUCCESSOR_RUNTIME / name
        if root.is_dir():
            queues.extend(
                path.relative_to(SUCCESSOR_RUNTIME).as_posix()
                for path in root.rglob("*") if path.is_file() or path.is_symlink()
            )
    return {
        "root_exists": True,
        "state_sha256": digest(state_path.read_bytes()) if state_path.is_file() else None,
        "active": active,
        "reserved": reserved,
        "queue_entries": sorted(queues),
    }


def verify_receipt(path: Path, expected_schema: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise MigrationError(f"append-only predecessor receipt is missing: {path.name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    body = dict(value) if isinstance(value, dict) else {}
    authority = body.pop("authority_sha256", None)
    if value.get("schema_version") != expected_schema or not isinstance(authority, str) or digest(canonical(body)) != authority:
        raise MigrationError(f"append-only predecessor receipt is invalid: {path.name}")
    return value


def build() -> tuple[dict[Path, bytes], dict[str, Any]]:
    manager = load(MANAGER_PATH, "stage5_pool_expansion_manager")
    checker = load(CHECKER_PATH, "stage5_pool_expansion_checker")
    runtime = runtime_boundary()
    if runtime["active"] or runtime["reserved"]:
        raise MigrationError(f"active/reserved historical generations block migration: {runtime['active'][:5]}")
    ancestor = verify_receipt(
        ANCESTOR_RECEIPT,
        "awesome-theorems/stage5-conjecture-pool-expansion-migration/1.0",
    )
    prior = verify_receipt(
        PREDECESSOR_RECEIPT,
        "awesome-theorems/stage5-conjecture-pool-expansion-migration/1.0",
    )
    if (
        prior.get("predecessor", {}).get("blueprint_sha256")
        != ancestor.get("successor", {}).get("blueprint_sha256")
        or prior.get("predecessor", {}).get("gantt_sha256")
        != ancestor.get("successor", {}).get("gantt_sha256")
        or prior.get("successor", {}).get("blueprint_sha256") != digest(BLUEPRINT.read_bytes())
        or prior.get("successor", {}).get("gantt_sha256") != digest(GANTT.read_bytes())
    ):
        raise MigrationError("current predecessor is not the exact v2 pool successor chain")
    successor_runtime = successor_runtime_boundary()
    if successor_runtime["active"] or successor_runtime["reserved"] or successor_runtime["queue_entries"]:
        raise MigrationError("active/reserved/queued successor runtime blocks authority correction")
    tasks = manager.expected_tasks(manager.CONJECTURE)
    if len(tasks) != 16_622:
        raise MigrationError("successor checklist cardinality differs")
    if any(task.state != " " for task in tasks):
        raise MigrationError("successor checklist is not all blank")
    blueprint_raw = manager.render_blueprint(manager.CONJECTURE, tasks)
    with tempfile.NamedTemporaryFile(prefix="stage5-conjecture-pool-blueprint-", suffix=".md", delete=False) as stream:
        candidate = Path(stream.name)
        stream.write(blueprint_raw)
    try:
        spec, rows, parsed_raw = checker.parse_blueprint(candidate)
    finally:
        candidate.unlink(missing_ok=True)
    if parsed_raw != blueprint_raw:
        raise MigrationError("candidate Blueprint parse round-trip differs")
    generated_at = manager.utc_now()
    boot_outputs = checker.render_boot_data(parsed=(spec, rows, blueprint_raw))
    prompt_path = ROOT / manager.concurrency_prompt_path(manager.CONJECTURE)
    if not prompt_path.is_file() or prompt_path.is_symlink():
        raise MigrationError("reviewed predecessor concurrency prompt is missing")
    prompt = json.loads(prompt_path.read_text(encoding="utf-8"))
    prompt_body = dict(prompt) if isinstance(prompt, dict) else {}
    prompt_authority = prompt_body.pop("authority_sha256", None)
    predecessor_spec = json.loads((ROOT / "Docs/evidence/stage5_conjectures/execution-spec.json").read_text(encoding="utf-8"))
    if (
        not isinstance(prompt, dict)
        or prompt.get("schema_version") != manager.CONCURRENCY_PROMPT_SCHEMA
        or prompt.get("program") != manager.CONJECTURE.version
        or prompt.get("source") != "explicit operator prompt fixture; not a controller or Blueprint default"
        or set(prompt.get("concurrency", {})) != set(manager.CONCURRENCY_DIMENSIONS)
        or not isinstance(prompt_authority, str)
        or digest(canonical(prompt_body)) != prompt_authority
        or prompt.get("execution_spec_sha256") != digest(canonical(predecessor_spec))
    ):
        raise MigrationError("reviewed predecessor concurrency prompt differs")
    prompt_body["execution_spec_sha256"] = digest(canonical(spec))
    prompt = {**prompt_body, "authority_sha256": digest(canonical(prompt_body))}
    prompt_raw = json.dumps(prompt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    # The predecessor runtime is historical authority only.  Rendering the
    # successor must start from its deliberately blank checklist and refreshed
    # prompt, never project retired/stopped predecessor claims into it.
    manager.runtime_snapshot = lambda _program: (None, None)
    gantt_raw = manager.render_gantt(
        manager.CONJECTURE, blueprint_raw, tasks, generated_at,
        prompt_override=prompt_raw,
    )
    old_blueprint_sha = digest(BLUEPRINT.read_bytes()) if BLUEPRINT.is_file() else None
    old_gantt_sha = digest(GANTT.read_bytes()) if GANTT.is_file() else None
    added = sorted(row["item_id"] for row in rows if row["item_id"].startswith("S5CON-POOL-") and row["item_id"].endswith("-INTAKE"))
    if len(added) != 14_865 or added[0] != "S5CON-POOL-00000001-INTAKE" or added[-1] != "S5CON-POOL-00014865-INTAKE":
        raise MigrationError("successor pool ID range differs")
    receipt_body = {
        "schema_version": "awesome-theorems/stage5-conjecture-pool-expansion-migration/1.0",
        "status": "materialized_unaccepted",
        "program": manager.CONJECTURE.version,
        "generated_at": generated_at,
        "predecessor": {
            "blueprint_sha256": old_blueprint_sha,
            "gantt_sha256": old_gantt_sha,
            "strict_resolution_targets": 1_425,
            "historical_runtime_root": manager.CONJECTURE.runtime_root,
            "historical_runtime_preserved": True,
            "historical_handoffs_preserved": True,
            "historical_runtime_not_successor_authority": True,
            "runtime_authority_epoch": manager.CONJECTURE_RUNTIME_AUTHORITY_EPOCH,
            "historical_controller_state_sha256": (
                digest((RUNTIME / "state/controller-state.json").read_bytes())
                if (RUNTIME / "state/controller-state.json").is_file() else None
            ),
            "runtime_boundary": runtime,
            "correction_v5_receipt": {
                "path": ANCESTOR_RECEIPT.relative_to(ROOT).as_posix(),
                "sha256": digest(ANCESTOR_RECEIPT.read_bytes()),
                "authority_sha256": ancestor["authority_sha256"],
            },
            "correction_v6_receipt": {
                "path": PREDECESSOR_RECEIPT.relative_to(ROOT).as_posix(),
                "sha256": digest(PREDECESSOR_RECEIPT.read_bytes()),
                "authority_sha256": prior["authority_sha256"],
            },
            "successor_runtime_boundary": successor_runtime,
        },
        "successor": {
            "blueprint_sha256": digest(blueprint_raw),
            "gantt_sha256": digest(gantt_raw),
            "execution_spec_sha256": digest(canonical(spec)),
            "explicit_concurrency_prompt_sha256": digest(prompt_raw),
            "explicit_concurrency_vector_preserved": prompt["concurrency"],
            "strict_resolution_targets": 1_425,
            "source_occurrence_intake_targets": 14_865,
            "execution_members": 16_290,
            "checklist_items": 16_622,
            "added_item_id_set_sha256": digest(canonical(added)),
            "removed_item_ids": [],
            "all_rows_not_done": True,
            "boot_reacceptance_required": True,
            "strict_stage5_ids_unchanged": True,
            "stage5_release_5_6_unchanged": True,
            "stage6_release_6_0_unchanged": True,
            "strict_credits_granted": 0,
        },
        "pool_authority": {
            "current_pool_release_sha256": manager.CONJECTURE_POOL_CURRENT_SHA256,
            "pool_manifest_sha256": manager.CONJECTURE_POOL_MANIFEST_SHA256,
            "source_occurrence_pool_sha256": manager.CONJECTURE_POOL_OCCURRENCES_SHA256,
            "identity_review_registry_sha256": manager.CONJECTURE_POOL_IDENTITIES_SHA256,
            "source_archive_sha256": manager.CONJECTURE_POOL_SOURCE_ARCHIVE_SHA256,
            "source_commit": manager.CONJECTURE_POOL_SOURCE_COMMIT,
        },
        "semantic_boundary": {
            "occurrences_are_not_strict_identities": True,
            "intake_x_means_adjudication_only": True,
            "intake_rows_have_no_proof_resolution_debt": True,
            "promotion_requires_separate_append_only_stage5_and_stage6_migration": True,
            "strict_and_intake_aggregation_branches_are_separate": True,
        },
        "execution_boundary": {
            "explicit_concurrency_prompt_required": True,
            "concurrency_default_in_blueprint_or_skill": False,
            "gateway_or_websocket_contract_changed": False,
            "controller_not_activated": True,
            "closed_discriminated_work_contract": True,
            "strict_and_intake_worker_instructions_are_disjoint": True,
        },
        "artifact_sha256": {
            path.relative_to(ROOT).as_posix(): digest(raw)
            for path, raw in sorted(boot_outputs.items(), key=lambda item: item[0].as_posix())
        },
        "code_authority_sha256": {
            path.relative_to(ROOT).as_posix(): digest(path.read_bytes())
            for path in CODE_PATHS
        },
    }
    receipt = {**receipt_body, "authority_sha256": digest(canonical(receipt_body))}
    receipt_raw = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    outputs = {
        BLUEPRINT: blueprint_raw,
        GANTT: gantt_raw,
        **boot_outputs,
        prompt_path: prompt_raw,
        RECEIPT: receipt_raw,
    }
    return outputs, receipt


def validate(outputs: dict[Path, bytes]) -> dict[str, Any]:
    drift = [path.relative_to(ROOT).as_posix() for path, raw in outputs.items() if not path.is_file() or path.is_symlink() or path.read_bytes() != raw]
    if drift:
        raise MigrationError(f"successor artifact drift: {drift}")
    checker = load(CHECKER_PATH, "stage5_pool_expansion_final_checker")
    result = checker.validate()
    if result.get("strict_resolution_targets") != 1_425 or result.get("source_occurrence_intake_targets") != 14_865:
        raise MigrationError("final checker denominator differs")
    return {"valid": True, "checklist_items": result["items"], "strict_resolution_targets": 1_425, "source_occurrence_intake_targets": 14_865, "execution_members": 16_290, "blueprint_sha256": result["blueprint_sha256"]}


def validate_installed() -> dict[str, Any]:
    receipt = verify_receipt(
        RECEIPT,
        "awesome-theorems/stage5-conjecture-pool-expansion-migration/1.0",
    )
    successor = receipt.get("successor", {})
    if (
        successor.get("blueprint_sha256") != digest(BLUEPRINT.read_bytes())
        or successor.get("gantt_sha256") != digest(GANTT.read_bytes())
    ):
        raise MigrationError("installed v7 Blueprint/Gantt differ from receipt")
    for relative, expected in receipt.get("artifact_sha256", {}).items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink() or digest(path.read_bytes()) != expected:
            raise MigrationError(f"installed v7 artifact differs: {relative}")
    prompt_path = ROOT / "Docs/evidence/stage5_conjectures/execution/concurrency-prompt.json"
    if digest(prompt_path.read_bytes()) != successor.get("explicit_concurrency_prompt_sha256"):
        raise MigrationError("installed v7 concurrency prompt differs")
    for relative, expected in receipt.get("code_authority_sha256", {}).items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink() or digest(path.read_bytes()) != expected:
            raise MigrationError(f"installed v7 code authority differs: {relative}")
    checker = load(CHECKER_PATH, "stage5_pool_expansion_installed_checker")
    result = checker.validate()
    return {
        "valid": True,
        "checklist_items": result["items"],
        "strict_resolution_targets": result["strict_resolution_targets"],
        "source_occurrence_intake_targets": result["source_occurrence_intake_targets"],
        "execution_members": 16_290,
        "blueprint_sha256": result["blueprint_sha256"],
        "receipt": RECEIPT.relative_to(ROOT).as_posix(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.check and not args.write and RECEIPT.is_file():
            print(json.dumps(validate_installed(), ensure_ascii=False, sort_keys=True))
            return 0
        if args.write:
            manager = load(MANAGER_PATH, "stage5_pool_expansion_atomic_manager")
            with manager.conjecture_scheduler_transition_guard(), manager.manager_mutation_lock():
                if RECEIPT.exists() or RECEIPT.is_symlink():
                    raise MigrationError("append-only v7 correction receipt already exists")
                outputs, receipt = build()
                ordered = sorted(outputs.items(), key=lambda item: item[0].as_posix())
                expected_old = {path: manager.regular_file_expectation(path) for path, _ in ordered}
                expected_old[RECEIPT] = None
                guards = manager.source_input_expectations((manager.CONJECTURE,))
                for path in (*CODE_PATHS, ANCESTOR_RECEIPT, PREDECESSOR_RECEIPT):
                    expectation = manager.regular_file_expectation(path)
                    if expectation is None:
                        raise MigrationError(f"migration guard is missing: {path.relative_to(ROOT)}")
                    guards[path] = expectation
                observed_runtime = runtime_boundary()
                observed_successor_runtime = successor_runtime_boundary()
                if observed_runtime != receipt["predecessor"]["runtime_boundary"]:
                    raise MigrationError("historical runtime changed before correction commit")
                if observed_successor_runtime != receipt["predecessor"]["successor_runtime_boundary"]:
                    raise MigrationError("successor runtime changed before correction commit")
                manager.atomic_batch_write(
                    ordered,
                    expected_old=expected_old,
                    guards=guards,
                    precommit_validator=lambda: (
                        None if (
                            runtime_boundary() == observed_runtime
                            and successor_runtime_boundary() == observed_successor_runtime
                        ) else (_ for _ in ()).throw(MigrationError("runtime changed during correction commit"))
                    ),
                )
        else:
            outputs, receipt = build()
        if args.check or args.write:
            print(json.dumps(validate(outputs), ensure_ascii=False, sort_keys=True))
        else:
            print(json.dumps({"valid": True, "would_write": len(outputs), "receipt_authority_sha256": receipt["authority_sha256"]}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
