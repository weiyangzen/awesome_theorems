import ObligationTree
import RegularizedIBP
import SharpEstimate
import HardyLimit

/-!
# THM-M-1246 proof

The proof uses the smooth radial field `x / (‖x‖ ^ 2 + eps)`. Its divergence
and compact-support integration-by-parts identity give a lower bound for the
regularized inverse-square density. A sharp Young estimate bounds the radial
derivative term, and dominated convergence removes `eps`.
-/

noncomputable section

open MeasureTheory Filter
open scoped Topology

namespace Stage1Instances.THM_M_1246.Proof

open Stage1Instances.THM_M_1246
open Stage1Instances.THM_M_1246.ObligationTree

/-- The exact analytic terminal required by the frozen obligation tree. -/
theorem hardyTerminal : HardyTerminal := by
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

/-- The exact frozen root, obtained through its checked transport boundary. -/
theorem hardyInequality : HardyInequalityTarget :=
  root_of_hardyTerminal hardyTerminal

#check hardyTerminal
#check hardyInequality
#print axioms hardyTerminal
#print axioms hardyInequality

end Stage1Instances.THM_M_1246.Proof
