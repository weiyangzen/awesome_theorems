# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:2188-2193` supplies exactly the title `庞加莱不等式`, Henri
Poincare, 1890, the gloss `Sobolev函数的L^p估计`, importance `高`, and status `已验证`.
All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That commit is repository provenance, not a
mathematical source: the record contains no work, edition, theorem, page, definition, formula,
premise, proof, correction, erratum, or formal artifact.

`Docs/Stage0_Blueprint.md:8413-8437` projects the record as `THM-M-0305`. It explicitly leaves
precise definitions and premises, proof history and dependencies, equivalent forms, axioms,
machine status, and artifact links open. Its generic theorem-tree and leaf-budget text is planning
metadata. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

## Literal crosswalk

| Catalogue component | Mathematical choice still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Poincare inequality | one exact analytic inequality rather than a name | a source-faithful `Prop` with all definitions expanded or pinned | theorem family identified; root open |
| Sobolev function | exact scalar field, domain, weak derivatives, exponent, and function space | a reviewed Sobolev encoding or a checked dense smooth surrogate plus transports | no Sobolev model selected |
| `L^p` estimate | left/right functions, measures, exponents, norm convention, direction, and constant | `MeasureTheory.eLpNorm`/`MemLp` or another exact encoding | neither side is stated |
| normalization | mean subtraction, zero mean, zero trace, support, or quotient by constants | integral/average, trace, support, or quotient interfaces | absent from catalogue |
| domain | dimension, boundedness, connectedness, boundary regularity, and measure | a concrete set/domain and all required structures | absent from catalogue |
| Henri Poincare, 1890 | exact historical publication and statement genealogy | source provenance only | bibliographic lead, not H0 |
| `已验证` | claimed formal status | kernel declaration plus accepted receipt would be required | explicitly rejected as evidence |

## Duplicate and neighbor crosswalk

The research corpus repeats the same attribution, year, gloss, importance, and untrusted status at
`Docs/researches/math_theorems.md:9066-9071`, spelling the title `Poincaré不等式` and placing it
under PDE. The generator retains that record as `THM-M-1239`. Exact-name spelling is part of the
legacy deduplication signature, but this technical origin does not prove that the mathematical
targets are distinct. Master/source review must approve a distinction, alias/deduplication rule,
or correction before either target can share source or proof-body ownership.

The probability record `THM-M-0998` instead says `方差的上界` ("variance upper bound"). Its
legacy probability-facing predicates and finite-chain route do not identify this target. Similar
names, mathlib declarations, or another dossier's scope choices provide discovery leads only and
no transferred status.

## Historical source status

No theorem-level primary source is cited or accepted. A bibliographic search lead is H. Poincare,
*Sur les equations aux derivees partielles de la physique mathematique*, American Journal of
Mathematics 12(3) (1890), starting at page 211, DOI `10.2307/2369620`. This intake did not inspect
and admit an immutable source text, locate a particular theorem or inequality in it, establish
that it matches the modern Sobolev gloss, audit its assumptions or errata, or obtain independent
review. The citation is therefore an uncredited lead, not `E4` or `H0` evidence.

Before `H0` or exact-statement acceptance, accountable reviewers must preserve a lawful immutable
edition; identify the theorem, section and page; transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, exceptional case, normalization, and constant dependency;
map the historical statement to any modern Sobolev formulation; audit translation, corrections,
and errata; resolve the duplicate target; and independently approve the source-to-Lean crosswalk.

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
imports `Mathlib.Analysis.FunctionalSpaces.SobolevInequality` and checks `eLpNorm`, `fderiv`,
`eLpNorm_le_eLpNorm_fderiv_one`, `eLpNorm_le_eLpNorm_fderiv_of_eq`,
`eLpNorm_le_eLpNorm_fderiv_of_le`, and `eLpNorm_le_eLpNorm_fderiv`. Those declarations are
explicitly Gagliardo-Nirenberg-Sobolev results for concrete smooth/support models. They do not
resolve the catalogue's mean-zero versus zero-trace/support ambiguity, and none is credited as the
canonical root or as a checked alternate transport.

The probe establishes only that adjacent pinned statement interfaces elaborate. A bounded exact-
topic name search located no terminal PDE/real-analysis declaration named as the Poincare
inequality. This is not a global absence claim, an exhaustive external search, the downstream
anchor audit, or proof evidence. The root remains `[H1, M3, R4]` pending exact source selection.
