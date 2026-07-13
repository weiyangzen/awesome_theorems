# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3462-3467` supplies exactly the title `算术基本定理`, the
attribution `欧几里得`, the date `约公元前300年`, the statement `大于1的整数可唯一分解为素数乘积`,
importance `高`, and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The six-line excerpt SHA-256 is
`bceb698f679a295016ac8f0b3528128bc1d729613e8184892d4ba4a42868283d`.

`Docs/Stage0_Blueprint.md:12920-12945` repeats the gloss while explicitly leaving the precise
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine state, and
artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository gives no edition, book/proposition/page, translation, incorporated definitions,
proof passage, assumption map, correction or errata status, or independent reviewer. It therefore
supports discovery and a stable theorem-family reading, not `H0`.

## Component crosswalk

| Catalog component | Provisional mathematical meaning | Pinned Lean surface | Intake result |
|---|---|---|---|
| integer greater than one | positive integer represented by `n : Nat` and `1 < n` | `Nat`, `Nat.primeFactorsList` | exact Nat domain now elaborated; master acceptance pending |
| factorization | a finite list of prime naturals with product `n` | `Nat.prod_primeFactorsList`; primality via `Nat.prime_of_mem_primeFactorsList` | close candidate APIs elaborate |
| unique | every prime list with product `n` is equal up to order | `Nat.primeFactorsList_unique` returning `List.Perm` | direct theorem-family candidate, not accepted root proof |
| product of primes | repetition allowed, equivalently finite prime exponents | `Nat.prod_factorization_pow_eq_self`, `Nat.prod_pow_factorization_eq_self`, `Nat.factorizationEquiv` | alternate exponent representation; transport open |
| Euclid, circa 300 BCE | historical attribution | source provenance only | catalog metadata; exact genealogy not accepted |
| verified | untrusted catalog status | would require exact local kernel evidence | no H or M completion credit |

## Inspected historical leads

An online English presentation of David E. Joyce's edition of Euclid's *Elements* was inspected at
Book VII Proposition 30, Book VII Proposition 31, and Book IX Proposition 14. VII.30 gives Euclid's
lemma for a prime measuring a product; VII.31 gives existence of a prime divisor for a composite
number; IX.14 excludes any additional prime divisor from the least number measured by given primes.
The inspected HTML SHA-256 values were respectively
`1277ef2fd7becbd52ef50f07a9523299203b54fda452a3ffffc597009c35f398`,
`6810670e133b484776e5e41a5f84c4f70c8986b4481750a412bbf66e6faed06e`, and
`8b7ad7a2fbb4dd031ed729960ef74faef8b2f1d94c19f86252b0097370ad4a29`.

These propositions are historically relevant proof ingredients, but the inspected web pages are
not an archived lawful primary edition or a complete crosswalk to the modern theorem. In
particular, IX.14 is not verbatim the modern existence-and-uniqueness statement. Original-language
and edition provenance, translation fidelity, incorporated Euclidean definitions, the complete
derivation of arbitrary finite prime factorization, corrections/errata, and independent review
remain open. The historical leads therefore support `H1`, not `H0`.

Discovery URLs:

- <https://mathcs.clarku.edu/~djoyce/java/elements/bookVII/propVII30.html>
- <https://mathcs.clarku.edu/~djoyce/java/elements/bookVII/propVII31.html>
- <https://mathcs.clarku.edu/~djoyce/java/elements/bookIX/propIX14.html>

## Pinned Lean discovery anchors

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Data.Nat.Factors` contains the canonical increasing prime-factor list, product
reconstruction, primality of its members, nonemptiness exactly when `1 < n`, and
`Nat.primeFactorsList_unique`, whose source documentation names the fundamental theorem of
arithmetic. `Mathlib.Data.Nat.Factorization.Defs` contains prime-exponent reconstruction,
injectivity, inverse reconstruction, and `Nat.factorizationEquiv`.

`IntakeProbe.lean` checks the exact names and representative boundaries against the existing pinned
toolchain. This is a bounded repo-local/mathlib discovery probe, not the downstream exhaustive
candidate audit. The statement phase now owns an exact prime-list target and checked direct
expansion, but no checked list-to-exponent transport, terminal proof-body resolution, transitive
dependency audit, placeholder/axiom closure, proof wrapper, or M0 credit is claimed.

## Admission requirement

Before `H0`, a source reviewer must preserve a lawful immutable edition, locate every proposition
and incorporated definition used for both existence and uniqueness, map the ancient number and
measurement conventions to the modern natural-number claim, record translation and errata status,
and obtain independent review. Before formal statement acceptance, the integration lane must
separately approve the now-elaborated Lean expression, checked direct-expansion transport,
fingerprints, and mutation suite. Neither source confidence nor the pinned candidate can substitute
for the other.
