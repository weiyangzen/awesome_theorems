# THM-M-1235 proof-phase blocker

Item: `S56-M-1235-PROOF`  
Date: `2026-07-12`  
Base revision: `04422fd72f342b905dbd4fb4a5a4035cfae56e6e`

## Verdict

`blocked`: the exact canonical target is false under its frozen Lean encoding.
`Motion` stores conditions `(I)`--`(VIII)` as bare `Prop` fields, not proofs of
predicates over the five functions. Thus every five-function tuple determines a
`Motion`, independently of the intended Euler, initial, boundary, and regularity
conditions. Given any alleged unique motion, `Proof.lean` changes `velocityX`
pointwise to `velocityX + 1`; all other structure fields remain unchanged, but
`SameMotion` fails. Concrete source data discharge all explicit target premises.

Lean kernel-checks
`Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness` with only
`propext`, `Classical.choice`, and `Quot.sound`. No axiom, `sorry`, admitted
declaration, theorem substitution, or broadened target was introduced.

This is stronger than the predecessor's reported missing-proof-body blocker:
no proof body for the frozen proposition can exist in a consistent Lean
environment. The statement must be corrected and re-frozen before proof work.
Because the assigned proof phase is not complete, this attempt deliberately
does not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone. The pre-existing
`Formalizations/Lean/.lake` link supplied canonical pinned artifacts and was
not modified. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159, planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges pass; the stale frozen graph still reports the root open M3. |
| temporary owned `Statement.olean`, then `LEAN_PATH=... lean Proof.lean`, then removal | 0 | Both refutation declarations elaborate; the canonical target prints exactly, and the axiom report is `[propext, Classical.choice, Quot.sound]`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-blocker.json` | 0 | Blocker record is valid JSON. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx' Stage1_Instances/THM-M-1235 --glob '*.lean'` | 1 | No prohibited Lean token; exit 1 means no match. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace errors. |

The toolchain is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Retry boundary

Return to the statement phase. Conditions `(I)`--`(VIII)` must become native
predicates of the five functions with proof-bearing `Motion` fields. The source
crosswalk, canonical expression fingerprint, mutation suite, registry, and all
dependent graph/evidence hashes must then receive a versioned re-freeze. Merely
adding analytic existence and uniqueness packages to the current interface
cannot repair this counterexample.
