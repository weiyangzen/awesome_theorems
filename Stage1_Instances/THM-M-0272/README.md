# THM-M-0272 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the real-analysis Tonelli theorem.
The repository catalog supplies Leonida Tonelli, the year 1909, and only the gloss `非负函数的重积分`
("multiple integrals of nonnegative functions"). Its `已验证` label is untrusted metadata under
rev-5.6 and supplies no source, statement, or proof credit.

The gloss identifies the classical nonnegative-product-integration family but not one proposition.
It does not fix the measure spaces or their finiteness assumptions, the product-measure convention,
the function's codomain and measurability, whether values at infinity are allowed, the order and
orientation of the equality, or whether set-integral and measurability conclusions are part of the
root. Selecting a familiar textbook or mathlib formulation at intake would silently supply
proposition-changing mathematics.

Pinned mathlib contains a direct named candidate, `MeasureTheory.lintegral_prod`, and several
curried, symmetric, set-integral, and order-swap variants in
`Mathlib.MeasureTheory.Measure.Prod`. These are materially different interfaces. They elaborate in
the discovery-only probe, but no source-approved canonical target or checked transport is frozen.
The unrelated `THM-M-1266` is a calculus-of-variations existence theorem and receives no credit
here. The legacy `S1_M_272.lean` file is for `THM-M-0992` (Chebyshev's inequality), not this target.

The provisional vector is `[H1, M3, R4]`: a published classical theorem family is identifiable,
but no immutable primary proof passage and complete premise map is admitted; strong pinned formal
interfaces exist without a frozen root; and no source-faithful proof reconstruction exists. All six
downstream phases remain open in `task-dag.json`.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
