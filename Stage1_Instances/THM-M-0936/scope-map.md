# THM-M-0936 scope map

## Included theorem family

The intake recognizes the conventional Cauchy-Davenport family. Its standard prime-cyclic form
uses a prime `p`, two nonempty finite subsets `A, B` of the additive group `Z/pZ`, their pointwise
sumset `A + B = {a + b | a in A, b in B}`, and the lower bound

```text
|A + B| >= min(p, |A| + |B| - 1).
```

This is a candidate interpretation, not yet the canonical proposition. The repository's literal
finite-field gloss omits all of these binders and conditions.

## Decisions required at statement freeze

1. Admit and independently review an immutable source statement, including its definitions,
   proof boundary, historical attribution, and errata status.
2. Decide whether the root is the classical prime cyclic group `Z/pZ`, the prime field `F_p`, an
   arbitrary finite field with characteristic cap, or a group theorem using minimal element order.
3. Fix whether `p` is an explicit prime natural, whether `p = 2` is included, and what happens at
   impossible or degenerate moduli such as `0` and `1`.
4. Fix two subsets versus one repeated subset, and confirm that the Chinese term `子集和` means the
   two-set pointwise sumset rather than sums of elements selected from one set.
5. Fix the `Finset`, finite `Set`, or cardinal formulation and provide checked transports for every
   credited alternate encoding.
6. Make nonemptiness of both inputs explicit, or state a boundary convention that makes empty-set
   cases true without weakening the intended theorem.
7. Fix the exact inequality orientation, the cap `min p`, natural-number cardinalities, and the
   truncated subtraction in `|A| + |B| - 1`.
8. Freeze universes, notation scopes, typeclass assumptions, minimal imports, foundation/TCB/
   computation profiles, and every excluded boundary case.

## Finite-field boundary

For a finite field `F` of characteristic `p`, its additive group has nontrivial elements of order
`p`, so a group-level Cauchy-Davenport generalization naturally caps the lower bound at `p`, not at
`|F|` when `F` is a proper extension of `F_p`. The naive statement

```text
min(|F|, |A| + |B| - 1) <= |A + B|
```

is false in general: take a nontrivial proper additive subgroup `H` of `F` and set `A = B = H`.
Then `A + B = H`, while the proposed right-hand growth can exceed `|H|`. This counterexample is a
scope guard, not a replacement theorem or a formalized result in this intake.

## Other boundary cases

- Singleton inputs are included in the conventional formula and give the expected translation
  bound; they must not be excluded merely to simplify a proof.
- When `|A| + |B| - 1 >= p`, the conventional conclusion is saturation at least `p`, hence equality
  with all of `Z/pZ`; an uncapped inequality would be false.
- Nonemptiness matters: the empty sumset has cardinality zero while natural truncated subtraction
  can hide the intended mathematical premise.
- `Finset` pointwise addition deduplicates repeated sums; multiset or ordered-pair counts are not the
  same statement.

## Explicit exclusions

- The torsion-free, linearly ordered semigroup, arbitrary-group, or locally compact group
  generalizations as substitutes for the source-selected classical theorem.
- The Erdős-Heilbronn/Dias da Silva-Hamidoune restricted sumset theorem, where equal summands are
  excluded.
- Vosper's inverse theorem, Kneser's structural theorem, Kemperman's theorem, or a classification
  of equality cases.
- A single-set doubling statement, a subset-sum counting result, or an iterated `hA` theorem unless
  the accepted source explicitly selects it.
- A weakened consequence such as `max(|A|, |B|) <= |A + B|` or a bound that assumes the desired
  conclusion.
- A finite computation, exhaustive enumeration for selected primes, theorem name, untrusted
  `已验证` label, or discovery probe used as proof evidence.

## Neighbor and ownership boundary

`THM-M-0934` is the Erdős-Heilbronn conjecture, `THM-M-0935` its Dias da Silva-Hamidoune theorem,
`THM-M-0937` Vosper's inverse theorem, and `THM-M-0938` Kneser's theorem. Their statements,
evidence, and owned paths are not modified or credited here. This intake owns only
`Stage1_Instances/THM-M-0936`.
