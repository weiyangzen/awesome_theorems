#!/usr/bin/env python3
"""Deterministically build the Stage5.1 organization release candidate.

This builder never activates a controller or supplies concurrency.  Its two
program Blueprints start entirely blank and remain activation-blocked until a
separate accepted fence and complete operator concurrency prompt exist.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import heapq
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import urllib.request
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
COMMON_PATH = Path(__file__).with_name("stage5_1_common.py")
_SPEC = importlib.util.spec_from_file_location("stage5_1_common_for_builder", COMMON_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("cannot load stage5_1_common.py")
C = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = C
_SPEC.loader.exec_module(C)

RELEASE = "1.0"
RELEASE_ROOT = "Docs/catalog/stage5_1_organization/releases/1.0"
ORG_ROOT = "Docs/catalog/stage5_1_organization"
MSC_PATH = f"{ORG_ROOT}/sources/MSC_2020.csv"
MSC_URL = "https://msc2020.org/MSC_2020.csv"
MSC_SHA256 = "f7c889354c202551fe01f89bad2ae95ccadec4c57ac1f6f9de38bbd658d3c78c"
MSC_LICENSE = "CC BY-NC-SA 4.0"
CHECKLIST_BEGIN = "<!-- STAGE5-1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE5-1-EXECUTION-CHECKLIST:END -->"
OLD_BEGIN = "<!-- STAGE5-PROOF-DEBT-EXECUTION-CHECKLIST:BEGIN -->"
OLD_END = "<!-- STAGE5-PROOF-DEBT-EXECUTION-CHECKLIST:END -->"
SUBJECT_NODES_PATH = f"{RELEASE_ROOT}/Subject_Nodes.jsonl"
SUBJECT_ID_REGISTRY_PATH = f"{RELEASE_ROOT}/Subject_Node_ID_Registry.jsonl"
CLASSIFIER_PATH = "Docs/tools/classify_stage5_1_subjects.py"
POOL_SOURCE_TAR = "Docs/catalog/v5/sources/conjecturebench-357bcb1a-full-source.tar.gz"
CHECKER_PATH = "Docs/tools/check_stage5_1_organization_release.py"

INPUT_PATHS = {
    "catalog_current_release": "Docs/catalog/v5/Current_Release.json",
    "catalog_release_manifest": "Docs/catalog/v5/releases/5.6/Release_Manifest.json",
    "theorem_projection": "Docs/catalog/v5/releases/5.6/Theorem_List.json",
    "claim_catalog": "Docs/catalog/v5/releases/5.6/Claim_Catalog.json",
    "stage5_claim_registry": "Docs/catalog/v5/releases/5.6/Stage5_Claim_ID_Registry.json",
    "strict_conjecture_ledger": "Docs/catalog/v5/releases/5.6/Strict_Conjecture_Ledger.json",
    "pool_current_release": "Docs/catalog/v5/pools/Current_Pool_Release.json",
    "pool_manifest": "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json",
    "pool_occurrences": "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Source_Occurrence_Pool.jsonl",
    "pool_identity_registry": "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Identity_Registry.jsonl",
    "theorem_blueprint": "Docs/Stage5_Theorems_Blueprint.md",
    "theorem_gantt": "Docs/Stage5_Theorems_Gantt.md",
    "theorem_workset": "Docs/evidence/stage5_theorems/workset-5.6.json",
    "conjecture_blueprint": "Docs/Stage5_Conjectures_Blueprint.md",
    "conjecture_gantt": "Docs/Stage5_Conjectures_Gantt.md",
    "conjecture_workset": "Docs/evidence/stage5_conjectures/workset-5.6.json",
}

SCHEMA = {
    "source": "awesome-theorems/stage5-1-organization/source-input/1.0",
    "subject": "awesome-theorems/stage5-1-organization/subject-node/1.0",
    "subject_registry": "awesome-theorems/stage5-1-organization/subject-node-id-registry/1.0",
    "taxonomy": "awesome-theorems/stage5-1-organization/taxonomy/1.0",
    "object": "awesome-theorems/stage5-1-organization/object-index/1.0",
    "id_crosswalk": "awesome-theorems/stage5-1-organization/id-crosswalk/1.0",
    "checklist_crosswalk": "awesome-theorems/stage5-1-organization/checklist-crosswalk/1.0",
    "assignment": "awesome-theorems/stage5-1-organization/subject-assignment/1.0",
    "assessment": "awesome-theorems/stage5-1-organization/dependency-assessment/1.0",
    "relation": "awesome-theorems/stage5-1-organization/relation-edge/1.0",
    "hard_dag": "awesome-theorems/stage5-1-organization/execution-hard-dag/1.0",
    "closure": "awesome-theorems/stage5-1-organization/dependency-closure/1.0",
    "workset": "awesome-theorems/stage5-1-organization/organization-workset/1.0",
    "manifest": "awesome-theorems/stage5-1-organization/manifest/1.0",
    "migration": "awesome-theorems/stage5-1-organization/migration/1.0",
    "current": "awesome-theorems/stage5-1-organization/current-release/1.0",
}


def load_json(root: Path, relative: str) -> dict[str, Any]:
    value = C.strict_json((root / relative).read_bytes(), relative)
    if not isinstance(value, dict):
        raise C.Stage51Error(f"{relative}: expected object")
    return value


def state_name(mark: str) -> str:
    return {" ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted"}[mark]


def revise_item(item_id: str) -> str:
    if item_id.startswith("S5THM-"):
        return "S51THM-" + item_id.removeprefix("S5THM-")
    if item_id.startswith("S5CON-"):
        return "S51CON-" + item_id.removeprefix("S5CON-")
    raise C.Stage51Error(f"cannot revise legacy item ID {item_id}")


def row_sha(row: Any) -> str:
    return C.sha256_bytes(
        C.canonical_json({
            "item_id": row.item_id,
            "title": row.title,
            "dependencies": list(row.dependencies),
            "owned_paths": list(row.owned_paths),
            "gate": row.gate,
        })
    )


def acquire_msc(root: Path, source: Path | None, allow_network: bool) -> bytes:
    if source is not None:
        raw = source.read_bytes()
    elif (root / MSC_PATH).is_file():
        raw = (root / MSC_PATH).read_bytes()
    elif allow_network:
        with urllib.request.urlopen(MSC_URL, timeout=60) as response:
            raw = response.read()
    else:
        raise C.Stage51Error(f"pinned MSC source missing at {MSC_PATH}; --check never downloads")
    if C.sha256_bytes(raw) != MSC_SHA256:
        raise C.Stage51Error("MSC_2020.csv SHA-256 differs from pinned authority")
    return raw


def seal_taxonomy(nodes: list[dict[str, Any]], sentinels: dict[str, str]) -> dict[str, Any]:
    nodes_raw = C.canonical_jsonl(nodes)
    return C.seal_object({
        "schema_version": SCHEMA["taxonomy"], "organization_release": RELEASE,
        "root_subject_id": "S51-SUB-00000000", "sentinel_subject_ids": sentinels,
        "node_count": len(nodes), "node_id_set_sha256": C.set_digest(node["subject_id"] for node in nodes),
        "nodes_path": SUBJECT_NODES_PATH, "nodes_sha256": C.sha256_bytes(nodes_raw),
        "tree_policy": {
            "primary_parent_projection": "single_rooted_acyclic_tree",
            "broader_subject_projection": "acyclic_multi_parent_dag",
            "sentinels_for_unknown": True, "sentinels_forbidden_as_secondary": True,
            "subject_coordinates_do_not_define_identity": True,
        },
    })


def build_taxonomy(msc_raw: bytes) -> tuple[list[dict[str, Any]], dict[str, str], dict[str, Any]]:
    rows = list(csv.DictReader(io.StringIO(msc_raw.decode("iso-8859-1"), newline=""), delimiter="\t"))
    if len(rows) != 6603 or set(rows[0]) != {"code", "text", "description"}:
        raise C.Stage51Error("MSC source row/header count differs")
    root_id = "S51-SUB-00000000"
    sentinels = {
        "unclassified": "S51-SUB-UNCLASSIFIED",
        "ambiguous": "S51-SUB-AMBIGUOUS",
        "out_of_scope": "S51-SUB-OUT-OF-SCOPE",
        "review_pending": "S51-SUB-REVIEW-PENDING",
    }
    source_ref = {"path": MSC_PATH, "sha256": MSC_SHA256, "source_label": "MSC2020 official classification"}
    nodes: list[dict[str, Any]] = [C.seal_record({
        "schema_version": SCHEMA["subject"], "subject_id": root_id, "subject_key": "mathematics",
        "scheme": "internal", "edition": None, "notation": None, "rank": "root",
        "parent_subject_id": None, "broader_subject_ids": [], "label": {"en": "Mathematics", "zh": "数学"},
        "status": "active", "evidence_tier": "independent_review", "source_refs": [],
        "selectable_as_primary": False, "selectable_as_secondary": False,
    })]
    code_to_id: dict[str, str] = {}
    for ordinal, row in enumerate(rows, start=1):
        code_to_id[row["code"]] = f"S51-SUB-{ordinal:08d}"
    for row in rows:
        code = row["code"]
        if code.endswith("-XX"):
            parent, rank = root_id, "branch"
        elif code[2] == "-":
            parent, rank = code_to_id[code[:2] + "-XX"], "leaf"
        elif code.endswith("xx"):
            parent, rank = code_to_id[code[:2] + "-XX"], "branch"
        else:
            parent, rank = code_to_id[code[:3] + "xx"], "leaf"
        nodes.append(C.seal_record({
            "schema_version": SCHEMA["subject"], "subject_id": code_to_id[code],
            "subject_key": "msc2020." + code.lower(), "scheme": "MSC", "edition": "2020",
            "notation": code, "rank": rank, "parent_subject_id": parent,
            "broader_subject_ids": [parent], "label": {"en": row["text"], "zh": row["text"]},
            "status": "active", "evidence_tier": "source_exact", "source_refs": [source_ref],
            "selectable_as_primary": True, "selectable_as_secondary": True,
        }))
    for key, subject_id in sentinels.items():
        nodes.append(C.seal_record({
            "schema_version": SCHEMA["subject"], "subject_id": subject_id,
            "subject_key": "sentinel." + key.replace("_", "-"), "scheme": "internal", "edition": None,
            "notation": key.upper(), "rank": "sentinel", "parent_subject_id": root_id,
            "broader_subject_ids": [root_id], "label": {"en": key.replace("_", " ").title(), "zh": key},
            "status": "active", "evidence_tier": "none", "source_refs": [],
            "selectable_as_primary": True, "selectable_as_secondary": False,
        }))
    nodes.sort(key=lambda node: node["subject_id"])
    taxonomy = seal_taxonomy(nodes, sentinels)
    return nodes, code_to_id, taxonomy


def member_identity(kind: str, member: dict[str, Any]) -> tuple[str, str, str, str, str | None, str | None, str | None]:
    if kind == "theorem":
        legacy = member["target_item_id"]; digits = legacy.split("-")[1]
        return f"S51-THM-{digits}", f"S51THM-{digits}-TARGET", legacy, member["stage_claim_id"], member.get("variant_id"), None, member.get("display_name") or member["stage_claim_id"]
    if member["member_kind"] == "strict_resolution":
        legacy = member["target_item_id"]; digits = legacy.split("-")[1]
        return f"S51-CON-{digits}", f"S51CON-{digits}-TARGET", legacy, member["stage_claim_id"], member.get("variant_id"), None, member.get("display_name") or member["stage_claim_id"]
    legacy = member["target_item_id"]; pool = member["pool_id"]; digits = pool.removeprefix("S5POOL-")
    return f"S51-OCC-{digits}", f"S51CON-POOL-{digits}-INTAKE", legacy, None, None, pool, member.get("source_native_id") or pool


def _load_classifier() -> Any:
    path = ROOT / CLASSIFIER_PATH
    spec = importlib.util.spec_from_file_location("stage5_1_classifier_for_release", path)
    if spec is None or spec.loader is None:
        raise C.Stage51Error(f"cannot load {CLASSIFIER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _adapt_classifier(
    root: Path,
    msc_raw: bytes,
    base_nodes: list[dict[str, Any]],
    code_to_id: dict[str, str],
    sentinels: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Run the pinned classifier and adapt its rich signals to release IDs.

    The classifier preserves full-source field/class/tag signals and every
    source-exact AMS/MSC membership.  This adapter deliberately leaves all of
    them candidate/pending: only a later independent Master review may accept
    an assignment or derive an accepted cross-domain projection.
    """

    classifier = _load_classifier()
    classifier_nodes = classifier.parse_msc_csv(msc_raw, MSC_SHA256)
    taxonomy_builder = classifier.TaxonomyBuilder(classifier_nodes)
    theorem_doc = load_json(root, INPUT_PATHS["theorem_projection"])
    claim_doc = load_json(root, INPUT_PATHS["claim_catalog"])
    strict_doc = load_json(root, INPUT_PATHS["strict_conjecture_ledger"])
    pool_rows = [
        C.strict_json(line, "pool occurrence")
        for line in (root / INPUT_PATHS["pool_occurrences"]).read_bytes().splitlines()
    ]
    raw_by_pool = classifier._pool_raw_records(pool_rows, root / POOL_SOURCE_TAR)
    claim_by_id = {row["stage_claim_id"]: row for row in claim_doc["records"]}
    classifier_assignments = (
        classifier.classify_theorem_records(theorem_doc["records"], taxonomy_builder)
        + classifier.classify_strict_conjectures(strict_doc["strict_credits"], claim_by_id, taxonomy_builder)
        + classifier.classify_pool_occurrences(pool_rows, raw_by_pool, taxonomy_builder)
    )

    normalized_codes = {
        classifier.normalize_msc_code(code): subject_id
        for code, subject_id in code_to_id.items()
        if classifier.normalize_msc_code(code) is not None
    }
    id_map: dict[str, str] = {
        classifier.ROOT_NODE_ID: "S51-SUB-00000000",
        classifier.SENTINEL_ROOT_ID: "S51-SUB-00000000",
        classifier.SENTINELS["UNCLASSIFIED"]: sentinels["unclassified"],
        classifier.SENTINELS["AMBIGUOUS"]: sentinels["ambiguous"],
        classifier.SENTINELS["OTHER"]: sentinels["out_of_scope"],
        classifier.SENTINELS["OUT_OF_SCOPE"]: sentinels["out_of_scope"],
    }
    for classifier_id, node in taxonomy_builder.nodes.items():
        if node.get("scheme") == "MSC":
            normalized = classifier.normalize_msc_code(node.get("notation"))
            if normalized in normalized_codes:
                id_map[classifier_id] = normalized_codes[normalized]
    source_classifier_ids = sorted(
        classifier_id for classifier_id in taxonomy_builder.nodes
        if classifier_id not in id_map
    )
    next_ordinal = len(code_to_id) + 1
    for offset, classifier_id in enumerate(source_classifier_ids):
        id_map[classifier_id] = f"S51-SUB-{next_ordinal + offset:08d}"

    classifier_raw = (root / CLASSIFIER_PATH).read_bytes()
    pool_tar_raw = (root / POOL_SOURCE_TAR).read_bytes()
    claim_raw = (root / INPUT_PATHS["claim_catalog"]).read_bytes()
    children: dict[str, int] = {}
    for node in taxonomy_builder.nodes.values():
        parent = node.get("parent_node_id")
        if isinstance(parent, str):
            children[parent] = children.get(parent, 0) + 1
    nodes = list(base_nodes)
    for classifier_id in source_classifier_ids:
        node = taxonomy_builder.nodes[classifier_id]
        parent_classifier_id = node.get("parent_node_id")
        parent = id_map.get(parent_classifier_id, "S51-SUB-00000000")
        scheme_value = str(node.get("scheme") or "source_native")
        source_path = POOL_SOURCE_TAR if "CONJECTUREBENCH" in scheme_value or "SOURCE_" in scheme_value else INPUT_PATHS["claim_catalog"]
        source_sha = C.sha256_bytes(pool_tar_raw if source_path == POOL_SOURCE_TAR else claim_raw)
        label = str(node.get("label") or node.get("notation") or classifier_id)
        structural = classifier_id == classifier.NATIVE_ROOT_ID
        nodes.append(C.seal_record({
            "schema_version": SCHEMA["subject"], "subject_id": id_map[classifier_id],
            "subject_key": "source-native." + C.sha256_bytes(classifier_id.encode("utf-8"))[:24],
            "scheme": "arXiv" if scheme_value.upper() == "ARXIV" else "source_native",
            "edition": str(node.get("edition") or "source-pinned"),
            "notation": str(node.get("notation") or classifier_id),
            "rank": "branch" if children.get(classifier_id) else "leaf",
            "parent_subject_id": parent, "broader_subject_ids": [parent],
            "label": {"en": label, "zh": label}, "status": "active",
            "evidence_tier": "machine_crosswalk" if structural else "source_category",
            "source_refs": [{"path": source_path, "sha256": source_sha, "source_label": scheme_value}],
            "selectable_as_primary": not structural, "selectable_as_secondary": not structural,
        }))
    nodes.sort(key=lambda row: row["subject_id"])

    node_by_id = {row["subject_id"]: row for row in nodes}
    signals: dict[str, dict[str, Any]] = {}
    for assignment in classifier_assignments:
        object_id = assignment["member_id"]
        exact_rows: list[tuple[int, int, str, str]] = []
        for membership in assignment.get("accepted_memberships", []):
            mapped = id_map.get(membership.get("subject_id"))
            if mapped and mapped not in sentinels.values():
                exact_rows.append((
                    0 if membership.get("source_primary_claim") else 1,
                    int(membership.get("priority", 999)),
                    str(membership.get("evidence_path") or ""), mapped,
                ))
        exact_ids: list[str] = []
        for _, _, _, mapped in sorted(exact_rows):
            if mapped not in exact_ids:
                exact_ids.append(mapped)
        candidate_ids = sorted({
            id_map[candidate["subject_id"]]
            for candidate in assignment.get("candidate_subjects", [])
            if candidate.get("subject_id") in id_map
            and id_map[candidate["subject_id"]] not in sentinels.values()
            and id_map[candidate["subject_id"]] not in exact_ids
        })
        classifier_primary = id_map.get(assignment.get("primary_subject_id"))
        if exact_ids:
            primary, status, tier = exact_ids[0], "candidate", "source_exact"
            secondary = exact_ids[1:]
        elif classifier_primary == sentinels["out_of_scope"]:
            primary, status, tier, secondary = classifier_primary, "out_of_scope", "none", []
        elif classifier_primary == sentinels["ambiguous"]:
            primary, status, tier, secondary = classifier_primary, "ambiguous", "none", []
        elif candidate_ids:
            primary, status, tier, secondary = sentinels["review_pending"], "review_pending", "none", []
        else:
            primary, status, tier, secondary = sentinels["unclassified"], "unclassified", "none", []
        node = node_by_id[primary]
        notation = str(node.get("notation") or "")
        if node["rank"] == "sentinel":
            granularity = "sentinel"
        elif node.get("scheme") == "MSC" and len(notation) == 5 and not notation.endswith(("xx", "-XX")):
            granularity = "fine"
        elif node.get("scheme") == "MSC" and notation.endswith("-XX"):
            granularity = "broad"
        elif node.get("scheme") == "MSC" and notation.endswith("xx"):
            granularity = "intermediate"
        else:
            granularity = "broad"
        raw_labels = sorted({
            f"{row.get('scheme')}:{row.get('value')}"
            for row in assignment.get("raw_labels", []) if row.get("value")
        })
        selected_locators = sorted({
            locator for _, _, locator, mapped in exact_rows
            if mapped == primary and locator
        })
        if object_id.startswith("S51-OCC-"):
            evidence_path = POOL_SOURCE_TAR
        elif object_id.startswith("S51-THM-"):
            evidence_path = INPUT_PATHS["theorem_projection"]
        else:
            evidence_path = INPUT_PATHS["claim_catalog"]
        evidence_raw = (root / evidence_path).read_bytes()
        signals[object_id] = {
            "primary": primary, "secondary": secondary, "candidates": candidate_ids,
            "classification_status": status, "evidence_tier": tier,
            "granularity": granularity, "source_labels": raw_labels,
            "method_facets": sorted(set(assignment.get("review_flags", []))),
            "primary_evidence": [
                {"path": evidence_path, "sha256": C.sha256_bytes(evidence_raw),
                 "evidence_kind": "source_exact_subject_membership", "locator": locator}
                for locator in selected_locators
            ],
        }
    if len(signals) != 19790:
        raise C.Stage51Error(f"classifier coverage differs: expected 19790, got {len(signals)}")
    # Bind the exact classifier implementation that created these signals.
    if not classifier_raw:
        raise C.Stage51Error("empty classifier implementation")
    return nodes, signals


def build_bundle(
    root: Path,
    release: str,
    generated_at: str,
    msc_raw: bytes | None = None,
    predecessor_subject_registry: list[dict[str, Any]] | None = None,
) -> dict[str, bytes]:
    if release != RELEASE:
        raise C.Stage51Error("this builder version emits only organization release 1.0")
    C.validate_timestamp(generated_at)
    if msc_raw is None:
        msc_raw = acquire_msc(root, None, allow_network=False)
    bundle: dict[str, bytes] = {MSC_PATH: msc_raw}
    old_theorem = C.parse_blueprint_rows((root / INPUT_PATHS["theorem_blueprint"]).read_bytes(), OLD_BEGIN, OLD_END, "theorem predecessor")
    old_conjecture = C.parse_blueprint_rows((root / INPUT_PATHS["conjecture_blueprint"]).read_bytes(), OLD_BEGIN, OLD_END, "conjecture predecessor")
    if len(old_theorem) + len(old_conjecture) != 20197:
        raise C.Stage51Error("legacy checklist denominator differs from 20,197")
    theorem_workset = load_json(root, INPUT_PATHS["theorem_workset"])
    conjecture_workset = load_json(root, INPUT_PATHS["conjecture_workset"])
    catalog = load_json(root, INPUT_PATHS["claim_catalog"])
    catalog_by_id = {row["stage_claim_id"]: row for row in catalog["records"]}
    pool_rows = [C.strict_json(line, "pool occurrence") for line in (root / INPUT_PATHS["pool_occurrences"]).read_bytes().splitlines()]
    pool_by_id = {row["pool_id"]: row for row in pool_rows}
    base_nodes, code_to_id, taxonomy = build_taxonomy(msc_raw)
    sentinels = taxonomy["sentinel_subject_ids"]
    nodes, classification_signals = _adapt_classifier(
        root, msc_raw, base_nodes, code_to_id, sentinels,
    )
    provisional_ids = {C.subject_stable_key(node): node["subject_id"] for node in nodes}
    assigned_nodes, subject_registry = C.assign_subject_node_ids(
        nodes, predecessor_subject_registry,
    )
    id_remap = {
        provisional_ids[C.subject_stable_key(node)]: node["subject_id"]
        for node in assigned_nodes
    }
    nodes = []
    for node in assigned_nodes:
        value = dict(node)
        value.pop("record_sha256", None)
        parent = value.get("parent_subject_id")
        value["parent_subject_id"] = id_remap.get(parent, parent)
        value["broader_subject_ids"] = [
            id_remap.get(subject_id, subject_id)
            for subject_id in value.get("broader_subject_ids", [])
        ]
        nodes.append(C.seal_record(value))
    for signal in classification_signals.values():
        signal["primary"] = id_remap.get(signal["primary"], signal["primary"])
        signal["secondary"] = [id_remap.get(value, value) for value in signal["secondary"]]
        signal["candidates"] = [id_remap.get(value, value) for value in signal["candidates"]]
    sentinels = {key: id_remap.get(value, value) for key, value in sentinels.items()}
    taxonomy = seal_taxonomy(nodes, sentinels)
    bundle[SUBJECT_NODES_PATH] = C.canonical_jsonl(nodes)
    bundle[SUBJECT_ID_REGISTRY_PATH] = C.canonical_jsonl(subject_registry)
    bundle[f"{RELEASE_ROOT}/Subject_Taxonomy.json"] = C.canonical_json_pretty(taxonomy)

    objects: list[dict[str, Any]] = []
    crosswalks: list[dict[str, Any]] = []
    assignments: list[dict[str, Any]] = []
    assessments: list[dict[str, Any]] = []
    closures: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    legacy_state = {row.item_id: state_name(row.state) for row in old_theorem + old_conjecture}
    members = [("theorem", member) for member in theorem_workset["members"]] + [("conjecture", member) for member in conjecture_workset["members"]]
    for program_kind, member in members:
        object_id, item_id, legacy_item, claim_id, variant_id, pool_id, display_name = member_identity(program_kind, member)
        object_kind = "theorem" if program_kind == "theorem" else ("strict_conjecture" if claim_id else "source_occurrence")
        prefix = {"theorem": "THM", "strict_conjecture": "CON", "source_occurrence": "OCC"}[object_kind]
        digits = object_id.rsplit("-", 1)[1]
        assignment_id, assessment_id = f"S51-ASG-{prefix}-{digits}", f"S51-DEP-{prefix}-{digits}"
        source_record = catalog_by_id.get(claim_id) if claim_id else pool_by_id[pool_id]
        source_sha = member.get("record_sha256") or source_record.get("canonical_record_sha256") or source_record.get("record_sha256")
        semantic_sha = member.get("semantic_payload_sha256")
        identity_sha = C.sha256_bytes(C.canonical_json({"object_kind": object_kind, "legacy_item_id": legacy_item, "stage5_claim_id": claim_id, "variant_id": variant_id, "pool_id": pool_id, "source_record_sha256": source_sha, "semantic_payload_sha256": semantic_sha}))
        signal = classification_signals[object_id]
        subject_id = signal["primary"]
        classification_status = signal["classification_status"]
        evidence_tier = signal["evidence_tier"]
        source_labels = signal["source_labels"]
        objects.append(C.seal_record({
            "schema_version": SCHEMA["object"], "object_id": object_id, "object_kind": object_kind,
            "program": "theorems" if program_kind == "theorem" else "conjectures", "stage51_item_id": item_id,
            "legacy_item_id": legacy_item, "stage5_claim_id": claim_id, "variant_id": variant_id,
            "pool_id": pool_id, "display_name": display_name, "source_record_sha256": source_sha,
            "semantic_payload_sha256": semantic_sha, "identity_sha256": identity_sha,
            "subject_assignment_id": assignment_id, "dependency_assessment_id": assessment_id,
        }))
        crosswalks.append(C.seal_record({
            "schema_version": SCHEMA["id_crosswalk"], "object_id": object_id, "object_kind": object_kind,
            "legacy_item_id": legacy_item, "stage51_item_id": item_id, "mapping_type": "exact_member_successor",
            "identity_sha256": identity_sha, "stage5_claim_id": claim_id, "variant_id": variant_id, "pool_id": pool_id,
            "source_record_sha256": source_sha, "legacy_task_authority_sha256": member["target_task_authority_sha256"],
            "legacy_state": legacy_state[legacy_item], "stage51_initial_state": "not_done",
            "state_transfer": "evidence_only_revalidation_required",
        }))
        assignments.append(C.seal_record({
            "schema_version": SCHEMA["assignment"], "assignment_id": assignment_id, "object_id": object_id,
            "stage51_item_id": item_id,
            "primary": {"subject_id": subject_id, "granularity": signal["granularity"],
                        "assertion_state": classification_status, "evidence_tier": evidence_tier,
                        "evidence": signal["primary_evidence"]},
            "secondary_subject_ids": signal["secondary"],
            "candidate_subject_ids": signal["candidates"],
            "method_facets": signal["method_facets"], "source_labels": source_labels,
            "classification_status": classification_status,
            "cross_domain": {"value": False, "root_subject_ids": []},
            "review": {"state": "pending", "reviewer_id": None, "receipt_sha256": None},
            "legacy_binding": {"legacy_item_id": legacy_item, "identity_sha256": identity_sha, "source_record_sha256": source_sha},
        }))
        assessments.append(C.seal_record({
            "schema_version": SCHEMA["assessment"], "assessment_id": assessment_id, "object_id": object_id,
            "item_id": item_id, "evidence_scope": {"scope_kind": "source_metadata_only", "statement_bound": bool(member.get("statement_sha256") or member.get("statement_presence")), "proof_body_traversed": False, "artifact_consumption_checked": False},
            "audit_status": "unknown_not_independent_proof_claim", "outgoing_edge_ids": [], "incoming_edge_ids": [],
            "hard_prerequisite_item_ids": [], "unknown_reasons": ["no_admitted_content_bound_target_dependency_audit"], "evidence": [],
        }))
        closures.append(C.seal_record({
            "schema_version": SCHEMA["closure"], "item_id": item_id, "assessment_id": assessment_id,
            "direct_prerequisite_item_ids": [], "transitive_prerequisite_item_ids": [], "direct_edge_ids": [],
            "topological_rank": 0, "hard_dag_sha256": "0" * 64,
        }))

    objects.sort(key=lambda row: row["object_id"]); crosswalks.sort(key=lambda row: row["object_id"])
    assignments.sort(key=lambda row: row["object_id"]); assessments.sort(key=lambda row: row["object_id"])
    closures.sort(key=lambda row: row["item_id"])
    if len(objects) != 19790:
        raise C.Stage51Error("member denominator differs from 19,790")

    # Source-declared cross-record references remain nonblocking association
    # edges. They are intentionally absent from the execution hard DAG.
    object_by_pool = {row["pool_id"]: row for row in objects if row.get("pool_id")}
    pools_by_native: dict[str, list[str]] = {}
    for row in pool_rows:
        native = row.get("source_native_id")
        if isinstance(native, str):
            pools_by_native.setdefault(native, []).append(row["pool_id"])
    pool_evidence_sha = C.sha256_bytes((root / INPUT_PATHS["pool_occurrences"]).read_bytes())
    relation_by_id: dict[str, dict[str, Any]] = {}
    for source in pool_rows:
        consumer = object_by_pool[source["pool_id"]]
        for related_native in source.get("related_source_ids", []):
            matches = pools_by_native.get(related_native, [])
            if len(matches) != 1:
                continue
            provider = object_by_pool[matches[0]]
            if provider["object_id"] == consumer["object_id"]:
                continue
            identity_payload = {
                "consumer_member_id": consumer["object_id"],
                "provider_member_id": provider["object_id"],
                "consumer_identity_sha256": consumer["identity_sha256"],
                "provider_identity_sha256": provider["identity_sha256"],
                "consumer_object_record_sha256": consumer["record_sha256"],
                "provider_object_record_sha256": provider["record_sha256"],
                "relation_type": "related_source", "plane": "association",
                "direction_semantics": "consumer_requires_provider",
                "source_native_reference": related_native,
            }
            edge_id = "S51-REL-" + C.sha256_bytes(C.canonical_json(identity_payload))[:16]
            relation_by_id[edge_id] = C.seal_record({
                "schema_version": SCHEMA["relation"], "edge_id": edge_id,
                "consumer_member_id": consumer["object_id"],
                "provider_member_id": provider["object_id"],
                "consumer_identity_sha256": consumer["identity_sha256"],
                "provider_identity_sha256": provider["identity_sha256"],
                "consumer_object_record_sha256": consumer["record_sha256"],
                "provider_object_record_sha256": provider["record_sha256"],
                "relation_type": "related_source", "plane": "association",
                "provider_binding": {"binding_kind": "external_source_reference",
                                     "source_sha256": provider["source_record_sha256"]},
                "blocking": False, "scheduler_effect": "none",
                "evidence_tier": "D_source_reported", "review_state": "pending",
                "direction_semantics": "consumer_requires_provider",
                "evidence": [{"path": INPUT_PATHS["pool_occurrences"], "sha256": pool_evidence_sha,
                              "evidence_kind": "source_reported_related_source_id",
                              "locator": f"pool_id={source['pool_id']}/related_source_ids={related_native}"}],
                "credit_inheritance": False, "status_inheritance": False, "cross_domain": False,
            })
    relations = [relation_by_id[key] for key in sorted(relation_by_id)]
    object_by_item = {row["stage51_item_id"]: row for row in objects}
    item_by_object = {
        row["object_id"]: row["stage51_item_id"] for row in objects
    }
    outgoing: dict[str, list[str]] = {row["object_id"]: [] for row in objects}
    incoming: dict[str, list[str]] = {row["object_id"]: [] for row in objects}
    hard_prerequisites: dict[str, set[str]] = {
        row["object_id"]: set() for row in objects
    }
    for relation in relations:
        outgoing[relation["consumer_member_id"]].append(relation["edge_id"])
        incoming[relation["provider_member_id"]].append(relation["edge_id"])
        if relation["blocking"] is True:
            hard_prerequisites[relation["consumer_member_id"]].add(
                item_by_object[relation["provider_member_id"]]
            )
    assessments = [C.seal_record({
        **{key: value for key, value in row.items()
           if key not in {
               "record_sha256", "outgoing_edge_ids", "incoming_edge_ids",
               "hard_prerequisite_item_ids", "audit_status",
           }},
        "audit_status": (
            "audited_edges_present"
            if any(
                relation_by_id[edge_id]["review_state"] == "verified"
                for edge_id in outgoing[row["object_id"]] + incoming[row["object_id"]]
            ) else (
                "source_edges_present_pending_review"
                if outgoing[row["object_id"]] or incoming[row["object_id"]]
                else "unknown_not_independent_proof_claim"
            )
        ),
        "outgoing_edge_ids": sorted(outgoing[row["object_id"]]),
        "incoming_edge_ids": sorted(incoming[row["object_id"]]),
        "hard_prerequisite_item_ids": sorted(hard_prerequisites[row["object_id"]]),
    }) for row in assessments]

    # Project every admitted hard relation into the scheduler DAG.  The current
    # pinned source release has no such relation, but every downstream surface
    # deliberately derives from this collection rather than assuming zero.
    hard_relations = [row for row in relations if row["blocking"] is True]
    hard_edges = [{
        "edge_id": row["edge_id"],
        "provider_member_id": row["provider_member_id"],
        "consumer_member_id": row["consumer_member_id"],
        "scheduler_effect": row["scheduler_effect"],
        "relation_record_sha256": row["record_sha256"],
        "evidence_tier": row["evidence_tier"],
        "blocking": True,
    } for row in hard_relations]
    hard_edges.sort(key=lambda row: row["edge_id"])
    hard_children: dict[str, set[str]] = {
        item: set() for item in object_by_item
    }
    hard_indegree: dict[str, int] = {item: 0 for item in object_by_item}
    direct_hard_edges: dict[str, set[str]] = {
        item: set() for item in object_by_item
    }
    for relation in hard_relations:
        provider_item = item_by_object[relation["provider_member_id"]]
        consumer_item = item_by_object[relation["consumer_member_id"]]
        direct_hard_edges[consumer_item].add(relation["edge_id"])
        if consumer_item not in hard_children[provider_item]:
            hard_children[provider_item].add(consumer_item)
            hard_indegree[consumer_item] += 1
    ready = [item for item, degree in hard_indegree.items() if degree == 0]
    hard_root_count = len(ready)
    heapq.heapify(ready)
    topological_order: list[str] = []
    while ready:
        item = heapq.heappop(ready)
        topological_order.append(item)
        for child in sorted(hard_children[item]):
            hard_indegree[child] -= 1
            if hard_indegree[child] == 0:
                heapq.heappush(ready, child)
    if len(topological_order) != len(object_by_item):
        raise C.Stage51Error("admitted execution hard relations contain a cycle")
    hard = C.seal_object({
        "schema_version": SCHEMA["hard_dag"], "organization_release": RELEASE,
        "nodes": sorted(object_by_item), "edges": hard_edges,
        "topological_order": topological_order,
        "counts": {
            "node_count": len(object_by_item),
            "edge_count": len(hard_edges),
            "root_count": hard_root_count,
        },
        "edge_policy": {"admitted_review_state": "verified", "admitted_evidence_tiers": ["A2_target_owned_replay", "B_content_bound_artifact"], "direction_semantics": "consumer_requires_provider", "acyclic": True, "credit_inheritance": False, "status_inheritance": False, "unknown_means_independent": False},
    })
    hard_sha = C.sha256_bytes(C.canonical_json_pretty(hard))
    transitive_hard: dict[str, set[str]] = {item: set() for item in object_by_item}
    hard_rank: dict[str, int] = {item: 0 for item in object_by_item}
    for item in topological_order:
        for provider_item in hard_prerequisites[object_by_item[item]["object_id"]]:
            transitive_hard[item].add(provider_item)
            transitive_hard[item].update(transitive_hard[provider_item])
            hard_rank[item] = max(hard_rank[item], hard_rank[provider_item] + 1)
    assessment_by_object = {row["object_id"]: row for row in assessments}
    closures = [C.seal_record({
        "schema_version": SCHEMA["closure"],
        "item_id": item,
        "assessment_id": assessment_by_object[obj["object_id"]]["assessment_id"],
        "direct_prerequisite_item_ids": sorted(hard_prerequisites[obj["object_id"]]),
        "transitive_prerequisite_item_ids": sorted(transitive_hard[item]),
        "direct_edge_ids": sorted(direct_hard_edges[item]),
        "topological_rank": hard_rank[item],
        "hard_dag_sha256": hard_sha,
    }) for item, obj in sorted(object_by_item.items())]

    for name, rows in (("Object_Index", objects), ("Mathematical_ID_Crosswalk", crosswalks), ("Subject_Assignments", assignments), ("Dependency_Assessments", assessments), ("Relation_Edges", relations), ("Dependency_Closure", closures)):
        bundle[f"{RELEASE_ROOT}/{name}.jsonl"] = C.canonical_jsonl(rows)
    bundle[f"{RELEASE_ROOT}/Execution_Hard_DAG.json"] = C.canonical_json_pretty(hard)
    bundle[f"{RELEASE_ROOT}/Cross_Domain_Edges.jsonl"] = b""

    assignment_by_object = {row["object_id"]: row for row in assignments}
    crosswalk_by_object = {row["object_id"]: row for row in crosswalks}
    closure_by_item = {row["item_id"]: row for row in closures}
    program_worksets: dict[str, list[dict[str, Any]]] = {"theorems": [], "conjectures": []}
    for item, obj in sorted(object_by_item.items()):
        assignment = assignment_by_object[obj["object_id"]]; assessment = assessment_by_object[obj["object_id"]]
        program_worksets[obj["program"]].append(C.seal_record({
            "schema_version": SCHEMA["workset"], "program": obj["program"], "object_id": obj["object_id"],
            "object_kind": obj["object_kind"], "item_id": item, "legacy_item_id": obj["legacy_item_id"],
            "object_index_record_sha256": obj["record_sha256"], "id_crosswalk_record_sha256": crosswalk_by_object[obj["object_id"]]["record_sha256"],
            "subject_assignment_id": assignment["assignment_id"], "subject_assignment_record_sha256": assignment["record_sha256"],
            "dependency_assessment_id": assessment["assessment_id"], "dependency_assessment_record_sha256": assessment["record_sha256"],
            "dependency_closure_record_sha256": closure_by_item[item]["record_sha256"],
            "execution_dependency_item_ids": closure_by_item[item]["direct_prerequisite_item_ids"],
            "initial_state": "not_done",
        }))
    for program, rows in program_worksets.items():
        bundle[f"{RELEASE_ROOT}/programs/{program}/Organization_Workset.jsonl"] = C.canonical_jsonl(rows)

    checklist_crosswalk: list[dict[str, Any]] = []
    blueprints: dict[str, tuple[list[Any], bytes]] = {}
    for program, old_rows, old_path, new_path in (
        ("theorems", old_theorem, INPUT_PATHS["theorem_blueprint"], "Docs/Stage5_1_Theorems_Blueprint.md"),
        ("conjectures", old_conjecture, INPUT_PATHS["conjecture_blueprint"], "Docs/Stage5_1_Conjectures_Blueprint.md"),
    ):
        new_rows = []
        member_items = set(object_by_item)
        for old in old_rows:
            new_id = revise_item(old.item_id)
            new_dependencies = tuple(dict.fromkeys([
                *(revise_item(dep) for dep in old.dependencies),
                *(sorted(hard_prerequisites[object_by_item[new_id]["object_id"]])
                  if new_id in object_by_item else ()),
            ]))
            paths = old.owned_paths
            if new_id in member_items:
                obj = object_by_item[new_id]
                base = "Stage5_Theorem_Instances" if obj["object_kind"] == "theorem" else ("Stage5_Conjecture_Instances" if obj["object_kind"] == "strict_conjecture" else "Stage5_Conjecture_Pool_Intake")
                identity = obj["stage5_claim_id"] or obj["pool_id"]
                paths = paths + (f"{base}/{identity}/organization-binding.json", f"{base}/{identity}/subject-assignment.json", f"{base}/{identity}/dependency-assessment.json")
                gate = "One stable mathematical/source-occurrence member owns one isolated execution and must independently close the predecessor Stage5 proof obligations that remain applicable after the retired renumbering branch, plus its exact Stage5.1 identity crosswalk, evidence-bounded subject assignment and dependency assessment; legacy acceptance and retired aliases are evidence only, unknown edges do not mean independence, and only the canonical Master may accept the integrated result."
                relationship = "exact_member_successor"; members_intersection = [old.item_id]
            else:
                gate = "Canonical Master deterministic control operation: recompute exact predecessor membership, organization bindings, immutable receipts and descendant closure without launching a TUI worker; no control state or legacy acceptance transfers mathematical credit."
                relationship = "control_successor"; members_intersection = []
            new_rows.append(C.BlueprintRow(new_id, f"Stage5.1 successor of {old.item_id}: {old.title}", new_dependencies, paths, gate, " "))
            checklist_crosswalk.append(C.seal_record({
                "schema_version": SCHEMA["checklist_crosswalk"], "legacy_program": program,
                "legacy_item_id": old.item_id, "legacy_row_sha256": row_sha(old), "legacy_state": state_name(old.state),
                "relationship": relationship, "new_item_ids": [new_id], "member_intersection_count": len(members_intersection),
                "member_intersection_sha256": C.set_digest(members_intersection), "stage51_initial_state": "not_done",
            }))
        spec = {
            "schema_version": "awesome-theorems/stage5-1-organization/blueprint-spec/1.0", "program": program,
            "blueprint_revision": "Stage5.1", "base_catalog_release": "5.6", "not_catalog_release_5_1": True,
            "authoritative_blueprint": new_path, "same_prefix_gantt": C.expected_gantt_path(new_path),
            "organization_release_manifest": f"{RELEASE_ROOT}/Organization_Manifest.json",
            "execution_hard_dag": {"path": f"{RELEASE_ROOT}/Execution_Hard_DAG.json", "sha256": hard_sha},
            "concurrency_prompt_contract": {
                "value_source": "explicit_execution_prompt_only",
                "missing_policy": "fail_closed_before_materialization_reservation_launch_or_request",
                "defaults_forbidden": True,
                "required_dimensions": [
                    "logical_claims", "service_records",
                    "agent_executions", "startup_reservations", "launch_fanout_per_wave",
                    "live_transports", "authenticated_goals", "running_turns",
                    "outbound_request_starts_per_window", "in_flight_requests",
                    "max_outstanding_requests_per_execution", "integration", "validators",
                    "exact_path_conflicts", "desired_live_target", "hard_cap",
                ],
                "required_policy_fields": [
                    "request_window_seconds", "lifecycle_mode", "replacement_policy",
                ],
                "required_replacement_policy_fields": [
                    "replacement_limit", "startup_deadline_seconds", "tick_time_budget_seconds",
                ],
                "required_prompt_fields": [
                    "schema_version", "program", "policy_epoch", "source", "concurrency",
                    "request_window_seconds", "lifecycle_mode", "replacement_policy",
                    "route", "model", "reasoning_effort", "service_tier", "authority_sha256",
                ],
                "required_authority_fields": ["program", "policy_epoch", "source", "authority_sha256"],
                "required_route_fields": ["route", "model", "reasoning_effort", "service_tier"],
                "prompt_path": f"Docs/evidence/stage5_1_{program}/operator-concurrency-prompt.json",
            },
            "activation_contract": {
                "runtime_root": f".ops/stage5-1-{program}-execution-v1",
                "controller_path": f"scripts/stage5_1_{program}_execution_cron.py",
                "cron_marker_begin": f"# BEGIN AWESOME_THEOREMS_STAGE5_1_{program.upper()}_EXECUTION_V1",
                "cron_marker_end": f"# END AWESOME_THEOREMS_STAGE5_1_{program.upper()}_EXECUTION_V1",
                "prompt_path": f"Docs/evidence/stage5_1_{program}/operator-concurrency-prompt.json",
                "required_side_effect_absence": [
                    "runtime_root", "claims", "reservations", "task_roots", "tmux_sockets",
                    "processes", "request_leases", "turn_leases", "requests", "cron_marker",
                ],
                "predecessor_fence_receipt_path": "Docs/evidence/stage5_1_shared_execution/predecessor-fence.json",
            },
            "master_control": {
                "transport": "non_tui_controller", "worker_transport": "forbidden",
                "goal_submission": "forbidden",
            },
            "activation_status": "blocked",
            "activation_fence_receipt": "Docs/evidence/stage5_1_shared_execution/activation-fence.json",
        }
        lines = [
            f"# Stage5.1 {program.title()} Organization Execution Blueprint", "",
            f"> Current project SSOT for Stage5.1 {program} requirements and checklist state  ", f"> Blueprint revision: `Stage5.1`  ",
            "> Catalog parent release: `5.6`; this is not catalog release `5.1`  ", f"> Mandatory same-prefix Gantt: `{C.expected_gantt_path(new_path)}`  ",
            "> Initial state: all rows blank; activation blocked", "", "## Frozen execution specification", "", "```json",
            json.dumps(spec, ensure_ascii=False, sort_keys=True, indent=2), "```", "", "## Authoritative checklist", "", CHECKLIST_BEGIN,
            *[row.render() for row in new_rows], CHECKLIST_END, "",
        ]
        raw = "\n".join(lines).encode("utf-8")
        bundle[new_path] = raw
        blueprints[program] = (new_rows, raw)

    checklist_crosswalk.sort(key=lambda row: (row["legacy_program"], row["legacy_item_id"]))
    bundle[f"{RELEASE_ROOT}/Legacy_Checklist_Row_Crosswalk.jsonl"] = C.canonical_jsonl(checklist_crosswalk)
    if len(checklist_crosswalk) != 20197:
        raise C.Stage51Error("legacy checklist crosswalk denominator differs")

    for program, (rows, blueprint_raw) in blueprints.items():
        blueprint_path = "Docs/Stage5_1_Theorems_Blueprint.md" if program == "theorems" else "Docs/Stage5_1_Conjectures_Blueprint.md"
        gantt_path = C.expected_gantt_path(blueprint_path)
        taxonomy_raw = bundle[f"{RELEASE_ROOT}/Subject_Taxonomy.json"]
        assignment_raw = bundle[f"{RELEASE_ROOT}/Subject_Assignments.jsonl"]
        assessment_raw = bundle[f"{RELEASE_ROOT}/Dependency_Assessments.jsonl"]
        relation_raw = bundle[f"{RELEASE_ROOT}/Relation_Edges.jsonl"]
        node_by_id = {node["subject_id"]: node for node in nodes}
        outgoing_relations: dict[str, list[dict[str, Any]]] = {}
        incoming_relations: dict[str, list[dict[str, Any]]] = {}
        for relation in relations:
            outgoing_relations.setdefault(relation["consumer_member_id"], []).append(relation)
            incoming_relations.setdefault(relation["provider_member_id"], []).append(relation)
        program_objects = {
            row["object_id"] for row in objects if row["program"] == program
        }
        program_relations = {
            row["edge_id"]: row for row in relations
            if (row["consumer_member_id"] in program_objects or
                row["provider_member_id"] in program_objects)
        }
        program_assessments = [
            assessment_by_object[identity] for identity in sorted(program_objects)
        ]
        consumer_incident_count = sum(
            len(outgoing_relations.get(identity, ())) for identity in program_objects
        )
        provider_incident_count = sum(
            len(incoming_relations.get(identity, ())) for identity in program_objects
        )
        program_metadata_counts = {
            "assessment_status_counts": dict(sorted(Counter(
                row["audit_status"] for row in program_assessments
            ).items())),
            "relation_type_counts": dict(sorted(Counter(
                row["relation_type"] for row in program_relations.values()
            ).items())),
            "relation_plane_counts": dict(sorted(Counter(
                row["plane"] for row in program_relations.values()
            ).items())),
            "relation_review_state_counts": dict(sorted(Counter(
                row["review_state"] for row in program_relations.values()
            ).items())),
            "relation_scheduler_effect_counts": dict(sorted(Counter(
                row["scheduler_effect"] for row in program_relations.values()
            ).items())),
            "relation_incident_counts": {
                "consumer_required": consumer_incident_count,
                "provider_used_by": provider_incident_count,
                "total_endpoint_incidents": consumer_incident_count + provider_incident_count,
                "unique_relations": len(program_relations),
                "members_with_incident": sum(
                    bool(outgoing_relations.get(identity) or incoming_relations.get(identity))
                    for identity in program_objects
                ),
            },
            "cross_domain_assignment_count": sum(
                assignment_by_object[identity]["cross_domain"]["value"] is True
                for identity in program_objects
            ),
            "cross_domain_relation_count": sum(
                row["cross_domain"] is True for row in program_relations.values()
            ),
            "hard_edge_count": sum(
                row["blocking"] is True for row in program_relations.values()
            ),
        }
        gantt_lines = [
            f"# Stage5.1 {program.title()} Organization Gantt", "",
            f"> Generated read-only projection of `{blueprint_path}`; never a checklist authority.", "",
            "```mermaid", "gantt", f"    title Stage5.1 {program} recorded projection", "    dateFormat YYYY-MM-DDTHH:mm:ss",
            f"    section Projection", f"    Generated UTC :milestone, projection, {generated_at.removesuffix('Z')}, 0s", "```", "",
            "## Complete monitoring index", "",
            "| Item | Legacy/member mapping | State | Execution depends on | Owner / claim | Startup | Live | Handoff | Integration | Repair | Block | Subject code/path/label | Classification/review | Assignment SHA-256 | Assessment SHA-256 | Dependency assessment | Mathematical prerequisite consumer-required edge IDs | Mathematical prerequisite provider-used-by edge IDs | Semantic relation edge IDs | Reuse hint edge IDs | Hard edge review | Scheduler effect | Cross-domain | Timing |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for row in rows:
            obj = object_by_item.get(row.item_id)
            if obj is None:
                gantt_lines.append(
                    f"| `{row.item_id}` | control successor | not_done | `{','.join(row.dependencies) or '-'}` | unclaimed | not_started | not_live | no_handoff | no_integration | no_repair | blocked_activation | - | not_applicable | - | - | control_not_member | `[]` | `[]` | `[]` | `[]` | `[]` | `none` | `false` | unscheduled |"
                )
                continue
            assignment = assignment_by_object[obj["object_id"]]
            assessment = assessment_by_object[obj["object_id"]]
            subject_node = node_by_id[assignment["primary"]["subject_id"]]
            subject_path: list[str] = []
            cursor: str | None = subject_node["subject_id"]
            while cursor is not None:
                subject_path.append(cursor)
                cursor = node_by_id[cursor]["parent_subject_id"]
            subject_path.reverse()
            outgoing_associated = outgoing_relations.get(obj["object_id"], [])
            incoming_associated = incoming_relations.get(obj["object_id"], [])
            associated = outgoing_associated + incoming_associated
            consumer_math_ids = [edge["edge_id"] for edge in outgoing_associated if edge["plane"] in {"proof", "mathematical_prerequisite"}]
            provider_math_ids = [edge["edge_id"] for edge in incoming_associated if edge["plane"] in {"proof", "mathematical_prerequisite"}]
            semantic_ids = [edge["edge_id"] for edge in associated if edge["plane"] in {"mathematical_semantic", "association", "identity", "relation"}]
            reuse_ids = [edge["edge_id"] for edge in associated if edge["plane"] == "reuse_hint" or edge["relation_type"] == "reuse_hint"]
            hard_review = [
                f"{edge['edge_id']}:{edge['review_state']}"
                for edge in associated if edge["blocking"] is True
            ]
            scheduler_effect = [
                f"{edge['edge_id']}:{edge['scheduler_effect']}"
                for edge in outgoing_associated if edge["blocking"] is True
            ]
            gantt_lines.append(
                f"| `{row.item_id}` | `{obj['legacy_item_id']}→{obj['object_id']}` | not_done | `{','.join(row.dependencies) or '-'}` | "
                "unclaimed | not_started | not_live | no_handoff | no_integration | no_repair | blocked_activation | "
                f"`{subject_node.get('notation') or '-'}` / `{'/'.join(subject_path)}` / {str(subject_node['label']['en']).replace('|', '/')} | "
                f"`{assignment['classification_status']}/{assignment['review']['state']}` | `{assignment['record_sha256']}` | "
                f"`{assessment['record_sha256']}` | `{assessment['audit_status']}` | `{','.join(consumer_math_ids) or '[]'}` | "
                f"`{','.join(provider_math_ids) or '[]'}` | `{','.join(semantic_ids) or '[]'}` | "
                f"`{','.join(reuse_ids) or '[]'}` | `{','.join(hard_review) or '[]'}` | "
                f"`{','.join(scheduler_effect) or 'none'}` | "
                f"`{str(assignment['cross_domain']['value']).lower()}` | unscheduled |"
            )
        gantt_lines.extend(["", "## Projection metadata", "", "```json", json.dumps({
            "schema_version": "awesome-theorems/stage5-1-organization/gantt/1.0", "program": program,
            "blueprint_path": blueprint_path, "blueprint_sha256": C.sha256_bytes(blueprint_raw),
            "generated_at": generated_at, "item_count": len(rows), "all_timing_unknown": True,
            "activation_status": "blocked",
            "taxonomy_sha256": C.sha256_bytes(taxonomy_raw),
            "subject_assignments_sha256": C.sha256_bytes(assignment_raw),
            "dependency_assessments_sha256": C.sha256_bytes(assessment_raw),
            "relation_edges_sha256": C.sha256_bytes(relation_raw),
            "execution_hard_dag_sha256": hard_sha,
            **program_metadata_counts,
        }, ensure_ascii=False, sort_keys=True, indent=2), "```", ""])
        bundle[gantt_path] = "\n".join(gantt_lines).encode("utf-8")

    input_entries = []
    for role, relative in INPUT_PATHS.items():
        raw = (root / relative).read_bytes()
        input_entries.append({"role": role, "path": relative, "sha256": C.sha256_bytes(raw), "size_bytes": len(raw)})
    for relative in (CLASSIFIER_PATH, POOL_SOURCE_TAR):
        raw = (root / relative).read_bytes()
        input_entries.append({"role": "predecessor_evidence", "path": relative,
                              "sha256": C.sha256_bytes(raw), "size_bytes": len(raw)})
    input_entries.append({"role": "predecessor_evidence", "path": MSC_PATH, "sha256": MSC_SHA256, "size_bytes": len(msc_raw), "url": MSC_URL, "license": MSC_LICENSE})
    input_root = C.sha256_bytes(C.canonical_json(input_entries))
    source_manifest = C.seal_object({
        "schema_version": SCHEMA["source"], "organization_release": RELEASE, "blueprint_revision": "Stage5.1",
        "base_catalog_release": "5.6", "not_catalog_release_5_1": True, "inputs": input_entries,
        "counts": {"theorem_members": 3500, "strict_conjecture_members": 1425, "source_occurrence_members": 14865, "total_members": 19790, "legacy_checklist_rows": 20197, "msc_rows": 6603},
        "input_root_sha256": input_root,
    })
    bundle[f"{RELEASE_ROOT}/Source_Input_Manifest.json"] = C.canonical_json_pretty(source_manifest)

    # Manifest intentionally excludes itself, Current, and migration to avoid a
    # cyclic digest graph; those successor authorities bind it afterward.
    artifact_paths = sorted(bundle)
    artifacts = [{"path": path, "sha256": C.sha256_bytes(bundle[path]), "size_bytes": len(bundle[path]), "media_type": "text/csv" if path.endswith(".csv") else ("application/jsonl" if path.endswith(".jsonl") else ("application/json" if path.endswith(".json") else "text/markdown")), "rows": len(bundle[path].splitlines()) if path.endswith((".jsonl", ".csv")) else None} for path in artifact_paths]
    schema_paths = sorted(
        path.relative_to(root).as_posix()
        for path in (root / f"{ORG_ROOT}/schemas").glob("*.schema.json")
    )
    schemas = [
        {"path": path, "sha256": C.sha256_bytes((root / path).read_bytes())}
        for path in schema_paths
    ]
    builder_path = "Docs/tools/build_stage5_1_organization_release.py"
    common_path = "Docs/tools/stage5_1_common.py"
    manifest = C.seal_object({
        "schema_version": SCHEMA["manifest"], "organization_release": RELEASE, "blueprint_revision": "Stage5.1",
        "base_catalog_release": "5.6", "not_catalog_release_5_1": True, "generated_at": generated_at,
        "input_manifest": {"path": f"{RELEASE_ROOT}/Source_Input_Manifest.json", "sha256": C.sha256_bytes(bundle[f"{RELEASE_ROOT}/Source_Input_Manifest.json"]), "authority_sha256": source_manifest["authority_sha256"]},
        "counts": {"objects": 19790, "theorems": 3500, "strict_conjectures": 1425,
                   "source_occurrences": 14865, "legacy_checklist_rows": 20197,
                   "subject_nodes": len(nodes), "relation_edges": len(relations),
                   "hard_edges": len(hard_edges)},
        "subject_id_registry": {"path": SUBJECT_ID_REGISTRY_PATH,
                                "sha256": C.sha256_bytes(bundle[SUBJECT_ID_REGISTRY_PATH]),
                                "rows": len(subject_registry)},
        "artifacts": artifacts, "schemas": schemas,
        "candidate_output_root_sha256": C.bundle_digest(bundle),
        "canonicalization": {
            "json": "UTF-8 sorted keys no NaN final LF",
            "jsonl": "canonical compact rows sorted by stable ID final LF",
            "msc_source": "preserve exact ISO-8859-1 tab-delimited bytes",
            "object_seal": "sha256 canonical JSON excluding authority_sha256",
            "record_seal": "sha256 canonical JSON excluding record_sha256",
            "sorted_primary_ids": True,
        },
        "generator": {
            "builder_path": builder_path, "builder_sha256": C.sha256_bytes((root / builder_path).read_bytes()),
            "common_path": common_path, "common_sha256": C.sha256_bytes((root / common_path).read_bytes()),
            "checker_path": CHECKER_PATH, "checker_sha256": C.sha256_bytes((root / CHECKER_PATH).read_bytes()),
        },
        "activation": {"status": "blocked", "requires_explicit_operator_concurrency_prompt": True, "concurrency_defaults_present": False, "fence_receipt_path": "Docs/evidence/stage5_1_shared_execution/activation-fence.json", "preconditions": ["predecessor_admission_stopped", "predecessor_handoffs_dispositioned", "predecessor_live_generations_zero", "predecessor_cron_markers_absent", "stage51_boot_accepted", "complete_current_operator_concurrency_prompt_accepted"]},
    })
    manifest_path = f"{RELEASE_ROOT}/Organization_Manifest.json"
    bundle[manifest_path] = C.canonical_json_pretty(manifest)
    migration = C.seal_object({
        "schema_version": SCHEMA["migration"], "migration_id": "stage5-v2_to_stage5_1-1.0",
        "predecessor": {
            program: {
                "blueprint_path": (INPUT_PATHS["theorem_blueprint"] if program == "theorems" else INPUT_PATHS["conjecture_blueprint"]),
                "blueprint_sha256": C.sha256_bytes((root / (INPUT_PATHS["theorem_blueprint"] if program == "theorems" else INPUT_PATHS["conjecture_blueprint"])).read_bytes()),
            } for program in ("theorems", "conjectures")
        },
        "successor": {"manifest_path": manifest_path,
                      "manifest_sha256": C.sha256_bytes(bundle[manifest_path]),
                      "manifest_authority_sha256": manifest["authority_sha256"],
                      "organization_release": RELEASE},
        "subject_id_registry": {"path": SUBJECT_ID_REGISTRY_PATH,
                                "sha256": C.sha256_bytes(bundle[SUBJECT_ID_REGISTRY_PATH]),
                                "rows": len(subject_registry),
                                "policy": "reuse_predecessor_and_append_after_max"},
        "counts": {"mathematical_one_to_one": 19790, "legacy_checklist_one_to_one": 20197},
        "identity_policy": "exact_ordinal_preserving_bijection_subject_coordinates_are_not_identity",
        "state_policy": "predecessor_state_is_evidence_only_all_stage51_rows_start_not_done",
        "ownership_policy": "fresh_epoch_no_worker_transport_or_lease_inheritance",
        "activation_status": "blocked",
        "activation_preconditions": [
            "release_validated", "crosswalk_complete", "taxonomy_validated",
            "dependency_hard_dag_validated", "predecessor_admission_fenced",
            "predecessor_live_work_harvested_or_retired", "boot_independently_accepted",
            "complete_explicit_concurrency_prompt_supplied",
        ],
        "candidate_output_root_sha256": manifest["candidate_output_root_sha256"],
    })
    migration_path = f"{ORG_ROOT}/migrations/stage5-v2_to_stage5_1-1.0.json"
    bundle[migration_path] = C.canonical_json_pretty(migration)
    current = C.seal_object({
        "schema_version": SCHEMA["current"], "organization_release": RELEASE, "blueprint_revision": "Stage5.1",
        "base_catalog_release": "5.6", "not_catalog_release_5_1": True,
        "manifest": {"path": manifest_path, "sha256": C.sha256_bytes(bundle[manifest_path]), "authority_sha256": manifest["authority_sha256"]},
        "subject_id_registry": {"path": SUBJECT_ID_REGISTRY_PATH,
                                "sha256": C.sha256_bytes(bundle[SUBJECT_ID_REGISTRY_PATH]),
                                "rows": len(subject_registry)},
        "blueprints": {program: {"path": ("Docs/Stage5_1_Theorems_Blueprint.md" if program == "theorems" else "Docs/Stage5_1_Conjectures_Blueprint.md"), "sha256": C.sha256_bytes(bundle["Docs/Stage5_1_Theorems_Blueprint.md" if program == "theorems" else "Docs/Stage5_1_Conjectures_Blueprint.md"]), "gantt_path": ("Docs/Stage5_1_Theorems_Gantt.md" if program == "theorems" else "Docs/Stage5_1_Conjectures_Gantt.md"), "gantt_sha256": C.sha256_bytes(bundle["Docs/Stage5_1_Theorems_Gantt.md" if program == "theorems" else "Docs/Stage5_1_Conjectures_Gantt.md"])} for program in ("theorems", "conjectures")},
        "migration": {"path": migration_path, "sha256": C.sha256_bytes(bundle[migration_path]), "authority_sha256": migration["authority_sha256"]},
        "activation": {"status": "blocked", "reason_codes": ["activation_fence_unaccepted", "stage51_boot_unaccepted", "operator_concurrency_prompt_required"]},
    })
    bundle[f"{ORG_ROOT}/Current_Release.json"] = C.canonical_json_pretty(current)
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--release", default=RELEASE)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--msc-source", type=Path)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        msc = acquire_msc(root, args.msc_source, allow_network=args.write)
        bundle = build_bundle(root, args.release, args.generated_at, msc)
        C.validate_release_bundle(root, bundle)
        if args.check:
            differences = C.compare_bundle(root, bundle)
            if differences:
                raise C.Stage51Error("release differs: " + "; ".join(differences[:10]))
            result = {"valid": True, "mode": "check", "outputs": len(bundle), "bundle_sha256": C.bundle_digest(bundle)}
        else:
            digest = C.write_bundle_transaction(root, bundle)
            result = {"valid": True, "mode": "write", "outputs": len(bundle), "bundle_sha256": digest, "activation": "blocked"}
        print(json.dumps(result, sort_keys=True))
        return 0
    except (C.Stage51Error, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
