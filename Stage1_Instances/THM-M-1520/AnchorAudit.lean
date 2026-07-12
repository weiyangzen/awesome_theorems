import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.LinearAlgebra.SymplecticGroup
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

open MeasureTheory

namespace Stage1.THM_M_1520.AnchorAudit

-- Kernel-elaborated types for the substrate declarations credited by the audit.
#check MeasurePreserving
#check MeasurePreserving.id
#check MeasurePreserving.comp
#check MeasurePreserving.map_eq
#check MeasurePreserving.measure_preimage
#check (volume : Measure (EuclideanSpace Real (Fin 2)))
#check gradient
#check Matrix.symplecticGroup
#check SymplecticGroup.J_mem
#check SymplecticGroup.symplectic_det

/-- The pinned symplectic result gives only an invertible determinant. -/
example {n : Type} [DecidableEq n] [Fintype n]
    {A : Matrix (n ⊕ n) (n ⊕ n) Real}
    (hA : A ∈ Matrix.symplecticGroup n Real) : IsUnit A.det :=
  SymplecticGroup.symplectic_det hA

/-- A proof of measure preservation is already terminal for the exact conclusion. -/
example {X : Type} [MeasurableSpace X] (mu : Measure X) (f : X -> X)
    (hf : MeasurePreserving f mu mu) : Measure.map f mu = mu :=
  hf.map_eq

end Stage1.THM_M_1520.AnchorAudit
