import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0349: exact periodic conjugate-function statement

This module freezes the strong `L^p` boundedness claim on the unit additive
circle. It defines conjugacy by the classical Fourier multiplier and contains
no proof of the boundedness theorem.
-/

namespace Stage1Instances.THM_M_0349

open MeasureTheory

abbrev Circle := AddCircle (1 : Real)

/-- The multiplier for the periodic conjugate function: `-i * sign(n)`, with
the constant Fourier mode sent to zero. -/
def conjugateMultiplier (n : Int) : Complex :=
  if n < 0 then Complex.I else if 0 < n then -Complex.I else 0

/-- `g` is a conjugate function of `f` when its Fourier coefficients are
obtained using the classical conjugate-function multiplier. -/
def AreConjugate (f g : Circle -> Complex) : Prop :=
  forall n : Int, fourierCoeff g n = conjugateMultiplier n * fourierCoeff f n

/-- Marcel Riesz's periodic conjugate-function theorem, in strong-type form
for complex-valued functions on the unit circle with its Haar measure. -/
def ConjugateFunctionTheoremTarget : Prop :=
  forall p : ENNReal, 1 < p -> p != (⊤ : ENNReal) ->
    exists C : Real, 0 <= C /\
      forall f : Lp Complex p AddCircle.haarAddCircle,
        exists g : Lp Complex p AddCircle.haarAddCircle,
          AreConjugate (fun x => f x) (fun x => g x) /\ ‖g‖ <= C * ‖f‖

-- Structural mutations elaborated separately and rejected by the checker.
def mutationRemovedLowerEndpoint : Prop :=
  forall p : ENNReal, p != (⊤ : ENNReal) ->
    exists C : Real, 0 <= C /\
      forall f : Lp Complex p AddCircle.haarAddCircle,
        exists g : Lp Complex p AddCircle.haarAddCircle,
          AreConjugate (fun x => f x) (fun x => g x) /\ ‖g‖ <= C * ‖f‖

def mutationChangedDomain : Prop :=
  forall p : ENNReal, 1 < p -> p != (⊤ : ENNReal) ->
    exists C : Real, 0 <= C /\
      forall f : Lp Complex p (MeasureTheory.Measure.addHaar : Measure Real),
        exists g : Lp Complex p (MeasureTheory.Measure.addHaar : Measure Real),
          ‖g‖ <= C * ‖f‖

def mutationChangedBinderScope : Prop :=
  exists C : Real, 0 <= C /\
    forall p : ENNReal, 1 < p -> p != (⊤ : ENNReal) ->
      forall f : Lp Complex p AddCircle.haarAddCircle,
        exists g : Lp Complex p AddCircle.haarAddCircle,
          AreConjugate (fun x => f x) (fun x => g x) /\ ‖g‖ <= C * ‖f‖

def mutationIncludesUpperEndpoint : Prop :=
  forall p : ENNReal, 1 < p ->
    exists C : Real, 0 <= C /\
      forall f : Lp Complex p AddCircle.haarAddCircle,
        exists g : Lp Complex p AddCircle.haarAddCircle,
          AreConjugate (fun x => f x) (fun x => g x) /\ ‖g‖ <= C * ‖f‖

end Stage1Instances.THM_M_0349

set_option pp.explicit true in
#print Stage1Instances.THM_M_0349.ConjugateFunctionTheoremTarget
