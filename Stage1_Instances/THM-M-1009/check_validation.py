#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1009-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1009"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
LEAN_REVISION = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_EXPRESSION = "5933a50ff097d2de1336a67d4671b3caf7add728d2be6f8be22f95a0385dec1f"
EXPECTED_DENOMINATOR = "24570f903e38e644cc31fc4f8725224e3551ab48325fedc9a072fdedb4c1b93d"
EXPECTED_TOOLCHAIN_HASH = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_HASH = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_LEAN_HASH = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
EXPECTED_BOREL_SOURCE_HASH = "e0d1d942afe23e5168486650beb83255274103f1cc4b74bc74b4d3b5a72d500e"
EXPECTED_BOREL_OLEAN_HASH = "e21fee914acea119483ca07170e6fb18f050e27f51ae8f6be65d77481defc39a"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("validation failed: " + message)


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=360,
        check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def uncommented(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(?P<body>.*?)]",
        output,
        flags=re.DOTALL,
    )
    require(match is not None, f"missing axiom report for {declaration}")
    return {item.strip() for item in match.group("body").split(",") if item.strip()}


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
receipt = json.loads((HERE / "validation-receipt.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
proof_status = json.loads((HERE / "proof-status.json").read_text(encoding="utf-8"))

require(spec["item_id"] == "S56-M-1009-VALIDATION", "wrong validation item")
require(spec["theorem_id"] == "THM-M-1009", "wrong theorem in validation spec")
require(receipt["item_id"] == spec["item_id"], "receipt/spec item mismatch")
require(receipt["theorem_id"] == spec["theorem_id"], "receipt/spec theorem mismatch")
require(spec["argv"] == ["python3", "Stage1_Instances/THM-M-1009/check_validation.py"], "wrong argv")
require(spec["network_policy"] == "denied_by_recipe_contract_not_host_enforced", "wrong network policy")
require(spec["expected_exit"] == 0, "wrong expected exit")
require(spec["release_grade"] is False, "worker recipe cannot be release grade")
require(set(spec["allowed_observed_axioms"]) == EXPECTED_AXIOMS, "wrong axiom policy")

input_paths = {
    "validation_spec_sha256": HERE / "validation-spec.json",
    "validator_sha256": HERE / "check_validation.py",
    "validation_probe_sha256": HERE / "Validation.lean",
    "statement_sha256": HERE / "Statement.lean",
    "obligation_tree_sha256": HERE / "ObligationTree.lean",
    "proof_sha256": HERE / "Proof.lean",
    "statement_record_sha256": HERE / "statement.json",
    "anchor_audit_sha256": HERE / "anchor-audit.json",
    "obligation_registry_sha256": HERE / "obligation-registry.json",
    "typed_graphs_sha256": HERE / "typed-graphs.json",
    "validation_specs_sha256": HERE / "validation-specs.json",
    "proof_receipt_sha256": HERE / "proof-receipt.json",
    "proof_status_sha256": HERE / "proof-status.json",
    "proof_checker_sha256": HERE / "check_proof.py",
    "lean_toolchain_sha256": LEAN_ROOT / "lean-toolchain",
    "lake_manifest_sha256": LEAN_ROOT / "lake-manifest.json",
}
for key, path in input_paths.items():
    require(receipt["inputs"][key] == digest(path), f"stale receipt input: {key}")

target = statement["canonical_formal_target"]
require(target["statement_file_sha256"] == digest(HERE / "Statement.lean"), "statement record drift")
require(target["elaborated_expression_sha256"] == EXPECTED_EXPRESSION, "wrong expression fingerprint")
require(registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json"), "registry/statement drift")
require(registry["denominator_sha256"] == EXPECTED_DENOMINATOR, "wrong obligation denominator")
require(graphs["registry_denominator_sha256"] == EXPECTED_DENOMINATOR, "graph/registry drift")
require(graphs["closure_boundary"]["root_closed"] is False, "worker rewrote frozen root state")
require(graphs["closure_boundary"]["theorem_complete"] is False, "graph claims theorem completion")
require(proof_receipt["item_id"] == "S56-M-1009-PROOF", "wrong proof dependency")
require(proof_receipt["accepted"] is False, "proof dependency unexpectedly accepted")
require(proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean"), "stale proof body")
require(proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean"), "proof statement drift")
require(proof_receipt["inputs"]["obligation_tree_sha256"] == digest(HERE / "ObligationTree.lean"), "proof composition drift")
require(proof_receipt["inputs"]["obligation_registry_sha256"] == digest(HERE / "obligation-registry.json"), "proof registry drift")
require(proof_receipt["result"]["root_kernel_closed"] is True, "proof receipt omits local root closure")
require(proof_receipt["result"]["accepted_root_closed"] is False, "proof receipt claims acceptance")
require(proof_status["root_kernel_closed"] is True, "proof status omits local kernel closure")
require(proof_status["root_accepted"] is False, "proof status claims accepted root")
require(proof_status["theorem_complete"] is False, "proof status claims theorem completion")

probe = (HERE / "Validation.lean").read_text(encoding="utf-8")
require("import Proof" not in probe, "validation probe imports the proof module")
require("import ObligationTree" not in probe, "validation probe imports the composition module")
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|"
    r"implemented_by|native_decide)\b"
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    require(prohibited.search(uncommented(HERE / name)) is None, f"prohibited construct in {name}")

require(digest(LEAN_ROOT / "lean-toolchain") == EXPECTED_TOOLCHAIN_HASH, "toolchain file drift")
require(digest(LEAN_ROOT / "lake-manifest.json") == EXPECTED_MANIFEST_HASH, "Lake manifest drift")
manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
mathlib_entry = next((row for row in manifest["packages"] if row["name"] == "mathlib"), None)
require(mathlib_entry is not None and mathlib_entry["rev"] == MATHLIB_REVISION, "manifest mathlib pin drift")
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
require(mathlib.is_dir(), "canonical pinned mathlib artifact is missing")
require(run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION, "mathlib checkout pin drift")
require(run(["git", "status", "--short"], cwd=mathlib) == "", "pinned mathlib source is dirty")
borel_source = mathlib / "Mathlib" / "Probability" / "BorelCantelli.lean"
borel_olean = mathlib / ".lake" / "build" / "lib" / "lean" / "Mathlib" / "Probability" / "BorelCantelli.olean"
require(digest(borel_source) == EXPECTED_BOREL_SOURCE_HASH, "terminal import source drift")
require(digest(borel_olean) == EXPECTED_BOREL_OLEAN_HASH, "terminal import olean drift")

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
lean = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin" / "lean"
require(lean.is_file() and digest(lean) == EXPECTED_LEAN_HASH, "Lean executable identity drift")
require(LEAN_REVISION in run([str(lean), "--version"], cwd=LEAN_ROOT), "Lean revision drift")

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m1009-validation-") as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    env = os.environ.copy()
    env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LEAN_NUM_THREADS": "1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    })
    env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [str(lean), "--trust=0", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=tmp,
        env=env,
    )
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["ObligationTree.lean"] = run(
        [str(lean), "--trust=0", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=tmp,
        env=env,
    )
    outputs["Proof.lean"] = run([str(lean), "--trust=0", str(tmp / "Proof.lean")], cwd=tmp, env=env)
    outputs["Validation.lean"] = run([str(lean), "--trust=0", str(tmp / "Validation.lean")], cwd=tmp, env=env)

for declaration in (
    "Stage1Instances.THM_M_1009.erdosRenyiLowerBoundTarget",
    "Stage1Instances.THM_M_1009.erdosRenyiObligationRoot_via_frozen_composition",
):
    require(reported_axioms(outputs["Proof.lean"], declaration) == EXPECTED_AXIOMS, f"unexpected proof axioms: {declaration}")
for declaration in (
    "Stage1Instances.THM_M_1009.Validation.independentRootFromInterfaces",
    "Stage1Instances.THM_M_1009.Validation.exactTargetProbe",
):
    require(reported_axioms(outputs["Validation.lean"], declaration) == EXPECTED_AXIOMS, f"unexpected probe axioms: {declaration}")
require("sorryAx" not in "".join(outputs.values()), "kernel output exposes sorryAx")

result = receipt["result"]
require(result["root_kernel_replay"] == "pass", "receipt omits kernel pass")
require(result["trust_observation"] == "pass_for_observed_axioms_only", "receipt overstates trust")
require(result["local_provenance"] == "pass", "receipt omits local provenance pass")
require(result["independent_composition_probe"] == "pass_not_independent_mathematical_proof", "receipt overstates probe")
require(result["hermetic_release_gate"] == "fail_closed", "receipt overstates hermetic evidence")
require(result["independent_runner_gate"] == "fail_closed", "receipt overstates independent evidence")
require(result["audit_complete"] is False and result["theorem_complete"] is False, "receipt claims terminal completion")
require(receipt["release_grade"] is False, "worker receipt cannot be release grade")
require(receipt["first_failed_gate"] == "dependency.S56-M-1009-PROOF.master_acceptance", "wrong first failed gate")

print("PASS THM-M-1009 narrow validation")
print("kernel: exact frozen root and frozen composition replayed from temporary source copies")
print("trust: both root paths report exactly propext, Classical.choice, Quot.sound; hygiene passed")
print("provenance: frozen hashes, proof linkage, Lean identity, clean mathlib pin, source and olean hashes passed")
print("differential: independently written final composition and exact-type probe elaborated without importing Proof")
print("blocked: proof master acceptance, graph reconciliation, cold offline hermetic replay, and distinct-runner verification")
