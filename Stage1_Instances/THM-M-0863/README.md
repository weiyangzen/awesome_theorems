# THM-M-0863 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the graph-theoretic Whitney
theorem. The repository supplies Hassler Whitney, the year 1932, and only the gloss "ear
decomposition of 2-connected graphs." That identifies the standard ear-construction theorem
family, but it does not define 2-connectivity or an ear, state the forward or biconditional form,
or settle finite-simple-graph and boundary conventions.

Whitney's 1932 primary article was inspected as a source lead. Its Theorem 19 says that a
non-separable graph with at least two arcs can be built from a circuit by successively adding arcs
or suspended chains while every intermediate graph remains non-separable; the immediately
following sentence gives the converse. This is strong evidence for the intended family, but not
yet `H0`: the paper permits loops and parallel arcs, uses non-separability rather than the modern
simple-graph 2-connected predicate, and has no accepted definition/assumption/errata crosswalk or
independent review.

Pinned mathlib supplies simple-graph connectivity, paths, cycles, induced subgraphs, vertex
deletion, and walk-to-subgraph interfaces. `IntakeProbe.lean` authenticates those APIs. A bounded
exact-topic search found no ear-decomposition or named vertex-2-connectivity declaration. These
interfaces are encoding substrate, not the target theorem or proof.

The provisional vector is `[H1, M4, R4]`: a published primary proof source and its relevant
construction route were located, but the source-to-modern-statement mapping is not accepted; no
usable exact Lean artifact is credited; and no source-faithful readable reconstruction exists.
`instance.json` is the structured scope authority and `task-dag.json` keeps all downstream phases
open. No canonical Lean statement, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
