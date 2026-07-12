import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.Kernel.Composition.Comp

/-!
This file checks the pinned Lean substrate relevant to `THM-M-1094`. It is not the canonical
Kolmogorov backward-equation target: the accepted intake does not identify an exact source theorem
or fix enough mathematics to select that target without substitution.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1094.StatementProbe

universe u

variable {State : Type u} [MeasurableSpace State]

/-- A noncanonical boundary exposing only the kernel, density, and derivative APIs under review. -/
def SubstrateBoundary
    (transitionKernel : ℝ → Kernel State State)
    (referenceMeasure : Measure State)
    (transitionDensity : ℝ → State → State → ℝ)
    (backwardGenerator : (State → ℝ) → State → ℝ) : Prop :=
  transitionKernel 0 = Kernel.id ∧
    (∀ s t : ℝ, 0 ≤ s → 0 ≤ t →
      transitionKernel (s + t) = transitionKernel t ∘ₖ transitionKernel s) ∧
    (∀ t x, 0 ≤ t →
      transitionKernel t x =
        referenceMeasure.withDensity
          (fun y => ENNReal.ofReal (transitionDensity t x y))) ∧
    (∀ t x y, 0 < t →
      HasDerivAt (fun τ => transitionDensity τ x y)
        (backwardGenerator (fun z => transitionDensity t z y) x) t)

#check Kernel.id
#check Kernel.comp
#check Measure.withDensity
#check HasDerivAt
#check SubstrateBoundary

end Stage1Instances.THM_M_1094.StatementProbe
