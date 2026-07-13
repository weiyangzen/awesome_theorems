#!/usr/bin/env python3
"""Validate the immutable THM-M-0484 formal-anchor inventory and Lean probe."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
IMPORT_GRAPH = LEAN_ROOT / ".lake" / "packages" / "importGraph"
ITEM_ID = "S56-M-0484-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0484"
BASE_REVISION = "0c019b7194c9c43fa5f683fa82d637a0b275410d"
BASE_TREE = "43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
STATEMENT_SHA256 = "1baec8791288b46d6df61e060be07aa190ac1d0424229595523a095e8259c8dc"
ANCHOR_LEAN_SHA256 = "4337a2be005548dfe1686eca077c476138c3747c039c367eb9b56e2b9d36d717"
LEAN_OUTPUT_SHA256 = "4a27ad95b27c0cb355d434571d69fd7323c20fa9008c256e7a26257609207c37"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
    f"Stage1_Instances/{THEOREM_ID}/check_statement_artifacts.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def run(*args: str, cwd: Path = ROOT, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def tagged_sha256(path: Path) -> str:
    return f"sha256:{sha256(path)}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1365
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1365
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0484-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert sha256(HERE / "AnchorAudit.lean") == ANCHOR_LEAN_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0484.LucasLehmerTestTarget"
    )
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert output("git", "rev-parse", "HEAD:LICENSE", cwd=MATHLIB) == env["mathlib_license_blob"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["toolchain_file_sha256"]
    olean = MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/LucasLehmer.olean"
    assert olean.is_file(), "pinned LucasLehmer olean is missing"
    assert sha256(olean) == env["compiled_module_sha256"]
    assert olean.stat().st_size == env["compiled_module_bytes"]
    assert output("git", "rev-parse", "HEAD", cwd=IMPORT_GRAPH) == env["import_graph_revision"]
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=IMPORT_GRAPH) == env["import_graph_tree"]
    assert output("git", "status", "--short", cwd=IMPORT_GRAPH) == ""
    required_modules = IMPORT_GRAPH / "ImportGraph/Imports/RequiredModules.lean"
    assert output(
        "git", "rev-parse", "HEAD:ImportGraph/Imports/RequiredModules.lean", cwd=IMPORT_GRAPH
    ) == env["import_graph_required_modules_blob"]
    assert sha256(required_modules) == env["import_graph_required_modules_sha256"]
    assert output("git", "rev-parse", "HEAD:LICENSE", cwd=IMPORT_GRAPH) == env["import_graph_license_blob"]
    assert sha256(IMPORT_GRAPH / "LICENSE") == env["import_graph_license_sha256"]

    candidates = audit["candidates"]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    assert len(candidate_ids) == len(set(candidate_ids)) == 8
    direct = next(
        candidate
        for candidate in candidates
        if candidate["candidate_id"] == "M0484-C01-MATHLIB-EXACT-COMPOSITION"
    )
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output(
        "git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB
    )
    source_path = MATHLIB / direct["file"]
    assert sha256(source_path) == direct["file_sha256"]
    assert source_path.stat().st_size == direct["file_bytes"]
    source_bytes = source_path.read_bytes().splitlines(keepends=True)
    assert sha256_bytes(b"".join(source_bytes[580:591])) == direct["terminal_proof_body_ids"][0].split(":", 1)[1]
    assert sha256_bytes(b"".join(source_bytes[592:608])) == direct["terminal_proof_body_ids"][1].split(":", 1)[1]
    assert sha256_bytes(b"".join(source_bytes[580:608])) == direct["combined_terminal_slice_sha256"]
    definition_slice = (
        b"".join(source_bytes[36:39])
        + b"".join(source_bytes[151:165])
        + b"".join(source_bytes[193:218])
    )
    assert sha256_bytes(definition_slice) == direct["definition_slice_sha256"]

    source = source_path.read_text(encoding="utf-8")
    for marker in (
        "def mersenne (p : ℕ) : ℕ",
        "def LucasLehmerTest (p : ℕ) : Prop",
        "theorem lucas_lehmer_sufficiency",
        "theorem lucas_lehmer_necessity",
        "have h₁ := order_ineq p' t",
        "have h₂ := Nat.minFac_sq_le_self",
        "have := X.ω_pow_trace",
        "(legendreSym_mersenne_three w",
        "(legendreSym_mersenne_two w)",
    ):
        assert marker in source, marker

    history = direct["historical_provenance"]
    for prefix in ("lean4_sufficiency_port", "necessity_introduction"):
        commit = history[f"{prefix}_commit"]
        assert history[f"{prefix}_tree"] == output(
            "git", "rev-parse", f"{commit}^{{tree}}", cwd=MATHLIB
        )
        assert history[f"{prefix}_blob"] == output(
            "git", "rev-parse", f"{commit}:{direct['file']}", cwd=MATHLIB
        )
        historic = subprocess.check_output(
            ["git", "show", f"{commit}:{direct['file']}"], cwd=MATHLIB
        )
        assert sha256_bytes(historic) == history[f"{prefix}_source_sha256"]
        assert run(
            "git", "merge-base", "--is-ancestor", commit, MATHLIB_REVISION, cwd=MATHLIB
        ).returncode == 0

    archive = next(c for c in candidates if c["candidate_id"] == "M0484-C03-MATHLIB-ARCHIVE-EXAMPLES")
    archive_path = MATHLIB / archive["file"]
    assert archive["file_blob"] == output(
        "git", "rev-parse", f"HEAD:{archive['file']}", cwd=MATHLIB
    )
    assert sha256(archive_path) == archive["file_sha256"]
    archive_source = archive_path.read_text(encoding="utf-8")
    assert "example : ¬ LucasLehmerTest 2" in archive_source
    assert "example : (mersenne 2).Prime" in archive_source

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall p : Nat, 3 <= p ->",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "exact lucas_lehmer_sufficiency p (by omega)",
        "exact lucas_lehmer_necessity p hp",
        "assert_no_sorry lucas_lehmer_sufficiency",
        "#print sorries lucas_lehmer_sufficiency lucas_lehmer_necessity",
        "NameSet.transitivelyUsedConstants",
        "ANCHOR_CLOSURE bodyless_nonaxioms=",
        "ANCHOR_CLOSURE unsafe=",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|extern|proof_wanted)\b|"
        r"^\s*(?:axiom|constant|unsafe|opaque)\b",
        re.MULTILINE,
    )
    adapter_code = without_comments(adapter)
    adapter_code = re.sub(r"^.*(?:assert_no_sorry|#print sorries).*$", "", adapter_code, flags=re.MULTILINE)
    adapter_code = re.sub(r'^.*"ANCHOR_CLOSURE (?:bodyless_nonaxioms|unsafe)=.*$', "", adapter_code, flags=re.MULTILINE)
    assert not forbidden.search(adapter_code)
    terminal_code = without_comments("".join(line.decode() for line in source_bytes[580:608]))
    assert not forbidden.search(terminal_code)

    search = audit["search_evidence"]
    assert search["pinned_mathlib"]["lean_files"] == 8374
    assert search["pinned_mathlib"]["lucas_query_matching_lines"] == 81
    assert search["pinned_mathlib"]["mersenne_query_matching_lines"] == 133
    assert search["repository_local"]["tracked_lean_files"] == 2281
    assert search["repository_local"]["matching_lines"] == 44
    assert all(row["http_status"] == 200 and row["done"] for row in search["sourcegraph_queries"])
    assert all(row["skipped"] == [] for row in search["sourcegraph_queries"])
    assert all(row["match_count"] == 0 for row in search["formal_conjectures_queries"])
    assert audit["discovery_protocol"]["saturation_claim"] is False

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("8/8 frozen candidates")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2_nonrelease_worker_probe"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["statement_fingerprints"] == [f"sha256:{EXPRESSION_SHA256}"]
    assert receipt["statement_file_sha256"] == STATEMENT_SHA256
    assert receipt["anchor_audit_lean_sha256"] == f"sha256:{ANCHOR_LEAN_SHA256}"
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2_nonrelease_worker_probe"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["candidate_result"]["bodyless_nonaxioms"] == []
    assert receipt["candidate_result"]["unsafe_declarations"] == []
    assert receipt["root_vector_before"] == receipt["accepted_root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4",
    }
    assert receipt["root_candidate_vector_after"] == {"H": "H1", "M": "M0-W", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == tagged_sha256(ROOT / relative), f"stale source input: {relative}"

    lean = run(
        "lake", "env", "lean", "--trust=0",
        "../../Stage1_Instances/THM-M-0484/AnchorAudit.lean",
        cwd=LEAN_ROOT,
        timeout=180,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("propext, Classical.choice, Quot.sound") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal/wrapper or closure axiom report")
    required_output = (
        "Declarations are sorry-free!",
        "mp :=",
        "lucas_lehmer_sufficiency p",
        "mpr := lucas_lehmer_necessity p hp",
        "ANCHOR_CLOSURE declarations=35389 modules=1243",
        "ANCHOR_CLOSURE bodyless_nonaxioms=[]",
        "ANCHOR_CLOSURE unsafe=[]",
    )
    for marker in required_output:
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean output marker: {marker}")
    explicit = re.search(
        r"def Stage1Instances\.THM_M_0484\.AnchorAudit\.ExactTarget : Prop :=\n"
        r"(?P<expression>.*)\Z",
        lean.stdout,
        re.DOTALL,
    )
    if explicit is None:
        sys.stdout.write(lean.stdout)
        raise SystemExit("could not extract audit target expression")
    expected_expression = (
        "∀ (p : Nat), @LE.le.{0} Nat instLENat (@OfNat.ofNat.{0} Nat (nat_lit 3) "
        "(instOfNatNat (nat_lit 3))) p → Iff (LucasLehmerTest p) (Nat.Prime (mersenne p))"
    )
    if " ".join(explicit.group("expression").split()) != expected_expression:
        sys.stdout.write(lean.stdout)
        raise SystemExit("audit target differs from the frozen fully explicit expression")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    actual_changed = {".stage1-worker-selftest.json"}
    status = output(
        "git", "status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE)
    )
    for line in status.splitlines():
        relative = line[3:] if line[:2] == "??" else line[2:].lstrip()
        if not relative.startswith(f"Stage1_Instances/{THEOREM_ID}/"):
            raise SystemExit(f"out-of-scope changed path: {relative}")
        actual_changed.add(relative)
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

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
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "check_anchor_audit: ok "
        "(THM-M-0484; 8 candidates classified; exact pinned mathlib composition "
        "M0-W/E2 nonrelease; accepted root remains M3; audit_complete=false; "
        "theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
