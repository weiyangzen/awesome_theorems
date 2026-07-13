import Statement
import Mathlib.GroupTheory.Coset.Card

/-!
# THM-M-0061 conditional obligation composition

This module checks the child-to-parent interfaces selected by the frozen Lagrange architecture.
The arbitrary-group theorem and the engines behind the coset-product equivalence remain explicit
premises, so this file does not install the audited mathlib candidate or close the canonical root.
-/

noncomputable section

namespace Stage1Instances.THM_M_0061.ObligationTree

universe u
open scoped Pointwise

/-- The stronger arbitrary-group divisibility interface exported by the audited candidate. -/
def ArbitraryGroupDivisibility : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G), Nat.card H ∣ Nat.card G

/-- The exact cardinal product identity used to produce the divisibility witness. -/
def CardProductIdentity : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    Nat.card G = Nat.card (G ⧸ H) * Nat.card H

/-- Cardinality is multiplicative on products. -/
def NatCardProductEngine : Prop :=
  forall (alpha beta : Type u), Nat.card (alpha × beta) = Nat.card alpha * Nat.card beta

/-- Cardinality is invariant under equivalence. -/
def NatCardCongruenceEngine : Prop :=
  forall (alpha beta : Type u), (alpha ≃ beta) -> Nat.card alpha = Nat.card beta

/-- The non-canonical equivalence between a group and quotient-times-subgroup. -/
def CosetProductEquivalence : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G), G ≃ (G ⧸ H) × H

/-- Decompose a group into the sigma type of the quotient-map fibers. -/
def FiberDecomposition : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    G ≃ Σ L : G ⧸ H, {x : G // (x : G ⧸ H) = L}

/-- Identify a quotient-map fiber with the corresponding left coset. -/
def FiberToLeftCoset : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G) (L : G ⧸ H),
    {x : G // (x : G ⧸ H) = L} ≃ (Quotient.out L • (H : Set G) : Set G)

/-- Every left coset is equivalent to the subgroup. -/
def LeftCosetEquivalence : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G) (g : G),
    (g • (H : Set G) : Set G) ≃ H

/-- Collapse a constant sigma family to quotient-times-subgroup. -/
def SigmaProductEquivalence : Type (u + 1) :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    (Σ _L : G ⧸ H, H) ≃ (G ⧸ H) × H

/-- Checked composition of the four construction engines into the central equivalence. -/
noncomputable def cosetProduct_of_fiber_engines
    (fiber : FiberDecomposition.{u})
    (fiberToCoset : FiberToLeftCoset.{u})
    (cosetToSubgroup : LeftCosetEquivalence.{u})
    (sigmaProduct : SigmaProductEquivalence.{u}) :
    CosetProductEquivalence.{u} := fun G _ H =>
  (fiber G H).trans <|
    (Equiv.sigmaCongrRight fun L =>
      (fiberToCoset G H L).trans (cosetToSubgroup G H (Quotient.out L))).trans
        (sigmaProduct G H)

/-- Checked composition of product cardinality, congruence, and the central equivalence. -/
theorem cardProduct_of_engines
    (cardProduct : NatCardProductEngine.{u})
    (cardCongruence : NatCardCongruenceEngine.{u})
    (cosetProduct : CosetProductEquivalence.{u}) :
    CardProductIdentity.{u} := by
  intro G _ H
  calc
    Nat.card G = Nat.card ((G ⧸ H) × H) := cardCongruence G ((G ⧸ H) × H) (cosetProduct G H)
    _ = Nat.card (G ⧸ H) * Nat.card H := cardProduct (G ⧸ H) H

/-- Checked arithmetic step from the product identity to subgroup divisibility. -/
theorem divisibility_of_cardProduct
    (cardIdentity : CardProductIdentity.{u}) : ArbitraryGroupDivisibility.{u} := by
  intro G _ H
  refine ⟨Nat.card (G ⧸ H), ?_⟩
  simpa [mul_comm] using cardIdentity G H

/-- Checked adapter retaining the frozen finite-group premise. -/
theorem finiteScope_of_arbitraryGroup
    (anchor : ArbitraryGroupDivisibility.{u}) :
    Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget.{u} := by
  intro G _ _ H
  exact anchor G H

/-- Final identity composition into the exact canonical declaration. -/
theorem root_of_finiteScope
    (finiteScope : Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget.{u}) :
    Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget.{u} :=
  finiteScope

#check Subgroup.card_subgroup_dvd_card
#check Subgroup.card_eq_card_quotient_mul_card_subgroup
#check Nat.card_prod
#check Nat.card_congr
#check Subgroup.groupEquivQuotientProdSubgroup
#check Equiv.sigmaFiberEquiv
#check QuotientGroup.eq_class_eq_leftCoset
#check Quotient.out_eq'
#check Equiv.sigmaCongrRight
#check Subgroup.leftCosetEquivSubgroup
#check Equiv.sigmaEquivProd
#print axioms cosetProduct_of_fiber_engines
#print axioms cardProduct_of_engines
#print axioms divisibility_of_cardProduct
#print axioms finiteScope_of_arbitraryGroup
#print axioms root_of_finiteScope

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget

end Stage1Instances.THM_M_0061.ObligationTree
