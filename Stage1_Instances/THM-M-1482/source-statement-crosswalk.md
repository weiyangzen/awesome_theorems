# THM-M-1482 source-statement crosswalk

## Repository source and provenance

The complete upstream record is `Docs/researches/math_theorems.md:10833-10838`:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `遗传算法` | names the genetic-algorithm family |
| proposer | `John Holland` | historical attribution only |
| time | `1975` | bibliographic lead only |
| statement | `基于进化的优化算法` | topic/purpose gloss, not a proposition |
| importance | `高` | scheduling metadata only |
| formalization status | `已验证` | explicitly untrusted; no H/M credit |

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The source gives no bibliography, edition,
page, theorem, definitions, binders, assumptions, conclusion, proof, correction record, or formal
artifact. `Docs/Stage0_Blueprint.md:40297-40322` repeats the gloss while expressly leaving the
definitions and premises, proof path, dependencies, foundation, axioms, machine status, and
artifact links open.

## Historical primary-source leads, not H0 evidence

1. John H. Holland, *Adaptation in Natural and Artificial Systems: An Introductory Analysis with
   Applications to Biology, Control, and Artificial Intelligence*, University of Michigan Press,
   1975. This matches the catalog attribution and year, but the catalog does not cite it and this
   intake has not admitted an immutable edition or inspected an exact theorem passage.
2. John H. Holland, "Genetic Algorithms and the Optimal Allocation of Trials," *SIAM Journal on
   Computing* 2(2) (1973), 88-105, DOI `10.1137/0202009`. Crossref metadata confirms this
   bibliographic identity; Semantic Scholar reports its full text closed. Its year differs from the
   catalog and no statement mapping is accepted.

These leads establish only a plausible source family. They do not tell us whether the intended
root is a schema statement, an allocation result, an algorithm specification, or a later
convergence theorem. No edition, theorem/page, premise-to-conclusion mapping, correction audit, or
independent review is credited.

## Source-to-statement crosswalk

| Source element | Mathematical information actually fixed | Lean information required | Result |
|---|---|---|---|
| `遗传算法` | population-based evolutionary search family | exact genotype/population types and generation operator | family only; open |
| `基于进化` | selection and inherited variation in a broad sense | typed selection, crossover, mutation, replacement, and randomness semantics | components unidentified |
| `优化算法` | an intended search/optimization use | fitness/objective, constraints, optimizer notion, correctness or performance conclusion | conclusion unidentified |
| John Holland | historical source-family attribution | admitted edition and exact source-node map | lead only |
| 1975 | likely book-era locator | immutable edition, page/theorem, definitions, corrections | lead only |
| `已验证` | metadata screening claim | accepted source review or kernel receipt | no credit |

The literal gloss has no connective or conclusion whose truth Lean can check. It fixes neither an
algorithm nor what must be proved about one. Consequently no ordered binder, hypothesis, conclusion,
canonical expression, alternate encoding, or expression hash can be populated truthfully at intake.

## Non-equivalent candidate statement families

| Candidate | Material choices not supplied by the catalog | Intake decision |
|---|---|---|
| Holland schema theorem | schema representation, proportional selection convention, crossover/mutation model, expectation/bound form, finite-population approximation | not selected |
| finite-state reachability/convergence | transition kernel, elitism, mutation support, irreducibility/absorption, optimizer set, convergence mode | not selected |
| generation well-definedness | population carrier/size, selection normalization, offspring validity, replacement | not selected |
| executable correctness | program, random-state semantics, reference transition, refinement relation, termination | not selected |
| complexity/approximation | input encoding, problem class, cost model, probability and approximation parameters | not selected |

These claims are not interchangeable. In particular, a stochastic process reaching an optimum
under full-support mutation is not Holland's schema theorem, and a schema expectation bound is not
global convergence or implementation correctness.

## Pinned Lean substrate boundary

`IntakeProbe.lean` checks generic operations from:

- `Mathlib.Data.Multiset.Bind`: `Multiset.map`, `Multiset.bind`, population-like flattening, and a
  cardinality identity; and
- `Mathlib.Probability.ProbabilityMassFunction.Constructions`: `PMF.map`, `PMF.bind`, support
  mapping, and bind associativity.

These declarations can model fragments of a future source-selected transition. They do not supply
fitness semantics, genetic operators, a complete generation kernel, or any genetic-algorithm
result. A bounded case-insensitive search for `genetic algorithm`, `genetic programming`,
`evolutionary algorithm`, `evolutionary computation`, `schema theorem`, and `Holland` found no
occurrence in repo-local Lean or pinned mathlib. This is discovery evidence with a bounded query
list, not an exhaustive absence claim or downstream anchor audit.

## Source exit gate

Before statement execution, an independent reviewer must approve a lawful immutable source edition,
pinpoint result and proof boundary, all incorporated definitions, assumptions and corrections, and
a row-by-row mapping to one canonical mathematical claim. Only then may the statement phase freeze
the exact Lean expression, imports, environment fingerprint, transports, and required mutations.
Until that gate passes, the honest classification is `[H5, M4, R4]`, and all proof, audit, and
completion claims remain open.
