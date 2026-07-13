# THM-M-0971 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7092-7097` supplies exactly the title `Shearer bound`, James
Shearer, 1985, the gloss `optimal condition for the Lovasz Local Lemma`, high importance, and the
status `verified` (English translations of the catalog's Chinese fields). All six uncited lines
originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26470-26494` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `verified` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Primary-source lead

Crossref and the publisher identify J. B. Shearer, *On a problem of spencer*, Combinatorica 5(3)
(September 1985), 241-245, DOI `10.1007/BF02579368`. The publisher abstract describes events
`X_1,...,X_n` with probabilities `rho_i`, a graph `G` encoding independence from nonneighbors, and
`rho`, the probability that no event occurs. It defines a symmetric threshold `f(d)`, states
`f(1)=1/2` and `f(d)=(d-1)^(d-1)/d^d` for `d >= 2`, derives `d f(d) -> 1/e`, and also announces a
sharp bound for `rho` in terms of the individual probabilities and `G`.

The landing page and Crossref response were inspected as dated remote discovery inputs, not
accepted source artifacts. The full article was not available in this worker as lawfully preserved
text, the catalog does not cite it, and no exact theorem/definition transcription, assumption and
proof-boundary mapping, correction/errata audit, or independent review exists. It is therefore an
`H1` lead, not `H0` evidence.

## Component crosswalk

| Catalog component | Candidate source component | Prospective Lean surface | Intake status |
|---|---|---|---|
| Lovasz Local Lemma | finite family of bad events with sparse dependency | measurable events indexed by a finite type and a `SimpleGraph` | recognizable setting; exact dependency semantics open |
| optimal condition | sharp general avoidance bound, positivity region, or converse/tightness | signed weighted sums over independent vertex sets plus probability inequalities | exact root and polynomial convention not selected |
| Shearer bound | general graph-dependent result or symmetric `f(d)` corollary | general `p : V -> ENNReal` statement or a degree-bounded scalar theorem | catalog does not distinguish them |
| no event occurs | intersection of complements and its probability | measure of a finite intersection or complement of a union | exact subset/all-events conclusion open |
| 1985 / James Shearer | historical author and date | immutable provenance and source-to-node mapping | matching DOI found; full mapping and review open |
| `verified` | untrusted inventory metadata | no declaration or proof body | no H, M, or R credit |

## Variant boundary

Later descriptions of Shearer's condition use equivalent-looking `q_S` or subset-polynomial
families, and some strengthen the hypotheses to lopsided conditional bounds. The symmetric
maximum-degree threshold is a specialization, while necessity/optimality is a different direction
from the avoidance lower bound. None is credited as identical until a reviewed primary-source
statement and checked transports cover definitions, binders, side conditions, and boundary cases.

The entropy Shearer inequality and triangle-free-graph Shearer bound are excluded by the catalog's
LLL context. The ordinary Lovasz Local Lemma, Moser-Tardos algorithm, and Janson inequality are
neighboring results, not aliases.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the inspected APIs
provide `ProbabilityTheory.iIndepSet`, finite-intersection probability products, `SimpleGraph.IsIndepSet`,
`neighborFinset`, `maxDegree`, and independent-set enumeration. A bounded exact-topic search found
no Shearer, Lovasz Local Lemma, or independence-polynomial declaration in pinned mathlib or
repository-local Lean. The checked APIs are substrate only; they do not state the dependency-graph
hypothesis, polynomial criterion, sharp bound, or optimality conclusion.

## Required admission

The statement phase must preserve a lawfully accessible immutable primary edition, select and
transcribe one exact theorem plus incorporated definitions, map every ordered binder, hypothesis,
conclusion, exceptional case, proof boundary, correction, and erratum, and obtain independent source
review. It must then encode that same claim in Lean, minimize imports, serialize the elaborated
expression and environment, check every credited transport, and run the required statement
mutations. Until then the canonical statement and formal target remain null.
