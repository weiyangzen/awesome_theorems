import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

open MeasureTheory

/-!
# THM-M-1082 obligation composition

The two directions are explicit hypotheses in the final composition harness.  The
small checked lemmas below expose the constructor/projection boundary of the
pinned one-field structure; this file does not promote workflow state.
-/

namespace AwesomeTheorems.THM_M_1082.ObligationTree

universe u_1 u_2 u_3

variable {Omega : Type u_1} {E : Type u_2} {T : Type u_3}
variable {mOmega : MeasurableSpace Omega}
variable [MeasurableSpace E] [TopologicalSpace E] [AddCommMonoid E] [Module Real E]
variable (X : T -> Omega -> E) (P : Measure Omega)

abbrev FiniteDimensionalGaussian : Prop :=
  forall I : Finset T,
    ProbabilityTheory.HasGaussianLaw (fun omega => I.restrict (X . omega)) P

theorem forward_from_projection
    (h : ProbabilityTheory.IsGaussianProcess X P) :
    FiniteDimensionalGaussian X P :=
  h.hasGaussianLaw

theorem reverse_from_constructor
    (h : FiniteDimensionalGaussian X P) :
    ProbabilityTheory.IsGaussianProcess X P :=
  { hasGaussianLaw := h }

/-- Checked child-to-root composition.  Both registered directional children
are consumed rather than hidden behind an untyped equivalence claim. -/
theorem root_of_directions
    (forward : ProbabilityTheory.IsGaussianProcess X P ->
      FiniteDimensionalGaussian X P)
    (reverse : FiniteDimensionalGaussian X P ->
      ProbabilityTheory.IsGaussianProcess X P) :
    ProbabilityTheory.IsGaussianProcess X P <->
      FiniteDimensionalGaussian X P :=
  ⟨forward, reverse⟩

#print axioms forward_from_projection
#print axioms reverse_from_constructor
#print axioms root_of_directions

end AwesomeTheorems.THM_M_1082.ObligationTree
