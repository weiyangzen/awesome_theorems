import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0166 anchor-audit probes

This file checks the frozen target and the strongest adjacent declarations in
the pinned mathlib snapshot. None of the adjacent declarations proves the
Hopf-Rinow root.
-/

open Manifold

#check pathELength
#check riemannianEDist
#check riemannianEDist_le_pathELength
#check exists_lt_of_riemannianEDist_lt
#check exists_lt_locally_constant_of_riemannianEDist_lt
#check PseudoEMetricSpace.ofRiemannianMetric
#check EMetricSpace.ofRiemannianMetric
#check isCompact_closedBall
#check complete_of_proper

#print axioms riemannianEDist_le_pathELength
#print axioms exists_lt_of_riemannianEDist_lt
#print axioms exists_lt_locally_constant_of_riemannianEDist_lt
