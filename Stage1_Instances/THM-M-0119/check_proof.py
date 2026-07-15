#!/usr/bin/env python3
"""Fail-closed proof-phase checks for the frozen THM-M-0119 countermodel."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0119-PROOF"
THEOREM = "THM-M-0119"
BASE_REVISION = "472dc79eb4d406a6707691193fbe3ab58d0f0cc4"
BASE_TREE = "881d873727dc80435119839b8e60e9e9c2cfb208"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/proof-recheck-2026-07-15-head-472dc79e-slot17.json",
    f"Stage1_Instances/{THEOREM}/proof-recheck-2026-07-15-head-472dc79e-slot17.md",
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


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=900,
    )
    sys.stdout.write(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def parse_axioms(output: str, declaration: str) -> list[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]*)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return [part.strip() for part in match.group(1).split(",") if part.strip()]


def main() -> None:
    packet = load(ROOT / ".stage1-worker-selftest.json")
    evidence = load(
        HERE / "proof-recheck-2026-07-15-head-472dc79e-slot17.json"
    )
    task_dag = load(HERE / "task-dag.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    proof_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert proof_task["state"] == "open"
    assert proof_task["accepted_receipt_ids"] == []

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM
    assert packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["known_failures"] == evidence["known_failures"]

    assert evidence["item_id"] == ITEM and evidence["theorem_id"] == THEOREM
    assert evidence["base_revision"] == BASE_REVISION
    assert evidence["base_tree"] == BASE_TREE
    assert evidence["verdict"] == "blocked"
    assert evidence["state"] == "[_]"
    assert evidence["root_closed"] is False
    assert evidence["proof_phase_complete"] is False
    assert evidence["theorem_complete"] is False
    assert evidence["selftest_manifest_written"] is True
    assert set(evidence["changed_paths"]) == EXPECTED_CHANGED_PATHS

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for filename in ("Statement.lean", "Proof.lean", "ObligationTree.lean"):
        source = (HERE / filename).read_text(encoding="utf-8")
        assert prohibited.search(without_comments(source)) is None, filename

    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == evidence["environment"][
        "mathlib_revision"
    ]
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == evidence[
        "environment"
    ]["mathlib_tree"]
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_DIR).strip()
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_DIR
    ).strip()
    env = os.environ.copy()
    env["LC_ALL"] = "C.UTF-8"
    env["TZ"] = "Asia/Shanghai"
    env["LEAN_NUM_THREADS"] = "1"
    env["LEAN_PATH"] = lean_path

    with tempfile.TemporaryDirectory(prefix="thm-m-0119-proof-") as tmp_name:
        tmp = Path(tmp_name)
        run(
            [
                lean,
                "--trust=0",
                "-t0",
                "-o",
                str(tmp / "Statement.olean"),
                "Statement.lean",
            ],
            cwd=HERE,
            env=env,
        )
        proof_env = env.copy()
        proof_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        proof_output = run(
            [lean, "--trust=0", "-t0", "Proof.lean"], cwd=HERE, env=proof_env
        )
        obligation_output = run(
            [lean, "--trust=0", "-t0", "ObligationTree.lean"],
            cwd=HERE,
            env=env,
        )

    negative_declaration = (
        "Stage1Instances.THMM0119.not_kawamataViehwegVanishingTarget"
    )
    assert parse_axioms(proof_output, negative_declaration) == EXPECTED_AXIOMS
    for declaration in (
        "Stage1Instances.THMM0119.ObligationTree.positive_degrees_compose",
        "Stage1Instances.THMM0119.ObligationTree.implication_compose",
    ):
        assert (
            f"'{declaration}' does not depend on any axioms" in obligation_output
        ), declaration

    actual_changed = {
        line[3:]
        for line in subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == EXPECTED_CHANGED_PATHS, actual_changed

    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0119 proof phase: exact frozen target has a checked countermodel")
    print("positive root closure: blocked; theorem_complete=false")


if __name__ == "__main__":
    main()
