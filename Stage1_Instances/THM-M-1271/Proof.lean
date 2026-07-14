import ObligationTree
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Order.Compact

/-!
# THM-M-1271 proof implementation

This module implements the geometric mountain-pass package, minimax value
convergence, and the compactness and limit-passage part of the analytic
package. The derivative-small half of the Palais-Smale sequence construction
remains an explicit premise of the last theorem; no canonical-root proof is
claimed here.
-/

namespace Stage1Instances.THM_M_1271

open Filter Set

universe u

variable {X : Type u} [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]

/-- Every admissible path from zero to a point outside the `rho`-ball meets
the sphere of radius `rho`. -/
theorem admissiblePath_meets_sphere {e : X} {rho : ℝ} {gamma : ℝ → X}
    (hgamma : IsAdmissiblePath e gamma) (hrho : 0 < rho) (he : rho < ‖e‖) :
    ∃ t ∈ Icc (0 : ℝ) 1, ‖gamma t‖ = rho := by
  have hnorm : ContinuousOn (fun t : ℝ ↦ ‖gamma t‖) (Icc 0 1) :=
    continuous_norm.comp_continuousOn hgamma.1
  have hrange := intermediate_value_Icc (show (0 : ℝ) ≤ 1 by norm_num) hnorm
  have hrho_mem : rho ∈ Icc (‖gamma 0‖) (‖gamma 1‖) := by
    rw [hgamma.2.1, hgamma.2.2, norm_zero]
    exact ⟨hrho.le, he.le⟩
  rcases hrange hrho_mem with ⟨t, ht, hteq⟩
  exact ⟨t, ht, hteq⟩

/-- The spherical barrier is a lower bound for the height of every admissible
path. -/
theorem alpha_le_pathHeight {Phi : X → ℝ} {rho alpha : ℝ} {e : X} {gamma : ℝ → X}
    (hC1 : ContDiff ℝ 1 Phi) (hgamma : IsAdmissiblePath e gamma)
    (hrho : 0 < rho) (he : rho < ‖e‖)
    (hsphere : ∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) :
    alpha ≤ PathHeight Phi gamma := by
  obtain ⟨t, ht, ht_norm⟩ := admissiblePath_meets_sphere hgamma hrho he
  have hmem : Phi (gamma t) ∈ {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} :=
    ⟨t, ht, rfl⟩
  have hcompact : IsCompact (Phi '' (gamma '' Icc (0 : ℝ) 1)) :=
    ((isCompact_Icc.image_of_continuousOn hgamma.1).image_of_continuousOn
      hC1.continuous.continuousOn)
  have hbdd : BddAbove {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} := by
    have heq : {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} =
        Phi '' (gamma '' Icc (0 : ℝ) 1) := by
      ext r
      constructor
      · rintro ⟨s, hs, rfl⟩
        exact ⟨gamma s, ⟨s, hs, rfl⟩, rfl⟩
      · rintro ⟨x, ⟨s, hs, rfl⟩, rfl⟩
        exact ⟨s, hs, rfl⟩
    rw [heq]
    exact hcompact.bddAbove
  exact (hsphere (gamma t) ht_norm).trans (le_csSup hbdd hmem)

/-- The `sSup` representation of an admissible path height is attained on the
compact parameter interval. -/
theorem pathHeight_attained {Phi : X → ℝ} {e : X} {gamma : ℝ → X}
    (hC1 : ContDiff ℝ 1 Phi) (hgamma : IsAdmissiblePath e gamma) :
    ∃ t ∈ Icc (0 : ℝ) 1, PathHeight Phi gamma = Phi (gamma t) := by
  have hcontinuous : ContinuousOn (fun t : ℝ ↦ Phi (gamma t)) (Icc 0 1) :=
    hC1.continuous.comp_continuousOn hgamma.1
  obtain ⟨t, ht, hmax⟩ := isCompact_Icc.exists_sSup_image_eq
    (nonempty_Icc.2 (show (0 : ℝ) ≤ 1 by norm_num)) hcontinuous
  refine ⟨t, ht, ?_⟩
  rw [PathHeight]
  have heq : {r : ℝ | ∃ s ∈ Icc (0 : ℝ) 1, r = Phi (gamma s)} =
      (fun s : ℝ ↦ Phi (gamma s)) '' Icc 0 1 := by
    ext r
    constructor
    · rintro ⟨s, hs, rfl⟩
      exact ⟨s, hs, rfl⟩
    · rintro ⟨s, hs, rfl⟩
      exact ⟨s, hs, rfl⟩
  rw [heq]
  exact hmax

/-- The complete geometric package used by the root composition theorem. -/
theorem mountainPassBarrierPackage : MountainPassBarrierPackage.{u} := by
  intro X _group _space _complete Phi rho alpha e hC1 _hzero hrho halpha hsphere he _hout
  have hpath : IsAdmissiblePath e (fun t : ℝ ↦ t • e) := by
    refine ⟨(continuous_id.smul continuous_const).continuousOn, ?_, ?_⟩
    · simp
    · simp
  apply le_csInf
  · exact ⟨PathHeight Phi (fun t : ℝ ↦ t • e), (fun t : ℝ ↦ t • e), hpath, rfl⟩
  · rintro c ⟨gamma, hgamma, rfl⟩
    exact alpha_le_pathHeight hC1 hgamma hrho he hsphere

/-- A sequence approaching the minimax value while its derivative norm tends
to zero.  Constructing such a sequence is the remaining deformation/Ekeland
obligation. -/
def IsPalaisSmaleSequenceAt (Phi : X → ℝ) (c : ℝ) (x : ℕ → X) : Prop :=
  Tendsto (fun n ↦ Phi (x n)) atTop (nhds c) ∧
  Tendsto (fun n ↦ ‖fderiv ℝ Phi (x n)‖) atTop (nhds 0)

/-- Minimax order and compact path maxima produce points whose functional
values tend to the mountain-pass level. This is the value-convergence half of
the still-open Palais-Smale sequence construction. -/
theorem exists_valueSequence_at_mountainPassLevel
    {Phi : X → ℝ} {rho alpha : ℝ} {e : X}
    (hC1 : ContDiff ℝ 1 Phi) (hrho : 0 < rho)
    (hsphere : ∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) (he : rho < ‖e‖) :
    ∃ x : ℕ → X, Tendsto (fun n ↦ Phi (x n)) atTop
      (nhds (MountainPassLevel Phi e)) := by
  let heights : Set ℝ :=
    {c : ℝ | ∃ gamma : ℝ → X, IsAdmissiblePath e gamma ∧ c = PathHeight Phi gamma}
  have hline : IsAdmissiblePath e (fun t : ℝ ↦ t • e) := by
    refine ⟨(continuous_id.smul continuous_const).continuousOn, ?_, ?_⟩
    · simp
    · simp
  have hheights : heights.Nonempty := by
    exact ⟨PathHeight Phi (fun t : ℝ ↦ t • e), (fun t : ℝ ↦ t • e), hline, rfl⟩
  have hbdd : BddBelow heights := by
    refine ⟨alpha, ?_⟩
    rintro c ⟨gamma, hgamma, rfl⟩
    exact alpha_le_pathHeight hC1 hgamma hrho he hsphere
  obtain ⟨c, _hcmono, hc_lim, hc_mem⟩ := exists_seq_tendsto_sInf hheights hbdd
  have hc_data : ∀ n, ∃ gamma : ℝ → X,
      IsAdmissiblePath e gamma ∧ c n = PathHeight Phi gamma := by
    simpa only [heights] using hc_mem
  choose gamma hgamma hc_height using hc_data
  have ht_data : ∀ n, ∃ t ∈ Icc (0 : ℝ) 1,
      PathHeight Phi (gamma n) = Phi (gamma n t) :=
    fun n ↦ pathHeight_attained hC1 (hgamma n)
  choose t _ht htmax using ht_data
  refine ⟨fun n ↦ gamma n (t n), ?_⟩
  have heq : (fun n ↦ Phi (gamma n (t n))) = c := by
    funext n
    exact ((hc_height n).trans (htmax n)).symm
  rw [heq]
  simpa only [MountainPassLevel, heights] using hc_lim

/-- Global Palais-Smale compactness and continuity turn a Palais-Smale
sequence into a critical point at its limiting value. -/
theorem exists_criticalPoint_of_psSequence {Phi : X → ℝ} {c : ℝ} {x : ℕ → X}
    (hC1 : ContDiff ℝ 1 Phi) (hPS : PalaisSmale Phi)
    (hx : IsPalaisSmaleSequenceAt Phi c x) :
    ∃ a : X, fderiv ℝ Phi a = 0 ∧ Phi a = c := by
  have hbounded : Bornology.IsBounded (range (fun n ↦ Phi (x n))) :=
    Metric.isBounded_range_of_tendsto (fun n ↦ Phi (x n)) hx.1
  obtain ⟨a, k, hk, hka⟩ := hPS x hbounded hx.2
  have hphi_sub : Tendsto (fun n ↦ Phi (x (k n))) atTop (nhds c) :=
    hx.1.comp hk.tendsto_atTop
  have hphi_a : Tendsto (fun n ↦ Phi (x (k n))) atTop (nhds (Phi a)) :=
    hC1.continuous.continuousAt.tendsto.comp hka
  have hvalue : Phi a = c := tendsto_nhds_unique hphi_a hphi_sub
  have hderiv_cont : Continuous (fderiv ℝ Phi) := hC1.continuous_fderiv (by norm_num)
  have hnorm_a : Tendsto (fun n ↦ ‖fderiv ℝ Phi (x (k n))‖) atTop
      (nhds ‖fderiv ℝ Phi a‖) :=
    (continuous_norm.comp hderiv_cont).continuousAt.tendsto.comp hka
  have hnorm_zero : Tendsto (fun n ↦ ‖fderiv ℝ Phi (x (k n))‖) atTop (nhds 0) :=
    hx.2.comp hk.tendsto_atTop
  have : ‖fderiv ℝ Phi a‖ = 0 := tendsto_nhds_unique hnorm_a hnorm_zero
  exact ⟨a, norm_eq_zero.mp this, hvalue⟩

/-- The exact analytic package follows once the single remaining variational
construction supplies a Palais-Smale sequence at the canonical minimax level. -/
theorem mountainPassCriticalPackage_of_psSequence
    (produce : ∀ (X : Type u) [NormedAddCommGroup X] [NormedSpace ℝ X] [CompleteSpace X]
      (Phi : X → ℝ) (rho alpha : ℝ) (e : X),
      ContDiff ℝ 1 Phi → PalaisSmale Phi → Phi 0 = 0 → 0 < rho → 0 < alpha →
      (∀ x : X, ‖x‖ = rho → alpha ≤ Phi x) → rho < ‖e‖ → Phi e ≤ 0 →
      ∃ x : ℕ → X, IsPalaisSmaleSequenceAt Phi (MountainPassLevel Phi e) x) :
    MountainPassCriticalPackage.{u} := by
  intro X _group _space _complete Phi rho alpha e hC1 hPS hzero hrho halpha hsphere he hout
  obtain ⟨x, hx⟩ := produce X Phi rho alpha e hC1 hPS hzero hrho halpha hsphere he hout
  exact exists_criticalPoint_of_psSequence hC1 hPS hx

#print axioms admissiblePath_meets_sphere
#print axioms alpha_le_pathHeight
#print axioms pathHeight_attained
#print axioms mountainPassBarrierPackage
#print axioms exists_valueSequence_at_mountainPassLevel
#print axioms exists_criticalPoint_of_psSequence
#print axioms mountainPassCriticalPackage_of_psSequence

end Stage1Instances.THM_M_1271
