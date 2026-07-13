import Statement

/-!
# THM-M-1259 frozen-target counterexample components

The frozen statement quantifies over an arbitrary measure.  In particular, at the zero measure
its predicate `IsSmoothDistribution` can hold only for the zero distribution.  The declarations
below kernel-check that collapse, construct a nonzero scalar distribution on the zero-dimensional
Euclidean space, and refute the exact frozen target.  They do not alter the statement or assert
Hormander's source theorem.
-/

noncomputable section

open MeasureTheory
open scoped Distributions

namespace Stage1Instances.THM_M_1259.Counterexample

abbrev Point := Fin 0 -> Real

abbrev TestFunction := 𝓓((⊤ : TopologicalSpace.Opens Point), Real)

abbrev ScalarDistribution := Distribution (⊤ : TopologicalSpace.Opens Point) Real ⊤

/-- Evaluation is a continuous functional on test functions, hence a scalar distribution. -/
def evaluationDistribution (x : Point) : ScalarDistribution :=
  TestFunction.limitCLM Real (fun phi : TestFunction => phi x)
    (fun _ _ =>
      (BoundedContinuousFunction.evalCLM Real x).comp
        (ContDiffMapSupportedIn.toBoundedContinuousFunctionCLM Real))
    (fun _ _ _ => rfl)

@[simp]
theorem evaluationDistribution_apply (x : Point) (phi : TestFunction) :
    evaluationDistribution x phi = phi x :=
  rfl

/-- The constant-one test function is legal because the zero-dimensional Euclidean space is
compact and the domain is the top open set. -/
def oneTestFunction : TestFunction where
  toFun := fun _ => 1
  contDiff' := contDiff_const
  hasCompactSupport' := HasCompactSupport.of_compactSpace _
  tsupport_subset' := Set.subset_univ _

theorem evaluationDistribution_ne_zero (x : Point) : evaluationDistribution x ≠ 0 := by
  intro h
  have hzero := DFunLike.congr_fun h oneTestFunction
  change (1 : Real) = 0 at hzero
  have : (1 : Real) = 0 := hzero
  exact one_ne_zero this

/-- Relative to the zero measure, the dossier's smooth-density predicate collapses to `T = 0`.
This is the key reason the arbitrary-measure root cannot be the usual hypoellipticity theorem. -/
theorem smoothDensity_zeroMeasure_iff (T : ScalarDistribution) :
    (exists f : Point -> Real,
      ContDiffOn Real ⊤ f (Set.univ : Set Point) /\
        forall phi : TestFunction, T phi = ∫ x, phi x * f x ∂(0 : Measure Point)) <-> T = 0 := by
  constructor
  · rintro ⟨f, _, hf⟩
    ext phi
    rw [hf phi, integral_zero_measure]
    rfl
  · rintro rfl
    refine ⟨fun _ => 0, contDiffOn_const, ?_⟩
    intro phi
    change (0 : Real) = _
    simp only [mul_zero, integral_zero]

theorem evaluationDistribution_not_smoothAtZeroMeasure (x : Point) :
    ¬ (exists f : Point -> Real,
      ContDiffOn Real ⊤ f (Set.univ : Set Point) /\
        forall phi : TestFunction,
          evaluationDistribution x phi = ∫ y, phi y * f y ∂(0 : Measure Point)) := by
  intro h
  exact evaluationDistribution_ne_zero x ((smoothDensity_zeroMeasure_iff _).mp h)

/-- The canonical zero-dimensional formal adjoint.  Every tangent vector and every derivative is
zero because `Fin 0 -> Real` is a subsingleton. -/
def zeroDimFormalAdjoint (Omega : TopologicalSpace.Opens Point)
    (a : Stage1Instances.THM_M_1259.Coefficients 0) :
    Stage1Instances.THM_M_1259.FormalAdjoint Omega a where
  toTestFunction := 0
  apply_eq := by
    intro phi x
    have hv : Stage1Instances.THM_M_1259.asVectorField a x = 0 := Subsingleton.elim _ _
    have hf : fderiv Real (phi : Point -> Real) x = 0 := Subsingleton.elim _ _
    simp [Stage1Instances.THM_M_1259.vectorFieldApply,
      Stage1Instances.THM_M_1259.divergence, hv, hf]

/-- The canonical sum-of-squares bundle for the degenerate `n = r = 0` instance. -/
def zeroDimOperator (Omega : TopologicalSpace.Opens Point) :
    Stage1Instances.THM_M_1259.SumOfSquaresFormalAdjoint Omega
      (0 : Stage1Instances.THM_M_1259.Coefficients 0)
      (0 : Fin 0 -> Stage1Instances.THM_M_1259.Coefficients 0) 0 where
  fieldAdjoint := fun j => Fin.elim0 j
  driftAdjoint := zeroDimFormalAdjoint Omega 0
  toTestFunction := 0
  apply_eq := by simp [zeroDimFormalAdjoint]

theorem zeroDim_bracketGenerating :
    Stage1Instances.THM_M_1259.BracketGenerating
      (⊤ : TopologicalSpace.Opens Point)
      (0 : Stage1Instances.THM_M_1259.Coefficients 0)
      (0 : Fin 0 -> Stage1Instances.THM_M_1259.Coefficients 0) := by
  intro x hx
  apply Subsingleton.elim

/-- The frozen target is false: its deliberately admitted `n = 0`, `r = 0` boundary and arbitrary
measure binder allow the zero operator at the zero measure.  The zero image is represented by a
smooth zero density, but the nonzero evaluation distribution cannot have any density at that
measure. -/
theorem not_hormanderTarget : ¬ Stage1Instances.THM_M_1259.hormanderTarget := by
  intro htarget
  let Omega : TopologicalSpace.Opens Point := ⊤
  let A := zeroDimOperator Omega
  have hhypo : Stage1Instances.THM_M_1259.IsHypoelliptic (0 : Measure Point) A :=
    htarget 0 0 Omega 0 0 0 0 A
      (by intro i; exact Fin.elim0 i)
      (by intro j; exact Fin.elim0 j)
      contDiff_zero_fun.contDiffOn
      zeroDim_bracketGenerating
  have himage : Stage1Instances.THM_M_1259.IsDistributionalImage A
      (evaluationDistribution 0) 0 := by
    intro phi
    simp [A, zeroDimOperator]
  have hzeroSmooth : Stage1Instances.THM_M_1259.IsSmoothDistribution
      (0 : Measure Point) (0 : ScalarDistribution) := by
    simpa [Stage1Instances.THM_M_1259.IsSmoothDistribution] using
      (smoothDensity_zeroMeasure_iff (0 : ScalarDistribution)).2 rfl
  have hevalSmooth :
      Stage1Instances.THM_M_1259.IsSmoothDistribution
        (0 : Measure Point) (evaluationDistribution 0) :=
    hhypo (evaluationDistribution 0) 0 himage hzeroSmooth
  apply evaluationDistribution_not_smoothAtZeroMeasure 0
  simpa [Stage1Instances.THM_M_1259.IsSmoothDistribution] using hevalSmooth

end Stage1Instances.THM_M_1259.Counterexample

#print axioms Stage1Instances.THM_M_1259.Counterexample.smoothDensity_zeroMeasure_iff
#print axioms Stage1Instances.THM_M_1259.Counterexample.evaluationDistribution_not_smoothAtZeroMeasure
#print axioms Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget
