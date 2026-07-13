# THM-M-1479 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10791-10796` supplies exactly the title `Monte Carlo方法`,
attribution `Stanislaw Ulam/John von Neumann`, year `1946`, gloss `基于随机采样的数值方法`,
importance "high," and status `已验证`. Git provenance places all six uncited lines in repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, quantity to
approximate, probability model, estimator, binder, hypothesis, conclusion, proof, theorem locator,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:40216-40241` repeats the gloss while explicitly leaving exact definitions
and premises, proof or observation, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Its generic closed-result and leaf-audit wording is planning metadata, not
evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| random sampling | iid draws, dependent chain, stratification, importance law, or another process | probability space plus random variables or a kernel | no law supplied |
| numerical method | estimator or randomized algorithm | exact recurrence/output and sample-size convention | no algorithm supplied |
| based on | approximation, convergence, error, or complexity relationship | ordered hypotheses and a truth-valued conclusion | no relationship stated |
| Monte Carlo | integration, probability estimation, simulation, optimization, or a broad family | target quantity, domains, error notion, and computation profile | no branch selected |
| Ulam/von Neumann, 1946 | historical origin metadata | immutable edition and pinpoint proposition | no locator supplied |
| `已验证` | untrusted screening label | reviewed source or kernel receipt would be required | no H or M credit |

The gloss cannot populate a canonical domain, ordered binders, hypotheses, conclusion, alternate
encodings, excluded cases, or Lean expression fingerprint.

## Historical source-family lead, not an admitted source

Crossref metadata was inspected on 2026-07-13 for Nicholas Metropolis and S. Ulam, "The Monte
Carlo Method," *Journal of the American Statistical Association* 44(247), September 1949, pages
335-341, DOI `10.1080/01621459.1949.10483310`. The deterministic metadata projection has SHA-256
`d4061580fd50532e28d984325f3ca201629efe280e4653969e6d2e43e26d7dbf`.

This article is a plausible history lead, not the repository-selected statement: the catalog says
1946 and Ulam/von Neumann, while the article is 1949 and Metropolis/Ulam. Moreover,
`Docs/researches/physics_theorems.md:955-961` separately records a 1949 Metropolis/Ulam Monte Carlo
target for statistical mechanics. No complete article, exact theorem passage, assumptions, proof
boundary, corrections, or independent review was admitted. The record is `E5` discovery evidence
and establishes neither target identity nor `H0`.

## Neighbor and Lean boundary

The repository separately schedules laws of large numbers (`THM-M-0983` through `THM-M-0986`),
central-limit results, MCMC and named samplers (`THM-M-1100` through `THM-M-1103`), quasi-Monte
Carlo (`THM-M-1480`), and the physics target `THM-P-0108`. Their statements, sources, and proof
receipts are not inherited.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Probability.StrongLaw` and `Mathlib.Probability.Moments.Variance` provide expectation,
independence, identical-distribution, variance, Chebyshev-bound, and strong-law interfaces.
`IntakeProbe.lean` checks representative declarations in the pinned environment. These APIs do not
define a Monte Carlo estimator or select an approximation theorem. The strong law is especially
adjacent but not source identity for this root. A bounded exact-topic search found no
source-selected `THM-M-1479` terminal declaration. This is intake discovery, not an exhaustive
anchor audit, global absence claim, or proof evidence.

## Source exit gate

Before leaving `H5`, accountable reviewers must redirect the method-family label to one corrected,
truth-valued proposition; preserve an immutable primary or authoritative edition; select an exact
theorem/section/page and proof boundary; map every target quantity, probability law, estimator,
ordered binder, hypothesis, moment/regularity condition, conclusion, rate, constant, computation
boundary, and degenerate case; reconcile neighboring targets; audit corrections; and obtain
independent probability/numerical-analysis and source review.

Only then may the statement phase freeze minimal imports, elaborate and preserve the identical Lean
expression and environment fingerprint, compile checked transports, and mutation-test a removed
hypothesis, changed domain, changed binder scope, and boundary case. Until then no exact statement,
H0, M0, R0, proof, audit completion, or theorem completion is claimed.
