# THM-M-0827 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6075-6080` supplies exactly the title `Floyd-Warshall算法`, the
attribution Robert Floyd/Stephen Warshall, year 1962, the gloss `全源最短路径算法` ("all-pairs
shortest-path algorithm"), high importance, and status `已验证`. Git history attributes all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, formula, graph or weight definition, algorithm, ordered binders, assumptions,
conclusion, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22577-22602` repeats the gloss while expressly leaving the formal system,
foundations, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

The separate computer-science record at `Docs/researches/cs_theorems.md:168` and Stage0 UID
`THM-C-0093` say `全源最短路径O(n^3)算法`. This is ambiguity and boundary evidence, not source
authority for `THM-M-0827`: its complexity clause cannot be silently added to the shorter
mathematical record.

## Bibliographic leads, not accepted source evidence

Crossref and Semantic Scholar metadata were inspected on 2026-07-13 for two 1962 publications:

1. Robert W. Floyd, "Algorithm 97: Shortest path," *Communications of the ACM* 5(6), page 345,
   DOI `10.1145/367766.368168`. This is the direct shortest-path source-family lead.
2. Stephen Warshall, "A Theorem on Boolean Matrices," *Journal of the ACM* 9(1), pages 11-12,
   DOI `10.1145/321105.321107`. Metadata identifies a Boolean-matrix paper; its exact relationship
   to a source-selected shortest-path proposition remains uninspected.

The metadata corroborates the catalog's people and year. Both ACM PDF requests returned HTTP 403,
so the paper texts, exact algorithms, statements, definitions, assumptions, proofs, variants,
corrections, and errata were not inspected. No independent source reviewer has admitted an
immutable edition or approved a Floyd-to-Warshall transport. These leads therefore do not establish
H0 or select the canonical root.

## Component crosswalk

| Catalog or related component | Mathematical information fixed | Lean information still required | Intake result |
|---|---|---|---|
| `Floyd-Warshall算法` | conventional name for an algorithm family | exact state, recurrence, enumeration, update semantics, and output relation | family only; open |
| `全源` | intended result concerns every ordered vertex pair | finite vertex type, pair matrix/function, reachability and infinity | domains open |
| `最短路径` | shortest-path purpose, with cost measure unspecified | edge/weight model, walk/path semantics, minimum versus infimum, negative cycles | semantics open |
| Robert Floyd | historical shortest-path algorithm lead | admitted text, pinpoint algorithm/result/proof and premise map | metadata only |
| Stephen Warshall | historical Boolean-matrix paper lead | approved relationship or transport to the selected shortest-path proposition | transport open |
| 1962 | publication-year lead | exact source chronology and target composition | bibliographic only |
| companion `O(n^3)` | familiar complexity clause in another UID | source-approved inclusion and a precise cost model | excluded pending decision |
| `已验证` | inventory screening label | accepted source review or kernel receipt | no credit |

The literal M-record has no connective or conclusion whose truth Lean can check. It therefore fixes
no ordered binder, hypothesis, canonical conclusion, alternate encoding, expression, or expression
hash.

## Non-equivalent candidate statement families

| Candidate | Material choices absent from the catalog | Intake decision |
|---|---|---|
| recurrence invariant after `k` intermediates | vertex order, base matrix, allowed walk class, infinity and negative cycles | not selected |
| final distance-matrix correctness | distance domain, reachability, negative-cycle scope, attainment and output equality | not selected |
| predecessor/path reconstruction | next-hop state, ties, cycle behavior, witness validity | not selected |
| transitive closure | Boolean versus min-plus algebra and checked relationship to the named target | not selected |
| negative-cycle detection | global or pair-specific meaning and soundness/completeness directions | not selected |
| termination or `O(n^3)` complexity | executable loops, matrix representation, operation and arithmetic cost model | not selected |

These are not interchangeable. In particular, Boolean reachability does not alone prove weighted
shortest distances, and a triple-loop count does not prove correctness.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks
directed adjacency, dependent paths and length, additive path weight and composition, and unweighted
undirected extended distance. These interfaces show only that generic graph/path substrate exists.
They do not define Floyd-Warshall state, the intermediate-vertex recurrence, all-pairs weighted
distance, negative-cycle handling, execution, or complexity.

A bounded case-insensitive search of repo-local Lean and pinned mathlib for Floyd-Warshall and
all-pairs-shortest-path phrases found no occurrence. This is discovery evidence, not an exhaustive
formal-candidate audit or proof of absence.

## Source exit gate

Before statement execution, independent algorithms and source reviewers must approve a lawful
immutable source edition, select one exact truth-valued proposition, inspect its definitions,
assumptions, proof, corrections, and errata, and map every component to the catalog scope. They must
also resolve Floyd versus Warshall provenance, the weighted-versus-Boolean transport, whether
`O(n^3)` is outside or inside the root, and all negative-cycle and boundary conventions. Only then
may the statement phase freeze minimal imports, ordered binders, a canonical Lean expression,
environment and expression fingerprints, checked transports, and the required mutations.
