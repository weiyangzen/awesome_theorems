# Source-statement crosswalk

## Repository source

The authoritative catalog record is `Docs/researches/math_theorems.md:10567-10572`:

| Catalog field | Literal value | Intake interpretation |
|---|---|---|
| name | `Cholesky分解` | recognizable theorem-family title only |
| attribution | `Andre-Louis Cholesky` | catalog metadata; not a proof citation |
| time | `1910` | catalog metadata; exact historical publication not supplied |
| statement | `对称正定矩阵的分解` | "decomposition of a symmetric positive-definite matrix"; not binder-complete |
| importance | `高` | scheduling metadata only |
| formal status | `已验证` | explicitly untrusted; no source or machine credit |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The current file has Git blob
`b78ec1f48495aa5747ef252665ab58e418d195e4`; the originating blob is
`5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf`. No later repository record adds a
bibliography, theorem locator, formula, assumptions, proof, errata decision, or reviewer.

The generated Stage0 projection at `Docs/Stage0_Blueprint.md:39352-39377` repeats the gloss and
explicitly leaves exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. It is not a second source.

## Claim-node crosswalk

| Required node | Source wording | Candidate mathematical meaning | Lean surface | Gate state |
|---|---|---|---|---|
| scalar/domain | `矩阵` | finite real square matrix, or complex square matrix | `Matrix n n R` | open |
| symmetry | `对称` | real transpose symmetry; possibly Hermitian in the complex variant | `Matrix.IsSymm` or `Matrix.IsHermitian` | open |
| positivity | `正定` | strict positivity of the quadratic or Hermitian form on nonzero vectors | `Matrix.PosDef` | adjacent definition located; mapping open |
| factor witness | `分解` | lower `L` or upper `U` | matrix existential witness | open |
| triangularity | implicit | lower or upper triangular under an ordered finite index | a source-selected triangular predicate | open |
| product identity | implicit | `A=L*Lᵀ`, `A=L*Lᴴ`, `A=Uᵀ*U`, or `A=Uᴴ*U` | exact matrix equality | open |
| diagonal condition | absent | positive diagonal commonly normalizes the factor | pointwise strict positivity | open |
| uniqueness | absent | unique normalized factor, or existence only | equality of witnesses | open |
| boundary cases | absent | empty and singleton indices; singular/semidefinite exclusion | explicit source-mapped cases | open |

No row is admitted as canonical merely because it is conventional. A later statement phase must
select an immutable approved source, map every incorporated definition and row, audit corrections,
and obtain independent source review before elaborating an exact target.

## Inspected source lead

The Netlib LAPACK Users' Guide, section 2.3.4, "Computational Routines", was inspected at
`https://www.netlib.org/lapack/lug/node38.html` on 2026-07-13. The observed HTML had SHA-256
`f81af691fc5fa08f7f2e9a93943d03d3ad530c30c1f406c227208cd1a7039621`. Its matrix-factorization
survey treats symmetric and Hermitian positive-definite matrices by Cholesky factorization and
distinguishes upper and lower triangular factors. This is an authoritative source lead for the
family and an ambiguity witness, not H0: it is not cited by the catalog, does not settle every
canonical mathematical and boundary convention, has no accepted preservation packet, and has not
received independent source-fidelity review.

## Pinned Lean boundary

Pinned mathlib module `Mathlib.LinearAlgebra.Matrix.PosDef` defines `Matrix.PosDef` and supplies
`Matrix.PosDef.isHermitian`, `Matrix.PosDef.diag_pos`, `Matrix.PosDef.isUnit`,
`Matrix.posDef_iff_dotProduct_mulVec`, and factor-to-positive-definite results. Module
`Mathlib.Analysis.InnerProductSpace.GramMatrix` supplies positive-definiteness/linear-independence
facts for Gram matrices. These are ingredients and converse-direction checks, not an exact
Cholesky factor-existence theorem.

Pinned `Mathlib.Analysis.Matrix.LDL` constructs `LDL.lower hS` and the diagonal
`LDL.diag hS`, with `LDL.lower_conj_diag` proving `L * D * Lᴴ = S`. The module TODO says that
lower-triangularity of `LDL.lower` still needs to be proved from `LDL.lowerInv_triangular`; it also
does not absorb square roots of the diagonal into a positive-diagonal triangular factor or prove
the source-selected uniqueness clause. It is a close formal lead, not an exact Cholesky theorem.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no Cholesky-named or
source-identical `LLᴴ` factor-existence declaration. This limited intake search is not the downstream
immutable exhaustive anchor audit and cannot establish global absence.

## Debt boundary

The provisional source debt is `H1`: the classical theorem family and an authoritative source lead
are identifiable, but no catalog-cited, pinpoint, fully mapped, errata-audited, independently
reviewed exact proposition exists. Machine debt is `M4`: adjacent infrastructure is present but no
source-identical usable formal artifact is credited. Readability debt is `R4`: this dossier maps the
missing statement boundary but reconstructs no source-faithful proof.
