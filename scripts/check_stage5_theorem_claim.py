#!/usr/bin/env python3
"""Validate Stage5 theorem claim cards, worker results and Master receipts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_theorems_blueprint.py"
EVIDENCE = ROOT / "Docs/evidence/stage5_theorems"
RUNTIME = ROOT / ".ops/stage5-theorems-execution-v2"
PROGRAM = "stage5-theorem-proof-debt/2.0"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}$")
CONCURRENCY_DIMENSIONS = (
    "logical_claims", "service_records", "agent_executions",
    "startup_reservations", "launch_fanout_per_wave", "live_transports",
    "authenticated_goals", "running_turns",
    "outbound_request_starts_per_window", "in_flight_requests",
    "integration", "validators", "exact_path_conflicts",
)
CONCURRENCY_POSITIVE = frozenset(CONCURRENCY_DIMENSIONS) - {
    "service_records", "exact_path_conflicts",
}


class ClaimError(RuntimeError):
    pass


def load_checker() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_theorem_checker_for_claim", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise ClaimError("cannot load ongoing theorem checker")
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


def validate_concurrency_vector(value: Any, label: str) -> dict[str, int | str]:
    if not isinstance(value, dict) or tuple(value) != CONCURRENCY_DIMENSIONS:
        # Canonical prompt/schema order is itself a small audit surface.
        if not isinstance(value, dict) or set(value) != set(CONCURRENCY_DIMENSIONS):
            raise ClaimError(f"{label}: incomplete or unknown concurrency dimensions")
    for key in CONCURRENCY_DIMENSIONS:
        amount = value[key]
        if key == "service_records":
            if amount != "not_applicable":
                raise ClaimError(f"{label}: service_records must be not_applicable")
        elif not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
            raise ClaimError(f"{label}: {key} is not a non-negative integer")
        elif key in CONCURRENCY_POSITIVE and amount == 0:
            raise ClaimError(f"{label}: {key} must be positive")
    fanout = value["launch_fanout_per_wave"]
    for key in (
        "agent_executions", "startup_reservations", "live_transports",
        "authenticated_goals", "running_turns",
        "outbound_request_starts_per_window", "in_flight_requests",
    ):
        if fanout > value[key]:
            raise ClaimError(f"{label}: launch fanout exceeds {key}")
    return dict(value)


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
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
    if isinstance(kind, list):
        if value is not None and not (kind == ["string", "null"] and isinstance(value, str)):
            raise ClaimError(f"{path}: union value differs")
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
    if kind == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ClaimError(f"{path}: expected number")
        if value < float(schema.get("minimum", float("-inf"))) or value > float(schema.get("maximum", float("inf"))):
            raise ClaimError(f"{path}: number outside bounds")
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
    if not path.is_absolute():
        raise ClaimError(f"{label}: expected absolute path")
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ClaimError(f"{label}: escapes {root}") from exc
    return path


def mode_for(item_id: str) -> str:
    if item_id == "S5THM-BOOT-001":
        return "BOOT"
    if item_id == "S5THM-PROGRAM-RELEASE":
        return "PROGRAM-RELEASE"
    if re.fullmatch(r"S5THM-SHARD-[A-Z]+-[0-9]{3}", item_id):
        return "SHARD"
    if item_id == "S5THM-AGG-001":
        return "AGG"
    if item_id == "S5THM-QA-001":
        return "QA"
    match = re.fullmatch(r"S5THM-[0-9]{8}-(.+)", item_id)
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
    baseline_path = task_root / "work/_baseline/Stage5_Theorems_Blueprint.md"
    specification, rows, blueprint_raw = blueprint_context(baseline_path)
    item_id = value["item_id"]
    row = rows.get(item_id)
    if row is None:
        raise ClaimError("claim item is not in the authoritative Blueprint")
    if value["program"] != PROGRAM or value["mode"] != mode_for(item_id):
        raise ClaimError("claim program/mode differs")
    if tuple(value["dependencies"]) != row["dependencies"]:
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
        "Docs/Stage5_Theorems_Blueprint.md", "Docs/Stage5_Theorems_Gantt.md",
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
    identity = value["execution_identity"]
    if identity["lane_id"] != item_id or identity["generation_id"] != value["run_id"]:
        raise ClaimError("claim lane/generation identity differs")
    if identity["execution_spec_sha256"] != baseline["execution_spec_sha256"]:
        raise ClaimError("claim execution identity specification differs")
    requested = validate_concurrency_vector(
        identity["requested_concurrency"], "requested concurrency",
    )
    resolved = validate_concurrency_vector(
        identity["resolved_concurrency"], "resolved concurrency",
    )
    for key in CONCURRENCY_DIMENSIONS:
        if key != "service_records" and resolved[key] > requested[key]:
            raise ClaimError(f"resolved concurrency increases requested dimension {key}")
    prompt, prompt_raw = strict_document(
        task_root / "work/_baseline/concurrency-prompt.json", "concurrency prompt",
    )
    if digest(prompt_raw) != identity["prompt_digest"]:
        raise ClaimError("claim concurrency prompt digest differs")
    if not isinstance(prompt, dict):
        raise ClaimError("claim concurrency prompt is not an object")
    prompt_body = dict(prompt)
    prompt_authority = prompt_body.pop("authority_sha256", None)
    if not isinstance(prompt_authority, str) or digest(canonical(prompt_body)) != prompt_authority:
        raise ClaimError("claim concurrency prompt seal differs")
    if (
        prompt.get("schema_version") != "awesome-theorems/stage5-concurrency-prompt/2.0"
        or prompt.get("program") != PROGRAM
        or prompt.get("policy_epoch") != identity["prompt_epoch"]
        or prompt.get("execution_spec_sha256") != identity["execution_spec_sha256"]
        or prompt.get("concurrency") != requested
        or prompt.get("execution_limits") != value.get("execution_policy", {}).get("execution_limits")
        or prompt.get("recovery") != value.get("execution_policy", {}).get("recovery")
    ):
        raise ClaimError("claim concurrency prompt binding differs")
    result_schema = value["result_schema"]
    expected_result_path = "Docs/evidence/stage5_theorems/worker-result.schema.json"
    if (
        result_schema["path"] != expected_result_path
        or result_schema["schema_id"] != load_schema("worker-result.schema.json")["$id"]
        or result_schema["sha256"] != file_digest(ROOT / expected_result_path)
    ):
        raise ClaimError("worker result schema binding differs")
    budget = value["resource_budget"]
    if any((key == "model_turns" and amount != "unbounded") or (key != "model_turns" and (not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0)) for key, amount in budget.items()):
        raise ClaimError("claim budget is not strictly positive and finite")
    maxima = specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
    if any(key != "model_turns" and key in maxima and budget[key] > maxima[key] for key in budget):
        raise ClaimError("claim budget exceeds operator maxima")
    retry = value["retry_budget"]
    replacement_cap = value["execution_policy"]["recovery"]["generation_replacements_per_work_item"]
    lineage = value["generation_lineage"]
    if (
        lineage["replacement_cap"] != replacement_cap
        or not 0 <= lineage["replacement_ordinal"] <= replacement_cap
        or retry["attempt"] != lineage["replacement_ordinal"] + 1
        or retry["max_attempts"] != replacement_cap + 1
        or retry["attempt"] > retry["max_attempts"]
        or (lineage["replacement_ordinal"] == 0) != (lineage["previous_generation_id"] is None)
    ):
        raise ClaimError("retry budget differs")
    commands = value["validation_commands"]
    if item_id.endswith("-TARGET"):
        work_root = task_root / "work"
        expected_argv = [
            "/usr/bin/python3", str(work_root / "_baseline/check_stage5_theorem_item.py"),
            "--claim-card", str(task_root / "claim.json"),
            "--work-root", str(work_root),
            "--no-lean",
        ]
        # Compatibility boundary for generations admitted under the previous
        # immutable claim baseline.  Those cards required the same validator
        # with canonical Lean compilation; Master integration still reruns
        # trust-zero compilation for both forms.  Successor claims always bind
        # the task-local semantic preflight above.
        legacy_expected_argv = expected_argv[:-1]
        if (
            len(commands) != 1
            or commands[0]["command_id"] != "complete-target-semantic-proof-debt"
            or commands[0]["cwd"] != str(work_root)
            or commands[0]["argv"] not in (expected_argv, legacy_expected_argv)
            or commands[0]["environment"] != []
            or commands[0]["timeout_seconds"] < 900
            or commands[0]["network"] != "denied"
        ):
            raise ClaimError("TARGET semantic proof-debt validation command differs")
    else:
        expected_validator = task_root / "work/_baseline/check_stage5_theorem_program_item.py"
        expected_argv = [
            "/usr/bin/python3", str(expected_validator),
            "--claim-card", str(task_root / "claim.json"),
            "--work-root", str(task_root / "work"),
        ]
        expected_command = f"validate-{value['mode'].lower()}-program-artifacts"
        if (
            len(commands) != 1
            or commands[0]["command_id"] != expected_command
            or commands[0]["cwd"] != str(task_root / "work")
            or commands[0]["argv"] != expected_argv
            or commands[0]["environment"] != []
            or commands[0]["timeout_seconds"] < 900
            or commands[0]["network"] != "denied"
        ):
            raise ClaimError("mode-specific program validation command differs")
    for entry in value["read_only_bootstrap_files"]:
        relative = canonical_relative(entry["path"], "read-only bootstrap path")
        source = task_root / "work" / relative
        if source.is_symlink() or not source.is_file():
            raise ClaimError(f"missing read-only bootstrap file {relative}")
        if source.stat().st_size != entry["size_bytes"] or file_digest(source) != entry["sha256"]:
            raise ClaimError(f"read-only bootstrap binding differs: {relative}")
    if item_id.endswith("-TARGET") and not any(
        entry["path"] == "_baseline/check_stage5_theorem_item.py"
        for entry in value["read_only_bootstrap_files"]
    ):
        raise ClaimError("TARGET validator is absent from the read-only baseline")
    if item_id.endswith("-TARGET") and not any(
        entry["path"].startswith("_baseline/provider-sources/")
        for entry in value["read_only_bootstrap_files"]
    ):
        raise ClaimError("pinned provider sources are absent from the read-only baseline")
    if not item_id.endswith("-TARGET") and not any(
        entry["path"] == "_baseline/check_stage5_theorem_program_item.py"
        for entry in value["read_only_bootstrap_files"]
    ):
        raise ClaimError("program-item validator is absent from the read-only baseline")
    if digest(raw) != file_digest(path):
        raise ClaimError("claim card changed while reading")
    return value


def validate_result(path: Path, claim_path: Path) -> dict[str, Any]:
    claim = validate_claim(claim_path)
    value, raw = strict_document(path, "worker result")
    validate_schema(value, load_schema("worker-result.schema.json"))
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
    for artifact in value["artifacts"]:
        artifact_path = exact_descendant(artifact["path"], task_root, "artifact")
        if artifact_path.is_symlink() or not artifact_path.is_file():
            raise ClaimError("worker artifact is missing")
        if artifact_path.stat().st_size != artifact["size_bytes"] or file_digest(artifact_path) != artifact["sha256"]:
            raise ClaimError("worker artifact binding differs")
    unsigned = dict(value)
    authority = unsigned.pop("authority_sha256")
    if digest(canonical(unsigned)) != authority:
        raise ClaimError("worker result authority seal differs")
    if digest(raw) != file_digest(path):
        raise ClaimError("worker result changed while reading")
    return value


def validate_acceptance(path: Path) -> dict[str, Any]:
    value, _ = strict_document(path, "Master acceptance")
    validate_schema(value, load_schema("master-acceptance.schema.json"))
    if value["program"] != PROGRAM or value["state_transition"]["from"] != "handoff_waiting_master" or value["state_transition"]["to"] != "master_accepted":
        raise ClaimError("Master acceptance program/transition differs")
    unsigned = dict(value)
    authority = unsigned.pop("authority_sha256")
    if digest(canonical(unsigned)) != authority:
        raise ClaimError("Master acceptance authority seal differs")
    if not value["review_decisions"] or not value["validation_gates"]:
        raise ClaimError("Master acceptance lacks review or validation evidence")
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
