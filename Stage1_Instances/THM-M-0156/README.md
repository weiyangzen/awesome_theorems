# THM-M-0156 rev-5.6 dossier

This directory is the `planned` intake for the divergence theorem (Gauss--Ostrogradsky theorem).
The repository source freezes only the family-level claim: the volume integral of the divergence of
a vector field equals its outward flux across the boundary. It does not specify the domain,
regularity, integration, orientation, or boundary conventions needed to make that slogan a unique
proposition.

The statement phase selects the positive-dimensional rectangular-box formulation documented by the
pinned mathlib divergence module. `Statement.lean` freezes and elaborates its volume-divergence and
signed outward-face-flux equation without importing or asserting a proof of that proposition. This
scope decision does not silently claim a theorem for arbitrary sufficiently regular domains.

The provisional root vector is `[H1, M3, R4]`. The canonical Lean expression is self-tested pending
master acceptance. No accepted proof state, audit completion, or theorem completion is claimed. See
`statement.json` and `statement-validation.md` for the exact statement evidence.
