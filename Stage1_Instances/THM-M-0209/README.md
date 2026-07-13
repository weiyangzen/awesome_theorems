# THM-M-0209 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the
Descartes circle theorem. The repository supplies only the gloss "the curvature relation of four
tangent circles," attributes it to Rene Descartes in 1643, and labels it verified. Under rev-5.6,
that label is untrusted inventory metadata rather than a source audit, exact Lean proposition, or
proof receipt.

Lagarias, Mallows, and Wilks' published article *Beyond the Descartes Circle Theorem* was inspected
as an authoritative modern source lead. Its Theorem 1.1 gives the familiar quadratic relation for
the bends of a Descartes configuration, while the surrounding text distinguishes positive-radius,
oriented/signed-curvature, enclosing-circle, and straight-line cases. It also reports that
Descartes' 1643 proof sketch was incomplete and identifies later complete proofs. This sharply
disambiguates the theorem family, but the repository does not cite the article, the source's exact
configuration and orientation definitions have not received independent review, and no historical
source proof was audited. The article is therefore an `H1` source lead, not `H0` evidence.

Pinned mathlib supplies Euclidean spheres and internal/external sphere-tangency predicates with
center-distance characterizations. `IntakeProbe.lean` authenticates those adjacent interfaces. A
bounded exact-topic search found no Descartes four-circle curvature theorem, oriented-circle model,
or signed-bend API in pinned mathlib or repo-local Lean. The probe is discovery evidence only.

The provisional vector is `[H1, M4, R4]`: an authoritative modern exact-statement and proof-route
lead is known but exact source admission and mapping remain open; no usable exact formal artifact is
credited; and no source-faithful proof reconstruction exists. `instance.json` is the structured
scope authority and `task-dag.json` keeps all six dependent phases open. No H0, M0, R0, accepted state, audit
completion, theorem completion, or master acceptance is claimed.
