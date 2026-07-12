# THM-M-0639 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the point-set-topology catalog
record "Kakutani fixed-point theorem." The repository supplies only the gloss "a fixed point of a
set-valued map," an attribution to Shizuo Kakutani, the year 1941, and an untrusted `verified`
label. Those fields identify a familiar theorem family, not a binder-complete proposition.

## Intake result

The likely family is the classical finite-dimensional Kakutani theorem: a suitably upper
semicontinuous correspondence on a nonempty closed bounded convex Euclidean set, with nonempty
closed convex values contained in the domain, has a point belonging to its value. This description
is recorded only as a source-selection candidate. The catalog does not fix the ambient space,
compact versus closed-bounded presentation, value regularity, semicontinuity convention, encoding,
or boundary cases. The primary paper could not be inspected through its publisher endpoint during
this intake, so choosing that familiar formulation as the exact target would add unapproved
mathematics.

The separately scheduled `THM-M-0320` has the same title and theorem family in a different catalog
category. Its files are a discovery lead only. No statement, proof, debt, receipt, or completion
credit transfers to this target without an authoritative duplicate-resolution decision and fresh
target-specific evidence.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned mathlib types for Euclidean spaces, convexity,
boundedness, compactness, and upper hemicontinuity. It does not state or prove Kakutani's theorem.
The canonical mathematical statement and Lean expression remain null, and every downstream task
is open.

The provisional vector is `[H1, M4, R4]`: the published theorem and primary-source lead are known,
but exact statement/source mapping and independent review remain open; this target has no credited
formal artifact; and no proof reconstruction can attach to an unfrozen root. No accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
