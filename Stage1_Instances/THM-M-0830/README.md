# THM-M-0830 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Push-Relabel algorithm. The repository supplies only the gloss "the push-relabel algorithm for
maximum flow," attributes it to Andrew Goldberg and Robert Tarjan in 1988, and labels it verified.
Under rev-5.6 that label is untrusted inventory metadata, not an exact theorem or proof evidence.

The primary Goldberg-Tarjan paper was inspected. It defines finite directed real-capacity flow
networks and the generic preflow/push/relabel method, proves conditional correctness in Theorem
3.4, proves termination after `O(n^2 m)` basic operations in Theorem 3.11, and proves an `O(n^3)`
running-time bound for the FIFO implementation in Theorem 4.5. These are substantive published
results, but the math catalog does not select correctness, generic termination, FIFO complexity, or
a conjunction of them. A separate CS catalog target says `O(V^3)`; it is useful scope evidence but
cannot silently redefine this mathematical target.

Pinned mathlib provides directed-graph, path, weight, and finite-sum substrate. A bounded search
found no flow-network, preflow, residual-network, maximum-flow, or push-relabel formal artifact.
`IntakeProbe.lean` authenticates only that substrate. No canonical algorithm, target declaration, or
proof is introduced.

The provisional vector is `[H1, M4, R4]`: the primary paper contains complete proof routes for the
recognizable result family, while exact source-to-catalog statement selection and independent
review remain open; no usable formal artifact or readable reconstruction of an exact selected root
exists. `instance.json` is the structured scope authority and `task-dag.json` keeps all six
downstream phases open. No H0, M0, R0, accepted state, audit completion, theorem completion, or
master acceptance is claimed.
