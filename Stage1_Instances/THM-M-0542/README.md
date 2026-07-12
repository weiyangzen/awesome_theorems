# THM-M-0542 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "de Rham
cohomology". The authoritative record supplies only the gloss "cohomology of differential
forms". That describes a mathematical construction, not a unique theorem: it does not select a
degree, coefficient field, smoothness convention, manifold hypotheses, or a proposition about the
resulting cohomology.

The intake therefore freezes the intended construction family, real de Rham cohomology in degree
`k` as closed smooth differential `k`-forms modulo exact forms, while leaving the exact source
statement and Lean target open. It does not substitute the adjacent de Rham theorem, which asserts
a comparison with singular cohomology. The provisional root vector is `[H3, M4, R4]`; no exact
statement, proof, audit completion, or theorem completion is claimed.

The scope map records the proposition-critical choices. The source crosswalk separates repository
metadata, a historical primary-source lead, and existing abstract Lean discovery artifacts. Exact
intake validation is recorded in `validation.md`.
