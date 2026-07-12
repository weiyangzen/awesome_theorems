# THM-M-1116 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "preferential
attachment model". The source inventory gives Barabasi and Albert, the year 1999, and only the
gloss "scale-free network model". That describes a model and a phenomenon, not a unique theorem:
degree-distribution limits, expected degree counts, maximum degree, and almost-sure statements are
different propositions, and several non-equivalent random graph processes are called preferential
attachment.

The intended theorem family is a power-law degree-distribution result for a growing random graph
in which attachment probability is proportional to current degree. The precise process, initial
graph, attachment rule, random variable, convergence mode, and limiting formula remain open for
the statement phase. The provisional root vector is `[H1, M4, R4]`. No exact source proposition,
Lean target, source review, formal candidate, audit completion, or theorem completion is claimed.

`scope-map.md` records the proposition-changing choices,
`source-statement-crosswalk.md` records the source ambiguity and required mapping, and
`task-dag.json` leaves every downstream phase open. The intake checks are in `validation.md`.
