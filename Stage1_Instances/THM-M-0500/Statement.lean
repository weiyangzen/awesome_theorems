import Mathlib.Data.ZMod.Coprime
import Mathlib.Order.Interval.Finset.Basic

/-!
# THM-M-0500 canonical Lean statement

This module freezes Dirichlet's theorem on primes in arithmetic progressions. It deliberately
imports only the residue-class/unit API and the order-theoretic infinitude transport, not mathlib's
module containing the proof of Dirichlet's theorem.
-/

namespace Stage1Instances.THM_M_0500

/-- For every nonzero natural modulus, every unit residue class contains infinitely many primes. -/
def DirichletPrimesInAPTarget : Prop :=
  ∀ (q : ℕ) [NeZero q] (a : ZMod q), IsUnit a →
    {p : ℕ | p.Prime ∧ (p : ZMod q) = a}.Infinite

/-- The equivalent formulation saying that a suitable prime exists above every bound. -/
def DirichletPrimesInAPUnboundedTarget : Prop :=
  ∀ (q : ℕ) [NeZero q] (a : ZMod q), IsUnit a → ∀ n : ℕ,
    ∃ p > n, p.Prime ∧ (p : ZMod q) = a

/-- Checked transport between set infinitude and unbounded existence. -/
theorem dirichletPrimesInAPTarget_iff_unbounded :
    DirichletPrimesInAPTarget ↔ DirichletPrimesInAPUnboundedTarget := by
  constructor
  · intro h q _ a ha n
    obtain ⟨p, hp, hnp⟩ := Set.infinite_iff_exists_gt.mp (h q a ha) n
    exact ⟨p, hnp, hp⟩
  · intro h q _ a ha
    apply Set.infinite_iff_exists_gt.mpr
    intro n
    obtain ⟨p, hnp, hp⟩ := h q a ha n
    exact ⟨p, hp, hnp⟩

-- Structural mutations are separately elaborated but must not type as the canonical target.
def mutationRemovedUnitHypothesis : Prop :=
  ∀ (q : ℕ) [NeZero q] (a : ZMod q),
    {p : ℕ | p.Prime ∧ (p : ZMod q) = a}.Infinite

def mutationChangedPrimeDomainToInt : Prop :=
  ∀ (q : ℕ) [NeZero q] (a : ZMod q), IsUnit a →
    {p : ℤ | p.natAbs.Prime ∧ (p : ZMod q) = a}.Infinite

def mutationChangedModulusBinderScope : Prop :=
  ∃ q : ℕ, NeZero q ∧ ∀ a : ZMod q, IsUnit a →
    {p : ℕ | p.Prime ∧ (p : ZMod q) = a}.Infinite

def mutationExcludedModulusOne : Prop :=
  ∀ (q : ℕ) [NeZero q], q ≠ 1 → ∀ a : ZMod q, IsUnit a →
    {p : ℕ | p.Prime ∧ (p : ZMod q) = a}.Infinite

variable
  (hRemoved : mutationRemovedUnitHypothesis)
  (hDomain : mutationChangedPrimeDomainToInt)
  (hScope : mutationChangedModulusBinderScope)
  (hBoundary : mutationExcludedModulusOne)

#check_failure (show DirichletPrimesInAPTarget from hRemoved)
#check_failure (show DirichletPrimesInAPTarget from hDomain)
#check_failure (show DirichletPrimesInAPTarget from hScope)
#check_failure (show DirichletPrimesInAPTarget from hBoundary)

set_option pp.explicit true in
#print DirichletPrimesInAPTarget

#check dirichletPrimesInAPTarget_iff_unbounded
#print axioms dirichletPrimesInAPTarget_iff_unbounded

end Stage1Instances.THM_M_0500
