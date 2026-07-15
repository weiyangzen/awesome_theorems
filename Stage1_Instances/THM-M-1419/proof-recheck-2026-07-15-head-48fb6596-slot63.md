# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `48fb6596b1844f4183c411142415d872ff21e842`

Base tree: `eb8dfff0e90b5ce5b11ac2096777060d62874064`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot63`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the phase is not genuinely
self-tested, no `.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen target quantifies
a plain equivalence `T : Omega Equiv Omega`. Its `Ergodic T mu` hypothesis
supplies `Measurable T`, but no frozen hypothesis supplies
`Measurable T.symm`. Pinned mathlib's `Ergodic.symm` instead requires
`T : Omega MeasurableEquiv Omega`, whose structure stores forward and inverse
measurability separately.

This is material to the selected two-sided route, which constructs a backward
filtration over `T.symm`. The substantive external declaration
`ErgodicTheory.oseledets_splitting` has the same bimeasurable-base requirement.
The checked API comparison establishes a statement-to-route mismatch, not a
kernel-checked countermodel to the complete target, so the root stays
`[H2, M3, R3]` rather than being promoted to `M5`.

The prose freeze is also inconsistent with the Lean expression:
`statement.md` and `source-statement-crosswalk.md` say inverse measurability was
retained, while `MutationWithoutInverseMoment` removes only measurability of
the matrix inverse and its inverse logarithmic moment. It does not expose or
restore measurability of the base inverse. A proof worker cannot silently add
that missing premise. The statement must first be reopened, corrected to use a
measurable equivalence or an explicit inverse-measurability hypothesis, and
accepted with a new expression fingerprint and obligation-registry version.

## Remaining proof frontier

The direct prerequisite `S56-M-1419-OBLIGATION_TREE` remains `[_]`, not master
accepted `[x]`. Its frozen registry has 13 machine-required obligations; 12
lack terminal proof-body IDs. The only recorded body,
`target_of_construction_package`, returns a premise definitionally equal to the
whole target and consumes none of the four proof children recorded for
assembly, so it earns no substantive proof credit.

Repo-local `THM-M-1057` supplies checked Kingman limit theorems, but only as an
analytic input. It does not construct the exterior-power limits,
forward/backward filtrations, measurable splitting, equivariance, or vector
growth required by this target.

The external candidate is absent from the pinned Lake closure and targets Lean
`4.30.0-rc2` with mathlib `34f7a6cd...`, rather than this repository's Lean
`4.29.0` and mathlib `8a178386...`. A read-only compatibility scratch outside
the owned path has progressed substantially but still has no terminal
`SplittingAssembly.olean`; its first currently unresolved module is
`Extensions/DetIdentity`, rejected at an unavailable
`Function.det_eq_prod_eigenvalues` API. Scratch work receives no proof credit.
Even a completed compatible port would still require checked transports for
the missing base hypothesis, almost-everywhere versus pointwise cocycle
assumptions, norms, cocycle order, measurable subspaces, direct sums, positive
finrank, equivariance, and output indexing.

Prior structured proof rechecks record six unresolved execution ticks. Section
10.2 of the rev-5.6 standard therefore requires the master to stop relaunching
this unchanged oversized item and split/version the proof work after repairing
the statement. This worker may not edit the authoritative DAG.

## Fresh validation

All commands ran from this worker clone. No `lake update`, `lake build`, clone,
fetch, dependency repair, or `.lake` mutation was performed. The
automation-provided `.lake` symlink was reused read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | rank 688; planned; rework required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | 14 obligations and 41 typed edges passed; denominator `ad691633...5999`; root remains open `M3` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...716fb04` |
| fresh `lake env lean --trust=0 -t0` replay of `OseledetsStatement.lean` | 0 | exact target elaborated; fresh olean SHA-256 `f5222f72...3a9169` |
| fresh `lake env lean --trust=0 -t0` replay of `ObligationTree.lean` | 0 | conditional wrapper elaborated; axioms exactly `propext`, `Classical.choice`, `Quot.sound`; fresh olean SHA-256 `4fd543d8...50a6` |
| pinned mathlib API and external source inspection | 0 | `Ergodic.symm` and the candidate require `MeasurableEquiv`; the target has plain `Equiv` |
| current external-scratch inspection | 0 | upstream terminal source SHA-256 `e47ced0d...1c6e9407`; no terminal olean; current failing log SHA-256 `71bc905b...1dd4a` |
| scoped proof-input/pin diff from `b05dfe30...` to `HEAD` | 0 | empty; no target, architecture, Kingman, toolchain, manifest, or dependency input changed |
| token-anchored prohibited-device scan | 1 | expected no-match exit; no prohibited proof device occurs in target Lean files |

The replay copied the two target modules to a fresh temporary directory,
obtained `LEAN_PATH` through the pinned Lake environment, compiled fresh oleans
with `LEAN_NUM_THREADS=1`, `timeout 300`, `--trust=0`, and `-t0`, hashed the
outputs, and removed the directory. Cached target oleans were neither used as
outputs nor modified.

## Retry condition and boundary

Master must reopen and accept a repaired statement and new registry, then split
the oversized proof work. Only after that may workers integrate or implement
the complete Oseledets closure, all exact transports, and a typed composer that
consumes the frozen proof children. This file is current-base negative
nonrelease evidence only: it does not satisfy `S56-M-1419-PROOF`, close an
obligation or root, change scheduler state, establish audit/theorem completion,
or claim validation, release, receipt acceptance, or master acceptance.
