# Scope map

## Preserved repository scope

The intake preserves target `THM-M-0204`, the title `斯图尔特定理`, Matthew Stewart attribution,
year 1746, and literal gloss `三角形中线长度公式`. Importance and `已验证` are inventory metadata,
not source or proof evidence. The gloss commits only to a Euclidean triangle median-length family;
it does not contain a formula, definitions, binders, hypotheses, direction, or boundary policy.

The usual general-cevian Stewart theorem is a candidate interpretation, not the selected root.
Conversely, treating the gloss as the midpoint identity usually called Apollonius's theorem may
discard intended general-cevian scope. Only an approved source crosswalk may resolve this conflict.

## Proposition-changing decisions

An accepted statement phase must freeze all of the following from a pinpoint immutable source:

1. Whether the root is the general cevian identity, the median specialization, or an explicitly
   source-justified relationship between them.
2. The ordered triangle vertices, the endpoint side, the division point, and the mapping of every
   conventional side-length variable to an oriented pair of points.
3. For the general identity, whether the division point lies strictly between the endpoints,
   weakly between them, anywhere on the supporting line, or on an external extension, and whether
   directed or ordinary nonnegative lengths are used.
4. For the median identity, whether the midpoint is constructed by `midpoint`, supplied as a point
   with equal-distance/betweenness hypotheses, or encoded algebraically, and whether the
   conclusion solves explicitly for the median square or states an undivided equality.
5. The ambient domain: the Euclidean plane, a two-dimensional real affine inner-product space, or
   mathlib's arbitrary real inner-product affine torsor. A stronger dimensional generalization is
   not automatically source fidelity.
6. Triangle nondegeneracy, distinctness and noncollinearity requirements, side positivity, use of
   powers versus products, equality orientation, coercions, universes, typeclasses, and all ordered
   binders and hypotheses.
7. The source edition, exact theorem/page, incorporated definitions, proof boundary, translation,
   corrections, errata, historical attribution, and an independent source review.

These choices produce materially different propositions. This list is a resolution ledger, not a
theorem statement.

## Boundary cases to resolve

- Coincident endpoints `b = c`, all vertices equal, or exactly two vertices equal.
- A collinear or otherwise degenerate triangle and a zero-length median or cevian.
- The point equal to an endpoint, strictly internal, weakly internal, or external to the segment.
- Zero-, one-, two-, and higher-dimensional ambient affine spaces.
- Swapping endpoints, reversing the cevian, renaming vertices, or exchanging the two subsegments.
- Ordinary distances versus directed lengths for an external division point.
- Division by the base length or by two when rewriting the identity as a length formula.

No case is excluded at intake. In particular, pinned mathlib's midpoint theorem handles `b = c`,
whereas its general Stewart theorem assumes an angle of pi at the division point and therefore a
strict-betweenness convention through the angle API.

## Candidate encodings, not credited statements

| Candidate | Relationship to the catalog | Intake boundary |
|---|---|---|
| `EuclideanGeometry.dist_sq_mul_dist_add_dist_sq_mul_dist` | direct general-cevian Stewart identity | broader than the literal median gloss; angle/pi and ordinary-distance scope; source mapping open |
| `EuclideanGeometry.dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq` | direct midpoint/median identity | matches the gloss but is documented as Apollonius's theorem; may be a specialization rather than the intended root |
| a checked specialization of general Stewart at the midpoint | connects the two candidates | no source-approved canonical direction or checked dossier transport at intake |
| a coordinate-plane algebraic formulation | familiar textbook route | coordinate choices and transport to invariant distance geometry remain open |
| an explicit formula for the median square or length | literal “length formula” reading | division, nonnegativity, and square-root conventions change the target |

## Explicit exclusions and neighbors

The law of cosines, parallelogram law, Pythagorean theorem, and vector norm identities may support
a proof but cannot silently replace this root. A numerical diagram, a single triangle, a stored
premise containing the desired equality, an axiom, oracle, or unchecked certificate supplies no
credit. The catalog's untrusted status and a declaration-name match are not evidence.

`THM-M-0200` (Ceva), `THM-M-0203` (Heron), and `THM-M-0205` (Morley) own separate triangle
statements. The midpoint identity's conventional Apollonius name does not create or transfer state
from another target.

## First downstream gate

An accountable reviewer must preserve and independently approve an exact authoritative source
statement and resolve the general-cevian versus median mismatch and every choice above. Only then
may the statement phase encode one exact Lean proposition with minimal imports, serialize its
expression and environment fingerprints, compile any credited transport, and run all required
statement mutations.
