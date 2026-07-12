import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
# THM-M-0156 immutable anchor check

This file independently restates the frozen rectangular target and checks the
adapter to the pinned mathlib theorem. It is candidate-audit evidence, not the
accepted proof artifact for the later proof phase.
-/

noncomputable section

open Finset MeasureTheory Set
open scoped BigOperators

namespace Stage1Instances.THM_M_0156.AnchorAudit

abbrev Euclidean (n : Nat) := Fin (n + 1) -> Real

def coordinateDivergence {n : Nat}
    (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n)
    (x : Euclidean n) : Real :=
  ∑ i : Fin (n + 1), f' x (Pi.single i 1) i

def face {n : Nat} (a b : Euclidean n) (i : Fin (n + 1)) : Set (Fin n -> Real) :=
  Icc (a ∘ i.succAbove) (b ∘ i.succAbove)

def frontFace {n : Nat} (b : Euclidean n) (i : Fin (n + 1))
    (x : Fin n -> Real) : Euclidean n :=
  i.insertNth (b i) x

def backFace {n : Nat} (a : Euclidean n) (i : Fin (n + 1))
    (x : Fin n -> Real) : Euclidean n :=
  i.insertNth (a i) x

def outwardFlux {n : Nat} (a b : Euclidean n) (f : Euclidean n -> Euclidean n) : Real :=
  ∑ i : Fin (n + 1),
    ((∫ x in face a b i, f (frontFace b i x) i) -
      ∫ x in face a b i, f (backFace a i x) i)

def DivergenceTheoremTarget : Prop :=
  forall (n : Nat) (a b : Euclidean n),
    a <= b ->
    forall (f : Euclidean n -> Euclidean n)
      (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n),
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

/-- Exact adapter from the pinned mathlib theorem, with an empty exceptional set. -/
theorem canonicalTarget_mathlib_candidate : DivergenceTheoremTarget := by
  intro n a b hab f f' hcont hderiv hint
  exact MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable
    a b hab f f' ∅ Set.countable_empty hcont (fun x hx => hderiv x hx.1) hint

end Stage1Instances.THM_M_0156.AnchorAudit

#print axioms Stage1Instances.THM_M_0156.AnchorAudit.canonicalTarget_mathlib_candidate
