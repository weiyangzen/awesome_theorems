# Scope map

## Preserved theorem family

The repository fixes the eponym, authors, year, and subject "maximum size of an intersecting
family." The statement phase selects the standard positive uniform maximum-value form within the
classical finite-set Erdős-Ko-Rado family. The following nearby claims remain materially different:

1. **Original at-most-size antichain bound.** If subsets of an `m`-element ground set are pairwise
   incomparable, have size at most `l`, every pair intersects, and `1 <= l <= m / 2`, then the
   family has at most `choose (m - 1) (l - 1)` members. Distinct equal-size members are
   automatically incomparable, so the premise disappears in the uniform specialization.
2. **Uniform upper bound.** If every member has exactly `r` elements, the family is pairwise
   intersecting, and `2 * r <= n`, then its cardinality is at most
   `choose (n - 1) (r - 1)`. Pinned `Finset.erdos_ko_rado` has this shape.
3. **Sharp maximum statement.** The upper bound is paired with a construction, normally all
   `r`-subsets containing one fixed ground element, which attains that cardinality.
4. **Equality characterization.** Every family attaining the bound is classified. Its exact scope
   depends on the strict boundary `n > 2 * r`; at `n = 2 * r`, choosing one member from each
   complementary pair yields many extremal families.
5. **General `t`-intersection and nontrivial-family variants.** These are later, stronger, or
   differently scoped results and are not selected by the eponym alone.

## Statement-freeze decisions

1. The root is the standard uniform maximum value: the universal upper bound plus an attaining
   star. It is neither the broader original at-most-size antichain theorem nor an all-extremizers
   equality classification.
2. The ground set is `Fin n`; the family is `Finset (Finset (Fin n))`, so members and the family
   contain no duplicates.
3. Uniformity is `Set.Sized r`, and `1 <= r` is explicit. The original antichain/at-most-size
   premises receive no statement or proof credit here.
4. Mathlib's `Set.Intersecting` quantifies a member against itself, so a
   family containing the empty set is not intersecting; a distinct-pairs-only definition treats a
   singleton empty-set family differently. `sized_intersecting_iff_pairwise` checks agreement with
   distinct-pair intersection for the selected positive uniform domain.
5. The range is `r <= n / 2`, including equality. Natural subtraction and `Nat.choose` use their
   Lean meanings. No positive rank is admissible at `n = 0` or `n = 1`; a star is checked at the
   `n = 2 * r` boundary. Rank zero is excluded.
6. Pinned mathlib explicitly handles `r = 0` by forcing an intersecting uniform family empty.
   The printed source quantifies intersection only over distinct indices, so a singleton family
   containing the empty set exposes a possible implicit convention or degenerate exception in its
   strict-if-smaller clause; do not claim literal total equivalence before source review.
7. Stars are attainment witnesses only. The target does not classify all extremizers.
8. `Statement.lean`, `statement.json`, and `statement-receipt.json` freeze the Lean expression,
   checked alternate forms, profiles, four mutations, and current provisional fingerprints.
   Independent source admission, corrections review, and master acceptance remain open.

## Explicit exclusions

- `THM-M-0821` Sperner's antichain theorem and `THM-M-0966` Kruskal-Katona; the latter is used by
  mathlib's proof but is not the EKR root.
- `THM-M-0964` Hilton-Milner, which concerns the maximum size of a nontrivial intersecting family.
- `THM-M-0962` Frankl-Wilson and `THM-M-0963` Ray-Chaudhuri-Wilson intersection bounds.
- `THM-M-0965` Ahlswede-Khachatrian complete `t`-intersection theorem.
- EKR analogues for permutations, multisets, vector spaces, designs, matchings, independent sets,
  groups, or simplicial complexes.
- A weakened asymptotic bound, a fixed numerical example, an assumed star construction, or a
  convenient equality theorem substituted for the selected maximum-value claim.
- The catalog's `已验证` label, a theorem name, docstring, `#check`, or axiom report treated as
  human-source, statement-identity, proof, or completion evidence.

The statement phase freezes a provisional canonical expression, fingerprint, and checked
transports. It does not freeze an obligation registry or discovery protocol, add accepted proof
state, or make an audit/theorem-completion claim.
