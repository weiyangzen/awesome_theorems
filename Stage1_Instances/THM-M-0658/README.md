# THM-M-0658 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Shelah
stability theory". The source record says only "stability theory" and names a subject rather than
one theorem. It does not select a definition-equivalence theorem, a stability-spectrum theorem, a
type-counting bound, or a classification result. Intake preserves that ambiguity instead of
inventing a convenient root proposition.

The scope map records the model-theoretic objects and proposition-changing choices that a source-
pinned statement would need. The source crosswalk separates the repository metadata from Shelah's
monograph as a discovery lead. No edition, theorem/page, assumptions, or errata have yet been
accepted, so the historical `1978` and `已验证` labels supply no proof credit.

Pinned mathlib has first-order theories and complete type spaces. `IntakeProbe.lean` checks only
those ingredients. The scoped search found no model-theoretic stable-theory, order-property,
forking, or stability-spectrum declaration. The related legacy artifact for `THM-M-0660` defines a
local type-counting proxy and explicitly disclaims classical stability theory; it belongs to a
different target and is discovery input only.

The provisional root vector is `[H3, M4, R4]`. The canonical human claim and Lean expression remain
open, as do source review, obligation freezing, proof, audit, and release. This dossier claims only
a self-tested planned intake pending master acceptance, not statement closure, audit completion,
or theorem completion.
