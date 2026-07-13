# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:2195-2200` supplies exactly the title
`弗里德里希斯不等式`, Kurt Friedrichs, 1929, the gloss `紧支集Sobolev函数的估计`, importance
`高`, and status `已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That commit is repository provenance, not a
mathematical source: the record contains no publication, edition, theorem, page, definition,
formula, premise, proof, correction, erratum, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:8440-8465` projects the record as `THM-M-0306`. It explicitly leaves
the formal system, logical foundation, precise definitions and premises, proof history and
dependencies, equivalent forms, logical principles, machine status, and artifact links open. Its
generic theorem-tree and leaf-budget text is planning metadata. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalogue component | Mathematical choice still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Friedrichs inequality | one exact historical or modern inequality rather than a name | one source-faithful `Prop`, with checked relationships to alternates | theorem family identified; root open |
| compact support | support in the ambient space, compact containment in a domain, or zero-trace closure | `HasCompactSupport`, support inclusion, or a reviewed zero-trace Sobolev encoding | exact condition and transports absent |
| Sobolev function | scalar field, domain, weak derivative, exponent, and function space | exact Sobolev model or checked smooth dense surrogate | no model selected |
| estimate | both operands, measures, exponents, norm convention, direction, and constant | `MeasureTheory.eLpNorm`, `fderiv`, weak gradient, or another exact encoding | formula absent |
| Kurt Friedrichs, 1929 | exact work, edition, statement, and genealogy | source provenance only | catalogue date conflicts with a strong secondary lead |
| `已验证` | claimed formal status | kernel declaration and accepted receipt would be required | explicitly rejected as evidence |

## Duplicate crosswalk

The research corpus repeats the same attribution, year, gloss, importance, and untrusted status at
`Docs/researches/math_theorems.md:9073-9078`, spelling the title `Friedrichs不等式` and placing it
under PDE. The generator retains that record as `THM-M-1240`. Exact title spelling and category
created separate catalogue identities, but this technical origin does not prove the mathematical
targets distinct. Master/source review must approve a distinction, alias/deduplication rule, or
correction before either target can share source or proof-body ownership. The older
`THM-M-1240` intake is discovery material only and transfers no state or evidence.

## Historical source discovery

The *Encyclopedia of Mathematics* entry `Friedrichs inequality`, revision 46991, was inspected as
a secondary source-family discriminator. It states a modern `W_2^1` boundary-term inequality on a
bounded Euclidean domain with locally Lipschitz boundary and says that Friedrichs obtained a
two-dimensional `C^2` version. Its reference [1] is K. O. Friedrichs, *Eine invariante Formulierung
des Newtonschen Gravitationsgesetzes und des Grenzueberganges vom Einsteinschen zum Newtonschen
Gesetz*, *Mathematische Annalen* 98, pages 566-575.

Springer metadata and the Goettingen Digitalisation Centre volume scan identify that article as
Kurt Friedrichs, DOI `10.1007/BF01451608`, issue date March 1928, received 16 November 1926.
Inspection of scanned pages 566-575 shows a gravitation paper, not an evident Sobolev inequality
statement. This conflicts with both the catalogue's 1929 date and the secondary entry's attribution
path. It is a source-integrity blocker, not a corrected citation adopted by this intake. The
secondary entry may contain a miscitation, the relevant inequality may be embedded under different
terminology, or the catalogue may intend another source; independent expert review must decide.

This discovery supports provisional `H1`, not `H0`. No exact primary theorem, incorporated
definition chain, assumption map, proof boundary, correction/errata decision, or independent
review is accepted. No temporary downloaded source was added to the repository.

Before `H0` or exact-statement acceptance, accountable reviewers must preserve a lawful immutable
primary edition; identify the theorem, section and page; resolve the 1926/1928/1929 chronology and
secondary-reference conflict; transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, exceptional case, support/trace condition, norm, exponent, and constant
dependency; resolve the duplicate target; and independently approve the source-to-Lean crosswalk.

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
imports `Mathlib.Analysis.FunctionalSpaces.SobolevInequality` and checks `eLpNorm`, `fderiv`,
`HasCompactSupport`, `eLpNorm_le_eLpNorm_fderiv_one`,
`eLpNorm_le_eLpNorm_fderiv_of_eq`, `eLpNorm_le_eLpNorm_fderiv_of_le`, and
`eLpNorm_le_eLpNorm_fderiv`. These declarations are explicitly Gagliardo-Nirenberg-Sobolev
results for concrete smooth/support models. They do not resolve the catalogue's source, domain,
support-versus-trace, or exponent ambiguity, and none is credited as the canonical root or as a
checked alternate transport.

The probe establishes only that adjacent pinned interfaces elaborate. A bounded exact-topic name
search located no declaration named Friedrichs in repository-local Lean or pinned mathlib. This is
not a global absence claim, an exhaustive external search, the downstream anchor audit, or proof
evidence. The root remains `[H1, M3, R4]` pending exact source selection.
