# THM-M-0813 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the theorem family cataloged as
Menger's theorem with the gloss "the maximum number of disjoint paths in a graph." The catalog
does not say what this number equals, or select vertex versus edge disjointness, two terminal sets
versus two vertices, finite versus infinite graphs, directed versus undirected graphs, or a local
versus global connectivity formulation.

Karl Menger's 1927 paper *Zur allgemeinen Kurventheorie* was preserved from its publisher and its
bibliographic identity was checked through the DOI record. The available scan has no text layer,
and this intake did not reconstruct a graph-theoretic proposition from the German topological
source. An inspected modern source, Reinhard Diestel's *Graph Theory*, sixth edition (2025),
Theorem 3.3.1, states the finite set-to-set vertex form: the minimum number of vertices separating
sets `A` and `B` equals the maximum number of pairwise vertex-disjoint `A`-`B` paths. The same
section separately derives point-to-point vertex, edge, and global connectivity forms. This is a
strong source-family lead, not authority to choose a root omitted by the catalog.

There is also a distinct repository target, `THM-M-0862`, whose gloss is "vertex connectivity and
disjoint paths." No accepted alias, deduplication, or ownership decision relates it to this target.
Its wording and any future evidence therefore receive no credit here.

Pinned mathlib supplies simple-graph paths, reachability, induced subgraphs, and edge-connectivity
interfaces. `IntakeProbe.lean` authenticates those adjacent APIs. A bounded exact-topic search found
no Menger theorem, vertex-separator package, or theorem equating separators with disjoint paths.
The interfaces are ingredients only, so the provisional vector is `[H1, M4, R4]`.

The canonical statement and formal target remain null, and all six downstream tasks remain open.
No exact proposition, H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed. Only the integration lane may accept this self-tested worker
proposal.
