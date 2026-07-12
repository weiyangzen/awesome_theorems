# Scope map

## Preserved repository scope

- Named result: Christoffel problem (`克里斯托费尔问题`).
- Attribution and date: Elwin Christoffel, 1865.
- Subject: differential geometry of convex surfaces.
- Available statement phrase: `凸体表面预定曲率问题` (a prescribed-curvature problem for the
  surface of a convex body).

The repository provides no mathematical definitions or bibliography. In particular, its phrase is
identical to the phrase attached to the adjacent Minkowski problem. Intake therefore cannot treat
the wording alone as an exact proposition.

## Candidate historical scope

The 1865 paper is the historical locator for a reconstruction problem from local curvature data.
Modern convex geometry commonly distinguishes the Christoffel problem by first area measure; for
a smooth convex surface in Euclidean three-space this is expressed using the sum of the principal
radii of curvature as a function of the outer unit normal. A typical solution statement must also
specify compatibility conditions and uniqueness modulo translation.

These observations identify a theorem family, not a canonical claim. Choosing the smooth function,
weak measure, or higher-dimensional formulation changes the domains, hypotheses, and conclusion.

## Decisions required before statement freeze

1. Pin a primary or authoritative modern source that states the exact existence and uniqueness
   theorem, including theorem/page and any errata.
2. Select dimension and the category of convex bodies: smooth/strictly convex bodies or general
   compact convex bodies.
3. Define the prescribed datum: sum of principal radii, first area measure, or another explicitly
   source-justified quantity.
4. Freeze positivity, regularity, balance/orthogonality, and nondegeneracy conditions on the datum.
5. State equality or uniqueness modulo translations and treat lower-dimensional bodies and
   degenerate data.
6. Select Lean encodings for Euclidean convex bodies, support functions, spherical measure, and
   curvature, then elaborate the exact proposition and check all claimed transports.

## Explicit exclusions

- The Minkowski problem prescribing surface-area/Gauss-curvature measure.
- A PDE existence theorem without the convex-body reconstruction and uniqueness conclusion.
- A uniqueness-only theorem or a theorem assuming the desired body already exists.
- Christoffel symbols, Levi-Civita connections, or unrelated results sharing Christoffel's name.
- An arbitrary prescribed-curvature statement with omitted compatibility conditions.
