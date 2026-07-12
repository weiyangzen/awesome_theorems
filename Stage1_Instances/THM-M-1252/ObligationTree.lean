import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.Support

/-!
# THM-M-1252 obligation-tree composition checks

This module checks the interfaces frozen by the obligation registry.  The root composition is
deliberately conditional: installing the pinned theorem as the target proof belongs to the later
proof phase.
-/

noncomputable section

open Set TopologicalSpace
open scoped Distributions

namespace Stage1Instances.THM_M_1252.ObligationTree

universe u

/-- A separately elaborated copy of the frozen canonical expression. Its source fingerprint is
bound to `Statement.lean` by the structured registry and the expressions are definitionally equal. -/
def CanonicalTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      (Distribution.dsupport T)ᶜ =
        ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsOpen U}

/-- The exact conclusion supplied by the imported generic support theorem after specialization. -/
def SpecializedAnchor : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      (Distribution.dsupport T)ᶜ =
        ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsOpen U}

/-- A checked child-to-parent composition certificate.  It consumes the exact specialized bridge
conclusion and yields the canonical target without adding a premise. -/
theorem root_of_specializedAnchor
    (h : SpecializedAnchor.{u}) :
    CanonicalTarget.{u} := by
  exact h

/-- A checked expansion of the vanishing predicate. It is represented separately so it cannot
receive duplicate proof-body credit. -/
theorem expanded_of_root (h : CanonicalTarget.{u}) :
    ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
      (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
        (Distribution.dsupport T)ᶜ =
          ⋃₀ {U : Set E |
            (∀ φ : TestFunction Ω ℝ ⊤, tsupport φ ⊆ U → T φ = 0) ∧ IsOpen U} := by
  simpa only [Distribution.IsVanishingOn] using h

end Stage1Instances.THM_M_1252.ObligationTree

#check Distribution.dsupport_compl_eq
#print axioms Stage1Instances.THM_M_1252.ObligationTree.root_of_specializedAnchor
#print axioms Stage1Instances.THM_M_1252.ObligationTree.expanded_of_root
