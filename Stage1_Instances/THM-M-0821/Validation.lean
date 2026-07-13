import Statement
import Mathlib.Combinatorics.SetFamily.LYM
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0821 independent validation probe

This module intentionally does not import `Proof.lean` or
`ObligationTree.lean`.  It reconstructs the exact frozen maximum-size target
directly from the lower-middle powerset slice and the pinned mathlib Sperner
bound.
-/

namespace Stage1Instances.THM_M_0821.Validation

universe u

open Stage1Instances.THM_M_0821

/-- An independently written construction of an attaining antichain. -/
theorem independentMiddleLayerAttainment :
    forall (alpha : Type u) [Fintype alpha],
      exists A : Finset (Finset alpha),
        IsSpernerFamily A /\
          A.card = Nat.choose (Fintype.card alpha) (Fintype.card alpha / 2) := by
  intro alpha _
  refine ⟨middleLayer alpha, ?_, ?_⟩
  · simp [IsSpernerFamily, middleLayer]
    exact
      (Set.sized_powersetCard (Finset.univ : Finset alpha)
        (Fintype.card alpha / 2)).isAntichain
  · simp [middleLayer, Finset.card_powersetCard]

/-- Independent exact reconstruction of the frozen Sperner maximum target. -/
theorem independentlyReconstructedSpernerMaximum :
    SpernerMaximumTarget.{u} := by
  intro alpha _
  refine ⟨independentMiddleLayerAttainment alpha, ?_⟩
  intro A hA
  exact hA.sperner

assert_no_sorry IsAntichain.sperner
assert_no_sorry independentMiddleLayerAttainment
assert_no_sorry independentlyReconstructedSpernerMaximum

#print sorries IsAntichain.sperner
#print sorries independentMiddleLayerAttainment
#print sorries independentlyReconstructedSpernerMaximum

#print axioms IsAntichain.sperner
#print axioms independentMiddleLayerAttainment
#print axioms independentlyReconstructedSpernerMaximum

end Stage1Instances.THM_M_0821.Validation
