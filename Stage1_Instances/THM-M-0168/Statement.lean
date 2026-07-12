import Mathlib.Analysis.Calculus.ContDiff.Defs

/-!
# THM-M-0168: exact two-dimensional Bernstein statement

This module freezes the classical minimal-graph PDE statement only. It does not
contain a proof of Bernstein's theorem.
-/

namespace Stage1Instances.THM_M_0168

abbrev Plane := Real × Real

/-- The two coordinate directions in the domain plane. -/
def coordinateVector : Fin 2 -> Plane
  | 0 => (1, 0)
  | 1 => (0, 1)

/-- A coordinate first derivative, defined using the Frechet derivative. -/
noncomputable def partialDeriv (u : Plane -> Real) (i : Fin 2) (p : Plane) : Real :=
  fderiv Real u p (coordinateVector i)

/-- An ordered coordinate second derivative. -/
noncomputable def secondPartial (u : Plane -> Real) (i j : Fin 2) (p : Plane) : Real :=
  fderiv Real (partialDeriv u i) p (coordinateVector j)

/-- The nonparametric minimal-surface equation in two variables. -/
noncomputable def SatisfiesMinimalSurfaceEquation (u : Plane -> Real) : Prop :=
  forall p : Plane,
    (1 + (partialDeriv u 1 p) ^ 2) * secondPartial u 0 0 p
      - 2 * partialDeriv u 0 p * partialDeriv u 1 p * secondPartial u 0 1 p
      + (1 + (partialDeriv u 0 p) ^ 2) * secondPartial u 1 1 p = 0

/-- The exact entire-graph Bernstein target: every `C2` solution of the
two-dimensional minimal-surface equation on all of `R^2` is affine. -/
def BernsteinMinimalGraphTarget : Prop :=
  forall u : Plane -> Real,
    ContDiff Real 2 u ->
    SatisfiesMinimalSurfaceEquation u ->
    exists a b c : Real, forall p : Plane, u p = a * p.1 + b * p.2 + c

-- Structural mutations are elaborated and rejected by `check_statement.py`.
def mutationRemovedMinimality : Prop :=
  forall u : Plane -> Real,
    ContDiff Real 2 u ->
    exists a b c : Real, forall p : Plane, u p = a * p.1 + b * p.2 + c

def mutationChangedDomain : Prop :=
  forall u : Real -> Real,
    ContDiff Real 2 u ->
    exists a b : Real, forall x : Real, u x = a * x + b

def mutationChangedBinderScope : Prop :=
  exists a b c : Real, forall u : Plane -> Real,
    ContDiff Real 2 u ->
    SatisfiesMinimalSurfaceEquation u ->
    forall p : Plane, u p = a * p.1 + b * p.2 + c

def mutationStrengthenedHypothesis : Prop :=
  forall u : Plane -> Real,
    ContDiff Real 2 u ->
    SatisfiesMinimalSurfaceEquation u ->
    (forall p, partialDeriv u 0 p = 0) ->
    exists a b c : Real, forall p : Plane, u p = a * p.1 + b * p.2 + c

end Stage1Instances.THM_M_0168

set_option pp.explicit true in
#print Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget
