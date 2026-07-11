import Mathlib.AlgebraicGeometry.Properties

/-!
# THM-M-0119: Kawamata--Viehweg vanishing statement

This module freezes the projective klt-pair formulation selected at intake.
The pinned mathlib snapshot has schemes, but not the required bundled APIs for
Q-divisors, klt pairs, positivity, divisorial sheaves, or their coherent
cohomology. `KawamataViehwegData` therefore exposes those unavailable notions
as typed data and named predicates. No field assumes the vanishing conclusion.

This file states the target only; it does not prove the vanishing theorem.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u w

namespace Stage1Instances.THMM0119

/-- The base scheme of a field. -/
abbrev SpecOf (k : Type u) [CommRing k] : Scheme.{u} :=
  Spec (CommRingCat.of k)

/--
Data needed to state the selected Kawamata--Viehweg theorem in the current
dependency snapshot. The compatibility predicates name the standard
algebro-geometric meanings absent from the pinned APIs. `cohomology D i` is
the coherent cohomology group `H^i(X, O_X(D))`.
-/
structure KawamataViehwegData (k : Type u) [Field k] [CharZero k] where
  X : Scheme.{u}
  structureMap : X ⟶ SpecOf k
  isVarietyOverBase : Prop
  isNormal : Prop
  isProjective : Prop
  qDivisor : Type w
  cartierDivisor : Type w
  delta : qDivisor
  D : cartierDivisor
  canonicalPlusBoundary : qDivisor
  cartierToQDivisor : cartierDivisor -> qDivisor
  qSub : qDivisor -> qDivisor -> qDivisor
  deltaEffective : Prop
  canonicalPlusBoundaryModels : Prop
  canonicalPlusBoundaryQCartier : Prop
  pairIsKlt : Prop
  isNef : qDivisor -> Prop
  isBig : qDivisor -> Prop
  isAmple : qDivisor -> Prop
  cohomology : cartierDivisor -> Nat -> Type w
  [cohomologyAddCommGroup : forall D i, AddCommGroup (cohomology D i)]
  cohomologyModelsDivisorialSheaf : Prop

attribute [instance] KawamataViehwegData.cohomologyAddCommGroup

namespace KawamataViehwegData

variable {k : Type u} [Field k] [CharZero k]

/-- The full geometric and encoding hypotheses of the frozen pair model. -/
def Hypotheses (V : KawamataViehwegData.{u, w} k) : Prop :=
  V.isVarietyOverBase /\ V.isNormal /\ V.isProjective /\
    V.deltaEffective /\ V.canonicalPlusBoundaryModels /\
      V.canonicalPlusBoundaryQCartier /\ V.pairIsKlt /\
        V.cohomologyModelsDivisorialSheaf /\
          V.isNef (V.qSub (V.cartierToQDivisor V.D) V.canonicalPlusBoundary) /\
            V.isBig (V.qSub (V.cartierToQDivisor V.D) V.canonicalPlusBoundary)

/-- Vanishing of every positive-degree `H^i(X, O_X(D))`. -/
def VanishingConclusion (V : KawamataViehwegData.{u, w} k) : Prop :=
  forall i : Nat, 0 < i -> Subsingleton (V.cohomology V.D i)

end KawamataViehwegData

/--
The exact normalized target: over every characteristic-zero field, the higher
coherent cohomology of `O_X(D)` vanishes for a normal projective klt pair when
`D - (K_X + Delta)` is nef and big.
-/
def KawamataViehwegVanishingTarget : Prop :=
  forall (k : Type u) [Field k] [CharZero k]
    (V : KawamataViehwegData.{u, w} k),
      V.Hypotheses -> V.VanishingConclusion

/-- Checked expansion fixing all ordered binders, hypotheses, and degrees. -/
theorem kawamataViehwegVanishingTarget_iff_expanded :
    KawamataViehwegVanishingTarget.{u, w} <->
      forall (k : Type u) [Field k] [CharZero k]
        (V : KawamataViehwegData.{u, w} k),
          V.isVarietyOverBase /\ V.isNormal /\ V.isProjective /\
            V.deltaEffective /\ V.canonicalPlusBoundaryModels /\
              V.canonicalPlusBoundaryQCartier /\ V.pairIsKlt /\
                V.cohomologyModelsDivisorialSheaf /\
                  V.isNef
                    (V.qSub (V.cartierToQDivisor V.D) V.canonicalPlusBoundary) /\
                  V.isBig
                    (V.qSub (V.cartierToQDivisor V.D) V.canonicalPlusBoundary) ->
            forall i : Nat, 0 < i -> Subsingleton (V.cohomology V.D i) :=
  Iff.rfl

-- Separately elaborated mutations receive no identity or implication credit.
def MutationRemovedKlt : Prop :=
  forall (k : Type u) [Field k] [CharZero k]
    (V : KawamataViehwegData.{u, w} k),
      V.isNormal -> V.isProjective -> V.VanishingConclusion

def MutationAmpleInsteadOfNefAndBig : Prop :=
  forall (k : Type u) [Field k] [CharZero k]
    (V : KawamataViehwegData.{u, w} k),
      V.isNormal -> V.isProjective -> V.deltaEffective -> V.pairIsKlt ->
        V.isAmple
          (V.qSub (V.cartierToQDivisor V.D) V.canonicalPlusBoundary) ->
            V.VanishingConclusion

def MutationIncludesDegreeZero : Prop :=
  forall (k : Type u) [Field k] [CharZero k]
    (V : KawamataViehwegData.{u, w} k),
      V.Hypotheses -> Subsingleton (V.cohomology V.D 0)

end Stage1Instances.THMM0119

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0119.KawamataViehwegVanishingTarget
