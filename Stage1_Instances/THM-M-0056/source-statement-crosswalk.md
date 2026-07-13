# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:419-424` supplies exactly the Chinese title for Weyl's inequality,
Hermann Weyl, 1912, the gloss "perturbation theory for eigenvalues of Hermitian matrices," medium
importance, and status `verified`. Git blame attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no work, edition, theorem/page,
formula, domain, dimension, eigenvalue convention, index range, norm, proof boundary, corrections,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1645-1672` projects the record as `THM-M-0056` while leaving the formal
system, exact definitions and assumptions, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. Rev-5.6 retains `verified` only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Inspected historical primary lead

Hermann Weyl, *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller
Differentialgleichungen (mit einer Anwendung auf die Theorie der Hohlraumstrahlung)*,
*Mathematische Annalen* 71(4) (1912), 441-479, DOI `10.1007/BF01456804`, was inspected from the
public-domain Zenodo scan at `https://zenodo.org/record/1526112/files/article.pdf`. The observed
39-page PDF SHA-256 is
`47a614bca926c86e874335398c589ac4b3fac77452dc2859882f5f6001fda5af`.

Section 1 on printed pages 443-447 studies symmetric integral kernels under the Fredholm-Hilbert
theory. Weyl orders positive and negative reciprocal eigenparameters separately. Satz I on printed
pages 445-446 treats `K = K' + K''`: its formula (1) gives the corresponding upper sum inequality
for positive sequences, formula (2) gives the lower inequality for negative sequences, and formula
(3) gives an absolute-value estimate. The proof derives the positive case from a finite-rank
approximation lemma and obtains the negative case by applying it to `-K`.

This is a complete primary proof lead for the historical source family, but not `H0` for the
catalog claim. It is not literally a theorem about finite complex Hermitian matrices and uses
historical reciprocal eigenparameter notation. The catalog does not cite the paper or identify
Satz I rather than the paper's famous asymptotic application. A faithful translation, finite-matrix
specialization or modern-source decision, definition and assumption mapping, correction/errata
audit, lawful immutable admission, and independent review remain open.

## Modern finite-matrix leads

Sai-Nan Zheng, Xi Chen, Lily Li Liu, and Yi Wang, *Inertia indices and eigenvalue inequalities for
Hermitian matrices*, arXiv `1910.01966v4`, later *Linear and Multilinear Algebra* 70(8), 1543-1552,
DOI `10.1080/03081087.2020.1765957`, was inspected at
`https://arxiv.org/pdf/1910.01966v4`. The observed PDF SHA-256 is
`7ac7b4f9ca55ff5c6a5dd31cd92ec4e12672ea9098497faa6ff5359782cdd66a`. Page 1 fixes
decreasing eigenvalues of `n` by `n` Hermitian matrices. Corollary 2.5 on page 3 states and proves
the upper additive Weyl inequality. This is a versioned exact-family source lead, not the catalog's
selected source or an accepted H0 crosswalk.

Terence Tao's author-hosted *254A, Notes 3a: Eigenvalues and sums of Hermitian matrices*, dated 12
January 2010, was inspected at
`https://terrytao.wordpress.com/2010/01/12/254a-notes-3a-eigenvalues-and-sums-of-hermitian-matrices/`.
It displays the upper additive inequality, its lower companion, the per-index operator-norm
perturbation bound, and a Schatten refinement. The page is useful because it exposes the variants
hidden by the catalog gloss. It is mutable exposition, not an admitted primary source or H0 evidence.

## Clause crosswalk

| Catalog or source component | Prospective Lean surface | Intake assessment |
|---|---|---|
| "Hermitian matrix" | `A B : Matrix (Fin n) (Fin n) Complex` plus `A.IsHermitian` and `B.IsHermitian`, or source-approved finite types | scalar, dimension, and index representation open |
| ordered eigenvalues | `Matrix.IsHermitian.eigenvalues₀ : Fin (card n) -> Real` | pinned API exists; enumeration transport and empty dimension open |
| perturbation | matrix addition `A + B`, or comparison using `A - B` | exact binders and Hermitian closure clauses open |
| upper additive family | admissibly indexed inequality for `A+B`, `A`, and `B` | Zheng Corollary 2.5 lead; not selected |
| lower additive family | dual admissibly indexed inequality | modern lead; not selected or automatically included |
| perturbation bound | absolute difference of corresponding eigenvalues bounded by an induced operator norm | catalog-aligned candidate corollary; norm and transport open |
| Weyl 1912 Satz I | symmetric kernels and positive/negative reciprocal eigenparameter sequences | historical ancestor; finite-matrix/source transport unapproved |
| `verified` | kernel declaration plus accepted exact evidence would be required | explicitly rejected as evidence |

## Pinned Lean crosswalk

| Required role | Pinned declaration | Boundary |
|---|---|---|
| decreasing Hermitian eigenvalues | `Matrix.IsHermitian.eigenvalues₀`, `eigenvalues₀_antitone` | enumeration substrate only |
| eigenvectors and diagonalization | `mulVec_eigenvectorBasis`, `spectral_theorem` | spectral theorem, not a perturbation inequality |
| real spectrum bridge | `spectrum_real_eq_range_eigenvalues` | set/range identification only |
| Rayleigh addition | `ContinuousLinearMap.rayleighQuotient_add` | local quadratic-form identity only |
| Rayleigh norm bound | `rayleighQuotient_le_norm`, `norm_eq_iSup_rayleighQuotient` | endpoint/norm ingredients only |
| indexed minimax bridge | no declaration located by bounded search | required proof interface may be missing; downstream audit open |
| exact Weyl root | no declaration located by bounded search | provisional M4; no proof body credited |

`IntakeProbe.lean` checks the listed adjacent declarations against pinned mathlib. A bounded search
over repo-local and pinned Lean sources found no eigenvalue-of-sum or perturbation theorem; root-
system occurrences of "Weyl" are unrelated. Absence under these patterns is not a global
nonexistence claim and does not replace the downstream precommitted anchor audit.

## Gate assessment and retry condition

The source-family assessment is provisional `H1`: a complete historical primary proof passage and
modern exact-family proof lead were inspected, but exact catalog identity, variant selection,
kernel-to-matrix transport, incorporated assumptions, notation, corrections, preservation, and
independent review are unresolved. The formal assessment is provisional `M4`, and no readable
source-faithful reconstruction exists (`R4`). No root vector is assigned before statement freeze.

An accountable source reviewer must select one exact source proposition and record its edition,
stable locator, definitions, ordered binders, hypotheses, conclusion, admissible indices, proof
boundary, dependencies, corrections, and relationship to the 1912 attribution. Only then may the
statement phase encode the same proposition, minimize imports, serialize fingerprints, check
alternate forms, and mutation-test every proposition-changing choice.
