# THM-M-0324 rev-5.6 intake

This directory is the `planned` intake for Enflo's theorem. The repository summarizes the claim as
"Banach spaces need not have a basis." Here "basis" is provisionally read as a Schauder basis, not
an algebraic Hamel basis: every vector space has a Hamel basis under choice, whereas Enflo's 1973
counterexample concerns approximation by finite-rank operators and implies the absence of a
Schauder basis.

The conservative human root is: **there exists a Banach space with no Schauder basis**. Enflo's
primary paper constructs the stronger separable reflexive counterexample without the approximation
property. The implication from a Schauder basis to the bounded approximation property is part of
the source argument, but its exact hypotheses and the paper's Theorem 1 must still receive a
pinpoint, line-by-line source review. Consequently this intake freezes the theorem family and the
non-substitution boundary, but leaves the exact Lean target to the statement phase.

Pinned mathlib defines `SchauderBasis` and its finite-rank partial-sum projections.
`Statement.lean` now elaborates the exact selected real-scalar target using an existentially bundled
Banach space, with separability and infinite dimension excluding nonseparable and finite-dimensional
shortcuts. It checks a sigma-presentation transport, structural mutations, and the zero-space
boundary. It does not construct Enflo's space or prove the existential root.

The provisional vector remains `[H1, M3, R4]`. Lifecycle is `planned`; accepted proof state is empty.
There is no claim of H0, M0, R0, audit completion, or theorem completion. See `scope-map.md`,
`source-statement-crosswalk.md`, `statement.json`, `statement-validation.md`, `task-dag.json`, and
`validation.md` for the frozen boundary and exact checks performed.
