import Statement

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

#check isProbabilityMeasure_of_isWienerMeasure
#check measurableEvaluationLinear
#check continuousScale
#check zeroTimeVarianceAndLaw
#check zeroTimeLaw

#print axioms isProbabilityMeasure_of_isWienerMeasure
#print axioms measurableEvaluationLinear
#print axioms continuousScale
#print axioms zeroTimeVarianceAndLaw
#print axioms zeroTimeLaw

end Stage1Instances.THM_M_1060
