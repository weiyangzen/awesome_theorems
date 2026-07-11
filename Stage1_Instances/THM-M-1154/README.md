# THM-M-1154 rev-5.6 intake

This directory is the `planned` intake dossier for regular boundary points of the classical
Dirichlet problem. The repository source supplies only the phrases "regular boundary point" and
"existence of a solution to the Dirichlet problem". Those phrases do not determine a unique
theorem: the domain, operator, dimension, solution notion, boundary data, and definition of
regularity are all absent.

The intended family is therefore frozen, but an exact theorem is not. The statement phase must
select an inspected primary source and distinguish pointwise boundary convergence at one regular
point from global solvability when every boundary point is regular. The legacy Lean module is
discovery input only and receives no rev-5.6 proof credit. The provisional root vector is
`[H3, M4, R4]`; no exact Lean target, audit completion, or theorem completion is claimed.

`scope-map.md`, `source-statement-crosswalk.md`, and `task-dag.json` record the boundary and the
remaining work. Reproducible intake checks are recorded in `validation.md`.
