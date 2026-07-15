#!/usr/bin/env python3
"""Fail-closed packet checks for the partial THM-M-0996 proof work."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0996-PROOF"
THEOREM = "THM-M-0996"
BASE_REVISION = "718e166c56e53c552ebb861ee01427f9a606fc72"
BASE_TREE = "f2e15921b967c6f80b9e964361b684b5f9a011d9"
STATEMENT_SHA256 = "cdecb06daf3ca5cbc2b6f8f5def0a82fb3fc712695fdd5c2a047189d683edd14"
DENOMINATOR_SHA256 = "8d3affee638ef1cc6e3fbb2ee9d52fc76212b0a91327f7b42ecba1b4ae8b6e9e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SUPPORTED_IDS = [
    "M0996-N-PROFILE",
    "M0996-N-COORD",
    "M0996-B-DIM",
    "M0996-C-HALFSPACE",
    "M0996-L-HALFSPACE",
    "M0996-T-ASSEMBLE",
]
PARTIAL_PROGRESS_IDS = SUPPORTED_IDS.copy()
AUTHORITATIVE_CUT = ["M0996-L-HALFSPACE", "M0996-L-GENERAL"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-attempt.md",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
HISTORY_SUFFIX = """\n## Current worker supersession

The historical record above is preserved byte-for-byte. At base revision
`718e166c56e53c552ebb861ee01427f9a606fc72`, the current worker added further
placeholder-free proof bodies and an isolated module-chain replay. The new
work is recorded separately in `proof-validation.md`, `proof-receipt.json`,
and `proof-blocker.json`.

This supersession changes only the scope of self-tested partial progress. It
does not retroactively alter the original result, close any frozen obligation,
or prove the canonical root. The remaining root cut is still
`M0996-L-HALFSPACE` and `M0996-L-GENERAL`, and theorem completion remains
false.
"""


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_source_patch_sha256() -> str:
    paths = [
        f"Stage1_Instances/{THEOREM}/ObligationTree.lean",
        f"Stage1_Instances/{THEOREM}/Proof.lean",
        f"Stage1_Instances/{THEOREM}/proof-attempt.md",
    ]
    patch = subprocess.check_output(
        ["git", "diff", "--binary", BASE_REVISION, "--", *paths], cwd=ROOT)
    return hashlib.sha256(patch).hexdigest()


def git(*args: str, cwd: Path = ROOT, binary: bool = False):
    return subprocess.check_output(["git", *args], cwd=cwd, text=not binary)


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def printed_declarations(source: str) -> list[str]:
    values = re.findall(r"^#print axioms\s+(\S+)\s*$", source, re.MULTILINE)
    assert values and len(values) == len(set(values))
    return values


def main() -> None:
    statement_path = HERE / "Statement.lean"
    tree_path = HERE / "ObligationTree.lean"
    proof_path = HERE / "Proof.lean"
    statement = statement_path.read_text(encoding="utf-8")
    tree = tree_path.read_text(encoding="utf-8")
    proof = proof_path.read_text(encoding="utf-8")
    tree_declarations = printed_declarations(tree)
    proof_declarations = printed_declarations(proof)
    checked_declarations = tree_declarations + proof_declarations
    assert len(tree_declarations) == 1 and len(proof_declarations) == 34

    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    anchor = load(HERE / "anchor-audit.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    subprocess.check_call(
        ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"], cwd=ROOT)
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}").strip() == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 276
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0996-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders.")
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    predecessor = next(row for row in execution["items"]
                       if row["id"] == "S56-M-0996-OBLIGATION_TREE")
    assert predecessor["state"] in {"[_]", "[x]"}

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    for source in (statement, tree, proof):
        assert prohibited.search(without_comments(source)) is None
    assert tree.startswith('import «Stage1_Instances».«THM-M-0996».Statement\n')
    assert proof.startswith('import «Stage1_Instances».«THM-M-0996».ObligationTree\n')
    assert "import Mathlib.Probability.CDF\n" in proof[:200]
    for source in (tree, proof):
        assert not re.search(r"^def (?:IsUnitHalfspace|GaussianIsoperimetricTarget)\b", source,
                             re.MULTILINE)
    for declaration in checked_declarations:
        short = declaration.rsplit(".", 1)[-1]
        source = tree if declaration in tree_declarations else proof
        assert re.search(rf"\b(?:theorem|def) {re.escape(short)}\b", source), short
    for fragment in (
        "theorem coordEquiv_image_isUnitHalfspace",
        "theorem coordEquiv_unitHalfspace_profile_formula",
        "theorem continuous_stdGaussianReal_Iic",
        "theorem stdGaussianReal_Iic_surjective_Ioo",
        "theorem stdGaussianReal_Iic_range",
        "theorem halfspaceEnlargementFormula",
        "theorem target_of_generalSetEnlargementBound",
        "exact target_of_profile_bounds halfspaceProfile halfspaceEnlargementFormula hGeneral",
    ):
        assert fragment in proof, fragment

    assert sha256(statement_path) == STATEMENT_SHA256
    assert registry["root_obligation_id"] == "M0996-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    denominator = hashlib.sha256(json.dumps(registry["frozen_denominators"],
        sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert denominator == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    fingerprints = {oid: by_id[oid]["statement_fingerprint"] for oid in SUPPORTED_IDS}
    assert all(value.startswith("planned:v1:sha256:") for value in fingerprints.values())
    assert all(by_id[oid]["terminal_proof_body_id"] is None
               for oid in set(SUPPORTED_IDS) - {"M0996-T-ASSEMBLE"})
    assert by_id["M0996-T-ASSEMBLE"]["terminal_proof_body_id"] == (
        "local:Stage1Instances.THM_M_0996.target_of_profile_bounds")
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [],
        "conditionally_checked_compositions": ["M0996-T-ASSEMBLE"],
        "root_machine_debt": "M3",
    }
    assert graphs["remaining_root_cut_set"] == AUTHORITATIVE_CUT
    assert graphs["theorem_complete"] is False
    edges = {(edge["from"], edge["type"], edge["to"])
             for edge in graphs["graphs"]["proof"]["edges"]}
    for edge in (
        ("M0996-L-HALFSPACE", "proof_requires", "M0996-C-HALFSPACE"),
        ("M0996-L-HALFSPACE", "proof_requires", "M0996-N-PROFILE"),
        ("M0996-C-HALFSPACE", "proof_requires", "M0996-N-COORD"),
    ):
        assert edge in edges

    assert anchor["exact_root_candidate"] is None
    assert anchor["source_body_provenance"].endswith(
        "No external proof body was imported or credited.")
    assert anchor["repository_searches"]["github_repository_result"].startswith(
        "both GitHub REST repository searches returned total_count 0")
    current_evidence = "\n".join((json.dumps(receipt), json.dumps(blocker),
        (HERE / "proof-validation.md").read_text(encoding="utf-8")))
    assert re.search(r"\b(?:Atlas|LSLT)\b", current_evidence) is None

    history = (HERE / "proof-attempt.md").read_bytes()
    historical = git(
        "show", f"{BASE_REVISION}:Stage1_Instances/{THEOREM}/proof-attempt.md", binary=True)
    assert history == historical + HISTORY_SUFFIX.encode()

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib).strip() == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib).strip() == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib).strip() == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == blocker["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["exact_declarations"] == checked_declarations
    assert receipt["supported_obligation_ids"] == blocker["supported_obligation_ids"] == SUPPORTED_IDS
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["obligation_statement_fingerprints"] == fingerprints
    assert blocker["obligation_statement_fingerprints"] == fingerprints
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert blocker["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == blocker["accepted_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["nonrelease_worktree"]["tracked_source_patch_sha256"] == (
        tracked_source_patch_sha256())
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_attempt_sha256", "proof-attempt.md"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["tree_checked_declaration_count"] == len(tree_declarations)
    assert receipt["result"]["proof_checked_declaration_count"] == len(proof_declarations)
    assert receipt["result"]["checked_declaration_count"] == len(checked_declarations)
    replay = receipt["result"]["replay_hashes"]
    assert replay["statement_source_sha256"] == sha256(statement_path)
    assert replay["obligation_tree_source_sha256"] == sha256(tree_path)
    assert replay["proof_source_sha256"] == sha256(proof_path)
    assert set(replay) == {
        "statement_source_sha256", "obligation_tree_source_sha256",
        "proof_source_sha256", "statement_output_sha256",
        "obligation_tree_output_sha256", "proof_output_sha256",
        "statement_olean_sha256", "obligation_tree_olean_sha256",
        "proof_olean_sha256",
    }
    assert all(re.fullmatch(r"[0-9a-f]{64}", value) for value in replay.values())
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["authoritative_graph_open_cut_set_unchanged"] == AUTHORITATIVE_CUT
    assert blocker["authoritative_graph_open_cut_set_unchanged"] == AUTHORITATIVE_CUT
    assert "provisional_mathematical_remaining_cut" not in receipt
    assert "provisional_mathematical_remaining_cut" not in blocker
    assert receipt["predecessor_evidence"]["status"] == "stale_re_review_required"
    assert blocker["predecessor_evidence"]["status"] == "stale_re_review_required"
    assert receipt["predecessor_evidence"]["accepted"] is False
    assert receipt["validated_at"] == blocker["recorded_at"]

    if packet is not None:
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary",
                               "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM
        assert packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

        # These freshness/worktree checks are intentionally worker-only. An integration
        # commit has different mtimes and no longer carries the root handoff packet.
        recorded_ns = int(datetime.fromisoformat(receipt["validated_at"]).timestamp()
                          * 1_000_000_000)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean",
                         "check_proof.py", "check_proof.sh", "proof-attempt.md",
                         "proof-validation.md", "proof-blocker.json"):
            assert (HERE / filename).stat().st_mtime_ns <= recorded_ns, filename
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True)
        actual_changed = {line[3:] for line in status.splitlines()
                          if line[3:] != "Formalizations/Lean/.lake"}
        assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    normalized_validation = re.sub(r"\s+", " ", validation)
    for fragment in ("34 proof declarations", "one obligation-tree declaration",
                     "M0996-L-HALFSPACE", "M0996-L-GENERAL", "theorem_complete=false",
                     "No frozen obligation is provisionally closed"):
        assert fragment in normalized_validation, fragment
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        if not relative.endswith("/proof-attempt.md"):
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0996 proof packet: 35 declarations and evidence checked")
    print("provisional closures: none; frozen fingerprints remain planned:v1")
    print("root open at M3; authoritative cut: M0996-L-HALFSPACE, M0996-L-GENERAL")
    print("predecessor evidence stale; re-review required; theorem_complete=false")


if __name__ == "__main__":
    main()
