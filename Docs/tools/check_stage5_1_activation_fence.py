#!/usr/bin/env python3
"""Read-only, fail-closed Stage5.1 activation-fence snapshot.

The checker never stops a predecessor, creates a receipt, changes cron, or
starts a successor.  It answers three deliberately separate questions:

* is the materialized organization release valid and still all blank;
* may a fresh Stage5.1 BOOT reacceptance be started; and
* may ordinary member admission start after BOOT acceptance.

The default CLI phase is ``member``.  Therefore a pristine all-blank release
is expected to remain non-zero until its new BOOT rows have been independently
accepted.  ``--phase boot`` exposes the earlier migration/drain boundary.
"""

from __future__ import annotations

import argparse
from collections import Counter
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from typing import Any, Iterable, Mapping, Sequence

# Dynamic release-checker imports must not create ``__pycache__`` during an
# ordinary (non-``-B``) ``--check`` invocation.
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
CURRENT = PurePosixPath("Docs/catalog/stage5_1_organization/Current_Release.json")
CATALOG_CURRENT = PurePosixPath("Docs/catalog/v5/Current_Release.json")
FENCE_RECEIPT = PurePosixPath("Docs/evidence/stage5_1_shared_execution/activation-fence.json")
PREDECESSOR_FENCE_RECEIPT = PurePosixPath(
    "Docs/evidence/stage5_1_shared_execution/predecessor-fence.json"
)

REPORT_SCHEMA = "awesome-theorems/stage5.1-activation-fence-report/1.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHECKLIST_RE = re.compile(r"(?m)^- \[(?P<state>[ _x])\] `(?P<id>[A-Z0-9_.:-]+)`")

PROGRAMS = {
    "theorems": {
        "blueprint": PurePosixPath("Docs/Stage5_1_Theorems_Blueprint.md"),
        "runtime": PurePosixPath(".ops/stage5-theorems-execution-v2"),
        "cron_begin": "# BEGIN AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V2",
        "cron_end": "# END AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V2",
        "controller_token": "stage5_theorems_execution_cron_v2.py",
        "locks": (
            ".ops/stage5-theorems-execution-v2.scheduler.lock",
            ".ops/stage5-theorems-execution-v2.admission-pump.lock",
            ".ops/stage5-theorems-execution-v2/scheduler.lock",
            ".ops/stage5-theorems-execution-v2/locks/scheduler.lock",
        ),
        "active": frozenset({
            "reserved", "materialized", "tmux_started", "goal_pasted",
            "request_reserved", "submission_committed", "goal_submitted", "live",
            "terminal_pending_disposition", "generation_retire_required",
        }),
    },
    "conjectures": {
        "blueprint": PurePosixPath("Docs/Stage5_1_Conjectures_Blueprint.md"),
        "runtime": PurePosixPath(".ops/stage5-conjectures-execution-v2"),
        "cron_begin": "# BEGIN AWESOME_THEOREMS_STAGE5_CONJECTURES_EXECUTION_V2",
        "cron_end": "# END AWESOME_THEOREMS_STAGE5_CONJECTURES_EXECUTION_V2",
        "controller_token": "stage5_conjectures_execution_cron_v2.py",
        "locks": (
            ".ops/stage5-conjectures-execution-v2.scheduler.lock",
            ".ops/stage5-conjectures-execution-v2.admission-pump.lock",
            ".ops/stage5-conjectures-execution-v2/scheduler.lock",
            ".ops/stage5-conjectures-execution-v2/locks/scheduler.lock",
        ),
        "active": frozenset({
            "reserved", "materialized", "tmux_started", "goal_pasted",
            "request_reserved", "submission_committed", "goal_submitted", "live",
            "terminal_pending_disposition", "generation_retire_required",
        }),
    },
}

CONCURRENCY_FIELDS = frozenset({
    "logical_claims", "service_records", "agent_executions",
    "startup_reservations", "launch_fanout_per_wave", "live_transports",
    "authenticated_goals", "running_turns",
    "outbound_request_starts_per_window", "in_flight_requests", "integration",
    "max_outstanding_requests_per_execution", "validators", "exact_path_conflicts",
    "desired_live_target", "hard_cap",
})
PROMPT_POLICY_FIELDS = frozenset({
    "request_window_seconds", "lifecycle_mode", "replacement_policy",
})
POSITIVE_CONCURRENCY_FIELDS = CONCURRENCY_FIELDS - {
    "service_records", "exact_path_conflicts",
}
REPLACEMENT_POLICY_FIELDS = frozenset({
    "replacement_limit", "startup_deadline_seconds", "tick_time_budget_seconds",
})
ROUTE_FIELDS = frozenset({"route", "model", "reasoning_effort", "service_tier"})
AUTHORITY_PROMPT_FIELDS = frozenset({
    "program", "policy_epoch", "source", "authority_sha256",
})
SUCCESSOR_ABSENCE_FIELDS = frozenset({
    "runtime_root", "claims", "reservations", "task_roots", "tmux_sockets",
    "processes", "request_leases", "turn_leases", "requests", "cron_marker",
})
TERMINAL_STATUSES = frozenset({
    "retired", "stopped", "finished", "master_accepted", "handoff_ready",
})


class FenceError(RuntimeError):
    """An invalid authority or unavailable observation."""


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise FenceError("non-canonical JSON value") from exc


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _strict_json(raw: bytes, label: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise FenceError(f"{label}: duplicate JSON key {key!r}")
            value[key] = child
        return value

    def constant(token: str) -> Any:
        raise FenceError(f"{label}: non-finite number {token}")

    try:
        return json.loads(raw, object_pairs_hook=hook, parse_constant=constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FenceError(f"{label}: invalid strict UTF-8 JSON") from exc


def _root_path(root: Path, relative: PurePosixPath | str, label: str,
               *, required: bool = True) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts:
        raise FenceError(f"{label}: path is not repository-relative")
    candidate = root.joinpath(*posix.parts)
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except ValueError as exc:
        raise FenceError(f"{label}: path escapes repository root") from exc
    if required and (not candidate.is_file() or candidate.is_symlink()):
        raise FenceError(f"{label}: missing regular file")
    return candidate


def _load_json_file(root: Path, relative: PurePosixPath | str, label: str) -> tuple[dict[str, Any], bytes]:
    path = _root_path(root, relative, label)
    raw = path.read_bytes()
    value = _strict_json(raw, label)
    if not isinstance(value, dict):
        raise FenceError(f"{label}: expected JSON object")
    return value, raw


def _verify_authority(value: Mapping[str, Any], label: str) -> None:
    authority = value.get("authority_sha256")
    if not isinstance(authority, str) or SHA256_RE.fullmatch(authority) is None:
        raise FenceError(f"{label}: malformed authority_sha256")
    body = dict(value)
    body.pop("authority_sha256", None)
    if _sha(_canonical(body)) != authority:
        raise FenceError(f"{label}: authority_sha256 mismatch")


def _reason(code: str, plane: str, scope: str, disposition: str,
            *, evidence_refs: Iterable[str] = (), expected: Any = None,
            observed: Any = None, item_id: str | None = None,
            generation_id: str | None = None, dimension: str | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "code": code,
        "plane": plane,
        "disposition": disposition,
        "scope": scope,
        "retry_class": "operator_reconciliation_required",
        "evidence_refs": sorted(set(evidence_refs)),
    }
    if expected is not None:
        value["expected"] = expected
    if observed is not None:
        value["observed"] = observed
    if item_id is not None:
        value["item_id"] = item_id
    if generation_id is not None:
        value["generation_id"] = generation_id
    if dimension is not None:
        value["dimension"] = dimension
    return value


def _reason_key(value: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(str(value.get(key, "")) for key in (
        "plane", "scope", "code", "item_id", "generation_id", "dimension",
    ))


def _load_release_checker(root: Path) -> Any:
    path = _root_path(root, "Docs/tools/check_stage5_1_organization_release.py",
                      "Stage5.1 release checker")
    spec = importlib.util.spec_from_file_location(
        f"stage5_1_release_for_fence_{id(root)}", path,
    )
    if spec is None or spec.loader is None:
        raise FenceError("cannot import Stage5.1 release checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise FenceError(f"cannot import Stage5.1 release checker: {exc}") from exc
    return module


def _release_audit(root: Path, pointer: Mapping[str, Any],
                   activation_receipt: Mapping[str, Any] | None = None) -> dict[str, Any]:
    release = pointer.get("organization_release")
    if not isinstance(release, str) or not release:
        raise FenceError("Stage5.1 current pointer lacks organization_release")
    checker = _load_release_checker(root)
    try:
        if activation_receipt is None:
            result = checker.audit_release(
                root, release, rebuild=True, cursor_mode="initial_blank",
            )
        else:
            result = checker.audit_release(
                root, release, rebuild=True,
                cursor_mode="boot_accepted_overlay",
                activation_receipt=activation_receipt,
            )
    except Exception as exc:
        raise FenceError(f"Stage5.1 release audit failed: {exc}") from exc
    if not isinstance(result, dict):
        raise FenceError("Stage5.1 release checker returned malformed result")
    return result


def _validate_pointer(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    pointer, _ = _load_json_file(root, CURRENT, "Stage5.1 current pointer")
    _verify_authority(pointer, "Stage5.1 current pointer")
    activation_pointer = pointer.get("activation")
    if (not isinstance(activation_pointer, dict)
            or activation_pointer.get("status") != "blocked"):
        raise FenceError("Stage5.1 current pointer must remain blocked before activation")
    manifest_binding = pointer.get("manifest")
    if not isinstance(manifest_binding, dict):
        raise FenceError("Stage5.1 current pointer lacks manifest binding")
    manifest_path = manifest_binding.get("path")
    if not isinstance(manifest_path, str):
        raise FenceError("Stage5.1 current pointer lacks manifest path")
    manifest, manifest_raw = _load_json_file(root, manifest_path, "Stage5.1 manifest")
    _verify_authority(manifest, "Stage5.1 manifest")
    if manifest_binding.get("sha256") != _sha(manifest_raw):
        raise FenceError("Stage5.1 current pointer manifest digest mismatch")
    if manifest_binding.get("authority_sha256") != manifest.get("authority_sha256"):
        raise FenceError("Stage5.1 current pointer manifest authority mismatch")
    activation = manifest.get("activation")
    if not isinstance(activation, dict) or activation.get("status") != "blocked":
        raise FenceError("Stage5.1 manifest must remain blocked before activation")
    if (activation.get("requires_explicit_operator_concurrency_prompt") is not True
            or activation.get("concurrency_defaults_present") is not False
            or activation.get("fence_receipt_path") != str(FENCE_RECEIPT)):
        raise FenceError("Stage5.1 manifest activation contract is incomplete")
    return pointer, manifest


def _catalog_parent_valid(root: Path) -> dict[str, Any]:
    value, _ = _load_json_file(root, CATALOG_CURRENT, "Stage5 catalog current pointer")
    _verify_authority(value, "Stage5 catalog current pointer")
    if value.get("release") != "5.6" or value.get("manifest_path") != "releases/5.6/Release_Manifest.json":
        raise FenceError("Stage5 parent catalog pointer no longer selects 5.6")
    return value


def _extract_spec(text: str, label: str) -> dict[str, Any]:
    fences = re.findall(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    candidates: list[dict[str, Any]] = []
    for index, body in enumerate(fences):
        value = _strict_json(body.encode("utf-8"), f"{label} JSON fence {index + 1}")
        if isinstance(value, dict) and isinstance(value.get("concurrency_prompt_contract"), dict):
            candidates.append(value)
    if len(candidates) != 1:
        raise FenceError(f"{label}: expected one execution specification")
    return candidates[0]


def _blueprint_contracts(root: Path, pointer: Mapping[str, Any],
                         activation_receipt: Mapping[str, Any] | None = None) -> tuple[dict[str, dict[str, Any]], dict[str, bool]]:
    pointer_rows = pointer.get("blueprints")
    if not isinstance(pointer_rows, dict):
        raise FenceError("Stage5.1 current pointer blueprints malformed")
    by_program = pointer_rows
    if set(by_program) != set(PROGRAMS):
        raise FenceError("Stage5.1 current pointer must bind both programs exactly once")
    specifications: dict[str, dict[str, Any]] = {}
    boot_accepted: dict[str, bool] = {}
    for program, policy in PROGRAMS.items():
        relative = policy["blueprint"]
        row = by_program[program]
        if not isinstance(row, dict) or row.get("path") != str(relative):
            raise FenceError(f"{program} Blueprint path differs from fixed Stage5.1 authority")
        path = _root_path(root, relative, f"{program} Blueprint")
        raw = path.read_bytes()
        if activation_receipt is None:
            if row.get("sha256") != _sha(raw):
                raise FenceError(f"{program} Blueprint pointer digest mismatch")
        else:
            boots = activation_receipt.get("boot_acceptance")
            binding = boots.get(program) if isinstance(boots, Mapping) else None
            if (not isinstance(binding, Mapping)
                    or binding.get("pre_blueprint_sha256") != row.get("sha256")
                    or binding.get("post_blueprint_sha256") != _sha(raw)):
                raise FenceError(f"{program} Blueprint overlay digest mismatch")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise FenceError(f"{program} Blueprint is not UTF-8") from exc
        rows = [(match.group("id"), match.group("state")) for match in CHECKLIST_RE.finditer(text)]
        if not rows:
            raise FenceError(f"{program} Blueprint has no checklist rows")
        invalid_nonboot = [identity for identity, state in rows
                           if "BOOT" not in identity and state != " "]
        if invalid_nonboot:
            raise FenceError(f"{program} Blueprint contains nonblank ordinary rows")
        boot_rows = [(identity, state) for identity, state in rows if "BOOT" in identity]
        if len(boot_rows) != 1:
            raise FenceError(f"{program} Blueprint must contain exactly one BOOT row")
        boot_accepted[program] = boot_rows[0][1] == "x"
        specifications[program] = _extract_spec(text, f"{program} Blueprint")
    return specifications, boot_accepted


def _prompt_path(specification: Mapping[str, Any], program: str) -> str:
    contract = specification.get("concurrency_prompt_contract")
    if not isinstance(contract, dict):
        raise FenceError(f"{program} Blueprint lacks concurrency_prompt_contract")
    required = contract.get("required_dimensions", contract.get("required_fields"))
    if not isinstance(required, list) or not all(isinstance(field, str) for field in required):
        raise FenceError(f"{program} Blueprint has malformed required concurrency dimensions")
    if set(required) != CONCURRENCY_FIELDS or len(required) != len(set(required)):
        raise FenceError(f"{program} Blueprint concurrency dimension contract is incomplete")
    policy_fields = contract.get("required_policy_fields")
    if (not isinstance(policy_fields, list)
            or not all(isinstance(field, str) for field in policy_fields)
            or set(policy_fields) != PROMPT_POLICY_FIELDS
            or len(policy_fields) != len(set(policy_fields))):
        raise FenceError(f"{program} Blueprint prompt policy-field contract is incomplete")
    replacement_fields = contract.get("required_replacement_policy_fields")
    if (not isinstance(replacement_fields, list)
            or set(replacement_fields) != REPLACEMENT_POLICY_FIELDS
            or len(replacement_fields) != len(set(replacement_fields))):
        raise FenceError(f"{program} Blueprint replacement-policy contract is incomplete")
    route_fields = contract.get("required_route_fields", contract.get("required_prompt_fields"))
    if (not isinstance(route_fields, list)
            or not all(isinstance(field, str) for field in route_fields)
            or set(route_fields) != ROUTE_FIELDS
            or len(route_fields) != len(set(route_fields))):
        raise FenceError(f"{program} Blueprint prompt route-field contract is incomplete")
    authority_fields = contract.get("required_authority_fields")
    if (not isinstance(authority_fields, list)
            or not all(isinstance(field, str) for field in authority_fields)
            or set(authority_fields) != AUTHORITY_PROMPT_FIELDS
            or len(authority_fields) != len(set(authority_fields))):
        raise FenceError(f"{program} Blueprint prompt authority-field contract is incomplete")
    if contract.get("value_source") != "explicit_execution_prompt_only":
        raise FenceError(f"{program} Blueprint permits a non-prompt concurrency source")
    if not str(contract.get("missing_policy", "")).startswith("fail_closed"):
        raise FenceError(f"{program} Blueprint does not fail closed on a missing prompt")
    if contract.get("defaults_forbidden") is not True:
        raise FenceError(f"{program} Blueprint does not explicitly forbid defaults")
    for key, value in contract.items():
        lowered = key.lower()
        if lowered == "defaults_forbidden" and value is True:
            continue
        if "default" in lowered:
            raise FenceError(f"{program} Blueprint concurrency contract embeds a default")
    path = contract.get("prompt_path", contract.get("expected_prompt_path"))
    if not isinstance(path, str) or not path:
        raise FenceError(f"{program} Blueprint does not declare the expected prompt path")
    return path


def _successor_contract(specification: Mapping[str, Any], program: str) -> dict[str, str]:
    activation = specification.get("activation_contract")
    if not isinstance(activation, dict):
        raise FenceError(f"{program} Blueprint lacks activation_contract")
    runtime = activation.get("runtime_root")
    controller = activation.get("controller_path")
    begin = activation.get("cron_marker_begin")
    end = activation.get("cron_marker_end")
    activation_prompt = activation.get("prompt_path")
    predecessor_receipt = activation.get("predecessor_fence_receipt_path")
    concurrency_prompt = specification.get("concurrency_prompt_contract", {}).get("prompt_path")
    absence = activation.get("required_side_effect_absence")
    if (not isinstance(runtime, str) or not runtime.startswith(".ops/")
            or not isinstance(controller, str)
            or not isinstance(begin, str) or not isinstance(end, str)
            or not begin or not end
            or not isinstance(activation_prompt, str)
            or activation_prompt != concurrency_prompt
            or predecessor_receipt != str(PREDECESSOR_FENCE_RECEIPT)
            or not isinstance(absence, list)
            or set(absence) != SUCCESSOR_ABSENCE_FIELDS):
        raise FenceError(f"{program} Blueprint lacks the exact successor runtime/cron contract")
    posix_runtime = PurePosixPath(runtime)
    if posix_runtime.is_absolute() or ".." in posix_runtime.parts:
        raise FenceError(f"{program} Blueprint successor runtime path is unsafe")
    if not controller.startswith("scripts/") or ".." in PurePosixPath(controller).parts:
        raise FenceError(f"{program} Blueprint successor controller path is unsafe")
    return {
        "runtime_root": runtime, "controller_path": controller,
        "cron_begin": begin, "cron_end": end,
    }


def _valid_prompt(root: Path, specification: Mapping[str, Any], program: str) -> tuple[bool, dict[str, Any]]:
    path_text = _prompt_path(specification, program)
    path = _root_path(root, path_text, f"{program} concurrency prompt", required=False)
    observation: dict[str, Any] = {"path": path_text, "present": path.is_file() and not path.is_symlink()}
    if not observation["present"]:
        return False, observation
    raw = path.read_bytes()
    try:
        prompt = _strict_json(raw, f"{program} concurrency prompt")
    except FenceError as exc:
        observation["error"] = str(exc)
        return False, observation
    if not isinstance(prompt, dict):
        observation["error"] = "prompt is not an object"
        return False, observation
    vector = prompt.get("concurrency")
    if not isinstance(vector, dict) or set(vector) != CONCURRENCY_FIELDS:
        observation["error"] = "concurrency vector is not exact and complete"
        return False, observation
    for field, value in vector.items():
        if field == "service_records":
            if value != "not_applicable" and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                observation["error"] = f"invalid {field}"
                return False, observation
        elif field == "exact_path_conflicts":
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                observation["error"] = f"invalid {field}"
                return False, observation
        elif field in POSITIVE_CONCURRENCY_FIELDS:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                observation["error"] = f"invalid {field}"
                return False, observation
    source = prompt.get("source")
    source_lower = source.lower() if isinstance(source, str) else ""
    denies_default = any(token in source_lower for token in (
        "no default", "not a default", "defaults forbidden", "default forbidden",
    ))
    denies_inheritance = any(token in source_lower for token in (
        "no inherit", "no inherited", "not inherited", "nor inherited",
        "inheritance forbidden", "inherited value forbidden",
    ))
    if (not isinstance(source, str)
            or not all(token in source_lower for token in ("explicit", "current", "operator", "prompt"))
            or ("default" in source_lower and not denies_default)
            or ("inherit" in source_lower and not denies_inheritance)):
        observation["error"] = "prompt source is not explicitly current-operator supplied"
        return False, observation
    if not isinstance(prompt.get("policy_epoch"), str) or not prompt["policy_epoch"]:
        observation["error"] = "missing policy_epoch"
        return False, observation
    request_window = prompt.get("request_window_seconds")
    if not isinstance(request_window, int) or isinstance(request_window, bool) or request_window <= 0:
        observation["error"] = "request_window_seconds must be an explicit positive integer"
        return False, observation
    lifecycle_mode = prompt.get("lifecycle_mode")
    if lifecycle_mode not in {"bounded", "persistent_pool"}:
        observation["error"] = "lifecycle_mode is missing or invalid"
        return False, observation
    replacement = prompt.get("replacement_policy")
    if not isinstance(replacement, dict) or set(replacement) != REPLACEMENT_POLICY_FIELDS:
        observation["error"] = "replacement_policy is missing or incomplete"
        return False, observation
    if any(not isinstance(value, int) or isinstance(value, bool) or value <= 0
           for value in replacement.values()):
        observation["error"] = "replacement_policy contains an implicit value"
        return False, observation
    for field in ROUTE_FIELDS:
        value = prompt.get(field)
        if not isinstance(value, str) or not value:
            observation["error"] = f"missing explicit route field {field}"
            return False, observation
    if prompt.get("program") not in {program, f"stage5.1-{program}", f"stage5_1_{program}"}:
        observation["error"] = "program/epoch binding differs"
        return False, observation
    if isinstance(prompt.get("authority_sha256"), str):
        try:
            _verify_authority(prompt, f"{program} concurrency prompt")
        except FenceError as exc:
            observation["error"] = str(exc)
            return False, observation
    else:
        observation["error"] = "missing authority_sha256"
        return False, observation
    observation.update({"sha256": _sha(raw), "policy_epoch": prompt["policy_epoch"], "complete": True})
    return True, observation


def _host_crontab() -> tuple[str, str | None]:
    try:
        result = subprocess.run(
            ["crontab", "-l"], check=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return "", str(exc)
    if result.returncode not in {0, 1}:
        return "", f"crontab -l exited {result.returncode}"
    # Common implementations use exit 1 for an empty crontab.
    if result.returncode == 1 and result.stdout:
        return "", f"crontab -l failed: {result.stderr.strip()}"
    return result.stdout, None


def _host_processes() -> tuple[list[dict[str, Any]], str | None]:
    rows: list[dict[str, Any]] = []
    proc = Path("/proc")
    try:
        candidates = [path for path in proc.iterdir() if path.name.isdigit()]
    except OSError as exc:
        return [], str(exc)
    for path in candidates:
        try:
            raw_stat = (path / "stat").read_text()
            tail = raw_stat.rsplit(") ", 1)[1].split()
            start_ticks = int(tail[19])
            argv_raw = (path / "cmdline").read_bytes()
            argv = argv_raw.replace(b"\x00", b" ").decode("utf-8", "replace").strip()
            cwd = os.readlink(path / "cwd")
            environ = (path / "environ").read_bytes().split(b"\x00")
            codex_home = None
            for item in environ:
                if item.startswith(b"CODEX_HOME="):
                    codex_home = item.split(b"=", 1)[1].decode("utf-8", "replace")
                    break
            rows.append({
                "pid": int(path.name), "start_ticks": start_ticks, "argv": argv,
                "cwd": cwd, "codex_home": codex_home,
            })
        except (OSError, ValueError, IndexError):
            continue
    return rows, None


def _marker_count(text: str, begin: str, end: str) -> tuple[int, bool]:
    begins = text.count(begin)
    ends = text.count(end)
    ambiguous = begins != ends or begins > 1 or ends > 1
    return max(begins, ends), ambiguous


def _load_state(root: Path, runtime: PurePosixPath,
                program: str) -> tuple[dict[str, Any], str | None, str | None]:
    relative = runtime / "state/controller-state.json"
    path = _root_path(root, relative, f"{program} predecessor state", required=False)
    if not path.exists():
        return {}, None, None
    if not path.is_file() or path.is_symlink():
        return {}, "predecessor state is not a regular file", None
    raw = path.read_bytes()
    try:
        value = _strict_json(raw, f"{program} predecessor state")
    except FenceError as exc:
        return {}, str(exc), _sha(raw)
    if not isinstance(value, dict) or not isinstance(value.get("claims", {}), dict):
        return {}, "predecessor state/claims schema is malformed", _sha(raw)
    authority = value.get("authority_sha256")
    if authority is not None:
        if not isinstance(authority, str) or SHA256_RE.fullmatch(authority) is None:
            return {}, "predecessor state authority_sha256 is malformed", _sha(raw)
        body = dict(value)
        body.pop("authority_sha256", None)
        if _sha(_canonical(body)) != authority:
            return {}, "predecessor state authority_sha256 mismatch", _sha(raw)
    return value, None, _sha(raw)


def _claims(state: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = state.get("claims", {})
    return [dict(row) for row in value.values() if isinstance(row, dict)] if isinstance(value, dict) else []


def _path_under(value: Any, root: Path) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        Path(value).resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except (OSError, ValueError):
        return False


def _owner_processes(process_rows: Sequence[Mapping[str, Any]], runtime_path: Path,
                     claims: Sequence[Mapping[str, Any]], controller_token: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    identities = {
        (row.get("pane_pid"), row.get("pane_pid_start_ticks"))
        for row in claims if isinstance(row.get("pane_pid"), int)
    }
    controllers: list[dict[str, Any]] = []
    descendants: list[dict[str, Any]] = []
    for row in process_rows:
        compact = {key: row.get(key) for key in ("pid", "start_ticks", "argv", "cwd", "codex_home")}
        if controller_token in str(row.get("argv", "")):
            controllers.append(compact)
        exact = (row.get("pid"), row.get("start_ticks")) in identities
        owned = exact or _path_under(row.get("cwd"), runtime_path) or _path_under(row.get("codex_home"), runtime_path)
        if owned:
            descendants.append(compact)
    return controllers, descendants


def _socket_census(runtime_path: Path) -> list[str]:
    if not runtime_path.exists():
        return []
    found: list[str] = []
    try:
        for path in runtime_path.rglob("tmux.sock"):
            try:
                mode = path.lstat().st_mode
            except OSError:
                continue
            if stat.S_ISSOCK(mode) or path.is_symlink():
                found.append(path.relative_to(runtime_path).as_posix())
    except OSError:
        return ["<socket-census-failed>"]
    return sorted(found)


def _unharvested_active_work(claims: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    """Find active generations with changed owned files but no durable result/checkpoint.

    This remains observational.  It deliberately does not try to manufacture a
    result or checkpoint from worker bytes.
    """

    pending: list[dict[str, str]] = []
    for claim in claims:
        work_root = claim.get("work_root", claim.get("cwd"))
        task_root = claim.get("task_root")
        owned = claim.get("owned_paths")
        if not isinstance(work_root, str) or not isinstance(task_root, str) or not isinstance(owned, list):
            continue
        changed = False
        for relative in owned:
            if not isinstance(relative, str):
                continue
            path = Path(work_root) / relative
            try:
                if path.is_file() and path.stat().st_size > 0:
                    changed = True
                    break
            except OSError:
                changed = True
                break
        if not changed:
            continue
        result_candidates = (
            Path(task_root) / "_outbox/result.json",
            Path(work_root) / "_outbox/result.json",
        )
        disposition = claim.get("checkpoint") or claim.get("terminal_disposition") or claim.get("handoff")
        if not any(path.is_file() and not path.is_symlink() for path in result_candidates) and not isinstance(disposition, dict):
            pending.append({
                "item_id": str(claim.get("item_id", "")),
                "generation_id": str(claim.get("run_id", "")),
            })
    return pending


def _lock_held(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    except OSError:
        return True
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        finally:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
        return False
    finally:
        os.close(fd)


def _latest_leases(root: Path, runtime: PurePosixPath) -> tuple[list[dict[str, Any]], list[str]]:
    unresolved: list[dict[str, Any]] = []
    errors: list[str] = []
    for name in ("request-leases.jsonl", "turn-leases.jsonl"):
        path = _root_path(root, runtime / "ledgers" / name, name, required=False)
        if not path.exists():
            continue
        if not path.is_file() or path.is_symlink():
            errors.append(f"{name}:nonregular")
            continue
        latest: dict[str, dict[str, Any]] = {}
        try:
            for number, line in enumerate(path.read_bytes().splitlines(), 1):
                if not line:
                    raise FenceError(f"{name}:{number}: blank row")
                row = _strict_json(line, f"{name}:{number}")
                if not isinstance(row, dict) or not isinstance(row.get("lease_id"), str):
                    raise FenceError(f"{name}:{number}: malformed lease")
                latest[row["lease_id"]] = row
        except FenceError as exc:
            errors.append(str(exc))
            continue
        unresolved.extend(row for row in latest.values() if row.get("status") != "released")
    return unresolved, errors


def _queue_inventory(root: Path, runtime: PurePosixPath) -> tuple[dict[str, int], str, bool]:
    counts: dict[str, int] = {}
    inventory: list[dict[str, Any]] = []
    valid = True
    for name in ("integration", "repair", "checkpoints", "handoffs"):
        path = root.joinpath(*(runtime / name).parts)
        try:
            files = sorted(child for child in path.rglob("*"))
            if path.exists() and (not path.is_dir() or path.is_symlink()):
                raise OSError(f"{runtime / name} is not a regular directory")
            regular = []
            for child in files:
                if child.is_symlink():
                    raise OSError(f"{child} is a symlink")
                if child.is_file():
                    raw = child.read_bytes()
                    regular.append(child)
                    inventory.append({
                        "path": child.relative_to(root).as_posix(),
                        "sha256": _sha(raw), "size_bytes": len(raw),
                    })
            counts[name] = len(regular)
        except OSError:
            counts[name] = -1
            valid = False
    return counts, _sha(_canonical(inventory)), valid


def _queue_disposition(root: Path, runtime: PurePosixPath, receipt: Mapping[str, Any] | None,
                       program: str) -> tuple[dict[str, int], str, bool]:
    counts, inventory_sha256, inventory_valid = _queue_inventory(root, runtime)
    pending = counts["integration"] > 0 or counts["repair"] > 0
    if not inventory_valid:
        return counts, inventory_sha256, False
    if not pending:
        return counts, inventory_sha256, True
    if not isinstance(receipt, Mapping):
        return counts, inventory_sha256, False
    programs = receipt.get("predecessors")
    if not isinstance(programs, Mapping):
        return counts, inventory_sha256, False
    disposition = programs.get(program)
    if not isinstance(disposition, Mapping):
        return counts, inventory_sha256, False
    return counts, inventory_sha256, (
        disposition.get("queues_dispositioned") is True
        and disposition.get("queue_inventory_sha256") == inventory_sha256
    )


def _predecessor_fence_receipt(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = _root_path(root, PREDECESSOR_FENCE_RECEIPT, "predecessor fence receipt", required=False)
    if not path.exists():
        return None, None
    if not path.is_file() or path.is_symlink():
        return None, "predecessor fence receipt is not a regular file"
    try:
        value = _strict_json(path.read_bytes(), "predecessor fence receipt")
        if not isinstance(value, dict):
            raise FenceError("predecessor fence receipt is not an object")
        _verify_authority(value, "predecessor fence receipt")
        expected_keys = {
            "schema_version", "organization_release", "status", "evidence_as_of",
            "manifest_sha256", "crontab_sha256", "checker", "reviewer_id",
            "review_receipt_sha256", "prompt_digests", "predecessors", "authority_sha256",
        }
        if set(value) != expected_keys:
            raise FenceError("predecessor fence receipt has a non-closed top-level shape")
        if (value.get("schema_version") != "awesome-theorems/stage5-1-predecessor-fence/1.0"
                or value.get("organization_release") != "1.0"
                or value.get("status") != "accepted"
                or not isinstance(value.get("evidence_as_of"), str)
                or not isinstance(value.get("reviewer_id"), str)
                or not value["reviewer_id"]):
            raise FenceError("predecessor fence receipt identity/status is invalid")
        for field in ("manifest_sha256", "crontab_sha256", "review_receipt_sha256"):
            if not isinstance(value.get(field), str) or SHA256_RE.fullmatch(value[field]) is None:
                raise FenceError(f"predecessor fence receipt has malformed {field}")
        checker_binding = value.get("checker")
        checker_path = "Docs/tools/check_stage5_1_activation_fence.py"
        if (not isinstance(checker_binding, dict)
                or set(checker_binding) != {"path", "sha256"}
                or checker_binding.get("path") != checker_path
                or checker_binding.get("sha256") != _sha(_root_path(root, checker_path, "fence checker").read_bytes())):
            raise FenceError("predecessor fence receipt checker binding differs")
        for group_name in ("prompt_digests", "predecessors"):
            group = value.get(group_name)
            if not isinstance(group, dict) or set(group) != set(PROGRAMS):
                raise FenceError(f"predecessor fence receipt {group_name} is incomplete")
        for program, predecessor in value["predecessors"].items():
            expected_predecessor = {
                "runtime_root", "state_sha256", "admission_fenced",
                "live_generations_zero", "reservations_zero", "queues_dispositioned",
                "owner_processes_zero", "tmux_sockets_zero", "leases_released",
                "queue_inventory_sha256",
            }
            if not isinstance(predecessor, dict) or set(predecessor) != expected_predecessor:
                raise FenceError(f"predecessor fence receipt {program} predecessor shape differs")
            if predecessor.get("runtime_root") != str(PROGRAMS[program]["runtime"]):
                raise FenceError(f"predecessor fence receipt {program} runtime differs")
            for flag in (
                "admission_fenced", "live_generations_zero", "reservations_zero",
                "queues_dispositioned", "owner_processes_zero", "tmux_sockets_zero",
                "leases_released",
            ):
                if predecessor.get(flag) is not True:
                    raise FenceError(f"predecessor fence receipt {program} {flag} is not true")
            for field in ("state_sha256", "queue_inventory_sha256"):
                if not isinstance(predecessor.get(field), str) or SHA256_RE.fullmatch(predecessor[field]) is None:
                    raise FenceError(f"predecessor fence receipt {program} {field} is malformed")
        return value, None
    except FenceError as exc:
        return None, str(exc)


def _validate_predecessor_receipt_bindings(
    receipt: Mapping[str, Any], *, pointer: Mapping[str, Any],
    crontab_text: str, prompt_observations: Mapping[str, Mapping[str, Any]],
    runtime_observations: Mapping[str, Mapping[str, Any]], bind_prompts: bool,
) -> str | None:
    """Rebind a signed predecessor receipt to the live read-only census."""

    try:
        manifest = pointer.get("manifest")
        if (not isinstance(manifest, Mapping)
                or receipt.get("manifest_sha256") != manifest.get("sha256")):
            raise FenceError("predecessor receipt manifest digest is stale")
        if receipt.get("crontab_sha256") != _sha(crontab_text.encode("utf-8")):
            raise FenceError("predecessor receipt crontab digest is stale")
        prompt_digests = receipt.get("prompt_digests")
        predecessor_rows = receipt.get("predecessors")
        if not isinstance(prompt_digests, Mapping) or not isinstance(predecessor_rows, Mapping):
            raise FenceError("predecessor receipt binding groups are malformed")
        for program in PROGRAMS:
            observed = runtime_observations.get(program)
            expected = predecessor_rows.get(program)
            if bind_prompts:
                prompt = prompt_observations.get(program)
                if (not isinstance(prompt, Mapping)
                        or prompt_digests.get(program) != prompt.get("sha256")):
                    raise FenceError(f"predecessor receipt {program} prompt digest is stale")
            if not isinstance(observed, Mapping) or not isinstance(expected, Mapping):
                raise FenceError(f"predecessor receipt {program} census is absent")
            for receipt_field, observed_field, zero in (
                ("admission_fenced", "admission_fenced", True),
                ("live_generations_zero", "active_claims", 0),
                ("reservations_zero", "active_reservations", 0),
                ("queues_dispositioned", "queues_dispositioned", True),
                ("owner_processes_zero", "owner_processes", 0),
                ("tmux_sockets_zero", "tmux_sockets", 0),
                ("leases_released", "unreleased_leases", 0),
            ):
                if expected.get(receipt_field) is not True or observed.get(observed_field) != zero:
                    raise FenceError(
                        f"predecessor receipt {program} {receipt_field} differs from live census"
                    )
            if (expected.get("state_sha256") != observed.get("state_sha256")
                    or expected.get("queue_inventory_sha256")
                    != observed.get("queue_inventory_sha256")):
                raise FenceError(f"predecessor receipt {program} state/queue digest is stale")
        return None
    except FenceError as exc:
        return str(exc)


def _activation_receipt(root: Path, predecessor_raw: bytes | None,
                        predecessor: Mapping[str, Any] | None) -> tuple[dict[str, Any] | None, str | None]:
    path = _root_path(root, FENCE_RECEIPT, "activation fence receipt", required=False)
    if not path.exists():
        return None, None
    if not path.is_file() or path.is_symlink():
        return None, "activation fence receipt is not a regular file"
    try:
        value = _strict_json(path.read_bytes(), "activation fence receipt")
        if not isinstance(value, dict):
            raise FenceError("activation fence receipt is not an object")
        _verify_authority(value, "activation fence receipt")
        if set(value) != {
            "schema_version", "organization_release", "status",
            "predecessor_fence", "boot_acceptance", "authority_sha256",
        }:
            raise FenceError("activation fence receipt has a non-closed shape")
        if (value.get("schema_version") != "awesome-theorems/stage5-1-activation-fence/1.0"
                or value.get("organization_release") != "1.0"
                or value.get("status") != "accepted"):
            raise FenceError("activation fence receipt identity/status differs")
        binding = value.get("predecessor_fence")
        if (not isinstance(binding, dict) or set(binding) != {"path", "sha256", "authority_sha256"}
                or binding.get("path") != str(PREDECESSOR_FENCE_RECEIPT)
                or predecessor_raw is None or predecessor is None
                or binding.get("sha256") != _sha(predecessor_raw)
                or binding.get("authority_sha256") != predecessor.get("authority_sha256")):
            raise FenceError("activation fence predecessor receipt binding differs")
        boots = value.get("boot_acceptance")
        if not isinstance(boots, dict) or set(boots) != set(PROGRAMS):
            raise FenceError("activation fence boot acceptance is incomplete")
        for program, boot in boots.items():
            if not isinstance(boot, dict) or set(boot) != {
                "item_id", "pre_blueprint_sha256", "post_blueprint_sha256",
                "post_gantt_sha256", "review_receipt_sha256",
            }:
                raise FenceError(f"activation fence {program} BOOT shape differs")
            for field in (
                "pre_blueprint_sha256", "post_blueprint_sha256",
                "post_gantt_sha256", "review_receipt_sha256",
            ):
                if not isinstance(boot.get(field), str) or SHA256_RE.fullmatch(boot[field]) is None:
                    raise FenceError(f"activation fence {program} {field} is malformed")
        return value, None
    except FenceError as exc:
        return None, str(exc)


def _successor_side_effects(root: Path, crontab_text: str,
                            process_rows: Sequence[Mapping[str, Any]],
                            contracts: Mapping[str, Mapping[str, str]]) -> list[str]:
    effects: list[str] = []
    for program, contract in sorted(contracts.items()):
        relative = PurePosixPath(contract["runtime_root"])
        successor_root = root.joinpath(*relative.parts)
        if successor_root.exists():
            effects.append(f"runtime:{program}:{relative}")
        count, ambiguous = _marker_count(
            crontab_text, contract["cron_begin"], contract["cron_end"],
        )
        if count or ambiguous:
            effects.append(f"cron:{program}")
        token = PurePosixPath(contract["controller_path"]).name
        if any(token in str(row.get("argv", "")) for row in process_rows):
            effects.append(f"process:{program}")
    return sorted(set(effects))


def evaluate(root: Path = ROOT, *, phase: str = "member",
             crontab_text: str | None = None,
             process_rows: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Evaluate the fence without mutating repository or host state.

    Tests may inject ``crontab_text`` and ``process_rows``.  Production calls
    take read-only snapshots from ``crontab -l`` and ``/proc``.
    """

    if phase not in {"materialization", "boot", "member"}:
        raise ValueError("phase must be materialization, boot, or member")
    root = Path(root).resolve()
    reasons: list[dict[str, Any]] = []
    checks: dict[str, dict[str, Any]] = {}
    observations: dict[str, Any] = {"requested_phase": phase}

    predecessor_path = _root_path(
        root, PREDECESSOR_FENCE_RECEIPT, "predecessor fence receipt", required=False,
    )
    predecessor_raw = (predecessor_path.read_bytes()
                       if predecessor_path.is_file() and not predecessor_path.is_symlink() else None)
    predecessor_receipt, predecessor_receipt_error = _predecessor_fence_receipt(root)
    activation_receipt, activation_receipt_error = _activation_receipt(
        root, predecessor_raw, predecessor_receipt,
    )

    try:
        if not root.is_dir():
            raise FenceError("repository root is not a directory")
        pointer, manifest = _validate_pointer(root)
        parent = _catalog_parent_valid(root)
        release_counts = _release_audit(root, pointer, activation_receipt)
        specifications, boot_accepted = _blueprint_contracts(
            root, pointer, activation_receipt,
        )
        successor_contracts = {
            program: _successor_contract(specification, program)
            for program, specification in specifications.items()
        }
        materialization_valid = True
        observations.update({
            "organization_release": pointer.get("organization_release"),
            "release_counts": release_counts,
            "catalog_parent_release": parent.get("release"),
            "release_activation_status": manifest.get("activation", {}).get("status"),
            "boot_accepted": boot_accepted,
        })
        checks["materialization"] = {"passed": True}
    except (OSError, FenceError) as exc:
        materialization_valid = False
        specifications = {}
        successor_contracts = {}
        boot_accepted = {program: False for program in PROGRAMS}
        reasons.append(_reason(
            "STAGE51_AUTHORITY_INVALID", "authority", "stage5.1-release",
            "repair_materialized_release", observed=str(exc),
            evidence_refs=[str(CURRENT)],
        ))
        checks["materialization"] = {"passed": False}

    if crontab_text is None:
        crontab_text, cron_error = _host_crontab()
    else:
        cron_error = None
    if process_rows is None:
        process_rows, process_error = _host_processes()
    else:
        process_rows = [dict(row) for row in process_rows]
        process_error = None
    if cron_error or process_error:
        reasons.append(_reason(
            "OBSERVATION_FAILED", "host", "host-observation", "retry_read_only_observation",
            observed={"crontab": cron_error, "processes": process_error},
        ))

    if predecessor_receipt_error:
        reasons.append(_reason(
            "PREDECESSOR_FENCE_RECEIPT_INVALID", "migration", "predecessors",
            "repair_fence_receipt", observed=predecessor_receipt_error,
            evidence_refs=[str(PREDECESSOR_FENCE_RECEIPT)],
        ))
    elif predecessor_receipt is None:
        reasons.append(_reason(
            "PREDECESSOR_FENCE_RECEIPT_REQUIRED", "migration", "predecessors",
            "independently_review_and_accept_predecessor_fence",
            evidence_refs=[str(PREDECESSOR_FENCE_RECEIPT)],
        ))
    if activation_receipt_error:
        reasons.append(_reason(
            "ACTIVATION_FENCE_RECEIPT_INVALID", "activation", "stage5.1",
            "repair_post_boot_activation_receipt", observed=activation_receipt_error,
            evidence_refs=[str(FENCE_RECEIPT)],
        ))

    prompt_valid: dict[str, bool] = {}
    prompt_observations: dict[str, Any] = {}
    if materialization_valid:
        for program, specification in specifications.items():
            try:
                valid, observed = _valid_prompt(root, specification, program)
            except FenceError as exc:
                valid, observed = False, {"error": str(exc)}
            prompt_valid[program] = valid
            prompt_observations[program] = observed
            if not observed.get("present", False):
                reasons.append(_reason(
                    "CONCURRENCY_PROMPT_REQUIRED", "concurrency", program,
                    "supply_current_operator_prompt", evidence_refs=[str(PROGRAMS[program]["blueprint"])],
                ))
            elif not valid:
                reasons.append(_reason(
                    "CONCURRENCY_PROMPT_INVALID", "concurrency", program,
                    "replace_with_complete_explicit_prompt", observed=observed.get("error"),
                    evidence_refs=[str(observed.get("path", ""))],
                ))
    else:
        prompt_valid = {program: False for program in PROGRAMS}
    observations["concurrency_prompts"] = prompt_observations

    predecessor_observations: dict[str, Any] = {}
    predecessor_ready = True
    for program, policy in PROGRAMS.items():
        runtime = policy["runtime"]
        runtime_path = root.joinpath(*runtime.parts)
        marker_count, marker_ambiguous = _marker_count(
            crontab_text, policy["cron_begin"], policy["cron_end"],
        )
        state, state_error, state_sha256 = _load_state(root, runtime, program)
        claims = _claims(state)
        statuses = Counter(str(row.get("status")) for row in claims)
        active_claims = [row for row in claims if row.get("status") in policy["active"]]
        unknown_claims = [row for row in claims
                          if row.get("status") not in policy["active"] | TERMINAL_STATUSES]
        controllers, descendants = _owner_processes(
            process_rows, runtime_path, claims, policy["controller_token"],
        )
        sockets = _socket_census(runtime_path)
        held_locks = []
        for relative_text in policy["locks"]:
            relative = PurePosixPath(relative_text)
            path = root.joinpath(*relative.parts)
            if _lock_held(path):
                held_locks.append(str(relative))
        unresolved_leases, lease_errors = _latest_leases(root, runtime)
        queue_counts, queue_inventory_sha256, queues_dispositioned = _queue_disposition(
            root, runtime, predecessor_receipt, program,
        )
        reservations = state.get("reservations", [])
        if reservations is None:
            reservations = []
        if not isinstance(reservations, list) or not all(
            isinstance(row, dict) for row in reservations
        ):
            reservation_error = "predecessor reservations schema is malformed"
            active_reservations: list[Mapping[str, Any]] = []
        else:
            reservation_error = None
            # A predecessor may retain append-only reservation history, but a
            # Stage5.1 fence requires explicit terminal disposition.  Merely
            # expiring a `reserved` row is never an implicit release.
            active_reservations = [
                row for row in reservations
                if row.get("status") not in {"released", "retired", "stopped", "settled"}
            ]
        unharvested_work = _unharvested_active_work(active_claims)
        predecessor_observations[program] = {
            "cron_marker_count": marker_count,
            "cron_marker_ambiguous": marker_ambiguous,
            "admission_fenced": not marker_count and not marker_ambiguous
                                and not controllers and not held_locks,
            "state_sha256": state_sha256,
            "claim_status_counts": dict(sorted(statuses.items())),
            "active_claims": len(active_claims),
            "active_reservations": len(active_reservations),
            "unknown_claims": len(unknown_claims),
            "controller_processes": len(controllers),
            "owner_processes": len(descendants),
            "tmux_sockets": len(sockets),
            "held_scheduler_locks": len(held_locks),
            "unreleased_leases": len(unresolved_leases),
            "unharvested_active_work": len(unharvested_work),
            "queue_files": queue_counts,
            "queue_inventory_sha256": queue_inventory_sha256,
            "queues_dispositioned": queues_dispositioned,
        }
        evidence = [str(runtime / "state/controller-state.json")]
        if marker_ambiguous:
            reasons.append(_reason("LEGACY_CRON_AMBIGUOUS", "admission", program,
                                   "remove_exact_predecessor_cron_marker", observed=marker_count))
        elif marker_count:
            reasons.append(_reason("LEGACY_CRON_PRESENT", "admission", program,
                                   "remove_exact_predecessor_cron_marker", observed=marker_count))
        if state_error:
            reasons.append(_reason("STATE_SCHEMA_INVALID", "runtime", program,
                                   "reconcile_predecessor_state", observed=state_error, evidence_refs=evidence))
        if reservation_error:
            reasons.append(_reason("STATE_SCHEMA_INVALID", "runtime", program,
                                   "reconcile_predecessor_reservations",
                                   observed=reservation_error, evidence_refs=evidence))
        if active_reservations:
            reasons.append(_reason(
                "LEGACY_RESERVATION_ACTIVE", "admission", program,
                "publish_explicit_reservation_disposition",
                observed=len(active_reservations), evidence_refs=evidence,
            ))
        for row in active_claims:
            reasons.append(_reason(
                "LEGACY_ACTIVE_CLAIM", "runtime", program, "harvest_and_terminalize_generation",
                item_id=row.get("item_id") if isinstance(row.get("item_id"), str) else None,
                generation_id=row.get("run_id") if isinstance(row.get("run_id"), str) else None,
                observed=row.get("status"), evidence_refs=evidence,
            ))
        if unknown_claims:
            reasons.append(_reason("STATE_UNKNOWN_STATUS", "runtime", program,
                                   "repair_unknown_lifecycle_status", observed=len(unknown_claims), evidence_refs=evidence))
        if controllers:
            reasons.append(_reason("LEGACY_CONTROLLER_PROCESS_LIVE", "admission", program,
                                   "stop_exact_predecessor_controller", observed=len(controllers)))
        if descendants:
            reasons.append(_reason("LEGACY_DESCENDANT_PROCESS_LIVE", "transport", program,
                                   "fence_owner_scoped_descendants", observed=len(descendants), evidence_refs=evidence))
        if sockets:
            reasons.append(_reason("LEGACY_TRANSPORT_LIVE", "transport", program,
                                   "fence_exact_task_local_tmux", observed=len(sockets), evidence_refs=evidence))
        if held_locks:
            reasons.append(_reason("LEGACY_CONTROLLER_LOCK_HELD", "admission", program,
                                   "release_predecessor_scheduler_lock", observed=held_locks))
        if lease_errors:
            reasons.append(_reason("LEASE_LEDGER_INVALID", "request", program,
                                   "repair_predecessor_lease_ledger", observed=lease_errors))
        if unresolved_leases:
            reasons.append(_reason("LEGACY_LEASE_UNRELEASED", "request", program,
                                   "publish_explicit_lease_release", observed=len(unresolved_leases)))
        for row in unharvested_work:
            reasons.append(_reason(
                "LEGACY_WORK_UNHARVESTED", "handoff", program,
                "publish_content_addressed_typed_checkpoint_before_fence",
                item_id=row["item_id"] or None, generation_id=row["generation_id"] or None,
                evidence_refs=evidence,
            ))
        if not queues_dispositioned:
            reasons.append(_reason("LEGACY_QUEUE_DISPOSITION_REQUIRED", "migration", program,
                                   "publish_queue_mapping_disposition", observed=queue_counts,
                                   evidence_refs=[str(FENCE_RECEIPT)]))
        clean = not any((marker_count, marker_ambiguous, state_error, reservation_error,
                         active_reservations, active_claims,
                         unknown_claims, controllers, descendants, sockets, held_locks,
                         lease_errors, unresolved_leases, unharvested_work,
                         not queues_dispositioned))
        predecessor_ready = predecessor_ready and clean

    observations["predecessors"] = predecessor_observations
    receipt_binding_error = None
    prompt_receipt_binding_error = None
    if predecessor_receipt is not None and materialization_valid:
        receipt_binding_error = _validate_predecessor_receipt_bindings(
            predecessor_receipt, pointer=pointer, crontab_text=crontab_text,
            prompt_observations=prompt_observations,
            runtime_observations=predecessor_observations,
            bind_prompts=False,
        )
        if receipt_binding_error:
            reasons.append(_reason(
                "PREDECESSOR_FENCE_RECEIPT_STALE", "migration", "predecessors",
                "repeat_independent_fence_review_against_current_snapshot",
                observed=receipt_binding_error,
                evidence_refs=[str(PREDECESSOR_FENCE_RECEIPT)],
            ))
        if receipt_binding_error is None:
            prompt_receipt_binding_error = _validate_predecessor_receipt_bindings(
                predecessor_receipt, pointer=pointer, crontab_text=crontab_text,
                prompt_observations=prompt_observations,
                runtime_observations=predecessor_observations,
                bind_prompts=True,
            )
            if prompt_receipt_binding_error:
                reasons.append(_reason(
                    "PREDECESSOR_FENCE_PROMPT_BINDING_STALE", "concurrency",
                    "predecessors", "repeat_prompt_bound_independent_review",
                    observed=prompt_receipt_binding_error,
                    evidence_refs=[str(PREDECESSOR_FENCE_RECEIPT)],
                ))
    effects = _successor_side_effects(root, crontab_text, process_rows, successor_contracts)
    observations["successor_side_effects"] = effects
    if effects:
        reasons.append(_reason(
            "ACTIVATION_SIDE_EFFECT_BEFORE_READY", "activation", "stage5.1-successor",
            "fence_successor_and_reconcile_overlap", observed=effects,
        ))
    controller_missing = []
    for program, contract in sorted(successor_contracts.items()):
        controller = _root_path(
            root, contract["controller_path"], f"{program} successor controller", required=False,
        )
        if not controller.is_file() or controller.is_symlink():
            controller_missing.append(program)
            reasons.append(_reason(
                "STAGE51_CONTROLLER_MISSING", "activation", program,
                "implement_and_validate_successor_controller",
                evidence_refs=[contract["controller_path"]],
            ))

    all_prompts = materialization_valid and all(prompt_valid.get(program, False) for program in PROGRAMS)
    all_boots = materialization_valid and all(boot_accepted.values())
    ready_for_boot = (materialization_valid and predecessor_ready
                      and predecessor_receipt is not None
                      and receipt_binding_error is None
                      and not effects)
    ready_for_member = (ready_for_boot and all_prompts and all_boots
                        and prompt_receipt_binding_error is None
                        and activation_receipt is not None and not controller_missing)
    if materialization_valid and not all_boots:
        for program, accepted in sorted(boot_accepted.items()):
            if not accepted:
                reasons.append(_reason(
                    "STAGE51_BOOT_NOT_ACCEPTED", "acceptance", program,
                    "independently_review_and_accept_new_boot",
                    evidence_refs=[str(PROGRAMS[program]["blueprint"])],
                ))
    if activation_receipt is None:
        reasons.append(_reason(
            "ACTIVATION_FENCE_RECEIPT_REQUIRED", "activation", "stage5.1",
            "accept_post_boot_activation_fence",
            evidence_refs=[str(FENCE_RECEIPT)],
        ))

    axes = {
        "materialization_valid": materialization_valid,
        "ready_for_boot_reacceptance": ready_for_boot,
        "ready_for_member_admission": ready_for_member,
    }
    checks.update({name: {"passed": value} for name, value in axes.items()})
    observations["axes"] = axes
    selected = {
        "materialization": materialization_valid,
        "boot": ready_for_boot,
        "member": ready_for_member,
    }[phase]
    invalid = not materialization_valid or any(
        reason["code"] in {"OBSERVATION_FAILED", "STATE_SCHEMA_INVALID", "STATE_UNKNOWN_STATUS",
                           "LEASE_LEDGER_INVALID", "PREDECESSOR_FENCE_RECEIPT_INVALID",
                           "ACTIVATION_FENCE_RECEIPT_INVALID"}
        for reason in reasons
    )
    status = "ready" if selected else ("invalid" if invalid else "blocked")
    relevant_reasons = [] if selected else sorted(reasons, key=_reason_key)
    # A materialization-only success still exposes later blockers under
    # observations, but its verdict is intentionally scoped to that phase.
    if phase == "materialization" and selected:
        relevant_reasons = []
    return {
        "schema_version": REPORT_SCHEMA,
        "status": status,
        "ready": bool(selected),
        "phase": phase,
        "axes": axes,
        "reasons": relevant_reasons,
        "checks": checks,
        "observations": observations,
    }


def _render_check(report: Mapping[str, Any]) -> str:
    lines = [
        f"stage5.1 activation fence: {report['status']} (phase={report['phase']})",
        "axes: " + ", ".join(
            f"{key}={'yes' if value else 'no'}" for key, value in report["axes"].items()
        ),
    ]
    for reason in report["reasons"]:
        suffix = ""
        if reason.get("item_id"):
            suffix += f" item={reason['item_id']}"
        if reason.get("generation_id"):
            suffix += f" generation={reason['generation_id']}"
        lines.append(f"- {reason['code']} [{reason['scope']}]{suffix}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="print a compact human-readable snapshot")
    mode.add_argument("--json", action="store_true", help="print the complete machine-readable snapshot")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--phase", choices=("materialization", "boot", "member"), default="member")
    args = parser.parse_args(argv)
    try:
        report = evaluate(args.root, phase=args.phase)
    except Exception as exc:  # Last-resort fail-closed CLI envelope.
        report = {
            "schema_version": REPORT_SCHEMA, "status": "invalid", "ready": False,
            "phase": args.phase,
            "axes": {"materialization_valid": False,
                     "ready_for_boot_reacceptance": False,
                     "ready_for_member_admission": False},
            "reasons": [_reason("OBSERVATION_FAILED", "checker", "internal",
                                "repair_checker_or_observation", observed=str(exc))],
            "checks": {}, "observations": {"requested_phase": args.phase},
        }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    else:
        print(_render_check(report))
    return 0 if report["ready"] is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
