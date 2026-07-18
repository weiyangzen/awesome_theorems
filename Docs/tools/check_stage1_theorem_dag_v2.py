#!/usr/bin/env python3
"""Validate the Stage1 v2 theorem DAG against immutable inputs and blueprint state."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import heapq
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
TARGETS = ROOT / "Docs" / "Stage1_Target_Membership_v2.json"
BLUEPRINT = ROOT / "Docs" / "Stage1_Blueprint_v2.md"
PHASE_DAG = ROOT / "Docs" / "Stage1_Phase_DAG_v2.json"
DAG = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
GENERATOR = ROOT / "Docs" / "tools" / "generate_stage1_theorem_dag_v2.py"
PHASES = ("intake", "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release")
VALID_STATES = {"[ ]", "[_]", "[x]"}
BUCKET_ORDER = {
    "master_complete": 0,
    "fully_self_tested": 1,
    "partial": 2,
    "unstarted": 3,
}
EXECUTION_CONTRACT = {
    "claim_order": ["v2_execution_rank", "phase_layer", "phase_item_id"],
    "proof_parent_inspection": {
        "scope": ["direct_hard_parents", "transitive_hard_ancestors"],
        "order": "ascending_v2_execution_rank_parent_before_child",
        "complete_closure_required": True,
    },
    "accepted_reuse_relationships": ["exact", "checked_transport"],
    "checked_transport_requires": [
        "content_bound_provider_source",
        "provider_and_consumer_statement_fingerprints",
        "consumer_owned_import_or_wrapper",
        "consumer_kernel_replay",
    ],
    "provider_checkbox_state_is_observation_only": True,
    "provider_acceptance_inherited": False,
    "consumer_acceptance_required": True,
}
AUDIT_STATUSES = {
    "audited_hard_dependency_found",
    "audited_reuse_only",
    "unknown_not_independent_proof_claim",
}
FOCUS_POLICY = {
    "requirements_source": "Docs/Stage1_Blueprint_v2.md",
    "receipt_schema": "stage1-focus-eligibility/1.0",
    "receipt_path_pattern": "Stage1_Instances/<THEOREM-ID>/focus-eligibility.json",
    "schema_contract": "Docs/Stage1_Focus_Eligibility_Schema.json",
    "validator": "scripts/stage1_focus_eligibility.py",
    "default_disposition": "research_required",
    "unknown_or_invalid_fails_closed": True,
    "frontier_exception_minimum_probability": 0.70,
    "worker_self_assessment_authorizes_exception": False,
}
HARD_TYPES = {"proof_dependency", "artifact_dependency"}
LEAN_MODULE_ID = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*")
LEAN_DECLARATION_ID = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)+")
PINNED_GLOBAL_DECLARATION_ID = re.compile(
    r"mathlib:[0-9a-f]{7,64}:[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)+"
)
LEAN_RESERVED_SEGMENTS = {
    "and", "as", "axiom", "by", "class", "constant", "def", "deriving",
    "do", "else", "end", "example", "export", "extends", "for", "from",
    "fun", "if", "import", "in", "include", "inductive", "infix", "instance",
    "let", "macro", "match", "namespace", "opaque", "open", "private", "protected",
    "section", "structure", "syntax", "theorem", "then", "universe", "variable", "where",
    "with",
}

sys.path.insert(0, str(ROOT / "scripts"))
import stage1_focus_eligibility as focus_eligibility  # noqa: E402


def fail(message: str) -> NoReturn:
    raise SystemExit(f"check_stage1_theorem_dag_v2: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must contain an object")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        fail(f"cannot hash {path.relative_to(ROOT)}: {exc}")
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def safe_repo_path(value: Any, context: str) -> Path:
    require(isinstance(value, str) and value, f"{context} path must be nonempty")
    pure = PurePosixPath(value)
    require(not pure.is_absolute() and ".." not in pure.parts, f"{context} path is not repo-relative: {value}")
    path = ROOT / pure
    require(path.is_file(), f"{context} evidence is missing: {value}")
    return path


def bucket(states: list[str]) -> str:
    if all(state == "[x]" for state in states):
        return "master_complete"
    if all(state == "[_]" for state in states):
        return "fully_self_tested"
    if all(state == "[ ]" for state in states):
        return "unstarted"
    return "partial"


def load_generator() -> Any:
    spec = importlib.util.spec_from_file_location("stage1_theorem_dag_v2_generator", GENERATOR)
    require(spec is not None and spec.loader is not None, "cannot import v2 DAG generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_blueprint_state(data: dict[str, Any], target_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    """Validate both JSON projections against the blueprint's sole cursor."""
    generator = load_generator()
    items = generator.blueprint_state_items()
    phase_dag = load_json(PHASE_DAG)
    require(phase_dag.get("requirements_source") == "Docs/Stage1_Blueprint_v2.md", "derived execution DAG source is stale")
    projected = phase_dag.get("items")
    require(isinstance(projected, list) and len(projected) == 10822, "derived execution DAG must contain exactly 10822 phase items")
    projected_state = [
        {"id": item.get("id"), "theorem_id": item.get("theorem_id"), "phase": item.get("phase"),
         "state": item.get("state"), "attempts": item.get("attempts", 0)}
        for item in projected
    ]
    require(projected_state == items, "derived execution DAG state disagrees with the v2 blueprint SSOT")
    ids = [item.get("id") for item in items if isinstance(item, dict)]
    require(len(ids) == 10822 and len(set(ids)) == 10822 and all(isinstance(item_id, str) for item_id in ids), "stable item IDs must be complete and unique")
    by_target: dict[str, dict[str, Any]] = defaultdict(dict)
    for item in items:
        theorem_id, phase, state = item.get("theorem_id"), item.get("phase"), item.get("state")
        require(theorem_id in target_ids, f"phase item has unknown theorem: {item.get('id')}")
        require(phase in PHASES and state in VALID_STATES, f"phase item has invalid phase/state: {item.get('id')}")
        require(phase not in by_target[theorem_id], f"duplicate blueprint phase: {theorem_id}/{phase}")
        by_target[theorem_id][phase] = item
    require(set(by_target) == target_ids, "blueprint theorem coverage disagrees with target set")
    require(all(set(rows) == set(PHASES) for rows in by_target.values()), "each theorem must retain all seven blueprint phases")
    records = [
        {"id": item["id"], "state": item["state"], "attempts": item.get("attempts", 0)}
        for item in sorted(items, key=lambda row: row["id"])
    ]
    snapshot = data.get("blueprint_state_snapshot")
    require(isinstance(snapshot, dict), "blueprint_state_snapshot must be an object")
    require(snapshot.get("authoritative_blueprint") == "Docs/Stage1_Blueprint_v2.md", "state snapshot authority is stale")
    require(snapshot.get("authoritative_blueprint_sha256") == sha256(BLUEPRINT), "authoritative blueprint digest is stale")
    require(snapshot.get("item_count") == 10822, "blueprint state snapshot item count is stale")
    require(snapshot.get("item_state_counts") == dict(sorted(Counter(item["state"] for item in items).items())), "blueprint state counts changed")
    require(snapshot.get("item_state_attempts_sha256") == canonical_sha256(records), "one or more blueprint item states/attempts changed")
    current = {item["id"]: item["state"] for item in items}
    return by_target, current


def validate_evidence(rows: Any, context: str) -> None:
    require(isinstance(rows, list) and rows, f"{context} evidence must be nonempty")
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"{context} evidence[{index}] must be an object")
        require(set(row) == {"path", "locator", "evidence_kind", "sha256"}, f"{context} evidence[{index}] has invalid fields")
        path = safe_repo_path(row["path"], context)
        require(isinstance(row["locator"], str) and row["locator"], f"{context} locator is empty")
        require(isinstance(row["evidence_kind"], str) and row["evidence_kind"], f"{context} evidence_kind is empty")
        require(row["sha256"] == sha256(path), f"{context} evidence digest is stale: {row['path']}")


def validate_material_sources(
    rows: Any,
    *,
    owner: str,
    context: str,
) -> dict[str, dict[str, Any]]:
    """Validate an edge-local, content-bound Lean source/declaration allowlist."""
    require(isinstance(rows, list) and rows, f"{context} material sources must be nonempty")
    by_path: dict[str, dict[str, Any]] = {}
    owner_prefix = PurePosixPath("Stage1_Instances", owner)
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"{context}[{index}] must be an object")
        require(set(row) == {"path", "sha256", "declarations"}, f"{context}[{index}] has invalid fields")
        pure = PurePosixPath(row["path"])
        require(tuple(pure.parts[:2]) == tuple(owner_prefix.parts), f"{context} source escapes its theorem owner")
        path = safe_repo_path(row["path"], context)
        require(path.suffix == ".lean" and row["path"] not in by_path, f"{context} source is not a unique Lean file")
        require(row["sha256"] == sha256(path), f"{context} source digest is stale: {row['path']}")
        declarations = row["declarations"]
        require(
            isinstance(declarations, list)
            and declarations == sorted(set(declarations))
            and all(isinstance(name, str) and name for name in declarations),
            f"{context} declarations are invalid: {row['path']}",
        )
        source_text = path.read_text(encoding="utf-8", errors="replace")
        for declaration in declarations:
            tail = declaration.rsplit(".", 1)[-1]
            require(
                re.search(
                    rf"(?m)^\s*(?:private\s+)?(?:theorem|lemma|def|abbrev|structure|class)\s+{re.escape(tail)}\b",
                    source_text,
                )
                is not None,
                f"{context} declaration is absent from {row['path']}: {declaration}",
            )
        by_path[row["path"]] = row
    return by_path


def validate_material_contract(edge: dict[str, Any]) -> None:
    """Bind each hard edge to the exact admitted provider/consumer material."""
    edge_id = edge["edge_id"]
    parent = edge["parent_theorem_id"]
    child = edge["child_theorem_id"]
    contract = edge.get("material_contract")
    require(isinstance(contract, dict), f"{edge_id} lacks a material contract")
    provider = validate_material_sources(
        contract.get("provider_sources"), owner=parent, context=f"{edge_id} provider material"
    )
    consumer = validate_material_sources(
        contract.get("consumer_sources"), owner=child, context=f"{edge_id} consumer material"
    )
    if edge["edge_type"] == "proof_dependency":
        require(
            set(contract) == {"contract_kind", "provider_sources", "consumer_sources", "receipt_input_binding"}
            and contract["contract_kind"] == "cross_target_import_and_proof_receipt_input",
            f"{edge_id} has invalid proof material contract fields",
        )
        binding = contract["receipt_input_binding"]
        require(
            isinstance(binding, dict)
            and set(binding) == {"path", "sha256", "json_pointer"}
            and binding["json_pointer"].startswith("/inputs/"),
            f"{edge_id} lacks its proof-receipt input binding",
        )
        receipt_path = safe_repo_path(binding["path"], edge_id)
        require(binding["sha256"] == sha256(receipt_path), f"{edge_id} proof-receipt binding is stale")
        require(
            PurePosixPath(binding["path"]).parts[:2] == ("Stage1_Instances", child),
            f"{edge_id} proof receipt escapes the consumer",
        )
        receipt = load_json(receipt_path)
        pointer_key = binding["json_pointer"].removeprefix("/inputs/")
        inputs = receipt.get("inputs")
        bound = inputs.get(pointer_key) if isinstance(inputs, dict) else None
        require(isinstance(bound, dict), f"{edge_id} proof-receipt input pointer is stale")
        bound_hashes = {value for key, value in bound.items() if key.endswith("_sha256")}
        require(
            all(row["sha256"] in bound_hashes for row in provider.values()),
            f"{edge_id} provider material is not bound by its proof receipt input",
        )
        imported_paths = {
            row["path"]
            for row in edge["evidence"]
            if row["evidence_kind"] == "exact_cross_target_lean_import"
        }
        require(imported_paths and imported_paths == set(consumer), f"{edge_id} import material disagrees with the consumer allowlist")
        consumer_text = "\n".join(
            safe_repo_path(path, edge_id).read_text(encoding="utf-8", errors="replace")
            for path in consumer
        )
        for row in provider.values():
            for declaration in row["declarations"]:
                consumer_name = declaration.removeprefix("Stage1Instances.")
                require(
                    re.search(rf"\b{re.escape(consumer_name)}\b", consumer_text) is not None,
                    f"{edge_id} consumer does not use admitted provider declaration: {declaration}",
                )
    else:
        require(
            set(contract) == {"contract_kind", "provider_sources", "consumer_sources", "source_manifest_binding"}
            and contract["contract_kind"] == "source_manifest_and_consumer_adapter",
            f"{edge_id} has invalid artifact material contract fields",
        )
        binding = contract["source_manifest_binding"]
        required_binding_fields = {
            "path", "sha256", "source_theorem_id_pointer", "source_path_sha256_pointer",
            "source_declaration_pointer", "consumer_adapter_path", "consumer_adapter_sha256",
            "consumer_replay_path", "consumer_replay_sha256",
        }
        require(isinstance(binding, dict) and set(binding) == required_binding_fields, f"{edge_id} has invalid source-manifest binding")
        manifest_path = safe_repo_path(binding["path"], edge_id)
        adapter_path = safe_repo_path(binding["consumer_adapter_path"], edge_id)
        replay_path = safe_repo_path(binding["consumer_replay_path"], edge_id)
        require(binding["sha256"] == sha256(manifest_path), f"{edge_id} source manifest digest is stale")
        require(binding["consumer_adapter_sha256"] == sha256(adapter_path), f"{edge_id} adapter digest is stale")
        require(binding["consumer_replay_sha256"] == sha256(replay_path), f"{edge_id} replay digest is stale")
        require(
            PurePosixPath(binding["consumer_adapter_path"]).parts[:2] == ("Stage1_Instances", child)
            and PurePosixPath(binding["consumer_replay_path"]).parts[:2] == ("Stage1_Instances", child),
            f"{edge_id} adapter/replay escapes the consumer",
        )
        manifest = load_json(manifest_path)
        require(
            binding["source_theorem_id_pointer"] == "/source_theorem_id"
            and binding["source_path_sha256_pointer"] == "/source_path_sha256"
            and binding["source_declaration_pointer"] == "/source_declaration"
            and manifest.get("source_theorem_id") == parent,
            f"{edge_id} source manifest relationship is stale",
        )
        path_hashes = manifest.get("source_path_sha256")
        require(
            isinstance(path_hashes, dict)
            and all(path_hashes.get(path) == row["sha256"] for path, row in provider.items()),
            f"{edge_id} provider material is not derived from source_path_sha256",
        )
        source_declaration = manifest.get("source_declaration")
        require(
            isinstance(source_declaration, str)
            and any(source_declaration in row["declarations"] for row in provider.values()),
            f"{edge_id} source declaration is outside the provider allowlist",
        )
        adapter_text = adapter_path.read_text(encoding="utf-8", errors="replace")
        replay_text = replay_path.read_text(encoding="utf-8", errors="replace")
        require(f"import {manifest.get('source_module')}" in adapter_text, f"{edge_id} adapter does not admit the source module")
        require("BrouwerSource.lean" in replay_text and "Proof.lean" in replay_text, f"{edge_id} replay does not consume adapter and proof")
        require(
            any(
                re.search(
                    rf"\b{re.escape(source_declaration)}\b",
                    safe_repo_path(path, edge_id).read_text(encoding="utf-8", errors="replace"),
                )
                is not None
                for path in consumer
            ),
            f"{edge_id} consumer allowlist does not use the admitted declaration",
        )


def validate_edges(data: dict[str, Any], target_ids: set[str]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    edges = data.get("hard_edges")
    require(isinstance(edges, list), "hard_edges must be an array")
    edge_ids = [edge.get("edge_id") for edge in edges if isinstance(edge, dict)]
    require(len(edge_ids) == len(edges) and len(edge_ids) == len(set(edge_ids)), "hard edge IDs must be unique")
    parents = {theorem_id: [] for theorem_id in target_ids}
    children = {theorem_id: [] for theorem_id in target_ids}
    for edge in edges:
        require(isinstance(edge, dict), "hard edge must be an object")
        require(set(edge) == {"edge_id", "edge_type", "parent_theorem_id", "child_theorem_id", "blocking", "evidence_strength", "evidence", "material_contract", "state_semantics"}, f"invalid hard edge fields: {edge.get('edge_id')}")
        parent, child = edge["parent_theorem_id"], edge["child_theorem_id"]
        require(parent in target_ids and child in target_ids and parent != child, f"invalid hard edge endpoints: {edge['edge_id']}")
        require(edge["edge_type"] in HARD_TYPES and edge["blocking"] is True, f"invalid hard edge type/blocking: {edge['edge_id']}")
        require(isinstance(edge["evidence_strength"], str) and edge["evidence_strength"].startswith(("A_", "B_")), f"hard edge lacks A/B evidence: {edge['edge_id']}")
        require(isinstance(edge["state_semantics"], str) and "never" in edge["state_semantics"], f"hard edge must reject state inheritance: {edge['edge_id']}")
        validate_evidence(edge["evidence"], edge["edge_id"])
        validate_material_contract(edge)
        parents[child].append(parent)
        children[parent].append(child)
    pairs = {(edge["parent_theorem_id"], edge["child_theorem_id"], edge["edge_type"]) for edge in edges}
    require(pairs == {("THM-M-0989", "THM-M-0990", "proof_dependency"), ("THM-M-0318", "THM-M-0320", "artifact_dependency")}, "audited hard edge set is incomplete or overclaims dependencies")
    return ({key: sorted(value) for key, value in parents.items()}, {key: sorted(value) for key, value in children.items()})


def validate_reuse(data: dict[str, Any], target_ids: set[str]) -> dict[str, list[str]]:
    hints = data.get("reuse_hints")
    require(isinstance(hints, list), "reuse_hints must be an array")
    ids = [hint.get("hint_id") for hint in hints if isinstance(hint, dict)]
    require(len(ids) == len(hints) and len(ids) == len(set(ids)), "reuse hint IDs must be unique")
    by_consumer: dict[str, list[str]] = defaultdict(list)
    for hint in hints:
        require(isinstance(hint, dict), "reuse hint must be an object")
        require(set(hint) == {"hint_id", "hint_type", "provider_theorem_id", "consumer_theorem_id", "blocking", "confidence", "evidence", "reuse_boundary"}, f"invalid reuse hint fields: {hint.get('hint_id')}")
        provider, consumer = hint["provider_theorem_id"], hint["consumer_theorem_id"]
        require(provider in target_ids and consumer in target_ids and provider != consumer, f"invalid reuse endpoints: {hint['hint_id']}")
        require(hint["blocking"] is False, f"reuse hint must be nonblocking: {hint['hint_id']}")
        require(hint["confidence"] in {"medium", "checked_candidate", "hint"}, f"invalid reuse confidence: {hint['hint_id']}")
        require(isinstance(hint["reuse_boundary"], str) and hint["reuse_boundary"], f"reuse boundary is empty: {hint['hint_id']}")
        validate_evidence(hint["evidence"], hint["hint_id"])
        by_consumer[consumer].append(hint["hint_id"])
    expected = {
        ("THM-M-0318", "THM-M-0319"),
        ("THM-M-1057", "THM-M-1056"),
        ("THM-M-1057", "THM-M-1419"),
        ("THM-M-0990", "THM-M-1063"),
        ("THM-M-1013", "THM-M-1063"),
    }
    require({(hint["provider_theorem_id"], hint["consumer_theorem_id"]) for hint in hints} == expected, "audited reuse hint set is incomplete or stale")
    return {key: sorted(value) for key, value in by_consumer.items()}


def validate_shared_groups(data: dict[str, Any], target_ids: set[str]) -> dict[str, list[str]]:
    groups = data.get("shared_lemma_groups")
    require(isinstance(groups, list), "shared_lemma_groups must be an array")
    ids = [group.get("group_id") for group in groups if isinstance(group, dict)]
    require(len(ids) == len(groups) and len(ids) == len(set(ids)), "shared group IDs must be unique")
    by_theorem: dict[str, list[str]] = defaultdict(list)
    identities: set[tuple[str, str]] = set()
    for group in groups:
        require(isinstance(group, dict), "shared group must be an object")
        require(set(group) == {"group_id", "group_type", "identity_kind", "canonical_identity", "member_theorem_ids", "evidence_paths", "confidence", "blocking", "reuse_boundary"}, f"invalid shared group fields: {group.get('group_id')}")
        require(group["identity_kind"] in {"lean_module", "terminal_proof_body"}, f"invalid shared identity kind: {group['group_id']}")
        require(isinstance(group["canonical_identity"], str) and group["canonical_identity"], f"empty shared identity: {group['group_id']}")
        identity_value = group["canonical_identity"]
        if group["identity_kind"] == "lean_module":
            require(group["group_type"] == "shared_module_cluster", f"module group is not typed as a weak shared_module_cluster: {group['group_id']}")
            require(group["group_id"].startswith("SHARED-MODULE-"), f"module group ID is not explicit: {group['group_id']}")
            require(LEAN_MODULE_ID.fullmatch(identity_value) is not None, f"invalid/prose/path Lean module identity: {identity_value!r}")
            require(all(segment not in LEAN_RESERVED_SEGMENTS for segment in identity_value.split(".")), f"Lean module identity contains a reserved word: {identity_value!r}")
            require("not a common lemma or proof body" in group["reuse_boundary"], f"module cluster overclaims lemma reuse: {group['group_id']}")
        else:
            require(group["group_type"] == "shared_terminal_body", f"terminal group has invalid type: {group['group_id']}")
            require(group["group_id"].startswith("SHARED-TERMINAL-"), f"terminal group ID is not explicit: {group['group_id']}")
            lowered = identity_value.lower()
            is_local_or_path = (
                lowered.startswith(("local:", "repo-local:", "repo_local:", "path:", "file:"))
                or identity_value.startswith(("Stage1_Instances.", "Stage1Instances.THM_", "AwesomeTheorems.Stage1.S1_M_"))
                or "/" in identity_value
                or "\\" in identity_value
                or lowered.endswith((".lean", ".json", ".yaml", ".yml", ".md"))
            )
            require(not is_local_or_path and "::" not in identity_value, f"local/path terminal identity escaped theorem namespacing: {identity_value!r}")
            require(
                LEAN_DECLARATION_ID.fullmatch(identity_value) is not None
                or PINNED_GLOBAL_DECLARATION_ID.fullmatch(identity_value) is not None,
                f"terminal identity is not a true global canonical body: {identity_value!r}",
            )
        identity = (group["identity_kind"], group["canonical_identity"])
        require(identity not in identities, f"duplicate shared identity: {identity}")
        identities.add(identity)
        members = group["member_theorem_ids"]
        require(isinstance(members, list) and len(members) >= 2 and members == sorted(set(members)), f"shared group members invalid: {group['group_id']}")
        require(set(members) <= target_ids, f"shared group has unknown member: {group['group_id']}")
        require(group["confidence"] == "hint" and group["blocking"] is False, f"shared group must remain a nonblocking hint: {group['group_id']}")
        paths = group["evidence_paths"]
        require(isinstance(paths, list) and paths == sorted(set(paths)) and paths, f"shared group evidence paths invalid: {group['group_id']}")
        for path in paths:
            safe_repo_path(path, group["group_id"])
        for theorem_id in members:
            by_theorem[theorem_id].append(group["group_id"])
    return {key: sorted(value) for key, value in by_theorem.items()}


def validate_topology(
    rows: list[dict[str, Any]], parents: dict[str, list[str]], children: dict[str, list[str]], buckets: dict[str, str], original_ranks: dict[str, int]
) -> tuple[list[str], dict[str, int], dict[str, list[str]]]:
    indegree = {theorem_id: len(parents[theorem_id]) for theorem_id in parents}
    layers = {theorem_id: 0 for theorem_id in parents}
    ready: list[tuple[int, int, int, str]] = []
    for theorem_id, degree in indegree.items():
        if degree == 0:
            heapq.heappush(ready, (BUCKET_ORDER[buckets[theorem_id]], 0, original_ranks[theorem_id], theorem_id))
    order = []
    while ready:
        _, _, _, theorem_id = heapq.heappop(ready)
        order.append(theorem_id)
        for child in children[theorem_id]:
            layers[child] = max(layers[child], layers[theorem_id] + 1)
            indegree[child] -= 1
            if indegree[child] == 0:
                heapq.heappush(ready, (BUCKET_ORDER[buckets[child]], layers[child], original_ranks[child], child))
    require(len(order) == len(parents), "hard theorem graph contains a cycle")
    order_index = {theorem_id: index for index, theorem_id in enumerate(order)}
    ancestors: dict[str, list[str]] = {}
    for theorem_id in order:
        closure = set(parents[theorem_id])
        for parent in parents[theorem_id]:
            closure.update(ancestors[parent])
        ancestors[theorem_id] = sorted(closure, key=order_index.__getitem__)
        require(
            all(order_index[ancestor] < order_index[theorem_id] for ancestor in ancestors[theorem_id]),
            f"hard ancestor is not ordered before its consumer: {theorem_id}",
        )
    require([row["theorem_id"] for row in rows] == order, "theorem array is not in deterministic v2 execution order")
    return order, layers, ancestors


def main() -> None:
    targets_data = load_json(TARGETS)
    data = load_json(DAG)
    require(data.get("schema_version") == "stage1-theorem-dag/2.1", "unsupported theorem DAG schema")
    require(data.get("generated_by") == "Docs/tools/generate_stage1_theorem_dag_v2.py", "generated_by is stale")
    require(data.get("requirements_source") == "Docs/Stage1_Blueprint_v2.md", "requirements_source must be the v2 blueprint")
    require(data.get("target_manifest") == "Docs/Stage1_Target_Membership_v2.json", "target_manifest is stale")
    require(data.get("execution_dag_projection") == "Docs/Stage1_Phase_DAG_v2.json", "derived execution DAG path is stale")
    require(data.get("state_protocol") == {"not_done": "[ ]", "worker_self_tested": "[_]", "master_accepted": "[x]"}, "state protocol changed")
    require(data.get("completion_bucket_order") == list(BUCKET_ORDER), "completion bucket order changed")
    require(data.get("execution_contract") == EXECUTION_CONTRACT, "execution contract is incomplete or stale")
    require(data.get("focus_policy") == FOCUS_POLICY, "focus policy is incomplete or stale")
    policy = data.get("edge_policy")
    require(isinstance(policy, dict) and set(policy) == {"hard_edge_admission", "reuse_hint_admission", "unknown_policy", "hard_dependency_worker_policy", "reuse_hint_worker_policy"}, "edge_policy is incomplete")
    require("unknown_not_independent_proof_claim" in policy["unknown_policy"], "unknown dependencies must not be called independent")

    targets = targets_data.get("targets")
    require(isinstance(targets, list) and len(targets) == 1546, "target manifest must contain 1546 targets")
    target_ids = {target.get("theorem_id") for target in targets if isinstance(target, dict)}
    require(len(target_ids) == 1546 and None not in target_ids, "target theorem IDs must be unique")
    expected_id_hash = targets_data.get("scope", {}).get("canonical_sorted_target_id_set_sha256")
    require(data.get("target_id_set_sha256") == expected_id_hash, "target ID-set digest changed")
    by_target, _ = validate_blueprint_state(data, target_ids)

    rows = data.get("theorems")
    require(isinstance(rows, list) and len(rows) == 1546, "theorems must contain exactly 1546 nodes")
    ids = [row.get("theorem_id") for row in rows if isinstance(row, dict)]
    require(len(ids) == 1546 and len(set(ids)) == 1546 and set(ids) == target_ids, "theorem DAG does not exactly cover the target set")
    expected_fields = {
        "theorem_id", "name", "category", "original_execution_rank", "v2_execution_rank",
        "completion_bucket", "phase_states", "phase_attempts", "state_counts", "topological_layer",
        "direct_hard_parents", "direct_hard_children", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids", "dependency_context_sha256", "dependency_audit_status",
        "focus_eligibility", "evidence_inventory", "reusable_artifacts",
    }
    target_by_id = {target["theorem_id"]: target for target in targets}
    original_ranks = {theorem_id: target_by_id[theorem_id]["execution_rank"] for theorem_id in target_ids}
    require(sorted(original_ranks.values()) == list(range(1, 1547)), "original target ranks are not contiguous")
    buckets: dict[str, str] = {}
    for row in rows:
        theorem_id = row["theorem_id"]
        require(set(row) == expected_fields, f"invalid theorem fields: {theorem_id}")
        require(row["name"] == target_by_id[theorem_id]["name"] and row["category"] == target_by_id[theorem_id]["category"], f"target metadata changed: {theorem_id}")
        require(row["original_execution_rank"] == original_ranks[theorem_id], f"original rank changed: {theorem_id}")
        expected_states = {phase: by_target[theorem_id][phase]["state"] for phase in PHASES}
        expected_attempts = {phase: by_target[theorem_id][phase].get("attempts", 0) for phase in PHASES}
        require(row["phase_states"] == expected_states, f"blueprint phase state changed in v2 projection: {theorem_id}")
        require(row["phase_attempts"] == expected_attempts, f"blueprint phase attempts changed in v2 projection: {theorem_id}")
        require(row["state_counts"] == dict(sorted(Counter(expected_states.values()).items())), f"state counts stale: {theorem_id}")
        expected_bucket = bucket(list(expected_states.values()))
        require(row["completion_bucket"] == expected_bucket, f"completion bucket stale: {theorem_id}")
        buckets[theorem_id] = expected_bucket
        require(row["dependency_audit_status"] in AUDIT_STATUSES, f"invalid dependency audit status: {theorem_id}")
        focus = row["focus_eligibility"]
        require(
            focus == focus_eligibility.evaluate_target(ROOT, theorem_id),
            f"focus eligibility projection is stale: {theorem_id}",
        )
        inv = row["evidence_inventory"]
        require(isinstance(inv, dict) and set(inv) == {"instance_directory", "instance_directory_exists", "lean_sources", "receipt_files", "structured_json_files"}, f"invalid evidence inventory: {theorem_id}")
        require(all(isinstance(inv[field], list) and inv[field] == sorted(set(inv[field])) for field in ("lean_sources", "receipt_files", "structured_json_files")), f"inventory paths invalid: {theorem_id}")
        for path in inv["lean_sources"] + inv["receipt_files"] + inv["structured_json_files"]:
            safe_repo_path(path, theorem_id)
        reusable_paths: set[str] = set()
        require(isinstance(row["reusable_artifacts"], list), f"reusable_artifacts must be a list: {theorem_id}")
        for artifact in row["reusable_artifacts"]:
            require(isinstance(artifact, dict) and set(artifact) == {"path", "artifact_kind", "sha256"}, f"invalid reusable artifact: {theorem_id}")
            require(artifact["path"] not in reusable_paths, f"duplicate reusable artifact: {theorem_id}/{artifact['path']}")
            reusable_paths.add(artifact["path"])
            require(artifact["artifact_kind"] in {"lean_source", "evidence_receipt", "dependency_source_manifest"}, f"invalid artifact kind: {theorem_id}")
            require(artifact["sha256"] == sha256(safe_repo_path(artifact["path"], theorem_id)), f"reusable artifact digest stale: {artifact['path']}")

    parents, children = validate_edges(data, target_ids)
    hints_by_consumer = validate_reuse(data, target_ids)
    groups_by_theorem = validate_shared_groups(data, target_ids)
    hard_by_child: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in data["hard_edges"]:
        hard_by_child[edge["child_theorem_id"]].append(edge)
    hint_by_id = {hint["hint_id"]: hint for hint in data["reuse_hints"]}
    group_by_id = {group["group_id"]: group for group in data["shared_lemma_groups"]}
    order, layers, ancestors = validate_topology(rows, parents, children, buckets, original_ranks)
    ranks = [row["v2_execution_rank"] for row in rows]
    require(ranks == list(range(1, 1547)), "v2 execution ranks are not contiguous or disagree with array order")
    row_by_id = {row["theorem_id"]: row for row in rows}
    for theorem_id in order:
        row = row_by_id[theorem_id]
        require(row["topological_layer"] == layers[theorem_id], f"topological layer stale: {theorem_id}")
        require(row["direct_hard_parents"] == parents[theorem_id], f"direct hard parents stale: {theorem_id}")
        require(row["direct_hard_children"] == children[theorem_id], f"direct hard children stale: {theorem_id}")
        require(row["transitive_hard_ancestors"] == ancestors[theorem_id], f"ancestor closure stale: {theorem_id}")
        require(row["direct_reuse_hint_ids"] == hints_by_consumer.get(theorem_id, []), f"reuse hint references stale: {theorem_id}")
        require(row["shared_lemma_group_ids"] == groups_by_theorem.get(theorem_id, []), f"shared group references stale: {theorem_id}")
        context_nodes = set(ancestors[theorem_id]) | {theorem_id}
        dependency_context = {
            "direct_hard_parents": parents[theorem_id],
            "transitive_hard_ancestors": ancestors[theorem_id],
            "hard_edges": sorted(
                (
                    edge
                    for child in context_nodes
                    for edge in hard_by_child[child]
                    if edge["parent_theorem_id"] in context_nodes
                ),
                key=lambda edge: edge["edge_id"],
            ),
            "direct_reuse_hints": [
                hint_by_id[hint_id] for hint_id in hints_by_consumer.get(theorem_id, [])
            ],
            "shared_groups": [
                group_by_id[group_id] for group_id in groups_by_theorem.get(theorem_id, [])
            ],
        }
        require(
            row["dependency_context_sha256"] == canonical_sha256(dependency_context),
            f"dependency context digest stale: {theorem_id}",
        )
        expected_audit = (
            "audited_hard_dependency_found"
            if parents[theorem_id]
            else "audited_reuse_only"
            if hints_by_consumer.get(theorem_id) or groups_by_theorem.get(theorem_id)
            else "unknown_not_independent_proof_claim"
        )
        require(row["dependency_audit_status"] == expected_audit, f"dependency audit status stale: {theorem_id}")
        require(
            all(row_by_id[ancestor]["v2_execution_rank"] < row["v2_execution_rank"] for ancestor in ancestors[theorem_id]),
            f"hard ancestor is not ranked before child: {theorem_id}",
        )

    summary = data.get("graph_summary")
    require(isinstance(summary, dict), "graph_summary must be an object")
    expected_summary = {
        "theorem_count": 1546,
        "hard_edge_count": len(data["hard_edges"]),
        "reuse_hint_count": len(data["reuse_hints"]),
        "shared_lemma_group_count": len(data["shared_lemma_groups"]),
        "shared_group_type_counts": dict(sorted(Counter(group["group_type"] for group in data["shared_lemma_groups"]).items())),
        "root_count": sum(not parents[theorem_id] for theorem_id in target_ids),
        "max_topological_layer": max(layers.values(), default=0),
        "completion_bucket_counts": {name: Counter(buckets.values())[name] for name in BUCKET_ORDER},
        "dependency_audit_status_counts": dict(sorted(Counter(row["dependency_audit_status"] for row in rows).items())),
    }
    require(summary == expected_summary, "graph_summary is stale")

    focus_rows = [row["focus_eligibility"] for row in rows]
    expected_focus_summary = {
        "receipt_present_count": sum(row["present"] for row in focus_rows),
        "receipt_valid_count": sum(row["valid"] for row in focus_rows),
        "machine_evidence_class_counts": dict(
            sorted(Counter(row["machine_evidence_class"] for row in focus_rows).items())
        ),
        "execution_disposition_counts": dict(
            sorted(Counter(row["execution_disposition"] for row in focus_rows).items())
        ),
        "phase_eligible_counts": {
            phase: sum(row["phase_permissions"][phase] for row in focus_rows)
            for phase in PHASES
        },
    }
    require(
        data.get("focus_eligibility_summary") == expected_focus_summary,
        "focus_eligibility_summary is stale",
    )

    # Strong reproducibility check: the checked-in artifact must equal a fresh
    # in-memory build, covering evidence discovery, inventories, hashes, ranks,
    # ancestor closure, and every one of the 10822 blueprint phase states.
    expected = load_generator().build()
    require(data == expected, "checked-in theorem DAG differs from a fresh deterministic generation")
    # A dependency-reuse ledger is a graph consumer, never a discovery input;
    # otherwise writing the required proof ledger would change its own context.
    require(
        "if path.name == \"dependency-reuse-ledger.json\"" in GENERATOR.read_text(encoding="utf-8"),
        "generator must exclude dependency reuse ledgers from graph discovery",
    )
    generator_source = GENERATOR.read_text(encoding="utf-8")
    require(
        "TRANSIENT_INSTANCE_DIR_PREFIXES" in generator_source
        and "durable_instance_file" in generator_source,
        "generator must exclude transient validator scratch trees from graph discovery",
    )
    print(
        "check_stage1_theorem_dag_v2: ok "
        f"(1546 theorems, 10822 blueprint states, {len(data['hard_edges'])} hard edges, "
        f"{len(data['reuse_hints'])} reuse hints, {len(data['shared_lemma_groups'])} shared groups, acyclic)"
    )


if __name__ == "__main__":
    main()
