# Scope map

## Preserved source scope

- Subject: a diffusion process.
- Claimed property: a moment estimate, named a Krylov estimate.
- Attribution and date: Nikolai Krylov, 1980, as repository metadata only.
- Target formal system: Lean 4 with mathlib.

This is all the mathematical scope fixed by the repository source. In particular, intake does not
silently replace "moment estimate" with the occupation-time estimate proposed by the legacy module.

## Decisions required before statement freeze

The statement phase must identify a primary edition and theorem/page, then freeze the process model
(SDE, martingale problem, or other diffusion), time horizon/stopping time, state dimension, drift and
diffusion coefficient assumptions, ellipticity regime, initial law, the estimated quantity, exponent
range, test-function space, reference measure, constant dependencies, and endpoint/degenerate cases.
It must determine whether "moment" means a moment of the process, an occupation integral, or another
quantity, rather than choosing the easiest available Lean encoding.

## Explicit exclusions

- A Krylov-Safonov Harnack estimate, which is separately tracked as `THM-M-1051`.
- A generic martingale, Kolmogorov continuity, or finite-dimensional moment inequality.
- An occupation-time `L^p` inequality unless a primary source crosswalk identifies it as this target.
- A structure containing boundedness, ellipticity, or the desired conclusion as supplied data.
- The metadata label `已验证` or elaboration of the legacy boundary as proof evidence.
