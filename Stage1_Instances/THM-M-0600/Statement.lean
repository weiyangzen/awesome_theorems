import Mathlib.Geometry.Manifold.ContMDiff.NormedSpace

/-!
# THM-M-0600: exact Morse lemma statement

This module freezes the local, finite-dimensional real-manifold statement. It
contains no proof of the Morse lemma.
-/

noncomputable section

open Set Function
open scoped Topology Manifold ContDiff

namespace Stage1Instances.THM_M_0600

universe u

/-- The standard `n`-dimensional real model space. -/
abbrev Euclidean (n : Nat) := Fin n -> Real

/-- Smooth coordinates centered at `p`, recorded only on their local source
and target. The inverse laws prevent this structure from supplying any
normal-form information about a function. -/
structure SmoothLocalCoordinates {n : Nat} (M : Type*) [TopologicalSpace M]
    [ChartedSpace (Euclidean n) M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n)) (p : M) where
  source : Set M
  target : Set (Euclidean n)
  toFun : M -> Euclidean n
  invFun : Euclidean n -> M
  source_open : IsOpen source
  target_open : IsOpen target
  mem_source : p ∈ source
  zero_mem_target : (0 : Euclidean n) ∈ target
  centered : toFun p = 0
  mapsTo_toFun : MapsTo toFun source target
  mapsTo_invFun : MapsTo invFun target source
  left_inv : Set.LeftInvOn invFun toFun source
  right_inv : Set.RightInvOn invFun toFun target
  toFun_smooth : ContMDiffOn I 𝓘(Real, Euclidean n) ⊤ toFun source
  invFun_smooth : ContMDiffOn 𝓘(Real, Euclidean n) I ⊤ invFun target

/-- Coordinate representative of a real-valued function. -/
def inCoordinates {n : Nat} {M : Type*} [TopologicalSpace M]
    [ChartedSpace (Euclidean n) M]
    {I : ModelWithCorners Real (Euclidean n) (Euclidean n)} {p : M}
    (c : SmoothLocalCoordinates M I p) (f : M -> Real) : Euclidean n -> Real :=
  f ∘ c.invFun

/-- The Hessian of `f` in the chosen centered coordinates. -/
def coordinateHessian {n : Nat} {M : Type*} [TopologicalSpace M]
    [ChartedSpace (Euclidean n) M]
    {I : ModelWithCorners Real (Euclidean n) (Euclidean n)} {p : M}
    (c : SmoothLocalCoordinates M I p) (f : M -> Real) :
    (Euclidean n →L[Real] (Euclidean n →L[Real] Real)) :=
  fderiv Real (fun x => fderiv Real (inCoordinates c f) x) 0

/-- The diagonal quadratic form having `index` negative directions. -/
def morseQuadratic {n : Nat} (index : Nat) (x : Euclidean n) : Real :=
  -(∑ i ∈ Finset.univ.filter (fun i : Fin n => (i : Nat) < index), (x i) ^ 2) +
    ∑ i ∈ Finset.univ.filter (fun i : Fin n => index ≤ (i : Nat)), (x i) ^ 2

/-- The canonical Morse lemma target.

For a smooth function near a nondegenerate critical point of a finite-dimensional
real smooth manifold without boundary, there are centered smooth local
coordinates in which the function is exactly a diagonal quadratic form. The
existential `index` is the number of negative squares.
-/
def MorseLemmaTarget : Prop :=
  ∀ (n : Nat) (M : Type u) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      fderiv Real (inCoordinates base f) 0 = 0 ->
      Function.Injective (coordinateHessian base f) ->
      ∃ (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index ≤ n ∧ ∀ x ∈ normal.target,
          f (normal.invFun x) = f p + morseQuadratic index x

/-- Directly expanded spelling used to check the statement boundary. -/
def ExpandedTarget : Prop := MorseLemmaTarget.{u}

theorem morseLemmaTarget_iff_expandedTarget :
    MorseLemmaTarget.{u} ↔ ExpandedTarget.{u} := Iff.rfl

-- Structural mutations: all elaborate, but deliberately change the target.
def mutationRemovedCriticalPoint : Prop :=
  ∀ (n : Nat) (M : Type*) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      Function.Injective (coordinateHessian base f) ->
      ∃ (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index ≤ n ∧ ∀ x ∈ normal.target,
          f (normal.invFun x) = f p + morseQuadratic index x

def mutationAllowsDegenerateHessian : Prop :=
  ∀ (n : Nat) (M : Type*) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      fderiv Real (inCoordinates base f) 0 = 0 ->
      ∃ (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index ≤ n ∧ ∀ x ∈ normal.target,
          f (normal.invFun x) = f p + morseQuadratic index x

def mutationLocalEqualityOnlyAtZero : Prop :=
  ∀ (n : Nat) (M : Type*) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      fderiv Real (inCoordinates base f) 0 = 0 ->
      Function.Injective (coordinateHessian base f) ->
      ∃ (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index ≤ n ∧ f (normal.invFun 0) = f p

def mutationPositiveSquaresFirst : Prop :=
  ∀ (n : Nat) (M : Type*) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      fderiv Real (inCoordinates base f) 0 = 0 ->
      Function.Injective (coordinateHessian base f) ->
      ∃ (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index ≤ n ∧ ∀ x ∈ normal.target,
          f (normal.invFun x) = f p - morseQuadratic index x

end Stage1Instances.THM_M_0600

set_option pp.explicit true in
#print Stage1Instances.THM_M_0600.MorseLemmaTarget
