# THM-M-0824 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6054-6059` supplies exactly the title `Prim算法`, attribution
Robert Prim, year 1957, gloss `最小生成树的另一种算法`, importance `高`, and status `已验证`.
All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no graph or weight definition,
algorithm, ordered binder, assumption, conclusion, theorem/page locator, proof, correction record,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22496-22521` repeats the gloss while explicitly leaving the formal
system, precise definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic closed-result and leaf-audit text is planning
metadata, not evidence. Rev-5.6 retains `已验证` only as untrusted metadata and starts this target at
`L0 / rework_required`.

## Related repository wording

`Docs/researches/cs_theorems.md:170` contains a second record, `Prim算法正确性`, with the gloss
`Prim最小生成树算法正确`, Robert Prim, and 1957. Its Stage0 projection is `THM-C-0095` at
`Docs/Stage0_Blueprint.md:83999-84026`; that projection leaves the computation model, resource
measure, exact premises, executable specification, proof, and artifact link open.

`THM-C-0095` is absent from the closed 1546-target rev-5.6 manifest. The repository exposes no
accepted alias or deduplication crosswalk proving how its wording relates to `THM-M-0824`.
Accordingly it is useful discovery metadata but cannot broaden this target, select an exact
statement, or contribute source or proof credit.

## Bibliographic lead

Crossref metadata identifies R. C. Prim, *Shortest Connection Networks And Some Generalizations*,
*Bell System Technical Journal* 36(6), November 1957, pages 1389-1401, DOI
`10.1002/j.1538-7305.1957.tb01515.x`. The authorship, date, and subject are a strong match for the
catalog family. Unpaywall reports the article closed with no open location.

Only mutable bibliographic metadata was observed. The repository does not cite the article; no
article body, exact definition, algorithm passage, theorem, page-specific premise/conclusion map,
proof boundary, correction history, or errata was inspected or independently reviewed. This lead
therefore supplies neither a selected root nor H0 evidence.

## Literal crosswalk

| Repository component | Required mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| Prim algorithm | one exact state transition and execution semantics | state/result types and transition or recursive function | family name only |
| minimum spanning tree | input graph, weights, spanning/tree predicate, total weight, and minimality | `SimpleGraph`, tree/spanning encoding, edge-weight sum, `IsLeast`-style conclusion | every representation and convention open |
| another algorithm | relationship to other MST algorithms, if any | checked equivalence/refinement only if source-relevant | descriptive phrase, not a proposition |
| Robert Prim, 1957 | provenance and possible historical source | provenance only | uncited attribution; bibliographic lead not admitted |
| verified | catalog screening field | accepted source and kernel receipts | explicitly rejected as evidence |

The literal record cannot populate a canonical domain, ordered quantifiers, hypotheses, conclusion,
alternate encodings, degenerate cases, or Lean expression fingerprint.

## Candidate-meaning boundary

Spanning-tree existence is weaker than algorithm correctness. A run that returns a tree may still
return a nonminimal tree. A proof that each step chooses a least frontier edge needs a cut/exchange
argument before it implies global optimality. A nondeterministic specification can be correct for
every tie choice without fixing the same output tree. Distinct weights may imply uniqueness, but
that stronger hypothesis is absent. Correctness under exact weights does not establish a heap
implementation, finite-precision behavior, or any complexity bound.

Choosing any one of these formulations from the title alone would invent proposition-changing
mathematics. No checked equality, `Iff`, implication, or refinement between them is credited.

## Pinned Lean crosswalk

| Declaration | What it supplies | Why it is not the target |
|---|---|---|
| `SimpleGraph.Subgraph.IsSpanning` | a spanning predicate for a simple-graph subgraph | no weights, algorithm, tree property, or optimality |
| `SimpleGraph.IsTree` | connectedness plus acyclicity for a simple graph | no relationship to an input graph or minimum total weight |
| `SimpleGraph.Connected.exists_isTree_le` | existence of a tree subgraph of a connected simple graph | existential tree substrate, not construction by Prim or minimality |
| `SimpleGraph.edgeFinset` | a finite set of graph edges under finiteness assumptions | no weight sum, frontier, selection, state, or correctness |

`IntakeProbe.lean` checks these declarations at the pinned revision. A bounded exact-topic search
found no named Prim/minimum-spanning-tree correctness declaration in repo-local Lean or pinned
mathlib. The probe and bounded search are discovery evidence only, not a canonical target,
exhaustive anchor audit, absence proof, or proof body.

## Source gate

The first downstream gate requires accountable reviewers to select an immutable source proposition
and map the graph representation, finiteness, connectedness, weights and order, start vertex,
frontier and tie rule, state invariant, termination, output, exact correctness conjunction,
quantifier order, boundary cases, proof passage, and corrections. A formal reviewer must then map
that claim to a minimal-import Lean expression and checked transports without using a neighboring
algorithm or a stronger assumption as a substitute.

Until that happens, `H5` records that the catalog algorithm-family wording is not yet a stable
truth-valued proposition, `M4` records the lack of a source-identical usable formal artifact, and
`R4` records the lack of an anchorable proof reconstruction. These classifications do not say that
established Prim correctness theorems are false or open.
