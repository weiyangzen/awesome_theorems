# THM-M-0597 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the tubular neighborhood theorem. Historical
Stage1 code is discovery material only and contributes no accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A smoothly embedded submanifold of a finite-dimensional smooth Riemannian manifold has a tubular neighborhood modeled on its normal bundle | Exact Lean binders, boundary conventions, and expression fingerprint belong to the statement phase |
| Input geometry | smooth embedding, tangent restriction, metric orthogonal normal bundle, zero section | Existing mathlib representations must be identified and pinned |
| Output geometry | open zero-section domain, open ambient neighborhood, diffeomorphism, and agreement with inclusion | Retraction-only or proposition-field packages are not silently substituted |
| Construction | normal exponential map, local invertibility along the zero section, and global shrinking/injectivity | Architecture only; no leaf is credited closed |
| Variants | Euclidean ambient space and unique-normal-coordinate/retraction forms | These need checked specializations or equivalences |
| Edge policy | empty and whole-manifold carriers are boundary probes | They cannot establish the general root; compact/uniform-radius and boundary variants are excluded |
| Foundations | Lean 4 kernel and a pinned mathlib manifold stack | Toolchain, imports, trust profile, and TCB fingerprint remain open |

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_253.lean` contains a useful
candidate API and checked special cases. Its `StatementShape` still uses proposition-valued stand-ins
for essential geometry and is therefore only a candidate for later statement work, not the frozen
formal root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no accepted elaborated expression, environment fingerprint,
checked source transport, or mutation suite. The theorem is not complete.

## Validation

The commands and exact intake-only results are recorded in `validation.md`. They establish target
membership, repository-standard consistency, JSON syntax, and dossier hygiene only. No Lean kernel
closure is claimed.
