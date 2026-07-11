# THM-M-1146 rev-5.6 intake

This is the `planned` intake dossier for the Schwarz reflection principle. The metadata source says
only "harmonic continuation"; to avoid silently substituting the more commonly named holomorphic
variant, the root is the real-valued harmonic, zero-boundary, odd-reflection theorem.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Geometry | An open planar domain invariant under conjugation; its upper part and interior real-axis portion | Arbitrary analytic arcs and nonsymmetric domains are excluded |
| Input | A real-valued harmonic function above the axis, continuous to and zero on the axis portion | The precise Lean regularity predicate is not selected yet |
| Construction | Odd reflection: `u z` above/on the axis and `-u (conj z)` below | Piecewise well-definedness and smoothness are future obligations |
| Result | Harmonicity on the full domain and agreement with the original function above | No uniqueness or maximal continuation claim |
| Related theorem | Holomorphic reflection for real boundary values | Candidate related encoding only; it receives no proof credit |
| Foundations | Lean 4 kernel and a pinned mathlib environment | Imports, version, axioms, TCB, and expression fingerprint remain open |

The structured binder order, assumptions, conclusion, boundary exclusions, and profiles are in
`intake.json`. Source fidelity and the unresolved ambiguity in the repository metadata are tracked
in `source_statement_crosswalk.md`.

## Open task DAG

`STATEMENT` must select definitions, elaborate the exact target, fingerprint the environment, and
mutation-test symmetry, openness, continuity, boundary vanishing, and sign. `ANCHOR_AUDIT` must then
search pinned Lean candidates and audit a primary mathematical source. `OBLIGATION_TREE`, `PROOF`,
`VALIDATION`, and `RELEASE` remain dependency-ordered and open. No downstream node is credited here.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M4, R3]`. The first failed gate is primary-source exact
statement identification, followed by Lean statement elaboration. The metadata label `已验证` is
untrusted discovery input, not evidence. The theorem is not complete.

## Validation

The commands and exact outcomes for this intake are recorded in `validation.md`. They check target
membership, repository structure, JSON syntax, local references, and whitespace only. No Lean
declaration or kernel result is claimed.
