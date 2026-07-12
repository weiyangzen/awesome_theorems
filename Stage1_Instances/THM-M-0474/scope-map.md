# Scope map

## Candidate root claim

For natural numbers `a` and `p`, if `p` is prime and `a` is coprime to `p`, then
`a^(p - 1)` is congruent to `1` modulo `p`.

This is the conventional completion of the catalog gloss, not yet an independently accepted source
statement. The statement phase must select a pinpoint source and decide whether the canonical
domain is natural numbers or integers before it freezes the exact Lean expression.

| Surface | Candidate in-scope meaning | Intake boundary |
|---|---|---|
| Modulus | `p : Nat` with `p.Prime` | Primality is absent from the catalog but indispensable to the named theorem |
| Base | `a : Nat` provisionally | An integer-base version is an alternate encoding until a source selects the domain |
| Nonzero class | `a.Coprime p`, equivalently for prime `p`, `Not (p divides a)` | This prerequisite is also absent from the catalog |
| Exponent | Natural subtraction `p - 1` | `p.Prime` implies `1 < p`, so truncation is harmless only under the prime premise |
| Conclusion | `a ^ (p - 1) congruent to 1 [MOD p]` | Equality in `ZMod p`, divisibility, and remainder forms require checked transports before credit |

## Why the missing premise cannot be ignored

With `a = p`, prime `p` divides the base and `p^(p-1)` is congruent to `0`, not `1`, modulo `p`.
`IntakeProbe.lean` kernel-checks this counterexample for every natural prime `p`. Thus the literal
unconditional gloss is not a broadened version of Fermat's little theorem; it is false. Coprimality
or nondivisibility is a semantic prerequisite, not a convenient proof assumption.

## Related forms, not substitutes

- The all-base form `a^p congruent to a (mod p)` does not require coprimality and is conventionally
  also called Fermat's little theorem, but it is not the catalog's displayed exponent/conclusion.
- Euler's totient theorem specializes to the candidate root when `p` is prime and
  `phi(p) = p - 1`; it is a more general theorem and has its own repository target.
- Equality in `ZMod p`, the units form, the integer congruence form, and a divisibility or remainder
  form are alternate encodings. No one of them receives target credit at intake.
- `Mathlib.NumberTheory.Fermat` concerns Fermat numbers and is not the relevant import.

## Degenerate and mutation boundaries

The later statement gate must cover at least removal of coprimality, removal of primality, changed
base domain, changed binder scope, and boundary values such as `a = 0` and `p = 2`. Intake records
these requirements but does not claim the full rev-5.6 mutation suite or a canonical expression
fingerprint.
