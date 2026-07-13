# THM-M-1011 proof-phase attempt

Item: `S56-M-1011-PROOF`  
Date: `2026-07-14` (`Asia/Shanghai`)  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`blocked`: no eligible proof body for the exact frozen Prokhorov target exists in the repository or
pinned dependency closure. The immediate root cut remains `M1011-N-SEPARATION`. The frozen context
has `PseudoMetricSpace X`, while the only located tightness-to-compactness body,
`MeasureTheory.isCompact_closure_of_isTightMeasureSet`, additionally requires `T2Space X`.
Instance synthesis for that premise fails in the exact context.

`ObligationTree.lean` contains three genuine placeholder-free bodies. `compact_to_tight` proves the
exact reverse direction. `tight_to_compact_of_t2` proves the forward direction only after accepting
an explicit `T2Space X` dictionary, and `canonical_of_t2` composes both directions under that same
extra premise. The latter two do not inhabit `CanonicalStatement X`; returning either would
substitute a conditional theorem for the frozen root.

A separation-quotient route remains plausible but is not a ready pinned wrapper. Mathlib equips
`SeparationQuotient X` with metric and completeness instances, but bounded repository-wide searches
found no probability-measure equivalence or transport of `IsTightMeasureSet` and compact weak
closure between `X` and its separation quotient. Such a route would be substantive new proof work
and would also require a versioned change to the frozen proof graph rather than silently bypassing
its required separation child. No counterexample was established, so this record says unsupported,
not false.

Root debt remains `[H1, M5, R4]`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone using the existing canonical pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1011` | 0 | rank 260; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1011/check_statement.py` | 0 | exact canonical expression and four structural mutations checked in the pinned environment |
| Isolated `Statement.olean` followed by `ObligationTree.lean` with `lake env which lean` and the pinned `LEAN_PATH` | 0 | exact reverse and both explicit-`T2Space` conditional declarations elaborated; `canonical_of_t2` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1011/check_obligation_tree.py` | 0 | 14 obligations and 35 typed edges passed; denominator `3dd41add...bdd90`; exact root remained open M5 at the separation cut |
| Repository-wide `rg` for the two Prokhorov declarations and `SeparationQuotient` measure transports | 0 | the only exact forward body found was the known T2-conditional mathlib declaration; no MeasureTheory separation-quotient transport was found |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum` on the statement, conditional composition, registry, and anchor audit | 0 | `6bf24878...1d66`; `4395f2cb...7c9d`; `e427e163...a40`; `7d75a5b6...93a2` |
| `python3 -m json.tool Stage1_Instances/THM-M-1011/proof-blocker.json` | 0 | blocker record parsed as valid JSON |
| Prohibited-construct scan over `Statement.lean` and `ObligationTree.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, custom `axiom`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1011` | 0 | no whitespace errors |

The pre-existing untracked `Formalizations/Lean/.lake` entry is the automation-provided symlink to
the canonical pinned artifacts and was reused read-only.

## Reopen condition

Resume only after a placeholder-free proof of the exact non-T2 forward implication with a truthful
versioned proof-architecture update, or after the statement phase re-freezes the intended Polish
claim with `MetricSpace X` or explicit `T2Space X` and all dependent gates are rerun.
