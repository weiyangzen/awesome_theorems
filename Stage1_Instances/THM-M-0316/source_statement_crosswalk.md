# Source-statement crosswalk

## Repository source

| Claim component | Repository anchor | Intake assessment |
|---|---|---|
| Theorem identity | `Docs/Stage1_Targets_rev-5.6.json`: `THM-M-0316`, "Riesz-Schauder theory" | Manifest membership and name are authoritative, not mathematical proof evidence |
| Supplied statement | `Docs/researches/math_theorems.md`: "spectral theory of compact operators" | Too broad to determine one exact proposition |
| Supplied status | `source_status_untrusted = 已验证` | Metadata only; it supplies no source, kernel, or acceptance receipt |

## Mathematical source discovery

| Candidate component | Discovery anchor | Mapping state |
|---|---|---|
| Compact-operator spectral theory | F. Riesz, *Über lineare Funktionalgleichungen*, Acta Mathematica 41 (1918), 71-98 | Historical primary-source candidate; exact theorem/page, terminology transport, edition hash, and errata review remain open |
| Completely continuous operator theory and adjoint/Fredholm results | J. Schauder, *Über lineare, vollstetige Funktionaloperationen*, Studia Mathematica 2 (1930), 183-196 | Historical primary-source candidate; exact clause mapping and assumptions remain open |
| Modern theorem-family formulation | T. Kato, *Perturbation Theory for Linear Operators*, Springer, Chapter III, compact-operator spectral theory | Secondary discovery anchor only; edition, theorem numbers, and clause-level mapping remain open |

These citations identify a credible genealogy but do not establish `H0`. In particular, this intake
has not verified scans against bibliographic records, pinned immutable copies, located corrections,
or mapped every hypothesis and conclusion to stable proof nodes.

## Lean candidate crosswalk

The repo-local pinned mathlib source at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the following discovery candidates:

| Provisional clause | Module and declaration | Relationship | Intake credit |
|---|---|---|---|
| `RS-SPEC` | `Mathlib.Analysis.Normed.Operator.FredholmAlternative`; `IsCompactOperator.hasEigenvalue_iff_mem_spectrum` | States that a nonzero scalar is an eigenvalue iff it lies in the spectrum for a compact operator on a complete normed space | Candidate only; exact type elaboration and trust audit belong to later phases |
| `RS-FRED` | Same module; `IsCompactOperator.hasEigenvalue_or_mem_resolventSet` | Fredholm alternative at a nonzero scalar | Related candidate, not evidence that it belongs to the root |
| `RS-FDIM` | `Mathlib.Analysis.InnerProductSpace.Spectrum`; `IsCompactOperator.finite_dimensional_eigenspace` | Finite-dimensional eigenspace in an inner-product/self-adjoint development | Restricted candidate; cannot discharge the general Banach-space clause without an exact scope decision |
| `RS-ACC` | No exact declaration located during bounded intake search | Needed for the zero-only accumulation clause | Open formal discovery |

No declaration is accepted or counted as machine closure here. The statement phase must first select
the exact human root, then elaborate it under minimal pinned imports and check all credited
relationships. The anchor-audit phase must separately inspect declaration bodies, axioms,
transitive provenance, and scope compatibility.

## First failed gate

The first unavailable gate is exact-statement identity: the repository wording does not decide
which Riesz-Schauder clauses form the root. Retry after a primary-source audit records immutable
artifacts, theorem/page anchors, scalar and completeness assumptions, exact conclusions, errata,
and an independent clause-selection review.
