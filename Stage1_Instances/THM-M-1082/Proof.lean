import ObligationTree

/-!
# THM-M-1082 proof-phase closure

This module closes the frozen proof graph by applying the checked projection,
constructor, and composition bodies to the exact canonical proposition.
-/

open MeasureTheory

namespace AwesomeTheorems.THM_M_1082.Proof

universe u_1 u_2 u_3

variable {Omega : Type u_1} {E : Type u_2} {T : Type u_3}
variable {mOmega : MeasurableSpace Omega}
variable [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module Real E]

/-- Exact proof-phase root assembled from both frozen directional bodies. -/
theorem gaussianProcess_iff_finiteDimensionalGaussian
    (X : T -> Omega -> E) (P : Measure Omega) :
    ProbabilityTheory.IsGaussianProcess X P <->
      forall I : Finset T,
        ProbabilityTheory.HasGaussianLaw (fun omega => I.restrict (X . omega)) P := by
  exact ObligationTree.root_of_directions X P
    (ObligationTree.forward_from_projection X P)
    (ObligationTree.reverse_from_constructor X P)

#check gaussianProcess_iff_finiteDimensionalGaussian
#print axioms gaussianProcess_iff_finiteDimensionalGaussian

end AwesomeTheorems.THM_M_1082.Proof
