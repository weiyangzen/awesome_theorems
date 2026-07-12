import Statement

/-!
# THM-M-0985 conditional obligation composition

This module checks the architecture's child-to-root boundary. The pinned
strong-law theorem remains an explicit premise; this file does not claim the
root proof.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THMM0985.ObligationTree

universe u

/-- Exact imported terminal interface, kept separate from the canonical root
so its provenance and trust closure cannot be hidden by a short wrapper. -/
def PairwiseStrongLawPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
      (X : Nat -> Omega -> Real),
    Integrable (X 0) mu ->
    Pairwise (Function.onFun (fun f g => ProbabilityTheory.IndepFun f g mu) X) ->
    (forall n, ProbabilityTheory.IdentDistrib (X n) (X 0) mu mu) ->
    ∀ᵐ omega ∂mu,
      Tendsto (fun n : Nat => (n : Real)⁻¹ * ∑ i ∈ range n, X i omega)
        atTop (𝓝 (∫ x, X 0 x ∂mu))

/-- Mutual independence supplies the exact pairwise premise of the imported
terminal interface. -/
theorem pairwise_of_mutual {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real)
    (h : ProbabilityTheory.iIndepFun X mu) :
    Pairwise (Function.onFun (fun f g => ProbabilityTheory.IndepFun f g mu) X) := by
  intro i j hij
  exact h.indepFun hij

/-- Checked composition from the frozen imported-terminal interface into the
exact canonical statement. Measurability and probability-space assumptions
are preserved even though this terminal interface does not consume them. -/
theorem root_of_pairwiseStrongLawPackage
    (strongLaw : PairwiseStrongLawPackage.{u}) :
    Stage1Instances.THMM0985.KolmogorovStrongLaw.{u} := by
  intro Omega _ mu _ X _hMeas hMutual hIdent hIntegrable
  exact strongLaw Omega mu X hIntegrable (pairwise_of_mutual mu X hMutual) hIdent

#print axioms pairwise_of_mutual
#print axioms root_of_pairwiseStrongLawPackage

end Stage1Instances.THMM0985.ObligationTree
