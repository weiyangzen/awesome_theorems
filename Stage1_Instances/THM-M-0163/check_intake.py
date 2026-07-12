#!/usr/bin/env python3
"""Fail-closed structural self-test for the THM-M-0163 planned intake."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances" / "THM-M-0163"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"check_intake: FAIL: {message}")


intake = json.loads((DOSSIER / "intake.json").read_text(encoding="utf-8"))
targets = json.loads((ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target_rows = targets["targets"] if isinstance(targets, dict) else targets
row = next((entry for entry in target_rows if entry.get("theorem_id") == "THM-M-0163"), None)

require(row is not None, "target is absent from the rev-5.6 manifest")
require(row["execution_rank"] == 662, "execution rank is not 662")
require(row["baseline"] == "L0" and row["rework_required"] is True,
        "manifest does not retain the uniform L0/rework-required baseline")
require(intake["schema_version"] == "stage1-instance/5.6.0", "wrong schema version")
require(intake["item_id"] == "S56-M-0163-INTAKE", "wrong item ID")
require(intake["theorem_id"] == "THM-M-0163", "wrong theorem ID")
require(intake["lifecycle_mode"] == "planned", "intake must remain planned")
require(intake["theorem_complete"] is False, "intake must not claim theorem completion")
require(intake["canonical_formal_target"]["gate_state"] == "open_pending_statement_phase",
        "statement gate must remain explicitly open")
require(intake["canonical_formal_target"]["elaborated_expression_hash"] is None,
        "intake must not invent an expression hash")
require(intake["obligation_registry_hash"] is None, "intake must not pre-credit a registry hash")
require(intake["root_vector"] == {"human": "H2", "machine": "M4", "readability": "R3"},
        "unexpected provisional debt vector")
require(len(intake["quantifiers"]) >= 6 and len(intake["hypotheses"]) >= 4,
        "scope does not enumerate binders and hypotheses")
require(len(intake["alternate_encodings"]) == 3,
        "intrinsic, variational, and minimization encodings must stay explicit")

for rel in intake["public_merge_targets"]:
    require((ROOT / rel).is_file(), f"missing public merge target: {rel}")

readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
crosswalk = (DOSSIER / "source_statement_crosswalk.md").read_text(encoding="utf-8")
require("globally" in readme and "locally minimizing" in readme,
        "README omits the local/global boundary")
require("THM-P-0639" in crosswalk, "crosswalk omits the neighboring physics exclusion")
require("No source above is accepted as `H0`" in crosswalk, "source status boundary is absent")

print("check_intake: ok (THM-M-0163 planned scope, source crosswalk, and open gates validated)")
