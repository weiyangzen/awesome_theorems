#!/usr/bin/env python3
"""Fail-closed validator for one complete Stage5 theorem TARGET package.

This is deliberately a semantic validator, not a file-existence check.  A
worker may propose a package, but only the canonical controller/Master may use
this validator's result as one input to acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import signal
import sys
from typing import Any


PROGRAM = "stage5-theorem-proof-debt/2.0"
TARGET = re.compile(r"^S5THM-([0-9]{8})-TARGET$")
SHA = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_LEAN = re.compile(
    r"(?m)^\s*(?:sorry|admit|axiom|unsafe\s+(?:def|theorem)|opaque)\b"
)
SEMANTIC_DECLARATION_KINDS = (
    "def", "abbrev", "theorem", "lemma", "structure", "inductive",
    "class", "instance", "notation", "syntax", "macro", "macro_rules",
)
REQUIRED_FILENAMES = {
    "intake.json", "Statement.lean", "statement-crosswalk.json",
    "anchor-audit.json", "proof-units.json", "process-audit.md", "Proof.lean",
    "machine-closure.json", "machine-checked-audit.md", "proof-outline.md",
    "full-study.md", "readability-review.json", "Audit.lean",
    "build-validation.md", "current-validation.json", "README.md", "meta.json",
    "release-decision.json",
}
SEMANTIC_KEYS = {
    "provider_id", "provider_revision", "source_module", "source_path",
    "source_file_sha256", "source_declaration_sha256",
    "source_declaration_type_sha256", "elaborated_source_expr_sha256",
    "elaborated_target_expr_sha256", "transitive_constants",
    "source_surface_symbols", "local_shadowed_source_symbols",
    "semantic_substitutions", "bidirectional_transport",
    "recompute_evidence",
}


class ItemError(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ItemError("value is not canonical finite JSON") from exc


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_json(path: Path, label: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ItemError(f"{label}: missing regular file {path}")

    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ItemError(f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_bytes(), object_pairs_hook=pairs,
            parse_constant=lambda item: (_ for _ in ()).throw(
                ItemError(f"{label}: nonfinite {item}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ItemError(f"{label}: invalid strict JSON") from exc
    if not isinstance(value, dict):
        raise ItemError(f"{label}: expected object")
    return value


def sealed(value: dict[str, Any], label: str) -> None:
    authority = value.get("authority_sha256")
    body = dict(value)
    body.pop("authority_sha256", None)
    if (
        not isinstance(authority, str) or not SHA.fullmatch(authority)
        or sha(canonical(body)) != authority
    ):
        raise ItemError(f"{label}: authority seal differs")


def exact_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ItemError(f"{label}: fields differ; expected={sorted(keys)}")
    return value


def unique_strings(value: Any, label: str, *, nonempty: bool = True) -> list[str]:
    if (
        not isinstance(value, list) or (nonempty and not value)
        or any(not isinstance(row, str) or not row.strip() for row in value)
        or len(value) != len(set(value))
    ):
        raise ItemError(f"{label}: expected unique strings")
    return value


def safe_relative(value: str) -> Path:
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or path.as_posix() != value
        or "." in path.parts or ".." in path.parts
    ):
        raise ItemError(f"unsafe relative path {value!r}")
    return Path(*path.parts)


def nonempty(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ItemError(f"{label}: missing regular file")
    raw = path.read_bytes()
    if not raw.strip():
        raise ItemError(f"{label}: empty file")
    return raw


def strip_lean_inert(text: str) -> str:
    """Blank nested comments and strings while preserving lines/offsets."""
    output: list[str] = []
    index = 0
    block_depth = 0
    line_comment = False
    string = False
    escaped = False
    while index < len(text):
        if line_comment:
            if text[index] == "\n":
                line_comment = False
                output.append("\n")
            else:
                output.append(" ")
            index += 1
            continue
        if block_depth:
            if text.startswith("/-", index):
                block_depth += 1
                output.extend((" ", " "))
                index += 2
            elif text.startswith("-/", index):
                block_depth -= 1
                output.extend((" ", " "))
                index += 2
            else:
                output.append("\n" if text[index] == "\n" else " ")
                index += 1
            continue
        if string:
            character = text[index]
            output.append("\n" if character == "\n" else " ")
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                string = False
            index += 1
            continue
        if text.startswith("--", index):
            line_comment = True
            output.extend((" ", " "))
            index += 2
        elif text.startswith("/-", index):
            block_depth = 1
            output.extend((" ", " "))
            index += 2
        elif text[index] == '"':
            string = True
            output.append(" ")
            index += 1
        else:
            output.append(text[index])
            index += 1
    if block_depth or string:
        raise ItemError("Lean artifact has an unterminated comment or string")
    return "".join(output)


def lean_module_spelling(module: str) -> str:
    """Recover Lean's quoted arXiv directory identifier from catalog text.

    The catalog deliberately stores provider modules as filesystem-like dotted
    strings.  Most arXiv directories are numeric (``2208.14736``), while the
    legacy namespace uses one mixed directory (``math.0110202``).  Both dots
    belong to one Lean identifier; treating ``math`` as a namespace component
    asks Lake for a different, nonexistent module.
    """
    parts = module.split(".")
    result: list[str] = []
    index = 0
    while index < len(parts):
        if (
            index > 0
            and parts[index - 1] == "Arxiv"
            and parts[index] == "math"
            and index + 1 < len(parts)
            and parts[index + 1].isdigit()
        ):
            result.append(f"«math.{parts[index + 1]}»")
            index += 1
        elif parts[index].isdigit():
            numeric = [parts[index]]
            while index + 1 < len(parts) and parts[index + 1].isdigit():
                index += 1
                numeric.append(parts[index])
            result.append("«" + ".".join(numeric) + "»")
        else:
            result.append(parts[index])
        index += 1
    return ".".join(result)


def claim_theorem_declarations(text: str) -> set[str]:
    """Collect claim-owned theorem/lemma names through namespace scopes."""
    scopes: list[tuple[str, list[str]]] = []
    declarations: set[str] = set()
    for line in text.splitlines():
        namespace = re.match(r"^\s*namespace\s+([^\s]+)\s*$", line)
        if namespace:
            scopes.append(("namespace", namespace.group(1).split(".")))
            continue
        if re.match(r"^\s*section(?:\s+[^\s]+)?\s*$", line):
            scopes.append(("section", []))
            continue
        if re.match(r"^\s*end(?:\s+[^\s]+)?\s*$", line):
            if scopes:
                scopes.pop()
            continue
        declaration = re.match(
            r"^\s*(?:(?:private|protected|noncomputable)\s+)*"
            r"(?:theorem|lemma)\s+([^\s:{(]+)", line,
        )
        if declaration:
            name = declaration.group(1)
            if name.startswith("_root_."):
                declarations.add(name[len("_root_."):])
            else:
                prefix = [part for kind, parts in scopes if kind == "namespace" for part in parts]
                declarations.add(".".join([*prefix, name]) if prefix else name)
    return declarations


def find_member(work: Path, stage_claim_id: str, item_id: str) -> dict[str, Any]:
    workset = strict_json(work / "_baseline/workset-5.6.json", "workset")
    sealed(workset, "workset")
    members = workset.get("members")
    if not isinstance(members, list):
        raise ItemError("workset members differ")
    matches = [
        row for row in members
        if isinstance(row, dict) and row.get("stage_claim_id") == stage_claim_id
    ]
    if len(matches) != 1:
        raise ItemError("exact workset member is absent or duplicated")
    member = matches[0]
    if (
        member.get("target_item_id") != item_id
        or member.get("internal_subchecklist")
        != ["INTAKE", "STATEMENT", "ANCHOR", "TREE", "MACHINE", "READABLE", "VALIDATE", "RELEASE"]
        or not SHA.fullmatch(str(member.get("target_task_authority_sha256", "")))
    ):
        raise ItemError("TARGET member authority differs")
    return member


def member_statement_authority(
    member: dict[str, Any], work: Path,
) -> dict[str, str]:
    """Normalize the two frozen provider catalog shapes without fallback."""
    formal = member.get("formal_statement")
    if not isinstance(formal, dict):
        raise ItemError("frozen formal statement is absent")
    provider_id = member.get("provider_id")
    if provider_id == "formal-conjectures-2270d31e":
        locator = member.get("source_locator")
        if not isinstance(locator, dict):
            raise ItemError("Formal Conjectures source locator is absent")
        authority = {
            "provider_revision": locator.get("revision"),
            "source_module": member.get("module"),
            "source_path": locator.get("member_path"),
            "source_file_sha256": locator.get("file_sha256"),
            "source_declaration_sha256": formal.get("declaration_sha256"),
            "source_declaration_type_sha256": formal.get("declaration_type_sha256"),
            "qualified_declaration": formal.get("qualified_declaration"),
            "declaration_type": formal.get("declaration_type"),
        }
    elif provider_id == "mathlib-8a178386":
        evidence = member.get("proof_evidence")
        module = formal.get("module")
        declaration = formal.get("declaration")
        formal_type = formal.get("formal_type")
        if (
            not isinstance(evidence, dict)
            or evidence.get("mathlib_commit")
            != "8a178386ffc0f5fef0b77738bb5449d50efeea95"
            or evidence.get("compiled_module") != module
            or evidence.get("uses_sorry") is not False
            or not isinstance(module, str) or not module.startswith("Mathlib.")
            or not isinstance(declaration, str) or not declaration
            or not isinstance(formal_type, str) or not formal_type
        ):
            raise ItemError("mathlib statement/proof authority differs")
        source_path = module.replace(".", "/") + ".lean"
        source = (
            work / "_baseline/provider-sources" / str(provider_id)
            / evidence["mathlib_commit"] / source_path
        )
        source_raw = nonempty(source, "pinned mathlib provider source")
        authority = {
            "provider_revision": evidence["mathlib_commit"],
            "source_module": module,
            "source_path": source_path,
            "source_file_sha256": sha(source_raw),
            "source_declaration_sha256": sha(canonical(formal)),
            "source_declaration_type_sha256": formal.get("formal_type_sha256"),
            "qualified_declaration": declaration,
            "declaration_type": formal_type,
        }
    else:
        raise ItemError(f"unsupported statement provider: {provider_id}")
    if any(not isinstance(value, str) or not value for value in authority.values()):
        raise ItemError("normalized statement authority is incomplete")
    for key in (
        "source_file_sha256", "source_declaration_sha256",
        "source_declaration_type_sha256",
    ):
        if SHA.fullmatch(authority[key]) is None:
            raise ItemError(f"normalized statement authority {key} is malformed")
    route = strict_json(
        work / "_baseline/provider-kernel-route.json", "provider kernel route",
    )
    sealed(route, "provider kernel route")
    exact_keys(route, {
        "schema_version", "provider_id", "revision", "module", "lean_module",
        "qualified_declaration", "toolchain", "master_environment",
        "proof_authority", "provider_body_authority", "authority_sha256",
    }, "provider kernel route")
    expected_toolchain = (
        "leanprover/lean4:v4.27.0"
        if provider_id == "formal-conjectures-2270d31e"
        else "leanprover/lean4:v4.29.0"
    )
    expected_environment = (
        "Formalizations/Lean/.lake/packages/formal-conjectures"
        if provider_id == "formal-conjectures-2270d31e"
        else "Formalizations/Lean"
    )
    if route != {
        "schema_version": "awesome-theorems/stage5-provider-kernel-route/1.0",
        "provider_id": provider_id,
        "revision": authority["provider_revision"],
        "module": authority["source_module"],
        "lean_module": lean_module_spelling(authority["source_module"]),
        "qualified_declaration": authority["qualified_declaration"],
        "toolchain": expected_toolchain,
        "master_environment": expected_environment,
        "proof_authority": "claim_owned_root_only",
        "provider_body_authority": False,
        "authority_sha256": route["authority_sha256"],
    }:
        raise ItemError("provider kernel route differs")
    return authority


def semantic_environment(
    crosswalk: dict[str, Any], member: dict[str, Any], lean_paths: list[Path],
    work: Path, machine: dict[str, Any],
) -> str:
    exact_keys(crosswalk, {
        "schema_version", "program", "item_id", "stage_claim_id",
        "member_record_sha256", "source_formal_type_sha256",
        "semantic_environment", "authority_sha256",
    }, "statement crosswalk")
    sealed(crosswalk, "statement crosswalk")
    if (
        crosswalk["schema_version"]
        != "awesome-theorems/stage5-theorem-statement-crosswalk/2.0"
        or crosswalk["program"] != PROGRAM
        or crosswalk["stage_claim_id"] != member["stage_claim_id"]
        or crosswalk["item_id"] != member["target_item_id"]
        or crosswalk["member_record_sha256"] != member["record_sha256"]
        or crosswalk["source_formal_type_sha256"]
        != (
            member.get("formal_type_sha256")
            or member.get("formal_statement", {}).get("formal_type_sha256")
        )
    ):
        raise ItemError("statement crosswalk identity differs")
    environment = exact_keys(
        crosswalk["semantic_environment"], SEMANTIC_KEYS, "semantic environment",
    )
    formal = member["formal_statement"]
    authority = member_statement_authority(member, work)
    expected = {
        "provider_id": member["provider_id"],
        **{key: authority[key] for key in (
            "provider_revision", "source_module", "source_path",
            "source_file_sha256", "source_declaration_sha256",
            "source_declaration_type_sha256",
        )},
    }
    for key, wanted in expected.items():
        if environment[key] != wanted:
            raise ItemError(f"semantic environment {key} differs")
    for key in ("elaborated_source_expr_sha256", "elaborated_target_expr_sha256"):
        if not SHA.fullmatch(str(environment[key])):
            raise ItemError(f"semantic environment {key} is malformed")
    if environment["elaborated_source_expr_sha256"] != environment["elaborated_target_expr_sha256"]:
        raise ItemError("source and target elaborated expressions differ")
    constants = environment["transitive_constants"]
    if not isinstance(constants, list) or not constants:
        raise ItemError("transitive semantic constant census is empty")
    registry = strict_json(work / "_baseline/provider-registry.json", "provider registry")
    sealed(registry, "provider registry")
    providers = {
        row.get("provider_id"): row for row in registry.get("providers", [])
        if isinstance(row, dict) and isinstance(row.get("provider_id"), str)
    }
    names: list[str] = []
    for row in constants:
        exact_keys(row, {
            "name", "declaration_kind", "provider_id", "provider_revision",
            "source_path", "source_sha256", "type_sha256", "body_sha256",
        }, "transitive semantic constant")
        names.append(row["name"])
        provider = providers.get(row["provider_id"])
        if (
            not isinstance(provider, dict)
            or provider.get("revision") != row["provider_revision"]
        ):
            raise ItemError("transitive constant provider/revision is not pinned")
        source_relative = safe_relative(row["source_path"])
        provider_source = (
            work / "_baseline/provider-sources" / row["provider_id"]
            / row["provider_revision"] / source_relative
        )
        provider_raw = nonempty(
            provider_source, f"pinned provider source for {row['name']}",
        )
        if sha(provider_raw) != row["source_sha256"]:
            raise ItemError(f"pinned provider source digest differs: {row['name']}")
        if (
            not isinstance(row["name"], str) or not row["name"].strip()
            or row["declaration_kind"] not in SEMANTIC_DECLARATION_KINDS
            or any(not SHA.fullmatch(str(row[key])) for key in (
                "source_sha256", "type_sha256", "body_sha256",
            ))
            or not isinstance(row["provider_id"], str)
            or not isinstance(row["provider_revision"], str)
            or not isinstance(row["source_path"], str)
        ):
            raise ItemError("transitive semantic constant binding differs")
    if len(names) != len(set(names)):
        raise ItemError("transitive semantic constants are duplicated")
    surface = unique_strings(
        environment["source_surface_symbols"], "source surface symbols",
    )
    if environment["local_shadowed_source_symbols"] != []:
        raise ItemError("source symbols are locally shadowed")
    if environment["semantic_substitutions"] != []:
        raise ItemError("semantic substitutions are present")
    transport = exact_keys(environment["bidirectional_transport"], {
        "source_to_target_theorem", "target_to_source_theorem",
        "lean_checked", "master_recompute_required",
    }, "bidirectional transport")
    if (
        not transport["lean_checked"] or not transport["master_recompute_required"]
        or not all(isinstance(transport[key], str) and transport[key].strip() for key in (
            "source_to_target_theorem", "target_to_source_theorem",
        ))
    ):
        raise ItemError("bidirectional semantic transport is incomplete")
    recompute = exact_keys(environment["recompute_evidence"], {
        "audit_declaration", "command_id", "trust", "cold_from_source",
        "worker_recomputed", "master_recompute_required",
    }, "semantic recompute evidence")
    if (
        recompute["trust"] != 0 or not recompute["cold_from_source"]
        or not recompute["worker_recomputed"]
        or not recompute["master_recompute_required"]
        or not isinstance(recompute["audit_declaration"], str)
        or not isinstance(recompute["command_id"], str)
    ):
        raise ItemError("semantic recompute evidence differs")

    active_by_name = {
        path.name: strip_lean_inert(
            nonempty(path, f"Lean semantic artifact {path.name}").decode("utf-8")
        ) for path in lean_paths
    }
    combined = "\n".join(active_by_name.values())
    if FORBIDDEN_LEAN.search(combined):
        raise ItemError("Lean package contains a placeholder or forbidden oracle")
    # The source module is part of the semantic authority.  A target that
    # merely reproduces a proposition under `import Mathlib` (or another
    # substitute import) is not a transport of the frozen provider theorem.
    # Require the exact provider module to be imported by the claim-owned
    # Lean surface so the kernel elaborates against the pinned source.
    exact_import = re.compile(
        rf"(?m)^\s*import\s+{re.escape(lean_module_spelling(authority['source_module']))}\s*$"
    )
    if any(not exact_import.search(active_by_name[path.name]) for path in lean_paths):
        raise ItemError("exact provider module import is missing; import substitution rejected")
    qualified = authority["qualified_declaration"]
    if not isinstance(qualified, str) or not qualified.strip():
        raise ItemError("frozen provider qualified declaration is missing")
    if qualified not in combined:
        raise ItemError("frozen provider declaration reference is missing; semantic source substitution rejected")
    root = machine.get("root_declaration")
    audit = active_by_name.get("Audit.lean", "")
    claim_declarations = set().union(*(
        claim_theorem_declarations(text) for text in active_by_name.values()
    ))
    if (
        not isinstance(root, str) or not root.strip()
        or root not in claim_declarations
    ):
        raise ItemError("claim-owned machine root is absent from active Lean code")
    exact_root_witness = re.compile(
        rf"(?m)^\s*example\s*:\s*type_of%\s+{re.escape(qualified)}"
        rf"\s*:=\s*{re.escape(root)}\s*$"
    )
    if (
        root == qualified
        or exact_root_witness.search(audit) is None
        or not re.search(
            rf"(?m)^\s*#print\s+axioms\s+{re.escape(root)}\s*$", audit,
        )
    ):
        raise ItemError(
            "Audit.lean lacks active exact-type transport or terminal root axiom query"
        )

    # A local `def`/`abbrev` can silently turn an open or sorry-backed source
    # statement into a different proposition while retaining an apparently
    # convincing theorem header.  The Blueprint therefore admits only
    # theorem/lemma transport declarations in the target files; semantic
    # helper definitions, aliases, parser extensions, local instances and
    # oracle declarations are all rejected before any result can be harvested.
    forbidden_local = re.compile(
        r"(?m)^\s*(?:(?:private|protected|noncomputable|scoped)\s+)*(?:"
        r"def|abbrev|structure|inductive|class|instance|axiom|opaque|"
        r"notation(?::\d+)?|syntax|macro(?:_rules)?|local\s+instance)\b"
    )
    if forbidden_local.search(combined):
        raise ItemError("local semantic shadow/redefinition or parser substitution rejected")

    # Namespace aliases are another way to capture a source name without a
    # declaration spelling that the checks above can see.
    if re.search(r"(?m)^\s*namespace\s+[^\n=]+=>\s*[^\n]+$", combined):
        raise ItemError("namespace alias substitution rejected")
    # The worker does not choose the complete shadow-check set.  Independently
    # derive surface identifiers from the frozen source declaration and reject
    # any local declaration or parser rule that captures one of them.
    source_type = authority["declaration_type"]
    local_declarations = re.findall(
        r"(?m)^\s*(?:def|abbrev|structure|inductive|class|axiom|opaque)\s+([^\s:{(]+)",
        combined,
    )
    for local_name in local_declarations:
        if re.search(rf"(?<![\w.]){re.escape(local_name)}(?![\w.])", source_type):
            raise ItemError(f"local semantic shadow/redefinition rejected: {local_name}")
    parser_lines = re.findall(
        r"(?m)^\s*(?:notation(?::\d+)?|syntax|macro(?:_rules)?)\b[^\n]*", combined,
    )
    source_identifiers = set(re.findall(r"[\wℝℕΦ]+", source_type, re.UNICODE))
    for line in parser_lines:
        captured = source_identifiers & set(re.findall(r"[\wℝℕΦ]+", line, re.UNICODE))
        if captured - {"term"}:
            raise ItemError(
                "local semantic parser substitution rejected: "
                + ",".join(sorted(captured - {"term"}))
            )
    for symbol in surface:
        base = symbol.rsplit(".", 1)[-1]
        declaration = re.compile(
            rf"(?m)^\s*(?:def|abbrev|structure|inductive|class|axiom|opaque)\s+{re.escape(base)}\b"
        )
        syntax = re.compile(
            rf"(?m)^\s*(?:notation|syntax|macro(?:_rules)?)\b[^\n]*{re.escape(base)}"
        )
        if declaration.search(combined) or syntax.search(combined):
            raise ItemError(f"local semantic shadow/redefinition rejected: {symbol}")
    return sha(canonical(environment))


def validate_machine(value: dict[str, Any], identity: dict[str, str], semantic_sha: str) -> None:
    exact_keys(value, {
        "schema_version", "program", "item_id", "stage_claim_id",
        "semantic_environment_sha256", "machine_level", "root_declaration",
        "root_expr_sha256", "declaration_census", "dependency_edges",
        "observed_axioms", "remaining_machine_cut_set", "trust",
        "cold_from_source_replay", "authority_sha256",
    }, "machine closure")
    sealed(value, "machine closure")
    if any(value[key] != wanted for key, wanted in identity.items()):
        raise ItemError("machine closure identity differs")
    if (
        value["semantic_environment_sha256"] != semantic_sha
        or value["machine_level"] not in {"M0-L", "M0-W", "M0-P"}
        or value["remaining_machine_cut_set"] != []
        or value["trust"] != 0 or not value["cold_from_source_replay"]
        or not SHA.fullmatch(str(value["root_expr_sha256"]))
        or not isinstance(value["declaration_census"], list)
        or not value["declaration_census"]
        or not isinstance(value["dependency_edges"], list)
        or not isinstance(value["observed_axioms"], list)
        or len(value["observed_axioms"]) != len(set(value["observed_axioms"]))
        or any(
            not isinstance(axiom, str)
            or axiom not in {"propext", "Classical.choice", "Quot.sound"}
            for axiom in value["observed_axioms"]
        )
        or not any(
            isinstance(row, dict) and row.get("name") == value["root_declaration"]
            for row in value["declaration_census"]
        )
    ):
        raise ItemError("machine closure is not exact M0 with cold trust-zero replay")


def validate_readability(value: dict[str, Any], identity: dict[str, str]) -> None:
    exact_keys(value, {
        "schema_version", "program", "item_id", "stage_claim_id",
        "readability_level", "required_nodes", "node_to_anchor",
        "anchor_to_fragment", "reviewers", "remaining_readability_cut_set",
        "distilled", "authority_sha256",
    }, "readability review")
    sealed(value, "readability review")
    if any(value[key] != wanted for key, wanted in identity.items()):
        raise ItemError("readability identity differs")
    required = unique_strings(value["required_nodes"], "required readable nodes")
    forward = value["node_to_anchor"]
    reverse = value["anchor_to_fragment"]
    if (
        value["readability_level"] != "R0"
        or not isinstance(forward, dict) or set(forward) != set(required)
        or len(set(forward.values())) != len(required)
        or not isinstance(reverse, dict) or set(reverse) != set(forward.values())
        or value["remaining_readability_cut_set"] != []
    ):
        raise ItemError("readability mapping is not total, injective R0")
    for anchor, row in reverse.items():
        exact_keys(row, {
            "node_id", "path", "fragment_sha256", "hypotheses", "inference",
            "output", "formal_anchor", "downstream_uses", "exceptional_cases",
            "trust_boundary",
        }, f"readability fragment {anchor}")
        if (
            forward.get(row["node_id"]) != anchor
            or not SHA.fullmatch(str(row["fragment_sha256"]))
            or any(not isinstance(row[key], (str, list)) or not row[key] for key in (
                "hypotheses", "inference", "output", "formal_anchor",
                "downstream_uses", "exceptional_cases", "trust_boundary",
            ))
        ):
            raise ItemError("readability fragment loses mathematical content")
    reviewers = value["reviewers"]
    if (
        not isinstance(reviewers, list) or len(reviewers) < 2
        or len({row.get("reviewer_id") for row in reviewers if isinstance(row, dict)})
        != len(reviewers)
    ):
        raise ItemError("independent readability reviewers are insufficient")
    distilled = exact_keys(value["distilled"], {
        "duplicate_prose_removed", "structured_inventory_not_duplicated",
        "mathematical_content_preserved", "deletion_mutations_passed",
    }, "distilled proof")
    if not all(distilled.values()):
        raise ItemError("distilled output simplified or duplicated the proof")


def validate_release(value: dict[str, Any], identity: dict[str, str], semantic_sha: str) -> None:
    exact_keys(value, {
        "schema_version", "program", "item_id", "stage_claim_id", "decision",
        "semantic_environment_sha256", "machine_complete", "readable_complete",
        "human_cut_set", "machine_cut_set", "readability_cut_set",
        "current_trace_sha256", "strict_dominance", "theorem_complete_candidate",
        "master_accepted", "authority_sha256",
    }, "release decision")
    sealed(value, "release decision")
    if any(value[key] != wanted for key, wanted in identity.items()):
        raise ItemError("release identity differs")
    dominance = exact_keys(value["strict_dominance"], {
        "fixture", "fixture_status", "all_applicable_shape_predicates_passed",
        "exact_m0", "true_r0", "empty_hmr_cuts", "semantic_environment_added",
        "semantic_substitution_mutations_passed", "cold_from_source_replay_passed",
        "strict_dimensions",
    }, "strict-dominance certificate")
    if (
        value["decision"] != "provisional_release_candidate"
        or value["semantic_environment_sha256"] != semantic_sha
        or not value["machine_complete"] or not value["readable_complete"]
        or value["human_cut_set"] != [] or value["machine_cut_set"] != []
        or value["readability_cut_set"] != []
        or not SHA.fullmatch(str(value["current_trace_sha256"]))
        or not value["theorem_complete_candidate"] or value["master_accepted"]
        or dominance["fixture"] != "THM-M-0387"
        or dominance["fixture_status"] != "incomplete_H1_M2_R0_negative_fixture"
        or not all(dominance[key] for key in (
            "all_applicable_shape_predicates_passed", "exact_m0", "true_r0",
            "empty_hmr_cuts", "semantic_environment_added",
            "semantic_substitution_mutations_passed",
            "cold_from_source_replay_passed",
        ))
        or set(unique_strings(dominance["strict_dimensions"], "strict dimensions"))
        < {"semantic_environment", "semantic_substitution_mutations", "cold_from_source_replay"}
    ):
        raise ItemError("release does not strictly dominate the THM-M-0387 negative fixture")


def compile_lean(
    path: Path, canonical_root: Path, *, timeout_seconds: int = 900,
    lean_root: Path | None = None, toolchain: str | None = None,
) -> subprocess.CompletedProcess[str]:
    nonempty(path, f"Lean artifact {path.name}")
    lean_root = lean_root or (canonical_root / "Formalizations/Lean")
    toolchain = toolchain or nonempty(
        lean_root / "lean-toolchain", "lean-toolchain",
    ).decode().strip()
    elan = Path(os.environ.get("ELAN_HOME", str(Path.home() / ".elan"))) / "bin/elan"
    if not elan.is_file() or not os.access(elan, os.X_OK):
        raise ItemError("pinned elan executable is unavailable")
    command = [str(elan), "run", toolchain, "lake", "env", "lean", "--trust=0", str(path.resolve())]
    process = subprocess.Popen(
        command, cwd=lean_root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, start_new_session=True,
        env={**os.environ, "LAKE_NO_CACHE": "1"},
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
        completed = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except subprocess.TimeoutExpired as exc:
        # elan -> lake -> lean is a process group; killing only the wrapper
        # leaves trust-zero Lean children burning the next scheduler tick.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(command, timeout_seconds, output=stdout, stderr=stderr) from exc
    if completed.returncode:
        # Lake/Lean versions do not consistently route elaboration diagnostics
        # to stderr.  Preserve a bounded tail of both streams so the active
        # generation and repair ledger receive an actionable Master failure
        # rather than the former empty ``failed: `` message.
        stdout_tail = completed.stdout[-4000:].strip()
        stderr_tail = completed.stderr[-4000:].strip()
        diagnostic = "\n".join(
            part for part in (
                f"stdout:\n{stdout_tail}" if stdout_tail else "",
                f"stderr:\n{stderr_tail}" if stderr_tail else "",
            ) if part
        )
        if not diagnostic:
            diagnostic = "no stdout/stderr diagnostic"
        raise ItemError(
            f"Lean trust-zero elaboration failed (exit={completed.returncode}): "
            f"{diagnostic}"
        )
    return completed


def kernel_route(member: dict[str, Any], canonical_root: Path) -> tuple[Path, str]:
    """Select and authenticate the provider-native kernel environment."""
    provider_id = member.get("provider_id")
    if provider_id == "formal-conjectures-2270d31e":
        root = canonical_root / "Formalizations/Lean/.lake/packages/formal-conjectures"
        expected_revision = "2270d31e8dd611521f979de6d86da364930b7669"
        expected_toolchain = "leanprover/lean4:v4.27.0"
        locator = member.get("source_locator")
        if not isinstance(locator, dict):
            raise ItemError("Formal Conjectures source locator is absent")
        source = root / safe_relative(str(locator.get("member_path", "")))
        if (
            locator.get("revision") != expected_revision
            or sha(nonempty(source, "provider-native source"))
            != locator.get("file_sha256")
        ):
            raise ItemError("provider-native source/revision differs")
    elif provider_id == "mathlib-8a178386":
        root = canonical_root / "Formalizations/Lean"
        expected_revision = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
        expected_toolchain = "leanprover/lean4:v4.29.0"
        evidence = member.get("proof_evidence")
        if (
            not isinstance(evidence, dict)
            or evidence.get("mathlib_commit") != expected_revision
            or evidence.get("compiled_module")
            != member.get("formal_statement", {}).get("module")
            or evidence.get("uses_sorry") is not False
        ):
            raise ItemError("mathlib kernel route revision differs")
    else:
        raise ItemError(f"unsupported kernel provider route: {provider_id}")
    checkout = (
        root if provider_id == "formal-conjectures-2270d31e"
        else root / ".lake/packages/mathlib"
    )
    if checkout.is_symlink() or not (checkout / ".git").exists():
        raise ItemError("provider-native checkout is unavailable")
    if provider_id == "mathlib-8a178386":
        # The catalog's proof claim is bound to the exact elaborated module,
        # not merely to matching source bytes at the recorded commit.  Replay
        # both compiled artifacts before using this checkout as kernel
        # authority; a rebuilt, missing, or substituted cache must fail closed.
        for kind in ("olean", "ilean"):
            relative = safe_relative(str(evidence.get(f"{kind}_path", "")))
            expected_digest = evidence.get(f"{kind}_sha256")
            if (
                SHA.fullmatch(str(expected_digest or "")) is None
                or sha(nonempty(checkout / relative, f"pinned mathlib {kind}"))
                != expected_digest
            ):
                raise ItemError(f"mathlib kernel {kind} digest differs")
    revision = subprocess.run(
        ["/usr/bin/git", "-C", str(checkout), "rev-parse", "HEAD"],
        text=True, capture_output=True, check=False, timeout=30,
    )
    dirty = subprocess.run(
        ["/usr/bin/git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=no"],
        text=True, capture_output=True, check=False, timeout=30,
    )
    actual_toolchain = nonempty(root / "lean-toolchain", "provider-native lean-toolchain").decode().strip()
    if (
        revision.returncode != 0 or revision.stdout.strip() != expected_revision
        or dirty.returncode != 0 or dirty.stdout.strip()
        or actual_toolchain != expected_toolchain
    ):
        raise ItemError("provider-native kernel checkout/toolchain differs")
    return root, expected_toolchain


def reported_root_axioms(output: str, root: str) -> list[str]:
    """Extract the exact terminal root's `#print axioms` report."""
    reports: list[list[str]] = []
    for declaration, body in re.findall(
        r"(?m)^'([^']+)' depends on axioms:\s*\[([^\]]*)\]\s*$", output,
    ):
        if declaration == root:
            reports.append([
                item.strip() for item in body.split(",") if item.strip()
            ])
    for declaration in re.findall(
        r"(?m)^'([^']+)' does not depend on any axioms\s*$", output,
    ):
        if declaration == root:
            reports.append([])
    if len(reports) != 1:
        raise ItemError("Audit.lean lacks one parseable terminal root axiom report")
    if len(reports[0]) != len(set(reports[0])):
        raise ItemError("terminal root axiom report contains duplicates")
    return reports[0]


def validate_target(
    claim: dict[str, Any], work: Path, canonical_root: Path, *, compile_files: bool = True,
    compile_timeout_seconds: int = 900,
) -> dict[str, Any]:
    match = TARGET.fullmatch(str(claim.get("item_id", "")))
    if match is None:
        raise ItemError("this validator accepts one complete theorem TARGET only")
    item_id = claim["item_id"]
    stage_claim_id = f"S5-CLM-{match.group(1)}"
    member = find_member(work, stage_claim_id, item_id)
    writable = claim.get("writable_paths")
    if not isinstance(writable, list) or len(writable) != len(set(writable)):
        raise ItemError("TARGET writable paths differ")
    owned = [work / safe_relative(value) for value in writable]
    if {path.name for path in owned} != REQUIRED_FILENAMES:
        raise ItemError("complete TARGET artifact set differs")
    for relative, path in zip(writable, owned):
        nonempty(path, relative)
    by_name = {path.name: path for path in owned}
    lean_paths = [by_name[name] for name in ("Statement.lean", "Proof.lean", "Audit.lean")]
    crosswalk = strict_json(by_name["statement-crosswalk.json"], "statement crosswalk")
    machine = strict_json(by_name["machine-closure.json"], "machine closure")
    semantic_sha = semantic_environment(crosswalk, member, lean_paths, work, machine)
    identity = {"program": PROGRAM, "item_id": item_id, "stage_claim_id": stage_claim_id}
    validate_machine(machine, identity, semantic_sha)
    validate_readability(strict_json(by_name["readability-review.json"], "readability review"), identity)
    validate_release(strict_json(by_name["release-decision.json"], "release decision"), identity, semantic_sha)
    if compile_files:
        lean_root, toolchain = kernel_route(member, canonical_root)
        audit_completed: subprocess.CompletedProcess[str] | None = None
        for path in lean_paths:
            completed = compile_lean(
                path, canonical_root, timeout_seconds=compile_timeout_seconds,
                lean_root=lean_root, toolchain=toolchain,
            )
            if path.name == "Audit.lean":
                audit_completed = completed
        if audit_completed is None:
            raise ItemError("Audit.lean was not compiled")
        observed_axioms = reported_root_axioms(
            audit_completed.stdout + "\n" + audit_completed.stderr,
            machine["root_declaration"],
        )
        if observed_axioms != machine["observed_axioms"]:
            raise ItemError("machine closure terminal axiom report differs from Lean")
    return {
        "valid": True, "item_id": item_id, "stage_claim_id": stage_claim_id,
        "semantic_environment_sha256": semantic_sha,
        "owned_paths": writable,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-card", type=Path, required=True)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--no-lean", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args(argv)
    try:
        claim_path = arguments.claim_card.resolve()
        claim = strict_json(claim_path, "claim card")
        if claim.get("program") != PROGRAM:
            raise ItemError("claim program differs")
        task_root = claim_path.parent
        if Path(claim.get("task_root", "")).resolve() != task_root:
            raise ItemError("claim task root differs")
        work = (arguments.work_root or (task_root / "work")).resolve()
        canonical_root = Path(claim.get("canonical_repository_root", "")).resolve()
        runtime = canonical_root / ".ops/stage5-theorems-execution-v2/tasks"
        try:
            work.relative_to(runtime)
        except ValueError as exc:
            raise ItemError("validation work root escapes the theorem runtime") from exc
        result = validate_target(
            claim, work, canonical_root, compile_files=not arguments.no_lean,
        )
    except (ItemError, OSError, KeyError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
