import Statement

/-!
Proof work for the exact `THM-M-1234` interface.

This module closes the degenerate zero-data boundary case.  It deliberately
does not declare the canonical `Statement`: arbitrary admissible initial data
still requires the approximation and equation-closure packages frozen in the
obligation registry.
-/

noncomputable section

open MeasureTheory

namespace Stage1Rev56.THMM1234

theorem zero_initial_data : InitialData (0 : StaticVelocity) (0 : StaticVorticity) := by
  refine {
    velocityMeasurable := aestronglyMeasurable_zero
    vorticityMeasurable := aestronglyMeasurable_zero
    finiteEnergy := MemLp.zero
    boundedVorticity := MemLp.zero
    divergenceFree := ?_
    vorticityIsCurl := ?_
  }
  · intro ψ _
    simp
  · intro ψ _
    simp

private lemma zero_momentum :
    WeakMomentumEquation (0 : StaticVelocity) (0 : Velocity) := by
  intro φ _ _
  simp [dot]

theorem zero_data_solution :
    Nonempty (GlobalWeakSolution (0 : StaticVelocity) (0 : StaticVorticity)) := by
  refine ⟨{
    velocity := 0
    vorticity := 0
    velocityMeasurable := ?_
    vorticityMeasurable := ?_
    finiteEnergy := ?_
    boundedVorticity := ?_
    divergenceFree := ?_
    vorticityIsCurl := ?_
    momentumEquation := zero_momentum
    initialVorticityTrace := ?_
  }⟩
  · intro t _
    simpa using
      (aestronglyMeasurable_zero : AEStronglyMeasurable (fun _ : Plane => (0 : Plane)) volume)
  · intro t _
    simpa using
      (aestronglyMeasurable_zero : AEStronglyMeasurable (fun _ : Plane => (0 : ℝ)) volume)
  · intro t _
    exact MemLp.zero
  · intro t _
    exact MemLp.zero
  · intro t _ ψ _
    simp
  · intro t _ ψ _
    simp
  · intro ψ _
    simpa using tendsto_const_nhds (x := (0 : ℝ))

theorem zero_data_statement :
    InitialData (0 : StaticVelocity) (0 : StaticVorticity) →
      Nonempty (GlobalWeakSolution (0 : StaticVelocity) (0 : StaticVorticity)) := by
  intro _
  exact zero_data_solution

#print axioms zero_data_solution
#print axioms zero_data_statement
#print axioms zero_initial_data

end Stage1Rev56.THMM1234
