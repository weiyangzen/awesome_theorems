# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1738-1743` supplies exactly the title `黎曼-希尔伯特问题`,
Bernhard Riemann/David Hilbert, 1900, the gloss `单值群与微分方程`, importance "high," and
status `已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula,
definition, theorem statement, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md` repeats those fields and explicitly leaves the formal system, precise
definitions and premises, proof history and dependencies, equivalent forms, axioms, machine state,
and artifact links open. Its generic tree and leaf-budget language is planning metadata, not
theorem evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `黎曼-希尔伯特问题` | historical inverse-monodromy or realization problem | exact relation between monodromy data and a differential system/connection | family identified; variant open |
| `单值群` | monodromy group, representation, generators, or conjugacy data | `FundamentalGroup` representation into `Matrix.GeneralLinearGroup`, with basepoint and equivalence | rank and data convention open |
| `微分方程` | complex linear scalar equation, matrix system, or flat meromorphic/logarithmic connection | concrete coefficient, bundle, connection, horizontal transport, and monodromy APIs | model and regularity open |
| historical problem | existence or obstruction for prescribed monodromy | exact existential, restricted, classification, or counterexample `Prop` | no conclusion selected |
| Riemann/Hilbert, 1900 | historical provenance | pinpoint editions and source-to-node mapping | no proof-source credit |
| `已验证` | untrusted inventory metadata | inspectable human proof and kernel receipt would be required | no H or M credit |

## Inspected discovery source

The AMS-hosted English publication David Hilbert, *Mathematical problems*, *Bulletin of the
American Mathematical Society* 8(10) (1902), pages 437-479, DOI
`10.1090/S0002-9904-1902-00923-3`, was inspected at printed pages 470-471. Problem 21 asks for a
linear differential equation of the Fuchsian class with given singular points and prescribed
monodromic group, describes `n` functions with finite-order singularities and prescribed linear
substitutions, and notes a then-known special case. This pins a historical problem formulation but
does not establish which theorem or later corrected variant the repository intends, nor a complete
accepted proof. The PDF SHA-256 is recorded in `instance.json` and the provisional receipt.

This is discovery evidence, not H0: the German original and translation relationship, incorporated
definitions, later proof sources, correction history, and a complete assumption-to-target mapping
have not been independently reviewed.

## Correction and proof-source candidates

Plemelj's early work is a candidate source for a positive solution route. A. A. Bolibrukh,
*The Riemann-Hilbert problem*, *Russian Mathematical Surveys* 45(2) (1990), pages 1-58, DOI
`10.1070/RM1990v045n02ABEH002350`, is a candidate correction/counterexample source. Only Crossref
metadata for the Bolibrukh work was checked here; its theorem text, hypotheses, exact pages, proofs,
and errata were not inspected. Neither candidate receives H credit at intake.

## Neighbor and duplicate boundary

The separate `THM-M-0242` record names Hilbert's twenty-first problem and the Fuchsian-equation
monodromy gloss. The separate `THM-M-1559` record uses an integrable-systems gloss, and its legacy
Lean module encodes an operator-valued contour jump problem rather than monodromy realization.
These records confirm ambiguity and overlap; they do not authorize cross-target statement or proof
credit. This dossier remains independently scoped to `THM-M-0241`.

## Source gate

Before H0 or statement acceptance, accountable reviewers must preserve immutable primary editions,
select the exact positive, restricted, obstruction, or counterexample proposition, transcribe all
definitions, ordered binders, hypotheses, conclusions, and exceptional cases, map every material
premise and proof transition, inspect corrections and errata, reconcile duplicate targets, and
approve the source-to-Lean crosswalk. Until then the canonical statement and expression remain null.
