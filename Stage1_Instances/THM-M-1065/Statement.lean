import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1065: Komlos-Major-Tusnady strong approximation statement

This module freezes the normalized partial-sum form of the KMT strong approximation. It contains
only the target, its direct expansion, and statement-boundary tests; it does not prove KMT.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1065

/-- A centered, variance-one law with a two-sided exponential moment. -/
def AdmissibleLaw (mu : Measure Real) : Prop :=
  IsProbabilityMeasure mu /\
  Integrable (fun x : Real => x) mu /\
  (integral mu fun x : Real => x) = 0 /\
  Integrable (fun x : Real => x ^ 2) mu /\
  (integral mu fun x : Real => x ^ 2) = 1 /\
  exists delta : Real, 0 < delta /\
    Integrable (fun x : Real => Real.exp (delta * |x|)) mu

/-- The event that the two coupled walks differ by more than `C * log n + x` at some time
`1 <= k <= n`. `Finset.range k` makes the time-`k` sum contain precisely increments `0,...,k-1`. -/
def DiscrepancyEvent {Omega : Type*} (X Y : Nat -> Omega -> Real)
    (C x : Real) (n : Nat) : Set Omega :=
  {omega | exists k : Nat, 1 <= k /\ k <= n /\
    |(Finset.range k).sum (fun i => X i omega) -
      (Finset.range k).sum (fun i => Y i omega)| > C * Real.log n + x}

/-- The normalized KMT strong-approximation target. Constants may depend on the input law, but not
on `n` or `x`; the constructed sequences live on one probability space. -/
def KMTStrongApproximationTarget : Prop :=
  forall mu : Measure Real, AdmissibleLaw mu ->
    exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
      (X Y : Nat -> Omega -> Real) (C K lambda : Real),
      IsProbabilityMeasure P /\
      0 < C /\ 0 < K /\ 0 < lambda /\
      (forall i, ProbabilityTheory.HasLaw (X i) mu P) /\
      ProbabilityTheory.iIndepFun X P /\
      (forall i, ProbabilityTheory.HasLaw (Y i)
        (ProbabilityTheory.gaussianReal 0 1) P) /\
      ProbabilityTheory.iIndepFun Y P /\
      forall (n : Nat), 1 <= n -> forall x : Real, 0 <= x ->
        P (DiscrepancyEvent X Y C x n) <=
          ENNReal.ofReal (K * Real.exp (-lambda * x))

/-- Full direct expansion, used to ensure that the named predicates hide no weaker conclusion. -/
def ExpandedSourceShape : Prop :=
  forall mu : Measure Real,
    (IsProbabilityMeasure mu /\
      Integrable (fun z : Real => z) mu /\
      (integral mu fun z : Real => z) = 0 /\
      Integrable (fun z : Real => z ^ 2) mu /\
      (integral mu fun z : Real => z ^ 2) = 1 /\
      exists delta : Real, 0 < delta /\
        Integrable (fun z : Real => Real.exp (delta * |z|)) mu) ->
    exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
      (X Y : Nat -> Omega -> Real) (C K lambda : Real),
      IsProbabilityMeasure P /\ 0 < C /\ 0 < K /\ 0 < lambda /\
      (forall i, ProbabilityTheory.HasLaw (X i) mu P) /\
      ProbabilityTheory.iIndepFun X P /\
      (forall i, ProbabilityTheory.HasLaw (Y i)
        (ProbabilityTheory.gaussianReal 0 1) P) /\
      ProbabilityTheory.iIndepFun Y P /\
      forall (n : Nat), 1 <= n -> forall x : Real, 0 <= x ->
        P {omega | exists k : Nat, 1 <= k /\ k <= n /\
          |(Finset.range k).sum (fun i => X i omega) -
            (Finset.range k).sum (fun i => Y i omega)| > C * Real.log n + x} <=
          ENNReal.ofReal (K * Real.exp (-lambda * x))

theorem target_iff_expandedSourceShape :
    KMTStrongApproximationTarget <-> ExpandedSourceShape := by
  rfl

-- Deliberately non-equivalent, separately elaborated statement mutations.
def mutationRemovedExponentialMoment : Prop :=
  forall mu : Measure Real,
    (IsProbabilityMeasure mu /\ (integral mu fun x : Real => x) = 0 /\
      (integral mu fun x : Real => x ^ 2) = 1) ->
    exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
      (X Y : Nat -> Omega -> Real) (C K lambda : Real), True

def mutationChangedDomainToRat : Prop :=
  forall mu : Measure Rat, IsProbabilityMeasure mu -> True

def mutationTerminalTimeOnly : Prop :=
  forall mu : Measure Real, AdmissibleLaw mu ->
    exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
      (X Y : Nat -> Omega -> Real) (C K lambda : Real),
      forall n : Nat, 1 <= n -> forall x : Real, 0 <= x ->
        P {omega | |(Finset.range n).sum (fun i => X i omega) -
          (Finset.range n).sum (fun i => Y i omega)| > C * Real.log n + x} <=
          ENNReal.ofReal (K * Real.exp (-lambda * x))

def mutationAllowsZeroTime : Prop :=
  forall mu : Measure Real, AdmissibleLaw mu ->
    exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
      (X Y : Nat -> Omega -> Real) (C K lambda : Real),
      forall n : Nat, forall x : Real, 0 <= x ->
        P (DiscrepancyEvent X Y C x n) <= ENNReal.ofReal (K * Real.exp (-lambda * x))

/-- At the boundary `n = 1`, the running event is exactly the discrepancy of the first increments. -/
theorem discrepancyEvent_one {Omega : Type*} (X Y : Nat -> Omega -> Real) (C x : Real) :
    DiscrepancyEvent X Y C x 1 =
      {omega | |X 0 omega - Y 0 omega| > C * Real.log 1 + x} := by
  ext omega
  constructor
  · rintro ⟨k, hk1, hk2, hk⟩
    have : k = 1 := by omega
    subst k
    simpa using hk
  · intro h
    exact ⟨1, by simp, by simpa using h⟩

end Stage1Instances.THM_M_1065

set_option pp.explicit true in
#print Stage1Instances.THM_M_1065.KMTStrongApproximationTarget
