# THM-M-0773 proof-phase validation

Validated at `2026-07-12T17:31:24+08:00` from base revision
`5314165df54baa70993fddf08cc142a9739a74e0`. The worker reused the pinned,
pre-existing `.lake` dependency artifacts without fetching or modifying them.

| Command | Exit | Result |
|---|---:|---|
| `TMPDIR="$(mktemp -d)"; LEAN_PATH="$(cd Formalizations/Lean && lake env printenv LEAN_PATH)" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean -o "$TMPDIR/Statement.olean" Stage1_Instances/THM-M-0773/Statement.lean; LEAN_PATH="$TMPDIR:$(cd Formalizations/Lean && lake env printenv LEAN_PATH)" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Stage1_Instances/THM-M-0773/Proof.lean; rm -rf "$TMPDIR"` | 0 | Exact statement and proof elaborated; both proof declarations report `[propext, Classical.choice, Quot.sound]`. |
| `python3 Stage1_Instances/THM-M-0773/check_proof.py` | 0 | Proof source, frozen denominator, receipt hashes, exact root, axiom disclosure, and prohibited-token checks passed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed. |
| `git diff --check -- Stage1_Instances/THM-M-0773 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

This is proof-node evidence only. Master acceptance, validation, release,
source/readability closure, independent replay, and theorem completion remain
outside this assignment.
