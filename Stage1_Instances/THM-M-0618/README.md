# THM-M-0618 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Heine-Borel theorem. The
repository catalog gives the attribution Eduard Heine/Emile Borel, the year 1895, and the gloss
`R^n中有界闭集等价于紧集` (in `R^n`, a set is bounded and closed if and only if it is compact).
It does not cite an edition or theorem, define `R^n`, fix the dimension binder, specify the
boundedness encoding, or record the empty and zero-dimensional cases.

Pinned mathlib contains `Metric.isCompact_iff_isClosed_bounded`, explicitly documented as the
Heine-Borel theorem for proper Hausdorff pseudometric spaces. It also contains
`FiniteDimensional.proper`, which supplies properness for finite-dimensional real normed spaces.
These are unusually close formal candidates. They do not by themselves authorize an exact
specialization to the catalog's `R^n`, choose between `EuclideanSpace Real (Fin n)` and
`Fin n -> Real`, or replace a source-reviewed statement crosswalk.

The provisional vector is `[H1, M3, R4]`: the classical published theorem family is identified,
but no pinpoint source proposition or independent source review is admitted; direct pinned Lean
interfaces elaborate without a frozen root or proof credit; and no source-faithful readable proof
reconstruction exists.

`instance.json` is the structured scope authority. The scope map and source-statement crosswalk
freeze the unresolved choices, `task-dag.json` leaves all six downstream phases open, and
`IntakeProbe.lean` checks candidate APIs only. No exact statement, H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
