# THM-M-0869 source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:6369-6374` supplies exactly a title, collective attribution,
twentieth-century date, the gloss `禁用子图类的刻画`, importance "high," and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, named graph class,
containment relation, formula, binders, hypotheses, conclusion, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23711-23736` repeats the gloss and calls it a problem or decision
proposition. It explicitly leaves precise definitions and premises, proof route, dependencies,
equivalent statements, axioms, machine status, and artifact links open. Its generic theorem-tree
language is planning metadata, not missing mathematical content. The rev-5.6 manifest preserves the
catalog status only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog element | Mathematical information required | Prospective Lean surface | Intake result |
|---|---|---|---|
| `子图` / subgraph | exact containment notion and relation orientation | `IsContained`, `IsIndContained`, or a separately defined minor/topological-minor relation | ordinary versus induced versus minor is unresolved |
| forbidden | noncontainment convention and equality up to isomorphism | `SimpleGraph.Free` or quantified negation of containment | usable ordinary-copy API exists; no convention selected |
| graph class | domain of graphs, isomorphism closure, and membership predicate | a typed predicate or set of graph/isomorphism-class representatives | absent |
| characterization | exact equality/iff and direction hypotheses | one binder-complete `Prop` plus checked transports | no truth-valued statement supplied |
| problem | theorem, classification task, decision language, or research program | one proposition or an explicitly typed branch ledger | target kind unresolved |
| `已验证` | evidence for one exact claim | accepted source/kernel receipts | untrusted metadata; no credit |

## Distinguishing candidate statement families

For ordinary subgraph containment, a representation claim would quantify a graph class `C` and
obstruction family `F`, then relate `C G` to avoidance of every `H` in `F`. An induced variant
changes the containment predicate and the closure property. A minor-closed finite-basis theorem adds
both a different preorder and a nontrivial finiteness conclusion. These are not alternate spellings
of one statement.

The surrounding catalog reinforces the ambiguity. It separately records Kuratowski's theorem at
lines 6341-6346, Wagner's theorem at 6348-6353, the Robertson-Seymour theorem at 6355-6360, and the
Graph Minor Theorem at 6362-6367. `THM-M-0840` separately records the Strong Perfect Graph Theorem.
The assigned generic label cannot inherit their statements or evidence.

## Source gate

There is no repository-selected primary source or stable proposition. Before leaving `H5`, an
accountable graph-theory source reviewer must select and lawfully preserve the intended source,
pinpoint the theorem or problem and incorporated definitions, decide which containment and graph-
class notions the Chinese words denote, map every premise and conclusion, audit corrections and
neighbor ownership, and obtain independent approval. Only then may the statement phase elaborate
and mutation-test an identical Lean expression.

`H5` here classifies the received wording as ill-posed for proof execution. It does not say that
forbidden-subgraph mathematics is false, open, or unsupported in the literature.

## Lean discovery boundary

Pinned mathlib's `Mathlib.Combinatorics.SimpleGraph.Copy` defines cross-vertex-type copy containment
`SimpleGraph.IsContained`, the convenience predicate `SimpleGraph.Free`, and induced containment
`SimpleGraph.IsIndContained`. It provides transitivity and equivalences to isomorphic subgraphs.
`IntakeProbe.lean` elaborates those interfaces under the pinned toolchain.

The probe does not define the catalog's graph class or obstruction family, choose ordinary versus
induced containment, provide a minor relation, state a characterization, or locate a proof body. A
bounded exact-topic search is only intake discovery. Canonical module, target expression,
expression/environment fingerprints, alternate encodings, and statement mutations remain null.
