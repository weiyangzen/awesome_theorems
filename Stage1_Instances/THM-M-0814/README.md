# THM-M-0814 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0814`, the max-flow
min-cut theorem. The repository supplies only the gloss "the maximum value of a network flow
equals the minimum cut capacity," attributes it to L. R. Ford and D. R. Fulkerson in 1956, and
labels it verified. Under rev-5.6 that label is untrusted metadata, not source or proof evidence.

The original six-page article *Maximal Flow Through a Network* was inspected. Its Theorem 1 on
printed page 400 states that the maximal flow value in a finite network is the minimum capacity
over all disconnecting arc sets. The paper's network is an undirected finite graph with distinct
source and sink, strictly positive real arc capacities, and a flow represented as a finite
collection of nonnegative simple source-to-sink chain flows. This is a strong primary-source lead,
but the catalog does not cite that article or select its chain-flow encoding over the familiar
directed edge-flow formulation. No independent source or errata review has accepted the mapping.

Pinned mathlib provides undirected multigraph incidence and finite-sum/maximum infrastructure, but
a bounded exact-topic search found no network-flow, capacity, cut-capacity, or max-flow min-cut
declaration. `IntakeProbe.lean` authenticates only those adjacent APIs. They neither define the
source's network and flow nor prove the target.

The provisional root vector is `[H1, M4, R4]`: a pinpoint primary theorem has been inspected but
the exact source-to-catalog formulation and assumptions remain unaccepted; no usable exact Lean
artifact is credited; and no reviewed readable reconstruction exists. `instance.json` is the
structured scope authority, while `task-dag.json` leaves all six downstream phases open. No H0,
M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
