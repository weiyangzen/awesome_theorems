import Statement
import PoissonUnitDisk

/-!
# THM-M-1148 proof work

This module composes the implemented Poisson construction with mathlib's
representation theorem and closes the exact frozen target. It retains the
conditional unit-disk construction as a separately checked interface.
-/

noncomputable section

open InnerProductSpace Metric Real Set

namespace Stage1Instances.THM_M_1148.Proof

open Stage1Instances.THM_M_1148.PoissonUnitDisk

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

/-- The exact root follows from a Dirichlet extension package. -/
theorem dirichletExtension_to_root : DirichletExtension → RootTarget := by
  intro extension c R hR g hg
  obtain ⟨u, harmonic, continuous, trace⟩ := extension c R hR g hg
  refine ⟨u, harmonic, continuous, trace, ?_⟩
  exact interiorFormula_of_harmonicContOnCl_of_eqOn
    (HarmonicContOnCl.mk_ball harmonic continuous) trace

/-- The local root spelling is definitionally the exact frozen target. -/
theorem rootTarget_to_frozen :
    RootTarget → PoissonIntegralFormula := by
  intro root c R hR g hg
  exact root c R hR g hg

/-- Conditional composition all the way to the exact frozen target. -/
theorem dirichletExtension_to_frozen :
    DirichletExtension → PoissonIntegralFormula :=
  rootTarget_to_frozen ∘ dirichletExtension_to_root

/-- The implemented construction supplies the previously open extension package. -/
theorem dirichletExtension : DirichletExtension := by
  intro c R hR g hg
  exact generalDiskConstruction c R hR g hg

/-- Exact closure of the frozen rev-5.6 target. -/
theorem poissonIntegralFormula : PoissonIntegralFormula :=
  dirichletExtension_to_frozen dirichletExtension

/-- Unit-disk construction from arbitrary continuous boundary data. -/
theorem unitDiskConstruction_of_boundaryConvergence
    {g : ℂ → ℝ} (hg : ContinuousOn g (sphere (0 : ℂ) 1))
    (hboundary : ∀ z0 ∈ sphere (0 : ℂ) 1,
      Filter.Tendsto (poissonIntegral g)
        (nhdsWithin z0 (ball 0 1)) (nhds (g z0))) :
    ∃ u : ℂ → ℝ,
      HarmonicOnNhd u (ball 0 1) ∧
        ContinuousOn u (closedBall 0 1) ∧ EqOn u g (sphere 0 1) := by
  let U : C(ℂ, ℝ) := by
    let boundary : C(sphere (0 : ℂ) 1, ℝ) :=
      ⟨fun z => g z, continuousOn_iff_continuous_restrict.mp hg⟩
    exact Classical.choose
      (boundary.exists_restrict_eq (isClosed_sphere : IsClosed (sphere (0 : ℂ) 1)))
  have hUg : EqOn U g (sphere (0 : ℂ) 1) := by
    let boundary : C(sphere (0 : ℂ) 1, ℝ) :=
      ⟨fun z => g z, continuousOn_iff_continuous_restrict.mp hg⟩
    have hrestrict := Classical.choose_spec
      (boundary.exists_restrict_eq (isClosed_sphere : IsClosed (sphere (0 : ℂ) 1)))
    intro z hz
    let zh : sphere (0 : ℂ) 1 := ⟨z, hz⟩
    have heq : U zh = boundary zh := by
      exact DFunLike.congr_fun hrestrict zh
    simpa [U, boundary] using heq
  have hFormula : poissonIntegral U = poissonIntegral g := by
    funext a
    apply circleAverage_congr_sphere
    intro z hz
    change poissonKernel 0 a z * U z = poissonKernel 0 a z * g z
    rw [hUg (by simpa using hz)]
  have hboundaryU : ∀ z0 ∈ sphere (0 : ℂ) 1,
      Filter.Tendsto (poissonIntegral U)
        (nhdsWithin z0 (ball 0 1)) (nhds (U z0)) := by
    intro z0 hz0
    rw [hFormula, hUg hz0]
    exact hboundary z0 hz0
  refine ⟨unitDiskExtension U, ?_, ?_, ?_⟩
  · exact unitDiskExtension_harmonic U
      (U.continuous.continuousOn.circleIntegrable' (c := 0) (R := 1))
  · exact unitDiskExtension_continuousOn U U.continuous hboundaryU
  · exact (unitDiskExtension_eqOn_sphere U).trans hUg

#print axioms interiorFormula_of_harmonicContOnCl_of_eqOn
#print axioms dirichletExtension_to_root
#print axioms rootTarget_to_frozen
#print axioms dirichletExtension_to_frozen
#print axioms dirichletExtension
#print axioms poissonIntegralFormula
#print axioms unitDiskConstruction_of_boundaryConvergence

end Stage1Instances.THM_M_1148.Proof
