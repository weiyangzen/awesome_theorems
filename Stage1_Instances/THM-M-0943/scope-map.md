# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0943`, the name Plunnecke-Ruzsa inequality, the combined
Plunnecke/Ruzsa attribution, the year 1970, and the slogan "growth of sumsets." This identifies the
classical additive-combinatorics family relating small first sumsets to higher sum-and-difference
sets. It does not fix one truth-valued claim.

A close standard formulation says that for finite sets `A` and `B` in an additive commutative
group, with `A` nonempty, the cardinality of `mB - nB` is bounded by
`(|A + B| / |A|)^(m+n) * |A|`. Pinned mathlib implements this ratio form. It is a candidate scope
locator, not the canonical target at intake.

## Proposition-changing decisions

The source-reviewed statement phase must freeze all of the following:

1. Whether the ambient domain is an arbitrary additive commutative group, a finite abelian group,
   or the integers, and the exact universe and decidable-equality context.
2. Whether `A` and `B` are finsets, finite sets, or another encoding, and which of them must be
   nonempty.
3. Whether the hypothesis is expressed through the exact ratio `|A+B| / |A|`, through a parameter
   `K` satisfying `|A+B| <= K|A|`, or through a minimizing subset.
4. Whether the conclusion is the two-index sum-and-difference bound `|mB-nB|`, the one-index higher
   sumset bound `|nB|`, Plunnecke's subset-growth theorem, or a checked package of these results.
5. Whether the base is `A+B` or `A-B`, and whether subtraction means pointwise group subtraction
   rather than set difference.
6. The cardinality codomain and coercions, including `Nat`, rational numbers, nonnegative rationals,
   nonnegative reals, or a parameterized inequality without division.
7. The ordered quantifiers over `G`, `A`, `B`, a growth parameter, and `m,n`, plus the exact exponent
   convention.
8. Whether `m+n>1` is required as in one source formulation or all natural indices are included as
   in the pinned mathlib theorem, with the low-index cases proved internally.

Each choice changes the proposition or its proof boundary. Any credited alternative needs a
source-approved and kernel-checked transport.

## Boundary cases

- `A = empty`, where the ratio denominator vanishes and the pinned candidate instead assumes
  `A.Nonempty`.
- `B = empty` and singleton or subgroup inputs.
- `m = 0`, `n = 0`, and `m+n` equal to zero or one.
- Trivial and finite ambient groups, torsion groups, and the integers.
- Pointwise zero-fold sumsets, inverses, subtraction, and their notation conventions.
- A ratio exactly zero or one, and equality/sharpness cases.
- The difference between an existentially chosen subset `X` and a conclusion retaining the
  original set `A`.

No case is excluded at intake because no canonical proposition has been selected.

## Explicit exclusions

- Ruzsa's triangle inequality alone and `THM-M-0942` Ruzsa covering lemma.
- Plunnecke's subset-growth theorem alone when the selected root is the Ruzsa sum-difference
  extension, or conversely the extension silently replacing an original-growth claim.
- The Plunnecke-Petridis minimization lemma without the final higher-sumset conclusion.
- A noncommutative small-tripling theorem, where small doubling does not imply the same result.
- Freiman's structure theorem, Kneser's theorem, the Balog-Szemeredi-Gowers theorem, or any inverse
  theorem for small doubling.
- A special case only for `A = B`, only `nB`, fixed indices, integers, finite cyclic groups, or a
  stored hypothesis containing the desired bound.
- The catalog's untrusted verified label, the matching mathlib filename, or the API probe used as
  proof credit for an unidentified root.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen during intake.
