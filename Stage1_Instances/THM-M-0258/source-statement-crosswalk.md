# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1857-1862` supplies exactly the title `沃尔夫-登乔定理`, the
attribution Hartmut Wolf/Ken'ichi Ohshika, the year 1990, the gloss `泰希米勒空间的边界`
("boundary of Teichmuller space"), importance "high," and status `已验证`. Git blame attributes
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, exact theorem, definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7139-7164` repeats that tuple while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Its generic planning language is not source evidence. The
rev-5.6 manifest preserves `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Identity mismatch

The received fields do not jointly select a known theorem statement:

| Catalog field | Candidate reading | Missing decision | Intake status |
|---|---|---|---|
| `沃尔夫-登乔定理` | a transposed rendering of the classical Denjoy-Wolff theorem | exact historical source, unit-disc or hyperbolic-domain version, fixed-point assumptions, iterate convergence conclusion | name resemblance only; attribution and gloss conflict |
| Hartmut Wolf / Ken'ichi Ohshika | an unspecified result associated with Teichmuller or Kleinian geometry | correct author identities, joint or separate source, theorem locator, date, definitions, assumptions, and conclusion | uncited metadata only |
| 1990 | publication or result date | source work and edition corresponding to that date | no locator supplied |
| boundary of Teichmuller space | Thurston, Bers, Gardiner-Masur, Weil-Petersson, horofunction, or another boundary/compactification | surface type, boundary construction, topology, embedding, equivalence, and theorem asserted | object/topic gloss, not a proposition |
| `已验证` | inventory label | reviewed human proof and kernel receipt | no H or M credit |

The standard Denjoy-Wolff family concerns holomorphic dynamics, not by its name alone a theorem
about a boundary of Teichmuller space. Conversely, many inequivalent compactifications and boundary
theorems exist in Teichmuller theory. No source in the repository authorizes identifying the target
with either family or joining them into a new statement.

## Bibliographic discovery boundary

Crossref metadata was queried only to test the catalog identity. It returned Michael Wolf's
*The Teichmuller theory of harmonic maps*, Journal of Differential Geometry 29 (1989), DOI
`10.4310/jdg/1214442885`, and *High energy degeneration of harmonic maps between surfaces and rays
in Teichmuller space*, Topology 30(4) (1991), 517-540, DOI
`10.1016/0040-9383(91)90037-5`. It also returned Ken'ichi Ohshika's *Ending Laminations and
Boundaries for Deformation Spaces of Kleinian Groups*, Journal of the London Mathematical Society
s2-42(1) (1990), 111-121, DOI `10.1112/jlms/s2-42.1.111`. These records show three nearby but
distinct identity components; they do not establish a joint Wolf/Ohshika theorem, corroborate the
name Hartmut Wolf, or connect the Denjoy-Wolff label to the boundary gloss. No primary text,
theorem/page, definitions, premises, proof, correction record, or independent review was inspected
or credited. These are identity-warning leads only, not H0 evidence.

## Prospective formal crosswalk

| Required mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|
| holomorphic self-map reading | `Complex.UnitDisc`, differentiability/analyticity, iteration, topology and limits | generic unit-disc and Schwarz APIs exist; no target reading selected |
| Teichmuller-space reading | marked finite-type Riemann surfaces, quasiconformal equivalence, moduli/metric structure | no source-selected types, definitions, or root proposition |
| boundary reading | a chosen compactification, embedding, boundary subset, topology, and convergence relation | generic `OnePoint` is not a Teichmuller compactification and is not a substitute |
| theorem conclusion | fixed point, convergence, homeomorphism, identification, compactness, classification, or another sourced result | wholly open |

A bounded search of repo-local Lean and pinned mathlib found no exact Denjoy-Wolff or
Teichmuller-space-boundary declaration. The probe checks adjacent generic interfaces only. This is
intake discovery, not the later immutable anchor audit and not a global absence theorem.

## Source gate

Before ordinary statement execution, accountable reviewers must correct and independently approve
the target identity, preserve an immutable primary or authoritative source, select one exact
theorem and incorporated definitions, map every domain, binder, hypothesis, conclusion, and
boundary case, and audit attribution, date, translations, corrections, and errata. Only then may
the statement phase freeze and mutation-test a canonical Lean expression. Until then the received
catalog target remains provisionally `H5`, with machine and readability debt `M4` and `R4`.
