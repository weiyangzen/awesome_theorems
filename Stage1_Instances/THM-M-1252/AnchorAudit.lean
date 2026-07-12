import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.Support

/-!
# THM-M-1252 mathlib anchor audit

This narrowly scoped harness checks that the pinned generic mathlib theorem specializes to the
exact frozen target. It is audit evidence, not the target's release proof artifact.
-/

noncomputable section

open Set TopologicalSpace
open scoped Distributions

namespace Stage1Instances.THM_M_1252.AnchorAudit

universe u

/-- Exact specialization of the pinned generic mathlib anchor to the frozen distribution type. -/
theorem exactMathlibCandidate :
    ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
      (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
        (Distribution.dsupport T)ᶜ =
          ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsOpen U} := by
  intro E _ _ _ Ω T
  exact Distribution.dsupport_compl_eq

end Stage1Instances.THM_M_1252.AnchorAudit

#check Distribution.dsupport_compl_eq
#print axioms Distribution.dsupport_compl_eq
#print axioms Stage1Instances.THM_M_1252.AnchorAudit.exactMathlibCandidate
