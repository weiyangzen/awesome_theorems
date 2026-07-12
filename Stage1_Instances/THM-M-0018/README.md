# THM-M-0018 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Artin-Schreier theorem`. The repository attributes it to Emil Artin and Otto Schreier in 1927,
but gives only the gloss `the theory of real closed fields`. That identifies a historical theorem
family, not one binder-complete proposition.

The inspected source leads distinguish several proposition-changing readings: the characterization
of real closed fields by a finite nontrivial algebraic closure, the construction and uniqueness of
real closures of ordered fields, and the orderability criterion that `-1` is not a sum of squares.
The same English name is also used for a different characteristic-`p` extension theorem. The
catalog selects none of these, so this intake does not choose a convenient variant from memory or
conjoin an entire theory into a replacement target.

`IntakeProbe.lean` elaborates only adjacent pinned APIs for semireal rings, orderings, real closed
fields, algebraically closed fields, algebraic extensions, and finite dimension. In particular,
pinned mathlib's `IsRealClosed` class adopts one polynomial/square presentation and expressly leaves
equivalent conditions as future work. The probe is vocabulary evidence, not an Artin-Schreier
statement or proof.

The provisional vector is `[H1, M4, R4]`: credible primary and authoritative source leads identify
the established family, but exact source-root selection, assumptions, correction review, and
independent approval remain open; no usable exact formal artifact is credited; and no readable
proof reconstruction can attach to an unfrozen root. All six downstream phases remain open. No
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
