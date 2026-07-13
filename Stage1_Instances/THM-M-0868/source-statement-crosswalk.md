# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6362-6367` supplies the title `图子式定理`, attribution to
Robertson/Seymour, the period 1983-2004, the gloss `Wagner猜想的证明`, importance `高`, and status
`已验证`. All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, theorem locator,
formula, graph or minor definition, binders, hypotheses, conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23684-23709` repeats the gloss while explicitly leaving the formal
system, foundation, precise definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Primary publication lead

Bibliographic services confirm Neil Robertson and P. D. Seymour, "Graph Minors. XX. Wagner's
conjecture," *Journal of Combinatorial Theory, Series B* 92(2) (November 2004), 325-357, DOI
`10.1016/j.jctb.2004.08.001`, PII `S0095-8956(04)00078-4`.

The primary article body was not available for full-text inspection during intake: the DOI landing
path denied automated PDF access, and the full Elsevier API view required credentials. No theorem
number, printed page, incorporated definition, proof passage, erratum, or correction is therefore
reported as inspected. Crossref and OpenAlex confirmed bibliographic identity only. A CORE record
supplied the secondary abstract text: "We prove Wagner's conjecture, that for every infinite set of
finite graphs, one of its members is isomorphic to a minor of another." That text is useful for
scope discrimination but is not treated as an admitted primary theorem statement.

Consequently the source classification is `H1`: the complete published theorem family and primary
paper identity are strongly established, while exact statement, assumptions, graph conventions,
proof-node mapping, errata/corrections, lawful immutable preservation, and independent review are
open. The classification does not settle whether `THM-M-0868` and `THM-M-0867` should be one target.

## Component crosswalk

| Repository/source component | Prospective mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| "graph" | finite graph under the source's loop/parallel-edge convention | a finite graph carrier and representation | exact graph category open |
| "infinite set" | infinite collection or equivalent sequence of isomorphism classes | `Set.Infinite`, an enumeration, or `Nat -> GraphCode` | quantifier and choice transport open |
| "one ... another" | distinct members with an orientation imposed by sequence indices | witnesses `i < j` or distinct set elements | exact binder form open |
| "isomorphic" | graph identity modulo renaming | `SimpleGraph.Iso` or a quotient/canonical code | quotient/representative convention open |
| "minor" | deletion/contraction or equivalent branch-set model | a future graph-minor relation plus checked equivalences | contraction/minor API absent |
| WQO formulation | every sequence has an increasing related pair | `WellQuasiOrdered graphMinor` | generic predicate available; relation absent |
| `已验证` | untrusted inventory value | accepted source and kernel receipts | no H0 or M credit |

## Duplicate crosswalk

The immediately preceding catalog record, `Docs/researches/math_theorems.md:6355-6360`, names
`Robertson-Seymour图子式定理`, gives the same authors, dates it 2004, and glosses it as
`图子式良拟序定理`. Both records are separately manifested as `THM-M-0867` and `THM-M-0868`.
The repository states no mathematical distinction between "graph-minor WQO theorem" and "proof of
Wagner's conjecture." No neighboring dossier exists in this base snapshot.

This is probable duplicate evidence only. Neither target may import the other's future source,
statement, receipt, or proof status until the integration lane accepts identity, canonical
ownership, and an exact-statement transport or redirect.

## Pinned Lean discovery surface

| Module/declaration | Possible role | Credited status |
|---|---|---|
| `Mathlib.Order.WellQuasiOrder`: `WellQuasiOrdered` | generic infinite-sequence WQO conclusion shape | API availability only |
| `Mathlib.Combinatorics.SimpleGraph.DeleteEdges`: `SimpleGraph.deleteEdges` | one graph-minor operation | deletion substrate only |
| `Mathlib.Combinatorics.SimpleGraph.Subgraph`: `SimpleGraph.Subgraph.deleteVerts` | vertex-deletion substrate | deletion substrate only |
| `Mathlib.Combinatorics.SimpleGraph.Maps`: `SimpleGraph.Iso`, `SimpleGraph.induce` | graph isomorphism and induced-graph vocabulary | representation substrate only |

A bounded case-insensitive search of pinned mathlib and repo-local Lean found no `SimpleGraph`
minor relation, edge contraction, Graph Minor Theorem, Robertson-Seymour, or Wagner-conjecture
declaration. The only `IsMinor` hit was `Matroid.IsMinor`, which is not a graph-minor theorem.
Negative lexical search is neither exhaustive nor evidence of global absence. It is intake
discovery, not the downstream immutable anchor audit.

## Source gate

Before statement acceptance, reviewers must lawfully preserve and inspect an immutable primary
edition; locate the exact theorem and incorporated definitions; map every graph, finiteness,
collection/sequence, isomorphism, minor, contraction, relation-direction, and boundary convention;
audit proof and correction history; independently approve fidelity; and resolve `THM-M-0867`
identity and ownership. Only then may the statement phase define or pin the graph-minor relation,
select an exact Lean expression, minimize imports, record expression/environment fingerprints,
check alternate formulations, and execute all four mutation classes.
