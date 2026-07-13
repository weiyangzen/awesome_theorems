# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0923`, the title `贝尔数`, the attribution Eric Bell, the year
1934, and the gloss `集合划分的计数`. This intake preserves the conventional Bell-number and finite
set-partition subject. Importance `高` and status `已验证` are catalog metadata, not human-source or
kernel evidence.

The gloss is a noun phrase rather than an equality or quantified assertion. It does not say whether
the desired root is a definition, a cardinality theorem connecting an independently defined
sequence to partitions, a recurrence, a closed formula, a generating function, or a relation to
Stirling numbers.

## Candidate formulations not credited

1. Define `B(n)` to be the cardinality of the partitions of an `n`-element labeled set.
2. Prove that an independently or recursively defined `B(n)` equals that cardinality.
3. Prove `B(n) = sum_{k=0}^n S(n,k)`, where `S(n,k)` counts partitions into exactly `k`
   nonempty blocks.
4. Prove the recurrence `B(n+1) = sum_{k=0}^n choose(n,k) * B(k)` with `B(0) = 1`.
5. Prove the exponential generating function or Dobinski formula under an exact analytic domain
   and convergence interpretation.
6. Count partitions with a fixed multiset of block sizes or equal block sizes rather than all set
   partitions.

These statements are related, but they are not interchangeable. A recursive definition makes its
unfolding recurrence immediate while leaving the cardinality interpretation open. Conversely, a
cardinality definition makes the counting slogan definitional but does not automatically supply
the source-selected recurrence, generating function, or analytic formula.

## Decisions required before statement freeze

The dependent statement phase must independently approve and freeze:

1. An immutable source edition and exact definition/theorem/equation/section/page locator, including
   whether the catalog intends a definition, a theorem, or a bundle.
2. The Bell sequence definition and codomain, and whether the finite-set cardinality equality is
   definitional or a theorem relating two encodings.
3. The carrier representation: `Fin n`, an arbitrary finite type of cardinality `n`, a concrete
   set `{1, ..., n}`, or a checked transport among them.
4. The partition representation: equivalence relations, setoids, finite partitions, or collections
   of pairwise-disjoint nonempty blocks covering the carrier.
5. Whether partitions are labeled only through their carrier, whether block order is ignored, and
   which quotient/extensional equality identifies partitions.
6. Ordered binders, all hypotheses, exact conclusion, summation ranges, arithmetic codomains, and
   every credited alternate encoding.
7. The relationship to Stirling numbers of the second kind and whether their own counting
   interpretation is assumed, proved, or separately owed.
8. Foundation, TCB, computation, freshness, source-review, and correction/errata policies for the
   chosen root.

## Degenerate and boundary cases

No case is excluded at intake. Statement review must explicitly disposition:

- `n = 0`, including the single empty partition and the convention `B(0) = 1`;
- empty blocks, repeated blocks, ordered blocks, and blocks outside the carrier;
- exactly zero blocks for an empty or nonempty carrier and exactly `k > n` blocks;
- arbitrary finite carriers versus the canonical carrier `Fin n`, including invariance under
  equivalence;
- summation endpoints and zero-extension conventions for Stirling numbers;
- recurrence index changes between `B(n-k)` and `B(k)` forms;
- natural-number equality versus casts into integers, rationals, reals, formal power series, or
  analytic functions; and
- convergence, factorial, exponential, and infinite-sum conventions if an analytic formula is
  selected.

## Neighbor and substitution boundaries

- `THM-M-0922` (Stirling numbers) is a distinct target. Its second-kind sequence may refine Bell
  numbers by block count, but it supplies no inherited statement or proof credit.
- `THM-M-0921` (Catalan numbers) and `THM-M-0925` (Fibonacci numbers) are separate enumerative
  sequences and cannot select this target's root.
- Integer partitions, multiset partitions, permutations into cycles, and partitions with prescribed
  block sizes are not unrestricted set partitions unless an exact checked reduction is part of the
  selected claim.
- A recurrence obtained by unfolding `Nat.bell`, the values `B(0)`, `B(1)`, and `B(2)`, a finite
  table, or a structure field that assumes the result cannot substitute for a source-selected
  set-partition cardinality theorem.
- DLMF prose, a mathlib docstring, a TODO, the catalog's `已验证` value, and this intake probe are not
  proof receipts.

Statement ambiguity blocks obligation-tree construction. No canonical expression fingerprint,
discovery-protocol hash, obligation-registry hash, typed graph, or closure state is frozen here.
