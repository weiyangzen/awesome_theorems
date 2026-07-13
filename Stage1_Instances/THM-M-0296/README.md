# THM-M-0296 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`里斯-索林插值定理` (Riesz-Thorin interpolation theorem). The repository attributes it to Marcel
Riesz and Thorvald Thorin in 1939, supplies only the gloss `算子的插值理论` (interpolation theory
for operators), and labels it verified. The label is untrusted inventory metadata, not a source
audit, exact proposition, or machine-proof receipt.

## Intake result

The title identifies the classical strong-type operator-interpolation family, but the gloss does
not specify source and target measure spaces, scalar field, operator domain, endpoint exponents,
endpoint norm bounds, interpolation parameter, reciprocal-exponent equations, intermediate norm
constant, extension semantics, or boundary cases. Those choices change the proposition. Intake
therefore records the recognized family without inventing a binder-complete theorem.

Bibliographic discovery identified Marcel Riesz's 1926 paper *Sur les maxima des formes
bilineaires et sur les fonctionnelles lineaires* and zbMATH records for G. O. Thorin's 1939
extension *An extension of a convexity theorem due to M. Riesz* as source leads. The full Thorin
source text and an exact statement/assumption/proof crosswalk were not admitted, and no correction
audit or independent source review was performed. The catalog's expanded personal name still
requires source review. These leads support provisional `H1`, not `H0`.

## Formal boundary

`IntakeProbe.lean` checks pinned `Lp`, `MemLp`, induced `Lp`-map, and Hadamard three-lines APIs. A
bounded exact-name search found no Riesz-Thorin declaration in repository-local Lean or pinned
mathlib. Hadamard three-lines is a likely analytic ingredient, not a substitute for the operator
interpolation theorem. The probe declares no target or proof body and is only intake discovery.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`; all six downstream tasks remain open. No exact statement, `H0`, `M0`, `R0`,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
