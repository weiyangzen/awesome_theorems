import Mathlib.Probability.Kernel.Composition.Comp

/-!
# THM-M-1091 anchor-audit probes

This module checks the exact pinned mathlib anchors against the frozen target. It records
candidate closure only; proof-node and theorem-completion credit belong to later phases.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1091

universe u

#check ProbabilityTheory.Kernel.pow_add
#check ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral

/-- Exact expression copied from the separately elaborated frozen statement for this probe. -/
def AuditedChapmanKolmogorovTarget : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m n : Nat),
      κ ^ (m + n) = (κ ^ n) ∘ₖ (κ ^ m)

/-- Exact integral expression copied from the frozen alternate encoding for this probe. -/
def AuditedChapmanKolmogorovIntegralTarget : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m n : Nat)
    (x : State) (A : Set State),
      MeasurableSet A →
        (κ ^ (m + n)) x A = ∫⁻ y, (κ ^ n) y A ∂((κ ^ m) x)

/-- Exact checked bridge from the pinned kernel-power anchor to the frozen target. -/
theorem target_of_mathlib_pow_add : AuditedChapmanKolmogorovTarget.{u} := by
  intro State _ kappa _ m n
  simpa only [add_comm] using Kernel.pow_add kappa n m

/-- The pinned integral anchor also closes the frozen alternate encoding directly. -/
theorem integralTarget_of_mathlib_anchor : AuditedChapmanKolmogorovIntegralTarget.{u} := by
  intro State _ kappa _ m n x A hA
  exact Kernel.pow_add_apply_eq_lintegral kappa m n x hA

#print axioms ProbabilityTheory.Kernel.pow_add
#print axioms ProbabilityTheory.Kernel.pow_add_apply_eq_lintegral
#print axioms Stage1Instances.THM_M_1091.target_of_mathlib_pow_add
#print axioms Stage1Instances.THM_M_1091.integralTarget_of_mathlib_anchor

end Stage1Instances.THM_M_1091
