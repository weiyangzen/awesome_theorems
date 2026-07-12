import Mathlib.Analysis.Distribution.TemperedDistribution

/-!
# THM-M-1251: exact tempered-distribution statement

This module freezes the repository claim "tempered distributions are the dual
of Schwartz space" using mathlib's documented pointwise-convergence topology.
It is statement-gate evidence only.
-/

noncomputable section

open scoped SchwartzMap

universe u

namespace Stage1Instances.THM_M_1251

/-- The complex continuous dual of complex-valued Schwartz maps, equipped with
the pointwise-convergence topology used by mathlib's distribution API. -/
abbrev SchwartzPointwiseDual
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] : Type u :=
  SchwartzMap E ℂ →Lₚₜ[ℂ] ℂ

/-- The exact target selected from the intake scope. The finite-dimensional
assumption keeps the base-space scope aligned with the classical `ℝ^n` claim;
no stronger topology on the dual is asserted. -/
def TemperedDistributionsAreSchwartzDual : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E],
      TemperedDistribution E ℂ = SchwartzPointwiseDual E

/-- Direct expansion of the selected target through the documented mathlib
pointwise-convergence continuous-linear-map representation. -/
def ExpandedPointwiseDualTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E],
      TemperedDistribution E ℂ = (SchwartzMap E ℂ →Lₚₜ[ℂ] ℂ)

/-- Checked transport to the direct pointwise-dual expansion. -/
theorem target_iff_expandedPointwiseDualTarget :
    TemperedDistributionsAreSchwartzDual.{u} ↔
      ExpandedPointwiseDualTarget.{u} :=
  Iff.rfl

-- Structural mutations elaborated separately for fingerprint comparison.
def mutationRemovedFiniteDimensional : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E],
    TemperedDistribution E ℂ = SchwartzPointwiseDual E

def mutationChangedDomain : Prop :=
  ∀ (n : Nat),
    TemperedDistribution (EuclideanSpace ℝ (Fin n)) ℂ =
      SchwartzPointwiseDual (EuclideanSpace ℝ (Fin n))

def mutationChangedBinderScope : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E],
    (∀ (_realSpace : NormedSpace ℝ E) (_finite : FiniteDimensional ℝ E),
      TemperedDistribution E ℂ = SchwartzPointwiseDual E)

/-- The zero-dimensional Euclidean base is intentionally included. -/
theorem zeroDimensional_boundary :
    TemperedDistribution (EuclideanSpace ℝ (Fin 0)) ℂ =
      SchwartzPointwiseDual (EuclideanSpace ℝ (Fin 0)) :=
  rfl

end Stage1Instances.THM_M_1251

set_option pp.explicit true in
#print Stage1Instances.THM_M_1251.TemperedDistributionsAreSchwartzDual
