# THM-M-0944 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the
Balog-Szemeredi-Gowers theorem. The repository catalog supplies the theorem
name, attributes it to Balog, Szemeredi, and Gowers, gives 1994, and describes
it only as "the Freiman theorem for approximate groups." Its inherited
`verified` label is untrusted metadata under rev-5.6.

That gloss is not an exact BSG statement. Standard BSG formulations turn
large additive energy, or many edges with few restricted sums, into large
subsets having a small full sumset. Freiman structure theorems and approximate
group results are neighboring consequences or later structure theory, not
interchangeable statements. The catalog does not choose an energy or graph
form, one or two input sets, an ambient group, parameter ranges, quantitative
bounds, or boundary cases. Selecting a familiar form at intake would silently
replace missing mathematics.

The 1994 Balog-Szemeredi paper is identified bibliographically, but an exact
theorem passage was not accessible and admitted for review. A later arXiv
paper gives a precise secondary restatement of a Gowers refinement; it is a
source lead, not the catalog's accepted claim. The exact source statement,
incorporated definitions, relationship among variants, proof boundary,
corrections, errata, and independent review remain open.

`IntakeProbe.lean` checks only pinned additive-energy, doubling-constant,
approximate-subgroup, and Ruzsa-covering interfaces. It declares no target
theorem and supplies no BSG proof. The provisional root vector is
`[H1, M4, R4]`; every downstream task remains open. No canonical proposition,
exact Lean expression, H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
