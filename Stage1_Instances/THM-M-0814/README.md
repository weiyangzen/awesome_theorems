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

The provisional vector is now `[H1, M3, R4]`: an exact source-shaped Lean interface is self-tested,
while source acceptance, proof integration, and reviewed reconstruction remain open. No target
proof body is imported or declared. The lifecycle stays `planned`; the worker proposal awaits
dependency-ordered master acceptance. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or release is claimed.
