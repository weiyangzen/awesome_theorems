import Mathlib.Probability.Distributions.Gaussian.Real

/-! Checked composition interface for the frozen THM-M-1065 architecture. -/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1065.ObligationTree

def AdmissibleLaw (mu : Measure Real) : Prop :=
  IsProbabilityMeasure mu /\
  Integrable (fun x : Real => x) mu /\
  (integral mu fun x : Real => x) = 0 /\
  Integrable (fun x : Real => x ^ 2) mu /\
  (integral mu fun x : Real => x ^ 2) = 1 /\
  exists delta : Real, 0 < delta /\
    Integrable (fun x : Real => Real.exp (delta * |x|)) mu

def DiscrepancyEvent {Omega : Type*} (X Y : Nat -> Omega -> Real)
    (C x : Real) (n : Nat) : Set Omega :=
  {omega | exists k : Nat, 1 <= k /\ k <= n /\
    |(Finset.range k).sum (fun i => X i omega) -
      (Finset.range k).sum (fun i => Y i omega)| > C * Real.log n + x}

/-- The complete registered witness package. This is an interface, not a construction. -/
def CouplingData (mu : Measure Real) : Prop :=
  exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
    (X Y : Nat -> Omega -> Real) (C K lambda : Real),
    IsProbabilityMeasure P /\
    0 < C /\ 0 < K /\ 0 < lambda /\
    (forall i, ProbabilityTheory.HasLaw (X i) mu P) /\
    ProbabilityTheory.iIndepFun X P /\
    (forall i, ProbabilityTheory.HasLaw (Y i)
      (ProbabilityTheory.gaussianReal 0 1) P) /\
    ProbabilityTheory.iIndepFun Y P /\
    forall n : Nat, 1 <= n -> forall x : Real, 0 <= x ->
      P (DiscrepancyEvent X Y C x n) <=
        ENNReal.ofReal (K * Real.exp (-lambda * x))

def CouplingDataTarget : Prop :=
  forall mu : Measure Real, AdmissibleLaw mu -> CouplingData mu

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
      forall n : Nat, 1 <= n -> forall x : Real, 0 <= x ->
        P (DiscrepancyEvent X Y C x n) <=
          ENNReal.ofReal (K * Real.exp (-lambda * x))

/-- Exact child-to-parent composition. Both directions only repack the same fields. -/
theorem kmtTarget_iff_couplingData :
    KMTStrongApproximationTarget <-> CouplingDataTarget := by
  rfl

#check kmtTarget_iff_couplingData

end Stage1Instances.THM_M_1065.ObligationTree
