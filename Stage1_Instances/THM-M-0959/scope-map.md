# Scope map

## Preserved repository scope

The repository fixes `THM-M-0959`, the label `Croot-Lev-Pach方法`, the attribution
Croot/Lev/Pach, the year 2017, and the gloss "application of the polynomial method to the cap-set
problem." This identifies the 2017 Croot-Lev-Pach paper and its proof method, but it does not select
one binder-complete proposition.

The primary paper contains several materially different candidates. None is canonical at intake.

1. **Theorem 1:** for `n >= 1`, every progression-free `A` in `Z_4^n` satisfies
   `|A| <= 4^(gamma*n)`, where, for base-two binary entropy `H`,
   `gamma = max { (H(1/2 - epsilon) + H(2*epsilon))/2 | 0 < epsilon < 1/4 }`, approximately
   `0.926`.
2. **Corollary 1:** for a finite abelian group `G`, a progression-free `A` is bounded in terms of
   the number of invariant factors divisible by four.
3. **Lemma 1:** a bounded-degree multilinear polynomial whose off-diagonal evaluations vanish on a
   sufficiently large finite set must also vanish at zero.
4. **Proposition 1:** only exponentially few cosets of the involution subgroup can contain many
   points of a progression-free subset of `Z_4^n`.
5. **A provenance-sensitive method package:** the polynomial lemma, dimension argument, entropy
   estimate, coset decomposition, integral estimate, and tensor-power trick, with checked
   composition to a selected root.

The phrase "cap-set problem" does not authorize replacing these candidates with the distinct
Ellenberg-Gijswijt theorem over `F_3^n` or `F_q^n`.

## Proposition-changing decisions

Before statement elaboration, accountable source and scope review must freeze all of the following:

1. Select Theorem 1, Corollary 1, Lemma 1, Proposition 1, an exact conjunction, or a
   provenance-sensitive method package as the truth-valued root.
2. If Theorem 1 is selected, fix `Z_4^n` as `Fin n -> ZMod 4` or another checked-equivalent group,
   and preserve the paper's pairwise-distinct progression predicate. It is not equivalent to
   mathlib's stronger `ThreeAPFree` in exponent four: `{0, 2}` in `ZMod 4` is CLP-progression-free
   because it has only two points, but fails `ThreeAPFree` because `0 + 0 = 2 + 2`. Any credited
   transport must therefore state and prove its actual direction rather than assert equivalence.
3. Fix the real-valued constant `gamma`, the base-two normalization of entropy, whether the
   displayed decimal is commentary only, and how real exponentiation and natural cardinality are
   compared.
4. Resolve whether the paper's printed `max` over the open interval `0 < epsilon < 1/4` is encoded
   literally, as a supremum, or through a separately proved attained-value reformulation.
5. If Corollary 1 is selected, fix the invariant-factor decomposition, `rk_4`, subgroup/coset
   transport, and whether the theorem bounds each set or the extremal number `r_3(G)`.
6. If Lemma 1 is selected, fix the field, finite coordinate type, polynomial representation,
   multilinearity, total degree, binomial sum and floor convention, subtraction, and the exact
   off-diagonal predicate.
7. If the method/provenance package is selected, freeze which proof transitions are target
   requirements rather than merely one possible proof, and give every material step a typed node
   and checked composition edge.
8. Freeze minimal imports, universes, ordered binders, hypotheses, conclusion, alternate
   encodings, foundation/TCB/computation profiles, and all required statement mutations only after
   the root is selected.

## Boundary cases

No case is excluded at intake. Statement work must resolve `n = 0` versus the paper's `n >= 1`;
empty, singleton, and full subsets; repeated versus pairwise-distinct progression terms; constant
progressions; `ZMod 4` versus a product of cyclic groups; empty products; real powers and rounding;
the entropy endpoints `0` and `1/4`; existence of the stated maximum; zero-degree and zero-variable
polynomials; empty fields (impossible under `Field` but relevant to binder design); equality at the
cardinality threshold; and tensor powers of zero or one factor.

## Explicit exclusions

- `THM-M-0960` Ellenberg-Gijswijt or any `F_3^n`/`F_q^n` cap-set bound substituted for the CLP
  `Z_4^n` paper.
- `THM-M-0957` Behrend or `THM-M-0958` Elkin lower-bound constructions.
- `THM-M-0961` Meshulam's earlier finite-abelian-group upper bound.
- A generic slice-rank, polynomial-method, combinatorial Nullstellensatz, or matrix-rank theorem
  without a checked source-selected bridge to the root.
- Mathlib's Behrend lower bound, Roth theorem, `ThreeAPFree` predicate, or binary-entropy library
  treated as the CLP upper bound.
- The CLP polynomial lemma alone presented as Theorem 1, or Theorem 1 presented as proof that a
  particular proof method/provenance package was formalized.
- A hypothesis, structure, certificate, or precomputed bound that stores the desired conclusion.
- Numerical optimization of `gamma`, floating-point estimates, finite experiments, URLs, source
  titles, or the catalog's `已验证` label used as human or kernel proof evidence.

## Formal boundary

Pinned mathlib defines `ThreeAPFree`, `Fintype.card_pi_const`, `ZMod`, and `Real.binEntropy`.
`Mathlib.Combinatorics.Additive.AP.Three.Behrend` proves a lower-bound construction over natural
numbers, not the CLP exponential upper bound over `Z_4^n`. A bounded exact-topic search found no
CLP-named or source-identical theorem. These are discovery facts only, not a complete anchor audit
or a global absence claim.

No canonical Lean expression, expression fingerprint, checked transport, discovery protocol,
obligation registry, proof state, or completion claim is frozen during intake.
