# THM-M-0335 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Jones index theorem. The intended
claim is the index-value restriction for an inclusion of type `II_1` factors: below `4`, the index
is one of the discrete values `4 cos^2(pi/n)` for an integer `n >= 3`; together with the continuous
range at least `4`, this is conventionally written
`{4 cos^2(pi/n) | n = 3, 4, ...} union [4, infinity]`.

The original paper and immutable bibliographic metadata are identified, but its exact numbered
theorem, definitions, hypotheses, endpoint convention, and errata have not yet been independently
crosswalked. Those are statement-phase gates. The repository gloss "index values of subfactors"
does not by itself settle whether the target includes both the restriction and realization
directions, so realization is not silently included here.

A pinned Lean probe confirms that mathlib has concrete and abstract von Neumann algebra interfaces.
The bounded source search found no subfactor, Jones-index, finite-factor, or trace-index API from
which the exact proposition can presently be stated. The probe is encoding evidence only and gives
no statement or proof credit. The provisional root is `[H1, M4, R4]`; audit completion and theorem
completion are false.

