# Scope map

## Preserved theorem family

The intake preserves the catalog family conventionally called Heron's formula: the area of a
Euclidean triangle is determined by its three side lengths through a semiperimeter expression. A
familiar candidate presentation is

```text
s = (a + b + c) / 2,
area = sqrt (s * (s - a) * (s - b) * (s - c)).
```

This is a scope description, not the frozen canonical proposition. The repository itself supplies
neither this formula nor definitions and assumptions that select one of its variants.

## Decisions required at statement freeze

1. Admit and independently review an immutable source edition, exact proposition, incorporated
   definitions and proof boundary, translation, historical attribution, corrections, and errata.
2. Fix the triangle model: three points in the Euclidean plane, a two-dimensional real
   inner-product affine space, a general real inner-product affine torsor, or abstract positive
   side lengths satisfying source-selected triangle inequalities.
3. Fix the area object. Possibilities include nonnegative geometric area, absolute signed area,
   half an orientation form or determinant, `1 / 2 * a * b * sin gamma`, or a separately defined
   measure of a convex hull. These are not definitionally interchangeable.
4. Fix ordered binders and side correspondence. For points `p1 p2 p3`, decide which distances are
   `a`, `b`, and `c`, which angle is `gamma`, and how vertex permutations are transported.
5. Fix nondegeneracy: three distinct noncollinear vertices, two adjacent sides nonzero as in the
   pinned candidate, nonnegative side lengths with weak triangle inequalities, or strict triangle
   inequalities.
6. Fix semiperimeter syntax and arithmetic coercions, multiplication association, use of
   `Real.sqrt`, and the proof that its radicand is nonnegative in the selected domain.
7. Decide whether the canonical equality is the nonnegative square-root formula, the squared
   identity `area^2 = s(s-a)(s-b)(s-c)`, the trigonometric-to-radical equality used by the pinned
   candidate, or a checked package of equivalent forms.
8. Fix equality orientation, universes, typeclass parameters, foundation and computation profiles,
   and every alternate encoding with a kernel-checked transport.

## Boundary and degenerate cases

- all three points equal, exactly two points equal, or one of the two sides around the chosen angle
  having length zero;
- three distinct collinear points, including both between and same-ray configurations;
- valid degenerate side triples such as `a + b = c`, which conventionally yield zero area;
- arbitrary nonnegative triples that violate a triangle inequality and need not describe a
  Euclidean triangle;
- zero-, one-, two-, and higher-dimensional ambient affine spaces;
- orientation reversal and vertex permutations;
- negative radicands for nongeometric inputs and the totalized behavior of `Real.sqrt`;
- equality between a geometric area and its absolute, signed, trigonometric, determinant, or
  measure encoding.

No case is excluded at intake because no proposition has been selected.

## Candidate formal encoding, not credited

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Theorems100.heron` takes three points in a real inner-product affine torsor, assumes
`p1 != p2` and `p3 != p2`, defines the three distances and semiperimeter, and concludes that the
trigonometric triangle-area expression equals the usual square root. This is a close formal lead,
but its two-side nonzero hypotheses do not assert noncollinearity, its left side is an area formula
rather than a separately defined area object, and it lives in the optional `Archive` library.

The statement phase must compare that exact type with a source-approved canonical claim. The later
anchor audit must separately establish import feasibility, exact expression identity or checked
transport, terminal proof-body provenance, dependency and axiom closure, placeholder and unsafe
boundaries, and trust acceptance.

## Excluded substitutions

- Brahmagupta's formula for a cyclic quadrilateral, owned by `THM-M-0202`;
- the shoelace formula, determinant/cross-product area formula, or `1 / 2 * a * b * sin gamma`
  used alone as the root without the side-only Heron equality;
- the law of cosines, Pythagorean theorem, law of sines, or a triangle-inequality theorem used as
  the root rather than as a dependency;
- only the squared formula when the selected source requires a nonnegative area equality, or only
  the square-root formula when the source selects a polynomial identity;
- a numeric example such as the `3-4-5` triangle, floating-point computation, plotted diagram, or
  unverified algebraic normalization;
- a premise, structure field, axiom, oracle, or certificate that stores the desired equality;
- the catalog's `已验证` field, a citation, a theorem name, source compilation, or an intake probe
  treated as source or machine-proof credit.

## Neighbor boundaries

`THM-M-0202` separately owns Brahmagupta's cyclic-quadrilateral formula, `THM-M-0204` Stewart's
cevian-length theorem, and `THM-M-0193` the Pythagorean theorem. Those may supply later dependencies
only after exact statement and obligation freezes; none shares status or proof credit with this
target.
