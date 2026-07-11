import Mathlib.Data.Real.Basic

/-!
# THM-M-1228: Caffarelli-Kohn-Nirenberg statement boundary

The pinned library has no native suitable-weak-solution, regular-point, or
parabolic Hausdorff-measure API. This file therefore makes those three source
notions explicit parameters of the statement interface. It does not replace
parabolic measure by the Euclidean Hausdorff measure and contains no proof of
partial regularity.
-/

namespace Stage1Instances.THMM1228

/-- Three-dimensional space-time used in the CKN theorem. -/
abbrev SpaceTime : Type := (Fin 3 -> Real) × Real

/-- Velocity values for a three-dimensional incompressible flow. -/
abbrev Velocity : Type := Fin 3 -> Real

/-- Concrete fields on which the source notions of suitability and regularity
are evaluated. The exact distributional and integrability clauses belong to
`IsSuitableWeakSolution`, rather than being weakened into pointwise equations. -/
structure SolutionData where
  domain : Set SpaceTime
  velocity : SpaceTime -> Velocity
  pressure : SpaceTime -> Real
  force : SpaceTime -> Velocity

/-- Source-level semantic interface needed because the corresponding analytic
objects are absent from the pinned mathlib snapshot. None of these predicates
contains a witness or proof of the CKN conclusion. -/
structure CKNSourceSemantics where
  IsSuitableWeakSolution : SolutionData -> Prop
  RegularAt : SolutionData -> SpaceTime -> Prop
  ParabolicHausdorffOneMeasureZero : Set SpaceTime -> Prop

/-- Singular points are domain points that are not regular in the source sense. -/
def SingularSet (S : CKNSourceSemantics) (D : SolutionData) : Set SpaceTime :=
  {z | z ∈ D.domain ∧ ¬ S.RegularAt D z}

/-- Exact logical root selected at intake: the singular set of every suitable
weak solution of the three-dimensional incompressible Navier-Stokes equations
has zero one-dimensional parabolic Hausdorff measure. -/
def CaffarelliKohnNirenbergTarget (S : CKNSourceSemantics) : Prop :=
  ∀ D : SolutionData,
    S.IsSuitableWeakSolution D ->
      S.ParabolicHausdorffOneMeasureZero (SingularSet S D)

/-- Checked expansion fixing the binder order and the singular-set definition. -/
theorem caffarelliKohnNirenbergTarget_iff_expanded (S : CKNSourceSemantics) :
    CaffarelliKohnNirenbergTarget S <->
      ∀ D : SolutionData,
        S.IsSuitableWeakSolution D ->
          S.ParabolicHausdorffOneMeasureZero
            {z | z ∈ D.domain ∧ ¬ S.RegularAt D z} :=
  Iff.rfl

-- Separately elaborated structural mutations; none receives equivalence credit.
def MutationRemovedSuitability (S : CKNSourceSemantics) : Prop :=
  ∀ D : SolutionData,
    S.ParabolicHausdorffOneMeasureZero (SingularSet S D)

abbrev TwoDimensionalSpaceTime : Type := (Fin 2 -> Real) × Real

def MutationChangedSpatialDimension
    (IsSuitable : (Set TwoDimensionalSpaceTime) -> Prop)
    (Regular : TwoDimensionalSpaceTime -> Prop)
    (ParabolicMeasureZero : Set TwoDimensionalSpaceTime -> Prop) : Prop :=
  ∀ domain : Set TwoDimensionalSpaceTime,
    IsSuitable domain ->
      ParabolicMeasureZero {z | z ∈ domain ∧ ¬ Regular z}

def MutationChangedBinderScope (S : CKNSourceSemantics) : Prop :=
  ∀ z : SpaceTime, ∀ D : SolutionData,
    S.IsSuitableWeakSolution D -> z ∈ D.domain ->
      ¬ S.RegularAt D z ->
        S.ParabolicHausdorffOneMeasureZero (SingularSet S D)

def MutationRegularEverywhere (S : CKNSourceSemantics) : Prop :=
  ∀ D : SolutionData,
    S.IsSuitableWeakSolution D ->
      ∀ z ∈ D.domain, S.RegularAt D z

end Stage1Instances.THMM1228

set_option pp.explicit true in
#print Stage1Instances.THMM1228.CaffarelliKohnNirenbergTarget
