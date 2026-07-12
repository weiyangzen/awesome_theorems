# THM-M-0156 rev-5.6 intake

This directory is the `planned` intake for the divergence theorem (Gauss--Ostrogradsky theorem).
The repository source freezes only the family-level claim: the volume integral of the divergence of
a vector field equals its outward flux across the boundary. It does not specify the domain,
regularity, integration, orientation, or boundary conventions needed to make that slogan a unique
proposition.

The intake therefore preserves the classical Euclidean theorem as the intended scope while leaving
those choices to the statement phase and a pinpoint source audit. The pinned mathlib contains a real
rectangular-box Bochner-integral divergence theorem, but that theorem is discovery evidence only: it
must not silently replace a general sufficiently regular domain theorem.

The provisional root vector is `[H1, M4, R4]`. No canonical Lean expression, accepted proof state,
audit completion, or theorem completion is claimed. See `scope-map.md`,
`source-statement-crosswalk.md`, and `task-dag.json` for the frozen boundary and downstream work;
`validation.md` records the intake checks.
