# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `dc0f0264c1db312ac95025747d3212b689facb5e`

Base tree: `633bea3a2e72674768ee426a035a1850b9940ae7`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot64`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. No worker self-test manifest is emitted.

## First failed gate

Exact-target fidelity fails before proof implementation. The frozen target
quantifies a plain equivalence `T : Omega Equiv Omega`. Its
`MeasurePreserving T mu mu` and `Ergodic T mu` hypotheses provide
`Measurable T`, but they do not provide `Measurable T.symm`. Mathlib's theorem
`Ergodic.symm` instead requires `T : Omega MeasurableEquiv Omega`.

This missing inverse-measurability premise matters to the selected two-sided
splitting theorem. The substantive external candidate
`ErgodicTheory.oseledets_splitting` likewise requires a measurable equivalence.
The earlier structured blocker records a mathematical Bernoulli-shift
obstruction to recovering the required measurable equivariant splitting from
forward measurability alone. Because that obstruction is not kernel-formalized,
the root remains `[H2, M3, R3]`; this recheck does not promote it to `M5`.

The statement must first be reopened, changed to use `MeasurableEquiv` or to add
an explicit `Measurable T.symm` hypothesis, and re-elaborated. That correction
requires a new statement fingerprint and obligation-registry version plus fresh
statement, source, anchor, and obligation-tree acceptance. A proof worker may
not silently strengthen the assigned proposition.

This is also a statement-freeze mismatch: `statement.md` and
`source-statement-crosswalk.md` say that the selected proposition retains
inverse measurability, but the Lean target retains only measurability of the
matrix-valued function `fun omega => (A omega)⁻¹`, not measurability of the
base inverse `T.symm`.

## Proof frontier after prerequisite repair

No exact placeholder-free root body is in the pinned closure. The frozen
registry has 13 machine-required obligations; 12 lack terminal proof-body IDs.
The current `target_of_construction_package` theorem merely returns a premise
definitionally equal to the complete target and consumes none of the four proof
children recorded for assembly.

The repo-local `THM-M-1057` Kingman declarations are checked analytic inputs,
not an Oseledets closure. They do not construct the exterior-power limits,
forward/backward filtrations, measurable splitting, equivariance, or vector
growth needed here.

The external candidate at
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
is absent from the pinned Lake closure and targets Lean `4.30.0-rc2` with
mathlib `34f7a6cd...`, not this repository's Lean `4.29.0` and mathlib
`8a178386...`. Existing modified compatibility scratch trees contain at most
34 oleans and no `SplittingAssembly.olean`; these noncanonical scratch results
receive no proof credit. Even a completed port would still need checked
transports for almost-everywhere versus pointwise assumptions, Pi versus
Euclidean norms, cocycle order, measurable subspaces, direct sums, positive
finrank, equivariance, and output indexing.

## Fresh validation

All commands ran from this worker clone. No `lake update`, `lake build`, clone,
fetch, or dependency mutation was run. The automation-provided `.lake` symlink
was reused read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688; planned; rework required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | 14 obligations and 41 typed edges passed; denominator `ad691633...5999`; root remains open `M3` |
| `(cd Formalizations/Lean && lake env lean --version)` | 1 | shared pinned `flt-regular` checkout could not resolve `HEAD`; no repair or fetch was attempted |
| direct pinned Lean `--version` | 0 | Lean `4.29.0`, commit `98dc76e3...716fb04` |
| disposable direct trust-zero replay of statement and wrapper with existing dependency oleans | 0 | exact target and identity wrapper elaborated; axioms exactly `propext`, `Classical.choice`, `Quot.sound`; olean hashes `f5222f72...3a9169` and `4fd543d8...50a6` |
| current external-scratch inspection | 0 | terminal source hash `e47ced0d...1c6e9407`; at most 34 scratch oleans present; no terminal olean |
| scoped proof-input/pin diff from `63a9ed9c...` to `HEAD` | 0 | empty; no target, architecture, Kingman, manifest, toolchain, or dependency proof input changed |
| token-anchored prohibited-device scan | 1 | expected no-match exit: no proof placeholder, axiom declaration, or unsafe injection token occurs in target Lean files |

`lake env lean` is unavailable because the shared canonical `flt-regular`
checkout has no resolvable `HEAD`. The direct pinned-executable replay used only
already-present oleans and temporary output under `/tmp`; it is narrow
nonrelease fallback evidence, not a substitute for the required Lake gate.

## Retry condition and boundary

Reopen and accept the repaired statement and a new registry version first.
Then compatibly integrate or locally implement the complete Oseledets closure,
prove every exact transport, and replace the identity wrapper with a checked
composer consuming all four required children. This blocker is negative
nonrelease evidence only: it does not satisfy the proof item, close an
obligation or root, change scheduler state, establish audit/theorem completion,
or claim master acceptance.
