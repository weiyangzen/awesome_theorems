# THM-M-0854 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Ore's theorem in finite graph
theory. The repository gives the title `Ore定理`, attributes it to Oystein Ore in 1960, and
supplies only the gloss `Hamilton圈存在的度和条件` (a degree-sum condition for the existence of a
Hamiltonian cycle). Its `已验证` label is untrusted metadata and gives no source or proof credit.

The intended theorem family is recognizable: for a finite simple undirected graph on at least
three vertices, if every distinct nonadjacent pair has degree sum at least the number of vertices,
then the graph is Hamiltonian. The likely primary source is Oystein Ore, *Note on Hamilton
Circuits*, *The American Mathematical Monthly* 67(1) (1960), p. 55, DOI
`10.2307/2308928`. Only bibliographic metadata, not an immutable article text or a reviewed
theorem-level crosswalk, was available at intake. The exact source statement therefore remains
unaccepted.

The lower bound of three vertices and the distinctness condition are material. Mathlib's simple
graphs are loopless, so a premise quantified over all `u, v` with only `not G.Adj u v` would include
`u = v` and strengthen the usual Ore condition. Mathlib also proves every two-vertex simple graph
is non-Hamiltonian, while the usual condition can hold for the complete two-vertex graph if it is
restricted to distinct nonadjacent pairs. No convention is silently chosen here.

Pinned mathlib has the required finite-degree and Hamiltonicity APIs but no Ore declaration. A
read-only Git object already present in the dependency repository contains an old, divergent,
unmerged mathlib branch with a source-visible `SimpleGraph.ore_theorem`. It targets Lean 4.12.0-rc1,
is not in the pinned Lean 4.29.0 closure, was not elaborated here, and receives no M1 or M0 credit.

This intake freezes the candidate family, scope decisions, source crosswalk, external-candidate
boundary, and open task order. The canonical statement and Lean target remain null pending source
and convention review. The provisional root vector is `[H1, M4, R4]`; every downstream phase and
master acceptance remain open. No exact statement, proof, audit completion, or theorem completion
is claimed.
