import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Topology.MetricSpace.Holder

/-!
# THM-M-0304 discovery-only intake probe

These checks authenticate adjacent pinned Sobolev-inequality and Holder interfaces. The
inequalities concern sufficiently smooth compactly supported functions, while the Holder API only
states what Holder control means and what it implies. None supplies a source-selected Sobolev
representative theorem, so this file deliberately declares no target or proof body.
-/

#check MeasureTheory.lintegral_pow_le_pow_lintegral_fderiv
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check HolderOnWith
#check HolderOnWith.continuousOn
