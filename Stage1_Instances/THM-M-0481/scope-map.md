# Scope map

## Preserved theorem family

The intake preserves the natural-number Bertrand-postulate family named by the catalog: after a
positive natural number `n`, there is a prime no larger than its double. This is a scope description,
not the frozen canonical proposition.

Pinned mathlib states the candidate half-closed form

```text
for n : Nat, if n != 0, then there exists p : Nat such that
p is prime, n < p, and p <= 2 * n.
```

The repository gloss is too short to establish that this is its exact endpoint and boundary
convention. A future statement phase may select this form, the customary strict form under `1 < n`,
or a checked equivalent encoding only after the source boundary is approved.

## Decisions required at statement freeze

1. Fix the domain: natural numbers, positive natural numbers, integers restricted to a positive
   range, or another explicitly sourced encoding.
2. State the lower-bound premise as `n != 0`, `0 < n`, `1 <= n`, or `1 < n`.
3. Decide the interval convention: `n < p` and `p <= 2 * n`, or `n < p` and `p < 2 * n`.
4. Decide whether the conclusion is an existential prime witness or an equivalent nonempty finite
   interval/filter/set assertion.
5. Fix multiplication and coercion conventions, ordered binders, universe information, every
   hypothesis, the exact conclusion, and every credited alternate encoding with a checked
   transport.

These choices alter the proposition or its boundary cases. Intake does not infer them from the
theorem's familiar name.

## Boundary and degenerate cases

- `n = 0`: no prime satisfies `0 < p <= 0`; an unrestricted natural reading is false.
- `n = 1`: the half-closed form holds with `p = 2`, but the strict-upper form `p < 2` fails.
- `n = 2`: both common forms hold with `p = 3`.
- Overflow is irrelevant for mathematical `Nat`, but any fixed-width computational reformulation
  would be a different target.
- A prime at the upper endpoint can occur only at the `n = 1` boundary in the common natural-number
  formulation; this is why the premise and endpoint decisions must be made together.

## Related forms, not substitutions

- The half-closed positive form and strict form for `1 < n` are classically interderivable only
  after treating the `n = 1` boundary explicitly; they are not literally the same proposition.
- A claim about a prime in `(x, 2x)` for real `x`, a prime-gap bound, a statement using the
  prime-counting function, or a consequence of the prime number theorem is not automatically this
  target.
- The large-number theorem `Nat.exists_prime_lt_and_le_two_mul_eventually` is a proof branch, not
  the all-positive root.
- Central-binomial, primorial, or analytic inequalities used by the pinned proof are ingredients,
  not substitute conclusions.
- A structure or hypothesis storing the desired prime witness supplies no proof.
- A theorem name, `#check`, source URL, catalog `已验证` label, or discovery probe supplies no H0 or
  M0 credit.

## Neighbor boundaries

`THM-M-0480` owns the prime number theorem and `THM-M-0482` owns Chebyshev estimates. Either may
provide contextual mathematics, but neither is inherited evidence or proof credit for this target.
The false friend called Bertrand's closed-orbit theorem in the physics catalog is unrelated.

## Formal boundary

No canonical Lean expression or expression fingerprint is frozen at intake. At pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks the exact candidate
declaration, its alias, the eventually-large branch, and boundary facts. That is scoped discovery
evidence, not the later exhaustive anchor audit, proof-body integration, or theorem proof.
