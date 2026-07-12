# THM-M-1070 proof execution

Item: `S56-M-1070-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `dfacb54b5f277adf642e7658a065015f486d4cf2`

## Verdict

`blocked`. `Proof.lean` adds genuine placeholder-free introduction and elimination bodies for the
exact six-clause conjunction frozen as `IsLevyProcess`. The introduction theorem consumes the
probability, marginal measurability, almost-everywhere zero, joint independent-increment,
stationary-law, and stochastic-continuity clauses separately and constructs the canonical target.
The elimination theorem checks the converse exact shape, so the assembly cannot hide an extra
premise or weaken a clause.

This does not complete the assigned proof phase. The target is a predicate parameterized by `P`
and `X`, not a proposition selecting a particular process. The frozen obligation registry still
requires proof bodies for all six semantic clauses, and neither the dossier nor pinned mathlib
provides data from which those clauses can be proved. In particular, independent increments,
stationary increment laws, and stochastic continuity remain the first critical cut. Introducing
them as assumptions in a purported unconditional root theorem would broaden or substitute the
deliverable. No root closure or theorem completion is claimed, and `.stage1-worker-selftest.json`
is deliberately absent because the assigned phase is incomplete.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing pinned Lake artifacts. No update,
build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1070` | 0 | rank 512, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1070/check_obligation_tree.py` | 0 | 13 obligations and 26 typed edges passed; denominator `c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9`; root remains open M3 |
| Compile `Statement.lean` to a temporary dossier-local `Statement.olean`, then run `Proof.lean` with `LEAN_PATH=Stage1_Instances/THM-M-1070:$(cd Formalizations/Lean && lake env printenv LEAN_PATH)` and `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean`; remove the temporary object | 0 | both proof bodies elaborated; each `#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1070/Proof.lean` | 1 | expected no-match result; no prohibited declaration or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-1070` | 0 | no whitespace errors |

The first direct attempt to elaborate `Proof.lean` from `Formalizations/Lean` exited 1 because the
dossier-local import `Statement` is outside the Lake package search path. The subsequent scoped
`LEAN_PATH` command above is the successful narrow elaboration check; its temporary object was
removed. The pre-existing untracked `Formalizations/Lean/.lake` worker link was not changed.

## Reopen condition

Resume after the target is refined with a particular process and hypotheses or construction that
can discharge all six frozen clauses, or after an immutable exact Lean 4 result with compatible
conventions is pinned and checked locally. The audited LeanLevy near-match cannot be credited: it
uses pointwise zero and almost-everywhere cadlag paths rather than this target's almost-everywhere
zero and stochastic continuity package.
