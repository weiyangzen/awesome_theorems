# THM-M-1327 rev-5.6 intake

This directory is the `planned` intake for the Hessian comparison theorem. The repository source
supplies only the phrase "Hessian of the distance function". That phrase names a family of
comparison results rather than one exact theorem: upper sectional-curvature bounds and lower
sectional-curvature bounds give inequalities in opposite directions, with different model
functions and cut-locus domains.

Accordingly, this intake freezes the theorem family and its non-substitution boundary, but does not
invent a canonical member. The statement phase must select an inspected primary source and preserve
its curvature sign, distance domain, regularity, model function, and inequality direction. The
provisional root vector is `[H3, M4, R4]`. No exact Lean target, source fidelity, kernel proof, audit
completion, or theorem completion is claimed.

`scope-map.md` and `source-statement-crosswalk.md` record the decisions still needed;
`task-dag.json` is the open downstream DAG. Validation evidence is in `validation.md`.
