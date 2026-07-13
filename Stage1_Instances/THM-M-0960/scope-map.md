# Scope map

## Preserved catalog scope

The intake preserves the Ellenberg-Gijswijt cap-set upper-bound family named by the catalog. In the
published source, the cap-set problem concerns subsets of `(Z/3Z)^n` with no nontrivial three-term
arithmetic progression, and the paper proves an exponentially smaller upper bound than `3^n`.
This family description is not yet a canonical statement or Lean target.

## Candidate roots, not credited

The inspected publisher version presents at least three materially different candidate surfaces:

1. Theorem 4: for a finite field `F_q`, nonzero coefficients `alpha`, `beta`, `gamma` summing to
   zero, and `A subset F_q^n` with only diagonal solutions to the corresponding three-variable
   equation, `|A| <= 3 m_((q-1)n/3)`, where `m_d` counts bounded-exponent monomials.
2. Corollary 5: if `A subset (Z/3Z)^n` contains no three-term arithmetic progression, then
   `|A| = o(2.756^n)`.
3. The qualitative consequence that, for fixed odd prime `p`, the maximal progression-free subset
   of `(Z/pZ)^n` grows like at most `c^n` for some `c < p`.

The catalog's four-word gloss selects none of these. The intake does not choose among them.

## Proposition-changing decisions

Before statement elaboration, an admitted source and accountable review must freeze:

- whether the exact root is published Theorem 4, Corollary 5, or a checked consequence;
- `F_q` for prime powers versus `(Z/pZ)`, and whether `q` or `p` is fixed or quantified;
- whether `n` is positive or any natural number, and the interpretation of the zero-dimensional
  space;
- whether `A` is a `Set`, `Finset`, or subtype, together with finiteness and coercion conventions;
- whether "cap set" means `ThreeAPFree`, only diagonal solutions of `a + b + c = 0`, or pairwise
  distinct triples, including the role of characteristic three;
- for Theorem 4, the coefficient hypotheses, the "not all zero" clause, binder order, and the exact
  definition of `m_d` when the real cutoff `(q - 1)n/3` is nonintegral;
- for Corollary 5, the formal meaning of little-`o`, the base `2.756`, strictness, coercions to real
  numbers, and whether a finite explicit bound is intended instead;
- all rounding, empty-set, singleton, small-dimension, and degenerate-coefficient cases;
- exact minimal imports, foundation/choice policy, environment fingerprint, checked transports,
  and required statement mutations.

## Degenerate and boundary cases

Source review must explicitly resolve `n = 0`; the empty and singleton subsets; the entire ambient
space in small dimensions; repeated elements versus distinct elements in a progression; zero or
repeated coefficients; the difference between `F_3`, `ZMod 3`, and an arbitrary field of order
three; nonintegral monomial degree cutoffs; and the finite-prefix meaning of an asymptotic claim.
No case is excluded at intake because no canonical proposition has been selected.

## Excluded substitutions

- Mathlib's `roth_3ap_theorem` is a qualitative density result based on the corners theorem. It is
  not the Ellenberg-Gijswijt exponential bound and cannot replace the root.
- Meshulam's older `O(3^n/n)` bound, the Croot-Lev-Pach `Z/4Z` result, and lower-bound
  constructions are distinct targets or ingredients.
- A bound only for a fixed dimension, a checked numerical enumeration, or a precomputed table does
  not establish the universal or asymptotic theorem.
- A predicate or structure that assumes the desired upper bound, a theorem name, `#check`, a URL,
  or the catalog's untrusted `已验证` label supplies no proof credit.
- Theorem 4, Corollary 5, and a qualitative `exists c < q` consequence are not interchangeable
  without checked implications and a source-approved root decision.

## Neighbor boundaries

`THM-M-0959` owns the Croot-Lev-Pach method, `THM-M-0961` the Meshulam theorem, and
`THM-M-0947` a Roth theorem. Their statements, sources, and proof evidence remain independently
owned. They may later become explicit dependencies but grant no status to this target by proximity.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks
`ZMod.card`, `Fintype.card_fun`, `ThreeAPFree`, a prospective `(Fin n -> ZMod 3)` ambient space,
and finite-set cardinality. A bounded exact-topic search found no target declaration. These are
encoding ingredients and scoped discovery evidence only; the canonical expression, transports,
mutation tests, proof body, obligation registry, and discovery protocol remain open.
