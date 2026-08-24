#!/usr/bin/env python3
"""Hermetic tests for the digest-checked Stage5.1 query surface."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUERY_PATH = ROOT / "Docs/tools/query_stage5_1_organization.py"
spec = importlib.util.spec_from_file_location("stage51_query_test", QUERY_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot import {QUERY_PATH}")
query = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = query
spec.loader.exec_module(query)


def seal(value: dict, field: str = "authority_sha256") -> dict:
    result = dict(value)
    result[field] = query.hashlib.sha256(query.canonical_json(result)).hexdigest()
    return result


class Stage51QueryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.release = "9.7"
        self.base = self.root / query.CATALOG_ROOT / "releases" / self.release
        self.base.mkdir(parents=True)
        digest = "1" * 64
        nodes = [
            {"subject_id": "S51-SUB-00000000", "parent_subject_id": None, "rank": "root", "scheme": "internal", "notation": None, "label": {"en": "All", "zh": "All"}},
            {"subject_id": "S51-SUB-00000001", "parent_subject_id": "S51-SUB-00000000", "rank": "branch", "scheme": "MSC", "notation": "10-XX", "label": {"en": "Algebra", "zh": "Algebra"}},
            {"subject_id": "S51-SUB-00000002", "parent_subject_id": "S51-SUB-00000000", "rank": "branch", "scheme": "MSC", "notation": "20-XX", "label": {"en": "Analysis", "zh": "Analysis"}},
            {"subject_id": "S51-SUB-00000003", "parent_subject_id": "S51-SUB-00000002", "rank": "leaf", "scheme": "MSC", "notation": "20A01", "label": {"en": "Fine analysis", "zh": "Fine analysis"}},
        ]
        objects = [
            {"object_id": "S51-THM-00000001", "object_kind": "theorem", "stage51_item_id": "S51THM-00000001-TARGET", "legacy_item_id": "S5THM-00000001-TARGET", "stage5_claim_id": "S5-CLM-00000001", "variant_id": "ATV-00000001", "pool_id": None, "display_name": "One"},
            {"object_id": "S51-THM-00000002", "object_kind": "theorem", "stage51_item_id": "S51THM-00000002-TARGET", "legacy_item_id": "S5THM-00000002-TARGET", "stage5_claim_id": "S5-CLM-00000002", "variant_id": "ATV-00000002", "pool_id": None, "display_name": "Two"},
        ]
        evidence = [{"path": "evidence.json", "sha256": digest, "evidence_kind": "fixture"}]
        assignments = [
            {"object_id": "S51-THM-00000001", "classification_status": "accepted", "primary": {"subject_id": "S51-SUB-00000001", "granularity": "broad", "assertion_state": "accepted", "evidence_tier": "independent_review", "evidence": evidence}, "secondary_subject_ids": [], "candidate_subject_ids": ["S51-SUB-00000001", "S51-SUB-00000003"], "review": {"state": "accepted", "reviewer_id": "r", "receipt_sha256": digest}, "cross_domain": {"value": False, "root_subject_ids": ["S51-SUB-00000001"]}},
            {"object_id": "S51-THM-00000002", "classification_status": "candidate", "primary": {"subject_id": "S51-SUB-00000002", "granularity": "broad", "assertion_state": "candidate", "evidence_tier": "source_category", "evidence": evidence}, "secondary_subject_ids": [], "candidate_subject_ids": ["S51-SUB-00000001"], "review": {"state": "candidate", "reviewer_id": None, "receipt_sha256": None}, "cross_domain": {"value": False, "root_subject_ids": []}},
        ]
        relation = {"edge_id": "S51-REL-0000000000000001", "consumer_member_id": "S51-THM-00000001", "provider_member_id": "S51-THM-00000002", "plane": "association", "relation_type": "related_source", "review_state": "candidate", "evidence_tier": "D_source_reported", "evidence": evidence, "blocking": False, "scheduler_effect": "none"}
        assessments = [
            {"object_id": obj["object_id"], "assessment_id": f"dep-{index}", "item_id": obj["stage51_item_id"], "audit_status": "source_edges_present_pending_review" if index == 1 else "unknown_not_independent_proof_claim", "evidence": evidence}
            for index, obj in enumerate(objects, 1)
        ]
        closures = [
            {"item_id": obj["stage51_item_id"], "assessment_id": f"dep-{index}", "direct_prerequisite_item_ids": ["S51THM-00000002-TARGET"] if index == 1 else [], "transitive_prerequisite_item_ids": ["S51THM-00000002-TARGET"] if index == 1 else [], "direct_edge_ids": [relation["edge_id"]] if index == 1 else [], "topological_rank": index - 1, "hard_dag_sha256": digest}
            for index, obj in enumerate(objects, 1)
        ]
        checklist = [
            {"legacy_item_id": "S5THM-BOOT-001", "new_item_ids": ["S51THM-BOOT-001"], "relationship": "control_successor"},
            {"legacy_item_id": "S5THM-00000001-TARGET", "new_item_ids": ["S51THM-00000001-TARGET"], "relationship": "exact_member_successor"},
            {"legacy_item_id": "S5THM-00000002-TARGET", "new_item_ids": ["S51THM-00000002-TARGET"], "relationship": "exact_member_successor"},
        ]
        worksets = [{"object_id": obj["object_id"], "execution_dependency_item_ids": ["S51THM-BOOT-001"]} for obj in objects]
        hard = {"organization_release": self.release, "edges": [{"edge_id": relation["edge_id"], "consumer_member_id": objects[0]["object_id"], "provider_member_id": objects[1]["object_id"], "scheduler_effect": "block_until_accepted"}], "authority_sha256": digest}
        taxonomy = {"organization_release": self.release, "root_subject_id": nodes[0]["subject_id"]}
        values = {
            "Subject_Taxonomy.json": taxonomy,
            "Subject_Nodes.jsonl": nodes,
            "Object_Index.jsonl": objects,
            "Legacy_Checklist_Row_Crosswalk.jsonl": checklist,
            "Subject_Assignments.jsonl": assignments,
            "Dependency_Assessments.jsonl": assessments,
            "Relation_Edges.jsonl": [relation],
            "Execution_Hard_DAG.json": hard,
            "Dependency_Closure.jsonl": closures,
            "programs/theorems/Organization_Workset.jsonl": worksets,
            "programs/conjectures/Organization_Workset.jsonl": [],
        }
        artifacts = []
        for suffix, value in values.items():
            path = self.base / suffix
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = ((json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
                   if suffix.endswith(".json") else
                   b"".join((query.canonical_json(row) + b"\n") for row in value))
            path.write_bytes(raw)
            artifacts.append({"path": path.relative_to(self.root).as_posix(), "sha256": query.sha256(path)})
        manifest = seal({"organization_release": self.release, "artifacts": artifacts})
        manifest_path = self.base / "Organization_Manifest.json"
        manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
        current = seal({
            "organization_release": self.release,
            "manifest": {"path": manifest_path.relative_to(self.root).as_posix(), "sha256": query.sha256(manifest_path), "authority_sha256": manifest["authority_sha256"]},
        })
        current_path = self.root / query.CATALOG_ROOT / "Current_Release.json"
        current_path.write_text(json.dumps(current, sort_keys=True, indent=2) + "\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_navigation_and_all_identity_surfaces(self) -> None:
        data = query.load(self.root)
        self.assertEqual(query.summary(data)["organization_release"], "9.7")
        member = query.show_member(data, "S5-CLM-00000001", "association", "requires")
        self.assertEqual(member["classification"]["primary"]["granularity"], "broad")
        hint = member["classification"]["candidate_cross_root_hint"]
        self.assertFalse(hint["value"])
        self.assertFalse(hint["accepted_cross_domain_assertion"])
        self.assertGreaterEqual(len(hint["assignment_coordinate_root_subject_ids"]), 2)
        candidate_hint = query.show_member(data, "S5-CLM-00000002", None, None)["classification"]["candidate_cross_root_hint"]
        self.assertTrue(candidate_hint["value"])
        self.assertFalse(candidate_hint["accepted_cross_domain_assertion"])
        self.assertEqual(len(candidate_hint["assignment_coordinate_root_subject_ids"]), 2)
        self.assertEqual(member["relations"][0]["evidence"], [{"evidence_kind": "fixture", "path": "evidence.json", "sha256": "1" * 64}])
        self.assertEqual(member["execution_dependencies"], ["S51THM-BOOT-001"])
        self.assertEqual(member["hard_dependency_closure"]["topological_rank"], 0)
        self.assertEqual(query.show_member(data, "ATV-00000001", None, None)["object"]["object_id"], "S51-THM-00000001")
        control = query.show_member(data, "S51THM-BOOT-001", None, None)
        self.assertIsNone(control["mathematical_member"])
        self.assertEqual(control["checklist_crosswalks"][0]["legacy_item_id"], "S5THM-BOOT-001")
        self.assertEqual(query.children(data, "S51-SUB-00000000", 1)["child_count"], 2)
        self.assertEqual(query.find_subject(data, "analysis", 10)["match_count"], 2)
        self.assertEqual(query.list_subject(data, "S51-SUB-00000003", 10)["members"][0]["roles"], ["candidate"])

    def test_current_and_artifact_digest_tampering_fail_closed(self) -> None:
        current_path = self.root / query.CATALOG_ROOT / "Current_Release.json"
        current = json.loads(current_path.read_text())
        current["organization_release"] = "9.8"
        current_path.write_text(json.dumps(current) + "\n")
        with self.assertRaisesRegex(query.QueryError, "Current_Release authority_sha256 differs"):
            query.load(self.root)

        self.setUp()
        (self.base / "Object_Index.jsonl").write_bytes(b"{}\n")
        with self.assertRaisesRegex(query.QueryError, "artifact SHA-256 differs"):
            query.load(self.root)


if __name__ == "__main__":
    unittest.main()
