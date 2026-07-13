import Mathlib.Order.Antichain
import Mathlib.Order.Height
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0819 anchor-audit probe

This module checks the frozen primary Dilworth target and the closest interfaces
available in the manifest-pinned mathlib. It deliberately contains no proof of
Dilworth's theorem. The external finite-poset candidate is not imported: it is
outside the dependency closure, is not the arbitrary-poset target, and fails
when checked against the repository pin.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0819_AnchorAudit

universe u

/-- Audit-local copy of the statement phase's exact-cardinality predicate. -/
def HasExactly {alpha : Type u} (k : Nat) (s : Set alpha) : Prop :=
  Nonempty (s ≃ Fin k)

/-- Audit-local copy of the statement phase's dependence predicate. -/
def IsDependent {alpha : Type u} [LE alpha] (s : Set alpha) : Prop :=
  ∃ x ∈ s, ∃ y ∈ s, x ≠ y /\ (x <= y \/ y <= x)

/-- Audit-local copy of the statement phase's chain-decomposition predicate. -/
def IsDisjointChainDecomposition {alpha : Type u} [LE alpha]
  (k : Nat) (C : Fin k -> Set alpha) : Prop :=
  (forall i, IsChain (fun x y : alpha => x <= y) (C i)) /\
    forall x : alpha, ∃! i, x ∈ C i

/-- Literal audit copy of the statement phase's arbitrary-poset target. -/
def ExactTarget : Prop :=
  forall (alpha : Type u) [PartialOrder alpha] (k : Nat),
    (forall s : Set alpha, HasExactly (k + 1) s -> IsDependent s) ->
    (exists s : Set alpha, HasExactly k s /\
        IsAntichain (fun x y : alpha => x <= y) s) ->
    exists C : Fin k -> Set alpha, IsDisjointChainDecomposition k C

#check IsChain
#check IsAntichain
#check inter_subsingleton_of_isChain_of_isAntichain
#check Set.chainHeight
#check Set.exists_eq_chainHeight_of_finite
#check Set.encard
#check ENat.card

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0819_AnchorAudit
