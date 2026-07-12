import Statement

/-!
# THM-M-1526 conditional obligation composition

This module checks the final composition selected by the frozen obligation
architecture. The factorization identity remains an explicit premise; this
does not prove the free Dirac factorization theorem.
-/

namespace Stage1Instances.THM_M_1526

universe u

/-- The algebraic factorization package left open for the proof phase. -/
def FactorizationPackage : Prop :=
  forall (I : Type) (Psi : Type u)
    [Fintype I] [DecidableEq I] [AddCommGroup Psi] [Module Complex Psi]
    (D : FreeDiracData I Psi),
      (slash D + D.mass • (1 : SpinorOperator Psi)) *
          (slash D - D.mass • (1 : SpinorOperator Psi)) =
        kleinGordon D - D.mass ^ 2 • (1 : SpinorOperator Psi)

/-- Checked composition of the factorization identity with its pointwise
Dirac-to-Klein-Gordon consequence. -/
theorem root_of_factorization (factorization : FactorizationPackage.{u}) :
    FreeDiracFactorizationTarget.{u} := by
  intro I Psi _ _ _ _ D
  have hfactor := factorization I Psi D
  refine ⟨hfactor, ?_⟩
  intro psi hdirac
  rw [← hfactor]
  change (slash D + D.mass • (1 : SpinorOperator Psi))
    ((slash D - D.mass • (1 : SpinorOperator Psi)) psi) = 0
  rw [hdirac]
  exact map_zero _

#print axioms root_of_factorization

end Stage1Instances.THM_M_1526
