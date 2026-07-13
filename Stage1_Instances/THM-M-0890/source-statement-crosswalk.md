# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md:6516-6521` contains exactly the name `Hoffman bound`, Alan
Hoffman, 1970, the phrase `spectral upper bound for independent sets`, high importance, and an
untrusted `verified` label. All six uncited fields originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24278-24303` repeats the gloss while explicitly leaving precise
definitions and premises, proof route, dependency graph, equivalent formulations, axiom policy,
machine status, and artifact links open. Neither repository surface identifies a theorem number,
page, edition, proof, correction record, or formal artifact.

## Exact modern source lead

Willem H. Haemers, "Hoffman's ratio bound," *Linear Algebra and its Applications* 617 (2021),
215-219, DOI `10.1016/j.laa.2021.02.010`, is available as immutable arXiv version
`2102.05529v2`. The inspected five-page PDF has SHA-256
`e2a90698b4d6efa293cf0b486db422b94a6cecc2f9d8101e803b4a9cf0ec22bc`.

Section 2, Theorem 1 (journal pp. 215-216; arXiv pp. 1-2), fixes a simple graph `G` of order `n`,
adjacency matrix `A`, ordered eigenvalues `lambda_1 >= ... >= lambda_n`, independence number
`alpha`, and `k`-regularity, then concludes

```text
alpha <= n * (-lambda_n) / (k - lambda_n).
```

The proof uses the all-ones eigenvector, constructs a positive-semidefinite matrix, restricts it to
a principal submatrix indexed by a maximum independent set, and derives the inequality. The paper
also records equality information and later generalizations, which are distinct possible targets.

This is the statement phase's selected exact conventional target and proof-family discriminator,
not an accepted H0 packet.
The paper is a historical/modern reconstruction, not Hoffman's primary publication of the bound:
its abstract and Section 1 explicitly state that Hoffman did not publish the result. Section 3 says
that the 1970 paper *On Eigenvalues and Colorings of Graphs* is a wrong reference for the
independence-number bound, although it contains Hoffman's related chromatic bound. The catalog's
1970 field therefore requires correction and target-selection review rather than automatic source
credit. No independent source reviewer, correction/errata disposition, or accepted clause-to-Lean
transport exists yet.

## Clause crosswalk

| Repository or source phrase | Candidate mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `independent sets` | maximum cardinality `alpha` | `SimpleGraph.indepNum` | selected; every-independent-finset form remains an uncredited alternate |
| `spectral` | real eigenvalues of the symmetric adjacency matrix | `SimpleGraph.adjMatrix`, `SimpleGraph.isHermitian_adjMatrix`, `Matrix.IsHermitian.eigenvalues₀` | selected; least value is the last descending index |
| `upper bound` | `alpha <= n(-lambda_min)/(k-lambda_min)` | casted natural cardinality and real inequality | selected from Haemers Theorem 1 |
| `regular of degree k` | constant positive vertex degree | `SimpleGraph.IsRegularOfDegree` plus `0 < k` | regularity is source-explicit; positivity resolves the quotient's omitted edgeless boundary |
| `1970` | catalog provenance/attribution field | no Lean proposition | conflicts with modern history for this bound; review required |
| `verified` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Statement.lean`
elaborates the selected target from two minimal direct imports. `SimpleGraph.indepNum` supplies
`alpha`; the real adjacency matrix is Hermitian; its `eigenvalues₀` enumeration is antitone; and the
last valid index supplies `lambda_min`. A bounded search found no repo-local or pinned-mathlib
declaration named for Hoffman or the ratio bound. This closes the statement interface only; it is
not the downstream exhaustive anchor audit and supplies no proof.

## Required source acceptance work

The statement phase selects Haemers Theorem 1 and freezes and mutation-tests its Lean expression,
moving only the machine interface from `M4` to `M3`. The anchor/source audit must independently
review that choice; reconcile the catalog's attribution and year; approve the explicit positive-
degree treatment of the paper's zero-denominator omission; map source definitions, proof boundary,
corrections, equality material, and genealogy; and audit formal anchors. Until those later gates,
the root is only proposed as `H1/M3/R4`, with no source or proof closure credited.
