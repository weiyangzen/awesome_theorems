# THM-M-1468 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10714-10719` supplies exactly the title `hp有限元`, attribution
`Barna Szabo/Ivo Babuska`, year 1986, gloss `h-细化和p-升阶`, importance "high," and status
`已验证`. All six uncited fields entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, binder, hypothesis, conclusion, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:39919-39944` repeats the gloss while explicitly leaving the target formal
system, foundation, background, exact definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Source-family leads, not credited sources

Crossref and NUMDAM identify I. Babuska and Manil Suri, *The h-p version of the finite
element method with quasiuniform meshes*, technical report DOI `10.21236/ADA170144` (1986) and
journal version in *ESAIM: Mathematical Modelling and Numerical Analysis* 21(2) (1987), pages
199-238, DOI `10.1051/m2an/1987210201991`. This is a strong topical and date lead, but its authors
do not match the catalog pair. The journal work also contains multiple approximation and finite-
element error results, including separate regular and singular-solution regimes, rather than one
unambiguous target selected by the catalog gloss.

The 41-page NUMDAM journal PDF was inspected as a source-family lead. Its SHA-256 is
`0f7272597535ec9836eb8c00a6171cba094418db9b692b7ff7525c4f5d867805` and its byte size is
`2447814`. The introduction distinguishes h-, p-, and combined hp-versions; Theorem 4.8 on printed
pages 212-213 gives one quasiuniform-mesh error result for a regular-solution regime, while Theorem
5.4 on printed pages 218-219 gives a separate result incorporating singular-solution behavior.
These pinpoint observations demonstrate, rather than eliminate, root ambiguity. Formula OCR is
not admitted as an exact transcription.

Crossref also identifies I. Babuska, B. A. Szabo, and I. N. Katz, *The p-Version of the Finite
Element Method*, *SIAM Journal on Numerical Analysis* 18(3) (1981), pages 515-545, DOI
`10.1137/0718033`. Its authorship better matches the catalog, but it is a p-version result, predates
1986, and does not by itself select a combined hp theorem.

These bibliographic and source-family leads are `E5` discovery evidence only. No lead is admitted
as the canonical source, and no complete premise/conclusion crosswalk, correction audit, or
independent approval is claimed. Inspecting candidate theorem passages cannot turn the catalog
method gloss into H0 or decide which passage it meant.

## Clause crosswalk

| Repository element | Mathematical component to select | Prospective Lean component | Intake result |
|---|---|---|---|
| `hp有限元` | one finite-element theorem using both h and p variation | concrete mesh-indexed finite-element spaces and one proposition | family recognized; theorem absent |
| `h-细化` | smaller cells under a specified refinement regime | mesh family, diameter function, refinement/nestedness and regularity predicates | all conventions absent |
| `p-升阶` | larger local polynomial degree under a specified enrichment regime | degree assignment and inclusion between element spaces | local/global policy and conformity absent |
| combined `hp` | a coupling of mesh geometry and degree | joint index/family and exact limiting regime | no coupling or quantifier order given |
| expected accuracy | best approximation, error, or convergence behavior | norm inequality or limiting proposition | conclusion, rate, constants, and norms absent |
| Szabo/Babuska / 1986 | historical metadata | immutable source edition and theorem/page | source identity conflicts with major leads |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no H or M credit |

## Neighbor and non-substitution boundary

Generic finite-element theory, ordinary Galerkin projection, spectral elements, adaptive FEM, and
a priori or a posteriori error estimates are separately cataloged nearby. They may become explicit
dependencies after a source is selected, but none may be substituted for this root. Likewise, the
ordinary polynomial inclusion `degreeLE_mono` is only a local algebraic analogue of p-enrichment;
it says nothing about element geometry, conformity, a variational solution, or an hp error rate.

## Source and statement gate

Before leaving `H5`, accountable reviewers must redirect the method label to one stable proposition,
preserve an immutable source edition, reconcile the attribution/year mismatch, and map every
definition, binder, hypothesis, constant, conclusion, and degenerate case with its theorem/page and
correction status. Independent source review is required.

Only then may the statement phase freeze minimal Lean imports, a canonical expression and
environment fingerprint, checked alternate transports, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Until then the canonical target,
obligation registry, discovery protocol, proof credit, and completion decisions remain open.
