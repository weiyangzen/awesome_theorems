# Scope map

## Preserved source scope

- Object: a heat kernel associated with an unspecified heat evolution.
- Claim: both an upper bound and a lower bound.
- Context: differential equations / partial differential equations.
- Historical metadata: twentieth century, attributed only to multiple mathematicians.

This is all the repository source fixes. In particular, "heat kernel" alone does not distinguish
the explicit Euclidean kernel from a fundamental solution for a variable-coefficient operator, a
Laplace-Beltrami heat kernel, a Dirichlet or Neumann kernel, or a discrete kernel.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze: the ambient space and dimension;
the operator and coefficient regularity/ellipticity; time domain and sign convention; boundary
conditions; the kernel definition and reference measure; symmetry, positivity, and conservativity
assumptions; the exact upper and lower inequalities; distance and volume terms; constants and their
dependencies; local versus global time range; on-diagonal versus off-diagonal scope; and every
geometric, analytic, or probabilistic hypothesis. It must address zero time, coincident points,
empty or disconnected domains, boundary points, and any excluded degenerate dimensions.

## Explicit exclusions

- The Euclidean Gaussian heat kernel formula as a substitute for a general estimate.
- Aronson, Li-Yau, manifold, bounded-domain, or graph bounds selected merely for API convenience.
- Treating the adjacent target `THM-M-1192` ("Gaussian upper bound") as this two-sided target.
- Treating positivity or a maximum principle alone as the requested quantitative lower bound.
- Treating the untrusted metadata label `已验证` as source or kernel evidence.

No formal candidate is adopted at intake. Candidate discovery and exact comparison belong to the
statement and anchor-audit phases after a source theorem has fixed the intended family.
