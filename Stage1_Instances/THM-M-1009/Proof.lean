import Mathlib.Probability.BorelCantelli

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

universe u

namespace Stage1Instances.THM_M_1009

def partialEventMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  Finset.sum (Finset.range n) fun k => mu.real (A k)

def pairwiseEventMass {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  Finset.sum (Finset.range n) fun i =>
    Finset.sum (Finset.range n) fun j => mu.real (A i ∩ A j)

def eventMassRatio {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) : Real :=
  (partialEventMass mu A n) ^ 2 / pairwiseEventMass mu A n

/-- The finite counting random variable used in the second-moment argument. -/
def eventCount {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega) : Real :=
  Finset.sum (Finset.range n) fun k => (A k).indicator (fun _ => 1) omega

theorem partialEventMass_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) :
    0 <= partialEventMass mu A n := by
  exact Finset.sum_nonneg fun _ _ => measureReal_nonneg

theorem pairwiseEventMass_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) :
    0 <= pairwiseEventMass mu A n := by
  exact Finset.sum_nonneg fun _ _ =>
    Finset.sum_nonneg fun _ _ => measureReal_nonneg

theorem pairwiseEventMass_pos_of_partialEventMass_pos
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat)
    (h : 0 < partialEventMass mu A n) :
    0 < pairwiseEventMass mu A n := by
  classical
  unfold partialEventMass at h
  rcases (Finset.sum_pos_iff_of_nonneg
    (fun _ _ => measureReal_nonneg)).1 h with ⟨i, hi, hAi⟩
  unfold pairwiseEventMass
  refine Finset.sum_pos' (fun _ _ =>
    Finset.sum_nonneg fun _ _ => measureReal_nonneg) ⟨i, hi, ?_⟩
  refine Finset.sum_pos' (fun _ _ => measureReal_nonneg) ⟨i, hi, ?_⟩
  simpa [Set.inter_self] using hAi

theorem eventMassRatio_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) (A : Nat -> Set Omega) (n : Nat) :
    0 <= eventMassRatio mu A n := by
  exact div_nonneg (sq_nonneg _) (pairwiseEventMass_nonneg mu A n)

theorem measurable_eventCount {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    Measurable (eventCount A n) := by
  unfold eventCount
  exact Finset.measurable_fun_sum _ fun k _ => measurable_const.indicator (hA k)

theorem integrable_eventCount {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    Integrable (eventCount A n) mu := by
  unfold eventCount
  exact integrable_finset_sum _ fun k _ => (integrable_const 1).indicator (hA k)

theorem integral_eventCount {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    (∫ omega, eventCount A n omega ∂mu) = partialEventMass mu A n := by
  unfold eventCount partialEventMass
  rw [integral_finset_sum]
  · exact Finset.sum_congr rfl fun k _ => integral_indicator_one (hA k)
  · exact fun k _ => (integrable_const 1).indicator (hA k)

theorem eventCount_nonneg {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega) :
    0 <= eventCount A n omega := by
  refine Finset.sum_nonneg fun k _ => ?_
  by_cases h : omega ∈ A k
  · simp [Set.indicator_of_mem h]
  · simp [Set.indicator_of_notMem h]

theorem eventCount_sq_eq {Omega : Type u} [MeasurableSpace Omega]
    (A : Nat -> Set Omega) (n : Nat) (omega : Omega) :
    (eventCount A n omega) ^ 2 =
      Finset.sum (Finset.range n) fun i =>
        Finset.sum (Finset.range n) fun j =>
          (A i ∩ A j).indicator (fun _ => (1 : Real)) omega := by
  classical
  unfold eventCount
  rw [pow_two, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i hi
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  by_cases hi' : omega ∈ A i <;> by_cases hj' : omega ∈ A j <;>
    simp [Set.indicator_of_mem, Set.indicator_of_notMem, hi', hj']

theorem integrable_eventCount_sq {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    Integrable (fun omega => (eventCount A n omega) ^ 2) mu := by
  apply Integrable.congr (integrable_finset_sum _ fun i _ =>
    integrable_finset_sum _ fun j _ =>
      (integrable_const 1).indicator ((hA i).inter (hA j)))
  exact Filter.Eventually.of_forall fun omega => (eventCount_sq_eq A n omega).symm

theorem integral_eventCount_sq {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsFiniteMeasure mu]
    (A : Nat -> Set Omega) (hA : forall k, MeasurableSet (A k)) (n : Nat) :
    (∫ omega, (eventCount A n omega) ^ 2 ∂mu) = pairwiseEventMass mu A n := by
  classical
  simp_rw [eventCount_sq_eq A n]
  unfold pairwiseEventMass
  rw [integral_finset_sum]
  · apply Finset.sum_congr rfl
    intro i hi
    rw [integral_finset_sum]
    · exact Finset.sum_congr rfl fun j _ => integral_indicator_one ((hA i).inter (hA j))
    · exact fun j _ => (integrable_const 1).indicator ((hA i).inter (hA j))
  · intro i hi
    exact integrable_finset_sum _ fun j _ =>
      (integrable_const 1).indicator ((hA i).inter (hA j))

end Stage1Instances.THM_M_1009

#print axioms Stage1Instances.THM_M_1009.partialEventMass_nonneg
#print axioms Stage1Instances.THM_M_1009.pairwiseEventMass_pos_of_partialEventMass_pos
#print axioms Stage1Instances.THM_M_1009.integral_eventCount
#print axioms Stage1Instances.THM_M_1009.integral_eventCount_sq
