import Statement

/-!
# THM-M-0044 conditional obligation composition

This module checks the empty-dimension and exact-root composition interfaces chosen by the frozen
obligation graph. The positive-dimension real and complex packages remain explicit premises: this
file does not construct singular vectors or prove singular-value decomposition.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0044.ObligationTree

/-- Exact real half of the canonical conjunction. -/
def RealFullSVDPackage : Prop := FullSVDOver Real

/-- Exact complex half of the canonical conjunction. -/
def ComplexFullSVDPackage : Prop := FullSVDOver Complex

/-- Exactly the zero-row and zero-column branches needed by the selected Real and Complex root. -/
def SelectedEmptyDimensionPackage : Prop :=
  (forall (n : Nat) (A : Matrix (Fin 0) (Fin n) Real), IsFullSVD A) /\
  (forall (m : Nat) (A : Matrix (Fin m) (Fin 0) Real), IsFullSVD A) /\
  (forall (n : Nat) (A : Matrix (Fin 0) (Fin n) Complex), IsFullSVD A) /\
  (forall (m : Nat) (A : Matrix (Fin m) (Fin 0) Complex), IsFullSVD A)

/-- Checked empty-dimension package, assembled only from the statement module's exact witnesses. -/
theorem selectedEmptyDimensions : SelectedEmptyDimensionPackage := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact fun n A => zeroByNBoundary Real n A
  · exact fun m A => mByZeroBoundary Real m A
  · exact fun n A => zeroByNBoundary Complex n A
  · exact fun m A => mByZeroBoundary Complex m A

/-- Checked composition of the two exact scalar packages into the frozen canonical root. -/
theorem root_of_real_and_complex
    (realPackage : RealFullSVDPackage)
    (complexPackage : ComplexFullSVDPackage) :
    SingularValueDecompositionTarget :=
  ⟨realPackage, complexPackage⟩

#print axioms selectedEmptyDimensions
#print axioms root_of_real_and_complex

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0044.SingularValueDecompositionTarget

end Stage1Instances.THM_M_0044.ObligationTree
