# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `0c26cec0be4f7fada10abc2c6ed0b213656d1708`

Base tree: `52417604a8aaccfac38ae970ef94337e6f38d033`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot49`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not close, no
`.stage1-worker-selftest.json` is emitted.

The first failed gate is exact-target fidelity at `M1419-S-INTERFACE`. The
frozen target quantifies a plain equivalence `T : Omega Equiv Omega`.
`MeasurePreserving T mu mu` and `Ergodic T mu` supply `Measurable T`, but no
frozen hypothesis supplies `Measurable T.symm`. Pinned mathlib stores inverse
measurability separately in `MeasurableEquiv`, and its `Ergodic.symm` theorem
requires a measurable equivalence. A fresh disposable Lean probe rejected
`exact hT.measurable` at the goal `Measurable T.symm`: the supplied term has
type `Measurable T`, not `Measurable T.symm`.

This missing premise is material to the selected two-sided construction.
Earlier owned evidence records a future-sigma-algebra Bernoulli-shift
triangular-cocycle obstruction in which the equivariant fast line depends on
past coordinates. That countermodel has not been kernel-formalized, so this
packet conservatively retains machine state `M3` rather than claiming a
kernel-checked refutation or `M5`.

The statement prose is also inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, while
the proposition retains only measurability of the matrix inverse and never
assumes measurability of the base inverse. A proof worker may not silently add
that premise. The statement must be reopened and versioned before exact
positive proof work can proceed.

## Proof frontier

No relevant proof input changed since the preceding packet at `12d9becb`: the
target statement, frozen architecture, anchor audit, repo-local Kingman input,
integrated sibling Oseledets port, toolchain, and Lake manifest are unchanged.

Pinned mathlib contains no Oseledets, multiplicative-ergodic,
Lyapunov-filtration, subadditive-ergodic, or Kingman terminal declaration. The
repo-local `THM-M-1057` Kingman theorems are analytic inputs only and construct
neither forward/backward filtrations nor the selected splitting.

A complete Lean 4.29 port of `marcmorningstar/lean4-ergodic-theory` is present
under the separately owned target `THM-M-1056`. Its terminal declaration,
`ErgodicTheory.oseledets_splitting`, requires `T : X MeasurableEquiv X`,
pointwise matrix measurability, and pointwise determinant nonvanishing. The
frozen target has only a plain equivalence and almost-everywhere matrix
assumptions. No checked wrapper supplies the missing inverse base
measurability or all of the representative, Pi/Euclidean norm, cocycle-order,
subspace-measurability, direct-sum, finrank, equivariance, growth, and indexing
transports. The sibling receipt is provisional and unaccepted, and the sibling
item is not an accepted dependency of this theorem. Its source therefore
provides discovery evidence but no proof credit here.

The frozen validator still reports 14 obligations and 41 typed edges with
denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
and explicitly leaves the root open at `M3`. Twelve of 13 machine-required
obligations have no terminal proof-body ID. The sole recorded body,
`target_of_construction_package`, merely returns a premise definitionally
equal to the complete target; it consumes none of the four proof children and
receives no substantive composition credit.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted. Nineteen earlier proof-recheck packets plus one older blocker
are tracked while the authoritative DAG still records zero proof attempts.
Section 10.2 requires splitting after five unresolved execution ticks. Only
the master may reconcile packets with authoritative ticks, split or version
the node, reopen prerequisites, or change task state.

## Fresh validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network command, or deliberate `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `git status --short` before editing | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root explicitly remains open `M3`. |
| `cd Formalizations/Lean && lake --version && lake env lean --version` | 0 | Lake `5.0.0-src+98dc76e`; Lean `4.29.0`, commit `98dc76e3...716fb04`. |
| Fresh `/tmp` trust-zero replay of copied `OseledetsStatement.lean` and `ObligationTree.lean`, plus a `Mathlib.Util.AssertNoSorry` probe, using the existing `lake env` Lean path, explicit roots/outputs, `-j1`, and 300-second bounds | 0, 0, 0 | All elaborated; declarations were sorry-free; olean hashes were `f5222f72...3a9169`, `4fd543d8...50a6`, and `2add277c...6e16`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| Disposable derivation probe with `hT : Ergodic T mu`, goal `Measurable T.symm`, and body `exact hT.measurable`, through pinned `lake env lean --trust=0 -j1` | 1 expected | Lean reported `hT.measurable : Measurable T` but expected `Measurable T.symm`; temporary source, log, and outputs were removed. |
| `rg -n -i --glob '*.lean' 'oseledets\|multiplicative[ _-]?ergodic\|lyapunov (exponent\|filtration)\|subadditive ergodic\|kingman' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 expected | No matching terminal declaration exists in the pinned mathlib source tree. |
| Read-only inspection and hashing of the `THM-M-1056` terminal, proof source, receipt, and authoritative DAG state | 0 | The terminal requires `MeasurableEquiv`; hashes remain `e47ced0d...e9407`, `e93f37d7...a69`, and `c9916f9c...01a7`; sibling proof is `[_]` and receipt `accepted=false`. |
| `git diff --name-status 12d9becb170c3ef83e7aed51d1b3eed2a1940379..HEAD -- <scoped proof inputs; evidence packets excluded>` | 0 | Empty output: no target proof input, architecture, Kingman input, sibling port, toolchain, or dependency pin changed. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| `python3 -m json.tool <this JSON packet>` | 0 | The structured blocker packet parsed successfully. |
| `git diff --check`, then `git diff --no-index --check /dev/null <new-file>` for each packet file | 0, 1 expected, 1 expected | No whitespace diagnostics; each no-index check returned Git's expected nonempty-diff status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest was emitted for the blocked phase. |

The replay wrote target oleans only under fresh temporary directories and
removed them. It verifies that the exact statement and circular wrapper remain
sorry-free and elaborate; it does not prove the open Oseledets construction
package.

## Retry condition

The master must first reopen `S56-M-1419-STATEMENT`, replace the plain base
equivalence with a measurable equivalence or add `Measurable T.symm`, accept a
new exact expression fingerprint and obligation-registry version, and rerun
the source, mutation, anchor, and obligation-tree gates. It must also reconcile
the tracked negative packets with authoritative execution ticks and split this
oversized proof item if at least five qualify. After that, owned child tasks can
integrate the compatible Oseledets route, implement the exact
almost-everywhere and representation transports, and add checked composition
consuming every required child.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs
are empty; root vector remains `[H2, M3, R3]`. It does not satisfy
`S56-M-1419-PROOF`, close an obligation or root, change scheduler state, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.
