import Mathlib.Analysis.Complex.Harmonic.Poisson

/-!
# THM-M-1148 obligation interfaces

This file checks the interfaces and child-to-root composition used by the
frozen obligation graph.  Its hypotheses are deliberately not implementations
of the analytic obligations.
-/

noncomputable section

open InnerProductSpace Metric Real Set

namespace Stage1Instances.THM_M_1148.ObligationTree

def InteriorFormula (c : ℂ) (R : ℝ) (g u : ℂ → ℝ) : Prop :=
  ∀ w : ℂ, w ∈ ball c R →
    circleAverage (poissonKernel c w • g) c R = u w

def SolutionPackage (c : ℂ) (R : ℝ) (g u : ℂ → ℝ) : Prop :=
  HarmonicOnNhd u (ball c R) ∧
    ContinuousOn u (closedBall c R) ∧
      EqOn u g (sphere c R) ∧ InteriorFormula c R g u

def ConstructedSolution : Prop :=
  ∀ (c : ℂ) (R : ℝ), 0 < R → ∀ g : ℂ → ℝ,
    ContinuousOn g (sphere c R) → ∃ u : ℂ → ℝ, SolutionPackage c R g u

-- Kept textually identical to the elaborated target in `Statement.lean`; the
-- structural validator binds this interface to that target's fingerprint.
def RootTarget : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R → ∀ g : ℂ → ℝ, ContinuousOn g (sphere c R) →
      ∃ u : ℂ → ℝ,
        HarmonicOnNhd u (ball c R) ∧
          ContinuousOn u (closedBall c R) ∧
            EqOn u g (sphere c R) ∧
              ∀ w : ℂ, w ∈ ball c R →
                circleAverage (poissonKernel c w • g) c R = u w

theorem solutionPackage_compose {c : ℂ} {R : ℝ} {g u : ℂ → ℝ}
    (harmonic : HarmonicOnNhd u (ball c R))
    (continuous : ContinuousOn u (closedBall c R))
    (trace : EqOn u g (sphere c R))
    (formula : InteriorFormula c R g u) : SolutionPackage c R g u :=
  ⟨harmonic, continuous, trace, formula⟩

theorem constructedSolution_to_root :
    ConstructedSolution → RootTarget := by
  intro construction c R hR g hg
  obtain ⟨u, hu⟩ := construction c R hR g hg
  exact ⟨u, hu.1, hu.2.1, hu.2.2.1, hu.2.2.2⟩

theorem root_to_constructedSolution :
    RootTarget → ConstructedSolution := by
  intro root c R hR g hg
  obtain ⟨u, harmonic, continuous, trace, formula⟩ := root c R hR g hg
  exact ⟨u, harmonic, continuous, trace, formula⟩

theorem exact_root_transport :
    ConstructedSolution ↔ RootTarget :=
  ⟨constructedSolution_to_root, root_to_constructedSolution⟩

#print axioms solutionPackage_compose
#print axioms constructedSolution_to_root
#print axioms root_to_constructedSolution
#print axioms exact_root_transport

end Stage1Instances.THM_M_1148.ObligationTree
