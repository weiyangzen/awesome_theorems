# THM-M-1450 source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:10588-10593` contains exactly:

- title: `幂迭代` (power iteration);
- proposer: `众多数学家` (many mathematicians);
- time: `20世纪` (20th century);
- statement gloss: `最大特征值的迭代方法` (an iterative method for the largest eigenvalue);
- importance: high; and
- formalization status: `已验证` (verified).

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, domain,
hypotheses, convergence conclusion, proof, formal declaration, or validation link. The Stage0
projection at `Docs/Stage0_Blueprint.md:39433-39458` repeats the gloss and explicitly leaves the
definitions, premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links to be supplied. Under rev-5.6, the verified label is untrusted metadata.

## Literal crosswalk

| Repository phrase | Material ambiguity | Required exact statement component | Intake status |
|---|---|---|---|
| `幂迭代` | raw powers, normalized power method, block/subspace iteration, or a numerical implementation | recurrence, normalization, estimator, indexing, arithmetic model | open |
| `最大特征值` | largest ordered value, greatest modulus, spectral radius, or dominant invariant subspace | scalar order/modulus, spectral-gap and multiplicity hypotheses | open |
| `迭代方法` | termination/correctness, asymptotic convergence, rate, stability, or complexity | exact conclusion and convergence mode | open |
| `众多数学家` / `20世纪` | no accountable author, work, edition, theorem, or page | versioned source identity and historical review | open |
| `已验证` | catalog inventory label only | no human or machine proof component | explicitly untrusted |

The rows do not determine ordered binders or one truth-valued claim. Therefore the canonical human
statement and Lean expression remain null rather than silently importing a folklore theorem.

## Inspected secondary source lead

Z. Bai, J. Demmel, J. Dongarra, A. Ruhe, and H. van der Vorst, editors, *Templates for the
Solution of Algebraic Eigenvalue Problems: A Practical Guide*, SIAM, 2000, includes M. Gu's
section "Power Method" in the Hermitian eigenproblem chapter. The Netlib HTML at
`https://www.netlib.org/utk/people/JackDongarra/etemplates/node95.html` was observed on 2026-07-13
with SHA-256 `541ab6f6f74f3ee1c28396d9b4828e3703c4220500fd7f2d44271122b0844070`.

That section describes the intended numerical family more precisely: it seeks an eigenvalue of
largest absolute value and a corresponding eigenvector; exact-arithmetic convergence fails when
the start is perpendicular to the dominant eigenvector; otherwise generated vectors become
increasingly parallel; and the convergence rate depends on `|lambda_2 / lambda_1|`. This is useful
scope evidence, but it is a retrieved mutable secondary exposition not cited by the repository. The
page does not by itself supply an accepted, complete theorem/proof/premise/errata crosswalk, and it
does not settle non-Hermitian, multiplicity, sign/phase, normalization, estimator, or boundary
conventions. It is not H0 and does not repair the catalog statement without independent admission.

## Candidate source-to-statement rows

| Secondary-source component | Candidate mathematical component | Lean obligation if selected | Current boundary |
|---|---|---|---|
| Hermitian eigenproblem chapter | finite-dimensional Hermitian/self-adjoint matrix setting | field, inner-product space, dimension, matrix/operator transport, symmetry | catalog does not select it |
| eigenvalue largest in absolute value | unique dominant eigenvalue in modulus | eigenvalue enumeration, strict modulus gap, simplicity/nonzero premises | exact order and ties unresolved |
| start not perpendicular to dominant eigenvector | nonzero dominant eigencoordinate | inner-product/projection premise and nonzero-iterate lemmas | zero and multiplicity cases unresolved |
| vectors become increasingly parallel | projective or angle convergence | precise sequence, normalization, convergence predicate, sign/phase quotient | no exact conclusion supplied |
| rate depends on `|lambda_2/lambda_1|` | geometric convergence factor | exact bound/asymptotic statement, constants, quantifier order | prose does not choose one |
| accepted `lambda` and `x` in the algorithm | numerical eigenvalue/eigenvector output | estimator, tolerance, stopping and residual correctness | finite algorithm contract unresolved |

These are candidate rows for later source selection, not inherited clauses or a proof crosswalk.

## Pinned formal substrate, not a theorem anchor

The bounded intake search used pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Relevant adjacent declarations include:

- `Module.End.HasEigenvector.pow_apply` in
  `Mathlib.LinearAlgebra.Eigenspace.Basic`, proving the behavior of powers on an already supplied
  eigenvector;
- `Matrix.mulVecLin` and `Matrix.mulVecLin_mul` in
  `Mathlib.LinearAlgebra.Matrix.ToLin`, relating matrix multiplication and linear maps; and
- `LinearMap.IsSymmetric.eigenvalues`, `eigenvalues_antitone`,
  `hasEigenvector_eigenvectorBasis`, and `eigenvectorBasis_apply_self_apply` in
  `Mathlib.Analysis.InnerProductSpace.Spectrum`, providing finite-dimensional self-adjoint spectral
  coordinates.

No declaration named or documented as power method/power iteration or as convergence of normalized
operator powers was found in the bounded pinned-mathlib and repo-local Lean search. The named APIs
are definitions and ingredients only. `IntakeProbe.lean` elaborates checks of them but declares no
target theorem. This negative scoped search is not the later exhaustive anchor audit.

## Non-substitution boundary

An eigenvector-power identity handles a vector that is already exactly in one eigenspace; it does
not prove convergence from a mixed starting vector. A spectral theorem supplies an eigenbasis but
not the recurrence, normalization, dominant-component estimate, or limit. Perron-Frobenius can
provide a positive dominant eigenpair under positivity hypotheses but cannot replace a general
source-selected power-method convergence statement. A numerical trace or residual check cannot
replace an all-dimensions, all-iterations theorem.

## Gate result

Human status is provisionally `H5`: the catalog target is a method/gloss rather than one stable
proposition. Machine status is `M4`: no usable source-identical formal artifact exists while the
root is unidentified. Readability status is `R4`: this boundary explanation is not a readable proof
of an exact theorem. Retry requires an accountable, immutable source selection and independent
review fixing every material row above before exact statement elaboration.
