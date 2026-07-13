# THM-M-0861 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for König's edge-coloring theorem. The
repository gives the literal claim "the edge chromatic number of a bipartite graph equals its
maximum degree," attributes it to Dénes König in 1916, and labels it `已验证`. That label is
untrusted inventory metadata and supplies neither source nor machine-proof credit.

The 1916 primary paper was inspected from an open scan. Its printed pages 453-454 define finite
graphs while explicitly permitting finitely many parallel edges, and characterize `paare Graphen`
by a vertex bipartition. Satz C on printed page 455 says that if at most `k` edges meet at every
vertex, the edges can be assigned `k` indices so incident edges receive different indices; its
induction and alternating-index-path proof continues through page 456. This is the source's proper
`k`-edge-coloring upper-bound form. The catalog's chromatic-index equality also uses the elementary
lower bound at a maximum-degree vertex. No independent source review, correction audit, or accepted
modern equality transport exists yet, so the source status remains `H1`, not `H0`.

The historical theorem is about finite bipartite multigraphs; its pair-of-vertices edge model is
consistent with excluding loops, but that modern encoding choice still requires review. Pinned
mathlib supplies `Graph` with separate vertex and edge types, parallel-edge identity, loops, links,
incidence, and incidence sets. It does not yet supply the multigraph bipartiteness, degree, proper
edge-coloring, or chromatic-index interfaces needed here. Mathlib also supplies finite simple
graphs, bipartiteness, maximum degree, line graphs, vertex colorings, and arbitrary edge labelings.
`IntakeProbe.lean` authenticates those adjacent APIs. A simple graph's proper edge
coloring can prospectively be represented as a coloring of its line graph, but silently replacing
the source multigraph by a simple graph would weaken the target. The intake freezes the human claim
at the source-faithful multigraph level. The exact representation, chromatic-index definition,
degenerate conventions, and source-to-Lean transport belong to the statement phase.

The provisional vector is `[H1, M4, R4]`. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No canonical Lean expression, H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
