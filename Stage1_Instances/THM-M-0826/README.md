# THM-M-0826 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Bellman-Ford算法` (Bellman-Ford algorithm). The repository supplies only the gloss
`带负权边的最短路径算法` (a shortest-path algorithm with negative-weight edges), attributes it
to Richard Bellman and Lester Ford in 1958, and labels it `已验证`. An algorithm name and purpose
do not by themselves form a truth-valued proposition. The verified label is untrusted inventory
metadata and supplies neither source nor proof credit.

The label could denote single-source or single-sink distance correctness, predecessor-path
reconstruction, negative-cycle detection, termination, a running-time bound, or refinement of a
particular implementation. Those alternatives need different graph, weight, infinity, reachability,
cycle, output, iteration, and cost definitions. The catalog also does not say whether negative
cycles are forbidden globally, only when reachable from the source, or only on a source-to-target
route. Selecting the familiar textbook correctness theorem would therefore invent
proposition-changing mathematics.

Bellman's 1958 paper *On a routing problem*, DOI `10.1090/qam/102435`, is the natural historical
source lead matching one catalog author and year. Mutable bibliographic metadata was inspected,
but the publisher text was not available to this worker. MIT 6.006 Fall 2011 Lecture 17 was
inspected as a modern teaching source lead: it gives pseudocode, a no-negative-cycle correctness
theorem, a proof outline, and a reachable-negative-cycle corollary. The catalog cites neither
source, and no lawful immutable edition, exact source choice, complete definition and assumption
mapping, correction audit, or independent review has been admitted. Neither source receives `H0`
credit.

Pinned mathlib supplies generic directed graphs, quiver paths, and additive path weights.
`IntakeProbe.lean` authenticates those adjacent APIs only. It does not define Bellman-Ford,
relaxation, shortest distance, negative-cycle handling, or algorithm correctness. A bounded
exact-topic search found no Bellman-Ford declaration in pinned mathlib or repo-local Lean; the
later anchor-audit phase remains responsible for exhaustive candidate and provenance work.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received algorithm gloss as not yet a
stable proposition; it does not say that correctly stated Bellman-Ford theorems are false or open.
`instance.json` is the structured scope authority, and `task-dag.json` keeps all six downstream
phases open. No canonical statement, H0, M0, R0, accepted proof state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
