#!/usr/bin/env python3
"""Re-elaborate THM-M-1026 and distinguish its statement mutations."""

from __future__ import annotations

import hashlib
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = pathlib.Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_1026"
NAMES = [
    "GeneralizedCentralLimitTheorem",
    "MutationAllowsDegenerateLimit",
    "MutationAllowsZeroScale",
    "MutationGaussianOnly",
    "MutationNecessityOnly",
]


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    executable = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
    if re.search(r"\b(sorry|admit|axiom)\b|sorryAx", executable):
        raise SystemExit("forbidden proof gap in Statement.lean")

    run = subprocess.run(
        ["lake", "env", "lean", str(SOURCE)], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    if run.returncode:
        sys.stdout.write(run.stdout)
        return run.returncode

    rendered: dict[str, str] = {}
    for index, name in enumerate(NAMES):
        marker = f"def {NAMESPACE}.{name} : Prop :="
        start = run.stdout.find(marker)
        if start < 0:
            raise SystemExit(f"missing elaborated output for {name}")
        later = [run.stdout.find(f"def {NAMESPACE}.{n} : Prop :=", start + 1)
                 for n in NAMES[index + 1:]]
        ends = [position for position in later if position >= 0]
        rendered[name] = " ".join(run.stdout[start:min(ends) if ends else None].split())

    canonical = rendered[NAMES[0]]
    collisions = [name for name in NAMES[1:] if rendered[name] == canonical]
    if collisions:
        raise SystemExit(f"mutation not distinguished: {', '.join(collisions)}")
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    print(f"canonical expression SHA-256: {digest}")
    print("mutation distinction: ok (removed hypothesis, boundary, domain, binder scope)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
