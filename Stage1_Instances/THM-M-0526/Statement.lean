import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup

/-!
# THM-M-0526: exact Seifert-van Kampen statement

This module freezes the based two-open-set statement as the universal property
of a pushout of fundamental groups. It contains no proof of that statement.
-/

namespace Stage1Instances.THM_M_0526

open Set

universe u

noncomputable section

variable {X : Type u} [TopologicalSpace X]

/-- The continuous inclusion from a smaller subspace to a larger subspace. -/
def subspaceInclusion {A B : Set X} (hAB : A ⊆ B) : C(A, B) where
  toFun a := ⟨a.1, hAB a.2⟩
  continuous_toFun := continuous_subtype_val.subtype_mk _

/-- The continuous inclusion of a subspace into its ambient space. -/
def ambientInclusion (A : Set X) : C(A, X) where
  toFun := Subtype.val
  continuous_toFun := continuous_subtype_val

/-- The based fundamental-group map induced by a subspace inclusion. -/
def fundamentalGroupSubspaceMap {A B : Set X} (hAB : A ⊆ B) (x₀ : X)
    (hx : x₀ ∈ A) :
    FundamentalGroup A ⟨x₀, hx⟩ →*
      FundamentalGroup B ⟨x₀, hAB hx⟩ :=
  FundamentalGroup.map (subspaceInclusion hAB) ⟨x₀, hx⟩

/-- The based fundamental-group map induced by inclusion in the ambient space. -/
def fundamentalGroupAmbientMap (A : Set X) (x₀ : X) (hx : x₀ ∈ A) :
    FundamentalGroup A ⟨x₀, hx⟩ →* FundamentalGroup X x₀ :=
  FundamentalGroup.map (ambientInclusion A) ⟨x₀, hx⟩

/-- Universal-property formulation saying that the displayed square of groups
is a pushout. -/
def IsFundamentalGroupPushout (U V : Set X) (x₀ : X)
    (hxU : x₀ ∈ U) (hxV : x₀ ∈ V) : Prop :=
  let W : Set X := U ∩ V
  let hxW : x₀ ∈ W := ⟨hxU, hxV⟩
  let iWU := fundamentalGroupSubspaceMap (X := X) inter_subset_left x₀ hxW
  let iWV := fundamentalGroupSubspaceMap (X := X) inter_subset_right x₀ hxW
  let iUX := fundamentalGroupAmbientMap U x₀ hxU
  let iVX := fundamentalGroupAmbientMap V x₀ hxV
  iUX.comp iWU = iVX.comp iWV ∧
    ∀ (G : Type u) [Group G]
      (fU : FundamentalGroup U ⟨x₀, hxU⟩ →* G)
      (fV : FundamentalGroup V ⟨x₀, hxV⟩ →* G),
      fU.comp iWU = fV.comp iWV →
        ∃! lift : FundamentalGroup X x₀ →* G,
          lift.comp iUX = fU ∧ lift.comp iVX = fV

/-- The exact target selected for the classical based two-open-set
Seifert-van Kampen theorem. -/
def SeifertVanKampenTarget : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] (U V : Set X) (x₀ : X),
    ∀ (_hU : IsOpen U) (_hV : IsOpen V) (_hcover : U ∪ V = univ)
      (hxU : x₀ ∈ U) (hxV : x₀ ∈ V)
      (_hpcU : IsPathConnected U) (_hpcV : IsPathConnected V)
      (_hpcW : IsPathConnected (U ∩ V)),
      IsFundamentalGroupPushout U V x₀ hxU hxV

-- Separately elaborated structural mutations for statement-boundary checks.
def mutationRemovedOpenCover : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] (U V : Set X) (x₀ : X),
    ∀ (hxU : x₀ ∈ U) (hxV : x₀ ∈ V)
      (_hpcU : IsPathConnected U) (_hpcV : IsPathConnected V)
      (_hpcW : IsPathConnected (U ∩ V)),
      IsFundamentalGroupPushout U V x₀ hxU hxV

def mutationRemovedIntersectionConnected : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] (U V : Set X) (x₀ : X),
    ∀ (_hU : IsOpen U) (_hV : IsOpen V) (_hcover : U ∪ V = univ)
      (hxU : x₀ ∈ U) (hxV : x₀ ∈ V)
      (_hpcU : IsPathConnected U) (_hpcV : IsPathConnected V),
      IsFundamentalGroupPushout U V x₀ hxU hxV

def mutationGenerationOnly : Prop :=
  ∀ (X : Type u) [TopologicalSpace X] (U V : Set X) (x₀ : X)
    (_hU : IsOpen U) (_hV : IsOpen V) (_hcover : U ∪ V = univ)
    (hxU : x₀ ∈ U) (hxV : x₀ ∈ V)
    (_hpcU : IsPathConnected U) (_hpcV : IsPathConnected V)
    (_hpcW : IsPathConnected (U ∩ V)),
    ∀ g : FundamentalGroup X x₀,
      g ∈ Subgroup.closure
        (Set.range (fundamentalGroupAmbientMap U x₀ hxU) ∪
          Set.range (fundamentalGroupAmbientMap V x₀ hxV))

def mutationArbitrarySquare : Prop :=
  ∀ (A B C D : Type u) [Group A] [Group B] [Group C] [Group D]
    (f : A →* B) (g : A →* C) (h : B →* D) (i : C →* D),
    h.comp f = i.comp g →
    ∀ (G : Type u) [Group G] (p : B →* G) (q : C →* G),
      p.comp f = q.comp g → ∃! lift : D →* G, lift.comp h = p ∧ lift.comp i = q

/-- The common basepoint excludes an empty intersection. -/
theorem intersection_nonempty {U V : Set X} {x₀ : X} (hxU : x₀ ∈ U) (hxV : x₀ ∈ V) :
    (U ∩ V).Nonempty :=
  ⟨x₀, hxU, hxV⟩

end

end Stage1Instances.THM_M_0526

set_option pp.explicit true in
#print Stage1Instances.THM_M_0526.SeifertVanKampenTarget
