# THM-M-0816 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the theorem family cataloged as
Turán's theorem with the gloss "the maximum number of edges in a graph containing no complete
subgraph." The catalog does not specify the order of the forbidden clique, whether the root is the
sharp edge inequality, the equality case, or the uniqueness characterization, or the finite-graph
and boundary conventions.

The repository source record and Stage0 projection were inspected. The official REAL-J archive
metadata for *Matematikai és Fizikai Lapok* volume 48 (1941) also identifies Pál Turán's article
"Egy gráfelméleti szélsőérték feladatról." That archive-level record is a primary-source lead, but
the article pages, exact proposition, assumptions, proof, corrections, and independent review have
not been incorporated. It therefore supports `H1`, not `H0`.

Pinned mathlib contains the dedicated module
`Mathlib.Combinatorics.SimpleGraph.Extremal.Turan`. Its documentation states the finite
`(r + 1)`-clique-free extremal characterization, and it supplies candidate declarations for the
Turán graph, its edge count, the sharp upper bound, and uniqueness up to graph isomorphism. The
narrow Lean probe checks these exact interfaces. This is strong discovery evidence only: intake
does not choose one candidate as the canonical source claim, audit its terminal proof body, or
grant proof credit.

Accordingly the intake leaves the canonical mathematical statement and Lean target null, records
the root as `[H1, M3, R4]`, and opens the six downstream tasks. Accepted proof state, audit
completion, and theorem completion are false. Only the Stage1 integration lane may accept this
self-tested worker proposal.

