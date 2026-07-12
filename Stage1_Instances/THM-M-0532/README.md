# THM-M-0532 rev-5.6 intake

This directory is the fail-closed `planned` intake for the Kunneth theorem. The repository source
fixes only the historical attribution and the gloss "homology groups of product spaces". That
gloss does not select among the integral short exact sequence, its noncanonical splitting, the
field-coefficient isomorphism, cohomological versions, or versions for chain complexes.

The intended family is the singular-homology Kunneth theorem for a product of topological spaces.
The exact coefficient ring, topological hypotheses, grading conventions, natural cross-product
map, Tor term, and source proposition remain open for the statement phase. The provisional root
vector is `[H3, M4, R4]`. No exact Lean target, source fidelity, proof, audit completion, or theorem
completion is claimed.

`scope-map.md` records all proposition-changing choices, `source-statement-crosswalk.md` separates
the repository metadata from source evidence, and `task-dag.json` keeps every later phase open.
Exact intake checks are recorded in `validation.md`.
