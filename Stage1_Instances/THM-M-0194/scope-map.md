# Scope map

## Received claim

`Docs/researches/math_theorems.md` fixes the title `泰勒斯定理`, the attribution Thales of Miletus,
an approximate date of 600 BCE, and the gloss `圆周角等于圆心角的一半` (an inscribed angle is half
the central angle). It does not state the domains, ordered binders, hypotheses, angle convention,
or conclusion as a proposition. This intake preserves the theorem family and its unresolved choices
rather than supplying them from memory.

## Candidate classical boundary

A common form chooses a circle with center `O`, chord endpoints `B` and `C`, and a circumference
point `A`. The central angle `BOC` and inscribed angle `BAC` must subtend the same chord or selected
arc. A source-faithful statement must still decide:

- whether angles are ordinary values in `[0, pi]`, directed values modulo `2 * pi`, or another
  Euclidean convention;
- which arc or side contains `A`, and whether the central angle is minor or reflex;
- whether the conclusion is `central = 2 * inscribed`, `inscribed = central / 2`, or a congruence;
- whether the ambient object is the Euclidean plane, an oriented real inner-product affine space,
  or a higher-dimensional sphere with a coplanarity condition;
- which points must be pairwise distinct, whether the chord endpoints may coincide, and whether a
  radius-zero circle or a circumference point equal to an endpoint is allowed;
- whether converses, equal-angles-in-the-same-segment results, or the semicircle/right-angle
  corollary belong to the root.

These are scope questions, not a canonical statement.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Geometry.Euclidean.Angle.Sphere` contains:

```text
Sphere.oangle_center_eq_two_zsmul_oangle
  (hp1 : p1 in s) (hp2 : p2 in s) (hp3 : p3 in s)
  (hp2p1 : p2 != p1) (hp2p3 : p2 != p3) :
  oangle p1 s.center p3 = (2 : Int) • oangle p1 p2 p3
```

Its context is a two-dimensional oriented real inner-product affine torsor. Its conclusion is an
equality in `Real.Angle`, hence oriented modulo `2 * pi`; it avoids selecting a minor or reflex
representative. Lower-level vector forms in namespace `Orientation` use equal norms or an explicit
radius. This is a strong exact-topic candidate and supports provisional M3, but no source-selected
canonical target, exact expression fingerprint, wrapper, transport, provenance audit, or accepted
receipt exists.

The same file defines `Sphere.angle_eq_pi_div_two_iff_mem_sphere_of_isDiameter` and aliases the
is-diameter version as `Sphere.thales_theorem`. That result says an angle inscribed in a semicircle
is right. It is a corollary or separate traditional meaning of "Thales' theorem," not the general
inscribed-angle claim given by this catalogue.

## Required statement decisions

1. Admit and independently review an immutable source edition and pinpoint proposition, including
   its definitions, diagram/case conventions, proof boundary, corrections, and errata.
2. Resolve the repository's Thales attribution against the Euclid III.20 source family and the
   separate semicircle theorem commonly bearing Thales' name.
3. Freeze the circle, center, points, selected chord/arc, angle convention, orientation, ordered
   binders, distinctness conditions, conclusion direction, and all boundary cases.
4. Decide whether the pinned oriented declaration is the canonical target, a checked alternate
   encoding, or only a formal anchor.
5. Elaborate the selected expression with minimal imports and mutation-test removed hypotheses,
   changed domains, binder scope, and degenerate boundaries before proof credit is inspected.

## Explicit exclusions

- The semicircle/right-angle result substituted solely because mathlib aliases it as
  `thales_theorem`.
- A theorem about equal inscribed angles, cyclic quadrilaterals, tangents, the sine rule, or
  converse concyclicity used as the root.
- An unoriented minor-angle equality silently identified with the oriented modulo-`2 * pi`
  candidate, or the reverse.
- A two-dimensional special case used for a source that is explicitly more general, or a
  higher-dimensional strengthening used without a source transport.
- A statement that assumes the desired angle equality, chord/arc correspondence, or cyclicity as
  structure data.
- The untrusted `已验证` label, a theorem-name match, source URL, or intake probe used as proof
  credit.

No canonical Lean expression, ordered binders, hypotheses, checked alternate encoding, or
degenerate-case exclusion is frozen by this intake.
