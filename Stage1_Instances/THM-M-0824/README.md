# THM-M-0824 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Prim算法`
(Prim's algorithm). The mathematical catalog supplies only the gloss `最小生成树的另一种算法`
("another algorithm for minimum spanning trees"), the attribution Robert Prim, the year 1957,
and an untrusted `已验证` status. These fields identify an algorithm family and purpose, not a
truth-valued proposition with ordered binders, hypotheses, and a conclusion.

Prim correctness can be stated for several graph and program models. A source-faithful theorem
must select a finite weighted undirected graph model, connectedness and nonemptiness assumptions,
the weight carrier and comparison law, a start vertex, frontier and tie behavior, an exact state
transition and stopping rule, an output representation, and a conclusion. Termination, spanning
tree validity, minimum-weight optimality, and a complexity bound are separate claims. The catalog
selects none of these choices, so this intake does not silently install a familiar textbook
version.

Crossref metadata identifies R. C. Prim's 1957 paper *Shortest Connection Networks And Some
Generalizations* as a strong bibliographic lead. The repository does not cite it, and no article
body, exact algorithm passage, theorem, proof, assumption map, or errata review was admitted.
A second repository catalog row, `THM-C-0095`, says "Prim minimum-spanning-tree algorithm is
correct" but likewise leaves the computation model and exact premises open; it is not a rev-5.6
target and supplies no independent source or proof credit.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
root vector is `[H5, M4, R4]`: `H5` classifies the received algorithm-family wording as not yet a
stable proposition, not established Prim correctness results as false; `M4` records that no exact
formal artifact is credited; and `R4` records that no source-faithful proof reconstruction can
attach to an unfrozen root.

`IntakeProbe.lean` checks only adjacent pinned simple-graph APIs. All six downstream tasks remain
open. No canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
