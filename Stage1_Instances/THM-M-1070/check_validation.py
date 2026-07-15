#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1070-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import pwd
import re
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1070"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1070-VALIDATION"
THEOREM = "THM-M-1070"
BASE_REVISION = "be35cd8f5123e9d06247b12859f3843bdd90c66f"
BASE_TREE = "a275a21a449fbcbd6c2333f5cfe737e906b20db6"
EXPRESSION_SHA256 = "8e1440de837395201d12a0f2085afe0c03d2504e99240b68154595fc2f8cffc1"
DENOMINATOR_SHA256 = "c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REMAINING_ROOT_CUT = [
    "M1070-L-INDEPENDENT",
    "M1070-L-STATIONARY",
    "M1070-L-STOCH-CONT",
]
EXPECTED_INPUTS = {
    "Statement.lean": "6968f5fbf916f36d31518be99b631a560afe8a5fbc2ca30108ff1d57bd692268",
    "AnchorAudit.lean": "fcb2f2502a5e3488164d1bb3c3812c246a528a3fa717e4fede61a54cff7dfde9",
    "ObligationTree.lean": "fb81286bcc0f1cdb673f370dd40264ec940995a175099d418d650fa95d242142",
    "Proof.lean": "fccf2d4b3cafa1cfefc2cd8e6166285e7c7fd89fd78f2cae46908b0fa0e8f339",
    "statement.json": "eb1dd62ab3d16e9421809d29384bec55485ea35e5e66b30a779c2fa0a4c2316e",
    "anchor-audit.json": "74ec2b694f12b059f23d4816379f32a2cadb481da3ac12bed89fd4bc5fbd7679",
    "obligation-registry.json": "4e0fa630b1284cc79e8c02cb73b6f1e4c2ce69dedf9674e6a9b32a4797775a51",
    "typed-graphs.json": "ced9c0f2a6516be3d1fea8e7421d3b3a00c5d96ed81751461c465dd072025206",
    "validation-specs.json": "17d8cac2fefebba71950b3e06992ffd8956c41574855dcb266725e0b1be05b79",
    "proof-receipt.json": "bb42b68276a80de61d7f162ab1cc2e34fcff0fa264c3f209eedcfc353f3bb0e4",
    "proof-blocker.json": "f28427a13439fb96e3e15be061a63dc6ec65c77dbca13c88612207a4571b83fb",
    "proof-validation.md": "06cbbe3c36291bcd7e299a48cc582443a818158961ce6ebee80a1ed948590a91",
    "source-statement-crosswalk.md": "5024d6c477ec2457c9d7dc8ad89f655b339c6ae243bc1d6b982e50c6549f9483",
    "check_obligation_tree.py": "6d3869a0e76c953400e461df776c329c66217a7399f6acd609b7bd344b7a0bb9",
    "check_proof.sh": "6548791402960f371832c6b2dfea79404975610a4d149333dcd612f5186af6bf",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/Probability/Independence/Process/HasIndepIncrements.lean": (
        "b62be7fb5b68018a5d5f10707c2fc8098dc0076b",
        "5be36c5884f2e622e6c1c7be8e1043978de4b6a76c6ba52a586ad228078a97b1",
        "f49e6195451025f3f14fa52bcff529e2bc490383a74e87c37b5661e3a22d34ff",
    ),
    "Mathlib/Probability/IdentDistrib.lean": (
        "b635f61469cc90d48337c8079441836b79122e24",
        "37d719a0916697171f6a0e53d03897ab1311cf9f12d77ba180d1017c90119544",
        "b58506abfc1e8ae059a10ecceb2215ee4f05865ce1ff5f6d37dc9df92dff44e0",
    ),
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1070.isLevyProcess_of_clauses",
    "Stage1Instances.THM_M_1070.clauses_of_isLevyProcess",
    "Stage1Instances.THM_M_1070.isLevyProcess_zero",
    "Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess",
)
STATEMENT_DECLARATION = (
    "Stage1Instances.THM_M_1070.isLevyProcess_iff_expandedSourceShape"
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_1070.isLevyProcess_of_components",
    "Stage1Instances.THM_M_1070.isLevyProcess_iff_components",
)
SUMMARY_LINES = (
    "PASS THM-M-1070 network-isolated trust-zero replay of the frozen statement, conditional composition, and four proof-phase declarations",
    "PASS hygiene and observed trust: checked declarations are sorry-free and use exactly propext, Classical.choice, and Quot.sound",
    "PASS selected local provenance: frozen hashes, clean mathlib pin/tree/origin/license, selected sources, and oleans agree",
    "OPEN exact root: the canonical target is a predicate over arbitrary P and X; the specialized witness and conditional composers close no frozen obligation",
    "BLOCKED release gates: proof dependency/master acceptance, complete provenance/TCB, cold empty-cache hermetic replay, and distinct-runner verification",
)
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
    "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent", "--clearenv",
    "--setenv", "HOME", "/tmp", "--setenv", "PATH", "/usr/bin:/bin",
    "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
    "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
    "/usr/bin/python3", "-I", "-B",
    "Stage1_Instances/THM-M-1070/check_validation.py",
]
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 1200.0
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1070/Validation.lean",
    "Stage1_Instances/THM-M-1070/check_validation.py",
    "Stage1_Instances/THM-M-1070/validation-phase.md",
    "Stage1_Instances/THM-M-1070/validation-receipt.json",
    "Stage1_Instances/THM-M-1070/validation-spec.json",
}


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


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
            if source[index] == "\n":
                output.append("\n")
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, declaration
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def actual_changed_paths() -> set[str]:
    status = run(["/usr/bin/git", "status", "--short", "--untracked-files=all"])
    return {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    statement_record = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    anchor = load(HERE / "anchor-audit.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    receipt_path = HERE / "validation-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None
    verify_outputs = os.environ.get("STAGE1_SKIP_OUTPUT_CHECK") != "1"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 512 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 512,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1070-PROOF"],
        "owned_paths": ["Stage1_Instances/THM-M-1070"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1070-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    formal = statement_record["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1070.IsLevyProcess"
    assert formal["source_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    root_row = next(row for row in registry["obligations"] if row["obligation_id"] == "M1070-ROOT")
    assert root_row["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    ids = [row["obligation_id"] for row in registry["obligations"]]
    assert len(ids) == len(set(ids)) == 13
    assert registry["frozen_denominators"]["inventory"] == ids
    assert {row["obligation_id"] for row in frozen_specs["recipes"]} == set(ids)
    assert frozen_specs["item_id"] == "S56-M-1070-OBLIGATION_TREE"

    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": ["M1070-S-DEFINITIONS", "M1070-T-COMPOSE"],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": REMAINING_ROOT_CUT,
        "root_machine_debt": "M3",
        "composition_certificates": [
            "Stage1Instances.THM_M_1070.isLevyProcess_of_components"
        ],
        "reason": (
            "The composition is conditional and every substantive process clause remains an "
            "open premise."
        ),
    }
    assert proof_receipt["item_id"] == "S56-M-1070-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    for key, name in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
    ):
        assert proof_receipt["inputs"][key] == EXPECTED_INPUTS[name], key
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["proof_phase_complete"] is False
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == REMAINING_ROOT_CUT

    assert anchor["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False
    leanlevy = next(row for row in anchor["candidates"] if row["id"] == "LEANLEVY-IS-LEVY-PROCESS")
    assert leanlevy["revision"] == "93b635fba23398bfb1f0db8d220f88172f6900b6"
    assert leanlevy["machine_classification"] == "M3_nonidentical_external_anchor"
    assert leanlevy["integration_status"].startswith("not a repository dependency")

    all_nodes = set(ids)
    edge_ids: set[str] = set()
    for graph_name, graph in graphs["graphs"].items():
        for edge in graph["edges"]:
            assert edge["edge_id"] not in edge_ids
            edge_ids.add(edge["edge_id"])
            assert edge["from"] in all_nodes and edge["to"] in all_nodes
            assert edge["edge_id"] in graph["out"].get(edge["from"], [])
            assert edge["edge_id"] in graph["in"].get(edge["to"], [])
            if graph_name == "proof":
                reciprocal = edge["reciprocal_edge_id"]
                assert any(
                    other["edge_id"] == reciprocal
                    and other["from"] == edge["to"]
                    and other["to"] == edge["from"]
                    for other in graph["edges"]
                )
    assert len(edge_ids) == 26

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    )
    for name in lean_files:
        code = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(code) is None, name
    validation_code = code_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" in validation_code
    assert re.search(r"^(?:theorem|lemma|def)\s", validation_code, re.MULTILINE) is None
    for declaration in PROOF_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation_code
    assert f"assert_no_sorry {STATEMENT_DECLARATION}" in validation_code

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == RECIPE_ARGV
    assert spec["env_allowlist"] == {
        "HOME": "/tmp", "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1",
    }
    assert spec["timeout_seconds"] == 1200 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == ids
    assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"]))

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, (blob, source_digest, olean_digest) in MATHLIB_SOURCES.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / relative.replace(
            ".lean", ".olean"
        )
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(source) == source_digest and sha256(olean) == olean_digest

    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_bin = account_home / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(Path("/usr/bin/python3")) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path("/usr/bin/git")) == "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
    assert sha256(Path("/usr/bin/bwrap")) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], cwd=LEAN_ROOT)
    fixed_env = {
        "HOME": os.environ["HOME"],
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).strip()

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1070-validation-", dir="/tmp"))
    try:
        for name in (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
            "Validation.lean",
        ):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
            env = dict(fixed_env)
            env["HOME"] = str(tmp / "home")
            env["LEAN_PATH"] = f"{tmp}:{lean_path}" if module_path else lean_path
            return run([str(lean), "--trust=0", "-j1", "-t0", *args], cwd=tmp, env=env)

        statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
        anchor_output = isolated_lean(["AnchorAudit.lean"])
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
        )
        proof_output = isolated_lean(["-o", "Proof.olean", "Proof.lean"], module_path=True)
        validation_output = isolated_lean(["Validation.lean"], module_path=True)
    finally:
        shutil.rmtree(tmp)

    assert "Stage1Instances.THM_M_1070.IsLevyProcess" in statement_output
    assert reported_axioms(
        anchor_output,
        "Stage1Instances.THM_M_1070.AnchorAudit.hasIndepIncrements_iff_finiteFamily",
    ) == EXPECTED_AXIOMS
    assert reported_axioms(
        anchor_output,
        "Stage1Instances.THM_M_1070.AnchorAudit.pairwiseConsequence",
    ) == EXPECTED_AXIOMS
    for declaration in COMPOSITION_DECLARATIONS:
        assert reported_axioms(obligation_output, declaration) == EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert reported_axioms(validation_output, STATEMENT_DECLARATION) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 5
    combined_output = (
        statement_output + anchor_output + obligation_output + proof_output + validation_output
    )
    assert "declaration uses 'sorry'" not in combined_output and "sorryAx" not in combined_output
    assert "error:" not in combined_output

    if verify_outputs:
        assert receipt is not None and packet is not None
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == "provisional_worker_selftest"
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
        for name, expected in EXPECTED_INPUTS.items():
            assert receipt["inputs"][name] == expected, name
        assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
        assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
        assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
        assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
        assert receipt["recipe"] == spec
        assert receipt["result"]["supported_obligation_ids"] == []
        assert receipt["result"]["provisionally_closed_obligation_ids"] == []
        assert receipt["result"]["accepted_closed_obligation_ids"] == []
        assert receipt["result"]["root_closed"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["remaining_root_cut_set"] == REMAINING_ROOT_CUT
        assert receipt["known_failures"] == packet["known_failures"]
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert actual_changed_paths() == CHANGED_PATHS

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
