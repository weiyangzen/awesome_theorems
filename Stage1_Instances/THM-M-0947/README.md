# THM-M-0947 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Roth's theorem. The repository
catalog supplies only the slogan "integer sets contain a three-term arithmetic progression,"
attributes it to Klaus Roth in 1953, and labels it `verified`. Under rev-5.6 that label is untrusted
metadata and gives no human-source or machine-proof credit.

The slogan omits the density or size hypothesis that distinguishes Roth's theorem from a false
claim about arbitrary integer sets. It also does not choose a finite, asymptotic-extremal, or
infinite formulation; define the ambient integers or interval convention; order the quantifiers;
or require a nonconstant progression. Selecting any familiar variant at intake would silently add
or substitute mathematics.

The bibliographic record for K. F. Roth's 1953 paper *On Certain Sets of Integers* was inspected as
a primary-source lead, but the paper body, exact theorem and definitions, proof boundary, and errata
were not available for reviewed transcription. The provisional root vector is `[H1, M3, R4]`:
`H1` records that source-reconstruction debt; `M3` records that pinned mathlib contains direct
finite and asymptotic Roth-family declarations but no source-identical canonical target has been
selected or audited; and `R4` records that no source-faithful proof reconstruction can attach before
the target is frozen.

`IntakeProbe.lean` checks those pinned declarations and reports their axioms only as discovery
evidence. The scope boundary is in `scope-map.md`, the source and statement mapping is in
`source-statement-crosswalk.md`, and all six downstream phases remain open in `task-dag.json`.

No canonical Lean proposition, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
