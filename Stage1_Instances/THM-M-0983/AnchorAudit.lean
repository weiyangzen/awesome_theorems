import Mathlib.Probability.StrongLaw

/-!
# THM-M-0983: pinned anchor audit

This module checks the exact bridge from the frozen target to mathlib's strong
law. It is audit evidence only; downstream proof and validation nodes retain
their own acceptance gates.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0983

universe u

def auditedEmpiricalFrequency {Omega : Type u} (X : Nat -> Omega -> Real)
    (n : Nat) (omega : Omega) : Real :=
  (∑ i ∈ range n, X i omega) / (n : Real)

/-- Separately elaborated copy of the frozen proposition, used because the
dossier directory is outside the Lake module roots. The audit validator checks
this declaration against the statement source before Lean elaboration. -/
def AuditedBernoulliStrongLawTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (p : Real),
      Integrable (X 0) mu ->
      ProbabilityTheory.iIndepFun X mu ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      (forall i, ∀ᵐ omega ∂mu, X i omega = 0 \/ X i omega = 1) ->
      mu[X 0] = p ->
      ∀ᵐ omega ∂mu,
        Tendsto (fun n : Nat => auditedEmpiricalFrequency X n omega) atTop (nhds p)

#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_Lp
#check ProbabilityTheory.iIndepFun.indepFun

/-- The pinned mathlib theorem, together with the family-to-pairwise
independence projection, has exactly the strength needed by the frozen target.
The Bernoulli-value hypothesis is intentionally unused: the mathlib strong law
holds for every integrable real-valued IID family. -/
theorem exactTarget_from_pinned_mathlib : AuditedBernoulliStrongLawTarget.{u} := by
  intro Omega _ mu _ X p hint hindep hident _hBernoulli hexpect
  have hpair : Pairwise (Function.onFun (fun f g => f ⟂ᵢ[mu] g) X) := by
    intro i j hij
    exact hindep.indepFun hij
  have h := ProbabilityTheory.strong_law_ae_real X hint hpair hident
  filter_upwards [h] with omega homega
  simpa [auditedEmpiricalFrequency, hexpect] using homega

end Stage1Instances.THM_M_0983

#print axioms Stage1Instances.THM_M_0983.exactTarget_from_pinned_mathlib
