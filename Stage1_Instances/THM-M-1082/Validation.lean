import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

open MeasureTheory

/-!
# THM-M-1082 independent validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`.  It
inhabits the frozen target directly from the pinned one-field mathlib
definition, providing a same-worker differential check rather than a claim of
independent-runner validation.
-/

namespace AwesomeTheorems.THM_M_1082.Validation

universe u_1 u_2 u_3

variable {Omega : Type u_1} {E : Type u_2} {T : Type u_3}
variable {mOmega : MeasurableSpace Omega}
variable [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module Real E]

theorem independentRoot
    (X : T -> Omega -> E) (P : Measure Omega) :
    ProbabilityTheory.IsGaussianProcess X P <->
      forall I : Finset T,
        ProbabilityTheory.HasGaussianLaw (fun omega => I.restrict (X . omega)) P := by
  constructor
  · exact fun h => h.hasGaussianLaw
  · exact fun h => { hasGaussianLaw := h }

#check independentRoot
#print axioms independentRoot

end AwesomeTheorems.THM_M_1082.Validation
