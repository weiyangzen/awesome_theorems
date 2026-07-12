import Statement

/-!
# THM-M-1289 conditional composition interface

This file checks only that the frozen analytic components compose to the exact
public target. It deliberately supplies none of those analytic components.
-/

namespace Stage1Instances.THM_M_1289

open scoped ENNReal RealInnerProductSpace
open MeasureTheory

def PositivityComponent : Prop :=
  forall (n : Nat), 3 <= n -> forall (a : Euclidean n) (lambda : Real),
    0 < lambda -> forall x, 0 < bubble n a lambda x

def SmoothnessComponent : Prop :=
  forall (n : Nat), 3 <= n -> forall (a : Euclidean n) (lambda : Real),
    0 < lambda -> ContDiff Real ⊤ (bubble n a lambda)

def PDEComponent : Prop :=
  forall (n : Nat), 3 <= n -> forall (a : Euclidean n) (lambda : Real),
    0 < lambda -> forall x,
      -Laplacian.laplacian (bubble n a lambda) x =
        Real.rpow (bubble n a lambda x) (((n : Real) + 2) / ((n : Real) - 2))

def FunctionNormComponent : Prop :=
  forall (n : Nat), 3 <= n -> forall (a : Euclidean n) (lambda : Real),
    0 < lambda ->
      eLpNorm (bubble n a lambda) (criticalExponent n)
        (volume : Measure (Euclidean n)) < ⊤

def GradientNormComponent : Prop :=
  forall (n : Nat), 3 <= n -> forall (a : Euclidean n) (lambda : Real),
    0 < lambda -> gradientNorm (bubble n a lambda) < ⊤

def ExtremalComponent : Prop :=
  forall (n : Nat), 3 <= n -> forall (a : Euclidean n) (lambda : Real),
    0 < lambda -> exists C : Real, IsSharpSobolevConstant n C /\
      eLpNorm (bubble n a lambda) (criticalExponent n)
          (volume : Measure (Euclidean n)) =
        ENNReal.ofReal C * gradientNorm (bubble n a lambda)

/-- Checked child-to-root composition. The six premises are intentionally
abstract: this is an architecture certificate, not a proof of any component. -/
theorem aubinTalentiTarget_of_components
    (hpos : PositivityComponent) (hsmooth : SmoothnessComponent)
    (hpde : PDEComponent) (hfun : FunctionNormComponent)
    (hgrad : GradientNormComponent) (hext : ExtremalComponent) :
    AubinTalentiTarget := by
  intro n hn a lambda hl
  exact ⟨hpos n hn a lambda hl, hsmooth n hn a lambda hl,
    hpde n hn a lambda hl, hfun n hn a lambda hl,
    hgrad n hn a lambda hl, hext n hn a lambda hl⟩

#print axioms aubinTalentiTarget_of_components

end Stage1Instances.THM_M_1289
