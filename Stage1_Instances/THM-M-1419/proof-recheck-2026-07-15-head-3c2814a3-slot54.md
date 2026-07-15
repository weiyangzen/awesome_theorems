# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `3c2814a370c2fee02158ca79aa44a48e411c4d18`

Base tree: `e1bd7e27bd922b779322c089410a471b6a1535f0`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot54`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not pass, no
`.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen Lean target uses
a plain equivalence `T : Omega Equiv Omega`. `MeasurePreserving T mu mu` and
`Ergodic T mu` supply forward measurability only; no hypothesis supplies
`Measurable T.symm`. Pinned mathlib stores inverse measurability as a separate
field of `MeasurableEquiv`, and its theorem `Ergodic.symm` requires such a
measurable equivalence.

This missing premise is material to the selected two-sided splitting theorem.
The previously recorded Bernoulli-shift triangular-cocycle obstruction explains
why a theorem with a bimeasurable base cannot simply be imported to prove this
target. This recheck does not kernel-formalize that countermodel, so it retains
the conservative root classification `[H2, M3, R3]` rather than claiming a
kernel-checked refutation.

The prose freeze is also inconsistent with the Lean expression:
`statement.md` and `source-statement-crosswalk.md` say inverse measurability was
retained, but the expression retains measurability of the matrix inverse only,
not of the base inverse. A proof worker cannot silently strengthen the target.
The statement must be reopened, corrected to use `MeasurableEquiv` or an
explicit `Measurable T.symm` hypothesis, and accepted with a new expression
fingerprint and obligation-registry version before positive proof work.

## Proof frontier

No relevant proof input changed between the strongest preceding recheck at
base `350285c4` and this base. The frozen registry still has 14 obligations and
41 typed edges; 12 of 13 machine-required obligations have no terminal proof
body. `target_of_construction_package` merely returns a premise definitionally
equal to the whole target and consumes none of the four recorded proof
children. Its successful elaboration is conditional-interface evidence, not a
proof of Oseledets' theorem.

The repo-local `THM-M-1057` Kingman declarations supply only an analytic input.
They do not construct the forward or backward Lyapunov filtrations, measurable
splitting, equivariance, or exact vector-growth conclusion.

A surviving read-only compatibility scratch contains all 62 ordered transitive modules
of `marcmorningstar/lean4-ergodic-theory@ed3fa6b...` and a trust-zero checked
`ErgodicTheory.oseledets_splitting`. It receives no proof credit: it is outside
the repository and pinned Lake closure; 26 transitive source files differ from
upstream; its theorem requires a measurable equivalence, pointwise matrix
measurability, and pointwise nonzero determinant; and no checked transports to
the frozen Pi-space, distance-to-fiber, direct-sum, cocycle-product, or output
interfaces exist. Its terminal source and olean hashes are respectively
`e47ced0d...1c6e9407` and `3f3165b7...d3067197`; the terminal axiom probe reports
exactly `propext`, `Classical.choice`, and `Quot.sound`. These are observational
scratch fingerprints only.

The prerequisite obligation-tree task remains provisional `[_]`, not master
accepted. Seven earlier proof-recheck JSON/Markdown pairs are already tracked,
while the authoritative DAG still records `attempts: 0`. This is an eighth
observed packet for the unchanged proof node. Section 10.2 requires unresolved
work to be split after five execution ticks. Only the master may determine
which packets count as ticks, reconcile attempts, reopen prerequisites, version
nodes, or change task state.

## Fresh validation

The automation-provided untracked `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root explicitly remains open `M3`. |
| Fresh disposable replay of `OseledetsStatement.lean` and `ObligationTree.lean` with `lake env lean --trust=0 -t0` | 0, 0 | Both elaborated under Lean 4.29.0; olean hashes were `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary files were removed. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` stores forward and inverse measurability separately, and `Ergodic.symm` requires `MeasurableEquiv`. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe proof injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| Read-only external scratch audit | 0 | All 62 ordered modules had oleans, 26 sources differed from upstream, terminal source matched upstream, and the terminal declaration used only the three allowed classical axioms above. |
| Scoped proof-input diff from `350285c4` to this base | 0 | Empty: target, architecture, anchor, Kingman sources, toolchain, and dependency manifest were unchanged. |

## Retry condition

The master must first reopen and repair `S56-M-1419-STATEMENT`, accept a new
exact expression and obligation-registry version, rerun prerequisite gates, and
reconcile the eight observed proof packets with the authoritative zero-attempt
record. If at least five unresolved packets count as execution ticks, the proof
node must be split rather than relaunched unchanged. After that, an owned
integration task can vendor and provenance-audit a compatible Oseledets
implementation, prove all exact transports, and replace the identity wrapper
with typed composition that consumes the required children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs are
empty. It does not satisfy `S56-M-1419-PROOF`, close an obligation or root,
change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
