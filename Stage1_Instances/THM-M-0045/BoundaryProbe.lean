import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.UnitaryGroup

/-! Concrete boundary and convention probes for THM-M-0045. -/

namespace Stage1Instances.THM_M_0045

/-- The selected target specialized to one matrix dimension. -/
def SchurTargetAt (n : Nat) (A : Matrix (Fin n) (Fin n) Complex) : Prop :=
  exists U : Matrix (Fin n) (Fin n) Complex,
    U ∈ Matrix.unitaryGroup (Fin n) Complex ∧
      Matrix.BlockTriangular (star U * A * U) id

/-- The zero-dimensional case is included and has the identity witness. -/
example (A : Matrix (Fin 0) (Fin 0) Complex) : SchurTargetAt 0 A := by
  refine ⟨1, (Matrix.unitaryGroup (Fin 0) Complex).one_mem, ?_⟩
  intro i
  exact Fin.elim0 i

/-- The one-dimensional case is included and has the identity witness. -/
example (A : Matrix (Fin 1) (Fin 1) Complex) : SchurTargetAt 1 A := by
  refine ⟨1, (Matrix.unitaryGroup (Fin 1) Complex).one_mem, ?_⟩
  intro i j hji
  have hi : i = 0 := Fin.eq_zero i
  have hj : j = 0 := Fin.eq_zero j
  subst i
  subst j
  exact (LT.lt.false hji).elim

/-- `BlockTriangular id` says entries strictly below the diagonal vanish. -/
example {n : Nat} {T : Matrix (Fin n) (Fin n) Complex}
    (hT : Matrix.BlockTriangular T id) {i j : Fin n} (hji : j < i) : T i j = 0 :=
  hT hji

/-- The selected unitary convention supplies the left-inverse equation used by the target. -/
example {n : Nat} {U : Matrix (Fin n) (Fin n) Complex}
    (hU : U ∈ Matrix.unitaryGroup (Fin n) Complex) : star U * U = 1 :=
  Matrix.mem_unitaryGroup_iff'.mp hU

end Stage1Instances.THM_M_0045
