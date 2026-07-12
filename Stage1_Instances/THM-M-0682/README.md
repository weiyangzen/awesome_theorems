# THM-M-0682 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`微分伽罗瓦理论` (differential Galois theory). The available source record gives only the subject
gloss "the Galois theory of differential equations", Ellis Kolchin, and 1973. It does not select a
theorem. In particular, it does not say whether the intended root is the Picard-Vessiot existence
theorem, the fundamental Galois correspondence, the fixed-field theorem, or a result about
solvability by Liouvillian functions.

The scope map preserves those alternatives without substituting one for the source. Pinned mathlib
contains differential-field and ordinary Galois-theory infrastructure, but the intake search found
no Picard-Vessiot extension or differential Galois correspondence declaration. `IntakeProbe.lean`
checks only the nearby infrastructure and receives no proof credit for the unspecified root.

The lifecycle is `planned` at `[H3, M4, R4]`. A pinpoint primary-source proposition, canonical Lean
expression, statement mutations, source approval, obligation tree, proof, and release evidence all
remain open. No accepted proof state, audit completion, or theorem completion is claimed.
