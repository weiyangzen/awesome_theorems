import Mathlib.Probability.Martingale.BorelCantelli
import Statement

/-!
# THM-M-1007 proof execution

This module closes the truncation, measurability, postcomposition-independence,
and summable-large-jump Borel--Cantelli leaves of the frozen proof tree.  The
two bounded independent-series directions are not available in pinned mathlib,
so no declaration of the canonical root is made here.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_1007.Proof

universe u

/-- The scalar function whose postcomposition realizes the canonical truncation. -/
def truncationFunction (c : Real) (x : Real) : Real :=
  if |x| <= c then x else 0

/-- Scalar truncation is Borel measurable. -/
theorem measurable_truncationFunction (c : Real) :
    Measurable (truncationFunction c) := by
  exact Measurable.ite (measurableSet_le measurable_id.norm measurable_const)
    measurable_id measurable_const

/-- The canonical truncation of a measurable random variable is measurable. -/
theorem measurable_truncate {Omega : Type u} [MeasurableSpace Omega]
    {c : Real} {Z : Omega -> Real} (hZ : Measurable Z) :
    Measurable (Stage1Instances.THM_M_1007.truncate c Z) := by
  simpa [Stage1Instances.THM_M_1007.truncate, truncationFunction,
    Function.comp_def] using (measurable_truncationFunction c).comp hZ

/-- The strict large-jump event in the canonical target is measurable. -/
theorem measurableSet_largeJump {Omega : Type u} [MeasurableSpace Omega]
    {X : Nat -> Omega -> Real} (hX : forall n, Measurable (X n))
    (c : Real) (n : Nat) :
    MeasurableSet {omega | c < |X n omega|} := by
  exact measurableSet_lt measurable_const (hX n).norm

/-- Measurable coordinatewise truncation preserves independence. -/
theorem iIndepFun_truncate {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {X : Nat -> Omega -> Real}
    (hX : iIndepFun X mu) (c : Real) :
    iIndepFun (fun n => Stage1Instances.THM_M_1007.truncate c (X n)) mu := by
  simpa [Stage1Instances.THM_M_1007.truncate, truncationFunction,
    Function.comp_def] using
      hX.comp (fun _ : Nat => truncationFunction c)
        (fun _ : Nat => measurable_truncationFunction c)

/-- Real summability of event probabilities supplies the `ENNReal` hypothesis
of pinned Borel--Cantelli. -/
theorem largeJump_tsum_ne_top {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real)
    (hs : Summable (fun n => mu.real {omega | c < |X n omega|})) :
    (∑' n, mu {omega | c < |X n omega|}) ≠ (⊤ : ENNReal) := by
  simpa [ofReal_measureReal] using
    (Summable.tsum_ofReal_ne_top
      (f := fun n => mu.real {omega | c < |X n omega|}) hs)

/-- The first three-series condition implies that large jumps occur only
finitely often, almost surely. -/
theorem ae_eventually_no_largeJump {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real)
    (hs : Summable (fun n => mu.real {omega | c < |X n omega|})) :
    ∀ᵐ omega ∂mu, ∀ᶠ n in atTop, ¬ c < |X n omega| := by
  simpa only [Set.mem_setOf_eq] using
    (ae_eventually_notMem (largeJump_tsum_ne_top mu X c hs))

/-- Eventual absence of large jumps makes the original and truncated terms
eventually identical, pointwise. -/
theorem eventuallyEq_truncate {Omega : Type u} (X : Nat -> Omega -> Real)
    (c : Real) (omega : Omega)
    (h : ∀ᶠ n in atTop, ¬ c < |X n omega|) :
    (fun n => Stage1Instances.THM_M_1007.truncate c (X n) omega) =ᶠ[atTop]
      (fun n => X n omega) := by
  filter_upwards [h] with n hn
  simp [Stage1Instances.THM_M_1007.truncate, not_lt.mp hn]

#print axioms measurable_truncationFunction
#print axioms measurable_truncate
#print axioms measurableSet_largeJump
#print axioms iIndepFun_truncate
#print axioms largeJump_tsum_ne_top
#print axioms ae_eventually_no_largeJump
#print axioms eventuallyEq_truncate

end Stage1Instances.THM_M_1007.Proof
