# Scope map

## Preserved theorem family

The intake preserves the catalog's Euclidean-geometry family: for a right triangle, the square of
the side opposite the right angle equals the sum of the squares of the two adjacent sides. It does
not replace this with a numerical Pythagorean-triple statement, the converse, or a generic identity
whose hypothesis already stores the desired equation.

The inspected Euclid lead names a triangle `ABC` with the right angle at `C`, hypotenuse `AB`, and
legs `AC` and `BC`. Pinned mathlib's most direct affine candidate takes points `p1 p2 p3`, places
the angle at `p2`, and writes the squared hypotenuse `dist p1 p3 * dist p1 p3` first. These are
plausibly transportable presentations, but intake does not assert their exact identity.

## Decisions required at statement freeze

1. Preserve and independently review an authoritative source edition, pinpoint proposition,
   incorporated definitions, proof boundary, translation, corrections, and errata.
2. Fix the ordered points and right-angle vertex. For an `A-B-C` Lean ordering, specify whether the
   premise is `angle A B C = pi / 2` and the hypotenuse is `AC`.
3. Fix the ambient domain: the Euclidean plane, a two-dimensional real affine inner-product space,
   or mathlib's general real inner-product affine torsor. General dimension is not automatic source
   fidelity merely because a library theorem supports it.
4. Decide whether a triangle must have three distinct noncollinear vertices. Euclid's ordinary
   triangle convention and mathlib's intentionally degenerate-compatible angle theorem have
   different boundary surfaces.
5. Fix the conclusion's syntax and orientation: constructed-square area equality, squared
   distances using `^ 2`, or multiplication `d * d`; and hypotenuse-square-first versus
   leg-squares-first.
6. Decide whether the canonical root is only the forward implication or the stronger iff. Euclid
   Book I Proposition XLVIII owns the converse; it must not be silently bundled into Proposition
   XLVII or the catalog gloss.
7. Fix universes, typeclass parameters, namespace/options, foundation profile, and every explicit
   or inferred binder before expression hashing and mutation tests.

## Boundary cases to resolve

- repeated points, a zero-length leg, or all three points equal;
- distinct but collinear points and whether an angle expression can equal `pi / 2` there;
- zero-dimensional, one-dimensional, two-dimensional, and higher-dimensional ambient spaces;
- arbitrary affine inner-product torsors versus the coordinate plane;
- equality at an unoriented angle of `pi / 2` and the library's zero-vector angle convention;
- swapping the two legs, reversing endpoint order, and renaming vertices;
- multiplication versus exponent notation over nonnegative real distances.

No case is excluded at intake. A later source-approved statement must either include a case or
state and justify its exclusion.

## Candidate encodings, not credited statements

| Candidate | Relationship to the catalog | Intake boundary |
|---|---|---|
| `EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_iff_angle_eq_pi_div_two` | direct affine distance/angle iff | stronger iff and broader degenerate/domain scope; source transport open |
| forward projection of that iff | close to the one-way catalog gloss | no checked canonical wrapper or fingerprint at intake |
| `InnerProductGeometry.norm_add_sq_eq_norm_sq_add_norm_sq'` | vector right-angle formulation | vector sum is not yet mapped to three ordered triangle points |
| inner-product-zero norm identity | algebraic orthogonality form | right-angle and affine-point transports remain open |
| Euclid I.47 constructed-square area equality | inspected human-source formulation | area-to-distance-square transport and exact definitions remain open |

## Excluded substitutions

- Euclid I.48 or a forward-and-converse package used as the received one-way theorem;
- classification or generation of integer Pythagorean triples;
- the law of cosines, parallelogram law, polarization identity, or orthogonal projection theorem
  used as the root rather than a dependency or transport;
- only the coordinate identity `(x + y)^2 = x^2 + 2*x*y + y^2`;
- only a `3-4-5` example, numerical computation, diagram, or area experiment;
- a premise, structure field, axiom, oracle, or certificate that assumes the squared-side equality;
- a theorem-name match, catalog status, source citation, or API probe treated as proof credit.

## Neighbor boundaries

`THM-M-0194` (Thales' theorem), `THM-M-0195` (Euler line), and other Euclidean-geometry targets own
distinct statements. Pythagorean-triple APIs used by the FLT dossier are number-theoretic
classification results and do not define or receive proof credit for this affine triangle root.

## First downstream gate

The statement phase must admit an independently reviewed exact source claim, resolve every choice
above, encode only that claim with minimal pinned imports, preserve its elaborated expression and
environment fingerprint, compile any credited transports, and run the four required mutation
classes. Until then the canonical expression, obligation registry, and proof credit stay empty.
