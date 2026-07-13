import Mathlib.Analysis.Complex.RemovableSingularity
import Mathlib.Analysis.Meromorphic.Order
import Mathlib.Topology.ClusterPt

/-!
# THM-M-0229 discovery-only intake probe

These checks authenticate adjacent pinned interfaces for punctured neighborhoods, complex
analyticity, removable and pole-like singularities, and cluster values. They do not define an
essential isolated singularity, select a canonical Great Picard statement, or provide a proof.
-/

#check nhdsWithin
#check DifferentiableAt
#check AnalyticAt
#check Complex.analyticAt_of_differentiable_on_punctured_nhds_of_continuousAt
#check Complex.tendsto_limUnder_of_differentiable_on_punctured_nhds_of_bounded_under
#check MeromorphicAt
#check MeromorphicAt.eventually_analyticAt
#check meromorphicOrderAt
#check tendsto_cobounded_iff_meromorphicOrderAt_neg
#check tendsto_nhds_iff_meromorphicOrderAt_nonneg
#check MapClusterPt
#check mapClusterPt_iff_frequently
