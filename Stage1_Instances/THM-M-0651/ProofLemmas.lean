import Mathlib.ModelTheory.Encoding

/-!
# THM-M-0651 proof-phase lemmas

This module contains unconditional, placeholder-free bodies for the countable
enumeration package used by a future Henkin construction.  It deliberately
does not assume either open interface from `ObligationTree.lean` and does not
claim the omitting-types root.
-/

namespace Stage1Instances.THM_M_0651.ProofLemmas

open FirstOrder FirstOrder.Language

universe u v w

/-- Countability of the function and relation symbols at every arity gives
countability of the combined symbol type expected by mathlib's syntax API. -/
theorem countable_symbols (L : Language.{u, v})
    [forall n, Countable (L.Functions n)]
    [forall n, Countable (L.Relations n)] : Countable L.Symbols := by
  unfold Language.Symbols
  infer_instance

/-- The syntax that must be scheduled by a countable Henkin construction is
countable, uniformly in every finite tuple arity. -/
theorem countable_finite_arity_syntax (L : Language.{u, v})
    [forall n, Countable (L.Functions n)]
    [forall n, Countable (L.Relations n)] :
    Countable (Sigma fun arity : Nat => L.Formula (Fin arity)) := by
  letI : Countable L.Symbols := countable_symbols L
  infer_instance

/-- The varying-arity formula requirements form a nonempty countable type and
therefore have a fair schedule. -/
theorem exists_surjective_formula_schedule (L : Language.{u, v})
    [forall n, Countable (L.Functions n)]
    [forall n, Countable (L.Relations n)] :
    exists schedule : Nat -> Sigma fun arity : Nat => L.Formula (Fin arity),
      Function.Surjective schedule := by
  letI : Countable L.Symbols := countable_symbols L
  letI : Countable (Sigma fun arity : Nat => L.Formula (Fin arity)) :=
    countable_finite_arity_syntax L
  exact exists_surjective_nat _

/-- Formula requirements, family indices, and finite tuples of natural-number
names can be combined into one countable work-item type. -/
theorem countable_avoidance_requirements
    (L : Language.{u, v}) (arity : Nat -> Nat)
    [forall n, Countable (L.Functions n)]
    [forall n, Countable (L.Relations n)] :
    Countable
      ((Sigma fun n : Nat => L.Formula (Fin n)) ⊕
        (Sigma fun i : Nat => Fin (arity i) -> Nat)) := by
  letI : Countable L.Symbols := countable_symbols L
  infer_instance

/-- The zero-arity boundary is included in the syntax schedule rather than
being discarded by an implicit positive-arity assumption. -/
theorem zero_arity_formula_requirement_inhabited (L : Language.{u, v}) :
    Nonempty (Sigma fun n : Nat => L.Formula (Fin n)) :=
  ⟨⟨0, ⊤⟩⟩

/-- Empty tuples of names are available at arity zero. -/
theorem zero_arity_tuple_requirement_inhabited (arity : Nat -> Nat)
    (i : Nat) (hi : arity i = 0) :
    Nonempty (Sigma fun j : Nat => Fin (arity j) -> Nat) := by
  refine ⟨⟨i, ?_⟩⟩
  intro x
  exact Fin.elim0 (hi ▸ x)

/-- A single fair schedule can visit every syntax or avoidance requirement.
This establishes only enumeration facts; density, Henkin construction, and the
term-model omission argument remain separate open obligations. -/
theorem exists_surjective_avoidance_schedule
    (L : Language.{u, v}) (arity : Nat -> Nat)
    [forall n, Countable (L.Functions n)]
    [forall n, Countable (L.Relations n)] :
    exists schedule : Nat ->
        ((Sigma fun n : Nat => L.Formula (Fin n)) ⊕
          (Sigma fun i : Nat => Fin (arity i) -> Nat)),
      Function.Surjective schedule := by
  letI : Countable L.Symbols := countable_symbols L
  letI : Countable
      ((Sigma fun n : Nat => L.Formula (Fin n)) ⊕
        (Sigma fun i : Nat => Fin (arity i) -> Nat)) :=
    countable_avoidance_requirements L arity
  exact exists_surjective_nat _

#print axioms countable_symbols
#print axioms countable_finite_arity_syntax
#print axioms exists_surjective_formula_schedule
#print axioms countable_avoidance_requirements
#print axioms zero_arity_formula_requirement_inhabited
#print axioms zero_arity_tuple_requirement_inhabited
#print axioms exists_surjective_avoidance_schedule

#check exists_surjective_avoidance_schedule

end Stage1Instances.THM_M_0651.ProofLemmas
