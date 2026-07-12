#!/usr/bin/env python3
"""Fail-closed local checks for the THM-M-0696 immutable anchor inventory."""

from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_DIR / ".lake" / "packages" / "mathlib"
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())


def run(args: list[str], cwd: Path = ROOT) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    return result.stdout


assert AUDIT["item_id"] == "S56-M-0696-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0696"
assert AUDIT["audit_complete_for_phase"] is True
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert AUDIT["root_machine_classification"] == "M3"

manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
mathlib_rev = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_rev == AUDIT["local_environment"]["mathlib"]
assert run(["git", "rev-parse", "HEAD"], MATHLIB).strip() == mathlib_rev

digest_lines = []
for source in sorted((MATHLIB / "Mathlib").rglob("*.lean")):
    digest_lines.append(
        f"{hashlib.sha256(source.read_bytes()).hexdigest()}  {source.relative_to(MATHLIB)}\n"
    )
# Digest the ordered per-file content hashes and mathlib-relative paths.
digest = hashlib.sha256("".join(digest_lines).encode()).hexdigest()
assert digest == AUDIT["local_environment"]["mathlib_lean_tree_sha256"]

candidate = next(c for c in AUDIT["candidates"] if c["id"] == "M0696-C02")
assert re.fullmatch(r"[0-9a-f]{40}", candidate["revision"])
assert re.fullmatch(r"[0-9a-f]{64}", candidate["source_sha256"])
assert candidate["statement_match"] == "nearby_empty_context_candidate_not_exact"
assert len(candidate["blockers"]) >= 4

# An exact pinned candidate would have to mention this dossier's local root API.
needle = re.compile(r"THM_M_0696|PropositionalCompletenessTarget|SemanticallyEntails")
hits = []
for source in (MATHLIB / "Mathlib").rglob("*.lean"):
    if needle.search(source.read_text(errors="replace")):
        hits.append(str(source))
assert not hits, f"unexpected exact-candidate API hits: {hits}"

run(["lake", "env", "lean", "../../Stage1_Instances/THM-M-0696/Statement.lean"], LEAN_DIR)
print("anchor audit check: ok (4 candidates, pinned tree digest, no exact mathlib API hit)")
