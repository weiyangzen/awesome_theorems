# Scope map

## Preserved theorem family

The repository fixes the eponym, authors, year, and subject "maximum size of an intersecting
family." The intended statement must remain within the classical finite-set Erdős-Ko-Rado family.
Intake does not silently choose among these materially different claims:

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

## Decisions required at statement freeze

1. Admit one primary edition and select the exact theorem, remark, or accepted modern formulation.
2. Decide whether the root requests only an upper bound, the maximum with an attainment witness,
   or an equality characterization. A source or docstring saying "sharp" does not add a conclusion
   absent from the Lean declaration.
3. Freeze the ground set as an abstract finite type or `Fin n`, and freeze whether the family is a
   finite set, finite family with no duplicates, or ordinary set with finiteness evidence.
4. Select the original antichain plus `card <= l` premises or the uniform `card = r` premise, and
   supply a checked bridge, including automatic incomparability at fixed cardinality, if both are
   credited.
5. Fix intersecting semantics. Mathlib's `Set.Intersecting` quantifies a member against itself, so a
   family containing the empty set is not intersecting; a distinct-pairs-only definition treats a
   singleton empty-set family differently.
6. Fix `r <= n / 2` versus `2 * r <= n`, natural-number subtraction, binomial conventions, and all
   coercions before comparing statements.
7. Resolve `r = 0`, `r = 1`, `n = 0`, `n = 1`, empty family, singleton family, and the exact
   `n = 2 * r` boundary. Pinned mathlib explicitly handles `r = 0` by forcing the family empty.
   The printed source quantifies intersection only over distinct indices, so a singleton family
   containing the empty set exposes a possible implicit convention or degenerate exception in its
   strict-if-smaller clause; do not claim literal total equivalence before source review.
8. If equality is included, state whether stars are merely witnesses or the unique extremizers,
   and state all exceptions.
9. Freeze foundation, TCB, computation, freshness, statement mutation, and alternate-encoding
   profiles after the exact root is chosen.

## Explicit exclusions

- `THM-M-0821` Sperner's antichain theorem and `THM-M-0966` Kruskal-Katona; the latter is used by
  mathlib's proof but is not the EKR root.
- `THM-M-0964` Hilton-Milner, which concerns the maximum size of a nontrivial intersecting family.
- `THM-M-0962` Frankl-Wilson and `THM-M-0963` Ray-Chaudhuri-Wilson intersection bounds.
- `THM-M-0965` Ahlswede-Khachatrian complete `t`-intersection theorem.
- EKR analogues for permutations, multisets, vector spaces, designs, matchings, independent sets,
  groups, or simplicial complexes.
- A weakened asymptotic bound, a fixed numerical example, an assumed star construction, or a
  convenient equality theorem substituted for the unselected catalog claim.
- The catalog's `已验证` label, a theorem name, docstring, `#check`, or axiom report treated as
  human-source, statement-identity, proof, or completion evidence.

No canonical expression, statement fingerprint, checked transport, obligation registry, discovery
protocol, accepted proof state, or completion claim is frozen at intake.
