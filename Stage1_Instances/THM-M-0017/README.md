# THM-M-0017 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Steinitz
theorem`. The repository attributes it to Ernst Steinitz in 1910 but gives only the gloss
`characterization of algebraically closed fields`. That identifies a field-theory family, not one
binder-complete proposition.

A direct inspection of Steinitz's paper finds several plausible roots. Section 21, Satz 9 on page
287 says that every field admits an algebraic extension to an algebraically closed field,
essentially uniquely. Satz 8 gives the more general polynomial-family splitting result from which
it is derived, while Section 17, Satz 2 concerns the smallest algebraically closed subextension of
an already algebraically closed overfield. A modern classification reading instead says that
algebraically closed fields are classified up to field isomorphism by characteristic and
transcendence degree. The catalog does not choose among these proposition-changing readings. Other
sources use the same theorem name for the primitive-element/intermediate-field equivalence or an
unrelated polytope theorem.

The primary paper and candidate passages were inspected through a versioned GDZ IIIF manifest and
page OCR. However, the catalog-to-`Satz` selection, exact transcription against the scan,
incorporated definitions, correction history, and independent review remain open. Consequently
this intake does not invent a canonical statement.

`IntakeProbe.lean` checks adjacent pinned mathlib algebraic-closure existence/uniqueness,
classification, transcendence-basis APIs, and the primitive-element namesake. These checks
establish vocabulary and collision boundaries only; they are not a source selection, canonical
statement, or proof.

The provisional vector is `[H1, M4, R4]`: a credible primary publication and secondary
disambiguation identify an established theorem family, but the exact source proposition remains
open; no exact theorem-specific formal artifact is credited; and no readable proof can attach to an
unfrozen root. All six downstream phases remain open. No accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
