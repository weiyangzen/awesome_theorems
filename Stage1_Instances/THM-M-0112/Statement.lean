import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0112: weak topological Lefschetz statement boundary

The pinned library has homotopy groups, but not complex analytification or a
bundled smooth projective hyperplane-section API. The structure below exposes
those missing notions as typed interface propositions and exposes the map that
such a realization induces on homotopy groups. No field assumes injectivity,
surjectivity, or the conclusion of weak Lefschetz.

This module freezes the target only. It does not prove the theorem.
-/

noncomputable section

open scoped Topology

namespace Stage1Instances.THMM0112

universe uX uY

/-- Data needed to state weak topological Lefschetz against the APIs available
in the pinned snapshot. The four geometric propositions denote their standard
complex-algebraic meanings; closing them against a future analytification API
is an integration obligation, not theorem evidence supplied here. -/
structure LefschetzHyperplaneData
    (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y] where
  complexDimension : Nat
  inclusion : C(Y, X)
  basePoint : Y
  ambientConnected : IsConnected (Set.univ : Set X)
  ambientSmoothOverComplex : Prop
  ambientProjectiveOverComplex : Prop
  sectionIsSmooth : Prop
  sectionIsHyperplaneForInclusion : Prop
  piMap : forall k : Nat,
    HomotopyGroup.Pi k Y basePoint ->
      HomotopyGroup.Pi k X (inclusion basePoint)
  piMapIsInducedByInclusion : Prop

namespace LefschetzHyperplaneData

variable
  {X : Type uX} [TopologicalSpace X]
  {Y : Type uY} [TopologicalSpace Y]

/-- The full weak topological Lefschetz conclusion, including its boundary
degree. Natural-number subtraction makes the low-dimensional range explicit. -/
def Conclusion (D : LefschetzHyperplaneData X Y) : Prop :=
  (forall k : Nat, k < D.complexDimension - 1 ->
    Function.Bijective (D.piMap k)) /\
  Function.Surjective (D.piMap (D.complexDimension - 1))

end LefschetzHyperplaneData

/-- Exact selected root: for a connected smooth complex projective variety of
complex dimension `n` and a smooth hyperplane section, inclusion induces
isomorphisms on `pi_k` below `n - 1` and a surjection in degree `n - 1`.

`Function.Bijective` is used uniformly because mathlib's `Pi 0` is a type of
path components rather than a group. -/
def WeakTopologicalLefschetzTarget : Prop :=
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex ->
      D.ambientProjectiveOverComplex ->
      D.sectionIsSmooth ->
      D.sectionIsHyperplaneForInclusion ->
      D.piMapIsInducedByInclusion ->
      D.Conclusion

/-- Checked expansion fixing all binders, hypotheses, ranges, and the two
components of the conclusion. -/
theorem weakTopologicalLefschetzTarget_iff_expanded :
    WeakTopologicalLefschetzTarget.{uX, uY} <->
      forall (X : Type uX) [TopologicalSpace X]
        (Y : Type uY) [TopologicalSpace Y]
        (D : LefschetzHyperplaneData X Y),
          D.ambientSmoothOverComplex ->
          D.ambientProjectiveOverComplex ->
          D.sectionIsSmooth ->
          D.sectionIsHyperplaneForInclusion ->
          D.piMapIsInducedByInclusion ->
          (forall k : Nat, k < D.complexDimension - 1 ->
            Function.Bijective (D.piMap k)) /\
          Function.Surjective (D.piMap (D.complexDimension - 1)) :=
  Iff.rfl

-- Separately elaborated structural mutations; none receives equivalence credit.
def MutationRemovedProjectivity : Prop :=
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex -> D.sectionIsSmooth ->
      D.sectionIsHyperplaneForInclusion -> D.piMapIsInducedByInclusion ->
      D.Conclusion

def MutationChangedDimensionDomain : Prop :=
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex -> D.ambientProjectiveOverComplex ->
      D.sectionIsSmooth -> D.sectionIsHyperplaneForInclusion ->
      D.piMapIsInducedByInclusion ->
      (forall k : Nat, (k : Int) < (D.complexDimension : Int) - 1 ->
        Function.Bijective (D.piMap k)) /\
      Function.Surjective (D.piMap (D.complexDimension - 1))

def MutationChangedBinderScope : Prop :=
  forall k : Nat,
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex -> D.ambientProjectiveOverComplex ->
      D.sectionIsSmooth -> D.sectionIsHyperplaneForInclusion ->
      D.piMapIsInducedByInclusion ->
      k < D.complexDimension - 1 -> Function.Bijective (D.piMap k)

def MutationIncludesBoundaryInIsomorphism : Prop :=
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex -> D.ambientProjectiveOverComplex ->
      D.sectionIsSmooth -> D.sectionIsHyperplaneForInclusion ->
      D.piMapIsInducedByInclusion ->
      forall k : Nat, k <= D.complexDimension - 1 ->
        Function.Bijective (D.piMap k)

end Stage1Instances.THMM0112

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget
