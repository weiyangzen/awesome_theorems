import Statement

/-!
# THM-M-0545 degree-zero proof blocker

The frozen definition of exactness requires a natural predecessor in every
degree. Consequently it has no witness in degree zero, while the target still
requires a decomposition in that degree. This file checks the resulting
negation of the exact universal target independently of the operator laws.
-/

noncomputable section

namespace Stage1Instances.THMM0545

open HodgeAnalyticData

universe uE uH uM

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners Real E H}
  {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]

/-- The frozen exactness predicate has no degree-zero inhabitants because a
natural number cannot satisfy `j + 1 = 0`. -/
theorem not_isExact_zero (D : HodgeAnalyticData E H I M) (e : D.Form 0) :
    ¬ D.IsExact 0 e := by
  rintro ⟨j, _alpha, hj, _heq⟩
  omega

/-- Since exactness is mandatory for every decomposition triple, the frozen
target admits no degree-zero decomposition at all. -/
theorem no_degreeZeroDecomposition (D : HodgeAnalyticData E H I M)
    (omega : D.Form 0) : ¬ D.HasUniqueDecomposition 0 omega := by
  rintro ⟨_h, e, _c, _hh, he, _hc, _ho, _hsum, _unique⟩
  exact not_isExact_zero D e he

/-- A minimal admitted realization used only to instantiate the universal
manifold target; the contradiction itself depends only on degree zero. -/
def degreeZeroCounterexampleData : HodgeAnalyticData E H I M where
  Form := fun _ => Complex
  exteriorDerivative := fun _ => 0
  codifferential := fun _ => 0
  laplacian := fun _ => 0
  isOriented := True
  isBoundaryless := True
  realizesSmoothComplexForms := True
  realizesHodgeOperators := True

private abbrev ZeroModel := EuclideanSpace Real (Fin 0)

private instance : Unique ZeroModel := inferInstance

/-- Degree zero alone refutes the exact frozen universal target. -/
theorem not_hodgeDecompositionTarget_degreeZero :
    ¬ HodgeDecompositionTarget.{0, 0, 0, 0} := by
  intro target
  have decomposition := target ZeroModel ZeroModel
    (modelWithCornersSelf Real ZeroModel) ZeroModel
    (degreeZeroCounterexampleData
      (I := modelWithCornersSelf Real ZeroModel) (M := ZeroModel))
    trivial trivial trivial trivial 0 (0 : Complex)
  exact no_degreeZeroDecomposition _ _ decomposition

#print not_hodgeDecompositionTarget_degreeZero
#print axioms not_hodgeDecompositionTarget_degreeZero

end Stage1Instances.THMM0545
