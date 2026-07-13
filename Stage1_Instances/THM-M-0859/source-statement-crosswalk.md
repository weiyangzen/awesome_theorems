# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6299-6304` supplies exactly the title `Vizing定理`, attribution to
Vadim Vizing, the year 1964, the gloss `图的边色数` ("the edge chromatic number of a graph"),
importance "high," and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no inequality, graph convention,
definition, bibliography, theorem/page locator, binder, premise, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23441-23466` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected source leads

The permanent Encyclopedia of Mathematics revision `51407`, "Vizing theorem," was inspected on
2026-07-13. It assumes a finite, undirected, loopless graph, allows parallel edges, defines
`mu(G)` as maximum edge multiplicity and `chi'(G)` as the least number of colors in a proper edge
coloring, and identifies Vizing's 1964 result as

`Delta(G) <= chi'(G) <= Delta(G) + mu(G)`.

It explicitly derives the simple-graph specialization
`Delta(G) <= chi'(G) <= Delta(G) + 1` and cites V. G. Vizing, "On an estimate of the chromatic
class of a p-graph," *Diskret. Anal.* 3 (1964), 25-30 (Russian). Its historical note identifies
recoloring as the proof's cornerstone.

Crossref record `10.1007/BF01885700` confirms V. G. Vizing, "The chromatic class of a multigraph,"
*Cybernetics* 1(3) (1965), 32-41. Its reference 19 points to the 1964 paper, and references 20-21
show nearby Vizing publications that must not be conflated with the target. The publisher's full
text was not available through the inspected access path, and the 1964 Russian primary paper was
not obtained or inspected. Thus these leads support provisional `H1`, not `H0`: primary text,
translation fidelity, exact theorem/proof pages, definitions, assumptions, corrections, and
independent review remain open.

## Clause crosswalk

| Repository/source component | Mathematical content | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| graph | finite undirected loopless multigraph in the reference source | a reviewed multigraph representation, or `G : SimpleGraph V` only for the specialization | catalog does not choose; representation open |
| `Delta(G)` | maximum vertex degree, counting parallel edges in the general form | `SimpleGraph.maxDegree` for finite simple graphs | pinned API probed; multigraph degree open |
| `mu(G)` | maximum number of parallel edges joining a vertex pair | absent from `SimpleGraph`, where multiplicity is at most one | exact general encoding open |
| `chi'(G)` | least colors in a proper edge coloring | direct edge-color predicate or line-graph `chromaticNumber`/`Colorable` | minimum/existence transport open |
| proper edge coloring | adjacent edges receive different colors | `G.lineGraph.Coloring` or `G.lineGraph.Colorable n` | line-graph adjacency API probed; equivalence not frozen |
| lower bound | `Delta(G) <= chi'(G)` | separate lower-bound obligation or part of an exact numeric root | root composition decision open |
| Vizing upper bound | `chi'(G) <= Delta(G) + mu(G)` | future multigraph coloring existence statement | source family identified; no Lean multigraph target selected |
| simple corollary | `chi'(G) <= Delta(G) + 1` | `G.lineGraph.Colorable (G.maxDegree + 1)` | plausible simple specialization only; not canonical at intake |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies
`SimpleGraph.edgeSet`, `SimpleGraph.lineGraph`, `SimpleGraph.lineGraph_adj_iff_exists`,
`SimpleGraph.Coloring`, `SimpleGraph.Colorable`, `SimpleGraph.maxDegree`, and
`SimpleGraph.degree_le_maxDegree`. `IntakeProbe.lean` verifies that these declarations elaborate
together and that the prospective simple-graph proposition is well-formed. `EdgeLabeling` assigns
labels to edges but explicitly reserves "edge-colouring" for the unprovided properness condition.

A bounded case-insensitive search of pinned mathlib and repo-local Lean found no Vizing,
chromatic-index/class, or proper edge-coloring theorem. The only edge-colouring wording was the
`EdgeLabeling` distinction just described. This is intake discovery, not the later immutable
candidate audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must lawfully preserve and independently inspect an
immutable primary edition (and any required translation), pinpoint the theorem and proof, map every
definition, binder, premise, conclusion, graph/multiplicity convention, and correction, and decide
whether the catalog root is the multigraph theorem or simple specialization. Only then may the
statement phase freeze the exact Lean expression, minimal imports, direct/line-graph checked
transport, expression and environment hashes, and required domain, binder, hypothesis, and
boundary mutations.
