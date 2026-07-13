import Statement
import DoobLp
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1005 differential validation reconstruction

This module imports the frozen statement and the vendored analytic terminal, but neither
`Proof.lean` nor `ObligationTree.lean`. It independently reconstructs the exact public root from
`MeasureTheory.maximal_ineq_Lp`. This is a same-worker differential check, not a distinct-runner
attestation or a second analytic proof body.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1005.Validation

universe u

/-- A separately written direct reconstruction of the exact frozen Doob `L^p` root. -/
theorem independentlyReconstructedDoobLpMomentEstimate :
    Stage1Instances.THM_M_1005.Statement.{u} := by
  intro Omega _ mu _ G f hf p hp hptop n
  have hsub : Submartingale (fun k omega => |f k omega|) G mu := by
    simpa only [abs_eq_max_neg, Pi.sup_apply, Pi.neg_apply] using
      hf.submartingale.sup hf.neg.submartingale
  have hp_ne_top : p ≠ (∞ : ENNReal) := by
    apply ne_of_lt
    simpa using hptop
  have hp_real : (1 : Real) < p.toReal := by
    rw [<- ENNReal.toReal_one]
    exact ENNReal.toReal_strict_mono hp_ne_top hp
  have h := MeasureTheory.maximal_ineq_Lp hsub (fun _ _ => abs_nonneg _) hp_real n
  rw [ENNReal.ofReal_toReal hp_ne_top] at h
  rw [<- eLpNorm_norm (f n)]
  simpa only [Stage1Instances.THM_M_1005.runningAbsMax, Real.norm_eq_abs, eLpNorm_norm] using h

#check independentlyReconstructedDoobLpMomentEstimate
assert_no_sorry MeasureTheory.maximal_ineq_Lp
assert_no_sorry independentlyReconstructedDoobLpMomentEstimate
#print sorries MeasureTheory.maximal_ineq_Lp
#print sorries independentlyReconstructedDoobLpMomentEstimate
#print axioms MeasureTheory.maximal_ineq_Lp
#print axioms independentlyReconstructedDoobLpMomentEstimate

end Stage1Instances.THM_M_1005.Validation
