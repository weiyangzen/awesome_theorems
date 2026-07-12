import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-1245: exact Sobolev inequality statement

This module freezes the classical first-order Euclidean norm inequality selected
at intake. It states the target only; it does not claim proof or anchor credit.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1245

/--
For every positive Euclidean dimension and Sobolev exponents `1 <= p < n`
(the strict upper bound follows from the displayed conjugacy equation), there
is a constant depending only on `n`, `p`, and `q` such that every compactly
supported continuously differentiable real function has its `L^q` norm
bounded by that constant times the `L^p` norm of its Frechet derivative.

The domain carries mathlib's Lebesgue `volume`; the function is real-valued;
the first derivative is measured in its operator norm; and both endpoints
admitted by the hypotheses, including `p = 1`, are intentional.
-/
def SobolevInequalityTarget : Prop :=
  forall (n : Nat) (p q : NNReal),
    0 < n ->
    1 <= p ->
    (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹ ->
    exists C : NNReal,
      forall u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real 1 u ->
        HasCompactSupport u ->
        eLpNorm u q volume <= C * eLpNorm (fderiv Real u) p volume

/-- Checked expansion fixes the binder order and the placement of the uniform
constant outside the function binder. -/
theorem sobolevInequalityTarget_iff_expanded :
    SobolevInequalityTarget <->
      forall (n : Nat) (p q : NNReal),
        0 < n ->
        1 <= p ->
        (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹ ->
        exists C : NNReal,
          forall u : EuclideanSpace Real (Fin n) -> Real,
            ContDiff Real 1 u ->
            HasCompactSupport u ->
            eLpNorm u q volume <= C * eLpNorm (fderiv Real u) p volume :=
  Iff.rfl

-- Separately elaborated structural mutations; none is the canonical target.
def mutationConstantDependsOnFunction : Prop :=
  forall (n : Nat) (p q : NNReal)
      (u : EuclideanSpace Real (Fin n) -> Real),
    0 < n -> 1 <= p ->
    (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹ ->
    ContDiff Real 1 u -> HasCompactSupport u ->
    exists C : NNReal,
      eLpNorm u q volume <= C * eLpNorm (fderiv Real u) p volume

def mutationRemovedCompactSupport : Prop :=
  forall (n : Nat) (p q : NNReal),
    0 < n -> 1 <= p ->
    (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹ ->
    exists C : NNReal,
      forall u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real 1 u ->
        eLpNorm u q volume <= C * eLpNorm (fderiv Real u) p volume

def mutationChangedDomainToOneDimension : Prop :=
  forall (p q : NNReal),
    1 <= p ->
    (q : Real)⁻¹ = (p : Real)⁻¹ - 1 ->
    exists C : NNReal,
      forall u : Real -> Real,
        ContDiff Real 1 u -> HasCompactSupport u ->
        eLpNorm u q volume <= C * eLpNorm (fderiv Real u) p volume

def mutationRemovedLowerExponentBound : Prop :=
  forall (n : Nat) (p q : NNReal),
    0 < n ->
    (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹ ->
    exists C : NNReal,
      forall u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real 1 u -> HasCompactSupport u ->
        eLpNorm u q volume <= C * eLpNorm (fderiv Real u) p volume

end Stage1Instances.THM_M_1245

set_option pp.explicit true in
#print Stage1Instances.THM_M_1245.SobolevInequalityTarget
