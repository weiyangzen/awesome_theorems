# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10553-10558` supplies exactly the title `高斯消元法`, attribution
to Carl Friedrich Gauss, year 1810, gloss `线性方程组的直接解法`, high importance, and status
`已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, algorithm, ordered binders, hypotheses, conclusion, proof, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:39298-39323` repeats the gloss while explicitly leaving the target formal
system, foundations, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic closed-result and leaf-audit language
is planning metadata, not source evidence. Rev-5.6 retains `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Inspected specification and historical lead

Joseph F. Grcar, "How Ordinary Elimination Became Gaussian Elimination," *Historia Mathematica*
38(2) (2011), 163-218, DOI `10.1016/j.hm.2010.06.003`, arXiv `0907.2397`, was inspected in the
56-page arXiv v4 PDF observed on 2026-07-13. Its SHA-256 is
`e1e0509ea763a44327ce521c39851fdab6e69178ddd6a09de66ab15841f4b2f2`.

Section 1.2 describes the canonical schoolbook method: equations and variables may be rearranged
to choose a leading variable; the leading equation eliminates that variable from following
equations; the process recurses; and a remaining triangular system is back-substituted. The
elementary operations produce an equivalent upper-triangular system. The same section says the
technical literature instead views the arithmetic as triangular factorization. Section 3.3 places
Gauss's 1810 work in least-squares calculations and distinguishes it from the older general
schoolbook method.

This is a strong family/specification lead, not `H0`. The catalog does not cite it or choose between
its distinct views; the arXiv page itself requests citation of the corrected published article; no
lawfully preserved published edition, pinpoint proposition, complete assumptions, errata audit,
source-to-node mapping, or independent review has been accepted.

## Literal crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| `线性方程组` | `A x = b`, homogeneous or affine | `A : Matrix m n K`, `b : m -> K`, `A *ᵥ x = b` | domain, shape, RHS, and consistency unspecified |
| `消元` | pivot, swap, scale, and row addition | transvections, permutation matrices, augmented states | operation set and pivot policy absent |
| `直接解法` | finite reduction plus substitution/readout | executable function and a preservation/correctness relation | no output or conclusion supplied |
| equivalent system | equality of solution sets after each step | set equality or an iff for `mulVec` equations | plausible source component, not catalog-selected |
| upper-triangular/echelon result | recursive normal form | future echelon predicate or pinned triangular predicates | exact normal form absent |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no credit |

The literal record therefore cannot populate the canonical domain, ordered quantifiers,
hypotheses, conclusion, alternate encodings, boundary cases, or expression fingerprint.

## Pinned Lean crosswalk

| Candidate | What is checked | Why it is not the target |
|---|---|---|
| `Matrix.transvection_mul_apply_same` | left multiplication adds a multiple of one row to another | one elementary-operation semantic lemma only |
| `Matrix.Pivot.exists_list_transvec_mul_mul_list_transvec_eq_diagonal` | a finite square matrix over a field is reduced to diagonal by left and right transvections | includes column operations; no RHS, solution-set equivalence, algorithm output, or substitution |
| `Matrix.Pivot.exists_list_transvec_mul_diagonal_mul_list_transvec` | transvection/diagonal factorization exists | factorization substrate, not solver correctness |
| `Matrix.inv_mulVec_eq_vec` and `Matrix.mulVecLin_mul` | invertible solving and composition interfaces | do not implement or characterize Gaussian elimination |
| `Mathlib.Tactic.Linarith.SimplexAlgorithm.Gauss.getTableau` | meta implementation returns a tableau for homogeneous `A x = 0` | no located correctness theorem; meta/oracle, homogeneous, and representation-specific |

These pinned candidates are discovery evidence only. No exact source-identical formal declaration or
proof body is credited, and no exhaustive external-project audit has been performed.

## Source gate

The first downstream gate requires an accountable correction that selects one immutable source
edition and exact truth-valued proposition; maps every definition, binder, premise, conclusion,
algorithm state, boundary case, and proof boundary; reconciles the Gauss/1810 attribution and LU
neighbor; audits corrections; and receives independent source and numerical-linear-algebra review.
Only then may the statement phase freeze a Lean expression, minimal imports, checked transports,
and required statement mutations.

Until that correction exists, `H5` describes the catalog target's ill-posed proposition status,
`M4` records the absence of a source-identical usable formal artifact, and `R4` records the absence
of an anchorable reconstruction. These classifications do not say that standard Gaussian-
elimination results are false or mathematically open.
