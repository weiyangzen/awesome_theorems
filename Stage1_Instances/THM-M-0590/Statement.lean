import Mathlib.Analysis.InnerProductSpace.Adjoint

noncomputable section

open scoped ComplexConjugate InnerProduct

namespace THMM0590

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

/-- A bounded operator is Fredholm when its kernel and cokernel are finite-dimensional and its
range is closed.  This local definition is necessary because pinned mathlib has no Fredholm-index
API; it fixes the conventional analytic meaning rather than replacing the BDF invariant. -/
def IsFredholm (A : E →L[ℂ] E) : Prop :=
  FiniteDimensional ℂ A.ker ∧
    FiniteDimensional ℂ (E ⧸ A.range) ∧
      IsClosed (A.range : Set E)

/-- The Fredholm index `dim ker A - dim coker A`.  It is used only under `IsFredholm`. -/
def fredholmIndex (A : E →L[ℂ] E) : ℤ :=
  (Module.finrank ℂ A.ker : ℤ) -
    (Module.finrank ℂ (E ⧸ A.range) : ℤ)

/-- The essential spectrum in the Fredholm characterization, with the sign convention
`A - λI`. -/
def essentialSpectrum (A : E →L[ℂ] E) : Set ℂ :=
  {z | ¬ IsFredholm (A - z • ContinuousLinearMap.id ℂ E)}

/-- Essential normality with the syntactic commutator convention `A† A - A A†`. -/
def IsEssentiallyNormal (A : E →L[ℂ] E) : Prop :=
  IsCompactOperator ((A† ∘L A) - (A ∘L A†))

/-- Unitary equivalence modulo compact operators, oriented as `U A U⁻¹ - B`. -/
def UnitaryEquivalentModuloCompacts
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
    (A : E →L[ℂ] E) (B : F →L[ℂ] F) : Prop :=
  ∃ U : E ≃ₗᵢ[ℂ] F,
    IsCompactOperator
      (U.toContinuousLinearEquiv.toContinuousLinearMap ∘L A ∘L
          U.symm.toContinuousLinearEquiv.toContinuousLinearMap - B)

/-- Exact target selected at intake for the Brown-Douglas-Fillmore classification theorem.

The spaces are separable, infinite-dimensional complex Hilbert spaces.  The index convention is
`A - λI`; equality is required only off the (equal) essential spectrum. -/
def brownDouglasFillmoreTarget : Prop :=
  ∀ (H K : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [TopologicalSpace.SeparableSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    [TopologicalSpace.SeparableSpace K]
    (T : H →L[ℂ] H) (S : K →L[ℂ] K),
    (¬ FiniteDimensional ℂ H) →
      (¬ FiniteDimensional ℂ K) →
    IsEssentiallyNormal T →
      IsEssentiallyNormal S →
        (UnitaryEquivalentModuloCompacts T S ↔
          essentialSpectrum T = essentialSpectrum S ∧
            ∀ z : ℂ, z ∉ essentialSpectrum T →
              fredholmIndex (T - z • ContinuousLinearMap.id ℂ H) =
                fredholmIndex (S - z • ContinuousLinearMap.id ℂ K))

#check brownDouglasFillmoreTarget

end THMM0590
