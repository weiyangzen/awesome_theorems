import ObligationTree

/-!
Kernel-checked diagnostic for the frozen `EquationAndTraceClosurePackage`.

That package quantifies over every structurally admissible `CandidateFields`,
including the identically-zero fields.  Its trace conclusion would therefore
force every admissible initial-vorticity test pairing to be zero.  This exposes
the over-quantification in the frozen proof architecture; it is not a proof of
the canonical Yudovich statement.
-/

noncomputable section

open MeasureTheory

namespace Stage1Rev56.THMM1234

/-- Identically-zero fields satisfy the deliberately weak candidate interface. -/
def zeroCandidateFields
    (u0 : StaticVelocity) (omega0 : StaticVorticity) : CandidateFields u0 omega0 where
  velocity := 0
  vorticity := 0
  velocityMeasurable := fun _ _ => aestronglyMeasurable_zero
  vorticityMeasurable := fun _ _ => aestronglyMeasurable_zero
  finiteEnergy := fun _ _ => MemLp.zero
  boundedVorticity := fun _ _ => MemLp.zero
  divergenceFree := by
    intro _ _ psi _
    simp
  vorticityIsCurl := by
    intro _ _ psi _
    simp

/-- The same zero candidate makes the frozen closure package erase every
admissible initial-velocity pairing against a divergence-free test. -/
theorem initialVelocityPairing_eq_zero_of_equationAndTraceClosure
    (close : EquationAndTraceClosurePackage)
    (u0 : StaticVelocity) (omega0 : StaticVorticity)
    (hdata : InitialData u0 omega0)
    (phi : Real -> Plane -> Plane)
    (hphi : SmoothCompactSpacetimeVectorTest phi)
    (hdiv : DivergenceFreeTest phi) :
    integral volume (fun x => dot (u0 x) (phi 0 x)) = 0 := by
  let c : CandidateFields u0 omega0 := zeroCandidateFields u0 omega0
  have hmomentum := (close u0 omega0 hdata c).1 phi hphi hdiv
  simpa [c, zeroCandidateFields] using hmomentum

/-- The frozen closure package collapses every admissible initial-vorticity
pairing against a smooth compactly supported test to zero. -/
theorem initialVorticityPairing_eq_zero_of_equationAndTraceClosure
    (close : EquationAndTraceClosurePackage)
    (u0 : StaticVelocity) (omega0 : StaticVorticity)
    (hdata : InitialData u0 omega0)
    (psi : Plane -> Real) (hpsi : SmoothCompactScalarTest psi) :
    integral volume (fun x => omega0 x * psi x) = 0 := by
  let c : CandidateFields u0 omega0 := zeroCandidateFields u0 omega0
  have htrace := (close u0 omega0 hdata c).2 psi hpsi
  have hzero : Filter.Tendsto
      (fun _ : Real => (0 : Real))
      (nhdsWithin 0 (Set.Ioi 0))
      (nhds 0) := tendsto_const_nhds
  have htraceZero : Filter.Tendsto
      (fun t => integral volume (fun x => c.vorticity t x * psi x))
      (nhdsWithin 0 (Set.Ioi 0))
      (nhds 0) := by
    simp [c, zeroCandidateFields]
  exact tendsto_nhds_unique htrace htraceZero

#print axioms initialVorticityPairing_eq_zero_of_equationAndTraceClosure
#print axioms initialVelocityPairing_eq_zero_of_equationAndTraceClosure

end Stage1Rev56.THMM1234
