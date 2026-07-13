# THM-M-1459 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10651` through `:10656` supplies exactly the title
`快速多极子方法`, attribution to Leslie Greengard and Vladimir Rokhlin, year 1987, gloss
`N体问题的快速算法`, high importance, and status `已验证`. All six uncited lines originate at
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliography, kernel, dimension, algorithm, ordered binders, hypotheses, error or cost conclusion,
proof, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:39676` through `:39701` repeats the gloss while explicitly leaving the
target formal system, foundations, exact definitions and premises, proof route, dependencies,
alternate forms, axioms, machine status, and artifact links open. Its generic closed-result and
leaf-audit language is planning metadata, not source evidence. Rev-5.6 retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected source leads

Crossref's publisher-maintained record for DOI `10.1016/0021-9991(87)90140-9` was inspected on
2026-07-13 (response SHA-256
`6be90529ec44dbd32cea883cf1baec3968ee896cb3120e2b4262e673da4740b8`). It identifies L.
Greengard and V. Rokhlin, *A fast algorithm for particle simulations*, *Journal of Computational
Physics* **73** (1987), no. 2, 325-348. Leslie Greengard's NYU publication page was also inspected
(HTML SHA-256 `6665bf314afda2c47bed2bc0275f15cd21c6e8eb7d36416603942ef76f3a1bd7`);
it lists the same work, coauthor, journal, volume, page, and year.

These sources establish a credible historical article identity and explain the catalog's
attribution and year. They do not make a proposition canonical. The article body was not preserved
and inspected: the publisher text endpoint rate-limited the request, OpenAlex and Semantic Scholar
reported no open full text, and historical mirrors located by metadata were unavailable. No
article theorem/formula locator, incorporated-definition map, assumptions, error/complexity
crosswalk, correction audit, or independent review exists. Bibliographic metadata and an author
publication list are discovery evidence, not `H0`.

Rick Beatson and Leslie Greengard, *A short course on fast multipole methods*, was inspected from
Greengard's NYU-hosted PDF (SHA-256
`2691e493b4cebc167573dc3db12f9d568a724ecd0469b7c92d068ed2a2db1128`). The PDF has 37
printed pages. Its introduction says this family reduces all pairwise interactions among `N`
particles from quadratic work to linear or `N log N` work, but later sections make that slogan
precise through distinct results. Printed pp. 16-17 give Lemma 4.2, a two-dimensional logarithmic
multipole expansion and truncation bound for charges inside a disk and targets outside it. Printed
pp. 21-23 give translation Lemmas 4.6-4.8; pp. 24-25 derive an approximate `40 N p` operation count
after choosing a leaf occupancy parameter equal to the expansion order. Printed pp. 27-28 give
Theorem 5.2, a separate three-dimensional Laplace multipole expansion and error bound. Its
bibliography identifies the 1987 paper as reference 29.

This author-hosted course is a valuable specification and source-family lead, not `H0`: it is later
than the catalog date, contains multiple non-equivalent roots, does not show which the catalog
intends, has not been admitted as an immutable edition, and has no complete assumption/errata map
or independent review. In particular, Lemma 4.2 alone is not the `40 N p` algorithm claim, and the
two-dimensional and three-dimensional theorems are not interchangeable.

The author-hosted PDF of J. Carrier, L. Greengard, and V. Rokhlin, *A fast adaptive multipole
algorithm for particle simulations*, *SIAM Journal on Scientific and Statistical Computing* **9**
(1988), 669-686, DOI `10.1137/0909044`, was inspected as a second, later source-family lead
(SHA-256 `a49ce4a647fb29a7701c0e8db58c250f13f6f7d3fe3dca94d2b765b39f1333d1`). Its
Theorem 2.1 states a planar complex/logarithmic multipole expansion with a truncation estimate and
points back to the 1987 paper for detailed proofs. Its later sections separately fix a unit-square
adaptive hierarchy, set expansion order from machine precision, require separation for analytic
error bounds, derive resource formulas linear in `N` for fixed precision and selected leaf size,
and report empirical timings and roundoff behavior. This reinforces the need to distinguish an
analytic lemma, an adaptive algorithm, conditional asymptotic resource bounds, and experiments.
It is a 1988 follow-up, not the uninspected 1987 body or an accepted mapping of the catalog root.

## Literal crosswalk

| Repository element | Source-family component | Prospective Lean component | Intake result |
|---|---|---|---|
| fast multipole method | hierarchical aggregation and translation of distant particle interactions | tree/box data, finite source and target families, expansion and translation functions | algorithm family identified; variant absent |
| `N体问题` | particle positions and pairwise interactions, possibly static evaluation or dynamics | finite index types, position vectors, source strengths, kernel, collision policy | domain and even static-versus-dynamic task absent |
| fast algorithm | correctness plus a sourced resource claim | exact approximation relation and an explicit cost model | complexity variable, accuracy regime, operations, and bound absent |
| multipole expansion | kernel-specific separated expansion | complex/real series, powers, truncations, separation hypotheses | kernel, dimension, center, convergence region, and order absent |
| hierarchy | quadtree/octree or adaptive clustering and interaction lists | finite rooted tree, boxes, invariants, near/far relations | no construction or invariant selected |
| accuracy | analytic truncation and possibly floating-point error | norm inequality with requested tolerance | metric, parameter dependence, and arithmetic model absent |
| 1987 / Greengard-Rokhlin | historical locator | source provenance only | exact article identified bibliographically; body not inspected |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no H or M credit |

The literal record therefore cannot populate the canonical domain, ordered quantifiers,
hypotheses, conclusion, alternate encodings, boundary exclusions, or expression fingerprint.

## Pinned Lean crosswalk

| Candidate | What is checked | Why it is not the target |
|---|---|---|
| `norm_sum_le` | norm of a finite sum is bounded by the sum of norms | generic aggregation inequality; no particles, kernel, hierarchy, or approximation |
| `summable_geometric_of_norm_lt_one` | powers in a normed field are summable below unit norm | analytic substrate only; no source-selected multipole series or separation mapping |
| `tsum_geometric_of_norm_lt_one` | the infinite geometric series equals `(1 - x)⁻¹` | no truncation-error theorem or FMM algorithm |
| `tsum_geometric_le_of_norm_lt_one` | a norm bound for the geometric sum | not a local or global FMM error bound |
| `Complex.norm_mul` and `norm_inv` | complex multiplication and inversion respect norm | representation interface only |
| `Complex.hasSum_taylorSeries_neg_log` | the Taylor series for `-log (1 - z)` converges when `‖z‖ < 1` | close analytic ingredient for a planar log kernel, but no charges, centers, hierarchy, or cost theorem |
| `Complex.norm_log_one_sub_inv_add_logTaylor_neg_le` | explicit remainder bound for the truncated logarithm series | one-series error substrate only; no finite-source or end-to-end FMM composition |

A bounded exact-topic search found no source-selected terminal FMM theorem in pinned mathlib or
repo-local Lean. This is discovery evidence only and is not a global absence proof or the required
immutable external-project anchor audit. `IntakeProbe.lean` checks the named adjacent APIs without
declaring a target or proof body.

## Source gate

The first downstream gate requires an accountable correction that selects a lawfully preserved,
immutable source edition and one exact truth-valued proposition; maps every kernel, dimension,
particle and strength binder, collision premise, tree/box invariant, separation rule, expansion and
translation, error condition, resource model, conclusion, and boundary case; distinguishes static
evaluation from time integration and analytic exact arithmetic from floating-point behavior;
audits corrections; and receives independent numerical-analysis and source review. Only then may
the statement phase freeze a Lean expression, minimal imports, checked transports, and required
statement mutations.

Until that correction exists, `H5` describes the catalog target's ill-posed proposition status,
`M4` records the absence of a source-identical usable formal artifact, and `R4` records the absence
of an anchorable reconstruction. These classifications do not say that established fast-multipole
results are false or mathematically open.
