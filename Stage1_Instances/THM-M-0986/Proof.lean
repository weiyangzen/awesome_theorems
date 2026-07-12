import ObligationTree

/-!
# THM-M-0986 proof

This module closes the frozen machine-proof route: integrability and identical
distribution provide measurability, finite sums preserve it, mathlib's pinned
strong law supplies almost-everywhere convergence, and the frozen composition
transports that convergence to the exact weak-law target.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology Function

namespace Stage1Instances.THM_M_0986

universe u

/-- Finite empirical averages are a.e. strongly measurable whenever every
observation is. -/
theorem averageMeasurabilityPackage : AverageMeasurabilityPackage.{u} := by
  intro Omega _ mu X hmeas n
  unfold empiricalAverage
  exact AEStronglyMeasurable.const_mul
    (aestronglyMeasurable_fun_sum (range n) fun i _ => hmeas i) (n : Real)⁻¹

/-- The almost-everywhere package is exactly the real specialization of the
pinned mathlib strong law. -/
theorem strongLawPackage : StrongLawPackage.{u} := by
  intro Omega _ mu _ X hint hindep hident
  simpa only [empiricalAverage, smul_eq_mul] using
    (ProbabilityTheory.strong_law_ae X hint hindep hident)

/-- Khinchin's weak law in the exact statement frozen by `Statement.lean`. -/
theorem khinchinWeakLaw : KhinchinWeakLawTarget.{u} :=
  root_of_strongLaw_packages strongLawPackage averageMeasurabilityPackage

#print axioms averageMeasurabilityPackage
#print axioms strongLawPackage
#print axioms khinchinWeakLaw

end Stage1Instances.THM_M_0986
