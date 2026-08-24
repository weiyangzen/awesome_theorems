#!/usr/bin/env python3
"""Validate and materialize the Stage5 theorem execution authorities.

This is the ongoing, repository-local checker installed by S5THM-BOOT-001.
Unlike the pristine scaffold manager it accepts ordinary checklist states, but
it never changes a checkbox.  It also contains the deterministic one-time data
materializer used by the BOOT producer; normal validation is read-only.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from typing import Any, Iterable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "Docs/Stage5_Theorems_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Theorems_Gantt.md"
EVIDENCE = ROOT / "Docs/evidence/stage5_theorems"
THEOREM_SOURCE = ROOT / "Docs/catalog/v5/releases/5.6/Theorem_List.json"
STAGE6_REGISTRY = ROOT / "Docs/catalog/v6/releases/6.0/Stage6_ID_Registry.json"
MANAGER = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
SCHEMA_CONTRACT = ROOT / "scripts/stage5_boot_schema_contract.py"
WORKSET = EVIDENCE / "workset-5.6.json"
WORKSET_RECEIPT = EVIDENCE / "workset-5.6-receipt.json"
EXECUTION_SPEC = EVIDENCE / "execution-spec.json"
FOUNDATION_PROFILES = EVIDENCE / "foundation-profiles.json"
PROVIDER_REGISTRY = EVIDENCE / "provider-registry.json"
MIGRATION_RECEIPT = (
    ROOT
    / "Docs/evidence/stage5_shared_execution"
    / "one-object-one-goal-v1-to-v2-migration.json"
)
ISOLATION_MIGRATION_DIR = ROOT / "Docs/evidence/stage5_shared_execution/blueprint-migrations"
BUDGET_OVERRUN_INVALIDATION = EVIDENCE / "execution/budget-overrun-invalidation-v1.json"
SEMANTIC_CREDIT_INVALIDATION = EVIDENCE / "execution/semantic-credit-invalidation-v1.json"
BOOT_ROLE_TRUST_ROOT = EVIDENCE / "controller-bootstrap-role-trust-root.json"

PROGRAM = "stage5-theorem-proof-debt/2.0"
FROZEN_SERVICE_TIER = "default"
BLUEPRINT_SCHEMA = "awesome-theorems/stage5-theorems-blueprint/2.0"
CHECKLIST_BEGIN = "<!-- STAGE5-PROOF-DEBT-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE5-PROOF-DEBT-EXECUTION-CHECKLIST:END -->"
SPEC_BEGIN = "<!-- STAGE5-PROOF-DEBT-EXECUTION-SPEC:BEGIN -->"
SPEC_END = "<!-- STAGE5-PROOF-DEBT-EXECUTION-SPEC:END -->"
REQUIREMENTS_BEGIN = "<!-- STAGE5-PROOF-DEBT-REQUIREMENTS:BEGIN -->"
REQUIREMENTS_END = "<!-- STAGE5-PROOF-DEBT-REQUIREMENTS:END -->"
GANTT_META_BEGIN = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:BEGIN -->"
GANTT_META_END = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:END -->"
GANTT_INDEX_BEGIN = "<!-- STAGE5-PROOF-DEBT-GANTT-INDEX:BEGIN -->"
GANTT_INDEX_END = "<!-- STAGE5-PROOF-DEBT-GANTT-INDEX:END -->"
ROW_RE = re.compile(
    r"^- \[(?P<state>[ _x])\] `(?P<id>[A-Z0-9-]+)` "
    r"(?P<title>.+?) \| depends_on=(?P<depends>[^|]+?) "
    r"\| owned_paths=(?P<paths>[^|]+?) \| gate=(?P<gate>.+)$"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ITEM_RE = re.compile(r"^S5THM-(?:BOOT-001|[0-9]{8}-TARGET|SHARD-[A-Z]+-[0-9]{3}|AGG-001|QA-001|PROGRAM-RELEASE)$")
TARGET_RE = re.compile(r"^S5THM-(?P<number>[0-9]{8})-TARGET$")
THEOREM_SOURCE_SHA256 = "c7b997fb72d0b29f055346ef49750aa5b7340667d70f38a6bc3ade7eeb4ddd6b"
THEOREM_AUTHORITY_SHA256 = "9a9388c4df2b27fa051b451f4a3dc56afa6fe7dd147a5aaa1e7c28c76df77015"
STAGE6_REGISTRY_SHA256 = "eb531fec1312927f8f7df6b5f21f5729ee96f2be86ddaa9af6c15165e58979ff"
STAGE6_REGISTRY_AUTHORITY_SHA256 = "da198be5b4b3acd43cad7049123b6942e22eecfe2c9b23e2d39fbe9161b47d0c"
LEGACY_V1_BLUEPRINT_SHA256 = "5cb94720290319522b5f1d8341828ac2aaacb6404ce763dfeca69b9c45bf7806"
LEGACY_V1_GANTT_SHA256 = "757713ba55ce615ff48f4490399fe84a8fbd060f27201ab130075d436b1df01f"


class CheckError(RuntimeError):
    pass


def verify_signed_role(value: Any, role: str, label: str) -> dict[str, Any]:
    trust = verify_seal(
        strict_json(BOOT_ROLE_TRUST_ROOT.read_bytes(), "BOOT role trust root"),
        "BOOT role trust root",
    )
    keys = {row["key_id"]: row for row in trust.get("keys", []) if isinstance(row, dict)}
    if not isinstance(value, dict):
        raise CheckError(f"{label}: signed document is malformed")
    key = keys.get(value.get("key_id"))
    if (
        value.get("schema_version") != "awesome-theorems/stage5-controller-successor-signed/1.0"
        or value.get("program") != PROGRAM or value.get("role") != role
        or value.get("signature_algorithm") != "Ed25519"
        or not isinstance(value.get("payload"), dict)
        or not isinstance(key, dict) or key.get("allowed_role") != role
        or key.get("principal_id") != value.get("principal_id")
    ):
        raise CheckError(f"{label}: signed role identity differs")
    unsigned = {
        name: value[name] for name in (
            "schema_version", "program", "role", "principal_id", "key_id",
            "signature_algorithm", "payload",
        )
    }
    signed_sha = value.get("signed_payload_sha256")
    signature = value.get("signature")
    if (
        signed_sha != sha256_bytes(canonical(unsigned))
        or not isinstance(signature, str) or re.fullmatch(r"[0-9a-f]{128}", signature) is None
        or value.get("authority_sha256") != sha256_bytes(canonical({
            **unsigned, "signed_payload_sha256": signed_sha, "signature": signature,
        }))
    ):
        raise CheckError(f"{label}: signature envelope differs")
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(key["public_key_hex"])).verify(
            bytes.fromhex(signature), canonical(unsigned),
        )
    except (ValueError, InvalidSignature) as exc:
        raise CheckError(f"{label}: Ed25519 signature is invalid") from exc
    return value


def validate_budget_overrun_invalidation(
    rows: list[dict[str, Any]], blueprint_raw: bytes,
) -> dict[str, Any] | None:
    if not BUDGET_OVERRUN_INVALIDATION.is_file() or BUDGET_OVERRUN_INVALIDATION.is_symlink():
        return None
    master = verify_signed_role(
        strict_json(BUDGET_OVERRUN_INVALIDATION.read_bytes(), "budget overrun invalidation"),
        "master", "budget overrun invalidation",
    )
    payload = master["payload"]
    if (
        payload.get("item_id") != "S5THM-00003496-TARGET"
        or not isinstance(payload.get("migration_id"), str)
        or re.fullmatch(r"[0-9a-f]{64}", payload["migration_id"]) is None
    ):
        raise CheckError("budget overrun invalidation identity differs")
    migration_id = payload["migration_id"]
    epoch_prefix = (
        EVIDENCE / "execution/budget-overrun-invalidations" / migration_id
    )
    producer_locator = payload.get("producer")
    reviewer_locators = payload.get("reviewers")
    if not isinstance(producer_locator, dict) or not isinstance(reviewer_locators, list) or len(reviewer_locators) != 2:
        raise CheckError("budget overrun invalidation review locators differ")

    def locator_path(locator: dict[str, Any], label: str) -> Path:
        relative = locator.get("path")
        if not isinstance(relative, str):
            raise CheckError(f"{label}: path is malformed")
        path = ROOT / PurePosixPath(relative)
        try:
            path.relative_to(epoch_prefix)
        except ValueError as exc:
            raise CheckError(f"{label}: path is outside invalidation epoch") from exc
        return path

    producer_path = locator_path(producer_locator, "budget invalidation producer")
    producer_raw = producer_path.read_bytes()
    producer = verify_signed_role(
        strict_json(producer_raw, "budget invalidation producer"),
        "producer", "budget invalidation producer",
    )
    subject = producer.get("payload", {}).get("review_subject")
    subject_sha = producer.get("payload", {}).get("review_subject_sha256")
    if (
        sha256_bytes(producer_raw) != producer_locator.get("file_sha256")
        or producer["authority_sha256"] != producer_locator.get("authority_sha256")
        or not isinstance(subject, dict) or sha256_bytes(canonical(subject)) != subject_sha
        or subject_sha != payload.get("review_subject_sha256")
        or producer.get("payload", {}).get("decision") != "self_tested"
        or producer.get("payload", {}).get("conflicts") != []
    ):
        raise CheckError("budget overrun invalidation producer differs")
    subject_fields = {
        "item_id", "invalidated_master_acceptance", "overrun_generation",
        "pre", "post", "preserved_master_accepted_item_ids",
    }
    if set(subject) != subject_fields or any(payload.get(name) != subject[name] for name in subject_fields):
        raise CheckError("budget overrun invalidation reviewed subject differs")
    principals = {master["principal_id"], producer["principal_id"]}
    reviewer_authorities = []
    for index, locator in enumerate(reviewer_locators):
        path = locator_path(locator, f"budget invalidation reviewer {index + 1}")
        raw = path.read_bytes()
        reviewer = verify_signed_role(
            strict_json(raw, f"budget invalidation reviewer {index + 1}"),
            "reviewer", f"budget invalidation reviewer {index + 1}",
        )
        if (
            sha256_bytes(raw) != locator.get("file_sha256")
            or reviewer["authority_sha256"] != locator.get("authority_sha256")
            or reviewer.get("payload", {}).get("producer_authority_sha256") != producer["authority_sha256"]
            or reviewer.get("payload", {}).get("review_subject_sha256") != subject_sha
            or reviewer.get("payload", {}).get("decision") != "pass"
            or reviewer.get("payload", {}).get("conflicts") != []
        ):
            raise CheckError("budget overrun invalidation reviewer differs")
        principals.add(reviewer["principal_id"])
        reviewer_authorities.append(reviewer["authority_sha256"])
    if len(principals) != 4 or reviewer_authorities != payload.get("reviewer_authorities"):
        raise CheckError("budget overrun invalidation principals differ")
    post = payload.get("post", {})
    pre = payload.get("pre", {})
    post_blueprint = locator_path(
        {"path": post.get("blueprint_path")}, "budget invalidation post Blueprint",
    )
    post_gantt = locator_path(
        {"path": post.get("gantt_path")}, "budget invalidation post Gantt",
    )
    if (
        sha256_file(post_blueprint) != post.get("blueprint_sha256")
        or sha256_file(post_gantt) != post.get("gantt_sha256")
    ):
        raise CheckError("budget overrun invalidation post projections differ")
    # The invalidation archive binds the exact Gantt written with the
    # x-to-blank transition.  The active Gantt is an ongoing runtime
    # projection and legitimately changes on every reconcile/refill; its
    # current bytes are independently regenerated and checked by
    # validate_gantt(), rather than being frozen to this historical snapshot.
    pre_blueprint = locator_path(
        {"path": pre.get("blueprint_path")}, "budget invalidation pre Blueprint",
    )
    if sha256_file(pre_blueprint) != pre.get("blueprint_sha256"):
        raise CheckError("budget overrun invalidation pre Blueprint differs")
    _, pre_rows, _ = parse_blueprint(pre_blueprint)
    _, archived_post_rows, _ = parse_blueprint(post_blueprint)
    pre_states = {row["item_id"]: row["state"] for row in pre_rows}
    post_states = {row["item_id"]: row["state"] for row in archived_post_rows}
    changed = [item for item in pre_states if pre_states[item] != post_states[item]]
    current_states = {row["item_id"]: row["state"] for row in rows}
    if (
        changed != [payload["item_id"]]
        or pre_states[payload["item_id"]] != "x"
        or post_states[payload["item_id"]] != " "
        or current_states[payload["item_id"]] != " "
    ):
        raise CheckError("budget overrun invalidation is not the unique reviewed x-to-blank transition")
    preserved = [
        row["item_id"] for row in archived_post_rows if row["state"] == "x"
    ]
    if preserved != payload.get("preserved_master_accepted_item_ids"):
        raise CheckError("budget overrun invalidation preserved acceptance set differs")
    overrun = payload.get("overrun_generation", {})
    acceptance = payload.get("invalidated_master_acceptance", {})
    acceptance_path = ROOT / PurePosixPath(str(acceptance.get("path", "")))
    acceptance_raw = acceptance_path.read_bytes()
    acceptance_value = verify_seal(
        strict_json(acceptance_raw, "invalidated Master acceptance"),
        "invalidated Master acceptance",
    )
    if (
        sha256_bytes(acceptance_raw) != acceptance.get("file_sha256")
        or acceptance_value.get("authority_sha256") != acceptance.get("authority_sha256")
        or acceptance_value.get("handoff", {}).get("run_id") != acceptance.get("run_id")
        or overrun.get("run_id") != acceptance.get("run_id")
        or overrun.get("claim_model_input_tokens") != 2_000_000
        or not isinstance(overrun.get("measured_goal_tokens_used"), int)
        or overrun["measured_goal_tokens_used"] <= overrun["claim_model_input_tokens"]
        or overrun.get("violation") != "model_input_token_budget_exceeded"
    ):
        raise CheckError("budget overrun invalidation evidence differs")
    return master


def validate_semantic_credit_invalidation(
    rows: list[dict[str, Any]], blueprint_raw: bytes,
) -> dict[str, Any] | None:
    if not SEMANTIC_CREDIT_INVALIDATION.is_file() or SEMANTIC_CREDIT_INVALIDATION.is_symlink():
        return None
    master = verify_signed_role(
        strict_json(SEMANTIC_CREDIT_INVALIDATION.read_bytes(), "semantic credit invalidation"),
        "master", "semantic credit invalidation",
    )
    payload = master.get("payload", {})
    migration_id = payload.get("migration_id")
    invalidated = payload.get("invalidated")
    if (
        not isinstance(migration_id, str) or re.fullmatch(r"[0-9a-f]{64}", migration_id) is None
        or not isinstance(invalidated, list) or not invalidated
        or not isinstance(payload.get("validator_sha256"), str)
        or re.fullmatch(r"[0-9a-f]{64}", payload["validator_sha256"]) is None
    ):
        raise CheckError("semantic credit invalidation identity differs")
    epoch = EVIDENCE / "execution/semantic-credit-invalidations" / migration_id

    def repository_path(value: Any, label: str) -> Path:
        if not isinstance(value, str):
            raise CheckError(f"{label}: path is malformed")
        relative = PurePosixPath(value)
        if (
            not value or relative.is_absolute() or value != relative.as_posix()
            or ".." in relative.parts
        ):
            raise CheckError(f"{label}: path is not a safe repository-relative path")
        path = ROOT / relative
        if path.is_symlink() or not path.is_file():
            raise CheckError(f"{label}: regular file is absent")
        return path

    def epoch_path(value: Any, label: str) -> Path:
        path = repository_path(value, label)
        try:
            path.relative_to(epoch)
        except ValueError as exc:
            raise CheckError(f"{label}: path is outside invalidation epoch") from exc
        return path

    producer_locator = payload.get("producer")
    reviewers = payload.get("reviewers")
    if not isinstance(producer_locator, dict) or not isinstance(reviewers, list) or len(reviewers) != 2:
        raise CheckError("semantic credit invalidation review locators differ")
    producer_path = epoch_path(producer_locator.get("path"), "semantic invalidation producer")
    producer_raw = producer_path.read_bytes()
    producer = verify_signed_role(
        strict_json(producer_raw, "semantic invalidation producer"),
        "producer", "semantic invalidation producer",
    )
    subject = producer.get("payload", {}).get("review_subject")
    subject_sha = producer.get("payload", {}).get("review_subject_sha256")
    subject_fields = {
        "invalidated", "pre", "post", "preserved_master_accepted_item_ids",
        "validator_sha256",
    }
    if (
        sha256_bytes(producer_raw) != producer_locator.get("file_sha256")
        or producer["authority_sha256"] != producer_locator.get("authority_sha256")
        or not isinstance(subject, dict) or set(subject) != subject_fields
        or sha256_bytes(canonical(subject)) != subject_sha
        or subject_sha != payload.get("review_subject_sha256")
        or any(payload.get(key) != subject[key] for key in subject_fields)
        or producer.get("payload", {}).get("decision") != "self_tested"
        or producer.get("payload", {}).get("conflicts") != []
    ):
        raise CheckError("semantic credit invalidation producer differs")
    principals = {master["principal_id"], producer["principal_id"]}
    authorities: list[str] = []
    for index, locator in enumerate(reviewers):
        if not isinstance(locator, dict):
            raise CheckError("semantic credit invalidation reviewer locator differs")
        path = epoch_path(locator.get("path"), f"semantic invalidation reviewer {index + 1}")
        raw = path.read_bytes()
        reviewer = verify_signed_role(
            strict_json(raw, f"semantic invalidation reviewer {index + 1}"),
            "reviewer", f"semantic invalidation reviewer {index + 1}",
        )
        if (
            sha256_bytes(raw) != locator.get("file_sha256")
            or reviewer["authority_sha256"] != locator.get("authority_sha256")
            or reviewer.get("payload", {}).get("producer_authority_sha256")
            != producer["authority_sha256"]
            or reviewer.get("payload", {}).get("review_subject_sha256") != subject_sha
            or reviewer.get("payload", {}).get("decision") != "pass"
            or reviewer.get("payload", {}).get("conflicts") != []
        ):
            raise CheckError("semantic credit invalidation reviewer differs")
        principals.add(reviewer["principal_id"])
        authorities.append(reviewer["authority_sha256"])
    if len(principals) != 4 or authorities != payload.get("reviewer_authorities"):
        raise CheckError("semantic credit invalidation principals differ")
    item_ids = []
    for entry in invalidated:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("item_id"), str)
            or entry.get("replay_exit_code") != 1
            or not isinstance(entry.get("replay_failure"), str)
            or sha256_bytes(entry["replay_failure"].encode())
            != entry.get("replay_failure_sha256")
        ):
            raise CheckError("semantic credit invalidation replay evidence differs")
        receipt_path = repository_path(
            entry.get("master_receipt_path"), "semantic invalidated Master receipt",
        )
        claim_path = repository_path(
            entry.get("claim_path"), "semantic invalidated claim",
        )
        receipt_raw = receipt_path.read_bytes()
        receipt = verify_seal(strict_json(receipt_raw, "semantic invalidated Master receipt"),
                              "semantic invalidated Master receipt")
        claim_raw = claim_path.read_bytes()
        claim = strict_json(claim_raw, "semantic invalidated claim")
        if (
            sha256_bytes(receipt_raw) != entry.get("master_receipt_file_sha256")
            or receipt.get("authority_sha256") != entry.get("master_receipt_authority_sha256")
            or receipt.get("item_id") != entry["item_id"]
            or receipt.get("handoff", {}).get("run_id") != entry.get("run_id")
            or sha256_bytes(claim_raw) != entry.get("claim_sha256")
            or claim.get("item_id") != entry["item_id"]
            or claim.get("run_id") != entry.get("run_id")
        ):
            raise CheckError("semantic credit invalidation Master/claim binding differs")
        item_ids.append(entry["item_id"])
    if item_ids != sorted(item_ids) or len(item_ids) != len(set(item_ids)):
        raise CheckError("semantic credit invalidation item set differs")
    pre = payload.get("pre", {})
    post = payload.get("post", {})
    projection_fields = {
        "blueprint_path", "blueprint_sha256", "gantt_path", "gantt_sha256",
        "state_path", "state_sha256",
    }
    if set(pre) != projection_fields or set(post) != projection_fields:
        raise CheckError("semantic credit invalidation projection locators differ")
    pre_blueprint = epoch_path(pre.get("blueprint_path"), "semantic invalidation pre Blueprint")
    post_blueprint = epoch_path(post.get("blueprint_path"), "semantic invalidation post Blueprint")
    for projection, label in ((pre, "pre"), (post, "post")):
        for kind in ("blueprint", "gantt", "state"):
            path = epoch_path(
                projection[f"{kind}_path"],
                f"semantic invalidation {label} {kind}",
            )
            if sha256_file(path) != projection[f"{kind}_sha256"]:
                raise CheckError("semantic credit invalidation archived projection differs")
    if (
        post_blueprint.read_bytes() != blueprint_raw
    ):
        raise CheckError("semantic credit invalidation Blueprint projections differ")
    _, pre_rows, _ = parse_blueprint(pre_blueprint)
    pre_states = {row["item_id"]: row["state"] for row in pre_rows}
    post_states = {row["item_id"]: row["state"] for row in rows}
    changed = sorted(key for key in pre_states if pre_states[key] != post_states[key])
    if (
        changed != item_ids
        or any(pre_states[key] != "x" or post_states[key] != " " for key in item_ids)
        or [row["item_id"] for row in rows if row["state"] == "x"]
        != payload.get("preserved_master_accepted_item_ids")
    ):
        raise CheckError("semantic credit invalidation is not the reviewed x-to-blank batch")
    replay_identity = [{
        "item_id": entry["item_id"], "run_id": entry["run_id"],
        "master_receipt_file_sha256": entry["master_receipt_file_sha256"],
        "replay_failure_sha256": entry["replay_failure_sha256"],
    } for entry in invalidated]
    expected_migration_id = sha256_bytes(canonical({
        "schema_version": "awesome-theorems/stage5-semantic-credit-invalidation-id/1.0",
        "program": PROGRAM, "invalidated": replay_identity,
        "pre_blueprint_sha256": pre["blueprint_sha256"],
        "post_blueprint_sha256": post["blueprint_sha256"],
        "pre_state_sha256": pre["state_sha256"],
        "post_state_sha256": post["state_sha256"],
        "validator_sha256": payload.get("validator_sha256"),
    }))
    if migration_id != expected_migration_id:
        raise CheckError("semantic credit invalidation content address differs")
    return master


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise CheckError("value is not canonical finite JSON") from exc


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise CheckError(f"{label}: duplicate key {key!r}")
            result[key] = value
        return result

    def constant(value: str) -> Any:
        raise CheckError(f"{label}: non-finite number {value}")

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CheckError(f"{label}: invalid strict UTF-8 JSON") from exc


def sealed(unsigned: dict[str, Any]) -> dict[str, Any]:
    result = dict(unsigned)
    result["authority_sha256"] = sha256_bytes(canonical(unsigned))
    return result


def verify_seal(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CheckError(f"{label}: expected object")
    authority = value.get("authority_sha256")
    body = dict(value)
    body.pop("authority_sha256", None)
    if not isinstance(authority, str) or not SHA256_RE.fullmatch(authority):
        raise CheckError(f"{label}: missing authority seal")
    if sha256_bytes(canonical(body)) != authority:
        raise CheckError(f"{label}: authority seal mismatch")
    return value


def atomic_write(path: Path, raw: bytes, mode: int = 0o644) -> None:
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


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(
        path,
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n",
    )


def extract_once(text: str, begin: str, end: str, label: str) -> str:
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) >= text.index(end):
        raise CheckError(f"{label}: marker identity/order differs")
    return text.split(begin, 1)[1].split(end, 1)[0]


def parse_spec(text: str) -> dict[str, Any]:
    block = extract_once(text, SPEC_BEGIN, SPEC_END, "execution specification").strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise CheckError("execution specification fence differs")
    value = strict_json(block[8:-4].encode("utf-8"), "execution specification")
    if not isinstance(value, dict):
        raise CheckError("execution specification is not an object")
    return value


def split_list(value: str) -> tuple[str, ...]:
    if value.strip() == "-":
        return ()
    result = tuple(piece.strip() for piece in value.split(","))
    if not result or any(not piece for piece in result) or len(result) != len(set(result)):
        raise CheckError(f"malformed list field {value!r}")
    return result


def safe_owned_path(value: str, item_id: str) -> None:
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or value != path.as_posix() or ".." in path.parts
        or path.parts[0] in {".git", ".ops"}
        or any(character in value for character in "|`<>\\*?[]{}")
    ):
        raise CheckError(f"{item_id}: unsafe owned path {value!r}")


def parse_blueprint(path: Path = BLUEPRINT) -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CheckError("Blueprint is not UTF-8") from exc
    specification = parse_spec(text)
    block = extract_once(text, CHECKLIST_BEGIN, CHECKLIST_END, "checklist")
    rows: list[dict[str, Any]] = []
    for line in block.splitlines():
        if not line.strip():
            continue
        match = ROW_RE.fullmatch(line)
        if match is None:
            raise CheckError(f"malformed checklist row: {line[:160]!r}")
        item_id = match.group("id")
        if not ITEM_RE.fullmatch(item_id):
            raise CheckError(f"unsupported theorem item ID {item_id}")
        dependencies = split_list(match.group("depends"))
        owned_paths = split_list(match.group("paths"))
        for owned in owned_paths:
            safe_owned_path(owned, item_id)
        gate = match.group("gate")
        if len(gate) < 80:
            raise CheckError(f"{item_id}: gate is too weak")
        rows.append({
            "item_id": item_id,
            "state": match.group("state"),
            "title": match.group("title"),
            "dependencies": dependencies,
            "owned_paths": owned_paths,
            "gate": gate,
        })
    validate_rows(rows)
    return specification, rows, raw


def validate_rows(rows: list[dict[str, Any]]) -> None:
    if len(rows) != 3575:
        raise CheckError(f"theorem checklist cardinality differs: {len(rows)}")
    ids = [row["item_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise CheckError("duplicate checklist item ID")
    by_id = {row["item_id"]: row for row in rows}
    if ids[0] != "S5THM-BOOT-001" or ids[-1] != "S5THM-PROGRAM-RELEASE":
        raise CheckError("BOOT/program-release boundary differs")
    targets = [row for row in rows if TARGET_RE.fullmatch(row["item_id"])]
    if len(targets) != 3500:
        raise CheckError(f"theorem TARGET cardinality differs: {len(targets)}")
    target_numbers = [TARGET_RE.fullmatch(row["item_id"]).group("number") for row in targets]
    if len(target_numbers) != len(set(target_numbers)):
        raise CheckError("duplicate theorem mathematical TARGET identity")
    for row in targets:
        if row["dependencies"] != ("S5THM-BOOT-001",):
            raise CheckError(f"{row['item_id']}: mathematical TARGET is not BOOT-only independent")
        if "one isolated tmux and one /goal" not in row["title"]:
            raise CheckError(f"{row['item_id']}: one-object/one-tmux title contract missing")
        gate = row["gate"]
        required_clauses = (
            ("task-local tmux server/socket/session", "one task-local tmux"),
            ("private writable CODEX_HOME",),
            ("thread",),
            ("exactly one submitted /goal", "exactly one active /goal"),
            ("may never claim another mathematical ID", "or claim another mathematical ID"),
            ("no generation may inspect another task root",),
            ("transitive non-foundation constant environment",),
            ("may not shadow or reinterpret source symbols",),
            ("semantic-substitution mutations",),
            ("strict-dominance certificate",),
            ("Distilled output removes duplication",),
        )
        for alternatives in required_clauses:
            if not any(clause in gate for clause in alternatives):
                raise CheckError(f"{row['item_id']}: worker bijection clause missing: {alternatives[0]}")
    owners: dict[str, str] = {}
    children: dict[str, list[str]] = {item_id: [] for item_id in ids}
    indegree = {item_id: 0 for item_id in ids}
    for row in rows:
        item_id = row["item_id"]
        for dependency in row["dependencies"]:
            if dependency not in by_id or dependency == item_id:
                raise CheckError(f"{item_id}: missing/self dependency {dependency}")
            if by_id[dependency]["state"] != "x" and row["state"] in {"_", "x"}:
                raise CheckError(f"{item_id}: advanced before dependency {dependency}")
            children[dependency].append(item_id)
            indegree[item_id] += 1
        for owned in row["owned_paths"]:
            if owned in owners:
                raise CheckError(f"owned path collision {owned}: {owners[owned]} vs {item_id}")
            owners[owned] = item_id
    for owned in owners:
        parent = PurePosixPath(owned).parent
        while parent != PurePosixPath("."):
            if parent.as_posix() in owners:
                raise CheckError(f"owned path prefix collision: {parent} vs {owned}")
            parent = parent.parent
    queue = deque(sorted(item_id for item_id, count in indegree.items() if count == 0))
    visited: list[str] = []
    while queue:
        current = queue.popleft()
        visited.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(visited) != len(rows):
        raise CheckError("checklist dependency graph contains a cycle")
    ancestors: set[str] = set()
    stack = list(by_id["S5THM-PROGRAM-RELEASE"]["dependencies"])
    while stack:
        current = stack.pop()
        if current in ancestors:
            continue
        ancestors.add(current)
        stack.extend(by_id[current]["dependencies"])
    if ancestors != set(ids) - {"S5THM-PROGRAM-RELEASE"}:
        raise CheckError("program release does not cover the complete DAG")


def validate_spec(specification: dict[str, Any]) -> None:
    required = {
        "schema_version": "awesome-theorems/stage5-proof-debt-execution-spec/2.0",
        "program": PROGRAM,
        "blueprint_schema": BLUEPRINT_SCHEMA,
        "authoritative_blueprint": "Docs/Stage5_Theorems_Blueprint.md",
        "gantt_projection": "Docs/Stage5_Theorems_Gantt.md",
        "runtime_root": ".ops/stage5-theorems-execution-v2",
        "shared_runtime_root": None,
        "worker_platform": "codex",
        "worker_transport": "tmux_codex_tui",
        "goal_command": "/goal",
    }
    for key, expected in required.items():
        if specification.get(key) != expected:
            raise CheckError(f"execution specification {key} differs")
    route = specification.get("route_policy")
    if route != {
        "provider": "sub2api",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "ultra",
        "service_tier": FROZEN_SERVICE_TIER,
        "rule": route.get("rule") if isinstance(route, dict) else None,
    }:
        raise CheckError("frozen Codex route differs")
    nested = specification.get("nested_agent_policy")
    if not isinstance(nested, dict) or nested.get("enabled") is not True:
        raise CheckError("reviewed theorem subagent authority is missing")
    if set(nested) != {
        "enabled", "operator_authority", "capacity_rule", "transport_rule",
        "identity_rule", "disabled_feature_boundary",
    }:
        raise CheckError("theorem nested-agent policy has an unknown or missing field")
    if (
        "parent plus children never exceed 24" not in str(nested.get("capacity_rule", ""))
        or "every admitted child generation must use its own task-local tmux" not in str(nested.get("transport_rule", ""))
        or "distinct claim/run/execution identity" not in str(nested.get("identity_rule", ""))
        or "subagents are admitted only by the controller as first-class executions" not in str(nested.get("disabled_feature_boundary", ""))
    ):
        raise CheckError("theorem subagents are not independently isolated and globally accounted")
    if "single_thread_policy" in specification:
        raise CheckError("obsolete blanket subagent prohibition remains in the execution specification")
    if "default_limits" in specification or "default_host_headroom" in specification:
        raise CheckError("concurrency defaults are forbidden; use an explicit operator prompt")
    contract = specification.get("concurrency_prompt_contract")
    required_dimensions = {
        "logical_claims", "service_records", "agent_executions", "startup_reservations",
        "launch_fanout_per_wave", "live_transports", "authenticated_goals", "running_turns",
        "outbound_request_starts_per_window", "in_flight_requests", "integration", "validators",
        "exact_path_conflicts",
    }
    if not isinstance(contract, dict) or set(contract.get("required_dimensions", [])) != required_dimensions:
        raise CheckError("complete prompt concurrency dimension contract is missing")
    if contract.get("value_source") != "explicit_execution_prompt_only" or contract.get("missing_policy") != "fail_closed_before_materialization_or_launch":
        raise CheckError("prompt must be explicit and fail closed before side effects")
    limits = contract.get("execution_limits")
    recovery = contract.get("recovery")
    if not isinstance(limits, dict) or set(limits) != {
        "generation_lifetime_seconds", "model_input_tokens", "model_output_tokens",
        "model_turns", "cpu_seconds", "external_launches",
    } or limits.get("generation_lifetime_seconds") != 1209600 or limits.get("model_turns") != "unbounded":
        raise CheckError("explicit fourteen-day/unlimited-turn execution limits are missing")
    if not isinstance(recovery, dict) or set(recovery) != {
        "startup_attempts_per_generation", "provider_attempts_per_request",
        "repair_attempts_per_failure_identity", "generation_replacements_per_work_item",
        "backoff_initial_seconds", "backoff_max_seconds", "backoff_multiplier",
        "backoff_jitter_ratio", "retry_after_precedence", "breaker_scope",
        "breaker_failure_threshold", "breaker_cooldown_seconds", "breaker_failure_classes",
    } or recovery.get("generation_replacements_per_work_item") != 60 or recovery.get("provider_attempts_per_request") != 60 or recovery.get("backoff_initial_seconds") != 60 or recovery.get("backoff_max_seconds") != 3600 or recovery.get("backoff_multiplier") != 2 or recovery.get("retry_after_precedence") != "provider_retry_after_then_exponential" or recovery.get("breaker_scope") != "provider" or recovery.get("breaker_failure_threshold") != 3 or recovery.get("breaker_cooldown_seconds") != 1800 or set(recovery.get("breaker_failure_classes", [])) != {"http_429", "http_503", "provider_unavailable"}:
        raise CheckError("explicit recovery/backoff/breaker policy is missing")
    if "shared_coordination" in specification:
        raise CheckError("shared theorem/conjecture coordinator remains in v2 specification")
    coordination = specification.get("coordination_authority")
    if not isinstance(coordination, dict) or coordination.get("root") != specification["runtime_root"]:
        raise CheckError("program-local coordination authority is missing or points outside this runtime")
    if "caps" in coordination or coordination.get("concurrency_prompt_contract") != contract:
        raise CheckError("program-local coordination must bind the prompt contract, not frozen caps")
    program_coordination = specification.get("program_coordination", {})
    if "no combined total" not in str(program_coordination.get("no_cross_program_pool", "")):
        raise CheckError("cross-program pool prohibition is missing")
    forbidden = set(specification.get("forbidden_transports", []))
    expected_forbidden = {
        "codex_app_server", "app_server_json_rpc", "codex_exec",
        "shared_codex_daemon", "shared_tmux_server",
        "shared_writable_CODEX_HOME", "no_tmux_codex",
        "docker_worker_transport", "container_worker_transport",
    }
    if forbidden != expected_forbidden:
        raise CheckError("forbidden transport set differs")
    if "worker_container_boundary" in specification:
        raise CheckError("legacy worker container boundary remains in v2 specification")
    boundary = specification.get("worker_runtime_boundary", {})
    if boundary.get("worker_container_transport") != "forbidden":
        raise CheckError("Docker/container worker transport is not forbidden")
    if boundary.get("tmux_topology") != "one private tmux server/socket/session per claim; never multiple mathematical objects in windows or panes of one server":
        raise CheckError("task-local tmux topology differs")
    object_protocol = specification.get("mathematical_object_worker_protocol", {})
    if object_protocol.get("no_second_id") != "a TARGET worker may not claim, edit or opportunistically complete any second mathematical or source-occurrence ID":
        raise CheckError("one mathematical ID per worker contract differs")
    if "opens no reviewer worker" not in str(object_protocol.get("review", "")):
        raise CheckError("reviewer worker prohibition differs")
    contract = specification.get("theorem_acceptance_contract")
    required_contract_fields = {
        "fixture_role", "strict_dominance", "semantic_identity",
        "machine_completion", "readable_completion", "trace",
        "distilled", "release_conjunction",
    }
    if not isinstance(contract, dict) or set(contract) != required_contract_fields:
        raise CheckError("closed theorem acceptance contract differs")
    if "incomplete H1/M2/R0 negative fixture" not in contract["fixture_role"]:
        raise CheckError("THM-M-0387 is not bound as an incomplete negative fixture")
    if (
        "elaborated root expression" not in contract["semantic_identity"]
        or "reject local definition" not in contract["semantic_identity"]
        or "strictly adds" not in contract["strict_dominance"]
        or "retaining every hypothesis" not in contract["distilled"]
        or "exact semantic binding and M0 and R0" not in contract["release_conjunction"]
    ):
        raise CheckError("theorem dominance/semantic/distilled predicates are incomplete")
    profiles = specification.get("validation_profiles", [])
    for profile in (
        "transitive_semantic_environment_and_no_shadowing",
        "strict_dominance_over_m0387_negative_fixture",
        "distilled_proof_sufficiency_and_nonduplication",
    ):
        if profile not in profiles:
            raise CheckError(f"mandatory theorem validation profile is missing: {profile}")


def task_authority(row: dict[str, Any]) -> str:
    return sha256_bytes(canonical({
        "item_id": row["item_id"], "title": row["title"],
        "dependencies": list(row["dependencies"]),
        "owned_paths": list(row["owned_paths"]), "gate": row["gate"],
    }))


def dag_object(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "item_id": row["item_id"],
        "dependencies": list(row["dependencies"]),
        "owned_paths": list(row["owned_paths"]),
        "task_authority_sha256": task_authority(row),
    } for row in rows]


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise CheckError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def materialize_boot_data() -> None:
    """Generate closed BOOT data from the sealed source and current manager."""
    if sha256_file(THEOREM_SOURCE) != THEOREM_SOURCE_SHA256:
        raise CheckError("sealed theorem source SHA drift")
    if sha256_file(STAGE6_REGISTRY) != STAGE6_REGISTRY_SHA256:
        raise CheckError("sealed Stage6 registry SHA drift")
    manager = load_module(MANAGER, "stage5_manager_for_theorem_boot")
    schema_contract = load_module(SCHEMA_CONTRACT, "stage5_boot_schema_contract_for_theorem_boot")
    specification, rows, blueprint_raw = parse_blueprint()
    canonical_spec = manager.spec_object(manager.THEOREM)
    if specification != canonical_spec:
        raise CheckError("Blueprint specification is not the current canonical manager specification")
    source = verify_seal(strict_json(THEOREM_SOURCE.read_bytes(), "theorem source"), "theorem source")
    if source.get("authority_sha256") != THEOREM_AUTHORITY_SHA256:
        raise CheckError("theorem source authority drift")
    records = source.get("records")
    if not isinstance(records, list) or len(records) != 3500:
        raise CheckError("theorem source cardinality differs")
    stage6 = verify_seal(strict_json(STAGE6_REGISTRY.read_bytes(), "Stage6 registry"), "Stage6 registry")
    if stage6.get("authority_sha256") != STAGE6_REGISTRY_AUTHORITY_SHA256:
        raise CheckError("Stage6 registry authority drift")
    aliases: dict[str, dict[str, Any]] = {}
    for entry in stage6.get("claims", []):
        parent = entry.get("parent_s5_claim_id")
        if isinstance(parent, str):
            aliases[parent] = {
                "stage6_claim_id": entry.get("stage6_claim_id"),
                "stage6_variant_id": entry.get("stage6_variant_id"),
                "parent_variant_id": entry.get("parent_variant_id"),
                "current_resolution_kind": (entry.get("current_resolution") or {}).get("kind"),
            }
    by_item = {row["item_id"]: row for row in rows}
    members: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    for record in records:
        stage_id = record.get("stage_claim_id")
        if not isinstance(stage_id, str) or not re.fullmatch(r"S5-CLM-[0-9]{8}", stage_id):
            raise CheckError("theorem record has invalid Stage5 ID")
        number = stage_id.rsplit("-", 1)[1]
        target_item_id = f"S5THM-{number}-TARGET"
        if target_item_id not in by_item:
            raise CheckError(f"{stage_id}: one-object TARGET is missing")
        proof = record.get("proof_evidence")
        formal = record.get("formal_statement") if isinstance(record.get("formal_statement"), dict) else {}
        if isinstance(proof, dict):
            cohort = "ML-KERNEL"
            baseline_axioms = proof.get("batch_axiom_dependency_union", [])
            provider = "mathlib-8a178386"
        else:
            baseline_axioms = formal.get("axioms", [])
            cohort = "FC-SORRY" if "sorryAx" in baseline_axioms else "FC-REPLAY"
            provider = "formal-conjectures-2270d31e"
            baseline_axioms = [] if "sorryAx" in baseline_axioms else baseline_axioms
        alias = aliases.get(stage_id)
        if alias is None or alias.get("parent_variant_id") != record.get("variant_id"):
            raise CheckError(f"{stage_id}: Stage6 alias differs")
        record_sha = sha256_bytes(canonical(record))
        member = {
            "stage_claim_id": stage_id,
            "variant_id": record.get("variant_id"),
            "family_id": record.get("family_id"),
            "stage6_alias": alias,
            "cohort": cohort,
            "provider_id": provider,
            "record_sha256": record_sha,
            "semantic_payload_sha256": record.get("semantic_payload_sha256"),
            "statement_sha256": record.get("statement_sha256"),
            "formal_type_sha256": record.get("formal_type_sha256"),
            "display_name": record.get("display_name"),
            "qualified_name": record.get("qualified_name"),
            "module": record.get("module"),
            "source_id": record.get("source_id"),
            "source_locator": record.get("locator") or formal.get("locator"),
            "formal_statement": formal,
            "proof_evidence": proof,
            "target_item_id": target_item_id,
            "target_task_authority_sha256": task_authority(by_item[target_item_id]),
            "internal_subchecklist": [
                "INTAKE", "STATEMENT", "ANCHOR", "TREE", "MACHINE",
                "READABLE", "VALIDATE", "RELEASE",
            ],
            "worker_bijection": "one theorem, one TARGET, one task-local tmux, one private CODEX_HOME, one thread, one active /goal",
        }
        members.append(member)
        profile_body = {
            "stage_claim_id": stage_id,
            "profile_version": 1,
            "status": "boot_baseline_requires_exact_per_declaration_replay_before_acceptance",
            "lean_toolchain_sha256": sha256_file(ROOT / "Formalizations/Lean/lean-toolchain"),
            "provider_id": provider,
            "allowed_transitive_axiom_names": sorted(set(baseline_axioms)),
            "allowed_bodyless_foundation_declarations": [],
            "per_name_justifications": {
                name: "source provider batch union; final claim receipt must replace this upper bound with the exact observed per-declaration set"
                for name in sorted(set(baseline_axioms))
            },
        }
        profile = dict(profile_body)
        profile["profile_authority_sha256"] = sha256_bytes(canonical(profile_body))
        profiles.append(profile)
    ids = [member["stage_claim_id"] for member in members]
    workset = sealed({
        "schema_version": "awesome-theorems/stage5-theorem-workset/1.0",
        "program": PROGRAM,
        "release": "5.6",
        "target_count": 3500,
        "task_count": len(rows),
        "source_path": THEOREM_SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": THEOREM_SOURCE_SHA256,
        "source_authority_sha256": THEOREM_AUTHORITY_SHA256,
        "stage6_registry_path": STAGE6_REGISTRY.relative_to(ROOT).as_posix(),
        "stage6_registry_sha256": STAGE6_REGISTRY_SHA256,
        "stage6_registry_authority_sha256": STAGE6_REGISTRY_AUTHORITY_SHA256,
        "member_id_set_sha256": sha256_bytes(canonical(sorted(ids))),
        "member_record_set_sha256": sha256_bytes(canonical(sorted(
            [member["record_sha256"] for member in members]
        ))),
        "checklist_dag_sha256": sha256_bytes(canonical(dag_object(rows))),
        "members": members,
    })
    workset_raw = json.dumps(workset, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    provider_registry = sealed({
        "schema_version": "awesome-theorems/stage5-provider-registry/1.0",
        "program": PROGRAM,
        "providers": [
            {
                "provider_id": "mathlib-8a178386",
                "kind": "pinned_lean_provider",
                "revision": "8a178386ffc0f5fef0b77738bb5449d50efeea95",
                "source_registry_id": "SRC-MATH-V5-MATHLIB-8A178386",
                "trust": "Lean4 kernel replay at trust=0 plus exact declaration body/dependency/axiom audit",
            },
            {
                "provider_id": "formal-conjectures-2270d31e",
                "kind": "pinned_statement_provider_not_proof_authority",
                "revision": "2270d31e8dd611521f979de6d86da364930b7669",
                "source_registry_id": "SRC-MATH-V5-FORMAL-CONJECTURES-2270D31E",
                "trust": "exact statement/source bytes only; sorryAx and source claims provide no proof closure",
            },
        ],
    })
    provider_raw = json.dumps(provider_registry, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    foundation = sealed({
        "schema_version": "awesome-theorems/stage5-foundation-profile-registry/1.0",
        "program": PROGRAM,
        "profile_count": len(profiles),
        "provider_registry_sha256": sha256_bytes(provider_raw),
        "profiles": profiles,
    })
    foundation_raw = json.dumps(foundation, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    receipt = sealed({
        "schema_version": "awesome-theorems/stage5-theorem-workset-receipt/1.0",
        "program": PROGRAM,
        "workset_path": WORKSET.relative_to(ROOT).as_posix(),
        "workset_sha256": sha256_bytes(workset_raw),
        "target_count": 3500,
        "member_id_set_sha256": workset["member_id_set_sha256"],
        "member_record_set_sha256": workset["member_record_set_sha256"],
        "blueprint_sha256": sha256_bytes(blueprint_raw),
        "execution_spec_sha256": sha256_bytes(canonical(canonical_spec)),
        "manager_sha256": sha256_file(MANAGER),
        "source_bundle_sha256": canonical_spec["source_bundle"]["sha256"],
        "checklist_dag_sha256": workset["checklist_dag_sha256"],
    })
    atomic_write(WORKSET, workset_raw)
    atomic_json(WORKSET_RECEIPT, receipt)
    atomic_json(EXECUTION_SPEC, canonical_spec)
    atomic_write(PROVIDER_REGISTRY, provider_raw)
    atomic_write(FOUNDATION_PROFILES, foundation_raw)
    for filename in schema_contract.BOOT_SCHEMA_FILENAMES:
        atomic_write(EVIDENCE / filename, schema_contract.expected_boot_schema_bytes("theorem", filename))


def validate_boot_data(specification: dict[str, Any], rows: list[dict[str, Any]], blueprint_raw: bytes) -> dict[str, Any]:
    expected_files = (
        WORKSET, WORKSET_RECEIPT, EXECUTION_SPEC, FOUNDATION_PROFILES, PROVIDER_REGISTRY,
        EVIDENCE / "claim-card.schema.json", EVIDENCE / "worker-result.schema.json",
        EVIDENCE / "master-acceptance.schema.json",
    )
    missing = [path.relative_to(ROOT).as_posix() for path in expected_files if not path.is_file() or path.is_symlink()]
    if missing:
        raise CheckError(f"missing BOOT data files: {missing}")
    observed_spec = strict_json(EXECUTION_SPEC.read_bytes(), "execution-spec.json")
    if observed_spec != specification:
        raise CheckError("execution-spec.json differs from embedded specification")
    workset = verify_seal(strict_json(WORKSET.read_bytes(), "workset"), "workset")
    receipt = verify_seal(strict_json(WORKSET_RECEIPT.read_bytes(), "workset receipt"), "workset receipt")
    providers = verify_seal(strict_json(PROVIDER_REGISTRY.read_bytes(), "provider registry"), "provider registry")
    profiles = verify_seal(strict_json(FOUNDATION_PROFILES.read_bytes(), "foundation profiles"), "foundation profiles")
    members = workset.get("members")
    if not isinstance(members, list) or len(members) != 3500 or workset.get("target_count") != 3500:
        raise CheckError("workset target cardinality differs")
    ids = [member.get("stage_claim_id") for member in members if isinstance(member, dict)]
    if len(ids) != 3500 or len(set(ids)) != 3500:
        raise CheckError("workset member identity is incomplete or duplicated")
    if workset.get("member_id_set_sha256") != sha256_bytes(canonical(sorted(ids))):
        raise CheckError("workset member-set digest differs")
    if workset.get("checklist_dag_sha256") != sha256_bytes(canonical(dag_object(rows))):
        raise CheckError("workset checklist DAG digest differs")
    if receipt.get("workset_sha256") != sha256_file(WORKSET):
        raise CheckError("workset receipt digest differs")
    if receipt.get("execution_spec_sha256") != sha256_bytes(canonical(specification)):
        raise CheckError("workset receipt specification digest differs")
    if receipt.get("checklist_dag_sha256") != workset.get("checklist_dag_sha256"):
        raise CheckError("workset receipt DAG digest differs")
    if providers.get("program") != PROGRAM or len(providers.get("providers", [])) != 2:
        raise CheckError("provider registry differs")
    if profiles.get("profile_count") != 3500 or len(profiles.get("profiles", [])) != 3500:
        raise CheckError("foundation profile cardinality differs")
    if profiles.get("provider_registry_sha256") != sha256_file(PROVIDER_REGISTRY):
        raise CheckError("foundation/provider binding differs")
    schema_contract = load_module(SCHEMA_CONTRACT, "stage5_boot_schema_contract_for_theorem_check")
    for filename in schema_contract.BOOT_SCHEMA_FILENAMES:
        schema_contract.validate_boot_schema_bytes(
            (EVIDENCE / filename).read_bytes(), program_kind="theorem", schema_filename=filename,
        )
    return {
        "workset_sha256": sha256_file(WORKSET),
        "workset_authority_sha256": workset["authority_sha256"],
        "execution_spec_sha256": sha256_bytes(canonical(specification)),
        "checklist_dag_sha256": workset["checklist_dag_sha256"],
        "blueprint_sha256": sha256_bytes(blueprint_raw),
    }


def validate_migration_receipt(rows: list[dict[str, Any]], blueprint_raw: bytes) -> dict[str, Any]:
    if not MIGRATION_RECEIPT.is_file() or MIGRATION_RECEIPT.is_symlink():
        # The one-object receipt is immutable historical evidence.  A v2
        # program-isolation migration may preserve it in its superseded archive
        # while the active checker continues to bind the latest migration.
        archive = ROOT / "Docs/evidence/stage5_theorems/bootstrap/superseded-v1-boot-authorities/one-object-one-goal-v1-to-v2-migration.json"
        if archive.is_file() and not archive.is_symlink():
            migration_bytes = archive.read_bytes()
        else:
            raise CheckError("one-object v2 migration receipt is missing")
    else:
        migration_bytes = MIGRATION_RECEIPT.read_bytes()
    value = verify_seal(
        strict_json(migration_bytes, "one-object v2 migration receipt"),
        "one-object v2 migration receipt",
    )
    if value.get("schema_version") != "awesome-theorems/stage5-one-object-one-goal-migration/1.0":
        raise CheckError("one-object v2 migration schema differs")
    record = value.get("programs", {}).get("theorem")
    if not isinstance(record, dict):
        raise CheckError("theorem migration record is missing")
    lifecycle_receipts = sorted(ISOLATION_MIGRATION_DIR.glob("S5PD-BLUEPRINT-MIGRATE-*-lifecycle.json")) if ISOLATION_MIGRATION_DIR.is_dir() else []
    isolation_receipts = sorted(ISOLATION_MIGRATION_DIR.glob("S5PD-BLUEPRINT-MIGRATE-*-program-isolation.json")) if ISOLATION_MIGRATION_DIR.is_dir() else []
    latest_lifecycle_ordinal = int(re.search(r"MIGRATE-(\d+)-", lifecycle_receipts[-1].name).group(1)) if lifecycle_receipts else -1
    latest_isolation_ordinal = int(re.search(r"MIGRATE-(\d+)-", isolation_receipts[-1].name).group(1)) if isolation_receipts else -1
    if lifecycle_receipts and latest_lifecycle_ordinal > latest_isolation_ordinal:
        path = lifecycle_receipts[-1]
        lifecycle = verify_seal(
            strict_json(path.read_bytes(), "theorem lifecycle migration"),
            "theorem lifecycle migration",
        )
        if (
            lifecycle.get("schema_version")
            != "awesome-theorems/stage5-theorem-lifecycle-migration/1.0"
            or lifecycle.get("migration_id") != path.stem
            or lifecycle.get("program") != PROGRAM
            or lifecycle.get("row_count") != len(rows)
            or lifecycle.get("target_count") != 3500
        ):
            raise CheckError("theorem lifecycle migration identity differs")
        text = blueprint_raw.decode("utf-8")
        requirements = extract_once(
            text, REQUIREMENTS_BEGIN, REQUIREMENTS_END, "requirements"
        ).encode("utf-8")
        specification = parse_spec(text)
        if (
            lifecycle.get("new_requirements_sha256") != sha256_bytes(requirements)
            or lifecycle.get("execution_spec_sha256")
            != sha256_bytes(canonical(specification))
            or lifecycle.get("checklist_task_authority_sha256")
            != sha256_bytes(canonical(dag_object(rows)))
            or lifecycle.get("preserved")
            != [
                "mathematical TARGET IDs",
                "checklist states",
                "TARGET dependencies",
                "owned paths",
                "task gates",
                "embedded execution specification",
                "active generation claim baselines",
            ]
        ):
            raise CheckError("theorem lifecycle migration binding differs")
        required_lifecycle_clauses = (
            "terminal_pending_disposition",
            "machine_complete_reading_debt",
            "proof_search_checkpoint",
            "provider_retryable",
            "validation_repair_required",
            "proof_blocked_with_evidence",
            "boundary_invalid",
            "supplies no concurrency fallback",
        )
        if any(clause not in text for clause in required_lifecycle_clauses):
            raise CheckError("theorem lifecycle requirements are incomplete")
        return {
            "migration_receipt_sha256": sha256_file(path),
            "migration_authority_sha256": lifecycle["authority_sha256"],
            "legacy_v1_blueprint_sha256": LEGACY_V1_BLUEPRINT_SHA256,
            "legacy_v1_gantt_sha256": LEGACY_V1_GANTT_SHA256,
        }
    if isolation_receipts:
        value = verify_seal(strict_json(isolation_receipts[-1].read_bytes(), "program-isolation migration"), "program-isolation migration")
        record = value.get("programs", {}).get("theorem")
        if not isinstance(record, dict) or record.get("row_count") != len(rows) or record.get("target_count") != 3500:
            raise CheckError("program-isolation migration receipt does not bind current theorem Blueprint")
        current_sha = sha256_bytes(blueprint_raw)
        migration_sha = record.get("new_blueprint_sha256")
        if current_sha != migration_sha:
            # BOOT acceptance is the first legitimate post-migration cursor
            # transition.  Once it (or the ongoing controller) advances a
            # state, the immutable BOOT acceptance receipt becomes the
            # authority for the current bytes; the migration receipt remains
            # the predecessor binding and must not be mistaken for a stale
            # checklist failure.
            acceptance_path = EVIDENCE / "controller-bootstrap-acceptance.json"
            if acceptance_path.is_file() and not acceptance_path.is_symlink():
                acceptance = verify_seal(strict_json(acceptance_path.read_bytes(), "BOOT acceptance"), "BOOT acceptance")
                if (
                    acceptance.get("program") != PROGRAM
                    or acceptance.get("cron_activated") is not False
                    or rows[0]["item_id"] != "S5THM-BOOT-001"
                    or rows[0]["state"] != "x"
                ):
                    raise CheckError("post-migration theorem Blueprint is not bound by BOOT acceptance")
                # After BOOT, every subsequent checklist transition is a
                # canonical-Master CAS.  Bind the current cursor through the
                # immutable Master transition receipts rather than requiring
                # the one-time post-migration all-blank snapshot.
                current_sha = sha256_bytes(blueprint_raw)
                transitions = []
                handoff_root = EVIDENCE / "execution/handoffs"
                if handoff_root.is_dir():
                    for receipt_path in handoff_root.rglob("master-integration.json"):
                        try:
                            receipt = verify_seal(strict_json(receipt_path.read_bytes(), "Master integration"), "Master integration")
                        except CheckError:
                            continue
                        transition = receipt.get("state_transition", {})
                        if transition.get("post_blueprint_sha256") == current_sha:
                            transitions.append(receipt)
                if any(row["state"] == "x" for row in rows[1:]) and not transitions:
                    invalidation = validate_budget_overrun_invalidation(
                        rows, blueprint_raw,
                    )
                    if invalidation is None:
                        raise CheckError("post-migration theorem Blueprint lacks Master transition receipt")
                elif not any(row["state"] == "x" for row in rows[1:]) and not transitions:
                    semantic = validate_semantic_credit_invalidation(rows, blueprint_raw)
                    if semantic is None:
                        raise CheckError("blank mathematical cursor lacks semantic invalidation authority")
            else:
                # A reviewed pre-activation invalidation may intentionally
                # reopen the pristine blank cursor.  Its signed completion
                # receipt is the predecessor authority until the new BOOT
                # chain is accepted.
                archives = sorted(
                    (EVIDENCE / "bootstrap/superseded").glob("*/invalidation.json")
                )
                archives += sorted(
                    (EVIDENCE / "bootstrap/superseded").glob("*/refresh.json")
                )
                matched = False
                for archive in reversed(archives):
                    try:
                        invalidation = verify_seal(
                            strict_json(archive.read_bytes(), "BOOT invalidation completion"),
                            "BOOT invalidation completion",
                        )
                    except CheckError:
                        continue
                    if (
                        invalidation.get("program") == PROGRAM
                        and invalidation.get("post_blueprint_sha256") == current_sha
                        and invalidation.get("post_gantt_sha256") == sha256_file(GANTT)
                        and invalidation.get("mathematical_rows_advanced") == 0
                        and (
                            invalidation.get("activation_present") is False
                            or invalidation.get("cron_present") is False
                        )
                        and invalidation.get("runtime_present") is False
                    ):
                        matched = True
                        break
                if not matched:
                    raise CheckError("post-migration theorem Blueprint has no accepted transition receipt")
        elif any(row["state"] != " " for row in rows):
            # Reviewed v2->v3 migration preserves an existing cursor.  Bind
            # the exact state counts to the migration receipt instead of
            # incorrectly demanding a fresh pristine BOOT acceptance.
            expected_counts = record.get("new_state_counts")
            observed_counts = Counter(row["state"] for row in rows)
            if expected_counts != {
                "not_done": observed_counts.get(" ", 0),
                "handoff_waiting_master": observed_counts.get("_", 0),
                "master_accepted": observed_counts.get("x", 0),
            }:
                raise CheckError("migration-bound theorem checklist state counts differ")
        return {
            "migration_receipt_sha256": sha256_file(isolation_receipts[-1]),
            "migration_authority_sha256": value["authority_sha256"],
            "legacy_v1_blueprint_sha256": LEGACY_V1_BLUEPRINT_SHA256,
            "legacy_v1_gantt_sha256": LEGACY_V1_GANTT_SHA256,
        }
    expected = {
        "program": "stage5-theorem-proof-debt/1.0",
        "blueprint_sha256": LEGACY_V1_BLUEPRINT_SHA256,
        "gantt_sha256": LEGACY_V1_GANTT_SHA256,
        "checklist_item_count": 28075,
        "mathematical_phase_row_count": 28000,
        "v2_program": PROGRAM,
        "v2_blueprint_sha256": sha256_bytes(blueprint_raw),
        "v2_checklist_item_count": len(rows),
        "v2_target_count": 3500,
        "v2_initial_state_counts": {
            "not_done": len(rows),
            "handoff_waiting_master": 0,
            "master_accepted": 0,
        },
    }
    for key, wanted in expected.items():
        if record.get(key) != wanted:
            raise CheckError(f"theorem migration receipt {key} differs")
    if any(row["state"] != " " for row in rows):
        raise CheckError("migrated v2 theorem checklist must start wholly blank")
    for path in (
        ROOT / ".ops/stage5-theorems-execution-v2",
        ROOT / ".ops/stage5-proof-debt-shared-v2",
    ):
        if os.path.lexists(path):
            raise CheckError(f"migrated scaffold check refuses v2 runtime: {path.relative_to(ROOT)}")
    return {
        "migration_receipt_sha256": sha256_file(MIGRATION_RECEIPT),
        "migration_authority_sha256": value["authority_sha256"],
        "legacy_v1_blueprint_sha256": LEGACY_V1_BLUEPRINT_SHA256,
        "legacy_v1_gantt_sha256": LEGACY_V1_GANTT_SHA256,
    }


def validate_gantt(rows: list[dict[str, Any]], blueprint_raw: bytes) -> None:
    if not GANTT.is_file() or GANTT.is_symlink():
        raise CheckError("same-prefix Gantt is missing")
    text = GANTT.read_text(encoding="utf-8")
    metadata_block = extract_once(text, GANTT_META_BEGIN, GANTT_META_END, "Gantt metadata").strip()
    if not metadata_block.startswith("```json\n") or not metadata_block.endswith("\n```"):
        raise CheckError("Gantt metadata fence differs")
    metadata = strict_json(metadata_block[8:-4].encode(), "Gantt metadata")
    if metadata.get("blueprint_sha256") != sha256_bytes(blueprint_raw):
        raise CheckError("Gantt Blueprint digest is stale")
    if metadata.get("item_count") != len(rows):
        raise CheckError("Gantt item cardinality differs")
    index = extract_once(text, GANTT_INDEX_BEGIN, GANTT_INDEX_END, "Gantt index")
    indexed = re.findall(r'^\| "([A-Z0-9-]+)" \|', index, re.MULTILINE)
    if indexed != [row["item_id"] for row in rows]:
        raise CheckError("Gantt monitoring index coverage/order differs")
    if re.search(r"- \[[ _x]\]", index):
        raise CheckError("Gantt contains mutable checkboxes")


def check(*, require_boot_data: bool = True, require_gantt: bool = True) -> dict[str, Any]:
    specification, rows, blueprint_raw = parse_blueprint()
    validate_spec(specification)
    if require_boot_data:
        boot_evidence = validate_boot_data(specification, rows, blueprint_raw)
        migration_evidence = validate_migration_receipt(rows, blueprint_raw)
        evidence = {**boot_evidence, **migration_evidence}
    else:
        evidence = {}
    if require_gantt:
        validate_gantt(rows, blueprint_raw)
    counts = Counter(row["state"] for row in rows)
    return {
        "valid": True,
        "program": PROGRAM,
        "items": len(rows),
        "targets": 3500,
        "states": {"not_done": counts[" "], "handoff_waiting_master": counts["_"], "master_accepted": counts["x"]},
        "route": specification["route_policy"],
        "concurrency_prompt_contract": specification["concurrency_prompt_contract"],
        **evidence,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialize-boot-data", action="store_true")
    parser.add_argument("--no-gantt", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.materialize_boot_data:
            materialize_boot_data()
        result = check(require_boot_data=True, require_gantt=not arguments.no_gantt)
    except (CheckError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
