# THM-M-0859 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Vizing's theorem. The repository
supplies the title, attribution to Vadim Vizing, the year 1964, and only the gloss "the edge
chromatic number of a graph." That identifies a theorem family but does not itself state an
inequality, fix simple graphs versus loopless multigraphs, or define edge adjacency and chromatic
index.

The immutable Encyclopedia of Mathematics revision `51407` was inspected as a source lead. It
states the loopless-multigraph bound
`Delta(G) <= chi'(G) <= Delta(G) + mu(G)` and its finite-simple-graph corollary
`Delta(G) <= chi'(G) <= Delta(G) + 1`, and cites Vizing's 1964 Russian paper, pages 25-30. Crossref
metadata for Vizing's related 1965 multigraph paper confirms the bibliography and cites the 1964
paper. The primary 1964 text was not obtained or inspected, so the catalog's intended variant,
assumptions, proof boundary, translation, and errata remain unaccepted.

Pinned mathlib contains finite simple graphs, line graphs, graph colorings, maximum degree, and edge
sets. `IntakeProbe.lean` authenticates those interfaces and the prospective proposition that the
line graph is colorable with `G.maxDegree + 1` colors. A bounded exact-topic search found no Vizing
or chromatic-index declaration. This is encoding substrate, not a frozen target or proof.

The provisional vector is `[H1, M4, R4]`: a standard published result and bibliographic primary
lead are identified, but primary-source fidelity is open; no usable source-identical Lean artifact
is credited; and no source-faithful readable proof reconstruction exists. `instance.json` is the
structured scope authority and `task-dag.json` keeps all six downstream phases open. No canonical
Lean statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
