# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `9db995936e3354d71e109c055e31b9e9588569c5`

Base tree: `12006c9a7309e04bbf337d2b19dc0eeae3c9b265`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot65`

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
field of `MeasurableEquiv`, and `Ergodic.symm` requires such a measurable
equivalence.

This missing premise is material to the selected two-sided splitting theorem.
Earlier owned evidence records a future-sigma Bernoulli-shift triangular-cocycle
obstruction. This recheck does not kernel-formalize that countermodel, so it
retains the conservative root classification `[H2, M3, R3]` rather than claiming
a kernel-checked refutation.

The prose freeze is inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, and
`statement.md` calls the deleted data inverse measurability, but the expression
retains measurability of the matrix inverse only. A proof worker cannot silently
strengthen the target. The statement must be reopened, corrected to use
`MeasurableEquiv` or an explicit `Measurable T.symm` hypothesis, and accepted
with a new expression fingerprint and obligation-registry version before
positive proof work.

## Proof frontier

No scoped proof input changed since the strongest preceding current-environment
recheck. The frozen registry still has 14 obligations and 41 typed edges; 12 of
13 machine-required obligations have no terminal proof body.
`target_of_construction_package` merely returns a premise definitionally equal
to the complete target and consumes none of the four recorded proof children.
Its successful elaboration is conditional-interface evidence, not a proof of
Oseledets' theorem.

The repo-local `THM-M-1057` Kingman declarations supply only an analytic input.
They do not construct the forward or backward Lyapunov filtrations, measurable
splitting, equivariance, or exact vector-growth conclusion.

A surviving read-only compatibility scratch contains all 62 ordered transitive
modules of `marcmorningstar/lean4-ergodic-theory@ed3fa6b...` and a trust-zero
checked `ErgodicTheory.oseledets_splitting`. It receives no proof credit: it is
outside the repository and pinned Lake closure; 26 transitive sources differ
from upstream; its theorem requires `T : X MeasurableEquiv X`, pointwise matrix
measurability, and pointwise determinant nonvanishing; and no exact wrapper or
transports to the frozen interfaces exist. The terminal source and olean hashes
are `e47ced0d...1c6e9407` and `3f3165b7...d3067197`; a fresh terminal probe
reported exactly `propext`, `Classical.choice`, and `Quot.sound`. These are
observational scratch fingerprints only.

The prerequisite obligation-tree task remains provisional `[_]`, not master
accepted. Eight earlier proof-recheck JSON/Markdown pairs are already tracked,
while the authoritative DAG still records `attempts: 0`. This is a ninth
observed packet for the unchanged proof node. Section 10.2 requires unresolved
work to be split after five execution ticks. Only the master may determine
which packets count as ticks, reconcile attempts, reopen prerequisites, version
nodes, or change task state.

## Fresh validation

The automation-provided untracked `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network command, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root explicitly remains open `M3`. |
| Disposable copies of `OseledetsStatement.lean` and `ObligationTree.lean`, compiled from `Formalizations/Lean` with pinned `LEAN_PATH`, `lake env lean --trust=0 -t0`, and 300-second bounds | 0, 0 | Both elaborated under Lean 4.29.0; olean hashes were `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary files were removed. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` stores inverse measurability separately, and `Ergodic.symm` requires `MeasurableEquiv`. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe proof injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| Scoped proof-input diff from `3c2814a3` to this base | 0 | Empty: target, architecture, anchor, Kingman sources, toolchain, and dependency manifest were unchanged. |
| Trust-zero external terminal probe | 0 | `ErgodicTheory.oseledets_splitting` elaborated with the three allowed classical axioms above; output SHA-256 was `6f3cf561...98f1`; scratch receives no proof credit. |
| `python3 -m json.tool` on the structured companion | 0 | JSON parsed successfully. |
| `git diff --no-index --check -- /dev/null` on each new artifact | 1 expected | Both files differed from `/dev/null`; diagnostic output was empty, so no whitespace error was reported. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists. |

The structured companion records the full disposable replay command, hashes,
environment pins, trust boundary, known failures, and retry cut set.

## Retry condition

The master must first reopen and repair `S56-M-1419-STATEMENT`, accept a new
exact expression and obligation-registry version, rerun prerequisite gates, and
reconcile the nine observed proof packets with the authoritative zero-attempt
record. If at least five unresolved packets count as execution ticks, the proof
node must be split rather than relaunched unchanged. After that, an owned
integration task can vendor and provenance-audit a compatible Oseledets
implementation, prove all exact transports, and replace the identity wrapper
with typed composition that consumes the required children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs are
empty. It does not satisfy `S56-M-1419-PROOF`, close an obligation or root,
change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
