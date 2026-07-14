#!/usr/bin/env python3
"""Fail-closed provenance, pin, source, receipt, and handoff checks for THM-M-1083."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
VENDOR = HERE / "Vendor/BrownianMotion"
ITEM = "S56-M-1083-PROOF"
THEOREM = "THM-M-1083"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
TARGET_EXPRESSION = "fb7209158513f98f9692a12449560573c5009e1a2366ed34eb8e61f9cae7c58a"
DENOMINATOR = "06ca47d90b0a7af9d99c935d0c7766cea3df5e722f08b563d226d7736baf6a50"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_MANIFEST = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
UPSTREAM_REVISION = "91885e6172648ea7f9c6a16b3a7069f92c88e023"
UPSTREAM_MANIFEST = "baeba6af6f09aad37899666edf987cba2f75f0ad4dd1740314c2357293f1210c"
ADAPTED_MANIFEST = "f43079ae9b6ae2745f57dc63cf07e9508a4532691a99b885bbaf26d33cc9b2aa"
NOTICE = "-- Modified locally only to namespace-qualify vendored BrownianMotion imports.\n\n"
PREFIX = "«Stage1_Instances».«THM-M-1083».Vendor."

SOURCE_ROWS = {
    "Auxiliary/Algebra.lean": ("9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3", "9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3"),
    "Auxiliary/ENNReal.lean": ("108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6", "108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6"),
    "Auxiliary/FiniteInf.lean": ("042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a", "042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a"),
    "Auxiliary/MeanInequalities.lean": ("67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d", "67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d"),
    "Auxiliary/MeasureTheory.lean": ("e6637d648b5782dad84bd3fe114e731a31cb2911534f04e2ef27012b8e1ac7a0", "3df7b5faa5795bda61419b864048349d2ae32d8381a4376bac0a337089b383e6"),
    "Auxiliary/Metric.lean": ("13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e", "13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e"),
    "Auxiliary/Nat.lean": ("43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae", "43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae"),
    "Auxiliary/Topology.lean": ("ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6", "ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6"),
    "Continuity/Chaining.lean": ("dbb3f80c0e56d708c4dfcd1a30cd7420f280af2f50cdf2785fa2f2ad34cc7b19", "75e88c2b7800ebf9f0f3b3f52538444e3323a30f0cbfd603847d2874e3db87bc"),
    "Continuity/CoveringNumber.lean": ("89829da52abf33125f18c30f82f2b76d89516682483c1a5cc3caa65d3a649f9d", "1d4cad9147985c271cd58fc90bc60a8697933258db6b8228a85a0e2f125f543b"),
    "Continuity/HasBoundedInternalCoveringNumber.lean": ("8166a60c831bf60262171d94f53298908e7372ebfb76a136e9e7de6cd4725f03", "688b05f9a645d3d87f8e5cab131b3d2b1723cac32b44703c8b54d92d45cd29e8"),
    "Continuity/IsKolmogorovProcess.lean": ("e54c594363a9cd15f60faeba19b643e972507d5af568f90ee277ec655ea78dcc", "62f9ae5b726aba8f36db7a0cb92f9b446ba62e5b583804707aa2ae18b3378a02"),
    "Continuity/KolmogorovChentsov.lean": ("ce2b9dc8fc18f083d3ebe86c5ef68bd3e8d4e2c1f1587d4fa7c6e503144578a9", "8c60d137ebb5918ebde96e5158867ff5a7e25b9711ef68cbcb9cb4626df9360b"),
    "Continuity/KolmogorovChentsovInequality.lean": ("502061001bd4c2244e3e69d7610aace1e759c0d26f78ada78ccb26e35a6fda51", "0d8fd8b5bcd66770c79337fbc2ba9dcac7a888c9703f40ac665cef1504a30576"),
    "Gaussian/StochasticProcesses.lean": ("c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81", "c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81"),
}

PROOF_IDS = [
    "M1083-ROOT", "M1083-N-KOLMOGOROV", "M1083-N-COVERING", "M1083-B-SCALES",
    "M1083-C-NETS", "M1083-L-MARKOV", "M1083-L-BOREL-CANTELLI", "M1083-L-CAUCHY",
    "M1083-C-MODIFICATION", "M1083-L-HOLDER-NET", "M1083-L-HOLDER-EXTEND",
    "M1083-T-ONE-GAMMA", "M1083-T-MODIFICATION", "M1083-T-COMPOSE",
]
IMPLEMENTED_CANDIDATE_IDS = [
    "M1083-N-KOLMOGOROV", "M1083-N-COVERING",
    "M1083-T-MODIFICATION", "M1083-T-COMPOSE",
]
RECONCILIATION_PENDING_IDS = [
    "M1083-N-KOLMOGOROV", "M1083-N-COVERING", "M1083-B-SCALES",
    "M1083-C-NETS", "M1083-L-MARKOV",
    "M1083-L-BOREL-CANTELLI", "M1083-L-CAUCHY", "M1083-C-MODIFICATION",
    "M1083-L-HOLDER-NET", "M1083-L-HOLDER-EXTEND", "M1083-T-ONE-GAMMA",
    "M1083-T-MODIFICATION", "M1083-T-COMPOSE", "M1083-ROOT",
]
INTERFACE_IDS = ["M1083-S-DEFINITIONS", "M1083-S-BOUNDARY"]
OPEN_IDS = ["M1083-S-FOUNDATION"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
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
    assert depth == 0
    return "".join(output)


def reconstruct(source: str, adapted: bool) -> bytes:
    if adapted:
        assert source.count(NOTICE) == 1
        source = source.replace(NOTICE, "", 1)
        assert PREFIX in source
        source = source.replace(PREFIX, "")
    else:
        assert NOTICE not in source and PREFIX not in source
    return source.encode("utf-8")


def changed_paths() -> set[str]:
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    return {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}


def main() -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 525, "phase": "proof",
        "layer": 4, "state": "[ ]", "depends_on": ["S56-M-1083-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert next(row for row in execution["items"] if row["id"] == "S56-M-1083-OBLIGATION_TREE")["state"] == "[_]"
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR
    assert set(registry["frozen_denominators"]["required_machine"]) == set(PROOF_IDS + INTERFACE_IDS + OPEN_IDS)

    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+", re.MULTILINE,
    )
    for path in [HERE / "Proof.lean", *sorted(VENDOR.rglob("*.lean"))]:
        assert prohibited.search(strip_comments(path.read_text(encoding="utf-8"))) is None, path
    for marker in (
        "ProbabilityTheory.exists_modification_holder",
        "theorem timeInterval_hasBoundedCoveringNumber",
        "theorem isKolmogorovProcess_of_increment",
        "theorem kolmogorovContinuity : Stage1Instances.THM_M_1083.KolmogorovContinuity.{u}",
        "theorem canonicalProof : Stage1Instances.THM_M_1083.Statement.{u}",
    ):
        assert marker in proof, marker

    assert len(list(VENDOR.rglob("*.lean"))) == len(SOURCE_ROWS) == 15
    upstream_lines: list[str] = []
    adapted_lines: list[str] = []
    adapted_count = import_count = 0
    provenance = (HERE / "PORT_PROVENANCE.md").read_text(encoding="utf-8")
    assert UPSTREAM_REVISION in provenance
    for name, (upstream_digest, adapted_digest) in SOURCE_ROWS.items():
        path = VENDOR / name
        source = path.read_text(encoding="utf-8")
        adapted = upstream_digest != adapted_digest
        if adapted:
            adapted_count += 1
            import_count += source.count(PREFIX)
        assert sha256(path) == adapted_digest, name
        assert hashlib.sha256(reconstruct(source, adapted)).hexdigest() == upstream_digest, name
        upstream_lines.append(f"{upstream_digest}  BrownianMotion/{name}\n")
        adapted_lines.append(f"{adapted_digest}  BrownianMotion/{name}\n")
        for value in (name, upstream_digest, adapted_digest):
            assert value in provenance, (name, value)
    assert adapted_count == 7 and import_count == 15
    assert hashlib.sha256("".join(upstream_lines).encode()).hexdigest() == UPSTREAM_MANIFEST
    assert hashlib.sha256("".join(adapted_lines).encode()).hexdigest() == ADAPTED_MANIFEST
    assert sha256(HERE / "Vendor/LICENSE") == "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"

    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST
    assert (LEAN_ROOT / ".lake").is_symlink()

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION
    assert receipt["registry_denominator_sha256"] == DENOMINATOR
    assert receipt["exact_root_kernel_closed"] is True
    assert receipt["exact_root_frozen_graph_closed"] is False
    assert receipt["kernel_inhabited_obligation_ids_observed"] == ["M1083-ROOT"]
    assert receipt["directly_implemented_or_realized_candidate_ids_no_proof_credit"] == IMPLEMENTED_CANDIDATE_IDS
    assert receipt["closed_obligation_ids_proposed"] == []
    assert receipt["closure_candidate_after_master_reconciliation"] == ["M1083-ROOT"]
    assert receipt["frozen_graph_reconciliation_pending_ids"] == RECONCILIATION_PENDING_IDS
    assert receipt["integrated_informational_ids"] == ["M1083-X-EXTERNAL"]
    assert receipt["predecessor_interface_ids_not_reclaimed"] == INTERFACE_IDS
    assert receipt["foundation_open_ids"] == OPEN_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["inputs"]["check_proof_py_sha256"] == sha256(Path(__file__))
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    for key, filename in (
        ("statement_sha256", "Statement.lean"), ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"), ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"), ("validation_specs_sha256", "validation-specs.json"),
        ("port_provenance_sha256", "PORT_PROVENANCE.md"), ("license_sha256", "Vendor/LICENSE"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key

    assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    actual = changed_paths()
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == actual
    assert packet["known_failures"] == receipt["known_failures"]
    for relative in actual:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, relative
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), relative

    print("PASS THM-M-1083 proof phase: exact root and vendored source provenance checked")
    print(f"proof sha256: {sha256(HERE / 'Proof.lean')}")
    print("provisional proof state only; accepted state and theorem_complete remain unchanged")


if __name__ == "__main__":
    main()
