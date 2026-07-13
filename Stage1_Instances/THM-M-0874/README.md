# THM-M-0874 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Babai算法`
(Babai's algorithm). The repository supplies the gloss `图同构的准多项式算法` ("a
quasipolynomial algorithm for graph isomorphism"), attributes it to Laszlo Babai in 2015, and
labels it `已验证`. The label is untrusted metadata and supplies neither source nor proof credit.

The human theorem family is identifiable. Babai's arXiv paper *Graph Isomorphism in
Quasipolynomial Time*, version 2, states String Isomorphism in quasipolynomial time as Theorem
1.1.1 and Graph Isomorphism as Corollary 1.1.2. That version is not a final source by itself:
Babai's January 2017 update records an error that invalidated its timing analysis, a repaired
Split-or-Johnson call, and another Design Lemma correction. The separate four-page UPCC note gives
only one repair. Helfgott, Bajpai, and Dona's post-repair Bourbaki exposition reconstructs the
result, says the proof is now correct, and states the graph result as Corollary 1.2. These are strong
source leads, but no full correction bundle, incorporated-definition map, node-level proof
crosswalk, errata audit, or independent acceptance has yet established `H0`.

The provisional human claim is therefore: a deterministic algorithm solves Graph Isomorphism in
quasipolynomial time. An exact Lean proposition is not frozen. The catalog and source-level
shorthand do not fix graph serialization, malformed input behavior, Boolean versus witness output,
the machine and cost model, the relationship between vertex count and encoded length, or the exact
bound and its small-input convention. Selecting those details at intake would invent a formal
target rather than elaborate the received theorem.

Pinned mathlib supplies graph isomorphisms, formal languages, computable reductions, and a bundled
Turing-machine time interface. `IntakeProbe.lean` authenticates only those adjacent APIs. It does
not define a graph encoding, Graph Isomorphism language, Babai procedure, resource-bounded
reduction, quasipolynomial predicate, or proof.

The provisional vector is `[H1, M4, R4]`: the exact human proof/source/correction mapping remains
open, no usable source-identical Lean artifact is credited, and no accepted readable reconstruction
exists. All six downstream phases remain open. No canonical Lean statement, `H0`, `M0`, `R0`,
accepted execution state, audit completion, theorem completion, accepted receipt, or master
acceptance is claimed.

See `scope-map.md` for proposition-changing choices, `source-statement-crosswalk.md` for source and
Lean boundaries, `instance.json` for structured authority, `task-dag.json` for open work, and
`validation.md` for the exact self-test record.
