import OseledetsStatement

/-!
# THM-M-1419 conditional obligation composition

This module gives the frozen architecture an exact typed final boundary.  The
construction package is an explicit premise: this file does not prove it or
the Oseledets target.
-/

noncomputable section

open Filter MeasureTheory

namespace Stage1Instances.THM_M_1419

universe u

/-- The output data required after fixing the cocycle and probability system. -/
def OseledetsConclusion {d : ℕ} {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (T : Ω ≃ Ω) (A : Ω → SquareMatrix d) : Prop :=
  ∃ (k : ℕ) (exponents : Fin k → ℝ)
    (E : Ω → Fin k → Submodule ℝ (Vector d)),
    0 < k ∧
    StrictAnti exponents ∧
    MeasurableSubspaceField E ∧
    (∀ᵐ ω ∂μ,
      iSupIndep (E ω) ∧
      (⨆ i, E ω i) = ⊤ ∧
      (∀ i, 0 < Module.finrank ℝ (E ω i)) ∧
      (∀ i, Submodule.map (Matrix.mulVecLin (A ω)) (E ω i) = E (T ω) i) ∧
      ∀ i v, v ∈ E ω i → v ≠ 0 →
        Tendsto
          (fun n : ℕ => ((n : ℝ)⁻¹ * Real.log ‖(cocycleProduct T A n ω).mulVec v‖))
          atTop (nhds (exponents i)))

/-- Exact conditional package consumed by the final composition node.  It is
kept definitionally equal to the canonical target so no interface weakening
can be hidden in the architecture wrapper. -/
def OseledetsConstructionPackage : Prop :=
  OseledetsMultiplicativeErgodicTarget.{u}

/-- Checked final composition.  Its substantive package premise remains open. -/
theorem target_of_construction_package
    (package : OseledetsConstructionPackage.{u}) :
    OseledetsMultiplicativeErgodicTarget.{u} := by
  exact package

#check OseledetsConclusion
#check OseledetsConstructionPackage
#print axioms target_of_construction_package

end Stage1Instances.THM_M_1419
