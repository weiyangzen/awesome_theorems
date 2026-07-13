import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-!
# THM-M-0268 discovery-only intake probe

These checks authenticate exact-topic dominated-convergence interfaces in the pinned mathlib
snapshot. They do not select a source proposition, freeze the canonical Lean target, audit
terminal proof-body provenance, or give the repository target proof credit.
-/

#check MeasureTheory.tendsto_integral_of_dominated_convergence
#check MeasureTheory.tendsto_integral_filter_of_dominated_convergence
#check MeasureTheory.tendsto_lintegral_of_dominated_convergence
#check MeasureTheory.tendsto_lintegral_of_dominated_convergence'
#check MeasureTheory.tendsto_lintegral_filter_of_dominated_convergence
#check MeasureTheory.hasFiniteIntegral_of_dominated_convergence
#check MeasureTheory.tendsto_lintegral_norm_of_dominated_convergence

#print axioms MeasureTheory.tendsto_integral_of_dominated_convergence
#print axioms MeasureTheory.tendsto_lintegral_of_dominated_convergence
#print axioms MeasureTheory.hasFiniteIntegral_of_dominated_convergence
