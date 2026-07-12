# THM-M-0197 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`费马点定理` (Fermat point theorem). The repository supplies only the gloss
`三角形内到三顶点距离之和最小的点`: a point inside a triangle for which the sum of the
distances to its three vertices is minimal. It attributes the item to Pierre de Fermat in 1643
and labels it `已验证`; the label is untrusted metadata, not source or kernel evidence.

The gloss does not determine one proposition. It omits the ambient Euclidean plane, triangle
nondegeneracy, whether `内` means strict interior or the closed triangle, the comparison domain,
existence versus uniqueness, and whether the result includes the 120-degree characterization.
These omissions are material. A reviewed modern source lead states two branches: an angle at least
120 degrees makes the corresponding vertex the minimizer, while otherwise the unique minimizer is
inside and sees the three sides at 120 degrees. Thus an unrestricted strict-interior reading of the
catalog gloss conflicts with the first branch. Intake cannot silently add an all-angles-less-than-
120-degrees hypothesis or broaden "inside" to include the boundary or the whole plane.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received wording as not yet a
stable proposition; it does not say that the Fermat-Torricelli theorem is false or open. A pinned
Lean probe checks generic distance, convex-hull, triangle-angle, and minimum interfaces only. It
declares no target and supplies no proof credit.

The structured scope authority is `instance.json`. `scope-map.md` records proposition-changing
choices and exclusions, `source-statement-crosswalk.md` records the repository wording and the
inspected modern source lead, and `task-dag.json` leaves all dependent phases open. No canonical
Lean expression, source acceptance, H0, M0, R0, audit completion, theorem completion, or master
acceptance is claimed.
