# THM-M-0825 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Dijkstra算法`
(Dijkstra's algorithm). The catalog supplies only the gloss `单源最短路径算法` (single-source
shortest-path algorithm), attributes it to Edsger Dijkstra in 1959, and labels it `已验证`. That
label is untrusted metadata and supplies neither human-source nor kernel-proof credit.

## Intake result

The catalog identifies a recognizable algorithm family, not a binder-complete correctness theorem.
It does not fix a graph model, weight domain and nonnegativity premise, reachability convention,
algorithm state and tie behavior, output contract, termination claim, or complexity model. These
choices distinguish shortest-path existence, one-pair correctness, all-reachable-vertices
correctness, predecessor-tree correctness, total solver correctness, and complexity theorems.
Selecting one at intake would silently change the received claim.

E. W. Dijkstra's primary paper, *A Note on Two Problems in Connexion with Graphs*, was inspected as
a strong source lead. Its page 270 states Problem 2 as finding a minimum-total-length path between
given nodes `P` and `Q`, describes constructing minimum paths from `P` in increasing length, and
gives the familiar relaxation and least-tentative-distance steps. Page 269 assumes finitely many
nodes, assigned branch lengths, and a path between every pair; a page-270 remark permits
direction-dependent branch lengths. This disambiguates the historical family but does not by itself
select the catalog's modern single-source output contract or provide an accepted premise/proof
crosswalk. It is therefore recorded as an `H1` lead, not `H0`.

## Formal boundary

Pinned mathlib supplies unweighted simple-graph distance, additive quiver-path weights, and an
unweighted noncomputable shortest-path specification. `IntakeProbe.lean` authenticates those
interfaces. A bounded search found no Dijkstra implementation or correctness theorem. None of the
probed declarations executes the named algorithm or proves the unresolved root.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a pinpoint primary source lead exists but exact source-to-catalog fidelity is open;
no usable formal artifact for the algorithm root is credited; and no readable proof can attach to
an unidentified root. All six downstream tasks remain open. No accepted state, audit completion,
theorem completion, accepted receipt, or master acceptance is claimed.
