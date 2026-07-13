# THM-M-0207 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0207`, the catalog item
`拿破仑定理` (Napoleon's theorem). The repository gives only the gloss "the centers of equilateral
triangles constructed externally on a triangle form an equilateral triangle," attributes it to
Napoleon Bonaparte in 1825, and labels it `已验证`. Those are uncited, untrusted catalog fields, not
an exact source crosswalk or machine-proof evidence.

The gloss identifies the classical external Napoleon theorem family, but not one formal
proposition. It leaves open the Euclidean-plane model, nondegeneracy of the original triangle,
orientation and the meaning of "external," correspondence of constructed triangles to sides,
whether "center" means centroid or another coincident center, and the exact equilateral predicate.
It also does not distinguish the internal variant. Intake freezes these choices as open rather than
silently supplying them from convention.

Pinned mathlib exposes affine triangles, their centroids, and an equilateral-simplex predicate with
distance and angle lemmas. `IntakeProbe.lean` authenticates those adjacent interfaces. A bounded
search found no Napoleon theorem or external-equilateral-triangle construction in the pinned local
closure. The probe therefore supplies discovery evidence only, not a usable root or proof body.

The provisional vector is `[H1, M4, R4]`: a recognizable classical theorem family lacks an
accepted pinpoint source and assumption map; no usable exact formal artifact has been located; and
no source-faithful readable proof reconstruction exists. `instance.json` is the structured scope
authority and `task-dag.json` keeps all six downstream phases open. No canonical Lean statement,
H0, M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
