import Statement
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic

/-!
# THM-M-1060 proof-phase boundary lemmas

These are unconditional map-side substrate and direct consequences of the
frozen `IsWienerMeasure` predicate.  They expose the probability and one-time
Gaussian laws needed by the Wiener-normalization branch.  They do not prove
either large-deviation bound, goodness of the rate function, or the exact
Schilder root.
-/

noncomputable section

open MeasureTheory Set
open scoped NNReal

namespace Stage1Instances.THM_M_1060

/-- Finite linear combinations of path evaluations are measurable.  This is
the map-side prerequisite for using the laws in `IsWienerMeasure`. -/
theorem measurableEvaluationLinear {n : Nat} (t : Fin n -> Icc (0 : Real) 1)
    (a : Fin n -> Real) :
    Measurable (fun f : BasedPath => Finset.sum Finset.univ fun i => a i * f.1 (t i)) := by
  apply Finset.measurable_sum
  intro i _hi
  exact measurable_const.mul
    (((continuous_eval_const (t i)).comp continuous_subtype_val).borel_measurable)

/-- Scaling based paths is continuous. -/
theorem continuousScale (c : Real) : Continuous (scale c) := by
  apply Continuous.subtype_mk
  exact (continuous_const_smul c).comp continuous_subtype_val

/-- The probability-measure component of the frozen Wiener predicate. -/
theorem isProbabilityMeasure_of_isWienerMeasure {W : Measure BasedPath}
    (hW : IsWienerMeasure W) : IsProbabilityMeasure W :=
  hW.1

/-- The zero-time specialization of the finite-dimensional law has variance
zero.  This checks the based-path boundary without assuming an LDP. -/
theorem zeroTimeVarianceAndLaw (W : Measure BasedPath) (hW : IsWienerMeasure W) :
    exists v : NNReal, v = 0 /\
      Measure.map (fun f : BasedPath =>
        Finset.sum Finset.univ fun _i : Fin 1 =>
          (1 : Real) * f.1 (show Icc (0 : Real) 1 from ⟨0, by norm_num⟩)) W =
        ProbabilityTheory.gaussianReal 0 v := by
  rcases hW.2 1 (fun _ => ⟨0, by norm_num⟩) (fun _ => 1) with ⟨v, hv, hmap⟩
  have hv0 : v = 0 := by
    apply NNReal.eq
    simpa using hv
  exact ⟨v, hv0, hmap⟩

/-- At time zero the frozen finite-dimensional law is the expected degenerate
Gaussian. -/
theorem zeroTimeLaw (W : Measure BasedPath) (hW : IsWienerMeasure W) :
    Measure.map (fun f : BasedPath =>
      Finset.sum Finset.univ fun _i : Fin 1 =>
        (1 : Real) * f.1 (show Icc (0 : Real) 1 from ⟨0, by norm_num⟩)) W =
      ProbabilityTheory.gaussianReal 0 0 := by
  rcases zeroTimeVarianceAndLaw W hW with ⟨v, rfl, hmap⟩
  exact hmap

/-- Every one-time marginal supplied by the frozen Wiener predicate has the
expected variance.  Unlike `zeroTimeLaw`, this covers arbitrary times in the
frozen interval. -/
theorem oneTimeVarianceAndLaw (W : Measure BasedPath) (hW : IsWienerMeasure W)
    (t : Icc (0 : Real) 1) :
    exists v : NNReal, (v : Real) = t /\
      Measure.map (fun f : BasedPath => f.1 t) W =
        ProbabilityTheory.gaussianReal 0 v := by
  rcases hW.2 1 (fun _ => t) (fun _ => 1) with ⟨v, hv, hmap⟩
  refine ⟨v, ?_, ?_⟩
  · simpa using hv
  · simpa using hmap

/-- The exact one-time marginal law, with the nonnegative time represented as
an `NNReal` variance. -/
theorem oneTimeLaw (W : Measure BasedPath) (hW : IsWienerMeasure W)
    (t : Icc (0 : Real) 1) :
    Measure.map (fun f : BasedPath => f.1 t) W =
      ProbabilityTheory.gaussianReal 0 ⟨t, t.2.1⟩ := by
  rcases oneTimeVarianceAndLaw W hW t with ⟨v, hv, hmap⟩
  have hvar : v = (⟨t, t.2.1⟩ : NNReal) := by
    apply NNReal.eq
    exact hv
  simpa [hvar] using hmap

/-- The coordinate process under a frozen Wiener measure is jointly Gaussian.
This packages the finite-dimensional law predicate in mathlib's reusable
`IsGaussianProcess` interface. -/
theorem isGaussianProcess_of_isWienerMeasure (W : Measure BasedPath)
    (hW : IsWienerMeasure W) :
    ProbabilityTheory.IsGaussianProcess
      (fun (t : Icc (0 : Real) 1) (f : BasedPath) => f.1 t) W := by
  refine ⟨?_⟩
  intro I
  refine ⟨ProbabilityTheory.isGaussian_of_map_eq_gaussianReal
    (E := I -> Real) (μ := W.map fun f : BasedPath => I.restrict fun t => f.1 t) fun L => ?_⟩
  let n := Fintype.card I
  let e : Fin n ≃ I := Fintype.equivFin I |>.symm
  let t : Fin n -> Icc (0 : Real) 1 := fun i => (e i).1
  let a : Fin n -> Real := fun i => L (Pi.single (e i) 1)
  rcases hW.2 n t a with ⟨v, hv, hmap⟩
  refine ⟨0, v, ?_⟩
  rw [← hmap]
  rw [Measure.map_map L.measurable]
  · congr 1
    funext f
    change L (I.restrict fun t => f.1 t) = _
    have hL := LinearMap.pi_apply_eq_sum_univ L.toLinearMap
      (I.restrict fun t => f.1 t)
    change L.toLinearMap (I.restrict fun t => f.1 t) = _
    rw [hL]
    rw [Fintype.sum_equiv e]
    intro i
    rw [mul_comm]
    change f.1 (e i).1 * L (Pi.single (e i) 1) =
      f.1 (e i).1 * L (fun j => if e i = j then 1 else 0)
    congr 1
    congr 1
    funext j
    simp [Pi.single, Function.update, eq_comm]
  · apply measurable_pi_lambda
    intro i
    change Measurable (fun f : BasedPath => f.1 i.1)
    exact ((continuous_eval_const i.1).comp continuous_subtype_val).borel_measurable

#check isProbabilityMeasure_of_isWienerMeasure
#check measurableEvaluationLinear
#check continuousScale
#check zeroTimeVarianceAndLaw
#check zeroTimeLaw
#check oneTimeVarianceAndLaw
#check oneTimeLaw
#check isGaussianProcess_of_isWienerMeasure

#print axioms isProbabilityMeasure_of_isWienerMeasure
#print axioms measurableEvaluationLinear
#print axioms continuousScale
#print axioms zeroTimeVarianceAndLaw
#print axioms zeroTimeLaw
#print axioms oneTimeVarianceAndLaw
#print axioms oneTimeLaw
#print axioms isGaussianProcess_of_isWienerMeasure

end Stage1Instances.THM_M_1060
