import Statement
import Mathlib.FieldTheory.Cardinality
import Mathlib.Logic.Small.Basic
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0424 universe-boundary counterexample

The exact frozen target quantifies the carrier universe independently from the
field universe. At `u = 1` and `v = 0`, its `oneRep_equiv_base` field would
make the universe-large field `Type` equivalent to a type in `Type 0`, which
contradicts `not_small_type`. This module kernel-checks that contradiction;
it is blocked-phase evidence, not a proof of the positive target.
-/

noncomputable section

namespace Stage1Instances.THM_M_0424.UniverseCounterexample

/-- The `oneRep` compatibility field forces the base field to fit in the
representative carrier universe. -/
theorem small_of_one_rep_equiv
    {K : Type u} [Field K]
    {A : CSA.{u, v} K} (e : Nonempty ((A : Type v) ≃ₐ[K] K)) :
    Small.{v} K := by
  obtain ⟨e⟩ := e
  exact small_map e.toEquiv.symm

/-- No field structure on `Type` can have a `Type 0` CSA representative
algebra-equivalent to the base field. -/
theorem no_small_base_representative
    (fieldType : Field (Type 0))
    (A : @CSA.{1, 0} (Type 0) fieldType)
    (e : Nonempty ((A : Type 0) ≃ₐ[Type 0] Type 0)) : False := by
  letI : Field (Type 0) := fieldType
  exact not_small_type (small_of_one_rep_equiv (K := Type 0) (A := A) e)

/-- Consequently the exact `BrauerGroupLawData.{1,0}` package is empty for
the field structure on `Type` supplied by `Infinite.nonempty_field`. -/
theorem no_law_data_at_unrelated_universes
    (LawData : (K : Type 1) -> [Field K] -> Type 1)
    (oneRep : forall (K : Type 1) (inst : Field K),
      @LawData K inst -> @CSA.{1, 0} K inst)
    (oneRep_equiv_base : forall (K : Type 1) (inst : Field K)
      (data : @LawData K inst),
      Nonempty (((oneRep K inst data : @CSA.{1, 0} K inst) : Type 0) ≃ₐ[K] K))
    (h : forall (K : Type 1) (inst : Field K), Nonempty (@LawData K inst)) : False := by
  letI : Infinite (Type 0) := Infinite.of_injective
    (fun n : Nat => Fin (n + 1)) (fun m n h => by
      have : m + 1 = n + 1 := by
        simpa using Fintype.card_congr (Equiv.cast h)
      omega)
  obtain ⟨fieldType⟩ := Infinite.nonempty_field (α := Type 0)
  obtain ⟨data⟩ := h (Type 0) fieldType
  exact no_small_base_representative fieldType (oneRep (Type 0) fieldType data)
    (oneRep_equiv_base (Type 0) fieldType data)

/-- The canonical frozen target is false at the valid specialization
`u = 1`, `v = 0`. -/
theorem not_brauerGroupStatement :
    Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1, 0} := by
  apply no_law_data_at_unrelated_universes
    (LawData := fun K [Field K] =>
      Stage1Instances.THM_M_0424.BrauerGroupLawData.{1, 0} K)
    (oneRep := fun _ _ data => data.oneRep)
    (oneRep_equiv_base := fun _ _ data => data.oneRep_equiv_base)

#print axioms small_of_one_rep_equiv
#print axioms no_small_base_representative
#print axioms no_law_data_at_unrelated_universes
#check (show Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1, 0} from
  not_brauerGroupStatement)
assert_no_sorry small_of_one_rep_equiv
assert_no_sorry no_small_base_representative
assert_no_sorry no_law_data_at_unrelated_universes
assert_no_sorry not_brauerGroupStatement
#print axioms not_brauerGroupStatement

end Stage1Instances.THM_M_0424.UniverseCounterexample
