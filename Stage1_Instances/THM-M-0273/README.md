# THM-M-0273 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Radon-Nikodym theorem. The
repository catalogue gives Johann Radon and Otto Nikodym, the year 1930, and only the gloss
"absolute continuity of measures and density functions." Its `已验证` label is untrusted metadata
under rev-5.6 and supplies no source, statement, or proof credit.

The gloss identifies the classical theorem family but not one proposition. It does not select
positive, signed, complex, or vector measures; finite, sigma-finite, s-finite, or localizable
hypotheses; the orientation of the two measures; an `if`, `only if`, or `iff` result; the codomain
and measurability of the density; equality of measures versus an integral formula; or almost-
everywhere uniqueness. Choosing the familiar positive sigma-finite form at intake would silently
supply proposition-changing mathematics.

A publisher record and image-only scan of Nikodym's 1930 paper were inspected as a primary-source
lead. They match the historical family, but no reviewed transcription of a theorem passage,
incorporated definitions, exact assumptions, proof boundary, corrections, or errata is admitted.
Pinned mathlib contains the strong exact-topic candidate
`Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq`. It concerns positive measures under a
`HaveLebesgueDecomposition` instance and represents the density as an `ENNReal`-valued `rnDeriv`
through `withDensity`. A separate pinned declaration handles signed measures. Neither is silently
equated with the unfrozen catalogue root.

The provisional root vector is `[H1, M3, R4]`: a matching published source lead exists but its exact
statement mapping is open; a usable pinned formal candidate exists but no canonical source target
or checked transport is frozen; and no source-faithful readable proof reconstruction exists. All
six downstream phases remain open in `task-dag.json`.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
