# THM-M-0629 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Alexandroff one-point
compactification theorem family. The repository catalog gives only the gloss `局部紧Hausdorff空间的
一点紧化` (one-point compactification of a locally compact Hausdorff space), attributes it to
Pavel Alexandrov in 1924, and labels it `已验证`. The label is untrusted inventory metadata under
rev-5.6, not a source or kernel receipt.

The gloss identifies a standard theorem family, but not one binder-complete proposition. It does
not say whether the root is the construction, compact Hausdorff extension, open or dense embedding,
one-point complement, uniqueness characterization, or a conjunction of these. Density changes the
domain: a compact input is not dense in mathlib's `OnePoint X`, which deliberately adds an isolated
point when `X` is already compact. Intake therefore does not add a noncompactness hypothesis or
silently select a convenient property bundle.

`IntakeProbe.lean` authenticates the direct pinned mathlib interfaces for this family. The probe is
API evidence only; exact source identity, a canonical expression, checked transports, proof-body
provenance, and trust closure remain downstream.

An archival scan was inspected at the exact primary passage: Alexandroff's `Fundamentalsatz 1`,
journal page 296. It explicitly assumes the space is not itself `bikompakt`, adjoins one point to
make it `bikompakt`, and asserts uniqueness. The following page warns that uniqueness can fail for
the merely `kompakt` analogue. Mapping this 1924 terminology to modern compact Hausdorff language
and to a precise Lean bundle still needs independent review.

The provisional vector is `[H1, M3, R4]`: a primary theorem and proof passage is located but its
historical terminology, dependencies, proof boundary, and exact catalog mapping are not accepted;
direct formal interfaces exist but no source-exact root is frozen; and no source-faithful proof
reconstruction exists. `instance.json` is the structured scope authority and
`task-dag.json` leaves all six later phases open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
