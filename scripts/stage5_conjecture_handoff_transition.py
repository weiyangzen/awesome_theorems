#!/usr/bin/env python3
"""Publish conjecture handoff and canonical Master acceptance transitions.

This is the conjecture-program counterpart of the theorem handoff transition.
It validates an already-harvested, content-addressed worker result, prepares a
fresh same-name Gantt projection, and atomically publishes both projections.
The default operation publishes ``[ ]`` -> ``[_]`` without applying a patch.
``--accept`` is the distinct canonical-Master operation: it revalidates the
immutable archive, atomically publishes exact owned artifacts, Blueprint,
same-name Gantt and a content-addressed acceptance receipt, then writes ``[x]``.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
from pathlib import PurePosixPath
import sys
import tempfile
import uuid
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "Docs/Stage5_Conjectures_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Conjectures_Gantt.md"
EVIDENCE = ROOT / "Docs/evidence/stage5_conjectures/execution/transitions"
ACCEPTANCES = ROOT / "Docs/evidence/stage5_conjectures/execution/acceptances"
PROGRAM = "stage5-conjecture-proof-debt/2.0"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(value: dict) -> dict:
    body = dict(value)
    body["authority_sha256"] = digest(canonical(value))
    return body


def regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"{label}: missing regular file")
    return path.read_bytes()


def safe_relative(value: str, label: str) -> str:
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or value != path.as_posix()
        or "." in path.parts or ".." in path.parts
    ):
        raise RuntimeError(f"{label}: unsafe repository-relative path {value!r}")
    return value


def verify_seal(value: object, label: str) -> dict:
    if not isinstance(value, dict) or not isinstance(value.get("authority_sha256"), str):
        raise RuntimeError(f"{label}: malformed authority")
    body = dict(value); authority = body.pop("authority_sha256")
    if digest(canonical(body)) != authority:
        raise RuntimeError(f"{label}: authority mismatch")
    return value


def load_controller():
    path = ROOT / "scripts/stage5_conjectures_execution_cron_v2.py"
    spec = importlib.util.spec_from_file_location("stage5_conjecture_controller", path)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load conjecture controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_boot_authority(checker) -> None:
    """Fail before any cursor/runtime mutation unless current BOOT is valid."""
    _, rows, _ = checker.parse_blueprint()
    checker.validate()
    boot_rows = [row for row in rows if row.get("item_id") == "S5CON-BOOT-001"]
    if len(boot_rows) != 1 or boot_rows[0].get("state") != "x":
        raise RuntimeError(
            "conjecture BOOT must be Master accepted before handoff integration"
        )


def result_and_claim(controller, item_id: str) -> tuple[Path, Path, dict]:
    state = controller.load_state(False)
    if state.get("runtime_authority_epoch") != controller.RUNTIME_AUTHORITY_EPOCH:
        raise RuntimeError("controller state belongs to a historical runtime authority epoch")
    record = state.get("claims", {}).get(item_id)
    if not isinstance(record, dict) or record.get("status") != "handoff_ready":
        raise RuntimeError(f"{item_id}: no harvested handoff_ready record")
    if record.get("runtime_authority_epoch") != controller.RUNTIME_AUTHORITY_EPOCH:
        raise RuntimeError(f"{item_id}: handoff belongs to a historical runtime authority epoch")
    archive = Path(record["handoff"]["archive"])
    task_root = Path(record["task_root"])
    result_path = task_root / "work/_outbox/result.json"
    claim_path = task_root / "claim.json"
    claim_value = json.loads(claim_path.read_text())
    if "work_contract" not in claim_value:
        raise RuntimeError(f"{item_id}: legacy handoff lacks current discriminated work contract")
    result = controller.claim_checker_module().validate_result(result_path, claim_path)
    if result.get("item_id") != item_id or result.get("status") != "self_tested":
        raise RuntimeError(f"{item_id}: worker result is not exact self-tested handoff")
    archived_result = archive / "result.json"
    if digest(archived_result.read_bytes()) != digest(result_path.read_bytes()):
        raise RuntimeError(f"{item_id}: archived result differs from source result")
    return result_path, claim_path, record


def prepare_gantt(
    post_blueprint: bytes,
    checker,
    generated_at: str | None = None,
) -> bytes:
    generator_path = ROOT / "Docs/tools/generate_stage5_conjectures_gantt.py"
    spec = importlib.util.spec_from_file_location("stage5_conjecture_gantt_transition", generator_path)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load conjecture Gantt generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.NamedTemporaryFile(
        prefix=".Stage5_Conjectures_Blueprint.", dir=BLUEPRINT.parent, delete=False
    ) as stream:
        stream.write(post_blueprint)
        temporary = Path(stream.name)
    try:
        checker.parse_blueprint(temporary)
        module.BLUEPRINT = temporary
        return module.render(generated_at)
    finally:
        temporary.unlink(missing_ok=True)


def transition_receipt(item_id: str, record: dict) -> tuple[Path, dict]:
    candidates: list[tuple[Path, dict]] = []
    root = EVIDENCE / item_id
    for path in sorted(root.glob("*.json")) if root.is_dir() else []:
        try:
            value = verify_seal(json.loads(regular(path, "handoff transition")), "handoff transition")
        except (OSError, ValueError, RuntimeError, json.JSONDecodeError):
            continue
        handoff = value.get("handoff", {})
        if (
            value.get("program") == PROGRAM
            and value.get("item_id") == item_id
            and value.get("runtime_authority_epoch") == record.get("runtime_authority_epoch")
            and handoff.get("claim_id") == record.get("claim_id")
            and handoff.get("run_id") == record.get("run_id")
            and handoff.get("immutable_archive")
            == str(Path(record["handoff"]["archive"]).relative_to(ROOT))
        ):
            candidates.append((path, value))
    if len(candidates) != 1:
        raise RuntimeError(f"{item_id}: exact reviewed handoff transition is missing or ambiguous")
    return candidates[0]


def archived_bundle(controller, item_id: str) -> tuple[dict, dict, dict, Path, dict]:
    state = controller.load_state(False)
    if state.get("runtime_authority_epoch") != controller.RUNTIME_AUTHORITY_EPOCH:
        raise RuntimeError("controller state belongs to a historical runtime authority epoch")
    record = state.get("claims", {}).get(item_id)
    if not isinstance(record, dict) or record.get("status") != "handoff_ready":
        raise RuntimeError(f"{item_id}: no current harvested handoff_ready record")
    if record.get("runtime_authority_epoch") != controller.RUNTIME_AUTHORITY_EPOCH:
        raise RuntimeError(f"{item_id}: handoff belongs to a historical runtime authority epoch")
    archive = Path(record["handoff"]["archive"])
    manifest_raw = regular(archive / "harvest-manifest.json", "harvest manifest")
    manifest = verify_seal(json.loads(manifest_raw), "harvest manifest")
    claim = json.loads(regular(archive / "claim.json", "archived claim"))
    result = verify_seal(json.loads(regular(archive / "result.json", "archived result")), "archived result")
    patch_raw = regular(archive / "changes.patch", "archived patch")
    if (
        manifest.get("schema_version") != "awesome-theorems/stage5-harvest-manifest/1.1"
        or manifest.get("item_id") != item_id
        or manifest.get("claim_id") != record.get("claim_id")
        or manifest.get("run_id") != record.get("run_id")
        or manifest.get("baseline_sha256") != result.get("baseline_sha256")
        or manifest.get("patch_sha256") != result.get("patch", {}).get("sha256")
        or digest(patch_raw) != manifest.get("patch_sha256")
        or digest(regular(archive / "claim.json", "archived claim")) != result.get("claim_card_sha256")
        or digest(manifest_raw) != record.get("handoff", {}).get("manifest_sha256")
    ):
        raise RuntimeError(f"{item_id}: immutable harvest binding differs")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or [row.get("path") for row in artifacts] != claim.get("writable_paths"):
        raise RuntimeError(f"{item_id}: immutable artifact ownership differs")
    for artifact in artifacts:
        archive_path = archive / safe_relative(artifact.get("archive_path", ""), "archive artifact")
        raw = regular(archive_path, "archived owned artifact")
        if digest(raw) != artifact.get("sha256") or len(raw) != artifact.get("size_bytes"):
            raise RuntimeError(f"{item_id}: immutable artifact digest differs")
    return claim, result, manifest, archive, record


def validate_artifact_semantics(claim: dict, result: dict, archive: Path, manifest: dict) -> list[dict]:
    """Recheck typed outcome against archived bytes without trusting the task root."""
    artifacts = manifest["artifacts"]
    by_path = {row["path"]: row for row in artifacts}
    if set(by_path) != set(claim["writable_paths"]):
        raise RuntimeError("Master archived artifact set differs from exact ownership")
    outcome = result.get("typed_outcome")
    if not isinstance(outcome, dict):
        raise RuntimeError("Master typed outcome is missing")
    contract = claim.get("work_contract", {}).get("kind")
    if contract == "strict_resolution_proof_search":
        if outcome.get("kind") != "strict_resolution":
            raise RuntimeError("Master strict outcome discriminator differs")
        human = [row for path, row in by_path.items() if path.endswith("/human-resolution.md")]
        lean = [row for path, row in by_path.items() if path.endswith("/Proof.lean")]
        if (
            len(human) != 1 or len(lean) != 1
            or human[0]["sha256"] != outcome.get("human_resolution_sha256")
            or lean[0]["sha256"] != outcome.get("lean_root_sha256")
            or outcome.get("machine_cut_set_empty") is not True
            or outcome.get("readability_cut_set_empty") is not True
        ):
            raise RuntimeError("Master strict typed evidence differs")
    elif contract == "source_occurrence_intake":
        if outcome.get("kind") != "source_occurrence_intake":
            raise RuntimeError("Master intake outcome discriminator differs")
        for suffix, field in (
            ("/status-review.json", "status_review_sha256"),
            ("/rights-review.json", "rights_review_sha256"),
            ("/importance-review.json", "importance_review_sha256"),
            ("/identity-crosswalk.json", "identity_crosswalk_sha256"),
        ):
            rows = [row for path, row in by_path.items() if path.endswith(suffix)]
            if len(rows) != 1 or rows[0]["sha256"] != outcome.get(field):
                raise RuntimeError(f"Master intake {field} differs")
        if any(outcome.get(field) is not False for field in (
            "strict_credit_granted", "stage5_claim_id_allocated", "stage6_alias_allocated",
        )):
            raise RuntimeError("Master intake grants forbidden credit/allocation")
    else:
        raise RuntimeError("Master work contract is unsupported")
    return [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in artifacts
    ]


def workset_member_binding(controller, item_id: str) -> dict:
    workset = json.loads(regular(controller.EVIDENCE / "workset-5.6.json", "workset"))
    members = [row for row in workset.get("members", []) if row.get("target_item_id") == item_id]
    if len(members) != 1:
        raise RuntimeError(f"{item_id}: canonical workset member is missing or ambiguous")
    member = members[0]
    return {
        "member_id": member["member_id"], "member_kind": member["member_kind"],
        "target_item_id": member["target_item_id"],
        "workset_record_sha256": member["workset_record_sha256"],
        "source_record_sha256": member["record_sha256"],
    }


def validate_acceptance_candidate(
    *,
    controller,
    checker,
    manager,
    item_id: str,
    claim: dict,
    result: dict,
    manifest: dict,
    archive: Path,
    record: dict,
    receipt_path: Path,
    review_receipt: dict,
    workset_member: dict,
    integrated_files: list[dict],
    pre_blueprint: bytes,
    post_blueprint: bytes,
    post_gantt: bytes,
    gantt_generated_at: str,
    acceptance_path: Path,
    expected_acceptance: dict,
    expected_acceptance_raw: bytes,
    artifact_outputs: list[tuple[Path, bytes]],
    outputs: list[tuple[Path, bytes]],
    guards: dict[Path, object],
    archive_replay: Callable[[Path, str], tuple] | None = None,
) -> None:
    """Replay and validate every candidate byte before a repository rename.

    The committed-state acceptance validator cannot validate a candidate whose
    Blueprint cursor is not yet ``x``.  This precommit counterpart therefore
    binds the exact closed acceptance document to the immutable archive and
    transition receipt, the staged owned artifacts, and independently rendered
    post-Blueprint/Gantt bytes.  It is deliberately called once before creating
    output directories and again by ``atomic_batch_write`` after staging.
    """
    expected_paths = [
        *(path for path, _ in artifact_outputs),
        BLUEPRINT,
        GANTT,
        acceptance_path,
    ]
    candidate_paths = [path for path, _ in outputs]
    if candidate_paths != expected_paths or len(set(candidate_paths)) != len(candidate_paths):
        raise RuntimeError(f"{item_id}: Master candidate output set/order differs")
    candidate_by_path = dict(outputs)

    # Strictly decode, schema-check and seal-check the exact receipt bytes that
    # the transaction will stage.  Pretty encoding is part of this artifact's
    # byte authority, so alternate encodings and duplicate-key JSON fail too.
    acceptance_raw = candidate_by_path[acceptance_path]
    if len(acceptance_raw) > 4 * 1024 * 1024:
        raise RuntimeError(f"{item_id}: candidate Master acceptance is oversized")
    candidate_acceptance = checker.strict_json(
        acceptance_raw, "candidate Master acceptance"
    )
    claim_validator = controller.claim_checker_module()
    claim_validator.validate_schema(
        candidate_acceptance,
        claim_validator.reviewed_schema("master-acceptance.schema.json"),
    )
    verify_seal(candidate_acceptance, "candidate Master acceptance")
    if (
        candidate_acceptance.get("program") != PROGRAM
        or candidate_acceptance.get("item_id") != item_id
        or candidate_acceptance.get("mode") != claim.get("mode")
    ):
        raise RuntimeError(f"{item_id}: candidate Master identity differs")
    encoded_candidate = json.dumps(
        candidate_acceptance, ensure_ascii=False, sort_keys=True, indent=2
    ).encode() + b"\n"
    if (
        candidate_acceptance != expected_acceptance
        or acceptance_raw != expected_acceptance_raw
        or acceptance_raw != encoded_candidate
    ):
        raise RuntimeError(f"{item_id}: candidate Master acceptance bytes differ")
    expected_acceptance_path = (
        ACCEPTANCES / item_id / result["baseline_sha256"]
        / expected_acceptance["integration"]["post_tree_sha256"]
        / f"{expected_acceptance['authority_sha256']}.json"
    )
    if acceptance_path != expected_acceptance_path:
        raise RuntimeError(f"{item_id}: candidate acceptance path grammar differs")

    # The post Blueprint is exactly one authenticated underscore-to-x edit.
    # Parsing both candidates rechecks the full immutable row/DAG authority.
    pre_marker = f"- [_] `{item_id}`".encode()
    post_marker = f"- [x] `{item_id}`".encode()
    if (
        regular(BLUEPRINT, "current pre-acceptance Blueprint") != pre_blueprint
        or pre_blueprint.count(pre_marker) != 1
        or pre_blueprint.count(post_marker) != 0
        or post_blueprint != pre_blueprint.replace(pre_marker, post_marker, 1)
        or candidate_by_path[BLUEPRINT] != post_blueprint
    ):
        raise RuntimeError(f"{item_id}: candidate Blueprint transition differs")
    for label, raw in (
        ("pre-acceptance Blueprint", pre_blueprint),
        ("post-acceptance Blueprint", candidate_by_path[BLUEPRINT]),
    ):
        with tempfile.NamedTemporaryFile(
            prefix=f".{label.replace(' ', '-')}.",
            dir=BLUEPRINT.parent,
            delete=False,
        ) as stream:
            stream.write(raw)
            temporary = Path(stream.name)
        try:
            checker.parse_blueprint(temporary)
        finally:
            temporary.unlink(missing_ok=True)

    # Render from the staged Blueprint again, rather than trusting the earlier
    # prepared projection or merely comparing its advertised digest.
    independently_rendered_gantt = prepare_gantt(
        candidate_by_path[BLUEPRINT], checker, gantt_generated_at
    )
    if (
        candidate_by_path[GANTT] != post_gantt
        or independently_rendered_gantt != candidate_by_path[GANTT]
    ):
        raise RuntimeError(f"{item_id}: candidate Gantt bytes differ")
    transition = candidate_acceptance["state_transition"]
    if transition != {
        "from": "handoff_waiting_master",
        "to": "master_accepted",
        "pre_blueprint_sha256": digest(pre_blueprint),
        "post_blueprint_sha256": digest(candidate_by_path[BLUEPRINT]),
        "post_gantt_sha256": digest(candidate_by_path[GANTT]),
    }:
        raise RuntimeError(f"{item_id}: candidate state-transition digests differ")

    # Replay the archive through both the handoff-local binding checks and the
    # standalone offline validator.  Equality to the originally reviewed
    # values prevents a consistently replaced archive/state pair from slipping
    # through this boundary; the CAS guards below independently fence bytes.
    fresh_claim, fresh_result, fresh_manifest, fresh_archive, fresh_record = (
        archived_bundle(controller, item_id)
    )
    if (
        fresh_claim != claim
        or fresh_result != result
        or fresh_manifest != manifest
        or fresh_archive != archive
        or fresh_record != record
    ):
        raise RuntimeError(f"{item_id}: archived handoff changed during acceptance")
    replay = archive_replay or claim_validator.validate_archived_claim_result
    (
        offline_claim,
        offline_result,
        offline_manifest,
        offline_integrated,
        offline_manifest_raw,
    ) = replay(archive, item_id)
    if (
        offline_claim != claim
        or offline_result != result
        or offline_manifest != manifest
        or offline_integrated != integrated_files
        or digest(offline_manifest_raw)
        != candidate_acceptance["handoff"]["immutable_archive_sha256"]
    ):
        raise RuntimeError(f"{item_id}: offline archive replay differs")

    fresh_receipt_path, fresh_review_receipt = transition_receipt(item_id, record)
    strict_review_receipt = checker.strict_json(
        regular(receipt_path, "candidate handoff transition receipt"),
        "candidate handoff transition receipt",
    )
    verify_seal(strict_review_receipt, "candidate handoff transition receipt")
    review_state = review_receipt.get("state_transition", {})
    review_handoff = review_receipt.get("handoff", {})
    if (
        fresh_receipt_path != receipt_path
        or fresh_review_receipt != review_receipt
        or strict_review_receipt != review_receipt
        or review_state.get("from") != "not_done"
        or review_state.get("to") != "handoff_waiting_master"
        or review_state.get("post_blueprint_sha256") != digest(pre_blueprint)
        or review_handoff.get("claim_id") != record.get("claim_id")
        or review_handoff.get("run_id") != record.get("run_id")
        or review_handoff.get("immutable_archive")
        != archive.relative_to(ROOT).as_posix()
        or review_handoff.get("harvest_manifest_sha256")
        != digest(regular(archive / "harvest-manifest.json", "harvest manifest"))
        or review_receipt.get("canonical_integration") != {
            "integrated": False,
            "canonical_write": "forbidden_until_master_acceptance",
        }
    ):
        raise RuntimeError(f"{item_id}: reviewed transition receipt differs")
    if candidate_acceptance["review_decisions"] != [{
        "reviewer_id": "canonical-master-handoff-review",
        "decision": "accepted",
        "decision_receipt_path": receipt_path.relative_to(ROOT).as_posix(),
        "decision_receipt_sha256": digest(
            regular(receipt_path, "handoff transition receipt")
        ),
    }]:
        raise RuntimeError(f"{item_id}: candidate review decision differs")

    # Bind every staged canonical artifact to freshly read archive bytes and to
    # both manifest/result metadata.  A mutation after initial preparation is
    # therefore rejected at the transaction boundary.
    if (
        len(artifact_outputs) != len(integrated_files)
        or len(manifest["artifacts"]) != len(integrated_files)
    ):
        raise RuntimeError(f"{item_id}: candidate artifact cardinality differs")
    for integrated, archived, (destination, originally_prepared) in zip(
        integrated_files, manifest["artifacts"], artifact_outputs
    ):
        expected_destination = ROOT / safe_relative(
            integrated["path"], "candidate canonical artifact"
        )
        source = archive / safe_relative(
            archived["archive_path"], "candidate archive artifact"
        )
        source_raw = regular(source, "candidate archived artifact")
        staged_raw = candidate_by_path.get(destination)
        source_relative = source.relative_to(archive).as_posix()
        if (
            destination != expected_destination
            or archived.get("path") != integrated["path"]
            or not isinstance(archived.get("source_path"), str)
            or source_relative != archived.get("archive_path")
            or archived.get("sha256") != integrated["sha256"]
            or archived.get("size_bytes") != integrated["size_bytes"]
            or originally_prepared != source_raw
            or staged_raw != source_raw
            or digest(source_raw) != integrated["sha256"]
            or len(source_raw) != integrated["size_bytes"]
        ):
            raise RuntimeError(
                f"{item_id}: candidate artifact differs: {integrated['path']}"
            )

    if (
        candidate_acceptance["workset_member"] != workset_member
        or candidate_acceptance["accepted_outcome"] != result["typed_outcome"]
        or candidate_acceptance["integration"]["integrated_files"]
        != integrated_files
        or candidate_acceptance["integration"]["integrated_bytes_sha256"]
        != digest(canonical(integrated_files))
    ):
        raise RuntimeError(f"{item_id}: candidate semantic acceptance binding differs")
    expected_gate = {
        "gate_id": "conjecture-master-archive-replay",
        "command_sha256": digest(canonical([
            "archive-replay", item_id, *claim["writable_paths"],
        ])),
        "exit_code": 0,
        "passed": True,
        "stdout_sha256": digest(canonical({
            "item_id": item_id,
            "mode": claim["mode"],
            "accepted_outcome_sha256": digest(canonical(result["typed_outcome"])),
        })),
        "stderr_sha256": digest(b""),
    }
    if candidate_acceptance["validation_gates"] != [expected_gate]:
        raise RuntimeError(f"{item_id}: candidate validation-gate binding differs")
    if candidate_acceptance["integration"] != {
        "pre_tree_sha256": claim["baseline"]["owned_paths_baseline_sha256"],
        "post_tree_sha256": digest(canonical([
            [row["path"], row["sha256"]] for row in integrated_files
        ])),
        "integrated_bytes_sha256": digest(canonical(integrated_files)),
        "integrated_files": integrated_files,
    }:
        raise RuntimeError(f"{item_id}: candidate integration tree binding differs")
    for path, expectation in guards.items():
        manager.validate_file_expectation(path, expectation)


def build_acceptance_candidate(
    *,
    item_id: str,
    claim: dict,
    result: dict,
    archive: Path,
    record: dict,
    receipt_path: Path,
    workset_member: dict,
    integrated_files: list[dict],
    pre_blueprint: bytes,
    post_blueprint: bytes,
    post_gantt: bytes,
    accepted_at: str,
    master_thread_id: str,
    master_objective_sha256: str,
) -> tuple[Path, dict, bytes]:
    """Construct the one exact content-addressed Master decision candidate."""
    if (
        not isinstance(master_thread_id, str)
        or not master_thread_id
        or not isinstance(master_objective_sha256, str)
        or len(master_objective_sha256) != 64
        or any(character not in "0123456789abcdef" for character in master_objective_sha256)
    ):
        raise RuntimeError(f"{item_id}: Master operator authority is malformed")
    pre_tree = claim["baseline"]["owned_paths_baseline_sha256"]
    post_tree = digest(canonical([
        [row["path"], row["sha256"]] for row in integrated_files
    ]))
    gate_stdout = canonical({
        "item_id": item_id,
        "mode": claim["mode"],
        "accepted_outcome_sha256": digest(canonical(result["typed_outcome"])),
    })
    gate = {
        "gate_id": "conjecture-master-archive-replay",
        "command_sha256": digest(canonical([
            "archive-replay", item_id, *claim["writable_paths"],
        ])),
        "exit_code": 0,
        "passed": True,
        "stdout_sha256": digest(gate_stdout),
        "stderr_sha256": digest(b""),
    }
    body = {
        "schema_version": "awesome-theorems/stage5-proof-debt-master-acceptance/1.0",
        "program": PROGRAM,
        "item_id": item_id,
        "mode": claim["mode"],
        "master": {
            "principal_id": f"codex-user-goal:{master_thread_id}",
            "decision_id": f"master-{item_id.lower()}-{post_tree[:16]}",
            "authentication_sha256": digest(canonical({
                "thread_id": master_thread_id,
                "objective_sha256": master_objective_sha256,
            })),
        },
        "handoff": {
            "claim_id": record["claim_id"],
            "run_id": record["run_id"],
            "claim_card_sha256": digest(
                regular(archive / "claim.json", "archived claim")
            ),
            "worker_result_sha256": digest(
                regular(archive / "result.json", "archived result")
            ),
            "baseline_sha256": result["baseline_sha256"],
            "patch_sha256": result["patch"]["sha256"],
            "immutable_archive_path": archive.relative_to(ROOT).as_posix(),
            "immutable_archive_sha256": digest(
                regular(archive / "harvest-manifest.json", "harvest manifest")
            ),
        },
        "review_decisions": [{
            "reviewer_id": "canonical-master-handoff-review",
            "decision": "accepted",
            "decision_receipt_path": receipt_path.relative_to(ROOT).as_posix(),
            "decision_receipt_sha256": digest(
                regular(receipt_path, "handoff transition receipt")
            ),
        }],
        "integration": {
            "pre_tree_sha256": pre_tree,
            "post_tree_sha256": post_tree,
            "integrated_bytes_sha256": digest(canonical(integrated_files)),
            "integrated_files": integrated_files,
        },
        "validation_gates": [gate],
        "state_transition": {
            "from": "handoff_waiting_master",
            "to": "master_accepted",
            "pre_blueprint_sha256": digest(pre_blueprint),
            "post_blueprint_sha256": digest(post_blueprint),
            "post_gantt_sha256": digest(post_gantt),
        },
        "workset_member": workset_member,
        "accepted_outcome": result["typed_outcome"],
        "accepted_at": accepted_at,
    }
    acceptance = seal(body)
    acceptance_raw = json.dumps(
        acceptance, ensure_ascii=False, sort_keys=True, indent=2
    ).encode() + b"\n"
    acceptance_path = (
        ACCEPTANCES / item_id / result["baseline_sha256"] / post_tree
        / f"{acceptance['authority_sha256']}.json"
    )
    return acceptance_path, acceptance, acceptance_raw


def master_accept(item_id: str) -> dict:
    controller = load_controller()
    checker = controller.checker_module()
    manager = checker.manager()
    checker.manager = lambda: manager
    master_thread_id, master_objective_sha256, _ = manager.operator_goal_binding(
        manager.CONJECTURE
    )
    with manager.conjecture_scheduler_transition_guard(), manager.manager_mutation_lock():
        require_boot_authority(checker)
        state_before = controller.load_state(False)
        record_before = state_before.get("claims", {}).get(item_id)
        if not isinstance(record_before, dict):
            raise RuntimeError(f"{item_id}: controller claim record is missing")
        if record_before.get("runtime_authority_epoch") != controller.RUNTIME_AUTHORITY_EPOCH:
            raise RuntimeError(f"{item_id}: claim belongs to a historical runtime epoch")
        _, current_rows, _ = checker.parse_blueprint()
        current_state = {
            row["item_id"]: row["state"] for row in current_rows
            if isinstance(row, dict) and isinstance(row.get("item_id"), str)
        }.get(item_id)
        if current_state == "x":
            candidates = _acceptance_candidates(item_id, record_before)
            valid = _valid_acceptance_candidates(
                controller, item_id, record_before
            )
            if len(candidates) != len(valid):
                raise RuntimeError(
                    f"{item_id}: invalid or foreign acceptance candidate is present"
                )
            if len(valid) == 1:
                return _reconcile_acceptance_locked(
                    controller, item_id, record_before, valid[0]
                )
            raise RuntimeError(
                f"{item_id}: accepted cursor lacks one exact valid acceptance"
            )
        if current_state != "_":
            raise RuntimeError(
                f"{item_id}: Master acceptance requires an underscore cursor"
            )
        claim, result, manifest, archive, record = archived_bundle(controller, item_id)
        integration_entry = _validated_integration_entry(controller, checker, record)
        receipt_path, review_receipt = transition_receipt(item_id, record)
        workset_member = workset_member_binding(controller, item_id)
        if claim.get("workset_member") != workset_member:
            raise RuntimeError(f"{item_id}: claim/workset binding differs")
        integrated_files = validate_artifact_semantics(claim, result, archive, manifest)
        pre_blueprint = regular(BLUEPRINT, "current Blueprint")
        pre_marker = f"- [_] `{item_id}`".encode()
        if pre_blueprint.count(pre_marker) != 1:
            raise RuntimeError(f"{item_id}: Master acceptance requires one underscore row")
        post_blueprint = pre_blueprint.replace(pre_marker, f"- [x] `{item_id}`".encode(), 1)
        gantt_generated_at = (
            datetime.now(timezone.utc).replace(microsecond=0)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        post_gantt = prepare_gantt(post_blueprint, checker, gantt_generated_at)
        artifact_outputs: list[tuple[Path, bytes]] = []
        expected_old: dict[Path, object] = {}
        created_destination_parents: set[Path] = set()
        for artifact, archived in zip(integrated_files, manifest["artifacts"]):
            destination = ROOT / safe_relative(artifact["path"], "canonical artifact")
            source = archive / safe_relative(archived["archive_path"], "archive artifact")
            raw = regular(source, "archived canonical source")
            old = manager.regular_file_expectation(destination)
            if old is not None and old.sha256 != artifact["sha256"]:
                raise RuntimeError(f"canonical destination conflict: {artifact['path']}")
            artifact_outputs.append((destination, raw))
            expected_old[destination] = old
        observed_pre_tree = digest(canonical([
            [row["path"], expected_old[ROOT / row["path"]].sha256 if expected_old[ROOT / row["path"]] else None]
            for row in integrated_files
        ]))
        if observed_pre_tree != claim["baseline"]["owned_paths_baseline_sha256"]:
            raise RuntimeError(f"{item_id}: canonical owned-path baseline changed")
        acceptance_path, acceptance, acceptance_raw = build_acceptance_candidate(
            item_id=item_id,
            claim=claim,
            result=result,
            archive=archive,
            record=record,
            receipt_path=receipt_path,
            workset_member=workset_member,
            integrated_files=integrated_files,
            pre_blueprint=pre_blueprint,
            post_blueprint=post_blueprint,
            post_gantt=post_gantt,
            accepted_at=gantt_generated_at,
            master_thread_id=master_thread_id,
            master_objective_sha256=master_objective_sha256,
        )
        outputs = [
            *artifact_outputs, (BLUEPRINT, post_blueprint), (GANTT, post_gantt),
            (acceptance_path, acceptance_raw),
        ]
        expected_old.update({
            BLUEPRINT: manager.regular_file_expectation(BLUEPRINT),
            GANTT: manager.regular_file_expectation(GANTT), acceptance_path: None,
        })
        guards = {
            controller.STATE: manager.regular_file_expectation(controller.STATE),
            archive / "claim.json": manager.regular_file_expectation(archive / "claim.json"),
            archive / "result.json": manager.regular_file_expectation(archive / "result.json"),
            archive / "changes.patch": manager.regular_file_expectation(archive / "changes.patch"),
            archive / "harvest-manifest.json": manager.regular_file_expectation(archive / "harvest-manifest.json"),
            receipt_path: manager.regular_file_expectation(receipt_path),
            integration_entry: manager.regular_file_expectation(integration_entry),
        }
        for archived in manifest["artifacts"]:
            source = archive / safe_relative(
                archived["archive_path"], "archive artifact guard"
            )
            guards[source] = manager.regular_file_expectation(source)
        if any(expectation is None for expectation in guards.values()):
            raise RuntimeError(f"{item_id}: Master acceptance guard disappeared")
        candidate_arguments = {
            "controller": controller,
            "checker": checker,
            "manager": manager,
            "item_id": item_id,
            "claim": claim,
            "result": result,
            "manifest": manifest,
            "archive": archive,
            "record": record,
            "receipt_path": receipt_path,
            "review_receipt": review_receipt,
            "workset_member": workset_member,
            "integrated_files": integrated_files,
            "pre_blueprint": pre_blueprint,
            "post_blueprint": post_blueprint,
            "post_gantt": post_gantt,
            "gantt_generated_at": gantt_generated_at,
            "acceptance_path": acceptance_path,
            "expected_acceptance": acceptance,
            "expected_acceptance_raw": acceptance_raw,
            "artifact_outputs": artifact_outputs,
            "outputs": outputs,
            "guards": guards,
        }

        # Validate the full candidate before creating any missing destination
        # directory.  The transaction invokes the same replay again after all
        # candidate bytes have been staged and immediately before rename.
        validate_acceptance_candidate(**candidate_arguments)
        try:
            for destination, _ in [*artifact_outputs, (acceptance_path, acceptance_raw)]:
                if not destination.parent.exists():
                    missing = [
                        parent
                        for parent in (destination.parent, *destination.parent.parents)
                        if parent != ROOT
                        and parent.is_relative_to(ROOT)
                        and not parent.exists()
                    ]
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    created_destination_parents.update(
                        parent
                        for parent in missing
                        if parent.is_dir() and not parent.is_symlink()
                    )
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
            def boundary() -> None:
                validate_acceptance_candidate(**candidate_arguments)
            manager.atomic_batch_write(
                outputs, expected_old=expected_old, guards=guards,
                precommit_validator=boundary,
                additional_allowed_destinations=manager.conjecture_item_owned_destinations(item_id),
            )
        except BaseException:
            # The preflight is zero-target-write; if a later transaction
            # boundary rejects, remove only directories this call created and
            # only while they remain empty.  Existing directories are never
            # removed, and atomic_batch_write owns file rollback.
            candidates = set(created_destination_parents)
            for directory in sorted(candidates, key=lambda path: len(path.parts), reverse=True):
                try:
                    directory.relative_to(ROOT)
                    directory.rmdir()
                except (FileNotFoundError, OSError, ValueError):
                    pass
            raise
        # Verify the committed receipt from immutable archive plus canonical
        # bytes before the runtime record is observationally reconciled.
        controller.claim_checker_module().validate_acceptance(acceptance_path)
        outcome = _reconcile_acceptance_locked(
            controller, item_id, record, (acceptance_path, acceptance)
        )
        outcome.update({
            "post_blueprint_sha256": digest(post_blueprint),
            "post_gantt_sha256": digest(post_gantt),
        })
        return outcome


def transition(item_id: str) -> dict:
    controller = load_controller()
    checker = controller.checker_module()
    manager = checker.manager()
    # Bind the checker to this exact loaded manager instance so the scheduler
    # and mutation locks are not duplicated by a second dynamic import.
    checker.manager = lambda: manager
    with manager.conjecture_scheduler_transition_guard(), manager.manager_mutation_lock():
        require_boot_authority(checker)
        _, current_rows, _ = checker.parse_blueprint()
        current_state = {
            row["item_id"]: row["state"] for row in current_rows
            if isinstance(row, dict) and isinstance(row.get("item_id"), str)
        }.get(item_id)
        if current_state == "_":
            state = controller.load_state(False)
            record = state.get("claims", {}).get(item_id)
            if not isinstance(record, dict):
                raise RuntimeError(f"{item_id}: controller claim record is missing")
            receipt_path, _ = transition_receipt(item_id, record)
            return {
                "valid": True,
                "item_id": item_id,
                "state": "handoff_waiting_master",
                "receipt": receipt_path.relative_to(ROOT).as_posix(),
                "reconciled": True,
            }
        if current_state != " ":
            raise RuntimeError(
                f"{item_id}: handoff transition requires a blank cursor"
            )
        result_path, claim_path, record = result_and_claim(controller, item_id)
        integration_entry = _validated_integration_entry(controller, checker, record)
        state_path = controller.STATE
        pre_blueprint = BLUEPRINT.read_bytes()
        marker = f"- [ ] `{item_id}`".encode()
        replacement = f"- [_] `{item_id}`".encode()
        if pre_blueprint.count(marker) != 1:
            raise RuntimeError(f"{item_id}: expected exactly one blank authoritative row")
        post_blueprint = pre_blueprint.replace(marker, replacement, 1)
        post_gantt = prepare_gantt(post_blueprint, checker)
        archive = Path(record["handoff"]["archive"])
        manifest_path = archive / "harvest-manifest.json"
        guarded_paths = (
            state_path, claim_path, result_path, manifest_path, integration_entry,
        )
        guards = {path: manager.regular_file_expectation(path) for path in guarded_paths}
        if any(expectation is None for expectation in guards.values()):
            raise RuntimeError(f"{item_id}: transition input disappeared")
        receipt_body = {
            "schema_version": "awesome-theorems/stage5-conjecture-handoff-transition/1.0",
            "program": PROGRAM,
            "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
            "item_id": item_id,
            "state_transition": {
                "from": "not_done", "to": "handoff_waiting_master",
                "pre_blueprint_sha256": digest(pre_blueprint),
                "post_blueprint_sha256": digest(post_blueprint),
                "post_gantt_sha256": digest(post_gantt),
            },
            "handoff": {
                "claim_id": record["claim_id"], "run_id": record["run_id"],
                "claim_card_sha256": digest(claim_path.read_bytes()),
                "worker_result_sha256": digest(result_path.read_bytes()),
                "harvest_manifest_path": str(manifest_path.relative_to(ROOT)),
                "harvest_manifest_sha256": digest(manifest_path.read_bytes()),
                "immutable_archive": str(archive.relative_to(ROOT)),
                "patch_sha256": json.loads(result_path.read_text())["patch"]["sha256"],
            },
            "canonical_integration": {
                "integrated": False,
                "canonical_write": "forbidden_until_master_acceptance",
            },
            "prepared_at": datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "transition_id": f"S5PD-HANDOFF-{item_id}-{uuid.uuid4().hex[:12]}",
        }
        receipt_raw = json.dumps(
            seal(receipt_body), ensure_ascii=False, sort_keys=True, indent=2
        ).encode() + b"\n"
        receipt_path = EVIDENCE / item_id / f"{digest(receipt_raw)}.json"
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        outputs = [(BLUEPRINT, post_blueprint), (GANTT, post_gantt), (receipt_path, receipt_raw)]
        expected_old = {
            BLUEPRINT: manager.regular_file_expectation(BLUEPRINT),
            GANTT: manager.regular_file_expectation(GANTT),
            receipt_path: None,
        }
        manager.atomic_batch_write(
            outputs,
            expected_old=expected_old,
            guards=guards,
            precommit_validator=lambda: result_and_claim(controller, item_id),
        )
        return {"valid": True, "item_id": item_id,
                "state": "handoff_waiting_master",
                "receipt": str(receipt_path.relative_to(ROOT)),
                "post_blueprint_sha256": digest(post_blueprint),
                "post_gantt_sha256": digest(post_gantt)}


def _integration_entry(controller, record: dict) -> Path:
    return controller.INTEGRATION_QUEUE / (
        f"{record['item_id']}--{record['claim_id']}--{record['run_id']}.json"
    )


def _validated_integration_entry(controller, checker, record: dict) -> Path:
    """Validate the exact immutable queue pointer for one harvested run."""
    entry = _integration_entry(controller, record)
    value = checker.strict_json(regular(entry, "integration entry"), "integration entry")
    verify_seal(value, "integration entry")
    handoff = record.get("handoff")
    if not isinstance(handoff, dict):
        raise RuntimeError(f"{record.get('item_id')}: handoff binding is missing")
    try:
        queue = Path(handoff["queue"]).relative_to(ROOT).as_posix()
        archive = Path(handoff["archive"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(
            f"{record.get('item_id')}: handoff path binding is unsafe"
        ) from exc
    manifest_raw = regular(archive / "harvest-manifest.json", "harvest manifest")
    manifest = verify_seal(
        checker.strict_json(
            manifest_raw, "harvest manifest",
        ),
        "harvest manifest",
    )
    try:
        archive_relative = archive.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise RuntimeError(
            f"{record.get('item_id')}: archive is outside the repository"
        ) from exc
    if (
        manifest.get("schema_version")
        != "awesome-theorems/stage5-harvest-manifest/1.1"
        or manifest.get("program") != PROGRAM
        or manifest.get("item_id") != record.get("item_id")
        or manifest.get("claim_id") != record.get("claim_id")
        or manifest.get("run_id") != record.get("run_id")
        or manifest.get("queue") != queue
        or manifest.get("archive") != archive_relative
        or handoff.get("manifest_sha256") != digest(manifest_raw)
    ):
        raise RuntimeError(
            f"{record.get('item_id')}: integration handoff binding differs"
        )
    expected = seal({
        "schema_version": "awesome-theorems/stage5-integration-entry/1.0",
        "program": PROGRAM,
        "item_id": record.get("item_id"),
        "claim_id": record.get("claim_id"),
        "run_id": record.get("run_id"),
        "queue": queue,
        "baseline_sha256": manifest.get("baseline_sha256"),
        "patch_sha256": manifest.get("patch_sha256"),
    })
    if value != expected:
        raise RuntimeError(
            f"{record.get('item_id')}: integration entry binding differs"
        )
    return entry


def _remove_integration_entry(controller, checker, record: dict) -> bool:
    """Remove only an exact queue entry; absence is an idempotent success."""
    entry = _integration_entry(controller, record)
    if not entry.exists() and not entry.is_symlink():
        return False
    _validated_integration_entry(controller, checker, record)
    entry.unlink()
    return True


def _acceptance_candidates(item_id: str, record: dict) -> list[Path]:
    root = ACCEPTANCES / item_id
    if not root.is_dir() or root.is_symlink():
        return []
    result: list[Path] = []
    for path in root.glob("*/*/*.json"):
        if path.is_file() and not path.is_symlink():
            result.append(path)
    return sorted(result)


def _valid_acceptance_candidates(
    controller, item_id: str, record: dict,
) -> list[tuple[Path, dict]]:
    """Return exact current-run acceptances; reject duplicate authorities."""
    valid: list[tuple[Path, dict]] = []
    for path in _acceptance_candidates(item_id, record):
        try:
            value = controller.claim_checker_module().validate_acceptance(path)
        except Exception:
            continue
        handoff = value.get("handoff", {})
        if (
            handoff.get("claim_id") == record.get("claim_id")
            and handoff.get("run_id") == record.get("run_id")
        ):
            valid.append((path, value))
    return valid


def _reconcile_acceptance_locked(
    controller, item_id: str, record: dict, selected: tuple[Path, dict],
) -> dict:
    """Repair state/queue after the canonical acceptance transaction commits."""
    path, acceptance = selected
    checker = controller.checker_module()
    entry = _integration_entry(controller, record)
    if entry.exists() or entry.is_symlink():
        _validated_integration_entry(controller, checker, record)
    expected_integration = {
        "acceptance_path": str(path),
        "acceptance_sha256": digest(regular(path, "Master acceptance")),
        "accepted_at": acceptance["accepted_at"],
    }
    state = controller.load_state(False)
    current = state.get("claims", {}).get(item_id)
    if (
        not isinstance(current, dict)
        or current.get("runtime_authority_epoch")
        != controller.RUNTIME_AUTHORITY_EPOCH
        or current.get("claim_id") != record.get("claim_id")
        or current.get("run_id") != record.get("run_id")
    ):
        raise RuntimeError(f"{item_id}: controller claim changed during reconciliation")
    state_changed = (
        current.get("status") != "master_accepted"
        or current.get("integration") != expected_integration
    )
    current["status"] = "master_accepted"
    current["integration"] = expected_integration
    if state_changed:
        controller.save_state(state)
    queue_removed = _remove_integration_entry(controller, checker, current)
    return {
        "valid": True,
        "item_id": item_id,
        "state": "master_accepted",
        "acceptance": path.relative_to(ROOT).as_posix(),
        "reconciled": state_changed or queue_removed,
        "queue_removed": queue_removed,
    }


def reconcile_acceptance(item_id: str) -> dict:
    """Repair runtime state after an acceptance commit/state-save crash."""
    controller = load_controller()
    checker = controller.checker_module()
    manager = checker.manager()
    checker.manager = lambda: manager
    with manager.conjecture_scheduler_transition_guard(), manager.manager_mutation_lock():
        require_boot_authority(checker)
        state = controller.load_state(False)
        record = state.get("claims", {}).get(item_id)
        if not isinstance(record, dict):
            raise RuntimeError(f"{item_id}: controller claim record is missing")
        if record.get("runtime_authority_epoch") != controller.RUNTIME_AUTHORITY_EPOCH:
            raise RuntimeError(f"{item_id}: claim belongs to a historical runtime epoch")
        _, rows, _ = checker.parse_blueprint()
        row_states = {
            row["item_id"]: row["state"] for row in rows
            if isinstance(row, dict) and isinstance(row.get("item_id"), str)
        }
        if row_states.get(item_id) != "x":
            raise RuntimeError(
                f"{item_id}: acceptance reconciliation requires an accepted cursor"
            )
        candidates = _acceptance_candidates(item_id, record)
        valid = _valid_acceptance_candidates(controller, item_id, record)
        if len(candidates) != len(valid):
            raise RuntimeError(
                f"{item_id}: invalid or foreign acceptance candidate is present"
            )
        if len(valid) != 1:
            raise RuntimeError(
                f"{item_id}: exact valid acceptance is missing or ambiguous"
            )
        return _reconcile_acceptance_locked(
            controller, item_id, record, valid[0]
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--accept", action="store_true")
    parser.add_argument("--reconcile", action="store_true")
    parser.add_argument("item_id", nargs="+")
    args = parser.parse_args()
    try:
        if args.accept and args.reconcile:
            raise RuntimeError("--accept and --reconcile are mutually exclusive")
        operation = (
            reconcile_acceptance if args.reconcile
            else master_accept if args.accept
            else transition
        )
        print(json.dumps({"valid": True,
                          "transitions": [operation(item) for item in args.item_id]},
                         ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
