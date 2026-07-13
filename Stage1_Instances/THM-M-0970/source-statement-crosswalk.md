# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7085-7090` supplies exactly the title `Moser-Tardos算法`, the
attribution Robin Moser/Gabor Tardos, the year 2010, the gloss `Lovász局部引理的构造性证明`
("a constructive proof of the Lovasz Local Lemma"), importance "high," and status `已验证`.
Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem locator,
formula, definitions, ordered binders, algorithm, probability or complexity conclusion, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26443-26468` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected primary source lead

Robin A. Moser and Gabor Tardos, *A constructive proof of the general Lovasz Local Lemma*, arXiv
`0903.0544v3` (submitted 3 March 2009; version 3 dated 20 May 2009), later *Journal of the ACM*
57(2), 2010, article 11, pages 11:1-11:15, DOI `10.1145/1667053.1667060`, was inspected. The archived
version-3 PDF has SHA-256
`394a21143451acad99ae93e934dc12a5d7df4da68659b8060786fdd8a9665a0c`.

In the archived version, Section 1 defines the determining-variable set `vbl(A)`, the dependency
graph by overlap of those sets, and the sequential resampling procedure as Algorithm 1.1. Theorem
1.2 on printed page 3 states the central result. For finite mutually independent random variables
and finitely many events determined by them, suppose `x(A)` lies strictly between zero and one and
each bad-event probability is at most `x(A)` times the product of `1 - x(B)` over events sharing a
determining variable with `A`. Then a satisfying valuation exists; moreover Algorithm 1.1 resamples
each event at most `x(A)/(1-x(A))` times in expectation, and the expected total resampling count is
bounded by the corresponding finite sum. Sections 2 and 3 prove this via execution logs, proper
witness trees, and a branching-process bound.

This establishes an `H1` source lead, not `H0`. The catalog does not cite or adopt this edition or
pinpoint theorem. A bounded comparison found the Theorem 1.2 formula and conclusions unchanged from
arXiv v1 through v3; v3 adds the assumption that `vbl(A)` is supplied to algorithms and clarifies
parts of the witness-tree proof. No correction or erratum was identified in the arXiv history or
Crossref relation fields, but that negative check is not exhaustive. The journal-versus-archive
semantic delta, every incorporated definition and proof node, and the relation between the prose
word "constructive" and randomized expected termination have not been independently reviewed. A
later source review must also decide whether the root is Theorem 1.2 alone or another explicitly
approved package. Theorem 1.3 (parallel algorithm), Theorem 1.4 (deterministic algorithm), and the
Section 6 lopsided version are related extensions, not automatically part of this singular catalog
target.

## Clause crosswalk

| Catalog/source component | Candidate Theorem 1.2 component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Lovasz Local Lemma" | asymmetric product criterion for a finite bad-event family | finite event type, probability measure, `Measure`, `Finset.prod` | exact numeric codomain and casts open |
| underlying variables | finite mutually independent random variables, each with its distribution | dependent family of measurable value types and `ProbabilityTheory.iIndepFun`, or finite PMFs | probability-space encoding open |
| event determination | each bad event is determined by its minimal variable set `vbl(A)` | measurable cylinder events plus finite support/determination predicate | no pinned determination API located |
| dependency neighborhood | distinct events whose determining-variable sets intersect | `Finset` support intersection or a `SimpleGraph` | source minimality and graph transport open |
| constructive procedure | initialize independently; repeatedly choose any violated event and resample its variables independently | stochastic transition/kernel, scheduler, execution log, stopping time | algorithm and scheduler semantics open |
| termination/output | find a valuation violating no event | almost-sure termination plus terminal-state correctness, with a checked existential consequence | exact termination formulation open |
| quantitative guarantee | expected resamplings of `A` at most `x(A)/(1-x(A))`, total bounded by the finite sum | event-count random variables and integrals/expectations | arithmetic type and integrability open |
| `已验证` | untrusted inventory label | kernel receipt and source review would be required | no H0 or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, indexed independence,
finite product-law, probability measure, PMF, and moment/integral APIs are available.
`IntakeProbe.lean` checks representative declarations without defining a target. A bounded search
of pinned mathlib and repo-local Lean found no exact Moser-Tardos, algorithmic local-lemma, witness
tree, or resampling declaration. This is scoped intake discovery, not the later immutable external
anchor audit and not a global absence theorem.

Before leaving `H1`, accountable reviewers must preserve an approved immutable source edition,
reconcile it with the journal version, audit corrections and errata, select the exact proposition,
map all incorporated definitions, assumptions, algorithm steps, proof nodes, and conclusions, and
independently approve fidelity. Only then may the statement phase freeze an exact Lean target,
minimal imports, expression and environment fingerprints, checked alternate encodings, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
