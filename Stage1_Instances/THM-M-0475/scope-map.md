# Scope map

## Received claim

The repository fixes only the name `Euler theorem`, the formula `a^phi(n) congruent to 1 (mod n)`,
Leonhard Euler, and 1763. The displayed formula does not bind `a` or `n`, define the totient or
congruence conventions, or state the necessary relation between the base and modulus.

The literal unconditional natural-number reading is false. `IntakeProbe.lean` checks the instance
`a = 2`, `n = 4`: `Nat.totient 4 = 2`, so the left side is `4`, which is not congruent to `1`
modulo `4`.

## Conventional candidate, not yet canonical

The closest conventional natural-number proposition is:

> For natural numbers `a` and `n`, if `a` is coprime to `n`, then `a^phi(n)` is congruent to `1`
> modulo `n`.

At the pinned mathlib revision this has the candidate encoding
`Nat.ModEq n (a ^ Nat.totient n) 1`, with hypothesis `Nat.Coprime a n`. Intake does not freeze it as
the canonical claim because the repository has no source edition, theorem locator, translation,
assumption audit, or independent review that licenses the repair.

## Proposition-changing decisions

The statement phase must resolve all of the following from an immutable, reviewed source:

- whether the base and modulus range over naturals, integers, positive naturals, or residue classes;
- whether coprimality is stated as `gcd(a,n)=1`, invertibility modulo `n`, or another equivalent form;
- whether the modulus is restricted to `n > 1`, `n > 0`, or includes `0` and `1` under a specified
  totient and congruence convention;
- whether `phi(n)` counts integers in `1..n` or naturals strictly below `n`, and how degenerate
  moduli are defined;
- whether congruence is `Nat.ModEq`, `Int.ModEq`, equality in `ZMod n`, or equality of remainders;
- the ordered binders, explicit hypotheses, coercions, and typeclass context; and
- which alternate encodings are equal, equivalent, stronger, or only related, with checked
  transports for every credited form.

These choices are mathematically harmless only after their hypotheses and boundaries are mapped;
they are not interchangeable by name alone.

## Boundary cases

Pinned mathlib defines `Nat.totient 0 = 0`, `Nat.totient 1 = 1`, and
`Nat.ModEq n x y` as `x % n = y % n`. Its direct candidate therefore covers:

- `n = 0` only when `a = 1`, the sole natural base coprime to zero; then `a^0 = 1`;
- `n = 1` for every `a`, because every pair with modulus one is coprime and all naturals are
  congruent modulo one; and
- composite moduli without difficulty when the base is coprime to the modulus.

These are properties of the candidate encoding, not evidence that a historical source intended
those conventions. A future remainder-equality form such as `a^phi(n) % n = 1` generally needs a
nontrivial-modulus premise because the right side is not reduced.

## Explicit exclusions

- The unconditional catalog formula is not accepted; the concrete `a = 2`, `n = 4` mutation refutes
  it.
- Fermat's little theorem is a prime-modulus specialization and belongs to `THM-M-0474`; it cannot
  replace this root.
- Carmichael's theorem uses a generally smaller exponent and is a strengthening, not the displayed
  statement.
- The units, `ZMod`, integer, divisibility, and remainder forms are alternate encodings requiring
  source mapping and checked transports before credit.
- Euler's criterion, Euler's partition theorem, Euler's homogeneous function theorem, Euler's
  identity, and other namesakes are unrelated targets.
- The catalog's untrusted `verified` label and the pinned API probe are not human-source or theorem
  completion evidence.

## Formal boundary

`Mathlib.FieldTheory.Finite.Basic` declares `Nat.ModEq.pow_totient` and `ZMod.pow_totient` at the
manifest-pinned revision. The probe authenticates their types and kernel elaboration, but intake
does not freeze an expression fingerprint, audit terminal bodies or transitive dependencies, or
credit a proof. Those are the statement and anchor-audit phases.
