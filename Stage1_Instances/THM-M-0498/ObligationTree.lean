import Statement

/-!
# THM-M-0498 conditional obligation composition

This module checks only the final interface selected by the frozen obligation
architecture. The analytic explicit-formula package remains an explicit
premise; no proof of that package or of the root is asserted here.
-/

noncomputable section

open Filter Nat
open scoped Topology

namespace Stage1Instances.THM_M_0498

/-- The exact pointwise conclusion consumed by the canonical root. -/
def ExplicitFormulaAt (E : NontrivialZeroEnumeration) (x : Real) : Prop :=
  Tendsto (fun N : Nat ↦
      (x : Complex) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
        (1 / 2 : Complex) * Complex.log (1 - (x : Complex) ^ (-2 : Complex)))
    atTop (nhds (Chebyshev.psi x : Complex))

/-- Output interface of the inverse-Mellin, contour, residue, and zero-sum
packages. Its proof remains an open obligation. -/
def AnalyticExplicitFormulaPackage : Prop :=
  ∀ (E : NontrivialZeroEnumeration) (x : Real),
    1 < x → IsNotPrimePower x → ExplicitFormulaAt E x

/-- Checked conditional composition from the analytic package into the exact
canonical target. This theorem gives no proof credit to its open premise. -/
theorem root_of_analytic_package
    (analytic : AnalyticExplicitFormulaPackage) :
    RiemannVonMangoldtTarget := by
  intro E x hx hpp
  exact analytic E x hx hpp

theorem explicitFormulaAt_iff_expanded
    (E : NontrivialZeroEnumeration) (x : Real) :
    ExplicitFormulaAt E x ↔
      Tendsto (fun N : Nat ↦
          (x : Complex) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
            (1 / 2 : Complex) * Complex.log (1 - (x : Complex) ^ (-2 : Complex)))
        atTop (nhds (Chebyshev.psi x : Complex)) := by
  rfl

#print axioms root_of_analytic_package

end Stage1Instances.THM_M_0498
