# THM-M-0908 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0908`, catalogued as
`Thomassen定理`. The repository supplies Carsten Thomassen, the year 1994, and only the gloss
`平面图的列表色数` (the list chromatic number/list coloring of planar graphs). It supplies no
citation, definition, binders, graph or planarity convention, list-coloring convention, numbered
result, proof boundary, errata record, or formal artifact. The catalog's `已验证` field is untrusted
metadata under rev-5.6.

## Intake result

Bibliographic metadata identifies the intended family with C. Thomassen's two-page paper *Every
Planar Graph Is 5-Choosable*, *Journal of Combinatorial Theory, Series B* 62(1) (1994), 180-181,
DOI `10.1006/jctb.1994.1062`. Secondary literature states the conventional result: every planar
graph is 5-choosable, meaning it remains properly colorable whenever every vertex is assigned a
list of at least five available colors. These records distinguish the target from ordinary
five-colorability, but no immutable primary text or pinpoint theorem/proof passage was admitted.

The family still does not select one binder-complete proposition. Material choices include finite
versus locally finite graphs, abstract planarity versus a supplied plane embedding, simple graphs
versus plane-map structures, exactly-five versus at-least-five finite color sets, the color carrier,
disconnected and degenerate graphs, and `5`-choosability versus a list-chromatic-number inequality.
Installing a familiar modern formulation at intake would add decisions that the repository source
does not make.

Pinned mathlib supplies ordinary simple-graph coloring but no located list-coloring or graph-
planarity interface; the coloring module lists planar graphs as future work. `IntakeProbe.lean`
checks only this adjacent substrate. An immutable external Lean lead declares a five-list-coloring
result for a narrower supplied `PlanarGraph`, but its proof and dependencies contain explicit
placeholders and use a different toolchain. It supplies interface discovery only and no machine
credit.

Accordingly the canonical human and Lean statements remain null, the provisional root vector is
`[H1, M4, R4]`, and all six downstream tasks remain open. No exact statement, H0, M0, R0, accepted
proof state, audit completion, theorem completion, or master acceptance is claimed.
