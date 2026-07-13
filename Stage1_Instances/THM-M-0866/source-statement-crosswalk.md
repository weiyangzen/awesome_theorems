# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6348-6353` supplies exactly the title `Wagner定理`, attribution
Klaus Wagner, year 1937, gloss `平面图的禁用 minors 刻画`, importance high, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, theorem locator,
definitions, ordered binders, hypotheses, conclusion, proof boundary, correction record, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:23630-23655` repeats the gloss while explicitly leaving the formal
system, exact definitions and premises, proof route, dependencies, equivalent statements, axioms,
machine status, and artifact links open. Its generic closed-result and leaf-audit prose is planning
metadata, not evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Primary-source lead

Crossref metadata identifies K. Wagner, *Über eine Eigenschaft der ebenen Komplexe*,
*Mathematische Annalen* 114(1), 570-590 (1937), DOI `10.1007/BF01594196`. The title, author, date,
journal, volume, pages, language, and DOI match the catalog's attribution, year, and theorem family.
Springer bibliographic metadata was also inspected; Semantic Scholar reports the article as closed
access. The zbMATH API identifies EuDML record `159935` and reproduces a German JFM review by Erika
Pannwitz. That review describes Wagner's contraction process as repeated edge deletion and endpoint
identification with parallel-edge merging, then summarizes a structural basis theorem for the
resulting complexes and its relationship to the four-color theorem. It also says the final sentence
of the introduction is incorrect. The review is secondary evidence and does not itself select or
transcribe the catalog's modern forbidden-minor characterization.

This is a primary bibliographic lead, not an admitted primary theorem statement. The full article
was not available for a lawful pinpoint reading in this intake, so no source-era definition of
"complex," exact numbered or unnumbered proposition, assumptions, proof boundary, or corrections
were transcribed. The relationship between Wagner's source results and the familiar modern
finite-graph `K5`/`K3,3` forbidden-minor biconditional was not independently reviewed, and the
review's correction warning has not been reconciled against the primary text. The lead therefore
supports `H1`, not `H0` or a canonical proposition.

## Clause crosswalk

| Repository or candidate component | Mathematical information required | Prospective Lean surface | Intake result |
|---|---|---|---|
| planar graphs | abstract graphs admitting a plane/sphere embedding; graph-class and finiteness conventions | an explicit `IsPlanar` predicate with accepted embedding semantics | no pinned interface; definition open |
| forbidden minors | exact graph-minor orientation and deletion/contraction witness model | a graph-minor relation, not `SimpleGraph.IsContained` or an induced embedding | no pinned graph-minor interface |
| familiar obstruction `K5` | complete graph on five vertices | `completeGraph (Fin 5)` after checked representation transport | constructor probed; obstruction role uncredited |
| familiar obstruction `K3,3` | complete bipartite graph with parts of size three | `completeBipartiteGraph (Fin 3) (Fin 3)` after checked transport | constructor probed; obstruction role uncredited |
| characterization | exact biconditional and quantifier order | one source-identical `Prop`, possibly with checked alternate encodings | not frozen |
| Klaus Wagner / 1937 | primary article and source-era terminology | provenance only | bibliographic lead, no pinpoint statement |
| `已验证` | claimed validation status | accepted source and kernel receipts | explicitly rejected as proof credit |

## Pinned Lean boundary

`IntakeProbe.lean` imports the pinned `SimpleGraph.Bipartite` and `SimpleGraph.Copy` modules and
checks `SimpleGraph`, the complete and complete-bipartite constructors, `SimpleGraph.Copy`,
`SimpleGraph.IsContained`, `SimpleGraph.IsIndContained`, and `SimpleGraph.induce`. These are useful
finite simple-graph and subgraph APIs, but ordinary or induced containment is strictly stronger than
being a graph minor and cannot encode the required contraction closure by renaming.

A bounded exact-topic search found no repo-local or pinned-mathlib graph-planarity, graph-minor, or
Wagner theorem declaration. The `Matroid.IsMinor` family is unrelated to the required graph-minor
relation, and metric-space declarations bearing Kuratowski's name are unrelated to planar graph
obstructions. This search is not the immutable exhaustive formal-candidate audit assigned to the
later anchor phase, and it makes no claim about unsearched external projects.

## Source gate

Before statement credit, accountable reviewers must lawfully preserve and hash a complete primary
edition; pinpoint the exact proposition and referenced definitions; map all graph-class, finiteness,
planarity, deletion/contraction, minor-direction, obstruction, binder, and boundary clauses; inspect
corrections and errata; explain any modernization from complexes or multigraphs to Lean simple
graphs through checked transports; and independently approve the result. Only that claim may be
elaborated and mutation-tested. Until then, no exact statement, H0, formal closure, or theorem
completion is claimed.
