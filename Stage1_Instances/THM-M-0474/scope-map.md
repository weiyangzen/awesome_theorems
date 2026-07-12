# Scope map

## Canonical local root claim

For natural numbers `a` and `p`, if `p` is prime and `a` is coprime to `p`, then
`a^(p - 1)` is congruent to `1` modulo `p`.

This is the conventional completion of the catalog gloss selected at intake. This statement phase
freezes the natural-number encoding as the canonical local target; it is not yet an independently
accepted primary-source statement. A pinpoint historical source, translation, premise audit, and
errata review remain open on the human-source axis.

| Surface | Candidate in-scope meaning | Intake boundary |
|---|---|---|
| Modulus | `p : Nat` with `p.Prime` | Primality is absent from the catalog but indispensable to the selected theorem |
| Base | `a : Nat` | This is the frozen local encoding; an integer-base form remains related but uncredited |
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

`Statement.lean` and `check_statement.py` reject removal of coprimality, replacement of the natural
base by an integer base, changing the universal base binder to an existential witness, and exclusion
of the `p = 2` boundary. The exact expression is fingerprinted. The canonical assumptions also
exclude composite or zero `p` and the `a = 0` case, because no prime is coprime to zero. No stronger
claim about an integer, `ZMod`, or all-base encoding is credited.
