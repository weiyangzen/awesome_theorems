# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1745-1750` supplies exactly the title `希尔伯特第21问题`, David
Hilbert, 1900, the gloss `Fuchs方程的单值群`, importance "high," and status `已验证`. All six lines
entered the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, formula, incorporated definitions, theorem statement, proof, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:6707-6732` repeats those fields and explicitly leaves the formal system,
precise definitions and premises, proof history and dependencies, equivalent forms, axioms,
machine state, and artifact links open. Its generic tree and leaf-budget language is planning
metadata, not theorem evidence. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `希尔伯特第21问题` | historical prescribed-monodromy realization problem | exact relation between monodromy data and a differential equation, system, or connection | family identified; corrected variant open |
| `Fuchs方程` | scalar Fuchsian equation or first-order Fuchsian system, possibly contrasted with a regular-singular connection | concrete coefficient/system or bundle/connection API and regularity predicate | object and convention open |
| `单值群` | monodromy group, representation, generators, or conjugacy data | `FundamentalGroup` representation into `Matrix.GeneralLinearGroup`, with basepoint and equivalence | rank and data convention open |
| historical problem | existence for prescribed monodromy | exact existential, restricted, obstruction, classification, or counterexample `Prop` | no later true conclusion selected |
| David Hilbert, 1900 | historical provenance | pinpoint edition, translation relation, and source-to-node mapping | discovery source inspected; no proof-source credit |
| `已验证` | untrusted inventory metadata | inspectable human proof and kernel receipt would be required | no H or M credit |

## Inspected discovery source

The AMS-hosted English publication David Hilbert, *Mathematical problems*, *Bulletin of the
American Mathematical Society* 8(10) (1902), pages 437-479, DOI
`10.1090/S0002-9904-1902-00923-3`, was inspected at printed pages 470-471. Problem 21 asks to show
that a linear differential equation of the Fuchsian class always exists with given singular points
and monodromic group. It describes `n` functions regular off those points, of only finite-order
growth there, and undergoing prescribed linear substitutions around circuits. It also records only
a special case as rigorously proved at that time.

This source pins the historical problem family, but it does not establish the exact later corrected
theorem the repository intends. It is discovery evidence, not H0: the German original and
translation relation, incorporated definitions, later proof and counterexample sources, correction
history, and a complete assumption-to-target mapping have not been independently reviewed. The PDF
SHA-256 is recorded in `instance.json` and the provisional receipt.

## Correction and proof-source candidates

Plemelj's early work is a candidate positive-solution source. A. A. Bolibrukh, *The Riemann-Hilbert
problem*, *Russian Mathematical Surveys* 45(2) (1990), pages 1-58, DOI
`10.1070/RM1990v045n02ABEH002350`, is a candidate correction/counterexample source. Intake checked
only its Crossref metadata; its theorem text, hypotheses, exact pages, proofs, and errata were not
inspected. Neither candidate receives H credit.

## Neighbor and duplicate boundary

The separate `THM-M-0241` record names the Riemann-Hilbert problem using the broader gloss
"monodromy group and differential equations." The separate `THM-M-1559` record uses an
integrable-systems gloss and has a legacy operator-valued contour jump interface. These records
confirm ambiguity and overlap; they do not authorize cross-target statement or proof credit. This
dossier remains independently scoped to `THM-M-0242`.

## Source gate

Before H0 or statement acceptance, accountable reviewers must preserve immutable primary editions,
select one exact true positive, restricted, obstruction, classification, or counterexample
proposition, transcribe every incorporated definition, ordered binder, hypothesis, conclusion, and
exceptional case, map material premises and proof transitions, inspect corrections and errata,
reconcile duplicate targets, and approve the source-to-Lean crosswalk. Until then the canonical
statement and Lean expression remain null.
