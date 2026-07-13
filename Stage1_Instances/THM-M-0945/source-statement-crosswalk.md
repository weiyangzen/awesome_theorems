# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6903-6908` supplies exactly the title `Green-Tao theorem`,
attribution Ben Green/Terence Tao, year 2004, slogan `the primes contain arbitrarily long arithmetic
progressions`, importance `high`, and status `verified` (English descriptions here translate the
catalog's Chinese fields). All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:25768-25793` projects the record as `THM-M-0945` while explicitly leaving
the formal system, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Rev-5.6 therefore retains `verified` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Primary-source lead

The inspected publication is Ben Green and Terence Tao, "The primes contain arbitrarily long
arithmetic progressions," *Annals of Mathematics* 167(2) (2008), 481-547, DOI
`10.4007/annals.2008.167.481`. The Annals-hosted 67-page PDF observed on 2026-07-13 had SHA-256
`967dd6f5bb53d70abdbb07be0afe59e60b2a232e2c3387966013a09960e52c89`.
Its page 482 states Theorem 1.1: "The prime numbers contain infinitely many arithmetic progressions
of length k for all k." The arXiv record `math/0404188v6` reports original submission on 2004-04-08,
revision on 2007-09-23, and "Further minor corrections."

The proof of Theorem 1.1 on page 524 explicitly says that the degenerate case with common
difference `r = 0` is discarded. This is evidence that the source intends nonconstant
progressions, but the exact positive-difference Lean encoding still requires reviewed admission.

This is a strong pinpoint primary-source lead, not `H0`. The paper and revision metadata were
inspected outside the repository and were not admitted as immutable public artifacts. Intake did
not complete a reviewed source-definition transcription for arithmetic progressions and primes,
fix the domain and boundary conventions for `k`, map every proof dependency and correction, audit
later errata, or obtain independent review.

## Component crosswalk

| Catalog component | Primary-source component | Prospective Lean surface | Intake status |
|---|---|---|---|
| primes | "prime numbers" in Theorem 1.1 | `Nat.Prime` or a checked positive-integer encoding | carrier and transport open |
| arbitrarily long | "of length k for all k" | an ordered length binder with explicit small-case policy | binder domain open |
| arithmetic progressions | source's standard progression notion | witnesses `a`, `d`, indexed membership, and nondegeneracy | representation and definitions not frozen |
| existence strength | "infinitely many" for every length | an infinite witness set or a checked implication to existence | catalog/source strength mapping open |
| Green/Tao, 2004 | 2004 preprint; revised 2007; journal publication 2008 | immutable provenance and correction ledger | matching source found; full audit open |
| `verified` | repository inventory label only | accepted kernel declaration and receipt would be required | explicitly rejected |

## Variant boundary

Theorem 1.2 of the same paper asserts infinitely many length-`k` progressions in every subset of
the primes with positive relative upper density. It is stronger than the catalog slogan and is not
the selected root. Szemeredi's positive-density theorem, Roth's length-three theorem, Dirichlet's
primes-in-a-residue-class theorem, Green-Tao-Ziegler linear-equations results, and computationally
found long prime progressions are related but not aliases.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`Nat.Prime`, `Nat.exists_infinite_primes`, `Nat.infinite_setOf_prime`, `ThreeAPFree`,
`roth_3ap_theorem_nat`, and `Combinatorics.exists_mono_homothetic_copy`. These provide prime
infinitude, length-three additive-combinatorics, and finite-color infrastructure only.

A bounded case-insensitive search over repo-local Lean and pinned mathlib found no Green-Tao or
arbitrary-length prime-progression declaration. Pinned mathlib does contain Dirichlet's theorem on
primes in a residue class, but that is not a finite progression whose every term is prime. These
observations are intake discovery only, not a complete external anchor audit or a global absence
claim. No target declaration or proof body is present in the probe, so machine status remains
`M4`.

## Required admission

Before statement acceptance, reviewers must lawfully preserve an immutable source version,
transcribe and approve Theorem 1.1 plus every incorporated definition and convention, reconcile the
2004/2007/2008 versions and corrections, audit errata, and freeze the exact length domain, prime
carrier, progression witnesses, nonzero-difference rule, quantifier order, infinite-many strength,
and boundary cases. The statement phase must then encode only that claim, minimize pinned imports,
serialize the elaborated expression and environment, compile every credited transport, and run all
required statement mutations.
