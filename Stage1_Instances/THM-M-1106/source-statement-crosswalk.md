# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` supplies the authors Marchenko/Pastur, the year 1967, and only the
phrase "eigenvalues of sample covariance matrices". `Docs/Stage0_Blueprint.md` repeats that phrase
while leaving definitions, assumptions, proof route, axioms, and formal artifacts unspecified. The
rev-5.6 manifest treats `已验证` as untrusted source metadata. These records identify a subject, not
an exact proposition.

## Primary-source candidate

- V. A. Marchenko and L. A. Pastur, "Distribution of eigenvalues for some sets of random matrices",
  *Mathematics of the USSR-Sbornik* 1 (1967), no. 4, 457-483; translated from the 1967 Russian
  original.

This bibliographic identification matches the repository authors and date. The original theorem
number, exact page span for the relevant statement, translation differences, complete assumptions,
and corrections or errata have not been independently inspected in this intake. It is therefore a
discovery anchor, not `H0`. A modern textbook formulation may clarify conventions but may not
silently replace the attributed result.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "sample covariance matrix" | normalized Gram matrix of rectangular random data | finite matrices, transpose/adjoint, scalar normalization | included; orientation and field open |
| "eigenvalues" | empirical measure of the covariance spectrum | eigenvalue multiset/counting measure with multiplicity | included; representation open |
| increasing sample size | two matrix dimensions diverge | indexed dimension sequences and limit hypotheses | required; indexing open |
| aspect ratio | dimension quotient tends to a positive parameter | real-valued ratio convergence and parameter bounds | required; reciprocal convention open |
| Marchenko-Pastur law | deterministic measure with parameterized density/support and possible zero atom | probability measure and exact formula | family identified; convention open |
| convergence | limiting spectral distribution | weak convergence plus almost-sure/in-probability quantification | exact mode open |
| Marchenko/Pastur, 1967 | original random-matrix result | source IDs mapped to each binder and premise | paper identified; locator/review open |
| `已验证` | repository screening label | accepted source review or kernel receipt | no credit |

## Non-equivalent conventions

If the empirical measure counts eigenvalues of the larger Gram matrix, forced zero eigenvalues can
produce an atom at zero; using the smaller Gram matrix changes that mass. Likewise, parameterizing
by rows divided by columns rather than columns divided by rows changes the displayed density and
atom formula. These are not cosmetic changes. They require an explicit checked transport after one
convention is made canonical.

## Required source and machine audit

Before `H0`, an independent reviewer must record an immutable source edition, exact theorem/page,
every premise and referenced definition, translation or errata status, and a row-by-row map to the
canonical Lean expression. No repo-local or external Lean declaration is credited at intake. The
anchor-audit phase must inspect pinned mathlib and credible Lean 4 projects and record exact module
and declaration types, revisions, proof-body provenance, placeholders, axioms, and dependency
feasibility. Matrix, eigenvalue, probability, or weak-convergence APIs alone do not constitute a
formalization of this limit law.
