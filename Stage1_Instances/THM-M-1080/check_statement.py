#!/usr/bin/env python3
"""Re-elaborate and fingerprint the THM-M-1080 statement and its mutations."""

from __future__ import annotations

import hashlib
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
STATEMENT = ROOT / "Stage1_Instances" / "THM-M-1080" / "Statement.lean"
NAMES = [
    "AzumaUpperTail",
    "ExpandedSourceShape",
    "MutationRemovedMartingale",
    "MutationChangedDomain",
    "MutationUniformBinderScope",
    "MutationPositiveThresholdOnly",
]


def main() -> int:
    source = STATEMENT.read_text(encoding="utf-8")
    code = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
    if re.search(r"\b(sorry|admit|axiom)\b|sorryAx", code):
        raise SystemExit("forbidden proof-gap declaration in Statement.lean")

    run = subprocess.run(
        ["lake", "env", "lean", str(STATEMENT)],
        cwd=LEAN_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        return run.returncode

    rendered: dict[str, str] = {}
    for index, name in enumerate(NAMES):
        marker = f"Stage1Instances.THM_M_1080.{name}"
        start = run.stdout.find(marker)
        if start < 0:
            raise SystemExit(f"missing elaborated output for {name}")
        later = [run.stdout.find(f"Stage1Instances.THM_M_1080.{n}", start + 1)
                 for n in NAMES[index + 1 :]]
        ends = [position for position in later if position >= 0]
        rendered[name] = " ".join(run.stdout[start : min(ends) if ends else None].split())

    canonical = rendered[NAMES[0]]
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    collisions = [name for name in NAMES[2:] if rendered[name] == canonical]
    if collisions:
        raise SystemExit(f"mutation not distinguished: {', '.join(collisions)}")
    if "∑ k ∈ Finset.range n" not in rendered["ExpandedSourceShape"]:
        raise SystemExit("expanded source shape did not print the explicit squared-bound sum")
    print(f"canonical expression SHA-256: {digest}")
    print("checked expansion: ok")
    print("mutation distinction: ok (hypothesis, domain, binder scope, threshold boundary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
