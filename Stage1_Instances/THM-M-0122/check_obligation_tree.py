#!/usr/bin/env python3
"""Fail-closed semantic validator for the THM-M-0122 obligation freeze."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0122-OBLIGATION_TREE"
THEOREM = "THM-M-0122"
ROOT_ID = "M0122-ROOT"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
STATEMENT_SHA256 = "824c2d9410bbf3117fa6340e4259f9a3a7df6ff892c4b7cc6dad94a03ab437e8"
ANCHOR_SHA256 = "3da3f5c769e138a1c623eea5395483982e068a1d23c7f06fd69842f13524ac16"
ROOT_EXPRESSION = "f3e5f585b30ab9543bc47551d0d91c695523bace26fdb5484869add319ef7dac"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust",
    "documentation", "workflow",
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity",
}
ROLE_PATHS = {
    "obligation_registry": f"Stage1_Instances/{THEOREM}/obligation-registry.json",
    "typed_graph_bundle": f"Stage1_Instances/{THEOREM}/typed-graphs.json",
    "readable_tree": f"Stage1_Instances/{THEOREM}/obligation-tree.md",
    "composition_source": f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
    "phase_receipt": f"Stage1_Instances/{THEOREM}/obligation-tree-receipt.json",
}

BUILDER_SPEC = importlib.util.spec_from_file_location(
    "thm_m_0122_obligation_builder", HERE / "build_obligation_artifacts.py"
)
if BUILDER_SPEC is None or BUILDER_SPEC.loader is None:
    raise RuntimeError("cannot load target-owned obligation builder")
build_obligation_artifacts = importlib.util.module_from_spec(BUILDER_SPEC)
BUILDER_SPEC.loader.exec_module(build_obligation_artifacts)


class ValidationFailure(Exception):
    """A target-scoped semantic validation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def load(relative: str) -> dict:
    path = ROOT / relative

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {relative}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"{relative} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def canonical_receipt_payload(receipt: dict) -> dict:
    payload = json.loads(json.dumps(receipt))
    binding = next(
        item for item in payload["selected_artifact_bindings"]
        if item["role"] == "phase_receipt"
    )
    binding["sha256"] = None
    binding["git_blob"] = None
    return payload


def canonical_receipt_bindings(receipt: dict) -> tuple[str, str]:
    data = (json.dumps(
        canonical_receipt_payload(receipt), indent=2, ensure_ascii=True
    ) + "\n").encode("utf-8")
    sha = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
    return sha, blob


def output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def check_acyclic(edges: list[dict], ignored_types: set[str] | None = None) -> None:
    ignored = ignored_types or set()
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        if item["type"] not in ignored:
            adjacency.setdefault(item["from"], []).append(item["to"])
    active: set[str] = set()
    complete: set[str] = set()

    def visit(identifier: str) -> None:
        require(identifier not in active, f"typed graph cycle at {identifier}")
        if identifier in complete:
            return
        active.add(identifier)
        for child in adjacency.get(identifier, []):
            visit(child)
        active.remove(identifier)
        complete.add(identifier)

    for identifier in adjacency:
        visit(identifier)


def run_lean() -> str:
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0122-obligation-") as directory:
        temp = Path(directory)
        (temp / "Statement.lean").write_bytes((HERE / "Statement.lean").read_bytes())
        (temp / "ObligationTree.lean").write_bytes((HERE / "ObligationTree.lean").read_bytes())
        env = {**os.environ, "LEAN_PATH": lean_path, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"}
        statement = subprocess.run(
            [lean, "--trust=0", "-o", str(temp / "Statement.olean"), "Statement.lean"],
            cwd=temp, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        require(statement.returncode == 0, "Statement.lean failed narrow --trust=0 elaboration")
        obligation = subprocess.run(
            [lean, "--trust=0", "ObligationTree.lean"], cwd=temp,
            env={**env, "LEAN_PATH": f"{temp}:{lean_path}"}, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        require(obligation.returncode == 0, "ObligationTree.lean failed narrow --trust=0 elaboration")
    text = obligation.stdout
    require(text.count("Declarations are sorry-free!") == 1, "Lean no-sorry assertion did not pass")
    require("sorryAx" not in text and "declaration uses 'sorry'" not in text, "Lean output reports a placeholder")
    for declaration in (
        "finite_of_injective_and_finite_range",
        "terminal_of_normalization_abelJacobi_mordellLang",
        "root_of_exactTerminal",
    ):
        require(declaration in text, f"Lean output omitted {declaration}")
    normalized = re.sub(r"\s+", " ", text)
    require(normalized.count("[propext, Classical.choice, Quot.sound]") == 3, "conditional axiom profile drift")
    return text


def lean_stdout_sha256() -> str:
    """Return the deterministic digest bound by the receipt.

    The actual replay still runs below.  The digest is computed from the same
    normalized no-sorry/axiom evidence emitted by the pinned compiler, avoiding
    incidental temporary-directory paths in diagnostic output.
    """
    text = run_lean()
    normalized = re.sub(r"/tmp/thm-m-0122-obligation-[^/\s]+", "/tmp/THM-M-0122", text)
    return hashlib.sha256(normalized.encode()).hexdigest()


def validate() -> tuple[int, str]:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    registry = load(ROLE_PATHS["obligation_registry"])
    bundle = load(ROLE_PATHS["typed_graph_bundle"])
    recipes = load(f"Stage1_Instances/{THEOREM}/validation-specs.json")
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load(f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json")
    statement = load(f"Stage1_Instances/{THEOREM}/statement.json")
    anchor = load(f"Stage1_Instances/{THEOREM}/anchor-audit.json")

    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository base revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository base tree drift")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    require(target["execution_rank"] == 41, "original execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True, "target baseline drift")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False, "target lifecycle drift")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    require(node["v2_execution_rank"] == 275 and node["topological_layer"] == 0, "v2 claim order drift")
    require(node["phase_states"]["obligation_tree"] == "[ ]", "authoritative phase is no longer claimable")
    require(node["phase_attempts"]["obligation_tree"] == 0, "authoritative phase attempt count drift")
    require(node["direct_hard_parents"] == node["transitive_hard_ancestors"] == [], "hard parent closure changed")
    require(node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == [], "reuse context changed")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "dependency context digest drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256, "theorem DAG digest drift")

    phase = next(row for row in contract["phases"] if row["phase"] == "obligation_tree")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256, "phase contract digest drift")
    require(phase["intent"] == "audit" and phase["layer"] == 3, "phase contract identity drift")
    selected = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            candidate.format(theorem_id=THEOREM) for candidate in role["path_candidates"]
            if (ROOT / candidate.format(theorem_id=THEOREM)).is_file()
        ]
        if role["requirement"] == "required" or role["role"] == "composition_source":
            require(len(candidates) == 1, f"role {role['role']} is missing or ambiguous")
            selected[role["role"]] = candidates[0]
    require(selected == ROLE_PATHS, "HEAD phase artifact roles resolve differently")
    require([
        row["path_pattern"].format(theorem_id=THEOREM)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ] == [f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"], "validator selection is missing or ambiguous")

    require(registry["schema_version"] == "stage1-obligation-registry/1.0", "registry schema mismatch")
    require(bundle["schema_version"] == "stage1-typed-graphs/1.0", "typed graph schema mismatch")
    require(recipes["schema_version"] == "stage1-validation-specs/1.0", "validation specification schema mismatch")
    require(registry["item_id"] == bundle["item_id"] == recipes["item_id"] == ITEM, "artifact item identity mismatch")
    require(registry["theorem_id"] == bundle["theorem_id"] == recipes["theorem_id"] == THEOREM, "artifact theorem identity mismatch")
    require(registry["registry_version"] == 1 and registry["append_only_delta"] == [], "registry version or delta mismatch")
    require(registry["freeze_status_independent"] is True, "registry was not frozen status-independently")
    require(registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean") == STATEMENT_SHA256, "statement binding drift")
    require(registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256, "anchor binding drift")
    require(statement["canonical_formal_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION, "root expression drift")
    require(anchor["canonical_target"]["expression_sha256"] == ROOT_EXPRESSION, "anchor/root expression mismatch")

    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    require(len(ids) == len(set(ids)) == 23, "registry identity count mismatch")
    require(ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID, "root identity mismatch")
    for row in rows:
        require(set(row) == set(build_obligation_artifacts.REGISTRY_FIELDS), f"registry fields mismatch for {row['obligation_id']}")
        excluded = any(row[field] != "required" for field in ("machine_eligibility", "human_source_eligibility", "readable_eligibility"))
        require((row["exclusion_reason"] is not None) == excluded, f"eligibility exclusion mismatch for {row['obligation_id']}")
    projection = [{field: row[field] for field in build_obligation_artifacts.REGISTRY_FIELDS} for row in rows]
    denominator = build_obligation_artifacts.digest(projection)
    require(denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"], "registry denominator mismatch")
    require(registry["frozen_denominators"]["inventory"] == ids, "frozen inventory order mismatch")
    for field, key in (
        ("machine_eligibility", "required_machine"),
        ("human_source_eligibility", "required_human_source"),
        ("readable_eligibility", "required_readable"),
    ):
        require(registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == "required"], f"{key} denominator mismatch")
    layers = registry["layer_applicability"]
    require(set(layers) == {
        "S_statement_foundation", "N_normalization", "B_mathematical_branch",
        "C_construction", "L_core_lemma", "X_external_computation", "T_terminal",
    }, "mandatory layer analysis mismatch")
    require(layers["B_mathematical_branch"]["state"] == "not_applicable_pending_independent_approval" and layers["B_mathematical_branch"]["reason"], "branch-layer review boundary missing")
    require(registry["computation_exclusion"]["status"] == "not_applicable_pending_independent_approval" and registry["computation_exclusion"]["reason"], "computation exclusion review boundary missing")
    require(registry["deduplication"]["accepted_terminal_body_ids"] == [], "registry assigns unaccepted terminal body credit")

    expected_registry, expected_bundle, expected_recipes = build_obligation_artifacts.build()
    require((HERE / "obligation-registry.json").read_text(encoding="utf-8") == build_obligation_artifacts.render(expected_registry), "generated registry is stale")
    require((HERE / "typed-graphs.json").read_text(encoding="utf-8") == build_obligation_artifacts.render(expected_bundle), "generated graph bundle is stale")
    require((HERE / "validation-specs.json").read_text(encoding="utf-8") == build_obligation_artifacts.render(expected_recipes), "generated validation specs are stale")

    nodes = bundle["nodes"]
    require(len(nodes) == len(ids) and {item["obligation_id"] for item in nodes} == set(ids), "typed node coverage mismatch")
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
    step_ids: set[str] = set()
    for item in nodes:
        require(set(item) == NODE_FIELDS, f"node fields mismatch for {item['obligation_id']}")
        require(0 < item["step_budget"] <= 100, f"invalid step budget for {item['obligation_id']}")
        steps = item["semantic_step_ledger"]["steps"]
        require(0 < len(steps) <= item["step_budget"], f"semantic ledger exceeds budget for {item['obligation_id']}")
        for step in steps:
            require(set(step) == {"step_id", "premise_ids", "inference_or_source", "exact_output", "outgoing_use_ids"}, f"step fields mismatch for {item['obligation_id']}")
            require(step["step_id"] not in step_ids and step["premise_ids"] and step["inference_or_source"] and step["exact_output"] and step["outgoing_use_ids"], f"non-substantive or duplicate step for {item['obligation_id']}")
            step_ids.add(step["step_id"])
        path, anchor_id = item["public_readable_target"].split("#", 1)
        require(path == f"Stage1_Instances/{THEOREM}/obligation-tree.md", "readable path escapes target owner")
        require(f"### {anchor_id}" in readable, f"missing readable anchor {anchor_id}")
        require(item["task_ids"] == [ITEM], f"node task ownership drift for {item['obligation_id']}")

    require(set(bundle["graphs"]) == GRAPH_NAMES, "typed graph family set mismatch")
    obligation_ids = set(ids)
    workflow_ids = set(bundle["workflow_task_nodes"])
    all_edge_ids: set[str] = set()
    for name, graph in bundle["graphs"].items():
        endpoints = workflow_ids if name == "workflow" else obligation_ids
        require(set(graph) == {"edges", "out", "in"}, f"graph shape mismatch: {name}")
        require(set(graph["out"]) == set(graph["in"]) == endpoints, f"graph endpoint index mismatch: {name}")
        for item in graph["edges"]:
            require(item["edge_id"] not in all_edge_ids, f"duplicate edge id {item['edge_id']}")
            require(item["type"] in ALLOWED_EDGES and item["from"] in endpoints and item["to"] in endpoints, f"invalid typed edge {item['edge_id']}")
            require(item["edge_id"] in graph["out"][item["from"]] and item["edge_id"] in graph["in"][item["to"]], f"non-reciprocal graph index {item['edge_id']}")
            all_edge_ids.add(item["edge_id"])
        # Reverse proof edges are reciprocal indexes, not a second dependency
        # direction.  Acyclicity concerns the proof_requires dependency DAG.
        check_acyclic(
            graph["edges"],
            {"composes", "logical_decomposition"} if name == "proof" else set(),
        )

    proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for item in proof.values():
        require("reciprocal_edge_id" in item, f"proof edge lacks reciprocal id: {item['edge_id']}")
        reverse = proof[item["reciprocal_edge_id"]]
        require(reverse["reciprocal_edge_id"] == item["edge_id"], f"reciprocal backlink mismatch: {item['edge_id']}")
        require((reverse["from"], reverse["to"]) == (item["to"], item["from"]), f"reciprocal endpoints mismatch: {item['edge_id']}")
        require("proof_requires" in {item["type"], reverse["type"]}, f"proof reciprocal types mismatch: {item['edge_id']}")
        if item["type"] == "proof_requires":
            children.setdefault(item["from"], []).append(item["to"])
    require(children == {key: list(value) for key, value in build_obligation_artifacts.PROOF_CHILDREN.items()}, "proof architecture child order drift")
    require("M0122-T-TERMINAL" not in {
        parent for parent, child_ids in children.items()
        if any(child not in build_obligation_artifacts.CHECKED_PARENTS.get(parent, {}).get("lean_child_ids", []) for child in child_ids)
    }, "checked terminal has an unused direct proof child")

    refinement_children: dict[str, list[str]] = {}
    for item in bundle["graphs"]["refinement"]["edges"]:
        if item["type"] in {"logical_decomposition", "transports"}:
            refinement_children.setdefault(item["from"], []).append(item["to"])
    expected_refinements = {
        parent: [child for _kind, child in values]
        for parent, values in build_obligation_artifacts.REFINEMENT_CHILDREN.items()
    }
    require(refinement_children == expected_refinements, "refinement architecture drift")
    reachable: set[str] = set()

    def reach(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.add(identifier)
        for child in children.get(identifier, []):
            reach(child)
        for child in refinement_children.get(identifier, []):
            reach(child)

    reach(ROOT_ID)
    support_ids = {"M0122-S-FOUNDATION", "M0122-X-SOURCE", "M0122-X-PROVENANCE", "M0122-X-TRUST", "M0122-X-READABLE", "M0122-X-WORKFLOW"}
    require(obligation_ids - support_ids <= reachable, f"root-relevant architecture orphaned: {sorted((obligation_ids - support_ids) - reachable)}")
    source_edges = bundle["graphs"]["provenance"]["edges"]
    for row in rows:
        if row["obligation_id"] != "M0122-X-SOURCE" and row["human_source_eligibility"] == "required":
            require(any(item["from"] == row["obligation_id"] and item["type"] == "source_map" and item["to"] == "M0122-X-SOURCE" for item in source_edges), f"missing source edge for {row['obligation_id']}")

    certificates = {item["parent_obligation_id"]: item for item in bundle["composition_certificates"]}
    require(set(certificates) == set(build_obligation_artifacts.CHECKED_PARENTS), "checked composition certificate set mismatch")
    for parent, item in certificates.items():
        require(item["required_child_ids"] == children[parent], f"certificate child list mismatch for {parent}")
        require(item["yields_exact_parent"] is True and item["no_undeclared_inputs"] is True, f"composition boundary mismatch for {parent}")
        require(item["status"] == "provisionally_elaborated_not_accepted" and item["accepted"] is False, f"composition overclaims acceptance for {parent}")
    require(certificates[ROOT_ID]["consumes_all_required_children"] is True, "root certificate does not consume its child")
    require(certificates["M0122-T-TERMINAL"]["consumes_all_required_children"] is True, "terminal certificate does not consume every direct package child")
    plans = {item["parent_obligation_id"]: item for item in bundle["unverified_decomposition_plans"]}
    require(set(plans) == set(children) - set(certificates), "unverified decomposition coverage mismatch")
    for parent, item in plans.items():
        require(item["planned_child_ids"] == children[parent] and item["status"] == "architecture_decomposition_pending_exact_child_to_parent_certificate", f"decomposition plan drift for {parent}")

    closure = bundle["closure_boundary"]
    require(closure["accepted_closed_obligations"] == [], "graph assigns accepted closure")
    require(closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False, "graph overclaims terminal state")
    require(registry["status_observed_after_freeze"]["accepted_closed_obligations"] == [], "registry assigns accepted closure")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1", "reuse ledger schema mismatch")
    require(ledger["consumer_theorem_id"] == THEOREM, "reuse ledger consumer mismatch")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256 and ledger["dependency_context_sha256"] == CONTEXT_SHA256, "reuse ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "reuse ledger revision mismatch")
    for field in ("direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids", "shared_group_ids", "parent_inspection_order", "inspections", "reuse_decisions", "unresolved_compatibility_obligations"):
        require(ledger[field] == [], f"empty declared reuse context is not empty at {field}")
    require(ledger["closure_audit"]["status"] == "complete_for_declared_empty_context", "empty context was not audited")

    lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|implemented_by|extern|native_decide|proof_wanted)\b|^\s*(?:axiom|constant|unsafe|opaque)\b", re.MULTILINE)
    require(forbidden.search(without_comments(lean_source)) is None, "prohibited Lean construct in ObligationTree.lean")
    for marker in (
        "def FiniteExtensionNormalization", "def AbelJacobiPackage",
        "def MordellLangFinitenessPackage", "theorem finite_of_injective_and_finite_range",
        "theorem terminal_of_normalization_abelJacobi_mordellLang",
        "theorem root_of_exactTerminal", "assert_no_sorry",
    ):
        require(marker in lean_source, f"Lean architecture marker missing: {marker}")
    lean_hash = lean_stdout_sha256()

    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION, "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE, "mathlib tree drift")
    require(output("git", "status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == "", "mathlib worktree is dirty")

    required_receipt_fields = {pointer.split("/")[1] for pointer in phase["phase_receipt_required_fields"] if pointer.count("/") == 1}
    require(required_receipt_fields <= set(receipt), f"phase receipt missing required fields: {sorted(required_receipt_fields - set(receipt))}")
    require(receipt["schema_version"] == "stage1-node-receipt/1.0", "phase receipt schema mismatch")
    require(receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM, "phase receipt identity mismatch")
    require(receipt["phase"] == "obligation_tree" and receipt["intent"] == "audit", "phase receipt phase/intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE, "phase receipt base mismatch")
    require(receipt["support_state"] == "provisional_worker_selftest_pending_master_acceptance", "phase receipt support state mismatch")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False, "worker receipt claims master acceptance")
    require(receipt["verdict"] == "accepted" and receipt["selftest_status"] == "passed", "worker phase predicate is not self-tested")
    require(receipt["selftest_result"]["exit_code"] == 0 and receipt["selftest_result"]["commands"], "receipt self-test command record is incomplete")
    require(receipt["registry_denominator_sha256"] == denominator and receipt["canonical_obligation_ids"] == ids, "receipt registry binding mismatch")
    require(receipt["composition_certificates"] == bundle["composition_certificates"], "receipt composition binding mismatch")
    require(receipt["lean_output_sha256"] == lean_hash, "receipt Lean output digest mismatch")
    require(receipt["audit_complete"] is receipt["theorem_complete"] is False, "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["retry_condition"] and receipt["status_boundary"] and receipt["invalidation_inputs"], "receipt lacks fail-closed boundaries")
    require(receipt["first_failed_gate"] is None, "self-tested phase predicate reports a failed phase gate")
    require(receipt["inputs"]["theorem_dag_sha256"] == GRAPH_SHA256 and receipt["inputs"]["dependency_context_sha256"] == CONTEXT_SHA256, "receipt dependency input mismatch")
    bindings = {item["role"]: item for item in receipt["selected_artifact_bindings"]}
    require(set(bindings) == set(ROLE_PATHS), "receipt artifact role binding mismatch")
    for role, relative in ROLE_PATHS.items():
        binding = bindings[role]
        require(binding["path"] == relative, f"receipt role path mismatch for {role}")
        required_binding_fields = {"role", "path", "sha256", "git_blob"}
        if role == "phase_receipt":
            require(set(binding) == required_binding_fields | {"binding_mode"}, "receipt self-binding fields mismatch")
            expected_sha, expected_blob = canonical_receipt_bindings(receipt)
            require(binding["binding_mode"] == "canonical_self_binding_v1", "receipt self-binding mode mismatch")
            require(binding["sha256"] == expected_sha and binding["git_blob"] == expected_blob, "canonical receipt self-binding drift")
        else:
            require(set(binding) == required_binding_fields, f"artifact binding fields mismatch for {role}")
            require(binding["sha256"] == sha256(ROOT / relative), f"receipt role SHA drift for {role}")
            require(binding["git_blob"] == git_blob(ROOT / relative), f"receipt role blob drift for {role}")
    validator = receipt["validator_binding"]
    validator_path = ROOT / validator["path"]
    require(validator["path"] == f"Stage1_Instances/{THEOREM}/check_obligation_tree.py", "validator binding path mismatch")
    require(validator["sha256"] == sha256(validator_path) and validator["git_blob"] == git_blob(validator_path), "validator byte binding mismatch")
    require(validator["stdout_schema"] == "stage1-validator-semantic-result/1.0", "validator stdout schema binding mismatch")

    packet = load(".stage1-worker-selftest.json")
    require(set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}, "worker packet schema mismatch")
    require(packet["item_id"] == ITEM and packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION, "worker packet identity mismatch")
    require(packet["commands"] == receipt["selftest_result"]["commands"], "worker packet command mismatch")
    require(packet["known_failures"] == receipt["known_failures"], "worker packet failure boundary mismatch")
    require(packet["changed_paths"] == receipt["changed_paths"], "worker packet changed paths mismatch")
    status = output("git", "status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json"))
    actual_changed = {line[3:] if line[:2] == "??" else line[2:].lstrip() for line in status.splitlines()}
    require(actual_changed == set(packet["changed_paths"]), f"owned changed path mismatch: {sorted(actual_changed ^ set(packet['changed_paths']))}")

    for relative in packet["changed_paths"]:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, f"text normalization failure: {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {relative}")
    selected_text = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in ROLE_PATHS.values())
    require("/home/" not in selected_text and ".cron/" not in selected_text, "selected public artifact leaks an automation path")
    return len(ids), lean_hash


def semantic_result(*, passed: bool, message: str, open_obligations: int) -> dict:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "obligation_tree",
        "status": "passed" if passed else "failed",
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": None if passed else "OBLIGATION-TREE-SEMANTIC-CHECK",
        "open_obligations": open_obligations,
        "stale_inputs": [],
        "blocked": False,
        "message": message,
    }


def main() -> int:
    try:
        count, lean_hash = validate()
    except Exception as exc:  # Exactly one typed semantic result, including failures.
        print(json.dumps(semantic_result(
            passed=False,
            message=str(exc),
            open_obligations=23,
        ), sort_keys=True, separators=(",", ":")))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            f"T01-T04 proven for the status-independent {count}-obligation denominator, "
            "seven typed graph families, substantive bounded ledgers, empty dependency context, "
            f"and conditional Lean composition (output sha256 {lean_hash}); no proof closure inferred."
        ),
        # This counts unfinished *architecture gates*, not the mathematical
        # proof debt recorded inside the accepted phase artifact.  T01-T04
        # are all discharged by this validator.
        open_obligations=0,
    ), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
