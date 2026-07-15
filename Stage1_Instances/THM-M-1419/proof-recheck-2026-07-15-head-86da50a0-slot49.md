# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `86da50a0693b7d557e5f3bb2c72d42525956526f`

Base tree: `e2c87c9dc7ec274bc22013bc1159aff46bae12aa`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot49`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase is not genuinely
self-tested, no `.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen target quantifies
a plain equivalence `T : Omega Equiv Omega`. Its `MeasurePreserving T mu mu`
and `Ergodic T mu` hypotheses supply `Measurable T`, but no hypothesis supplies
`Measurable T.symm`. Pinned mathlib stores inverse measurability as the separate
`measurable_invFun` field of `MeasurableEquiv`; both `MeasurePreserving.symm`
and `Ergodic.symm` require a measurable equivalence.

A disposable Lean probe confirmed the exact type failure: using
`hT.measurable` for a goal `Measurable T.symm` fails because the term has type
`Measurable T`. This is material to the selected two-sided theorem, whose
backward filtration is over `T.symm`. The separately checked external terminal
likewise quantifies `T : X MeasurableEquiv X`; it does not prove the frozen
plain-equivalence target.

Earlier owned evidence gives a mathematical countermodel: take the two-sided
fair Bernoulli shift with only its future-coordinate sigma algebra and
`A(omega) = [[4, 0], [omega_0, 1]]`. A measurable equivariant fast line would
have slope `u` satisfying `u(T omega) = (u(omega) + omega_0) / 4`; backward
iteration forces `u(omega) = sum_(r >= 1) 4^(-r) omega_(-r)`, which depends on
past coordinates and is not future-measurable. Thus the frozen proposition is
mathematically false, not merely unsupported by the available proof route.
Because this countermodel is not kernel-formalized, the conservative machine
classification remains `[H2, M3, R3]` rather than being promoted to `M5`.

The statement prose is also inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, but
the proposition retains only measurability of the matrix-valued inverse and
never assumes measurability of the base inverse. A proof worker cannot silently
add that premise. The statement must first be reopened, repaired to use a
measurable equivalence or an explicit `Measurable T.symm` premise, and accepted
with a new expression fingerprint and obligation-registry version.

## Proof frontier

No exact placeholder-free root body exists in this repository or pinned Lake
closure. Pinned mathlib contains no Oseledets or Kingman terminal declaration.
Repo-local `THM-M-1057` supplies checked Kingman limit theorems, but only as an
analytic input; it does not construct the forward and backward filtrations,
measurable splitting, equivariance, or vector-growth closure required here.

The external project at
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
has a separately provisioned Lean 4.29 compatibility port under `THM-M-1056`.
This is discovery evidence, not proof credit for `THM-M-1419`: its sources are
outside this target and the pinned closure, and its packet is not master
accepted. More importantly, its terminal requires a measurable equivalence,
pointwise matrix measurability, and pointwise determinant nonvanishing. Exact
Pi/Euclidean norm, cocycle-order, measurable-subspace, direct-sum,
positive-finrank, equivariance, growth, and indexing transports remain open.

The frozen registry still has 14 obligations and 41 typed edges. Twelve of 13
machine-required obligations have no terminal proof-body ID.
`target_of_construction_package` merely returns a premise definitionally equal
to the complete root and consumes none of the four required proof children, so
its successful elaboration supplies no substantive proof credit.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted `[x]`. Twelve prior recheck packets plus one older blocker are
tracked, while the authoritative DAG records zero proof attempts. Section 10.2
requires splitting an unresolved item after five execution ticks. Only the
master may reconcile those packets with authoritative ticks, reopen the
statement, split or version the work, or change task state.

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
| Disposable copies of `OseledetsStatement.lean` and `ObligationTree.lean`, compiled through the existing pinned environment with `--trust=0 -t0`, explicit temporary outputs, and 300-second bounds | 0, 0 | Both elaborated; olean hashes `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| Pinned mathlib API inspection plus disposable inverse-measurability derivation probe | 0, 1 expected | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` separately stores inverse measurability, and the frozen hypotheses cannot derive `Measurable T.symm`. |
| Pinned mathlib terminal-name search | 1 expected | No Oseledets, multiplicative-ergodic, Lyapunov-filtration, subadditive-ergodic, or Kingman terminal declaration was found. |
| Repo-local Kingman declaration inspection | 0 | Found checked analytic inputs only, not an Oseledets splitting closure. |
| Read-only inspection of the separate `THM-M-1056` compatibility packet | 0 | Its terminal requires `T : X MeasurableEquiv X`; no source was copied or credited. |
| Scoped proof-input diff from `20808d65...` to this base | 0 | Only the already integrated prior recheck pair changed; theorem source, architecture, anchor, Kingman sources, toolchain, and dependency manifest are unchanged. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |

The disposable replay used only existing dependency oleans and wrote target
oleans under fresh `/tmp` directories, which were removed. It confirms the
exact statement and circular wrapper still elaborate; it does not prove the
open construction package.

## Retry condition

The master must first reopen and repair `S56-M-1419-STATEMENT`, accept a new
exact expression fingerprint and obligation-registry version, and rerun every
prerequisite gate. Including this handoff, it must reconcile 14 tracked
negative packets with authoritative execution ticks and split the proof work
if at least five qualify. A later owned integration task can then use the
separately ported Oseledets implementation, prove every exact transport, and
replace the identity wrapper with typed composition consuming all required
children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs are
empty. It does not satisfy `S56-M-1419-PROOF`, close an obligation or root,
change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
