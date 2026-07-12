# THM-M-1227 immutable anchor audit

## Verdict

The pinned mathlib checkout contains the analytic substrate needed to express the frozen target,
but no terminal Leray-Hopf or Navier-Stokes existence declaration. The inspected external Lean 4
candidate defines weak-solution structures but contains no existence theorem or proof body.
Consequently the canonical target remains `M4`; the remaining debt is `formalization_debt`, not
repo-local integration debt.

## Pinned mathlib

The `lake-manifest.json` pin and installed checkout both identify mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A case-insensitive source search for `Leray`,
`LerayHopf`, `NavierStokes`, `Navier-Stokes`, and `weak solution` found only explanatory prose in
`Mathlib.Analysis.Distribution.TestFunction`; it found no terminal declaration. `AnchorAudit.lean`
elaborates probes for `TestFunction`, `fderiv`, `ContDiff`, `integral`, `Integrable`, `volume`, and
measure restriction. These are useful substrate only.

This is a bounded negative result over the immutable pinned Mathlib source tree, not a claim that
no relevant Lean development can exist elsewhere.

## External candidate

`lean-dojo/LeanMillenniumPrizeProblems` was inspected at immutable commit
`540da94826f70f3edf4d4fc66ce6cda20e903f61` (toolchain `leanprover/lean4:v4.26.0`, Apache-2.0).
`Problems/NavierStokes/Navierstokes.lean` declares `NavierStokes.WeakSolution` and
`NavierStokes.LerayHopfSolution`. The latter merely extends the former with an energy-inequality
field. It is finite-horizon, includes pressure and forcing, and supplies every analytic condition
as structure data. There is no theorem producing the structure from finite-energy divergence-free
initial data. It therefore cannot inhabit, transport to, or close the frozen whole-space global
existence target.

GitHub repository discovery on 2026-07-12 returned zero repositories for the exact phrase
`Leray-Hopf` with Lean language and 16 noisy repositories for `Navier-Stokes` with Lean language.
This metadata query is not treated as exhaustive code search. The structured ledger records its
scope and the exact source hash for the candidate actually inspected.

## Classification

Human existence mathematics is known, but neither audited surface supplies an exact public Lean 4
proof. No external proof exists here that merely awaits pin/import/check, so
`repo_local_integration_debt` is not assigned. The result is `formalization_debt`; root state stays
`M4`, with `[H2, M4, R4]` unchanged. This phase makes no source-fidelity, proof, audit-completion,
or theorem-completion claim.
