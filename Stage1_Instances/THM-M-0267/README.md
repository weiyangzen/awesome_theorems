# THM-M-0267 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Arzela-Ascoli theorem. The
repository catalog gives only the title, the attribution Cesare Arzela/Giulio Ascoli, the year
1889, and the gloss "a criterion for compactness of sequences of functions." This identifies a
classical theorem family, but it does not fix one proposition with exact domains, topology,
hypotheses, conclusion, and direction.

Pinned mathlib contains direct named Arzela-Ascoli declarations for bounded continuous functions
on compact domains and for uniform convergence on compact sets. They are materially different:
some require a closed family, some conclude compactness of a closure, and their range-compactness
premises differ. The general module also leaves the converse compact-implies-equicontinuous result
as a TODO. Selecting one declaration from its name would silently decide whether the catalog means
a sequence-extraction theorem, a relative-compactness implication, or a full characterization.

The intake freezes the catalog record, source leads, candidate formal interfaces, unresolved scope
choices, and six open downstream phases while leaving the canonical statement and Lean target
null. The provisional vector is `[H1, M3, R4]`: the published classical family is identifiable but
the exact primary statement and assumption mapping are not audited; usable pinned statement
interfaces exist but no source-identical target or checked transport is frozen; and no proof
reconstruction exists for an exact root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record what later statement and source review must resolve.
`IntakeProbe.lean` authenticates candidate APIs only. No canonical proposition, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
