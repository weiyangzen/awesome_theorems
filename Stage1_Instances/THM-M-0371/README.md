# THM-M-0371 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Rubio de Francia extrapolation
theorem. The repository gives only the gloss "extrapolation of weighted inequalities", Jose Rubio
de Francia, and 1984. It does not state the initial exponent, the weight class, an operator or
family of pairs, the dependence of constants, or the extrapolated conclusion.

Several standard formulations are related but not literally interchangeable: extrapolation for a
family of pairs of nonnegative functions, an operator formulation, vector-valued extrapolation,
limited-range variants, and endpoint or off-diagonal results. Choosing one without a pinpoint
source would broaden or substitute the repository target.

This intake therefore freezes the ambiguity and scope boundary rather than inventing a theorem.
The provisional root is `[H1, M4, R4]`: the classical source is plausibly identifiable, but its
exact statement has not been inspected and independently crosswalked, and no formal target is
selected. `IntakeProbe.lean` only verifies pinned Lean APIs for weighted measures and `L^p`
quantities. It is not a theorem statement or proof.
