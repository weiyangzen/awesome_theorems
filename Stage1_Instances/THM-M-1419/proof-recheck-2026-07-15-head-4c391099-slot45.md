# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `4c391099fc585eb02188ea57450990b3af042aab`

Base tree: `f96bc1a1b7c35e476a2e6191def82f8c33458e3c`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot45`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not pass, no
`.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen Lean expression
quantifies a plain equivalence `T : Omega Equiv Omega`. Its
`MeasurePreserving T mu mu` and `Ergodic T mu` hypotheses supply
`Measurable T`, but no hypothesis supplies `Measurable T.symm`. A fresh
disposable Lean probe rejected `exact hT.measurable` at the inverse goal with
the exact mismatch `Measurable T` versus `Measurable T.symm`. Pinned mathlib's
`Ergodic.symm` and the substantive two-sided Oseledets terminal instead require
`T : Omega MeasurableEquiv Omega`.

This is a frozen-statement fidelity defect, not a missing convenience lemma.
`source-statement-crosswalk.md` says that inverse measurability was retained,
whereas the Lean target retains only measurability of the matrix inverse and
never assumes measurability of the base inverse. Earlier owned evidence records
a future-sigma Bernoulli-shift triangular-cocycle obstruction, but no
kernel-checked countermodel to the complete root exists. This recheck therefore
keeps the conservative root vector `[H2, M3, R3]`; it does not claim `H5` or
`M5`.

## Proof frontier

No exact placeholder-free root body exists in the pinned closure. The frozen
registry has 13 machine-required obligations; 12 have no terminal proof-body
ID. `target_of_construction_package` merely returns a premise definitionally
equal to the complete target and consumes none of the four proof children
recorded for assembly, so it earns no composition or root proof credit.

The pinned mathlib source tree has no terminal Oseledets, multiplicative
ergodic, or Kingman declaration. `THM-M-1057` supplies checked Kingman limit
theorems only, not the filtrations, measurable splitting, equivariance, and
vector-growth closure required here.

A separately owned automation clone currently records a provisional Lean 4.29
port of `ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
That mutable packet is outside this target and its pinned Lake closure and
receives no proof credit. More importantly, it proves a different interface:
it requires a measurable equivalence, pointwise measurable and pointwise
invertible matrices, and different fiber, cocycle, measurable-subspace, and
output APIs. The missing inverse-base measurability alone prevents an exact
wrapper for the frozen target; the almost-everywhere, representation, direct
sum, finrank, equivariance, growth, and indexing transports also remain open.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted `[x]`. Fifteen earlier recheck packets plus one older blocker
are tracked, while the authoritative DAG records zero proof attempts and no
children. Section 10.2 requires an unresolved item to be split after five
execution ticks. Only the master may reconcile packets with authoritative
ticks, reopen prerequisites, split or version the item, or change scheduler
state.

## Fresh validation

All commands ran from this worker clone. No `lake update`, `lake build`, clone,
fetch, network command, or dependency mutation was run. The automation-provided
untracked `.lake` symlink was reused read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688; planned; rework required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | 14 obligations and 41 typed edges passed; denominator `ad691633...5999`; root remains open M3 |
| `(cd Formalizations/Lean && lake --version && lake env lean --version)` | 0 | Lake 5.0.0-src+98dc76e; Lean 4.29.0 commit `98dc76e3...716fb04` |
| copied-source `lake env lean -R <tmp> --trust=0 -t0` replay of `OseledetsStatement.lean` and `ObligationTree.lean` | 0, 0 | both elaborated; olean hashes `f5222f72...a9169` and `4fd543d8...50a6`; wrapper axioms exactly `propext`, `Classical.choice`, `Quot.sound`; temporary outputs removed |
| disposable inverse-measurability probe | 1 expected | `hT.measurable` has type `Measurable T`, not the required `Measurable T.symm`; temporary probe removed |
| pinned-mathlib terminal-name search | 1 expected | no Oseledets, multiplicative-ergodic, Lyapunov-filtration, subadditive-ergodic, or Kingman terminal declaration found |
| repo-local Kingman declaration search | 0 | found `tendsto_kingman`, its ergodic form, and mean theorem only; none closes an Oseledets splitting |
| scoped proof-input diff from `062e0b53...` to `HEAD` | 0 | no target source, architecture, Kingman source, toolchain, dependency manifest, or target manifest changed |
| token-anchored prohibited-device scan over owned Lean files | 1 expected | no `sorry`, `admit`, axiom declaration, unsafe/oracle hook, `native_decide`, `implemented_by`, or `extern` token found |

The trust-zero replay confirms only that the exact statement and circular
conditional wrapper elaborate. It does not prove the open construction
package, and the untracked cache makes the replay nonrelease evidence.

## Retry condition and boundary

The master must first reopen the statement, require a bimeasurable base, accept
a new expression fingerprint and versioned obligation registry, and rerun the
statement, source, anchor, and obligation-tree gates. It must also reconcile the
16 earlier tracked negative packets plus this packet with authoritative
execution ticks and split this oversized item if at least five count. Only then
may an owned proof task integrate a compatible Oseledets implementation and
implement all exact transports and typed composition.

This file is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-1419-PROOF`, close an obligation or root, change scheduler state, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.
