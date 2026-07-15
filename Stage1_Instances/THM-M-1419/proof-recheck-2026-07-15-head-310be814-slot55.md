# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `310be814cb307a91263e232acf691a6b3eded70e`

Base tree: `947289604e1bf9c317b6dc3dd174d3f8fb54ba0e`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot55`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not pass, no
`.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen target quantifies
a plain equivalence `T : Omega Equiv Omega`. Its `MeasurePreserving T mu mu`
and `Ergodic T mu` hypotheses supply `Measurable T`, but no hypothesis supplies
`Measurable T.symm`. Pinned mathlib stores inverse measurability in the separate
`measurable_invFun` field of `MeasurableEquiv`, and its `Ergodic.symm` theorem
requires `T : Omega MeasurableEquiv Omega`.

A fresh disposable Lean probe confirmed the exact type failure:
`hT.measurable` has type `Measurable T`, not the required
`Measurable T.symm`. This is material to the selected two-sided theorem, whose
backward filtration is over `T.symm`.

Earlier owned evidence gives a mathematical countermodel: the two-sided fair
Bernoulli shift equipped only with the future-coordinate sigma algebra, with
triangular cocycle `A(omega) = [[4, 0], [omega_0, 1]]`. Equivariance forces the
fast-line slope to depend on past coordinates, contradicting the target's
measurable splitting. This countermodel is not kernel-formalized, so the
conservative root classification remains `[H2, M3, R3]` rather than `M5`.

The prose freeze is inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, but the
proposition retains only measurability of the matrix-valued inverse and never
assumes measurability of the base inverse. A proof worker cannot silently add
that missing premise. The statement must first be reopened and repaired to use
a measurable equivalence or an explicit `Measurable T.symm` hypothesis, with a
new expression fingerprint and obligation-registry version.

## Proof frontier

The pinned Lake closure contains no exact Oseledets terminal theorem. Repo-local
`THM-M-1057` supplies checked Kingman limit theorems, but only as an analytic
input; it does not construct the forward/backward filtrations, measurable
splitting, equivariance, or vector-growth closure required here.

A separate current scratch packet contains a complete Lean 4.29 compatibility
port of
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
A fresh trust-zero probe checked its terminal
`ErgodicTheory.oseledets_splitting`, its sorry-free declaration, and its axiom
set `[propext, Classical.choice, Quot.sound]`. The terminal source and olean
hashes are respectively `e47ced0d...1c6e9407` and
`3f3165b7...d3067197`.

That scratch receives no proof credit: it is outside this target and the pinned
Lake closure, is mutable nonrelease evidence, and proves a different interface.
Its terminal requires a measurable equivalence, pointwise matrix measurability,
and pointwise determinant nonvanishing. The frozen target instead has a plain
equivalence and almost-everywhere matrix hypotheses. Exact Pi/Euclidean norm,
cocycle-order, measurable-subspace, direct-sum, positive-finrank, equivariance,
growth, and output-index transports are also absent.

The frozen registry still has 14 obligations and 41 typed edges. Twelve of 13
machine-required obligations have no terminal proof-body ID.
`target_of_construction_package` merely returns a premise definitionally equal
to the complete root and consumes none of the four required proof children, so
its elaboration supplies no substantive proof credit.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted `[x]`. Thirteen earlier recheck packets plus one older blocker
are tracked, while the authoritative DAG records zero proof attempts. Section
10.2 requires an unresolved item to be split after five execution ticks. Only
the master may reconcile packets with authoritative ticks, reopen prerequisites,
split or version the item, or change scheduler state.

## Fresh validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network command, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root remains open `M3`. |
| `cd Formalizations/Lean && lake --version && lake env lean --version` | 0 | Lake `5.0.0-src+98dc76e`; Lean `4.29.0`, commit `98dc76e3...716fb04`. |
| Fresh temporary copies of `OseledetsStatement.lean` and `ObligationTree.lean`, compiled via the existing pinned environment with `--trust=0 -t0`, explicit temporary outputs, and 300-second bounds | 0, 0 | Both elaborated; olean hashes `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms exactly `[propext, Classical.choice, Quot.sound]`; temporary files were removed. |
| Disposable exact derivation probe at goal `Measurable T.symm` using `hT.measurable` | 1 expected | Lean reported `hT.measurable : Measurable T`, not `Measurable T.symm`; probe and log were removed. |
| Trust-zero probe of the separate compatible external terminal | 0 | `ErgodicTheory.oseledets_splitting` checked, was sorry-free, and reported exactly the three allowed classical axioms; scratch received no proof credit. |
| `git diff --name-status b05dfe30...HEAD --` over target source/architecture, Kingman inputs, toolchain, and dependency manifest | 0 | Empty; no scoped proof input or pin changed. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |

The target replay wrote both target oleans under a fresh `/tmp` directory and
removed it. It confirms only that the exact statement and circular conditional
wrapper elaborate; it does not prove the open construction package. The
external probe was read-only inspection of already existing scratch artifacts.

## Retry condition

The master must first reopen and repair `S56-M-1419-STATEMENT`, accept a new
exact expression fingerprint and obligation-registry version, and rerun every
prerequisite gate. Including this handoff, it must reconcile 15 tracked
negative packets with authoritative execution ticks and split the proof work
if at least five qualify. A later owned integration task can then vendor and
provenance-audit the compatible Oseledets implementation, prove every exact
transport, and replace the identity wrapper with typed composition consuming
all required children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs are
empty. It does not satisfy `S56-M-1419-PROOF`, close an obligation or root,
change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
