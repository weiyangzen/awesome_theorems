# THM-M-0194 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item "Thales'
theorem." The repository gives Thales of Miletus, approximately 600 BCE, and the gloss "an
inscribed angle is half the central angle." Its `已验证` label is untrusted metadata under
rev-5.6 and supplies no source, statement, or proof credit.

The gloss identifies the general inscribed-angle theorem family, but it does not yet determine one
proposition. In particular, it omits the common-circle hypotheses, the chord and arc selected by
the two angles, ordinary versus oriented angles, the minor/reflex convention, dimension and
orientation, distinctness premises, and degenerate cases. Those choices are material: division by
two is not automatically interchangeable with doubling for an angle represented modulo `2 * pi`.

Euclid's *Elements*, Book III, Proposition 20 is recorded as a matching source lead. A bounded
inspection of David E. Joyce's English edition states that the angle at the center is double the
angle at the circumference when both have the same circumference as base. The edition, incorporated
definitions, cases, attribution, corrections, and errata have not been independently reviewed, so
it is not H0 evidence.

Pinned mathlib contains the exact-topic candidate
`EuclideanGeometry.Sphere.oangle_center_eq_two_zsmul_oangle`. It proves an oriented-angle equality
in a two-dimensional oriented real inner-product affine space. The same module uses the name
`Sphere.thales_theorem` for the different semicircle/right-angle theorem. The latter must not be
substituted merely because its declaration bears the catalogue name.

The provisional vector is `[H1, M3, R4]`: a matching published source lead exists but the exact
source crosswalk is open; strong pinned formal candidates elaborate but no canonical claim or
checked source transport is frozen; and no source-faithful readable proof reconstruction exists.
All six downstream phases remain open in `task-dag.json`.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
