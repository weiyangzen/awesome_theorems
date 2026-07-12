# THM-M-0791 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Woodin
cardinal". The repository source supplies only the gloss "properties of Woodin cardinals", an
attribution, a year, and an untrusted `verified` label. It does not state a proposition.

A Woodin cardinal is a large-cardinal notion with several equivalent characterizations involving
closure points, strongness for subsets or functions, elementary embeddings, and extender models.
Those formulations require substantial set-theoretic conventions and are not interchangeable as
formal targets until a source selects one. The word "properties" could denote a definition,
equivalence theorem, consequence, consistency-strength result, or interaction with determinacy.
Choosing any such result from the title alone would substitute invented mathematics for the target.

The intake therefore freezes the ambiguity and exclusion boundary rather than a proposition. The
root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes cardinals,
regular/inaccessible cardinals, and a ZFC-set model as nearby encoding ingredients; it is not a
Woodin-cardinal definition, theorem statement, or proof. Exact commands and results are recorded in
`validation.md`.
