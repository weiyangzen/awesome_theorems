import Statement

/-!
# THM-M-1235 independent proof-phase refutation

This module independently checks the blocker in `Proof.lean` by perturbing a
different field of the frozen `Motion` structure. It refutes only the frozen
formal encoding, not Wolibner's mathematical theorem.
-/

namespace Stage1Instances.THMM1235

def perturbPressure {D : SourceData} {T : Real} (S : Motion D T) : Motion D T :=
  { S with pressure := fun p t => S.pressure p t + 1 }

theorem perturbPressure_not_same {D : SourceData} {T : Real} (S : Motion D T) :
    Not (SameMotion (perturbPressure S) S) := by
  intro h
  have hvalue := congrFun (congrFun h.2.2.2.2 (0, 0)) 0
  simp [perturbPressure] at hvalue

/-- Source data satisfying every explicit premise in the frozen target. -/
def counterexampleDataForIndependentRefutation : SourceData where
  domain := {
    carrier := Set.univ
    boundaryComponentCount := 0
    boundaryIsFiniteUnionOfClosedAnalyticCurves := True
    isClosedPlanarRegion := True
    containsInfinity := false
  }
  density := 1
  density_pos := by norm_num
  vorticity := 0
  potential := 0
  pressureAtBasePoint := 0
  vorticityLebesgueIntegrableOnDomain := True
  vorticityHasSourceDecay := True
  vorticityIsHolderContinuous := True
  initialCirculationOnEveryInteriorBoundaryComponentIsZero := True

/-- A second kernel-checked negation of the exact frozen target. Unlike the
tracked witness in `Proof.lean`, this one changes `pressure`. -/
theorem independently_not_wolibnerGlobalExistenceAndUniqueness :
    Not WolibnerGlobalExistenceAndUniqueness := by
  intro h
  obtain ⟨S, hS⟩ := h counterexampleDataForIndependentRefutation 1
    trivial trivial trivial trivial trivial trivial (by norm_num)
  exact perturbPressure_not_same S (hS (perturbPressure S))

#print axioms perturbPressure_not_same
#print axioms independently_not_wolibnerGlobalExistenceAndUniqueness

end Stage1Instances.THMM1235
