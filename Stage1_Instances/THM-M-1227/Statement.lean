import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar

/-!
# THM-M-1227: the Leray whole-space weak-solution target

This file freezes an unforced, three-dimensional, whole-space formulation.  It only elaborates the
target; it does not assert or prove the existence theorem.
-/

open Filter MeasureTheory Set
open scoped Topology

namespace Stage1.THM_M_1227

abbrev Space := Fin 3 -> Real
abbrev Velocity := Fin 3 -> Real
abbrev Gradient := Fin 3 -> Fin 3 -> Real

private def dot (a b : Velocity) : Real :=
  ∑ i, a i * b i

private def sqNorm (a : Velocity) : Real :=
  dot a a

private def gradSqNorm (g : Gradient) : Real :=
  ∑ i, ∑ j, g i j * g i j

private noncomputable def spatialPartial (f : Space -> Real) (j : Fin 3) (x : Space) : Real :=
  fderiv Real f x (Pi.single j 1)

private noncomputable def componentSpatialPartial
    (phi : Real -> Space -> Velocity) (i j : Fin 3) (t : Real) (x : Space) : Real :=
  spatialPartial (fun y => phi t y i) j x

private noncomputable def timePartial
    (phi : Real -> Space -> Velocity) (i : Fin 3) (t : Real) (x : Space) : Real :=
  fderiv Real (fun s => phi s x i) t 1

/-- Smooth, compactly supported, solenoidal test velocities supported at nonnegative times. -/
def IsSolenoidalTest (phi : Real -> Space -> Velocity) : Prop :=
  ContDiff Real ⊤ (Function.uncurry phi) ∧
  HasCompactSupport (Function.uncurry phi) ∧
  (∀ t x, t < 0 -> phi t x = 0) ∧
  ∀ t x, ∑ i, componentSpatialPartial phi i i t x = 0

/-- `g` is the distributional spatial gradient of `u` at almost every nonnegative time. -/
def IsWeakGradient (u : Real -> Space -> Velocity) (g : Real -> Space -> Gradient) : Prop :=
  ∀ᵐ t ∂(volume.restrict (Ici (0 : Real))), ∀ i j (psi : Space -> Real),
    ContDiff Real ⊤ psi -> HasCompactSupport psi ->
      Integrable (fun x => u t x i * spatialPartial psi j x) ∧
      Integrable (fun x => g t x i j * psi x) ∧
      ∫ x, u t x i * spatialPartial psi j x = -∫ x, g t x i j * psi x

/-- The explicit Leray-Hopf conditions used by the canonical existence target below. -/
def IsLerayHopfSolution (nu : Real) (u0 : Space -> Velocity)
    (u : Real -> Space -> Velocity) (g : Real -> Space -> Gradient) : Prop :=
  IsWeakGradient u g ∧
  (∀ᵐ t ∂(volume.restrict (Ici (0 : Real))),
    Integrable (fun x => sqNorm (u t x)) ∧ Integrable (fun x => gradSqNorm (g t x))) ∧
  (∀ᵐ t ∂(volume.restrict (Ici (0 : Real))), ∀ᵐ x ∂volume,
    ∑ i, g t x i i = 0) ∧
  (∀ phi, IsSolenoidalTest phi ->
    Integrable (fun t => integral volume (fun x =>
      (-∑ i, u t x i * timePartial phi i t x) -
      (∑ i, ∑ j, u t x i * u t x j * componentSpatialPartial phi i j t x) +
      nu * (∑ i, ∑ j, g t x i j * componentSpatialPartial phi i j t x)))
      (volume.restrict (Ici (0 : Real))) ∧
    (integral (volume.restrict (Ici (0 : Real))) (fun t => integral volume (fun x =>
      (-∑ i, u t x i * timePartial phi i t x) -
      (∑ i, ∑ j, u t x i * u t x j * componentSpatialPartial phi i j t x) +
      nu * (∑ i, ∑ j, g t x i j * componentSpatialPartial phi i j t x))) =
      integral volume (fun x => dot (u0 x) (phi 0 x)))) ∧
  Tendsto (fun t => integral volume (fun x => sqNorm (u t x - u0 x)))
    (nhdsWithin 0 (Ioi 0)) (nhds 0) ∧
  ∀ t, 0 ≤ t ->
    integral volume (fun x => sqNorm (u t x)) +
      2 * nu * integral (volume.restrict (Set.Icc (0 : Real) t))
        (fun s => integral volume (fun x => gradSqNorm (g s x))) ≤
    integral volume (fun x => sqNorm (u0 x))

/--
The canonical THM-M-1227 proposition: every distributionally divergence-free finite-energy datum
on `R^3`, and every positive viscosity, admits a global unforced Leray-Hopf weak solution.
-/
def lerayHopfExistenceTarget : Prop :=
  ∀ (nu : Real) (u0 : Space -> Velocity),
    0 < nu ->
    Integrable (fun x => sqNorm (u0 x)) ->
    (∀ i (psi : Space -> Real), ContDiff Real ⊤ psi -> HasCompactSupport psi ->
      Integrable (fun x => u0 x i * spatialPartial psi i x)) ->
    (∀ psi : Space -> Real, ContDiff Real ⊤ psi -> HasCompactSupport psi ->
      integral volume (fun x => ∑ i, u0 x i * spatialPartial psi i x) = 0) ->
    ∃ (u : Real -> Space -> Velocity) (g : Real -> Space -> Gradient),
      IsLerayHopfSolution nu u0 u g

/--
Conditional composition certificate for the six semantic components of the frozen solution
predicate.  The obligation-tree phase checks only this assembly step; it does not construct `u`,
`g`, or any of the component premises.
-/
theorem isLerayHopfSolution_compose (nu : Real) (u0 : Space -> Velocity)
    (u : Real -> Space -> Velocity) (g : Real -> Space -> Gradient)
    (weakGradient : IsWeakGradient u g)
    (energyClass : ∀ᵐ t ∂(volume.restrict (Ici (0 : Real))),
      Integrable (fun x => sqNorm (u t x)) ∧ Integrable (fun x => gradSqNorm (g t x)))
    (incompressible : ∀ᵐ t ∂(volume.restrict (Ici (0 : Real))), ∀ᵐ x ∂volume,
      ∑ i, g t x i i = 0)
    (weakMomentum : ∀ phi, IsSolenoidalTest phi ->
      Integrable (fun t => integral volume (fun x =>
        (-∑ i, u t x i * timePartial phi i t x) -
        (∑ i, ∑ j, u t x i * u t x j * componentSpatialPartial phi i j t x) +
        nu * (∑ i, ∑ j, g t x i j * componentSpatialPartial phi i j t x)))
        (volume.restrict (Ici (0 : Real))) ∧
      (integral (volume.restrict (Ici (0 : Real))) (fun t => integral volume (fun x =>
        (-∑ i, u t x i * timePartial phi i t x) -
        (∑ i, ∑ j, u t x i * u t x j * componentSpatialPartial phi i j t x) +
        nu * (∑ i, ∑ j, g t x i j * componentSpatialPartial phi i j t x))) =
        integral volume (fun x => dot (u0 x) (phi 0 x))))
    (initialTrace : Tendsto (fun t => integral volume (fun x => sqNorm (u t x - u0 x)))
      (nhdsWithin 0 (Ioi 0)) (nhds 0))
    (energyInequality : ∀ t, 0 ≤ t ->
      integral volume (fun x => sqNorm (u t x)) +
        2 * nu * integral (volume.restrict (Set.Icc (0 : Real) t))
          (fun s => integral volume (fun x => gradSqNorm (g s x))) ≤
      integral volume (fun x => sqNorm (u0 x))) :
    IsLerayHopfSolution nu u0 u g :=
  ⟨weakGradient, energyClass, incompressible, weakMomentum, initialTrace, energyInequality⟩

#check lerayHopfExistenceTarget
#print axioms isLerayHopfSolution_compose

end Stage1.THM_M_1227
