import ObligationTree

/-!
# THM-M-0579: proof-availability blocker probe

This module checks that the frozen immediate root cut is equivalent to the
canonical Poincare target and that the matching `proof_wanted` source markers
are not retained declarations in the pinned mathlib environment. It records a
proof-phase obstruction; it does not prove the target.
-/

noncomputable section

universe u

namespace Stage1Instances.THMM0579

/-- The frozen recognition/rigidity cut does not reduce the canonical root:
the root itself supplies both packages, and the existing composition supplies
the converse. -/
theorem immediate_cut_iff_statement :
    (HomotopySphereRecognition.{u} ∧
      HomotopySphereTopologicalRigidity.{u}) ↔ Statement.{u} := by
  constructor
  · rintro ⟨recognition, rigidity⟩
    exact root_of_recognition_and_rigidity recognition rigidity
  · intro root
    constructor
    · intro M _ _ _ _ _
      rcases root M with ⟨homeomorph⟩
      exact ⟨homeomorph.toHomotopyEquiv⟩
    · intro M _ _ _ _ _ _
      exact root M

#print axioms immediate_cut_iff_statement

-- Batteries elaborates these `proof_wanted` markers without modifying the
-- environment, so importing the mathlib module must leave all names absent.
#check_failure ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
#check_failure SimplyConnectedSpace.nonempty_homeomorph_sphere_three
#check_failure SimplyConnectedSpace.nonempty_diffeomorph_sphere_three

end Stage1Instances.THMM0579
