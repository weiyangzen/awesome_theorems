import Mathlib.MeasureTheory.Integral.Bochner.Basic

open scoped BigOperators
open MeasureTheory

namespace AwesomeTheorems.Stage1.THM_M_1021

/-- The finite-family positive-definiteness condition used by the probability
form of Bochner's theorem.  The existential real witnesses both reality and
nonnegativity of the complex quadratic sum. -/
def IsPositiveDefinite (phi : Real -> Complex) : Prop :=
  forall (n : Nat) (t : Fin n -> Real) (c : Fin n -> Complex),
    exists r : Real, 0 <= r /\
      (Finset.univ.sum fun j => Finset.univ.sum fun k =>
        c j * star (c k) * phi (t j - t k)) = (r : Complex)

/-- The characteristic function convention fixed for this target uses
`exp (i * s * x)` and an explicitly normalized Borel measure on `Real`. -/
def IsCharacteristicFunction (phi : Real -> Complex) : Prop :=
  exists mu : Measure Real, IsProbabilityMeasure mu /\
    forall s : Real,
      phi s = integral mu (fun x : Real =>
        Complex.exp (Complex.I * (s : Complex) * (x : Complex)))

/-- Exact canonical Lean target for THM-M-1021 (Bochner's theorem on `Real`). -/
def BochnerTarget (phi : Real -> Complex) : Prop :=
  IsCharacteristicFunction phi <->
    Continuous phi /\ phi 0 = 1 /\ IsPositiveDefinite phi

#check BochnerTarget
#check (BochnerTarget : (Real -> Complex) -> Prop)

end AwesomeTheorems.Stage1.THM_M_1021
