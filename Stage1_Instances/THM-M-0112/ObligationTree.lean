import Statement

/-!
# THM-M-0112 conditional composition certificates

This file checks only how separate below-boundary and boundary packages compose
to the frozen root. It does not supply either mathematical package.
-/

namespace Stage1Instances.THMM0112

universe uX uY

def BelowBoundaryPackage : Prop :=
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex ->
      D.ambientProjectiveOverComplex ->
      D.sectionIsSmooth ->
      D.sectionIsHyperplaneForInclusion ->
      D.piMapIsInducedByInclusion ->
      forall k : Nat, k < D.complexDimension - 1 ->
        Function.Bijective (D.piMap k)

def BoundaryPackage : Prop :=
  forall (X : Type uX) [TopologicalSpace X]
    (Y : Type uY) [TopologicalSpace Y]
    (D : LefschetzHyperplaneData X Y),
      D.ambientSmoothOverComplex ->
      D.ambientProjectiveOverComplex ->
      D.sectionIsSmooth ->
      D.sectionIsHyperplaneForInclusion ->
      D.piMapIsInducedByInclusion ->
      Function.Surjective (D.piMap (D.complexDimension - 1))

/-- Exact checked recomposition. Both substantive packages remain premises. -/
theorem weakTopologicalLefschetz_of_packages
    (below : BelowBoundaryPackage.{uX, uY})
    (boundary : BoundaryPackage.{uX, uY}) :
    WeakTopologicalLefschetzTarget.{uX, uY} := by
  intro X _ Y _ D hsmooth hprojective hsection hhyperplane hinduced
  exact
    ⟨below X Y D hsmooth hprojective hsection hhyperplane hinduced,
      boundary X Y D hsmooth hprojective hsection hhyperplane hinduced⟩

#print axioms weakTopologicalLefschetz_of_packages

end Stage1Instances.THMM0112
