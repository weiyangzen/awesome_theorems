# THM-M-1135 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Laplace equation. The screened source label
does not identify a theorem: it gives only the topic-level wording "the fundamental equation of
harmonic functions." Consequently this intake preserves, rather than silently repairs, the source
ambiguity.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human source record | `Laplace方程`, attributed to Pierre-Simon Laplace (1785) | The repository research record is metadata, not a primary mathematical source |
| Intended equation | the classical scalar equation `Delta u = 0` | Dimension, scalar field, domain, regularity, and pointwise/weak interpretation are absent |
| Candidate root | a predicate saying a twice differentiable scalar function has zero Laplacian on a domain | Candidate only; no exact theorem can be frozen from the supplied wording |
| Nearby results | harmonic-function definition, mean-value property, maximum principle, boundary problems | Excluded from this target unless a later source audit identifies one as the intended claim |
| Lean surface | a future definition/theorem over a finite-dimensional real space | No declaration, import, elaboration, or proof credit is claimed at intake |
| Foundations | Lean 4 kernel and a pinned mathlib environment | Toolchain, imports, TCB, and foundation profile remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R3]`. The first failed gate is exact
source-statement identification: an equation/definition by itself is not a theorem and the screened
record supplies no quantified claim or assumptions. The statement phase must not choose a maximum
principle, existence theorem, uniqueness theorem, or harmonic-function characterization without
primary-source evidence. The theorem is not complete.

The structured scope is in `intake.json`, the source relationship and exact open questions are in
`source_statement_crosswalk.md`, and reproducible intake checks are in `validation.md`.
