# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3595-3600` supplies the name `张益唐定理`, attribution Yitang
Zhang, year 2013, and the gloss `存在无穷多对素数差小于7000万`: there are infinitely many pairs
of primes whose difference is less than seventy million. Git blame assigns all six uncited lines
to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:13433-13458` repeats the gloss while explicitly leaving precise
definitions and premises, proof process and dependencies, equivalent forms, axioms, and machine
artifacts open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`. Those repository records identify the theorem family but
provide no H0 or machine-proof evidence.

## Primary publication

Yitang Zhang, "Bounded gaps between primes," *Annals of Mathematics* 179 (2014), no. 3,
1121-1174, DOI `10.4007/annals.2014.179.3.7`, is the primary source. The journal records receipt
on 2013-04-17, revision on 2013-05-16, acceptance on 2013-05-21, and online publication on
2014-05-01. This explains the catalog's 2013 date without changing the publication identity.

The abstract on journal page 1121 states

```text
lim inf as n tends to infinity of (p_(n+1) - p_n) < 7 * 10^7,
```

where `p_n` is the nth prime. On journal page 1122, Theorem 1 states the admissible-tuple result
for `k0 >= 3.5 * 10^6` and gives the same liminf inequality as its consequence. The publisher PDF
retrieved during intake has SHA-256
`231a33cffb19a76305df262e3ab1fac4142865493d6350c6bc142011e1c8a7a1`; the publisher landing
page had SHA-256 `791b2e24c4e2423fc65037a2753be02c04cf233dad4bc90f430b46ab7d25906c`.
These are reproducibility observations, not vendored release evidence or an independent review.

## Component crosswalk

| Repository wording | Primary-source resolution | Candidate pinned Lean surface | Intake disposition |
|---|---|---|---|
| `素数` (primes) | `p_n` is the nth prime | `Nat.Prime`; `Nat.nth Nat.Prime`; `Nat.prime_nth_prime` | direct statement substrate only |
| `素数对` (pairs) | consecutive pair `(p_n, p_(n+1))` | next two values of the strictly monotone enumeration | catalog omission repaired only by the source; transport still open |
| `无穷多` (infinitely many) | liminf as the index tends to infinity | candidate `forall N, exists n >= N, ...` or `Frequently atTop` | exact equivalence and encoding must be checked |
| `差` (difference) | positive consecutive gap `p_(n+1) - p_n` | natural subtraction plus `Nat.nth_strictMono` | domain/cast choice remains statement work |
| `小于7000万` | strict `< 7 * 10^7` | candidate `< 70000000` | exact strict bound preserved; `<=` is excluded |
| theorem proof source | admissible-tuple Theorem 1 implies the gap bound | no located exact pinned declaration | future obligation/provenance node, not a substituted root |

## Source status boundary

The primary statement was inspected, so the theorem family and consecutive-gap correction are
much firmer than the catalog alone. H0 nevertheless remains unavailable at intake: no independent
review has checked the complete assumption/definition mapping, proof-node crosswalk, incorporated
references, correction and errata status, equivalence between liminf and the proposed Lean
infinitely-often encoding, or translation back to the Chinese gloss. The source paper itself also
does not assert that its result was machine formalized.

## Pinned formal lead

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.NumberTheory.PrimeCounting` imports the nth-prime infrastructure and exposes:

| Declaration | Role | Boundary |
|---|---|---|
| `Nat.nth` | zero-indexed enumeration of naturals satisfying a predicate | generic enumerator, not Zhang's theorem |
| `Nat.infinite_setOf_prime` | infinitude of the prime set | ensures the enumeration is total |
| `Nat.prime_nth_prime` | every enumerated value is prime | statement substrate only |
| `Nat.nth_strictMono` | enumeration of an infinite set is strictly monotone | justifies positive adjacent gaps |
| `Nat.primeCounting` | number of primes up to a bound | adjacent analytic infrastructure only |

A bounded case-insensitive search over the repo-local Lean tree and pinned mathlib for Zhang,
bounded/prime gaps, the DOI, and the decimal bound found no target-specific declaration. That
negative result supports `M4` at intake; it is not the later exhaustive immutable anchor audit and
does not prove that no external formalization exists.

## Downstream source gate

Before statement acceptance, accountable reviewers must preserve a lawful immutable source,
approve the consequence rather than silently substituting Theorem 1, fix indexing and gap domains,
kernel-check equivalence of the chosen infinitude formulation with the published liminf claim,
record corrections and errata, and map every binder, definition, assumption, conclusion, and
boundary case. Until then the canonical expression, fingerprint, accepted proof state, and
H0/M0/R0 claims remain null.
