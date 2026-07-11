# Scope map

## Preserved source scope

- Object: a double-layer potential, understood only at the level of the repository's name.
- Construction: some boundary integral involving a kernel derivative and a boundary density.
- Claimed role: a boundary integral representation for an unspecified boundary-value problem.
- Historical scope: nineteenth-century potential theory with no named author or theorem anchor.

This is all the repository record fixes. In common usage, a double-layer potential may itself be a
definition, while a representation theorem or its boundary traces are distinct results. Intake
does not conflate them.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the operator (for example Laplace or
Helmholtz), ambient dimension and scalar field, fundamental-solution normalization, domain and
boundary regularity/orientation, surface measure, density space, normal-derivative convention,
interior or exterior region, solution and equality notions, and all decay or compatibility
hypotheses. It must distinguish the potential's definition from harmonicity away from the boundary,
a Green representation formula, boundary jump limits, and an integral-equation consequence.
Degenerate dimensions, empty boundary, zero density, boundary points, and singular-integral
interpretations must be addressed where applicable.

## Explicit exclusions

- The single-layer potential or Newton potential as a substitute.
- The jump relation, catalogued separately as `THM-M-1160`, unless it is merely a cited dependency.
- An arbitrary boundary integral declared equal to a solution by hypothesis.
- A formula specialized to a sphere or half-space without source justification.
- The untrusted `已验证` label as evidence of a human proof or kernel closure.

The eventual Lean target must expose the concrete kernel, boundary integral, density, domain, and
represented conclusion, or record a precise foundational/API blocker.
