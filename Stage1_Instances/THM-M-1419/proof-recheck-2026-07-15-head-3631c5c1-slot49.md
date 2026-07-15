# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `3631c5c14fbe46cb219d7fb03b5a64c50782e8f0`

Base tree: `640bca710e5550b90f0727860958561186ccb51f`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot49`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the phase did not genuinely close,
no `.stage1-worker-selftest.json` is emitted.

The first failed gate is exact-target fidelity at `M1419-S-INTERFACE`. The
frozen target quantifies a plain equivalence `T : Omega Equiv Omega`.
`MeasurePreserving T mu mu` and `Ergodic T mu` supply `Measurable T`, but no
frozen hypothesis supplies `Measurable T.symm`. Pinned mathlib records inverse
measurability as a separate field of `MeasurableEquiv`; its `Ergodic.symm`
theorem requires a measurable equivalence. A fresh disposable Lean probe
rejected `exact hT.measurable` at the goal `Measurable T.symm`, reporting that
the term has type `Measurable T` instead.

This is material to the selected two-sided measurable splitting. Earlier owned
evidence records a future-sigma-algebra Bernoulli-shift triangular-cocycle
obstruction in which the required equivariant fast line depends on past
coordinates. That countermodel is not kernel-formalized, so this packet
conservatively retains machine state `M3`; it does not claim a checked
refutation or promote the root to `M5`.

The prose freeze is inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, but
the proposition assumes measurability only of the matrix-valued inverse and
not of the base inverse. A proof worker may neither add the missing premise nor
replace the target with the conventional measurable-equivalence theorem.

## Proof frontier

No substantive proof input changed between the previous current-base packet at
`0c26cec0...` and this base. Pinned mathlib contains no Oseledets,
multiplicative-ergodic, Lyapunov-filtration, subadditive-ergodic, or Kingman
terminal declaration. Repo-local `THM-M-1057` supplies checked Kingman limit
theorems, but those are analytic inputs and do not construct the forward and
backward filtrations, measurable splitting, equivariance, or vector-growth
closure.

The separately owned `THM-M-1056` tree contains a substantive Lean 4.29 port
whose terminal `ErgodicTheory.oseledets_splitting` requires
`T : X MeasurableEquiv X`, pointwise matrix measurability, and pointwise
determinant nonvanishing. It proves a differently scoped target. No checked
transport supplies the missing inverse base measurability or all required
almost-everywhere representative, Pi/Euclidean norm, cocycle-order,
subspace-measurability, direct-sum, finrank, equivariance, growth, and indexing
bridges. Its proof item is provisional `[_]`, its receipt says
`accepted=false`, and it is not an accepted dependency of `THM-M-1419`.

The frozen validator still reports 14 obligations and 41 typed edges with
denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
and leaves the root open at `M3`. Twelve of 13 machine-required obligations
have no terminal proof-body ID. The sole recorded body,
`target_of_construction_package`, merely returns a premise definitionally equal
to the complete target and consumes none of its four required graph children.
It therefore supplies no substantive proof or composition credit.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted `[x]`. Twenty earlier recheck packet pairs plus the older
blocker are tracked while the authoritative proof item records zero attempts.
Rev-5.6 section 10.2 requires an unresolved item to be split after five
execution ticks. Only the master may reconcile packets with authoritative
ticks, reopen prerequisites, split or version the node, or change task state.

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
| Fresh `/tmp` trust-zero replay of copied `OseledetsStatement.lean` and `ObligationTree.lean`, plus a `Mathlib.Util.AssertNoSorry` probe, through the existing `lake env` Lean path with explicit temporary roots/outputs, `-j1`, and 300-second bounds | 0, 0, 0 | All elaborated; the declarations were sorry-free; olean hashes were `f5222f72...3a9169`, `4fd543d8...50a6`, and `dc3bc6cd...fee9`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| Disposable derivation probe with `hT : Ergodic T mu`, goal `Measurable T.symm`, and body `exact hT.measurable`, through pinned `lake env` Lean with `--trust=0 -j1` and a 300-second bound | 1 expected | Lean reported `hT.measurable : Measurable T` but expected `Measurable T.symm`; no olean was produced; log SHA-256 was `d74589c9...b8a7bdb`; temporary files were removed. |
| Pinned mathlib terminal-name search | 1 expected | No Oseledets, multiplicative-ergodic, Lyapunov-filtration, subadditive-ergodic, or Kingman terminal declaration was found. |
| Repo-local Kingman declaration inspection | 0 | Located `tendsto_kingman`, `tendsto_kingman_ergodic`, and `tendsto_kingman_ergodic_means`; none is an Oseledets splitting closure. |
| Read-only hash and type/state inspection of the `THM-M-1056` terminal, proof source, receipt, and DAG entry | 0 | Terminal requires `MeasurableEquiv`; hashes remain `e47ced0d...e9407`, `e93f37d7...a69`, and `c9916f9c...01a7`; sibling proof is `[_]` and receipt `accepted=false`. |
| `git diff --name-status 0c26cec0...HEAD -- <scoped proof inputs; evidence packets excluded>` | 0 | Empty output: target source, architecture, Kingman input, sibling port, toolchain, and dependency manifest are unchanged. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-1419/proof-recheck-2026-07-15-head-3631c5c1-slot49.json >/dev/null` | 0 | The structured blocker packet parsed successfully. |
| `git diff --check`, then `git diff --no-index --check /dev/null <new-file>` for each packet file | 0, 1 expected, 1 expected | No whitespace diagnostics; each no-index command returned Git's expected nonempty-diff status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest was emitted for the blocked proof phase. |

The replay wrote target oleans only below fresh temporary directories and
removed them. It verifies that the exact statement and circular wrapper remain
sorry-free and elaborate; it does not prove the open Oseledets construction
package.

## Retry condition

The master must first reopen `S56-M-1419-STATEMENT`, replace the plain base
equivalence with a measurable equivalence or add `Measurable T.symm`, accept a
new exact expression fingerprint and obligation-registry version, and rerun
the statement, source, mutation, anchor, and obligation-tree gates. It must
also reconcile the accumulated negative packets with authoritative execution
ticks and split this proof item if at least five qualify. Later owned child
tasks can then integrate the compatible Oseledets route, implement every exact
almost-everywhere and representation transport, and replace the identity
wrapper with typed composition consuming all required children.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs
are empty; root vector remains `[H2, M3, R3]`. It does not satisfy
`S56-M-1419-PROOF`, close an obligation or root, change scheduler state, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.
