import Statement
import Mathlib.Analysis.Calculus.Deriv.Add

/-!
# THM-M-1515 conditional obligation composition

This module checks the final proof interface selected by the frozen obligation
architecture.  The two chain-rule packages are explicit premises; this file
does not provide their proofs and therefore does not prove Noether's theorem.
-/

noncomputable section

namespace Stage1Instances.THM_M_1515

universe u

variable (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- The momentum covector paired with the infinitesimal generator. -/
def momentumPairing (D : NoetherData E) (q : ℝ → E) (t : ℝ) : ℝ :=
  velocityDerivative E D (q t) (velocity E q t) (D.generator (q t))

/-- Open analytic package: product/chain rules plus Euler--Lagrange give the
derivative of the momentum-generator pairing. -/
def MomentumPairingDerivative : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q → IsEulerLagrange E D q → ∀ t : ℝ,
        HasDerivAt (momentumPairing E D q)
          (positionDerivative E D (q t) (velocity E q t) (D.generator (q t)) +
            velocityDerivative E D (q t) (velocity E q t)
              (fderiv ℝ D.generator (q t) (velocity E q t))) t

/-- Open analytic package: the chain rule differentiates the boundary term
along the trajectory. -/
def BoundaryAlongCurveDerivative : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q → ∀ t : ℝ,
        HasDerivAt (fun s : ℝ => D.boundary (q s))
          (fderiv ℝ D.boundary (q t) (velocity E q t)) t

/-- Checked conditional composition of the two analytic derivative packages,
the frozen symmetry equation, and subtraction into the exact root target. -/
theorem root_of_derivative_packages
    (momentumDerivative : MomentumPairingDerivative.{u})
    (boundaryDerivative : BoundaryAlongCurveDerivative.{u}) :
    NoetherFirstTheoremTarget.{u} := by
  intro E _ _ _ D q hregular hsymmetry heuler t
  have hp := momentumDerivative E D q hregular heuler t
  have hb := boundaryDerivative E D q hregular t
  simpa [noetherCharge, momentumPairing, hsymmetry (q t) (velocity E q t)] using hp.sub hb

#print axioms root_of_derivative_packages

end Stage1Instances.THM_M_1515
