# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

Attempt date: `2026-07-16` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot45`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not close, no
`.stage1-worker-selftest.json` is emitted.

The first failed gate is exact-target fidelity at `M1419-S-INTERFACE`. The
frozen target quantifies a plain equivalence `T : Omega Equiv Omega`.
`MeasurePreserving T mu mu` and `Ergodic T mu` supply `Measurable T`, but no
frozen hypothesis supplies `Measurable T.symm`. Pinned mathlib stores inverse
measurability separately in `MeasurableEquiv`, and `Ergodic.symm` requires a
measurable equivalence. A fresh disposable trust-zero Lean probe rejected
`exact hT.measurable` at the goal `Measurable T.symm`: the term has type
`Measurable T` instead.

This premise is material, not merely an API inconvenience. The existing owned
blocker describes a standard-semantics countermodel using the bilateral fair
Bernoulli shift with only the future-coordinate sigma algebra and the triangular
cocycle `A(omega) = [[4, 0], [omega_0, 1]]`. The forward shift is measurable,
measure-preserving, ergodic, and bijective, while its inverse is not measurable.
An equivariant fast-line slope must depend on past coordinates and cannot be a
measurable subspace field for that sigma algebra. The countermodel has not been
formalized in Lean, so this packet conservatively retains `M3`; it does not
claim a kernel-checked refutation or `M5`.

The prose freeze is inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, while
the proposition assumes measurability only of the matrix-valued inverse and
never of the base inverse. The frozen typed graph's closed interface record is
therefore invalidated and needs an append-only statement/registry revision. A
proof worker may not silently add the missing premise or substitute the
conventional measurable-equivalence theorem.

## Dependency and reuse audit

The required schema 1.1 ledger now binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
context digest
`588c2d8ca15af5561c903d27b8cbbb7ee84977bc442f29cda9316d4866ce21fa`,
and this base revision. The hard-parent and transitive-ancestor closure is
empty, so there are zero hard-parent inspections. All eight nonblocking
contexts have explicit decisions: the one Kingman hint is `candidate_only`,
and the seven weak shared-module clusters are `not_applicable`. The ledger also
records seven open compatibility obligations. Its production validator passed.

`THM-M-1057` provides the checked declarations `tendsto_kingman`,
`tendsto_kingman_ergodic`, and `tendsto_kingman_ergodic_means`. These are real
analytic inputs, but they construct neither the forward/backward filtrations
nor the measurable invariant splitting. The provider proof phase is `[_]`, its
receipt is provisional and unaccepted, and no Kingman result transfers root or
checkbox credit.

## Current proof frontier

The repository now contains a substantive 62-module Lean 4.29 Oseledets port
under separately owned `THM-M-1056`, culminating in
`ErgodicTheory.oseledets_splitting`. That is meaningful new candidate
infrastructure, but it does not change this blocker. Its exact base binder is
`T : X MeasurableEquiv X`; it additionally uses pointwise matrix measurability,
pointwise invertibility, L2 operator norms, Euclidean fibers, and its own
cocycle and measurable-subspace interfaces. The sibling proof task is `[_]`,
its proof receipt is unaccepted, and no checked consumer wrapper supplies the
missing base inverse measurability or the remaining almost-everywhere, norm,
coordinate, cocycle, subspace, direct-sum, equivariance, growth, and indexing
transports. A wrapper cannot manufacture a logically missing hypothesis.

The frozen validator still reports 14 obligations and 41 typed edges with
denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
and explicitly leaves the root open at `M3`. Twelve of 13 machine-required
obligations have no terminal proof-body ID. The sole recorded body,
`target_of_construction_package`, merely returns a premise definitionally
equal to the complete target and consumes none of the four required proof
children. It supplies no substantive proof or composition credit.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted `[x]`. Twenty-four earlier recheck pairs and one older blocker
are tracked while the authoritative proof item still records zero attempts.
Rev-5.6 requires splitting after five unresolved execution ticks. The master
must reconcile durable packets with authoritative ticks and split or version
this item if at least five qualify; a worker may not edit that authority.

## Fresh validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network command, or deliberate `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 expected at nested graph gate | Manifest/assurance checks reached the nested v2 gate, which detected expected inventory drift from the new target-owned proof packet; the ledger is excluded from reuse-context discovery but remains inventory-visible. The standalone manifest check passed 1546 targets. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 expected after writing artifacts | The checked graph differs from a fresh generation only because the ledger and proof-recheck JSON would enter the target evidence inventory. The ledger remains excluded from shared-group/reuse-context discovery, so its context digest is stable. Workers may not regenerate the graph; the integration lane must do so after accepting or normalizing the blocker. |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-1419` | 0 | Passed 1546 unique ordered targets; target remains rank 688, planned, and incomplete. |
| Production `validate_dependency_reuse_ledger` call binding graph digest and git `HEAD` | 0 | Passed schema 1.1 with zero hard inspections, eight decisions, and seven open compatibility obligations. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; root remains open `M3`. |
| Fresh `/tmp` trust-zero replay of copied `OseledetsStatement.lean` and `ObligationTree.lean`, plus a `Mathlib.Util.AssertNoSorry` probe, through the existing `lake env` Lean path | 0 | All elaborated; the conditional wrapper was sorry-free and used exactly `[propext, Classical.choice, Quot.sound]`; olean hashes were `f5222f72...3a9169`, `4fd543d8...50a6`, and `dc3bc6cd...9fee9`; temporary outputs were removed. |
| Disposable derivation probe with `hT : Ergodic T mu`, goal `Measurable T.symm`, and body `exact hT.measurable` | 1 expected | Lean reported `Measurable T` where `Measurable T.symm` was required; no olean was produced; log SHA-256 was `d7113b37...496eb0`. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` stores inverse measurability separately, and `Ergodic.symm` requires `MeasurableEquiv`. |
| Pinned mathlib terminal-name search | 1 expected | No relevant terminal declaration was found. |
| Current `THM-M-1056` and `THM-M-1057` exact type, source, receipt, and state inspection | 0 | The Oseledets port proves a distinct `MeasurableEquiv` target; Kingman supplies analytic inputs only; both proof marks are provisional `[_]`. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| JSON parsing plus fail-closed semantic assertions | 0 | The ledger and packet parse and preserve blocked-state semantics. |
| `git diff --check -- <the three owned handoff artifacts>` | 0 | All owned handoff artifacts passed whitespace checks. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest was emitted. |

The replay wrote oleans only below fresh temporary directories and removed
them. It verifies that the exact statement and circular wrapper still
elaborate without placeholders; it does not prove the open Oseledets package.

## Retry condition

The master must first reopen `S56-M-1419-STATEMENT`, replace the plain base
equivalence with a measurable equivalence or add `Measurable T.symm`, accept a
new exact expression fingerprint and obligation-registry version, and rerun
the statement, source, mutation, anchor, and obligation-tree gates. It must
also reconcile accumulated negative packets with authoritative execution
ticks. Later owned proof tasks can then implement every exact transport over
the current Oseledets port and replace the identity wrapper with typed
composition consuming all required children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs
are empty; root vector remains `[H2, M3, R3]`. It does not satisfy
`S56-M-1419-PROOF`, close an obligation or root, change scheduler state, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.
