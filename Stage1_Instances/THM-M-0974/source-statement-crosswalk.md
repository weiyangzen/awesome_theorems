# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7113` through `:7118` supplies exactly the title
`Talagrand集中不等式`, Michel Talagrand, the year 1995, the gloss `凸Lipschitz函数的集中`,
importance `high`, and status `已验证`. The identical block at lines 7301 through 7306 is a source-
corpus duplicate, not independent evidence. Both originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` and contain no bibliography, theorem locator, formula,
domain, binders, hypotheses, constants, proof, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26551` through `:26576` repeats the gloss while explicitly leaving exact
definitions and premises, proof path, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Its generic closed-result language is planning metadata. Rev-5.6 retains the
verified label only as untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected 1995 primary source lead

Michel Talagrand, *Concentration of measure and isoperimetric inequalities in product spaces*,
*Publications Mathematiques de l'IHES* 81 (1995), 73-205, DOI `10.1007/BF02699376`, is a strong
source-family match. The publisher-hosted article was inspected during intake.

The introduction defines a concentration function for a metric probability space and records the
generic implication that a 1-Lipschitz function concentrates around a median. It then specializes
the paper to product spaces and different set-fattening notions. It explicitly says that all Part I
concentration results are stated for sets and: "We will, however, give no abstract statement of this
type" for functions. Section 4.1's leading result is a convex-hull-distance inequality for a set in
a product space, not a theorem whose binders say "convex Lipschitz function."

This source therefore validates the broad Talagrand/product-concentration genealogy but does not
select the repository's exact functional root. The article is a discovery and derivation lead, not
an `H0` source crosswalk.

## Competing source surface

Han Huang and Konstantin Tikhomirov, *On dimension-dependent concentration for convex Lipschitz
functions in product spaces*, *Electronic Journal of Probability* 28 (2023), DOI
`10.1214/23-EJP944` (arXiv `2106.06121`), distinguishes two relevant surfaces. It calls the
convex Euclidean-1-Lipschitz bound on the uniform cube `{-1,1}^n` a classical Talagrand result and
jointly cites the 1995 paper and Talagrand's 1996 paper *A new look at independence*. Separately, it
states a bounded-coordinate-support product-measure extension of Talagrand's argument and cites a
later secondary treatment. These are formulation and eponym witnesses, not a pinpoint primary
functional theorem, exact-constant authority, primary proof source, or `H0` evidence.

The 1996 paper is therefore a competing primary-author lead despite the catalog's 1995 date. Its
exact theorem/page, relation to the 1995 set theorem, assumptions, constants, corrections, and
errata were not admitted at intake.

## Literal crosswalk

| Repository component | Source alternatives | Prospective Lean component | Intake result |
|---|---|---|---|
| Talagrand, 1995 | 1995 product-space set inequalities; later functional consequences also cite a 1996 refinement | immutable source identity and reviewed derivation boundary | family lead only |
| convex | convex function on all of a real normed space, on a product support, or a convex-hull set distance | `ConvexOn` with exact scalar, domain, support, and function | domain and predicate open |
| Lipschitz | Euclidean 1-Lipschitz, general constant, weighted product norm, or another metric | `LipschitzWith` plus fixed metric/norm and scale | norm and constant open |
| functions | real-valued measurable function of finite independent coordinates | product type, product measure, measurability and integrability | all binders open |
| concentration | upper/lower/two-sided median or mean tail | measurable deviation event and probability inequality | center, direction and event open |
| constants | exact `1/4` in a convex-distance set theorem versus universal constants in functional forms | real/`ENNReal` expression with side conditions | no constant selected |
| verified | untrusted catalog field | accepted source and kernel receipts | no H or M credit |

## Pinned Lean crosswalk

| Checked interface | What it supplies | Why it is not the target |
|---|---|---|
| `ConvexOn` | a standard convex-function predicate on a set | no probability space, Lipschitz condition, or tail theorem |
| `LipschitzWith` | metric Lipschitz continuity with a nonnegative constant | no convexity or concentration conclusion |
| `Measure.pi`, `Measure.infinitePi` | finite/infinite product-measure infrastructure | no Talagrand set or function inequality |
| `ProbabilityTheory.HasSubgaussianMGF` and `.measure_ge_le` | an assumed MGF property and its generic upper-tail consequence | assuming sub-Gaussianity would hide the theorem to be proved |

`IntakeProbe.lean` authenticates these names at the pinned revision. A bounded lexical search found
no source-identical Talagrand convex-Lipschitz declaration. Neither observation is an exhaustive
anchor audit, an absence proof, a canonical target, or a proof body.

## Statement gate

Before statement work, accountable reviewers must preserve and independently approve one immutable
primary or authoritative source proposition, resolve the 1995 set-theorem versus 1996 functional-
refinement boundary, and map every incorporated definition, assumption, constant, quantifier,
proof step, correction, erratum, and boundary case. If the root is a corollary of the 1995 convex-
distance theorem, the derivation itself must be explicit and reviewed.

Only then may the statement phase encode the exact Lean target, minimize imports, serialize the
expression and environment, check credited transports, and run the required statement mutations.
Until then the honest provisional vector is `[H1, M4, R4]`: a published complete proof family is
known, but exact statement and source mapping remain unresolved.
