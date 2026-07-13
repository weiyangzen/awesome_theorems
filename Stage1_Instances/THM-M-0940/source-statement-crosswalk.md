# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6868-6873` is the complete source record. It contains the title
`加法组合学基本定理`, attribution `众多数学家` (many mathematicians), period `20世纪`, gloss
`加法组合的核心结果`, importance "high," and status `已验证`. Git blame places all six uncited
lines in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, theorem locator, mathematical definitions, domains, ordered binders, hypotheses,
conclusion, constants, proof boundary, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25633-25658` repeats the same gloss and explicitly leaves the target
formal system, logical foundation, exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Mathematical component required | Prospective Lean component | Intake result |
|---|---|---|---|
| `加法组合学` | exact carrier, additive structure, input objects, and finiteness or density model | explicit types, universes, structures, typeclasses, and representations | subject area only |
| `基本定理` | stable theorem identity, exact primary-source locator, and correction history | one canonical `Prop` and provenance identity | no standard result selected |
| `核心结果` | one direct, inverse, structural, extremal, covering, or counting claim | ordered binders, premises, and exact conclusion | not truth-valued |
| many mathematicians / twentieth century | attributable source genealogy and edition | immutable source and node crosswalk | no author, work, theorem, or page |
| `已验证` | accepted human-source and kernel evidence would be required | checked declaration, body provenance, trust closure, and receipt | untrusted metadata; no H or M credit |

## Source-discovery boundary

The repository contains no other occurrence that identifies this row's theorem. A dated exact-title
arXiv query returned zero results. A Crossref title query returned books and unrelated works on
additive combinatorics, not a uniquely named "fundamental theorem" source. A general web query
timed out and receives no evidentiary weight. These bounded searches do not prove global absence;
they show only that intake did not obtain a source capable of selecting a proposition.

No primary mathematical source candidate is admitted. Accordingly there is no edition, theorem or
page, assumption map, proof boundary, corrections audit, errata audit, source-to-node crosswalk, or
independent review from which H0 or even an exact H1 proposition could be derived. The worker
proposes H5 only for the received catalog wording as an unstable target; it makes no claim about
the truth or published status of any standard additive-combinatorics theorem.

## Candidate-result crosswalk

| Candidate family | Distinguishing contract | Repository ownership | Intake status |
|---|---|---|---|
| Cauchy-Davenport | lower bound on a finite sumset, with prime-cyclic or generalized group hypotheses | `THM-M-0936` | separate target; not selected |
| Kneser / Kemperman | sumset structure and stabilizer phenomena in abelian groups | `THM-M-0938` / `THM-M-0939` | separate targets; not selected |
| Freiman | inverse structure of finite sets with small doubling | `THM-M-0941` | separate target; not selected |
| Ruzsa covering | cover a set by controlled translates of a difference set | `THM-M-0942` | separate target; not selected |
| Plunnecke-Ruzsa | bounds for iterated sums and differences under small growth | `THM-M-0943` | separate target; not selected |
| Balog-Szemeredi-Gowers | large additive energy yields a structured large subset | `THM-M-0944` | separate target; not selected |
| Green-Tao | arbitrarily long arithmetic progressions in the primes | `THM-M-0945` | separate target; not selected |

The candidates are neither aliases nor interchangeable formulations. Combining them would create
a new theorem package absent from the source record.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, representative exact
APIs include `cauchy_davenport_minOrder_add`, `ZMod.cauchy_davenport`, `IsAddFreimanHom`,
`Finset.ruzsa_covering_add`, `Finset.ruzsa_triangle_inequality_sub_sub_sub`, and
`Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_add`. Their signatures elaborate in the pinned
toolchain, but they state different results. An exact-phrase search found no Lean declaration for
the catalog title. This is bounded intake discovery, not an exhaustive anchor audit, a proof of
absence, or evidence for a canonical target.

## Required correction and admission

Before statement work, the integration lane must correct or confirm the target identity from one
lawfully accessible immutable authoritative source, select a pinpoint truth-valued proposition,
map all incorporated definitions, ordered binders, assumptions, constants, conclusion, proof
boundary, corrections, errata, and neighbor relationships, and obtain independent source review.
Only then may a statement worker encode that same claim in Lean, minimize imports, serialize its
elaborated expression and environment, check transports, and run the required statement mutations.
Until then the canonical mathematical and Lean statements remain null.
