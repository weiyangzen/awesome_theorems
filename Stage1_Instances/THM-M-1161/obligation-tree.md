# THM-M-1161 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 19 semantic obligations before proof execution. Seventeen are required
machine obligations; `X-SOURCE` and `X-TCB` are informational overlays. No obligation is excluded
because an adjacent mathlib theorem exists, and no obligation is marked closed. Any correction,
split, merge, eligibility, exclusion, or risk change requires a version-2 append-only delta.

## Typed proof route

```text
M1161-ROOT [open M4]
`-- M1161-T-ASSEMBLE [conditional composition checked]
    |-- M1161-B-DICHOTOMY
    |-- M1161-B-TRIVIAL
    |   |-- M1161-L-BIJECTIVE
    |   |   `-- M1161-X-SPECTRAL
    |   `-- M1161-N-TRANSPORT
    |       `-- M1161-N-OPERATOR
    |           `-- M1161-S-SOLVES
    `-- M1161-B-NONTRIVIAL
        |-- M1161-L-CLOSED-RANGE
        |-- M1161-L-ORTHOGONAL
        |   `-- M1161-X-ADJOINT
        `-- M1161-C-ADJOINT
```

## root

The root is the full frozen pointwise integral-equation alternative, not the nearby spectral
eigenvalue/resolvent theorem.

## s-model

The model fixes the compact measured domain, complex Hilbert space, continuous kernel, injective
function realization, compact operator, integrability, and pointwise integral equality.

## s-solves

`Solves` retains the pointwise equation and is not silently replaced by an abstract operator
equation. The equivalence is owned by `N-OPERATOR` and `N-TRANSPORT`.

## s-boundary

Lambda zero, zero kernel, zero datum, trivial kernel, and nontrivial kernel remain in scope.

## s-foundation

The selected foundation is classical complex Hilbert-space analysis. The conditional composition
currently reports `propext`, `Classical.choice`, and `Quot.sound`; transitive trust remains open.

## n-operator

This node proves that the pointwise equation is faithfully represented by
`(I - lambda T) phi = f`, using `operator_eq_integral` and `realize_injective`.

## n-transport

This node transports zero solutions, existence, uniqueness, range membership, and equality between
the operator and pointwise formulations. It is material proof work, not a definitional slogan.

## b-dichotomy

This exhaustive branch separates trivial from nontrivial homogeneous kernels. Classical logical
decidability and its exact use must be exposed by the proof phase.

## b-trivial

The first branch must derive unique solvability for every datum from the trivial homogeneous
kernel, rather than merely show absence of a selected eigenvalue.

## b-nontrivial

The second branch retains both a nonzero homogeneous solution and the biconditional adjoint
compatibility condition for every datum.

## c-adjoint

This construction owns `Astar = adjoint (I - lambda T)` and the identification of its kernel with
adjoint homogeneous solutions.

## l-bijective

This analytic engine upgrades injectivity of the compact perturbation of the identity to
bijectivity, with a separate valid lambda-zero path.

## l-closed-range

This node establishes that the range of `I - lambda T` is closed. It cannot be inferred from the
orthogonal-complement identity alone.

## l-orthogonal

Using closed range and adjoint identities, this node proves the exact equivalence between range
membership and orthogonality to the adjoint kernel.

## x-spectral

The pinned `hasEigenvalue_or_mem_resolventSet` theorem is a supporting boundary. Its statement does
not itself close either root branch.

## x-adjoint

The pinned `orthogonal_range` theorem is another supporting boundary; the closed-range and
pointwise transports remain separate obligations.

## x-source

The primary-source edition, pinpoint pages, assumptions, errata, and node mapping remain `H1` and
require independent review.

## x-tcb

Full declaration provenance, axiom closure, compiled dependencies, and reproducible validation are
release work and remain open.

## t-assemble

`root_compose` consumes the dichotomy plus both conditional branch results and yields the exact
restated root. It proves only composition: all analytic premises remain open.

## Status boundary

All step budgets are at most 100, but they are architecture estimates rather than proof evidence or
`R0`. Separate proof, refinement, provenance, evidence, trust, documentation, and workflow graphs
are stored in `typed-graphs.json`. This phase claims neither analytic closure, human-source review,
readability review, audit completion, theorem completion, release readiness, nor master acceptance.
