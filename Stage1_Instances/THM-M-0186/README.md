# THM-M-0186 rev-5.6 intake

This directory is the `planned` intake for the Willmore conjecture. The intended human claim is
the lower bound `W(f) >= 2*pi^2` for a smooth immersed two-torus in Euclidean three-space, with
scalar mean curvature normalized by `H = (k1 + k2) / 2`.

The 2014 Marques-Neves proof is a source anchor, not machine evidence. The exact source-to-Lean
assumption map and a concrete differential-geometric Lean target remain open. The provisional root
vector is `[H1, M4, R4]`; this dossier claims neither statement elaboration nor proof completion.

`scope-map.md` records inclusions and exclusions, `source-statement-crosswalk.md` separates the
Euclidean claim from the spherical min-max formulation, and `task-dag.json` keeps every later phase
open. Intake checks and their exact results are in `validation.md`.
