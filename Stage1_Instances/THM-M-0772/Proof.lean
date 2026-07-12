import Mathlib.Order.CompleteLattice.Chain

/-!
# THM-M-0772 proof phase

This module installs the pinned mathlib maximal-chain construction at the
exact partial-order target frozen by `Statement.lean`.
-/

namespace Stage1Instances.THM_M_0772.Proof

universe u

/-- The exact frozen target, repeated transparently because the dossier is
outside the Lake library source tree. -/
def ProofTarget : Prop :=
  ∀ (P : Type u) [PartialOrder P], ∃ c : Set P, IsMaxChain (· ≤ ·) c

/-- Hausdorff's maximal principle, obtained by specializing mathlib's pinned
relation-generic maximal-chain construction to the partial-order relation. -/
theorem hausdorffMaximalPrinciple : ProofTarget.{u} := by
  intro P _order
  exact ⟨maxChain (· ≤ ·), maxChain_spec⟩

/-- Expanded result, checking that the proof supplies both chainhood and
inclusion-maximality at the statement boundary. -/
theorem expandedHausdorffMaximalPrinciple :
    ∀ (P : Type u) [PartialOrder P], ∃ c : Set P,
      IsChain (· ≤ ·) c ∧
        ∀ ⦃t : Set P⦄, IsChain (· ≤ ·) t → c ⊆ t → c = t := by
  exact hausdorffMaximalPrinciple

end Stage1Instances.THM_M_0772.Proof

#print axioms maxChain_spec
#print axioms Stage1Instances.THM_M_0772.Proof.hausdorffMaximalPrinciple
#print axioms Stage1Instances.THM_M_0772.Proof.expandedHausdorffMaximalPrinciple
