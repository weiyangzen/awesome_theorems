import Statement
import Mathlib.MeasureTheory.Measure.Dirac

/-!
# THM-M-1056 statement-consistency sanity instance

This file constructs one nontrivial admissible instance of the frozen target's
conclusion. It is negative blocker evidence only: an existential example cannot
prove the target, which universally quantifies over every admissible cocycle.
-/

open Filter Function MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1056

/-- The identity on the one-point probability space is ergodic. -/
theorem unitRefl_ergodic : Ergodic (MeasurableEquiv.refl Unit) (Measure.dirac ()) where
  toMeasurePreserving := by
    simpa using MeasurePreserving.id (Measure.dirac ())
  toPreErgodic :=
    { aeconst_set := fun _ _ _ => EventuallyConst.of_subsingleton_left }

/-- All hypotheses of the canonical target hold for the identity cocycle on
the one-point base with real one-dimensional fiber. -/
theorem unitIdentityAntecedents :
    0 < Module.finrank Real Real ∧
      Ergodic (MeasurableEquiv.refl Unit) (Measure.dirac ()) ∧
      StronglyMeasurable (fun _ : Unit =>
        (ContinuousLinearEquiv.refl Real Real).toContinuousLinearMap) ∧
      Integrable (fun _ : Unit =>
        logPlus (norm (ContinuousLinearEquiv.refl Real Real).toContinuousLinearMap))
        (Measure.dirac ()) ∧
      Integrable (fun _ : Unit =>
        logPlus (norm (ContinuousLinearEquiv.refl Real Real).symm.toContinuousLinearMap))
        (Measure.dirac ()) := by
  exact ⟨by simp, unitRefl_ergodic, stronglyMeasurable_const,
    integrable_const _, integrable_const _⟩

/-- Identity cocycle iterates fix every real vector. -/
@[simp] theorem cocycleVector_unitRefl (n : Nat) (x : Real) :
    cocycleVector (MeasurableEquiv.refl Unit)
        (fun _ => ContinuousLinearEquiv.refl Real Real) n () x = x := by
  induction n with
  | zero => rfl
  | succ n ih => simp [cocycleVector, ih]

theorem cocycleVector_unitRefl' (n : Nat) (omega : Unit) (x : Real) :
    cocycleVector (MeasurableEquiv.refl Unit)
        (fun _ => ContinuousLinearEquiv.refl Real Real) n omega x = x := by
  cases omega
  exact cocycleVector_unitRefl n x

/-- A concrete splitting for the identity cocycle on a one-point base. -/
noncomputable def unitIdentitySplitting :
    LyapunovSplitting (MeasurableEquiv.refl Unit)
      (fun _ => ContinuousLinearEquiv.refl Real Real) (Measure.dirac ()) where
  count := 1
  count_pos := Nat.zero_lt_succ 0
  exponent := fun _ => 0
  exponent_strict := by
    intro i j hij
    have : i = j := Subsingleton.elim i j
    subst j
    exact (lt_irrefl i hij).elim
  projection := fun _ _ => ContinuousLinearMap.id Real Real
  projection_measurable := fun _ => stronglyMeasurable_const
  projection_idempotent := Filter.Eventually.of_forall fun _ _ => by simp
  projection_disjoint := Filter.Eventually.of_forall fun _ i j hij => by
    exact (hij (Subsingleton.elim i j)).elim
  projection_sum := Filter.Eventually.of_forall fun _ => by simp
  projection_nonzero := Filter.Eventually.of_forall fun _ _ => by
    intro h
    have := DFunLike.congr_fun h (1 : Real)
    simp at this
  equivariant := Filter.Eventually.of_forall fun _ _ => by simp
  growth := Filter.Eventually.of_forall fun _ _ x _ _ => by
    simp only [cocycleVector_unitRefl']
    exact tendsto_const_div_atTop_nhds_zero_nat (Real.log (norm x))

theorem unitIdentitySplitting_nonempty :
    Nonempty (LyapunovSplitting (MeasurableEquiv.refl Unit)
      (fun _ => ContinuousLinearEquiv.refl Real Real) (Measure.dirac ())) :=
  ⟨unitIdentitySplitting⟩

#print axioms unitIdentitySplitting_nonempty

end Stage1Instances.THM_M_1056
