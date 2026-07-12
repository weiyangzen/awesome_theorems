import Statement

/-!
Conditional composition witness for the frozen THM-M-1234 architecture.
The two substantial package premises remain explicit; this is not a proof of
Yudovich existence.
-/

noncomputable section

open MeasureTheory

namespace Stage1Rev56.THMM1234

structure CandidateFields (u₀ : StaticVelocity) (ω₀ : StaticVorticity) : Type where
  velocity : Velocity
  vorticity : Vorticity
  velocityMeasurable : ∀ t : ℝ, 0 ≤ t → AEStronglyMeasurable (velocity t) volume
  vorticityMeasurable : ∀ t : ℝ, 0 ≤ t → AEStronglyMeasurable (vorticity t) volume
  finiteEnergy : ∀ t : ℝ, 0 ≤ t → MemLp (velocity t) 2 volume
  boundedVorticity : ∀ t : ℝ, 0 ≤ t → MemLp (vorticity t) ⊤ volume
  divergenceFree : ∀ t : ℝ, 0 ≤ t → WeaklyDivergenceFree (velocity t)
  vorticityIsCurl : ∀ t : ℝ, 0 ≤ t → WeakCurl (velocity t) (vorticity t)

def CandidateConstructionPackage : Prop :=
  ∀ (u₀ : StaticVelocity) (ω₀ : StaticVorticity),
    InitialData u₀ ω₀ → Nonempty (CandidateFields u₀ ω₀)

def EquationAndTraceClosurePackage : Prop :=
  ∀ (u₀ : StaticVelocity) (ω₀ : StaticVorticity),
    InitialData u₀ ω₀ → ∀ c : CandidateFields u₀ ω₀,
      WeakMomentumEquation u₀ c.velocity ∧
        ∀ ψ : Plane → ℝ, SmoothCompactScalarTest ψ →
          Filter.Tendsto
            (fun t => ∫ x, c.vorticity t x * ψ x)
            (nhdsWithin 0 (Set.Ioi 0))
            (nhds (∫ x, ω₀ x * ψ x))

theorem root_of_construction_and_closure
    (construct : CandidateConstructionPackage)
    (close : EquationAndTraceClosurePackage) : Statement := by
  intro u₀ ω₀ hdata
  obtain ⟨c⟩ := construct u₀ ω₀ hdata
  obtain ⟨hmomentum, htrace⟩ := close u₀ ω₀ hdata c
  exact ⟨{
    velocity := c.velocity
    vorticity := c.vorticity
    velocityMeasurable := c.velocityMeasurable
    vorticityMeasurable := c.vorticityMeasurable
    finiteEnergy := c.finiteEnergy
    boundedVorticity := c.boundedVorticity
    divergenceFree := c.divergenceFree
    vorticityIsCurl := c.vorticityIsCurl
    momentumEquation := hmomentum
    initialVorticityTrace := htrace
  }⟩

#print axioms root_of_construction_and_closure

end Stage1Rev56.THMM1234
