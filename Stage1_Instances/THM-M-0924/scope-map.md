# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0924`, the title `卢卡斯数`, attribution to Edouard Lucas, the
year 1878, and the gloss `斐波那契数列的推广`. This intake preserves the Lucas-number and
Lucas-sequence subject suggested by those fields. Importance `中` and status `已验证` are catalog
metadata, not human-source or kernel evidence.

The wording names a mathematical object or family and describes its relation to Fibonacci numbers.
It does not state a proposition. In particular, it does not decide whether `Lucas numbers` means
the classical companion sequence `2, 1, 3, 4, 7, ...`, a general first-kind sequence `U_n(P,Q)`,
a second-kind sequence `V_n(P,Q)`, or a bundled theory of both.

## Candidate roots not credited

1. Define the classical natural Lucas sequence by `L(0) = 2`, `L(1) = 1`, and
   `L(n + 2) = L(n) + L(n + 1)`.
2. Given an independently defined sequence, prove its initial values and recurrence.
3. Prove that exactly one sequence has those initial values and recurrence.
4. Define `U_n(P,Q)` or `V_n(P,Q)` over integers or a more general carrier, with the sign and
   parameter conventions fixed.
5. Prove a relation such as `L(n) = F(n - 1) + F(n + 1)` on a source-specified domain.
6. Prove a Binet-type formula, addition law, divisibility property, counting interpretation, or
   another theorem about one selected Lucas family.

These are related but not interchangeable. A definition is not the same target as uniqueness; the
classical companion sequence is not the general `U` family; and a Fibonacci identity introduces
index and boundary choices not present in a recurrence definition.

## Decisions required before statement freeze

An approved target correction and independent source review must decide:

1. The exact truth-valued root rather than an object or family heading.
2. Classical `L_n` versus general `U_n(P,Q)`, `V_n(P,Q)`, or another source-defined convention.
3. Initial values, recurrence coefficients and signs, index origin, recurrence start, and whether
   parameters are fixed or quantified.
4. Index and value domains (`Nat`, `Int`, or another carrier), universes, and every required
   algebraic typeclass assumption.
5. Whether the target names a concrete sequence or characterizes arbitrary solutions, and whether
   the conclusion is pointwise, functional, existential, or unique-existential.
6. Ordered binders, all hypotheses, exact conclusion, and checked relationships among any credited
   alternate encodings.
7. One immutable source edition with statement/definition/proof locators, incorporated assumptions,
   corrections and errata, translation boundary, and accountable reviewers.
8. Foundation, TCB, computation, freshness, revocation, and archive policies for the selected root.

## Boundary cases

No case is excluded at intake. Statement review must explicitly disposition indices zero and one,
the first recurrence instance, predecessor notation below one, natural subtraction, negative
indices, zero or exceptional parameters, repeated or zero characteristic roots, degenerate
discriminant, coercions among number systems, and every denominator or division side condition in
a closed form. If a relation to Fibonacci numbers is chosen, its index shift and low-index cases
must be checked rather than inferred from notation.

## Neighbor and substitution boundaries

- `THM-M-0925` separately owns the Fibonacci sequence; it supplies no statement or proof credit.
- `THM-M-0926` (Cassini identity) and `THM-M-0927` (Binet formula) are separate targets, not a
  license to redefine this root as a familiar Fibonacci identity.
- `THM-M-0405` owns the Bilu-Hanrot-Voutier Lucas/Lehmer primitive-divisor theorem. Its legacy
  recurrence object is foreign-target discovery material only.
- Lucas-Lehmer and Lucas primality tests concern primality certificates, not the Lucas-number
  sequence named here.
- A finite value table, executable recurrence, generic recurrence API, docstring, or catalog status
  cannot substitute for a source-selected proposition and proof.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Algebra.LinearRecurrence` exposes generic recurrence, construction, solution, and uniqueness
interfaces. `Mathlib.Data.Nat.Fib.Basic` exposes `Nat.fib`. They are encoding substrate only. The
bounded exact-topic package search found no classical Lucas-number or Lucas-sequence declaration;
one prose mention in the elliptic-divisibility-sequence module supplies no object or theorem.

No canonical module, declaration, normalized expression, environment fingerprint, alternate
transport, mutation suite, obligation registry, or discovery protocol is frozen by this intake.

