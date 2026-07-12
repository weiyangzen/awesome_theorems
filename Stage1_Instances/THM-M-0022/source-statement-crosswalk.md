# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:177-182` is the complete repository source record. It gives the
title `赫克特征标定理`, Erich Hecke, 1917, the gloss `关于L-函数的函数方程`, importance `高`, and
status `已验证`. All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; no citation or formula accompanies them.

`Docs/Stage0_Blueprint.md:717-742` projects the same record and marks exact definitions and
premises, proof, dependencies, equivalent statements, axioms, classical-choice use, machine
status, and artifact links as `待补充`. The manifest deliberately carries `已验证` only as
`source_status_untrusted`. These records identify inventory provenance, not an exact proposition,
primary source, `H0` proof, or machine theorem.

## Primary-source status

No immutable primary edition, exact theorem/page passage, incorporated definition chain,
transcription, translation review, errata search, or independent reviewer is accepted for this
target. Two bibliographic discovery leads are recorded by the separate `THM-M-0426` intake:

- Erich Hecke, *Eine neue Art von Zetafunktionen und ihre Beziehungen zur Verteilung der
  Primzahlen*, *Mathematische Zeitschrift* 1 (1918), 357-376. The separate intake associates DOI
  `10.1007/BF01203828` with this paper, but Crossref identifies that DOI as Nonogaki et al.,
  "Effects of superoxide dismutase on mouse in vitro fertilization and embryo culture system,"
  *Journal of Assisted Reproduction and Genetics* 9 (1992), 274-280; it is an erroneous legacy
  locator, not a competing Hecke source. A fresh Crossref title query instead returned
  `10.1007/BF01465095` for volume 1,
  pages 357-376, and `10.1007/BF01202991` for a 1920 continuation in volume 6, pages 11-51. That
  metadata query supplied no theorem text, and neither DOI record is admitted as this target;
- John Tate, *Fourier Analysis in Number Fields and Hecke's Zeta-Functions*, in Cassels and
  Froehlich (eds.), *Algebraic Number Theory* (1967), 305-347.

An open GDZ scan of the 1918 paper was inspected as source-family discovery. The stable article
locator is `http://resolver.sub.uni-goettingen.de/purl?GDZPPN002364182`; the observed 1,212,494-byte
PDF has SHA-256 `9709ad2c5cc05a663bf1d49d82f9f8d66a92d02f5cc06e5cd5795c8ca307dd9e`.
Section 4 begins on journal page 368 and is titled "Das analytische Verhalten der Zetafunktionen
mit Charakteren und ihre Funktionalgleichung." Journal page 370, around displayed equation (21),
states an entire-function and functional-equation result subject to nontriviality and proper
character conditions. Pages 368-370 also fix gamma and conductor/discriminant normalization data.

This is a precise historical theorem-family candidate, not an accepted crosswalk. The scan was
visually inspected but its OCR is noisy; exact symbols, all incorporated definitions from earlier
sections, hypotheses, translation, proof boundary, corrections, and the relationship to
`THM-M-0426` require independent verification. The scan's use terms also preclude treating a copied
PDF as an unrestricted repository artifact, so only its locator, size, and observed hash are
recorded. The paper ends "Basel, Februar 1918" and records receipt on 14 February 1918, so the
catalogue's 1917 date conflicts even with the candidate paper's internal dating and remains
unreconciled. A source
locator and preliminary passage by themselves cannot establish `H0`.

## Claim crosswalk

| Catalogue component | Mathematical choice still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Hecke character" | ideal/ray-class versus idele-class definition; finite-order, unitary, algebraic, or general quasicharacter | a future concrete character type with continuity, quotient, conductor, infinity-type, dual, and primitivity data | family recognized; object and character class open |
| "L-functions" | Euler factors, bad places, convergence region, analytic continuation, gamma factors, and completion | future concrete Hecke L-function construction; `WeakFEPair`/`StrongFEPair` are only generic analytic machinery | no exact analytic object selected |
| "functional equation" | reflection center, dual/conjugate, conductor exponent, epsilon/root number, equality domain, and polar cases | future expression over the constructed completion | conclusion and normalization open |
| Hecke / 1917 | historical identity | immutable publication and exact passage with a reviewed translation | bibliographic metadata only |
| `已验证` | claimed prior formal status | accepted kernel receipt for the exact expression | explicitly untrusted; no credit |

## Neighboring-target identity

`Docs/researches/math_theorems.md:3117-3122` separately records `THM-M-0426`, "the functional
equation for Hecke characters," with the gloss "the functional equation of Hecke L-functions,"
the same author, year, importance, and status. Different Chinese wording prevented exact-record
deduplication, but it does not prove mathematical distinctness. No source-statement partition,
alias, or canonical-root ownership decision is accepted.

The sibling's legacy `S1_M_080.lean` module expressly says its checked `StatementShape` is an
abstract boundary rather than a terminal theorem. Its user-supplied fields cannot serve as a
source-faithful alternate encoding or proof. Neither that module nor the sibling intake is imported
or credited here.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks:

- `WeakFEPair.functional_equation` and `StrongFEPair.functional_equation`, generic
  Mellin-transform functional-equation machinery;
- `DirichletCharacter.IsPrimitive.completedLFunction_one_sub`, a concrete special case for
  primitive Dirichlet characters;
- `NumberField.AdeleRing` and `NumberField.prod_abs_eq_one`, adjacent number-field
  infrastructure.

A bounded exact-topic search found no concrete `HeckeCharacter`, Hecke L-function, or idele-class
character declaration in pinned mathlib. This is intake discovery, not the later exhaustive anchor
audit or a global absence claim. The APIs do not select the source theorem and do not earn `M0` or
special-case credit for the general root.

Before source acceptance, an independent reviewer must pin a lawful source edition, identify the
exact theorem and every incorporated definition, map all ordered binders, hypotheses, normalizations,
boundary cases, conclusion, proof dependency, and erratum, resolve the `THM-M-0426` identity, and
approve the mapping. Only afterward may the statement phase freeze minimal imports, an elaborated
expression and environment fingerprint, checked transports, and the required mutations.
