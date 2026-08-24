import Mathlib

/-!
Frozen provider provenance (comment only; this numeric provider module is not an
active canonical import):
import FormalConjectures.Arxiv.1308.0994.BoxdotConjecture
Arxiv.«1308.0994».BoxdotConjecture

The audit proves both directions between the set-theoretic surface used by the
claim-owned theorem and its fully elementwise reading.  Thus the wrapper does
not hide an added conclusion, altered carrier, or changed membership relation.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003489

/-- Transport the elementwise frozen reading to the claim-owned set surface. -/
theorem boxdotConjecture_source_to_target
    {Formula : Type*} (L KT : Set Formula) (boxdot : Formula → Formula)
    (h : (∀ φ, φ ∈ L → boxdot φ ∈ L) →
      (∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) →
        ∀ φ, φ ∈ L → φ ∈ KT) :
    Set.MapsTo boxdot L L →
      (∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) → L ⊆ KT := by
  intro hclosed faithful φ hφ
  exact h (fun ψ hψ => hclosed hψ) faithful φ hφ

/-- Transport the claim-owned set surface back to the elementwise reading. -/
theorem boxdotConjecture_target_to_source
    {Formula : Type*} (L KT : Set Formula) (boxdot : Formula → Formula)
    (h : Set.MapsTo boxdot L L →
      (∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) → L ⊆ KT) :
    (∀ φ, φ ∈ L → boxdot φ ∈ L) →
      (∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) →
        ∀ φ, φ ∈ L → φ ∈ KT := by
  intro hclosed faithful φ hφ
  exact h (by
    intro ψ hψ
    exact hclosed ψ hψ) faithful hφ

/-- Bidirectional transport between `Set.MapsTo`/subset and elementwise form. -/
theorem boxdotConjecture_bidirectional_transport
    {Formula : Type*} (L KT : Set Formula) (boxdot : Formula → Formula) :
    (Set.MapsTo boxdot L L →
        (∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) → L ⊆ KT) ↔
      ((∀ φ, φ ∈ L → boxdot φ ∈ L) →
        (∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) →
          ∀ φ, φ ∈ L → φ ∈ KT) := by
  constructor
  · exact boxdotConjecture_target_to_source L KT boxdot
  · exact boxdotConjecture_source_to_target L KT boxdot

/-- Trust-zero audit root, proved without any bodyless declaration. -/
theorem boxdotConjecture_audit_root
    {Formula : Type*} (L KT : Set Formula) (boxdot : Formula → Formula)
    (translation_closed : Set.MapsTo boxdot L L)
    (faithful : ∀ φ, boxdot φ ∈ L ↔ φ ∈ KT) :
    L ⊆ KT := by
  intro φ hφ
  exact (faithful φ).mp (translation_closed hφ)

end AwesomeTheorems.Stage5.S5_CLM_00003489
