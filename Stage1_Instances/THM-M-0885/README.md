# THM-M-0885 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0885`, the repository label
`Morgenstern theorem`. The catalog attributes it to Moshe Morgenstern in 1994 and supplies only the
gloss `Ramanujan graph existence`. It gives no citation, quantified proposition, graph convention,
degree family, spectral definition, construction requirement, or boundary cases. Its `verified`
field is untrusted metadata under rev-5.6.

The exact bibliographic match is Moshe Morgenstern, *Existence and Explicit Constructions of q + 1
Regular Ramanujan Graphs for Every Prime Power q*, Journal of Combinatorial Theory, Series B 62(1)
(1994), 44-62, DOI `10.1006/jctb.1994.1054`. Crossref and DBLP metadata identify that article, but
the catalog does not cite it and an edition containing the theorem text was not admitted or
independently reviewed. The title is discovery evidence, not authority to invent the missing
binders and definitions.

In particular, `Ramanujan graph existence` does not select between a single finite graph, an
infinite family, or an explicit construction; it does not say whether the graphs are connected,
simple or allow multiple edges; and it does not state which trivial adjacency eigenvalues are
excluded. The tempting reading "for every prime power q, there are explicit (q+1)-regular
Ramanujan graphs" is therefore recorded only as a candidate source family, not as the canonical
claim.

`instance.json` freezes the provisional root vector `[H1, M4, R4]`. `H1` records that a published
proof family is identified while exact statement, assumptions, source mapping, errata disposition,
and review remain open. `IntakeProbe.lean` elaborates only adjacent pinned finite-simple-graph,
regularity, adjacency-matrix, and Hermitian-spectrum interfaces. Those interfaces provide no
Morgenstern statement or proof credit. All six downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
