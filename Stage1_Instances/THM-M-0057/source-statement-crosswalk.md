# THM-M-0057 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:426-431` supplies exactly the title `霍夫曼-魏兰德特定理`, the
attribution A. J. Hoffman/H. W. Wielandt, the year 1953, the gloss
`正规矩阵特征值的扰动`, importance `中`, and status `已验证`. Git history attributes all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:1672-1697` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

The catalog contains no bibliography, formula, matrix domain, normality definition, eigenvalue
enumeration, multiplicity convention, permutation, norm, ordered binders, boundary case, proof
boundary, correction record, reviewer, or formal artifact. It names a theorem family but not one
stable proposition.

## Original-paper lead

Crossref, OpenAlex, and Semantic Scholar metadata identify A. J. Hoffman and H. W. Wielandt, "The
variation of the spectrum of a normal matrix," *Duke Mathematical Journal* 20(1) (1953), 37-39,
DOI `10.1215/S0012-7094-53-02004-3`. The publisher/Project Euclid full-text endpoint returned an
access interstitial in this environment, so no theorem passage, definitions, proof, or errata were
inspected. Bibliographic identity is a primary-source lead, not `H0` evidence.

## Inspected secondary source lead

Xuefeng Xu and Chen-Song Zhang, "New perturbation bounds for the spectrum of a normal matrix,"
arXiv `1612.05759v2` (version 2 dated 2017-07-02), was inspected from the 20-page arXiv PDF on
2026-07-13. The observed bytes have SHA-256
`c508f6c7f5f1b66ba93e654d380c134f9bc6b4bb98a30eccb9b59ab844cfa953`.

- The abstract states that for normal `A, A_tilde in C^(n x n)` with respective spectra
  `{lambda_i}` and `{lambda_tilde_i}`, a permutation `pi` exists for which the `l2` matching
  distance is no larger than the Frobenius norm of `A_tilde - A`.
- Introduction pages 1-2 define conjugate transpose, the Frobenius norm, and normality as
  `A A^* = A^* A`.
- Introduction pages 1-2 define
  `D2 = (sum_i |lambda_tilde_(pi(i)) - lambda_i|^2)^(1/2)`, set
  `E = A_tilde - A`, and state `D2 <= ||E||_F`, attributing this to Hoffman and Wielandt [1].
- Reference [1] identifies the original paper as *Duke Math. J.* 20 (1953), 37-39.

This later paper is a precise source-discrimination lead, not an accepted root source. It is
secondary, the catalog does not cite it, and the original theorem wording, indexing and proof have
not been checked against it. Incorporated definitions, correction/errata status, lawful durable
preservation, and independent review remain open. It supports provisional `H1`, not `H0`.

## Clause crosswalk

| Catalog component | Inspected source lead | Prospective Lean surface | Intake result |
|---|---|---|---|
| normal matrices | both `A` and `A_tilde` in `C^(n x n)`, with `AA* = A*A` | `Matrix (Fin n) (Fin n) Complex` plus `IsStarNormal` or an explicit equation | domain, predicate encoding, and zero dimension open |
| eigenvalues | two spectral lists of length `n`, counted with multiplicity | charpoly roots/enumerations; Hermitian `Matrix.IsHermitian.eigenvalues` only for a specialization | general-normal enumeration and completeness bridge missing |
| perturbation | an existential matching permutation | `Equiv.Perm (Fin n)` or equivalent finite reindexing | direction and index transport open |
| matching distance | square root of the sum of squared complex moduli | finite sum, `Complex.abs`/norm, real square root or `L2` norm | exact coercions and squared alternate open |
| matrix distance | Frobenius norm of `A_tilde - A` | scoped matrix Frobenius norm and `Matrix.frobenius_norm_def` | instance/definition and difference orientation open |
| conclusion | matching distance is at most matrix distance | an existential inequality | exact ordered binders and boundary behavior open |
| `已验证` | no cited source or formal artifact | accepted source and kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

Pinned mathlib provides generic `IsStarNormal`, matrix spectrum and eigenspace bridges, Frobenius
norm definitions and invariances, and Hermitian eigenvalues with algebraic-multiplicity and
spectral-theorem facts. `IntakeProbe.lean` elaborates selected exact declarations and prints axiom
reports for representative adjacent theorems. The Hermitian APIs do not cover arbitrary normal
complex matrices, and no checked declaration combines normality, two complete eigenvalue
enumerations, a permutation, and the Frobenius perturbation inequality.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no
Hoffman-Wielandt declaration. The only `Wielandt` matches in mathlib concerned unrelated finite
permutation-group citations. This is intake discovery only, not the later immutable external
anchor audit and not a proof of global absence.

## Exit gate

Before statement freeze, independent source and formal reviewers must admit a pinpoint primary or
authoritative proposition and approve the complex matrix domain, normality hypotheses, complete
eigenvalue enumerations with multiplicity, permutation convention, Frobenius norm, inequality
form, binders, and zero-dimensional behavior. The statement phase must then elaborate that exact
target, compile every credited transport, and run removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. Until then the mathematical and Lean targets remain null and
the root remains `[H1, M4, R4]`.
