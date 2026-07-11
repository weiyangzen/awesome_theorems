import Statement

/-! Kernel-checked countermodel to the frozen THM-M-0545 statement interface. -/

noncomputable section

namespace Stage1Instances.THMM0545

open HodgeAnalyticData

universe uE uH uM

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners Real E H}
  {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]

/-- An admitted realization whose forms are scalars, whose `d` and `delta`
vanish, and whose Laplacian is the identity. -/
def counterexampleData : HodgeAnalyticData E H I M where
  Form := fun _ => Complex
  exteriorDerivative := fun _ => 0
  codifferential := fun _ => 0
  laplacian := fun _ => ContinuousLinearMap.id Complex Complex
  isOriented := True
  isBoundaryless := True
  realizesSmoothComplexForms := True
  realizesHodgeOperators := True

theorem counterexampleData_hypotheses :
    (counterexampleData (I := I) (M := M)).isOriented ∧
      (counterexampleData (I := I) (M := M)).isBoundaryless ∧
      (counterexampleData (I := I) (M := M)).realizesSmoothComplexForms ∧
      (counterexampleData (I := I) (M := M)).realizesHodgeOperators := by
  exact ⟨trivial, trivial, trivial, trivial⟩

/-- The nonzero scalar form has no claimed decomposition: all three summands
would have to be zero. -/
theorem counterexampleData_no_decomposition :
    ¬ (counterexampleData (I := I) (M := M)).HasUniqueDecomposition 1 (1 : Complex) := by
  rintro ⟨h, e, c, hh, he, hc, _ho, hsum, _unique⟩
  have hh0 : h = 0 := by
    simpa [HodgeAnalyticData.IsHarmonic, counterexampleData] using hh
  have he0 : e = 0 := by
    rcases he with ⟨j, alpha, hj, heq⟩
    simpa [counterexampleData] using heq.symm
  have hc0 : c = 0 := by
    rcases hc with ⟨beta, hbeta⟩
    simpa [counterexampleData] using hbeta.symm
  have : (1 : Complex) = 0 := by
    rw [hh0, he0, hc0] at hsum
    simpa only [add_zero] using hsum
  exact one_ne_zero this

end Stage1Instances.THMM0545
