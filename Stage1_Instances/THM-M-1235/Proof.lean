import Statement

/-!
# THM-M-1235 proof-phase result

The frozen canonical target is not merely missing Wolibner's analytic proof:
its `Motion` condition fields contain propositions rather than proofs of the
conditions. Consequently the five functions are unconstrained, and the
claimed uniqueness is false. This module gives a kernel-checked refutation of
that exact target. It does not replace the target or prove Wolibner's theorem.
-/

namespace Stage1Instances.THMM1235

/-- Change one of a motion's five functions while preserving every other
field of the frozen structure. -/
def perturbVelocityX {D : SourceData} {T : Real} (S : Motion D T) : Motion D T :=
  { S with velocityX := fun p t => S.velocityX p t + 1 }

theorem perturbVelocityX_not_same {D : SourceData} {T : Real} (S : Motion D T) :
    Not (SameMotion (perturbVelocityX S) S) := by
  intro h
  have hfun := h.2.2.1
  have hvalue := congrFun (congrFun hfun (0, 0)) 0
  simp [perturbVelocityX] at hvalue

/-- Concrete source data satisfying all six explicit premises of the frozen
target. The propositions stored inside a `Motion` remain unconstrained. -/
def counterexampleData : SourceData where
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

/-- The exact canonical proposition frozen by the statement phase is false.
For any alleged unique motion, changing `velocityX` produces another `Motion`
which is not the same five-function motion. -/
theorem not_wolibnerGlobalExistenceAndUniqueness :
    Not WolibnerGlobalExistenceAndUniqueness := by
  intro h
  obtain ⟨S, hS⟩ := h counterexampleData 1 trivial trivial trivial trivial trivial trivial (by norm_num)
  exact perturbVelocityX_not_same S (hS (perturbVelocityX S))

#print axioms perturbVelocityX_not_same
#print axioms not_wolibnerGlobalExistenceAndUniqueness

end Stage1Instances.THMM1235
