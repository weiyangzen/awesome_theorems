import «Stage1_Instances».«THM-M-0526».Statement

/-!
# THM-M-0526: typed obligation-tree composition

This module checks only the interfaces by which the three universal-property
obligations compose.  The hypotheses below are deliberately not proofs of van
Kampen: their implementations remain open proof-phase obligations.
-/

namespace Stage1Instances.THM_M_0526

open Set

universe u

noncomputable section

variable {X : Type u} [TopologicalSpace X]

private abbrev PieceGroup (A : Set X) (x0 : X) (hx : x0 ∈ A) :=
  FundamentalGroup A ⟨x0, hx⟩

/-- `OBL-SQUARE`: the two inclusion composites agree. -/
def SquareCommutativity (U V : Set X) (x0 : X)
    (hxU : x0 ∈ U) (hxV : x0 ∈ V) : Prop :=
  let hxW : x0 ∈ U ∩ V := ⟨hxU, hxV⟩
  let iWU := fundamentalGroupSubspaceMap (X := X) inter_subset_left x0 hxW
  let iWV := fundamentalGroupSubspaceMap (X := X) inter_subset_right x0 hxW
  let iUX := fundamentalGroupAmbientMap U x0 hxU
  let iVX := fundamentalGroupAmbientMap V x0 hxV
  iUX.comp iWU = iVX.comp iWV

/-- `OBL-LIFT-EXISTS`: every compatible cocone has a mediator. -/
def LiftExistence (U V : Set X) (x0 : X)
    (hxU : x0 ∈ U) (hxV : x0 ∈ V) : Prop :=
  let hxW : x0 ∈ U ∩ V := ⟨hxU, hxV⟩
  let iWU := fundamentalGroupSubspaceMap (X := X) inter_subset_left x0 hxW
  let iWV := fundamentalGroupSubspaceMap (X := X) inter_subset_right x0 hxW
  let iUX := fundamentalGroupAmbientMap U x0 hxU
  let iVX := fundamentalGroupAmbientMap V x0 hxV
  ∀ (G : Type u) [Group G]
    (fU : PieceGroup U x0 hxU →* G)
    (fV : PieceGroup V x0 hxV →* G),
    fU.comp iWU = fV.comp iWV →
      ∃ lift : FundamentalGroup X x0 →* G,
        lift.comp iUX = fU ∧ lift.comp iVX = fV

/-- `OBL-LIFT-UNIQUE`: two mediators agreeing on both pieces are equal. -/
def LiftUniqueness (U V : Set X) (x0 : X)
    (hxU : x0 ∈ U) (hxV : x0 ∈ V) : Prop :=
  let iUX := fundamentalGroupAmbientMap U x0 hxU
  let iVX := fundamentalGroupAmbientMap V x0 hxV
  ∀ (G : Type u) [Group G]
    (fU : PieceGroup U x0 hxU →* G)
    (fV : PieceGroup V x0 hxV →* G)
    (lift lift' : FundamentalGroup X x0 →* G),
    lift.comp iUX = fU → lift.comp iVX = fV →
    lift'.comp iUX = fU → lift'.comp iVX = fV → lift' = lift

/-- Checked child-to-parent certificate for the universal-property node. -/
theorem compose_pushout
    (U V : Set X) (x0 : X) (hxU : x0 ∈ U) (hxV : x0 ∈ V)
    (hSquare : SquareCommutativity U V x0 hxU hxV)
    (hExists : LiftExistence U V x0 hxU hxV)
    (hUnique : LiftUniqueness U V x0 hxU hxV) :
    IsFundamentalGroupPushout U V x0 hxU hxV := by
  refine ⟨hSquare, ?_⟩
  intro G _ fU fV hcompat
  obtain ⟨lift, hU, hV⟩ := hExists G fU fV hcompat
  refine ⟨lift, ⟨hU, hV⟩, ?_⟩
  intro lift' hlift'
  exact hUnique G fU fV lift lift' hU hV hlift'.1 hlift'.2

/-- Checked root certificate.  Its three package arguments are the open proof
interfaces; this theorem gives them no proof credit. -/
theorem compose_root
    (squarePackage : ∀ (X : Type u) [TopologicalSpace X]
      (U V : Set X) (x0 : X), IsOpen U → IsOpen V → U ∪ V = univ →
      (hxU : x0 ∈ U) → (hxV : x0 ∈ V) →
      IsPathConnected U → IsPathConnected V → IsPathConnected (U ∩ V) →
      SquareCommutativity U V x0 hxU hxV)
    (existencePackage : ∀ (X : Type u) [TopologicalSpace X]
      (U V : Set X) (x0 : X), IsOpen U → IsOpen V → U ∪ V = univ →
      (hxU : x0 ∈ U) → (hxV : x0 ∈ V) →
      IsPathConnected U → IsPathConnected V → IsPathConnected (U ∩ V) →
      LiftExistence U V x0 hxU hxV)
    (uniquenessPackage : ∀ (X : Type u) [TopologicalSpace X]
      (U V : Set X) (x0 : X), IsOpen U → IsOpen V → U ∪ V = univ →
      (hxU : x0 ∈ U) → (hxV : x0 ∈ V) →
      IsPathConnected U → IsPathConnected V → IsPathConnected (U ∩ V) →
      LiftUniqueness U V x0 hxU hxV) :
    SeifertVanKampenTarget.{u} := by
  intro X _ U V x0 hU hV hcover hxU hxV hpcU hpcV hpcW
  apply compose_pushout U V x0 hxU hxV
  · exact squarePackage X U V x0 hU hV hcover hxU hxV hpcU hpcV hpcW
  · exact existencePackage X U V x0 hU hV hcover hxU hxV hpcU hpcV hpcW
  · exact uniquenessPackage X U V x0 hU hV hcover hxU hxV hpcU hpcV hpcW

end

end Stage1Instances.THM_M_0526

#check Stage1Instances.THM_M_0526.compose_pushout
#check Stage1Instances.THM_M_0526.compose_root
#print axioms Stage1Instances.THM_M_0526.compose_pushout
#print axioms Stage1Instances.THM_M_0526.compose_root
