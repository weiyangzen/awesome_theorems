#!/usr/bin/env python3
"""Validate the historical THM-M-0387 dossier fixture.

This compatibility validator can replay the retained dossier's internal claims,
but it has no current Stage1 v2 phase, admission, acceptance, or release
authority. Current requirements and task state come only from the v2 blueprint.
"""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, deque
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn


SCHEMA_VERSION = "5.6"
BLUEPRINT_PATH = "Docs/Stage1_Blueprint_v2.md"
THEOREM_ID = "THM-M-0387"
NODE_FIELDS = {
    "node_id",
    "parent_ids",
    "child_ids",
    "kind",
    "human_statement",
    "formal_target",
    "inputs",
    "output",
    "composition_edge",
    "human_debt",
    "machine_debt",
    "readability_debt",
    "evidence_tiers",
    "source_and_revision",
    "proof_body_location",
    "axioms_and_classical_use",
    "automation_or_computation",
    "step_budget",
    "public_readable_target",
    "validation_command",
    "status_boundary",
    "dependencies",
    "owned_paths",
    # Historical execution fields made explicit by this instance.
    "title",
    "evidence_refs",
    "axiom_report",
    "placeholder_state",
    "trust_boundary",
    "step_ledger",
    "status",
    "blocker",
    "public_surface",
    "targets",
    "lean4",
}
INTAKE_FIELDS = {
    "theorem_id",
    "canonical_name",
    "canonical_statement",
    "formal_statement_target",
    "domain_and_universes",
    "quantifiers",
    "hypotheses",
    "conclusion",
    "equivalent_forms",
    "excluded_degenerate_cases",
    "logic_and_axiom_policy",
    "formal_system",
    "source_revisions",
    "authoritative_blueprint",
    "public_merge_targets",
}
TOP_LEVEL_FIELDS = {
    "schema_version",
    "theorem_id",
    "root_id",
    "generated_on",
    "authoritative_blueprint",
    "theorem_intake",
    "pins",
    "source_revisions",
    "axiom_policy",
    "evidence_levels",
    "debt_scales",
    "coverage_metrics",
    "public_surfaces",
    "nodes",
}
KINDS = {
    "root",
    "definition",
    "normalization",
    "reduction",
    "branch",
    "construction",
    "bridge",
    "core_lemma",
    "computation",
    "certificate",
    "transport",
    "terminal",
}
H_DEBTS = {f"H{i}" for i in range(6)}
M_DEBTS = {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
R_DEBTS = {f"R{i}" for i in range(5)}
EVIDENCE_TIERS = {f"E{i}" for i in range(6)}
PROOF_BODY_LOCATIONS = {"local", "mathlib", "pinned_external", "none"}
STATUSES = {"machine_closed", "machine_partial", "machine_open", "blocked"}
TARGET_KEYS = {"classification", "machine", "readable", "human_source"}
METRIC_SPECS = {
    "tree_classification": ("classification", lambda n: True),
    "machine_closure": ("machine", lambda n: n["machine_debt"].startswith("M0-")),
    "readable_closure": ("readable", lambda n: n["readability_debt"] == "R0"),
    "human_source": ("human_source", lambda n: n["human_debt"] == "H0"),
}
M0_EVIDENCE = {"M0-L": "E0", "M0-W": "E1", "M0-P": "E1"}
M0_LOCATION = {"M0-L": "local", "M0-W": "mathlib", "M0-P": "pinned_external"}
EXPECTED_PUBLIC_ROLES = {
    "theorem_readme",
    "machine_metadata",
    "proof_outline",
    "proof_unit_manifest",
    "machine_audit",
    "process_tree_audit",
    "long_readable_proof",
    "build_validation",
    "formal_source_tree",
}
LOCAL_SOURCE_ROOTS = {
    "local": None,
    "mathlib": Path("Formalizations/Lean/.lake/packages/mathlib"),
    "pinned_external": Path("Formalizations/Lean/.lake/packages/flt-regular"),
}
ACCEPTED_LEAN_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PLACEHOLDER_TOKEN = re.compile(r"\b(?:sorry|admit|sorryAx)\b")
CUSTOM_DECL_TOKEN = re.compile(r"^\s*(?:axiom|constant)\s+([^\s:{(]+)", re.MULTILINE)
PRIVATE_PUBLIC_PATTERN = re.compile(
    r"(?:/Users/|/home/|/tmp(?:/|\b)|/var/folders/|[A-Za-z]:\\Users\\|"
    r"\bPID\s*[:=#]?\s*\d+|\bprocess[-_ ]?pid\b|\bpid[-_ ]file\b|\btmux\b|"
    r"\.cron(?:/|\b)|\.ops(?:/|\b)|"
    r"runtime[-_ ](?:log|ledger|path)|worker[-_ ](?:log|ledger|path))",
    re.IGNORECASE,
)
CHECKLIST_ID = re.compile(r"^S56-M0387-[A-Z][0-9]{2}$")
LEAN_DECL = re.compile(r"^[A-Za-z_][A-Za-z0-9_'.]*(?:\.[A-Za-z_][A-Za-z0-9_']*)*$")


def fail(message: str) -> NoReturn:
    raise SystemExit(f"lint_theorem_dossier: {message}")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        fail(f"cannot execute {args[0]!r}: {exc}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")
    ensure(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalized_lean_type(value: str) -> str:
    """Normalize harmless presentation differences, not mathematical syntax."""
    return re.sub(r"\s+", "", value).replace("AwesomeTheorems.NumberTheory.THM_M_0387.", "")


def string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(nonempty_string(item) for item in value)
    )


def stable_repo_path(value: Any, field: str, repo_root: Path, *, must_exist: bool = True) -> Path:
    ensure(nonempty_string(value), f"{field} must be a nonempty repo-relative path")
    raw = value.split("#", 1)[0]
    ensure(not raw.startswith(("/", "~")), f"{field} must not be absolute: {value!r}")
    pure = PurePosixPath(raw)
    ensure(".." not in pure.parts and "." not in pure.parts, f"{field} must not escape the repo: {value!r}")
    ensure("\\" not in raw, f"{field} must use POSIX separators: {value!r}")
    ensure(not PRIVATE_PUBLIC_PATTERN.search(value), f"{field} contains a private/runtime reference: {value!r}")
    path = repo_root / raw
    ensure(not path.is_symlink(), f"{field} must not be a symlink: {value!r}")
    if must_exist:
        ensure(path.exists(), f"{field} does not exist: {value!r}")
    return path


def github_anchor(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r" +", "-", text)


def assert_markdown_anchor(value: str, field: str, repo_root: Path) -> None:
    path = stable_repo_path(value, field, repo_root)
    if "#" not in value:
        return
    ensure(path.suffix.lower() == ".md", f"{field} uses a heading on a non-Markdown path: {value!r}")
    fragment = value.split("#", 1)[1]
    ensure(bool(fragment), f"{field} has an empty heading fragment: {value!r}")
    headings: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.add(github_anchor(match.group(1)))
    ensure(fragment in headings, f"{field} heading #{fragment} is absent from {path.relative_to(repo_root)}")


def git_paths(repo_root: Path, theorem_dir: Path) -> set[str]:
    rel_dir = theorem_dir.relative_to(repo_root).as_posix()
    outputs: dict[str, set[str]] = {}
    for label, args in {
        "tracked": ["git", "ls-files", "--", rel_dir],
        "deleted": ["git", "ls-files", "--deleted", "--", rel_dir],
        "untracked": ["git", "ls-files", "--others", "--exclude-standard", "--", rel_dir],
    }.items():
        result = run(args, repo_root)
        ensure(result.returncode == 0, result.stdout.strip() or f"git ls-files ({label}) failed")
        outputs[label] = {line for line in result.stdout.splitlines() if line}
    public_paths = (outputs["tracked"] - outputs["deleted"]) | outputs["untracked"]
    return {
        Path(path).relative_to(rel_dir).as_posix()
        for path in public_paths
        if Path(path).name != ".DS_Store"
    }


def assert_folder_contract(repo_root: Path, theorem_dir: Path, meta: dict[str, Any], *, allow_extra: bool = False) -> None:
    contract_value = meta.get("folder_contract")
    ensure(string_list(contract_value, nonempty=True), "meta.json folder_contract must be a nonempty string array")
    contract = set(contract_value)
    ensure(len(contract) == len(contract_value), "meta.json folder_contract contains duplicate paths")
    for index, value in enumerate(contract_value):
        stable_repo_path(f"{theorem_dir.relative_to(repo_root).as_posix()}/{value}", f"folder_contract[{index}]", repo_root)
    actual = git_paths(repo_root, theorem_dir)
    if contract != actual and not (allow_extra and contract <= actual):
        details = []
        if contract - actual:
            details.append(f"missing files: {sorted(contract - actual)}")
        if actual - contract:
            details.append(f"extra files: {sorted(actual - contract)}")
        fail("folder_contract mismatch; " + "; ".join(details))


def assert_top_level(manifest: dict[str, Any]) -> None:
    missing = sorted(TOP_LEVEL_FIELDS - manifest.keys())
    ensure(not missing, f"proof_units.json missing top-level fields: {missing}")
    ensure(str(manifest["schema_version"]) == SCHEMA_VERSION, f"schema_version must be {SCHEMA_VERSION!r}")
    ensure(manifest["theorem_id"] == THEOREM_ID, f"theorem_id must be {THEOREM_ID!r}")
    ensure(manifest["authoritative_blueprint"] == BLUEPRINT_PATH, f"authoritative_blueprint must be {BLUEPRINT_PATH!r}")
    ensure(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(manifest["generated_on"])) is not None,
           "generated_on must be an absolute YYYY-MM-DD date")

    intake = manifest["theorem_intake"]
    ensure(isinstance(intake, dict), "theorem_intake must be an object")
    missing_intake = sorted(INTAKE_FIELDS - intake.keys())
    ensure(not missing_intake, f"theorem_intake missing fields: {missing_intake}")
    ensure(intake["theorem_id"] == THEOREM_ID, "theorem_intake.theorem_id disagrees with theorem_id")
    ensure(intake["authoritative_blueprint"] == BLUEPRINT_PATH,
           "theorem_intake.authoritative_blueprint disagrees with the manifest")
    for field in INTAKE_FIELDS - {"quantifiers", "hypotheses", "equivalent_forms", "excluded_degenerate_cases", "source_revisions", "public_merge_targets"}:
        ensure(nonempty_string(intake[field]), f"theorem_intake.{field} must be a nonempty string")
    for field in {"quantifiers", "equivalent_forms", "excluded_degenerate_cases", "public_merge_targets"}:
        ensure(string_list(intake[field], nonempty=True), f"theorem_intake.{field} must be a nonempty string array")
    ensure(string_list(intake["hypotheses"]), "theorem_intake.hypotheses must be a string array (possibly empty)")
    ensure(isinstance(intake["source_revisions"], (dict, list)) and bool(intake["source_revisions"]),
           "theorem_intake.source_revisions must be a nonempty object or array")

    evidence_levels = manifest["evidence_levels"]
    debt_scales = manifest["debt_scales"]
    ensure(isinstance(evidence_levels, dict) and set(evidence_levels) == EVIDENCE_TIERS,
           f"evidence_levels must define exactly {sorted(EVIDENCE_TIERS)}")
    ensure(isinstance(debt_scales, dict), "debt_scales must be an object")
    for key, expected in {"human": H_DEBTS, "machine": M_DEBTS, "readability": R_DEBTS}.items():
        value = debt_scales.get(key)
        actual = set(value) if isinstance(value, list) else set(value) if isinstance(value, dict) else set()
        ensure(actual == expected, f"debt_scales.{key} must define exactly {sorted(expected)}")

    policy = manifest["axiom_policy"]
    ensure(isinstance(policy, dict), "axiom_policy must be an object")
    ensure(set(policy.get("accepted", [])) == ACCEPTED_LEAN_AXIOMS,
           f"axiom_policy.accepted must be exactly {sorted(ACCEPTED_LEAN_AXIOMS)}")
    disallowed = policy.get("disallowed")
    ensure(string_list(disallowed, nonempty=True), "axiom_policy.disallowed must be a nonempty string array")
    disallowed_text = " ".join(disallowed).lower()
    for token in ("sorry", "admit", "sorryax", "custom axiom"):
        ensure(token in disallowed_text, f"axiom_policy.disallowed must explicitly cover {token!r}")


def assert_node_shape(node: Any, index: int) -> None:
    ensure(isinstance(node, dict), f"nodes[{index}] must be an object")
    missing = sorted(NODE_FIELDS - node.keys())
    ensure(not missing, f"nodes[{index}] missing required fields: {missing}")
    node_id = node.get("node_id", f"nodes[{index}]")
    ensure(nonempty_string(node_id), f"nodes[{index}].node_id must be a nonempty string")
    for alias, canonical in (("id", "node_id"), ("dependency_ids", "dependencies")):
        if alias in node:
            ensure(node[alias] == node[canonical], f"{node_id}: {alias} disagrees with {canonical}")
    ensure(node["kind"] in KINDS, f"{node_id}: invalid kind {node['kind']!r}")
    ensure(node["human_debt"] in H_DEBTS, f"{node_id}: invalid human_debt {node['human_debt']!r}")
    ensure(node["machine_debt"] in M_DEBTS, f"{node_id}: invalid machine_debt {node['machine_debt']!r}")
    ensure(node["readability_debt"] in R_DEBTS,
           f"{node_id}: invalid readability_debt {node['readability_debt']!r}")
    ensure(node["proof_body_location"] in PROOF_BODY_LOCATIONS,
           f"{node_id}: invalid proof_body_location {node['proof_body_location']!r}")
    ensure(node["status"] in STATUSES, f"{node_id}: invalid status {node['status']!r}")
    for field in ("human_statement", "formal_target", "inputs", "output", "source_and_revision",
                  "axioms_and_classical_use", "automation_or_computation", "public_readable_target",
                  "validation_command", "status_boundary", "title", "axiom_report", "placeholder_state",
                  "trust_boundary"):
        ensure(nonempty_string(node[field]), f"{node_id}: {field} must be a nonempty string")
    for field in ("parent_ids", "child_ids", "dependencies", "owned_paths", "evidence_refs", "public_surface"):
        ensure(string_list(node[field], nonempty=(field in {"owned_paths", "evidence_refs", "public_surface"})),
               f"{node_id}: {field} must be {'a nonempty ' if field in {'owned_paths', 'evidence_refs', 'public_surface'} else 'a '}string array")
        ensure(len(node[field]) == len(set(node[field])), f"{node_id}: {field} contains duplicates")
    ensure(string_list(node["evidence_tiers"], nonempty=True), f"{node_id}: evidence_tiers must be nonempty")
    ensure(set(node["evidence_tiers"]) <= EVIDENCE_TIERS, f"{node_id}: invalid evidence_tiers")
    targets = node["targets"]
    ensure(isinstance(targets, dict) and set(targets) == TARGET_KEYS,
           f"{node_id}: targets must have exactly {sorted(TARGET_KEYS)}")
    ensure(all(isinstance(value, bool) for value in targets.values()), f"{node_id}: target values must be booleans")
    ensure(targets["classification"], f"{node_id}: every discovered required node must target classification")
    for field, values in (("dependencies", node["dependencies"]), ("owned_paths", node["owned_paths"])):
        for value in values:
            if field == "dependencies":
                ensure(CHECKLIST_ID.fullmatch(value) is not None,
                       f"{node_id}: invalid blueprint dependency id {value!r}")
            else:
                ensure(not value.startswith(("/", "~")) and ".." not in PurePosixPath(value).parts,
                       f"{node_id}: owned path must be stable and repo-relative: {value!r}")

    composition = node["composition_edge"]
    ensure(isinstance(composition, dict), f"{node_id}: composition_edge must be an object")
    ensure(composition.get("type") in {"checked", "open", "leaf"},
           f"{node_id}: composition_edge.type must be checked, open, or leaf")
    if composition["type"] == "checked":
        for field in ("declaration", "exact_type", "evidence_ref"):
            ensure(nonempty_string(composition.get(field)), f"{node_id}: checked composition missing {field}")
        ensure(composition.get("checked") is True, f"{node_id}: checked composition must set checked=true")
    elif composition["type"] == "open":
        ensure(nonempty_string(composition.get("reason")), f"{node_id}: open composition missing reason")

    is_leaf = not node["child_ids"]
    ledger = node["step_ledger"]
    ensure(isinstance(ledger, list), f"{node_id}: step_ledger must be an array")
    if is_leaf:
        budget = node["step_budget"]
        ensure(isinstance(budget, int) and not isinstance(budget, bool) and 1 <= budget <= 100,
               f"{node_id}: final leaf step_budget must be an integer in 1..100")
        ensure(len(ledger) == budget,
               f"{node_id}: leaf step_ledger count must equal step_budget (got {len(ledger)}, budget {budget})")
        for step_index, entry in enumerate(ledger, start=1):
            ensure(isinstance(entry, dict) and set(entry) >= {"step", "claim"},
                   f"{node_id}: step_ledger[{step_index - 1}] must contain step and claim")
            ensure(entry["step"] == step_index, f"{node_id}: step_ledger numbering must be contiguous from 1")
            ensure(nonempty_string(entry["claim"]), f"{node_id}: step {step_index} claim must be nonempty")
        if node["machine_debt"].startswith("M0-"):
            ensure(composition["type"] == "checked",
                   f"{node_id}: a machine-closed leaf must use a checked composition edge")
        else:
            ensure(composition["type"] in {"open", "leaf"} and nonempty_string(composition.get("reason")),
                   f"{node_id}: a machine-open leaf must record an open/leaf composition reason")
    else:
        ensure(node["step_budget"] is None, f"{node_id}: nonleaf step_budget must be null")
        ensure(not ledger, f"{node_id}: nonleaf step_ledger must be []")
        ensure(composition["type"] != "leaf", f"{node_id}: nonleaf cannot have a leaf composition edge")

    m_debt = node["machine_debt"]
    evidence = set(node["evidence_tiers"])
    if m_debt.startswith("M0-"):
        ensure(M0_EVIDENCE[m_debt] in evidence,
               f"{node_id}: {m_debt} requires {M0_EVIDENCE[m_debt]} evidence")
        ensure(node["proof_body_location"] == M0_LOCATION[m_debt],
               f"{node_id}: {m_debt} requires proof_body_location={M0_LOCATION[m_debt]!r}")
        ensure(node["status"] == "machine_closed", f"{node_id}: {m_debt} requires status=machine_closed")
        ensure(node["targets"]["machine"], f"{node_id}: every M0-* node must count as a machine target")
        ensure(node["blocker"] is None, f"{node_id}: machine-closed node cannot carry a blocker")
        ensure(node["readability_debt"] == "R0",
               f"{node_id}: every released M0-* node must be R0 under the historical gate")
        ensure(isinstance(node["lean4"], dict), f"{node_id}: {m_debt} requires a lean4 evidence object")
    else:
        ensure(node["lean4"] is None, f"{node_id}: only M0-* nodes may carry local Lean closure evidence")
        ensure(node["status"] != "machine_closed", f"{node_id}: non-M0 node cannot be machine_closed")
        if not node["targets"]["machine"]:
            ensure(bool(node["parent_ids"]), f"{node_id}: an evidence-overlay node must be connected below the root")
            ensure("overlay" in (node["status_boundary"] + " " + str(node["blocker"])).lower(),
                   f"{node_id}: a non-machine-target node must explicitly identify itself as a connected evidence overlay")
    if m_debt == "M1":
        ensure("E2" in evidence, f"{node_id}: M1 requires E2")
    if m_debt == "M5":
        ensure(node["status"] == "blocked" and nonempty_string(node["blocker"]),
               f"{node_id}: M5 requires blocked status and a concrete blocker")
    if m_debt in {"M2", "M3", "M4"}:
        ensure(nonempty_string(node["blocker"]), f"{node_id}: open/partial machine debt needs a concrete blocker")
    if node["human_debt"] == "H0":
        ensure("E4" in evidence, f"{node_id}: H0 requires E4 primary human evidence")
    if node["readability_debt"] == "R0":
        ensure(targets["readable"], f"{node_id}: R0 must count as a readable target")


def assert_tree(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes = manifest["nodes"]
    ensure(isinstance(nodes, list) and nodes, "nodes must be a nonempty array")
    for index, node in enumerate(nodes):
        assert_node_shape(node, index)
    ids = [node["node_id"] for node in nodes]
    duplicates = sorted(node_id for node_id, count in Counter(ids).items() if count > 1)
    ensure(not duplicates, f"duplicate node ids: {duplicates}")
    by_id = {node["node_id"]: node for node in nodes}
    root_id = manifest["root_id"]
    ensure(root_id in by_id, f"root_id {root_id!r} does not reference a node")
    roots = [node["node_id"] for node in nodes if not node["parent_ids"]]
    ensure(roots == [root_id], f"manifest must have exactly one parentless root {root_id!r}; found {roots}")
    ensure(by_id[root_id]["kind"] == "root", f"root node {root_id} must have kind=root")

    for node in nodes:
        node_id = node["node_id"]
        for child_id in node["child_ids"]:
            ensure(child_id in by_id, f"{node_id}: unknown child {child_id!r}")
            ensure(node_id in by_id[child_id]["parent_ids"],
                   f"edge {node_id} -> {child_id} is not reciprocal in parent_ids")
        for parent_id in node["parent_ids"]:
            ensure(parent_id in by_id, f"{node_id}: unknown parent {parent_id!r}")
            ensure(node_id in by_id[parent_id]["child_ids"],
                   f"edge {parent_id} -> {node_id} is not reciprocal in child_ids")
        ensure(node_id not in node["child_ids"] and node_id not in node["parent_ids"],
               f"{node_id}: self edge is forbidden")

    indegree = {node_id: len(node["parent_ids"]) for node_id, node in by_id.items()}
    queue = deque(sorted(node_id for node_id, degree in indegree.items() if degree == 0))
    seen: list[str] = []
    while queue:
        node_id = queue.popleft()
        seen.append(node_id)
        for child_id in by_id[node_id]["child_ids"]:
            indegree[child_id] -= 1
            if indegree[child_id] == 0:
                queue.append(child_id)
    ensure(len(seen) == len(nodes), f"proof tree contains a cycle involving {sorted(set(by_id) - set(seen))}")

    reachable: set[str] = set()
    queue = deque([root_id])
    while queue:
        node_id = queue.popleft()
        if node_id in reachable:
            continue
        reachable.add(node_id)
        queue.extend(by_id[node_id]["child_ids"])
    ensure(reachable == set(by_id), f"nodes disconnected from root {root_id}: {sorted(set(by_id) - reachable)}")

    for node in nodes:
        node_id = node["node_id"]
        m_children = [by_id[c] for c in node["child_ids"] if by_id[c]["targets"]["machine"]]
        if node["machine_debt"].startswith("M0-") and m_children:
            edge = node["composition_edge"]
            ensure(edge["type"] == "checked" and nonempty_string(edge.get("declaration")),
                   f"{node_id}: closed parent requires a named checked composition edge")
            open_children = [child["node_id"] for child in m_children if not child["machine_debt"].startswith("M0-")]
            ensure(not open_children,
                   f"{node_id}: closed parent has machine-required nonclosed children {open_children}")
        if node["machine_debt"].startswith("M0-") and node["child_ids"]:
            lean4 = node["lean4"]
            edge = node["composition_edge"]
            ensure(lean4.get("composition_declaration") == edge.get("declaration"),
                   f"{node_id}: checked composition declaration is absent/mismatched in lean4 evidence")
            ensure(lean4.get("composition_expected_type") == edge.get("exact_type"),
                   f"{node_id}: checked composition exact type is absent/mismatched in lean4 evidence")
    return by_id


def assert_metrics(manifest: dict[str, Any], nodes: list[dict[str, Any]]) -> None:
    metrics = manifest["coverage_metrics"]
    ensure(isinstance(metrics, dict), "coverage_metrics must be an object")
    for metric_name, (target_key, closes) in METRIC_SPECS.items():
        claimed = metrics.get(metric_name)
        ensure(isinstance(claimed, dict), f"coverage_metrics.{metric_name} must be an object")
        required = [node for node in nodes if node["targets"][target_key]]
        numerator = sum(bool(closes(node)) for node in required)
        denominator = len(required)
        ensure(denominator > 0, f"coverage_metrics.{metric_name} has an empty denominator")
        percent = round(100 * numerator / denominator, 2)
        ensure(claimed.get("numerator") == numerator and claimed.get("denominator") == denominator,
               f"coverage_metrics.{metric_name} must be recomputed as {numerator}/{denominator}, got "
               f"{claimed.get('numerator')}/{claimed.get('denominator')}")
        claimed_percent = claimed.get("percent")
        ensure(isinstance(claimed_percent, (int, float)) and not isinstance(claimed_percent, bool)
               and math.isclose(float(claimed_percent), percent, abs_tol=0.01),
               f"coverage_metrics.{metric_name}.percent must be {percent}")
    root_closed = next(node for node in nodes if node["node_id"] == manifest["root_id"])["machine_debt"].startswith("M0-")
    ensure(metrics.get("root_machine_closed") is root_closed,
           f"coverage_metrics.root_machine_closed must be {root_closed}")


def assert_public_status_consistency(
    meta: dict[str, Any], manifest: dict[str, Any], repo_root: Path, probe_count: int
) -> None:
    """Keep the durable summaries tied to the recomputed manifest result."""
    metrics = manifest["coverage_metrics"]
    ensure(meta.get("coverage_metrics") == metrics,
           "meta.json coverage_metrics must exactly equal proof_units.json coverage_metrics")
    ensure(meta.get("status") == "部分验证", "meta.json status must remain 部分验证 while root is open")
    status_detail = str(meta.get("status_detail", ""))
    ensure("[H1, M2, R0]" in status_detail and "no placeholder-free" in status_detail,
           "meta.json status_detail must preserve the exact open-root vector and blocker")

    validation = meta.get("repo_local_validation")
    ensure(isinstance(validation, dict), "meta.json repo_local_validation must be an object")
    ensure(validation.get("status") == "pass" and validation.get("exit_code") == 0,
           "meta.json must record the passing canonical local validation")
    ensure(validation.get("lean_probe_check_count") == probe_count,
           f"meta.json lean_probe_check_count must be {probe_count}")
    checked_modules = validation.get("checked_modules")
    ensure(string_list(checked_modules, nonempty=True),
           "meta.json repo_local_validation.checked_modules must be nonempty")
    ensure("AwesomeTheorems.NumberTheory.THM_M_0387.InternalCoveragePath" in checked_modules,
           "meta.json checked_modules must include InternalCoveragePath")

    formalization = meta.get("formalization_status")
    ensure(isinstance(formalization, dict), "meta.json formalization_status must be an object")
    ensure(formalization.get("overall") == "partial"
           and formalization.get("repo_local_full_theorem") is False
           and formalization.get("repo_local_full_theorem_name") is None,
           "meta.json must not claim repo-local exact-root closure")

    summary_files = [
        "THM-M-0387/README.md",
        "THM-M-0387/proof_outline.md",
        "THM-M-0387/machine_checked_audit.md",
        "THM-M-0387/process_audit.md",
        "THM-M-0387/build_validation.md",
    ]
    required_patterns = {
        "tree classification 132/132": re.compile(r"132\s*/\s*132"),
        "machine closure 29/93": re.compile(r"29\s*/\s*93"),
        "machine percent 31.18": re.compile(r"31\.18\s*%"),
        "human-source closure 0/113": re.compile(r"0\s*/\s*113"),
        "exact root vector": re.compile(r"\[\s*H1\s*,\s*M2\s*,\s*R0\s*\]"),
    }
    for rel in summary_files:
        text = (repo_root / rel).read_text(encoding="utf-8")
        missing = [label for label, pattern in required_patterns.items() if pattern.search(text) is None]
        ensure(not missing, f"{rel} is missing final public status fields: {missing}")

def assert_public_surfaces(manifest: dict[str, Any], nodes: list[dict[str, Any]], repo_root: Path) -> set[Path]:
    surfaces = manifest["public_surfaces"]
    ensure(isinstance(surfaces, dict), "public_surfaces must be an object")
    missing = EXPECTED_PUBLIC_ROLES - surfaces.keys()
    ensure(not missing, f"public_surfaces missing roles: {sorted(missing)}")
    public_files: set[Path] = set()
    for role in EXPECTED_PUBLIC_ROLES:
        values = surfaces[role] if isinstance(surfaces[role], list) else [surfaces[role]]
        ensure(string_list(values, nonempty=True), f"public_surfaces.{role} must be a path or nonempty path array")
        for index, value in enumerate(values):
            path = stable_repo_path(value, f"public_surfaces.{role}[{index}]", repo_root)
            if path.is_file() and path.suffix.lower() in {".md", ".json"}:
                public_files.add(path)
    intake_targets = manifest["theorem_intake"]["public_merge_targets"]
    for index, value in enumerate(intake_targets):
        public_files.add(stable_repo_path(value, f"theorem_intake.public_merge_targets[{index}]", repo_root))
    for node in nodes:
        node_id = node["node_id"]
        assert_markdown_anchor(node["public_readable_target"], f"{node_id}.public_readable_target", repo_root)
        for index, value in enumerate(node["public_surface"]):
            assert_markdown_anchor(value, f"{node_id}.public_surface[{index}]", repo_root)
            path = repo_root / value.split("#", 1)[0]
            if path.suffix.lower() in {".md", ".json"}:
                public_files.add(path)
    for path in sorted(public_files):
        ensure(path.is_file(), f"public surface must be a file: {path.relative_to(repo_root)}")
        if path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8")
            match = PRIVATE_PUBLIC_PATTERN.search(text)
            if match is not None:
                fail(
                    f"stable public surface {path.relative_to(repo_root)} contains forbidden "
                    f"private/runtime text {match.group(0)!r}"
                )
    return public_files


def manifest_packages(lake_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    packages = lake_manifest.get("packages")
    ensure(isinstance(packages, list), "lake-manifest.json has no packages array")
    result: dict[str, dict[str, Any]] = {}
    for package in packages:
        if not isinstance(package, dict):
            continue
        name = str(package.get("name", "")).strip("«»")
        if name:
            result[name] = package
    return result


def pin_revision(pin: Any, field: str) -> str:
    if isinstance(pin, str):
        revision = pin
    elif isinstance(pin, dict):
        revision = pin.get("revision") or pin.get("commit")
    else:
        revision = None
    ensure(isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}", revision) is not None,
           f"{field} must contain a full 40-hex revision")
    return revision


def assert_pins(manifest: dict[str, Any], repo_root: Path) -> None:
    pins = manifest["pins"]
    ensure(isinstance(pins, dict), "pins must be an object")
    for name in ("lean", "mathlib", "flt_regular", "checkdecls", "imperial_candidate"):
        ensure(name in pins, f"pins missing {name}")
    lean = pins["lean"]
    ensure(isinstance(lean, dict) and nonempty_string(lean.get("version")), "pins.lean.version is required")
    lean_commit = pin_revision(lean, "pins.lean")
    toolchain = (repo_root / "Formalizations/Lean/lean-toolchain").read_text(encoding="utf-8").strip()
    ensure(toolchain.endswith(f"v{lean['version']}") or toolchain.endswith(str(lean["version"])),
           f"lean-toolchain {toolchain!r} disagrees with pins.lean.version={lean['version']!r}")
    toolchain_lean = (
        Path.home()
        / ".elan/toolchains"
        / f"leanprover--lean4---v{lean['version']}"
        / "bin/lean"
    )
    ensure(toolchain_lean.is_file(), f"pinned Lean binary is missing: {toolchain_lean}")
    lean_result = run([str(toolchain_lean), "--version"], repo_root)
    ensure(lean_result.returncode == 0, lean_result.stdout.strip() or "lean --version failed")
    ensure(str(lean["version"]) in lean_result.stdout and lean_commit in lean_result.stdout,
           f"local Lean version/commit disagrees with manifest: {lean_result.stdout.strip()}")

    lake_manifest = load_json(repo_root / "Formalizations/Lean/lake-manifest.json")
    packages = manifest_packages(lake_manifest)
    package_map = {"mathlib": "mathlib", "flt_regular": "flt-regular", "checkdecls": "checkdecls"}
    lakefile = (repo_root / "Formalizations/Lean/lakefile.lean").read_text(encoding="utf-8")
    for pin_name, package_name in package_map.items():
        revision = pin_revision(pins[pin_name], f"pins.{pin_name}")
        package = packages.get(package_name)
        ensure(package is not None, f"lake-manifest.json is missing {package_name}")
        ensure(package.get("rev") == revision,
               f"{pin_name} manifest pin {revision} disagrees with lake-manifest rev {package.get('rev')}")
        package_dir = repo_root / f"Formalizations/Lean/.lake/packages/{package_name}"
        ensure(package_dir.is_dir(), f"local pinned dependency checkout is missing: {package_dir.relative_to(repo_root)}")
        head = run(["git", "rev-parse", "HEAD"], package_dir)
        ensure(head.returncode == 0 and head.stdout.strip() == revision,
               f"{pin_name} local dependency HEAD disagrees with pin: {head.stdout.strip()!r} != {revision!r}")
        if pin_name in {"mathlib", "flt_regular"}:
            ensure(revision in lakefile, f"lakefile.lean does not directly pin {pin_name} revision {revision}")
    pin_revision(pins["imperial_candidate"], "pins.imperial_candidate")

    revisions = manifest["source_revisions"]
    ensure(isinstance(revisions, dict), "source_revisions must be an object")
    for pin_name in ("mathlib", "flt_regular", "checkdecls", "imperial_candidate"):
        ensure(pin_name in revisions, f"source_revisions missing {pin_name}")
        ensure(pin_revision(revisions[pin_name], f"source_revisions.{pin_name}") == pin_revision(pins[pin_name], f"pins.{pin_name}"),
               f"source_revisions.{pin_name} disagrees with pins.{pin_name}")


def strip_lean_comments_and_strings(text: str) -> str:
    """Replace Lean comments and string contents while preserving newlines."""
    out: list[str] = []
    index = 0
    block_depth = 0
    in_line = False
    in_string = False
    while index < len(text):
        pair = text[index:index + 2]
        char = text[index]
        if in_line:
            if char == "\n":
                in_line = False
                out.append("\n")
            else:
                out.append(" ")
            index += 1
            continue
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if in_string:
            if char == "\\" and index + 1 < len(text):
                out.extend("  ")
                index += 2
            elif char == '"':
                in_string = False
                out.append(" ")
                index += 1
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if pair == "--":
            in_line = True
            out.extend("  ")
            index += 2
        elif pair == "/-":
            block_depth = 1
            out.extend("  ")
            index += 2
        elif char == '"':
            in_string = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    return "".join(out)


def assert_clean_lean_source(path: Path, display: str) -> None:
    ensure(path.is_file(), f"Lean proof source is missing: {display}")
    cleaned = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
    placeholder = PLACEHOLDER_TOKEN.search(cleaned)
    if placeholder is not None:
        fail(f"disallowed Lean placeholder {placeholder.group(0)!r} in {display}")
    custom = CUSTOM_DECL_TOKEN.search(cleaned)
    if custom is not None:
        fail(f"unreviewed custom declaration {custom.group(0)!r} in {display}")


def source_contains_declaration(path: Path, declaration: str) -> bool:
    cleaned = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
    short_name = declaration.rsplit(".", 1)[-1]
    return re.search(rf"^\s*(?:theorem|lemma|def|abbrev)\s+{re.escape(short_name)}\b", cleaned, re.MULTILINE) is not None


def assert_local_and_pinned_source_scans(repo_root: Path) -> None:
    targets = [
        repo_root / "Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387",
        repo_root / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_001.lean",
        repo_root / "THM-M-0387/FermatLastTheorem_Sample.lean",
        repo_root / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/FLT",
        repo_root / "Formalizations/Lean/.lake/packages/flt-regular/FltRegular",
    ]
    for target in targets:
        ensure(target.exists(), f"required source scan target is missing: {target.relative_to(repo_root)}")
        paths = [target] if target.is_file() else sorted(target.rglob("*.lean"))
        ensure(paths, f"source scan target has no Lean files: {target.relative_to(repo_root)}")
        for path in paths:
            assert_clean_lean_source(path, path.relative_to(repo_root).as_posix())


def assert_lean_evidence(nodes: list[dict[str, Any]], repo_root: Path) -> int:
    lean_root = repo_root / "Formalizations/Lean"
    imports: set[str] = set()
    probes: list[tuple[str, str, list[str]]] = []
    composition_seen: set[tuple[str, str]] = set()
    for node in nodes:
        if not node["machine_debt"].startswith("M0-"):
            continue
        node_id = node["node_id"]
        lean4 = node["lean4"]
        required = {"imports", "declaration", "expected_type", "axioms", "local_wrapper", "source_file"}
        missing = sorted(required - lean4.keys())
        ensure(not missing, f"{node_id}: lean4 evidence missing {missing}")
        ensure(string_list(lean4["imports"], nonempty=True), f"{node_id}: lean4.imports must be nonempty")
        for module in lean4["imports"]:
            ensure(re.fullmatch(r"[A-Za-z0-9_'.]+", module) is not None,
                   f"{node_id}: invalid Lean import module {module!r}")
            imports.add(module)
        declaration = lean4["declaration"]
        ensure(nonempty_string(declaration) and LEAN_DECL.fullmatch(declaration) is not None,
               f"{node_id}: invalid lean4.declaration {declaration!r}")
        ensure(nonempty_string(lean4["expected_type"]), f"{node_id}: lean4.expected_type must be nonempty")
        ensure(normalized_lean_type(node["formal_target"]) == normalized_lean_type(lean4["expected_type"]),
               f"{node_id}: formal_target does not exactly match lean4.expected_type; "
               f"{node['formal_target']!r} != {lean4['expected_type']!r}")
        ensure(string_list(lean4["axioms"]), f"{node_id}: lean4.axioms must be a string array")
        ensure(set(lean4["axioms"]) <= ACCEPTED_LEAN_AXIOMS,
               f"{node_id}: lean4.axioms contains a disallowed axiom: {lean4['axioms']}")
        wrapper = lean4["local_wrapper"]
        ensure(nonempty_string(wrapper) and LEAN_DECL.fullmatch(wrapper) is not None,
               f"{node_id}: lean4.local_wrapper must name a declaration")
        source_path = stable_repo_path(lean4["source_file"], f"{node_id}.lean4.source_file", repo_root)
        ensure(source_path.suffix == ".lean", f"{node_id}: lean4.source_file must be a Lean file")
        ensure(source_contains_declaration(source_path, wrapper),
               f"{node_id}: local wrapper {wrapper} is not declared in {lean4['source_file']}")
        ensure(declaration == wrapper,
               f"{node_id}: M0 evidence must check its named repo-local wrapper directly; "
               f"declaration {declaration!r} != local_wrapper {wrapper!r}")
        assert_clean_lean_source(source_path, lean4["source_file"])

        proof_source = lean4.get("proof_body_source")
        if node["proof_body_location"] in {"mathlib", "pinned_external"}:
            ensure(nonempty_string(proof_source),
                   f"{node_id}: {node['machine_debt']} requires the nonlocal proof_body_source path")
        if node["proof_body_location"] == "local":
            ensure(proof_source in {None, lean4["source_file"]},
                   f"{node_id}: M0-L proof_body_source must be omitted or equal its repo-local source_file")
        if proof_source is not None:
            ensure(nonempty_string(proof_source), f"{node_id}: proof_body_source must be a nonempty path")
            base = LOCAL_SOURCE_ROOTS[node["proof_body_location"]]
            if base is None:
                proof_path = stable_repo_path(proof_source, f"{node_id}.lean4.proof_body_source", repo_root)
            else:
                ensure(not proof_source.startswith(("/", "~")) and ".." not in PurePosixPath(proof_source).parts,
                       f"{node_id}: proof_body_source must be package-relative")
                proof_path = repo_root / base / proof_source
                ensure(proof_path.is_file(), f"{node_id}: proof body source is missing: {proof_path.relative_to(repo_root)}")
            assert_clean_lean_source(proof_path, proof_path.relative_to(repo_root).as_posix())
        probes.append((node_id, declaration, list(lean4["axioms"])))

        composition = node["composition_edge"]
        if composition["type"] == "checked":
            comp_decl = lean4.get("composition_declaration")
            comp_type = lean4.get("composition_expected_type")
            ensure(comp_decl == composition["declaration"] and comp_type == composition["exact_type"],
                   f"{node_id}: Lean composition evidence must exactly match composition_edge")
            ensure(normalized_lean_type(node["formal_target"]) == normalized_lean_type(comp_type),
                   f"{node_id}: formal_target does not exactly match the checked composition type")
            key = (comp_decl, comp_type)
            if key not in composition_seen:
                composition_seen.add(key)
                # Composition axioms are checked through their node declaration when identical;
                # otherwise they get an independent accepted-policy probe.
                if comp_decl != declaration:
                    probes.append((f"{node_id}:composition", comp_decl, list(lean4.get("composition_axioms", lean4["axioms"]))))

    ensure(probes, "manifest contains no M0-* Lean evidence to validate")
    body: list[str] = [*(f"import {module}" for module in sorted(imports)), ""]
    for index, node in enumerate(nodes):
        if not node["machine_debt"].startswith("M0-"):
            continue
        declaration = node["lean4"]["declaration"]
        expected_type = node["lean4"]["expected_type"]
        body.extend([
            f"example : {expected_type} := by",
            f"  exact {declaration}",
            "",
        ])
        composition = node["composition_edge"]
        if composition["type"] == "checked" and composition["declaration"] != declaration:
            body.extend([
                f"example : {composition['exact_type']} := by",
                f"  exact {composition['declaration']}",
                "",
            ])
    for index, (node_id, declaration, _) in enumerate(probes):
        marker = f"{index}|{node_id}"
        body.extend([
            f'#eval IO.println "AXIOM_PROBE_BEGIN|{marker}"',
            f"#print axioms {declaration}",
            f'#eval IO.println "AXIOM_PROBE_END|{marker}"',
            "",
        ])

    fd, raw_path = tempfile.mkstemp(prefix="m0387-historical-probe-", suffix=".lean", dir=lean_root)
    probe_path = Path(raw_path)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write("\n".join(body))
        elan_home = os.environ.get("ELAN_HOME")
        elan = Path(elan_home) / "bin" / "elan" if elan_home else None
        if elan is None or not elan.is_file():
            resolved = shutil.which("elan")
            elan = Path(resolved) if resolved else None
        ensure(elan is not None and elan.is_file(),
               "official elan is unavailable; set ELAN_HOME or put elan on PATH")
        toolchain = (lean_root / "lean-toolchain").read_text(encoding="utf-8").strip()
        result = run(
            [str(elan), "run", toolchain, "lake", "env", "lean", probe_path.name],
            lean_root,
        )
        ensure(result.returncode == 0, "exact-type/axiom Lean probe failed:\n" + result.stdout)
        for index, (node_id, _, expected_axioms) in enumerate(probes):
            marker = re.escape(f"{index}|{node_id}")
            match = re.search(
                rf"AXIOM_PROBE_BEGIN\|{marker}\n(.*?)\nAXIOM_PROBE_END\|{marker}",
                result.stdout,
                re.DOTALL,
            )
            ensure(match is not None, f"{node_id}: could not parse #print axioms output")
            report = match.group(1).strip()
            if "does not depend on any axioms" in report:
                actual: set[str] = set()
            else:
                axiom_match = re.search(r"depends on axioms:\s*\[([^]]*)\]", report)
                ensure(axiom_match is not None, f"{node_id}: unexpected #print axioms output: {report!r}")
                actual = {item.strip() for item in axiom_match.group(1).split(",") if item.strip()}
            ensure(actual == set(expected_axioms),
                   f"{node_id}: axiom report mismatch; expected {sorted(expected_axioms)}, got {sorted(actual)}")
            ensure(actual <= ACCEPTED_LEAN_AXIOMS,
                   f"{node_id}: #print axioms reports disallowed axioms {sorted(actual - ACCEPTED_LEAN_AXIOMS)}")
    finally:
        probe_path.unlink(missing_ok=True)
    return len(probes)


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    args = argv[1:]
    diagnostic = False
    if "--diagnostic" in args:
        diagnostic = True
        args.remove("--diagnostic")
    ensure(len(args) <= 1, "usage: lint_theorem_dossier.py [THM-M-0387] [--diagnostic]")
    theorem_arg = args[0] if args else THEOREM_ID
    theorem_dir = (repo_root / theorem_arg).resolve()
    ensure(theorem_dir.is_dir() and theorem_dir.parent == repo_root,
           f"{theorem_arg!r} must name a direct theorem directory under the repository root")
    ensure(theorem_dir.name == THEOREM_ID, f"this historical lint instance is scoped to {THEOREM_ID}")

    meta = load_json(theorem_dir / "meta.json")
    manifest = load_json(theorem_dir / "proof_units.json")
    assert_folder_contract(repo_root, theorem_dir, meta, allow_extra=diagnostic)
    assert_top_level(manifest)
    nodes = manifest["nodes"]
    assert_tree(manifest)
    assert_metrics(manifest, nodes)
    assert_public_surfaces(manifest, nodes, repo_root)
    assert_pins(manifest, repo_root)
    assert_local_and_pinned_source_scans(repo_root)
    probe_count = assert_lean_evidence(nodes, repo_root)
    assert_public_status_consistency(meta, manifest, repo_root, probe_count)
    print(
        f"lint_theorem_dossier: ok ({THEOREM_ID}, schema {SCHEMA_VERSION}, "
        f"{len(nodes)} nodes, {probe_count} exact-type/axiom probes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
