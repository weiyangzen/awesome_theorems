import Mathlib.GroupTheory.Focal

/-!
# THM-M-0072 discovery-only intake probe

These checks authenticate pinned finite-group, conjugacy, transfer, and focal-subgroup interfaces
adjacent to Thompson's transfer lemma. The envelope below checks that the prospective source scope
is representable, but does not select it as the canonical target or prove the conclusion.
-/

namespace Stage1Instances.THM_M_0072

/-- Literal candidate encoding of the source's "no subgroup of index two" premise. -/
def NoIndexTwoSubgroup (G : Type*) [Group G] : Prop :=
  ∀ H : Subgroup G, H.index ≠ 2

/-- Noncanonical source-scope envelope; the statement phase owns target selection and transports. -/
def ThompsonSourceEnvelope : Prop :=
  ∀ (G : Type*) [Group G] [Finite G],
    Even (Nat.card G) → NoIndexTwoSubgroup G →
      ∀ (S : Sylow 2 G) (M : Subgroup S), IsCoatom M →
        ∀ u : S, orderOf u = 2 → ∃ m : M, IsConj (u : G) ((m : S) : G)

#check Sylow
#check Subgroup.index
#check IsCoatom
#check orderOf
#check IsConj
#check isConj_iff
#check MonoidHom.transfer
#check MonoidHom.transfer_eq_pow
#check MonoidHom.ker_transferSylow_isComplement'
#check Subgroup.focalSubgroup
#check Subgroup.transferFocal
#check Subgroup.transferFocal_eq_pow
#check Subgroup.commutator_inf_eq_focalSubgroup
#check NoIndexTwoSubgroup
#check ThompsonSourceEnvelope

#print axioms MonoidHom.transfer_eq_pow
#print axioms MonoidHom.ker_transferSylow_isComplement'
#print axioms Subgroup.commutator_inf_eq_focalSubgroup

end Stage1Instances.THM_M_0072
