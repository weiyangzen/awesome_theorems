# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `3862149a6bcf2a64e19fabdced9dd80a706f288e`

Base tree: `d3e57e661c2326a97c8b48580abe1f4a3797cd98`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot71`

## Verdict

`blocked`; the proof phase remains `[ ]`. No proof body, axiom, placeholder,
weakened theorem, dependency, frozen authority artifact, receipt, or task state
was added or changed. Because the requested proof phase did not pass, no
`.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen target quantifies
a plain equivalence `T : Omega Equiv Omega`. Its `MeasurePreserving T mu mu`
and `Ergodic T mu` hypotheses provide `Measurable T`, but no frozen hypothesis
provides `Measurable T.symm`. Pinned mathlib stores inverse measurability as a
separate field of `MeasurableEquiv`, and its `Ergodic.symm` theorem requires
`T : Omega MeasurableEquiv Omega`.

This is material to the selected two-sided splitting theorem, whose backward
filtration is built over `T.symm`. The substantive external candidate
`ErgodicTheory.oseledets_splitting` also requires a measurable equivalence.
Earlier owned evidence describes a Bernoulli-shift obstruction to recovering
the desired measurable splitting from forward measurability alone, but no
kernel-checked countermodel to the complete root is present. The conservative
root classification therefore remains `[H2, M3, R3]`; this attempt does not
promote the target to `M5`.

The statement prose is inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, but
the proposition retains only measurability of the matrix-valued inverse and
never assumes measurability of the base inverse. A proof worker cannot silently
add that premise. The statement must first be reopened, corrected to use a
measurable equivalence or an explicit `Measurable T.symm` hypothesis, and
accepted with a new statement fingerprint and obligation-registry version.

## Proof frontier

No exact placeholder-free root body exists in the repository or pinned Lake
closure. Pinned mathlib has no Oseledets, multiplicative-ergodic, or Kingman
terminal declaration. The repo-local `THM-M-1057` Kingman theorems are useful
analytic inputs, but do not construct the exterior-power limits, forward and
backward filtrations, measurable splitting, equivariance, or vector-growth
closure required here.

The external candidate at
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
is outside this repository and the pinned Lake closure. Its source requires a
measurable equivalence, pointwise matrix measurability, and pointwise
invertibility. The frozen target has only a plain equivalence and
almost-everywhere matrix hypotheses. Exact Pi/Euclidean norm, cocycle-order,
measurable-subspace, direct-sum, positive-finrank, equivariance, growth, and
output-index transports are also absent. Surviving automation scratch state is
mutable and inconsistent across retries and receives no proof credit.

The frozen registry still has 14 obligations and 41 typed edges. Twelve of 13
machine-required obligations have no terminal proof-body ID.
`target_of_construction_package` merely returns a premise definitionally equal
to the complete root and consumes none of the four required proof children, so
its successful elaboration is not substantive proof evidence.

The prerequisite `S56-M-1419-OBLIGATION_TREE` is provisional `[_]`, not master
accepted `[x]`. Ten earlier recheck packets plus one older blocker are tracked,
while the authoritative DAG records zero proof attempts. Section 10.2 requires
an unresolved item to be split after five execution ticks. Only the master may
reconcile those packets with authoritative ticks, split or version the item,
reopen prerequisites, or change scheduler state.

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
| Disposable copies of `OseledetsStatement.lean` and `ObligationTree.lean`, compiled through the existing pinned environment with `--trust=0 -t0`, explicit temporary outputs, and 300-second bounds | 0, 0 | Both elaborated; olean hashes `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms exactly `[propext, Classical.choice, Quot.sound]`; temporary files were removed. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` stores inverse measurability separately, and `Ergodic.symm` requires `MeasurableEquiv`. |
| Pinned mathlib terminal-name search | 1 expected | No Oseledets, multiplicative-ergodic, or Kingman terminal declaration was found. |
| Repo-local Kingman declaration inspection | 0 | Found checked analytic inputs only, not an Oseledets splitting closure. |
| `git diff --name-status b98f9f43...HEAD --` scoped proof inputs and pins | 0 | Empty: the target, architecture, anchor, Kingman sources, toolchain, and dependency manifest are unchanged since the preceding accepted packet base. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |

The disposable replay used only existing dependency oleans and wrote both
target oleans under a fresh `/tmp` directory, which was removed. It confirms
the exact statement and circular wrapper still elaborate; it does not prove
the open construction package.

## Retry condition

The master must first reopen and repair `S56-M-1419-STATEMENT`, accept a new
exact expression fingerprint and obligation-registry version, and rerun all
prerequisite gates. Including this handoff, it must also reconcile the 12
tracked negative packets with authoritative execution ticks and split the
proof work if at least five qualify. After that, an owned integration task can vendor and provenance-audit
a compatible Oseledets implementation, prove every exact transport, and
replace the identity wrapper with typed composition consuming all required
children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs
are empty. It does not satisfy `S56-M-1419-PROOF`, close an obligation or root,
change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
