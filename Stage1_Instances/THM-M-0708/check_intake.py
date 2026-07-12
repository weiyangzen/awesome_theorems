#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / "intake.json").read_text(encoding="utf-8"))

required = {
    "schema_version", "item_id", "theorem_id", "execution_rank", "lifecycle_mode",
    "canonical_name", "canonical_statement", "canonical_formal_target",
    "domain_and_universes", "quantifiers", "hypotheses", "conclusion",
    "alternate_encodings", "excluded_degenerate_cases", "foundation_profile",
    "tcb_profile", "computation_profile", "formal_system", "source_revisions",
    "obligation_registry_hash", "discovery_protocol_hash", "authoritative_blueprint",
    "public_merge_targets", "owners_and_reviewers", "freshness_and_revocation_policy",
    "root_vector", "theorem_complete", "status_boundary",
}
missing = sorted(required - data.keys())
assert not missing, f"missing intake fields: {missing}"
assert data["item_id"] == "S56-M-0708-INTAKE"
assert data["theorem_id"] == "THM-M-0708"
assert data["execution_rank"] == 749
assert data["lifecycle_mode"] == "planned"
assert data["canonical_formal_target"]["gate_state"] == "open_pending_statement_phase"
assert data["canonical_formal_target"]["elaborated_expression_hash"] is None
assert data["theorem_complete"] is False
assert data["root_vector"] == {"human": "H1", "machine": "M4", "readability": "R3"}
for target in data["public_merge_targets"]:
    path = root.parents[1] / target
    assert path.is_file(), f"missing public merge target: {target}"
for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md"):
    text = (root / name).read_text(encoding="utf-8")
    assert "theorem_complete=true" not in text
print("check_intake: ok (planned THM-M-0708 dossier; H1/M4/R3; no theorem-completion claim)")
