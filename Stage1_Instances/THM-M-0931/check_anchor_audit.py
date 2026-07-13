#!/usr/bin/env python3
"""Validate the immutable local evidence for the THM-M-0931 anchor audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
THEOREM_ID = "THM-M-0931"
ITEM_ID = "S56-M-0931-ANCHOR_AUDIT"
BASE_REVISION = "a1c9974d7fb28cd680e6494b968544bf801a93a2"
BASE_TREE = "1fa287bc821355aca2ca9e3ce107830a3eb58e64"
EXPRESSION_SHA256 = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
STATEMENT_SHA256 = "d0e7e43d896a0625e87b3fac55319d5e999351c8f74cdda4e699d9360d651020"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_OUTPUT_SHA256 = "3ae69c74dd460ea6701315fcfca8f7d021b5305bd88bacd0b8c17f3190c253e5"
PROTOCOL_SHA256 = "414354fb29745cf8618f41ffc3b8e9c9d00e58e735f8621f2e3eec8c71b3b0a6"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
FORBIDDEN_WORDS = tuple(
    "".join(chr(code) for code in codes)
    for codes in (
        (115, 111, 114, 114, 121),
        (97, 100, 109, 105, 116),
        (115, 111, 114, 114, 121, 65, 120),
        (97, 120, 105, 111, 109),
        (99, 111, 110, 115, 116, 97, 110, 116),
        (117, 110, 115, 97, 102, 101),
        (105, 109, 112, 108, 101, 109, 101, 110, 116, 101, 100, 95, 98, 121),
        (101, 120, 116, 101, 114, 110),
        (111, 112, 97, 113, 117, 101),
        (110, 97, 116, 105, 118, 101, 95, 100, 101, 99, 105, 100, 101),
        (114, 117, 110, 95, 116, 97, 99),
        (112, 114, 111, 111, 102, 95, 119, 97, 110, 116, 101, 100),
    )
)
FORBIDDEN = re.compile(r"\b(?:" + "|".join(FORBIDDEN_WORDS) + r")\b")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1470
    assert audit["base_revision"] == receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["candidate_result"]["classification"] == (
        "M0-W_candidate_pending_downstream_acceptance"
    )
    assert receipt["candidate_result"]["evidence_level"] == "E2_local_nonrelease_kernel_probe"
    assert receipt["candidate_result"]["kernel_checked"] is True
    assert receipt["candidate_result"]["sorry_free"] is True
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert target["execution_rank"] == 1470
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0931-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["protocol_id"] == "S56-M-0931-ANCHOR-DISCOVERY-20260713-01"
    assert protocol["inventory_version"] == audit["inventory_version"]
    assert protocol["saturation_claim"] is False
    assert len(protocol["aliases"]) >= 10 and len(protocol["surfaces"]) >= 7
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["lean_toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert output("git", "rev-parse", "HEAD:LICENSE", cwd=MATHLIB) == env["mathlib_license_blob"]

    candidates = audit["candidates"]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    assert len(candidate_ids) == len(set(candidate_ids)) == 7
    direct = next(c for c in candidates if c["candidate_id"] == "M0931-C01-MATHLIB-INT-MULTISET")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["terminal_declaration"] == "Int.erdos_ginzburg_ziv_multiset"
    assert direct["local_role"] == "audit-only exact wrapper candidate"
    assert direct["terminal_proof_body_id"] == (
        "git-blob:dbe223c73d6c612461bc900d3d7dd70be3c1d747:Int.erdos_ginzburg_ziv_multiset"
    )
    assert len(direct["direct_proof_dependencies"]) >= 7
    assert direct["machine_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    egz = MATHLIB / direct["file"]
    assert sha256(egz) == direct["source_sha256"]
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == direct["source_git_blob"]
    body_slice = b"".join(egz.read_bytes().splitlines(keepends=True)[191:195])
    assert hashlib.sha256(body_slice).hexdigest() == direct["proof_body_slice_sha256"]
    assert output(
        "git", "merge-base", "--is-ancestor", direct["introduction_revision"], "HEAD", cwd=MATHLIB
    ) == ""
    assert output(
        "git", "rev-parse", f"{direct['introduction_revision']}^{{tree}}", cwd=MATHLIB
    ) == direct["introduction_tree"]
    assert output(
        "git", "rev-parse", f"{direct['introduction_revision']}:{direct['file']}", cwd=MATHLIB
    ) == direct["introduction_source_blob"]
    introduction = subprocess.check_output(
        ["git", "show", f"{direct['introduction_revision']}:{direct['file']}"], cwd=MATHLIB
    )
    assert hashlib.sha256(introduction).hexdigest() == direct["introduction_source_sha256"]

    for module in direct["direct_module_imports"]:
        file = MATHLIB / (module["module"].replace(".", "/") + ".lean")
        assert sha256(file) == module["source_sha256"]
        relative = file.relative_to(MATHLIB).as_posix()
        assert output("git", "rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == module["git_blob"]

    egz_source = egz.read_text(encoding="utf-8")
    for marker in (
        "theorem Int.erdos_ginzburg_ziv (a : ι → ℤ)",
        "induction n using Nat.prime_composite_induction",
        "Int.erdos_ginzburg_ziv_prime a ht",
        "char_dvd_card_solutions_of_add_lt p",
        "theorem Int.erdos_ginzburg_ziv_multiset",
        "Int.erdos_ginzburg_ziv (s := s.toEnumFinset)",
        "Multiset.map_fst_le_of_subset_toEnumFinset",
        "theorem ZMod.erdos_ginzburg_ziv_multiset",
    ):
        assert marker in egz_source, marker
    assert not FORBIDDEN.search(without_comments(egz_source))

    support = next(c for c in candidates if c["candidate_id"] == "M0931-C04-MATHLIB-CHEVALLEY-WARNING")
    support_source = MATHLIB / support["file"]
    assert sha256(support_source) == support["file_sha256"]
    assert output("git", "rev-parse", f"HEAD:{support['file']}", cwd=MATHLIB) == support["file_blob"]
    support_text = support_source.read_text(encoding="utf-8")
    assert "theorem char_dvd_card_solutions_of_sum_lt" in support_text
    assert "theorem char_dvd_card_solutions_of_add_lt" in support_text
    assert not FORBIDDEN.search(without_comments(support_text))

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall (n : Nat), 0 < n -> forall (s : Multiset Int)",
        "theorem exactTarget_mathlib_candidate : ExactTarget := by",
        "exact Int.erdos_ginzburg_ziv_multiset s hs.ge",
        "#print axioms Int.erdos_ginzburg_ziv_multiset",
        "#print axioms char_dvd_card_solutions_of_add_lt",
        "#print sorries Int.erdos_ginzburg_ziv_multiset",
        "#print sorries exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    assert not FORBIDDEN.search(without_comments(adapter))

    decision = audit["inventory_decision"]
    assert decision["inventory_classified"] is True
    assert decision["source_boundary_coverage"].startswith("7/7")
    assert decision["exact_candidate_located"] is True
    assert decision["exact_candidate_kernel_probed"] is True
    assert decision["candidate_accepted_by_master"] is False
    assert decision["root_machine_candidate_classification"] == (
        "M0-W_candidate_pending_downstream_acceptance"
    )
    assert decision["authoritative_root_vector_before"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert decision["authoritative_root_vector_after"] == decision["authoritative_root_vector_before"]
    assert decision["kernel_closed_as_accepted_root"] is False
    assert audit["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0931/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") != 6:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected transitive sorry report")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0931; 7 records; exact pinned mathlib adapter; "
        "candidate M0-W, accepted root H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
