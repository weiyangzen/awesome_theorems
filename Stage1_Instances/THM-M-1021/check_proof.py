#!/usr/bin/env python3
"""Fail-closed structural and provenance checks for S56-M-1021-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1021-PROOF"
THEOREM = "THM-M-1021"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
STATEMENT_EXPRESSION = "5b397ee9de0936db2c62ba953794ee0c2b9dc3192370aa06825fdf4aafc8322b"
REGISTRY_DENOMINATOR = "032b467a59ae30caf2d637b9707358e6ba7259edf774ba0bd8bf162e48924688"
UPSTREAM_REVISION = "1b56973aff9b4e6ba761a6bd8af678e38bfd8d10"
UPSTREAM_TREE = "a031b68a944a46488384ba01ac386e1b17dc242d"
UPSTREAM_POSITIVE_DEFINITE = "2f5e07e86773b57551203b3556057a2ee3dd842b627474a76c3ec98c0c74bff2"
UPSTREAM_FEJER = "503f9aaeb17becd77b5f986ebc82a3c17abcce79fd7568d3fcd66524ef352f24"
UPSTREAM_MAIN = "5a23ba46df0866f33eae31354b659f194e5ebc1a26fd47cd92f838658b278d3b"
LOCAL_POSITIVE_DEFINITE = "2f5e07e86773b57551203b3556057a2ee3dd842b627474a76c3ec98c0c74bff2"
LOCAL_FEJER = "a4bc1a1d3a6dc67f02f9afe8b09507131780fc2e4e94f9c0940170e264423a2c"
LOCAL_MAIN = "9ab4cd83b1694d98059ec4b6cb7b57a56e1d6798f7609938b1939a2a0788cbd0"
LICENSE_SHA256 = "8ebdd6164d5245aba45342f898b1a9f1c1509246a22fdf3002a66bbbe5d70089"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"

CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/External/Bochner/FejerPD.lean",
    f"Stage1_Instances/{THEOREM}/External/Bochner/Main.lean",
    f"Stage1_Instances/{THEOREM}/External/Bochner/PositiveDefinite.lean",
    f"Stage1_Instances/{THEOREM}/External/LICENSE",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/ProofAudit.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}

WITHHELD_ROUTE_IDS = [
    "M1021-BR",
    "M1021-C",
    "M1021-C1",
    "M1021-C1.1",
    "M1021-C1.2",
    "M1021-C2",
    "M1021-C2.1",
    "M1021-C2.2",
    "M1021-C3",
    "M1021-C3.1",
    "M1021-C3.2",
    "M1021-C4",
    "M1021-C5",
    "M1021-C5.1",
    "M1021-C5.2",
    "M1021-T2",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    """Remove nested Lean block comments and line comments for hygiene scans."""
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def main() -> None:
    if not __debug__:
        raise SystemExit("FAIL: Python assertions are disabled")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 497,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-1021-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }

    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert statement["canonical_declaration"] == (
        "AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget"
    )
    assert statement["elaborated_print_sha256"] == STATEMENT_EXPRESSION
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    obligation_fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
    }
    assert len(obligation_fingerprints) == 50
    assert registry["root_obligation_id"] == "M1021-ROOT"
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M1021-BR", "M1021-C"],
        "proof_claimed": False,
        "theorem_complete": False,
    }

    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    audit = (HERE / "ProofAudit.lean").read_text(encoding="utf-8")
    external_paths = [
        HERE / "External/Bochner/PositiveDefinite.lean",
        HERE / "External/Bochner/FejerPD.lean",
        HERE / "External/Bochner/Main.lean",
    ]
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|run_tac|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for path in [*external_paths, HERE / "Proof.lean", HERE / "ProofAudit.lean"]:
        executable = without_comments(path.read_text(encoding="utf-8"))
        assert prohibited.search(executable) is None, path

    for marker in (
        "import External.Bochner.Main",
        "theorem bochner_forward (phi : Real -> Complex)",
        "theorem bochner_reverse (phi : Real -> Complex)",
        "theorem bochner_exact (phi : Real -> Complex) : BochnerTarget phi := by",
        "exact bochner_forward phi",
        "exact bochner_reverse phi hcont hzero hpd",
        "#print axioms bochner_exact",
    ):
        assert marker in proof, marker
    for declaration in ("bochner_theorem", "bochner_forward", "bochner_reverse", "bochner_exact"):
        assert f"assert_no_sorry {declaration}" in audit or (
            f"assert_no_sorry AwesomeTheorems.Stage1.THM_M_1021.{declaration}" in audit
        )

    positive, fejer, main_source = (path.read_text(encoding="utf-8") for path in external_paths)
    assert sha256(external_paths[0]) == LOCAL_POSITIVE_DEFINITE
    assert sha256(external_paths[1]) == LOCAL_FEJER
    assert sha256(external_paths[2]) == LOCAL_MAIN
    assert digest_text(positive) == UPSTREAM_POSITIVE_DEFINITE
    assert fejer.count("import External.Bochner.PositiveDefinite") == 1
    reconstructed_fejer = fejer.replace(
        "import External.Bochner.PositiveDefinite", "import Bochner.PositiveDefinite"
    )
    assert digest_text(reconstructed_fejer) == UPSTREAM_FEJER
    assert main_source.count("import External.Bochner.PositiveDefinite") == 1
    assert main_source.count("import External.Bochner.FejerPD") == 1
    assert main_source.count(
        "The preceding characteristic-function bound makes the family tight."
    ) == 1
    reconstructed_main = main_source.replace(
        "import External.Bochner.PositiveDefinite", "import Bochner.PositiveDefinite"
    ).replace("import External.Bochner.FejerPD", "import Bochner.FejerPD").replace(
        "The preceding characteristic-function bound makes the family tight.",
        "The set of measures is tight (from axiom)",
    )
    assert digest_text(reconstructed_main) == UPSTREAM_MAIN
    assert sha256(HERE / "External/LICENSE") == LICENSE_SHA256

    manifest = load(ROOT / "Formalizations/Lean/lake-manifest.json")
    mathlib = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib["rev"] == MATHLIB_REVISION
    mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib_root) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib_root) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib_root) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "proof" and receipt["intent"] == "prove"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["obligation_statement_fingerprints"] == obligation_fingerprints
    assert receipt["closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["withheld_frozen_route_ids"] == WITHHELD_ROUTE_IDS
    assert receipt["root_evidence"]["root_kernel_declaration_closed"] is True
    assert receipt["root_evidence"]["frozen_graph_closed"] is False
    assert receipt["root_evidence"]["accepted_root_closed"] is False
    assert receipt["root_evidence"]["internal_per_node_composition_credit"] is False
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["placeholder_scan"] == "pass"
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["upstream"]["revision"] == UPSTREAM_REVISION
    assert receipt["upstream"]["tree"] == UPSTREAM_TREE
    assert receipt["upstream"]["source_sha256"] == {
        "Bochner/PositiveDefinite.lean": UPSTREAM_POSITIVE_DEFINITE,
        "Bochner/FejerPD.lean": UPSTREAM_FEJER,
        "Bochner/Main.lean": UPSTREAM_MAIN,
    }
    assert receipt["inputs"]["proof_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["inputs"]["proof_audit_sha256"] == sha256(HERE / "ProofAudit.lean")
    assert receipt["inputs"]["positive_definite_local_sha256"] == LOCAL_POSITIVE_DEFINITE
    assert receipt["inputs"]["fejer_local_sha256"] == LOCAL_FEJER
    assert receipt["inputs"]["main_local_sha256"] == LOCAL_MAIN
    assert receipt["inputs"]["license_sha256"] == LICENSE_SHA256
    for key, path in (
        ("statement_sha256", HERE / "BochnerStatement.lean"),
        ("statement_json_sha256", HERE / "statement.json"),
        ("obligation_tree_sha256", HERE / "obligation-tree.md"),
        ("obligation_registry_sha256", HERE / "obligation-registry.json"),
        ("typed_graphs_sha256", HERE / "typed-graphs.json"),
        ("anchor_audit_json_sha256", HERE / "anchor_audit.json"),
        ("check_proof_py_sha256", HERE / "check_proof.py"),
        ("check_proof_sh_sha256", HERE / "check_proof.sh"),
        ("proof_validation_sha256", HERE / "proof-validation.md"),
        ("lake_manifest_sha256", ROOT / "Formalizations/Lean/lake-manifest.json"),
        ("standard_sha256", ROOT / "Docs/Stage1_Blueprint_rev-5.6.md"),
        ("execution_skill_sha256", ROOT / "skills/execute-stage1-rev56/SKILL.md"),
    ):
        assert receipt["inputs"][key] == sha256(path), key

    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    status = git_output("status", "--short", "--untracked-files=all")
    actual = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (sorted(actual), sorted(CHANGED_PATHS))

    print(
        "PASS THM-M-1021 proof packet: exact canonical root kernel-checks; "
        "frozen Riesz route and acceptance remain open"
    )
    print(f"upstream revision/tree: {UPSTREAM_REVISION} / {UPSTREAM_TREE}")
    print("accepted frozen obligations: 0; theorem_complete=false")


if __name__ == "__main__":
    main()
