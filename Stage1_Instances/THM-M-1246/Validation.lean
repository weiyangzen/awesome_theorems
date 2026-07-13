import ObligationTree
import RegularizedIBP
import SharpEstimate
import HardyLimit
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1246 same-worker differential validation

This module deliberately does not import `Proof`. Independently of that
wrapper module, it replays the positive-regularization assembly against the frozen analytic
terminal and then uses the frozen terminal-to-root composition boundary. This
checks that no hidden dependency on `Proof.olean` is needed, but the assembly
mirrors the proof source and is not independent reasoning, a distinct verifier
identity, or a distinct runner.
-/

noncomputable section

open MeasureTheory Filter
open scoped Topology

namespace Stage1Instances.THM_M_1246.Validation

open Stage1Instances.THM_M_1246
open Stage1Instances.THM_M_1246.ObligationTree
open Stage1Instances.THM_M_1246.Proof

/-- A replay of the exact terminal assembly without the `Proof` wrapper module. -/
theorem independentlyReconstructedHardyTerminal : HardyTerminal := by
  intro n hn u hu huc
  have hlam : 0 < (n : Real) - 2 := by
    have hnR : (2 : Real) < (n : Real) := by
      exact_mod_cast (show 2 < n by omega)
    linarith
  let A : Nat -> Real := fun k => ∫ x, |u x| ^ 2 /
    (‖x‖ ^ 2 + 1 / ((k : Real) + 1))
  let C : Real := (2 / ((n : Real) - 2)) ^ 2 *
    ∫ x, ‖fderiv Real u x‖ ^ 2
  have hA : forall k, A k <= C := by
    intro k
    let eps : Real := 1 / ((k : Real) + 1)
    have heps : 0 < eps := by positivity
    have hdens := regularized_density_integrable u hu huc eps heps
    have hleft : Integrable (fun x =>
        ((n : Real) - 2) * (|u x| ^ 2 / (‖x‖ ^ 2 + eps))) :=
      hdens.const_mul _
    have hright := regularized_divergence_integrable u hu.continuous huc eps heps
    have hlower := integral_mul_divergence_lower u eps heps hleft (by
      simpa only [sq_abs] using hright)
    have hibp := regularized_summed_ibp u hu huc eps heps
    have hibpLower : ((n : Real) - 2) *
        (∫ x, |u x| ^ 2 / (‖x‖ ^ 2 + eps)) <=
        |∫ x, 2 * u x * (fderiv Real u x x / (‖x‖ ^ 2 + eps))| := by
      calc
        _ <= ∫ x, |u x| ^ 2 *
            ((n : Real) / (‖x‖ ^ 2 + eps) -
              2 * ‖x‖ ^ 2 / (‖x‖ ^ 2 + eps) ^ 2) := hlower
        _ = - ∫ x, 2 * u x *
            (fderiv Real u x x / (‖x‖ ^ 2 + eps)) := by
          simpa only [sq_abs] using hibp
        _ <= |∫ x, 2 * u x *
            (fderiv Real u x x / (‖x‖ ^ 2 + eps))| := neg_le_abs _
    simpa [A, C, eps] using
      regularized_sharp_from_ibp_lower u hu huc eps ((n : Real) - 2)
        heps hlam hibpLower
  exact le_of_tendsto'
    (regularized_integral_tendsto n hn u hu.continuous huc) hA

/-- The separately replayed terminal passed through the frozen root edge. -/
theorem independentlyReconstructedHardyInequality : HardyInequalityTarget :=
  root_of_hardyTerminal independentlyReconstructedHardyTerminal

assert_no_sorry independentlyReconstructedHardyTerminal
assert_no_sorry independentlyReconstructedHardyInequality
#print sorries independentlyReconstructedHardyTerminal
#print sorries independentlyReconstructedHardyInequality
#print axioms independentlyReconstructedHardyTerminal
#print axioms independentlyReconstructedHardyInequality

end Stage1Instances.THM_M_1246.Validation
