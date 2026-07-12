# THM-M-0640 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the point-set-topology catalog
record "Brouwer fixed-point theorem." The repository supplies the gloss "every continuous map
from an n-dimensional ball to itself has a fixed point," attributes it to Luitzen Brouwer, gives
the year 1910, and marks it with an untrusted `verified` label.

## Intake result

The wording identifies the classical finite-dimensional ball theorem, but it is not yet a
binder-complete proposition. It does not fix whether "ball" means the closed ball, the scalar and
Euclidean model, the range of the dimension, center and radius conventions, subtype versus ambient
self-map encoding, the continuity domain, or degenerate cases. In particular, replacing the ball
by an open ball would not merely change notation, and copying the compact-convex formulation owned
by `THM-M-0319` or the generic Brouwer family owned by `THM-M-0636` would silently resolve a
target-identity and transport question.

A 1911 Brouwer paper is recorded as a primary-source discovery lead, but no exact theorem/page,
incorporated definition chain, translation, correction or errata disposition, or independent
review is accepted. The canonical human statement and Lean expression therefore remain null.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned mathlib types for Euclidean space, metric
closed balls, continuity, maps into a set, and fixed points. It neither states nor proves Brouwer's
theorem. The bounded topic search is discovery only and is not the scheduled anchor audit.

The provisional vector is `[H1, M4, R4]`: a published theorem family and historical lead are known,
but exact source mapping remains open; no source-identical formal artifact is credited; and no
readable proof reconstruction can attach to an unfrozen root. Every downstream task remains open.
No accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
