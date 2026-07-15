# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `952a52b764e12269aeeeccdb678e3e83e1c49ba8`

Base tree: `d024f123bc0a0a408d43b12bb9d0cc3b77c9e522`

Attempt date: `2026-07-16` (`Asia/Shanghai`)

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

## Proof frontier

No relevant positive input changed since the preceding integrated packet. The
target statement, frozen architecture, repo-local Kingman input, sibling
Oseledets proof body, toolchain, and dependency lock are unchanged; the only
scoped change from the preceding base is that packet itself.

The tracked 62-module Lean 4.29 compatibility port under the separately owned
`THM-M-1056` path contains the substantive theorem
`ErgodicTheory.oseledets_splitting`, but its exact base binder is
`T : X MeasurableEquiv X`; it also has pointwise matrix measurability and
pointwise determinant nonvanishing. It cannot inhabit this weaker
plain-equivalence/almost-everywhere target. No checked wrapper supplies the
missing inverse base measurability or all required representative,
Pi/Euclidean norm, cocycle-order, subspace-measurability, direct-sum, finrank,
equivariance, growth, and indexing transports. Its proof node is provisional
`[_]`, its receipt says `accepted=false`, and it is not an accepted dependency
of this target.

Pinned mathlib contains no Oseledets, multiplicative-ergodic,
Lyapunov-filtration, subadditive-ergodic, or Kingman terminal declaration.
Repo-local `THM-M-1057` supplies checked Kingman limit theorems only; those do
not construct an Oseledets splitting.

The frozen validator still reports 14 obligations and 41 typed edges with
denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
and explicitly leaves the root open at `M3`. Twelve of 13 machine-required
obligations have no terminal proof-body ID. The sole recorded body,
`target_of_construction_package`, merely returns a premise definitionally
equal to the complete target and consumes none of the four required proof
children. It supplies no substantive proof or composition credit.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not
master accepted `[x]`. Twenty-three earlier recheck pairs and one older blocker
are tracked while the authoritative proof item still records zero attempts.
Rev-5.6 section 10.2 requires splitting after five unresolved execution ticks.
The master must reconcile durable packets with authoritative ticks and split or
version this oversized item if at least five qualify; a worker may not edit
that authority.

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
| `cd Formalizations/Lean && env -u LEAN_PATH lake --version && env -u LEAN_PATH lake env lean --version` | 0 | Lake `5.0.0-src+98dc76e`; Lean `4.29.0`, commit `98dc76e3...716fb04`. |
| Fresh `/tmp` trust-zero replay of copied `OseledetsStatement.lean` and `ObligationTree.lean`, plus a `Mathlib.Util.AssertNoSorry` probe, through the existing `lake env` Lean path with explicit roots/outputs, `-j1`, and 300-second bounds | 0, 0, 0 | All elaborated; the wrapper was sorry-free; olean hashes were `f5222f72...3a9169`, `4fd543d8...50a6`, and `09bf8e19...5a6219`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| Disposable derivation probe with `hT : Ergodic T mu`, goal `Measurable T.symm`, and body `exact hT.measurable`, through pinned Lean with `--trust=0 -j1` | 1 expected | Lean reported `hT.measurable : Measurable T` but expected `Measurable T.symm`; no olean was produced; log SHA-256 was `bcc1f3d1...540481f`; temporary files were removed. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability, `MeasurableEquiv` stores inverse measurability separately, and `Ergodic.symm` requires `MeasurableEquiv`. |
| Pinned mathlib terminal-name search | 1 expected | No relevant terminal declaration was found. |
| Repo-local Kingman and tracked `THM-M-1056` type/state inspection | 0 | Kingman supplies analytic inputs only; the Oseledets terminal requires `MeasurableEquiv`; its proof task is `[_]` and receipt is unaccepted. |
| `git diff --name-status f26cfacf...HEAD -- <scoped proof inputs>` | 0 | Only the preceding `THM-M-1419` recheck pair was added; no statement, architecture, Kingman proof, Oseledets proof body, toolchain, or dependency pin changed. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| `python3 -m json.tool <this-packet>.json` plus fail-closed semantic assertions | 0 | The structured packet parsed; item, base, state, verdict, closure flags, receipt lists, and changed paths passed. |
| `git diff --check -- <this-packet>.{md,json}` | 0 | Both owned handoff artifacts passed the whitespace check. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest was emitted. |

The replay wrote oleans only below fresh temporary directories and removed
them. It verifies that the exact statement and circular wrapper still
elaborate without placeholders; it does not prove the open Oseledets package.

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
