# THM-M-0814 rev-5.6 dossier

This directory is the fail-closed `planned` theorem dossier for `THM-M-0814`, the max-flow
min-cut theorem. The repository supplies only the gloss "the maximum value of a network flow
equals the minimum cut capacity," attributes it to L. R. Ford and D. R. Fulkerson in 1956, and
labels it verified. Under rev-5.6 that label is untrusted metadata, not source or proof evidence.

The original six-page article *Maximal Flow Through a Network* was inspected. Its Theorem 1 on
printed page 400 states that the maximal flow value in a finite network is the minimum capacity
over all disconnecting arc sets. The paper's network is an undirected finite graph with distinct
source and sink, positive arc capacities, and a flow represented as a finite collection of
nonnegative simple source-to-sink chain flows. The statement phase selects that source-shaped
formulation rather than substituting the familiar directed conservation form. Independent source,
historical-definition, and errata review remain open.

`Statement.lean` defines non-self-intersecting chains, finite nonnegative chain-flow collections,
arc loads, feasibility, disconnecting sets, and their values. The canonical target requires an
attained maximal feasible flow and minimum disconnecting set with equal values. It elaborates with
only pinned `Finsupp`, `Graph`, and `NNReal` modules. `check_statement.py` verifies import
minimality, serializes the full helper-definition bundle, and distinguishes all four required
mutation classes.

The anchor audit freezes an eleven-group version-2 discovery inventory. Pinned mathlib and the other
materialized dependencies contain no max-flow/min-cut theorem. The strongest public Lean 4 lead is
`facebookresearch/atlas-lean@34ffed396`, whose `NetworkFlow.max_flow_min_cut` proves a conditional
directed-flow/partition-cut equality. It does not close this target's undirected explicit-arc,
parallel-edge-aware `Chain ->₀ NNReal` encoding, flow and cut existence, or universal extrema
clauses. `TankTechnology/CLRS-Lean@4fc689e2` offers only partial nonexact directed-flow support.
Three other immutable projects are wrong-backend and/or placeholder-tainted. Exact source, pin,
license, trust, search-limit, and reopen evidence is in `anchor-audit.json` and
`external-anchor-snapshot.json`.

The provisional vector is now `[H1, M3, R4]`: an exact source-shaped Lean interface is self-tested,
and the bounded anchor inventory is classified, while source acceptance, an obligation tree, exact
proof integration, and reviewed reconstruction remain open. No target proof body is imported or
declared. The lifecycle stays `planned`; the worker proposals await dependency-ordered master
acceptance. No H0, M0, R0, accepted proof state, `AUDIT-Z`, theorem completion, or release is
claimed.
