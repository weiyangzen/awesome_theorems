# THM-M-0403 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Schlickewei--Evertse
finiteness theorem used in the study of zeros of nondegenerate linear
recurrences. It does not inherit proof credit, statement acceptance, or build
evidence from the legacy `S1_M_016.lean` artifact.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Finiteness of the zero set of a nonempty simple exponential polynomial over a characteristic-zero field, assuming nonzero coefficients and roots and nontorsion quotients of distinct roots | This is the provisional canonical claim selected by the legacy dossier; exact Lean elaboration belongs to the statement phase |
| Deep arithmetic input | Finiteness of nondegenerate solutions of a linear equation in a finite-rank multiplicative group | Input architecture only; no proof or imported theorem is credited |
| Reduction | Convert a zero index into a multiplicative-group equation and separate vanishing proper subsums | Open proof architecture |
| Extraction | Bound each nondegenerate support pattern and deduce finiteness of zero indices | Open proof architecture |
| Recurrence wrapper | Characteristic-root decomposition of a simple nondegenerate linear recurrence | Downstream candidate, not the root; the full periodic zero-set theorem belongs to the adjacent Skolem--Mahler--Lech target |
| Degenerate cases | Repeated roots, zero coefficients/roots, torsion root quotients, and the identically-zero sequence | Excluded from this root and must be handled by separate transports or branches |
| Foundations | Lean 4 kernel plus pinned mathlib, with an accepted classical/choice/quotient policy | Exact profile and dependency fingerprint remain open |

The canonical human claim, ordered binders, exclusions, and provisional Lean
surface are structured in `intake.json`. Source genealogy and the unresolved
primary-source pinpoint audit are recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. `H2` is
deliberate: primary papers relevant to the multiplicative-group input and the
recurrence application have been identified, but an edition/page/theorem and
errata crosswalk has not been independently accepted. The first failed theorem
gate is the statement gate: no normalized expression hash, environment
fingerprint, checked transports, or mutation results exist under rev-5.6.
The theorem is not complete.

## Validation

The exact intake checks and results are recorded in `validation.md`. They
establish manifest membership, standard consistency, JSON syntax, and
dossier-local integrity only. They do not establish a Lean theorem.
