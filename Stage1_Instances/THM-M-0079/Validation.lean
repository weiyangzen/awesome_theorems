import Statement
import Mathlib.GroupTheory.FreeGroup.NielsenSchreier
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0079 same-worker differential validation probe

This module reconstructs the exact frozen Nielsen-Schreier target from the pinned quotient-action,
free-groupoid, connected-end, and multiplicative-equivalence APIs. It deliberately imports neither
`Proof` nor `ObligationTree`. This is same-worker corroboration over the same mathematical route,
not the distinct-runner independent verification required for release.
-/

noncomputable section

open CategoryTheory CategoryTheory.ActionCategory

universe u

namespace Stage1Instances.THM_M_0079.Validation

open Stage1Instances.THM_M_0079

/-- A separately written adapter that expands the major pinned Nielsen-Schreier route. -/
theorem independentlyReconstructedTarget : NielsenSchreierTarget.{u} := by
  intro G _ _ H
  letI : MulAction.IsPretransitive G (G ⧸ H) := MulAction.isPretransitive_quotient G H
  letI : Nonempty (G ⧸ H) := Nonempty.intro ((1 : G) : G ⧸ H)
  have hConnected : IsConnected (ActionCategory G (G ⧸ H)) := inferInstance
  letI : IsFreeGroupoid (ActionCategory G (G ⧸ H)) :=
    IsFreeGroupoid.actionGroupoidIsFree
  have hEnd : @IsFreeGroup
      (End (objEquiv G (G ⧸ H) ((1 : G) : G ⧸ H))) (End.group _) :=
    @IsFreeGroupoid.endIsFreeOfConnectedFree
      (ActionCategory G (G ⧸ H)) inferInstance hConnected inferInstance
      (objEquiv G (G ⧸ H) ((1 : G) : G ⧸ H))
  exact @IsFreeGroup.ofMulEquiv
    (End (objEquiv G (G ⧸ H) ((1 : G) : G ⧸ H)))
    (End.group _) hEnd H H.toGroup (endMulEquivSubgroup H)

assert_no_sorry subgroupIsFreeOfIsFree
assert_no_sorry independentlyReconstructedTarget

#print sorries subgroupIsFreeOfIsFree
#print sorries independentlyReconstructedTarget
#print axioms subgroupIsFreeOfIsFree
#print axioms independentlyReconstructedTarget

end Stage1Instances.THM_M_0079.Validation
