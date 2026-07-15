# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `b98f9f4368d78fd9f600d1619f36d55ed0d6f751`

Base tree: `166b9e92bfa134dcffd9b1c707f1e26cad247239`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot65`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not pass, no
`.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen Lean target uses
a plain equivalence `T : Omega Equiv Omega`. `MeasurePreserving T mu mu` stores
forward measurability, and `Ergodic T mu` extends it, but neither supplies
`Measurable T.symm`. Pinned mathlib stores inverse measurability separately in
`MeasurableEquiv`; its `Ergodic.symm` theorem requires such a measurable
equivalence.

This missing premise is material to the selected two-sided splitting theorem.
Earlier owned evidence records a future-sigma Bernoulli-shift triangular-cocycle
obstruction, but no kernel-checked countermodel to the complete target exists.
The conservative root classification therefore remains `[H2, M3, R3]` rather
than being promoted to `M5`.

The prose freeze is inconsistent with the Lean expression.
`source-statement-crosswalk.md` says inverse measurability was retained, while
the proposition retains measurability of the matrix inverse only and never
assumes measurability of the base inverse. A proof worker cannot silently add
that hypothesis. The statement must be reopened, corrected to use
`MeasurableEquiv` or an explicit `Measurable T.symm` premise, and accepted with
a new expression fingerprint and obligation-registry version before positive
proof work can proceed.

## Proof frontier

No scoped proof input or dependency pin changed since the immediately preceding
recheck. The frozen registry still has 14 obligations and 41 typed edges; 12 of
13 machine-required obligations have no terminal proof body.
`target_of_construction_package` merely returns a premise definitionally equal
to the complete target. It consumes none of the four proof children recorded
for assembly, so its successful elaboration supplies no substantive proof
credit.

Pinned mathlib has no Oseledets, multiplicative-ergodic, or Kingman terminal
declaration. The repo-local `THM-M-1057` Kingman theorems provide only an
analytic limit input; they do not construct forward/backward filtrations,
measurable splitting, equivariance, or vector-growth closure.

A read-only compatibility scratch contains a trust-zero checked
`ErgodicTheory.oseledets_splitting` from
`marcmorningstar/lean4-ergodic-theory@ed3fa6b...`. It receives no proof credit:
it is outside the repository and pinned Lake closure, and no exact wrapper
exists. More importantly, its input is `T : X MeasurableEquiv X` with
pointwise matrix measurability and determinant nonvanishing. The frozen target
has only a plain equivalence and almost-everywhere matrix hypotheses. Exact
Euclidean/Pi norm, cocycle order, measurable-subspace, direct-sum, finrank,
equivariance, and output-indexing transports also remain unproved. The scratch
terminal source and olean hashes are `e47ced0d...1c6e9407` and
`3f3165b7...d3067197`; a fresh probe reported only `propext`,
`Classical.choice`, and `Quot.sound`.

The prerequisite obligation-tree task is only provisional, not master
accepted. Nine earlier proof-recheck packets plus one older blocker are tracked,
while the authoritative DAG records zero attempts. Section 10.2 requires an
oversized item to be split after five unresolved execution ticks. Only the
master may decide which packets count as ticks, reconcile attempts, reopen
prerequisites, split or version nodes, or change task state.

## Fresh validation

The automation-provided untracked `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network command, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root remains open `M3`. |
| `cd Formalizations/Lean && lake --version && lake env lean --version` | 0 | Lake `5.0.0-src+98dc76e`; Lean `4.29.0`, commit `98dc76e3...716fb04`. |
| Disposable copies of `OseledetsStatement.lean` and `ObligationTree.lean`, compiled with pinned `LEAN_PATH`, `lake env lean --trust=0 -t0`, and 300-second bounds | 0, 0 | Both elaborated; olean hashes `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms exactly `[propext, Classical.choice, Quot.sound]`. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` stores inverse measurability separately, and `Ergodic.symm` requires `MeasurableEquiv`. |
| Pinned mathlib terminal-name search | 1 expected | No Oseledets, multiplicative-ergodic, or Kingman terminal declaration was found. |
| Repo-local Kingman declaration inspection | 0 | Found checked analytic inputs only, not an Oseledets splitting closure. |
| Trust-zero external terminal probe in the read-only compatibility scratch | 0 | `ErgodicTheory.oseledets_splitting` elaborated with the three classical axioms above; scratch receives no proof credit. |
| Scoped proof-input diff from `9db99593` to this base | 0 | Empty: target, architecture, anchor, Kingman sources, toolchain, and dependency manifest were unchanged. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |

The structured companion records the exact hashes, environment pins, trust
boundary, known failures, and remaining root cut set.

## Retry condition

The master must first reopen and repair `S56-M-1419-STATEMENT`, accept a new
exact expression fingerprint and obligation-registry version, and rerun all
prerequisite gates. It must also reconcile the tracked negative packets with
the authoritative zero-attempt record and split the proof item if at least five
count as unresolved execution ticks. After that, an owned integration task can
vendor and provenance-audit a compatible Oseledets implementation, prove every
exact transport, and replace the identity wrapper with typed composition that
consumes all four required children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs are
empty. It does not satisfy `S56-M-1419-PROOF`, close an obligation or root,
change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
