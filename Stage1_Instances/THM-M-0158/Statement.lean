import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

/-!
# THM-M-0158: exact Weingarten-equations statement

This module freezes the local-coordinate statement only. It contains no proof of the
Weingarten equations.
-/

namespace Stage1Instances.THM_M_0158

abbrev ParameterSpace := EuclideanSpace Real (Fin 2)
abbrev AmbientSpace := EuclideanSpace Real (Fin 3)

/-- The `i`th coordinate vector in the parameter plane. -/
noncomputable def coordinateVector (i : Fin 2) : ParameterSpace :=
  EuclideanSpace.single i 1

/-- Coordinate partial derivative, relative to a parameter domain. -/
noncomputable def partialWithin (U : Set ParameterSpace) (f : ParameterSpace -> AmbientSpace)
    (i : Fin 2) (q : ParameterSpace) : AmbientSpace :=
  fderivWithin Real f U q (coordinateVector i)

/-- First fundamental form matrix in the coordinate tangent basis. -/
noncomputable def firstFundamentalForm (U : Set ParameterSpace)
    (x : ParameterSpace -> AmbientSpace) (q : ParameterSpace) : Matrix (Fin 2) (Fin 2) Real :=
  fun i j => @inner Real AmbientSpace _ (partialWithin U x i q) (partialWithin U x j q)

/-- Second fundamental form matrix, with `II i j = <x_ij, N>`. -/
noncomputable def secondFundamentalForm (U : Set ParameterSpace)
    (x N : ParameterSpace -> AmbientSpace) (q : ParameterSpace) : Matrix (Fin 2) (Fin 2) Real :=
  fun i j => @inner Real AmbientSpace _ (partialWithin U (partialWithin U x i) j q) (N q)

/-- The exact local Weingarten-equations target. The column indexed by `i` says
`N_i = sum_j (-(I^-1 * II))_ji x_j`. -/
def WeingartenEquationsTarget : Prop :=
  forall (U : Set ParameterSpace) (x N : ParameterSpace -> AmbientSpace) (p : ParameterSpace),
    IsOpen U ->
    p ∈ U ->
    ContDiffOn Real 2 x U ->
    ContDiffOn Real 1 N U ->
    (forall q, q ∈ U -> ‖N q‖ = 1) ->
    (forall q, q ∈ U -> forall i : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin U x i q) = 0) ->
    Matrix.det (firstFundamentalForm U x p) ≠ 0 ->
    forall i : Fin 2,
      partialWithin U N i p =
        ∑ j : Fin 2,
          (-(firstFundamentalForm U x p)⁻¹ * secondFundamentalForm U x N p) j i •
            partialWithin U x j p

-- Structural mutations elaborated separately and rejected by the statement checker.
def mutationRemovedRegularity : Prop :=
  forall (U : Set ParameterSpace) (x N : ParameterSpace -> AmbientSpace) (p : ParameterSpace),
    IsOpen U -> p ∈ U -> ContDiffOn Real 2 x U -> ContDiffOn Real 1 N U ->
    (forall q, q ∈ U -> ‖N q‖ = 1) ->
    (forall q, q ∈ U -> forall i : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin U x i q) = 0) ->
    forall i : Fin 2,
      partialWithin U N i p =
        ∑ j : Fin 2,
          (-(firstFundamentalForm U x p)⁻¹ * secondFundamentalForm U x N p) j i •
            partialWithin U x j p

def mutationChangedDomain : Prop :=
  forall (x N : ParameterSpace -> AmbientSpace) (p : ParameterSpace),
    ContDiff Real 2 x -> ContDiff Real 1 N ->
    (forall q, ‖N q‖ = 1) ->
    (forall q, forall i : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin Set.univ x i q) = 0) ->
    Matrix.det (firstFundamentalForm Set.univ x p) ≠ 0 ->
    forall i : Fin 2,
      partialWithin Set.univ N i p =
        ∑ j : Fin 2,
          (-(firstFundamentalForm Set.univ x p)⁻¹ *
            secondFundamentalForm Set.univ x N p) j i • partialWithin Set.univ x j p

def mutationChangedBinderScope : Prop :=
  forall (U : Set ParameterSpace) (x N : ParameterSpace -> AmbientSpace),
    IsOpen U -> ContDiffOn Real 2 x U -> ContDiffOn Real 1 N U ->
    (forall q, q ∈ U -> ‖N q‖ = 1) ->
    (forall q, q ∈ U -> forall i : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin U x i q) = 0) ->
    forall p, p ∈ U -> Matrix.det (firstFundamentalForm U x p) ≠ 0 ->
      forall i : Fin 2,
        partialWithin U N i p =
          ∑ j : Fin 2,
            (-(firstFundamentalForm U x p)⁻¹ * secondFundamentalForm U x N p) j i •
              partialWithin U x j p

def mutationAllowsBoundaryPoint : Prop :=
  forall (U : Set ParameterSpace) (x N : ParameterSpace -> AmbientSpace) (p : ParameterSpace),
    IsOpen U ->
    ContDiffOn Real 2 x U -> ContDiffOn Real 1 N U ->
    (forall q, q ∈ U -> ‖N q‖ = 1) ->
    (forall q, q ∈ U -> forall i : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin U x i q) = 0) ->
    Matrix.det (firstFundamentalForm U x p) ≠ 0 ->
    forall i : Fin 2,
      partialWithin U N i p =
        ∑ j : Fin 2,
          (-(firstFundamentalForm U x p)⁻¹ * secondFundamentalForm U x N p) j i •
            partialWithin U x j p

end Stage1Instances.THM_M_0158

set_option pp.explicit true in
#print Stage1Instances.THM_M_0158.WeingartenEquationsTarget
