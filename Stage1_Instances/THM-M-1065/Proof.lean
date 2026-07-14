import Statement
import Mathlib.Probability.HasLawExists
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1065 proof-phase substrate

This module constructs, on one product probability space, an iid sequence with an admissible input
law and an iid standard Gaussian sequence. The two sequences are independent here, so this is only
common-carrier and marginal-law substrate. It does not provide the dependent KMT coupling or its
logarithmic maximal-discrepancy tail estimate and therefore does not prove the canonical target.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1065

/-- A checked common-carrier package for the two required iid marginal families. This deliberately
does not include a KMT discrepancy estimate. -/
def CommonIIDSequences (mu : Measure Real) : Prop :=
  exists (Omega : Type) (_m : MeasurableSpace Omega) (P : Measure Omega)
    (X Y : Nat -> Omega -> Real),
    IsProbabilityMeasure P /\
    (forall i, ProbabilityTheory.HasLaw (X i) mu P) /\
    ProbabilityTheory.iIndepFun X P /\
    (forall i, ProbabilityTheory.HasLaw (Y i)
      (ProbabilityTheory.gaussianReal 0 1) P) /\
    ProbabilityTheory.iIndepFun Y P

/-- Product-space construction of the input-law and Gaussian iid sequences. The `Sum Nat Nat`
index keeps the two families on one carrier while allowing independence to be restricted to each
summand. -/
theorem exists_commonIIDSequences (mu : Measure Real) (hmu : AdmissibleLaw mu) :
    CommonIIDSequences mu := by
  letI : IsProbabilityMeasure mu := hmu.1
  let nu : Sum Nat Nat -> Measure Real := fun
    | Sum.inl _ => mu
    | Sum.inr _ => ProbabilityTheory.gaussianReal 0 1
  letI : forall i, IsProbabilityMeasure (nu i) := fun i => by
    cases i <;> simp only [nu] <;> infer_instance
  let Omega := (i : Sum Nat Nat) -> Real
  letI : MeasurableSpace Omega := .pi
  let P : Measure Omega := Measure.infinitePi nu
  let Z : (i : Sum Nat Nat) -> Omega -> Real := fun i omega => omega i
  let X : Nat -> Omega -> Real := fun i => Z (Sum.inl i)
  let Y : Nat -> Omega -> Real := fun i => Z (Sum.inr i)
  have hZ_measurable : forall i, Measurable (Z i) := fun i => measurable_pi_apply i
  have hZ_law : forall i, ProbabilityTheory.HasLaw (Z i) (nu i) P := fun i =>
    (MeasurePreserving.hasLaw (measurePreserving_eval_infinitePi nu i))
  have hZ_indep : ProbabilityTheory.iIndepFun Z P := by
    simpa [Z, P] using
      (ProbabilityTheory.iIndepFun_infinitePi (P := nu) (X := fun _ => id)
        (fun _ => measurable_id))
  refine ⟨Omega, inferInstance, P, X, Y, by infer_instance, ?_, ?_, ?_, ?_⟩
  · intro i
    simpa [X, Z, nu] using hZ_law (Sum.inl i)
  · exact hZ_indep.precomp Sum.inl_injective
  · intro i
    simpa [Y, Z, nu] using hZ_law (Sum.inr i)
  · exact hZ_indep.precomp Sum.inr_injective

#check exists_commonIIDSequences
#print axioms exists_commonIIDSequences

end Stage1Instances.THM_M_1065
