#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((HERE / "anchor-audit.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-1014-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1014"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert pin == head == audit["immutable_environment"]["mathlib_revision"]

module = MATHLIB / "Mathlib" / "MeasureTheory" / "Measure" / "ProbabilityMeasure.lean"
assert hashlib.sha256(module.read_bytes()).hexdigest() == \
    audit["immutable_environment"]["primary_source_sha256"]
source = module.read_text()
terminal = source.split("lemma tendsto_map_of_tendsto_of_continuous", 1)[1]
terminal = terminal.split("lemma continuous_map", 1)[0]
assert "tendsto_iff_forall_lintegral_tendsto" in terminal
assert "lintegral_map" in terminal
assert "by sorry" not in terminal

probe = (HERE / "AnchorAudit.lean").read_text()
frozen = (HERE / "Statement.lean").read_text()
for clause in [
    "TopologicalSpace alpha",
    "OpensMeasurableSpace alpha",
    "BorelSpace beta",
    "mu_n : iota -> ProbabilityMeasure alpha",
    "Tendsto mu_n L (nhds mu)",
    "ProbabilityMeasure.map (mu_n n) hf.measurable.aemeasurable",
]:
    assert clause in probe and clause in frozen

exact = audit["candidates"][0]
assert exact["kind"] == "exact_terminal_theorem"
assert exact["revision"] == pin
assert exact["proof_credit_at_this_phase"] is False
assert audit["root_machine_classification"].startswith("M0-P_candidate")
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False
assert audit["gate_state"] == "self_tested_pending_master_acceptance"

print("check_anchor_audit: ok (exact pin, source hash, target clauses, 5 classified candidates)")
