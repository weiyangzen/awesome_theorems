import DoobLp
import ObligationTree

/-!
# THM-M-1005 proof execution

This module closes the frozen proof architecture. It specializes the locally vendored strong
Doob `L^p` proof to the absolute-value submartingale, transports the real exponent back to the
frozen finite `ENNReal` exponent, and checks the result through the frozen root composer.
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

/-- Exact strong finite-horizon Doob estimate for the frozen `ENNReal` exponent interface. -/
theorem doobLpMomentEstimate : Stage1Instances.THM_M_1005.Statement.{u} := by
  intro Omega _ mu _ G f hf p hp hptop n
  have hp_ne_top : p ≠ (∞ : ENNReal) := by
    apply ne_of_lt
    simpa using hptop
  have hp_real : (1 : Real) < p.toReal := by
    rw [← ENNReal.toReal_one]
    exact ENNReal.toReal_strict_mono hp_ne_top hp
  have h := MeasureTheory.maximal_ineq_Lp
    (absSubmartingale hf) (fun _ _ => abs_nonneg _) hp_real n
  rw [ENNReal.ofReal_toReal hp_ne_top] at h
  rw [← eLpNorm_norm (f n)]
  simpa only [Stage1Instances.THM_M_1005.runningAbsMax, Real.norm_eq_abs, eLpNorm_norm] using h

/-- The same exact root, consumed by the composition boundary frozen before proof search. -/
theorem doobLpMomentEstimate_via_frozen_composition :
    Stage1Instances.THM_M_1005.Statement.{u} :=
  Stage1Instances.THM_M_1005.ObligationTree.root_of_strongDoobTerminal
    doobLpMomentEstimate

#check absSubmartingale
#check measurable_runningAbsMax
#check weakMaximal_abs
#check doobLpMomentEstimate
#check doobLpMomentEstimate_via_frozen_composition
#print axioms absSubmartingale
#print axioms measurable_runningAbsMax
#print axioms weakMaximal_abs
#print axioms MeasureTheory.maximal_ineq_Lp
#print axioms doobLpMomentEstimate
#print axioms doobLpMomentEstimate_via_frozen_composition

end Stage1Instances.THM_M_1005.Proof
