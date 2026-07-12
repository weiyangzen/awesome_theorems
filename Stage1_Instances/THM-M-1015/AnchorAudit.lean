import Mathlib.MeasureTheory.Function.ConvergenceInDistribution

/-!
# THM-M-1015 pinned anchor probes

These wrappers check the three globally continuous branches supplied by the
pinned mathlib Slutsky family.  Division is deliberately absent: `(x, y) ↦
x / y` is not continuous on all of `Real × Real`, so the global continuous-map
anchor does not directly prove the frozen quotient branch.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Topology ProbabilityTheory

namespace Stage1Instances.THM_M_1015.AnchorAudit

universe u v w

variable {iota : Type u} {Omega : Type v} {OmegaL : Type w}
  [MeasurableSpace Omega] [MeasurableSpace OmegaL]
  (mu : Measure Omega) [IsProbabilityMeasure mu]
  (muL : Measure OmegaL) [IsProbabilityMeasure muL]
  {l : Filter iota} [l.IsCountablyGenerated]
  {X Y : iota -> Omega -> Real} {Z : OmegaL -> Real} {c : Real}

/-- Direct wrapper around mathlib's pair-valued Slutsky theorem. -/
theorem pinnedPair
    (hXZ : TendstoInDistribution X l Z (fun _ : iota => mu) muL)
    (hY : TendstoInMeasure mu Y l (fun _ : Omega => c))
    (hYmeas : forall n, AEMeasurable (Y n) mu) :
    TendstoInDistribution (fun n omega => (X n omega, Y n omega)) l
      (fun omega => (Z omega, c)) (fun _ : iota => mu) muL :=
  hXZ.prodMk_of_tendstoInMeasure_const X Y Z hY hYmeas

/-- Direct wrapper around mathlib's additive specialization. -/
theorem pinnedAdd
    (hXZ : TendstoInDistribution X l Z (fun _ : iota => mu) muL)
    (hY : TendstoInMeasure mu Y l (fun _ : Omega => c))
    (hYmeas : forall n, AEMeasurable (Y n) mu) :
    TendstoInDistribution (fun n omega => X n omega + Y n omega) l
      (fun omega => Z omega + c) (fun _ : iota => mu) muL :=
  hXZ.add_of_tendstoInMeasure_const hY hYmeas

/-- Multiplication is a specialization of the continuous-function anchor. -/
theorem pinnedMul
    (hXZ : TendstoInDistribution X l Z (fun _ : iota => mu) muL)
    (hY : TendstoInMeasure mu Y l (fun _ : Omega => c))
    (hYmeas : forall n, AEMeasurable (Y n) mu) :
    TendstoInDistribution (fun n omega => X n omega * Y n omega) l
      (fun omega => Z omega * c) (fun _ : iota => mu) muL := by
  simpa using hXZ.continuous_comp_prodMk_of_tendstoInMeasure_const
    (g := fun p : Prod Real Real => p.1 * p.2) (by fun_prop) hY hYmeas

#check MeasureTheory.TendstoInDistribution.prodMk_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.continuous_comp_prodMk_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.add_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.continuous_comp
#print axioms pinnedPair
#print axioms pinnedAdd
#print axioms pinnedMul

end Stage1Instances.THM_M_1015.AnchorAudit
