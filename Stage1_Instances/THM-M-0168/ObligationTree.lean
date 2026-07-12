import Mathlib.Analysis.Calculus.ContDiff.Defs

/-!
# THM-M-0168 obligation composition harness

This file checks the exact top-level decomposition.  The two mathematical
packages are propositions supplied as hypotheses; no Bernstein proof is
asserted here.
-/

namespace Stage1Instances.THM_M_0168_Obligations

abbrev Plane := Real × Real

def coordinateVector : Fin 2 -> Plane
  | 0 => (1, 0)
  | 1 => (0, 1)

noncomputable def partialDeriv (u : Plane -> Real) (i : Fin 2) (p : Plane) : Real :=
  fderiv Real u p (coordinateVector i)

noncomputable def secondPartial (u : Plane -> Real) (i j : Fin 2) (p : Plane) : Real :=
  fderiv Real (partialDeriv u i) p (coordinateVector j)

noncomputable def SatisfiesMinimalSurfaceEquation (u : Plane -> Real) : Prop :=
  forall p : Plane,
    (1 + (partialDeriv u 1 p) ^ 2) * secondPartial u 0 0 p
      - 2 * partialDeriv u 0 p * partialDeriv u 1 p * secondPartial u 0 1 p
      + (1 + (partialDeriv u 0 p) ^ 2) * secondPartial u 1 1 p = 0

def BernsteinMinimalGraphTarget : Prop :=
  forall u : Plane -> Real,
    ContDiff Real 2 u ->
    SatisfiesMinimalSurfaceEquation u ->
    exists a b c : Real, forall p : Plane, u p = a * p.1 + b * p.2 + c

/-- Open analytic/geometric engine: both first coordinate derivatives are
constant on the entire plane. -/
def DerivativeRigidity : Prop :=
  forall u : Plane -> Real,
    ContDiff Real 2 u ->
    SatisfiesMinimalSurfaceEquation u ->
    exists a b : Real, forall p : Plane,
      partialDeriv u 0 p = a /\ partialDeriv u 1 p = b

/-- Open calculus bridge from constant Frechet coordinate derivatives to the
global affine formula. -/
def ConstantPartialsToAffine : Prop :=
  forall u : Plane -> Real,
    ContDiff Real 2 u ->
    forall a b : Real,
      (forall p : Plane,
        partialDeriv u 0 p = a /\ partialDeriv u 1 p = b) ->
      exists c : Real, forall p : Plane, u p = a * p.1 + b * p.2 + c

/-- Conditional child-to-root composition.  Both open packages are consumed
and the result is the complete canonical target. -/
theorem compose_root
    (rigidity : DerivativeRigidity)
    (integrate : ConstantPartialsToAffine) :
    BernsteinMinimalGraphTarget := by
  intro u hu hminimal
  obtain ⟨a, b, hab⟩ := rigidity u hu hminimal
  obtain ⟨c, hc⟩ := integrate u hu a b hab
  exact ⟨a, b, c, hc⟩

#check compose_root
set_option pp.explicit true in
#print BernsteinMinimalGraphTarget
#print axioms compose_root

end Stage1Instances.THM_M_0168_Obligations
