# THM-M-0907 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Alon-Tarsi定理` (Alon-Tarsi theorem). The repository supplies Noga Alon and Michael Tarsi, the
year 1992, and only the gloss `列表着色的组合Nullstellensatz方法` (a combinatorial-Nullstellensatz
method for list coloring). The manifest's `已验证` label is untrusted metadata, not a source,
statement, or proof receipt.

Alon and Tarsi's primary paper *Colorings and orientations of graphs* is an exact-topic source lead.
Its Theorem 1.1 gives the orientation criterion usually associated with their names: unequal
numbers of even and odd Eulerian spanning subdigraphs imply a proper coloring from vertex lists of
size outdegree plus one. The same paper also contains materially different corollaries, a graph-
polynomial coefficient bridge, a Nullstellensatz-type proposition, choosability applications, and a
conditional reduction of the Dinitz conjecture. The catalog does not cite the paper or choose among
these roots, and its phrase "method" is not itself a truth-valued proposition.

The intake therefore preserves Theorem 1.1 as the strongest candidate rather than silently making
it canonical. Source review still must fix the finite/simple/oriented graph model, spanning-
subdigraph semantics, Eulerian balance and parity counts, empty subgraph, integer-list and proper-
coloring conventions, exact-versus-lower-bound list size, ordered binders, boundary cases, and the
relationship to the later 1999 Combinatorial Nullstellensatz. The primary copy has been inspected,
but no complete premise/proof-node/errata map or independent review supports `H0`.

`IntakeProbe.lean` checks adjacent pinned digraph, ordinary-coloring, and generic Combinatorial
Nullstellensatz interfaces. It states no Alon-Tarsi target and supplies no proof credit. The
provisional vector is `[H1, M4, R4]`: a published complete proof candidate is known, but exact
source identity and assumptions remain unaudited; no usable exact formal artifact is credited; and
no source-faithful readable proof is reconstructed.

All six downstream tasks remain open. No canonical statement, expression fingerprint, H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
