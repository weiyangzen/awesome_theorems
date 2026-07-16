#!/usr/bin/env python3
"""Fail-closed, scheduler-owned adaptation of Stage1 validator output.

The adapter is deliberately separate from target-owned validators.  A phase
may use an adapter only when its authoritative contract row contains an exact
``semantic_adapter_profile`` declaration.  The current v1.0 contract has no
such declarations, so every current legacy validator produces a typed
unsupported result rather than an inferred acceptance.

This first adapter version intentionally has no positive legacy profile.  Its
only legacy profile preserves negative evidence while returning
``phase_accepted: false``.  A future positive profile must be added to the
scheduler-owned registry together with independent semantic-gate
implementations; exit zero, ``PASS`` prose, and target-owned booleans are not
such implementations.
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Mapping, NoReturn, Sequence


ADAPTER_RECEIPT_SCHEMA = "stage1-validator-adapter-receipt/1.0"
SEMANTIC_RESULT_SCHEMA = "stage1-validator-semantic-result/1.0"
LEGACY_NEGATIVE_ONLY_PROFILE = "stage1-legacy-negative-only/1.0"
PROFILE_OWNER = "scheduler_master_lane"
PROFILE_FIELD = "semantic_adapter_profile"
MAX_OUTPUT_BYTES = 16 * 1024 * 1024

ITEM_RE = re.compile(r"^S56-M-([0-9]{4})-([A-Z_]+)$")
THEOREM_RE = re.compile(r"^THM-M-([0-9]{4})$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
PHASE_SUFFIXES = {
    "intake": "INTAKE",
    "statement": "STATEMENT",
    "anchor_audit": "ANCHOR_AUDIT",
    "obligation_tree": "OBLIGATION_TREE",
    "proof": "PROOF",
    "validation": "VALIDATION",
    "release": "RELEASE",
}
NEGATIVE_WORD_RE = re.compile(
    r"\b(blocked|blocking|failed|failure|open|rejected|revoked|stale|"
    r"superseded|timeout|timed_out)\b",
    re.IGNORECASE,
)

# This descriptor is hashed into every receipt.  The module hash binds the
# actual implementation; this descriptor makes the intended capability
# explicit to downstream verifiers.
PROFILE_REGISTRY: dict[str, dict[str, Any]] = {
    LEGACY_NEGATIVE_ONLY_PROFILE: {
        "mode": "negative_evidence_preservation_only",
        "positive_acceptance_capable": False,
        "positive_evidence_source": None,
    }
}


class AdapterError(RuntimeError):
    """The adapter input or content binding is malformed."""


def _fail(message: str) -> NoReturn:
    raise AdapterError(message)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob_oid(value: bytes, *, algorithm: str = "sha1") -> str:
    """Return the Git blob object ID for ``value`` using SHA-1 or SHA-256."""

    if algorithm not in {"sha1", "sha256"}:
        _fail("Git blob algorithm must be sha1 or sha256")
    framed = f"blob {len(value)}\0".encode("ascii") + value
    return hashlib.new(algorithm, framed).hexdigest()


def _strict_json_object(value: bytes, label: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, child in pairs:
            if key in result:
                _fail(f"{label} contains duplicate key {key!r}")
            result[key] = child
        return result

    try:
        parsed = json.loads(
            value.decode("utf-8"), object_pairs_hook=reject_duplicates
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdapterError(f"{label} is not one UTF-8 JSON object") from exc
    if not isinstance(parsed, dict):
        _fail(f"{label} must be a JSON object")
    return parsed


def _safe_relative(value: str, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        _fail(f"{label} is malformed")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or str(pure) != value:
        _fail(f"{label} is not a canonical repository-relative path")
    return value


def _require_git_blob(value: bytes, oid: str, label: str) -> None:
    if not isinstance(oid, str) or not GIT_OID_RE.fullmatch(oid):
        _fail(f"{label} Git blob is malformed")
    algorithm = "sha1" if len(oid) == 40 else "sha256"
    if git_blob_oid(value, algorithm=algorithm) != oid:
        _fail(f"{label} Git blob does not bind the supplied bytes")


def _require_identity(item_id: str, theorem_id: str, phase: str) -> None:
    item = ITEM_RE.fullmatch(item_id) if isinstance(item_id, str) else None
    theorem = THEOREM_RE.fullmatch(theorem_id) if isinstance(theorem_id, str) else None
    if item is None or theorem is None or phase not in PHASE_SUFFIXES:
        _fail("adapter item identity is malformed")
    if item.group(1) != theorem.group(1) or item.group(2) != PHASE_SUFFIXES[phase]:
        _fail("adapter item, theorem, and phase disagree")


def _phase_row(contract: Mapping[str, Any], phase: str) -> dict[str, Any]:
    rows = contract.get("phases")
    if not isinstance(rows, list):
        _fail("contract phases must be a list")
    matches = [row for row in rows if isinstance(row, dict) and row.get("phase") == phase]
    if len(matches) != 1:
        _fail("contract must contain exactly one row for the adapted phase")
    return dict(matches[0])


def _profile_declaration(phase_row: Mapping[str, Any]) -> dict[str, Any]:
    declared = PROFILE_FIELD in phase_row
    raw = phase_row.get(PROFILE_FIELD)
    required = {"profile_id", "owner", "output_schema"}
    valid = (
        isinstance(raw, dict)
        and set(raw) == required
        and isinstance(raw.get("profile_id"), str)
        and bool(raw.get("profile_id"))
        and raw.get("owner") == PROFILE_OWNER
        and raw.get("output_schema") == SEMANTIC_RESULT_SCHEMA
    )
    profile_id = raw.get("profile_id") if isinstance(raw, dict) else None
    supported = bool(valid and profile_id in PROFILE_REGISTRY)
    if not declared:
        reason = "phase_adapter_profile_not_declared"
    elif not valid:
        reason = "phase_adapter_profile_malformed"
    elif not supported:
        reason = "phase_adapter_profile_not_implemented"
    else:
        reason = None
    descriptor = PROFILE_REGISTRY.get(str(profile_id)) if supported else None
    return {
        "declared": declared,
        "valid_declaration": valid,
        "supported": supported,
        "profile_id": profile_id,
        "owner": raw.get("owner") if isinstance(raw, dict) else None,
        "output_schema": raw.get("output_schema") if isinstance(raw, dict) else None,
        "profile_implementation_sha256": (
            sha256_bytes(canonical_json(descriptor)) if descriptor is not None else None
        ),
        "reason": reason,
    }


def _tolerant_json(value: bytes) -> Any | None:
    try:
        return json.loads(value.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _collect_negative_values(value: Any, result: dict[str, Any]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized == "blocked" and child is True:
                result["blocked"] = True
                result["tokens"].add("blocked")
            elif normalized in {"status", "verdict", "result", "state"} and isinstance(child, str):
                result["tokens"].update(
                    token.lower() for token in NEGATIVE_WORD_RE.findall(child)
                )
            elif normalized in {"open_obligations", "open_goals", "open_count"}:
                if isinstance(child, int) and not isinstance(child, bool) and child > 0:
                    result["open_obligations"] = max(result["open_obligations"], child)
                    result["tokens"].add("open")
                elif isinstance(child, list) and child:
                    result["open_obligations"] = max(result["open_obligations"], len(child))
                    result["tokens"].add("open")
            elif normalized in {"stale_inputs", "stale_paths"}:
                if isinstance(child, str) and child:
                    result["stale_inputs"].add(child)
                    result["tokens"].add("stale")
                elif isinstance(child, list):
                    strings = {entry for entry in child if isinstance(entry, str) and entry}
                    if strings:
                        result["stale_inputs"].update(strings)
                        result["tokens"].add("stale")
            elif normalized == "first_failed_gate" and child not in {None, ""}:
                result["tokens"].add("failed")
            _collect_negative_values(child, result)
    elif isinstance(value, list):
        for child in value:
            _collect_negative_values(child, result)
    elif isinstance(value, str):
        result["tokens"].update(
            token.lower() for token in NEGATIVE_WORD_RE.findall(value)
        )


def _negative_signals(
    stdout: bytes,
    stderr: bytes,
    *,
    exit_code: int | None,
    timed_out: bool,
) -> dict[str, Any]:
    mutable: dict[str, Any] = {
        "tokens": set(),
        "blocked": False,
        "open_obligations": 0,
        "stale_inputs": set(),
    }
    parsed_stdout = _tolerant_json(stdout)
    if parsed_stdout is None:
        mutable["tokens"].update(
            token.lower()
            for token in NEGATIVE_WORD_RE.findall(stdout.decode("utf-8", "replace"))
        )
    else:
        _collect_negative_values(parsed_stdout, mutable)
    parsed_stderr = _tolerant_json(stderr)
    if parsed_stderr is None:
        mutable["tokens"].update(
            token.lower()
            for token in NEGATIVE_WORD_RE.findall(stderr.decode("utf-8", "replace"))
        )
    else:
        _collect_negative_values(parsed_stderr, mutable)
    if timed_out:
        mutable["tokens"].add("timeout")
    if exit_code not in {None, 0}:
        mutable["tokens"].add("failed")
    if "blocked" in mutable["tokens"] or "blocking" in mutable["tokens"]:
        mutable["blocked"] = True
    if "open" in mutable["tokens"] and mutable["open_obligations"] == 0:
        mutable["open_obligations"] = 1
    if "stale" in mutable["tokens"] and not mutable["stale_inputs"]:
        mutable["stale_inputs"].add("legacy-output-reported-stale")
    return {
        "tokens": sorted(mutable["tokens"]),
        "blocked": mutable["blocked"],
        "open_obligations": mutable["open_obligations"],
        "stale_inputs": sorted(mutable["stale_inputs"]),
        "nonzero_exit": exit_code not in {None, 0},
        "timed_out": timed_out,
    }


def _negative_semantic_result(
    *,
    item_id: str,
    theorem_id: str,
    phase: str,
    signals: Mapping[str, Any],
    unsupported: bool,
) -> dict[str, Any]:
    tokens = set(signals.get("tokens", []))
    if signals.get("blocked"):
        status, verdict, gate = "blocked", "blocked", "ADAPTER-LEGACY-BLOCKED"
    elif signals.get("timed_out") or "timeout" in tokens or "timed_out" in tokens:
        status, verdict, gate = "failed", "repair_required", "ADAPTER-REPLAY-TIMEOUT"
    elif signals.get("stale_inputs") or tokens & {"stale", "superseded", "revoked"}:
        status, verdict, gate = "stale", "repair_required", "ADAPTER-LEGACY-STALE"
    elif signals.get("open_obligations") or "open" in tokens:
        status, verdict, gate = "open", "repair_required", "ADAPTER-LEGACY-OPEN"
    elif signals.get("nonzero_exit") or tokens & {"failed", "failure"}:
        status, verdict, gate = "failed", "repair_required", "ADAPTER-LEGACY-FAILED"
    elif "rejected" in tokens:
        status, verdict, gate = "rejected", "rejected", "ADAPTER-LEGACY-REJECTED"
    elif unsupported:
        status, verdict, gate = "rejected", "repair_required", "ADAPTER-PROFILE-UNSUPPORTED"
    else:
        status, verdict, gate = (
            "rejected",
            "repair_required",
            "ADAPTER-POSITIVE-PROOF-UNAVAILABLE",
        )
    message = (
        "No contract-declared scheduler adapter is available for this phase."
        if unsupported
        else "The declared legacy adapter preserves negatives but cannot prove phase acceptance."
    )
    return {
        "schema_version": SEMANTIC_RESULT_SCHEMA,
        "item_id": item_id,
        "theorem_id": theorem_id,
        "phase": phase,
        "status": status,
        "verdict": verdict,
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": gate,
        "open_obligations": int(signals.get("open_obligations", 0)),
        "stale_inputs": list(signals.get("stale_inputs", [])),
        "blocked": bool(signals.get("blocked")),
        "message": message,
    }


def _module_sha256() -> str:
    return sha256_bytes(Path(__file__).resolve().read_bytes())


def _receipt_digest(receipt: Mapping[str, Any]) -> str:
    body = dict(receipt)
    body.pop("receipt_sha256", None)
    return sha256_bytes(canonical_json(body))


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        _fail(f"{label} fields are not exact")


def verify_adapter_receipt(receipt: Mapping[str, Any]) -> None:
    """Verify the receipt's content address and embedded complete outputs."""

    _require_exact_keys(
        receipt,
        {
            "schema_version",
            "item_id",
            "theorem_id",
            "phase",
            "contract",
            "adapter",
            "validator",
            "invocation",
            "output",
            "negative_signals",
            "semantic_result",
            "semantic_result_sha256",
            "receipt_sha256",
        },
        "adapter receipt",
    )
    if receipt.get("schema_version") != ADAPTER_RECEIPT_SCHEMA:
        _fail("adapter receipt schema is unsupported")
    _require_identity(
        receipt.get("item_id"), receipt.get("theorem_id"), receipt.get("phase")
    )
    digest = receipt.get("receipt_sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        _fail("adapter receipt digest is malformed")
    if _receipt_digest(receipt) != digest:
        _fail("adapter receipt digest does not bind its content")
    contract = receipt.get("contract")
    if not isinstance(contract, dict):
        _fail("adapter receipt contract binding is malformed")
    _require_exact_keys(
        contract, {"schema_version", "sha256", "git_blob"}, "contract binding"
    )
    if (
        not isinstance(contract.get("schema_version"), str)
        or not isinstance(contract.get("sha256"), str)
        or not SHA256_RE.fullmatch(contract["sha256"])
        or not isinstance(contract.get("git_blob"), str)
        or not GIT_OID_RE.fullmatch(contract["git_blob"])
    ):
        _fail("adapter receipt contract binding is malformed")
    adapter_binding = receipt.get("adapter")
    if not isinstance(adapter_binding, dict):
        _fail("adapter receipt implementation binding is malformed")
    _require_exact_keys(
        adapter_binding,
        {
            "declared",
            "valid_declaration",
            "supported",
            "profile_id",
            "owner",
            "output_schema",
            "profile_implementation_sha256",
            "reason",
            "module_sha256",
        },
        "adapter implementation binding",
    )
    if (
        not isinstance(adapter_binding.get("module_sha256"), str)
        or not SHA256_RE.fullmatch(adapter_binding["module_sha256"])
    ):
        _fail("adapter receipt module digest is malformed")
    validator = receipt.get("validator")
    if not isinstance(validator, dict):
        _fail("adapter receipt validator binding is malformed")
    _require_exact_keys(
        validator, {"path", "sha256", "git_blob"}, "validator binding"
    )
    _safe_relative(validator.get("path"), "validator path")
    if (
        not isinstance(validator.get("sha256"), str)
        or not SHA256_RE.fullmatch(validator["sha256"])
        or not isinstance(validator.get("git_blob"), str)
        or not GIT_OID_RE.fullmatch(validator["git_blob"])
    ):
        _fail("adapter receipt validator binding is malformed")
    invocation = receipt.get("invocation")
    if not isinstance(invocation, dict):
        _fail("adapter receipt invocation binding is malformed")
    _require_exact_keys(
        invocation, {"argv", "exit_code", "timed_out", "shell"}, "invocation binding"
    )
    argv = invocation.get("argv")
    if (
        not isinstance(argv, list)
        or not argv
        or any(not isinstance(part, str) or "\x00" in part for part in argv)
        or invocation.get("shell") is not False
        or not isinstance(invocation.get("timed_out"), bool)
    ):
        _fail("adapter receipt invocation binding is malformed")
    exit_code = invocation.get("exit_code")
    if invocation["timed_out"]:
        if exit_code is not None:
            _fail("adapter receipt timeout binding is malformed")
    elif not isinstance(exit_code, int) or isinstance(exit_code, bool):
        _fail("adapter receipt exit binding is malformed")
    output = receipt.get("output")
    if not isinstance(output, dict):
        _fail("adapter receipt output binding is malformed")
    _require_exact_keys(
        output,
        {
            "stdout_base64",
            "stdout_sha256",
            "stdout_size",
            "stdout_complete",
            "stderr_base64",
            "stderr_sha256",
            "stderr_size",
            "stderr_complete",
        },
        "output binding",
    )
    for stream in ("stdout", "stderr"):
        if output.get(f"{stream}_complete") is not True:
            _fail(f"adapter receipt {stream} is incomplete")
        encoded = output.get(f"{stream}_base64")
        if not isinstance(encoded, str):
            _fail(f"adapter receipt {stream} base64 is malformed")
        try:
            raw = base64.b64decode(encoded, validate=True)
        except ValueError as exc:
            raise AdapterError(f"adapter receipt {stream} base64 is malformed") from exc
        if (
            len(raw) != output.get(f"{stream}_size")
            or sha256_bytes(raw) != output.get(f"{stream}_sha256")
        ):
            _fail(f"adapter receipt {stream} binding is stale")
    semantic = receipt.get("semantic_result")
    if not isinstance(semantic, dict):
        _fail("adapter receipt semantic result is malformed")
    _require_exact_keys(
        semantic,
        {
            "schema_version",
            "item_id",
            "theorem_id",
            "phase",
            "status",
            "verdict",
            "phase_accepted",
            "audit_complete",
            "theorem_complete",
            "phase_predicate_proven",
            "first_failed_gate",
            "open_obligations",
            "stale_inputs",
            "blocked",
            "message",
        },
        "adapter semantic result",
    )
    if (
        semantic.get("schema_version") != SEMANTIC_RESULT_SCHEMA
        or semantic.get("item_id") != receipt.get("item_id")
        or semantic.get("theorem_id") != receipt.get("theorem_id")
        or semantic.get("phase") != receipt.get("phase")
        or semantic.get("phase_accepted") is not False
        or semantic.get("phase_predicate_proven") is not False
    ):
        _fail("adapter receipt semantic result is not fail-closed or identity-bound")
    if sha256_bytes(canonical_json(semantic)) != receipt.get("semantic_result_sha256"):
        _fail("adapter receipt semantic result binding is stale")


def adapt_validator_result(
    *,
    contract_bytes: bytes,
    contract_sha256: str,
    contract_git_blob: str,
    item_id: str,
    theorem_id: str,
    phase: str,
    validator_path: str,
    validator_bytes: bytes,
    validator_git_blob: str,
    argv: Sequence[str],
    exit_code: int | None,
    timed_out: bool,
    stdout: bytes,
    stderr: bytes,
    stdout_complete: bool = True,
    stderr_complete: bool = True,
) -> dict[str, Any]:
    """Adapt one complete validator observation into a content-bound receipt.

    Unsupported or negative semantics are normal typed results.  Malformed
    identities, blobs, digests, argv, or incomplete output raise
    :class:`AdapterError` because no trustworthy receipt can be constructed.
    """

    for value, label in (
        (contract_bytes, "contract bytes"),
        (validator_bytes, "validator bytes"),
        (stdout, "validator stdout"),
        (stderr, "validator stderr"),
    ):
        if not isinstance(value, bytes):
            _fail(f"{label} must be bytes")
    if not isinstance(contract_sha256, str) or not SHA256_RE.fullmatch(contract_sha256):
        _fail("contract SHA-256 is malformed")
    if sha256_bytes(contract_bytes) != contract_sha256:
        _fail("contract SHA-256 does not bind the supplied bytes")
    _require_git_blob(contract_bytes, contract_git_blob, "contract")
    _require_git_blob(validator_bytes, validator_git_blob, "validator")
    _require_identity(item_id, theorem_id, phase)
    relative_validator = _safe_relative(validator_path, "validator path")
    if (
        not isinstance(argv, Sequence)
        or isinstance(argv, (str, bytes))
        or not argv
        or any(not isinstance(part, str) or "\x00" in part for part in argv)
    ):
        _fail("validator argv is malformed")
    if not isinstance(timed_out, bool):
        _fail("validator timeout flag must be boolean")
    if timed_out:
        if exit_code is not None:
            _fail("timed-out validator must have a null exit code")
    elif not isinstance(exit_code, int) or isinstance(exit_code, bool):
        _fail("completed validator must have an integer exit code")
    if stdout_complete is not True or stderr_complete is not True:
        _fail("adapter requires complete stdout and stderr")
    if len(stdout) > MAX_OUTPUT_BYTES or len(stderr) > MAX_OUTPUT_BYTES:
        _fail("validator output exceeds the complete-output limit")

    contract = _strict_json_object(contract_bytes, "acceptance contract")
    phase_row = _phase_row(contract, phase)
    profile = _profile_declaration(phase_row)
    signals = _negative_signals(
        stdout, stderr, exit_code=exit_code, timed_out=timed_out
    )
    supported = profile["supported"] is True
    semantic = _negative_semantic_result(
        item_id=item_id,
        theorem_id=theorem_id,
        phase=phase,
        signals=signals,
        unsupported=not supported,
    )
    output = {
        "stdout_base64": base64.b64encode(stdout).decode("ascii"),
        "stdout_sha256": sha256_bytes(stdout),
        "stdout_size": len(stdout),
        "stdout_complete": True,
        "stderr_base64": base64.b64encode(stderr).decode("ascii"),
        "stderr_sha256": sha256_bytes(stderr),
        "stderr_size": len(stderr),
        "stderr_complete": True,
    }
    receipt: dict[str, Any] = {
        "schema_version": ADAPTER_RECEIPT_SCHEMA,
        "item_id": item_id,
        "theorem_id": theorem_id,
        "phase": phase,
        "contract": {
            "schema_version": contract.get("schema_version"),
            "sha256": contract_sha256,
            "git_blob": contract_git_blob,
        },
        "adapter": {
            **profile,
            "module_sha256": _module_sha256(),
        },
        "validator": {
            "path": relative_validator,
            "sha256": sha256_bytes(validator_bytes),
            "git_blob": validator_git_blob,
        },
        "invocation": {
            "argv": list(argv),
            "exit_code": exit_code,
            "timed_out": timed_out,
            "shell": False,
        },
        "output": output,
        "negative_signals": signals,
        "semantic_result": semantic,
        "semantic_result_sha256": sha256_bytes(canonical_json(semantic)),
    }
    receipt["receipt_sha256"] = _receipt_digest(receipt)
    verify_adapter_receipt(receipt)
    return receipt


__all__ = [
    "ADAPTER_RECEIPT_SCHEMA",
    "AdapterError",
    "LEGACY_NEGATIVE_ONLY_PROFILE",
    "PROFILE_FIELD",
    "PROFILE_OWNER",
    "SEMANTIC_RESULT_SCHEMA",
    "adapt_validator_result",
    "canonical_json",
    "git_blob_oid",
    "sha256_bytes",
    "verify_adapter_receipt",
]
