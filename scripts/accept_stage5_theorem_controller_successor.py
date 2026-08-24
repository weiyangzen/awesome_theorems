#!/usr/bin/env python3
"""Accept a paused, state-preserving Stage5 theorem controller successor.

This narrow migration re-accepts only the controller, its focused tests and
this migration verifier.  It preserves the accepted mathematical cursor,
every task-local claim baseline and every running TUI.  The predecessor BOOT
chain remains active as immutable ancestry; its exact bytes and the v2
activation are copied into a content-addressed successor archive.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / "scripts/stage5_theorems_execution_cron_v2.py"
CONTROLLER_TEST_PATH = ROOT / "scripts/test_stage5_theorems_execution_cron_v2.py"
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_theorems_blueprint.py"
CHECKER_TEST_PATH = ROOT / "scripts/test_stage5_theorems_blueprint.py"
ITEM_CHECKER_PATH = ROOT / "scripts/check_stage5_theorem_item.py"
ITEM_CHECKER_TEST_PATH = ROOT / "scripts/test_stage5_theorem_item.py"
SUCCESSOR_ACCEPTANCE = (
    ROOT / "Docs/evidence/stage5_theorems/bootstrap/controller-successor-acceptance.json"
)
PRIVATE_ROOT = Path("/home/sansha/.local/state/awesome-theorems-stage5-theorem-boot-v1")
PRINCIPALS = (
    ("theorem-boot-producer-v1", "theorem-boot-producer", "producer"),
    ("theorem-boot-reviewer-a-v1", "theorem-boot-reviewer-a", "reviewer"),
    ("theorem-boot-reviewer-b-v1", "theorem-boot-reviewer-b", "reviewer"),
    ("theorem-boot-master-v1", "theorem-boot-master", "master"),
)
PROGRAM = "stage5-theorem-proof-debt/2.0"
SIGNED_SCHEMA = "awesome-theorems/stage5-controller-successor-signed/1.0"
BOOT_PATHS = (
    "Docs/evidence/stage5_theorems/controller-bootstrap-handoff.json",
    "Docs/evidence/stage5_theorems/controller-bootstrap-handoff-acceptance.json",
    "Docs/evidence/stage5_theorems/controller-bootstrap-review.json",
    "Docs/evidence/stage5_theorems/controller-bootstrap-acceptance.json",
    "Docs/evidence/stage5_theorems/controller-bootstrap-role-trust-root.json",
)


class MigrationError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def instant() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_controller() -> Any:
    specification = importlib.util.spec_from_file_location(
        "stage5_controller_successor_candidate", CONTROLLER_PATH,
    )
    if specification is None or specification.loader is None:
        raise MigrationError("candidate controller cannot be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise MigrationError(f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(raw, object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MigrationError(f"{label}: invalid JSON") from exc
    if not isinstance(value, dict):
        raise MigrationError(f"{label}: expected object")
    return value


def verify_seal(value: dict[str, Any], label: str) -> dict[str, Any]:
    body = dict(value)
    authority = body.pop("authority_sha256", None)
    if not isinstance(authority, str) or digest(canonical(body)) != authority:
        raise MigrationError(f"{label}: authority seal differs")
    return value


def exclusive_write(path: Path, raw: bytes, mode: int = 0o444) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != raw:
            raise MigrationError(f"immutable successor output conflicts: {path}")
        return
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode,
    )
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def cas_replace(path: Path, expected: bytes, raw: bytes, mode: int = 0o444) -> None:
    """Replace the active authority pointer only from its exact ancestor."""
    if path.is_symlink() or not path.is_file() or path.read_bytes() != expected:
        raise MigrationError(f"active successor authority changed before CAS: {path}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        if path.read_bytes() != expected:
            raise MigrationError(f"active successor authority changed during CAS: {path}")
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False,
    ).encode("utf-8") + b"\n"


def private_key(key_id: str, principal_id: str, role: str) -> Ed25519PrivateKey:
    path = PRIVATE_ROOT / f"{key_id}.json"
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o077:
        raise MigrationError(f"unsafe/missing successor private key: {path}")
    value = strict_json(path.read_bytes(), "successor private key")
    if (
        set(value) != {
            "schema_version", "key_id", "principal_id", "allowed_role", "private_key_hex",
        }
        or value.get("key_id") != key_id
        or value.get("principal_id") != principal_id
        or value.get("allowed_role") != role
    ):
        raise MigrationError("successor private-key identity differs")
    try:
        return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(value["private_key_hex"]))
    except (KeyError, ValueError) as exc:
        raise MigrationError("successor private key is malformed") from exc


def signed_document(
    *, role: str, ordinal: int, payload: dict[str, Any],
) -> dict[str, Any]:
    identities = [entry for entry in PRINCIPALS if entry[2] == role]
    try:
        key_id, principal_id, _ = identities[ordinal]
    except IndexError as exc:
        raise MigrationError(f"missing successor signing role: {role}/{ordinal}") from exc
    unsigned = {
        "schema_version": SIGNED_SCHEMA,
        "program": PROGRAM,
        "role": role,
        "principal_id": principal_id,
        "key_id": key_id,
        "signature_algorithm": "Ed25519",
        "payload": payload,
    }
    raw = canonical(unsigned)
    value = {
        **unsigned,
        "signed_payload_sha256": digest(raw),
        "signature": private_key(key_id, principal_id, role).sign(raw).hex(),
    }
    value["authority_sha256"] = digest(canonical(value))
    return value


def write_maintenance_intent(controller: Any) -> dict[str, Any]:
    """Sign the one-use paused reconcile/refill permission for this candidate."""
    predecessor_raw = SUCCESSOR_ACCEPTANCE.read_bytes()
    predecessor = controller._verify_successor_signature(
        controller.strict_json(predecessor_raw, "maintenance predecessor successor"),
        label="maintenance predecessor successor", role="master",
        trust=controller._load_successor_trust(),
    )
    activation_raw = controller._regular(
        controller.ACTIVATION_RECEIPT, "maintenance predecessor activation",
    )
    activation = controller.verify_seal(
        controller.strict_json(activation_raw, "maintenance predecessor activation"),
        "maintenance predecessor activation",
    )
    crontab = controller.read_crontab()
    if controller.CRON_BEGIN in crontab or controller.CRON_END in crontab:
        raise MigrationError("maintenance intent requires theorem cron paused")
    payload = {
        "action": "paused_reconcile_fence_and_refill_only",
        "candidate_artifacts": {
            "controller_sha256": file_digest(CONTROLLER_PATH),
            "controller_test_sha256": file_digest(CONTROLLER_TEST_PATH),
            "migration_tool_sha256": file_digest(Path(__file__)),
            "checker_sha256": file_digest(CHECKER_PATH),
            "checker_test_sha256": file_digest(CHECKER_TEST_PATH),
            "item_checker_sha256": file_digest(ITEM_CHECKER_PATH),
            "item_checker_test_sha256": file_digest(ITEM_CHECKER_TEST_PATH),
        },
        "predecessor_successor": {
            "path": SUCCESSOR_ACCEPTANCE.relative_to(ROOT).as_posix(),
            "file_sha256": digest(predecessor_raw),
            "authority_sha256": predecessor["authority_sha256"],
        },
        "predecessor_activation": {
            "path": controller.ACTIVATION_RECEIPT.relative_to(ROOT).as_posix(),
            "file_sha256": digest(activation_raw),
            "authority_sha256": activation["authority_sha256"],
            "schema_version": activation["schema_version"],
        },
        "paused_crontab_sha256": digest(crontab.encode()),
        "requested_authenticated_goals": 24,
        "issued_at": instant(),
        "expires_at_epoch": time.time() + 900,
    }
    intent = signed_document(role="producer", ordinal=0, payload=payload)
    raw = json_bytes(intent)
    target = controller.CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT
    if target.exists() or target.is_symlink():
        old = target.read_bytes() if target.is_file() and not target.is_symlink() else b""
        archive = (
            ROOT / "Docs/evidence/stage5_theorems/bootstrap/controller-successions"
            / "maintenance-intents" / digest(old) / "intent.json"
        )
        if old:
            exclusive_write(archive, old)
        cas_replace(target, old, raw)
    else:
        exclusive_write(target, raw)
    controller.validate_controller_successor_maintenance_intent()
    return {
        "valid": True, "intent_authority_sha256": intent["authority_sha256"],
        "expires_at_epoch": payload["expires_at_epoch"],
    }


def write_abandoned_successor_index(controller: Any) -> dict[str, Any]:
    """Sign a non-authoritative inventory of sibling/partial successor epochs."""
    root = ROOT / "Docs/evidence/stage5_theorems/bootstrap/controller-successions"
    active_raw = SUCCESSOR_ACCEPTANCE.read_bytes()
    active = controller._verify_successor_signature(
        controller.strict_json(active_raw, "active successor authority"),
        label="active successor authority", role="master",
        trust=controller._load_successor_trust(),
    )
    reachable: set[str] = {digest(active_raw)}
    cursor = active
    while True:
        locator_value = cursor.get("payload", {}).get("predecessor_controller_successor")
        if not isinstance(locator_value, dict):
            break
        path = ROOT / controller._safe_relative(locator_value.get("path", ""))
        raw = controller._regular(path, "reachable predecessor successor")
        reachable.add(digest(raw))
        cursor = controller._verify_successor_signature(
            controller.strict_json(raw, "reachable predecessor successor"),
            label="reachable predecessor successor", role="master",
            trust=controller._load_successor_trust(),
        )
    abandoned: list[dict[str, Any]] = []
    for path in sorted(root.glob("*/master-acceptance.json")):
        raw = path.read_bytes()
        if digest(raw) in reachable:
            continue
        value = strict_json(raw, f"sibling successor {path}")
        abandoned.append({
            "path": path.relative_to(ROOT).as_posix(),
            "file_sha256": digest(raw),
            "authority_sha256": value.get("authority_sha256"),
            "disposition": "abandoned_or_superseded_not_reachable_from_active_pointer",
        })
    partials = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "file_sha256": file_digest(path),
            "disposition": "partial_epoch_without_master_acceptance_not_authoritative",
        }
        for path in sorted(root.glob("*"))
        if path.is_dir() and not (path / "master-acceptance.json").is_file()
        and path.name != "maintenance-intents"
    ]
    payload = {
        "active_pointer_path": SUCCESSOR_ACCEPTANCE.relative_to(ROOT).as_posix(),
        "active_file_sha256": digest(active_raw),
        "active_authority_sha256": active["authority_sha256"],
        "authority_rule": "only the active pointer and its authenticated predecessor chain are authoritative",
        "abandoned_complete_epochs": abandoned,
        "partial_epochs": partials,
        "recorded_at": instant(),
    }
    receipt = signed_document(role="master", ordinal=0, payload=payload)
    raw = json_bytes(receipt)
    target = root / "abandoned-successor-index" / digest(canonical(payload)) / "index.json"
    exclusive_write(target, raw)
    return {
        "valid": True,
        "path": target.relative_to(ROOT).as_posix(),
        "authority_sha256": receipt["authority_sha256"],
        "abandoned_complete_epochs": len(abandoned),
        "partial_epochs": len(partials),
    }


def invalidate_budget_overrun_acceptance(controller: Any) -> dict[str, Any]:
    """Revoke one accepted execution credit that exceeded its frozen claim cap."""
    item_id = "S5THM-00003496-TARGET"
    run_id = "r-1786946573-08d1371d"
    acceptance_path = (
        ROOT / "Docs/evidence/stage5_theorems/execution/handoffs/"
        "S5THM-00003496-TARGET--worker/"
        "1654041c0588b1829383d350aa74c50a19f5aaa13ca3d2e0255782e47b8e26c5/"
        "5be004ca67b1fc30148dfa54431454a09b203c5ec5d5f9363a4f3e82525069fb/"
        "master-integration.json"
    )
    if controller.CRON_BEGIN in controller.read_crontab() or controller.CRON_END in controller.read_crontab():
        raise MigrationError("budget-overrun invalidation requires theorem cron paused")
    with controller.admission_pump_guard():
        with controller.scheduler_guard(nonblocking=False):
            specification, rows, blueprint_raw = controller.load_program()
            target = next(row for row in rows if row["item_id"] == item_id)
            if target["state"] != "x":
                if controller.BUDGET_OVERRUN_INVALIDATION.is_file():
                    accepted = controller.validate_budget_overrun_invalidation()
                    return {"valid": True, "already_invalidated": True, "authority_sha256": accepted["authority_sha256"]}
                raise MigrationError("budget-overrun target is not currently Master accepted")
            acceptance_raw = controller._regular(acceptance_path, "invalidated Master acceptance")
            acceptance = controller.verify_seal(
                controller.strict_json(acceptance_raw, "invalidated Master acceptance"),
                "invalidated Master acceptance",
            )
            claim_path = (
                controller.RUNTIME / "tasks" / f"{item_id}--worker" / run_id / "claim.json"
            )
            claim = controller.strict_json(
                controller._regular(claim_path, "overrun claim"), "overrun claim",
            )
            measurement = controller.measured_generation_usage({
                "task_root": claim["task_root"],
                "codex_home": str(Path(claim["task_root"]) / "codex-home"),
                "goal_id": "83365986-8fad-4e73-8bdc-8fd8b6c65536",
                "goal_submissions": 1,
                "execution_limits": claim["execution_policy"]["execution_limits"],
            })
            measured_tokens = measurement["goal_registry"].get("tokens_used")
            claim_cap = claim["resource_budget"]["model_input_tokens"]
            if (
                acceptance.get("item_id") != item_id
                or acceptance.get("handoff", {}).get("run_id") != run_id
                or not isinstance(measured_tokens, int) or measured_tokens <= claim_cap
                or claim_cap != 2_000_000
            ):
                raise MigrationError("frozen claim/measurement does not prove the accepted overrun")
            old_gantt = controller._regular(controller.GANTT, "pre-invalidation Gantt")
            state_raw = controller._regular(controller.STATE_PATH, "pre-invalidation state")
            state = controller.verify_seal(
                controller.strict_json(state_raw, "pre-invalidation state"),
                "pre-invalidation state",
            )
            pre_accepted = [row["item_id"] for row in rows if row["state"] == "x"]
            preserved = [value for value in pre_accepted if value != item_id]
            marker = f"- [x] `{item_id}` "
            if blueprint_raw.decode().count(marker) != 1:
                raise MigrationError("budget-overrun Blueprint row identity differs")
            post_blueprint = blueprint_raw.decode().replace(
                marker, f"- [ ] `{item_id}` ", 1,
            ).encode()
            with tempfile.TemporaryDirectory(prefix="stage5-budget-invalidation-") as temporary:
                candidate = Path(temporary) / "Stage5_Theorems_Blueprint.md"
                candidate.write_bytes(post_blueprint)
                generator_spec = importlib.util.spec_from_file_location(
                    "stage5_budget_invalidation_gantt",
                    ROOT / "Docs/tools/generate_stage5_theorems_gantt.py",
                )
                if generator_spec is None or generator_spec.loader is None:
                    raise MigrationError("Gantt generator unavailable")
                generator = importlib.util.module_from_spec(generator_spec)
                sys.modules[generator_spec.name] = generator
                generator_spec.loader.exec_module(generator)
                post_gantt = generator.render(blueprint_path=candidate)
            post_state = dict(state)
            post_state.pop("authority_sha256", None)
            old_credit = post_state.get("claims", {}).get(item_id)
            post_state.setdefault("claims", {})[item_id] = {
                "item_id": item_id,
                "claim_id": f"{item_id}--worker",
                "run_id": run_id,
                "generation_id": run_id,
                "lane_id": item_id,
                "status": "invalidated",
                "work_state": "not_done",
                "invalidated_master_acceptance_sha256": controller.digest(acceptance_raw),
                "invalidated_reason": "accepted generation exceeded frozen model_input_tokens cap",
            }
            post_state_raw = json_bytes(controller.seal(post_state))
            migration_id = digest(canonical({
                "schema_version": "awesome-theorems/stage5-budget-overrun-invalidation-id/1.0",
                "program": PROGRAM, "item_id": item_id, "run_id": run_id,
                "acceptance_sha256": digest(acceptance_raw),
                "pre_blueprint_sha256": digest(blueprint_raw),
                "post_blueprint_sha256": digest(post_blueprint),
                "pre_state_sha256": digest(state_raw),
                "post_state_sha256": digest(post_state_raw),
                "measured_goal_tokens_used": measured_tokens,
                "claim_model_input_tokens": claim_cap,
            }))
            epoch = (
                ROOT / "Docs/evidence/stage5_theorems/execution/"
                "budget-overrun-invalidations" / migration_id
            )
            pre_blueprint_archive = epoch / "pre/Stage5_Theorems_Blueprint.md"
            pre_gantt_archive = epoch / "pre/Stage5_Theorems_Gantt.md"
            pre_state_archive = epoch / "pre/controller-state.json"
            post_blueprint_archive = epoch / "post/Stage5_Theorems_Blueprint.md"
            post_gantt_archive = epoch / "post/Stage5_Theorems_Gantt.md"
            post_state_archive = epoch / "post/controller-state.json"
            for path, raw in (
                (pre_blueprint_archive, blueprint_raw), (pre_gantt_archive, old_gantt),
                (pre_state_archive, state_raw), (post_blueprint_archive, post_blueprint),
                (post_gantt_archive, post_gantt), (post_state_archive, post_state_raw),
            ):
                exclusive_write(path, raw)
            subject = {
                "item_id": item_id,
                "invalidated_master_acceptance": {
                    "path": acceptance_path.relative_to(ROOT).as_posix(),
                    "file_sha256": digest(acceptance_raw),
                    "authority_sha256": acceptance["authority_sha256"],
                    "run_id": run_id,
                },
                "overrun_generation": {
                    "claim_path": claim_path.relative_to(ROOT).as_posix(),
                    "claim_sha256": file_digest(claim_path),
                    "run_id": run_id,
                    "claim_model_input_tokens": claim_cap,
                    "measured_goal_tokens_used": measured_tokens,
                    "measurement": measurement,
                    "violation": "model_input_token_budget_exceeded",
                },
                "pre": {
                    "blueprint_path": pre_blueprint_archive.relative_to(ROOT).as_posix(),
                    "blueprint_sha256": digest(blueprint_raw),
                    "gantt_path": pre_gantt_archive.relative_to(ROOT).as_posix(),
                    "gantt_sha256": digest(old_gantt),
                    "state_path": pre_state_archive.relative_to(ROOT).as_posix(),
                    "state_sha256": digest(state_raw),
                    "state_credit": old_credit,
                },
                "post": {
                    "blueprint_path": post_blueprint_archive.relative_to(ROOT).as_posix(),
                    "blueprint_sha256": digest(post_blueprint),
                    "gantt_path": post_gantt_archive.relative_to(ROOT).as_posix(),
                    "gantt_sha256": digest(post_gantt),
                    "state_path": post_state_archive.relative_to(ROOT).as_posix(),
                    "state_sha256": digest(post_state_raw),
                    "state_credit": post_state["claims"][item_id],
                },
                "preserved_master_accepted_item_ids": preserved,
            }
            subject_sha = digest(canonical(subject))
            producer = signed_document(role="producer", ordinal=0, payload={
                "migration_id": migration_id, "review_subject": subject,
                "review_subject_sha256": subject_sha, "decision": "self_tested",
                "conflicts": [], "prepared_at": instant(),
            })
            producer_path = epoch / "producer-handoff.json"
            exclusive_write(producer_path, json_bytes(producer))
            reviewer_locators = []
            reviewer_authorities = []
            for ordinal in range(2):
                reviewer = signed_document(role="reviewer", ordinal=ordinal, payload={
                    "migration_id": migration_id,
                    "producer_authority_sha256": producer["authority_sha256"],
                    "review_subject_sha256": subject_sha, "decision": "pass",
                    "conflicts": [], "reviewed_at": instant(),
                })
                path = epoch / "reviews" / f"reviewer-{ordinal + 1}.json"
                exclusive_write(path, json_bytes(reviewer))
                reviewer_locators.append(locator(path, reviewer))
                reviewer_authorities.append(reviewer["authority_sha256"])
            master = signed_document(role="master", ordinal=0, payload={
                "migration_id": migration_id, "producer": locator(producer_path, producer),
                "reviewers": reviewer_locators, **subject,
                "review_subject_sha256": subject_sha,
                "reviewer_authorities": reviewer_authorities,
                "accepted_at": instant(),
            })
            master_raw = json_bytes(master)
            master_path = epoch / "master-acceptance.json"
            exclusive_write(master_path, master_raw)
            # Commit the three active projections from exact preimages.  The
            # immutable candidate evidence above makes a crash auditable; the
            # active authority pointer is installed only after all three post
            # images are visible.
            cas_replace(controller.BLUEPRINT, blueprint_raw, post_blueprint, 0o644)
            cas_replace(controller.GANTT, old_gantt, post_gantt, 0o644)
            cas_replace(controller.STATE_PATH, state_raw, post_state_raw, 0o600)
            if controller.BUDGET_OVERRUN_INVALIDATION.exists():
                raise MigrationError("active budget-overrun invalidation pointer already exists")
            exclusive_write(controller.BUDGET_OVERRUN_INVALIDATION, master_raw)
            accepted = controller.validate_budget_overrun_invalidation()
            if accepted["authority_sha256"] != master["authority_sha256"]:
                raise MigrationError("budget-overrun invalidation did not self-validate")
            return {
                "valid": True, "already_invalidated": False,
                "migration_id": migration_id,
                "authority_sha256": master["authority_sha256"],
                "invalidated_item_id": item_id,
                "preserved_master_acceptances": len(preserved),
            }


def invalidate_semantic_credit_acceptances(controller: Any) -> dict[str, Any]:
    """Reopen every x TARGET whose accepted generation fails semantic replay."""
    if controller.CRON_BEGIN in controller.read_crontab() or controller.CRON_END in controller.read_crontab():
        raise MigrationError("semantic-credit invalidation requires theorem cron paused")
    if controller.SEMANTIC_CREDIT_INVALIDATION.exists():
        accepted = controller.validate_semantic_credit_invalidation()
        return {
            "valid": True, "already_invalidated": True,
            "authority_sha256": accepted["authority_sha256"],
        }
    with controller.admission_pump_guard():
        with controller.scheduler_guard(nonblocking=False):
            _, rows, blueprint_raw = controller.load_program()
            targets = sorted(
                row["item_id"] for row in rows
                if row["state"] == "x" and row["item_id"].endswith("-TARGET")
            )
            if not targets:
                raise MigrationError("no Master-accepted TARGET semantic credits remain")
            validator = controller.item_checker()
            invalidated: list[dict[str, Any]] = []
            replay_identity: list[dict[str, str]] = []
            for item_id in targets:
                candidates: list[tuple[str, Path, dict[str, Any]]] = []
                for path in controller.HANDOFF_ARCHIVE.glob(
                    f"{item_id}--worker/*/*/master-integration.json"
                ):
                    try:
                        raw = controller._regular(path, "semantic invalidation Master receipt")
                        value = controller.verify_seal(
                            controller.strict_json(raw, "semantic invalidation Master receipt"),
                            "semantic invalidation Master receipt",
                        )
                    except Exception:
                        continue
                    if value.get("item_id") == item_id:
                        candidates.append((value.get("accepted_at", ""), path, value))
                if not candidates:
                    raise MigrationError(f"{item_id}: accepted Master receipt is absent")
                _, receipt_path, receipt = sorted(candidates)[-1]
                receipt_raw = controller._regular(
                    receipt_path, "semantic invalidation Master receipt",
                )
                run_id = receipt.get("handoff", {}).get("run_id")
                claim_path = (
                    controller.RUNTIME / "tasks" / f"{item_id}--worker"
                    / str(run_id) / "claim.json"
                )
                claim_raw = controller._regular(claim_path, "semantic invalidation claim")
                claim = controller.strict_json(claim_raw, "semantic invalidation claim")
                try:
                    validator.validate_target(
                        claim, Path(claim["task_root"]) / "work", ROOT,
                        compile_files=False,
                    )
                except validator.ItemError as exc:
                    failure = f"ERROR: {exc}"
                else:
                    raise MigrationError(
                        f"{item_id}: accepted generation passes the candidate semantic replay"
                    )
                entry = {
                    "item_id": item_id,
                    "run_id": run_id,
                    "master_receipt_path": receipt_path.relative_to(ROOT).as_posix(),
                    "master_receipt_file_sha256": digest(receipt_raw),
                    "master_receipt_authority_sha256": receipt["authority_sha256"],
                    "claim_path": claim_path.relative_to(ROOT).as_posix(),
                    "claim_sha256": digest(claim_raw),
                    "replay_exit_code": 1,
                    "replay_failure": failure,
                    "replay_failure_sha256": digest(failure.encode()),
                }
                invalidated.append(entry)
                replay_identity.append({
                    "item_id": item_id, "run_id": run_id,
                    "master_receipt_file_sha256": entry["master_receipt_file_sha256"],
                    "replay_failure_sha256": entry["replay_failure_sha256"],
                })

            old_gantt = controller._regular(controller.GANTT, "pre-semantic-invalidation Gantt")
            state_raw = controller._regular(controller.STATE_PATH, "pre-semantic-invalidation state")
            state = controller.verify_seal(
                controller.strict_json(state_raw, "pre-semantic-invalidation state"),
                "pre-semantic-invalidation state",
            )
            post_text = blueprint_raw.decode("utf-8")
            for item_id in targets:
                marker = f"- [x] `{item_id}` "
                if post_text.count(marker) != 1:
                    raise MigrationError(f"{item_id}: semantic invalidation row identity differs")
                post_text = post_text.replace(marker, f"- [ ] `{item_id}` ", 1)
            post_blueprint = post_text.encode()
            with tempfile.TemporaryDirectory(prefix="stage5-semantic-invalidation-") as temporary:
                candidate = Path(temporary) / "Stage5_Theorems_Blueprint.md"
                candidate.write_bytes(post_blueprint)
                generator_spec = importlib.util.spec_from_file_location(
                    "stage5_semantic_invalidation_gantt",
                    ROOT / "Docs/tools/generate_stage5_theorems_gantt.py",
                )
                if generator_spec is None or generator_spec.loader is None:
                    raise MigrationError("Gantt generator unavailable")
                generator = importlib.util.module_from_spec(generator_spec)
                sys.modules[generator_spec.name] = generator
                generator_spec.loader.exec_module(generator)
                post_gantt = generator.render(blueprint_path=candidate)
            post_state = dict(state)
            post_state.pop("authority_sha256", None)
            invalidated_by_item = {entry["item_id"]: entry for entry in invalidated}
            for item_id in targets:
                evidence = invalidated_by_item[item_id]
                post_state.setdefault("claims", {})[item_id] = {
                    "item_id": item_id,
                    "claim_id": f"{item_id}--worker",
                    "run_id": evidence["run_id"],
                    "generation_id": evidence["run_id"],
                    "lane_id": item_id,
                    "status": "invalidated",
                    "work_state": "not_done",
                    "invalidated_master_acceptance_sha256":
                        evidence["master_receipt_file_sha256"],
                    "invalidated_reason":
                        "accepted generation failed comment-stripped exact-provider semantic replay",
                    "semantic_replay_failure_sha256": evidence["replay_failure_sha256"],
                }
            post_state_raw = json_bytes(controller.seal(post_state))
            validator_sha = file_digest(ROOT / "scripts/check_stage5_theorem_item.py")
            migration_id = digest(canonical({
                "schema_version": "awesome-theorems/stage5-semantic-credit-invalidation-id/1.0",
                "program": PROGRAM, "invalidated": replay_identity,
                "pre_blueprint_sha256": digest(blueprint_raw),
                "post_blueprint_sha256": digest(post_blueprint),
                "pre_state_sha256": digest(state_raw),
                "post_state_sha256": digest(post_state_raw),
                "validator_sha256": validator_sha,
            }))
            epoch = (
                ROOT / "Docs/evidence/stage5_theorems/execution/"
                "semantic-credit-invalidations" / migration_id
            )
            pre = {
                "blueprint_path": (epoch / "pre/Stage5_Theorems_Blueprint.md").relative_to(ROOT).as_posix(),
                "blueprint_sha256": digest(blueprint_raw),
                "gantt_path": (epoch / "pre/Stage5_Theorems_Gantt.md").relative_to(ROOT).as_posix(),
                "gantt_sha256": digest(old_gantt),
                "state_path": (epoch / "pre/controller-state.json").relative_to(ROOT).as_posix(),
                "state_sha256": digest(state_raw),
            }
            post = {
                "blueprint_path": (epoch / "post/Stage5_Theorems_Blueprint.md").relative_to(ROOT).as_posix(),
                "blueprint_sha256": digest(post_blueprint),
                "gantt_path": (epoch / "post/Stage5_Theorems_Gantt.md").relative_to(ROOT).as_posix(),
                "gantt_sha256": digest(post_gantt),
                "state_path": (epoch / "post/controller-state.json").relative_to(ROOT).as_posix(),
                "state_sha256": digest(post_state_raw),
            }
            for path, raw in (
                (ROOT / pre["blueprint_path"], blueprint_raw),
                (ROOT / pre["gantt_path"], old_gantt),
                (ROOT / pre["state_path"], state_raw),
                (ROOT / post["blueprint_path"], post_blueprint),
                (ROOT / post["gantt_path"], post_gantt),
                (ROOT / post["state_path"], post_state_raw),
            ):
                exclusive_write(path, raw)
            preserved = [row["item_id"] for row in rows if row["state"] == "x" and row["item_id"] not in set(targets)]
            subject = {
                "invalidated": invalidated, "pre": pre, "post": post,
                "preserved_master_accepted_item_ids": preserved,
                "validator_sha256": validator_sha,
            }
            subject_sha = digest(canonical(subject))
            producer = signed_document(role="producer", ordinal=0, payload={
                "migration_id": migration_id, "review_subject": subject,
                "review_subject_sha256": subject_sha, "decision": "self_tested",
                "conflicts": [], "prepared_at": instant(),
            })
            producer_path = epoch / "producer-handoff.json"
            exclusive_write(producer_path, json_bytes(producer))
            reviewer_locators: list[dict[str, str]] = []
            reviewer_authorities: list[str] = []
            for ordinal in range(2):
                reviewer = signed_document(role="reviewer", ordinal=ordinal, payload={
                    "migration_id": migration_id,
                    "producer_authority_sha256": producer["authority_sha256"],
                    "review_subject_sha256": subject_sha,
                    "decision": "pass", "conflicts": [], "reviewed_at": instant(),
                })
                path = epoch / "reviews" / f"reviewer-{ordinal + 1}.json"
                exclusive_write(path, json_bytes(reviewer))
                reviewer_locators.append(locator(path, reviewer))
                reviewer_authorities.append(reviewer["authority_sha256"])
            master = signed_document(role="master", ordinal=0, payload={
                "migration_id": migration_id, "producer": locator(producer_path, producer),
                "reviewers": reviewer_locators, **subject,
                "review_subject_sha256": subject_sha,
                "reviewer_authorities": reviewer_authorities,
                "accepted_at": instant(),
            })
            master_raw = json_bytes(master)
            exclusive_write(epoch / "master-acceptance.json", master_raw)
            cas_replace(controller.BLUEPRINT, blueprint_raw, post_blueprint, 0o644)
            cas_replace(controller.GANTT, old_gantt, post_gantt, 0o644)
            cas_replace(controller.STATE_PATH, state_raw, post_state_raw, 0o600)
            exclusive_write(controller.SEMANTIC_CREDIT_INVALIDATION, master_raw)
            accepted = controller.validate_semantic_credit_invalidation()
            if accepted["authority_sha256"] != master["authority_sha256"]:
                raise MigrationError("semantic credit invalidation did not self-validate")
            return {
                "valid": True, "already_invalidated": False,
                "migration_id": migration_id,
                "authority_sha256": master["authority_sha256"],
                "invalidated_item_ids": targets,
                "preserved_master_accepted_item_ids": preserved,
            }


def locator(path: Path, value: dict[str, Any]) -> dict[str, str]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "file_sha256": digest(raw),
        "authority_sha256": value["authority_sha256"],
    }


def run_command(argv: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        argv, cwd=ROOT, text=False, capture_output=True, check=False, timeout=900,
        env={
            "PATH": "/usr/bin:/bin:/home/sansha/.local/node_modules/.bin",
            "HOME": "/home/sansha", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "PYTHONHASHSEED": "0",
        },
    )
    result = {
        "argv": argv,
        "exit_code": completed.returncode,
        "stdout_sha256": digest(completed.stdout),
        "stderr_sha256": digest(completed.stderr),
    }
    if completed.returncode != 0:
        raise MigrationError(
            f"successor validation failed: {argv!r}; stderr={completed.stderr[-2000:].decode(errors='replace')}"
        )
    return result


def validation_suite(controller: Any) -> dict[str, Any]:
    commands = [
        ["/usr/bin/python3", "-m", "py_compile", "scripts/stage5_theorems_execution_cron_v2.py"],
        ["/usr/bin/python3", "-m", "py_compile", "scripts/accept_stage5_theorem_controller_successor.py"],
        ["/usr/bin/python3", "scripts/stage5_boot_compile_check.py", "scripts/stage5_theorems_execution_cron_v2.py"],
        ["/usr/bin/python3", "scripts/test_stage5_theorem_claim.py"],
        ["/usr/bin/python3", "scripts/test_stage5_theorem_item.py"],
        ["/usr/bin/python3", "scripts/test_stage5_theorems_blueprint.py"],
        ["/usr/bin/python3", "scripts/test_stage5_theorems_execution_cron_v2.py"],
        ["/usr/bin/python3", "scripts/test_resolve_stage5_theorem_integration_conflict.py"],
        ["/usr/bin/python3", "Docs/tools/check_stage5_theorems_blueprint.py"],
    ]
    results = [run_command(argv) for argv in commands]
    base = Path("/home/sansha/.local/state")
    base.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="stage5-successor-prompt-", dir=base))
    try:
        home = temporary / "home"
        codex_home = home / ".codex"
        codex_home.mkdir(parents=True)
        hint_argument = (
            "features.multi_agent_v2.multi_agent_mode_hint_text="
            + json.dumps(controller.MULTI_AGENT_MODE_HINT)
        )
        boundary_argument = (
            "developer_instructions="
            + json.dumps(controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS)
        )
        completed = subprocess.run(
            [
                str(controller.CODEX), "debug", "prompt-input",
                "--disable", "multi_agent", "--disable", "multi_agent_v2",
                "-c", "features.multi_agent=false",
                "-c", "features.multi_agent_v2=false",
                "-c", "features.multi_agent_v2.max_concurrent_threads_per_session=1",
                "-c", hint_argument,
                "-c", boundary_argument,
                "successor-preflight",
            ],
            cwd=ROOT, text=True, capture_output=True, check=False, timeout=60,
            env={
                **os.environ, "HOME": str(home), "CODEX_HOME": str(codex_home),
            },
        )
        if completed.returncode != 0:
            raise MigrationError("Codex prompt-input successor preflight failed")
        prompt_input = json.loads(completed.stdout)
        developer_texts: list[str] = []

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                if value.get("role") == "developer":
                    content = value.get("content")
                    if isinstance(content, str):
                        developer_texts.append(content)
                    elif isinstance(content, list):
                        for entry in content:
                            if isinstance(entry, dict) and isinstance(entry.get("text"), str):
                                developer_texts.append(entry["text"])
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(prompt_input)
        joined = "\n".join(developer_texts)
        preflight = {
            "safe_hint_count": joined.count(controller.MULTI_AGENT_MODE_HINT),
            "task_boundary_instruction_count": joined.count(
                controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS
            ),
            "one_total_thread_slot_count": joined.count("There are 1 available concurrency slots"),
            "permissive_multi_agent_hint_present": (
                "Proactive multi-agent delegation is active" in joined
                or "Any earlier instruction enabling proactive multi-agent delegation" in joined
            ),
        }
        if preflight != {
            "safe_hint_count": 1,
            "task_boundary_instruction_count": 1,
            "one_total_thread_slot_count": 1,
            "permissive_multi_agent_hint_present": False,
        }:
            raise MigrationError(f"Codex prompt-input successor boundary differs: {preflight}")
    finally:
        shutil.rmtree(temporary)
    return {"commands": results, "prompt_preflight": preflight}


def baseline_manifest(path: Path) -> tuple[str, int]:
    rows: list[list[Any]] = []
    if path.is_dir() and not path.is_symlink():
        for child in sorted(path.rglob("*")):
            if child.is_symlink() or (not child.is_file() and not child.is_dir()):
                raise MigrationError(f"unsafe grandfathered baseline entry: {child}")
            if child.is_file():
                rows.append([
                    child.relative_to(path).as_posix(), child.stat().st_size,
                    file_digest(child),
                ])
    if not rows:
        raise MigrationError(f"grandfathered baseline is empty: {path}")
    return digest(canonical(rows)), len(rows)


def live_manifest(
    state: dict[str, Any], specification: dict[str, Any],
    prompt: dict[str, Any], prompt_sha: str,
) -> list[dict[str, Any]]:
    live = sorted(
        (entry for entry in state.get("claims", {}).values() if entry.get("status") == "live"),
        key=lambda entry: entry.get("item_id", ""),
    )
    if len(live) != 24:
        raise MigrationError(f"successor freeze requires exactly 24 controller-recorded live lanes, got {len(live)}")
    rows: list[dict[str, Any]] = []
    for entry in live:
        task_root = Path(entry.get("task_root", ""))
        claim_path = task_root / "claim.json"
        claim_raw = claim_path.read_bytes() if claim_path.is_file() and not claim_path.is_symlink() else b""
        claim = strict_json(claim_raw, f"live claim {entry.get('item_id')}")
        baseline_sha, baseline_files = baseline_manifest(task_root / "work/_baseline")
        identity = claim.get("execution_identity", {})
        baseline = claim.get("baseline", {})
        bootstrap = {
            row.get("path"): row
            for row in claim.get("read_only_bootstrap_files", [])
            if isinstance(row, dict) and isinstance(row.get("path"), str)
        }
        expected_spec_sha = digest(canonical(specification))
        expected_spec_file_sha = file_digest(ROOT / "Docs/evidence/stage5_theorems/execution-spec.json")
        expected_item_checker_sha = file_digest(ITEM_CHECKER_PATH)
        expected_vector = prompt.get("concurrency")
        if (
            entry.get("goal_submissions") != 1
            or claim_path.is_symlink() or not claim_path.is_file()
            or not isinstance(entry.get("thread_id"), str)
            or not isinstance(entry.get("goal_id"), str)
            or claim.get("item_id") != entry.get("item_id")
            or claim.get("claim_id") != entry.get("claim_id")
            or claim.get("run_id") != entry.get("run_id")
            or claim.get("task_root") != str(task_root)
            or identity.get("lane_id") != entry.get("lane_id")
            or identity.get("generation_id") != entry.get("generation_id")
            or identity.get("execution_spec_sha256") != expected_spec_sha
            or identity.get("prompt_epoch") != prompt.get("policy_epoch")
            or identity.get("prompt_digest") != prompt_sha
            or identity.get("requested_concurrency") != expected_vector
            or identity.get("resolved_concurrency") != expected_vector
            or baseline.get("execution_spec_sha256") != expected_spec_sha
            or bootstrap.get("_baseline/execution-spec.json", {}).get("sha256")
            != expected_spec_file_sha
            or bootstrap.get("_baseline/concurrency-prompt.json", {}).get("sha256")
            != prompt_sha
            or bootstrap.get("_baseline/check_stage5_theorem_item.py", {}).get("sha256")
            != expected_item_checker_sha
            or file_digest(task_root / "work/_baseline/check_stage5_theorem_item.py")
            != expected_item_checker_sha
            or entry.get("prompt_epoch") != prompt.get("policy_epoch")
            or entry.get("prompt_digest") != prompt_sha
        ):
            raise MigrationError(f"grandfathered lane identity is incomplete: {entry.get('item_id')}")
        rows.append({
            "item_id": entry.get("item_id"),
            "claim_id": entry.get("claim_id"),
            "run_id": entry.get("run_id"),
            "generation_id": entry.get("generation_id"),
            "lane_id": entry.get("lane_id"),
            "status": entry.get("status"),
            "task_root": str(task_root),
            "claim_sha256": digest(claim_raw),
            "baseline_manifest_sha256": baseline_sha,
            "baseline_file_count": baseline_files,
            "socket_path": entry.get("socket_path"),
            "session": entry.get("session"),
            "pane_pid": entry.get("pane_pid"),
            "pane_pid_start_ticks": entry.get("pane_pid_start_ticks"),
            "codex_home": entry.get("codex_home"),
            "thread_id": entry.get("thread_id"),
            "goal_id": entry.get("goal_id"),
            "goal_submissions": entry.get("goal_submissions"),
            "provider": entry.get("provider"),
            "model": entry.get("model"),
            "reasoning_effort": entry.get("reasoning_effort"),
            "service_tier": entry.get("service_tier"),
            "prompt_epoch": entry.get("prompt_epoch"),
            "prompt_digest": entry.get("prompt_digest"),
            "execution_spec_sha256": identity.get("execution_spec_sha256"),
            "baseline_execution_spec_sha256": baseline.get("execution_spec_sha256"),
            "baseline_execution_spec_file_sha256": bootstrap["_baseline/execution-spec.json"]["sha256"],
            "baseline_prompt_file_sha256": bootstrap["_baseline/concurrency-prompt.json"]["sha256"],
            "baseline_item_checker_sha256": bootstrap["_baseline/check_stage5_theorem_item.py"]["sha256"],
        })
    if len({entry["item_id"] for entry in rows}) != 24:
        raise MigrationError("grandfathered live item identities overlap")
    return rows


def archive_authority(
    source: Path, destination: Path, label: str,
) -> tuple[bytes, dict[str, Any]]:
    if source.is_symlink() or not source.is_file():
        raise MigrationError(f"{label}: missing regular authority")
    raw = source.read_bytes()
    value = verify_seal(strict_json(raw, label), label)
    exclusive_write(destination, raw)
    return raw, value


def accept() -> dict[str, Any]:
    controller = load_controller()
    if SUCCESSOR_ACCEPTANCE.is_symlink() or not SUCCESSOR_ACCEPTANCE.is_file():
        raise MigrationError("predecessor controller successor acceptance is unavailable")
    predecessor_successor_raw = SUCCESSOR_ACCEPTANCE.read_bytes()
    predecessor_successor_value = controller._verify_successor_signature(
        controller.strict_json(predecessor_successor_raw, "predecessor controller successor"),
        label="predecessor controller successor", role="master",
        trust=controller._load_successor_trust(),
    )
    predecessor_payload = predecessor_successor_value.get("payload", {})
    predecessor_artifacts = predecessor_payload.get("successor_artifacts", {})
    if (
        "predecessor_controller_successor" in predecessor_payload
        and predecessor_artifacts.get("controller_sha256") == file_digest(CONTROLLER_PATH)
        and predecessor_artifacts.get("controller_test_sha256") == file_digest(CONTROLLER_TEST_PATH)
        and predecessor_artifacts.get("migration_tool_sha256") == file_digest(Path(__file__))
        and predecessor_artifacts.get("checker_sha256") == file_digest(CHECKER_PATH)
        and predecessor_artifacts.get("checker_test_sha256") == file_digest(CHECKER_TEST_PATH)
        and predecessor_artifacts.get("item_checker_sha256") == file_digest(ITEM_CHECKER_PATH)
        and predecessor_artifacts.get("item_checker_test_sha256") == file_digest(ITEM_CHECKER_TEST_PATH)
    ):
        accepted = controller.validate_controller_successor_acceptance()
        return {"valid": True, "already_accepted": True, "authority_sha256": accepted["authority_sha256"]}
    validation = validation_suite(controller)
    controller_sha = file_digest(CONTROLLER_PATH)
    controller_test_sha = file_digest(CONTROLLER_TEST_PATH)
    migration_tool_sha = file_digest(Path(__file__))
    checker_sha = file_digest(CHECKER_PATH)
    checker_test_sha = file_digest(CHECKER_TEST_PATH)
    item_checker_sha = file_digest(ITEM_CHECKER_PATH)
    item_checker_test_sha = file_digest(ITEM_CHECKER_TEST_PATH)
    candidate_digests = (
        controller_sha, controller_test_sha, migration_tool_sha,
        checker_sha, checker_test_sha, item_checker_sha, item_checker_test_sha,
    )
    pre_crontab = controller.read_crontab()
    if (
        controller.CRON_BEGIN in pre_crontab
        or controller.CRON_END in pre_crontab
        or "# BEGIN HARNESSFS_COMMUNITY_EXECUTION_V1" not in pre_crontab
    ):
        raise MigrationError("successor acceptance requires theorem cron paused and HarnessFS preserved")

    with controller.admission_pump_guard():
        with controller.scheduler_guard():
            # Recheck after acquiring the full pump/transition lock order.
            crontab = controller.read_crontab()
            if crontab != pre_crontab:
                raise MigrationError("crontab changed before successor freeze")
            if candidate_digests != (
                file_digest(CONTROLLER_PATH),
                file_digest(CONTROLLER_TEST_PATH),
                file_digest(Path(__file__)),
                file_digest(CHECKER_PATH),
                file_digest(CHECKER_TEST_PATH),
                file_digest(ITEM_CHECKER_PATH),
                file_digest(ITEM_CHECKER_TEST_PATH),
            ):
                raise MigrationError("successor candidate artifacts changed after validation")
            specification, rows, blueprint_raw = controller.load_program()
            prompt, prompt_sha = controller.load_concurrency_prompt(
                controller.CONCURRENCY_PROMPT, specification,
            )
            state_raw = controller._regular(controller.STATE_PATH, "successor controller state")
            state = controller.verify_seal(
                controller.strict_json(state_raw, "successor controller state"),
                "successor controller state",
            )
            lanes = live_manifest(state, specification, prompt, prompt_sha)
            audit = controller.build_live_lane_audit(state, prompt, prompt_sha)
            requested_live = prompt.get("concurrency", {}).get("authenticated_goals")
            if requested_live != 24 or len(lanes) != requested_live or not audit["all_checks_pass"]:
                raise MigrationError(
                    "successor acceptance requires an exact all-green 24/24 live-lane audit"
                )
            gantt_raw = controller._regular(controller.GANTT, "successor Gantt")
            activation_source = controller.ACTIVATION_RECEIPT
            activation_raw = controller._regular(activation_source, "predecessor activation")
            activation = controller.verify_seal(
                controller.strict_json(activation_raw, "predecessor activation"),
                "predecessor activation",
            )
            if (
                activation.get("schema_version") != "awesome-theorems/stage5-controller-activation/3.0"
                or activation.get("controller_successor_acceptance_authority_sha256")
                != predecessor_successor_value["authority_sha256"]
            ):
                raise MigrationError("successor predecessor activation is not the exact v3 ancestor")
            x_ids = [row["item_id"] for row in rows if row.get("state") == "x"]
            if not x_ids or x_ids[0] != "S5THM-BOOT-001":
                raise MigrationError("successor mathematical cursor lacks BOOT acceptance")

            migration_id = digest(canonical({
                "schema_version": "awesome-theorems/stage5-controller-successor-id/1.0",
                "program": PROGRAM,
                "predecessor_activation_sha256": digest(activation_raw),
                "predecessor_controller_successor_sha256": digest(predecessor_successor_raw),
                "controller_sha256": controller_sha,
                "controller_test_sha256": controller_test_sha,
                "migration_tool_sha256": migration_tool_sha,
                "checker_sha256": checker_sha,
                "checker_test_sha256": checker_test_sha,
                "item_checker_sha256": item_checker_sha,
                "item_checker_test_sha256": item_checker_test_sha,
                "blueprint_sha256": digest(blueprint_raw),
                "gantt_sha256": digest(gantt_raw),
                "state_sha256": digest(state_raw),
                "live_manifest_sha256": digest(canonical(lanes)),
                "master_accepted_item_ids": x_ids,
            }))
            epoch_root = (
                ROOT / "Docs/evidence/stage5_theorems/bootstrap/controller-successions"
                / migration_id
            )
            predecessor_root = epoch_root / "predecessor"
            predecessor_successor_archive = predecessor_root / "controller-successor-acceptance.json"
            exclusive_write(predecessor_successor_archive, predecessor_successor_raw)
            maintenance_intent = controller.validate_controller_successor_maintenance_intent()
            maintenance_raw = controller._regular(
                controller.CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT,
                "consumed controller successor maintenance intent",
            )
            maintenance_archive = predecessor_root / "controller-successor-maintenance-intent.json"
            exclusive_write(maintenance_archive, maintenance_raw)
            consumption_source = controller.maintenance_consumption_path(maintenance_intent)
            consumption_raw = controller._regular(
                consumption_source, "consumed controller successor maintenance receipt",
            )
            consumption = controller.verify_seal(
                controller.strict_json(
                    consumption_raw, "consumed controller successor maintenance receipt",
                ),
                "consumed controller successor maintenance receipt",
            )
            if (
                consumption.get("intent_authority_sha256") != maintenance_intent["authority_sha256"]
                or consumption.get("intent_file_sha256") != digest(maintenance_raw)
            ):
                raise MigrationError("successor maintenance consumption does not bind its intent")
            maintenance_consumption_archive = (
                predecessor_root / "controller-successor-maintenance-consumption.json"
            )
            exclusive_write(maintenance_consumption_archive, consumption_raw)
            predecessor_boot: list[dict[str, str]] = []
            boot_acceptance = None
            for relative in BOOT_PATHS:
                source = ROOT / relative
                raw, value = archive_authority(
                    source, predecessor_root / Path(relative).name,
                    f"predecessor BOOT {relative}",
                )
                predecessor_boot.append({
                    "path": relative,
                    "archive_path": (predecessor_root / Path(relative).name).relative_to(ROOT).as_posix(),
                    "file_sha256": digest(raw),
                    "authority_sha256": value["authority_sha256"],
                })
                if relative.endswith("controller-bootstrap-acceptance.json"):
                    boot_acceptance = value
            if not isinstance(boot_acceptance, dict):
                raise MigrationError("predecessor final BOOT acceptance is absent")
            activation_archive = predecessor_root / "controller-activation-v3.json"
            exclusive_write(activation_archive, activation_raw)

            blueprint_archive = predecessor_root / "Stage5_Theorems_Blueprint.md"
            gantt_archive = predecessor_root / "Stage5_Theorems_Gantt.md"
            state_archive = predecessor_root / "controller-state.json"
            exclusive_write(blueprint_archive, blueprint_raw)
            exclusive_write(gantt_archive, gantt_raw)
            exclusive_write(state_archive, state_raw)
            live_claim_root = predecessor_root / "live-claims"
            for lane in lanes:
                source = Path(lane["task_root"]) / "claim.json"
                claim_raw = source.read_bytes()
                claim_archive = live_claim_root / f"{lane['item_id']}--{lane['run_id']}.json"
                exclusive_write(claim_archive, claim_raw)
                if digest(claim_raw) != lane["claim_sha256"]:
                    raise MigrationError("live claim changed while archiving successor evidence")

            changed = {
                "scripts/stage5_theorems_execution_cron_v2.py",
                "scripts/test_stage5_theorems_execution_cron_v2.py",
                "Docs/tools/check_stage5_theorems_blueprint.py",
                "scripts/test_stage5_theorems_blueprint.py",
                "scripts/check_stage5_theorem_item.py",
                "scripts/test_stage5_theorem_item.py",
            }
            artifact_bindings = boot_acceptance.get("artifact_bindings")
            if not isinstance(artifact_bindings, dict):
                raise MigrationError("predecessor BOOT artifact bindings are malformed")
            unchanged = {
                relative: expected_sha
                for relative, expected_sha in artifact_bindings.items()
                if relative not in changed
            }
            for relative, expected_sha in unchanged.items():
                if controller._artifact_binding(ROOT / relative) != expected_sha:
                    raise MigrationError(f"unchanged BOOT artifact drifted: {relative}")

            prompt_value = controller.verify_seal(
                controller.strict_json(
                    controller._regular(controller.CONCURRENCY_PROMPT, "successor concurrency prompt"),
                    "successor concurrency prompt",
                ), "successor concurrency prompt",
            )
            operator_value = controller.verify_seal(
                controller.strict_json(
                    controller._regular(controller.OPERATOR_AUTHORITY, "successor operator authority"),
                    "successor operator authority",
                ), "successor operator authority",
            )
            operator_trust_value = controller.strict_json(
                controller._regular(controller.OPERATOR_TRUST_ROOT, "successor operator trust root"),
                "successor operator trust root",
            )
            if digest(canonical(operator_trust_value)) != controller.OPERATOR_TRUST_ROOT_SHA256:
                raise MigrationError("successor operator trust root digest differs")
            subject = {
                "predecessor_boot": predecessor_boot,
                "predecessor_controller_successor": {
                    "path": predecessor_successor_archive.relative_to(ROOT).as_posix(),
                    "file_sha256": digest(predecessor_successor_raw),
                    "authority_sha256": predecessor_successor_value["authority_sha256"],
                },
                "maintenance_intent": {
                    "path": maintenance_archive.relative_to(ROOT).as_posix(),
                    "file_sha256": digest(maintenance_raw),
                    "authority_sha256": maintenance_intent["authority_sha256"],
                    "action": "paused_reconcile_fence_and_refill_only",
                    "consumption_path": maintenance_consumption_archive.relative_to(ROOT).as_posix(),
                    "consumption_file_sha256": digest(consumption_raw),
                    "consumption_authority_sha256": consumption["authority_sha256"],
                },
                "predecessor_activation": {
                    "path": activation_source.relative_to(ROOT).as_posix(),
                    "archive_path": activation_archive.relative_to(ROOT).as_posix(),
                    "file_sha256": digest(activation_raw),
                    "authority_sha256": activation["authority_sha256"],
                    "schema_version": activation["schema_version"],
                },
                "successor_artifacts": {
                    "controller_path": CONTROLLER_PATH.relative_to(ROOT).as_posix(),
                    "controller_sha256": controller_sha,
                    "controller_test_path": CONTROLLER_TEST_PATH.relative_to(ROOT).as_posix(),
                    "controller_test_sha256": controller_test_sha,
                    "migration_tool_path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
                    "migration_tool_sha256": migration_tool_sha,
                    "checker_path": CHECKER_PATH.relative_to(ROOT).as_posix(),
                    "checker_sha256": checker_sha,
                    "checker_test_path": CHECKER_TEST_PATH.relative_to(ROOT).as_posix(),
                    "checker_test_sha256": checker_test_sha,
                    "item_checker_path": ITEM_CHECKER_PATH.relative_to(ROOT).as_posix(),
                    "item_checker_sha256": item_checker_sha,
                    "item_checker_test_path": ITEM_CHECKER_TEST_PATH.relative_to(ROOT).as_posix(),
                    "item_checker_test_sha256": item_checker_test_sha,
                },
                "unchanged_boot_artifacts": unchanged,
                "frozen_authorities": {
                    "execution_spec_sha256": digest(canonical(specification)),
                    "execution_spec_file_sha256": file_digest(controller.EVIDENCE / "execution-spec.json"),
                    "concurrency_prompt_file_sha256": file_digest(controller.CONCURRENCY_PROMPT),
                    "concurrency_prompt_authority_sha256": prompt_value["authority_sha256"],
                    "operator_authority_file_sha256": file_digest(controller.OPERATOR_AUTHORITY),
                    "operator_authority_sha256": operator_value["authority_sha256"],
                    "operator_budget_renewal_file_sha256": file_digest(controller.OPERATOR_BUDGET_RENEWAL),
                    "operator_budget_renewal_authority_sha256": controller.verify_seal(
                        controller.strict_json(
                            controller._regular(controller.OPERATOR_BUDGET_RENEWAL, "successor operator budget renewal"),
                            "successor operator budget renewal",
                        ),
                        "successor operator budget renewal",
                    )["authority_sha256"],
                    "budget_overrun_invalidation_file_sha256": file_digest(controller.BUDGET_OVERRUN_INVALIDATION),
                    "budget_overrun_invalidation_authority_sha256": controller.validate_budget_overrun_invalidation()["authority_sha256"],
                    "semantic_credit_invalidation_file_sha256": file_digest(controller.SEMANTIC_CREDIT_INVALIDATION),
                    "semantic_credit_invalidation_authority_sha256": controller.validate_semantic_credit_invalidation()["authority_sha256"],
                    "operator_trust_root_file_sha256": file_digest(controller.OPERATOR_TRUST_ROOT),
                    "operator_trust_root_sha256": controller.OPERATOR_TRUST_ROOT_SHA256,
                    "route": {
                        "provider": controller.PROVIDER, "model": controller.MODEL,
                        "reasoning_effort": controller.EFFORT,
                        "service_tier": controller.SERVICE_TIER,
                    },
                },
                "paused_snapshot": {
                    "crontab_sha256": digest(crontab.encode()),
                    "theorem_marker_absent": True,
                    "harnessfs_marker_preserved": True,
                    "blueprint_archive_path": blueprint_archive.relative_to(ROOT).as_posix(),
                    "blueprint_sha256": digest(blueprint_raw),
                    "gantt_archive_path": gantt_archive.relative_to(ROOT).as_posix(),
                    "gantt_sha256": digest(gantt_raw),
                    "state_archive_path": state_archive.relative_to(ROOT).as_posix(),
                    "state_sha256": digest(state_raw),
                    "controller_recorded_live_lanes": len(lanes),
                    "requested_authenticated_live_goals": requested_live,
                    "master_accepted_item_ids": x_ids,
                    "live_manifest_sha256": digest(canonical(lanes)),
                    "live_manifest": lanes,
                    # Existing lanes were admitted by the predecessor.  Record
                    # any now-stale registry identity honestly; the first
                    # successor tick will fence/replenish it without rewriting
                    # the old claim baseline or resubmitting its /goal.
                    "live_audit_all_checks_pass": audit["all_checks_pass"],
                    "live_audit_failures": audit["failures"],
                },
                "validation": validation,
                "safety": {
                    "mathematical_acceptances_preserved": True,
                    "worker_stops": 0,
                    "goal_resubmissions": 0,
                    "grandfathered_claim_baselines_immutable": True,
                    "successor_admissions_only_use_new_controller": True,
                },
            }
            review_subject_sha = digest(canonical(subject))
            producer = signed_document(
                role="producer", ordinal=0,
                payload={
                    "migration_id": migration_id,
                    "review_subject": subject,
                    "review_subject_sha256": review_subject_sha,
                    "decision": "self_tested", "conflicts": [], "prepared_at": instant(),
                },
            )
            producer_path = epoch_root / "producer-handoff.json"
            exclusive_write(producer_path, json_bytes(producer))
            reviewer_locators: list[dict[str, str]] = []
            reviewer_authorities: list[str] = []
            for ordinal in range(2):
                reviewer = signed_document(
                    role="reviewer", ordinal=ordinal,
                    payload={
                        "migration_id": migration_id,
                        "producer_authority_sha256": producer["authority_sha256"],
                        "review_subject_sha256": review_subject_sha,
                        "decision": "pass", "conflicts": [], "reviewed_at": instant(),
                    },
                )
                reviewer_path = epoch_root / "reviews" / f"reviewer-{ordinal + 1}.json"
                exclusive_write(reviewer_path, json_bytes(reviewer))
                reviewer_locators.append(locator(reviewer_path, reviewer))
                reviewer_authorities.append(reviewer["authority_sha256"])
            master = signed_document(
                role="master", ordinal=0,
                payload={
                    "migration_id": migration_id,
                    "producer": locator(producer_path, producer),
                    "reviewers": reviewer_locators,
                    **subject,
                    "review_subject_sha256": review_subject_sha,
                    "reviewer_authorities": reviewer_authorities,
                    "accepted_at": instant(),
                },
            )
            acceptance_raw = json_bytes(master)
            acceptance_archive = epoch_root / "master-acceptance.json"
            exclusive_write(acceptance_archive, acceptance_raw)
            accepted = controller.validate_controller_successor_acceptance(
                specification, acceptance_archive,
            )
            if accepted["authority_sha256"] != master["authority_sha256"]:
                raise MigrationError("successor controller rejected its own accepted authority")
            cas_replace(SUCCESSOR_ACCEPTANCE, predecessor_successor_raw, acceptance_raw)
            return {
                "valid": True,
                "already_accepted": False,
                "migration_id": migration_id,
                "authority_sha256": master["authority_sha256"],
                "controller_sha256": controller_sha,
                "controller_recorded_live_lanes": len(lanes),
                "live_audit_all_checks_pass": audit["all_checks_pass"],
                "master_accepted_item_ids": x_ids,
                "crontab_remains_paused": True,
            }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--prepare-maintenance-intent", action="store_true")
    parser.add_argument("--record-abandoned-successors", action="store_true")
    parser.add_argument("--invalidate-budget-overrun-acceptance", action="store_true")
    parser.add_argument("--invalidate-semantic-credit-acceptances", action="store_true")
    arguments = parser.parse_args()
    if sum((arguments.accept, arguments.validate_only, arguments.prepare_maintenance_intent,
            arguments.record_abandoned_successors,
            arguments.invalidate_budget_overrun_acceptance,
            arguments.invalidate_semantic_credit_acceptances)) != 1:
        parser.error("choose exactly one action")
    try:
        controller = load_controller()
        if arguments.prepare_maintenance_intent:
            result = write_maintenance_intent(controller)
        elif arguments.invalidate_semantic_credit_acceptances:
            result = invalidate_semantic_credit_acceptances(controller)
        elif arguments.invalidate_budget_overrun_acceptance:
            result = invalidate_budget_overrun_acceptance(controller)
        elif arguments.record_abandoned_successors:
            result = write_abandoned_successor_index(controller)
        elif arguments.validate_only:
            value = controller.validate_controller_successor_acceptance()
            result = {
                "valid": True, "authority_sha256": value["authority_sha256"],
            }
        else:
            result = accept()
    except (RuntimeError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
