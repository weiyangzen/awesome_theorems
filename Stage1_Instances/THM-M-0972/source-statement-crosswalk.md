# THM-M-0972 source-statement crosswalk

## Repository source

The authoritative catalog text is `Docs/researches/math_theorems.md:7099-7104`, introduced in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Its Stage0 projection is
`Docs/Stage0_Blueprint.md:26497-26522`.

| Catalog field | Literal content | Intake disposition |
|---|---|---|
| title | Janson inequality | identifies a theorem family |
| proposer | Svante Janson | provenance lead, not a source citation |
| year | 1990 | matches multiple relevant publications |
| statement | probability of the union of rare events | too vague and directionally ambiguous |
| formal status | verified | explicitly untrusted under rev-5.6 |

Stage0 leaves the exact definitions, premises, proof route, dependency graph, alternate formulation,
axioms, and machine artifact unspecified. Nothing in either repository record supplies a formula,
theorem locator, source edition, correction record, or independent review.

## Immutable secondary crosswalk

The inspected `Encyclopedia of Mathematics` entry `Janson inequality`, immutable revision
`oldid=55421` (last edited 2024-02-10), is adapted from an article attributed to A. Rucinski. It is
a secondary source and receives no `H0` credit. It does establish why the repository wording cannot
select a root:

| Secondary node | What it records | Mapping status |
|---|---|---|
| setup | independent random subset of a finite base set; subset configurations and indicators | candidate domain only; exact source definitions unreviewed |
| `lambda`, `Delta`, `DeltaBar` | mean and pairwise-overlap quantities, with an ordered-pair convention | candidate definitions only |
| (a1) | exponential nonoccurrence bound `exp(-lambda + Delta)` | candidate root; not adopted |
| (a2) | quotient-form nonoccurrence bound | candidate root; not adopted |
| (a3) | Boppana-Spencer product refinement | separate authorship and hypotheses; not adopted |
| (a4) | Janson's 1990 full lower-tail estimate and quadratic weakening | candidate root; not adopted |
| Suen paragraph | a related arbitrary-indicator dependency-graph inequality | explicit non-substitute |

The entry says several inequalities carry the name. It also shows that nonoccurrence is the
complement of a union, while the catalog mentions the union probability without a direction or
formula. A source reviewer must resolve that discrepancy rather than silently complement or weaken
the theorem.

## Primary-source leads not yet admitted

1. S. Janson, T. Luczak, and A. Rucinski, *An exponential bound for the probability of
   nonexistence of a specified subgraph in a random graph*, in *Random Graphs '87*, Wiley, 1990,
   pp. 73-87. The immutable secondary entry associates it with a symmetry-restricted precursor of
   the quotient-form bound. Full text, incorporated definitions, theorem locator, assumptions,
   proof boundary, corrections, and independent review were not inspected here.
2. S. Janson, *Poisson approximation for large deviations*, *Random Structures & Algorithms*
   1(2), June 1990, DOI `10.1002/rsa.3240010209`. Crossref metadata gives pp. 221-229 and an abstract
   describing upper and lower bounds for `P(S <= k)` for a specially structured sum of indicators;
   the encyclopedia gives pp. 221-230 and attributes the general lower-tail form to this paper. The
   page discrepancy, exact formulas, definitions, assumptions, proof boundary, errata, and
   independent review remain open.

These are named source leads with a published complete theorem family, supporting provisional
`H1`. A citation and secondary formula table do not satisfy the rev-5.6 `H0` contract.

## Lean crosswalk

| Pinned module/declaration | Relevance | Boundary |
|---|---|---|
| `ProbabilityTheory.setBernoulli` | independent random-subset law with one parameter | no inhomogeneous source map or Janson theorem |
| `ProbabilityTheory.iIndepSet` | independence of event families | generic substrate only |
| `iIndepSet.meas_biInter` | measurable finite intersections | no configuration-count bound |
| `iIndepSet.iIndepFun_indicator` | event-to-indicator independence bridge | no dependent-overlap estimate |
| `measure_le_le_exp_mul_mgf` / `measure_le_le_exp_cgf` | generic lower-tail Chernoff interfaces | bound still requires a Janson-specific mgf estimate |
| `measure_biUnion_finset_le` | elementary finite union bound | explicitly a non-substitute |
| `SimpleGraph.binomialRandom` | `G(V,p)` probability law | an application space, not the general inequality; its module's unrelated `proof_wanted` gets no credit |

A bounded case-insensitive search for `janson` across repo-local Lean and pinned mathlib returned no
match. This is an intake discovery observation, not the exhaustive external anchor audit.

An immutable temporary source archive of `facebookresearch/atlas-lean` commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50` was also inspected without installing it into `.lake`.
Its pinned toolchain is Lean 4.29.0 and its mathlib revision matches this repository. The exact-topic
file `Atlas/ProbabilisticMethodsInCombinatorics/code/Janson.lean` defines `JansonSetup` and theorems
named `janson_inequality_I`, `janson_parametric_bound`, and `janson_inequality_II_full`. However,
the first root depends on `janson_chain_rule_harris := by sorry`, while the second depends on
`janson_parametric_bound := by sorry`. The companion `Chapter8/LowerTails.lean` lower-tail theorem
depends on `janson_III_intermediate_bound := by sorry`; its algebraic Chapter 8 optimizer consumes
an assumed parametric bound and does not close that premise. The archive therefore supplies a
credible exact-topic anchor but no proof credit (`M5` for the candidate; root remains `M4`). Its
root license is CC BY-NC 4.0 with a no-training rider, so compatibility must also be decided before
any integration. No build or complete transitive audit of that external project is claimed here.
The archive and inspected-file digests in `instance.json` are discovery metadata only: the temporary
external bytes are not durable receipt inputs, and the local checker does not authenticate them.
Any later admission must independently reacquire or lawfully preserve and content-address the source.

## Open source gates

- select and lawfully preserve one immutable primary proposition or explicit conjunction;
- independently transcribe and review every definition, binder, hypothesis, inequality, and boundary;
- map the catalog's union wording to the selected nonoccurrence or lower-tail conclusion;
- reconcile authorship, 1990 source roles, and the `221-229` versus `221-230` pagination;
- audit corrections and errata and map the proof's material transitions to later obligation nodes;
- independently approve the source-to-Lean encoding before statement acceptance.
- audit the Atlas candidate's exact statement relationship, all transitive placeholders and axioms,
  build feasibility, provenance, and restrictive license before any integration decision.

Until those gates close, the canonical statement and expression fingerprint remain null, the human
status is no stronger than `H1`, and no proof or theorem-completion claim is available.
