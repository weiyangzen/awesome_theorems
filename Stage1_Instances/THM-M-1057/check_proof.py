#!/usr/bin/env python3
"""Fail-closed provenance, source, pin, kernel, and receipt checks for THM-M-1057."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
ITEM = "S56-M-1057-PROOF"
THEOREM = "THM-M-1057"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
EXPRESSION_SHA256 = "aebaaa6256cc5cb252ff4662647955a625f2ff6f1311dbcea1c04463ab3c03af"
DENOMINATOR_SHA256 = "080ff4e9ec6298847c52b7135ca47d9d57aecd0797d2ff1acd6161aaf1b0f67c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"

SOURCE_ROWS = {
    "MaximalErgodic.lean": (
        "ErgodicTheory/Ergodic/MaximalErgodic.lean",
        "6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc",
        "1e6ecd26fe2f3587f292e82e41b3bc7e61f5110cf4be6e3a5e4bc53a8a45c6d5",
    ),
    "Birkhoff.lean": (
        "ErgodicTheory/Ergodic/Birkhoff.lean",
        "bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a",
        "0bb4ef8cc491100c54c8966ba31c44ac86661117b1e1eac8498564bc5384f789",
    ),
    "KingmanFekete.lean": (
        "ErgodicTheory/Ergodic/Kingman/Fekete.lean",
        "7e29b3f2e0dbf26e13d6c1aef53563052e85656e0e868dd50d846d62a474fcff",
        "4112aaeb5043c7bc5e659c62ef8f58b5f563ebfe94fae9eb3ad0c9bcbcf3749a",
    ),
    "KingmanDerriennic.lean": (
        "ErgodicTheory/Ergodic/Kingman/Derriennic.lean",
        "f3ca0c3903b1a07ea5533bc962233a834ddf3a3708118dd177b92e636f9a2a62",
        "1bd9754dcc2f957084804a9b7136e0a378bd9abc7e857a77b86857298934340a",
    ),
    "KingmanCompanion.lean": (
        "ErgodicTheory/Ergodic/Kingman/Companion.lean",
        "50f3716e5f059afb50086489349726ecb8f1b2f626a5fc2f605e49e4fd54d33e",
        "231b552e488d9b693edfaf1b461e612901698e205227db2fc579a4d4d54f9f2a",
    ),
    "KingmanBlockSqueeze.lean": (
        "ErgodicTheory/Ergodic/Kingman/BlockSqueeze.lean",
        "88854f77420ae853bf615b80e600c50b9048f2dccb17dfae4edbf5451c661c71",
        "3e26d917b00133917ea10788c8e54542cff61c8d03c7afd6c8138f60720ba567",
    ),
    "KingmanCore.lean": (
        "ErgodicTheory/Ergodic/Kingman/Core.lean",
        "d0335f2c93d23a70700deebd1b568aed91ef7f61ada70cc9ffcf4a4d60e2dbfa",
        "fb2fad9b2c30386476fa67b9db71eda07880823d902f183f9eab2a915a5a4d82",
    ),
    "KingmanMeans.lean": (
        "ErgodicTheory/TwoSided/KingmanMeans.lean",
        "80400f3fdb9847121a6f6c5b1a068979a0e223004409a34b4f1a96536f80a053",
        "96fc4065af56f39ca17602238a31d6de108d0d0bf3db6fd490c1a5a2b8e6cc52",
    ),
}

PROOF_IDS = [
    "M1057-ROOT",
    "M1057-N-EXPECTATION-SUBADDITIVE",
    "M1057-L-FEKETE",
    "M1057-C-BLOCK-DECOMPOSITION",
    "M1057-L-MAXIMAL-INEQUALITY",
    "M1057-L-AE-CONVERGENCE",
    "M1057-L-INVARIANCE",
    "M1057-L-ERGODIC-IDENTIFICATION",
    "M1057-T-LIMIT-PACKAGE",
    "M1057-T-ASSEMBLE",
]
OPEN_IDS = ["M1057-S-DEFINITIONS", "M1057-S-BOUNDARY", "M1057-S-FOUNDATION"]
VENDORED_MODULES = [
    "MaximalErgodic",
    "Birkhoff",
    "KingmanFekete",
    "KingmanDerriennic",
    "KingmanCompanion",
    "KingmanBlockSqueeze",
    "KingmanCore",
    "KingmanMeans",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in SOURCE_ROWS),
    f"Stage1_Instances/{THEOREM}/LICENSE",
    f"Stage1_Instances/{THEOREM}/PORT_PROVENANCE.md",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments(source: str) -> str:
    """Remove nested Lean block comments and line comments for token scanning."""
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
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reconstruct_upstream(name: str, source: str) -> str:
    """Invert exactly the documented, mechanical 4.29 port transformation."""
    notice = re.compile(
        r"/-\nPort notice: vendored from `marcmorningstar/lean4-ergodic-theory` at commit\n"
        r"`ed3fa6b8a30594eeb791160563942ba115581aa0`\..*?\n-/\n",
        re.DOTALL,
    )
    source, count = notice.subn("", source, count=1)
    assert count == 1, f"{name}: missing or duplicate exact port notice"
    source = source.replace("integral_finset_sum", "integral_finsetSum")
    source = source.replace("integrable_finset_sum", "integrable_finsetSum")
    imports = {
        "Birkhoff.lean": {"import MaximalErgodic": "import ErgodicTheory.Ergodic.MaximalErgodic"},
        "KingmanFekete.lean": {"import Birkhoff": "import ErgodicTheory.Ergodic.Birkhoff"},
        "KingmanDerriennic.lean": {
            "import KingmanFekete": "import ErgodicTheory.Ergodic.Kingman.Fekete"
        },
        "KingmanCompanion.lean": {
            "import KingmanDerriennic": "import ErgodicTheory.Ergodic.Kingman.Derriennic"
        },
        "KingmanBlockSqueeze.lean": {
            "import KingmanCompanion": "import ErgodicTheory.Ergodic.Kingman.Companion"
        },
        "KingmanCore.lean": {
            "import KingmanBlockSqueeze": "import ErgodicTheory.Ergodic.Kingman.BlockSqueeze"
        },
        "KingmanMeans.lean": {
            "import KingmanCore": "import ErgodicTheory.Ergodic.Kingman.Core",
            "import Birkhoff": "import ErgodicTheory.Ergodic.Birkhoff",
        },
    }
    for local, upstream in imports.get(name, {}).items():
        assert source.count(local) == 1, (name, local)
        source = source.replace(local, upstream, 1)
    if name == "KingmanBlockSqueeze.lean":
        helper = re.compile(
            r"\nprivate theorem tendsto_limsup_comp_le_limsup.*?"
            r"tendsto_limsup_comp_le_limsup \(β := βᵒᵈ\) hv hvf hg\n",
            re.DOTALL,
        )
        source, count = helper.subn("", source, count=1)
        assert count == 1, "BlockSqueeze compatibility helper changed"
        source = re.sub(
            r"tendsto_limsup_comp_le_limsup \(β := EReal\) hkdiv\n\s*"
            r"\(Filter\.isCobounded_le_of_bot\) \(Filter\.isBounded_le_of_top\)",
            "hkdiv.limsup_comp_le_limsup",
            source,
            count=1,
        )
        source = source.replace(
            "tendsto_limsup_comp_le_limsup hmul (u := fun j => usub g x j)",
            "hmul.limsup_comp_le_limsup (u := fun j => usub g x j)",
            1,
        )
        source = source.replace(
            "tendsto_liminf_le_liminf_comp hmul (u := fun j => usub g x j)",
            "hmul.liminf_le_liminf_comp (u := fun j => usub g x j)",
            1,
        )
        source = source.replace(
            "tendsto_liminf_le_liminf_comp hφ (u := fun k => usub g x (k * M))",
            "hφ.liminf_le_liminf_comp (u := fun k => usub g x (k * M))",
            1,
        )
    return source


def run_lean_trust_zero() -> str:
    lean = subprocess.check_output(
        ["lake", "env", "which", "lean"], cwd=LEAN_ROOT, text=True
    ).strip()
    lean_path = subprocess.check_output(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, text=True
    ).strip()
    output: list[str] = []
    with tempfile.TemporaryDirectory(prefix="thm-m-1057-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            shutil.copy2(HERE / filename, tmp / filename)
        for module in VENDORED_MODULES:
            shutil.copy2(HERE / f"{module}.lean", tmp / f"{module}.lean")
        env = os.environ.copy()
        env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        for module in ["Statement", "ObligationTree", *VENDORED_MODULES, "Proof"]:
            command = [lean, "--trust=0", "-o", f"{module}.olean", f"{module}.lean"]
            result = subprocess.run(
                command,
                cwd=tmp,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=1800,
                check=False,
            )
            output.append(f"[{module}]\n{result.stdout}")
            assert result.returncode == 0, "".join(output)
        assert not list(HERE.glob("*.olean")), "validation must not write owned .olean files"
    return "".join(output)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    receipt_path = HERE / "proof-receipt.json"
    validation_path = HERE / "proof-validation.md"
    packet_path = ROOT / ".stage1-worker-selftest.json"
    proof = proof_path.read_text(encoding="utf-8")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 249,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-1057-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1057-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1057.KingmanTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M1057-ROOT"
    assert set(registry["frozen_denominators"]["required_machine"]) == set(
        PROOF_IDS + OPEN_IDS
    )
    children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reached: set[str] = set()
    pending = ["M1057-ROOT"]
    while pending:
        node = pending.pop()
        if node not in reached:
            reached.add(node)
            pending.extend(children.get(node, []))
    assert reached == set(PROOF_IDS)

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    lean_paths = [proof_path, *(HERE / name for name in SOURCE_ROWS)]
    for path in lean_paths:
        assert prohibited.search(strip_comments(path.read_text(encoding="utf-8"))) is None, path
    for marker in (
        "import KingmanMeans",
        "namespace Strictification",
        "private def stableSet",
        "private theorem measure_compl_stableSet",
        "private theorem strictTransformation_ergodic",
        "private theorem strictProcess_subadditive",
        "ErgodicTheory.tendsto_kingman_ergodic_means",
        "theorem pointwiseLimitPackage : PointwiseLimitPackage.{u}",
        "theorem kingmanTarget : KingmanTarget.{u}",
        "root_of_pointwiseLimitPackage pointwiseLimitPackage",
        "#print sorries ErgodicTheory.tendsto_kingman_ergodic_means",
        "#print sorries pointwiseLimitPackage",
        "#print sorries kingmanTarget",
        "#print axioms pointwiseLimitPackage",
        "#print axioms kingmanTarget",
    ):
        assert marker in proof, marker

    provenance = (HERE / "PORT_PROVENANCE.md").read_text(encoding="utf-8")
    assert UPSTREAM_REVISION in provenance
    assert sha256(HERE / "LICENSE") == (
        "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
    )
    assert "Apache License" in (HERE / "LICENSE").read_text(encoding="utf-8")
    for name, (upstream_path, upstream_digest, port_digest) in SOURCE_ROWS.items():
        path = HERE / name
        assert sha256(path) == port_digest
        source = path.read_text(encoding="utf-8")
        reconstructed = reconstruct_upstream(name, source).encode("utf-8")
        assert hashlib.sha256(reconstructed).hexdigest() == upstream_digest, name
        for value in (name, upstream_path, upstream_digest, port_digest):
            assert value in provenance, (name, value)

    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink(), "worker must reuse the canonical pinned .lake symlink"

    lean_output = run_lean_trust_zero()
    assert "declaration uses 'sorry'" not in lean_output
    assert "declaration has metavariables" not in lean_output
    assert lean_output.count("Declarations are sorry-free!") == 3
    for declaration in (
        "Stage1Instances.THM_M_1057.pointwiseLimitPackage",
        "Stage1Instances.THM_M_1057.kingmanTarget",
    ):
        expected = (
            f"'{declaration}' depends on axioms: "
            "[propext, Classical.choice, Quot.sound]"
        )
        assert expected in lean_output, (declaration, lean_output[-4000:])

    receipt = load(receipt_path)
    packet = load(packet_path)
    assert receipt["schema_version"] in {
        "stage1-node-receipt/1.0",
        "stage1-proof-receipt/1.0",
    }
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt.get("base_tree", BASE_TREE) == BASE_TREE
    assert receipt.get("accepted", False) is False
    assert receipt.get("proposed_state", "[_]") == "[_]"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(receipt["provisionally_closed_proof_obligation_ids"]) == set(PROOF_IDS)
    assert receipt["required_machine_open_ids"] == OPEN_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["lake_manifest_sha256"] == MANIFEST_SHA256
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("port_provenance_sha256", "PORT_PROVENANCE.md"),
        ("license_sha256", "LICENSE"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key

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
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = validation_path.read_text(encoding="utf-8")
    assert "theorem completion" in validation.lower()
    assert "pending master acceptance" in validation.lower()
    for path in [
        *lean_paths,
        HERE / "LICENSE",
        HERE / "PORT_PROVENANCE.md",
        HERE / "check_proof.py",
        receipt_path,
        validation_path,
        packet_path,
    ]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path

    print("PASS THM-M-1057 proof: vendored Kingman stack reconstructs and exact root closes")
    print(f"proof sha256: {sha256(proof_path)}")
    print("provisional proof state only; accepted state and theorem_complete remain unchanged")


if __name__ == "__main__":
    main()
