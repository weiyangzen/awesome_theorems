import Statement

/-!
# THM-M-1005 proof execution

This module implements the normalization, finite-maximum measurability, and pinned weak-maximal
branches of the frozen proof architecture.  The layer-cake/Holder argument needed for the strong
`L^p` terminal remains open, so this module deliberately does not declare the canonical root.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1005.Proof

universe u

/-- `|f|` is a nonnegative submartingale when `f` is a real martingale. -/
theorem absSubmartingale {Omega : Type u} [mOmega : MeasurableSpace Omega]
    {mu : Measure Omega} {G : Filtration Nat mOmega} {f : Nat -> Omega -> Real}
    (hf : Martingale f G mu) : Submartingale (fun k omega => |f k omega|) G mu := by
  simpa only [abs_eq_max_neg, Pi.sup_apply, Pi.neg_apply] using
    hf.submartingale.sup hf.neg.submartingale

/-- The inclusive finite running absolute maximum is measurable. -/
theorem measurable_runningAbsMax {Omega : Type u} [mOmega : MeasurableSpace Omega]
    {mu : Measure Omega} {G : Filtration Nat mOmega} {f : Nat -> Omega -> Real}
    (hf : Martingale f G mu) (n : Nat) :
    Measurable (Stage1Instances.THM_M_1005.runningAbsMax f n) := by
  have hmeas : forall k, Measurable (f k) := fun k =>
    (hf.stronglyMeasurable k).measurable.mono (G.le k) le_rfl
  simpa only [Stage1Instances.THM_M_1005.runningAbsMax, Real.norm_eq_abs] using
    (Finset.measurable_range_sup'' (n := n) (f := fun k omega => |f k omega|)
      (fun k _ => (hmeas k).norm))

/-- Exact weak maximal estimate obtained by applying pinned mathlib to the absolute process. -/
theorem weakMaximal_abs {Omega : Type u} [mOmega : MeasurableSpace Omega]
    {mu : Measure Omega} [IsFiniteMeasure mu] {G : Filtration Nat mOmega}
    {f : Nat -> Omega -> Real} (hf : Martingale f G mu) {epsilon : NNReal} (n : Nat) :
    epsilon * mu {omega | (epsilon : Real) <=
        Stage1Instances.THM_M_1005.runningAbsMax f n omega} <=
      ENNReal.ofReal
        (integral (μ := mu.restrict {omega | (epsilon : Real) <=
          Stage1Instances.THM_M_1005.runningAbsMax f n omega})
          (fun omega => |f n omega|)) := by
  simpa only [Stage1Instances.THM_M_1005.runningAbsMax] using
    (MeasureTheory.maximal_ineq (absSubmartingale hf)
      (fun _ _ => abs_nonneg _) (ε := epsilon) n)

#check absSubmartingale
#check measurable_runningAbsMax
#check weakMaximal_abs
#print axioms absSubmartingale
#print axioms measurable_runningAbsMax
#print axioms weakMaximal_abs

end Stage1Instances.THM_M_1005.Proof
