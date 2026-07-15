# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `90a1d52c43113012c8aa0e2b110da02e58ce1724`

Base tree: `bc399f3ba59411f2a72d4f29d98eb85e7689b28c`

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
`exact hT.measurable` at the goal `Measurable T.symm` with that exact type
mismatch.

This is material to the selected two-sided theorem rather than a missing
syntactic transport. Earlier owned evidence records a future-sigma-algebra
Bernoulli-shift triangular-cocycle obstruction: the equivariant fast line must
depend on past coordinates and therefore cannot satisfy the target's
measurability requirement. That countermodel is not kernel-formalized here, so
the root remains conservatively classified `M3`, not `M5`.

The statement prose is also inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, but
the proposition retains only measurability of the matrix inverse and never
assumes measurability of the base inverse. A proof worker may not silently add
that premise. The statement must be reopened and versioned before exact
positive proof work can proceed.

## Candidate update

The complete placeholder-free Lean 4.29 source port of
`marcmorningstar/lean4-ergodic-theory` has now been integrated under the
separately owned target `THM-M-1056`. Its terminal declaration is
`ErgodicTheory.oseledets_splitting` in
`External/Oseledets/ErgodicTheory/TwoSided/SplittingAssembly.lean`; its proof
explicitly invokes the backward filtration through `hT.symm`. This is useful
repo-local discovery evidence, but it cannot close this item:

- its theorem requires `T : X MeasurableEquiv X`, pointwise `Measurable A`,
  and pointwise determinant nonvanishing;
- the frozen target has only a plain equivalence and almost-everywhere matrix
  measurability and invertibility;
- the sibling proof item and receipt are provisional `[_]`, not master
  accepted, and are not an accepted dependency of `THM-M-1419`;
- no checked bridge supplies inverse base measurability or all required
  representative, Pi/Euclidean norm, cocycle-order, subspace-measurability,
  direct-sum, finrank, equivariance, growth, and indexing transports.

The integrated terminal source has SHA-256
`e47ced0d869724a402369352f0ac0bd1f4bb8e57cfd7cefc2a44fa071c6e9407`.
Its sibling proof source has SHA-256
`e93f37d77807b8e7f8ac027f45955186159cd4a1e2370d1609f1f6bad05a2a69`,
and its provisional receipt has SHA-256
`c9916f9c13eb16561b0e66d216ff22ce2b32324d5435f49ee6a9e9eef8d901a7`.
These hashes authenticate inspected inputs only; they provide no proof credit
for this differently scoped target.

## Frozen architecture

The obligation-tree validator passes 14 obligations and 41 typed edges with
denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
but explicitly leaves the root open at `M3`. Twelve of 13 machine-required
obligations have no terminal proof-body ID. The sole recorded body,
`target_of_construction_package`, consumes a package definitionally equal to
the complete target, so it is a conditional identity wrapper rather than a
substantive composition of the four required proof children.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional rather than
master accepted. Seventeen earlier proof-recheck packets plus one older blocker
are tracked while the authoritative DAG still records zero attempts. Section
10.2 requires an unresolved item to be split after five execution ticks. Only
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
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root explicitly remains open `M3`. |
| `cd Formalizations/Lean && lake --version && lake env lean --version` | 0 | Lake `5.0.0-src+98dc76e`; Lean `4.29.0`, commit `98dc76e3...716fb04`. |
| Fresh temporary trust-zero replay of `OseledetsStatement.lean` and `ObligationTree.lean` through the existing `lake env lean` environment, with explicit temporary roots/outputs and 300-second bounds | 0, 0 | Both modules elaborated; olean hashes were `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| Disposable exact derivation probe using `hT.measurable` at goal `Measurable T.symm` under `lake env lean --trust=0` | 1 expected | Lean reported `hT.measurable : Measurable T`, while `Measurable T.symm` was required; the temporary probe was removed. |
| Pinned mathlib terminal-name search | 1 expected | No Oseledets, multiplicative-ergodic, Lyapunov-exponent/filtration, subadditive-ergodic, or Kingman terminal declaration was found. |
| Repo-local Kingman declaration inspection | 0 | `THM-M-1057` supplies analytic Kingman inputs only, not an Oseledets splitting. |
| Read-only inspection and hashing of the integrated `THM-M-1056` terminal, proof source, receipt, and task state | 0 | The terminal requires `MeasurableEquiv`; the sibling item is provisional `[_]`, `accepted=false`, and proves a different target. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| `git diff --check` before this packet, followed by `git diff --no-index --check /dev/null <new-file>` for each packet file | 0, 1 expected, 1 expected | The tracked diff had no whitespace errors; each new-file check returned Git's expected nonempty-diff status with no whitespace diagnostic. |

The replay wrote target oleans only under fresh `/tmp` directories and removed
them. It confirms that the exact statement and circular wrapper still
elaborate; it does not prove the open Oseledets construction package.

## Retry condition

The master must first reopen `S56-M-1419-STATEMENT`, replace the plain base
equivalence with a measurable equivalence or add `Measurable T.symm`, accept a
new exact expression fingerprint and obligation-registry version, and rerun
the source, mutation, anchor, and obligation-tree gates. It must also reconcile
the tracked negative packets with authoritative execution ticks and split this
oversized proof item if at least five qualify. After that, an owned integration
task can provenance-audit the Lean 4.29 port, implement the exact
almost-everywhere and representation transports, and add checked composition
consuming every required child.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs
are empty; root vector remains `[H2, M3, R3]`. It does not satisfy
`S56-M-1419-PROOF`, close an obligation or root, change scheduler state, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.
