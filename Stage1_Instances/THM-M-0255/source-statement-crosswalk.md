# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1836-1841` supplies exactly the title `拟共形映射理论`, Lars
Ahlfors, 1935, the gloss `拟共形映射的存在性与唯一性` ("existence and uniqueness of
quasiconformal mappings"), importance "high," and status `已验证`. Git blame attributes all six
uncited lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no bibliographic source, definitions, domains, ordered hypotheses, normalization,
conclusion, proof boundary, or formal artifact.

`Docs/Stage0_Blueprint.md:7058-7083` repeats the gloss while explicitly leaving the target formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its generated planning language is not
source evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Crossref identifies Lars Ahlfors, *Zur Theorie der Uberlagerungsflachen*, *Acta Mathematica* 65
(1935), pages 157-194, DOI `10.1007/BF02420945`. This matches the catalog's author and year, but
the title metadata does not establish that it is the intended quasiconformal existence-and-
uniqueness source.

Crossref also identifies Lars V. Ahlfors, *On quasiconformal mappings*, *Journal d'Analyse
Mathematique* 3 (1953), pages 1-58, DOI `10.1007/BF02803585`, and a correction at pages 207-208,
DOI `10.1007/BF02803589`. These records strengthen the identity, date, variant, and correction
ambiguity. They are bibliographic discovery leads only: no immutable primary text, theorem/page
locator within either work, definition chain, exact assumptions, proof boundary, or correction
impact was inspected or independently accepted. They supply no H0 credit and select no root.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `拟共形映射理论` | select one theorem rather than an umbrella theory | one exact canonical `Prop` | topic label only; root open |
| Lars Ahlfors / 1935 | identify the intended primary work and reconcile later literature and corrections | immutable source identity and version | no catalog citation; source leads unadmitted |
| `拟共形映射` | fix source definition and its domain/codomain and regularity | explicit map type, structures, predicates, universes, and binders | all choices absent |
| `存在性` | specify input data and the exact map or solution produced | existential conclusion with every witness property | input and witness clauses absent |
| `唯一性` | fix normalization or conformal equivalence and equality convention | exact uniqueness quantifiers and relation | normalization and relation absent |
| Beltrami reading | decide coefficient space, norm bound, a.e. equation, orientation, and global/local domain | measurable coefficient, derivative/equation predicates, null-set conventions | not named by the catalog |
| extremal reading | decide surfaces, markings, homotopy class, distortion, and extremality | surface and marking types plus minimization and uniqueness clauses | not named by the catalog |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Candidate readings and conflicts

A normalized measurable Riemann mapping theorem, a Teichmuller extremal mapping theorem, an
extension theorem, and an equivalence-of-definitions theorem are not interchangeable. Unnormalized
solutions commonly have conformal postcomposition freedom, so the bare word "uniqueness" cannot
be encoded without inventing a normalization or equivalence relation. Selecting an extremal or
deformation result may also absorb neighboring targets `THM-M-0256` and `THM-M-0257`.

## Required source correction

Before statement work, an accountable reviewer must approve one exact primary-source theorem and
immutable edition, pinpoint its theorem and incorporated definition locators, map every domain
restriction, binder, premise, normalization, conclusion, and dependent source node, inspect all
corrections and errata, reconcile the catalog's author/year with the selected result, and obtain an
independent crosswalk review. Only then may the statement phase encode and mutation-test a
canonical Lean expression. Until that correction, the catalog target is provisionally `H5`, while
machine and readability states remain `M4` and `R4`.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the API-only probe
checks generic homeomorphism, conformal-map, conformal-at-a-point, and conformal-groupoid surfaces.
A bounded exact-topic search found no quasiconformal, Beltrami-coefficient, measurable-Riemann-
mapping, or Ahlfors-Bers target. These checks neither elaborate a canonical target nor supply proof
evidence.
