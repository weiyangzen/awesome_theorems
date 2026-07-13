# Scope map

## Preserved theorem family

The catalog phrase `(a+b)^n` expansion formula identifies the classical binomial theorem family.
A conventional candidate scope is:

> In a commutative semiring, for every natural number `n` and elements `a` and `b`, the power
> `(a + b)^n` equals the finite sum of the terms
> `a^m * b^(n-m) * (n choose m)` for `0 <= m <= n`.

A pinned Lean candidate writes that family as:

```text
forall {R : Type u} [CommSemiring R] (a b : R) (n : Nat),
  (a + b) ^ n =
    sum m in Finset.range (n + 1), a ^ m * b ^ (n - m) * (Nat.choose n m : R)
```

This is a candidate family boundary, not a frozen canonical expression. The catalog supplies no
primary source, coefficient domain, commutativity premise, coefficient convention, or exact sum,
so source review and the dependent statement gate must approve those choices before statement
credit.

## Decisions required at statement freeze

1. Admit and independently review an immutable primary or authoritative source passage, including
   its exact statement, definitions, assumptions, proof boundary, corrections, and errata.
2. Freeze the coefficient domain: natural numbers, integers, a commutative semiring or ring, or a
   more general semiring with an explicit `Commute a b` premise.
3. Freeze universes, ordered binders, every typeclass and explicit hypothesis, equality direction,
   and the cast or scalar action used for `Nat.choose n m`.
4. Fix the index convention: exponent `m` on `a` and `n - m` on `b`, the reversed convention, or
   an antidiagonal pair with exponents summing to `n`.
5. Fix the finite index set and endpoints, including whether the formula uses
   `Finset.range (n + 1)`, an inclusive interval, or `Finset.antidiagonal n`.
6. Include `n = 0` and verify the empty-looking boundary actually has the single `m = 0` term;
   also check `n = 1`, `a = 0`, `b = 0`, and the zero or subsingleton coefficient type.
7. Distinguish a two-term binomial expansion from the multinomial theorem, Pascal's identity,
   special evaluations such as `(1 + 1)^n`, and subtraction or characteristic-specific variants.
8. Freeze foundation, TCB, computation, freshness, and ownership profiles, then perform the four
   required statement mutations before inspecting proof closure.

## Related forms, not substitutes

- `add_pow` uses a commutative semiring and a `Finset.range (n + 1)` sum.
- `Commute.add_pow` works in a possibly noncommutative semiring under `Commute a b`; selecting it
  changes an implicit algebraic premise and must be source-approved.
- `Commute.add_pow'` uses `Finset.antidiagonal n` and natural scalar action, avoiding natural
  subtraction. Its relationship to a chosen range-sum root needs a checked transport.
- Reversing the powers or coefficient index is mathematically related by symmetry, but a credited
  alternate form needs a checked equality or `Iff` in the selected environment.
- Polynomial, formal-power-series, integer, real, and complex specializations are instances of a
  sufficiently general root, not automatic replacements for it.

## Boundary and non-substitution rules

- `n = 0` is included and yields one on both sides through the single zero-index term.
- `n = 1` is included and must reduce to `a + b` without an extra side condition.
- `a = 0`, `b = 0`, characteristic-positive semirings, the zero semiring, and subsingleton models
  are not silently excluded unless an accepted source requires an exclusion.
- A formula proved only for natural, integer, real, or complex coefficients cannot replace a
  source-selected general algebraic target without a checked relationship in the correct direction.
- The multinomial theorem, Pascal's identity (`THM-M-0912`), inclusion-exclusion (`THM-M-0913`),
  generating functions (`THM-M-0915`), and Catalan-number identities (`THM-M-0921`) are distinct
  targets and provide no inherited status.
- A subtraction formula, Frobenius/characteristic formula, special value, fixed exponent, or
  numerical example is not the general binomial theorem.
- A structure, hypothesis, custom axiom, oracle, computation, or unchecked certificate containing
  the desired equality is circular and receives no proof credit.
- The catalog's `已验证` label, a theorem-name match, API output, and this discovery probe are not
  human-source or kernel-completion evidence.

No canonical expression, fingerprint, checked alternate transport, or proof body is frozen by this
intake. Those belong to dependency-ordered downstream phases.
