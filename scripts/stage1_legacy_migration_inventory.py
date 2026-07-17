#!/usr/bin/env python3
"""Build a read-only migration inventory for legacy Stage1 ``[_]`` items.

The inventory is evidence for planning migration, never acceptance evidence. It
reads repository bytes from Git, does not execute validators, and deliberately
uses ``unknown`` whenever runtime semantics cannot be proved statically.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from typing import Any, Iterable, NoReturn


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_PATH = "Docs/Stage1_Blueprint_v2.md"
CONTRACT_PATH = "Docs/Stage1_Phase_Acceptance_Contracts.json"
INVENTORY_SCHEMA = "stage1-legacy-migration-inventory/1.0"
ITEM_SCHEMA = "stage1-legacy-migration-item/1.0"
SEMANTIC_SCHEMA = "stage1-validator-semantic-result/1.0"
RECEIPT_SCHEMA = "stage1-node-receipt/1.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OID_RE = re.compile(r"^[0-9a-f]{40,64}$")
ITEM_RE = re.compile(
    r"^- \[_\] `(?P<item>S56-M-[0-9]{4}-(?P<suffix>[A-Z_]+))` / "
    r"`(?P<theorem>THM-M-[0-9]{4})` / `(?P<phase>[a-z_]+)`:"
    r".*?\{attempts=(?P<attempts>[0-9]+)\}$",
    re.MULTILINE,
)
CLASSIFICATIONS = (
    "missing_receipt",
    "legacy_receipt",
    "phase_mismatch",
    "missing_or_ambiguous_role",
    "validator_authority_superseded",
    "validator_base_mismatch",
    "validator_stdout_mismatch",
    "sandbox_incompatible",
)
STATUS = {"blocked", "clear", "unknown"}


class InventoryError(RuntimeError):
    """Repository authority cannot support a trustworthy inventory."""


def fail(message: str) -> NoReturn:
    raise InventoryError(message)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_git(
    root: Path, argv: Iterable[str], *, check: bool = True
) -> subprocess.CompletedProcess[bytes]:
    command = ["git", *argv]
    result = subprocess.run(
        command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        fail(
            f"git {' '.join(argv)} failed: "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result


def git_text(root: Path, *argv: str) -> str:
    return run_git(root, argv).stdout.decode("utf-8", "strict").strip()


def safe_relative(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        fail(f"{label} is not a repository-relative POSIX path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or path.as_posix() != value
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail(f"{label} is not a canonical repository-relative POSIX path")
    return value


def strict_json(data: bytes, label: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InventoryError(f"{label} is not strict UTF-8 JSON") from exc
    if not isinstance(value, dict):
        fail(f"{label} must contain one JSON object")
    return value


@dataclass(frozen=True)
class GitBlob:
    path: str
    oid: str
    sha256: str
    size: int
    mode: str
    data: bytes

    def binding(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "git_blob": self.oid,
            "sha256": self.sha256,
            "size": self.size,
            "git_mode": self.mode,
        }


class HeadReader:
    """Read immutable blobs from one resolved commit, with a small object cache."""

    def __init__(self, root: Path, revision: str = "HEAD") -> None:
        self.root = root.resolve()
        self.revision = git_text(self.root, "rev-parse", "--verify", f"{revision}^{{commit}}")
        self.tree = git_text(self.root, "rev-parse", f"{self.revision}^{{tree}}")
        self._cache: dict[str, GitBlob | None] = {}
        listing = run_git(
            self.root,
            ["ls-tree", "-r", "-z", self.revision, "--", "Stage1_Instances", "Docs"],
        ).stdout
        self._entries: dict[str, tuple[str, str]] = {}
        for raw in listing.split(b"\0"):
            if not raw:
                continue
            metadata, path_bytes = raw.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            if kind == "blob":
                self._entries[path_bytes.decode("utf-8", "strict")] = (mode, oid)

    def blob(self, relative: str) -> GitBlob | None:
        relative = safe_relative(relative, "Git blob path")
        if relative in self._cache:
            return self._cache[relative]
        entry = self._entries.get(relative)
        if entry is None:
            self._cache[relative] = None
            return None
        mode, oid = entry
        if mode not in {"100644", "100755"} or not OID_RE.fullmatch(oid):
            fail(f"HEAD path has an unsafe mode or object identity: {relative}")
        data = run_git(self.root, ["cat-file", "blob", oid]).stdout
        blob = GitBlob(relative, oid, sha256_bytes(data), len(data), mode, data)
        self._cache[relative] = blob
        return blob

    def blob_at(self, revision: str, relative: str) -> tuple[str, bytes] | None:
        if not isinstance(revision, str) or not OID_RE.fullmatch(revision):
            return None
        result = run_git(
            self.root,
            ["rev-parse", "--verify", f"{revision}:{safe_relative(relative, 'base blob path')}"] ,
            check=False,
        )
        if result.returncode:
            return None
        oid = result.stdout.decode("ascii", "strict").strip()
        if not OID_RE.fullmatch(oid):
            return None
        return oid, run_git(self.root, ["cat-file", "blob", oid]).stdout


def classification(
    name: str, status: str, reasons: list[str], bindings: list[dict[str, Any]]
) -> dict[str, Any]:
    if name not in CLASSIFICATIONS or status not in STATUS:
        fail("internal classification vocabulary error")
    if status == "clear" and reasons:
        fail("a clear classification cannot contain blockers")
    if status != "clear" and not reasons:
        fail("a non-clear classification must explain its boundary")
    return {
        "category": name,
        "status": status,
        "reasons": reasons,
        "bindings": bindings,
    }


def render(pattern: str, theorem_id: str, label: str) -> str:
    if not isinstance(pattern, str):
        fail(f"{label} pattern is malformed")
    value = pattern.replace("{theorem_id}", theorem_id)
    if "{" in value or "}" in value:
        fail(f"{label} has unresolved placeholders")
    return safe_relative(value, label)


MISSING_POINTER = object()


def pointer_value(document: dict[str, Any], pointer: Any) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        return MISSING_POINTER
    value: Any = document
    for raw in pointer[1:].split("/"):
        component = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict) and component in value:
            value = value[component]
        else:
            return MISSING_POINTER
    return value


def receipt_bound_paths(value: Any) -> list[str] | None:
    rows = value if isinstance(value, list) else [value]
    if not rows or any(not isinstance(row, dict) for row in rows):
        return None
    paths: list[str] = []
    for row in rows:
        if set(row) - {"path", "sha256", "git_blob", "role", "kind", "artifact_kind"}:
            return None
        try:
            relative = safe_relative(row.get("path"), "receipt-bound path")
        except InventoryError:
            return None
        digest = row.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            return None
        paths.append(relative)
    return paths if len(paths) == len(set(paths)) else None


def static_sandbox_findings(blob: GitBlob) -> tuple[list[str], list[str]]:
    text = blob.data.decode("utf-8", "replace")
    blocked: list[str] = []
    unknown: list[str] = []
    if re.search(
        r"NamedTemporaryFile\s*\([^)]*dir\s*=\s*(?:SOURCE|HERE|[^)]*\.parent)",
        text,
        re.DOTALL,
    ):
        blocked.append("validator creates a temporary file under the read-only repository")
    if re.search(
        r"(?:Path\([^\n]+\)|\b(?:SOURCE|HERE|ROOT)[^\n]*)\.write_(?:text|bytes)\s*\(",
        text,
    ):
        blocked.append("validator statically writes through a repository-derived path")
    if re.search(r"\b(?:lake|lean|elan)\b|\.lake|\.elan", text):
        unknown.append("validator references Lean/elan or .lake; authority-owned mounts need runtime proof")
    if re.search(r"\b(?:subprocess\.(?:run|check_output|Popen)|os\.system)\b", text):
        unknown.append("validator launches subprocesses; the closed runtime mount set needs execution proof")
    if re.search(r"https?://|\b(?:curl|wget)\b|requests\.", text):
        unknown.append("validator contains a network reference or client; denied-network behavior needs proof")
    return sorted(set(blocked)), sorted(set(unknown))


def inventory_item(
    reader: HeadReader,
    contract: dict[str, Any],
    contract_binding: dict[str, Any],
    blueprint_binding: dict[str, Any],
    row: dict[str, Any],
) -> dict[str, Any]:
    phase_rows = [
        value
        for value in contract.get("phases", [])
        if isinstance(value, dict) and value.get("phase") == row["phase"]
    ]
    if len(phase_rows) != 1:
        fail(f"contract lacks exactly one phase row for {row['phase']}")
    phase_contract = phase_rows[0]
    suffix = phase_contract.get("item_suffix")
    if suffix != row["suffix"]:
        fail(f"blueprint item suffix disagrees with contract: {row['item']}")

    receipt_roles = [
        role
        for role in phase_contract.get("required_artifact_roles", [])
        if isinstance(role, dict) and role.get("role") == "phase_receipt"
    ]
    if len(receipt_roles) != 1:
        fail(f"contract lacks exactly one receipt role for {row['phase']}")
    receipt_candidates: list[GitBlob] = []
    for pattern in receipt_roles[0].get("path_candidates", []):
        blob = reader.blob(render(pattern, row["theorem"], "receipt candidate"))
        if blob is not None:
            receipt_candidates.append(blob)

    classes: dict[str, dict[str, Any]] = {}
    receipt: dict[str, Any] | None = None
    receipt_binding = [blob.binding() for blob in receipt_candidates]
    if not receipt_candidates:
        classes["missing_receipt"] = classification(
            "missing_receipt", "blocked", ["no HEAD receipt candidate exists"], []
        )
    elif len(receipt_candidates) > 1:
        classes["missing_receipt"] = classification(
            "missing_receipt",
            "blocked",
            ["multiple receipt aliases exist; scheduler cannot select one"],
            receipt_binding,
        )
    else:
        classes["missing_receipt"] = classification("missing_receipt", "clear", [], receipt_binding)
        try:
            receipt = strict_json(receipt_candidates[0].data, "phase receipt")
        except InventoryError as exc:
            classes["legacy_receipt"] = classification(
                "legacy_receipt", "blocked", [str(exc)], receipt_binding
            )

    required_receipt_fields = phase_contract.get("phase_receipt_required_fields", [])
    if receipt is None and "legacy_receipt" not in classes:
        classes["legacy_receipt"] = classification(
            "legacy_receipt",
            "unknown",
            ["receipt content is unavailable because receipt selection failed"],
            receipt_binding,
        )
    elif receipt is not None:
        missing = [
            pointer
            for pointer in required_receipt_fields
            if pointer_value(receipt, pointer) is MISSING_POINTER
        ]
        reasons: list[str] = []
        if receipt.get("schema_version") != RECEIPT_SCHEMA:
            reasons.append("receipt schema is not stage1-node-receipt/1.0")
        if missing:
            reasons.append("missing required pointers: " + ",".join(sorted(missing)))
        classes["legacy_receipt"] = classification(
            "legacy_receipt", "blocked" if reasons else "clear", reasons, receipt_binding
        )

    if receipt is None:
        classes["phase_mismatch"] = classification(
            "phase_mismatch",
            "unknown",
            ["receipt identity cannot be inspected"],
            receipt_binding,
        )
    else:
        mismatches = [
            field
            for field, expected in (
                ("item_id", row["item"]),
                ("theorem_id", row["theorem"]),
                ("phase", row["phase"]),
            )
            if receipt.get(field) != expected
        ]
        classes["phase_mismatch"] = classification(
            "phase_mismatch",
            "blocked" if mismatches else "clear",
            ["receipt identity mismatch: " + ",".join(mismatches)] if mismatches else [],
            receipt_binding,
        )

    selected_role_bindings: list[dict[str, Any]] = []
    role_reasons: list[str] = []
    role_unknown: list[str] = []
    for role in phase_contract.get("required_artifact_roles", []):
        if not isinstance(role, dict):
            role_reasons.append("contract contains a malformed artifact role")
            continue
        name = str(role.get("role"))
        requirement = role.get("requirement")
        cardinality = role.get("cardinality")
        blobs: list[GitBlob] = []
        if role.get("resolution") == "path_candidates":
            for pattern in role.get("path_candidates", []):
                blob = reader.blob(render(pattern, row["theorem"], f"role {name}"))
                if blob is not None:
                    blobs.append(blob)
        elif role.get("resolution") == "receipt_bound_paths":
            if receipt is None:
                role_unknown.append(f"{name}: receipt-bound paths unavailable")
                continue
            paths = receipt_bound_paths(pointer_value(receipt, role.get("binding_pointer")))
            if paths is None:
                role_reasons.append(f"{name}: receipt binding is missing or malformed")
                continue
            for relative in paths:
                blob = reader.blob(relative)
                if blob is None:
                    role_reasons.append(f"{name}: bound HEAD blob is missing: {relative}")
                else:
                    blobs.append(blob)
        else:
            role_reasons.append(f"{name}: unsupported resolution")
            continue
        for blob in blobs:
            selected_role_bindings.append({"role": name, **blob.binding()})
        if requirement == "conditional" and not blobs:
            role_unknown.append(f"{name}: conditional applicability needs semantic evaluation")
        elif cardinality == "exactly_one" and len(blobs) != 1:
            role_reasons.append(f"{name}: expected exactly one HEAD blob, found {len(blobs)}")
        elif cardinality == "one_or_more" and not blobs:
            role_reasons.append(f"{name}: expected one or more HEAD blobs")
    classes["missing_or_ambiguous_role"] = classification(
        "missing_or_ambiguous_role",
        "blocked" if role_reasons else ("unknown" if role_unknown else "clear"),
        role_reasons if role_reasons else role_unknown,
        sorted(selected_role_bindings, key=lambda value: (value["role"], value["path"])),
    )

    current_authorities = phase_contract.get("validator_authorities", [])
    superseded_sources = phase_contract.get("superseded_validator_sources", [])
    if not isinstance(current_authorities, list) or not isinstance(
        superseded_sources, list
    ):
        fail("phase contract lacks validator authority registries")
    current_validators: list[GitBlob] = []
    for candidate in current_authorities:
        if not isinstance(candidate, dict):
            continue
        blob = reader.blob(
            render(candidate.get("path_pattern"), row["theorem"], "current validator authority")
        )
        if blob is not None:
            current_validators.append(blob)
    superseded_validators: list[GitBlob] = []
    for source in superseded_sources:
        if not isinstance(source, dict):
            continue
        blob = reader.blob(
            render(source.get("path_pattern"), row["theorem"], "superseded validator source")
        )
        if blob is not None:
            superseded_validators.append(blob)
    superseded_bindings = [blob.binding() for blob in superseded_validators]
    classes["validator_authority_superseded"] = classification(
        "validator_authority_superseded",
        "blocked" if superseded_validators else "clear",
        (
            [
                "pre-v2 validator source is historical negative-observation evidence only; "
                "it cannot provide current positive acceptance"
            ]
            if superseded_validators
            else []
        ),
        superseded_bindings,
    )
    validator_bindings = [blob.binding() for blob in current_validators]
    base_reasons: list[str] = []
    base_unknown: list[str] = []
    selected_validator = current_validators[0] if len(current_validators) == 1 else None
    if len(current_validators) != 1:
        base_reasons.append(
            "expected exactly one current stage1-v2 HEAD validator authority, "
            f"found {len(current_validators)}"
        )
    elif receipt is None:
        base_unknown.append("worker base cannot be read without a selected receipt")
    else:
        base_revision = receipt.get("base_revision")
        if not isinstance(base_revision, str) or not OID_RE.fullmatch(base_revision):
            base_reasons.append("receipt base_revision is missing or malformed")
        else:
            base_blob = reader.blob_at(base_revision, selected_validator.path)
            if base_blob is None:
                base_reasons.append("validator did not exist at receipt base_revision")
            elif base_blob[0] != selected_validator.oid:
                base_reasons.append("validator HEAD blob differs from receipt-base blob")
            else:
                validator_bindings.append(
                    {
                        "path": selected_validator.path,
                        "base_revision": base_revision,
                        "base_git_blob": base_blob[0],
                        "base_sha256": sha256_bytes(base_blob[1]),
                    }
                )
    classes["validator_base_mismatch"] = classification(
        "validator_base_mismatch",
        "blocked" if base_reasons else ("unknown" if base_unknown else "clear"),
        base_reasons if base_reasons else base_unknown,
        validator_bindings,
    )

    if selected_validator is None:
        classes["validator_stdout_mismatch"] = classification(
            "validator_stdout_mismatch",
            "unknown",
            ["validator stdout cannot be inspected without one selected validator"],
            validator_bindings,
        )
        classes["sandbox_incompatible"] = classification(
            "sandbox_incompatible",
            "unknown",
            ["sandbox compatibility cannot be inspected without one selected validator"],
            validator_bindings,
        )
    else:
        source = selected_validator.data.decode("utf-8", "replace")
        semantic_markers = (
            SEMANTIC_SCHEMA,
            "phase_predicate_proven",
            "phase_accepted",
            "open_obligations",
            "stale_inputs",
        )
        if not all(marker in source for marker in semantic_markers):
            classes["validator_stdout_mismatch"] = classification(
                "validator_stdout_mismatch",
                "blocked",
                ["validator source lacks the exact semantic schema marker set"],
                validator_bindings,
            )
        else:
            classes["validator_stdout_mismatch"] = classification(
                "validator_stdout_mismatch",
                "unknown",
                ["static markers exist, but unique runtime JSON stdout was not executed"],
                validator_bindings,
            )
        sandbox_blocked, sandbox_unknown = static_sandbox_findings(selected_validator)
        classes["sandbox_incompatible"] = classification(
            "sandbox_incompatible",
            "blocked" if sandbox_blocked else "unknown",
            sandbox_blocked
            if sandbox_blocked
            else (
                sandbox_unknown
                if sandbox_unknown
                else ["static scan is clean, but bwrap compatibility was not executed"]
            ),
            validator_bindings,
        )

    ordered_classes = [classes[name] for name in CLASSIFICATIONS]
    item = {
        "schema_version": ITEM_SCHEMA,
        "item_id": row["item"],
        "theorem_id": row["theorem"],
        "phase": row["phase"],
        "attempts": int(row["attempts"]),
        "authoritative_state": "[_]",
        "authority_revision": reader.revision,
        "authority_tree": reader.tree,
        "blueprint": blueprint_binding,
        "contract": contract_binding,
        "classifications": ordered_classes,
        "migration_ready": all(value["status"] == "clear" for value in ordered_classes),
        "acceptance_claimed": False,
    }
    item["item_sha256"] = sha256_bytes(canonical_json(item))
    return item


def load_contract(
    reader: HeadReader, candidate_contract: Path | None
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    head_blob = reader.blob(CONTRACT_PATH)
    if candidate_contract is None:
        if head_blob is None:
            fail("acceptance contract is not tracked at authoritative HEAD")
        return strict_json(head_blob.data, "HEAD acceptance contract"), head_blob.binding(), True
    path = candidate_contract.resolve()
    data = path.read_bytes()
    binding = {
        "path": str(path),
        "git_blob": None,
        "sha256": sha256_bytes(data),
        "size": len(data),
        "git_mode": None,
    }
    if head_blob is not None and data == head_blob.data:
        return strict_json(data, "candidate acceptance contract"), head_blob.binding(), True
    return strict_json(data, "candidate acceptance contract"), binding, False


def build_inventory(
    root: Path,
    *,
    revision: str = "HEAD",
    candidate_contract: Path | None = None,
) -> dict[str, Any]:
    reader = HeadReader(root, revision)
    blueprint = reader.blob(BLUEPRINT_PATH)
    if blueprint is None:
        fail("authoritative HEAD lacks the Stage1 v2 blueprint")
    contract, contract_binding, authoritative_contract = load_contract(
        reader, candidate_contract
    )
    if contract.get("schema_version") != "stage1-phase-acceptance-contracts/1.0":
        fail("acceptance contract schema is unsupported")
    rows = [match.groupdict() for match in ITEM_RE.finditer(blueprint.data.decode("utf-8"))]
    if not rows:
        fail("authoritative blueprint has no [_] items")
    items = [
        inventory_item(reader, contract, contract_binding, blueprint.binding(), row)
        for row in rows
    ]
    status_counts = Counter(
        (entry["category"], entry["status"])
        for item in items
        for entry in item["classifications"]
    )
    phase_counts = Counter(item["phase"] for item in items)
    inventory = {
        "schema_version": INVENTORY_SCHEMA,
        "generated_from_revision": reader.revision,
        "generated_from_tree": reader.tree,
        "authority_mode": "authoritative_head" if authoritative_contract else "candidate_preflight",
        "authoritative_for_acceptance": False,
        "mutates_repository": False,
        "executes_validators": False,
        "blueprint": blueprint.binding(),
        "contract": contract_binding,
        "item_count": len(items),
        "phase_counts": dict(sorted(phase_counts.items())),
        "classification_counts": {
            name: {
                status: status_counts[(name, status)]
                for status in ("blocked", "clear", "unknown")
            }
            for name in CLASSIFICATIONS
        },
        "migration_ready_count": sum(item["migration_ready"] for item in items),
        "items": items,
    }
    inventory["inventory_sha256"] = sha256_bytes(canonical_json(inventory))
    return inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument(
        "--candidate-contract",
        type=Path,
        help="explicit uncommitted contract for non-authoritative preflight only",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    inventory = build_inventory(
        args.repo,
        revision=args.revision,
        candidate_contract=args.candidate_contract,
    )
    payload = json.dumps(inventory, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except InventoryError as exc:
        raise SystemExit(f"stage1_legacy_migration_inventory: {exc}") from None
