#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0419-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0419"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0419-VALIDATION"
THEOREM = "THM-M-0419"
BASE_REVISION = "bd65bfeeea414dd3cfe270a499dca2b9fd65e34c"
BASE_TREE = "d78c646a63fe7e8004519c621319cbbef7adbb9c"
EXPRESSION_SHA256 = "d30ce90a242e9fe3900ec73e893184ad8878c5b90f5362a4f70ca3846342faeb"
DENOMINATOR_SHA256 = "84b22238b8c01210c72a112261776db3e96002fde700709d0336a2d07d799f71"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_CUT = [
    "M0419-B-INDUCTION",
    "M0419-L-TAME",
    "M0419-L-WILD-ODD",
    "M0419-L-WILD-TWO",
    "M0419-T-GLOBAL",
]
EXPECTED_INPUTS = {
    "Statement.lean": "db9efe3e6fbf82023500558480b83a88b583a51444272f2ee642a05fd38a0422",
    "ObligationTree.lean": "ac4ad27955b95ee77f2747cde2aea5f0552de2e7a009fb0b4aea39a8d8a38951",
    "Proof.lean": "1a42f62f56c5f62df0d9e5ee245f68a77fb44e7e42240dcbb9db7e5863220f7a",
    "statement.json": "ee0354ca1c5bc7ea046199e6c19e90b88beddfd51a0f3540d029f84dd0fee5de",
    "anchor-audit.json": "e2c1faabe061196d98145375329356da99ee7970be16728dec5f8e7e7f133f70",
    "obligation-registry.json": "860e52d35f41f870858a3d2d1b230b7a2418bcf17c374efa618d62f93bd1dd7b",
    "typed-graphs.json": "a4385d65ac70f1d772b4e8d1d3f06607a5ba893534c555d70488d1c7f78f85ae",
    "validation-specs.json": "8baa49ab69d0fdc1e1038aa7e9289c905e6cd1326246ff387c57ecc651a8e574",
    "proof-phase.json": "1f61e2a0371665484a49a30dcdc9d7593da600f26f31018c05e58c9f6a122f85",
    "proof-receipt.json": "c28bfe7d41195ff701a50c0f5eede7f5720feb4f21869d32b651f7557004ff59",
    "proof-recheck-2026-07-15-head-b1a5b03c-slot14.json":
        "2b6a10e46174660a9d5647561a754106afaf173612b52b1dc40dece9801bca29",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0419/Validation.lean",
    "Stage1_Instances/THM-M-0419/check_validation.py",
    "Stage1_Instances/THM-M-0419/validation-blocker.json",
    "Stage1_Instances/THM-M-0419/validation-phase.md",
    "Stage1_Instances/THM-M-0419/validation-receipt.json",
    "Stage1_Instances/THM-M-0419/validation-spec.json",
]
SUMMARY_LINES = (
    "PASS THM-M-0419 narrow validation",
    "PASS kernel replay: exact statement, frozen conditional compositions, partial proof transport, and differential transport elaborated at trust zero",
    "PASS trust observation: checked declarations report exactly propext, Classical.choice, and Quot.sound; closure reports no bodyless nonaxioms or unsafe declarations",
    "PASS selected provenance: frozen hashes, clean pinned mathlib revision/tree/origin/license, Cyclotomic.Basic source/blob/olean, and tool identities agree",
    "FAIL CLOSED dependency/root: proof is worker-provisional and five mathematical packages remain the exact-root cut; accepted root stays H1/M3/R3",
    "FAIL CLOSED assurance: accepted foundation profile, complete transitive provenance/TCB/SBOM closure, H0, and independent R0 review are absent",
    "FAIL CLOSED hermetic/independent: shared warm .lake and same-worker reconstruction are neither cold offline replay nor distinct signed verification; audit_complete=false; theorem_complete=false",
)
TIMEOUT_SECONDS = 600.0
STARTED = time.monotonic()


def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation exceeded its 600-second bound")
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
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
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


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]",
        re.DOTALL,
    )
    match = pattern.search(output)
    if match is None:
        assert re.search(
            rf"'[^'\n]*{re.escape(declaration)}' does not depend on any axioms", output
        ), declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def bwrap_lean(
    bwrap: str,
    lean: str,
    tmp: Path,
    lean_path: str,
    source: str,
    output: str | None = None,
) -> str:
    env = {
        "HOME": "/tmp/validation-home",
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": f"{tmp}:{lean_path}",
    }
    argv = [
        bwrap,
        "--ro-bind", "/", "/",
        "--bind", str(tmp), str(tmp),
        "--dev", "/dev",
        "--proc", "/proc",
        "--unshare-net",
        "--die-with-parent",
        "--chdir", str(tmp),
        lean,
        "--trust=0",
        "-t0",
    ]
    if output is not None:
        argv.extend(["-o", output])
    argv.append(source)
    return run(argv, cwd=tmp, env=env)


def main(worker_packet: Path) -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet = load(worker_packet)
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_phase = load(HERE / "proof-phase.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 74 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 74,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0419-PROOF"],
        "owned_paths": ["Stage1_Instances/THM-M-0419"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0419-PROOF")
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"stale tool input: {name}"
    assert statement["elaborated_output_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert closure["minimal_open_proof_cut_set"] == ROOT_CUT
    assert proof_phase["proposed_closed_obligation_ids"] == ["M0419-C-CYCLOTOMIC-IDENTIFY"]
    assert proof_phase["accepted_closed_obligation_ids"] == []
    assert proof_phase["remaining_root_cut_set"] == ROOT_CUT
    assert proof_phase["root_closed"] is proof_phase["audit_complete"] is proof_phase["theorem_complete"] is False
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["remaining_root_cut_set"] == ROOT_CUT
    assert frozen_specs["item_id"] == "S56-M-0419-OBLIGATION_TREE"
    assert all(row["closure_credit"] is False for row in frozen_specs["recipes"])

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited construct in {name}"
    differential = without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in ("import Proof", "import ObligationTree", "Proof.cyclotomicIdentify"):
        assert forbidden not in differential
    assert "theorem differentialCyclotomicIdentify" in differential
    assert "assert_no_sorry differentialCyclotomicIdentify" in differential

    lake_manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in lake_manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.is_dir(), "pinned mathlib artifacts are missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    cyclotomic_source = MATHLIB / "Mathlib/NumberTheory/Cyclotomic/Basic.lean"
    cyclotomic_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/Cyclotomic/Basic.olean"
    assert git("rev-parse", "HEAD:Mathlib/NumberTheory/Cyclotomic/Basic.lean", cwd=MATHLIB) == \
        "28802271b5329feb709c34f17b06614bdd90d4b7"
    assert sha256(cyclotomic_source) == "e608a9b38ee0191c076cf22fc912bea5050adedc1b086c76e08756a4ac55484a"
    assert sha256(cyclotomic_olean) == "0689ef737de10fd71ee50c8ee406d4d297460f3813f78f4826c90feb457db9e8"
    assert cyclotomic_olean.stat().st_size == 533280
    terminal = cyclotomic_source.read_text(encoding="utf-8")
    assert "noncomputable def algEquiv [IsCyclotomicExtension S K L]" in terminal
    assert "nonempty_algEquiv_adjoin_of_isSepClosed" in terminal

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for denied-network replay"
    python = Path(os.path.realpath("/usr/bin/python3"))
    git_exe = Path(os.path.realpath(shutil.which("git") or ""))
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(Path(bwrap)) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(git_exe) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"

    with tempfile.TemporaryDirectory(prefix="m0419-validation-") as tmp_name:
        tmp = Path(tmp_name)
        (tmp / "validation-home").mkdir()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_output = bwrap_lean(bwrap, lean, tmp, lean_path, "Statement.lean", "Statement.olean")
        obligation_output = bwrap_lean(
            bwrap, lean, tmp, lean_path, "ObligationTree.lean", "ObligationTree.olean"
        )
        proof_output = bwrap_lean(bwrap, lean, tmp, lean_path, "Proof.lean", "Proof.olean")
        validation_output = bwrap_lean(bwrap, lean, tmp, lean_path, "Validation.lean")

    assert EXPRESSION_SHA256 == hashlib.sha256(statement_output.encode()).hexdigest()
    for declaration in (
        "cyclicPrimePower_of_branches",
        "localContainment_of_induction",
        "checkedPositiveTransport",
        "checkedRootAssembly",
        "root_of_packages",
    ):
        assert printed_axioms(obligation_output, declaration) == EXPECTED_AXIOMS
    for declaration in ("cyclotomicIdentify", "IsCyclotomicExtension.algEquiv"):
        assert printed_axioms(proof_output, declaration) == EXPECTED_AXIOMS
    for declaration in ("differentialCyclotomicIdentify", "IsCyclotomicExtension.algEquiv"):
        assert printed_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 2
    combined = obligation_output + proof_output + validation_output
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+).*?"
        r"VALIDATION_CLOSURE axioms=\[propext, Classical.choice, Quot.sound\].*?"
        r"VALIDATION_CLOSURE bodyless_nonaxioms=\[\].*?"
        r"VALIDATION_CLOSURE unsafe=\[]",
        validation_output,
        re.DOTALL,
    )
    assert closure_match is not None
    assert (int(closure_match.group(1)), int(closure_match.group(2))) == (33153, 1178)

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0419-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == []
    assert recipe["validated_partial_progress_toward_obligation_ids"] == [
        "M0419-C-CYCLOTOMIC-IDENTIFY"
    ]
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["proposed_state"] == "[_]" and receipt["verdict"] == "blocked"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["provisionally_closed_obligation_ids"] == []
    assert receipt["result"]["remaining_root_cut_set"] == ROOT_CUT
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["trust"]["validation_closure"] == {
        "declarations": 33153,
        "modules": 1178,
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for name in ("Validation.lean", "check_validation.py", "validation-spec.json"):
        assert receipt["inputs"][name] == sha256(HERE / name)
    assert receipt["changed_paths"] == blocker["changed_paths"] == packet["changed_paths"] == CHANGED_PATHS
    assert receipt["known_failures"] == blocker["known_failures"] == packet["known_failures"]
    assert packet == {
        "item_id": ITEM,
        "changed_paths": CHANGED_PATHS,
        "commands": packet["commands"],
        "output_summary": packet["output_summary"],
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    status = git("status", "--short", "--untracked-files=all").splitlines()
    actual = {line[2:].lstrip() for line in status}
    actual.discard("Formalizations/Lean/.lake")
    assert actual == set(CHANGED_PATHS)
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["remaining_root_cut_set"] == ROOT_CUT
    assert blocker["validation_phase_self_tested"] is True
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, default=ROOT / ".stage1-worker-selftest.json")
    args = parser.parse_args()
    packet_path = args.worker_packet
    if not packet_path.is_absolute():
        packet_path = ROOT / packet_path
    main(packet_path)
