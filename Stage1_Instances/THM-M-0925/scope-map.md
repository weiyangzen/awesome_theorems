# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0925`, the title `斐波那契数列`, attribution to Leonardo
Fibonacci, the year 1202, and the gloss `递推序列的经典例子`. This intake preserves the Fibonacci
sequence and recurrence family identified by those fields. Importance `高` and status `已验证` are
catalog metadata, not human-source or kernel evidence.

The gloss names a mathematical object and calls it an example. It does not state a proposition.
In particular, it does not say whether the intended root is a definition, a recurrence property,
an existence-and-uniqueness theorem, or a counting theorem that constructs the sequence.

## Candidate roots not credited

1. Define the natural Fibonacci function by `F(0) = 0`, `F(1) = 1`, and
   `F(n + 2) = F(n) + F(n + 1)`.
2. Given an independently defined sequence, prove that it has those initial values and satisfies
   that recurrence.
3. Prove that exactly one natural-valued sequence has those initial values and recurrence.
4. Use the one-based convention `F(1) = F(2) = 1` and the predecessor recurrence for later terms.
5. Prove that the number of rabbit pairs in a source-specified model follows this sequence.
6. Characterize the sequence over integers, a semiring, or a general additive carrier rather than
   only over natural numbers.

These formulations are related but not identical. A recursive definition is not itself the same
claim as an existence-and-uniqueness theorem, and the historical rabbit model adds assumptions and
an indexing transport. The statement phase must select one source-backed proposition rather than
conjoin convenient facts.

## Decisions required before statement freeze

An approved target correction and source review must decide:

1. The exact truth-valued root and whether incorporated initial-value equations are premises,
   conclusions, or definitional reductions.
2. Zero-based `0, 1, 1, 2, ...` versus one-based `1, 1, 2, ...` indexing and the checked shift
   between any credited alternates.
3. The index domain (`Nat`, positive naturals, integers with negative-index extension, or another
   source-defined domain) and the value carrier (`Nat`, `Int`, or a general algebraic structure).
4. Whether one concrete sequence is named or an arbitrary function is characterized by initial
   values and recurrence.
5. Pointwise equations versus equality of functions or streams, and the exact ordered binders,
   universes, typeclasses, hypotheses, and conclusion.
6. Whether uniqueness, computability, monotonicity, a combinatorial interpretation, or any other
   property belongs to the root. None is imported merely because it is familiar.
7. The exact primary edition, theorem/problem/page locator, incorporated definitions, proof
   boundary, translation, corrections, errata, reviewer, and relationship to the catalog's 1202
   attribution.
8. The foundation, TCB, computation, freshness, and revocation profiles for the selected target.

## Boundary cases

No case is excluded at intake. Statement review must explicitly disposition index zero, index one,
the first recurrence instance, predecessor notation at indices below two, the empty or zero-length
counting model, zero- versus one-based shifts, negative indices if integers are selected, and
coercions to other codomains. For a generalized recurrence it must also address zero or nonstandard
initial values, noncommutative addition if relevant, and whether the recurrence starts at every
natural index.

## Excluded substitutions

- `THM-M-0924` (Lucas numbers) is a distinct recurrence family.
- `THM-M-0926` (Cassini's identity) and `THM-M-0927` (Binet's formula) are separate catalog targets
  about the Fibonacci sequence, not this unidentified root.
- Zeckendorf representation, gcd/divisibility laws, monotonicity, golden-ratio limits, fast
  computation, and an isolated numerical table are not substitutes.
- A recursive definition, structure field, or hypothesis that stores the desired conclusion cannot
  be presented as an independently sourced theorem proof.
- The Fibonacci toy branch in legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_018.lean`
  belongs to the distinct `THM-M-0405` primitive-divisor work. Its index-three computation grants
  no statement or proof credit here.
- A theorem name, API probe, `#check`, experiment, or the untrusted `已验证` label supplies no H or M
  completion credit.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Data.Nat.Fib.Basic` defines `Nat.fib` and exposes its zero, one, two, and recurrence
interfaces. These are candidate substrate for a future corrected target. No canonical module,
declaration, normalized expression, environment fingerprint, alternate transport, mutation suite,
obligation registry, or discovery protocol is frozen by this intake.
