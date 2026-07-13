# THM-M-0879 source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6439-6444` supplies exactly the title `多商品流`, attribution
`众多数学家`, period `20世纪`, gloss `多种商品的并发流`, importance `高`, and status `已验证`.
All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no network model, capacity or commodity
data, flow definition, objective, ordered binder, hypothesis, conclusion, theorem locator, proof,
correction record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23981-24006` repeats the gloss while explicitly leaving the formal
system, foundations, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic closed-result and leaf-audit prose is
planning metadata, not theorem evidence. Rev-5.6 retains `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `多商品流` | flow for several commodities sharing a network | one exact network, commodity, capacity, and flow encoding | subject identified; definitions open |
| `多种商品` | finite terminal-demand family or all ordered vertex pairs | commodity index, endpoints, demands, and quantifier order | data and boundary cases open |
| `并发流` | simultaneous feasibility or a common throughput factor | conservation, demand satisfaction, shared capacity, and objective predicates | meaning and conclusion open |
| `众多数学家`, `20世纪` | broad historical attribution | immutable primary edition and theorem/page map | no source credit |
| `已验证` | untrusted inventory metadata | accepted source and kernel receipts | no H or M credit |

The wording never states what is to be proved. Merely defining a multicommodity flow, or asserting
that a supplied routing is feasible, would broaden or substitute the catalog target rather than
recover a missing theorem.

## Bibliographic leads not selected

T. C. Hu, *Multi-Commodity Network Flows*, *Operations Research* 11(3), 344-360 (1963), DOI
`10.1287/opre.11.3.344`, is a primary-topic lead. Crossref metadata describes a capacitated
network and a generalization of max-flow/min-cut for maximum simultaneous flows of two commodities.
The catalog does not name Hu, restrict to two commodities, select the symmetric-capacity model, or
cite a theorem or page. The paper itself, theorem text, assumptions, proof boundary, published
corrections, and independent review were not available to this intake.

Farhad Shahrokhi and D. W. Matula, *The maximum concurrent flow problem*, *Journal of the ACM*
37(2), 318-334 (1990), DOI `10.1145/77600.77620`, is another primary-topic lead. Crossref metadata
defines throughput as supplied flow divided by demand, maximizes a common throughput under capacity
constraints, and reports an approximation scheme, an optimization dual, and a path-cut duality for
arbitrary demands and uniform capacity. These are several distinct claims. The catalog cites none
of them and does not select all-pairs demands, uniform capacity, an approximation theorem, or a
duality theorem. The article text and theorem locators, corrections, full assumption map, and
independent review remain uninspected.

The observed Crossref response digests are recorded in `instance.json` and the provisional worker
receipt. Crossref is mutable bibliographic and abstract metadata, not a primary theorem edition and
not H0 evidence. The two leads demonstrate ambiguity; they do not resolve it.

## Candidate-meaning boundary

A feasible simultaneous routing is not the same proposition as existence of an optimal common
throughput. Maximum total multicommodity flow differs from maximum concurrent flow. Fractional path
flow differs from integral or unsplittable routing. LP strong duality, a path-cut theorem, a
flow-cut gap, and a polynomial-time approximation guarantee add different definitions and
conclusions. A two-commodity or uniform-capacity theorem cannot silently stand for arbitrary
commodities and capacities.

Selecting among those meanings without a source decision would invent mathematics. The provisional
human-source classification is therefore `H5`: the received catalog wording is not yet a stable
proposition. This classifies the repository target, not the truth or historical status of standard
multicommodity-flow results.

## Pinned Lean crosswalk

| Declaration | What it supplies | Why it is not the target |
|---|---|---|
| `Graph`, `Graph.IsLink`, `Graph.Inc` | undirected multigraph incidence | no capacities, commodities, orientation, or flow conservation |
| `Graph.banana` | a parallel-edge graph example | no network-flow statement |
| `SimpleGraph.Walk`, `SimpleGraph.Path` | finite walks and simple paths | no path weights, demand routing, or shared capacity constraint |
| `Finset.sum` | generic finite aggregation | no flow value, congestion, or optimization theorem |

`IntakeProbe.lean` checks these adjacent pinned declarations. The bounded no-match search and probe
are not a canonical target, exhaustive anchor audit, formal absence proof, or terminal proof body.

## Source gate

Before the statement phase can close, accountable reviewers must select one immutable primary or
authoritative proposition and map every incorporated definition, ordered binder, premise,
conclusion, theorem/page locator, proof boundary, version difference, correction, and degenerate
case. They must also reconcile the boundaries with the related Stage1 targets. A formal reviewer
must then map only that claim to a minimal-import Lean expression and checked transports.

Until then no canonical mathematical or Lean statement, accepted source, expression fingerprint,
proof body, H0, M0, R0, audit completion, or theorem completion is claimed.
