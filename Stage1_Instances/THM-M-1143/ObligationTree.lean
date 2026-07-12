import Statement

/-!
# THM-M-1143 conditional obligation composition

This module checks only the interfaces and final composition selected by the frozen obligation
registry.  The two package parameters are intentionally explicit: neither is implemented here.
-/

open Bornology Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1143

/-- Analytic package: global bounded harmonicity forces the Frechet derivative to vanish. -/
def VanishingDerivativePackage : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n -> HarmonicOnNhd f univ -> IsBounded (range f) ->
    forall x, HasFDerivAt f (0 : Space n →L[ℝ] ℝ) x

/-- Calculus package: a differentiable real function with zero derivative is constant. -/
def ZeroDerivativeConstantPackage : Prop :=
  forall (n : Nat) (f : Space n -> Real),
    0 < n ->
    (forall x, HasFDerivAt f (0 : Space n →L[ℝ] ℝ) x) ->
    forall x y, f x = f y

/-- Checked composition of the two explicitly open packages into the exact frozen target. -/
theorem root_of_vanishingDerivative_packages
    (hvanish : VanishingDerivativePackage)
    (hconstant : ZeroDerivativeConstantPackage) :
    BoundedHarmonicIsConstant := by
  intro n f hn hh hb x y
  exact hconstant n f hn (hvanish n f hn hh hb) x y

end Stage1Instances.THM_M_1143

#check Stage1Instances.THM_M_1143.root_of_vanishingDerivative_packages
#print axioms Stage1Instances.THM_M_1143.root_of_vanishingDerivative_packages
