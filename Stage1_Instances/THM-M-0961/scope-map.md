# Scope map

## Preserved theorem family

The intake preserves the 1995 Meshulam upper-bound family named by the catalog. Bibliographic
evidence points to subsets of finite abelian groups with no nontrivial three-term arithmetic
progression. Liu-Spencer-Zhao (2011) reports the primary Theorem 1.2 invariantly as
`D3(G) <= 2 * |G| / c(G)` for finite odd-order abelian `G`: in an invariant-factor decomposition
`G ~= Z/k1 Z + ... + Z/kM Z` with nontrivial factors and `k_i` dividing `k_(i-1)`, `c(G) = M`.
Thus `G = (Z/3Z)^N` gives the familiar cap-set bound `2 * 3^N / N` for positive `N`. This is a
high-confidence provisional human target, not the intake's frozen canonical proposition: the
primary theorem text and its definitions have not been directly and independently accepted.

The title of the 1995 paper is broader than the catalog's cap-set gloss. The statement phase must
use the actual source to decide whether the root is the paper's general finite-abelian-group
theorem, its elementary-abelian specialization, or a checked source consequence. It may not silently
replace the target with a familiar modern formulation.

## Proposition-changing decisions

An exact, independently reviewed source statement must settle all of the following:

1. The ambient group: arbitrary finite abelian group, an odd-order or bounded-exponent class,
   `F_p^N`, or specifically `F_3^N`.
2. The parameters used to measure the group, such as cardinality, rank, exponent, smallest prime
   divisor, or vector-space dimension, and every hypothesis relating them.
3. Whether a cap set means no three distinct collinear points in `F_3^N`, no nonconstant affine
   line, or no nontrivial ordered solution of `a + c = 2 * b`.
4. The exact distinctness convention. In characteristic three, the equation `a + b + c = 0` and
   the usual three-term-progression equation need a checked transport and treatment of repeated
   elements.
5. Whether the conclusion is a concrete inequality, an asymptotic big-O statement, a density
   threshold, or a theorem quantified over a universal constant and a lower-dimensional cutoff.
6. The constant, logarithm base if any, denominator, rounding/coercion conventions, strict versus
   weak inequality, and all small-parameter exceptions.
7. The ordered binders, universes, finite/fintype representations, set versus finset encoding,
   cardinality operation, and typeclass hypotheses.
8. Whether translation between a general finite-group theorem and the `F_3^N` cap-set statement is
   part of the root or a separately checked implication.

Every alternate encoding needs a kernel-checked transport before it can receive statement or proof
credit.

The leading statement candidate is the reported primary Theorem 1.2 bound above, stated either
invariantly using `c(G)` or over source-faithful invariant-factor data. The `F_3^N` catalog reading is
a prospective checked specialization, not silently identical to the broader root. A Lean encoding
may avoid natural-number division via `c(G) * D3(G) <= 2 * |G|`, but only after checking that this is
equivalent to the source's intended rational inequality under `c(G) > 0`.

## Boundary cases

- Dimension `N = 0` and the one-element group; the reported invariant-factor theorem has at least
  one nontrivial constituent and does not directly cover the empty decomposition or `c(G) = 0`.
- Small dimensions for which a denominator `N` vanishes or an asymptotic threshold does not apply.
- The empty set, singleton sets, the whole group, and sets of size two.
- Constant triples, exactly two equal terms, and three distinct terms.
- Groups with even order or 2-torsion, where division by two and progression conventions differ.
- Exponent-three groups not presented as `Fin N -> ZMod 3`, and `F_3^N` presented with different
  finite-field or module encodings.
- Real, rational, and natural-number forms of a cardinality bound, including floors and ceilings.

No boundary case is excluded at intake because the exact source proposition is not yet frozen.

## Explicit exclusions

- Ellenberg-Gijswijt's later exponential cap-set bound (`THM-M-0960`) or the Croot-Lev-Pach method.
- Bateman-Katz's improvement from order `1 / N` to order `1 / N^(1 + epsilon)`.
- Roth's theorem for dense subsets of integer intervals (`THM-M-0947`).
- The qualitative statement that fixed positive density eventually forces a 3AP, unless the exact
  source-to-quantitative implication is checked in the required direction.
- A theorem only for natural numbers, cyclic groups, or one fixed dimension.
- A cap-set construction or lower bound, including Behrend/Elkin-style results.
- A premise or structure that stores the desired upper bound or progression witness.
- The catalog's untrusted verified label, a related theorem name, or the intake API probe used as
  proof evidence.

## Neighbor boundaries

`THM-M-0959` owns the Croot-Lev-Pach method, `THM-M-0960` owns the Ellenberg-Gijswijt theorem, and
`THM-M-0947` owns Roth's integer theorem. Those targets may share definitions or proof ideas, but
none can supply completion credit to this target without an exact checked bridge.

No canonical Lean target, expression fingerprint, alternate encoding, discovery protocol,
obligation registry, or proof state is frozen by this intake.
