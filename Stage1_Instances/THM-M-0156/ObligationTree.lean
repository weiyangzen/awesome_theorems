import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
# THM-M-0156 obligation-tree composition check

This module checks only the typed empty-exception adapter selected by the
frozen architecture. The external theorem remains an explicit premise, so
this file does not claim the proof-phase or root closure.
-/

noncomputable section

open Finset MeasureTheory Set
open scoped BigOperators

namespace Stage1Instances.THM_M_0156.ObligationTree

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

/-- Exact interface of the stronger off-countable theorem used by the adapter. -/
def OffCountablePackage : Prop :=
  forall (n : Nat) (a b : Euclidean n),
    a <= b ->
    forall (f : Euclidean n -> Euclidean n)
      (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n)
      (s : Set (Euclidean n)),
      s.Countable ->
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) ∩ sᶜ ->
        HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

/-- The separately named boundary leaf used in the empty-exception adapter. -/
theorem empty_exception_is_countable {n : Nat} :
    (∅ : Set (Euclidean n)).Countable :=
  Set.countable_empty

/-- Checked conditional child-to-parent composition; it does not supply `candidate`. -/
theorem root_of_offCountablePackage
    (candidate : OffCountablePackage) : DivergenceTheoremTarget := by
  intro n a b hab f f' hcont hderiv hint
  exact candidate n a b hab f f' ∅ empty_exception_is_countable hcont
    (fun x hx => hderiv x hx.1) hint

#print axioms empty_exception_is_countable
#print axioms root_of_offCountablePackage

end Stage1Instances.THM_M_0156.ObligationTree
