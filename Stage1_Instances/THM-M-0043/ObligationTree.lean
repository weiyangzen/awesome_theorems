import Statement

/-!
# THM-M-0043 conditional obligation composition

This module checks the exact child-to-root adapter frozen by the obligation registry. The audited
external spectral-theorem body remains an explicit premise; installing or independently rebuilding
that body belongs to the later proof phase.
-/

namespace Stage1Instances.THM_M_0043.ObligationTree

universe u

/-- Exact conjugated-diagonal conclusion exposed by the audited Atlas candidate. -/
def ExactConjugatedDiagonalAnchor : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] (A : Matrix n n Complex),
    IsStarNormal A ->
      exists (P : Matrix n n Complex) (_ : P ∈ Matrix.unitaryGroup n Complex)
        (d : n -> Complex),
        star P * A * P = Matrix.diagonal d

/-- Conditional composition from the exact audited child shape to the frozen canonical root. -/
theorem root_of_exactConjugatedDiagonalAnchor
    (anchor : ExactConjugatedDiagonalAnchor.{u}) :
    Stage1Instances.THM_M_0043.SpectralTheoremTarget.{u} := by
  intro n _ _ _ A hA
  obtain ⟨P, hP, d, hDiagonal⟩ := anchor n A hA
  let U : Matrix.unitaryGroup n Complex := ⟨P, hP⟩
  refine ⟨U, d, ?_⟩
  calc
    A = (1 : Matrix n n Complex) * A * 1 := by simp
    _ = (P * star P) * A * (P * star P) := by
      rw [Matrix.mem_unitaryGroup_iff.mp hP]
    _ = P * (star P * A * P) * star P := by simp only [mul_assoc]
    _ = P * Matrix.diagonal d * star P := by rw [hDiagonal]

#print axioms root_of_exactConjugatedDiagonalAnchor

end Stage1Instances.THM_M_0043.ObligationTree
