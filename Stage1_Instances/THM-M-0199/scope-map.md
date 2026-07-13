# Scope map

## Preserved repository scope

- Target: `THM-M-0199`, named `梅涅劳斯定理` (Menelaus's theorem).
- Catalog attribution and date: Menelaus of Alexandria, approximately 100 CE.
- Literal gloss: `共线点的比例关系` ("the ratio relation of collinear points").
- Catalog category: Euclidean geometry; importance medium; `已验证` is untrusted metadata.

The named classical family is preserved. The short gloss is not expanded into a stronger
projective theorem, a weaker one-way implication, an unsigned metric special case, or a coordinate
identity without a reviewed source decision.

## Candidate classical reading, not credited

For a nondegenerate ordered triangle with vertices `A`, `B`, and `C`, take points `D`, `E`, and `F`
on the extended lines `BC`, `CA`, and `AB`, respectively. A common directed-segment convention says
that `D`, `E`, and `F` are collinear if and only if the product of the three correspondingly
oriented side ratios is `-1`. Reversing one or more numerator/denominator orientations changes the
displayed sign or reciprocal form without changing the underlying geometric theorem after a
checked transport.

This paragraph is a planning description. The catalog does not select its notation, convention,
direction, domain, or boundary cases, so it is not the canonical statement.

## Decisions required at statement freeze

1. Select an immutable, independently reviewed source proposition and map every incorporated
   definition, assumption, conclusion, proof boundary, correction, and erratum.
2. Fix an ordered triangle representation, its noncollinearity or affine-independence condition,
   ambient affine/Euclidean space, scalar field, characteristic and order assumptions, universes,
   and typeclass context.
3. Fix the correspondence between `D`, `E`, `F` and the three side lines, and whether points may lie
   only on closed segments, on complete affine lines, or at projective infinity.
4. Define directed segments or affine parameters and select the three ratio orientations, the
   product order, the right-hand sign, and every nonzero denominator hypothesis.
5. Decide whether the root is collinearity implying the ratio identity, the converse, an iff, or a
   source-approved package with checked projections.
6. Fix the collinearity predicate, ordered binders, hypotheses, conclusion, alternate encodings,
   checked transports, minimal Lean imports, and all required statement mutations.

## Degenerate and boundary cases

- repeated or collinear triangle vertices;
- a side point equal to a triangle vertex, producing a zero numerator or denominator;
- coincident side points or a transversal equal to a side line;
- points beyond a side versus points inside the closed side segment;
- finite affine points versus a side point at infinity;
- fields of characteristic two, arbitrary fields, ordered fields, or only real Euclidean spaces;
- alternate directed-length conventions, reciprocal ratios, product order, and displayed sign;
- a one-way theorem whose converse needs additional nondegeneracy clauses.

No case is silently excluded at intake. The statement phase must resolve each one against the
accepted source.

## Explicit non-substitutions

- Ceva's theorem: it characterizes concurrency of cevians, not collinearity of three side-line
  points. Its pinned mathlib body supplies no inherited Menelaus status.
- Desargues, Pappus, Pascal, Brianchon, Ptolemy, or another incidence theorem.
- An unsigned distance product that loses exterior-point signs unless a checked source-approved
  case split restores the full statement.
- A result about only interior points, a fixed coordinate triangle, or one numerical diagram used as
  the general theorem.
- A determinant identity without checked transports to side membership, directed ratios, and
  collinearity.
- A structure field, premise, axiom, oracle, or unchecked certificate containing the desired ratio
  identity or collinearity result.
- The catalog's `已验证` label, theorem name, modern citation, bounded search, or API probe used as H
  or M completion evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, affine triangles,
affine lines, `AffineMap.lineMap`, and `Collinear` provide plausible substrate. The neighboring
`Mathlib.LinearAlgebra.AffineSpace.Ceva` module proves a ratio-like concurrency theorem but does not
state Menelaus. Intake authenticates these interfaces only. The later statement phase must freeze
one exact root; the anchor audit must then repeat an immutable exhaustive search and classify any
actual proof body, dependencies, trust, and provenance.
