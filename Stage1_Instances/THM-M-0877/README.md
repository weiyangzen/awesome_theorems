# THM-M-0877 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0877`, the repository topic
`网络流` (network flow). The catalog supplies only the gloss `最大流与最小割理论`, literally
"max-flow and min-cut theory," a collective attribution, a twentieth-century date, and the
untrusted status `已验证`.

That wording names a subject and theorem family, not one truth-valued proposition. It does not say
whether the root is max-flow/min-cut equality, existence and attainment of optima, weak duality,
integrality, an augmenting-path theorem, or an algorithm and correctness result. It also omits the
network model, capacity domain, feasible-flow and cut definitions, extrema, ordered binders, and
boundary cases.

The distinction is material because `THM-M-0814` separately owns the catalog's explicit max-flow
min-cut equality. Ford and Fulkerson's 1956 paper was inspected only to discriminate that precise
neighbor from this broader record. Its Theorem 1 uses finite undirected networks, positive arc
capacities, weighted simple source-to-sink chain flows, and disconnecting arc sets. It cannot be
silently substituted for this target or for the familiar directed conservation-flow formulation.

`instance.json` therefore records a provisional root vector `[H5, M4, R4]`. Here `H5` classifies
the received topic/gloss as not one stable proposition; it does not say that max-flow/min-cut
mathematics is false, independent, or open. `IntakeProbe.lean` elaborates only adjacent pinned graph,
digraph, finite-sum, and maximum APIs. All six downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
