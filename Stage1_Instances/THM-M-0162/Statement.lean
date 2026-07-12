import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.LinearAlgebra.CrossProduct

/-!
# THM-M-0162: exact Frenet-Serret statement

This module freezes the moving-frame equations for a unit-speed curve in
oriented Euclidean three-space. It contains no proof of those equations.
-/

namespace Stage1Instances.THM_M_0162

open Matrix

/-- Real coordinate vectors in the standard oriented Euclidean three-space. -/
abbrev Vec3 := Fin 3 -> Real

/-- The standard Euclidean norm on coordinate vectors. This is stated
explicitly so the ambient metric cannot silently become the Pi sup norm. -/
noncomputable def euclideanNorm (v : Vec3) : Real :=
  Real.sqrt (dotProduct v v)

/-- The exact pointwise-on-an-open-set target for the Frenet-Serret formulas.

The hypotheses expose derivative witnesses rather than using the noncomputable
`deriv`, fix the principal normal and oriented binormal by definition, and fix
the torsion sign as `-<B', N>`. The three derivative identities are conclusions,
not fields or assumptions. -/
def FrenetSerretTarget : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    IsOpen U ->
    (forall s, s ∈ U -> HasDerivAt alpha (T s) s) ->
    (forall s, s ∈ U -> HasDerivAt T (T' s) s) ->
    (forall s, s ∈ U -> HasDerivAt N (N' s) s) ->
    (forall s, s ∈ U -> HasDerivAt B (B' s) s) ->
    (forall s, s ∈ U -> euclideanNorm (T s) = 1) ->
    (forall s, s ∈ U -> kappa s = euclideanNorm (T' s)) ->
    (forall s, s ∈ U -> 0 < kappa s) ->
    (forall s, s ∈ U -> N s = (kappa s)⁻¹ • T' s) ->
    (forall s, s ∈ U -> B s = T s ⨯₃ N s) ->
    (forall s, s ∈ U -> tau s = -dotProduct (B' s) (N s)) ->
    forall s, s ∈ U ->
      T' s = kappa s • N s /\
      N' s = -(kappa s) • T s + tau s • B s /\
      B' s = -(tau s) • N s

-- Separately elaborated structural mutations for statement-boundary review.
def mutationAllowsZeroCurvature : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    IsOpen U ->
    (forall s, s ∈ U -> HasDerivAt alpha (T s) s) ->
    (forall s, s ∈ U -> HasDerivAt T (T' s) s) ->
    (forall s, s ∈ U -> HasDerivAt N (N' s) s) ->
    (forall s, s ∈ U -> HasDerivAt B (B' s) s) ->
    (forall s, s ∈ U -> euclideanNorm (T s) = 1) ->
    (forall s, s ∈ U -> kappa s = euclideanNorm (T' s)) ->
    (forall s, s ∈ U -> N s = (kappa s)⁻¹ • T' s) ->
    (forall s, s ∈ U -> B s = T s ⨯₃ N s) ->
    (forall s, s ∈ U -> tau s = -dotProduct (B' s) (N s)) ->
    forall s, s ∈ U ->
      T' s = kappa s • N s /\
      N' s = -(kappa s) • T s + tau s • B s /\
      B' s = -(tau s) • N s

def mutationNonUnitSpeed : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    IsOpen U ->
    (forall s, s ∈ U -> HasDerivAt alpha (T s) s) ->
    (forall s, s ∈ U -> HasDerivAt T (T' s) s) ->
    (forall s, s ∈ U -> HasDerivAt N (N' s) s) ->
    (forall s, s ∈ U -> HasDerivAt B (B' s) s) ->
    (forall s, s ∈ U -> kappa s = euclideanNorm (T' s)) ->
    (forall s, s ∈ U -> 0 < kappa s) ->
    (forall s, s ∈ U -> N s = (kappa s)⁻¹ • T' s) ->
    (forall s, s ∈ U -> B s = T s ⨯₃ N s) ->
    (forall s, s ∈ U -> tau s = -dotProduct (B' s) (N s)) ->
    forall s, s ∈ U ->
      T' s = kappa s • N s /\
      N' s = -(kappa s) • T s + tau s • B s /\
      B' s = -(tau s) • N s

def mutationOppositeTorsionSign : Prop :=
  forall (U : Set Real) (alpha T T' N N' B B' : Real -> Vec3)
      (kappa tau : Real -> Real),
    IsOpen U ->
    (forall s, s ∈ U -> HasDerivAt alpha (T s) s) ->
    (forall s, s ∈ U -> HasDerivAt T (T' s) s) ->
    (forall s, s ∈ U -> HasDerivAt N (N' s) s) ->
    (forall s, s ∈ U -> HasDerivAt B (B' s) s) ->
    (forall s, s ∈ U -> euclideanNorm (T s) = 1) ->
    (forall s, s ∈ U -> kappa s = euclideanNorm (T' s)) ->
    (forall s, s ∈ U -> 0 < kappa s) ->
    (forall s, s ∈ U -> N s = (kappa s)⁻¹ • T' s) ->
    (forall s, s ∈ U -> B s = T s ⨯₃ N s) ->
    (forall s, s ∈ U -> tau s = dotProduct (B' s) (N s)) ->
    forall s, s ∈ U ->
      T' s = kappa s • N s /\
      N' s = -(kappa s) • T s - tau s • B s /\
      B' s = tau s • N s

end Stage1Instances.THM_M_0162

set_option pp.explicit true in
#print Stage1Instances.THM_M_0162.FrenetSerretTarget
