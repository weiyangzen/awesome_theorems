# Source-statement crosswalk

## Source status

No primary source is accepted at intake. The repository's underlying metadata record in
`Docs/researches/math_theorems.md` repeats the name, Pontryagin attribution, year 1947, and the
integral/stable gloss, but provides no title, edition, theorem number, page, hypotheses, or errata.
That record therefore cannot support `H0` or an exact formal statement.

The name strongly suggests the Pontryagin square, but this is a discovery hypothesis only. A later
source audit must locate a stable facsimile or edition of the intended primary work, verify whether
Pontryagin is the source of the construction or only its namesake, and record exact theorem/page
anchors and corrections. A modern textbook may clarify notation but cannot silently replace or
repair the selected primary claim.

## Crosswalk

| Metadata component | Source-level ambiguity | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Pontryagin operation" | square, another cohomology operation, or a different Pontryagin-named construction | no declaration name or type is justified | blocking |
| "integral cohomology" | conflicts with the standard mod-2 to mod-4 typing commonly called Pontryagin square | coefficient objects and maps cannot be bound | blocking |
| "stable" | conflicts with degree doubling unless a different operation or qualified notion is intended | suspension/naturality law cannot be stated | blocking |
| "1947" and attribution | no bibliographic anchor accompanies either field | edition, theorem, page, assumptions, and errata are absent | unresolved |
| "verified" | provenance and formal system are absent | supplies no human or kernel evidence | rejected as proof credit |

## Required source decision

The statement phase must choose exactly one primary-source proposition, transcribe its assumptions
and conclusion, and explain every normalization used in Lean. If the primary record proves a family
of laws, the canonical root must say whether it asserts existence of the operation, a single law,
or the conjunction/package of laws. It must not blend variants from multiple sources.

Candidate Lean declarations and external formalizations belong to the later anchor-audit phase.
Before `H0`, an independent reviewer must verify the primary edition, theorem/page locations,
definitions, assumptions, attribution, date, and errata against the frozen canonical claim.
