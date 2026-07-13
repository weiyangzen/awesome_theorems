import Mathlib.GroupTheory.GroupExtension.Basic
import Mathlib.RepresentationTheory.Homological.GroupCohomology.LowDegree

/-!
# THM-M-0078 discovery-only intake probe

These checks authenticate pinned group-extension vocabulary and a split-extension boundary. They
do not choose a meaning for the catalog's unspecified classification claim, define its classifying
invariant, or prove a repository-local THM-M-0078 declaration.
-/

#check GroupExtension
#check GroupExtension.Equiv
#check GroupExtension.Section
#check GroupExtension.Splitting
#check SemidirectProduct.toGroupExtension
#check GroupExtension.Equiv.ofMonoidHom
#check GroupExtension.Splitting.semidirectProductToGroupExtensionEquiv
#check groupCohomology.H2

#print axioms GroupExtension.Equiv.ofMonoidHom
#print axioms GroupExtension.Splitting.semidirectProductToGroupExtensionEquiv

section

variable {N E G : Type*} [Group N] [Group E] [Group G]

noncomputable section

example (S S' : GroupExtension N E G) (equiv : S.Equiv S') : E ≃* E :=
  equiv.toMulEquiv

example (S : GroupExtension N E G) (s : S.Splitting) :
    (SemidirectProduct.toGroupExtension s.conjAct).Equiv S :=
  s.semidirectProductToGroupExtensionEquiv

end

end
