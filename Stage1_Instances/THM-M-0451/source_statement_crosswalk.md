# Source-statement crosswalk

| Claim component | Human source anchor | Lean target needed | Intake assessment |
|---|---|---|---|
| Canonical height limit and bounded comparison | J. H. Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed., Springer GTM 106 (2009), Chapter VIII, section 9, Theorem 9.3(a,b) | A number-field elliptic-curve point type, absolute `x`-height, convergence, and a real-valued `hat_h` | Primary theorem family located; exact scanned-page/hash and convention audit remain open |
| Quadraticity and parallelogram law | Silverman, same edition, Chapter VIII, Theorem 9.3(c,d) | Integer scalar multiplication and point addition/subtraction laws for `hat_h` | The source theorem uses a normalization that must match the formal definition |
| Nonnegativity and torsion kernel | Silverman, same edition, Chapter VIII, Theorem 9.3(e) | Ordered-real result and the formal torsion predicate on `E(K)` | Depends essentially on the number-field setting; no domain broadening is allowed |
| Bilinear Neron-Tate pairing | Silverman, same chapter, immediately following the canonical-height theorem via polarization | A derived symmetric bilinear pairing on the Mordell-Weil group modulo torsion | Corollary candidate only; not substituted for the root package |

Discovery link (not an immutable evidence receipt):

- Springer edition record: <https://doi.org/10.1007/978-0-387-09494-6>

The blueprint's short phrase, "height of points on elliptic curves," could also denote a height
machine, local heights, or only quadraticity. The intake therefore selects the standard canonical
height existence-and-properties package rather than silently claiming one convenient fragment. The
statement phase must verify the theorem numbering and normalization against a fixed source copy,
freeze the identity-point convention, inspect actual Lean types, and mutation-test omission of the
number-field hypothesis, the factor `1/2`, the torsion equivalence, and the integer scalar binder.

Repository-local searches for `Neron`, `canonicalHeight`, `canonical_height`, and elliptic-curve
height combinations produced no relevant mathlib declaration in this clone. This is only negative
discovery evidence, not a complete upstream anchor audit. No H0 or machine-closure claim is made.
