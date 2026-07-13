# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10742` through `:10747` supplies exactly the title
`Lax等价定理`, Peter Lax, the year 1956, the slogan `稳定性+相容性=收敛性`, importance `high`,
and status `已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, equation, domain,
definitions, ordered binders, hypotheses, direction, conclusion, proof, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:40027` through `:40052` repeats the slogan while explicitly leaving the
target formal system, foundation, exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Its generic closed-result and
leaf-audit wording is planning metadata, not evidence. Rev-5.6 retains `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Historical source lead

Crossref identifies P. D. Lax and R. D. Richtmyer, *Survey of the stability of linear finite
difference equations*, *Communications on Pure and Applied Mathematics* 9(2), 267-293 (May 1956),
DOI `10.1002/cpa.3160090206`. This is a strong bibliographic match for the catalog's title and year,
and it exposes a material omission: the repository attributes the result only to Lax.

The publisher article and PDF endpoints returned HTTP 403 during intake. Consequently no original
article text, theorem/page locator, incorporated definition, assumption, direction, proof boundary,
or erratum was inspected. Crossref metadata is a source-family lead, not a primary-proof crosswalk
or `H0` evidence. An accepted historical mapping requires preserved source bytes and independent
review.

## Inspected modern source and formal lead

Mohit Tekriwal, Karthik Duraisamy, and Jean-Baptiste Jeannin, *A Formal Proof of the Lax
Equivalence Theorem for Finite Difference Schemes*, NFM 2021, pages 322-339, arXiv
`2103.13534`, DOI `10.1007/978-3-030-76384-8_20`, was inspected in the arXiv version. Section 2
explicitly follows J. M. Sanz-Serna and C. Palencia's 1985 generalized discretization presentation,
not a transcription established here as identical to the 1956 article.

The modern paper's Theorem 1 states: for the continuous and approximate problems and maps defined
in its Definitions 1-5, consistency and stability imply convergence. Its material setup is:

| Paper locus | Source content | Intake mapping |
|---|---|---|
| Definition 1, pp. 3-4 | real or complex normed spaces `X,Y`; linear `A` on `D ⊂ X`; bounded linear solution operator `E : Y → X`, `EA = I` on `D`, and unique continuously data-dependent solutions | continuous problem and well-posedness binders |
| Definition 2, p. 4 | positive step set `H` with zero as unique limit point; normed `X_h,Y_h`; linear, well-posed `A_h` with `E_h=A_h⁻¹`; bounded linear `r_h,s_h` with uniformly bounded norms | approximation family and comparison maps |
| Definition 3, pp. 4-5 | convergence for every `f ∈ Y`: `‖r_h E f - E_h s_h f‖ → 0` | candidate convergence predicate |
| Definition 4, p. 5 | consistency on `D₀ ⊂ D`, with `A(D₀)` dense in `Y`: `‖A_h r_h u - s_h A u‖ → 0` | candidate consistency predicate and dense-core premise |
| Definition 5, p. 5 | stability: a step-independent `K` bounds every operator norm `‖E_h‖` | candidate stability predicate |
| Theorem 1 and proof, pp. 5-7 | consistency and stability imply convergence by linearity, `E_h A_h=I`, the operator-norm bound, and a squeeze argument | sufficiency only; not an audited classical iff |

The paper says its Coq development uses Coquelicot and the standard real library and is therefore
nonconstructive. The public repository `https://github.com/mohittkr/Lax_equivalence` was inspected
at immutable commit `c19b626513ce8ec1a6426f2364e6c45e8caa85ae`, tree
`2972b15fa05e611a7bf1a1369f71cc68e1aae56b`. File `lax_equivalence.v` contains declaration
`is_convergent`; the README pins Coq 8.9.1, MathComp 1.9.0, Flocq 3.2.0, Coquelicot 3.0.3,
coq-interval 3.4.1, BigNums 8.9.0, and an external CoqLM library.

Those observations establish a credible Coq candidate, not Lean closure. The dependency was not
cloned, fetched, built, vendored, or added to `.lake`; its exact type and proof graph were not
accepted as source-identical; and no Coq assurance state is imported into the Lean target.

## Literal statement crosswalk

| Repository phrase | Material source alternatives | Prospective Lean component | Result |
|---|---|---|---|
| stability | uniform bound on solution inverses, propagation stability, or another classical scheme notion | family of continuous linear maps plus exact uniformity/filter data | predicate open |
| consistency | dense-core operator consistency, truncation consistency, or scheme-specific order | quantified residual convergence in selected norms | domain and predicate open |
| convergence | solution convergence for each datum, uniform convergence, finite-time convergence, or a rate | filtered convergence of compared continuous/discrete solutions | mode and quantifiers open |
| `+` | conjunction under shared setup, not arithmetic addition | explicit hypotheses after source selection | typography is not a connective certificate |
| `=` / equivalence | sufficiency in the 2021 theorem, or necessity and sufficiency in a classical formulation | implication, iff, or two separately proved directions | direction open |
| Peter Lax, 1956 | likely Lax-Richtmyer article | provenance | coauthor and pinpoint source missing |
| verified | untrusted inventory label | accepted source and kernel receipts | no H or M credit |

The literal record cannot populate a canonical domain, ordered binders, hypotheses, conclusion,
alternate encodings, excluded cases, or formal expression fingerprint without adding mathematics.

## Pinned Lean crosswalk

| Candidate | What is checked | Why it is not the target |
|---|---|---|
| `ContinuousLinearMap.le_opNorm` | `‖f x‖ ≤ ‖f‖ * ‖x‖` | local analytic inequality only; no scheme or convergence theorem |
| `banach_steinhaus` | pointwise bounded maps from a complete normed space have uniformly bounded operator norms | possible necessity-direction substrate, but no discretization objects or statement transport |
| `ContinuousLinearMap.ofTendstoOfBoundedRange` | builds a continuous linear map from pointwise limit and uniform bounds | generic operator-limit interface only |
| `ContinuousLinearMap.tendsto_of_tendsto_pointwise_of_cauchySeq` | operator-norm convergence from pointwise convergence for a Cauchy sequence | sequence-specific limit substrate, not Lax equivalence |
| `squeeze_zero` | transfers convergence to zero through scalar bounds | final analytic step only |

`IntakeProbe.lean` checks these declarations at the pinned revision. No source-selected terminal Lean
theorem was found. The probe is discovery evidence only, not a canonical target, proof body,
exhaustive anchor audit, or absence proof.

## Source gate

Before statement work, accountable reviewers must preserve and select an exact source result;
settle the 1956 versus generalized formulation and the missing Richtmyer attribution; map every
problem, space, operator, step family, restriction map, consistency/stability/convergence
definition, norm, filter, direction, quantifier, time/data condition, and boundary case; audit
corrections; and independently approve the result. Only then may the statement phase freeze the
Lean expression, minimal imports, checked transports, and mutations.

Until then, `H1` records a published named theorem whose exact source mapping remains incomplete,
`M4` records that no source-identical usable Lean artifact is credited, and `R4` records that no
source-faithful reconstruction can anchor to an unfrozen root.
