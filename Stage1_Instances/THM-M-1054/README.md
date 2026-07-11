# THM-M-1054 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the von Neumann mean ergodic theorem. The
repository's source gloss is "L2 ergodic theorem"; this intake freezes its standard
measure-preserving-transformation form without inheriting the source label `已验证` as evidence.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | L2-norm convergence of positive-length Cesaro averages of Koopman iterates | No Lean expression or fingerprint exists yet |
| Ambient objects | Probability measure space, measurable measure-preserving endomorphism, real-valued L2 class | General sigma-finite, complex, and Hilbert-valued variants are not part of the root |
| Limit | Orthogonal projection onto the closed subspace fixed by the Koopman operator | Identification with conditional expectation is a candidate transport |
| Operator reduction | Koopman is an L2 isometry and the Hilbert-space mean ergodic theorem applies | Architecture only; no bridge is credited |
| Boundary behavior | Identity and non-ergodic transformations are included; average length is positive | Pointwise or almost-everywhere convergence is excluded |
| Foundations | Lean 4 kernel plus a versioned policy for classical choice, quotients, integration, and Hilbert projection | Exact profile and dependency fingerprint remain open |

The later obligation tree must at least expose the L2 Koopman construction, preservation of the L2
norm, bounded linear operator structure, fixed-subspace closure and projection, the abstract Cesaro
convergence theorem, and the checked transport back to functions. These are prospective nodes, not
proof claims.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the statement gate: the exact mathlib object model, ordered Lean binders, normalized expression,
environment fingerprint, transports, and mutation tests remain absent. The theorem is not complete.

## Validation

The commands and exact outcomes in `validation.md` validate membership, repository consistency,
JSON syntax, and dossier structure only. No Lean declaration or kernel proof is claimed.
