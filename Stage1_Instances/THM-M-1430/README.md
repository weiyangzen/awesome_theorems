# THM-M-1430 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Mandelbrot集` (Mandelbrot set). The source gloss, `复二次多项式的参数空间` ("parameter
space of complex quadratic polynomials"), identifies a mathematical object and subject area, not
a truth-valued theorem with ordered binders, hypotheses, and a conclusion. The catalog value
`已验证` is explicitly untrusted under rev-5.6 and supplies neither human-source nor Lean proof
credit.

A familiar definition would take parameters `c : ℂ` for which the critical orbit of `0` under
`z ↦ z^2 + c` is bounded. Even that normalization is not fixed by the repository wording: it does
not choose the quadratic-family coordinates, marked critical point, orbit indexing, or boundedness
encoding. Nor does it state a property of the resulting set. Selecting its connectedness would be
an especially direct substitution because the repository assigns that result to the distinct
`THM-M-1431` Douady-Hubbard target.

This intake therefore freezes the ambiguity rather than manufacturing a theorem. The provisional
root vector is `[H5, M4, R4]`: `H5` classifies the supplied object/topic label as not yet a stable
proposition; `M4` records that no usable formal target or proof artifact was located; `R4` records
that no proof reconstruction can exist before a proposition is selected. It does not refute the
standard definition or any established theorem about the Mandelbrot set.

The structured authority is `instance.json`, the permitted subject boundary is in `scope-map.md`,
and the literal repository mapping is in `source-statement-crosswalk.md`. All dependent phases
remain open in `task-dag.json`. `IntakeProbe.lean` checks only adjacent pinned complex-number,
iteration, and bounded-set APIs; it introduces no target declaration. Exact commands and limits
are recorded in `validation.md` and `intake-receipt.json`.

No H0, M0, R0, accepted proof state, audit completion, theorem completion, accepted receipt, or
master acceptance is claimed.
