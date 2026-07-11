# THM-M-1188 rev-5.6 intake

This directory is the `planned` instance for the weak maximum principle for the heat equation. The
Stage0 label only says "maximum principle for parabolic equations" and leaves its hypotheses open.
For an executable target, this intake selects the standard classical heat-operator result described
in `intake.json`; stronger, weak-solution, and variable-coefficient variants are explicitly excluded.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Space-time domain | bounded open `U` in finite-dimensional Euclidean space and finite `T > 0` | no unbounded domains or manifolds |
| Operator | `u_t - Laplacian u <= 0` | no general uniformly parabolic coefficients |
| Solution class | classical interior derivatives and continuity through the closed cylinder | no Sobolev, viscosity, or distributional solutions |
| Boundary | initial face plus lateral boundary (the parabolic boundary) | the terminal face is not boundary data |
| Conclusion | global maximum equals the parabolic-boundary maximum | not the strong principle or equality classification |
| Formalization | Lean 4/mathlib encoding to be selected | no declaration, expression hash, or machine closure yet |

The anticipated architecture has definition nodes for the cylinder and parabolic boundary, an
extreme-value/compactness node, the strict perturbation `u_epsilon = u - epsilon t`, an interior
maximum derivative-sign contradiction, a limiting argument, and boundary recomposition. This is a
scope map, not a frozen obligation registry or proof-tree completion claim.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that a standard
textbook statement anchor has been identified but primary historical provenance, edition-page
verification, assumptions, errata, and independent review remain open. `M4` records that no exact
Lean expression has been selected or elaborated. The first failed theorem gate is the Lean statement
gate. The theorem is not complete.

## Validation

The exact commands and results in `validation.md` check manifest membership, repository-standard
consistency, JSON syntax, dossier-local references, and whitespace only. They provide intake-node
evidence and no theorem proof credit.
