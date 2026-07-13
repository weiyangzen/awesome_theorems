import ObligationTree

/-!
Proof-phase analysis of the frozen construction interface for `THM-M-1234`.

`CandidateFields` asks only for time-indexed copies of the structural initial-data
properties.  Constant-in-time initial fields therefore inhabit that interface
without an Euler approximation or compactness argument.  This is a genuine proof
of the formal package type and exposes a mismatch in the frozen graph: the exact
formal target at `M1234-A-STRUCTURE` is much weaker than its approximation,
estimate, and compactness children.  Those semantic children are not claimed
closed here.
-/

noncomputable section

open MeasureTheory

namespace Stage1Rev56.THMM1234

/-- Regard admissible initial data as constant-in-time candidate fields. -/
def initialCandidateFields
    (u0 : StaticVelocity) (omega0 : StaticVorticity)
    (hdata : InitialData u0 omega0) : CandidateFields u0 omega0 where
  velocity := fun _ => u0
  vorticity := fun _ => omega0
  velocityMeasurable := fun _ _ => hdata.velocityMeasurable
  vorticityMeasurable := fun _ _ => hdata.vorticityMeasurable
  finiteEnergy := fun _ _ => hdata.finiteEnergy
  boundedVorticity := fun _ _ => hdata.boundedVorticity
  divergenceFree := fun _ _ => hdata.divergenceFree
  vorticityIsCurl := fun _ _ => hdata.vorticityIsCurl

/-- The exact frozen construction-package interface has a local proof body. -/
theorem candidateConstructionPackage_from_initialData :
    CandidateConstructionPackage := by
  intro u0 omega0 hdata
  exact Nonempty.intro (initialCandidateFields u0 omega0 hdata)

/-- The constant candidate has the required one-sided initial-vorticity trace. -/
theorem initialCandidateFields_trace
    (u0 : StaticVelocity) (omega0 : StaticVorticity)
    (hdata : InitialData u0 omega0) :
    forall psi : Plane -> Real, SmoothCompactScalarTest psi ->
      Filter.Tendsto
        (fun t => integral volume (fun x =>
          (initialCandidateFields u0 omega0 hdata).vorticity t x * psi x))
        (nhdsWithin 0 (Set.Ioi 0))
        (nhds (integral volume (fun x => omega0 x * psi x))) := by
  intro psi _
  simpa [initialCandidateFields] using
    (tendsto_const_nhds :
      Filter.Tendsto
        (fun _ : Real => integral volume (fun x => omega0 x * psi x))
        (nhdsWithin 0 (Set.Ioi 0))
        (nhds (integral volume (fun x => omega0 x * psi x))))

/-- With construction installed, the frozen composition reduces the root to
the still-open equation-and-trace package. -/
theorem root_of_equationAndTraceClosure
    (close : EquationAndTraceClosurePackage) : Statement :=
  root_of_construction_and_closure
    candidateConstructionPackage_from_initialData close

#print axioms candidateConstructionPackage_from_initialData
#print axioms initialCandidateFields_trace
#print axioms root_of_equationAndTraceClosure

end Stage1Rev56.THMM1234
