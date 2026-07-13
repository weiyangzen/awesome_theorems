import ObligationTree

/-!
# THM-M-0061 proof execution

This module realizes every machine-relevant leaf of the frozen Lagrange architecture, composes
the quotient-times-subgroup equivalence, derives the cardinal product identity, and closes the
exact finite-group target. The proof uses the pinned mathlib APIs inventoried by the anchor audit.
-/

noncomputable section

namespace Stage1Instances.THM_M_0061.Proof

open scoped Pointwise
open Stage1Instances.THM_M_0061

universe u

/-- The quotient map decomposes the group into the sigma type of its fibers. -/
noncomputable def fiberDecomposition :
    ObligationTree.FiberDecomposition.{u} := by
  intro G _ H
  exact (Equiv.sigmaFiberEquiv QuotientGroup.mk).symm

/-- A quotient-map fiber is the left coset represented by `Quotient.out`. -/
noncomputable def fiberToLeftCoset :
    ObligationTree.FiberToLeftCoset.{u} := by
  intro G _ H L
  rw [← QuotientGroup.eq_class_eq_leftCoset]
  change
    (_root_.Subtype fun x : G => Quotient.mk'' x = L) ≃
      _root_.Subtype fun x : G => Quotient.mk'' x = Quotient.mk'' _
  simp
  rfl

/-- Left multiplication identifies each left coset with the subgroup. -/
noncomputable def leftCosetEquivalence :
    ObligationTree.LeftCosetEquivalence.{u} := by
  intro G _ H g
  exact H.leftCosetEquivSubgroup g

/-- A constant sigma family is the corresponding product. -/
noncomputable def sigmaProductEquivalence :
    ObligationTree.SigmaProductEquivalence.{u} := by
  intro G _ H
  exact Equiv.sigmaEquivProd (G ⧸ H) H

/-- The four construction engines compose to the quotient-times-subgroup equivalence. -/
noncomputable def cosetProductEquivalence :
    ObligationTree.CosetProductEquivalence.{u} :=
  ObligationTree.cosetProduct_of_fiber_engines fiberDecomposition
    fiberToLeftCoset leftCosetEquivalence sigmaProductEquivalence

/-- `Nat.card` is multiplicative on products. -/
theorem natCardProduct : ObligationTree.NatCardProductEngine.{u} := by
  intro alpha beta
  exact Nat.card_prod alpha beta

/-- `Nat.card` is invariant under equivalence. -/
theorem natCardCongruence : ObligationTree.NatCardCongruenceEngine.{u} := by
  intro alpha beta e
  exact Nat.card_congr e

/-- The product-cardinality identity obtained from the constructed equivalence. -/
theorem cardProductIdentity : ObligationTree.CardProductIdentity.{u} :=
  ObligationTree.cardProduct_of_engines natCardProduct natCardCongruence
    cosetProductEquivalence

/-- The audited pinned product-cardinality bridge at the frozen interface. -/
theorem pinnedCardProductIdentity : ObligationTree.CardProductIdentity.{u} := by
  intro G _ H
  exact Subgroup.card_eq_card_quotient_mul_card_subgroup H

/-- The product identity supplies the Lagrange divisibility witness. -/
theorem arbitraryGroupDivisibility :
    ObligationTree.ArbitraryGroupDivisibility.{u} :=
  ObligationTree.divisibility_of_cardProduct cardProductIdentity

/-- The audited pinned Lagrange declaration, installed at its exact stronger interface. -/
theorem pinnedArbitraryGroupDivisibility :
    ObligationTree.ArbitraryGroupDivisibility.{u} := by
  intro G _ H
  exact Subgroup.card_subgroup_dvd_card H

/-- Specialize arbitrary-group divisibility to the frozen finite-group interface. -/
theorem finiteGroupDivisibility : LagrangeDivisibilityTarget.{u} :=
  ObligationTree.finiteScope_of_arbitraryGroup arbitraryGroupDivisibility

/-- The exact frozen Lagrange divisibility target. -/
theorem lagrangeDivisibility : LagrangeDivisibilityTarget.{u} :=
  ObligationTree.root_of_finiteScope finiteGroupDivisibility

/-- Independent exact-root wrapper over the pinned mathlib Lagrange declaration. -/
theorem lagrangeDivisibility_mathlib : LagrangeDivisibilityTarget.{u} :=
  ObligationTree.root_of_finiteScope <|
    ObligationTree.finiteScope_of_arbitraryGroup pinnedArbitraryGroupDivisibility

#print sorries fiberDecomposition
#print sorries fiberToLeftCoset
#print sorries leftCosetEquivalence
#print sorries sigmaProductEquivalence
#print sorries cosetProductEquivalence
#print sorries natCardProduct
#print sorries natCardCongruence
#print sorries cardProductIdentity
#print sorries pinnedCardProductIdentity
#print sorries arbitraryGroupDivisibility
#print sorries pinnedArbitraryGroupDivisibility
#print sorries finiteGroupDivisibility
#print sorries lagrangeDivisibility
#print sorries lagrangeDivisibility_mathlib
#print axioms fiberDecomposition
#print axioms fiberToLeftCoset
#print axioms leftCosetEquivalence
#print axioms sigmaProductEquivalence
#print axioms cosetProductEquivalence
#print axioms natCardProduct
#print axioms natCardCongruence
#print axioms cardProductIdentity
#print axioms pinnedCardProductIdentity
#print axioms arbitraryGroupDivisibility
#print axioms pinnedArbitraryGroupDivisibility
#print axioms finiteGroupDivisibility
#print axioms lagrangeDivisibility
#print axioms lagrangeDivisibility_mathlib

end Stage1Instances.THM_M_0061.Proof
