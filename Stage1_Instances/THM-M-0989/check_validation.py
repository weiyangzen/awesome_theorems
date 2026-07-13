#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0989-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0989"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0989-VALIDATION"
THEOREM = "THM-M-0989"
BASE_REVISION = "64ac616628d97140f9ca64eff0298e51d7f4e9ff"
BASE_TREE = "9ef0acd5b747e34cacb82c6f21fce1e1380e0cf2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
DENOMINATOR_SHA256 = "c5d0b41c35c0759e11055611925021d6c2e38fc251da666e8f3afe238eccdc15"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M0989-ROOT",
    "M0989-S-DEFINITIONS",
    "M0989-S-MEAS",
    "M0989-S-FOUNDATION",
    "M0989-C-FACTOR",
    "M0989-N-MOMENTS",
    "M0989-L-INFINITESIMAL",
    "M0989-L-TRUNCATE",
    "M0989-L-TAYLOR",
    "M0989-L-PRODUCT",
    "M0989-T-CHARFUN",
    "M0989-T-LEVY",
    "M0989-T-ASSEMBLE",
]
OBSERVED_IDS = MACHINE_IDS + ["M0989-X-PROVENANCE"]
EXPECTED_INPUTS = {
    "Statement.lean": "ccdd546c1997d1cd38879a6df2ac9acbb8aaf01b7565ce19625c981d7b32772a",
    "ObligationTree.lean": "57005c9602c9d27448871dd595af49980f26b938170b613c08e41ff53c1ecadb",
    "Proof.lean": "d470547c10d1d2eff25cc6b5780a350b4e71fc4a3ad92891fb2d764f2f37808f",
    "ProdExp.lean": "d70c57420bd79d8a6a8a402db14690ccac00ceafa79559afb3f8b1a398c9f622",
    "CharFunBound.lean": "6c94cf73831e55bb29eecbdf0927622d398b09c4b84d0d15195aa3d041e1b02f",
    "LindebergArray.lean": "4f2c86248a6aa9719600b7bf96ddc27a7c60dfea59342a2ef1ab086c4a65a16a",
    "Validation.lean": "7613977ba1f7f627186793886e817c3ff60a998a89ad52c8effbe706c56ff9a2",
    "intake.json": "62607c2158440dfca2eac4efc2a664ba028bed5969888cbd745800370cb471a8",
    "obligation-registry.json": "dbeb43c1d461ad3b81a93e90e974116384f62edb423c7eb4be6a1d0639cca6a6",
    "typed-graphs.json": "8e28d1471ea94e6e2272767433a3355e963e78d35419810e59adcc2277873502",
    "validation-specs.json": "4320e91edc7a1f94049f0cfb19bff716b0b9817fe4803774433dfbbbf3ef0a16",
    "proof-receipt.json": "459b40b0c04014f4ab7d6edbb6e0d5771666b641231e40666dbb5bd3c826874c",
    "check_proof.py": "d3d327baed7f766fde782e8f143790816ace901ce2b58886c26231a0b15b6d0c",
    "check_proof.sh": "a6c6101096fb906d5f082f6ad558219314ca40fd59cba235fd5929b01d90e547",
    "check_validation.sh": "e9e74bbf536650c4aa4eed21361592566ce6ad55f7a63083208787187a2e4a02",
    "validation-spec.json": "08cde44c9b509a3c7ba1f0e4f34301c3cba81d390189a89c8ca9901152bc2852",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_WORKER_INPUT_HASHES = {
    ".stage1-worker-selftest.json": "f6d2cde65ec7f00c00fdc9a0d2b91909ce1c2226fe8ce28dda5f0cb4a86ecafb",
    "Stage1_Instances/THM-M-0989/Validation.lean": EXPECTED_INPUTS["Validation.lean"],
    "Stage1_Instances/THM-M-0989/check_validation.py": "SELF_HASH_STRUCTURALLY_BOUND",
    "Stage1_Instances/THM-M-0989/check_validation.sh": EXPECTED_INPUTS["check_validation.sh"],
    "Stage1_Instances/THM-M-0989/validation-phase.md": "b970ec9258d7af9fe511b2a1d5b7d2fb7d73847056281496bbe658b271309693",
    "Stage1_Instances/THM-M-0989/validation-spec.json": EXPECTED_INPUTS["validation-spec.json"],
}
EXPECTED_WORKER_PATCH_HASHES = {
    ".stage1-worker-selftest.json": "eb8ca3524268d121a965aea39f4edb6325568a4e9cd7dea960b6a7d8bb065d22",
    "Stage1_Instances/THM-M-0989/Validation.lean": "d32c912afe6ff97688267e27f44a7a798a129eb4744e6ae65787accdf9452a58",
    "Stage1_Instances/THM-M-0989/check_validation.py": "SELF_HASH_STRUCTURALLY_BOUND",
    "Stage1_Instances/THM-M-0989/check_validation.sh": "44d487958d6247b9568b0fc10be1a1e5937708d9f9cfa651479e335246f949dc",
    "Stage1_Instances/THM-M-0989/validation-phase.md": "7738d6bf8b3311e1f3571197bcefbe0ac88dae5ebacbffb2197a654a26285f79",
    "Stage1_Instances/THM-M-0989/validation-spec.json": "8c757952f85adf6fc60fcff212c084d9addec8739d73e004bb356e03d1e0b056",
}
PROVENANCE = {
    "Mathlib/Probability/Independence/CharacteristicFunction.lean": {
        "blob": "5011e757544576dc1e74835578e7607d7f66a690",
        "source": "59038431e678c8e44b7dd26f39cde99e9d68ea781f5fb8e0b595c83f05b23fe2",
        "olean": "ea77f41ff916655a04dd91ff76510576a7649aef46da1ae55e1dc4f34e8c0d95",
    },
    "Mathlib/Probability/Distributions/Gaussian/Real.lean": {
        "blob": "f5795fbfb92475879b67b0ee8577687575a82258",
        "source": "f5321db08f0156c5a12e15986d2ced9108183c907e3082d2566da8ef8da931a8",
        "olean": "b5894530bc315c897142ff650c774ed5ee3180b1df45690021fdd830e6e82ea4",
    },
    "Mathlib/MeasureTheory/Measure/LevyConvergence.lean": {
        "blob": "fc0bf2a7054634763040aa9bbcaae5f2c93b8d5f",
        "source": "54fa4a3baec8a8ab916524dd63c52a6da70bc919031e20318b198fa20755fff8",
        "olean": "9f5a27181b909026ed757f7fd257f83407fdcbf3315cb0560c1a65e22e994865",
    },
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
    "PASS THM-M-0989 narrow validation",
    "PASS network-isolated kernel replay: six proof modules, exact root, and final-composition replay elaborated with --trust=0",
    "PASS trust observation: 25 declaration reports contain exactly propext, Classical.choice, and Quot.sound; transitive closure has no unsafe or unexpected bodyless declarations",
    "PASS selected provenance: frozen hashes, three mathlib source/blob/olean boundaries, clean dependency pin, remote, license, and tool identities agree",
    "PASS hygiene and architecture: parser-aware sorry checks, local prohibited scan, proof receipt, denominator, and frozen graph boundary agree",
    "FAIL CLOSED authority/foundation: proof master acceptance, a canonical expression hash, and an accepted versioned foundation/TCB profile remain open at H2/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: the final-composition replay shares analytic bodies, this worker, checkout, kernel, and cache; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
TIMEOUT_SECONDS = 1800.0
SUBPROCESS_ENV = {
    "HOME": os.environ.get("HOME", ""),
    "PATH": os.environ.get("PATH", ""),
    "LANG": "C",
    "LC_ALL": "C",
    "NO_COLOR": "1",
    "TZ": "UTC",
}

if not __debug__:
    raise RuntimeError("validation requires Python assertions (__debug__ must be true)")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation exceeded its 1800-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=SUBPROCESS_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_lean_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        char = source[index]
        pair = source[index:index + 2]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def changed_paths() -> set[str]:
    output = git("status", "--short", "--untracked-files=all")
    return {
        line[3:]
        for line in output.splitlines()
        if line[3:] == ".stage1-worker-selftest.json"
        or line[3:].startswith(f"Stage1_Instances/{THEOREM}/")
    }


def all_changed_paths() -> set[str]:
    output = git("status", "--short", "--untracked-files=all")
    return {line[3:] for line in output.splitlines()}


def no_index_patch_sha256(path: Path) -> str:
    relative = path.relative_to(ROOT)
    result = subprocess.run(
        ["git", "diff", "--no-index", "--binary", "/dev/null", str(relative)],
        cwd=ROOT,
        env=SUBPROCESS_ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    assert result.returncode == 1, path
    return hashlib.sha256(result.stdout).hexdigest()


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 269 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0989-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0989-PROOF")
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    assert intake["canonical_formal_target"]["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0989.Statement"
    )
    assert intake["canonical_formal_target"]["elaborated_expression_hash"] is None
    assert registry["root_obligation_id"] == "M0989-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0989-PROOF"
    assert proof_receipt["canonical_target"] == "Stage1Instances.THM_M_0989.Statement"
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOMS
    assert proof_receipt["accepted"] is False
    upstream = {
        row["path"]: row for row in proof_receipt["proof_body"]["upstream_sources"]
    }
    assert set(upstream) == {
        "Clt/ProdExp.lean", "Clt/CharFunBound.lean", "Clt/Lindeberg.lean",
    }
    for path, source_hash in {
        "Clt/ProdExp.lean": "6068339f52c68388a0ce45dfd30b4801de1aab5421ef98e1fc19a81cba05851c",
        "Clt/CharFunBound.lean": "2c04f861f5c5faf0622f6c39157420f67f4e41d2f5a3b8acc8282461897143e1",
        "Clt/Lindeberg.lean": "64020a1982986ca506b3623ff7b1f9a2bad2a57edb764ef0689ddda0ab43da3c",
    }.items():
        row = upstream[path]
        assert row["repository"] == "https://github.com/patrickrd/CLT-lindeberg"
        assert row["revision"] == "82249ccfc05c0d97b86f33fce2582f0bf4ff9c06"
        assert row["tree"] == "7d11c8e993bdecb4b072a9369ee6858db6728c61"
        assert row["source_sha256"] == source_hash
        assert row["license"] == "Apache-2.0"
        assert row["license_sha256"] == (
            "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
        )
        assert row["relationship"] == "derived_repo_local_adaptation"
    assert frozen_specs["item_id"] == "S56-M-0989-OBLIGATION_TREE"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean", "ProdExp.lean",
        "CharFunBound.lean", "LindebergArray.lean", "Validation.lean",
    ):
        source = without_lean_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source construct in {name}"
    validation_source = without_lean_comments((HERE / "Validation.lean").read_text())
    assert "rowLawCharFunConverges_proof A" in validation_source
    assert "lindebergFeller_exact" not in validation_source.split("theorem lindebergFeller_composition_replay", 1)[1].split("assert_no_sorry", 1)[0]

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for source_name, expected in PROVENANCE.items():
        source = MATHLIB / source_name
        olean = MATHLIB / ".lake/build/lib/lean" / source_name.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source"]
        assert sha256(olean) == expected["olean"]
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    python = Path(os.path.realpath(os.sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert "4.29.0" in run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert LEAN_COMMIT in run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run(["lake", "--version"], cwd=LEAN_ROOT)
    expected_tools = {
        lean: "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        lake: "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        python: "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        git_path: "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        bwrap: "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    }
    for path, expected in expected_tools.items():
        assert path.is_file() and sha256(path) == expected, path

    tree_output = run(["python3", str(HERE / "check_obligation_tree.py")])
    assert "PASS THM-M-0989 obligation tree: 15 obligations, 32 typed edges" in tree_output
    assert DENOMINATOR_SHA256 in tree_output
    assert "root closure: open (M3)" in tree_output

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    assert runner_output.count("depends on axioms:") == 25
    assert runner_output.count("Declarations are sorry-free!") == 5
    assert "VALIDATION_CLOSURE declarations=53251 modules=1748" in runner_output
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in runner_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in runner_output
    assert "VALIDATION_CLOSURE unsafe=[]" in runner_output
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-0989-VALIDATION-narrow-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["env_allowlist"] == {
        "HOME": (
            "inherited only for pinned elan/lake discovery; not visible to "
            "network-isolated Lean subprocesses"
        ),
        "LANG": "C",
        "LC_ALL": "C",
        "NO_COLOR": "1",
        "PATH": (
            "inherited only for content-hash-verified Python, Git, Bubblewrap, "
            "Lean, and Lake discovery"
        ),
        "TZ": "UTC",
    }
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]
    assert spec["timeout_seconds"] == 1800 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert "Host-side hash, pin, structure, and provenance checks make no network requests" in (
        spec["network_enforcement"]
    )
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]
    assert spec["covered_obligation_ids"] == OBSERVED_IDS
    assert len(spec["covered_declarations"]) == 24
    assert len(set(spec["covered_declarations"])) == 24

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["depends_on"] == ["S56-M-0989-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["owner"] == "THM-M-0989 validation lane"
    assert receipt["reviewer"] == "independent Stage1 integration lane"
    assert receipt["exact_statement_delta"].startswith("none;")
    assert "confined to Stage1_Instances/THM-M-0989" in receipt["ownership_and_change_impact"]
    repository_state = receipt["repository_state"]
    assert repository_state["dirty"] is True
    assert repository_state["tracked_patch_sha256"] is None
    assert repository_state["tracked_patch_bytes"] == 0
    assert repository_state["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert repository_state["canonical_lake_symlink_target_classification"] == (
        "scheduler-provided canonical pinned .lake outside the worker clone"
    )
    assert repository_state["canonical_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(ROOT / "Formalizations/Lean/.lake").encode()
    ).hexdigest()
    receipt_input_hashes = repository_state["untracked_input_hashes"]
    receipt_patch_hashes = repository_state["untracked_no_index_patch_hashes"]
    assert set(receipt_input_hashes) == set(EXPECTED_WORKER_INPUT_HASHES)
    assert set(receipt_patch_hashes) == set(EXPECTED_WORKER_PATCH_HASHES)
    for relative, expected in EXPECTED_WORKER_INPUT_HASHES.items():
        if expected == "SELF_HASH_STRUCTURALLY_BOUND":
            assert receipt_input_hashes[relative] == (
                "self_hash_excluded; current bytes structurally executed by worker; "
                "integration-lane review required"
            )
            continue
        assert receipt_input_hashes[relative] == expected
        assert sha256(ROOT / relative) == expected, relative
    for relative, expected in EXPECTED_WORKER_PATCH_HASHES.items():
        if expected == "SELF_HASH_STRUCTURALLY_BOUND":
            assert receipt_patch_hashes[relative] == (
                "self_hash_excluded; current patch structurally executed by worker; "
                "integration-lane review required"
            )
            continue
        assert receipt_patch_hashes[relative] == expected
        assert no_index_patch_sha256(ROOT / relative) == expected, relative
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0989.Statement",
        "terminal_root_declaration": "Stage1Instances.THM_M_0989.lindebergFeller_exact",
        "elaborated_expression_sha256": None,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["covered_obligation_ids"] == OBSERVED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["covered_declarations"] == spec["covered_declarations"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_path)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    assert provenance["local_terminal_declaration"] == (
        "Stage1Instances.THM_M_0989.lindebergFeller_exact"
    )
    assert provenance["mathlib_origin"] == {
        "remote": MATHLIB_REMOTE,
        "revision": MATHLIB_REVISION,
        "tree_hash": MATHLIB_TREE,
        "license_sha256": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
    }
    selected = {row["file"]: row for row in provenance["selected_boundaries"]}
    assert set(selected) == set(PROVENANCE)
    for source_name, expected in PROVENANCE.items():
        assert selected[source_name]["source_blob"] == expected["blob"]
        assert selected[source_name]["source_sha256"] == expected["source"]
        assert selected[source_name]["olean_sha256"] == expected["olean"]
    assert "does not content-address every transitive source" in provenance["transitive_boundary"]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == (
        "self_hash_excluded; current bytes structurally executed by worker; "
        "integration-lane review required"
    )
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    result = receipt["result"]
    assert result["exit_code"] == 0 and result["kernel_replay"] == "provisional_pass"
    assert result["axioms"] == EXPECTED_AXIOMS and result["axiom_probe_count"] == 25
    assert result["parser_aware_sorry_probe_count"] == 5
    assert result["placeholder_scan"] == "pass"
    assert result["transitive_declaration_count"] == 53251
    assert result["transitive_module_count"] == 1748
    assert result["unexpected_bodyless_declarations"] == []
    assert result["unsafe_declarations"] == []
    assert result["selected_provenance"] == "provisional_pass"
    assert result["complete_transitive_provenance_tcb"] == "fail_closed"
    assert result["canonical_expression_fingerprint_gate"] == "fail_closed"
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed_locally"] is True
    assert result["accepted_root_closed"] is False
    assert result["accepted_machine_debt"] == "M3"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    run_evidence = receipt["run_evidence"]
    started_at = datetime.fromisoformat(run_evidence["started_at"])
    ended_at = datetime.fromisoformat(run_evidence["ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at < ended_at == validated_at
    assert (ended_at - started_at).total_seconds() <= spec["timeout_seconds"]
    assert run_evidence["exit_code"] == 0
    assert run_evidence["stdout_sha256"] == (
        "a57db64c9ba9380575ee5efe36e4b6607c46732d25973fec29a6ca1d42cdb6ca"
    )
    assert run_evidence["stdout_bytes"] == 1141 and run_evidence["stdout_lines"] == 9
    assert run_evidence["stderr_sha256"] == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert run_evidence["stderr_bytes"] == 0
    assert receipt["first_failed_gate"] == "dependency.S56-M-0989-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["known_failures"] == packet["known_failures"]
    assert receipt["changed_paths"] == packet["changed_paths"]
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]" and set(packet["changed_paths"]) == CHANGED_PATHS
    assert changed_paths() == CHANGED_PATHS
    assert all_changed_paths() == CHANGED_PATHS | {"Formalizations/Lean/.lake"}
    assert all(isinstance(row, dict) for row in packet["commands"])
    assert all(isinstance(row.get("argv"), list) and row.get("exit_code") == 0
               for row in packet["commands"])
    command_text = json.dumps(packet["commands"], sort_keys=True)
    for command in (
        "check_stage1_standard.py", "stage1_target.py", "check_obligation_tree.py",
        "check_proof.sh", "check_validation.sh", "check_validation.py", "git", "diff",
    ):
        assert command in command_text
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
