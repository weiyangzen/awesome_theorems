# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6917-6922` supplies exactly these fields:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `Roth theorem` | recognizable theorem-family label |
| proposer | Klaus Roth | historical attribution only |
| time | 1953 | bibliographic lead |
| statement | integer sets contain a three-term arithmetic progression | incomplete slogan; no density or size premise |
| importance | high | scheduling metadata only |
| formalization status | verified | explicitly untrusted; no H, M, or R credit |

The English descriptions above translate the Chinese catalog text. All six uncited lines entered the
repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
`Docs/Stage0_Blueprint.md:25822-25847` repeats the slogan while explicitly leaving exact definitions
and premises, formal system, proof path, dependencies, alternate forms, axioms, machine status, and
artifact links open. The rev-5.6 manifest resets the target to `L0 / rework_required`.

## Primary-source lead

Crossref identifies K. F. Roth, "On Certain Sets of Integers," *Journal of the London Mathematical
Society* s1-28(1) (January 1953), 104-109, DOI `10.1112/jlms/s1-28.1.104`. This matches the catalog's
author and year. A second bibliographic service reports the same title, author, year, and DOI, and
reports no open-access PDF.

This is an `H1` primary bibliographic lead, not an `H0` source packet. The article body was not
inspected: no exact statement, incorporated definition, premise, proof step, correction, or erratum
was transcribed or independently reviewed. The DOI publisher endpoint was access-blocked in this
environment, and no remote file is admitted into the repository. Bibliographic metadata cannot
supply the catalog's missing density hypothesis or choose a formal variant.

## Component crosswalk

| Catalog component | Candidate mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| integer sets | a finite subset of an initial natural-number interval, or an infinite set of integers | `A : Finset Nat` with `A subset range n`, or a source-selected `Set Nat`/`Set Int` | domain and carrier open |
| omitted size premise | positive density, a finite lower cardinality bound, or an extremal little-o conclusion | real-cardinality inequality, a density predicate, or `IsLittleO atTop` | indispensable hypothesis/formulation absent from catalog |
| three-term arithmetic progression | nonconstant `a, b, c` in the set with `a + c = b + b` | negation of `ThreeAPFree`, after a checked convention map | equation, order, and nondegeneracy open |
| Klaus Roth / 1953 | historical theorem and proof source | immutable source record and source-to-node mapping | matching paper identified; body and mapping open |
| verified | untrusted inventory metadata | no declaration or proof body | no source or kernel credit |

The literal slogan cannot be the ordinary universal assertion over all integer sets: for example,
empty and singleton sets have no nonconstant three-term progression. That counterexample is a scope
diagnostic, not permission to repair the catalog silently. The missing premise must come from an
approved source.

## Pinned Lean candidate crosswalk

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.Additive.Corner.Roth` states that it proves Roth's theorem on progressions of
length three. It exposes three materially different candidate forms:

| Declaration | Exact candidate role | Intake boundary |
|---|---|---|
| `roth_3ap_theorem` | explicit finite-density theorem for a sufficiently large finite abelian group | broader/different ambient domain; not the integer root without a checked transfer |
| `roth_3ap_theorem_nat` | explicit finite-density theorem for `A subset range n`, using `cornersTheoremBound (epsilon / 3)` | direct finite natural-number candidate, but its quantitative bound and conventions are not source-selected |
| `rothNumberNat_isLittleO_id` | asymptotic extremal form `rothNumberNat N = o(N)` | direct asymptotic candidate, but equivalence to the received slogan is not frozen |

The definition module encodes `ThreeAPFree s` by requiring a triple in `s` satisfying
`a + c = b + b` to collapse, with a natural-number lemma exposing the endpoint-equality convention.
The natural-number theorem's docstring describes `{1, ..., n}`, while its checked type uses
`Finset.range n`, namely the zero-based carrier `{0, ..., n - 1}`. This convention mismatch is one
more reason to require an explicit source and interval transport rather than crediting the name.
The intake probe elaborates these declarations and reports their current axioms. That demonstrates
usable exact-family formal infrastructure, hence provisional `M3`; it does not select a canonical
statement, establish source identity, audit terminal proof bodies or transitive trust, or authorize
`M0`.

The bounded repository and pinned-mathlib search also encountered the Ruzsa-Szemeredi and Behrend
modules as neighboring work, and a Thue-Siegel-Roth reference in transcendence theory. None is an
alternate root merely because it contains "Roth."

One legacy repo-local audit for the distinct Diophantine-approximation Roth target already records
the additive module and the names `roth_3ap_theorem`, `roth_3ap_theorem_nat`, and
`rothNumberNat_isLittleO_id` in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_011.lean:989-1003,1069-1099`. Its conclusion that
they are a name collision is correct only relative to that different Diophantine target. For this
additive-combinatorics target the rows are useful prior discovery evidence, but their legacy owner,
statement, and receipts transfer no status or proof credit to `THM-M-0947`.

## Required admission

The statement phase must preserve and independently review an immutable exact source passage,
including definitions, premises, conclusion, proof boundary, corrections, and errata. It must then
justify the selected finite, asymptotic, or infinite form; freeze density, interval, binders,
nondegeneracy, and boundary cases; and map that claim to one exact Lean expression. Only later anchor
and provenance audits may decide whether any pinned candidate supplies a checked wrapper or proof
body. Until those gates run, the root remains `[H1, M3, R4]` and the canonical target is null.
