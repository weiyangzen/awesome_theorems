# THM-M-0032 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:249-254` supplies the title, Maurice Auslander and David
Buchsbaum attribution, year 1958, literal claim `正则局部环是UFD` ("a regular local ring is a
UFD"), importance "high," and status `已验证`. Git blame places all six uncited lines at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:992-1017` repeats the claim while leaving exact definitions, premises,
proof route, dependencies, equivalent statements, axioms, machine status, and artifacts open. The
rev-5.6 manifest keeps `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Inspected primary source

Maurice Auslander and D. A. Buchsbaum, *Unique Factorization in Regular Local Rings*,
*Proceedings of the National Academy of Sciences* **45**(5), 733-734 (May 1959), DOI
`10.1073/pnas.45.5.733`, PMCID `PMC222624`. The inspected NCBI page scans have SHA-256
`ca2e179777de42435f16d87939f22d7b7f58ed789ebd311fa5305cdee2642126` (page 733) and
`71ac88eb4b4f68a5eb604b00b2905ff8d788403f0ba3a209510428f0535267ea` (page 734).

Page 734 states Theorem 5: "Every regular local ring is a unique factorization domain." This is a
direct textual match to the catalog claim. The paper was communicated on March 6, 1959 and
published in May 1959; intake found no basis for the catalog's 1958 date, so that date remains an
unresolved discrepancy rather than an accepted source fact.

The paper says throughout that `R` is a local ring with maximal ideal `M` and follows definitions
and notation from an earlier Auslander-Buchsbaum paper. Thus inspection locates the exact root but
does not by itself supply a self-contained definition and assumption crosswalk. No independent
source reviewer has approved the mapping, so this remains H1 rather than H0.

## Primary proof-node lead

| Source node | Source role | Intake boundary |
|---|---|---|
| Proposition 1, p. 733 | under homological-dimension and minimal-generator conditions, an ideal is principal and its generator is a nonzerodivisor | definitions and notation inherited from reference 1 remain to be admitted |
| Corollary 2, pp. 733-734 | a prime ideal satisfying localization-dimension and homological-dimension bounds is principal | bridge into the dimension-three proof; exact premises must be mapped |
| Theorem 3, p. 734 | a local domain of dimension at most three with finite homological dimensions for minimal primes is a UFD | intermediate theorem, not the unrestricted target |
| Corollary 4, p. 734 | every regular local ring of dimension at most three is a UFD | strict dimension-bounded weakening |
| Theorem 5, p. 734 | every regular local ring is a UFD | exact catalog root; proof invokes Nagata's reduction |

The introduction attributes to Nagata a proposition reducing the unrestricted result to the
dimension-three case. The footnote says Nagata had an unpublished result for complete regular local
rings and that combining it with completion results gives another reduction proof. These source
boundaries require distinct obligations later; this intake does not certify their full genealogy,
assumptions, or correctness.

## Modern statement cross-check

The Stacks Project, Lemma 15.123.2, stable tag `0AG0`, states exactly "A regular local ring is a
UFD." The inspected HTML SHA-256 is
`785af7cb4e040abda98bcbe4414785a4c2367059925a01b6d5524c44455008b7`. Its modern proof uses
regular-local-domain, regular-quotient, height-one-prime, localization, invertible-module, and
factorization results. It corroborates the theorem family and identifies a possible modern proof
route, but it does not replace the primary-source premise/definition/history review or establish
H0.

## Component mapping

| Source component | Mathematical component to freeze | Prospective Lean surface | Intake status |
|---|---|---|---|
| "ring" and "local ring" | commutative unital nontrivial local ring with one maximal ideal | `[CommRing R]`, `IsLocalRing R` | source convention not independently mapped |
| "regular local ring" | Noetherian local ring with the accepted regularity definition | `IsRegularLocalRing R`, `isRegularLocalRing_iff`, cotangent-space characterization | adjacent API checked; source transport open |
| domain consequence | regular local rings are integral domains | `IsDomain R` or a derived instance | no pinned derivation located or credited |
| "unique factorization domain" | factorization into primes, unique up to units | `UniqueFactorizationMonoid R` | adjacent interface checked; encoding ratification open |
| unrestricted "every" | arbitrary dimension and arbitrary universe after accepted conventions | universal ring/structure binders | exact ordered binders not frozen |
| 1958 | alleged result date | no formal component | conflicts with inspected 1959 publication; unresolved |
| `已验证` | catalog inventory label | no formal component | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.RingTheory.RegularLocalRing.Defs` defines `IsRegularLocalRing`; the UFD class is in
`Mathlib.RingTheory.UniqueFactorizationDomain.Defs`. `IntakeProbe.lean` authenticates these APIs.
A bounded exact-topic search found no `Auslander`, `Buchsbaum`, or declaration deriving
`UniqueFactorizationMonoid R` from `IsRegularLocalRing R`. The only located direction involving
regular local rings and principal ideals is the reverse special-case instance that a local domain
which is a principal ideal ring is regular.

This is intake discovery, not an exhaustive anchor audit and not proof that no external Lean 4
formalization exists. The canonical module, proposition, elaborated-expression hash, environment
fingerprint, alternate encodings, mutations, terminal proof body, and trust closure remain open.
