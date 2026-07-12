import Mathlib.Dynamics.BirkhoffSum.Average
import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1055: exact ergodic Birkhoff target

This module freezes the real-valued, probability-space, ergodic specialization
of the pointwise Birkhoff theorem. It states only the target and contains no
proof of that target.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1055

universe u

/-- On every probability space, the Birkhoff averages of an integrable real
observable along an ergodic transformation converge almost everywhere to its
space integral. `Ergodic T mu` includes measurability and preservation of
`mu`; `birkhoffAverage` averages the first `n` iterates and is zero at `n = 0`.
-/
def BirkhoffErgodicTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℝ),
    Ergodic T mu → Integrable f mu →
      ∀ᵐ x ∂mu,
        Tendsto (fun n : ℕ ↦ birkhoffAverage ℝ T f n x) atTop
          (nhds (∫ y, f y ∂mu))

/-- The checked local spelling used to expose all ordered binders. -/
def ExpandedTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℝ),
    Ergodic T mu → Integrable f mu →
      ∀ᵐ x ∂mu,
        Tendsto (fun n : ℕ ↦ birkhoffAverage ℝ T f n x) atTop
          (nhds (∫ y, f y ∂mu))

theorem birkhoffErgodicTarget_iff_expandedTarget :
    BirkhoffErgodicTarget.{u} ↔ ExpandedTarget.{u} :=
  Iff.rfl

-- Structural mutations elaborated separately by the statement validator.
def mutationRemovedErgodicity : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℝ),
    Integrable f mu →
      ∀ᵐ x ∂mu,
        Tendsto (fun n : ℕ ↦ birkhoffAverage ℝ T f n x) atTop
          (nhds (∫ y, f y ∂mu))

def mutationRemovedIntegrability : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℝ),
    Ergodic T mu →
      ∀ᵐ x ∂mu,
        Tendsto (fun n : ℕ ↦ birkhoffAverage ℝ T f n x) atTop
          (nhds (∫ y, f y ∂mu))

def mutationChangedObservableCodomain : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℂ),
    Ergodic T mu → Integrable f mu →
      ∀ᵐ x ∂mu,
        Tendsto (fun n : ℕ ↦ birkhoffAverage ℂ T f n x) atTop
          (nhds (∫ y, f y ∂mu))

def mutationChangedLimitToZero : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℝ),
    Ergodic T mu → Integrable f mu →
      ∀ᵐ x ∂mu,
        Tendsto (fun n : ℕ ↦ birkhoffAverage ℝ T f n x) atTop (nhds 0)

end Stage1Instances.THM_M_1055

set_option pp.explicit true in
#print Stage1Instances.THM_M_1055.BirkhoffErgodicTarget
