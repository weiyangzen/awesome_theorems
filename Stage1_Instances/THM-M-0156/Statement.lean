import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-!
# THM-M-0156: rectangular divergence theorem statement

This module freezes the classical Euclidean divergence theorem on closed
rectangular boxes. It states the target and structural mutations; it does not
prove the target.
-/

noncomputable section

open Finset MeasureTheory Set
open scoped BigOperators

namespace Stage1Instances.THM_M_0156

/-- Positive-dimensional Euclidean coordinate space. -/
abbrev Euclidean (n : Nat) := Fin (n + 1) -> Real

/-- The trace of the Frechet derivative in the standard coordinate basis. -/
def coordinateDivergence {n : Nat}
    (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n)
    (x : Euclidean n) : Real :=
  ∑ i : Fin (n + 1), f' x (Pi.single i 1) i

/-- The coordinate model of a face perpendicular to `i`. -/
def face {n : Nat} (a b : Euclidean n) (i : Fin (n + 1)) : Set (Fin n -> Real) :=
  Icc (a ∘ i.succAbove) (b ∘ i.succAbove)

/-- Insert the upper endpoint in coordinate `i`. -/
def frontFace {n : Nat} (b : Euclidean n) (i : Fin (n + 1))
    (x : Fin n -> Real) : Euclidean n :=
  i.insertNth (b i) x

/-- Insert the lower endpoint in coordinate `i`. -/
def backFace {n : Nat} (a : Euclidean n) (i : Fin (n + 1))
    (x : Fin n -> Real) : Euclidean n :=
  i.insertNth (a i) x

/-- Outward flux through all faces of the coordinate box `[a,b]`. -/
def outwardFlux {n : Nat} (a b : Euclidean n) (f : Euclidean n -> Euclidean n) : Real :=
  ∑ i : Fin (n + 1),
    ((∫ x in face a b i, f (frontFace b i x) i) -
      ∫ x in face a b i, f (backFace a i x) i)

/--
The exact box-scoped divergence target selected from the repository's
family-level claim: the volume integral of divergence equals outward flux.
The derivative is required at every interior point; no exceptional set is
included in this canonical statement.
-/
def DivergenceTheoremTarget : Prop :=
  forall (n : Nat) (a b : Euclidean n),
    a <= b ->
    forall (f : Euclidean n -> Euclidean n)
      (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n),
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

/-- Binder-explicit form used to check the canonical declaration. -/
def ExpandedDivergenceTheoremTarget : Prop :=
  forall (n : Nat), forall (a b : Euclidean n),
    a <= b ->
    forall (f : Euclidean n -> Euclidean n),
    forall (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n),
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

/-- Checked transport to the binder-explicit encoding. -/
theorem target_iff_expanded :
    DivergenceTheoremTarget <-> ExpandedDivergenceTheoremTarget := by
  rfl

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedContinuity : Prop :=
  forall (n : Nat) (a b : Euclidean n),
    a <= b ->
    forall (f : Euclidean n -> Euclidean n)
      (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n),
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

def mutationChangedDomainToThreeSpace : Prop :=
  forall (a b : Euclidean 2),
    a <= b ->
    forall (f : Euclidean 2 -> Euclidean 2)
      (f' : Euclidean 2 -> Euclidean 2 →L[Real] Euclidean 2),
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

def mutationChangedBinderScope : Prop :=
  forall (n : Nat), exists a b : Euclidean n,
    a <= b /\
    forall (f : Euclidean n -> Euclidean n)
      (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n),
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

/-- This mutation excludes boxes with a zero-width coordinate. -/
def mutationExcludesDegenerateBoxes : Prop :=
  forall (n : Nat) (a b : Euclidean n),
    (forall i, a i < b i) ->
    forall (f : Euclidean n -> Euclidean n)
      (f' : Euclidean n -> Euclidean n →L[Real] Euclidean n),
      ContinuousOn f (Icc a b) ->
      (forall x, x ∈ Set.pi univ (fun i => Ioo (a i) (b i)) -> HasFDerivAt f (f' x) x) ->
      IntegrableOn (coordinateDivergence f') (Icc a b) ->
      (∫ x in Icc a b, coordinateDivergence f' x) = outwardFlux a b f

end Stage1Instances.THM_M_0156

set_option pp.explicit true in
#print Stage1Instances.THM_M_0156.DivergenceTheoremTarget
