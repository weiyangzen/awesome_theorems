#!/usr/bin/env python3
"""Prepare local-only Stage5 theorem BOOT principals and operator inputs.

Private Ed25519 material is stored outside the repository with mode 0600.
Only the closed public trust root and local active-goal budget inputs are
materialized in the repository.  Receipt signing is a separate explicit mode
used after the authoritative BOOT command suite has passed.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
from datetime import datetime, timezone
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
PUBLIC_ROOT = ROOT / "Docs/evidence/stage5_theorems/controller-bootstrap-role-trust-root.json"
SHARED_EVIDENCE = ROOT / "Docs/evidence/stage5_shared_execution"
PRIVATE_ROOT = Path("/home/sansha/.local/state/awesome-theorems-stage5-theorem-boot-v1")
PROGRAM = "stage5-theorem-proof-debt/2.0"
PRINCIPALS = (
    ("theorem-boot-producer-v1", "theorem-boot-producer", "producer"),
    ("theorem-boot-reviewer-a-v1", "theorem-boot-reviewer-a", "reviewer"),
    ("theorem-boot-reviewer-b-v1", "theorem-boot-reviewer-b", "reviewer"),
    ("theorem-boot-master-v1", "theorem-boot-master", "master"),
)


class PrepareError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def atomic_write(path: Path, raw: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_json(path: Path, value: Any, mode: int) -> None:
    atomic_write(
        path,
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n",
        mode,
    )


def exclusive_json(path: Path, value: Any, mode: int = 0o644) -> bytes:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False,
    ).encode("utf-8") + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
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
    return raw


def load_manager() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_manager_for_boot_preparation", MANAGER_PATH)
    if spec is None or spec.loader is None:
        raise PrepareError("cannot load canonical Stage5 manager")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_private_key(key_id: str, principal: str, role: str) -> Ed25519PrivateKey:
    path = PRIVATE_ROOT / f"{key_id}.json"
    if path.is_symlink() or not path.is_file() or (path.stat().st_mode & 0o077):
        raise PrepareError(f"private key file is unavailable or unsafe: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if (
        set(value) != {
            "schema_version", "key_id", "principal_id", "allowed_role",
            "private_key_hex",
        }
        or value.get("key_id") != key_id
        or value.get("principal_id") != principal
        or value.get("allowed_role") != role
    ):
        raise PrepareError(f"private key identity differs: {path}")
    try:
        return Ed25519PrivateKey.from_private_bytes(
            bytes.fromhex(value["private_key_hex"])
        )
    except (KeyError, ValueError) as exc:
        raise PrepareError(f"private key is invalid: {path}") from exc


def signed_document(unsigned: dict[str, Any], key: Ed25519PrivateKey) -> dict[str, Any]:
    payload = canonical(unsigned)
    value = dict(unsigned)
    value["signed_payload_sha256"] = digest(payload)
    value["signature"] = key.sign(payload).hex()
    value["authority_sha256"] = digest(canonical(value))
    return value


def instant() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def role_identity(role: str, ordinal: int = 0) -> tuple[str, str, str]:
    matches = [row for row in PRINCIPALS if row[2] == role]
    try:
        return matches[ordinal]
    except IndexError as exc:
        raise PrepareError(f"missing local BOOT principal for role={role!r}") from exc


def role_attestation(
    manager: Any, *, role: str, ordinal: int, claim_id: str, run_id: str,
) -> tuple[dict[str, Any], Ed25519PrivateKey, str, str]:
    key_id, principal, expected_role = role_identity(role, ordinal)
    key = load_private_key(key_id, principal, expected_role)
    program = manager.THEOREM
    unsigned = {
        "schema_version": manager.BOOT_ROLE_SCHEMA,
        "program": program.version,
        "role": role,
        "principal_id": principal,
        "key_id": key_id,
        "principal_context": "local",
        "claim_id": claim_id,
        "run_id": run_id,
        "item_id": f"{program.task_prefix}-BOOT-001",
        "manager_sha256": manager.manager_code_sha256(),
        "source_bundle_sha256": manager.source_bundle_sha256(program),
        "execution_spec_sha256": manager.sha256_bytes(
            manager.canonical(manager.spec_object(program))
        ),
        "observed_at": instant(),
        "signature_algorithm": "Ed25519",
    }
    return signed_document(unsigned, key), key, key_id, principal


def boot_context(manager: Any) -> tuple[Any, list[Any], bytes, bytes, dict[str, str]]:
    program = manager.THEOREM
    tasks = manager.expected_tasks(program)
    blueprint = program.blueprint.read_bytes()
    gantt = program.gantt.read_bytes()
    current = manager.parse_blueprint(
        program, blueprint, tasks, allow_boot_transition=True
    )
    bindings, _ = manager.boot_artifact_snapshot(program, tasks)
    return program, current, blueprint, gantt, bindings


def sign_producer_handoff() -> dict[str, Any]:
    manager = load_manager()
    program, current, blueprint, gantt, bindings = boot_context(manager)
    if current[0].state != " " or any(task.state != " " for task in current[1:]):
        raise PrepareError("producer handoff requires the wholly blank theorem Blueprint")
    handoff_path, acceptance_path, review_path, final_path = manager.boot_receipt_paths(program)
    if any(path.exists() or path.is_symlink() for path in (handoff_path, acceptance_path, review_path, final_path)):
        raise PrepareError("BOOT receipt already exists; refusing to overwrite or replay")
    command_results = manager.run_boot_commands(program)
    results_sha = manager.sha256_bytes(manager.canonical(command_results))
    attestation, key, key_id, principal = role_attestation(
        manager, role="producer", ordinal=0,
        claim_id="theorem-boot-producer-claim-v1",
        run_id=f"producer-{results_sha[:24]}",
    )
    common = manager.validate_boot_common(
        program, manager.expected_tasks(program), blueprint, current, bindings
    )
    command_spec_sha = manager.sha256_bytes(
        manager.canonical(manager.boot_command_spec(program))
    )
    unsigned = {
        "schema_version": manager.BOOT_HANDOFF_SCHEMA,
        "role": "producer",
        "principal_id": principal,
        "key_id": key_id,
        "signature_algorithm": "Ed25519",
        "status": "self_tested",
        **common,
        "gantt_sha256": manager.sha256_bytes(gantt),
        "command_spec_sha256": command_spec_sha,
        "expected_command_results_sha256": results_sha,
        "producer_attestation": attestation,
    }
    value = signed_document(unsigned, key)
    raw = exclusive_json(handoff_path, value)
    return {
        "path": handoff_path.relative_to(ROOT).as_posix(),
        "file_sha256": digest(raw),
        "authority_sha256": value["authority_sha256"],
        "command_results_sha256": results_sha,
        "principal_id": principal,
    }


def sign_review_bundle() -> dict[str, Any]:
    manager = load_manager()
    program, current, _, _, bindings = boot_context(manager)
    if current[0].state != "_" or any(task.state != " " for task in current[1:]):
        raise PrepareError("review bundle requires theorem BOOT at underscore only")
    handoff_path, acceptance_path, review_path, final_path = manager.boot_receipt_paths(program)
    if review_path.exists() or review_path.is_symlink() or final_path.exists() or final_path.is_symlink():
        raise PrepareError("BOOT review/final receipt already exists; refusing replay")
    handoff = manager.sealed_boot_receipt(
        handoff_path, manager.BOOT_HANDOFF_FIELDS, manager.BOOT_HANDOFF_SCHEMA,
        "BOOT handoff",
    )[0]
    acceptance = manager.sealed_boot_receipt(
        acceptance_path, manager.BOOT_HANDOFF_ACCEPTANCE_FIELDS,
        manager.BOOT_HANDOFF_ACCEPTANCE_SCHEMA, "BOOT handoff acceptance",
    )[0]
    if acceptance.get("handoff_authority_sha256") != handoff.get("authority_sha256"):
        raise PrepareError("manager-owned handoff acceptance chain differs")
    command_results = manager.run_boot_commands(program)
    results_sha = manager.sha256_bytes(manager.canonical(command_results))
    # The accepted handoff binds the blank-state command replay.  Review runs
    # after the manager has atomically advanced BOOT to underscore, so its
    # snapshot and command authorities are expected to differ.  The manager
    # validates each phase against its own state and connects them through the
    # handoff-acceptance authority; cross-state byte equality would make the
    # legal blank -> underscore transition impossible.
    command_spec_sha = manager.sha256_bytes(
        manager.canonical(manager.boot_command_spec(program))
    )
    gates = list(manager.BOOT_REVIEW_GATES)
    locators: list[dict[str, str]] = []
    reviewer_principals: list[str] = []
    for ordinal in range(2):
        attestation, key, key_id, principal = role_attestation(
            manager, role="reviewer", ordinal=ordinal,
            claim_id=f"theorem-boot-reviewer-{ordinal + 1}-claim-v1",
            run_id=f"reviewer-{ordinal + 1}-{results_sha[:20]}",
        )
        unsigned = {
            "schema_version": manager.BOOT_DECISION_SCHEMA,
            "role": "reviewer", "principal_id": principal, "key_id": key_id,
            "signature_algorithm": "Ed25519", "program": program.version,
            "boot_item_id": current[0].item_id,
            "handoff_acceptance_authority_sha256": acceptance["authority_sha256"],
            "artifact_bindings": bindings,
            "reviewer_attestation": attestation,
            "decision": "pass", "conflicts": [], "passed_gates": gates,
            "command_spec_sha256": command_spec_sha,
        }
        decision = signed_document(unsigned, key)
        raw = json.dumps(
            decision, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False,
        ).encode("utf-8") + b"\n"
        receipt_sha = digest(raw)
        path = (
            manager.boot_review_archive_root(program)
            / principal
            / f"{receipt_sha}.json"
        )
        exclusive_json(path, decision)
        locators.append({
            "principal_id": principal,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": receipt_sha,
        })
        reviewer_principals.append(principal)
    master_attestation, master_key, master_key_id, master_principal = role_attestation(
        manager, role="master", ordinal=0,
        claim_id="theorem-boot-master-claim-v1",
        run_id=f"master-{results_sha[:24]}",
    )
    review_unsigned = {
        "schema_version": manager.BOOT_REVIEW_SCHEMA,
        "program": program.version,
        "boot_item_id": current[0].item_id,
        "handoff_acceptance_authority_sha256": acceptance["authority_sha256"],
        "producer_principal_id": handoff["principal_id"],
        "master_attestation": master_attestation,
        "reviewer_decisions": locators,
        "passed_gates": gates,
        "command_spec_sha256": command_spec_sha,
        "expected_command_results_sha256": results_sha,
        "artifact_bindings": bindings,
        "role": "master", "principal_id": master_principal,
        "key_id": master_key_id, "signature_algorithm": "Ed25519",
    }
    review = signed_document(review_unsigned, master_key)
    raw = exclusive_json(review_path, review)
    return {
        "path": review_path.relative_to(ROOT).as_posix(),
        "file_sha256": digest(raw),
        "authority_sha256": review["authority_sha256"],
        "command_results_sha256": results_sha,
        "reviewer_principal_ids": reviewer_principals,
        "master_principal_id": master_principal,
    }


def load_or_create_key(key_id: str, principal: str, role: str) -> tuple[Ed25519PrivateKey, dict[str, Any]]:
    PRIVATE_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(PRIVATE_ROOT, 0o700)
    path = PRIVATE_ROOT / f"{key_id}.json"
    if path.exists():
        if path.is_symlink() or not path.is_file() or (path.stat().st_mode & 0o077):
            raise PrepareError(f"private key file is unsafe: {path}")
        value = json.loads(path.read_text(encoding="utf-8"))
        if set(value) != {"schema_version", "key_id", "principal_id", "allowed_role", "private_key_hex"}:
            raise PrepareError(f"private key record fields differ: {path}")
        if value["key_id"] != key_id or value["principal_id"] != principal or value["allowed_role"] != role:
            raise PrepareError(f"private key identity differs: {path}")
        try:
            key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(value["private_key_hex"]))
        except ValueError as exc:
            raise PrepareError(f"private key is invalid: {path}") from exc
    else:
        key = Ed25519PrivateKey.generate()
        private_hex = key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        ).hex()
        value = {
            "schema_version": "awesome-theorems/stage5-local-boot-private-key/1.0",
            "key_id": key_id, "principal_id": principal,
            "allowed_role": role, "private_key_hex": private_hex,
        }
        atomic_json(path, value, 0o600)
    public_hex = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    return key, {
        "key_id": key_id, "principal_id": principal, "allowed_role": role,
        "public_key_hex": public_hex, "status": "active",
    }


def init_trust_root() -> dict[str, Any]:
    keys = [load_or_create_key(*identity)[1] for identity in PRINCIPALS]
    unsigned = {
        "schema_version": "awesome-theorems/stage5-bootstrap-role-trust-root/2.0",
        "program": PROGRAM,
        "signature_algorithm": "Ed25519",
        "keys": keys,
    }
    value = dict(unsigned)
    value["authority_sha256"] = digest(canonical(unsigned))
    atomic_json(PUBLIC_ROOT, value, 0o644)
    return {
        "public_path": PUBLIC_ROOT.relative_to(ROOT).as_posix(),
        "public_file_sha256": digest(PUBLIC_ROOT.read_bytes()),
        "public_authority_sha256": value["authority_sha256"],
        "private_root": str(PRIVATE_ROOT),
        "principals": [row[1] for row in PRINCIPALS],
    }


def materialize_operator_inputs() -> dict[str, Any]:
    manager = load_manager()
    trust = manager.operator_goal_trust_root_object(manager.THEOREM)
    if digest(manager.canonical(trust)) != manager.OPERATOR_GOAL_TRUST_ROOT_SHA256:
        raise PrepareError("manager operator trust-root object differs")
    budget = manager.operator_budget_authority_object(
        manager.THEOREM, worker_launch_authorized=True,
    )
    body = dict(budget)
    authority = body.pop("authority_sha256")
    if digest(manager.canonical(body)) != authority:
        raise PrepareError("manager operator budget authority seal differs")
    if not isinstance(authority, str) or digest(manager.canonical(body)) != authority:
        raise PrepareError("manager operator budget authority identity differs")
    atomic_json(SHARED_EVIDENCE / "operator-budget-trust-root-v1.json", trust, 0o644)
    atomic_json(SHARED_EVIDENCE / "operator-budget-v1.json", budget, 0o644)
    return {
        "trust_root_sha256": digest(canonical(trust)),
        "budget_authority_sha256": authority,
        "budget_file_sha256": digest((SHARED_EVIDENCE / "operator-budget-v1.json").read_bytes()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init-trust-root", action="store_true")
    parser.add_argument("--materialize-operator-inputs", action="store_true")
    parser.add_argument("--sign-producer-handoff", action="store_true")
    parser.add_argument("--sign-review-bundle", action="store_true")
    arguments = parser.parse_args(argv)
    if not any((
        arguments.init_trust_root, arguments.materialize_operator_inputs,
        arguments.sign_producer_handoff, arguments.sign_review_bundle,
    )):
        parser.error("select at least one action")
    try:
        result: dict[str, Any] = {}
        if arguments.init_trust_root:
            result["boot_trust_root"] = init_trust_root()
        if arguments.materialize_operator_inputs:
            result["operator_inputs"] = materialize_operator_inputs()
        if arguments.sign_producer_handoff:
            result["producer_handoff"] = sign_producer_handoff()
        if arguments.sign_review_bundle:
            result["review_bundle"] = sign_review_bundle()
    except (PrepareError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
