# THM-M-0948 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Szemeredi's theorem. The repository
catalog supplies the recognizable slogan "positive-density sets contain arbitrarily long arithmetic
progressions," attributes it to Endre Szemeredi in 1975, and labels it `verified`. Under rev-5.6 the
label is untrusted metadata and provides no source or proof credit.

The slogan does not yet determine an exact proposition. It does not define density, choose natural
numbers or integers, order the quantifiers, fix an interval normalization, require a positive
common difference, or dispose of lengths zero through two. It also does not say whether the intended
root is the infinite positive-density form or a finite quantitative form. Selecting any familiar
variant at intake would silently supply missing mathematics.

The publisher record and a scan of Szemeredi's 1975 Acta Arithmetica paper were inspected as a
primary-source lead. They confirm a matching work, but the scan is image-only and this intake did
not complete a reviewed transcription of the theorem, incorporated definitions, assumptions,
proof boundary, or errata. The provisional root vector is `[H1, M4, R4]`: `H1` records that source
reconstruction debt; `M4` records that the bounded repo/pinned-mathlib intake probe located no usable
exact artifact for the still-unidentified root; and `R4` records that no source-faithful readable
proof route can attach before the statement is frozen.

`IntakeProbe.lean` checks only adjacent pinned mathlib APIs: Schnirelmann density, Roth's three-term
theorem, and finite-color homothetic copies. None is the arbitrary-length positive-density theorem.
The exact scope boundary is in `scope-map.md`, the source mapping is in
`source-statement-crosswalk.md`, and all six downstream phases remain open in `task-dag.json`.

No canonical Lean proposition, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
