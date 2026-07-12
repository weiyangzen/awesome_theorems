import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0994: obligation-tree composition probe

This module checks the interfaces and child-to-parent composition frozen by
registry version 1.  The two substantive interfaces remain premises, so this
is architecture evidence and not a proof of Hoeffding's inequality.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0994.ObligationTree

universe u v

def Root : Prop :=
  forall (I : Type v) [Fintype I]
    (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : I -> Omega -> Real) (a b : I -> Real),
      (forall i, Measurable (X i)) ->
      iIndepFun X mu ->
      (forall i, ∀ᵐ omega ∂mu, X i omega ∈ Set.Icc (a i) (b i)) ->
      forall epsilon : Real, 0 <= epsilon ->
        mu.real {omega | epsilon <=
          Finset.univ.sum (fun i => X i omega - ∫ x, X i x ∂mu)} <=
        exp ((-2 * epsilon ^ 2) /
          Finset.univ.sum (fun i => (b i - a i) ^ 2))

/-- The pinned mathlib route through centered independence, Hoeffding's lemma,
and the finite-sum subgaussian tail theorem. -/
def ProxyBoundInterface : Prop :=
  forall (I : Type v) [Fintype I]
    (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : I -> Omega -> Real) (a b : I -> Real),
      (forall i, Measurable (X i)) ->
      iIndepFun X mu ->
      (forall i, ∀ᵐ omega ∂mu, X i omega ∈ Set.Icc (a i) (b i)) ->
      forall epsilon : Real, 0 <= epsilon ->
        mu.real {omega | epsilon <=
          Finset.univ.sum (fun i => X i omega - ∫ x, X i x ∂mu)} <=
        exp (-epsilon ^ 2 /
          (2 * (Finset.univ.sum
            (fun i => ((nnnorm (b i - a i) / 2) ^ 2)) : NNReal)))

/-- Algebraic and boundary transport from mathlib's nonnegative proxy to the
exact real denominator. The proof phase must derive this from the interval
hypotheses, including the zero-total-width case. -/
def ProxyTransportInterface : Prop :=
  forall (I : Type v) [Fintype I] (a b : I -> Real) (epsilon : Real),
    0 <= epsilon ->
    (forall i, a i <= b i) ->
    exp (-epsilon ^ 2 /
      (2 * (Finset.univ.sum
        (fun i => ((nnnorm (b i - a i) / 2) ^ 2)) : NNReal))) <=
    exp ((-2 * epsilon ^ 2) /
      Finset.univ.sum (fun i => (b i - a i) ^ 2))

/-- Checked composition of the proxy theorem and exact-denominator transport.
The almost-sure bounds imply ordered interval endpoints because `mu` is a
probability measure. -/
theorem root_compose
    (proxy : ProxyBoundInterface.{u, v})
    (transport : ProxyTransportInterface.{v}) : Root.{u, v} := by
  intro I _ Omega _ mu _ X a b hmeas hindep hbound epsilon hepsilon
  have hab : forall i, a i <= b i := by
    intro i
    obtain ⟨omega, homega⟩ := (hbound i).exists
    exact homega.1.trans homega.2
  exact (proxy I Omega mu X a b hmeas hindep hbound epsilon hepsilon).trans
    (transport I a b epsilon hepsilon hab)

#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#print axioms root_compose

end Stage1Instances.THM_M_0994.ObligationTree
