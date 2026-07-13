# Scope map

## Preserved catalog scope

The intake preserves the family named by `Talagrand集中不等式` and the literal gloss
`凸Lipschitz函数的集中`: concentration of convex Lipschitz functions, attributed to Michel
Talagrand in 1995. It does not add a formula that the catalog never supplied. The duplicate catalog
block is provenance from metadata deduplication and supplies no second source or proof credit.

## Candidate family, not credited as a statement

A commonly cited Talagrand consequence says that a convex Lipschitz real-valued function of
independent bounded coordinates has Gaussian-type concentration around a median, with scale set by
the coordinate support diameters and the Lipschitz constant. This description is intentionally only
a family boundary. Neither it nor a remembered constant is the canonical proposition.

The inspected 1995 source instead presents general product-space inequalities for sets. Section 4.1
defines a convex hull distance from a point to a set and proves an exponential moment and tail
bound. Its introduction explicitly declines to state an abstract functional version. Any future
functional theorem must therefore cite a pinpoint source corollary or supply a reviewed derivation
from the set theorem; name similarity alone is insufficient.

## Proposition-changing decisions

An approved statement phase must freeze all of the following:

- the primary edition, exact theorem/corollary/page, incorporated definitions, proof boundary,
  corrections and errata, and an independent source review;
- the number and index type of coordinates, coordinate measurable spaces, individual probability
  laws, product-measure construction, independence encoding, and finite versus infinite product;
- whether coordinates lie in real intervals, bounded subsets of normed spaces, two-point spaces, or
  another source-defined support, together with exact diameter or radius bounds;
- the ambient real vector/normed space, norm used for Lipschitz continuity, scalar field, convexity
  on the entire ambient space versus only a convex support, and all universe/typeclass context;
- the real-valued function, measurability/integrability assumptions, Lipschitz constant convention,
  convex versus quasiconvex or separately convex hypothesis, and whether concave functions enter by
  negation;
- the center: a chosen median, lower/upper median, expectation, or another quantile, including
  existence and nonuniqueness conventions;
- upper, lower, or two-sided deviation event; strict versus non-strict comparison; exact prefactor,
  exponent, universal constant, parameter domain, and scaling by support and Lipschitz constants;
- ordered binders, hypotheses, conclusion, alternate encodings and checked transports; and
- foundation, classical-choice, quotient, noncomputability, TCB, and computation policies.

## Boundary cases to resolve

- zero coordinates; zero-dimensional ambient spaces; empty or singleton coordinate types;
- point-mass laws, zero-diameter supports, empty intervals, and infinite or unknown diameters;
- constant functions, zero Lipschitz constant, zero or negative deviation parameter, and zero scale;
- nonunique medians, atoms at the median, expectation undefined or infinite, and null exceptional
  sets;
- functions convex only on the support, extended-real functions, nonmeasurable functions, and
  almost-everywhere representatives;
- one coordinate versus arbitrary finite products and dimension-dependent versus dimension-free
  constants; and
- equality at the event boundary and coercions among real, nonnegative real, and extended
  nonnegative real probability bounds.

## Explicit exclusions

- `THM-M-1081`, whose catalog phrase is concentration of configuration functions and whose intake
  treats the convex-distance/product-configuration family separately.
- Talagrand's Gaussian transportation-cost (`T2`) inequality or another entropy-transport theorem.
- Gaussian isoperimetry or `THM-M-0996` silently used as the product bounded-coordinate result.
- McDiarmid, Azuma-Hoeffding, Hoeffding, Chernoff, or generic bounded differences with convexity
  omitted.
- A set-only convex-distance inequality presented as the requested function theorem without a
  checked, source-reviewed derivation.
- A fixed distribution, fixed dimension, one-sided special case, weakened constant, or asymptotic
  statement substituted for the selected source root.
- A structure, predicate, hypothesis, or sub-Gaussian assumption that already stores the desired
  tail conclusion.
- The catalog's `已验证` label, a citation, an API probe, or a bounded search used as proof credit.

## Lean and execution boundary

Pinned mathlib exposes `ConvexOn`, `LipschitzWith`, finite and infinite product measures, and
sub-Gaussian tail interfaces. These are vocabulary only. The intake does not freeze minimal imports,
a target expression, expression/environment fingerprint, transports, mutations, discovery protocol,
obligation registry, proof architecture, or terminal proof body. Those remain downstream tasks.
