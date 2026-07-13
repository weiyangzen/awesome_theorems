import Mathlib.Analysis.Complex.OpenMapping

/-!
# THM-M-0235 discovery-only intake probe

These checks authenticate direct open-mapping interfaces in the pinned mathlib snapshot. They do
not select one formulation as the catalog root, establish statement identity, or prove the target.
-/

#check AnalyticAt.eventually_constant_or_nhds_le_map_nhds
#check AnalyticOnNhd.is_constant_or_isOpen
#check AnalyticOnNhd.is_constant_or_isOpenMap
#check DifferentiableOn.analyticOnNhd
#check Complex.analyticOnNhd_iff_differentiableOn
#check IsOpenMap

#print axioms AnalyticAt.eventually_constant_or_nhds_le_map_nhds
#print axioms AnalyticOnNhd.is_constant_or_isOpen
#print axioms AnalyticOnNhd.is_constant_or_isOpenMap
