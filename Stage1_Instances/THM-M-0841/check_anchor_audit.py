#!/usr/bin/env python3
"""Validate the immutable, target-owned THM-M-0841 anchor audit."""

from __future__ import annotations

import argparse
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
ITEM_ID = "S56-M-0841-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0841"
RANK = 1398
BASE_REVISION = "b4319ef6d039de12cec559f173287d541c238d70"
BASE_TREE = "0b0762ebd01405d33218c3bcbcb24d4544b0fad0"
EXPRESSION_SHA256 = "ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733"
STATEMENT_SHA256 = "897dcc398df34c0dd6ad02dc2092a08f46a6cafc908c2e9f8497a895aa66663d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
COMPLETE_FILE = "Mathlib/Combinatorics/SimpleGraph/CompleteMultipartite.lean"
COMPLETE_BLOB = "d8c46737a0c7ac4062b7d0704c2a84a368aff314"
COMPLETE_SHA256 = "47d5f3f6aeef27940353ed98341de68673139973198de234482adbc139afb236"
DENSITY_FILE = "Mathlib/Combinatorics/SimpleGraph/Extremal/TuranDensity.lean"
DENSITY_BLOB = "0b9ff46f5a56fcbf80fdf29b675edb892a00ced7"
DENSITY_SHA256 = "a2724d485df3a96fcbcf6b7f0cc55ae62dab4251f625a6b85f75bb72692f55e7"
POST_PIN_REVISION = "b9df47b72b287802f6d40cf7588dada976bc657d"
POST_PIN_TREE = "e1dfb46b94cc7dbd9f95e96f1cd2f138f217d0d5"
POST_PIN_FILE = "Mathlib/Combinatorics/SimpleGraph/Extremal/ErdosStoneSimonovits.lean"
POST_PIN_BLOB = "ef28446b9a088309e814a0eb7eae4b2e975ac9cc"
POST_PIN_SHA256 = "455735f55b4f2ec2e5dd94a6ef7cb473121609d3ec35d3522031914b41b11148"
EXTERNAL_REVISION = "fd0134209519a72b59462f796e957981bb322e7c"
EXTERNAL_TREE = "4cc782dc121d40030432320fd23542698ab39b40"
EXTERNAL_ARCHIVE_SHA256 = "f8aa6d33638b139b96c553b063395cd3ba3ef02061863ea77fa4b818aad811a5"
EXTERNAL_SOURCE_SHA256 = "ba08fa485e27f97fc338f8e2b41b785c0d12474c932decff0d5482580addc61b"
LEAN_OUTPUT_SHA256 = "3f12cf995da28ccc798c2360ae52704a639b75ca0548ef25b5eef79757d4fee2"
LOCAL_SEARCH_SHA256 = "60a1f806b8e6c7e3bb43f93419c83efa5d872cd38f8b86ea1c5d44a817d97f8c"
SOURCEGRAPH_RESPONSE_SHA256 = "5bd92ba4f903d065b2f967fa42d4ab6f9742c60d12d29e7ecc598fce780dfe21"
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
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments_and_strings(source: str) -> str:
    result: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if in_string:
            if source[index] == "\\":
                index += 2
            elif source[index] == '"':
                in_string = False
                result.append('""')
                index += 1
            else:
                if source[index] == "\n":
                    result.append("\n")
                index += 1
        elif depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            result.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                result.append("\n")
            index += 1
        elif source[index] == '"':
            in_string = True
            index += 1
        else:
            result.append(source[index])
            index += 1
    if depth or in_string:
        raise SystemExit("unterminated Lean comment or string")
    return "".join(result)


def run_lean() -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    return subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0841/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def run_canonical_equivalence_fixture() -> subprocess.CompletedProcess[str]:
    """Elaborate the frozen statement and audit copy together without adding proof content."""
    statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
    anchor = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    statement_body = "\n".join(
        line for line in statement.splitlines() if not line.startswith("import ")
    )
    anchor_body = "\n".join(
        line for line in anchor.splitlines() if not line.startswith("import ")
    )
    fixture = "\n".join(
        (
            "import Mathlib.Analysis.SpecialFunctions.Log.Basic",
            "import Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite",
            "import Mathlib.Combinatorics.SimpleGraph.Extremal.TuranDensity",
            "import Mathlib.Util.AssertNoSorry",
            "import Mathlib.Util.PrintSorries",
            statement_body,
            anchor_body,
            "namespace Stage1Instances.THM_M_0841_AnchorAudit",
            "theorem canonicalTarget_eq_auditTarget :",
            "    Stage1Instances.THM_M_0841.ErdosStoneTarget = ExactTarget := rfl",
            "assert_no_sorry canonicalTarget_eq_auditTarget",
            "#print axioms canonicalTarget_eq_auditTarget",
            "end Stage1Instances.THM_M_0841_AnchorAudit",
            "",
        )
    )
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    with tempfile.TemporaryDirectory(prefix="thm-m-0841-anchor-") as directory:
        path = Path(directory) / "CanonicalEquivalence.lean"
        path.write_text(fixture, encoding="utf-8")
        return subprocess.run(
            ["lake", "env", "lean", str(path)],
            cwd=LEAN_ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["normative_profile"] == receipt["normative_profile"] == (
        "machine-theorem-assurance/1.0"
    )
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == receipt["execution_rank"] == RANK
    assert audit["base_revision"] == protocol["base_revision"] == receipt["base_revision"] == (
        BASE_REVISION
    )
    assert audit["base_tree"] == protocol["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == RANK
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    statement_item = next(row for row in execution["items"] if row["id"] == "S56-M-0841-STATEMENT")
    assert statement_item["state"] == "[_]"
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert (item["phase"], item["layer"], item["state"]) == ("anchor_audit", 2, "[ ]")
    assert item["depends_on"] == ["S56-M-0841-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    canonical = audit["canonical_target"]
    formal = statement["canonical_formal_target"]
    assert canonical["declaration"] == formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0841.ErdosStoneTarget"
    )
    assert canonical["expression_sha256"] == formal["elaborated_expression_sha256"] == (
        EXPRESSION_SHA256
    )
    assert canonical["statement_file_sha256"] == sha256(HERE / "Statement.lean") == (
        STATEMENT_SHA256
    )
    assert protocol["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert protocol["frozen_before_candidate_classification"] is True
    assert protocol["saturation_claim"] is audit["discovery_protocol"]["saturation_claim"] is False

    environment = audit["immutable_environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == environment["lake_manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == environment["lean_toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == environment["mathlib_license_sha256"]

    candidates = {row["candidate_id"]: row for row in audit["candidates"]}
    assert set(candidates) == set(protocol["inventory_members"])
    assert set(candidates) == {
        "M0841-C01-LOCAL-STATEMENT",
        "M0841-C02-PINNED-MATHLIB-SUPPORT",
        "M0841-C03-POST-PIN-MATHLIB-MIN-DEGREE",
        "M0841-C04-EXTERNAL-DENSE-FIXED-PART",
        "M0841-C05-PUBLIC-SEARCH-NEGATIVE",
    }
    assert all(row["candidate_classification"] in {
        "M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"
    } for row in candidates.values())

    pinned = candidates["M0841-C02-PINNED-MATHLIB-SUPPORT"]
    assert pinned["revision"] == MATHLIB_REVISION and pinned["tree"] == MATHLIB_TREE
    assert pinned["candidate_classification"] == "M3"
    files = {row["path"]: row for row in pinned["files"]}
    assert files[COMPLETE_FILE] == {
        "path": COMPLETE_FILE, "blob": COMPLETE_BLOB, "sha256": COMPLETE_SHA256
    }
    assert files[DENSITY_FILE] == {
        "path": DENSITY_FILE, "blob": DENSITY_BLOB, "sha256": DENSITY_SHA256
    }
    for relative, blob, digest in (
        (COMPLETE_FILE, COMPLETE_BLOB, COMPLETE_SHA256),
        (DENSITY_FILE, DENSITY_BLOB, DENSITY_SHA256),
    ):
        assert output("git", "rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / relative) == digest

    later = candidates["M0841-C03-POST-PIN-MATHLIB-MIN-DEGREE"]
    assert later["revision"] == POST_PIN_REVISION and later["tree"] == POST_PIN_TREE
    assert later["file_blob"] == POST_PIN_BLOB and later["file_sha256"] == POST_PIN_SHA256
    assert later["toolchain"] == "leanprover/lean4:v4.32.0-rc1"
    assert later["lake_manifest_sha256"] == (
        "e3aa6c216d1606e4c0e3a94d5a017cacf871019fc39eea8100f1155149649af5"
    )
    assert later["license"] == "Apache-2.0"
    assert later["license_sha256"] == environment["mathlib_license_sha256"]
    assert "bounded scan" in later["placeholder_boundary"]
    assert "Not importable" in later["dependency_feasibility"]
    assert output("git", "rev-parse", f"{POST_PIN_REVISION}^{{tree}}", cwd=MATHLIB) == POST_PIN_TREE
    assert output("git", "rev-parse", f"{POST_PIN_REVISION}:{POST_PIN_FILE}", cwd=MATHLIB) == (
        POST_PIN_BLOB
    )
    later_source = subprocess.check_output(
        ["git", "show", f"{POST_PIN_REVISION}:{POST_PIN_FILE}"], cwd=MATHLIB
    )
    assert sha256_bytes(later_source) == POST_PIN_SHA256
    assert sha256_bytes(subprocess.check_output(
        ["git", "show", f"{POST_PIN_REVISION}:lake-manifest.json"], cwd=MATHLIB
    )) == later["lake_manifest_sha256"]
    assert sha256_bytes(subprocess.check_output(
        ["git", "show", f"{POST_PIN_REVISION}:LICENSE"], cwd=MATHLIB
    )) == later["license_sha256"]
    assert subprocess.check_output(
        ["git", "show", f"{POST_PIN_REVISION}:lean-toolchain"], cwd=MATHLIB, text=True
    ).strip() == later["toolchain"]
    post_pin_forbidden = re.compile(
        rb"\b(?:sorry|admit|sorryAx|axiom|opaque|unsafe|native_decide|implemented_by|extern)\b"
    )
    assert post_pin_forbidden.search(later_source) is None
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", POST_PIN_REVISION, MATHLIB_REVISION],
        cwd=MATHLIB,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert ancestor.returncode == 1
    absent = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{POST_PIN_FILE}"],
        cwd=MATHLIB,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert absent.returncode != 0
    assert later["candidate_classification"] == "M5"

    external = candidates["M0841-C04-EXTERNAL-DENSE-FIXED-PART"]
    assert external["revision"] == EXTERNAL_REVISION and external["tree"] == EXTERNAL_TREE
    assert external["archive_sha256"] == EXTERNAL_ARCHIVE_SHA256
    assert external["file_sha256"] == EXTERNAL_SOURCE_SHA256
    assert external["toolchain"] == "leanprover/lean4:v4.16.0-rc2"
    assert external["mathlib_revision"] == "15f16b1ec50f425147926be1aede7b4baa725380"
    assert external["candidate_classification"] == "M5"
    assert "growing" in external["normalized_match"]
    assert "Do not integrate" in external["integration_decision"]

    searches = {row["surface"]: row for row in audit["search_results"]}
    assert searches["repository-local Lean source"]["result"].startswith("11 hits")
    assert searches["repository-local Lean source"]["normalized_output_sha256"] == (
        LOCAL_SEARCH_SHA256
    )
    assert searches["pinned mathlib source"]["normalized_output_sha256"] == hashlib.sha256(
        b""
    ).hexdigest()
    assert searches["other installed pinned packages"]["normalized_output_sha256"] == (
        hashlib.sha256(b"").hexdigest()
    )
    assert searches["Sourcegraph"]["response_sha256"] == SOURCEGRAPH_RESPONSE_SHA256

    anchor = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    required_markers = (
        "def ExactTarget : Prop",
        "SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ",
        "#check SimpleGraph.eventually_isContained_of_card_edgeFinset",
        "#check_failure SimpleGraph.eventually_completeEquipartiteGraph_isContained_of_minDegree",
        "#check_failure SimpleGraph.ErdosStone.filter",
        "assert_no_sorry SimpleGraph.eventually_isContained_of_card_edgeFinset",
        "#print axioms SimpleGraph.isContained_of_card_edgeFinset",
    )
    assert all(marker in anchor for marker in required_markers)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|implemented_by|native_decide)\b"
    )
    assert forbidden.search(without_comments_and_strings(anchor)) is None

    lean = run_lean()
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor Lean output hash changed")
    # `assert_no_sorry` is a silent assertion in this pinned mathlib version.
    # Reaching the following output and exit zero establishes that all five commands passed.
    assert lean.stdout.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 5
    assert "Unknown constant `SimpleGraph.eventually_completeEquipartiteGraph_isContained_of_minDegree`" in lean.stdout
    assert "Unknown constant `SimpleGraph.ErdosStone.filter`" in lean.stdout
    assert "sorryAx" not in lean.stdout

    equivalence = run_canonical_equivalence_fixture()
    if equivalence.returncode:
        sys.stdout.write(equivalence.stdout)
        raise SystemExit(equivalence.returncode)
    normalized_equivalence = re.sub(r"\s+", " ", equivalence.stdout)
    assert (
        "'Stage1Instances.THM_M_0841_AnchorAudit.canonicalTarget_eq_auditTarget' "
        "depends on axioms: [propext, Classical.choice, Quot.sound]"
    ) in normalized_equivalence
    assert "declaration uses 'sorry'" not in equivalence.stdout
    assert "sorryAx" not in equivalence.stdout

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["exact_candidate_located"] is result["candidate_kernel_checked"] is False
    assert result["support_interfaces_kernel_checked"] is True
    assert result["root_machine_debt_before"] == result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert audit["root_vector_before"] == audit["root_candidate_vector_after"] == vector
    assert audit["accepted_root_vector_after"] == vector
    assert audit["audit_complete"] is audit["theorem_complete"] is False
    assert audit["accepted_receipt_ids"] == []

    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["exact_candidate_found"] is False
    assert receipt["candidate_result"]["classification"] == "M3"
    assert receipt["candidate_result"]["kernel_checked_support"] is True
    assert receipt["candidate_result"]["root_kernel_checked"] is False
    assert receipt["inventory_result"]["classified_candidate_groups"] == 5
    assert receipt["inventory_result"]["exact_terminal_proof_bodies"] == 0
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["root_vector_before"] == receipt["root_candidate_vector_after"] == vector
    assert receipt["accepted_root_vector_after"] == vector
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_or_receipt_ids"] == []
    for relative, tagged in receipt["source_inputs"].items():
        algorithm, digest = tagged.split(":", 1)
        assert algorithm == "sha256" and sha256(ROOT / relative) == digest, relative
    assert receipt["artifact_hashes"] == {
        "AnchorAudit.lean": f"sha256:{sha256(HERE / 'AnchorAudit.lean')}",
        "anchor-audit.json": f"sha256:{sha256(HERE / 'anchor-audit.json')}",
        "anchor-audit-validation.md": f"sha256:{sha256(HERE / 'anchor-audit-validation.md')}",
        "anchor-discovery-protocol.json": (
            f"sha256:{sha256(HERE / 'anchor-discovery-protocol.json')}"
        ),
        "check_anchor_audit.py": f"sha256:{sha256(Path(__file__))}",
    }

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["commands"] == receipt["worker_packet_commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "check_anchor_audit: ok "
        "(THM-M-0841; 5 candidate groups classified; no exact candidate; "
        "pinned support probe passed; root H1/M3/R4; "
        "audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
