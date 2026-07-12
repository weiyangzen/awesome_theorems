import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic

/-!
# THM-M-1241: Nirenberg's Gagliardo-Nirenberg interpolation inequality

This is the statement boundary only.  It formalizes formulae (2.2)--(2.3)
on page 125 of Nirenberg's 1959 paper, including both exceptional cases.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1241

abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/-- The convention `1 / infinity = 0` used in the source's exponent equation. -/
def reciprocalExponent (p : ENNReal) : Real :=
  if p = (⊤ : ENNReal) then 0 else (p.toReal)⁻¹

/-- A coordinate vector in the standard orthonormal basis of `Real^n`. -/
def coordinateVector {n : Nat} (i : Fin n) : Space n :=
  EuclideanSpace.single i 1

/-- The ordered coordinate partial derivative selected by `directions`.
For order zero this definition is definitionally the original function. -/
def coordinateDerivative {n k : Nat} (u : Space n -> Real)
    (directions : Fin k -> Fin n) (x : Space n) : Real :=
  iteratedFDeriv Real k u x (fun i => coordinateVector (directions i))

/-- Nirenberg's `|D^k u|_p`: the maximum of the `L^p` norms of all
coordinate derivatives of order `k`. -/
def derivativeLpNorm {n : Nat} (k : Nat) (p : ENNReal)
    (u : Space n -> Real) : ENNReal :=
  Finset.univ.sup fun directions : Fin k -> Fin n =>
    eLpNorm (coordinateDerivative u directions) p volume

/-- The exceptional hypothesis on `u` when `j = 0`, `r*m < n`, and
`q = infinity`: either decay at infinity, or membership in some finite
positive `L^qTilde`. -/
def ZeroOrderExceptionalHypothesis {n : Nat} (u : Space n -> Real) : Prop :=
  Tendsto u (cocompact (Space n)) (nhds 0) ∨
    ∃ qTilde : ENNReal, 0 < qTilde ∧ qTilde < (⊤ : ENNReal) ∧
      eLpNorm u qTilde volume < (⊤ : ENNReal)

/-- Formulae (2.2)--(2.3), with exactly the parameter range and exceptional
cases printed in Nirenberg, *On elliptic partial differential equations*,
Ann. Scuola Norm. Sup. Pisa (3) 13 (1959), Lecture II, p. 125.

The formal surface uses `C^m` real functions, standard coordinate partial
derivatives, Lebesgue measure, and extended-real `L^p` seminorms.  This fixes
the classical-derivative reading of the source statement; no proof is
asserted here. -/
def GagliardoNirenbergTarget : Prop :=
  forall (n m j : Nat) (q r p : ENNReal) (a : Real),
    0 < n -> j < m -> 1 <= q -> 1 <= r ->
    reciprocalExponent p =
      (j : Real) / n + a * (reciprocalExponent r - (m : Real) / n) +
        (1 - a) * reciprocalExponent q ->
    (j : Real) / m <= a -> a <= 1 ->
    ((1 < r ∧ r < (⊤ : ENNReal) ∧
      ∃ z : Int, 0 <= z ∧ (m : Real) - j - n * reciprocalExponent r = z) -> a < 1) ->
    exists C : NNReal,
      forall u : Space n -> Real,
        ContDiff Real m u ->
        derivativeLpNorm 0 q u < (⊤ : ENNReal) ->
        derivativeLpNorm m r u < (⊤ : ENNReal) ->
        (j = 0 ∧ r < (⊤ : ENNReal) ∧ (r.toReal * m < n) ∧ q = (⊤ : ENNReal) ->
          ZeroOrderExceptionalHypothesis u) ->
        derivativeLpNorm j p u <=
          C * (derivativeLpNorm m r u) ^ a *
            (derivativeLpNorm 0 q u) ^ (1 - a)

theorem gagliardoNirenbergTarget_iff_expanded :
    GagliardoNirenbergTarget <-> GagliardoNirenbergTarget := Iff.rfl

-- Structural mutations are elaborated separately and fingerprinted by the
-- statement validator; none is credited as an alternate target.
def mutationRemovedLowerParameterBound : Prop :=
  forall (n m j : Nat) (q r p : ENNReal) (a : Real),
    0 < n -> j < m -> 1 <= q -> 1 <= r ->
    reciprocalExponent p =
      (j : Real) / n + a * (reciprocalExponent r - (m : Real) / n) +
        (1 - a) * reciprocalExponent q ->
    a <= 1 -> exists C : NNReal, forall u : Space n -> Real,
      ContDiff Real m u -> derivativeLpNorm 0 q u < (⊤ : ENNReal) ->
      derivativeLpNorm m r u < (⊤ : ENNReal) ->
      derivativeLpNorm j p u <= C * (derivativeLpNorm m r u) ^ a *
        (derivativeLpNorm 0 q u) ^ (1 - a)

def mutationChangedDomainToLine : Prop :=
  forall (m j : Nat) (_q r p : ENNReal) (a : Real),
    j < m -> exists C : NNReal, forall u : Real -> Real,
      ContDiff Real m u ->
      eLpNorm u p volume <= C * (eLpNorm (iteratedFDeriv Real m u) r volume) ^ a

def mutationConstantDependsOnFunction : Prop :=
  forall (n m j : Nat) (q r p : ENNReal) (a : Real) (u : Space n -> Real),
    exists C : NNReal, derivativeLpNorm j p u <=
      C * (derivativeLpNorm m r u) ^ a * (derivativeLpNorm 0 q u) ^ (1 - a)

def mutationRemovedExceptionalCases : Prop :=
  forall (n m j : Nat) (q r p : ENNReal) (a : Real),
    0 < n -> j < m -> 1 <= q -> 1 <= r ->
    reciprocalExponent p =
      (j : Real) / n + a * (reciprocalExponent r - (m : Real) / n) +
        (1 - a) * reciprocalExponent q ->
    (j : Real) / m <= a -> a <= 1 ->
    exists C : NNReal, forall u : Space n -> Real,
      ContDiff Real m u -> derivativeLpNorm 0 q u < (⊤ : ENNReal) ->
      derivativeLpNorm m r u < (⊤ : ENNReal) -> derivativeLpNorm j p u <=
        C * (derivativeLpNorm m r u) ^ a *
          (derivativeLpNorm 0 q u) ^ (1 - a)

end Stage1Instances.THM_M_1241

set_option pp.explicit true in
#print Stage1Instances.THM_M_1241.GagliardoNirenbergTarget
