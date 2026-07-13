# Scope map

## Preserved theorem family

`THM-M-0931` is the integer Erdős-Ginzburg-Ziv theorem: for a positive integer `n`, among exactly
`2 * n - 1` integer occurrences one can choose exactly `n` occurrences whose sum is divisible by
`n`. The input and witness must preserve repeated occurrences. The catalog's importance and
`已验证` fields are metadata, not source or kernel evidence.

The 1961 paper says "set" and "subset", but its proof writes the input as indexed integers and
repeatedly removes selected index blocks. A duplicate-free `Finset ℤ` would therefore change the
claim. A finite sequence, indexed family, or `Multiset ℤ` is the appropriate encoding family.

## Decisions required before statement freeze

1. Admit an immutable edition or scan and independently review the exact theorem, complete proof,
   citation pagination, translation, corrections, and errata.
2. Freeze `n` as positive. The source proof handles primes and composites and does not state `n = 0`;
   mathlib's total natural extension at zero is not silently source-identical.
3. Select the occurrence container: a length-indexed function, list, or multiset, with checked
   transports for every credited alternate.
4. Freeze exact input cardinality `2 * n - 1`. Mathlib's public theorem uses a lower bound and is a
   strengthening; equality-to-inequality specialization must be checked.
5. Freeze the witness as exactly `n` occurrences selected from the input, not `n` distinct values,
   an arbitrary nonempty zero-sum subcollection, or a consecutive subsequence.
6. Freeze the conclusion `(n : ℤ) ∣ sum` and any checked relationship to zero sum in `ZMod n`.
7. Resolve `n = 1`, repeated values, negative integers, all-equal inputs, and natural subtraction at
   `n = 0`; mutation-test positivity, domain, binder order, cardinalities, and divisibility.
8. Select foundation, accepted axiom, TCB, computation, freshness, and review profiles after the
   canonical expression and minimal imports are fixed.

## Candidate formulations not credited

1. The source-oriented exact-count multiset form with hypothesis `0 < n`.
2. Mathlib's stronger at-least-count integer multiset theorem, including its `n = 0` extension.
3. The equivalent residue-class multiset form in `ZMod n`, after a checked cast/divisibility bridge.
4. The indexed Finset form, where distinct indices preserve duplicate integer values.
5. The paper's finite-abelian-group extension, stated after the integer theorem.

These are related candidates, not interchangeable roots at intake.

## Explicit exclusions

- The finite-abelian-group generalization or any nonabelian-group conjecture substituted for the
  integer theorem. The paper explicitly says the nonabelian case was unknown.
- `THM-M-0932` (the broad zero-sum-sequence topic), `THM-M-0933` (Olson's theorem),
  `THM-M-0936` (Cauchy-Davenport), or `THM-M-0930` (Combinatorial Nullstellensatz).
- A duplicate-free set of integer values, a consecutive subsequence, a reordered list without an
  occurrence map, or an input whose values are assumed distinct.
- A weaker result choosing at most `n`, at least `n`, or merely a nonempty number of elements.
- Equality of the integer sum to zero substituted for divisibility by `n`.
- The sharp lower-bound example, the finite-group extension, or a prime-only theorem substituted
  for the composite integer root.
- The catalog label, a theorem name, an elaborated candidate, or mathlib documentation treated as
  accepted source fidelity or theorem completion.

## Provisional statement resolution

`Statement.lean` resolves the statement-node choices provisionally as follows: `n : Nat` with
`0 < n`; exactly `2 * n - 1` occurrences in `Multiset Int`; an existential `t <= s` with exactly
`n` occurrences; and `(n : Int) ∣ t.sum`. Repeated, negative, zero, and all-equal values remain in
scope. `n = 0` is excluded, while `n = 1` is included.

The exact-count root is distinct from the pinned at-least-count proposition shape, whose checked
direction is implication to the root. The residue alternate keeps the integer multiset and checks
only the equivalence between divisibility and the cast sum being zero in `ZMod n`. Finsets,
consecutive list subsequences, ZMod-valued input roots, and weaker witness-size claims remain
excluded. This resolution remains worker evidence pending independent source and master review;
no obligation registry, discovery protocol, graph, or proof state is frozen here.
