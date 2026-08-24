#!/usr/bin/env python3
"""Positive and isolated mutation tests for the Erdős parent-join checker."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CHECKER = REPO_ROOT / "Docs/catalog/v5/tools/check_erdos_parent_join_v5_5.py"
ARTIFACT_ROOT = REPO_ROOT / "Docs/catalog/v5/curation/erdos_parent_join_v5_5"
SNAPSHOT = REPO_ROOT / "Docs/catalog/v5/sources/erdosproblems-status-af90db96.json"
RELEASE_ROOT = REPO_ROOT / "Docs/catalog/v5/releases/5.4"


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def run_checker(*extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), *extra],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require_rejection(name: str, result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode == 0:
        raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> int:
    baseline = run_checker()
    if baseline.returncode != 0:
        raise AssertionError(f"baseline checker failed:\n{baseline.stdout}\n{baseline.stderr}")

    rejected = []
    with tempfile.TemporaryDirectory(prefix="erdos-parent-join-mutations-") as scratch_text:
        scratch = Path(scratch_text)

        mutated_artifacts = scratch / "artifacts"
        shutil.copytree(ARTIFACT_ROOT, mutated_artifacts)
        join_path = mutated_artifacts / "parent-erdos-join.jsonl"
        lines = join_path.read_text(encoding="utf-8").splitlines()
        first = json.loads(lines[0])
        first["exact_join"]["key"] = "999999"
        lines[0] = canonical(first)
        join_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        require_rejection(
            "joined_problem_number",
            run_checker("--artifact-root", str(mutated_artifacts)),
        )
        rejected.append("joined_problem_number")

        mutated_snapshot = scratch / "status-snapshot.json"
        snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        snapshot["records"][0]["informal_status"]["state"] = "proved"
        mutated_snapshot.write_text(canonical(snapshot) + "\n", encoding="utf-8")
        require_rejection(
            "pinned_status_row",
            run_checker("--snapshot", str(mutated_snapshot)),
        )
        rejected.append("pinned_status_row")

        mutated_release = scratch / "release-5.4"
        mutated_release.mkdir()
        for name in ("Claim_Catalog.json", "Strict_Conjecture_Ledger.json", "Release_Manifest.json"):
            shutil.copy2(RELEASE_ROOT / name, mutated_release / name)
        ledger_path = mutated_release / "Strict_Conjecture_Ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["strict_credits"][0]["grants_strict_conjecture_credit"] = False
        ledger_path.write_text(canonical(ledger) + "\n", encoding="utf-8")
        require_rejection(
            "parent_strict_credit",
            run_checker("--release-root", str(mutated_release)),
        )
        rejected.append("parent_strict_credit")

    print(
        canonical(
            {
                "baseline": "passed",
                "mutations_rejected": rejected,
                "test": "erdos_parent_join_v5_5",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
