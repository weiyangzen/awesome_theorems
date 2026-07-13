# THM-M-0203 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0203`, the catalog item
`海伦公式` (Heron's formula). The repository supplies only the gloss "the relationship between a
triangle's area and its three sides," attributes it to Heron of Alexandria around 60 CE, and labels
it `已验证`. Those fields identify a familiar theorem family, but they are untrusted inventory
metadata rather than an exact source statement or proof evidence.

The gloss omits the formula, the definition of area, the triangle and ambient-space model, side
ordering, semiperimeter, nondegeneracy, equality orientation, squared-versus-square-root form, and
all boundary cases. Intake therefore records the conventional semiperimeter formula only as a
candidate family and does not silently make those proposition-changing choices.

Pinned mathlib contains a particularly strong exact-topic candidate in the non-default `Archive`
library: `Theorems100.heron` in `Archive/Wiedijk100Theorems/HeronsFormula.lean`. It equates the
trigonometric expression `1 / 2 * a * b * sin gamma` with
`sqrt (s * (s - a) * (s - b) * (s - c))` for three affine Euclidean points with two nonzero
adjacent sides. The pinned source elaborates directly with `lake env lean` and contains a real proof
body. The canonical cache has no prebuilt `Archive` object for it, and more importantly the catalog
does not select its area encoding, assumptions, or scope. It is therefore an uncredited formal
candidate, not a canonical target or machine-completion receipt.

The provisional vector is `[H1, M3, R4]`: the classical source family and historical attribution
are credible leads but no independently reviewed pinpoint human source has been admitted; an
exact-topic pinned formal interface exists but no source-identical target or checked transport is
frozen; and no accepted source-faithful reconstruction exists. `instance.json` is the structured
scope authority and `task-dag.json` keeps all six downstream phases open.

No canonical mathematical or Lean proposition, accepted source, proof-body credit, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
