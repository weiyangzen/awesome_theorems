# THM-M-0184 rev-5.6 intake

This directory is the new rev-5.6 `planned` instance for the repository entry called
"Donaldson theorem." It does not inherit proof credit from the historical
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_131.lean` artifact or from the untrusted
source label `已验证`.

The repository source phrase, "moduli spaces of anti-self-dual connections on four-manifolds," is
not a uniquely identified theorem. This intake therefore freezes the intended theorem family and
the unresolved choices rather than inventing an exact theorem. The scope is a gauge-equivalence
quotient of anti-self-dual connections on an oriented compact Riemannian smooth four-manifold,
with regularity, expected dimension, orientation, and Uhlenbeck compactification as the intended
output package. The exact bundle, compact Lie group, irreducibility, generic-metric,
characteristic-class, and boundary hypotheses remain mandatory statement-phase decisions.

The structured authority is `intake.json`. `scope-map.md` records included and excluded surfaces,
`source-statement-crosswalk.md` records the source ambiguity and primary discovery anchors, and
`task-dag.json` keeps every dependent phase open.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M3, R3]`. The first failed theorem gate is
exact source identification: the metadata wording does not determine one canonical Donaldson
theorem. No Lean declaration is credited, no kernel closure is claimed, and the theorem is not
complete.

