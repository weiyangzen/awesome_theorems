import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0442 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently reconstructs three elementary consequences of the frozen order
predicates. It does not construct a `MazurEngine` or prove Mazur's theorem.
-/

namespace Stage1Instances.THMM0442.Validation

open Stage1Instances.THMM0442

/-- A differential reconstruction of the cyclic-order upper bound used by the
partial proof. -/
theorem cyclic_order_le_sixteen {n : Nat}
    (h : IsMazurCyclicOrder n) : n <= 16 := by
  rcases h with ⟨_, h10⟩ | rfl
  · omega
  · omega

/-- A differential reconstruction of the bicyclic-family cardinality bound. -/
theorem bicyclic_index_four_mul_le_sixteen {m : Nat}
    (h : IsMazurBicyclicIndex m) : 2 * (2 * m) <= 16 := by
  rcases h with ⟨_, h4⟩
  omega

/-- The two endpoint families imply the same finite cardinality ceiling. -/
theorem allowed_shape_cardinality_bound :
    (forall n : Nat, IsMazurCyclicOrder n -> n <= 16) /\
      (forall m : Nat, IsMazurBicyclicIndex m -> 2 * (2 * m) <= 16) := by
  exact ⟨fun _ => cyclic_order_le_sixteen, fun _ => bicyclic_index_four_mul_le_sixteen⟩

assert_no_sorry cyclic_order_le_sixteen
assert_no_sorry bicyclic_index_four_mul_le_sixteen
assert_no_sorry allowed_shape_cardinality_bound
#print sorries cyclic_order_le_sixteen
#print sorries bicyclic_index_four_mul_le_sixteen
#print sorries allowed_shape_cardinality_bound
#print axioms cyclic_order_le_sixteen
#print axioms bicyclic_index_four_mul_le_sixteen
#print axioms allowed_shape_cardinality_bound

end Stage1Instances.THMM0442.Validation
