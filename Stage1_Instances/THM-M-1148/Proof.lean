import Mathlib.Analysis.Complex.Harmonic.Poisson

/-!
# THM-M-1148 proof work

This module closes the representation-formula bridge for any candidate that
already has the required harmonicity, closed-disk continuity, and boundary
trace.  It does not construct such a candidate from arbitrary boundary data;
that analytic existence package remains open.
-/

noncomputable section

open InnerProductSpace Metric Real Set

namespace Stage1Instances.THM_M_1148.Proof

def InteriorFormula (c : ℂ) (R : ℝ) (g u : ℂ → ℝ) : Prop :=
  ∀ w : ℂ, w ∈ ball c R →
    circleAverage (poissonKernel c w • g) c R = u w

def DirichletExtension : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R → ∀ g : ℂ → ℝ, ContinuousOn g (sphere c R) →
      ∃ u : ℂ → ℝ,
        HarmonicOnNhd u (ball c R) ∧
          ContinuousOn u (closedBall c R) ∧ EqOn u g (sphere c R)

def RootTarget : Prop :=
  ∀ (c : ℂ) (R : ℝ),
    0 < R → ∀ g : ℂ → ℝ, ContinuousOn g (sphere c R) →
      ∃ u : ℂ → ℝ,
        HarmonicOnNhd u (ball c R) ∧
          ContinuousOn u (closedBall c R) ∧
            EqOn u g (sphere c R) ∧ InteriorFormula c R g u

/--
The pinned mathlib Poisson representation theorem supplies the formula part
of the target once the genuinely harder Dirichlet extension has been built.
The boundary trace is used under `circleAverage`, where only values on the
circle matter.
-/
theorem interiorFormula_of_harmonicContOnCl_of_eqOn
    {c : ℂ} {R : ℝ} {g u : ℂ → ℝ}
    (hu : HarmonicContOnCl u (ball c R))
    (hug : EqOn u g (sphere c R)) :
    InteriorFormula c R g u := by
  intro w hw
  have hR : 0 < R := pos_of_mem_ball hw
  apply (circleAverage_congr_sphere (fun x hx ↦ ?_)).trans
    (hu.circleAverage_poissonKernel_smul hw)
  rw [abs_of_pos hR] at hx
  simp only [smul_eq_mul, Pi.mul_apply, hug hx]

/-- The exact root follows from the still-open Dirichlet extension package. -/
theorem dirichletExtension_to_root : DirichletExtension → RootTarget := by
  intro extension c R hR g hg
  obtain ⟨u, harmonic, continuous, trace⟩ := extension c R hR g hg
  refine ⟨u, harmonic, continuous, trace, ?_⟩
  exact interiorFormula_of_harmonicContOnCl_of_eqOn
    (HarmonicContOnCl.mk_ball harmonic continuous) trace

#print axioms interiorFormula_of_harmonicContOnCl_of_eqOn
#print axioms dirichletExtension_to_root

end Stage1Instances.THM_M_1148.Proof
