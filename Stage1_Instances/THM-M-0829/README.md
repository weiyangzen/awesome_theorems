# THM-M-0829 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the Dinic
algorithm. The repository supplies only the gloss "a layered algorithm for maximum flow,"
attributes it to Yefim Dinitz in 1970, and labels it verified. Under rev-5.6 those are untrusted
inventory fields, not a precise theorem, source audit, Lean statement, or proof.

The gloss identifies a standard algorithm family, but it does not fix a directed-network model,
capacity domain, source and sink conditions, residual-edge convention, level-graph construction,
blocking-flow definition or implementation, output contract, correctness clause, termination
measure, or cost model. It also does not choose among the original general-network complexity
result, a later dynamic-tree improvement, specialized unit-capacity bounds, or a conjunction with
maximum-flow correctness. Intake does not fill those proposition-changing clauses from memory.

Publisher metadata for Yefim Dinitz's 2006 retrospective was inspected. Its reference list
identifies the 1970 Russian paper and English translation, but the primary paper text itself was
not inspected. The metadata separately lists the 1970 original paper and much later dynamic-tree
work, but does not by itself map either complexity bound to an algorithm variant. It is a strong
bibliographic lead, not an accepted statement/proof crosswalk.

Pinned mathlib exposes generic quiver paths, additive path weights, undirected simple-graph walks,
shortest-walk distance, and finite bounded-walk enumeration. `IntakeProbe.lean` authenticates those
interfaces. A bounded exact-topic search found no maximum-flow, residual-network, blocking-flow,
level-graph, or Dinic/Dinitz declaration. These APIs are infrastructure clues only; an undirected
simple-graph metric and an additive weight do not silently become a directed residual network or a
blocking-flow algorithm.

The provisional vector is `[H1, M4, R4]`: a precise published-paper lead identifies a standard
result family with an explicit unresolved source-mapping list, but its exact statement,
assumptions, proof, corrections, and source-to-node mapping have not been inspected; no usable
exact formal artifact is located; and no source-faithful proof reconstruction exists. All six
downstream phases remain open. No H0, M0, R0, accepted state, audit completion, theorem completion,
or master acceptance is claimed.
