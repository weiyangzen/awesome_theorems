#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1057-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1057"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1057-VALIDATION"
THEOREM = "THM-M-1057"
BASE_REVISION = "e8499ef6898f9562fb480587db7eb9220c04b6fc"
BASE_TREE = "d88a39b243dd6a835f2e7463b9805d1cb175fb80"
EXPRESSION_SHA256 = "aebaaa6256cc5cb252ff4662647955a625f2ff6f1311dbcea1c04463ab3c03af"
DENOMINATOR_SHA256 = "080ff4e9ec6298847c52b7135ca47d9d57aecd0797d2ff1acd6161aaf1b0f67c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_ARCHIVE_SHA256 = "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
TARGET_LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_IDS = [
    "M1057-ROOT",
    "M1057-S-DEFINITIONS",
    "M1057-S-BOUNDARY",
    "M1057-S-FOUNDATION",
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
PROOF_RECEIPT_IDS = [
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
EXPECTED_INPUTS = {
    "Statement.lean": "bdd8ad8026b13ec9de27a63aac9874e88d29e8f57a9d5dcf0380d3f14eb61073",
    "AnchorAudit.lean": "e56fab6de687822f640d476029b379a251261183dbec818e924d1a0ea19be1f1",
    "ObligationTree.lean": "637c86f449f9d6e0180a93cae59672f1ecbffe9fd06c216065adc1c3e4adfd7a",
    "MaximalErgodic.lean": "1e6ecd26fe2f3587f292e82e41b3bc7e61f5110cf4be6e3a5e4bc53a8a45c6d5",
    "Birkhoff.lean": "0bb4ef8cc491100c54c8966ba31c44ac86661117b1e1eac8498564bc5384f789",
    "KingmanFekete.lean": "4112aaeb5043c7bc5e659c62ef8f58b5f563ebfe94fae9eb3ad0c9bcbcf3749a",
    "KingmanDerriennic.lean": "1bd9754dcc2f957084804a9b7136e0a378bd9abc7e857a77b86857298934340a",
    "KingmanCompanion.lean": "231b552e488d9b693edfaf1b461e612901698e205227db2fc579a4d4d54f9f2a",
    "KingmanBlockSqueeze.lean": "3e26d917b00133917ea10788c8e54542cff61c8d03c7afd6c8138f60720ba567",
    "KingmanCore.lean": "fb2fad9b2c30386476fa67b9db71eda07880823d902f183f9eab2a915a5a4d82",
    "KingmanMeans.lean": "96fc4065af56f39ca17602238a31d6de108d0d0bf3db6fd490c1a5a2b8e6cc52",
    "Proof.lean": "235eb7cbbc9a3bb6fa7f4f651de1d260dc1e89b2d40471fac8f82757b32278ec",
    "statement.json": "7548489e0797f7d8ce20cade71c22e584f10205ca4f6f84697ab59751e20a5c0",
    "anchor-audit.json": "14b523ec4f5e2c1b918a0c1a0fcbe12fffaf46fe185333f277356472a2829003",
    "obligation-registry.json": "71394c3b69dd4b8970849416d502072fdc3fb7775d8ee92fdddf1fb5cf97ace0",
    "typed-graphs.json": "b9d95e5ec6c81f9196c72f175c45d3f426696871c45234fe0dd7ed7b8f1e3c96",
    "validation-specs.json": "b971c17b17d85e1700e57ec99b27d8dcd89ed82a1980c846d0ff6ea924d9320b",
    "proof-receipt.json": "d49b270822bab040d3455afbb40b552d9bf90b682083cfc015e0df11c15b5d32",
    "PORT_PROVENANCE.md": "7620ed425654a3fd729fcda38c8994a98db7e9e60944355a52c78f2cee4c17db",
    "source_statement_crosswalk.md": "5c4eaf9050d57f9f7348b46bee63a269f136f6ca2e465cb973d55644aadd62b0",
    "LICENSE": TARGET_LICENSE_SHA256,
    "Validation.lean": "f0be52b702f13ba0cb38d15e0e3a3366c6e70d14899cab64ca9cb3a35b55e942",
    "check_validation.sh": "76d84f62b74c9fc7532855f0cdd7686f1f332d2c78891f8995eb412b3cb3fea8",
    "validation-spec.json": "e7da3cc084a5ece111542516af992b8c7abab3ef1f5fdc6fe54c2d336a5fd18c",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SOURCE_ROWS = {
    "MaximalErgodic.lean": ("ErgodicTheory/Ergodic/MaximalErgodic.lean", "6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc"),
    "Birkhoff.lean": ("ErgodicTheory/Ergodic/Birkhoff.lean", "bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a"),
    "KingmanFekete.lean": ("ErgodicTheory/Ergodic/Kingman/Fekete.lean", "7e29b3f2e0dbf26e13d6c1aef53563052e85656e0e868dd50d846d62a474fcff"),
    "KingmanDerriennic.lean": ("ErgodicTheory/Ergodic/Kingman/Derriennic.lean", "f3ca0c3903b1a07ea5533bc962233a834ddf3a3708118dd177b92e636f9a2a62"),
    "KingmanCompanion.lean": ("ErgodicTheory/Ergodic/Kingman/Companion.lean", "50f3716e5f059afb50086489349726ecb8f1b2f626a5fc2f605e49e4fd54d33e"),
    "KingmanBlockSqueeze.lean": ("ErgodicTheory/Ergodic/Kingman/BlockSqueeze.lean", "88854f77420ae853bf615b80e600c50b9048f2dccb17dfae4edbf5451c661c71"),
    "KingmanCore.lean": ("ErgodicTheory/Ergodic/Kingman/Core.lean", "d0335f2c93d23a70700deebd1b568aed91ef7f61ada70cc9ffcf4a4d60e2dbfa"),
    "KingmanMeans.lean": ("ErgodicTheory/TwoSided/KingmanMeans.lean", "80400f3fdb9847121a6f6c5b1a068979a0e223004409a34b4f1a96536f80a053"),
}
MATHLIB_SOURCES = {
    "Mathlib/MeasureTheory/Function/AEMeasurableSequence.lean": ("72724264ce6ac6bf793b0071298a77691f58582e", "6471c853a700200d9db58f3350ce24f3abf31e8526072f286e0d7c750fdda8bc"),
    "Mathlib/Analysis/Subadditive.lean": ("29766b5d76f23f8a654d26de718a6ba334a99e2a", "8fab15e33d332e1cb78a33a35769b4ccc2d6e008af561b49259d60a0279b61c2"),
    "Mathlib/Dynamics/Ergodic/Function.lean": ("86b366bccf56d55b262b59157fef5d227cf68063", "9767f751f891a797ae46fc6715a830de83dc0b6a5c0661d62cd0205ba98e93c0"),
    "Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean": ("684a5cc254c1e01d9dc48c99e6dc605b95275b82", "572455e8b2d197efe5001ad3b1673a0894337aaa79cb19fd2260f1c1aff7f8ea"),
    "Mathlib/Dynamics/Ergodic/Ergodic.lean": ("d07e6257a84d3756217b5b692b5c86edccbe9bc7", "853dac930e9abd11a440ad1a6b1390d34a33ed09a5c96915b623196e943ac0f4"),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1057 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact statement, frozen composition, eight vendored modules, proof root, and trust probe elaborated",
    "PASS hygiene: Lean transitive sorry collectors and a comment-stripped prohibited-construct scan passed",
    "PASS selected provenance: local ports reconstruct, hashes and licenses agree, and the clean pinned mathlib identity matches",
    "FAIL CLOSED authority: proof is not master-accepted; graph and anchor inventory contradict later proof evidence; accepted root remains H1/M3/R3",
    "FAIL CLOSED node coverage: the proof receipt gives ten IDs only three exact declarations and no per-analytic-node body identities",
    "FAIL CLOSED foundation/trust: observed axioms are unaccepted and complete transitive declaration, compiled-artifact, and TCB closure are absent",
    "FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache clean-checkout offline replay or deterministic bundle",
    "FAIL CLOSED independent release: no proof-independent exact-root implementation, distinct signed runner, or minimal verifier exists",
    "audit_complete=false; theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def elan_binary(name: str) -> Path:
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    result = subprocess.run(
        ["elan", "which", name],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"cannot resolve pinned {name}: {result.stdout}")
    path = Path(result.stdout.strip())
    assert path.is_file(), f"pinned {name} executable missing"
    return path


def code_without_comments(source: str) -> str:
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
    notice = re.compile(
        r"/-\nPort notice: vendored from `marcmorningstar/lean4-ergodic-theory` at commit\n"
        r"`ed3fa6b8a30594eeb791160563942ba115581aa0`\..*?\n-/\n",
        re.DOTALL,
    )
    source, count = notice.subn("", source, count=1)
    assert count == 1, f"{name}: exact port notice missing"
    source = source.replace("integral_finset_sum", "integral_finsetSum")
    source = source.replace("integrable_finset_sum", "integrable_finsetSum")
    imports = {
        "Birkhoff.lean": {"import MaximalErgodic": "import ErgodicTheory.Ergodic.MaximalErgodic"},
        "KingmanFekete.lean": {"import Birkhoff": "import ErgodicTheory.Ergodic.Birkhoff"},
        "KingmanDerriennic.lean": {"import KingmanFekete": "import ErgodicTheory.Ergodic.Kingman.Fekete"},
        "KingmanCompanion.lean": {"import KingmanDerriennic": "import ErgodicTheory.Ergodic.Kingman.Derriennic"},
        "KingmanBlockSqueeze.lean": {"import KingmanCompanion": "import ErgodicTheory.Ergodic.Kingman.Companion"},
        "KingmanCore.lean": {"import KingmanBlockSqueeze": "import ErgodicTheory.Ergodic.Kingman.BlockSqueeze"},
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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 249 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 249,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1057-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1057-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1057.KingmanTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M3" and closure["root_closed"] is False
    assert closure["minimal_open_cut"] == ["M1057-T-LIMIT-PACKAGE"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-1057-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == PROOF_RECEIPT_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert len(proof_receipt["exact_declarations"]) == 3
    analytic = set(PROOF_RECEIPT_IDS) - {"M1057-ROOT", "M1057-T-ASSEMBLE"}
    body_ids = {
        row["obligation_id"]: row["terminal_proof_body_id"]
        for row in registry["obligations"]
    }
    assert all(body_ids[node] is None for node in analytic)
    assert all(
        not node["evidence_ids"] and node["provenance_id"] == "none"
        for node in graphs["nodes"]
        if node["obligation_id"] in analytic
    )

    assert anchor["terminal_mathlib_search"]["result_count"] == 0
    assert anchor["external_lean4_search"]["immutable_candidate_revisions"] == []
    assert anchor["classification"]["machine_status"] == "not_repo_local_closed"
    assert anchor["classification"]["root_vector_after_audit"] == {
        "human": "H1", "machine": "M3", "readability": "R3"
    }
    assert anchor["classification"]["theorem_complete"] is False
    assert proof_receipt["proof_body"]["origin"]["revision"] == UPSTREAM_REVISION
    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    assert "theorem/page premise mapping and errata review remain open (`H1`)" in crosswalk
    assert "No `H0` or machine-closure claim is made" in crosswalk

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_sources = [
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        *SOURCE_ROWS, "Proof.lean", "Validation.lean",
    ]
    for name in lean_sources:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    validation = code_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" in validation
    assert "theorem " not in validation and "def " not in validation
    for declaration in (
        "root_of_pointwiseLimitPackage",
        "tendsto_kingman_ergodic_means",
        "pointwiseLimitPackage",
        "kingmanTarget",
    ):
        assert f"assert_no_sorry {declaration}" in validation or (
            f"assert_no_sorry Stage1Instances.THM_M_1057.{declaration}" in validation
        ) or f"assert_no_sorry ErgodicTheory.{declaration}" in validation

    provenance = (HERE / "PORT_PROVENANCE.md").read_text(encoding="utf-8")
    assert UPSTREAM_REVISION in provenance
    assert sha256(HERE / "LICENSE") == TARGET_LICENSE_SHA256
    for name, (upstream_path, upstream_digest) in SOURCE_ROWS.items():
        reconstructed = reconstruct_upstream(
            name, (HERE / name).read_text(encoding="utf-8")
        ).encode("utf-8")
        assert hashlib.sha256(reconstructed).hexdigest() == upstream_digest, name
        for value in (name, upstream_path, upstream_digest, EXPECTED_INPUTS[name]):
            assert value in provenance, (name, value)

    archive = Path("/tmp/lean4-ergodic-ed3fa6b8.tar.gz")
    if archive.is_file():
        assert sha256(archive) == UPSTREAM_ARCHIVE_SHA256

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for relative, (blob, source_digest) in MATHLIB_SOURCES.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / relative) == source_digest
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = elan_binary("lean")
    lake = elan_binary("lake")
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    lake_version = run([str(lake), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    tools = {
        "lean": lean,
        "lake": lake,
        "python": Path(os.path.realpath(sys.executable)),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bash": Path(os.path.realpath(shutil.which("bash") or "")),
        "bubblewrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
        "elan": Path(os.path.realpath(shutil.which("elan") or "")),
    }
    assert sha256(tools["lean"]) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(tools["lake"]) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(tools["python"]) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(tools["git"]) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    assert sha256(tools["bash"]) == "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
    assert sha256(tools["bubblewrap"]) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    assert sha256(tools["elan"]) == "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"

    kernel_output = run(
        ["bash", str(HERE / "check_validation.sh")],
        cwd=ROOT,
    )
    assert kernel_output.count("Declarations are sorry-free!") == 11
    assert "declaration uses 'sorry'" not in kernel_output and "error:" not in kernel_output
    for declaration in (
        "Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage",
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_kingman",
        "ErgodicTheory.tendsto_kingman_ergodic",
        "ErgodicTheory.tendsto_kingman_ergodic_means",
        "Stage1Instances.THM_M_1057.pointwiseLimitPackage",
        "Stage1Instances.THM_M_1057.kingmanTarget",
    ):
        pattern = re.compile(
            re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
            re.DOTALL,
        )
        match = pattern.search(kernel_output)
        assert match is not None, declaration
        observed = {part.strip() for part in match.group(1).split(",")}
        assert observed == EXPECTED_AXIOMS, (declaration, observed)

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["recipe"] == spec

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1057-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["worktree_ref"] == "detached HEAD in isolated worker automation clone"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["result"]["kernel_output_sha256"] == hashlib.sha256(
        kernel_output.encode("utf-8")
    ).hexdigest()
    assert receipt["result"]["kernel_output_bytes"] == len(kernel_output.encode("utf-8"))
    assert receipt["result"]["kernel_log"] == {
        "stream": "captured stdout",
        "sha256": hashlib.sha256(kernel_output.encode("utf-8")).hexdigest(),
        "bytes": len(kernel_output.encode("utf-8")),
        "persisted_path": None,
    }
    assert receipt["provenance"]["upstream_archive_observed_this_run"] is True
    assert receipt["provenance"]["upstream_archive_required_for_replay"] is False
    assert receipt["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1057-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert receipt["known_failures"] == packet["known_failures"]

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
