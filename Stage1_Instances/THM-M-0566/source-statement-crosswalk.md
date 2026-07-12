# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` supply only a name, Pontryagin
attribution, the year 1942, and the gloss "integral characteristic classes of real vector bundles."
The rev-5.6 manifest repeats that metadata with an explicitly untrusted source status. None gives a
theorem number, page, assumptions, definitions, proof, or errata record.

## Bibliographic discovery anchors

- L. S. Pontryagin, "Characteristic cycles on differentiable manifolds," *Matematicheskii Sbornik*
  (N.S.) 21(63) (1947), 233-284. This is a historical primary-source candidate. Its exact language,
  indexing, target object, theorem/page, and relation to the repository's date have not been
  inspected here.
- John W. Milnor and James D. Stasheff, *Characteristic Classes*, Annals of Mathematics Studies 76,
  Princeton University Press (1974), the chapter on Pontryagin classes. This is a modern secondary
  source candidate for definitions and properties, not a primary-source substitute and not yet a
  pinpoint statement citation.

These entries are discovery anchors only. They do not establish `H0`; the statement phase must
inspect a stable edition, check errata, and obtain independent review.

## Crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Pontryagin characteristic classes" | a graded family `p_i`, total class `p`, or a property theorem | one selected declaration with an exact `Prop` conclusion | family identified; proposition open |
| "real vector bundles" | a real bundle `E -> X` in a specified category | concrete real vector-bundle object and base hypotheses | included; category and hypotheses open |
| "integral" | coefficients in `Z`, not merely rational de Rham classes | integral cohomology groups/ring and coefficient maps | included; cohomology model open |
| degree `4i` | `p_i(E) in H^(4i)(X; Z)` | grading and natural-number index convention | candidate; source convention open |
| complexification formula | `(-1)^i c_(2i)(E tensor C)` | complexification, Chern class, sign action, equality | candidate construction; not selected conclusion |
| characteristic | pullback naturality and often sum/product behavior | pullback maps and/or cup-product theorem | possible theorem family; exact property open |

## Formal boundary

A bounded repository search found historical generic mentions in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_118.lean`, whose own audit says the checked
Pontryagin APIs concern duality rather than characteristic classes and records the relevant class
API as missing. That file belongs to another legacy target and supplies no proof credit here. No
target-specific Lean artifact for `THM-M-0566` was found. A complete pinned-library and external
candidate audit belongs to `S56-M-0566-ANCHOR_AUDIT`, after the exact proposition is frozen.
