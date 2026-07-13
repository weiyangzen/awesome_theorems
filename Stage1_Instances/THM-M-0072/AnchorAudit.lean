import Mathlib.GroupTheory.Focal

/-!
# THM-M-0072 anchor-audit probes

This module checks the strongest pinned mathlib transfer and focal-subgroup interfaces against a
literal audit copy of the frozen Thompson target. None of the inspected declarations proves the
existential conjugacy conclusion, so this file deliberately defines no inhabitant of `ExactTarget`.
-/

namespace Stage1Instances.THM_M_0072_AnchorAudit

universe u

/-- Literal audit copy of the statement gate's canonical proposition. -/
def ExactTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) ->
      (forall H : Subgroup G, H.index != 2) ->
        forall (S : Sylow 2 G) (M : Subgroup S), IsCoatom M ->
          forall x : S, orderOf x = 2 ->
            exists m : M, IsConj (x : G) ((m : S) : G)

#check MonoidHom.transfer
#check MonoidHom.transfer_eq_prod_quotient_orbitRel_zpowers_quot
#check MonoidHom.transfer_eq_pow
#check MonoidHom.transferSylow
#check MonoidHom.transferSylow_eq_pow
#check MonoidHom.ker_transferSylow_isComplement'
#check Subgroup.focalSubgroupOf.mk'_conj_eq
#check Subgroup.transferFocal
#check Subgroup.transferFocal_eq_pow
#check Subgroup.transferFocal_surjective
#check Subgroup.ker_restrict_transferFocal_eq_focalSubgroupOf
#check Subgroup.ker_transferFocal_inf_eq_focalSubgroup
#check Subgroup.commutator_inf_eq_focalSubgroup

-- The strongest adjacent theorems have different conclusions from the frozen root.
#check_failure (MonoidHom.ker_transferSylow_isComplement' : ExactTarget.{u})
#check_failure (Subgroup.commutator_inf_eq_focalSubgroup : ExactTarget.{u})

#print axioms MonoidHom.transfer_eq_pow
#print axioms MonoidHom.ker_transferSylow_isComplement'
#print axioms Subgroup.focalSubgroupOf.mk'_conj_eq
#print axioms Subgroup.transferFocal_eq_pow
#print axioms Subgroup.commutator_inf_eq_focalSubgroup
#print sorries MonoidHom.transfer_eq_pow
#print sorries MonoidHom.ker_transferSylow_isComplement'
#print sorries Subgroup.focalSubgroupOf.mk'_conj_eq
#print sorries Subgroup.transferFocal_eq_pow
#print sorries Subgroup.commutator_inf_eq_focalSubgroup

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0072_AnchorAudit
