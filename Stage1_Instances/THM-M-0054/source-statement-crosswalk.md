# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:405-410` supplies exactly the title "Perron-Frobenius theorem,"
the attribution Oskar Perron/Ferdinand Frobenius, the year 1907, the gloss `非负矩阵的谱性质`
(`spectral properties of nonnegative matrices`), importance `high`, and status `verified`. Git
history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:1591-1618` repeats the metadata but explicitly leaves exact definitions
and premises, proof route, dependencies, equivalent forms, axiom policy, machine-checked status,
and artifact links open. The rev-5.6 target manifest preserves `verified` only as untrusted metadata
and resets this target to `L0 / rework_required`.

The catalog contains no bibliography, theorem/page locator, matrix domain, ordered binders,
hypotheses, conclusion bundle, incorporated definitions, proof boundary, correction record, or
reviewer. Its gloss identifies a theorem family but not one stable proposition.

## Historical source leads

Crossref metadata identifies Oskar Perron's *Zur Theorie der Matrices*, *Mathematische Annalen*
64(2) (June 1907), pages 248-263, DOI `10.1007/BF01449896`. This is a credible primary historical
lead matching the catalog date. The article itself was not admitted as a repository-owned complete
edition: the publisher PDF request returned an HTML interstitial rather than a PDF. No exact result
passage, incorporated definition, premise/conclusion crosswalk, correction audit, or independent
review is credited.

The combined theorem name also refers to Ferdinand Frobenius's later extensions from positive to
nonnegative/irreducible matrices. The catalog does not identify a Frobenius paper, year, edition,
or result. Those sources must be located and reviewed rather than inferred from the compound name.

Pinned mathlib's irreducibility file cites Eugene Seneta, *Non-negative Matrices and Markov Chains*,
revised printing of the second edition (Springer, 2006). It pinpoints Definition 1.1 page 14 for
primitivity and Definition 1.6 page 18 for irreducibility, not a Perron-Frobenius spectral theorem.
This is a definition lead and formal-source provenance, not an admitted root proof source.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `nonnegative matrix` | arbitrary, irreducible, primitive, or strictly positive finite square matrix | `Matrix n n Real` plus entrywise order and optional `Matrix.IsIrreducible`/`IsPrimitive` | structural hypothesis not selected |
| `spectral properties` | root existence, eigenvector positivity, simplicity, dominance, strict dominance, or cyclic peripheral spectrum | matrix spectrum/eigenspace, spectral radius, multiplicity, coordinate order | conclusion bundle absent |
| Perron root | largest real eigenvalue, spectral radius, or characteristic root | checked bridge among real/complex spectrum and `spectralRadius` | representation absent |
| eigenvector | right or left; nonzero/nonnegative/positive; normalized or projective | `Module.End.HasEigenvector` or coordinate equation | orientation and normalization absent |
| simple | algebraic multiplicity one, eigenspace dimension one, or both | charpoly multiplicity and eigenspace finrank | meaning absent |
| dominant | `|lambda| <= rho` versus strict inequality off the Perron root | quantified complex/real spectral membership | strictness depends on variant |
| `verified` | untrusted inventory label | no Lean declaration or proof body | explicitly rejected as evidence |

## Scope discriminator from the duplicate record

`Docs/researches/physics_theorems.md:7610-7616` contains a different record, projected in Stage0 as
`THM-P-0887` and outside the mathematics-only rev-5.6 target set, with the positive-matrix statement `正矩阵的最大特征值是正且单的`
(`the largest eigenvalue of a positive matrix is positive and simple`) and date 1907/1912. This
narrower claim supports the positive-versus-nonnegative distinction but is not a source citation
and is not the `THM-M-0054` target. Its hypotheses and conclusion cannot be silently imported.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
checks `Matrix.IsIrreducible`, `Matrix.IsPrimitive`, the irreducibility/power equivalence, a
matrix/linear-map spectrum bridge, generic finite-dimensional eigenvalue existence, the spectral
radius, and generic spectral-radius attainment. A bounded case-insensitive search found no
Perron-Frobenius spectral theorem joining nonnegative matrices to these eigenvalue conclusions.
This is discovery only, not an exhaustive external-project audit or proof of absence.

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select an exact result
and proof boundary, transcribe every incorporated definition, ordered binder, hypothesis, and
conclusion clause, reconcile Perron's and Frobenius's contributions, audit corrections, and obtain
independent review. It must then freeze and mutation-test the same exact Lean expression. Until
then the canonical mathematical and Lean targets remain null and source classification remains
`H1`.
