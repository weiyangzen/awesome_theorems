import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.Kernel.Composition.Comp

/-!
This file checks the pinned Lean substrate relevant to `THM-M-1092`.  It is not the canonical
Kolmogorov forward/backward target: the repository source does not fix enough mathematics to choose
that target without substitution.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1092.StatementProbe

universe u

variable {State : Type u} [MeasurableSpace State]

/-- The smallest checked boundary exposing the kernel, density, and time-derivative APIs. -/
def SubstrateBoundary
    (transitionKernel : ℝ → Kernel State State)
    (referenceMeasure : Measure State)
    (transitionDensity : ℝ → State → State → ℝ) : Prop :=
  transitionKernel 0 = Kernel.id ∧
    (∀ s t : ℝ, 0 ≤ s → 0 ≤ t →
      transitionKernel (s + t) = transitionKernel t ∘ₖ transitionKernel s) ∧
    (∀ t x, 0 ≤ t →
      transitionKernel t x =
        referenceMeasure.withDensity
          (fun y => ENNReal.ofReal (transitionDensity t x y))) ∧
    (∀ x y, DifferentiableOn ℝ (fun t => transitionDensity t x y) (Set.Ioi 0))

#check Kernel.id
#check Kernel.comp
#check Measure.withDensity
#check HasDerivAt
#check SubstrateBoundary

end Stage1Instances.THM_M_1092.StatementProbe
