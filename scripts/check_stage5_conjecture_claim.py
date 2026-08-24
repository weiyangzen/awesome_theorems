#!/usr/bin/env python3
"""Validate Stage5 conjecture claim cards, worker results and Master receipts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_conjectures_blueprint.py"
EVIDENCE = ROOT / "Docs/evidence/stage5_conjectures"
RUNTIME = ROOT / ".ops/stage5-conjectures-execution-v2/epochs/stage5-conjecture-occurrence-pool-v2"
PROGRAM = "stage5-conjecture-proof-debt/2.0"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}$")


class ClaimError(RuntimeError):
    pass


def load_checker() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_conjecture_checker_for_claim", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise ClaimError("cannot load ongoing conjecture checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ClaimError("value is not canonical finite JSON") from exc


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def strict_document(path: Path, label: str) -> tuple[Any, bytes]:
    if path.is_symlink() or not path.is_file():
        raise ClaimError(f"{label}: missing regular file {path}")
    raw = path.read_bytes()
    checker = load_checker()
    return checker.strict_json(raw, label), raw


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    branches = schema.get("oneOf")
    if isinstance(branches, list):
        accepted = 0
        failures: list[str] = []
        for branch in branches:
            try:
                validate_schema(value, branch, path)
                accepted += 1
            except ClaimError as exc:
                failures.append(str(exc))
        if accepted != 1:
            raise ClaimError(f"{path}: expected exactly one closed work-contract branch; accepted={accepted}; failures={failures[:2]}")
        return
    kind = schema.get("type")
    if kind == "object":
        if not isinstance(value, dict):
            raise ClaimError(f"{path}: expected object")
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if schema.get("additionalProperties") is not False or set(value) - set(properties):
            raise ClaimError(f"{path}: object fields are open/unknown")
        missing = set(required) - set(value)
        if missing:
            raise ClaimError(f"{path}: missing fields {sorted(missing)}")
        for key in required:
            validate_schema(value[key], properties[key], f"{path}.{key}")
        return
    if kind == "array":
        if not isinstance(value, list):
            raise ClaimError(f"{path}: expected array")
        if len(value) < int(schema.get("minItems", 0)):
            raise ClaimError(f"{path}: too few entries")
        if schema.get("uniqueItems") and len({canonical(item) for item in value}) != len(value):
            raise ClaimError(f"{path}: duplicate entries")
        for index, item in enumerate(value):
            validate_schema(item, schema["items"], f"{path}[{index}]")
        return
    if kind == "string":
        if not isinstance(value, str):
            raise ClaimError(f"{path}: expected string")
        if len(value) < int(schema.get("minLength", 0)):
            raise ClaimError(f"{path}: string is too short")
        if "const" in schema and value != schema["const"]:
            raise ClaimError(f"{path}: constant differs")
        if "enum" in schema and value not in schema["enum"]:
            raise ClaimError(f"{path}: enum value differs")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            raise ClaimError(f"{path}: string pattern differs")
        return
    if kind == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ClaimError(f"{path}: expected integer")
        if value < int(schema.get("minimum", -(1 << 63))):
            raise ClaimError(f"{path}: integer below minimum")
        if "const" in schema and value != schema["const"]:
            raise ClaimError(f"{path}: integer constant differs")
        return
    if kind == "boolean":
        if not isinstance(value, bool):
            raise ClaimError(f"{path}: expected boolean")
        if "const" in schema and value is not schema["const"]:
            raise ClaimError(f"{path}: boolean constant differs")
        return
    raise ClaimError(f"{path}: unsupported schema type {kind!r}")


def load_schema(filename: str) -> dict[str, Any]:
    value, _ = strict_document(EVIDENCE / filename, filename)
    if not isinstance(value, dict):
        raise ClaimError(f"{filename}: schema is not an object")
    return value


def reviewed_schema(filename: str) -> dict[str, Any]:
    """Load the reviewed generated schema, independent of migration order."""
    contract_path = ROOT / "scripts/stage5_boot_schema_contract.py"
    contract_spec = importlib.util.spec_from_file_location(
        f"stage5_conjecture_reviewed_{filename.replace('.', '_')}",
        contract_path,
    )
    if contract_spec is None or contract_spec.loader is None:
        raise ClaimError("cannot load reviewed conjecture schema contract")
    contract = importlib.util.module_from_spec(contract_spec)
    sys.modules[contract_spec.name] = contract
    contract_spec.loader.exec_module(contract)
    try:
        value = contract.expected_boot_schema("conjecture", filename)
    except (KeyError, RuntimeError, ValueError) as exc:
        raise ClaimError("cannot reconstruct reviewed conjecture schema") from exc
    if not isinstance(value, dict):
        raise ClaimError("reviewed conjecture schema is not an object")
    return value


def reviewed_schema_bytes(filename: str) -> bytes:
    contract_path = ROOT / "scripts/stage5_boot_schema_contract.py"
    contract_spec = importlib.util.spec_from_file_location(
        f"stage5_conjecture_reviewed_bytes_{filename.replace('.', '_')}",
        contract_path,
    )
    if contract_spec is None or contract_spec.loader is None:
        raise ClaimError("cannot load reviewed conjecture schema contract")
    contract = importlib.util.module_from_spec(contract_spec)
    sys.modules[contract_spec.name] = contract
    contract_spec.loader.exec_module(contract)
    try:
        return contract.expected_boot_schema_bytes("conjecture", filename)
    except (KeyError, RuntimeError, ValueError) as exc:
        raise ClaimError("cannot reconstruct reviewed conjecture schema bytes") from exc


def strict_current_specification() -> dict[str, Any]:
    """Load the installed spec and require equality with generated authority."""
    installed, _ = strict_document(EVIDENCE / "execution-spec.json", "execution specification")
    if not isinstance(installed, dict):
        raise ClaimError("execution specification is not an object")
    checker = load_checker()
    checker.validate_spec(installed)
    manager = checker.manager()
    if installed != manager.spec_object(manager.CONJECTURE):
        raise ClaimError("current conjecture authority is not atomically installed")
    return installed


def canonical_relative(value: str, label: str) -> str:
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or value != path.as_posix()
        or "." in path.parts or ".." in path.parts
    ):
        raise ClaimError(f"{label}: unsafe relative path {value!r}")
    return value


def exact_descendant(path_value: str, root: Path, label: str) -> Path:
    path = Path(path_value)
    if not path.is_absolute() or ".." in path.parts:
        raise ClaimError(f"{label}: expected absolute path")
    if path_value != os.path.normpath(path_value):
        raise ClaimError(f"{label}: path is not canonical")
    if not root.is_absolute() or root.is_symlink():
        raise ClaimError(f"{label}: unsafe descendant root")
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ClaimError(f"{label}: escapes {root}") from exc
    current = path
    while current != root:
        if current.is_symlink():
            raise ClaimError(f"{label}: symlink path component is forbidden")
        current = current.parent
    return path


def mode_for(item_id: str) -> str:
    if item_id == "S5CON-BOOT-001":
        return "BOOT"
    if item_id == "S5CON-PROGRAM-RELEASE":
        return "PROGRAM-RELEASE"
    if re.fullmatch(r"S5CON-SHARD-[A-Z]+-[0-9]{3}", item_id):
        return "SHARD"
    if item_id == "S5CON-AGG-001":
        return "AGG"
    if item_id == "S5CON-QA-001":
        return "QA"
    if re.fullmatch(r"S5CON-POOL-[0-9]{8}-INTAKE", item_id):
        return "POOL-INTAKE"
    match = re.fullmatch(r"S5CON-[0-9]{8}-(.+)", item_id)
    if match:
        return "TARGET-" + match.group(1)
    raise ClaimError(f"unsupported item ID {item_id}")


def blueprint_context(path: Path | None = None) -> tuple[Any, dict[str, dict[str, Any]], bytes]:
    checker = load_checker()
    specification, rows, blueprint_raw = checker.parse_blueprint(
        checker.BLUEPRINT if path is None else path
    )
    checker.validate_spec(specification)
    return specification, {row["item_id"]: row for row in rows}, blueprint_raw


def validate_claim(path: Path) -> dict[str, Any]:
    value, raw = strict_document(path, "claim card")
    validate_schema(value, load_schema("claim-card.schema.json"))
    task_root = exact_descendant(value["task_root"], RUNTIME / "tasks", "task root")
    baseline_path = task_root / "work/_baseline/Stage5_Conjectures_Blueprint.md"
    specification, rows, blueprint_raw = blueprint_context(baseline_path)
    item_id = value["item_id"]
    row = rows.get(item_id)
    if row is None:
        raise ClaimError("claim item is not in the authoritative Blueprint")
    if value["program"] != PROGRAM or value["mode"] != mode_for(item_id):
        raise ClaimError("claim program/mode differs")
    execution_identity = value.get("execution_identity")
    if not isinstance(execution_identity, dict):
        raise ClaimError("claim execution identity is missing")
    if (
        execution_identity.get("generation_id") != value["run_id"]
        or execution_identity.get("execution_spec_sha256") != digest(canonical(specification))
        or execution_identity.get("requested_concurrency")
        != execution_identity.get("resolved_concurrency")
    ):
        raise ClaimError("claim execution identity/spec/vector binding differs")
    prompt_entries = [
        entry for entry in value["read_only_bootstrap_files"]
        if entry.get("path") == "_baseline/concurrency-prompt.json"
    ]
    if len(prompt_entries) != 1:
        raise ClaimError("claim lacks its immutable concurrency prompt")
    prompt_path = task_root / "work/_baseline/concurrency-prompt.json"
    prompt, prompt_raw = strict_document(prompt_path, "concurrency prompt")
    if (
        execution_identity.get("prompt_epoch") != prompt.get("policy_epoch")
        or execution_identity.get("prompt_digest") != digest(prompt_raw)
        or execution_identity.get("requested_concurrency") != prompt.get("concurrency")
    ):
        raise ClaimError("claim exact concurrency prompt binding differs")
    member_path = task_root / "work/_baseline/workset-member.json"
    member, _ = strict_document(member_path, "workset member")
    expected_member = value.get("workset_member")
    if (
        not isinstance(member, dict)
        or not isinstance(expected_member, dict)
        or member.get("target_item_id") != item_id
        or member.get("member_id") != expected_member.get("member_id")
        or member.get("member_kind") != expected_member.get("member_kind")
        or member.get("workset_record_sha256") != expected_member.get("workset_record_sha256")
        or member.get("record_sha256") != expected_member.get("source_record_sha256")
    ):
        raise ClaimError("claim exact workset member binding differs")
    if tuple(value["dependencies"]) != tuple(row["dependencies"]):
        raise ClaimError("claim dependency set/order differs")
    if value["canonical_repository_root"] != str(ROOT) or value["canonical_write_policy"] != "forbidden":
        raise ClaimError("canonical repository write boundary differs")
    if task_root != path.parent:
        raise ClaimError("claim card is outside its exact task root")
    expected_root = RUNTIME / "tasks" / value["claim_id"] / value["run_id"]
    if task_root != expected_root:
        raise ClaimError("task root identity differs")
    writable = [canonical_relative(item, "writable path") for item in value["writable_paths"]]
    if writable != list(row["owned_paths"]):
        raise ClaimError("producer writable paths differ from exact Blueprint ownership")
    if len(writable) != len(set(writable)):
        raise ClaimError("duplicate writable path")
    for field in ("allowed_paths", "required_paths"):
        if value["artifact_policy"][field] != writable:
            raise ClaimError(f"artifact policy {field} differs from ownership")
    forbidden = set(value["artifact_policy"]["forbidden_paths"])
    required_forbidden = {
        "Docs/Stage5_Conjectures_Blueprint.md", "Docs/Stage5_Conjectures_Gantt.md",
        "Docs/catalog", ".git", ".ops",
    }
    if not required_forbidden.issubset(forbidden):
        raise ClaimError("artifact policy lacks mandatory forbidden paths")
    baseline = value["baseline"]
    if baseline["execution_spec_sha256"] != digest(canonical(specification)):
        raise ClaimError("claim execution specification baseline differs")
    if baseline["blueprint_sha256"] != digest(blueprint_raw):
        raise ClaimError("claim Blueprint baseline differs")
    if baseline["source_bundle_sha256"] != specification["source_bundle"]["sha256"]:
        raise ClaimError("claim source bundle baseline differs")
    work_contract = value.get("work_contract")
    if not isinstance(work_contract, dict):
        raise ClaimError("claim work contract is missing")
    if mode_for(item_id) == "POOL-INTAKE":
        expected_work_contract = {
            "kind": "source_occurrence_intake",
            "source_occurrence_intake": specification.get("conjecture_occurrence_intake_contract"),
        }
        if work_contract != expected_work_contract:
            raise ClaimError("occurrence-intake claim contract differs from specification")
        intake = work_contract["source_occurrence_intake"]
        if "do not attempt a proof" not in intake.get("short_goal_clause", ""):
            raise ClaimError("occurrence-intake contract does not prohibit proof work")
        source_files = [
            entry for entry in value["read_only_bootstrap_files"]
            if entry.get("path") == "_baseline/source-record.json"
        ]
        if len(source_files) != 1:
            raise ClaimError("occurrence-intake claim lacks its exact source record")
        source_path = task_root / "work/_baseline/source-record.json"
        source_value, _ = strict_document(source_path, "occurrence source record")
        if digest(canonical(source_value)) != expected_member.get("source_record_sha256"):
            raise ClaimError("occurrence source record differs from workset binding")
        if expected_member.get("member_kind") != "source_occurrence_intake":
            raise ClaimError("occurrence-intake workset member kind differs")
    else:
        expected_work_contract = {
            "kind": "strict_resolution_proof_search",
            "strict_resolution_proof_search": specification.get("conjecture_proof_search_prompt"),
        }
        if work_contract != expected_work_contract:
            raise ClaimError("strict-resolution proof-search contract differs from specification")
        proof_search = work_contract["strict_resolution_proof_search"]
        source = proof_search.get("source", {})
        extraction = ROOT / str(source.get("extraction_path", ""))
        if (
            source.get("repository") != "jinshanmu/CrouzeixConjecture"
            or source.get("commit") != "f9d5c8d39bece41ceedf6346ef50ad1fb393260e"
            or source.get("file_sha256") != "0a0c3000b81efc4d9edc65ec3cd1d53df0d4e69b24bfee9fe0860301d853d6fc"
            or not extraction.is_file() or extraction.is_symlink()
            or file_digest(extraction) != source.get("extraction_sha256")
            or proof_search.get("resolution_roots") != ["Claim", "Not Claim"]
            or proof_search.get("execution_adaptation", {}).get("child_agents") != "forbidden"
        ):
            raise ClaimError("claim proof-search source or execution adaptation differs")
        if expected_member.get("member_kind") != "strict_resolution":
            raise ClaimError("strict-resolution workset member kind differs")
    result_schema = value["result_schema"]
    expected_result_path = "Docs/evidence/stage5_conjectures/worker-result.schema.json"
    if (
        result_schema["path"] != expected_result_path
        or result_schema["schema_id"] != load_schema("worker-result.schema.json")["$id"]
        or result_schema["sha256"] != file_digest(ROOT / expected_result_path)
    ):
        raise ClaimError("worker result schema binding differs")
    budget = value["resource_budget"]
    finite_budget = {key: amount for key, amount in budget.items() if key != "model_turns"}
    if budget.get("model_turns") != "unbounded" or any(
        not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0
        for amount in finite_budget.values()
    ):
        raise ClaimError("claim budget differs from finite caps plus explicit unbounded turns")
    maxima = specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
    if any(budget[key] > maxima[key] for key in finite_budget):
        raise ClaimError("claim budget exceeds operator maxima")
    retry = value["retry_budget"]
    if not 1 <= retry["attempt"] <= retry["max_attempts"] <= 3:
        raise ClaimError("retry budget differs")
    for entry in value["read_only_bootstrap_files"]:
        relative = canonical_relative(entry["path"], "read-only bootstrap path")
        source = task_root / "work" / relative
        if source.is_symlink() or not source.is_file():
            raise ClaimError(f"missing read-only bootstrap file {relative}")
        if source.stat().st_size != entry["size_bytes"] or file_digest(source) != entry["sha256"]:
            raise ClaimError(f"read-only bootstrap binding differs: {relative}")
    if digest(raw) != file_digest(path):
        raise ClaimError("claim card changed while reading")
    return value


def validate_result(path: Path, claim_path: Path) -> dict[str, Any]:
    claim = validate_claim(claim_path)
    value, raw = strict_document(path, "worker result")
    # The reviewed BOOT contract is the authority for this discriminator.  A
    # stale on-disk predecessor schema must not silently re-admit untyped
    # conjecture results while an atomic authority migration is in flight.
    try:
        schema_contract_path = ROOT / "scripts/stage5_boot_schema_contract.py"
        spec = importlib.util.spec_from_file_location(
            "stage5_conjecture_worker_result_contract", schema_contract_path
        )
        if spec is None or spec.loader is None:
            raise ClaimError("cannot load reviewed conjecture worker-result contract")
        contract = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = contract
        spec.loader.exec_module(contract)
        reviewed_schema = contract.expected_boot_schema(
            "conjecture", "worker-result.schema.json"
        )
    except (OSError, RuntimeError, ValueError) as exc:
        raise ClaimError("cannot validate reviewed conjecture worker-result contract") from exc
    validate_schema(value, reviewed_schema)
    for field in ("program", "claim_id", "run_id", "item_id", "mode"):
        if value[field] != claim[field]:
            raise ClaimError(f"worker result {field} differs from claim")
    if value["claim_card_sha256"] != file_digest(claim_path):
        raise ClaimError("worker result claim-card digest differs")
    expected_baseline = digest(canonical(claim["baseline"]))
    if value["baseline_sha256"] != expected_baseline:
        raise ClaimError("worker result baseline digest differs")
    changed = value["changed_paths"]
    if changed != claim["writable_paths"]:
        raise ClaimError("worker result changed paths differ from exact ownership")
    commands = claim["validation_commands"]
    outcomes = value["command_outcomes"]
    if len(outcomes) != len(commands):
        raise ClaimError("worker result validation outcome count differs")
    for command, outcome in zip(commands, outcomes):
        expected_argv_sha = digest(canonical(command["argv"]))
        if (
            outcome["command_id"] != command["command_id"]
            or outcome["argv_sha256"] != expected_argv_sha
            or outcome["exit_code"] != 0 or outcome["passed"] is not True
        ):
            raise ClaimError("worker result validation outcome binding differs")
    task_root = claim_path.parent
    patch_path = exact_descendant(value["patch"]["path"], task_root, "patch")
    if patch_path.is_symlink() or not patch_path.is_file():
        raise ClaimError("worker patch is missing")
    if patch_path.stat().st_size != value["patch"]["size_bytes"] or file_digest(patch_path) != value["patch"]["sha256"]:
        raise ClaimError("worker patch binding differs")
    artifacts_by_relative_path: dict[str, dict[str, Any]] = {}
    work_root = task_root / "work"
    for artifact in value["artifacts"]:
        artifact_path = exact_descendant(artifact["path"], work_root, "artifact")
        if artifact_path.is_symlink() or not artifact_path.is_file():
            raise ClaimError("worker artifact is missing")
        if artifact_path.stat().st_size != artifact["size_bytes"] or file_digest(artifact_path) != artifact["sha256"]:
            raise ClaimError("worker artifact binding differs")
        try:
            relative = artifact_path.relative_to(work_root).as_posix()
        except ValueError as exc:
            raise ClaimError("worker artifact is outside the task work root") from exc
        if relative in artifacts_by_relative_path:
            raise ClaimError("worker result has duplicate artifact paths")
        artifacts_by_relative_path[relative] = artifact
    if set(artifacts_by_relative_path) != set(claim["writable_paths"]):
        raise ClaimError("worker artifacts differ from exact ownership")

    work_contract = claim["work_contract"]
    typed_outcome = value.get("typed_outcome")
    if not isinstance(typed_outcome, dict):
        raise ClaimError("worker result typed outcome is missing")

    def require_owned_digest(relative: str, field: str) -> None:
        if relative not in claim["writable_paths"]:
            raise ClaimError(f"worker typed outcome {field} path is not owned")
        artifact = artifacts_by_relative_path.get(relative)
        if artifact is None or typed_outcome[field] != artifact["sha256"]:
            raise ClaimError(f"worker typed outcome {field} binding differs")

    contract_kind = work_contract["kind"]
    if contract_kind == "strict_resolution_proof_search":
        if typed_outcome["kind"] != "strict_resolution":
            raise ClaimError("strict-resolution claim requires a strict-resolution outcome")
        human_paths = [item for item in claim["writable_paths"] if item.endswith("/human-resolution.md")]
        lean_paths = [item for item in claim["writable_paths"] if item.endswith("/Proof.lean")]
        if len(human_paths) != 1 or len(lean_paths) != 1:
            raise ClaimError("strict-resolution ownership lacks exact human/Lean roots")
        require_owned_digest(human_paths[0], "human_resolution_sha256")
        require_owned_digest(lean_paths[0], "lean_root_sha256")
    elif contract_kind == "source_occurrence_intake":
        if typed_outcome["kind"] != "source_occurrence_intake":
            raise ClaimError("occurrence-intake claim requires an occurrence-intake outcome")
        for suffix, field in (
            ("/status-review.json", "status_review_sha256"),
            ("/rights-review.json", "rights_review_sha256"),
            ("/importance-review.json", "importance_review_sha256"),
            ("/identity-crosswalk.json", "identity_crosswalk_sha256"),
        ):
            matches = [item for item in claim["writable_paths"] if item.endswith(suffix)]
            if len(matches) != 1:
                raise ClaimError(f"occurrence-intake ownership lacks exact {field} artifact")
            require_owned_digest(matches[0], field)
        if any(typed_outcome[field] is not False for field in (
            "strict_credit_granted", "stage5_claim_id_allocated", "stage6_alias_allocated",
        )):
            raise ClaimError("occurrence intake must grant zero strict/S5/S6 credit")
    else:
        raise ClaimError(f"unsupported claim work contract {contract_kind!r}")
    unsigned = dict(value)
    authority = unsigned.pop("authority_sha256")
    if digest(canonical(unsigned)) != authority:
        raise ClaimError("worker result authority seal differs")
    if digest(raw) != file_digest(path):
        raise ClaimError("worker result changed while reading")
    return value


def _real_descendant_directory(path: Path, root: Path, label: str) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ClaimError(f"{label}: escapes {root}") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink() or not current.exists():
            raise ClaimError(f"{label}: unsafe path component {current}")
    if not path.is_dir():
        raise ClaimError(f"{label}: not a directory")


def _verified_authority_member(
    specification: dict[str, Any],
    rows: dict[str, dict[str, Any]],
    item_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Rebuild the immutable task/member authority without a task root.

    Checklist progress is deliberately excluded.  A Master may replay a
    harvest after ``[_]`` or ``[x]`` changed the canonical Blueprint, while
    the immutable row and generated workset member must still be byte-exact.
    """
    row = rows.get(item_id)
    if row is None:
        raise ClaimError("archived claim item is not in the authoritative Blueprint")
    checker = load_checker()
    manager = checker.manager()
    expected_tasks = manager.expected_tasks(manager.CONJECTURE)
    expected = next((task for task in expected_tasks if task.item_id == item_id), None)
    if expected is None:
        raise ClaimError("archived claim item is not in generated task authority")
    immutable_row = {
        "item_id": expected.item_id,
        "state": row["state"],
        "title": expected.title,
        "dependencies": list(expected.dependencies),
        "owned_paths": list(expected.owned_paths),
        "gate": expected.gate,
    }
    if any(
        row.get(field) != immutable_row[field]
        for field in ("item_id", "title", "dependencies", "owned_paths", "gate")
    ):
        raise ClaimError("archived claim immutable Blueprint row differs")
    installed_workset, _ = strict_document(
        EVIDENCE / "workset-5.6.json", "current conjecture workset"
    )
    checker.verify_seal(installed_workset, "current conjecture workset")
    members = installed_workset.get("members")
    matches = [
        member for member in members
        if isinstance(member, dict) and member.get("target_item_id") == item_id
    ] if isinstance(members, list) else []
    if len(matches) != 1:
        raise ClaimError("archived claim workset member authority is missing or ambiguous")
    observed_member = matches[0]
    task_authority = digest(canonical({
        "item_id": immutable_row["item_id"],
        "title": immutable_row["title"],
        "dependencies": immutable_row["dependencies"],
        "owned_paths": immutable_row["owned_paths"],
        "gate": immutable_row["gate"],
    }))
    if re.fullmatch(r"S5CON-[0-9]{8}-TARGET", item_id):
        stage_id = f"S5-CLM-{item_id[6:14]}"
        strict_matches = [
            entry for entry in manager.strict_inventory()
            if entry["record"].get("stage_claim_id") == stage_id
        ]
        if len(strict_matches) != 1:
            raise ClaimError("strict workset source authority is missing or ambiguous")
        entry = strict_matches[0]
        record = entry["record"]
        formal = (
            record.get("formal_statement")
            if isinstance(record.get("formal_statement"), dict) else {}
        )
        expected_member = {
            "member_id": stage_id, "member_kind": "strict_resolution",
            "stage_claim_id": stage_id, "pool_id": None,
            "variant_id": record.get("variant_id"),
            "family_id": record.get("family_id"),
            "stage6_alias": manager.stage6_aliases()[stage_id],
            "cohort": manager.conjecture_cohort(entry),
            "provider_id": "formal-conjectures-2270d31e",
            "record_sha256": digest(canonical(record)),
            "semantic_payload_sha256": record.get("semantic_payload_sha256"),
            "statement_sha256": record.get("statement_sha256"),
            "formal_type_sha256": record.get("formal_type_sha256"),
            "display_name": record.get("display_name"),
            "qualified_name": record.get("qualified_name"),
            "module": record.get("module"), "source_id": record.get("source_id"),
            "source_locator": record.get("locator") or formal.get("locator"),
            "formal_statement": formal, "target_item_id": item_id,
            "strict_credit": True, "independent_current_open_verified": None,
            "execution_admission": "strict_resolution",
            "target_task_authority_sha256": task_authority,
            "internal_subchecklist": [
                "INTAKE", "STATEMENT", "STATUS", "FRONTIER", "EXPLORE",
                "RESOLUTION", "HUMAN", "LEAN", "READABLE", "VALIDATE",
                "RELEASE",
            ],
            "worker_bijection": (
                "one conjecture, one TARGET, one task-local tmux, one private "
                "CODEX_HOME, one thread, one active /goal"
            ),
        }
    else:
        occurrence_index = int(item_id[11:19]) - 1
        occurrences = manager.conjecture_occurrence_inventory()
        if not 0 <= occurrence_index < len(occurrences):
            raise ClaimError("occurrence workset source authority is missing")
        occurrence = occurrences[occurrence_index]
        expected_pool_id = f"S5POOL-{occurrence_index + 1:08d}"
        if occurrence.get("pool_id") != expected_pool_id:
            raise ClaimError("occurrence workset source identity differs")
        expected_member = {
            "member_id": expected_pool_id,
            "member_kind": "source_occurrence_intake",
            "stage_claim_id": None, "pool_id": expected_pool_id,
            "stage6_alias": None,
            "stable_source_key": occurrence.get("stable_source_key"),
            "source_native_id": occurrence.get("source_native_id"),
            "source_kind": occurrence.get("kind"),
            "source_status": occurrence.get("source_status"),
            "statement_presence": occurrence.get("statement_presence"),
            "record_path": occurrence.get("record_path"),
            "record_sha256": occurrence.get("canonical_record_sha256"),
            "occurrence_authority_sha256": occurrence.get("authority_sha256"),
            "cohort": manager.conjecture_occurrence_cohort(occurrence),
            "provider_id": "conjecturebench-357bcb1a",
            "strict_credit": False,
            "independent_current_open_verified": False,
            "execution_admission": occurrence.get("execution_admission"),
            "target_item_id": item_id,
            "target_task_authority_sha256": task_authority,
            "internal_subchecklist": [
                "INTAKE", "STATEMENT-EXACTIFICATION", "STATUS", "RIGHTS",
                "IMPORTANCE", "FULL-CATALOG-IDENTITY", "ADJUDICATION",
            ],
            "worker_bijection": (
                "one source occurrence, one intake TARGET, one task-local tmux, "
                "one private CODEX_HOME, one thread, one active /goal"
            ),
        }
    expected_member["workset_record_sha256"] = digest(canonical({
        "member_kind": expected_member["member_kind"],
        "record_sha256": expected_member["record_sha256"],
        "target_item_id": item_id,
        "target_task_authority_sha256": task_authority,
    }))
    if observed_member != expected_member:
        raise ClaimError("current conjecture workset member differs from source authority")
    if (
        installed_workset.get("program") != PROGRAM
        or installed_workset.get("target_count") != manager.CONJECTURE_TOTAL_TARGET_COUNT
        or installed_workset.get("strict_resolution_target_count")
        != manager.CONJECTURE_STRICT_TARGET_COUNT
        or installed_workset.get("source_occurrence_intake_target_count")
        != manager.CONJECTURE_POOL_COUNT
        or installed_workset.get("strict_source_sha256")
        != manager.STRICT_SOURCE_SHA256
        or installed_workset.get("strict_source_authority_sha256")
        != manager.STRICT_AUTHORITY_SHA256
        or installed_workset.get("occurrence_source_sha256")
        != manager.CONJECTURE_POOL_OCCURRENCES_SHA256
        or installed_workset.get("occurrence_manifest_sha256")
        != manager.CONJECTURE_POOL_MANIFEST_SHA256
        or installed_workset.get("occurrence_identity_registry_sha256")
        != manager.CONJECTURE_POOL_IDENTITIES_SHA256
    ):
        raise ClaimError("current conjecture workset source binding differs")
    return immutable_row, expected_member


def _validate_archived_claim_authority(
    claim: dict[str, Any], expected_item_id: str,
) -> None:
    """Replay controller-generated immutable claim semantics offline."""
    specification = strict_current_specification()
    checker = load_checker()
    manager = checker.manager()
    rows = {
        task.item_id: {
            "item_id": task.item_id, "state": task.state,
            "title": task.title, "dependencies": list(task.dependencies),
            "owned_paths": list(task.owned_paths), "gate": task.gate,
        }
        for task in manager.expected_tasks(manager.CONJECTURE)
    }
    row, member = _verified_authority_member(
        specification, rows, expected_item_id
    )
    expected_member = {
        "member_id": member["member_id"],
        "member_kind": member["member_kind"],
        "target_item_id": member["target_item_id"],
        "workset_record_sha256": member["workset_record_sha256"],
        "source_record_sha256": member["record_sha256"],
    }
    owned = list(row["owned_paths"])
    expected_contract = (
        {
            "kind": "source_occurrence_intake",
            "source_occurrence_intake": specification[
                "conjecture_occurrence_intake_contract"
            ],
        }
        if member["member_kind"] == "source_occurrence_intake"
        else {
            "kind": "strict_resolution_proof_search",
            "strict_resolution_proof_search": specification[
                "conjecture_proof_search_prompt"
            ],
        }
    )
    expected_artifact_policy = {
        "allowed_paths": owned,
        "required_paths": owned,
        "forbidden_paths": [
            "Docs/Stage5_Conjectures_Blueprint.md",
            "Docs/Stage5_Conjectures_Gantt.md",
            "Docs/catalog", ".git", ".ops",
        ],
    }
    expected_commands = [{
        "command_id": "claim-self-check", "cwd": ".",
        "argv": ["/usr/bin/python3", "-I", "-B", "-c", "pass"],
        "environment": [], "timeout_seconds": 30, "network": "denied",
    }]
    finite_keys = (
        "model_input_tokens", "model_output_tokens", "external_launches",
        "wall_seconds", "cpu_seconds",
    )
    maxima = specification["operator_budget_policy"]["finite_initial_allowances"][
        "per_claim_maxima"
    ]
    expected_budget = {key: maxima[key] for key in finite_keys}
    expected_budget["model_turns"] = "unbounded"
    expected_schema_path = (
        "Docs/evidence/stage5_conjectures/worker-result.schema.json"
    )
    worker_schema = reviewed_schema("worker-result.schema.json")
    worker_schema_raw = reviewed_schema_bytes("worker-result.schema.json")
    expected_result_schema = {
        "path": expected_schema_path,
        "schema_id": worker_schema["$id"],
        "sha256": digest(worker_schema_raw),
    }
    execution_spec_sha = digest(canonical(specification))
    identity = claim.get("execution_identity")
    baseline = claim.get("baseline")
    task_root = Path(str(claim.get("task_root", "")))
    canonical_root = Path(specification["canonical_repository_root"])
    expected_task_root = (
        canonical_root / specification["runtime_root"] / "epochs"
        / specification["runtime_authority_epoch"] / "tasks"
        / claim["claim_id"] / claim["run_id"]
    )
    immutable_checks = {
        "program": claim.get("program") == PROGRAM,
        "item_id": claim.get("item_id") == expected_item_id,
        "mode": claim.get("mode") == mode_for(expected_item_id),
        "claim_id": claim.get("claim_id") == f"{expected_item_id}--worker",
        "dependencies": claim.get("dependencies") == list(row["dependencies"]),
        "writable_paths": claim.get("writable_paths") == owned,
        "artifact_policy": claim.get("artifact_policy") == expected_artifact_policy,
        "validation_commands": claim.get("validation_commands") == expected_commands,
        "workset_member": claim.get("workset_member") == expected_member,
        "work_contract": claim.get("work_contract") == expected_contract,
        "result_schema": claim.get("result_schema") == expected_result_schema,
        "resource_budget": claim.get("resource_budget") == expected_budget,
        "retry_budget": claim.get("retry_budget") == {"attempt": 1, "max_attempts": 3},
        "deadline": claim.get("deadline") == "2027-08-12T00:00:00Z",
        "deliverable": claim.get("deliverable") == f"{row['title']}. {row['gate']}",
        "canonical_repository_root": claim.get("canonical_repository_root") == str(canonical_root),
        "canonical_write_policy": claim.get("canonical_write_policy") == "forbidden",
        "task_root": task_root == expected_task_root,
        "execution_identity_object": isinstance(identity, dict),
        "identity_lane": isinstance(identity, dict) and identity.get("lane_id") == expected_item_id,
        "identity_generation": isinstance(identity, dict) and identity.get("generation_id") == claim.get("run_id"),
        "identity_spec": isinstance(identity, dict) and identity.get("execution_spec_sha256") == execution_spec_sha,
        "identity_vector": isinstance(identity, dict) and identity.get("requested_concurrency") == identity.get("resolved_concurrency"),
        "baseline_object": isinstance(baseline, dict),
        "baseline_spec": isinstance(baseline, dict) and baseline.get("execution_spec_sha256") == execution_spec_sha,
        "baseline_source": isinstance(baseline, dict) and baseline.get("source_bundle_sha256") == specification["source_bundle"]["sha256"],
        "baseline_dependencies": isinstance(baseline, dict) and baseline.get("dependency_state_sha256") == digest(canonical([[dependency, "master_accepted"] for dependency in row["dependencies"]])),
        "baseline_owned": isinstance(baseline, dict) and baseline.get("owned_paths_baseline_sha256") == digest(canonical([[path, None] for path in owned])),
    }
    failed = [name for name, passed in immutable_checks.items() if not passed]
    if failed:
        raise ClaimError(f"archived immutable claim authority differs: {failed}")
    if not isinstance(baseline.get("blueprint_sha256"), str) or not SHA_RE.fullmatch(
        baseline["blueprint_sha256"]
    ):
        raise ClaimError("archived Blueprint baseline digest is malformed")
    # The prompt may be superseded after harvest; its exact bytes are not in
    # the archive.  Still close the immutable identity over a complete vector
    # and a nonempty epoch/digest rather than trusting an arbitrary dict.
    prompt_contract = specification["concurrency_prompt_contract"]
    required_dimensions = set(prompt_contract["required_dimensions"])
    requested = identity["requested_concurrency"]
    if (
        not isinstance(requested, dict)
        or set(requested) != required_dimensions
        or not isinstance(identity.get("prompt_epoch"), str)
        or not ID_RE.fullmatch(identity["prompt_epoch"])
        or not isinstance(identity.get("prompt_digest"), str)
        or not SHA_RE.fullmatch(identity["prompt_digest"])
    ):
        raise ClaimError("archived concurrency-prompt identity differs")
    for key, value in requested.items():
        if value == "not_applicable":
            if key != "service_records":
                raise ClaimError("archived concurrency vector differs")
        elif (
            isinstance(value, bool) or not isinstance(value, int)
            or value < (0 if key == "exact_path_conflicts" else 1)
        ):
            raise ClaimError("archived concurrency vector differs")
    bootstrap = claim.get("read_only_bootstrap_files")
    if not isinstance(bootstrap, list):
        raise ClaimError("archived bootstrap manifest differs")
    bootstrap_by_path = {
        entry.get("path"): entry for entry in bootstrap if isinstance(entry, dict)
    }
    expected_bootstrap = {
        "_baseline/workset-member.json",
        "_baseline/Stage5_Conjectures_Blueprint.md",
        "_baseline/workset-5.6-receipt.json",
        "_baseline/execution-spec.json",
        "_baseline/foundation-profiles.json",
        "_baseline/provider-registry.json",
        "_baseline/claim-card.schema.json",
        "_baseline/worker-result.schema.json",
        "_baseline/master-acceptance.schema.json",
        "_baseline/concurrency-prompt.json",
        "_baseline/Current_Pool_Release.json",
        "_baseline/Pool_Manifest.json",
    }
    if member["member_kind"] == "source_occurrence_intake":
        expected_bootstrap.add("_baseline/source-record.json")
    if set(bootstrap_by_path) != expected_bootstrap or len(bootstrap) != len(
        expected_bootstrap
    ):
        raise ClaimError("archived exact bootstrap-file set differs")
    for path, entry in bootstrap_by_path.items():
        canonical_relative(path, "archived bootstrap path")
        if (
            not isinstance(entry.get("sha256"), str)
            or not SHA_RE.fullmatch(entry["sha256"])
            or isinstance(entry.get("size_bytes"), bool)
            or not isinstance(entry.get("size_bytes"), int)
            or entry["size_bytes"] < 0
        ):
            raise ClaimError("archived bootstrap-file binding differs")
    exact_member_raw = (
        json.dumps(member, ensure_ascii=False, sort_keys=True, indent=2).encode()
        + b"\n"
    )
    bootstrap_binding_checks = {
        "workset_member": bootstrap_by_path["_baseline/workset-member.json"] == {
            "path": "_baseline/workset-member.json",
            "sha256": digest(exact_member_raw),
            "size_bytes": len(exact_member_raw),
        },
        "worker_schema": bootstrap_by_path["_baseline/worker-result.schema.json"]["sha256"] == expected_result_schema["sha256"],
        "prompt": bootstrap_by_path["_baseline/concurrency-prompt.json"]["sha256"] == identity["prompt_digest"],
        "blueprint": bootstrap_by_path["_baseline/Stage5_Conjectures_Blueprint.md"]["sha256"] == baseline["blueprint_sha256"],
    }
    failed_bootstrap = [
        name for name, passed in bootstrap_binding_checks.items() if not passed
    ]
    if failed_bootstrap:
        raise ClaimError(
            f"archived bootstrap authority binding differs: {failed_bootstrap}"
        )
    if member["member_kind"] == "source_occurrence_intake":
        archive_path = (
            ROOT / "Docs/catalog/v5/sources/"
            "conjecturebench-357bcb1a-full-source.tar.gz"
        )
        if archive_path.is_symlink() or not archive_path.is_file():
            raise ClaimError("occurrence source archive is missing")
        top = "conjecture-bench-357bcb1a1daf93917d42e8206ceaa55645729a09"
        try:
            with tarfile.open(archive_path, "r:gz") as source_archive:
                info = source_archive.getmember(f"{top}/{member['record_path']}")
                if not info.isfile() or info.issym() or info.islnk():
                    raise ClaimError("occurrence source archive member is unsafe")
                stream = source_archive.extractfile(info)
                if stream is None:
                    raise ClaimError("occurrence source archive member is unreadable")
                source_value = load_checker().strict_json(
                    stream.read(), "occurrence source record"
                )
        except (KeyError, OSError, tarfile.TarError) as exc:
            raise ClaimError("occurrence source archive record differs") from exc
        occurrence = load_checker().manager().conjecture_occurrence_inventory()[
            int(expected_item_id[11:19]) - 1
        ]
        if occurrence.get("kind") == "family":
            index = occurrence.get("family_container_index")
            records = (
                source_value.get("records") if isinstance(source_value, dict)
                else None
            )
            if (
                isinstance(index, bool) or not isinstance(index, int)
                or not isinstance(records, list) or not 0 <= index < len(records)
            ):
                raise ClaimError("occurrence family source pointer differs")
            source_value = records[index]
        source_raw = canonical(source_value) + b"\n"
        source_entry = bootstrap_by_path["_baseline/source-record.json"]
        if (
            digest(canonical(source_value)) != expected_member["source_record_sha256"]
            or source_entry["sha256"] != digest(source_raw)
            or source_entry["size_bytes"] != len(source_raw)
        ):
            raise ClaimError("archived occurrence source-record binding differs")
    immutable_bootstrap_sources = {
        "_baseline/workset-5.6-receipt.json": EVIDENCE / "workset-5.6-receipt.json",
        "_baseline/execution-spec.json": EVIDENCE / "execution-spec.json",
        "_baseline/foundation-profiles.json": EVIDENCE / "foundation-profiles.json",
        "_baseline/provider-registry.json": EVIDENCE / "provider-registry.json",
        "_baseline/claim-card.schema.json": EVIDENCE / "claim-card.schema.json",
        "_baseline/worker-result.schema.json": EVIDENCE / "worker-result.schema.json",
        "_baseline/master-acceptance.schema.json": EVIDENCE / "master-acceptance.schema.json",
        "_baseline/Current_Pool_Release.json": (
            ROOT / "Docs/catalog/v5/pools/Current_Pool_Release.json"
        ),
        "_baseline/Pool_Manifest.json": (
            ROOT / "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json"
        ),
    }
    for relative, source in immutable_bootstrap_sources.items():
        if source.is_symlink() or not source.is_file():
            raise ClaimError(f"archived bootstrap authority is missing: {relative}")
        entry = bootstrap_by_path[relative]
        if (
            entry["sha256"] != file_digest(source)
            or entry["size_bytes"] != source.stat().st_size
        ):
            raise ClaimError(f"archived bootstrap authority differs: {relative}")
    prompt_path = EVIDENCE / "execution/concurrency-prompt.json"
    prompt, prompt_raw = strict_document(prompt_path, "current concurrency prompt")
    if not isinstance(prompt, dict):
        raise ClaimError("current concurrency prompt is not an object")
    prompt_body = dict(prompt)
    prompt_authority = prompt_body.pop("authority_sha256", None)
    manager = load_checker().manager()
    thread_id, objective_sha, _ = manager.operator_goal_binding(manager.CONJECTURE)
    if (
        not isinstance(prompt_authority, str)
        or digest(canonical(prompt_body)) != prompt_authority
        or prompt.get("schema_version")
        != specification["concurrency_prompt_contract"]["schema_version"]
        or prompt.get("program") != PROGRAM
        or prompt.get("execution_spec_sha256") != execution_spec_sha
        or prompt.get("operator_identity") != f"codex-user-goal:{thread_id}"
        or prompt.get("operator_goal_thread_id") != thread_id
        or prompt.get("operator_goal_objective_sha256") != objective_sha
        or prompt.get("request_window_seconds") != 120
        or prompt.get("source")
        != "explicit operator prompt fixture; not a controller or Blueprint default"
        or prompt.get("execution_limits")
        != specification["concurrency_prompt_contract"]["execution_limits"]
        or prompt.get("recovery")
        != specification["concurrency_prompt_contract"]["recovery"]
        or prompt.get("policy_epoch") != identity["prompt_epoch"]
        or prompt.get("concurrency") != requested
        or digest(prompt_raw) != identity["prompt_digest"]
        or bootstrap_by_path["_baseline/concurrency-prompt.json"] != {
            "path": "_baseline/concurrency-prompt.json",
            "sha256": digest(prompt_raw), "size_bytes": len(prompt_raw),
        }
    ):
        raise ClaimError("archived claim concurrency prompt differs from authority")


def _validate_archive_tree(
    archive: Path, expected_files: set[str],
) -> None:
    """Reject every archive byte outside the closed manifest file tree."""
    observed: set[str] = set()
    observed_directories: set[str] = set()
    for current_root, directory_names, file_names in os.walk(
        archive, topdown=True, followlinks=False
    ):
        current = Path(current_root)
        _real_descendant_directory(current, archive, "Master archive tree")
        for name in list(directory_names):
            child = current / name
            if child.is_symlink() or not child.is_dir():
                raise ClaimError("Master archive has a symlink/non-directory component")
            observed_directories.add(child.relative_to(archive).as_posix())
        for name in file_names:
            child = current / name
            if child.is_symlink() or not child.is_file():
                raise ClaimError("Master archive has a symlink/non-regular file")
            relative = child.relative_to(archive).as_posix()
            canonical_relative(relative, "Master archive file")
            if relative in observed:
                raise ClaimError("Master archive has duplicate file identity")
            observed.add(relative)
    if observed != expected_files:
        raise ClaimError("Master archive tree differs from exact file set")
    expected_directories = {
        parent.as_posix()
        for relative in expected_files
        for parent in PurePosixPath(relative).parents
        if parent != PurePosixPath(".")
    }
    if observed_directories != expected_directories:
        raise ClaimError("Master archive directory tree differs from exact file set")


def validate_archived_claim_result(
    archive: Path,
    expected_item_id: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], bytes]:
    """Validate one harvest using only immutable archive bytes.

    This deliberately does not depend on the worker task root: accepted
    evidence remains replayable after task-local lifecycle cleanup.
    """
    claim_path = archive / "claim.json"
    result_path = archive / "result.json"
    patch_path = archive / "changes.patch"
    manifest_path = archive / "harvest-manifest.json"
    claim, claim_raw = strict_document(claim_path, "archived claim card")
    result, result_raw = strict_document(result_path, "archived worker result")
    manifest, manifest_raw = strict_document(manifest_path, "archived harvest manifest")
    validate_schema(claim, reviewed_schema("claim-card.schema.json"))
    try:
        contract_path = ROOT / "scripts/stage5_boot_schema_contract.py"
        contract_spec = importlib.util.spec_from_file_location(
            "stage5_archived_conjecture_worker_contract", contract_path
        )
        if contract_spec is None or contract_spec.loader is None:
            raise ClaimError("cannot load archived worker contract")
        contract = importlib.util.module_from_spec(contract_spec)
        sys.modules[contract_spec.name] = contract
        contract_spec.loader.exec_module(contract)
        validate_schema(
            result,
            contract.expected_boot_schema("conjecture", "worker-result.schema.json"),
        )
    except (OSError, RuntimeError, ValueError) as exc:
        raise ClaimError("cannot validate archived worker-result contract") from exc
    manifest_body = dict(manifest) if isinstance(manifest, dict) else {}
    manifest_authority = manifest_body.pop("authority_sha256", None)
    result_body = dict(result) if isinstance(result, dict) else {}
    result_authority = result_body.pop("authority_sha256", None)
    patch_raw = patch_path.read_bytes() if patch_path.is_file() and not patch_path.is_symlink() else None
    if (
        not isinstance(manifest_authority, str)
        or digest(canonical(manifest_body)) != manifest_authority
        or manifest.get("schema_version") != "awesome-theorems/stage5-harvest-manifest/1.1"
        or not isinstance(result_authority, str)
        or digest(canonical(result_body)) != result_authority
        or patch_raw is None
    ):
        raise ClaimError("archived result/manifest authority differs")
    for field in ("program", "claim_id", "run_id", "item_id", "mode"):
        if result.get(field) != claim.get(field):
            raise ClaimError(f"archived result {field} differs from claim")
    if (
        claim.get("program") != PROGRAM
        or claim.get("item_id") != expected_item_id
        or result.get("status") != "self_tested"
        or result.get("claim_card_sha256") != digest(claim_raw)
        or result.get("baseline_sha256") != digest(canonical(claim.get("baseline")))
        or result.get("changed_paths") != claim.get("writable_paths")
        or result.get("patch", {}).get("sha256") != digest(patch_raw)
        or result.get("patch", {}).get("size_bytes") != len(patch_raw)
    ):
        raise ClaimError("archived claim/result/patch binding differs")
    commands = claim.get("validation_commands", [])
    outcomes = result.get("command_outcomes", [])
    if len(commands) != len(outcomes):
        raise ClaimError("archived command outcome count differs")
    for command, outcome in zip(commands, outcomes):
        if (
            outcome.get("command_id") != command.get("command_id")
            or outcome.get("argv_sha256") != digest(canonical(command.get("argv")))
            or outcome.get("exit_code") != 0
            or outcome.get("passed") is not True
        ):
            raise ClaimError("archived command outcome binding differs")
    if (
        manifest.get("program") != PROGRAM
        or manifest.get("item_id") != expected_item_id
        or manifest.get("claim_id") != claim.get("claim_id")
        or manifest.get("run_id") != claim.get("run_id")
        or manifest.get("baseline_sha256") != result.get("baseline_sha256")
        or manifest.get("patch_sha256") != result.get("patch", {}).get("sha256")
        or manifest.get("changed_paths") != claim.get("writable_paths")
        or manifest.get("archive") != archive.relative_to(ROOT).as_posix()
    ):
        raise ClaimError("archived harvest identity/path binding differs")
    expected_archive = (
        EVIDENCE / "execution/handoffs" / claim["claim_id"]
        / result["baseline_sha256"] / result["patch"]["sha256"]
    )
    if archive != expected_archive:
        raise ClaimError("archived harvest path grammar differs")
    _real_descendant_directory(archive, EVIDENCE / "execution/handoffs", "Master archive")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or [row.get("path") for row in artifacts] != claim.get("writable_paths"):
        raise ClaimError("archived artifact ownership/order differs")
    result_by_relative: dict[str, dict[str, Any]] = {}
    task_work = Path(claim["task_root"]) / "work"
    for artifact in result.get("artifacts", []):
        try:
            relative = Path(artifact["path"]).relative_to(task_work).as_posix()
        except (KeyError, TypeError, ValueError) as exc:
            raise ClaimError("archived result artifact path differs") from exc
        if relative in result_by_relative:
            raise ClaimError("archived result has duplicate artifact path")
        result_by_relative[relative] = artifact
    if set(result_by_relative) != set(claim["writable_paths"]):
        raise ClaimError("archived result artifact set differs")
    integrated: list[dict[str, Any]] = []
    file_set: list[list[Any]] = []
    for row in artifacts:
        if not isinstance(row, dict) or set(row) != {
            "path", "source_path", "archive_path", "sha256", "size_bytes", "media_type",
        }:
            raise ClaimError("archived artifact manifest fields differ")
        relative = canonical_relative(row["path"], "archived artifact path")
        expected_archive_path = f"artifacts/{relative}"
        if row["archive_path"] != expected_archive_path:
            raise ClaimError("archived artifact content path differs")
        artifact_path = archive / expected_archive_path
        if artifact_path.is_symlink() or not artifact_path.is_file():
            raise ClaimError("archived owned artifact is missing")
        raw = artifact_path.read_bytes()
        source = result_by_relative.get(relative)
        if (
            digest(raw) != row["sha256"]
            or len(raw) != row["size_bytes"]
            or source is None
            or source.get("sha256") != row["sha256"]
            or source.get("size_bytes") != row["size_bytes"]
            or source.get("media_type") != row["media_type"]
            or source.get("path") != row["source_path"]
        ):
            raise ClaimError("archived owned artifact binding differs")
        integrated.append({
            "path": relative, "sha256": row["sha256"],
            "size_bytes": row["size_bytes"],
        })
        file_set.append([expected_archive_path, row["sha256"], row["size_bytes"]])
    expected_file_set = sorted([
        ["claim.json", digest(claim_raw), len(claim_raw)],
        ["result.json", digest(result_raw), len(result_raw)],
        ["changes.patch", digest(patch_raw), len(patch_raw)],
        *file_set,
    ])
    if (
        manifest.get("file_set") != expected_file_set
        or manifest.get("file_set_sha256") != digest(canonical(expected_file_set))
    ):
        raise ClaimError("archived exact file-set authority differs")
    _validate_archive_tree(
        archive,
        {
            "claim.json", "result.json", "changes.patch",
            "harvest-manifest.json",
            *(row[0] for row in expected_file_set if row[0].startswith("artifacts/")),
        },
    )
    # Do not spend authority-reconstruction work until the physical archive is
    # proved closed.  Extras and symlink components fail on their own boundary
    # even during a concurrent, fail-closed authority migration window.
    _validate_archived_claim_authority(claim, expected_item_id)
    typed = result.get("typed_outcome")
    contract_kind = claim.get("work_contract", {}).get("kind")
    member_kind = claim.get("workset_member", {}).get("member_kind")
    expected_pair = {
        "strict_resolution_proof_search": ("strict_resolution", "strict_resolution"),
        "source_occurrence_intake": ("source_occurrence_intake", "source_occurrence_intake"),
    }.get(contract_kind)
    if expected_pair is None or (member_kind, typed.get("kind") if isinstance(typed, dict) else None) != expected_pair:
        raise ClaimError("archived member/work-contract/outcome discriminator differs")
    integrated_by_path = {row["path"]: row for row in integrated}
    def typed_digest(suffix: str, field: str) -> None:
        matches = [row for name, row in integrated_by_path.items() if name.endswith(suffix)]
        if len(matches) != 1 or typed.get(field) != matches[0]["sha256"]:
            raise ClaimError(f"archived typed outcome {field} differs")
    if typed["kind"] == "strict_resolution":
        typed_digest("/human-resolution.md", "human_resolution_sha256")
        typed_digest("/Proof.lean", "lean_root_sha256")
        if typed.get("machine_cut_set_empty") is not True or typed.get("readability_cut_set_empty") is not True:
            raise ClaimError("archived strict cut-set outcome differs")
    else:
        for suffix, field in (
            ("/status-review.json", "status_review_sha256"),
            ("/rights-review.json", "rights_review_sha256"),
            ("/importance-review.json", "importance_review_sha256"),
            ("/identity-crosswalk.json", "identity_crosswalk_sha256"),
        ):
            typed_digest(suffix, field)
        if any(typed.get(field) is not False for field in (
            "strict_credit_granted", "stage5_claim_id_allocated", "stage6_alias_allocated",
        )):
            raise ClaimError("archived intake grants forbidden credit/allocation")
    return claim, result, manifest, integrated, manifest_raw


def validate_acceptance(path: Path) -> dict[str, Any]:
    value, raw = strict_document(path, "Master acceptance")
    contract_path = ROOT / "scripts/stage5_boot_schema_contract.py"
    contract_spec = importlib.util.spec_from_file_location(
        "stage5_conjecture_master_acceptance_contract", contract_path
    )
    if contract_spec is None or contract_spec.loader is None:
        raise ClaimError("cannot load reviewed Master acceptance contract")
    contract = importlib.util.module_from_spec(contract_spec)
    sys.modules[contract_spec.name] = contract
    contract_spec.loader.exec_module(contract)
    validate_schema(
        value,
        contract.expected_boot_schema("conjecture", "master-acceptance.schema.json"),
    )
    if value["program"] != PROGRAM or value["state_transition"]["from"] != "handoff_waiting_master" or value["state_transition"]["to"] != "master_accepted":
        raise ClaimError("Master acceptance program/transition differs")
    unsigned = dict(value)
    authority = unsigned.pop("authority_sha256")
    if digest(canonical(unsigned)) != authority:
        raise ClaimError("Master acceptance authority seal differs")
    if not value["review_decisions"] or not value["validation_gates"]:
        raise ClaimError("Master acceptance lacks review or validation evidence")
    item_id = value["item_id"]
    specification, rows, blueprint_raw = blueprint_context()
    row = rows.get(item_id)
    if row is None or value["mode"] != mode_for(item_id) or row["state"] != "x":
        raise ClaimError("Master acceptance item/mode/current cursor differs")
    checker_manager = load_checker().manager()
    goal_thread_id, goal_objective_sha256, _ = checker_manager.operator_goal_binding(
        checker_manager.CONJECTURE
    )
    expected_master = {
        "principal_id": f"codex-user-goal:{goal_thread_id}",
        "decision_id": value["master"]["decision_id"],
        "authentication_sha256": digest(canonical({
            "thread_id": goal_thread_id,
            "objective_sha256": goal_objective_sha256,
        })),
    }
    if value["master"] != expected_master:
        raise ClaimError("Master authentication differs from pinned operator authority")
    handoff = value["handoff"]
    archive_relative = canonical_relative(
        handoff["immutable_archive_path"], "Master immutable archive"
    )
    archive = ROOT / archive_relative
    archive_root = EVIDENCE / "execution/handoffs"
    try:
        archive.relative_to(archive_root)
    except ValueError as exc:
        raise ClaimError("Master immutable archive is outside conjecture handoffs") from exc
    claim, result, manifest, expected_integrated, manifest_raw = validate_archived_claim_result(
        archive, item_id
    )
    claim_path = archive / "claim.json"
    result_path = archive / "result.json"
    patch_path = archive / "changes.patch"
    if (
        file_digest(claim_path) != handoff["claim_card_sha256"]
        or file_digest(result_path) != handoff["worker_result_sha256"]
        or digest(manifest_raw) != handoff["immutable_archive_sha256"]
        or file_digest(patch_path) != handoff["patch_sha256"]
        or result.get("claim_card_sha256") != handoff["claim_card_sha256"]
        or result.get("baseline_sha256") != handoff["baseline_sha256"]
        or (result.get("patch") or {}).get("sha256") != handoff["patch_sha256"]
        or claim.get("item_id") != item_id
        or claim.get("claim_id") != handoff["claim_id"]
        or claim.get("run_id") != handoff["run_id"]
        or result.get("item_id") != item_id
        or result.get("claim_id") != handoff["claim_id"]
        or result.get("run_id") != handoff["run_id"]
    ):
        raise ClaimError("Master archived claim/result/patch binding differs")
    workset = strict_document(EVIDENCE / "workset-5.6.json", "conjecture workset")[0]
    members = [
        member for member in workset.get("members", [])
        if isinstance(member, dict) and member.get("target_item_id") == item_id
    ] if isinstance(workset, dict) else []
    expected_member = value["workset_member"]
    if len(members) != 1:
        raise ClaimError("Master acceptance lacks one canonical workset member")
    member = members[0]
    member_projection = {
        "member_id": member.get("member_id"),
        "member_kind": member.get("member_kind"),
        "target_item_id": member.get("target_item_id"),
        "workset_record_sha256": member.get("workset_record_sha256"),
        "source_record_sha256": member.get("record_sha256"),
    }
    if expected_member != member_projection or claim.get("workset_member") != member_projection:
        raise ClaimError("Master exact workset member binding differs")
    accepted_outcome = value["accepted_outcome"]
    if result.get("typed_outcome") != accepted_outcome:
        raise ClaimError("Master accepted outcome differs from archived worker result")
    contract_kind = (claim.get("work_contract") or {}).get("kind")
    expected_typed_kind = (
        "source_occurrence_intake"
        if contract_kind == "source_occurrence_intake"
        else "strict_resolution"
        if contract_kind == "strict_resolution_proof_search"
        else None
    )
    if accepted_outcome.get("kind") != expected_typed_kind:
        raise ClaimError("Master outcome/work-contract discriminator differs")
    if expected_typed_kind == "source_occurrence_intake" and any(
        accepted_outcome.get(field) is not False
        for field in (
            "strict_credit_granted", "stage5_claim_id_allocated",
            "stage6_alias_allocated",
        )
    ):
        raise ClaimError("Master occurrence intake grants forbidden credit/allocation")
    integrated = value["integration"]["integrated_files"]
    if (
        integrated != expected_integrated
        or value["integration"]["integrated_bytes_sha256"]
        != digest(canonical(integrated))
        or value["integration"]["pre_tree_sha256"]
        != claim["baseline"]["owned_paths_baseline_sha256"]
        or value["integration"]["post_tree_sha256"]
        != digest(canonical([[row["path"], row["sha256"]] for row in integrated]))
    ):
        raise ClaimError("Master integrated artifact set differs from archived result")
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
            "accepted_outcome_sha256": digest(canonical(accepted_outcome)),
        })),
        "stderr_sha256": digest(b""),
    }
    if value["validation_gates"] != [expected_gate]:
        raise ClaimError("Master validation-gate replay binding differs")
    for artifact in integrated:
        relative = canonical_relative(artifact["path"], "integrated artifact")
        target = ROOT / relative
        if (
            target.is_symlink() or not target.is_file()
            or target.stat().st_size != artifact["size_bytes"]
            or file_digest(target) != artifact["sha256"]
        ):
            raise ClaimError(f"Master canonical integrated artifact differs: {relative}")
    transition = value["state_transition"]
    pre_marker = f"- [_] `{item_id}`".encode()
    post_marker = f"- [x] `{item_id}`".encode()
    if blueprint_raw.count(post_marker) != 1:
        raise ClaimError("Master current Blueprint lacks exact accepted cursor")
    pre_blueprint = blueprint_raw.replace(post_marker, pre_marker, 1)
    checker = load_checker()
    with __import__("tempfile").NamedTemporaryFile(suffix=".md", delete=False) as stream:
        stream.write(pre_blueprint)
        pre_path = Path(stream.name)
    try:
        checker.parse_blueprint(pre_path)
    finally:
        pre_path.unlink(missing_ok=True)
    if (
        transition["pre_blueprint_sha256"] != digest(pre_blueprint)
        or transition["post_blueprint_sha256"] != digest(blueprint_raw)
        or transition["post_gantt_sha256"] != file_digest(checker.GANTT)
    ):
        raise ClaimError("Master Blueprint/Gantt transition binding differs")
    expected_acceptance = (
        EVIDENCE / "execution/acceptances" / item_id / handoff["baseline_sha256"]
        / value["integration"]["post_tree_sha256"] / f"{value['authority_sha256']}.json"
    )
    if path != expected_acceptance:
        raise ClaimError("Master acceptance content-addressed path differs")
    for decision in value["review_decisions"]:
        decision_path = ROOT / canonical_relative(
            decision["decision_receipt_path"], "Master review decision"
        )
        if decision_path.is_symlink() or not decision_path.is_file() or file_digest(decision_path) != decision["decision_receipt_sha256"]:
            raise ClaimError("Master review decision receipt binding differs")
        decision_value, _ = strict_document(decision_path, "Master review decision")
        decision_body = dict(decision_value) if isinstance(decision_value, dict) else {}
        decision_authority = decision_body.pop("authority_sha256", None)
        decision_handoff = decision_value.get("handoff", {}) if isinstance(decision_value, dict) else {}
        if (
            not isinstance(decision_authority, str)
            or digest(canonical(decision_body)) != decision_authority
            or decision_value.get("program") != PROGRAM
            or decision_value.get("item_id") != item_id
            or decision_value.get("runtime_authority_epoch")
            != "stage5-conjecture-occurrence-pool-v2"
            or decision_value.get("state_transition", {}).get("to")
            != "handoff_waiting_master"
            or decision_handoff.get("claim_id") != handoff["claim_id"]
            or decision_handoff.get("run_id") != handoff["run_id"]
            or decision_handoff.get("immutable_archive") != archive_relative
        ):
            raise ClaimError("Master review decision semantic binding differs")
    if digest(raw) != file_digest(path):
        raise ClaimError("Master acceptance changed while reading")
    return value


def self_check() -> dict[str, Any]:
    specification, rows, _ = blueprint_context()
    for filename in (
        "claim-card.schema.json", "worker-result.schema.json", "master-acceptance.schema.json",
    ):
        schema = load_schema(filename)
        if schema.get("additionalProperties") is not False:
            raise ClaimError(f"{filename}: root is not closed")
    return {
        "valid": True, "program": PROGRAM, "items": len(rows),
        "route": specification["route_policy"],
        "schemas": {filename: file_digest(EVIDENCE / filename) for filename in (
            "claim-card.schema.json", "worker-result.schema.json", "master-acceptance.schema.json",
        )},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--claim-for-result", type=Path)
    parser.add_argument("--acceptance", type=Path)
    arguments = parser.parse_args(argv)
    try:
        chosen = sum(value is not None for value in (arguments.claim, arguments.result, arguments.acceptance))
        if chosen > 1:
            raise ClaimError("select at most one validation target")
        if arguments.result is not None:
            if arguments.claim_for_result is None:
                raise ClaimError("--result requires --claim-for-result")
            result = validate_result(arguments.result.resolve(), arguments.claim_for_result.resolve())
        elif arguments.claim is not None:
            result = validate_claim(arguments.claim.resolve())
        elif arguments.acceptance is not None:
            result = validate_acceptance(arguments.acceptance.resolve())
        else:
            result = self_check()
    except (ClaimError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
