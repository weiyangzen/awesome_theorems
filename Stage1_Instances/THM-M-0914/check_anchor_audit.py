#!/usr/bin/env python3
"""Validate the immutable, locally replayable THM-M-0914 anchor-audit packet."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0914-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0914"
BASE_REVISION = "a1c9974d7fb28cd680e6494b968544bf801a93a2"
BASE_TREE = "1fa287bc821355aca2ca9e3ce107830a3eb58e64"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "faef4a7f73219dc5b6178b8788978e21377c593ad84b845b4d49547218e6ae3b"
STATEMENT_SHA256 = "953cf5ba54e27cf08cce5a91880fd79d36f4b5aa7b92228bd27474a1399233db"
LEAN_OUTPUT_SHA256 = "e1b4eed99fb2b93f247cebba950d7dd549dd62d29f2ba046b7a9843a66ef9da4"
DISCOVERY_SHA256 = "c303d49d324e32b5dd5d3b212bde7684801b1ca462571592d6daa93eea79fa10"
WRAPPER_FILE_SHA256 = "fa4604d2b1ae480f910e6000ca8814a632299082b48a14f598314303b68cc582"
WRAPPER_FILE_BLOB = "19ebeb40518e099dc572d5b3b627ce2f62c0745a"
WRAPPER_BODY_SHA256 = "d84d5bc0b4c083cfdfb02001f2def9855531a4c250dbc855132fd9064669eb2f"
TERMINAL_FILE_SHA256 = "5566f2afb81cb80e2aa7349d8b04214f3667d84e4b81d965f85714ec5a8f0e27"
TERMINAL_FILE_BLOB = "d1c2c1e36ea9028aa27c4724c2c9d76afd9af35b"
TERMINAL_BODY_SHA256 = "c88e185f9515ef671655ee204e5526c49887f3a23a56b99a0d849074cdcb9707"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
ZERO_TO_QED_REVISION = "877c7cc5a48833bcac5902d04ccdf65dc308aeaf"
ZERO_TO_QED_SOURCE_SHA256 = "30b14833b4c5aec997dd1c9e005b32a0d75f5101ddd0c12e679cd376cf013e44"
FORMALBOOK_REVISION = "701731c73f68dbc1559703f3568aa5c4924a7bdc"
FORMALBOOK_TREE = "46b452e2b288d837512babfe77aab757518755ed"
FORMALBOOK_SOURCE_SHA256 = "88cbc6496f36d5bae54bcca63f31c95960263dabb371240b74545a328525c5da"
FORMALBOOK_TOOLCHAIN_SHA256 = "194fcae7a59d3268baa175bd3e352dafab6954fe08a5b7caec13bedf36f80315"
FORMALBOOK_MANIFEST_SHA256 = "5fe58b0519da663bf87ccd6fda9aef13caba7fb2a91e5f3978843c3e115edc17"
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "a503b5bbe8ded92348d06711b061737feb0f8939758c25e3a9593bfa8d082d19",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "8ba497bacef09722235917b00b82905075850e83f9d9dbbdedcc209bdfd4343f",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": STATEMENT_SHA256,
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def line_slice_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return sha256_bytes(b"".join(lines[start - 1:end]))


def without_comments_and_strings(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def candidate(audit: dict, candidate_id: str) -> dict:
    return next(row for row in audit["candidates"] if row["candidate_id"] == candidate_id)


def check_actual_canonical_declaration(adapter_source: str) -> None:
    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    imports = (
        "import Mathlib.Data.Fintype.Pigeonhole\n"
        "import Mathlib.Util.AssertNoSorry\n"
        "import Mathlib.Util.PrintSorries\n"
    )
    adapter_body = re.sub(r"^import .*\n", "", adapter_source, flags=re.MULTILINE)
    comparison = r"""

namespace Stage1Instances.THM_M_0914_AnchorAudit

/-- Validator-only definitional identity with the actual statement declaration. -/
theorem actualCanonicalTarget_eq_auditTarget :
    Stage1Instances.THM_M_0914.PigeonholeTarget = ExactTarget :=
  rfl

/-- Validator-only candidate checked directly at the actual statement declaration. -/
theorem exactActualCanonicalAnchor : Stage1Instances.THM_M_0914.PigeonholeTarget :=
  exactTarget_mathlib_candidate

assert_no_sorry exactActualCanonicalAnchor
#print axioms exactActualCanonicalAnchor

end Stage1Instances.THM_M_0914_AnchorAudit
"""
    with tempfile.NamedTemporaryFile("w", suffix=".lean", encoding="utf-8", dir=ROOT) as handle:
        handle.write(imports + statement_source + "\n" + adapter_body + comparison)
        handle.flush()
        result = subprocess.run(
            ["lake", "env", "lean", handle.name],
            cwd=LEAN_ROOT,
            env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit("actual canonical declaration comparison failed")
    if "Declarations are sorry-free!" not in result.stdout:
        sys.stdout.write(result.stdout)
        raise SystemExit("actual canonical wrapper is not machine-reported sorry-free")
    normalized = re.sub(r"\s+", " ", result.stdout)
    actual_axioms = re.findall(r"depends on axioms: \[([^]]*)\]", normalized)
    expected = "propext, Classical.choice, Quot.sound"
    if len(actual_axioms) < 4 or actual_axioms[-1] != expected:
        sys.stdout.write(result.stdout)
        raise SystemExit("actual canonical wrapper axiom report changed")


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1456
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["depends_on"] == ["S56-M-0914-STATEMENT"]
    assert receipt["first_failed_gate"] == (
        "master_acceptance_of_provisional_statement_prerequisite_and_anchor_audit"
    )
    assert receipt["accepted_receipt_ids"] == audit["accepted_receipt_ids"] == []
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["item_id"] == ITEM_ID and packet["base_revision"] == BASE_REVISION
    assert packet["known_failures"] == receipt["known_failures"]
    immutable_inputs = receipt["immutable_inputs"]
    assert immutable_inputs["formalbook_revision"] == FORMALBOOK_REVISION
    assert immutable_inputs["formalbook_tree"] == FORMALBOOK_TREE
    assert immutable_inputs["formalbook_source_sha256"] == FORMALBOOK_SOURCE_SHA256
    assert immutable_inputs["formalbook_toolchain_sha256"] == FORMALBOOK_TOOLCHAIN_SHA256
    assert immutable_inputs["formalbook_lake_manifest_sha256"] == FORMALBOOK_MANIFEST_SHA256
    assert receipt["source_inputs"] == {
        path: f"sha256:{digest}" for path, digest in SOURCE_INPUTS.items()
    }
    for path, digest in SOURCE_INPUTS.items():
        assert sha256(ROOT / path) == digest, f"stale source input: {path}"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1456
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1456
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0914-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    formal = statement["canonical_formal_target"]
    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean") == STATEMENT_SHA256

    assert sha256(HERE / "anchor-discovery-protocol.json") == DISCOVERY_SHA256
    discovery = audit["discovery_protocol"]
    assert discovery["sha256"] == DISCOVERY_SHA256
    assert discovery["inventory_version"] == protocol["inventory_version"]
    assert protocol["frozen_before_candidate_classification"] is True
    assert protocol["saturation_claim"] is discovery["saturation_claim"] is False
    candidate_ids = {row["candidate_id"] for row in audit["candidates"]}
    assert candidate_ids == set(protocol["inventory_members"])
    assert len(candidate_ids) == 7

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == environment["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == environment["toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == environment["mathlib_license_sha256"]
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256

    direct = candidate(audit, "M0914-C01-MATHLIB-DIRECT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == WRAPPER_FILE_BLOB
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == WRAPPER_FILE_BLOB
    wrapper_path = MATHLIB / direct["file"]
    assert sha256(wrapper_path) == direct["file_sha256"] == WRAPPER_FILE_SHA256
    assert line_slice_sha256(wrapper_path, 46, 49) == direct["body_sha256"] == WRAPPER_BODY_SHA256
    assert direct["declaration"] == "Fintype.exists_ne_map_eq_of_card_lt"
    assert direct["local_adapter"].endswith("exactTarget_mathlib_candidate")
    assert direct["terminal_candidate_id"] == "M0914-C02-MATHLIB-FINSET-TERMINAL"
    assert direct["candidate_classification"] == "M3"
    assert direct["candidate_route_if_e1_accepted"] == "M0-W"
    assert direct["evidence_level"] == "provisional_worker_check_below_accepted_E1"
    probe = direct["machine_probe"]
    assert probe["output_sha256"] == LEAN_OUTPUT_SHA256
    assert probe["reported_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert probe["transitive_declaration_closure_count"] == 3623
    assert probe["transitive_module_count"] == 117
    assert probe["transitive_bodyless_nonaxioms"] == []
    assert probe["transitive_unsafe_declarations"] == []

    history = direct["historical_provenance"]
    assert history["lean4_port_tree"] == output(
        "git", "rev-parse", f"{history['lean4_port_commit']}^{{tree}}", cwd=MATHLIB
    )
    assert output(
        "git", "merge-base", "--is-ancestor",
        history["lean4_port_commit"], MATHLIB_REVISION, cwd=MATHLIB,
    ) == ""

    terminal = candidate(audit, "M0914-C02-MATHLIB-FINSET-TERMINAL")
    assert terminal["file_blob"] == TERMINAL_FILE_BLOB
    assert output("git", "rev-parse", f"HEAD:{terminal['file']}", cwd=MATHLIB) == TERMINAL_FILE_BLOB
    terminal_path = MATHLIB / terminal["file"]
    assert sha256(terminal_path) == terminal["file_sha256"] == TERMINAL_FILE_SHA256
    assert line_slice_sha256(terminal_path, 442, 449) == terminal["body_sha256"] == TERMINAL_BODY_SHA256
    terminal_history = terminal["historical_provenance"]
    assert terminal_history["lean4_port_tree"] == output(
        "git", "rev-parse", f"{terminal_history['lean4_port_commit']}^{{tree}}", cwd=MATHLIB
    )
    assert output(
        "git", "merge-base", "--is-ancestor",
        terminal_history["lean4_port_commit"], MATHLIB_REVISION, cwd=MATHLIB,
    ) == ""

    wrapper_source = wrapper_path.read_text(encoding="utf-8")
    terminal_source = terminal_path.read_text(encoding="utf-8")
    for marker in (
        "theorem exists_ne_map_eq_of_card_lt (f : alpha → beta)",
        "Finset.exists_ne_map_eq_of_card_lt_of_maps_to h",
        "Function.Embedding",
        "Fintype.exists_ne_map_eq_of_card_lt f h",
    ):
        marker = marker.replace("alpha", "α").replace("beta", "β")
        assert marker in wrapper_source, marker
    for marker in (
        "theorem exists_ne_map_eq_of_card_lt_of_maps_to",
        "by_contra! hz",
        "card_le_card_of_injOn f hf",
        "exact hz x hx y hy",
    ):
        assert marker in terminal_source, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|proof_wanted|native_decide|"
        r"implemented_by|extern)\b"
    )
    visible = "\n".join(wrapper_source.splitlines()[38:66])
    visible += "\n" + "\n".join(terminal_source.splitlines()[437:450])
    assert forbidden.search(without_comments_and_strings(visible)) is None

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "∀ (n : Nat) (f : Fin (n + 1) → Fin n)",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "exact Fintype.exists_ne_map_eq_of_card_lt f (by simp)",
        "assert_no_sorry Fintype.exists_ne_map_eq_of_card_lt",
        "assert_no_sorry exactTarget_mathlib_candidate",
        "#print_anchor_closure",
    ):
        assert marker in adapter, marker
    assert forbidden.search(without_comments_and_strings(adapter)) is None
    check_actual_canonical_declaration(adapter)

    external = candidate(audit, "M0914-C05-ZERO-TO-QED")
    assert external["revision"] == ZERO_TO_QED_REVISION
    assert external["file_sha256"] == ZERO_TO_QED_SOURCE_SHA256
    assert external["tree"] == "47537dd82603d98271ea1c6b8b855ce226ce9938"
    assert external["toolchain"] == "leanprover/lean4:v4.30.0"
    assert external["mathlib_revision"] == "c5ea00351c28e24afc9f0f84379aa41082b1188f"
    assert external["candidate_classification"] == "M3_external_exact_source_anchor"
    assert external["evidence_level"] == "E3"
    assert external["local_compatibility_probe"]["exit"] == 0
    assert external["local_compatibility_probe"]["output_sha256"] == hashlib.sha256(b"").hexdigest()
    assert "not independently built" in external["machine_boundary"]

    formalbook = candidate(audit, "M0914-C06-FORMALBOOK")
    assert formalbook["revision"] == FORMALBOOK_REVISION
    assert formalbook["tree"] == FORMALBOOK_TREE
    assert formalbook["file_blob"] == "9429463c8c7e1398e65f53e40fd18a1bb942454a"
    assert formalbook["file_sha256"] == FORMALBOOK_SOURCE_SHA256
    assert formalbook["toolchain_file_sha256"] == FORMALBOOK_TOOLCHAIN_SHA256
    assert formalbook["lake_manifest_sha256"] == FORMALBOOK_MANIFEST_SHA256
    assert formalbook["lakefile_sha256"] == (
        "0988b546f90f42309f0ce0522e099cb9003416391b867263b2ff9f92218fd76e"
    )
    assert formalbook["license_blob"] == "d645695673349e3947e8e5ae42332d0ac3164cd7"
    assert formalbook["terminal_candidate_id"] == "M0914-C01-MATHLIB-DIRECT"
    assert formalbook["candidate_classification"] == "M3_external_duplicate_wrapper"

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("7/7 frozen candidate groups")
    assert result["exact_candidate_located"] is result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["eligible_external_integration_debt"] is True
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_route"] == "M0-W"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "provisional_worker_check_below_accepted_E1"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is result["theorem_complete"] is False
    before = {"H": "H1", "M": "M3", "R": "R4"}
    assert audit["root_vector_before"] == audit["accepted_root_vector_after"] == before
    assert receipt["root_vector_before"] == receipt["accepted_root_vector_after"] == before
    assert audit["root_candidate_vector_after"] == receipt["root_candidate_vector_after"] == before
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False
    assert audit["gate_state"] == "worker_self_tested_pending_master_acceptance"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

    lean_environment = os.environ.copy()
    lean_environment.update({"LC_ALL": "C", "TZ": "UTC"})
    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0914/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        env=lean_environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if lean.stdout.count("Declarations are sorry-free!") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("expected three machine-produced sorry-free reports")
    normalized = re.sub(r"\s+", " ", lean.stdout)
    axiom_reports = re.findall(r"depends on axioms: \[([^]]*)\]", normalized)
    if axiom_reports != ["propext, Classical.choice, Quot.sound"] * 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected wrapper, terminal, or adapter axiom report")
    for marker in (
        "theorem Fintype.exists_ne_map_eq_of_card_lt",
        "theorem Finset.exists_ne_map_eq_of_card_lt_of_maps_to",
        "ANCHOR_CLOSURE declarations=3623 modules=117",
        "ANCHOR_CLOSURE axioms=[propext, Classical.choice, Quot.sound]",
        "ANCHOR_CLOSURE bodyless_nonaxioms=[]",
        "ANCHOR_CLOSURE unsafe=[]",
    ):
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean evidence marker: {marker}")
    if "sorryAx" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output contains a proof placeholder")
    exact_target = re.search(
        r"def Stage1Instances\.THM_M_0914_AnchorAudit\.ExactTarget : Prop :=\n"
        r"(?P<expression>.*)\Z",
        lean.stdout,
        re.DOTALL,
    )
    if exact_target is None:
        sys.stdout.write(lean.stdout)
        raise SystemExit("could not extract the audit target's explicit expression")
    explicit = " ".join(exact_target.group("expression").strip().split())
    frozen_explicit = formal["fully_explicit_expression"]
    # Lean's pretty-printer retains existential notation under pp.explicit. Normalize only those
    # two binders; the carriers and predicate remain the fully explicit frozen expression.
    carrier = (
        "Fin (@HAdd.hAdd.{0, 0, 0} Nat Nat Nat (@instHAdd.{0} Nat instAddNat) n "
        "(@OfNat.ofNat.{0} Nat (nat_lit 1) (instOfNatNat (nat_lit 1))))"
    )
    frozen_pretty = frozen_explicit.replace(
        f"@Exists.{{1}} ({carrier}) fun x => @Exists.{{1}} ({carrier}) fun y => ",
        "∃ x y, ",
    )
    if explicit != frozen_pretty:
        sys.stdout.write(lean.stdout)
        raise SystemExit("audit target is not expression-identical to the frozen statement")
    if sha256_bytes(lean.stdout.encode()) != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0914; 7 candidate groups classified; prospective pinned mathlib M0-W route "
        "held at M3 below accepted E1; "
        "accepted root remains H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
