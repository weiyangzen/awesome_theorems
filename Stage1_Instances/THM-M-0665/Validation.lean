import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0665 same-worker differential validation

This module deliberately imports neither `Proof` nor an obligation-tree Lean
module. It independently reconstructs three elementary consequences of the
frozen height and algebraic-part definitions. It does not prove the exact
Pila-Wilkie root.
-/

open Set

namespace Stage1Instances.THM_M_0665.Validation

open Stage1Instances.THM_M_0665

/-- Differential reconstruction that the algebraic part stays inside its
ambient set. -/
theorem algebraicPart_subset (X : Set (Fin n -> Real)) :
    algebraicPart X <= X := by
  rintro x ⟨A, hAX, _hSA, _hPre, _hNontrivial, hx⟩
  exact hAX hx

/-- Differential reconstruction that bounded rational height bounds both
members of the normalized numerator-denominator pair. -/
theorem normalized_components_bounded {q : Rat} {T : Nat}
    (hq : rationalHeight q <= T) :
    q.num.natAbs <= T /\ q.den <= T := by
  exact ⟨le_trans (le_max_left _ _) hq, le_trans (le_max_right _ _) hq⟩

/-- Differential reconstruction that the zero-dimensional affine height is
the empty supremum. -/
theorem zero_dimensional_height (q : RationalPoint 0) : pointHeight q = 0 := by
  simp [pointHeight]

assert_no_sorry algebraicPart_subset
assert_no_sorry normalized_components_bounded
assert_no_sorry zero_dimensional_height

#print sorries algebraicPart_subset
#print sorries normalized_components_bounded
#print sorries zero_dimensional_height

#print axioms algebraicPart_subset
#print axioms normalized_components_bounded
#print axioms zero_dimensional_height

end Stage1Instances.THM_M_0665.Validation
