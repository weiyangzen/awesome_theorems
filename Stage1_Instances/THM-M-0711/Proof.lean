import Mathlib.Computability.Reduce
import ObligationTree

/-!
# THM-M-0711 checked proof bodies

This module closes the generic computability-transfer and quotient-normalization
parts of the frozen route.  The Novikov-Boone construction itself is not
available in the pinned dependencies: the finite presentation and its
many-one reduction therefore remain explicit premises of the final theorem.
-/

namespace Stage1.THM_M_0711

/-- The identity predicate associated to a fixed finite presentation. -/
def IdentityPred (n : Nat) (rels : Finset (FreeGroup (Fin n)))
    (word : List (Fin n × Bool)) : Prop :=
  PresentedGroup.mk (rels : Set (FreeGroup (Fin n))) (evalWord word) = 1

/-- Quotient equality is exactly membership in the relators' normal closure. -/
theorem identityPred_iff_normalClosure (n : Nat)
    (rels : Finset (FreeGroup (Fin n))) (word : List (Fin n × Bool)) :
    IdentityPred n rels word ↔
      evalWord word ∈ Subgroup.normalClosure (rels : Set (FreeGroup (Fin n))) := by
  exact PresentedGroup.mk_eq_one_iff

/-- A many-one reduction transfers noncomputability from source to target. -/
theorem not_computablePred_of_manyOneReducible
    {alpha beta : Type*} [Primcodable alpha] [Primcodable beta]
    {source : alpha → Prop} {target : beta → Prop}
    (hsource : ¬ComputablePred source) (hred : source ≤₀ target) :
    ¬ComputablePred target := by
  intro htarget
  exact hsource (ComputablePred.computable_of_manyOneReducible hred htarget)

/-- The pinned mathlib terminal theorem in the exact source-predicate shape. -/
theorem haltingPredicate_not_computable (input : Nat) :
    ¬ComputablePred fun code : Nat.Partrec.Code =>
      (Nat.Partrec.Code.eval code input).Dom := by
  exact ComputablePred.halting_problem input

/-- A checked reduction from halting to one fixed presentation would establish
that presentation's required undecidable identity predicate. -/
theorem fixedPresentationUndecidable_of_haltingReduction
    (n : Nat) (rels : Finset (FreeGroup (Fin n))) (input : Nat)
    (hred : (fun code : Nat.Partrec.Code =>
      (Nat.Partrec.Code.eval code input).Dom) ≤₀ IdentityPred n rels) :
    FixedPresentationUndecidable n rels := by
  exact not_computablePred_of_manyOneReducible
    (haltingPredicate_not_computable input) hred

/-- Final checked assembly from the still-missing Novikov-Boone construction
and reduction.  No construction is hidden in this wrapper. -/
theorem novikovBooneTarget_of_haltingReduction
    (n : Nat) (rels : Finset (FreeGroup (Fin n))) (input : Nat)
    (hred : (fun code : Nat.Partrec.Code =>
      (Nat.Partrec.Code.eval code input).Dom) ≤₀ IdentityPred n rels) :
    NovikovBooneTarget := by
  exact novikovBooneTarget_of_witness
    (fixedPresentationUndecidable_of_haltingReduction n rels input hred)

#print axioms identityPred_iff_normalClosure
#print axioms not_computablePred_of_manyOneReducible
#print axioms haltingPredicate_not_computable
#print axioms fixedPresentationUndecidable_of_haltingReduction
#print axioms novikovBooneTarget_of_haltingReduction

end Stage1.THM_M_0711
