import ObligationTree
import SchurPort

/-!
# THM-M-0045 proof execution

This module specializes the current-pin Schur construction to finite complex matrices, packages
its unitary and upper-triangular witnesses at the frozen obligation interface, and composes that
package through the checked child-to-root adapter.
-/

namespace Stage1Instances.THM_M_0045.Proof

/-- The recursive Schur port supplies the exact equation-form package frozen by the obligation
tree. -/
theorem schurEquationPackage : ObligationTree.SchurEquationPackage := by
  intro n A
  exact ⟨A.schurTriangulationUnitary, A.schurTriangulation,
    A.schurTriangulationUnitary.property, A.schurTriangulation.property,
    A.schur_triangulation⟩

/-- The exact canonical target, obtained through the checked equation-package adapter. -/
theorem schurTriangularization : SchurTriangularizationTarget :=
  ObligationTree.root_of_equationPackage schurEquationPackage

#check schurEquationPackage
#check schurTriangularization
#print sorries schurEquationPackage
#print sorries schurTriangularization
#print axioms schurEquationPackage
#print axioms schurTriangularization

end Stage1Instances.THM_M_0045.Proof
