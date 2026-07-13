# THM-M-1483 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10840-10845` supplies exactly the title `粒子群优化`, attribution
to James Kennedy and Russell Eberhart, year 1995, gloss `基于群体智能的优化`, importance `high`,
and status `已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no recurrence, objective,
domain, random model, binder, hypothesis, conclusion, theorem/page locator, proof, correction
record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:40324-40349` repeats the gloss while explicitly leaving the formal system,
precise definitions and premises, proof route, dependencies, alternate forms, axioms, machine
status, and artifact links open. Its generic closed-result and leaf-audit wording is planning
metadata, not evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets this target
to `L0 / rework_required`.

## Inspected bibliographic source lead

Crossref and DBLP identify James Kennedy and Russell Eberhart, *Particle swarm optimization*,
Proceedings of ICNN'95 - International Conference on Neural Networks, volume 4, pages 1942-1948,
1995, DOI `10.1109/ICNN.1995.488968`; DBLP record key `conf/icnn/KennedyE95`. This closely matches
the catalog authors, title, and year.

Semantic Scholar's abstract describes the work as introducing a nonlinear-function optimization
concept, outlining multiple paradigms, discussing one implementation, describing benchmark tests,
and proposing applications. Unpaywall reports closed access and no repository copy; the attempted
IEEE PDF endpoint did not provide the article. Thus no primary article body, exact algorithm
definition, theorem passage, complete assumptions, proof, correction history, or errata were
inspected. Bibliographic services are mutable discovery leads, and the catalog does not cite this
paper. No independent source reviewer admitted it. This is not `H0`.

## Literal statement crosswalk

| Repository component | Required mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| particle swarm optimization | one exact algorithm variant or theorem about it | state type and exact transition or quantified `Prop` | family label only; target kind open |
| swarm intelligence | particle indices, neighborhood information, personal/social memory | finite index types, topology, state and best-update definitions | all objects and semantics absent |
| optimization | objective, search domain, optimum notion, observable and logical conclusion | objective function, feasible set, `IsMinOn` or source-specific predicate | no domain, assumptions, or conclusion |
| Kennedy/Eberhart, 1995 | historical attribution and likely ICNN'95 source family | provenance only | no cited work or admitted passage |
| verified | inventory screening label | accepted source and kernel receipts | explicitly rejected as evidence |

The literal record cannot populate a canonical domain, ordered binders, hypotheses, conclusion,
alternate encodings, degenerate cases, or Lean expression fingerprint.

## Candidate-meaning boundary

Defining an update rule proves no convergence. A deterministic spectral-stability theorem for a
linearized recurrence says nothing automatically about stochastic global-best PSO. Convergence of
positions, velocities, stored best positions, and stored best objective values are distinct.
Almost-sure, in-probability, mean, and mean-square convergence are distinct. Convergence to an
equilibrium need not mean convergence to a local or global optimum. A finite-domain global-hitting
theorem usually requires an exploration or irreducibility assumption absent from the catalog.
Empirical benchmark improvement is not a universal mathematical result.

Choosing any one of these meanings solely from the algorithm title would invent proposition-changing
mathematics. No checked equality, `Iff`, or implication between candidate formulations is credited.

## Pinned Lean crosswalk

| Candidate | What the pinned declaration supplies | Why it is not the target |
|---|---|---|
| `Finset.exists_min_image` | existence of a least value in the image of a nonempty finite set | no PSO state, update, randomness, or discovery process |
| `isFixedPt_of_tendsto_iterate` | an iteration limit is a fixed point under continuity | assumes convergence and has no optimization semantics |
| `ContractingWith.tendsto_iterate_fixedPoint` | iterates of a contraction converge to its fixed point | no evidence that a PSO transition is a contraction or that its fixed point is optimal |

`IntakeProbe.lean` checks these declarations at the pinned revision and reports axioms for three
adjacent library lemmas. The probe and bounded topic search are discovery evidence only, not a
canonical target, PSO proof body, exhaustive anchor audit, or absence proof.

## Neighbor boundary

Simulated annealing (`THM-M-1481`), genetic algorithms (`THM-M-1482`), Monte Carlo methods
(`THM-M-1479`), quasi-Monte Carlo methods (`THM-M-1480`), optimization theory (`THM-M-1490`), and
convex optimization (`THM-M-1491`) have separate catalog ownership. Related definitions or
theorems may later become explicit dependencies, but none selects or proves this target by
proximity.

## Source gate

The first downstream gate requires an accountable correction that selects and preserves one exact
immutable-source proposition; maps the PSO variant and update order, state spaces, swarm and
topology, objective and optimum notion, random variables and independence, initialization,
coefficient regime, arithmetic, observable, convergence or other conclusion, quantifier order, and
every boundary case; audits the incorporated proof and corrections; and receives independent
optimization/source review. Only then may the statement phase freeze the Lean expression, minimal
imports, checked transports, and required mutations.

Until then, `H5` records that the catalog algorithm-family label is not yet a stable truth-valued
proposition, `M4` records the lack of a source-identical usable formal artifact, and `R4` records the
lack of an anchorable proof reconstruction. These classifications do not say that established PSO
results are false or open.
