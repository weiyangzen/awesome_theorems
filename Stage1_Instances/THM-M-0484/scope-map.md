# Scope map

## Preserved theorem family

The repository names the Lucas-Lehmer primality test for Mersenne numbers. The candidate human
scope preserved at intake is the correctness criterion below:

- `p` is a natural exponent with `3 <= p` (equivalently, in the conventional source formulation,
  an odd prime exponent after the primality consequence is accounted for);
- the Mersenne number is `M_p = 2^p - 1`;
- the recurrence starts with `s_0 = 4` and satisfies `s_(n+1) = s_n^2 - 2`, computed modulo `M_p`;
- `M_p` is prime if and only if the residue after `p - 2` recurrence updates is zero.

This is a candidate scope, not the statement-phase canonical declaration. The catalog says none of
the formula, binder, hypothesis, recurrence, indexing, or low-exponent boundary explicitly.

## Candidate Lean encoding

At the pinned mathlib revision, the natural-number Mersenne function is `mersenne p = 2^p - 1`.
`LucasLehmer.s` is the integer recurrence with zero-based seed `s 0 = 4`;
`LucasLehmer.sZMod p` is its version in `ZMod (2^p - 1)`; the residue is
`sZMod p (p - 2)`; and `LucasLehmerTest p` says that residue is zero.

Mathlib exposes the two directions separately:

- a passing test implies primality under `1 < p`;
- Mersenne primality implies a passing test under `3 <= p`.

Their shared exact candidate scope is therefore `3 <= p -> (LucasLehmerTest p <->
(mersenne p).Prime)`. No separate `p.Prime` premise is needed for that candidate: primality of
`mersenne p` implies primality of `p` on the right, while a passing test already suffices on the
left. A source reviewer must decide whether to retain the conventional explicit odd-prime premise
or admit the sharper natural-number formulation through a checked source transport.

## Required statement decisions

1. Select an immutable, independently reviewed source proposition and decide whether `p` is an odd
   prime, any natural with `3 <= p`, or another explicitly equivalent domain.
2. Fix zero-based versus one-based recurrence indexing and prove the `p - 2` term transport.
3. Fix whether recurrence values live in integers with divisibility, natural remainders, or
   `ZMod (2^p - 1)`, and compile every credited equivalence.
4. Decide whether the theorem is the iff, only a certification/sufficiency direction, only the
   necessity direction, or also an algorithmic correctness and complexity statement.
5. Separate mathematical correctness from the catalog adjective "fast". Any runtime claim needs a
   cost model, arithmetic representation, algorithm, and asymptotic or concrete bound.
6. Freeze ordered binders, hypotheses, conclusion, minimal imports, normalized expression,
   foundation/TCB/computation profiles, and all required statement mutations.

## Boundary cases

- `p = 2` is not covered by the ordinary criterion: `mersenne 2 = 3` is prime, but the zero-based
  residue at `2 - 2 = 0` is `4 mod 3 = 1`, so `LucasLehmerTest 2` is false.
- `p = 0` and `p = 1` exercise truncated subtraction and degenerate moduli and are excluded by the
  candidate lower bound, not silently normalized away.
- Composite exponents at least three are included by the sharper mathlib candidate, but must be
  reconciled with the conventional odd-prime source domain before canonical selection.
- The statement tests one indexed Mersenne number. It does not enumerate all Mersenne primes,
  prove infinitely many exist, or certify a particular large exponent unless separately stated.

## Excluded substitutions

- `THM-M-0483`, the separate catalog entry "Mersenne primality criterion," does not transfer its
  future source, statement, proof, or status to this target.
- General Lucas primality tests, Fermat tests, Proth tests, trial division, and generic primality
  certificates are different algorithms.
- The Bilu-Hanrot-Voutier theorem on primitive divisors of Lucas/Lehmer sequences is unrelated to
  this Mersenne primality criterion despite sharing the names Lucas and Lehmer.
- A finite computation for selected exponents, a benchmark, a `norm_num` success, or a boolean
  implementation alone does not prove the universally quantified correctness theorem.
- The catalog's untrusted `已验证` label, a theorem name, a source URL, `#check`, or an API probe
  supplies no accepted H or M credit.

## Formal boundary

`IntakeProbe.lean` imports the exact-topic mathlib module, checks the definitions and both theorem
directions, reports their axioms, composes the candidate iff, and verifies the `p = 2` exception.
It does not freeze the canonical statement, establish the source/index transport, conduct the
exhaustive anchor or provenance audit, or install proof credit.
