# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6089-6094` supplies exactly the title `Dinic算法`, the attribution
Yefim Dinitz, year 1970, the gloss `最大流的分层算法` ("a layered algorithm for maximum flow"),
high importance, and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula, network or
flow definition, ordered binders, assumptions, algorithm, complexity model, proof boundary,
corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22631-22656` repeats the gloss while explicitly leaving the formal system,
foundations, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

The separate computer-science source record at `Docs/researches/cs_theorems.md:173` and its Stage0
projection `THM-C-0098` say `O(V^2E)或O(VE log V)最大流`. This is useful ambiguity evidence, but it
is a different UID and supplies neither definitions nor a proof. It cannot silently broaden or
replace the Stage1 mathematical row. In particular, the two displayed bounds can describe
different implementation or network regimes rather than interchangeable conclusions.

## Bibliographic source lead

Crossref's publisher record for DOI `10.1007/11685654_10` was inspected on 2026-07-13. It identifies
Yefim Dinitz, *Dinitz' Algorithm: The Original Version and Even's Version*, pages 218-240 in a 2006
Springer volume. The observed JSON payload was 10822 bytes with SHA-256
`711584c4a0f8846ab6120135c54878bdcba727aa393996d8be40fcdcee50ce60`.

Publisher-supplied reference `10_CR4` cites E. A. Dinic, *An algorithm for the solution of the
max-flow problem with the polynomial estimation*, *Doklady Akademii Nauk SSSR* 194(4) (1970), in
Russian, with English translation in *Soviet Mathematics Doklady* 11, pages 1277-1280 (1970).
Reference `10_CR19` separately cites Sleator and Tarjan's 1983 dynamic-tree paper. These
observations support bibliographic identity and the need to audit a material version boundary; the
bibliography alone does not map `O(VE log V)` to a particular implementation. They do not reproduce
or verify the 1970 theorem text, definitions, hypotheses, proof, complexity derivation,
corrections, or errata.

The primary 1970 paper and full 2006 chapter text were not inspected or immutably admitted. This is
therefore an H1 source lead with explicit reconstruction debt, not H0 or an exact source statement.

## Component crosswalk

| Repository or familiar component | Required source decision | Pinned Lean surface | Intake status |
|---|---|---|---|
| "maximum flow" | directed finite network, capacities, feasible flow, value, source/sink, and optimality | no maximum-flow declaration located | proposition definitions open |
| "layered algorithm" | residual distance, level graph, admissible edges, blocking-flow phase, update, and termination | `Quiver.Path`, `SimpleGraph.edist` | generic paths/undirected distance only |
| blocking flow | exact path-blocking or saturation/cut condition and construction | no declaration located | definition and implementation open |
| 1970 "polynomial estimation" | exact original algorithm, input size, cost model, counted vertices/edges, and bound | natural cardinality/arithmetic substrate | source text not inspected |
| companion `O(V^2E)` | decide whether the standard general-network bound belongs to the root | no declaration located | cross-record clue, not authority |
| companion `O(VE log V)` | identify its exact source, algorithm/version, and any required transport | no declaration located | mapping unresolved; must not be merged into the original by name |
| unit-capacity or unit-network variants | define restricted network class and specialized bound | no declaration located | excluded unless source-selected |
| path capacity/bottleneck | minimum positive residual capacity, not additive path weight | `Quiver.Path.addWeight`, `Quiver.Path.weight` | representation substrate; semantics mismatch |
| finite execution state | finite vertices, edges, BFS queue, blocking-flow state, and updates | bounded simple-walk enumeration APIs | no flow or algorithm execution |
| correctness | feasibility invariant, level progress, termination, no augmenting path, maximum flow, optional minimum cut | no exact candidate | entirely open |
| `已验证` | accepted primary-source and kernel evidence would be required | none | rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks quiver
paths and additive weights, simple-graph extended distance and shortest-walk existence, and finite
bounded-walk enumeration. These APIs show that a later model can reuse generic infrastructure.
They do not define directed capacitated networks, feasible flows, residual networks, level graphs,
blocking flows, augmentation, maximum-flow correctness, or asymptotic complexity.

A bounded case-insensitive search of repo-local Lean and pinned mathlib for Dinic/Dinitz,
maximum-flow, residual network, level graph, and blocking flow found no relevant declaration. This
is not the later exhaustive formal-candidate audit and does not establish global absence.

## Open source gate

Before statement freeze or H0, accountable reviewers must obtain an immutable lawful copy of an
approved primary or authoritative source; inspect the exact statement, definitions, assumptions,
algorithm, proof boundary, and corrections/errata; reconcile the layered-algorithm gloss with the
companion complexity wording; and distinguish original, dynamic-tree, and specialized variants.
Only then may the statement phase freeze ordered binders, a cost model, minimal imports, normalized
expression and environment fingerprints, checked alternate encodings, and required statement
mutations.
