#!/usr/bin/env python3
"""Fail-closed evidence checks for the THM-M-0711 partial proof phase."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0711-PROOF"
THEOREM = "THM-M-0711"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
STATEMENT_SHA256 = "624dd9575960ac9d10b05c677f744c333edc7b162ddda57cafa251642b803436"
DENOMINATOR_SHA256 = "9fbdae321a68e51a301e942864c9a785fab407f21f25247ab04cb74277bd8d24"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CLOSED = ["M0711-N-QUOTIENT", "M0711-L-HALTING", "M0711-L-MANYONE"]
PARTIAL = ["M0711-L-NONCOMP", "M0711-T-WITNESS", "M0711-ROOT"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
    f"Stage1_Instances/{THEOREM}/validation.md",
}


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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("diff", "--name-only", f"{BASE_REVISION}..HEAD") == ""
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 751
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0711-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0711-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import Mathlib.Computability.Reduce",
        "import Mathlib.Util.AssertNoSorry",
        "import Mathlib.Util.PrintSorries",
        "import ObligationTree",
        "theorem identityPred_iff_normalClosure",
        "PresentedGroup.mk_eq_one_iff",
        "theorem not_computablePred_of_manyOneReducible",
        "ComputablePred.computable_of_manyOneReducible hred htarget",
        "theorem haltingPredicate_not_computable",
        "ComputablePred.halting_problem input",
        "theorem fixedPresentationUndecidable_of_haltingReduction",
        "theorem novikovBooneTarget_of_haltingReduction",
        "assert_no_sorry ComputablePred.halting_problem",
        "#print sorries ComputablePred.halting_problem",
        "#print axioms ComputablePred.halting_problem",
    ):
        assert marker in proof, marker
    assert "theorem novikovBooneTarget :" not in proof

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    computed_denominator = hashlib.sha256(
        json.dumps(
            [{key: row[key] for key in fields} for row in registry["obligations"]],
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    assert computed_denominator == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    expected_fingerprints = {
        obligation_id: by_id[obligation_id]["statement_fingerprint"]
        for obligation_id in CLOSED + PARTIAL
    }
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M0711-B-REDUCTION", "M0711-S-FOUNDATION"],
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_source_sha256"] == STATEMENT_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["obligation_statement_fingerprints"] == expected_fingerprints
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["provisionally_closed_obligation_ids"] == CLOSED
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL
    assert receipt["accepted_closed_obligation_ids"] == []
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit-receipt.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    pinned_by_file = {row["file"]: row for row in receipt["pinned_sources"]}
    expected_oleans = {
        "Mathlib/GroupTheory/PresentedGroup.lean": (
            "Mathlib/GroupTheory/PresentedGroup.olean",
            "f8a8ba929e4756ab166577dc356c36de35a024b3feae622c54a7762cb1e2080b",
        ),
        "Mathlib/Computability/Reduce.lean": (
            "Mathlib/Computability/Reduce.olean",
            "ed05cc633a618b11db47fafc0daa6333c804d18e5114d7013c0cda9259c33dfe",
        ),
        "Mathlib/Computability/Halting.lean": (
            "Mathlib/Computability/Halting.olean",
            "a4d0f485725fd93028f52418d4c5b6251cbd59cececed2b4ff1f4ac5578a61ba",
        ),
    }

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["provisionally_closed_obligation_ids"] == CLOSED
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    expected_sources = {
        "Mathlib/GroupTheory/PresentedGroup.lean": (
            "8197660a6783c139ff5c5583e34792f148819e0e",
            "4226ec95821cd97aaf33a5fd22d3c58dd3b8de4cd3c46e4b8b92e232b77297a9",
        ),
        "Mathlib/Computability/Reduce.lean": (
            "aa5487c021cfdb4c7644efdd30ec5eb9dc0775bb",
            "30513e477c461fdce1518542f4dc16085f1d98ab47ba2bfbc28d5b741b18e556",
        ),
        "Mathlib/Computability/Halting.lean": (
            "0834371356762db805d37208b9cf8a1fc0efd217",
            "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de",
        ),
    }
    for path, (blob, digest) in expected_sources.items():
        assert git("rev-parse", f"HEAD:{path}", cwd=mathlib) == blob
        assert sha256(mathlib / path) == digest
        assert pinned_by_file[path]["git_blob"] == blob
        assert pinned_by_file[path]["source_sha256"] == digest
        olean_path, olean_digest = expected_oleans[path]
        assert sha256(mathlib / ".lake/build/lib/lean" / olean_path) == olean_digest
        assert pinned_by_file[path]["olean_sha256"] == olean_digest

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git(
        "status", "--short", "--untracked-files=all", "--",
        f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
    )
    actual_changes = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    tracked_changes = {
        path for path in git("diff", "--name-only", "--", f"Stage1_Instances/{THEOREM}").splitlines()
        if path
    }
    expected_tracked = {
        path for path in CHANGED_PATHS if path in git("ls-files").splitlines()
    }
    assert tracked_changes == expected_tracked, (tracked_changes, expected_tracked)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "not an unconditional witness or root proof" in validation
    assert "root stays `[H1, M4, R4]`" in validation
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0711 partial proof: quotient, halting, and transfer bodies checked")
    print("root closure: open (M4); finite-presentation reduction remains unimplemented")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
