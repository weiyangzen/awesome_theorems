# THM-M-0049 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the
Frobenius inequality. The repository attributes it to Ferdinand Frobenius in 1911, describes it
only as "an inequality of matrix ranks," and labels it verified. The label is untrusted inventory
metadata, not an exact source statement or machine-proof receipt.

## Planned boundary

The standard theorem family called the Frobenius rank inequality is a strong candidate reading:
for composable matrices `A`, `B`, and `C` over a field,
`rank (A * B) + rank (B * C) <= rank B + rank (A * B * C)`. An inspected immutable modern
source lead states precisely this formula and gives a quotient-space proof. It is not a source
cited by the catalog, is not the historical Frobenius source, and has not passed an assumption,
errata, attribution, translation, or independent-review gate. The intake therefore freezes this
reading only as a candidate family, not as the canonical mathematical claim.

The catalog omits the displayed inequality, coefficient domain, matrix shapes, multiplication
association, rank convention, and boundary cases. It could otherwise be confused with the
two-factor rank upper bounds, the Sylvester rank inequality, or unrelated inequalities bearing
Frobenius's name. Selecting any of them as the exact root at intake would invent missing
mathematics.

Pinned mathlib supplies matrix rank, two-factor rank monotonicity, linear-map composition rank,
rank-nullity, and a zero-product rank bound. `IntakeProbe.lean` authenticates those APIs and checks
one candidate triple-product proposition shape. No declaration named for, or documented as, the
full Frobenius triple-product rank inequality was found in the bounded repo-local and pinned-
mathlib search. The candidate shape is not a theorem declaration and carries no proof credit.

The provisional vector is `[H1, M3, R4]`: a complete modern proof lead is inspected but source
identity and fidelity are unaudited; adjacent pinned APIs and a candidate proposition shape
elaborate but no canonical target or root proof is credited; and no source-faithful readable
reconstruction exists. All six downstream tasks remain open. No accepted execution state, `H0`,
`M0`, `R0`, audit completion, theorem completion, or master acceptance is claimed.

