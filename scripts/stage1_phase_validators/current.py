#!/usr/bin/env python3
"""Current fail-closed Stage1 v2 authority for all seven phase predicates."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
from typing import Any, Mapping, NoReturn


INPUT_SCHEMA = "stage1-v2-validator-input/1.0"
OUTPUT_SCHEMA = "stage1-validator-semantic-result/1.0"
CONTRACT_PATH = "Docs/Stage1_Phase_Acceptance_Contracts.json"
PHASES = {
    "intake", "statement", "anchor_audit", "obligation_tree", "proof",
    "validation", "release",
}
RESEARCH_PHASES = {"intake", "statement", "anchor_audit"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMON_RECEIPT_KEYS = {
    "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
    "intent", "base_revision", "base_tree", "inputs", "support_state",
    "proposed_state", "accepted", "verdict", "selftest_status",
    "selftest_result", "known_failures", "first_failed_gate",
    "retry_condition", "status_boundary", "audit_complete",
    "theorem_complete", "invalidation_inputs",
}
PROHIBITED_LEAN = re.compile(r"\b(?:sorry|admit|sorryAx|unsafe)\b")
PROOF_BEARING_LEAN_DECLARATION = re.compile(
    r"(?m)^\s*(?:@[A-Za-z_][^\n]*\n\s*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)\s+)*"
    # `def hidden : True := by trivial` is as proof-bearing as a theorem, and
    # metaprogramming commands can manufacture declarations indirectly. A
    # research-only phase may record imports, namespaces, variables and checks,
    # but it may not add any persistent declaration or declaration generator.
    r"(?:theorem|lemma|opaque|example|def|abbrev|instance|axiom|constant|"
    r"inductive|structure|class|elab|macro|syntax|run_cmd|initialize|"
    r"builtin_initialize)\b"
)
LEAN_PROJECT = Path("Formalizations/Lean")
LEAN_TOOLCHAIN = LEAN_PROJECT / "lean-toolchain"
LEAN_LOCK = LEAN_PROJECT / "lake-manifest.json"
LEAN_REPLAY_TIMEOUT_SECONDS = 3600
LEAN_AUTHORITY_SCHEMA = "stage1-lean-authority/1.1"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
TOOLCHAIN_RE = re.compile(r"^leanprover/lean4:v([0-9]+\.[0-9]+\.[0-9]+)$")
DECLARATION_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_'.]*$")
PROBE_SCHEMA = "stage1-lean-probe-row/1.0"
DEPENDENCY_PROBE_SCHEMA = "stage1-lean-dependency-probe/1.0"
PROBE_BEGIN = "STAGE1_PROBE_BEGIN "
PROBE_END = " STAGE1_PROBE_END"
PHASE_RESULT_BEGIN = "STAGE1_PHASE_RESULT_BEGIN "
PHASE_RESULT_END = " STAGE1_PHASE_RESULT_END"
BASE_FOCUS_KEYS = {
    "focus_contract_sha256", "execution_disposition", "receipt_sha256",
}
INTEGRATION_FOCUS_KEYS = BASE_FOCUS_KEYS | {
    "machine_evidence_class", "exact_machine_source", "exact_machine_source_used",
    "introduced_root_critical_proof",
}
EXACT_MACHINE_SOURCE_KEYS = {
    "formal_system", "repository", "revision", "tree_or_archive_sha256", "file_path",
    "file_sha256", "module", "declaration", "declaration_type_sha256",
    "match_kind", "transport_evidence", "terminal_proof_body",
}
MACHINE_TRANSPORT_EVIDENCE_KEYS = {
    "path", "sha256", "role", "evidence_kind", "source_formal_system",
    "source_declaration", "source_declaration_type_sha256",
    "target_formal_system", "target_declaration",
    "target_declaration_type_sha256", "replay_receipt_sha256",
}
TRANSPORT_DECISION_KEYS = {
    "source_id", "consumer_obligation_id", "provider_theorem_id",
    "provider_obligation_id", "terminal_proof_body_id",
    "provider_body_source", "provider_statement_fingerprint",
    "consumer_required_fingerprint", "relationship", "provider_proof_state",
    "provider_receipts", "decision", "consumer_import_or_wrapper",
    "consumer_import_source", "provider_import_module", "context_digest",
}
RECEIPT_REFERENCE_KEYS = {"path", "receipt_id", "sha256"}
ARTIFACT_REFERENCE_KEYS = {"path", "sha256"}
V2_PHASE_STATES = {"[ ]", "[_]", "[x]"}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> NoReturn:
    raise ValidationError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def strict_object(data: bytes, label: str) -> dict[str, Any]:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{label} is not one UTF-8 JSON object") from exc
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def safe_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        fail(f"{label} is malformed")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or str(pure) != value:
        fail(f"{label} is not repository-relative")
    path = Path(value)
    if path.is_symlink() or not path.is_file():
        fail(f"{label} is missing or unsafe")
    return path


def safe_directory(value: Path, label: str) -> Path:
    current = Path(".")
    for component in value.parts:
        current /= component
        if current.is_symlink():
            fail(f"{label} traverses a symlink")
    if not value.is_dir():
        fail(f"{label} is missing")
    return value


def exact_file(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        fail(f"{label} is missing or unsafe")
    return path.read_bytes()


def valid_exact_machine_source(source: Any) -> bool:
    """Validate the complete immutable source identity carried at every phase."""
    if not isinstance(source, Mapping) or set(source) != EXACT_MACHINE_SOURCE_KEYS:
        return False
    repository = source.get("repository")
    revision = source.get("revision")
    file_path = source.get("file_path")
    module = source.get("module")
    declaration = source.get("declaration")
    terminal = source.get("terminal_proof_body")
    match_kind = source.get("match_kind")
    transports = source.get("transport_evidence")
    try:
        pure_file = PurePosixPath(str(file_path))
    except (TypeError, ValueError):
        return False
    if (
        source.get("formal_system") != "Lean 4"
        or not isinstance(repository, str)
        or not repository
        or not isinstance(revision, str)
        or re.fullmatch(r"[0-9a-f]{40,64}", revision) is None
        or not isinstance(file_path, str)
        or not file_path
        or pure_file.is_absolute()
        or ".." in pure_file.parts
        or not isinstance(module, str)
        or DECLARATION_RE.fullmatch(module) is None
        or not isinstance(declaration, str)
        or DECLARATION_RE.fullmatch(declaration) is None
        or any(
            not isinstance(source.get(field), str)
            or SHA256_RE.fullmatch(str(source[field])) is None
            for field in (
                "tree_or_archive_sha256", "file_sha256",
                "declaration_type_sha256",
            )
        )
        or not isinstance(terminal, Mapping)
        or set(terminal) != {"locator", "kind", "sha256"}
        or terminal.get("locator") != declaration
        or terminal.get("kind") not in {"theorem", "opaque", "definition", "proof_term"}
        or not isinstance(terminal.get("sha256"), str)
        or SHA256_RE.fullmatch(str(terminal["sha256"])) is None
    ):
        return False
    if match_kind == "exact":
        return transports == []
    if (
        match_kind != "checked_transport"
        or not isinstance(transports, list)
        or len(transports) != 1
        or not isinstance(transports[0], Mapping)
        or set(transports[0]) != MACHINE_TRANSPORT_EVIDENCE_KEYS
    ):
        return False
    transport = transports[0]
    try:
        transport_path = PurePosixPath(str(transport.get("path")))
    except (TypeError, ValueError):
        return False
    return bool(
        isinstance(transport.get("path"), str)
        and transport.get("path")
        and not transport_path.is_absolute()
        and ".." not in transport_path.parts
        and transport.get("role") == "statement_match"
        and transport.get("evidence_kind") == "machine_checked_statement_transport"
        and transport.get("source_formal_system") == source.get("formal_system")
        and transport.get("source_declaration") == declaration
        and transport.get("source_declaration_type_sha256")
        == source.get("declaration_type_sha256")
        and transport.get("target_formal_system") == "Lean 4"
        and isinstance(transport.get("target_declaration"), str)
        and DECLARATION_RE.fullmatch(str(transport["target_declaration"])) is not None
        and isinstance(transport.get("target_declaration_type_sha256"), str)
        and SHA256_RE.fullmatch(str(transport["target_declaration_type_sha256"]))
        is not None
        and transport.get("target_declaration_type_sha256")
        != source.get("declaration_type_sha256")
        and isinstance(transport.get("sha256"), str)
        and SHA256_RE.fullmatch(str(transport["sha256"])) is not None
        and transport.get("sha256") == transport.get("replay_receipt_sha256")
    )


def normalized_type_sha256(type_text: str) -> str:
    return sha256(" ".join(type_text.split()).encode("utf-8"))


def local_imports(data: bytes, label: str) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{label} is not UTF-8") from exc
    return re.findall(r"(?m)^\s*import\s+([A-Za-z_][A-Za-z0-9_'.]*)\s*$", text)


def parse_probe_output(
    output: bytes, declarations: list[str]
) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Parse only authority-marked JSON rows, ignoring all other Lean diagnostics."""
    try:
        lines = output.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ValidationError("Lean replay output is not UTF-8") from exc
    types: dict[str, str] = {}
    axioms: dict[str, list[str]] = {}
    seen_indices: set[int] = set()
    for line in lines:
        if not line.startswith(PROBE_BEGIN) or not line.endswith(PROBE_END):
            continue
        row = strict_object(
            line[len(PROBE_BEGIN):-len(PROBE_END)].encode("utf-8"),
            "Lean authority probe row",
        )
        if set(row) != {"schema", "index", "declaration", "type", "axioms"}:
            fail("Lean authority probe row schema is not exact")
        index = row.get("index")
        declaration = row.get("declaration")
        type_text = row.get("type")
        values = row.get("axioms")
        if (
            row.get("schema") != PROBE_SCHEMA
            or not isinstance(index, int)
            or isinstance(index, bool)
            or index < 0
            or index >= len(declarations)
            or declaration != declarations[index]
            or not isinstance(type_text, str)
            or not type_text.strip()
            or not isinstance(values, list)
            or any(not isinstance(value, str) or not value for value in values)
            or len(values) != len(set(values))
            or index in seen_indices
        ):
            fail("Lean authority probe row is malformed or ambiguous")
        seen_indices.add(index)
        types[declaration] = normalized_type_sha256(type_text)
        axioms[declaration] = sorted(values)
    if seen_indices != set(range(len(declarations))):
        fail("Lean replay did not report exactly one structured row per declaration")
    return types, axioms


def owner_root_for_source(relative_source: str) -> PurePosixPath:
    pure = PurePosixPath(relative_source)
    if (
        pure.is_absolute()
        or len(pure.parts) < 3
        or pure.parts[0] != "Stage1_Instances"
        or re.fullmatch(r"THM-M-[0-9]{4}", pure.parts[1]) is None
        or pure.suffix != ".lean"
    ):
        fail("proof replay source is not a target-owned Lean file")
    return PurePosixPath(*pure.parts[:2])


def module_name_for_source(relative: PurePosixPath, owner: PurePosixPath) -> str:
    try:
        within_owner = relative.relative_to(owner)
    except ValueError:
        fail("proof replay dependency escapes the selected theorem owner")
    components = (*within_owner.parts[:-1], within_owner.stem)
    if not components or any(
        re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*", component) is None
        for component in components
    ):
        fail("proof replay source path does not define a canonical Lean module")
    return ".".join(components)


def resolve_bound_import(
    imported: str,
    *,
    current_module: str,
    available: Mapping[str, Any],
) -> str | None:
    """Resolve an owner-local import, including legacy same-directory names."""
    if imported in available:
        return imported
    parent = current_module.rpartition(".")[0]
    relative = f"{parent}.{imported}" if parent else imported
    return relative if relative in available else None


def authority_probe_source(source_module: str, declarations: list[str]) -> bytes:
    rows: list[str] = [
        "import Lean\n",
        f"import {source_module}\n",
        "open Lean Elab Command\n",
    ]
    for index, declaration in enumerate(declarations):
        rows.append(
            "run_cmd do\n"
            f"  let declaration : Name := `{declaration}\n"
            "  let env ← getEnv\n"
            "  let some info := env.find? declaration | throwError \"missing declaration\"\n"
            "  let type ← liftCoreM <| Lean.Meta.MetaM.run' (Lean.Meta.ppExpr info.type)\n"
            "  let axioms ← Lean.collectAxioms declaration\n"
            "  let row := Lean.Json.mkObj [\n"
            f"    (\"schema\", \"{PROBE_SCHEMA}\"),\n"
            f"    (\"index\", {index}),\n"
            "    (\"declaration\", declaration.toString),\n"
            "    (\"type\", toString type),\n"
            "    (\"axioms\", toJson (axioms.toList.map toString))]\n"
            f"  IO.println s!\"{PROBE_BEGIN}{{row.compress}}{PROBE_END}\"\n"
        )
    return "".join(rows).encode("utf-8")


def declaration_dependency_probe_source(
    source_module: str,
    *,
    consumer_declaration: str,
    provider_declaration: str,
    provider_module: str,
    verify_provider_module: bool = True,
) -> bytes:
    """Ask Lean whether the consumer body directly uses the admitted provider."""
    if any(
        DECLARATION_RE.fullmatch(value) is None
        for value in (consumer_declaration, provider_declaration, provider_module)
    ):
        fail("Lean dependency probe declarations are malformed")
    relation = (
        "provider_constant_identity"
        if consumer_declaration == provider_declaration
        else "direct_proof_body_constant_dependency"
    )
    payload_row = {
        "schema": DEPENDENCY_PROBE_SCHEMA,
        "consumer": consumer_declaration,
        "provider": provider_declaration,
        "provider_module": provider_module,
        "relation": relation,
    }
    payload = json.dumps(
        payload_row,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (
        "import Lean\n"
        f"import {source_module}\n"
        "open Lean Elab Command\n"
        "run_cmd do\n"
        f"  let consumer : Name := `{consumer_declaration}\n"
        f"  let provider : Name := `{provider_declaration}\n"
        f"  let expectedProviderModule : Name := `{provider_module}\n"
        "  let env \u2190 getEnv\n"
        + (
            (
                "  let some providerModuleIdx := env.getModuleIdxFor? provider |\n"
                "    throwError \"provider declaration does not come from an imported module\"\n"
                "  let providerModule := env.header.moduleNames[providerModuleIdx.toNat]!\n"
                "  unless providerModule == expectedProviderModule do\n"
                "    throwError \"provider declaration module disagrees with admission\"\n"
            )
            if verify_provider_module
            else ""
        )
        + (
            (
                "  let some info := env.find? consumer | throwError \"missing consumer declaration\"\n"
                "  let some body := info.value? (allowOpaque := true) |\n"
                "    throwError \"consumer declaration has no inspectable proof body\"\n"
                "  unless body.getUsedConstantsAsSet.contains provider do\n"
                "    throwError \"consumer proof body does not directly depend on provider declaration\"\n"
            )
            if consumer_declaration != provider_declaration
            else ""
        )
        +
        f"  IO.println {json.dumps(payload, ensure_ascii=True)}\n"
    ).encode("utf-8")


def declaration_region_sha256(data: bytes, declaration: str) -> str | None:
    """Hash the same exact declaration region used by focus admission."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError("Lean integration source is not UTF-8") from exc
    if DECLARATION_RE.fullmatch(declaration) is None:
        fail("integration declaration name is malformed")
    short = declaration.rsplit(".", 1)[-1]
    start = re.search(
        rf"(?m)^\s*(?:theorem|lemma|opaque|def)\s+{re.escape(short)}\b", text
    )
    if start is None:
        return None
    tail = text[start.start():]
    next_declaration = re.search(
        r"(?m)^\s*(?:theorem|lemma|opaque|def|namespace|end)\s+",
        tail[start.end() - start.start():],
    )
    end = len(tail) if next_declaration is None else (
        start.end() - start.start() + next_declaration.start()
    )
    return sha256(tail[:end].encode("utf-8"))


def exact_vendored_provider(
    proof_sources: list[Mapping[str, Any]],
    artifact_bytes: Mapping[str, bytes],
    *,
    theorem_id: str,
    declaration: str,
    terminal_body_sha256: str,
) -> tuple[Mapping[str, Any], str] | None:
    """Locate one exact local copy of the admitted terminal declaration body."""
    matches: list[tuple[Mapping[str, Any], str]] = []
    owner = PurePosixPath("Stage1_Instances", theorem_id)
    for binding in proof_sources:
        path = str(binding.get("path", ""))
        data = artifact_bytes.get(path)
        if not path.endswith(".lean") or not isinstance(data, bytes):
            continue
        if declaration_region_sha256(data, declaration) != terminal_body_sha256:
            continue
        module = module_name_for_source(PurePosixPath(path), owner)
        matches.append((binding, module))
    if len(matches) > 1:
        fail("admitted provider terminal body is ambiguously vendored")
    return matches[0] if matches else None


def reject_research_proof_construction(
    phase: str,
    focus: Mapping[str, Any],
    role_map: Mapping[str, Any],
    artifact_bytes: Mapping[str, bytes],
) -> None:
    """Keep research-only phases from smuggling proof construction into HEAD."""

    if focus.get("execution_disposition") != "research_required":
        return
    changed = role_map.get("staged_delta_paths")
    if not isinstance(changed, list) or any(
        not isinstance(path, str) or not path for path in changed
    ):
        fail("research-only validation lacks the scheduler-bound changed-path inventory")
    changed_lean = sorted(path for path in changed if path.endswith(".lean"))
    if phase == "intake" and changed_lean:
        fail("research-only intake may not create or modify Lean declarations")
    for path in changed_lean:
        data = artifact_bytes.get(path)
        if not isinstance(data, bytes):
            fail("research-only changed Lean path is not a bound phase artifact")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError("research-only Lean artifact is not UTF-8") from exc
        if PROHIBITED_LEAN.search(text):
            fail("research-only Lean artifact contains a prohibited construct")
        if PROOF_BEARING_LEAN_DECLARATION.search(text):
            if phase == "statement":
                fail(
                    "research-only statement phase may not create or modify "
                    "proof-bearing or persistent Lean declarations"
                )
            if phase == "anchor_audit":
                fail(
                    "research-only anchor audit may not create or modify substantive "
                    "proof-bearing Lean declarations"
                )


def canonical_remote(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    result = value.rstrip("/")
    return result[:-4] if result.endswith(".git") else result


def pinned_provider_olean(
    lock_bytes: bytes,
    cache: Path,
    *,
    repository: str,
    revision: str,
    module: str,
) -> Path:
    """Resolve one admitted provider through the exact Lake manifest row."""
    manifest = strict_object(lock_bytes, "Lean dependency manifest")
    packages = manifest.get("packages")
    if not isinstance(packages, list):
        fail("Lean dependency manifest package inventory is malformed")
    expected_remote = canonical_remote(repository)
    rows = [
        row for row in packages
        if isinstance(row, Mapping)
        and canonical_remote(row.get("url")) == expected_remote
        and row.get("rev") == revision
    ]
    if len(rows) != 1:
        fail("admitted provider repository/revision is absent or ambiguous in Lake manifest")
    name = rows[0].get("name")
    if not isinstance(name, str) or not name:
        fail("admitted Lake provider has no package name")
    cache_name = name[1:-1] if name.startswith("«") and name.endswith("»") else name
    if re.fullmatch(r"[A-Za-z0-9_.-]+", cache_name) is None:
        fail("admitted Lake provider package name is unsafe")
    package = cache / "packages" / cache_name
    if package.is_symlink() or not package.is_dir():
        fail("admitted Lake provider package is absent from the pinned cache")
    olean = (
        package / ".lake/build/lib/lean" / Path(*module.split("."))
    ).with_suffix(".olean")
    if olean.is_symlink() or not olean.is_file():
        fail("admitted provider module is absent from its pinned Lake package")
    return olean


def pinned_toolchain_root(toolchain: str) -> Path:
    match = TOOLCHAIN_RE.fullmatch(toolchain)
    if match is None:
        fail("Formalizations/Lean has a noncanonical Lean toolchain pin")
    root = Path("/stage1-toolchain")
    if root.is_symlink() or not root.is_dir():
        fail("pinned Lean toolchain is unavailable inside the authority sandbox")
    for name in ("lean", "lake"):
        executable = root / "bin" / name
        if executable.is_symlink() or not executable.is_file() or not os.access(executable, os.X_OK):
            fail(f"pinned {name} executable is unavailable inside the authority sandbox")
    return root


def _descriptor_sha256(descriptor: int) -> str:
    hasher = hashlib.sha256()
    offset = 0
    while True:
        chunk = os.pread(descriptor, 1024 * 1024, offset)
        if not chunk:
            break
        hasher.update(chunk)
        offset += len(chunk)
    return hasher.hexdigest()


def _open_bound_executable(path: Path, label: str) -> tuple[int, tuple[int, ...], str]:
    """Open and hash one executable inode, rejecting path/read races."""

    try:
        descriptor = os.open(
            path, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
        )
    except OSError as exc:
        raise ValidationError(f"{label} is missing or unsafe") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_mode & 0o111 == 0:
            fail(f"{label} is not a regular executable")
        digest = _descriptor_sha256(descriptor)
        after = os.fstat(descriptor)
        identity = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        )
        if identity != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ) or digest != _descriptor_sha256(descriptor):
            fail(f"{label} changed while being bound")
        return descriptor, identity, digest
    except BaseException:
        os.close(descriptor)
        raise


def _run_bound_toolchain_command(
    command_runner: Any,
    tool_root: Path,
    arguments: list[str],
    *,
    expected_lean_sha256: str,
    expected_lake_sha256: str,
    **kwargs: Any,
) -> subprocess.CompletedProcess[bytes]:
    """Execute the exact open Lean/Lake inodes whose bytes were authorized."""

    lake_fd, lake_identity, lake_digest = _open_bound_executable(
        tool_root / "bin" / "lake", "Lake executable"
    )
    try:
        lean_fd, lean_identity, lean_digest = _open_bound_executable(
            tool_root / "bin" / "lean", "Lean executable"
        )
        try:
            if (
                lean_digest != expected_lean_sha256
                or lake_digest != expected_lake_sha256
            ):
                fail("pinned Lean/Lake executable differs from replay authority")
            # `/proc/self/fd` makes exec consume the already-open inode rather
            # than resolving a mutable path after validation. `pass_fds` keeps
            # both handles available when Lake launches the exact Lean binary.
            argv = [
                f"/proc/self/fd/{lake_fd}",
                "env",
                f"/proc/self/fd/{lean_fd}",
                *arguments,
            ]
            result = command_runner(
                argv, pass_fds=(lake_fd, lean_fd), **kwargs
            )
            for descriptor, identity, digest, path, label in (
                (
                    lake_fd, lake_identity, lake_digest,
                    tool_root / "bin" / "lake", "Lake executable",
                ),
                (
                    lean_fd, lean_identity, lean_digest,
                    tool_root / "bin" / "lean", "Lean executable",
                ),
            ):
                current = os.fstat(descriptor)
                current_identity = (
                    current.st_dev,
                    current.st_ino,
                    current.st_size,
                    current.st_mtime_ns,
                    current.st_ctime_ns,
                )
                try:
                    pathname = path.lstat()
                    path_identity = (
                        pathname.st_dev,
                        pathname.st_ino,
                        pathname.st_size,
                        pathname.st_mtime_ns,
                        pathname.st_ctime_ns,
                    )
                except OSError:
                    path_identity = ()
                if (
                    current_identity != identity
                    or path_identity != identity
                    or _descriptor_sha256(descriptor) != digest
                ):
                    fail(f"{label} changed during replay")
            return result
        finally:
            os.close(lean_fd)
    finally:
        os.close(lake_fd)


def readonly_lean_replay(
    source: Path,
    declarations: list[str],
    *,
    command_runner: Any = subprocess.run,
    tool_root: Path | None = None,
    cache: Path | None = None,
    scratch_root: Path | None = None,
    dependency_packages_sha256: str | None = None,
    toolchain_closure_sha256: str | None = None,
    toolchain_closure_file_count: int | None = None,
    toolchain_closure_bytes: int | None = None,
    compiled_cache_sha256: str | None = None,
    compiled_cache_file_count: int | None = None,
    compiled_cache_bytes: int | None = None,
    bound_sources: Mapping[str, bytes] | None = None,
    dependency_probe: tuple[str, str, str] | None = None,
    imported_provider: tuple[str, str, str, str] | None = None,
    bound_provider_source: tuple[str, bytes] | None = None,
) -> dict[str, Any]:
    """Compile and probe exact local bytes inside the outer authority sandbox."""
    project = safe_directory(LEAN_PROJECT, "Formalizations/Lean project")
    source_bytes = exact_file(source, "proof source")
    toolchain_bytes = exact_file(LEAN_TOOLCHAIN, "Lean toolchain pin")
    lock_bytes = exact_file(LEAN_LOCK, "Lean dependency lock")
    try:
        toolchain = toolchain_bytes.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ValidationError("Lean toolchain pin is not UTF-8") from exc
    tool_root = tool_root or pinned_toolchain_root(toolchain)
    lean_executable = tool_root / "bin" / "lean"
    lake_executable = tool_root / "bin" / "lake"
    lean_binary = exact_file(lean_executable, "Lean executable")
    lake_binary = exact_file(lake_executable, "Lake executable")
    cache = cache or Path("/stage1-lake-cache")
    if cache.is_symlink() or not cache.is_dir():
        fail("pinned Lean dependency cache is unavailable")
    for dependency in cache / "packages", cache / "build":
        if dependency.is_symlink() or not dependency.is_dir():
            fail("pinned Lean dependency cache is incomplete or unsafe")
    relative_source = source.as_posix()
    owner = owner_root_for_source(relative_source)
    if not declarations or any(
        not isinstance(value, str) or DECLARATION_RE.fullmatch(value) is None
        for value in declarations
    ):
        fail("proof replay declarations are malformed")
    scratch_root = scratch_root or Path("/scratch")
    if scratch_root.is_symlink() or not scratch_root.is_dir():
        fail("Lean authority scratch is unavailable or unsafe")
    with tempfile.TemporaryDirectory(
        prefix="stage1-lean-probe-", dir=scratch_root
    ) as raw:
        scratch = Path(raw)
        replay_project = scratch / "project"
        replay_project.mkdir()
        for name in ("lean-toolchain", "lake-manifest.json", "lakefile.lean"):
            source_file = project / name
            if source_file.is_symlink() or not source_file.is_file():
                fail(f"Lean project {name} is missing or unsafe")
            (replay_project / name).write_bytes(source_file.read_bytes())
        (replay_project / ".lake").symlink_to(cache)
        replay_owner = replay_project / owner.as_posix()
        replay_owner.mkdir(parents=True)
        supplied = dict(bound_sources or {relative_source: source_bytes})
        if supplied.get(relative_source) != source_bytes:
            fail("bound replay source bytes disagree with the selected proof source")
        source_by_module: dict[str, tuple[PurePosixPath, bytes]] = {}
        for relative, data in supplied.items():
            pure = PurePosixPath(relative)
            if (
                pure.is_absolute()
                or ".." in pure.parts
                or pure.suffix != ".lean"
                or not isinstance(data, bytes)
            ):
                fail("proof replay dependency is not a bound target-owned Lean source")
            module = module_name_for_source(pure, owner)
            if module in source_by_module:
                fail("proof replay source modules are ambiguous")
            source_by_module[module] = (pure, data)
            destination = replay_project / pure.as_posix()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        source_module = module_name_for_source(PurePosixPath(relative_source), owner)
        imported_provider_module: str | None = None
        imported_provider_declaration: str | None = None
        imported_provider_repository: str | None = None
        imported_provider_revision: str | None = None
        provider_is_local_vendored = False
        bound_provider_module: str | None = None
        if bound_provider_source is not None:
            provider_relative, provider_bytes = bound_provider_source
            provider_pure = PurePosixPath(provider_relative)
            if (
                provider_pure.is_absolute()
                or ".." in provider_pure.parts
                or len(provider_pure.parts) < 3
                or provider_pure.parts[0] != "Stage1_Instances"
                or provider_pure.parts[1] == owner.parts[1]
                or re.fullmatch(r"THM-M-[0-9]{4}", provider_pure.parts[1]) is None
                or provider_pure.suffix != ".lean"
                or not isinstance(provider_bytes, bytes)
            ):
                fail("bound provider source is not an independent target-owned Lean file")
            provider_owner = PurePosixPath(*provider_pure.parts[:2])
            bound_provider_module = module_name_for_source(provider_pure, provider_owner)
        if imported_provider is not None:
            (
                imported_provider_module,
                imported_provider_declaration,
                imported_provider_repository,
                imported_provider_revision,
            ) = imported_provider
            if (
                DECLARATION_RE.fullmatch(imported_provider_module) is None
                or DECLARATION_RE.fullmatch(imported_provider_declaration) is None
                or re.fullmatch(r"[0-9a-f]{40,64}", imported_provider_revision) is None
                or canonical_remote(imported_provider_repository) is None
            ):
                fail("admitted provider import identity is malformed or ambiguous")
            if (
                bound_provider_module is not None
                and imported_provider_module != bound_provider_module
            ):
                fail("bound provider source module disagrees with its import identity")
            provider_is_local_vendored = imported_provider_module in source_by_module
            if bound_provider_source is not None:
                if provider_is_local_vendored:
                    fail("bound provider module collides with a consumer-owned module")
                provider_is_local_vendored = True
            if not provider_is_local_vendored:
                pinned_provider_olean(
                    lock_bytes,
                    cache,
                    repository=imported_provider_repository,
                    revision=imported_provider_revision,
                    module=imported_provider_module,
                )
        replay_env = {
            "PATH": f"{tool_root / 'bin'}:/usr/bin:/bin",
            "HOME": scratch_root.as_posix(),
            "TMPDIR": scratch_root.as_posix(),
            "LAKE_HOME": (scratch_root / "lake").as_posix(),
            # `lake env` appends an inherited LEAN_PATH to its pinned package
            # paths. This is the only search root containing bound local modules.
            "LEAN_PATH": replay_owner.as_posix(),
        }
        local_search_roots = sorted({
            (replay_owner / Path(*module.split(".")).parent).as_posix()
            for module in source_by_module
        })
        replay_env["LEAN_PATH"] = os.pathsep.join(
            [replay_owner.as_posix(), *local_search_roots]
        )
        if bound_provider_source is not None:
            assert imported_provider_module is not None
            provider_relative, provider_bytes = bound_provider_source
            provider_source = replay_project / provider_relative
            provider_source.parent.mkdir(parents=True, exist_ok=True)
            provider_source.write_bytes(provider_bytes)
            provider_output = replay_owner / Path(
                *imported_provider_module.split(".")
            ).with_suffix(".olean")
            provider_output.parent.mkdir(parents=True, exist_ok=True)
            compiled = _run_bound_toolchain_command(
                command_runner,
                tool_root,
                [
                    "--trust=0", "-o", provider_output.as_posix(),
                    provider_source.as_posix(),
                ],
                expected_lean_sha256=sha256(lean_binary),
                expected_lake_sha256=sha256(lake_binary),
                cwd=replay_project,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=LEAN_REPLAY_TIMEOUT_SECONDS,
                check=False,
                shell=False,
                env=replay_env,
            )
            if compiled.returncode != 0:
                detail = (
                    compiled.stderr.decode("utf-8", "replace").strip()
                    or compiled.stdout.decode("utf-8", "replace").strip()
                )
                fail(
                    "bound provider Lean source failed to compile: "
                    + (detail or imported_provider_module)
                )
        # Compile the full explicitly bound theorem-owned tree. Local imports
        # resolve only from this replay root, never from an unbound worktree file.
        dependencies: dict[str, set[str]] = {}
        for module, (pure, data) in source_by_module.items():
            imports = local_imports(data, f"bound Lean source {module}")
            dependencies[module] = {
                resolved for imported in imports
                if (resolved := resolve_bound_import(
                    imported, current_module=module, available=source_by_module
                )) is not None
            }
            missing_local = {
                imported for imported in imports
                if resolve_bound_import(
                    imported, current_module=module, available=source_by_module
                ) is None
                and not (
                    replay_owner / Path(*imported.split("."))
                ).with_suffix(".olean").is_file()
                and not (cache / "build/lib/lean" / Path(*imported.split("."))).with_suffix(".olean").is_file()
            }
            if missing_local:
                fail("proof replay has an unbound or unavailable import")
        ordered: list[str] = []
        remaining = {module: set(values) for module, values in dependencies.items()}
        while remaining:
            ready = sorted(module for module, values in remaining.items() if not values)
            if not ready:
                fail("bound target-owned Lean imports contain a cycle")
            for module in ready:
                ordered.append(module)
                del remaining[module]
            for values in remaining.values():
                values.difference_update(ready)
        for module in ordered:
            pure, _ = source_by_module[module]
            sibling = replay_project / pure.as_posix()
            output = replay_owner / Path(*module.split(".")).with_suffix(".olean")
            output.parent.mkdir(parents=True, exist_ok=True)
            compiled = _run_bound_toolchain_command(
                command_runner,
                tool_root,
                ["--trust=0", "-o", output.as_posix(), sibling.as_posix()],
                expected_lean_sha256=sha256(lean_binary),
                expected_lake_sha256=sha256(lake_binary),
                cwd=replay_project,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=LEAN_REPLAY_TIMEOUT_SECONDS,
                check=False,
                shell=False,
                env=replay_env,
            )
            if compiled.returncode != 0:
                detail = (
                    compiled.stderr.decode("utf-8", "replace").strip()
                    or compiled.stdout.decode("utf-8", "replace").strip()
                )
                fail(
                    "bound target-owned Lean source failed to compile: "
                    + (detail or module)
                )
        probe = replay_owner / "AuthorityProbe.lean"
        probe_prefix = (
            f"import {imported_provider_module}\n".encode("utf-8")
            if imported_provider_module is not None
            and imported_provider_module != source_module
            else b""
        )
        probe.write_bytes(
            probe_prefix + authority_probe_source(source_module, declarations)
        )
        try:
            authority_result = _run_bound_toolchain_command(
                command_runner,
                tool_root,
                ["--trust=0", probe.as_posix()],
                expected_lean_sha256=sha256(lean_binary),
                expected_lake_sha256=sha256(lake_binary),
                cwd=replay_project,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=LEAN_REPLAY_TIMEOUT_SECONDS,
                check=False,
                shell=False,
                env=replay_env,
            )
        except subprocess.TimeoutExpired as exc:
            raise ValidationError("Lean authority replay timed out") from exc
        dependency_result: subprocess.CompletedProcess[bytes] | None = None
        dependency_payload: dict[str, str] | None = None
        if dependency_probe is not None:
            consumer_declaration, provider_declaration, provider_module = dependency_probe
            dependency_probe_file = replay_owner / "AuthorityDependencyProbe.lean"
            dependency_probe_file.write_bytes(
                (
                    f"import {imported_provider_module}\n".encode("utf-8")
                    if imported_provider_module is not None
                    and imported_provider_module != source_module
                    else b""
                ) + declaration_dependency_probe_source(
                    source_module,
                    consumer_declaration=consumer_declaration,
                    provider_declaration=provider_declaration,
                    provider_module=provider_module,
                    verify_provider_module=not provider_is_local_vendored,
                )
            )
            try:
                dependency_result = _run_bound_toolchain_command(
                    command_runner,
                    tool_root,
                    ["--trust=0", dependency_probe_file.as_posix()],
                    expected_lean_sha256=sha256(lean_binary),
                    expected_lake_sha256=sha256(lake_binary),
                    cwd=replay_project,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=LEAN_REPLAY_TIMEOUT_SECONDS,
                    check=False,
                    shell=False,
                    env=replay_env,
                )
            except subprocess.TimeoutExpired as exc:
                raise ValidationError("Lean dependency probe timed out") from exc
            if dependency_result.returncode != 0:
                detail = (
                    dependency_result.stderr.decode("utf-8", "replace").strip()
                    or dependency_result.stdout.decode("utf-8", "replace").strip()
                )
                fail(
                    "consumer proof body does not depend on the admitted provider: "
                    + (detail or provider_declaration)
                )
            expected_relation = (
                "provider_constant_identity"
                if consumer_declaration == provider_declaration
                else "direct_proof_body_constant_dependency"
            )
            expected_payload = {
                "schema": DEPENDENCY_PROBE_SCHEMA,
                "consumer": consumer_declaration,
                "provider": provider_declaration,
                "provider_module": provider_module,
                "relation": expected_relation,
            }
            try:
                dependency_lines = dependency_result.stdout.decode("utf-8").splitlines()
            except UnicodeDecodeError as exc:
                raise ValidationError("Lean dependency probe output is not UTF-8") from exc
            matches = [
                strict_object(line.encode("utf-8"), "Lean dependency probe row")
                for line in dependency_lines
                if line.startswith("{") and line.endswith("}")
            ]
            if matches != [expected_payload]:
                fail("Lean dependency probe did not emit its exact authority row")
            dependency_payload = expected_payload
    # The exact paths invoked above must still contain the bytes bound before
    # the first execution. This closes both PATH substitution and replacement
    # during replay; a changed executable never becomes authority evidence.
    if (
        exact_file(lean_executable, "Lean executable") != lean_binary
        or exact_file(lake_executable, "Lake executable") != lake_binary
    ):
        fail("pinned Lean/Lake executable changed during replay")
    if authority_result.returncode != 0:
        detail = (
            authority_result.stderr.decode("utf-8", "replace").strip()
            or authority_result.stdout.decode("utf-8", "replace").strip()
        )
        fail(f"Lean authority replay failed: {detail or 'no diagnostic'}")
    types, axioms = parse_probe_output(authority_result.stdout, declarations)
    unexpected = sorted(
        {axiom for values in axioms.values() for axiom in values} - ALLOWED_AXIOMS
    )
    if unexpected:
        fail("Lean authority replay found unpermitted axioms: " + ", ".join(unexpected))
    replay_facts: dict[str, Any] = {
        "toolchain": toolchain,
        "toolchain_file_sha256": sha256(toolchain_bytes),
        "dependency_lock_sha256": sha256(lock_bytes),
        "dependency_packages_sha256": dependency_packages_sha256,
        "toolchain_closure_sha256": toolchain_closure_sha256,
        "toolchain_closure_file_count": toolchain_closure_file_count,
        "toolchain_closure_bytes": toolchain_closure_bytes,
        "compiled_cache_sha256": compiled_cache_sha256,
        "compiled_cache_file_count": compiled_cache_file_count,
        "compiled_cache_bytes": compiled_cache_bytes,
        "lean_binary_sha256": sha256(lean_binary),
        "lake_binary_sha256": sha256(lake_binary),
        "source_path": relative_source,
        "source_sha256": sha256(source_bytes),
        "declaration_type_sha256s": types,
        "declaration_axioms": axioms,
        "stdout_sha256": sha256(authority_result.stdout),
        "stderr_sha256": sha256(authority_result.stderr),
        "network_policy": "denied",
        "repository_access": "read_only",
        "trust_level": 0,
    }
    if dependency_payload is not None and dependency_result is not None:
        replay_facts["provider_dependency"] = dependency_payload
        replay_facts["provider_dependency_stdout_sha256"] = sha256(dependency_result.stdout)
        replay_facts["provider_dependency_stderr_sha256"] = sha256(dependency_result.stderr)
    if imported_provider_module is not None and imported_provider_declaration is not None:
        replay_facts["provider_import"] = {
            "module": imported_provider_module,
            "declaration": imported_provider_declaration,
            "repository": imported_provider_repository,
            "revision": imported_provider_revision,
            "closure": (
                "exact_vendored_source"
                if provider_is_local_vendored
                else "pinned_lake_dependency"
            ),
        }
    return replay_facts


def replay_checked_transports(
    ledger: Mapping[str, Any],
    *,
    theorem_id: str,
    artifacts: list[dict[str, Any]],
    lean_authority: Mapping[str, Any],
    bound_sources: Mapping[str, bytes],
) -> list[dict[str, Any]]:
    """Replay every consumer-owned checked transport from content-bound evidence."""
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("proof dependency reuse ledger schema is unsupported")
    if ledger.get("consumer_theorem_id") != theorem_id:
        fail("proof dependency reuse ledger consumer identity is stale")
    decisions = ledger.get("reuse_decisions")
    inspections = ledger.get("inspections")
    unresolved = ledger.get("unresolved_compatibility_obligations")
    if not isinstance(decisions, list) or not isinstance(inspections, list):
        fail("proof dependency reuse ledger decisions are malformed")
    if (
        not isinstance(unresolved, list)
        or any(not isinstance(value, str) or not value for value in unresolved)
        or len(unresolved) != len(set(unresolved))
    ):
        fail("proof dependency reuse ledger unresolved compatibility list is malformed")

    artifact_rows: dict[str, list[Mapping[str, Any]]] = {}
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            fail("checked transport artifact binding is malformed")
        path = artifact.get("path")
        if not isinstance(path, str):
            fail("checked transport artifact binding path is malformed")
        artifact_rows.setdefault(path, []).append(artifact)

    def target_file(
        raw_path: Any, owner: str, label: str, *, suffix: str | None = None
    ) -> Path:
        if not isinstance(raw_path, str):
            fail(f"{label} path is malformed")
        pure = PurePosixPath(raw_path)
        expected = PurePosixPath("Stage1_Instances", owner)
        try:
            within_owner = pure.relative_to(expected)
        except ValueError:
            fail(f"{label} escapes its theorem owner")
        if not within_owner.parts or (suffix is not None and pure.suffix != suffix):
            fail(f"{label} path is not an owned {suffix or 'file'}")
        return safe_path(raw_path, label)

    def bound_artifact(
        reference: Any, *, owner: str, roles: set[str], label: str,
        suffix: str | None = None,
    ) -> tuple[Path, str, bytes]:
        if not isinstance(reference, Mapping) or set(reference) != ARTIFACT_REFERENCE_KEYS:
            fail(f"{label} reference schema is not exact")
        relative = reference.get("path")
        digest = reference.get("sha256")
        if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
            fail(f"{label} digest is malformed")
        path = target_file(relative, owner, label, suffix=suffix)
        data = exact_file(path, label)
        if sha256(data) != digest:
            fail(f"{label} digest is stale")
        matches = [
            row for row in artifact_rows.get(str(relative), [])
            if row.get("sha256") == digest and row.get("role") in roles
        ]
        if len(matches) != 1 or len(artifact_rows.get(str(relative), [])) != 1:
            fail(f"{label} is not uniquely content-bound by the phase artifact map")
        return path, digest, data

    def positive_commands(value: Any, label: str) -> None:
        if not isinstance(value, list) or not value:
            fail(f"{label} lacks successful replay commands")
        for command in value:
            if isinstance(command, str):
                if not command.strip():
                    fail(f"{label} has an empty replay command")
            elif isinstance(command, Mapping):
                argv = command.get("argv")
                if (
                    command.get("exit_code") != 0
                    or not isinstance(argv, list)
                    or not argv
                    or any(not isinstance(token, str) or not token for token in argv)
                ):
                    fail(f"{label} has a nonpositive replay command")
            else:
                fail(f"{label} has a malformed replay command")

    def node_receipt(
        reference: Any, *, owner: str, phases: set[str], label: str,
        require_artifact_role: bool, current_receipt: bool,
    ) -> tuple[dict[str, Any], str]:
        if not isinstance(reference, Mapping) or set(reference) != RECEIPT_REFERENCE_KEYS:
            fail(f"{label} reference schema is not exact")
        relative = reference.get("path")
        receipt_id = reference.get("receipt_id")
        digest = reference.get("sha256")
        if (
            not isinstance(receipt_id, str)
            or not receipt_id
            or not isinstance(digest, str)
            or SHA256_RE.fullmatch(digest) is None
        ):
            fail(f"{label} reference identity or digest is malformed")
        path = target_file(relative, owner, label, suffix=".json")
        data = exact_file(path, label)
        if sha256(data) != digest:
            fail(f"{label} reference digest is stale")
        if require_artifact_role:
            matches = [
                row for row in artifact_rows.get(str(relative), [])
                if row.get("sha256") == digest and row.get("role") == "provider_material"
            ]
            if len(matches) != 1 or len(artifact_rows.get(str(relative), [])) != 1:
                fail(f"{label} is not uniquely bound as provider material")
        receipt = strict_object(data, label)
        phase = receipt.get("phase")
        retained_provider = {
            "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
            "base_revision", "inputs", "support_state", "accepted", "verdict",
            "selftest_status", "selftest_result",
        }
        current_common = {
            "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
            "intent", "base_revision", "base_tree", "inputs", "support_state",
            "proposed_state", "accepted", "verdict", "selftest_status",
            "selftest_result", "known_failures", "first_failed_gate",
            "retry_condition", "status_boundary", "audit_complete",
            "theorem_complete", "invalidation_inputs",
        }
        selftest = receipt.get("selftest_result")
        positive_accepted = (
            receipt.get("accepted") is True
            and receipt.get("support_state") in {"accepted", "master_accepted"}
        )
        positive_provisional = (
            receipt.get("accepted") is False
            and receipt.get("support_state") == "provisional_worker_selftest"
            and receipt.get("proposed_state") == "[_]"
        )
        if (
            not retained_provider <= set(receipt)
            or (current_receipt and not current_common <= set(receipt))
            or receipt.get("schema_version") != "stage1-node-receipt/1.0"
            or receipt.get("receipt_id") != receipt_id
            or receipt.get("theorem_id") != owner
            or phase not in phases
            or receipt.get("item_id")
            != f"S56-{owner.removeprefix('THM-')}-{str(phase).upper()}"
            or not isinstance(receipt.get("base_revision"), str)
            or not receipt["base_revision"]
            or (
                current_receipt
                and (
                    not isinstance(receipt.get("base_tree"), str)
                    or re.fullmatch(r"[0-9a-f]{40,64}", receipt["base_tree"]) is None
                )
            )
            or not isinstance(receipt.get("inputs"), Mapping)
            or not receipt["inputs"]
            or not (positive_accepted or positive_provisional)
            or receipt.get("verdict") not in {"accepted", "passed", "no_state_change"}
            or receipt.get("selftest_status") != "passed"
            or not isinstance(selftest, Mapping)
            or selftest.get("exit_code") != 0
            or ("known_failures" in receipt and receipt.get("known_failures") != [])
            or ("first_failed_gate" in receipt and receipt.get("first_failed_gate") not in {None, ""})
            or (
                current_receipt
                and (
                    not isinstance(receipt.get("status_boundary"), str)
                    or not receipt["status_boundary"]
                    or not isinstance(receipt.get("audit_complete"), bool)
                    or not isinstance(receipt.get("theorem_complete"), bool)
                    or not isinstance(receipt.get("invalidation_inputs"), list)
                )
            )
        ):
            fail(f"{label} does not prove a complete positive node receipt")
        positive_commands(selftest.get("commands"), label)
        return receipt, str(relative)

    seen_sources: set[str] = set()
    for index, decision in enumerate(decisions):
        if not isinstance(decision, Mapping):
            fail(f"dependency reuse decision {index} is malformed")
        source_id = decision.get("source_id")
        if (
            not isinstance(source_id, str)
            or not source_id
            or source_id in seen_sources
        ):
            fail("dependency reuse decisions contain a missing or duplicate source_id")
        seen_sources.add(source_id)

    results: list[dict[str, Any]] = []
    for index, decision in enumerate(decisions):
        if decision.get("decision") != "reused_with_transport":
            continue
        keys = set(decision)
        if (
            keys != TRANSPORT_DECISION_KEYS
            and keys != TRANSPORT_DECISION_KEYS | {"consumer_validation_receipts"}
        ):
            fail(f"checked transport decision {index} schema is not exact")
        provider = decision.get("provider_theorem_id")
        wrapper = decision.get("consumer_import_or_wrapper")
        provider_declaration = decision.get("terminal_proof_body_id")
        provider_import_module = decision.get("provider_import_module")
        provider_fingerprint = decision.get("provider_statement_fingerprint")
        consumer_fingerprint = decision.get("consumer_required_fingerprint")
        context_digest = decision.get("context_digest")
        if (
            not isinstance(provider, str)
            or re.fullmatch(r"THM-M-[0-9]{4}", provider) is None
            or decision.get("relationship") != "checked_transport"
            or decision.get("provider_proof_state") not in V2_PHASE_STATES
            or not isinstance(wrapper, str)
            or DECLARATION_RE.fullmatch(wrapper) is None
            or not isinstance(provider_declaration, str)
            or DECLARATION_RE.fullmatch(provider_declaration) is None
            or not isinstance(provider_import_module, str)
            or DECLARATION_RE.fullmatch(provider_import_module) is None
            or not isinstance(provider_fingerprint, str)
            or SHA256_RE.fullmatch(provider_fingerprint) is None
            or not isinstance(consumer_fingerprint, str)
            or SHA256_RE.fullmatch(consumer_fingerprint) is None
            or provider_fingerprint == consumer_fingerprint
            or not isinstance(context_digest, str)
            or SHA256_RE.fullmatch(context_digest) is None
            or context_digest != ledger.get("dependency_context_sha256")
            or any(
                not isinstance(decision.get(field), str) or not decision[field]
                for field in (
                    "consumer_obligation_id", "provider_obligation_id", "source_id"
                )
            )
        ):
            fail(f"checked transport decision {index} identity or fingerprints are invalid")
        if unresolved:
            fail("checked transport cannot carry unresolved compatibility obligations")

        provider_path, provider_digest, provider_bytes = bound_artifact(
            decision.get("provider_body_source"),
            owner=provider,
            roles={"provider_material"},
            label="checked transport provider source",
            suffix=".lean",
        )
        consumer_path, consumer_digest, consumer_bytes = bound_artifact(
            decision.get("consumer_import_source"),
            owner=theorem_id,
            roles={"proof_sources"},
            label="checked transport consumer source",
            suffix=".lean",
        )
        if bound_sources.get(consumer_path.as_posix()) != consumer_bytes:
            fail("checked transport consumer source is absent from the bound replay closure")

        inspection_matches = [
            row for row in inspections
            if isinstance(row, Mapping) and row.get("theorem_id") == provider
        ]
        if len(inspection_matches) != 1:
            fail("checked transport lacks exactly one provider compatibility inspection")
        inspection = inspection_matches[0]
        phase_states = inspection.get("phase_states")
        artifact_digests = inspection.get("artifact_digests")
        if (
            inspection.get("compatibility") != "checked_transport"
            or not isinstance(phase_states, Mapping)
            or set(phase_states) != PHASES
            or set(phase_states.values()) - V2_PHASE_STATES
            or phase_states.get("proof") != decision.get("provider_proof_state")
            or not isinstance(artifact_digests, Mapping)
            or artifact_digests.get(provider_path.as_posix()) != provider_digest
        ):
            fail("checked transport provider inspection is stale or incompatible")

        provider_references = decision.get("provider_receipts")
        if not isinstance(provider_references, list) or not provider_references:
            fail("checked transport lacks provider receipt bindings")
        provider_receipts: list[dict[str, Any]] = []
        provider_receipt_ids: set[str] = set()
        for receipt_index, reference in enumerate(provider_references):
            receipt, _ = node_receipt(
                reference,
                owner=provider,
                phases={"proof", "validation", "release"},
                label=f"checked transport provider receipt {receipt_index}",
                require_artifact_role=True,
                current_receipt=False,
            )
            if receipt["receipt_id"] in provider_receipt_ids:
                fail("checked transport provider receipt bindings contain duplicates")
            provider_receipt_ids.add(receipt["receipt_id"])
            provider_receipts.append(receipt)
        proof_bindings = []
        for receipt in provider_receipts:
            if receipt.get("phase") != "proof":
                continue
            exact_declarations = receipt.get("exact_declarations")
            proof_body = receipt.get("proof_body")
            proof_result = receipt.get("result")
            if (
                receipt.get("intent") not in {"integrate", "frontier_prove"}
                or not isinstance(exact_declarations, list)
                or provider_declaration not in exact_declarations
                or len(exact_declarations) != len(set(exact_declarations))
                or not isinstance(proof_body, Mapping)
                or proof_body.get("source") != provider_path.as_posix()
                or proof_body.get("source_sha256") != provider_digest
                or not isinstance(proof_result, Mapping)
                or proof_result.get("exit_code") != 0
                or not isinstance(proof_result.get("axioms"), list)
                or set(proof_result["axioms"]) - ALLOWED_AXIOMS
            ):
                continue
            declared_types = proof_result.get("declaration_type_sha256s")
            if declared_types is not None and (
                not isinstance(declared_types, Mapping)
                or declared_types.get(provider_declaration) != provider_fingerprint
            ):
                fail("checked transport provider receipt fingerprint is stale")
            proof_bindings.append(receipt)
        if len(proof_bindings) != 1:
            fail("checked transport lacks exactly one positive provider proof binding")

        try:
            consumer_text = consumer_bytes.decode("utf-8")
            provider_text = provider_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError("checked transport Lean sources are not UTF-8") from exc
        stripped_consumer = re.sub(
            r'(?s)/-.*?-/|--[^\n]*|"(?:\\.|[^"\\])*"', "", consumer_text
        )
        stripped_provider = re.sub(
            r'(?s)/-.*?-/|--[^\n]*|"(?:\\.|[^"\\])*"', "", provider_text
        )
        if (
            re.search(
                rf"\b(?:theorem|lemma|def|abbrev)\s+{re.escape(wrapper.rsplit('.', 1)[-1])}\b",
                stripped_consumer,
            )
            is None
            or provider_declaration not in stripped_consumer
            or re.search(
                rf"\b(?:theorem|lemma|def|abbrev)\s+{re.escape(provider_declaration.rsplit('.', 1)[-1])}\b",
                stripped_provider,
            )
            is None
        ):
            fail("checked transport source does not bind its wrapper and provider declaration")

        validation_references = decision.get("consumer_validation_receipts", [])
        if not isinstance(validation_references, list):
            fail("checked transport consumer validation receipts are malformed")
        validation_receipt_ids: set[str] = set()
        for receipt_index, reference in enumerate(validation_references):
            receipt, _ = node_receipt(
                reference,
                owner=theorem_id,
                phases={"validation"},
                label=f"checked transport consumer validation receipt {receipt_index}",
                require_artifact_role=False,
                current_receipt=True,
            )
            if receipt["receipt_id"] in validation_receipt_ids:
                fail("checked transport consumer validation receipt bindings contain duplicates")
            validation_receipt_ids.add(receipt["receipt_id"])
            result = receipt.get("result")
            kernel = result.get("kernel_replay") if isinstance(result, Mapping) else None
            if (
                receipt.get("intent") != "validate"
                or not isinstance(result, Mapping)
                or result.get("exit_code") != 0
                or result.get("semantic_verdict") != "passed"
                or not isinstance(kernel, Mapping)
                or kernel.get("source") != consumer_path.as_posix()
                or not isinstance(kernel.get("declarations"), list)
                or wrapper not in kernel["declarations"]
                or len(kernel["declarations"]) != len(set(kernel["declarations"]))
                or not isinstance(kernel.get("declaration_type_sha256s"), Mapping)
                or kernel["declaration_type_sha256s"].get(wrapper) != consumer_fingerprint
            ):
                fail("checked transport consumer validation receipt does not bind the wrapper replay")

        replay = readonly_lean_replay(
            consumer_path,
            [wrapper],
            dependency_packages_sha256=lean_authority["dependency_packages_sha256"],
            toolchain_closure_sha256=lean_authority["toolchain_closure_sha256"],
            toolchain_closure_file_count=lean_authority["toolchain_closure_file_count"],
            toolchain_closure_bytes=lean_authority["toolchain_closure_bytes"],
            compiled_cache_sha256=lean_authority["compiled_cache_sha256"],
            compiled_cache_file_count=lean_authority["compiled_cache_file_count"],
            compiled_cache_bytes=lean_authority["compiled_cache_bytes"],
            bound_sources=bound_sources,
            dependency_probe=(wrapper, provider_declaration, provider_import_module),
            imported_provider=(
                provider_import_module,
                provider_declaration,
                f"stage1-local://{provider}",
                "0" * 40,
            ),
            bound_provider_source=(provider_path.as_posix(), provider_bytes),
        )
        authority_fields = {
            "toolchain", "toolchain_file_sha256", "dependency_lock_sha256",
            "dependency_packages_sha256", "toolchain_closure_sha256",
            "toolchain_closure_file_count", "toolchain_closure_bytes",
            "compiled_cache_sha256", "compiled_cache_file_count",
            "compiled_cache_bytes", "lean_binary_sha256", "lake_binary_sha256",
        }
        if (
            any(replay.get(field) != lean_authority.get(field) for field in authority_fields)
            or replay.get("source_path") != consumer_path.as_posix()
            or replay.get("source_sha256") != consumer_digest
            or replay.get("declaration_type_sha256s") != {wrapper: consumer_fingerprint}
            or replay.get("provider_dependency") != {
                "schema": DEPENDENCY_PROBE_SCHEMA,
                "consumer": wrapper,
                "provider": provider_declaration,
                "provider_module": provider_import_module,
                "relation": "direct_proof_body_constant_dependency",
            }
            or not isinstance(replay.get("declaration_axioms"), Mapping)
            or set(replay["declaration_axioms"]) != {wrapper}
            or not isinstance(replay["declaration_axioms"][wrapper], list)
            or set(replay["declaration_axioms"][wrapper]) - ALLOWED_AXIOMS
            or replay.get("network_policy") != "denied"
            or replay.get("repository_access") != "read_only"
            or replay.get("trust_level") != 0
        ):
            fail("checked transport Lean replay disagrees with its consumer type or authority")
        results.append({
            "source_id": decision["source_id"],
            "provider_theorem_id": provider,
            "provider_statement_fingerprint": provider_fingerprint,
            "consumer_wrapper": wrapper,
            "consumer_statement_fingerprint": consumer_fingerprint,
            "consumer_source_sha256": consumer_digest,
            "provider_dependency_proven": True,
            "provider_receipt_count": len(provider_receipts),
            "consumer_validation_receipt_count": len(validation_references),
        })
    return results


def pointer(document: dict[str, Any], value: Any) -> Any:
    if not isinstance(value, str) or not value.startswith("/"):
        fail("contract receipt pointer is malformed")
    current: Any = document
    for raw in value[1:].split("/"):
        component = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and component in current:
            current = current[component]
        elif isinstance(current, list) and component.isdecimal() and int(component) < len(current):
            current = current[int(component)]
        else:
            fail(f"phase receipt is missing {value}")
    return current


def require_focus_semantic_bindings(
    phase: str,
    receipt: Mapping[str, Any],
    focus: Mapping[str, Any],
    phase_row: Mapping[str, Any],
) -> None:
    """Require every phase receipt to preserve one permitted focus contract."""
    disposition = focus.get("execution_disposition")
    expected_focus_keys = (
        INTEGRATION_FOCUS_KEYS
        if disposition == "organize_or_integrate"
        else BASE_FOCUS_KEYS
    )
    expected_intent: Any = phase_row.get("intent")
    if isinstance(expected_intent, Mapping):
        expected_intent = expected_intent.get(disposition)
    phase_allowed = (
        disposition in {"organize_or_integrate", "frontier_exception"}
        or disposition == "research_required" and phase in RESEARCH_PHASES
    )
    integration_source = focus.get("exact_machine_source")
    integration_shape_valid = (
        disposition != "organize_or_integrate"
        or valid_exact_machine_source(integration_source)
        and focus.get("machine_evidence_class") in {
            "exact_pinned_closure", "exact_external_unintegrated"
        }
        and focus.get("exact_machine_source_used") is True
        and focus.get("introduced_root_critical_proof") is False
    )
    if (
        not phase_allowed
        or not integration_shape_valid
        or set(focus) != expected_focus_keys
        or any(
            not isinstance(focus.get(key), str)
            or SHA256_RE.fullmatch(str(focus[key])) is None
            for key in ("focus_contract_sha256", "receipt_sha256")
        )
        or not isinstance(expected_intent, str)
        or receipt.get("intent") != expected_intent
        or receipt.get("focus_execution") != focus
    ):
        fail("phase receipt is not exactly bound to a permitted focus contract")


def require_proof_semantic_bindings(
    receipt: Mapping[str, Any],
    focus: Mapping[str, Any],
    proof_sources: list[dict[str, Any]],
) -> tuple[list[str], str, list[str]]:
    """Bind proof credit to focus, source bytes, declarations, and obligations."""
    disposition = focus.get("execution_disposition")
    expected_intent = {
        "organize_or_integrate": "integrate",
        "frontier_exception": "frontier_prove",
    }.get(disposition)
    if expected_intent is None:
        fail("current focus disposition does not permit proof execution")
    if (
        receipt.get("intent") != expected_intent
        or receipt.get("focus_execution") != focus
    ):
        fail("proof receipt is not exactly bound to the admitted focus contract")
    declarations = receipt.get("exact_declarations")
    target = receipt.get("canonical_target")
    closed = receipt.get("closed_obligation_ids")
    bindings = receipt.get("obligation_bindings")
    proof_body = receipt.get("proof_body")
    result = receipt.get("result")
    if (
        not isinstance(declarations, list)
        or not declarations
        or any(
            not isinstance(value, str) or DECLARATION_RE.fullmatch(value) is None
            for value in declarations
        )
        or len(declarations) != len(set(declarations))
        or not isinstance(target, str)
        or target not in declarations
        or not isinstance(closed, list)
        or not closed
        or any(not isinstance(value, str) or not value for value in closed)
        or len(closed) != len(set(closed))
        or not isinstance(bindings, dict)
        or set(bindings) != set(closed)
        or any(value not in declarations for value in bindings.values())
        or target not in bindings.values()
        or not isinstance(proof_body, dict)
        or not isinstance(proof_body.get("source"), str)
        or not isinstance(proof_body.get("source_sha256"), str)
        or SHA256_RE.fullmatch(proof_body["source_sha256"]) is None
        or not isinstance(result, dict)
        or result.get("exit_code") != 0
        or not isinstance(result.get("axioms"), list)
        or any(not isinstance(value, str) for value in result["axioms"])
    ):
        fail("proof receipt does not bind kernel declarations to closed obligations")
    source_matches = [
        row for row in proof_sources
        if row.get("path") == proof_body["source"]
        and row.get("sha256") == proof_body["source_sha256"]
    ]
    if len(source_matches) != 1:
        fail("proof body is not content-bound to exactly one proof source")
    return declarations, target, result["axioms"]


def nonempty_strings(value: Any, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(row, str) or not row for row in value)
        or len(value) != len(set(value))
    ):
        fail(f"{label} must be a nonempty duplicate-free string list")
    return value


def json_artifact(
    role: str,
    actual_roles: Mapping[str, list[dict[str, Any]]],
    artifact_bytes: Mapping[str, bytes],
) -> dict[str, Any]:
    rows = actual_roles.get(role, [])
    if len(rows) != 1:
        fail(f"semantic gate requires exactly one {role} artifact")
    return strict_object(artifact_bytes[str(rows[0]["path"])], role)


def text_artifact(
    role: str,
    actual_roles: Mapping[str, list[dict[str, Any]]],
    artifact_bytes: Mapping[str, bytes],
) -> str:
    rows = actual_roles.get(role, [])
    if len(rows) != 1:
        fail(f"semantic gate requires exactly one {role} artifact")
    try:
        text = artifact_bytes[str(rows[0]["path"])].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{role} is not UTF-8") from exc
    if not text.strip():
        fail(f"{role} is empty")
    return text


def require_identity(value: Mapping[str, Any], item: str, theorem: str, label: str) -> None:
    if value.get("item_id") != item or value.get("theorem_id") != theorem:
        fail(f"{label} identity disagrees with the selected item")


def require_hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        fail(f"{label} is not a sha256 digest")
    return value


def semantic_gate_ids(phase_row: Mapping[str, Any], expected: list[str]) -> None:
    rows = phase_row.get("semantic_gates")
    if (
        not isinstance(rows, list)
        or [row.get("gate_id") if isinstance(row, Mapping) else None for row in rows]
        != expected
    ):
        fail("phase semantic gate contract is missing, reordered, or unsupported")


def binding_paths_at_pointer(receipt: Mapping[str, Any], raw_pointer: Any) -> set[str]:
    if raw_pointer is None:
        return set()
    value = pointer(dict(receipt), raw_pointer)
    rows = value if isinstance(value, list) else [value]
    paths: set[str] = set()
    for row in rows:
        if not isinstance(row, Mapping) or not isinstance(row.get("path"), str):
            fail(f"receipt artifact binding at {raw_pointer} is malformed")
        if row["path"] in paths:
            fail(f"receipt artifact binding at {raw_pointer} contains duplicates")
        require_hash(row.get("sha256"), f"receipt artifact binding at {raw_pointer}")
        paths.add(row["path"])
    return paths


def enforce_role_contract(
    phase_row: Mapping[str, Any],
    receipt: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]],
    theorem: str,
) -> None:
    declared_roles: set[str] = set()
    for declaration in phase_row.get("required_artifact_roles", []):
        if not isinstance(declaration, Mapping) or not isinstance(declaration.get("role"), str):
            fail("artifact role contract is malformed")
        role = declaration["role"]
        if role in declared_roles:
            fail("artifact role contract contains a duplicate role")
        declared_roles.add(role)
        rows = actual_roles.get(role, [])
        requirement = declaration.get("requirement")
        cardinality = declaration.get("cardinality")
        if requirement == "required" and not rows:
            fail(f"required artifact role {role} is absent")
        if cardinality == "exactly_one" and len(rows) != 1 and requirement == "required":
            fail(f"required exactly-one artifact role {role} is ambiguous")
        if cardinality == "exactly_one" and len(rows) > 1:
            fail(f"exactly-one artifact role {role} is ambiguous")
        if cardinality == "one_or_more" and requirement == "required" and len(rows) < 1:
            fail(f"required one-or-more artifact role {role} is absent")
        candidates = declaration.get("path_candidates")
        if isinstance(candidates, list) and candidates:
            allowed = {str(value).replace("{theorem_id}", theorem) for value in candidates}
            if any(str(row.get("path")) not in allowed for row in rows):
                fail(f"artifact role {role} does not use a contract path candidate")
        binding_pointer = declaration.get("binding_pointer")
        if binding_pointer is not None and rows:
            bound = binding_paths_at_pointer(receipt, binding_pointer)
            if bound != {str(row.get("path")) for row in rows}:
                fail(f"artifact role {role} disagrees with its receipt binding")
    if set(actual_roles) - declared_roles:
        fail("role map contains a role not declared by the selected phase contract")


def replay_declarations(
    source_binding: Mapping[str, Any],
    declarations: list[str],
    *,
    lean_authority: Mapping[str, Any],
    bound_sources: Mapping[str, bytes],
) -> dict[str, Any]:
    result = readonly_lean_replay(
        Path(str(source_binding["path"])),
        declarations,
        dependency_packages_sha256=lean_authority["dependency_packages_sha256"],
        toolchain_closure_sha256=lean_authority["toolchain_closure_sha256"],
        toolchain_closure_file_count=lean_authority["toolchain_closure_file_count"],
        toolchain_closure_bytes=lean_authority["toolchain_closure_bytes"],
        compiled_cache_sha256=lean_authority["compiled_cache_sha256"],
        compiled_cache_file_count=lean_authority["compiled_cache_file_count"],
        compiled_cache_bytes=lean_authority["compiled_cache_bytes"],
        bound_sources=bound_sources,
    )
    if (
        result.get("toolchain") != lean_authority["toolchain"]
        or result.get("toolchain_file_sha256") != lean_authority["toolchain_file_sha256"]
        or result.get("dependency_lock_sha256") != lean_authority["dependency_lock_sha256"]
        or result.get("dependency_packages_sha256")
        != lean_authority["dependency_packages_sha256"]
        or result.get("toolchain_closure_sha256")
        != lean_authority["toolchain_closure_sha256"]
        or result.get("toolchain_closure_file_count")
        != lean_authority["toolchain_closure_file_count"]
        or result.get("toolchain_closure_bytes") != lean_authority["toolchain_closure_bytes"]
        or result.get("compiled_cache_sha256") != lean_authority["compiled_cache_sha256"]
        or result.get("compiled_cache_file_count")
        != lean_authority["compiled_cache_file_count"]
        or result.get("compiled_cache_bytes") != lean_authority["compiled_cache_bytes"]
        or result.get("lean_binary_sha256") != lean_authority["lean_binary_sha256"]
        or result.get("lake_binary_sha256") != lean_authority["lake_binary_sha256"]
        or result.get("source_sha256") != source_binding.get("sha256")
    ):
        fail("Lean semantic replay disagrees with the bound authority or source")
    return result


def validate_intake_semantics(
    receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str,
) -> dict[str, Any]:
    semantic_gate_ids(phase_row, ["I01-ARTIFACTS", "I02-PLANNED-STATE", "I03-CONTENT"])
    instance = json_artifact("instance_manifest", actual_roles, artifact_bytes)
    dag = json_artifact("open_task_dag", actual_roles, artifact_bytes)
    scope = text_artifact("scope_map", actual_roles, artifact_bytes)
    crosswalk = text_artifact("source_crosswalk", actual_roles, artifact_bytes)
    require_identity(instance, item, theorem, "intake manifest")
    if (
        instance.get("schema_version") != "stage1-instance-intake/1.0"
        or instance.get("lifecycle_mode") != "planned"
        or instance.get("lifecycle") != "planned"
        or instance.get("theorem_complete") is not False
        or instance.get("audit_complete") is not False
        or receipt.get("intent") != "intake"
        or receipt.get("lifecycle_after") != "planned"
    ):
        fail("intake planned-state semantic gate failed")
    required = {
        "canonical_name", "canonical_statement", "canonical_formal_target",
        "domain_and_universes", "quantifiers", "hypotheses", "conclusion",
        "alternate_encodings", "excluded_degenerate_cases", "foundation_profile",
        "tcb_profile", "computation_profile", "formal_system", "source_revisions",
        "obligation_registry_hash", "discovery_protocol_hash", "public_merge_targets",
        "owners_and_reviewers", "freshness_and_revocation_policy", "status_boundary",
    }
    if not required <= set(instance):
        fail("intake manifest omits required section-5 semantics")
    if not isinstance(instance.get("canonical_name"), str) or not instance["canonical_name"].strip():
        fail("intake canonical name is empty")
    statement = instance.get("canonical_statement")
    formal = instance.get("canonical_formal_target")
    if not (
        isinstance(statement, str) and statement.strip()
        or (statement is None and formal is None and isinstance(instance.get("status_boundary"), str))
    ):
        fail("intake lacks a bounded claim or explicit open statement boundary")
    require_identity(dag, item, theorem, "open task DAG")
    tasks = dag.get("tasks")
    if (
        dag.get("schema_version") != "stage1-open-task-dag/1.0"
        or dag.get("lifecycle_mode") != "planned"
        or dag.get("lifecycle") != "planned"
        or dag.get("theorem_complete") is not False
        or not isinstance(tasks, list)
        or not tasks
    ):
        fail("intake open task DAG is incomplete")
    task_ids = [row.get("id") if isinstance(row, Mapping) else None for row in tasks]
    if any(not isinstance(value, str) or not value for value in task_ids) or len(task_ids) != len(set(task_ids)):
        fail("intake open task DAG has malformed task identities")
    known = set(task_ids) | {item}
    graph: dict[str, set[str]] = {}
    for row in tasks:
        dependencies = row.get("depends_on")
        if not isinstance(dependencies, list) or any(value not in known for value in dependencies):
            fail("intake open task DAG has an unknown dependency")
        graph[str(row["id"])] = set(dependencies) - {item}
        if row.get("state") not in {"open", "[ ]"}:
            fail("intake open task DAG claims accepted downstream state")
    remaining = dict(graph)
    while remaining:
        ready = [key for key, values in remaining.items() if not values]
        if not ready:
            fail("intake open task DAG contains a cycle")
        for key in ready:
            del remaining[key]
        for values in remaining.values():
            values.difference_update(ready)
    if theorem not in scope or theorem not in crosswalk:
        fail("intake scope or source crosswalk is not target-bound")
    return {"semantic_gates": ["I01-ARTIFACTS", "I02-PLANNED-STATE", "I03-CONTENT"]}


def validate_statement_semantics(
    receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str, lean_authority: Mapping[str, Any],
    bound_sources: Mapping[str, bytes],
) -> dict[str, Any]:
    semantic_gate_ids(phase_row, ["S01-ARTIFACTS", "S02-EXACT-TARGET", "S03-MUTATIONS"])
    record = json_artifact("statement_record", actual_roles, artifact_bytes)
    require_identity(record, item, theorem, "statement record")
    if (
        receipt.get("intent") != "audit"
        or record.get("schema_version") != "stage1-statement/1.0"
        or record.get("statement_elaborated") is not True
        or record.get("theorem_complete") is not False
        or record.get("audit_complete") is not False
    ):
        fail("statement record does not claim a positive statement-only boundary")
    target = record.get("canonical_formal_target")
    if not isinstance(target, Mapping):
        fail("statement record lacks its canonical formal target")
    declaration = target.get("declaration_or_expression")
    expected_type = target.get("elaborated_expression_sha256")
    if (
        target.get("backend") != "lean4"
        or not isinstance(declaration, str)
        or DECLARATION_RE.fullmatch(declaration) is None
        or not isinstance(expected_type, str)
        or SHA256_RE.fullmatch(expected_type) is None
    ):
        fail("statement canonical target binding is malformed")
    source_rows = actual_roles.get("statement_source", [])
    if len(source_rows) != 1:
        fail("statement phase requires one exact Lean source")
    source_path = str(source_rows[0]["path"])
    if target.get("module") != source_path:
        fail("statement record module disagrees with its bound source")
    source_sha = target.get("statement_file_sha256")
    if source_sha is not None and source_sha != source_rows[0]["sha256"]:
        fail("statement record source digest is stale")
    replay = replay_declarations(
        source_rows[0], [declaration], lean_authority=lean_authority,
        bound_sources=bound_sources,
    )
    if replay["declaration_type_sha256s"].get(declaration) != expected_type:
        fail("statement target type disagrees with independent Lean replay")
    fingerprints = nonempty_strings(receipt.get("statement_fingerprints"), "statement fingerprints")
    normalized = {expected_type, f"sha256:{expected_type}"}
    if len(fingerprints) != 1 or fingerprints[0] not in normalized:
        fail("statement receipt fingerprint disagrees with replay")
    required_mutations = [
        "removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case",
    ]
    for value, label in ((record.get("mutation_tests"), "statement record"),
                         (receipt.get("mutation_tests"), "statement receipt")):
        if not isinstance(value, Mapping):
            fail(f"{label} lacks mutation evidence")
        killed = value.get("killed", value.get("executed"))
        if not isinstance(killed, list):
            fail(f"{label} mutation evidence is malformed")
        kinds = [row.get("kind") if isinstance(row, Mapping) else None for row in killed]
        if sorted(kinds) != sorted(required_mutations):
            fail(f"{label} did not execute exactly the required mutation suite")
        mutation_hashes = [row.get("expression_sha256") for row in killed]
        if any(not isinstance(row, str) or SHA256_RE.fullmatch(row) is None for row in mutation_hashes):
            fail(f"{label} mutation fingerprints are malformed")
        if len(set(mutation_hashes + [expected_type])) != len(mutation_hashes) + 1:
            fail(f"{label} mutation suite did not distinguish the canonical target")
    return {
        "semantic_gates": ["S01-ARTIFACTS", "S02-EXACT-TARGET", "S03-MUTATIONS"],
        "statement_type_sha256": expected_type,
    }


def validate_anchor_semantics(
    receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str,
) -> dict[str, Any]:
    semantic_gate_ids(phase_row, ["A01-ARTIFACTS", "A02-DISCOVERY", "A03-CLASSIFICATION"])
    inventory = json_artifact("anchor_inventory", actual_roles, artifact_bytes)
    require_identity(inventory, item, theorem, "anchor inventory")
    if (
        receipt.get("intent") != "audit"
        or inventory.get("schema_version") != "stage1-anchor-audit/1.0"
        or inventory.get("audit_complete") is not False
        or inventory.get("theorem_complete") is not False
    ):
        fail("anchor inventory boundary is malformed")
    protocol_binding = inventory.get("discovery_protocol")
    if not isinstance(protocol_binding, Mapping):
        fail("anchor inventory lacks a content-bound discovery protocol")
    protocol_path = protocol_binding.get("path")
    protocol_digest = protocol_binding.get("sha256")
    protocol = strict_object(
        exact_file(safe_path(protocol_path, "anchor discovery protocol"), "anchor discovery protocol"),
        "anchor discovery protocol",
    )
    require_identity(protocol, item, theorem, "anchor discovery protocol")
    if sha256(canonical(protocol)) != protocol_digest:
        # Canonical and file-byte hashes are both common; require one exact representation.
        raw_protocol = exact_file(Path(str(protocol_path)), "anchor discovery protocol")
        if sha256(raw_protocol) != protocol_digest:
            fail("anchor discovery protocol digest is stale")
    expected_order = phase_row["semantic_gates"][1]["parameters"]["search_order"]
    observed_order = protocol.get("search_order")
    lane_terms = [
        ("repo", "local"), ("pinned", "mathlib"), ("official",),
        ("public",), ("statement",), ("historical",), ("human", "source"),
    ]
    if (
        protocol.get("schema_version") != "stage1-anchor-discovery-protocol/1.0"
        or not isinstance(observed_order, list)
        or len(observed_order) != len(expected_order)
        or any(
            not isinstance(row, str)
            or not all(term in row.lower() for term in terms)
            for terms, row in zip(lane_terms, observed_order)
        )
    ):
        fail("anchor discovery protocol does not cover the prescribed ordered lanes")
    if receipt.get("discovery_protocol_sha256") != protocol_digest:
        fail("anchor receipt does not bind the replayed discovery protocol")
    evidence_rows = actual_roles.get("discovery_evidence", [])
    if not evidence_rows:
        fail("anchor audit lacks discovery evidence")
    evidence_paths = {str(row["path"]) for row in evidence_rows}
    search_evidence = inventory.get("search_evidence")
    candidates = inventory.get("candidates")
    if not isinstance(search_evidence, list) or not search_evidence or not isinstance(candidates, list) or not candidates:
        fail("anchor inventory does not classify candidates and negative search evidence")
    for path in evidence_paths:
        if path != str(actual_roles["anchor_inventory"][0]["path"]):
            # Separate evidence must be receipt-bound; content is already digest checked above.
            pass
    allowed_states = set(phase_row["semantic_gates"][2]["parameters"]["machine_states"])
    prefixes = {state for state in allowed_states}
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            fail("anchor candidate classification is malformed")
        classification = candidate.get("candidate_classification")
        if not isinstance(classification, str) or not any(
            classification == state or classification.startswith(state + "_") for state in prefixes
        ):
            fail("anchor candidate uses an unsupported or missing machine classification")
        if not candidate.get("candidate_id") or not candidate.get("result"):
            fail("anchor candidate omits identity or result boundary")
    result = receipt.get("candidate_inventory_result")
    if not isinstance(result, Mapping) or result.get("inventory_version") != inventory.get("inventory_version"):
        fail("anchor receipt inventory summary is stale")
    if result.get("classified_candidate_groups") != len(candidates):
        fail("anchor receipt candidate count is not recomputed from the inventory")
    return {"semantic_gates": ["A01-ARTIFACTS", "A02-DISCOVERY", "A03-CLASSIFICATION"]}


def validate_obligation_tree_semantics(
    receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str, lean_authority: Mapping[str, Any],
    bound_sources: Mapping[str, bytes],
) -> dict[str, Any]:
    gates = ["T01-ARTIFACTS", "T02-REGISTRY", "T03-GRAPHS", "T04-COMPOSITION"]
    semantic_gate_ids(phase_row, gates)
    registry = json_artifact("obligation_registry", actual_roles, artifact_bytes)
    bundle = json_artifact("typed_graph_bundle", actual_roles, artifact_bytes)
    text_artifact("readable_tree", actual_roles, artifact_bytes)
    require_identity(registry, item, theorem, "obligation registry")
    require_identity(bundle, item, theorem, "typed graph bundle")
    if (
        receipt.get("intent") != "audit"
        or registry.get("schema_version") != "stage1-obligation-registry/1.0"
        or bundle.get("schema_version") != "stage1-typed-graphs/1.0"
    ):
        fail("obligation-tree artifact schema or intent is unsupported")
    obligations = registry.get("obligations")
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    if not isinstance(obligations, list) or not obligations:
        fail("obligation registry is empty")
    normalized: list[dict[str, Any]] = []
    ids: list[str] = []
    for row in obligations:
        if not isinstance(row, Mapping) or any(key not in row for key in fields):
            fail("obligation registry row is incomplete")
        identifier = row.get("obligation_id")
        if not isinstance(identifier, str) or not identifier:
            fail("obligation registry contains a malformed identity")
        ids.append(identifier)
        normalized.append({key: row[key] for key in fields})
    if len(ids) != len(set(ids)):
        fail("obligation registry contains duplicate identities")
    denominator = sha256(canonical(normalized))
    root = registry.get("root_obligation_id")
    if (
        root not in ids
        or registry.get("denominator_sha256") != denominator
        or bundle.get("registry_denominator_sha256") != denominator
        or receipt.get("registry_denominator_sha256") != denominator
        or receipt.get("canonical_obligation_ids") != ids
    ):
        fail("obligation denominator, root, or receipt inventory is stale")
    frozen = registry.get("frozen_denominators")
    layers = registry.get("mandatory_layer_analysis")
    if (
        not isinstance(frozen, Mapping)
        or frozen.get("inventory") != ids
        or not isinstance(layers, Mapping)
        or set(layers) != {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
        or any(not isinstance(value, list) for value in layers.values())
    ):
        fail("obligation frozen denominator or mandatory layers are incomplete")
    nodes = bundle.get("nodes")
    graphs = bundle.get("graphs")
    if not isinstance(nodes, list) or not isinstance(graphs, Mapping):
        fail("typed graph bundle has no nodes or graphs")
    node_ids = [row.get("obligation_id") if isinstance(row, Mapping) else None for row in nodes]
    if sorted(node_ids) != sorted(ids):
        fail("typed graph nodes do not exactly cover the obligation registry")
    for node in nodes:
        budget = node.get("step_budget")
        ledger = node.get("semantic_step_ledger")
        if (
            not isinstance(budget, int) or isinstance(budget, bool) or not 1 <= budget <= 100
            or not isinstance(ledger, list) or not ledger or len(ledger) > 100
            or any(
                not isinstance(step, Mapping)
                or not {"step_id", "premise_ids", "inference", "output"} <= set(step)
                for step in ledger
            )
        ):
            fail("typed graph node violates the substantive <=100-step ledger rule")
    expected_graphs = {
        "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow",
    }
    if set(graphs) != expected_graphs:
        fail("typed graph bundle does not contain exactly the seven graph families")
    reachable_edges: dict[str, set[str]] = {identifier: set() for identifier in ids}
    all_edges: dict[str, Mapping[str, Any]] = {}
    for name, graph in graphs.items():
        if not isinstance(graph, Mapping) or set(graph) != {"edges", "in", "out"}:
            fail("typed graph family schema is malformed")
        edges = graph["edges"]
        if not isinstance(edges, list):
            fail("typed graph edges are malformed")
        local: dict[str, Mapping[str, Any]] = {}
        for edge in edges:
            if not isinstance(edge, Mapping) or not isinstance(edge.get("edge_id"), str):
                fail("typed graph edge is malformed")
            edge_id = edge["edge_id"]
            if edge_id in local or edge_id in all_edges:
                fail("typed graph edge identity is duplicated")
            local[edge_id] = edge
            all_edges[edge_id] = edge
            source, target = edge.get("from"), edge.get("to")
            if name != "workflow" and (source not in ids or target not in ids):
                fail("typed graph edge has an unknown obligation endpoint")
            if name in {"proof", "refinement"} and source in ids and target in ids:
                reachable_edges[str(source)].add(str(target))
        for edge in edges:
            reciprocal_id = edge.get("reciprocal_edge_id")
            if reciprocal_id is not None:
                reciprocal = local.get(reciprocal_id)
                if (
                    reciprocal is None
                    or reciprocal.get("from") != edge.get("to")
                    or reciprocal.get("to") != edge.get("from")
                    or reciprocal.get("reciprocal_edge_id") != edge.get("edge_id")
                ):
                    fail("typed graph reciprocal edge is missing or inconsistent")
    reached = {str(root)}
    frontier = [str(root)]
    while frontier:
        for target in reachable_edges[frontier.pop()]:
            if target not in reached:
                reached.add(target)
                frontier.append(target)
    if reached != set(ids):
        fail("typed proof/refinement graphs contain an orphan or root-unreachable obligation")
    certificates = bundle.get("composition_certificates")
    if not isinstance(certificates, list):
        fail("typed graph composition certificates are malformed")
    receipt_certificates = receipt.get("composition_certificates")
    certificate_ids = [
        row.get("certificate_id") if isinstance(row, Mapping) else None for row in certificates
    ]
    if receipt_certificates != certificate_ids:
        fail("obligation receipt does not bind the exact composition certificate inventory")
    declarations: list[str] = []
    proof_edges = graphs["proof"]["edges"]
    for certificate in certificates:
        parent = certificate.get("parent_obligation_id")
        children = certificate.get("child_obligation_ids")
        declared = certificate.get("declarations")
        if parent not in ids or not isinstance(children, list) or not children:
            fail("composition certificate has a malformed parent or child inventory")
        for child in children:
            if not any(
                edge.get("from") == child and edge.get("to") == parent
                and edge.get("type") == "composes" for edge in proof_edges
            ):
                fail("composition certificate is not backed by a typed composes edge")
        declarations.extend(nonempty_strings(declared, "composition declarations"))
    if certificates:
        sources = actual_roles.get("composition_source", [])
        if len(sources) != 1:
            fail("composition certificates require exactly one Lean composition source")
        replay_declarations(
            sources[0], declarations, lean_authority=lean_authority,
            bound_sources=bound_sources,
        )
    return {"semantic_gates": gates, "registry_denominator_sha256": denominator}


def contains_negative_semantic(value: Any) -> bool:
    negative = {
        "blocked", "failed", "failure", "fail_closed", "open", "pending",
        "rejected", "revoked", "stale", "superseded", "timeout", "timed_out",
        "not_run", "unavailable", "incomplete",
    }
    if isinstance(value, str):
        normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
        return normalized in negative or any(
            normalized.startswith(token + "_") for token in negative
        )
    if isinstance(value, Mapping):
        return any(contains_negative_semantic(row) for row in value.values())
    if isinstance(value, list):
        return any(contains_negative_semantic(row) for row in value)
    return False


def content_digest(value: Mapping[str, Any], digest_field: str) -> str:
    unhashed = dict(value)
    claimed = unhashed.pop(digest_field, None)
    if not isinstance(claimed, str) or claimed != sha256(canonical(unhashed)):
        fail(f"{digest_field} does not bind the canonical artifact content")
    return claimed


def phase_replay_row(output: bytes, phase: str, gate_ids: list[str]) -> dict[str, Any]:
    try:
        lines = output.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ValidationError("phase semantic replay output is not UTF-8") from exc
    rows = [
        strict_object(line[len(PHASE_RESULT_BEGIN):-len(PHASE_RESULT_END)].encode(),
                      "phase semantic replay row")
        for line in lines
        if line.startswith(PHASE_RESULT_BEGIN) and line.endswith(PHASE_RESULT_END)
    ]
    if len(rows) != 1:
        fail("phase semantic replay did not emit exactly one authority-marked result")
    row = rows[0]
    expected_keys = {
        "schema_version", "phase", "semantic_verdict", "gate_results",
        "open_obligations", "stale_inputs", "blocked",
    }
    if (
        set(row) != expected_keys
        or row.get("schema_version") != "stage1-phase-semantic-replay/1.0"
        or row.get("phase") != phase
        or row.get("semantic_verdict") != "passed"
        or row.get("gate_results") != {gate: "passed" for gate in gate_ids}
        or row.get("open_obligations") != 0
        or row.get("stale_inputs") != []
        or row.get("blocked") is not False
    ):
        fail("phase semantic replay returned a nonpositive or malformed typed result")
    return row


def run_structured_phase_recipe(
    recipe: Mapping[str, Any], phase: str, gate_ids: list[str],
    *, command_runner: Any = subprocess.run,
) -> dict[str, Any]:
    argv = recipe.get("argv")
    cwd = recipe.get("cwd")
    timeout = recipe.get("timeout_seconds")
    network = recipe.get("network_policy")
    env_allowlist = recipe.get("env_allowlist")
    if (
        not isinstance(argv, list)
        or not argv
        or any(not isinstance(value, str) or not value for value in argv)
        or cwd != "."
        or not isinstance(timeout, int)
        or isinstance(timeout, bool)
        or not 1 <= timeout <= LEAN_REPLAY_TIMEOUT_SECONDS
        or network != "denied"
        or env_allowlist not in ({}, [])
        or recipe.get("expected_exit") != 0
    ):
        fail("phase semantic replay recipe is not hermetic and structured")
    executable = argv[0]
    allowed = {
        "/usr/bin/python3", "/stage1-toolchain/bin/lake",
        "/stage1-toolchain/bin/lean",
    }
    if executable not in allowed:
        fail("phase semantic replay executable is not authority-allowlisted")
    if executable == "/usr/bin/python3":
        if len(argv) < 4 or argv[1:3] != ["-I", "-B"]:
            fail("Python semantic replay must use isolated no-bytecode mode")
        validator_path = safe_path(argv[3], "phase semantic replay validator")
        if not validator_path.as_posix().startswith("scripts/stage1_phase_replays/"):
            fail("Python semantic replay validator is outside the authority namespace")
    env = {
        "PATH": "/stage1-toolchain/bin:/usr/bin:/bin",
        "HOME": "/scratch",
        "TMPDIR": "/scratch",
        "PYTHONHASHSEED": "0",
    }
    try:
        result = command_runner(
            argv, cwd=Path("."), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=timeout, check=False, shell=False, env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationError("phase semantic replay timed out") from exc
    if result.returncode != 0:
        fail("phase semantic replay command failed")
    return phase_replay_row(result.stdout, phase, gate_ids)


def validation_spec_recipes(specification: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    recipes = specification.get("recipes")
    if recipes is None and "argv" in specification:
        recipes = [specification]
    if not isinstance(recipes, list) or not recipes or any(not isinstance(row, Mapping) for row in recipes):
        fail("validation specification does not contain structured recipes")
    return recipes


def validate_dependency_receipt(
    role: str, actual_roles: Mapping[str, list[dict[str, Any]]],
    artifact_bytes: Mapping[str, bytes], expected_phase: str,
) -> dict[str, Any]:
    value = json_artifact(role, actual_roles, artifact_bytes)
    result = value.get("semantic_decision")
    if (
        value.get("schema_version") != "stage1-master-phase-acceptance/1.0"
        or value.get("phase") != expected_phase
        or value.get("phase_evidence_accepted") is not True
        or value.get("review_verdict") != "phase_accepted"
        or not isinstance(result, Mapping)
        or result.get("decision") != "phase_accepted"
        or result.get("phase_evidence_accepted") is not True
        or result.get("negative_reasons") != []
        or contains_negative_semantic(result)
    ):
        fail(f"{role} does not prove current master-accepted {expected_phase} semantics")
    return value


def validate_validation_semantics(
    receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str, lean_authority: Mapping[str, Any],
    bound_sources: Mapping[str, bytes],
) -> dict[str, Any]:
    gates = ["V01-ARTIFACTS", "V02-RECIPES", "V03-TRUST-PROVENANCE", "V04-CONSUMER-REUSE"]
    semantic_gate_ids(phase_row, gates)
    specification = json_artifact("validation_specification", actual_roles, artifact_bytes)
    require_identity(specification, item, theorem, "validation specification")
    if receipt.get("intent") != "validate":
        fail("validation receipt intent is not validate")
    proof_acceptance = validate_dependency_receipt(
        "proof_receipt", actual_roles, artifact_bytes, "proof"
    )
    recipes = validation_spec_recipes(specification)
    observed = [run_structured_phase_recipe(recipe, "validation", gates) for recipe in recipes]
    receipt_recipe = receipt.get("recipe")
    if receipt_recipe != recipes and not (len(recipes) == 1 and receipt_recipe == recipes[0]):
        fail("validation receipt recipe disagrees with the authority replay specification")
    result = receipt.get("result")
    trust = receipt.get("trust")
    provenance = receipt.get("provenance")
    independent = receipt.get("independent_validation")
    if (
        not isinstance(result, Mapping)
        or result.get("exit_code") != 0
        or result.get("semantic_verdict") != "passed"
        or result.get("gate_results") != {gate: "passed" for gate in gates}
        or contains_negative_semantic(result)
        or not isinstance(trust, Mapping)
        or trust.get("trust_level") != 0
        or trust.get("placeholder_unsafe_oracle_absent") is not True
        or trust.get("complete_transitive_tcb") is not True
        or contains_negative_semantic(trust)
        or not isinstance(provenance, Mapping)
        or provenance.get("all_terminal_objects_content_bound") is not True
        or provenance.get("source_and_dependency_boundaries_complete") is not True
        or contains_negative_semantic(provenance)
        or not isinstance(independent, Mapping)
        or independent.get("decision") != "passed"
        or contains_negative_semantic(independent)
    ):
        fail("validation trust, provenance, or independent semantic gate is not positive")
    kernel = result.get("kernel_replay")
    if not isinstance(kernel, Mapping):
        fail("validation result lacks an independently replayable kernel target")
    source_path = kernel.get("source")
    declarations = nonempty_strings(kernel.get("declarations"), "validation declarations")
    expected_types = kernel.get("declaration_type_sha256s")
    matches = [
        row for row in actual_roles.get("validation_sources", [])
        if row.get("path") == source_path
    ]
    if len(matches) != 1 or not isinstance(expected_types, Mapping):
        fail("validation kernel replay source or expected types are malformed")
    replay = replay_declarations(
        matches[0], declarations, lean_authority=lean_authority,
        bound_sources=bound_sources,
    )
    if replay["declaration_type_sha256s"] != expected_types:
        fail("validation independent kernel replay disagrees with the receipt")
    consumer_rows = actual_roles.get("consumer_validation_receipts", [])
    expected_consumers = proof_acceptance.get("accepted_hard_edge_consumers", [])
    if not isinstance(expected_consumers, list):
        fail("proof acceptance consumer reuse inventory is malformed")
    consumers: set[str] = set()
    for row in consumer_rows:
        value = strict_object(artifact_bytes[str(row["path"])], "consumer validation receipt")
        if (
            value.get("schema_version") != "stage1-master-phase-acceptance/1.0"
            or value.get("phase") != "validation"
            or value.get("phase_evidence_accepted") is not True
            or value.get("semantic_decision", {}).get("decision") != "phase_accepted"
        ):
            fail("consumer validation receipt is not master accepted")
        consumers.add(str(value.get("item_id")))
    if consumers != set(expected_consumers):
        fail("consumer validation receipts do not exactly cover accepted hard-edge reuse")
    return {"semantic_gates": gates, "semantic_replays": len(observed)}


def validate_release_semantics(
    receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str,
) -> dict[str, Any]:
    gates = ["R01-ARTIFACTS", "R02-PROTOCOL", "R03-TERMINAL-DECISIONS", "R04-PUBLIC"]
    semantic_gate_ids(phase_row, gates)
    specification = json_artifact("release_specification", actual_roles, artifact_bytes)
    decision = json_artifact("release_decision", actual_roles, artifact_bytes)
    validation = validate_dependency_receipt(
        "validation_receipt", actual_roles, artifact_bytes, "validation"
    )
    require_identity(specification, item, theorem, "release specification")
    require_identity(decision, item, theorem, "release decision")
    if receipt.get("intent") != "release":
        fail("release receipt intent is not release")
    recipes = validation_spec_recipes(specification)
    observed = [run_structured_phase_recipe(recipe, "release", gates) for recipe in recipes]
    if receipt.get("recipe") != recipes and not (len(recipes) == 1 and receipt.get("recipe") == recipes[0]):
        fail("release receipt recipe disagrees with the authority replay specification")
    protocol = specification.get("release_protocol")
    required_protocol = {
        "immutable_clean", "cold_empty_cache", "offline_replay", "sbom_and_licenses",
        "deterministic_bundle", "two_independent_attestations", "independent_minimal_verifier",
    }
    if not isinstance(protocol, Mapping) or set(protocol) != required_protocol or set(protocol.values()) != {True}:
        fail("release specification does not require the complete release protocol")
    bundle_binding = actual_roles.get("deterministic_evidence_bundle", [])
    if len(bundle_binding) != 1:
        fail("release requires exactly one deterministic evidence bundle")
    bundle = strict_object(
        artifact_bytes[str(bundle_binding[0]["path"])], "deterministic evidence bundle"
    )
    require_identity(bundle, item, theorem, "deterministic evidence bundle")
    bundle_digest = bundle_binding[0]["sha256"]
    if (
        bundle.get("schema_version") != "stage1-deterministic-evidence-bundle/1.0"
        or bundle.get("accepted") is not True
        or content_digest(bundle, "semantic_digest") != bundle.get("semantic_digest")
        or contains_negative_semantic(bundle)
        or receipt.get("deterministic_bundle_sha256") != bundle_digest
    ):
        fail("deterministic evidence bundle is missing, self-inconsistent, or nonpositive")
    attestations = []
    for row in actual_roles.get("independent_attestations", []):
        value = strict_object(artifact_bytes[str(row["path"])], "independent attestation")
        require_identity(value, item, theorem, "independent attestation")
        if (
            value.get("schema_version") != "stage1-independent-release-attestation/1.0"
            or value.get("accepted") is not True
            or value.get("bundle_sha256") != bundle_digest
            or not isinstance(value.get("identity"), str)
            or not isinstance(value.get("runner_id"), str)
            or value.get("shared_writable_cache") is not False
            or value.get("signature_verified") is not True
            or value.get("minimal_verifier_passed") is not True
            or content_digest(value, "attestation_sha256") != value.get("attestation_sha256")
            or contains_negative_semantic(value)
        ):
            fail("independent release attestation is malformed or nonpositive")
        attestations.append(value)
    if (
        len(attestations) < 2
        or len({value["identity"] for value in attestations}) != len(attestations)
        or len({value["runner_id"] for value in attestations}) != len(attestations)
    ):
        fail("release lacks two distinct independent identities and runners")
    expected_attestations = [value["attestation_sha256"] for value in attestations]
    if receipt.get("independent_attestations") != expected_attestations:
        fail("release receipt attestation inventory is stale")
    result = receipt.get("result")
    terminal = decision.get("terminal_decisions")
    if (
        not isinstance(result, Mapping)
        or result.get("exit_code") != 0
        or result.get("semantic_verdict") != "accepted"
        or result.get("gate_results") != {gate: "passed" for gate in gates}
        or contains_negative_semantic(result)
        or not isinstance(terminal, Mapping)
        or terminal.get("audit_complete") is not True
        or terminal.get("theorem_complete") is not receipt.get("theorem_complete")
        or decision.get("verdict") != receipt.get("verdict")
        or decision.get("remaining_root_cut_set") != receipt.get("remaining_root_cut_set")
        or decision.get("root_vector") != receipt.get("root_vector_after")
        or receipt.get("audit_complete") is not True
    ):
        fail("release terminal decision is inconsistent with replay or receipt")
    if receipt.get("verdict") == "accepted":
        vector = receipt.get("root_vector_after")
        machine = vector.get("M") if isinstance(vector, Mapping) else None
        if (
            receipt.get("theorem_complete") is not True
            or receipt.get("remaining_root_cut_set") != []
            or machine not in {"M0-L", "M0-W", "M0-P"}
        ):
            fail("accepted theorem release lacks exact M0 root closure")
    elif receipt.get("verdict") == "accepted_audit_only":
        fail("accepted-audit-only evidence cannot satisfy release")
    else:
        fail("release receipt uses a nonterminal positive verdict")
    projections = actual_roles.get("public_projections", [])
    bundle_projections = bundle.get("public_projections")
    if not isinstance(bundle_projections, list) or bundle_projections != [
        {"path": row["path"], "sha256": row["sha256"]} for row in projections
    ]:
        fail("public projections were not generated from the accepted bundle")
    if bundle.get("reconciliation_clean") is not True:
        fail("public projection reconciliation is not clean")
    if bundle.get("validation_acceptance_sha256") != sha256(canonical(validation)):
        fail("release bundle does not bind the accepted validation dependency")
    return {"semantic_gates": gates, "semantic_replays": len(observed)}


def validate_nonproof_semantics(
    phase: str, receipt: Mapping[str, Any], phase_row: Mapping[str, Any],
    actual_roles: Mapping[str, list[dict[str, Any]]], artifact_bytes: Mapping[str, bytes],
    item: str, theorem: str, lean_authority: Mapping[str, Any],
    bound_sources: Mapping[str, bytes],
) -> dict[str, Any]:
    if phase == "intake":
        return validate_intake_semantics(
            receipt, phase_row, actual_roles, artifact_bytes, item, theorem
        )
    if phase == "statement":
        return validate_statement_semantics(
            receipt, phase_row, actual_roles, artifact_bytes, item, theorem,
            lean_authority, bound_sources,
        )
    if phase == "anchor_audit":
        return validate_anchor_semantics(
            receipt, phase_row, actual_roles, artifact_bytes, item, theorem
        )
    if phase == "obligation_tree":
        return validate_obligation_tree_semantics(
            receipt, phase_row, actual_roles, artifact_bytes, item, theorem,
            lean_authority, bound_sources,
        )
    if phase == "validation":
        return validate_validation_semantics(
            receipt, phase_row, actual_roles, artifact_bytes, item, theorem,
            lean_authority, bound_sources,
        )
    if phase == "release":
        return validate_release_semantics(
            receipt, phase_row, actual_roles, artifact_bytes, item, theorem
        )
    fail("unsupported non-proof phase")


def negative(packet: dict[str, Any], gate: str, message: str) -> dict[str, Any]:
    return {
        "schema_version": OUTPUT_SCHEMA,
        "item_id": packet.get("item_id", "S56-M-0000-INTAKE"),
        "theorem_id": packet.get("theorem_id", "THM-M-0000"),
        "phase": packet.get("phase", "intake"),
        "status": "rejected",
        "verdict": "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": gate,
        "open_obligations": 1,
        "stale_inputs": [],
        "blocked": True,
        "message": message,
    }


def validate(raw: bytes) -> dict[str, Any]:
    if not raw or len(raw) > 16 * 1024 * 1024:
        fail("validator input size is invalid")
    packet = strict_object(raw, "validator input")
    expected_keys = {
        "schema_version", "item_id", "theorem_id", "phase",
        "authority_revision", "base_revision", "contract", "role_map",
        "focus_execution", "focus_contract_sha256", "lean_authority",
        "input_sha256",
    }
    if set(packet) != expected_keys or packet.get("schema_version") != INPUT_SCHEMA:
        fail("validator input schema is not exact")
    unhashed = dict(packet)
    claimed_input = unhashed.pop("input_sha256")
    if claimed_input != sha256(canonical(unhashed)):
        fail("validator input digest is stale")
    item = packet["item_id"]
    theorem = packet["theorem_id"]
    phase = packet["phase"]
    if (
        phase not in PHASES
        or not isinstance(item, str)
        or not isinstance(theorem, str)
        or item != f"S56-{theorem.removeprefix('THM-')}-{phase.upper()}"
    ):
        fail("validator input identity is inconsistent")
    focus = packet["focus_execution"]
    if (
        not isinstance(focus, dict)
        or packet["focus_contract_sha256"] != sha256(canonical(focus))
    ):
        fail("focus execution binding is stale")
    lean_authority = packet.get("lean_authority")
    expected_lean_authority_keys = {
        "schema_version",
        "toolchain", "toolchain_file_sha256", "dependency_lock_sha256",
        "dependency_packages_sha256",
        "toolchain_closure_sha256", "toolchain_closure_file_count",
        "toolchain_closure_bytes",
        "compiled_cache_sha256", "compiled_cache_file_count", "compiled_cache_bytes",
        "lean_binary_sha256", "lake_binary_sha256",
        "toolchain_mount", "lake_cache_mount", "network_policy", "repo_access",
    }
    if (
        not isinstance(lean_authority, dict)
        or set(lean_authority) != expected_lean_authority_keys
        or lean_authority.get("schema_version") != LEAN_AUTHORITY_SCHEMA
        or lean_authority.get("toolchain_mount") != "/stage1-toolchain"
        or lean_authority.get("lake_cache_mount") != "/stage1-lake-cache"
        or lean_authority.get("network_policy") != "denied"
        or lean_authority.get("repo_access") != "read_only"
        or not isinstance(lean_authority.get("dependency_packages_sha256"), str)
        or SHA256_RE.fullmatch(lean_authority["dependency_packages_sha256"]) is None
        or not isinstance(lean_authority.get("toolchain_closure_sha256"), str)
        or SHA256_RE.fullmatch(lean_authority["toolchain_closure_sha256"]) is None
        or not isinstance(lean_authority.get("toolchain_closure_file_count"), int)
        or isinstance(lean_authority.get("toolchain_closure_file_count"), bool)
        or lean_authority["toolchain_closure_file_count"] < 1
        or not isinstance(lean_authority.get("toolchain_closure_bytes"), int)
        or isinstance(lean_authority.get("toolchain_closure_bytes"), bool)
        or lean_authority["toolchain_closure_bytes"] < 1
        or not isinstance(lean_authority.get("compiled_cache_sha256"), str)
        or SHA256_RE.fullmatch(lean_authority["compiled_cache_sha256"]) is None
        or not isinstance(lean_authority.get("compiled_cache_file_count"), int)
        or isinstance(lean_authority.get("compiled_cache_file_count"), bool)
        or lean_authority["compiled_cache_file_count"] < 0
        or not isinstance(lean_authority.get("compiled_cache_bytes"), int)
        or isinstance(lean_authority.get("compiled_cache_bytes"), bool)
        or lean_authority["compiled_cache_bytes"] < 0
    ):
        fail("Lean replay authority binding is malformed")
    toolchain_bytes = exact_file(LEAN_TOOLCHAIN, "Lean toolchain pin")
    lock_bytes = exact_file(LEAN_LOCK, "Lean dependency lock")
    try:
        pinned_toolchain = toolchain_bytes.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ValidationError("Lean toolchain pin is not UTF-8") from exc
    if (
        lean_authority.get("toolchain") != pinned_toolchain
        or lean_authority.get("toolchain_file_sha256") != sha256(toolchain_bytes)
        or lean_authority.get("dependency_lock_sha256") != sha256(lock_bytes)
        or lean_authority.get("lean_binary_sha256")
        != sha256(exact_file(Path("/stage1-toolchain/bin/lean"), "Lean executable"))
        or lean_authority.get("lake_binary_sha256")
        != sha256(exact_file(Path("/stage1-toolchain/bin/lake"), "Lake executable"))
    ):
        fail("Lean replay authority disagrees with the pinned toolchain or lock")
    contract_binding = packet["contract"]
    if not isinstance(contract_binding, dict) or contract_binding.get("path") != CONTRACT_PATH:
        fail("contract binding is malformed")
    contract_path = safe_path(CONTRACT_PATH, "phase contract")
    contract_bytes = contract_path.read_bytes()
    if contract_binding.get("sha256") != sha256(contract_bytes):
        fail("phase contract digest is stale")
    contract = strict_object(contract_bytes, "phase contract")
    phase_rows = [
        row for row in contract.get("phases", [])
        if isinstance(row, dict) and row.get("phase") == phase
    ]
    if len(phase_rows) != 1:
        fail("phase contract row is missing or ambiguous")
    phase_row = phase_rows[0]
    role_map = packet["role_map"]
    if not isinstance(role_map, dict):
        fail("role map is malformed")
    role_unhashed = dict(role_map)
    role_digest = role_unhashed.pop("manifest_sha256", None)
    if role_digest != sha256(canonical(role_unhashed)):
        fail("role map digest is stale")
    allowed_role_keys = {
        "schema_version", "item_id", "theorem_id", "phase", "base_revision",
        "authority_revision", "contract_sha256", "contract_git_blob",
        "phase_receipt_path", "phase_receipt_sha256", "artifacts",
        "staged_delta_paths", "manifest_sha256",
    }
    if set(role_map) - allowed_role_keys:
        fail("role map contains unsupported authority fields")
    for key, expected in (("item_id", item), ("theorem_id", theorem), ("phase", phase)):
        if role_map.get(key) != expected:
            fail("role map identity disagrees with validator input")
    if role_map.get("authority_revision") != packet["authority_revision"]:
        fail("role map authority revision is stale")
    if role_map.get("base_revision") != packet["base_revision"]:
        fail("role map worker base is stale")
    artifacts = role_map.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        fail("role map has no artifacts")
    required_roles = {
        row["role"] for row in phase_row.get("required_artifact_roles", [])
        if isinstance(row, dict) and row.get("requirement") == "required"
    }
    actual_roles: dict[str, list[dict[str, Any]]] = {}
    artifact_bytes: dict[str, bytes] = {}
    for binding in artifacts:
        if not isinstance(binding, dict) or set(binding) != {"role", "path", "sha256", "git_blob"}:
            fail("artifact binding schema is not exact")
        role = binding.get("role")
        if not isinstance(role, str):
            fail("artifact role is malformed")
        path = safe_path(binding.get("path"), f"artifact {role}")
        data = path.read_bytes()
        if binding.get("sha256") != sha256(data):
            fail(f"artifact {role} digest is stale")
        actual_roles.setdefault(role, []).append(binding)
        artifact_bytes[str(binding["path"])] = data
    if not required_roles <= set(actual_roles):
        fail("required artifact role is absent")
    reject_research_proof_construction(
        phase, focus, role_map, artifact_bytes
    )
    owner_prefix = f"Stage1_Instances/{theorem}/"
    bound_lean_sources = {
        path: data
        for path, data in artifact_bytes.items()
        if path.startswith(owner_prefix) and path.endswith(".lean")
    }
    for declaration in phase_row.get("required_artifact_roles", []):
        if not isinstance(declaration, dict):
            fail("artifact role contract is malformed")
        count = len(actual_roles.get(str(declaration.get("role")), []))
        if declaration.get("cardinality") == "exactly_one" and count > 1:
            fail("exactly-one artifact role is ambiguous")
    receipt_rows = actual_roles.get("phase_receipt", [])
    if len(receipt_rows) != 1:
        fail("phase receipt role is missing or ambiguous")
    receipt = strict_object(
        artifact_bytes[str(receipt_rows[0]["path"])], "phase receipt"
    )
    enforce_role_contract(phase_row, receipt, actual_roles, theorem)
    if not COMMON_RECEIPT_KEYS <= set(receipt):
        fail("phase receipt lacks common authority fields")
    for required_pointer in phase_row.get("phase_receipt_required_fields", []):
        pointer(receipt, required_pointer)
    if (
        receipt.get("schema_version") != "stage1-node-receipt/1.0"
        or receipt.get("item_id") != item
        or receipt.get("theorem_id") != theorem
        or receipt.get("phase") != phase
        or receipt.get("base_revision") != packet["base_revision"]
        or receipt.get("proposed_state") != "[_]"
        or receipt.get("accepted") is not False
        or receipt.get("selftest_status") != "passed"
        or receipt.get("selftest_result", {}).get("exit_code") != 0
        or not isinstance(receipt.get("selftest_result", {}).get("commands"), list)
        or not receipt["selftest_result"]["commands"]
        or receipt.get("audit_complete") not in phase_row["audit_boundary"]["allowed_audit_complete_values"]
        or receipt.get("theorem_complete") not in phase_row["theorem_boundary"]["allowed_theorem_complete_values"]
    ):
        fail("phase receipt does not prove the positive worker boundary")
    eligible = phase_row.get("worker_verdicts_eligible_for_review", [])
    if receipt.get("verdict") not in eligible:
        fail("phase receipt verdict is not eligible for positive review")
    if phase == "release" and (
        receipt.get("verdict") != "accepted"
        or receipt.get("audit_complete") is not True
        or receipt.get("theorem_complete") is not True
    ):
        fail("release phase requires accepted with theorem_complete true")
    if receipt.get("first_failed_gate") not in {None, ""}:
        fail("phase receipt reports a failed gate")
    if receipt.get("known_failures") not in (None, False, "", 0, []):
        fail("phase receipt reports unresolved known failures")
    require_focus_semantic_bindings(phase, receipt, focus, phase_row)
    if phase in {"statement", "proof", "validation", "release"}:
        for binding in artifacts:
            if str(binding["path"]).endswith(".lean"):
                text = artifact_bytes[str(binding["path"])].decode("utf-8", "replace")
                if PROHIBITED_LEAN.search(text):
                    fail("credited Lean source contains a prohibited construct")
    integration: dict[str, Any] | None = None
    proof_declarations: list[str] | None = None
    proof_target: str | None = None
    proof_declared_axioms: list[str] | None = None
    if phase == "proof":
        proof_declarations, proof_target, proof_declared_axioms = (
            require_proof_semantic_bindings(
                receipt, focus, actual_roles.get("proof_sources", [])
            )
        )
    if phase == "proof" and focus.get("execution_disposition") == "organize_or_integrate":
        source = focus.get("exact_machine_source")
        worker = receipt.get("integration_source_evidence")
        proof_sources = actual_roles.get("proof_sources", [])
        if not isinstance(source, dict) or not isinstance(worker, dict) or len(proof_sources) < 1:
            fail("integration proof lacks independently replayable source evidence")
        local = worker.get("local_proof_source")
        matches = [
            row for row in proof_sources
            if isinstance(local, dict)
            and row.get("path") == local.get("path")
            and row.get("sha256") == local.get("sha256")
        ]
        exact_declarations = proof_declarations
        target = proof_target
        declared_axioms = proof_declared_axioms
        if (
            set(source) != EXACT_MACHINE_SOURCE_KEYS
            or worker.get("exact_machine_source") != source
            or worker.get("exact_machine_source_used") is not True
            or worker.get("introduced_root_critical_proof") is not False
            or len(matches) != 1
            or not isinstance(exact_declarations, list)
            or not exact_declarations
            or any(not isinstance(row, str) or not row for row in exact_declarations)
            or len(exact_declarations) != len(set(exact_declarations))
            or not isinstance(target, str)
            or target not in exact_declarations
            or not isinstance(declared_axioms, list)
            or any(not isinstance(row, str) for row in declared_axioms)
        ):
            fail("integration proof did not consume the exact admitted source")
        match_kind = source.get("match_kind")
        transport_evidence = source.get("transport_evidence")
        dependency_probe: tuple[str, str, str] | None = None
        imported_provider: tuple[str, str, str, str] | None = None
        source_consumption: str
        provider_dependency = False
        exact_vendoring = False
        machine_evidence_class = focus.get("machine_evidence_class")
        provider = source.get("declaration")
        provider_module = source.get("module")
        if (
            not isinstance(provider, str)
            or DECLARATION_RE.fullmatch(provider) is None
            or not isinstance(provider_module, str)
            or DECLARATION_RE.fullmatch(provider_module) is None
        ):
            fail("integration source provider identity is malformed")
        if match_kind == "exact":
            if transport_evidence != []:
                fail("exact integration source unexpectedly carries transport evidence")
            terminal = source.get("terminal_proof_body")
            terminal_sha = terminal.get("sha256") if isinstance(terminal, Mapping) else None
            if not isinstance(terminal_sha, str) or SHA256_RE.fullmatch(terminal_sha) is None:
                fail("admitted exact source terminal body identity is malformed")
            vendored = exact_vendored_provider(
                proof_sources,
                artifact_bytes,
                theorem_id=theorem,
                declaration=provider,
                terminal_body_sha256=terminal_sha,
            )
            if vendored is not None:
                vendored_binding, vendored_module = vendored
                exact_vendoring = True
                dependency_probe = (target, provider, vendored_module)
                imported_provider = (
                    vendored_module,
                    provider,
                    str(source.get("repository")),
                    str(source.get("revision")),
                )
                provider_dependency = True
                source_consumption = "exact_vendored_provider_dependency"
            else:
                if machine_evidence_class != "exact_pinned_closure":
                    fail(
                        "external exact integration must vendor the admitted terminal body; "
                        "it cannot substitute an independent local proof"
                    )
                dependency_probe = (target, provider, provider_module)
                imported_provider = (
                    provider_module, provider,
                    str(source.get("repository")), str(source.get("revision")),
                )
                provider_dependency = True
                source_consumption = (
                    "provider_constant_identity"
                    if target == provider
                    else "provider_constant_dependency"
                )
        elif match_kind == "checked_transport":
            if machine_evidence_class != "exact_pinned_closure":
                fail(
                    "checked transport provider must be in the pinned local closure "
                    "before proof acceptance"
                )
            if (
                not isinstance(transport_evidence, list)
                or len(transport_evidence) != 1
                or not isinstance(transport_evidence[0], Mapping)
                or set(transport_evidence[0]) != MACHINE_TRANSPORT_EVIDENCE_KEYS
            ):
                fail("checked transport integration lacks one exact admitted target binding")
            transport = transport_evidence[0]
            if (
                transport.get("role") != "statement_match"
                or transport.get("evidence_kind")
                != "machine_checked_statement_transport"
                or transport.get("source_formal_system") != source.get("formal_system")
                or transport.get("source_declaration") != provider
                or transport.get("source_declaration_type_sha256")
                != source.get("declaration_type_sha256")
                or transport.get("target_formal_system") != "Lean 4"
                or transport.get("target_declaration") != target
                or not isinstance(
                    transport.get("target_declaration_type_sha256"), str
                )
                or SHA256_RE.fullmatch(
                    str(transport.get("target_declaration_type_sha256"))
                ) is None
                or transport.get("target_declaration_type_sha256")
                == source.get("declaration_type_sha256")
                or transport.get("sha256") != transport.get("replay_receipt_sha256")
            ):
                fail("checked transport integration target disagrees with admission")
            dependency_probe = (target, provider, provider_module)
            imported_provider = (
                provider_module, provider,
                str(source.get("repository")), str(source.get("revision")),
            )
            provider_dependency = True
            source_consumption = "provider_constant_dependency"
        else:
            fail("integration source has an unsupported match kind")
        replay = readonly_lean_replay(
            Path(str(matches[0]["path"])),
            exact_declarations,
            dependency_packages_sha256=lean_authority[
                "dependency_packages_sha256"
            ],
            toolchain_closure_sha256=lean_authority["toolchain_closure_sha256"],
            toolchain_closure_file_count=lean_authority[
                "toolchain_closure_file_count"
            ],
            toolchain_closure_bytes=lean_authority["toolchain_closure_bytes"],
            compiled_cache_sha256=lean_authority["compiled_cache_sha256"],
            compiled_cache_file_count=lean_authority["compiled_cache_file_count"],
            compiled_cache_bytes=lean_authority["compiled_cache_bytes"],
            bound_sources=bound_lean_sources,
            **(
                {}
                if dependency_probe is None and imported_provider is None
                else {
                    "dependency_probe": dependency_probe,
                    "imported_provider": imported_provider,
                }
            ),
        )
        if (
            replay["toolchain"] != lean_authority["toolchain"]
            or replay["toolchain_file_sha256"]
            != lean_authority["toolchain_file_sha256"]
            or replay["lean_binary_sha256"] != lean_authority["lean_binary_sha256"]
            or replay["lake_binary_sha256"] != lean_authority["lake_binary_sha256"]
            or replay["dependency_lock_sha256"]
            != lean_authority["dependency_lock_sha256"]
            or replay["dependency_packages_sha256"]
            != lean_authority["dependency_packages_sha256"]
            or replay["toolchain_closure_sha256"]
            != lean_authority["toolchain_closure_sha256"]
            or replay["toolchain_closure_file_count"]
            != lean_authority["toolchain_closure_file_count"]
            or replay["toolchain_closure_bytes"]
            != lean_authority["toolchain_closure_bytes"]
            or replay["compiled_cache_sha256"]
            != lean_authority["compiled_cache_sha256"]
            or replay["compiled_cache_file_count"]
            != lean_authority["compiled_cache_file_count"]
            or replay["compiled_cache_bytes"] != lean_authority["compiled_cache_bytes"]
            or replay["source_sha256"] != matches[0]["sha256"]
            or sorted({axiom for rows in replay["declaration_axioms"].values() for axiom in rows})
            != sorted(set(declared_axioms))
        ):
            fail("Lean authority replay disagrees with proof receipt facts")
        admitted_type = source.get("declaration_type_sha256")
        observed_target_type = replay["declaration_type_sha256s"].get(target)
        expected_target_type = (
            admitted_type
            if match_kind == "exact"
            else transport_evidence[0]["target_declaration_type_sha256"]
        )
        if (
            not isinstance(admitted_type, str)
            or SHA256_RE.fullmatch(admitted_type) is None
            or not isinstance(expected_target_type, str)
            or SHA256_RE.fullmatch(expected_target_type) is None
            or observed_target_type != expected_target_type
        ):
            fail("local integration declaration type disagrees with admitted machine source")
        expected_relation = (
            "provider_constant_identity"
            if target == provider
            else "direct_proof_body_constant_dependency"
        )
        if provider_dependency and replay.get("provider_dependency") != {
            "schema": DEPENDENCY_PROBE_SCHEMA,
            "consumer": target,
            "provider": provider,
            "provider_module": provider_module,
            "relation": expected_relation,
        }:
            fail("integration replay did not prove admitted provider consumption")
        if provider_dependency and not isinstance(replay.get("provider_import"), Mapping):
            fail("integration replay did not bind the admitted provider import closure")
        integration = {
            "exact_machine_source_consumed": True,
            "exact_machine_source_sha256": sha256(canonical(source)),
            "introduced_root_critical_proof": False,
            "validated_artifact_sha256": matches[0]["sha256"],
            "match_kind": match_kind,
            "source_consumption": source_consumption,
            "provider_declaration": source.get("declaration"),
            "consumer_declaration": target,
            "provider_dependency_proven": provider_dependency,
            "exact_vendoring_proven": exact_vendoring,
        }
    elif phase == "proof":
        proof_sources = actual_roles.get("proof_sources", [])
        declarations = proof_declarations
        if (
            len(proof_sources) < 1
            or not isinstance(declarations, list)
            or not declarations
            or any(not isinstance(row, str) or not row for row in declarations)
        ):
            fail("proof phase lacks independently replayable Lean declarations")
        lean_sources = [
            row for row in proof_sources if str(row.get("path", "")).endswith(".lean")
        ]
        proof_body_source = receipt.get("proof_body", {}).get("source")
        replay_sources = [
            row for row in lean_sources if row.get("path") == proof_body_source
        ]
        if len(replay_sources) != 1:
            fail("proof phase must identify one receipt-selected replay-owning Lean source")
        replay = readonly_lean_replay(
            Path(str(replay_sources[0]["path"])),
            declarations,
            dependency_packages_sha256=lean_authority[
                "dependency_packages_sha256"
            ],
            toolchain_closure_sha256=lean_authority["toolchain_closure_sha256"],
            toolchain_closure_file_count=lean_authority[
                "toolchain_closure_file_count"
            ],
            toolchain_closure_bytes=lean_authority["toolchain_closure_bytes"],
            compiled_cache_sha256=lean_authority["compiled_cache_sha256"],
            compiled_cache_file_count=lean_authority["compiled_cache_file_count"],
            compiled_cache_bytes=lean_authority["compiled_cache_bytes"],
            bound_sources=bound_lean_sources,
        )
        if (
            replay["toolchain"] != lean_authority["toolchain"]
            or replay["toolchain_file_sha256"]
            != lean_authority["toolchain_file_sha256"]
            or replay["lean_binary_sha256"] != lean_authority["lean_binary_sha256"]
            or replay["lake_binary_sha256"] != lean_authority["lake_binary_sha256"]
            or replay["dependency_lock_sha256"]
            != lean_authority["dependency_lock_sha256"]
            or replay["dependency_packages_sha256"]
            != lean_authority["dependency_packages_sha256"]
            or replay["toolchain_closure_sha256"]
            != lean_authority["toolchain_closure_sha256"]
            or replay["toolchain_closure_file_count"]
            != lean_authority["toolchain_closure_file_count"]
            or replay["toolchain_closure_bytes"]
            != lean_authority["toolchain_closure_bytes"]
            or replay["compiled_cache_sha256"]
            != lean_authority["compiled_cache_sha256"]
            or replay["compiled_cache_file_count"]
            != lean_authority["compiled_cache_file_count"]
            or replay["compiled_cache_bytes"] != lean_authority["compiled_cache_bytes"]
            or replay["source_sha256"] != replay_sources[0]["sha256"]
        ):
            fail("Lean authority replay disagrees with the proof source or environment")
    if phase == "proof":
        ledger_rows = actual_roles.get("dependency_reuse_ledger", [])
        if len(ledger_rows) != 1:
            fail("proof phase lacks exactly one dependency reuse ledger")
        ledger = strict_object(
            artifact_bytes[str(ledger_rows[0]["path"])],
            "dependency reuse ledger",
        )
        replay_checked_transports(
            ledger,
            theorem_id=theorem,
            artifacts=artifacts,
            lean_authority=lean_authority,
            bound_sources=bound_lean_sources,
        )
    if phase != "proof":
        validate_nonproof_semantics(
            phase, receipt, phase_row, actual_roles, artifact_bytes, item, theorem,
            lean_authority, bound_lean_sources,
        )
    result = {
        "schema_version": OUTPUT_SCHEMA,
        "item_id": item,
        "theorem_id": theorem,
        "phase": phase,
        "status": "passed",
        "verdict": "phase_accepted",
        "phase_accepted": True,
        "audit_complete": receipt["audit_complete"],
        "theorem_complete": receipt["theorem_complete"],
        "phase_predicate_proven": True,
        "first_failed_gate": None,
        "open_obligations": 0,
        "stale_inputs": [],
        "blocked": False,
    }
    if integration is not None:
        result["integration_source_semantics"] = integration
    return result


def main() -> None:
    raw = sys.stdin.buffer.read()
    try:
        packet = validate(raw)
    except ValidationError as exc:
        try:
            identity = strict_object(raw, "validator input") if raw else {}
        except ValidationError:
            identity = {}
        print(json.dumps(negative(identity, "V2-AUTHORITY-REPLAY", str(exc)), sort_keys=True))
        return
    print(json.dumps(packet, sort_keys=True))


if __name__ == "__main__":
    main()
