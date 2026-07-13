# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6082-6087` supplies exactly the title `Edmonds-Karp算法`, the
attribution Jack Edmonds/Richard Karp, year 1972, the gloss `最大流的多项式算法` ("a
polynomial-time algorithm for maximum flow"), high importance, and status `已验证`. Git history
attributes all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has
no bibliography, formula, network or flow definition, ordered binders, assumptions, algorithm,
complexity model, proof boundary, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22604-22629` repeats the gloss while explicitly leaving the formal system,
foundations, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

The separate computer-science source record at `Docs/researches/cs_theorems.md:172` and its Stage0
projection `THM-C-0097` say `O(VE^2)最大流算法`. This is valuable ambiguity evidence: it makes a
usual complexity gloss explicit, but it is a different UID outside the theorem's owned Stage1
record and supplies no definitions or proof. It cannot silently broaden the mathematical row.

## Bibliographic source lead

Crossref's DOI record for `10.1145/321694.321699` was inspected on 2026-07-13. It identifies Jack
Edmonds and Richard M. Karp, *Theoretical Improvements in Algorithmic Efficiency for Network Flow
Problems*, *Journal of the ACM* 19(2), April 1972, pages 248-264. The observed JSON payload had
SHA-256 `25aa7ca0f3f4b1e93644a2e83cd5e2ea03639615f87502f8d579c0e46622d079` and 5971 bytes.
DBLP independently returned the same title, authors, venue, volume, pages, year, and DOI.

The ACM primary paper PDF returned HTTP 403 in this worker environment, so its theorem statements,
definitions, hypotheses, algorithm variants, proofs, corrections, and errata were not inspected.
Bibliographic agreement identifies a high-quality source lead but is not `H0` or an exact source
statement. The provisional H1 classification records a published result believed complete with an
explicit unresolved mapping list; it does not claim primary-text review.

## Component crosswalk

| Repository or familiar component | Required source decision | Pinned Lean surface | Intake status |
|---|---|---|---|
| "maximum flow" | directed finite network, capacities, feasible flow, value, source/sink, and optimality | no maximum-flow declaration located | proposition definitions open |
| "algorithm" | residual representation, shortest augmenting path, BFS/tie rule, bottleneck, update, and termination | `Quiver.Path`, `SimpleGraph.Walk` | generic paths only |
| "polynomial" | input encoding, cost model, counted vertices/edges, regime, and quantified bound | natural cardinality/arithmetic substrate | no complexity contract selected |
| companion `O(VE^2)` | decide whether this exact worst-case bound belongs to the root | no declaration located | cross-record clue, not authority |
| shortest path by edge count | source-directed residual reachability and minimum number of residual edges | `SimpleGraph.edist`, `SimpleGraph.Reachable.exists_walk_length_eq_edist` | undirected adjacent theorem only |
| path capacity/bottleneck | minimum positive residual capacity, not additive or multiplicative path weight | `Quiver.Path.addWeight`, `Quiver.Path.weight` | representation substrate; semantics mismatch |
| finite execution state | finite vertices, edges, walks, queues, and state updates | bounded simple-walk enumeration APIs | no BFS or residual-update correctness |
| correctness | feasibility invariant, termination, no augmenting path, maximum flow, optional minimum cut | no exact candidate | entirely open |
| `已验证` | accepted primary-source and kernel evidence would be required | none | rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks quiver
paths and additive weights, simple-graph extended distance and shortest-walk existence, and finite
bounded-walk enumeration. These APIs show that a later model can reuse some generic infrastructure.
They do not define directed capacitated networks, feasible flows, residual networks, augmentation,
BFS state, maximum-flow correctness, or asymptotic complexity.

A bounded case-insensitive search of repo-local Lean and pinned mathlib for Edmonds-Karp,
Ford-Fulkerson, maximum/minimum flow, augmenting paths, and residual networks found no relevant
declaration. This is not the later exhaustive formal-candidate audit and does not establish global
absence.

## Open source gate

Before statement freeze or H0, an accountable reviewer must obtain an immutable lawful copy of an
approved primary or authoritative source; inspect the exact statement, definitions, assumptions,
algorithm, proof boundary, and corrections/errata; reconcile the repository's generic polynomial
gloss with the companion `O(VE^2)` wording; and map every proposition component and boundary case.
Only then may the statement phase freeze ordered binders, a cost model, minimal imports, normalized
expression and environment fingerprints, checked alternate encodings, and the four required
statement mutations.
