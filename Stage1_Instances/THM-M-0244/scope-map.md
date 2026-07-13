# THM-M-0244 scope map

## Preserved catalog boundary

The intake preserves exactly the Phragmen-Lindelof maximum-principle family for holomorphic
functions on an angular complex domain. It does not freeze one proposition merely because a
primary paper and a pinned Lean theorem family are available. The catalog does not select a
numbered source theorem or supply the clauses needed to distinguish the variants.

## Candidate mathematical components

A later statement phase may select a root only after source review fixes all of the following:

1. Whether the domain is an open sector, its closure, a connected subdomain contained in a sector,
   a coordinate quadrant, a half-plane, or a strip obtained by an exponential or logarithmic map.
2. The sector vertex and orientation, its opening angle, whether the two boundary rays are included,
   and the treatment of the vertex and the point at infinity.
3. Whether `f` is scalar-valued or Banach-valued, holomorphic in the interior and continuous on the
   closure, or satisfies the source's older monogenic and single-valued-modulus conditions.
4. The exact boundary estimate: pointwise `|f| <= C` on both rays, the paper's limiting condition
   `(A)` at every finite boundary point, equality or vanishing on the boundary, or another variant.
5. The interior growth restriction and its relationship to the angle: fixed order below the
   reciprocal-angle threshold, little-o exponential growth for every positive epsilon, a Big-O
   power-exponential estimate, or a double-exponential strip estimate.
6. Whether the conclusion is `|f z| <= C` on the sector or closure, strict inequality for a
   nonconstant function, equality or zero propagation, extensionality, boundedness, or constancy of
   an entire function bounded along sufficiently dense rays.
7. Every ordered binder, universe, typeclass assumption, asymptotic filter, coercion, and checked
   transport between source notation and the chosen Lean expression.

These choices change hypotheses and conclusions. They are not harmless formatting conventions.

## Boundary and degenerate cases

Source and statement review must resolve a zero or reflex angle; a half-plane or full-plane limit;
the origin; a zero or negative boundary constant; constant and zero functions; boundary equality;
failure of continuity at the vertex or infinity; functions at the exact critical growth order;
growth strictly below, equal to, or above the angle threshold; empty or disconnected domains; and
whether an arbitrary angular region is required rather than only the four coordinate quadrants.

## Excluded substitutions

- `THM-M-0503`, the unresolved zeta-function Lindelof hypothesis, is unrelated to this maximum
  principle and cannot be substituted.
- `THM-M-1332`, Picard-Lindelof ODE existence and uniqueness, is a distinct theorem family.
- `THM-M-0225`, the maximum modulus principle on bounded domains, is an ingredient rather than this
  unbounded-domain extension.
- A horizontal or vertical strip, coordinate quadrant, or right-half-plane theorem cannot silently
  replace a source-selected arbitrary sector without a checked equivalence or implication of the
  required direction.
- Equality, zero-propagation, and extensionality corollaries do not replace the norm-bound root.
- A proposition field, hypothesis, or structure that stores the desired maximum bound is not a
  proof, and the catalog's verified label is not evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the module
`Mathlib.Analysis.Complex.PhragmenLindelof` contains complete proofs of representative strip,
coordinate-quadrant, and right-half-plane principles. The quadrant proof transports through the
complex exponential to `PhragmenLindelof.horizontal_strip`; the strip proof uses the bounded
maximum modulus principle on rectangles. The module does not expose a theorem parameterized by an
arbitrary opening angle or arbitrary rotated sector. The later statement and anchor-audit phases
must select a source proposition, establish exact identity or a checked transport, and audit the
terminal body, transitive dependencies, axioms, trust, and provenance. The intake probe establishes
only importability and declaration types.
