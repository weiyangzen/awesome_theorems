import Statement

/-!
# THM-M-0406 proof-phase countermodel

The frozen canonical proposition cannot have a proof body: its abstract
`SurfaceData` interface allows an empty curve type while its hypotheses do not
require a curve to exist.  The definitions below give a concrete model of all
canonical hypotheses and a kernel-checked proof that the conclusion is false.
-/

set_option autoImplicit false

noncomputable section

open AlgebraicGeometry

namespace Stage1Instances.THMM0406

/-- A model of the abstract surface interface whose curve type is empty. -/
def proofPhaseCounterexampleSurface : SurfaceData.{0} where
  projectiveSurface := Spec (.of ℚ)
  affineOpen := Spec (.of ℚ)
  boundaryDivisor := Fin 4
  point := Unit
  curve := Empty
  isGeometricallyIrreducibleNonsingularSurface := True
  isAffineOpenInProjectiveSurface := True
  boundaryComponents := Finset.univ
  boundaryIsProjectiveComplement := True
  isDistinctIrreducibleBoundaryComponent := fun _ => True
  threeSharePoint := fun _ _ _ => False
  intersectionNumber := fun _ _ => 1
  isCurveOnAffineOpen := fun _ => True
  isProperCurve := fun _ => True
  pointLiesOnCurve := fun _ _ => True

/-- Point data satisfying the finite-place side condition. -/
def proofPhaseCounterexamplePoints :
    IntegralPointData (k := ℚ) proofPhaseCounterexampleSurface where
  S := ∅
  S_finite := Set.finite_empty
  isKRationalPoint := fun _ => True
  isSIntegralPoint := fun _ => True

/-- All boundary hypotheses hold with four components and unit intersections. -/
theorem proofPhaseCounterexampleBoundary :
    HasTheoremOneBoundary proofPhaseCounterexampleSurface (fun _ => 1) 1 := by
  simp [HasTheoremOneBoundary, proofPhaseCounterexampleSurface]

/--
The exact frozen target is refuted by the model above.  This is blocker
evidence, not a replacement theorem and not proof credit for the target.
-/
theorem not_corvajaZannierTheoremOne :
    ¬ CorvajaZannierTheoremOne.{0, 0} (k := ℚ) := by
  intro h
  obtain ⟨C, _⟩ :=
    h proofPhaseCounterexampleSurface proofPhaseCounterexamplePoints trivial
      trivial trivial (fun _ => 1) 1 proofPhaseCounterexampleBoundary
  exact Empty.elim C

#print axioms proofPhaseCounterexampleBoundary
#print axioms not_corvajaZannierTheoremOne

end Stage1Instances.THMM0406
