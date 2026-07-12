# Immutable Lean 4 anchor audit

Audit node: `S56-M-1129-ANCHOR_AUDIT`. Audit date: 2026-07-12. Base repository revision:
`797546bf2bab359f9fc5be515c3d4e8943c9d931`. The only exact target is
`Stage1.THM_M_1129.PoissonFormulaTarget` in `Statement.lean`. A candidate receives no root proof
credit unless its elaborated type is that proposition or a checked transport connects the types.

## Frozen discovery protocol

The bounded search used the aliases `Poisson formula`, `Poisson integral`, `two-dimensional wave
equation`, `wave equation`, `Kirchhoff`, `d'Alembert`, `method of descent`, `Laplacian`, and their
identifier-style variants. The order was repo-local Lean, the pinned mathlib source, GitHub
repository discovery, immutable candidate archives, then GitHub code search. Searches were made
without credentials. The cutoff was 2026-07-12 (Asia/Shanghai). External archives were streamed to
`/tmp` for inspection only; no dependency was cloned, fetched, installed, or added to `.lake`.

## Pinned mathlib inventory

The existing Lake artifacts pin mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean at `v4.29.0`. The mathlib worktree was clean.

| Module and declaration | Audited role | Exact-root disposition |
|---|---|---|
| `Mathlib.Analysis.InnerProductSpace.Laplacian`; `Laplacian.laplacian`, `InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis` | Laplacian used by the wave predicate, plus its coordinate expansion | statement/proof substrate only; no time evolution or wave representation |
| `Mathlib.Analysis.Calculus.ParametricIntegral`; `hasDerivAt_integral_of_dominated_loc_of_lip`, `hasDerivAt_integral_of_dominated_loc_of_deriv_le` | differentiation under a fixed-domain integral under explicit domination hypotheses | supporting bridge API only; the singular disk weight still needs integrability and domination proofs |
| `Mathlib.MeasureTheory.Integral.Bochner.Basic`; `integral_add`, `integral_smul`, `integral_map` | algebra and change-of-variables interfaces for Bochner integrals | substrate only; none proves the disk kernel identity or wave PDE |
| `Mathlib.Analysis.Complex.Harmonic.Poisson`; `InnerProductSpace.HarmonicOnNhd.circleAverage_poissonKernel_smul`, `InnerProductSpace.HarmonicContOnCl.circleAverage_poissonKernel_smul` | genuine mathlib Poisson integral formula for harmonic functions on complex disks | rejected name collision: boundary-circle harmonic identity, not the positive-time Cauchy formula for a wave on `R^2` |

`AnchorAudit.lean` checks every named declaration against the pinned environment and mutation-checks
that the harmonic Poisson proposition is not definitionally the wave-shaped proposition. Source
SHA-256 values are recorded in `anchor_audit_receipt.json`. Searches of all pinned mathlib Lean
sources found no declaration for a wave-equation Poisson formula, Kirchhoff wave formula, or method
of descent. The repo-local hits in `S1_M_144.lean` are wrappers for the same harmonic Poisson API;
the nonlinear-wave files provide local records or metadata, not this terminal theorem.

## External Lean 4 candidates

GitHub repository search returned no repository for the exact queries `"wave equation" Lean
theorem prover`, `"Poisson formula" Lean theorem prover`, `"Poisson integral" Lean4`, `Kirchhoff
wave Lean4`, or `dAlembert wave Lean4`. Broader `Lean4 PDE` searches identified four plausible
topic repositories. Their full HEAD revisions were frozen and their tarballs inspected.

| Project and immutable revision | Inspection result | Classification and feasibility |
|---|---|---|
| `rootkiller6788/mini-harmonic-pde-geometric-analysis` at `ed1d36973c213f42cc69c023ebbc535f50f530c0` | `MiniHyperbolicPDE/Complete.lean` has `theorem_poisson : String`; its value is prose saying the solution "involves integration". The implemented `dAlembertSolution` is a rational-valued 1D function omitting the velocity integral. The project uses Lean `v4.7.0`; no license was exposed by the repository API or archive. | `E5`, statement/prose-only false candidate. No terminal Prop, proof body, compatible dependency, or wrapper exists; do not integrate. |
| `SmaniaD/BesovSpacesGoodGrid` at `182e3864891111d746b0f1325c16c85f359cb04d` | complete Lean-source search found no query hit; project concerns Besov spaces/good grids and pins Lean `v4.30.0-rc2`, mathlib `5032702f...`. | topic-level false positive, no declaration; incompatible pin and no integration value |
| `raphaelrrcoelho/formal-mathfin` at `29ae0e91669ac23f29f7714d15742c0c1127730d` | complete Lean-source search found no wave-formula hit; the advertised PDE work is mathematical finance. Lean `v4.31.0`, mathlib `fabf563a...`. | domain false positive, no declaration; incompatible pin and no integration value |
| `vporton/atgt` at `087c4089fcee44527486b6fb995b5f7ab3d92290` | complete Lean-source search found no query hit; project is unrelated filter/topology work. Lean `v4.28.0-rc1`, mathlib `fd5e5373...`. | domain false positive, no declaration; incompatible pin and no integration value |

The first archive has SHA-256 `4f1b2652a4dde4ff521db77419d97c95273607a9f876dc0a86a6cde1ef610733`;
its inspected `Complete.lean` has SHA-256
`23f9c856f13e52ae45e2c83240a5f87d53bf8a49bb3ba824f100d7843a9396f0`.
The remaining archive hashes appear in the receipt. Because none supplies a formal candidate, there
is no terminal dependency closure or axiom profile that could honestly be credited.

GitHub's unauthenticated code-search API returned HTTP 401 (`Requires authentication`) for five
exact source queries. Two later repository searches were rate-limited with HTTP 403. These are
explicit coverage limitations: this is a replayable bounded audit, not a proof that no external
formalization exists. A newly located candidate reopens the inventory and must be frozen, type-
compared, trust-audited, and locally integrated before any machine closure credit.

## Result and status boundary

No exact mathlib or external Lean 4 closure was found. Root machine debt remains `M3`: the exact
statement elaborates locally, but its proof is absent. The first machine cut is the analytic
derivation of the disk representation from the classical wave hypotheses, including the singular
weight's integrability, differentiation under the integral, the Laplacian/time-derivative
calculation, initial-data recovery, and uniqueness/representation bridge.

This node's bounded candidate inventory is self-tested and suitable for the obligation-tree phase.
It does not establish `H0`, prove the target, close trust or release gates, accept a receipt, or make
the theorem complete. Lifecycle stays `planned`; master acceptance remains required.
