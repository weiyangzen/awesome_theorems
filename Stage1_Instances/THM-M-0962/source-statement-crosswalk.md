# THM-M-0962 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7022-7027` contains exactly the Frankl-Wilson name, attribution
Péter Frankl/Richard Wilson, year 1981, the gloss `相交族的上界` (upper bound for an intersecting
family), importance "high," and status `已验证`. All six uncited lines entered the repository in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26227-26252` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

## Primary-source lead

The matching bibliographic record is P. Frankl and R. M. Wilson, *Intersection theorems with
geometric consequences*, *Combinatorica* 1(4) (December 1981), 357-368, DOI
`10.1007/BF02579457`. The publisher page, publisher-generated BibTeX, Crossref record, and OpenAlex
record were inspected on 2026-07-13. They agree on title, authors, journal, year, volume, issue, and
pages. OpenAlex reports the article closed, with no repository full text or open-access location;
the publisher PDF request returned an HTML access page rather than the article body.

The publisher abstract announces a modular uniform-family bound: a family `F` of `k`-subsets of an
`n`-set; distinct residues `mu_0, ..., mu_s` modulo a prime `p`; `k` congruent to `mu_0`; and, for
distinct family members, intersection size congruent to one of `mu_1, ..., mu_s`; then a binomial
cardinality bound is displayed. The HTML/BibTeX flatten the pair-membership notation and the stacked
binomial. The conventional reading is `|F| <= choose n s`, but the exact source typography,
quantifiers, qualifications, and theorem location must be checked in the primary body before this
becomes the canonical statement.

This supports `H1`: there is a named published source and a concrete unresolved mapping list. It is
not `H0`, because no theorem/page-level body, proof, assumptions, corrections, errata disposition,
or independent source review was available.

## Component crosswalk

| Repository/source component | Candidate mathematical meaning | Pinned Lean substrate | Intake status |
|---|---|---|---|
| "intersecting family" | likely modular restrictions on intersections of distinct uniform members, not merely nonempty intersections | `Set.IsIntersectingOf` expresses allowed exact natural intersection sizes | source identity lead only; modular transport is not defined |
| family of `k`-subsets of an `n`-set | duplicate-free finite uniform set family | `Set.Sized`, `Finset.powersetCard`, and `Fin n` can encode this | adjacent interfaces only |
| congruence modulo `p` | member size in one residue and pair intersections in listed other residues | `Nat.ModEq` or `ZMod p` are candidate encodings | carrier, coercions, and hypotheses open |
| distinct residues | source abstract says `mu_0, ..., mu_s` are distinct | a `Finset`, injective indexed family, or pairwise predicate could encode it | exact order and occurrence rules open |
| binomial upper bound | publisher markup conventionally reads `choose n s` | `Nat.choose n s` | exact typography and boundary cases open |
| Frankl/Wilson, 1981 | bibliographic attribution | no formal component | metadata match; proof-source admission open |
| `已验证` | catalog status label | no formal component | explicitly untrusted; no H/M credit |

## Pinned formal substrate and discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SetFamily.Intersecting` defines `Set.IsIntersectingOf` for distinct pairs of
finite sets whose intersection cardinalities lie in a set of naturals. `Mathlib.Data.Finset.Slice`
provides `Set.Sized` and uniform powerset slices, and `Mathlib.Data.Nat.ModEq` provides natural
congruence. The intake probe elaborates these APIs and `Nat.choose`.

A bounded case-insensitive search for the eponym and paper title over pinned mathlib Lean sources
found no matching declaration. This is an intake discovery result, not an exhaustive anchor audit,
an external-project search, or proof that no formalization exists. Definitions and interfaces alone
support only `M3`; no theorem body, exact statement match, or machine closure is credited.

## Required admission

The statement phase must acquire and pin an admissible source body, select and transcribe one exact
theorem, map every binder, hypothesis, conclusion, convention, and boundary case, resolve the
prime/prime-power and residue-occurrence questions, inspect corrections and errata, and obtain
independent source review. It must then elaborate exactly that claim in Lean with minimal imports,
serialize its expression and environment, check every credited transport, and run removed-
hypothesis, changed-domain, binder-scope, and boundary mutations. Until then the canonical target
is null and no downstream proof credit is lawful.
