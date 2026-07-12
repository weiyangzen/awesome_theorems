import ObligationTree
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul

/-!
# THM-M-1515 proof bodies

This module closes the two analytic packages in the frozen obligation tree and
composes them into the exact statement from `Statement.lean`.
-/

noncomputable section

namespace Stage1Instances.THM_M_1515

universe u

/-- The boundary term along a regular trajectory has the derivative specified
by its Frechet derivative. -/
theorem boundary_along_curve_derivative :
    BoundaryAlongCurveDerivative.{u} := by
  intro E _ _ _ D q hregular t
  rcases hregular with ⟨_, _, hboundary, hq⟩
  simpa [Function.comp_def] using
    (hboundary (q t)).hasFDerivAt.comp_hasDerivAt t
      ((hq.differentiable two_ne_zero t).hasDerivAt)

/-- Differentiate the momentum-generator pairing. The derivative of momentum
is supplied by Euler-Lagrange; the other factor follows by the chain rule. -/
theorem momentum_pairing_derivative :
    MomentumPairingDerivative.{u} := by
  intro E _ _ _ D q hregular heuler t
  rcases hregular with ⟨_, hgenerator, _, hq⟩
  have hq' : HasDerivAt q (velocity E q t) t := by
    simpa [velocity] using (hq.differentiable two_ne_zero t).hasDerivAt
  have hgenerator' :
      HasDerivAt (fun s : ℝ => D.generator (q s))
        (fderiv ℝ D.generator (q t) (velocity E q t)) t :=
    by
      simpa [Function.comp_def] using
        (hgenerator (q t)).hasFDerivAt.comp_hasDerivAt t hq'
  simpa [momentumPairing] using (heuler t).clm_apply hgenerator'

/-- The exact finite-dimensional Noether target selected at intake. -/
theorem noether_first_theorem : NoetherFirstTheoremTarget.{u} :=
  root_of_derivative_packages momentum_pairing_derivative
    boundary_along_curve_derivative

#print axioms boundary_along_curve_derivative
#print axioms momentum_pairing_derivative
#print axioms noether_first_theorem

end Stage1Instances.THM_M_1515
