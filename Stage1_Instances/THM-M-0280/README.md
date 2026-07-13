# THM-M-0280 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Minkowski's inequality. The
repository catalogue gives Hermann Minkowski, the year 1896, and only the gloss "the triangle
inequality in L^p space." Its `已验证` label is untrusted metadata under rev-5.6 and supplies no
source, statement, or proof credit.

The gloss identifies the classical theorem family but not one proposition. It does not select a
measure-theoretic integral formula, the extended `eLpNorm` seminorm, the real-valued `lpNorm`, or
the norm triangle inequality on the almost-everywhere quotient `Lp`. It also leaves open the
exponent domain and endpoints, measure space, scalar or vector codomain, measurability and
integrability premises, and treatment of infinite seminorms. Choosing any familiar formulation at
intake would silently supply proposition-changing mathematics.

Pinned mathlib contains several strong exact-topic candidates. In particular,
`MeasureTheory.eLpNorm_add_le` handles extended exponents `p >= 1`, including infinity, while
`MeasureTheory.lpNorm_add_le`, `ENNReal.lintegral_Lp_add_le`, the normed `Lp` instance, and finite-
sum `Real.Lp_add_le` expose different surfaces. `IntakeProbe.lean` authenticates those interfaces
and their direct axiom reports where applicable. None is silently equated with the unfrozen
catalogue root, and no terminal body or proof credit is audited in this phase.

The provisional vector is `[H1, M3, R4]`: a classical published theorem family is recognizable but
no immutable pinpoint source and assumption map has been accepted; usable pinned formal candidates
exist but no canonical source-faithful Lean expression or checked transport is frozen; and no
source-faithful readable proof reconstruction exists. `instance.json` is the structured scope
authority and `task-dag.json` leaves all six downstream phases open.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
