import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Data.Fintype.Perm
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

/-!
The canonical statement of Baik--Deift--Johansson, Theorem 1.1.  The analytic
predicate below spells out the source's definition of the Tracy--Widom CDF;
it is not an assumption of the desired permutation limit.
-/

namespace Stage1Instances.THM_M_1108

open Filter MeasureTheory Set Topology
open scoped BigOperators ENNReal NNReal Topology

noncomputable section

/-- Length of a longest strictly increasing subsequence of a permutation in
one-line notation.  A candidate subsequence is represented by its set of indices. -/
def lisLength {N : ℕ} (σ : Equiv.Perm (Fin N)) : ℕ :=
  Finset.univ.sup fun s : Finset (Fin N) =>
    if ∀ i ∈ s, ∀ j ∈ s, i < j → σ i < σ j then s.card else 0

/-- The uniform probability of the normalized LIS event in Theorem 1.1. -/
noncomputable def normalizedLISCDF (N : ℕ) (t : ℝ) : ℝ :=
  (Fintype.card {σ : Equiv.Perm (Fin N) //
      ((lisLength σ : ℝ) - 2 * Real.sqrt N) / (N : ℝ) ^ (1 / 6 : ℝ) ≤ t} : ℝ) /
    (Fintype.card (Equiv.Perm (Fin N)) : ℝ)

/-- A source-level characterization of the Airy function `Ai`: its ODE and
the positive-infinity normalization used in the BDJ paper. -/
def IsAiryAi (a : ℝ → ℝ) : Prop :=
  (∀ x, HasDerivAt a (deriv a x) x ∧ HasDerivAt (deriv a) (x * a x) x) ∧
  Tendsto
    (fun x : ℝ =>
      a x /
        (Real.exp (-(2 / 3 : ℝ) * x ^ (3 / 2 : ℝ)) /
          (2 * Real.sqrt Real.pi * x ^ (1 / 4 : ℝ))))
    atTop (nhds 1)

/-- The Hastings--McLeod Painleve II solution and the Tracy--Widom CDF as
defined in equations (1.4)--(1.6) of the source. -/
def IsTracyWidomCDF (F : ℝ → ℝ) : Prop :=
  ∃ a u : ℝ → ℝ,
    IsAiryAi a ∧
    (∀ x, HasDerivAt u (deriv u x) x ∧
      HasDerivAt (deriv u) (2 * (u x) ^ 3 + x * u x) x) ∧
    Tendsto (fun x => u x / (-a x)) atTop (nhds 1) ∧
    ∀ t, F t = Real.exp (-∫ x in Set.Ioi t, (x - t) * (u x) ^ 2)

/-- Baik--Deift--Johansson (1999), Theorem 1.1: for a uniformly random
permutation of `N` letters, `(L_N - 2 sqrt N) / N^(1/6)` converges in
distribution to the Tracy--Widom law. -/
def CanonicalStatement : Prop :=
  ∀ F : ℝ → ℝ, IsTracyWidomCDF F →
    ∀ t : ℝ, Tendsto (fun N : ℕ => normalizedLISCDF N t) atTop (nhds (F t))

/-- Fully unfolded outer encoding, used to check that the named target adds no
hidden premise or conclusion. -/
theorem canonicalStatement_iff_unfolded :
    CanonicalStatement ↔
      ∀ F : ℝ → ℝ,
        (∃ a u : ℝ → ℝ,
          IsAiryAi a ∧
          (∀ x, HasDerivAt u (deriv u x) x ∧
            HasDerivAt (deriv u) (2 * (u x) ^ 3 + x * u x) x) ∧
          Tendsto (fun x => u x / (-a x)) atTop (nhds 1) ∧
          ∀ t, F t = Real.exp (-∫ x in Set.Ioi t, (x - t) * (u x) ^ 2)) →
        ∀ t : ℝ, Tendsto (fun N : ℕ => normalizedLISCDF N t) atTop (nhds (F t)) := by
  rfl

/-! Type-directed mutation probes: a witness for any altered proposition is not
accepted as a witness for the frozen root. -/

def RemovedModelHypothesisMutation : Prop :=
  ∀ F : ℝ → ℝ, ∀ t : ℝ,
    Tendsto (fun N : ℕ => normalizedLISCDF N t) atTop (nhds (F t))

def ChangedScalingMutation : Prop :=
  ∀ F : ℝ → ℝ, IsTracyWidomCDF F → ∀ t : ℝ,
    Tendsto
      (fun N : ℕ =>
        (Fintype.card {σ : Equiv.Perm (Fin N) //
            ((lisLength σ : ℝ) - 2 * Real.sqrt N) / (N : ℝ) ^ (1 / 3 : ℝ) ≤ t} : ℝ) /
          (Fintype.card (Equiv.Perm (Fin N)) : ℝ))
      atTop (nhds (F t))

def ChangedBinderScopeMutation : Prop :=
  ∃ t : ℝ, ∀ F : ℝ → ℝ, IsTracyWidomCDF F →
    Tendsto (fun N : ℕ => normalizedLISCDF N t) atTop (nhds (F t))

def ExcludedBoundaryMutation : Prop :=
  ∀ F : ℝ → ℝ, IsTracyWidomCDF F → ∀ t : ℝ,
    Tendsto (fun N : ℕ => normalizedLISCDF (N + 1) t) atTop (nhds (F t))

variable
  (hRemoved : RemovedModelHypothesisMutation)
  (hScaling : ChangedScalingMutation)
  (hScope : ChangedBinderScopeMutation)
  (hBoundary : ExcludedBoundaryMutation)

#check_failure (show CanonicalStatement from hRemoved)
#check_failure (show CanonicalStatement from hScaling)
#check_failure (show CanonicalStatement from hScope)
#check_failure (show CanonicalStatement from hBoundary)

#check CanonicalStatement
#print CanonicalStatement
#check canonicalStatement_iff_unfolded
#print axioms canonicalStatement_iff_unfolded

end
end Stage1Instances.THM_M_1108
