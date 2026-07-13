# THM-M-0840 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the strong perfect graph theorem.
The repository supplies the title, the four authors, the year 2006, and only the gloss "forbidden
subgraph characterization of perfect graphs." That identifies the standard theorem family, but it
does not define perfect or Berge graphs, state finiteness and simplicity, or spell out whether the
forbidden objects are odd holes and odd antiholes as induced subgraphs.

The primary 2006 Annals article was inspected as a source lead. Its introduction defines all graphs
to be finite and simple, defines a graph as perfect when every induced subgraph has chromatic number
equal to maximum-clique size, defines a Berge graph by excluding odd holes and odd antiholes, and
states Theorem 1.2: a graph is perfect if and only if it is Berge. This strongly disambiguates the
catalog family. It is not yet `H0`: no immutable repository-owned source snapshot, full
definition/assumption/proof-node/errata crosswalk, or independent source review has been accepted.

Pinned mathlib contains finite simple graphs, induced graphs, complements, cycles, chromatic number,
and clique number. `IntakeProbe.lean` authenticates those interfaces. A bounded exact-topic search
found no perfect-graph, Berge-graph, odd-hole, odd-antihole, or strong-perfect-graph declaration.
The checked APIs are encoding substrate, not the target theorem or proof.

The provisional vector is `[H1, M4, R4]`: a complete published primary proof and exact theorem
family are known, but the source mapping is not accepted; no usable source-identical Lean artifact
is credited; and no source-faithful readable reconstruction exists. `instance.json` is the
structured scope authority and `task-dag.json` keeps all six downstream phases open. No canonical
Lean statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
