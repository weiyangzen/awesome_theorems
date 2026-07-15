import Statement
import Mathlib.Analysis.Analytic.Uniqueness
import Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension

/-!
# THM-M-1250: counterexample to the frozen characterization

The unscoped regularity order in `IsSchwartzFunction` elaborates as the
analytic order `omega`, not the infinitely differentiable order `infinity`.
This module constructs a nonzero, compactly supported smooth function, bundles
it as a `SchwartzMap`, and uses analytic uniqueness to refute the exact frozen
characterization.

This does not refute the classical Schwartz-space characterization with the
intended smoothness order.
-/

noncomputable section

open Set Filter
open scoped ContDiff

namespace Stage1Instances.THM_M_1250.Counterexample

/-- An analytic function with compact support on a Euclidean domain vanishes. -/
theorem analytic_compactSupport_eq_zero
    (f : EuclideanDomain 1 -> Complex)
    (analytic : ContDiff Real (⊤ : WithTop ENat) f)
    (compact : HasCompactSupport f) : f = 0 := by
  have support_ne_univ : tsupport f ≠ (univ : Set (EuclideanDomain 1)) :=
    compact.ne_univ
  obtain ⟨x, hx⟩ := (ne_univ_iff_exists_notMem (tsupport f)).mp support_ne_univ
  exact analytic.analyticOnNhd.eq_of_eventuallyEq
    analyticOnNhd_const
    (notMem_tsupport_iff_eventuallyEq.mp hx)

/-- The exact frozen proposition is false. A nonzero compactly supported
smooth function is a bundled Schwartz map, but it is not analytic. -/
theorem not_schwartzSpaceCharacterization : Not SchwartzSpaceCharacterization := by
  intro characterization
  obtain ⟨u, _, u_compact, u_smooth, _, u_zero⟩ :=
    exists_contDiff_tsupport_subset
      (E := EuclideanDomain 1) (n := (⊤ : ENat))
      (Metric.ball_mem_nhds (0 : EuclideanDomain 1) zero_lt_one)
  let f : EuclideanDomain 1 -> Complex := Complex.ofRealCLM ∘ u
  have f_compact : HasCompactSupport f := u_compact.comp_left rfl
  have f_smooth : ContDiff Real ∞ f :=
    Complex.ofRealCLM.contDiff.comp u_smooth
  have f_is_bundled :
      ∃ phi : SchwartzMap (EuclideanDomain 1) Complex,
        (phi : EuclideanDomain 1 -> Complex) = f :=
    ⟨f_compact.toSchwartzMap f_smooth, rfl⟩
  have f_analytic : ContDiff Real (⊤ : WithTop ENat) f :=
    ((characterization 1 f).mp f_is_bundled).1
  have f_zero : f = 0 :=
    analytic_compactSupport_eq_zero f f_analytic f_compact
  have at_zero := congr_fun f_zero (0 : EuclideanDomain 1)
  simp [f, u_zero] at at_zero

set_option pp.explicit true in
#check (show Not SchwartzSpaceCharacterization from not_schwartzSpaceCharacterization)
#print axioms analytic_compactSupport_eq_zero
#print axioms not_schwartzSpaceCharacterization

end Stage1Instances.THM_M_1250.Counterexample
