import Statement
import Mathlib.Analysis.Analytic.Uniqueness
import Mathlib.Analysis.Calculus.ContDiff.Basic

/-!
# THM-M-1277 proof execution

This module refutes the frozen target. In the statement's type,
`ContDiff Real top` is analytic (`C^omega`), not smooth (`C^infinity`). Every
compactly supported approximant is therefore zero by analytic uniqueness, so
the chosen completion contains only scalar fields that vanish almost
everywhere and the supercritical clause is false. The module also records
basic boundary and interior-ball lemmas discovered while checking the target.
-/

noncomputable section

open MeasureTheory Filter
open scoped ContDiff ENNReal Topology

namespace Stage1Rev56.THMM1277

/-- The concrete gradient selected by the statement sends the zero function
to the zero vector field. -/
theorem classicalGradient_zero :
    classicalGradient (0 : ScalarField) = (0 : VectorField) := by
  funext x
  apply (WithLp.equiv 2 (Fin 2 -> Real)).injective
  ext i
  simp [classicalGradient]

/-- The constant zero sequence realizes the zero function in the exact
completion encoding selected for `ZeroBoundarySobolev`. -/
theorem zeroBoundarySobolev_zero (Omega : Set Plane) :
    ZeroBoundarySobolev Omega (0 : ScalarField) (0 : VectorField) := by
  refine ⟨aestronglyMeasurable_zero, aestronglyMeasurable_zero,
    fun _ => (0 : ScalarField), ?_, ?_, ?_⟩
  · intro n
    refine ⟨contDiff_zero_fun, HasCompactSupport.zero, by simp⟩
  · simpa only [sub_zero, eLpNorm_zero] using (tendsto_const_nhds :
      Tendsto (fun _ : Nat => (0 : ENNReal)) atTop (nhds 0))
  · simp only [classicalGradient_zero, sub_zero]
    simpa only [eLpNorm_zero] using (tendsto_const_nhds :
      Tendsto (fun _ : Nat => (0 : ENNReal)) atTop (nhds 0))

/-- The zero scalar field is admissible on every domain. -/
theorem admissible_zero (Omega : Set Plane) :
    Admissible Omega (0 : ScalarField) := by
  refine ⟨(0 : VectorField), zeroBoundarySobolev_zero Omega, ?_⟩
  simp [GradientEnergy]

/-- At the zero function, the exponential integral is exactly the volume of
the domain, independently of the exponent. -/
theorem exponentialIntegral_zero (Omega : Set Plane) (alpha : Real) :
    ExponentialIntegral Omega alpha (0 : ScalarField) = volume Omega := by
  simp [ExponentialIntegral]

/-- Bounded domains have finite volume in the selected Euclidean measure. -/
theorem bounded_volume_lt_top
    (Omega : Set Plane) (hbounded : Bornology.IsBounded Omega) :
    volume Omega < (⊤ : ENNReal) := by
  exact hbounded.measure_lt_top

/-- The overloaded `top` in the frozen definition is definitionally the
analytic order `omega`. -/
theorem frozen_top_is_analytic_order (f : ScalarField) :
    ContDiff Real ⊤ f = ContDiff Real ω f := rfl

/-- The intended smooth order is the coerced top of `ℕ∞`, definitionally
mathlib's order `infinity`. -/
theorem coerced_enat_top_is_smooth_order (f : ScalarField) :
    ContDiff Real (((⊤ : ℕ∞) : WithTop ℕ∞)) f = ContDiff Real ∞ f := rfl

/-- Under the frozen `ContDiff Real top` encoding, compact support forces the
approximant to vanish: `top` here is the analytic order `omega`, not smooth
order `infinity`. -/
theorem smoothCompactIn_eq_zero
    (Omega : Set Plane) (phi : ScalarField)
    (hphi : SmoothCompactIn Omega phi) : phi = 0 := by
  have hanalytic : AnalyticOnNhd Real phi Set.univ :=
    hphi.1.analyticOnNhd
  have hproper : tsupport phi ≠ Set.univ := hphi.2.1.isCompact.ne_univ
  obtain ⟨x, hx⟩ := Set.nonempty_compl.mpr hproper
  have hlocal : phi =ᶠ[nhds x] (0 : ScalarField) := by
    rw [← notMem_tsupport_iff_eventuallyEq]
    exact hx
  exact AnalyticOnNhd.eq_of_eventuallyEq hanalytic analyticOnNhd_const hlocal

/-- The frozen completion predicate collapses its scalar component to zero
almost everywhere, because every declared approximant is analytic and
compactly supported and hence identically zero. -/
theorem zeroBoundarySobolev_ae_zero
    (Omega : Set Plane) (u : ScalarField) (g : VectorField)
    (h : ZeroBoundarySobolev Omega u g) : u =ᵐ[volume] 0 := by
  obtain ⟨phi, hsmooth, hu, _⟩ := h.2.2
  have hphi : forall n, phi n = 0 := fun n =>
    smoothCompactIn_eq_zero Omega (phi n) (hsmooth n)
  have hnorm : eLpNorm u 2 volume = 0 := by
    have hconst :
        Tendsto (fun n : Nat => eLpNorm (u - phi n) 2 volume) atTop
          (nhds (eLpNorm u 2 volume)) := by
      simpa only [hphi, sub_zero] using
        (tendsto_const_nhds :
          Tendsto (fun _ : Nat => eLpNorm u 2 volume) atTop (nhds (eLpNorm u 2 volume)))
    exact tendsto_nhds_unique hconst hu
  exact (eLpNorm_eq_zero_iff h.1 (by norm_num : (2 : ENNReal) ≠ 0)).mp hnorm

/-- Every function admitted by the frozen completion encoding has the same
exponential integral as zero. -/
theorem exponentialIntegral_eq_volume_of_zeroBoundarySobolev
    (Omega : Set Plane) (alpha : Real) (u : ScalarField) (g : VectorField)
    (h : ZeroBoundarySobolev Omega u g) :
    ExponentialIntegral Omega alpha u = volume Omega := by
  rw [ExponentialIntegral]
  calc
    (∫⁻ x in Omega, ENNReal.ofReal (Real.exp (alpha * u x ^ 2)) ∂volume) =
        ∫⁻ _x in Omega, (1 : ENNReal) ∂volume := by
          apply lintegral_congr_ae
          filter_upwards [ae_restrict_of_ae (zeroBoundarySobolev_ae_zero Omega u g h)] with x hx
          simp [hx]
    _ = volume Omega := by simp

/-- Admissibility exposes a selected weak gradient, so the preceding collapse
applies directly. -/
theorem exponentialIntegral_eq_volume_of_admissible
    (Omega : Set Plane) (alpha : Real) (u : ScalarField)
    (h : Admissible Omega u) :
    ExponentialIntegral Omega alpha u = volume Omega := by
  obtain ⟨g, hug, _⟩ := h
  exact exponentialIntegral_eq_volume_of_zeroBoundarySobolev Omega alpha u g hug

/-- The exact frozen statement is refutable: `ContDiff Real top` denotes
analytic regularity, so every compactly supported approximant vanishes and
the supercritical integral can never exceed the finite domain volume. -/
theorem not_statement : Not Statement := by
  intro hstatement
  let Omega : Set Plane := Metric.ball 0 1
  have hopen : IsOpen Omega := Metric.isOpen_ball
  have hne : Omega.Nonempty := Metric.nonempty_ball.mpr zero_lt_one
  have hbounded : Bornology.IsBounded Omega := Metric.isBounded_ball
  obtain ⟨_, hsharp⟩ := hstatement Omega hopen hne hbounded
  have hvolume : volume Omega < (⊤ : ENNReal) := bounded_volume_lt_top Omega hbounded
  obtain ⟨u, hu, hlt⟩ :=
    hsharp (4 * Real.pi + 1) (by linarith) (volume Omega) hvolume
  rw [exponentialIntegral_eq_volume_of_admissible Omega
    (4 * Real.pi + 1) u hu] at hlt
  exact (lt_irrefl _ hlt)

set_option pp.explicit true in
#check (show Not Statement from not_statement)

/-- Every nonempty open subset of the selected plane contains a closed ball
of positive radius. This is a candidate local lemma corresponding to
`M1277-C-INBALL`; the stale frozen registry does not yet wire it as a terminal
body. -/
theorem exists_interior_closedBall
    (Omega : Set Plane)
    (hopen : IsOpen Omega) (hne : Omega.Nonempty) :
    exists x : Plane, exists r : Real,
      0 < r ∧ Metric.closedBall x r ⊆ Omega := by
  obtain ⟨x, hx⟩ := hne
  obtain ⟨epsilon, hepsilon, hball⟩ := Metric.isOpen_iff.mp hopen x hx
  refine ⟨x, epsilon / 2, half_pos hepsilon, ?_⟩
  exact (Metric.closedBall_subset_ball (half_lt_self hepsilon)).trans hball

#check classicalGradient_zero
#check zeroBoundarySobolev_zero
#check admissible_zero
#check exponentialIntegral_zero
#check bounded_volume_lt_top
#check frozen_top_is_analytic_order
#check coerced_enat_top_is_smooth_order
#check smoothCompactIn_eq_zero
#check zeroBoundarySobolev_ae_zero
#check exponentialIntegral_eq_volume_of_zeroBoundarySobolev
#check exponentialIntegral_eq_volume_of_admissible
#check not_statement
#check exists_interior_closedBall
#print axioms classicalGradient_zero
#print axioms zeroBoundarySobolev_zero
#print axioms admissible_zero
#print axioms exponentialIntegral_zero
#print axioms bounded_volume_lt_top
#print axioms frozen_top_is_analytic_order
#print axioms coerced_enat_top_is_smooth_order
#print axioms smoothCompactIn_eq_zero
#print axioms zeroBoundarySobolev_ae_zero
#print axioms exponentialIntegral_eq_volume_of_zeroBoundarySobolev
#print axioms exponentialIntegral_eq_volume_of_admissible
#print axioms not_statement
#print axioms exists_interior_closedBall

end Stage1Rev56.THMM1277
