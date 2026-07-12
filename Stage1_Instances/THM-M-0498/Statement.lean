import Mathlib.NumberTheory.Chebyshev
import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.Analysis.Meromorphic.Order

/-!
# THM-M-0498: exact Riemann-von Mangoldt explicit-formula target

This module freezes the statement boundary only. It does not prove the
explicit formula.
-/

noncomputable section

open Filter Nat
open scoped Topology

namespace Stage1Instances.THM_M_0498

/-- A nontrivial zeta zero, with the open critical strip made explicit. -/
def IsNontrivialZetaZero (z : ℂ) : Prop :=
  riemannZeta z = 0 ∧ 0 < z.re ∧ z.re < 1

/-- Data specifying a multiplicity-weighted enumeration of all nontrivial
zeros. `heightOrdered` fixes the symmetric limiting convention: absolute
imaginary parts never decrease. -/
structure NontrivialZeroEnumeration where
  zero : Nat → ℂ
  multiplicity : Nat → Nat
  isZero : ∀ n, IsNontrivialZetaZero (zero n)
  multiplicity_pos : ∀ n, 0 < multiplicity n
  multiplicity_eq_order : ∀ n,
    meromorphicOrderAt riemannZeta (zero n) = (multiplicity n : ℤ)
  zero_injective : Function.Injective zero
  complete : ∀ z, IsNontrivialZetaZero z → ∃ n, zero n = z
  heightOrdered : ∀ m n, m ≤ n → |(zero m).im| ≤ |(zero n).im|

/-- `x` is not a prime-power discontinuity of `Chebyshev.psi`. -/
def IsNotPrimePower (x : ℝ) : Prop :=
  ∀ p k : Nat, p.Prime → 0 < k → x ≠ (p ^ k : Nat)

/-- The multiplicity-weighted partial sum over nontrivial zeta zeros. -/
def zeroPartialSum (E : NontrivialZeroEnumeration) (x : ℝ) (N : Nat) : ℂ :=
  ∑ n ∈ Finset.range N,
    (E.multiplicity n : ℂ) * (x : ℂ) ^ (E.zero n) / E.zero n

/-- The canonical weighted-prime-power Riemann-von Mangoldt formula.

It uses mathlib's right-continuous `Chebyshev.psi`, excludes its prime-power
discontinuities, counts every nontrivial zero with the supplied multiplicity,
and takes partial sums in nondecreasing absolute imaginary height. -/
def RiemannVonMangoldtTarget : Prop :=
  ∀ (E : NontrivialZeroEnumeration) (x : ℝ),
    1 < x → IsNotPrimePower x →
      Tendsto (fun N : Nat ↦
        (x : ℂ) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
          (1 / 2 : ℂ) * Complex.log (1 - (x : ℂ) ^ (-2 : ℂ)))
        atTop (nhds (Chebyshev.psi x : ℂ))

/-- An expanded encoding used to check the public target without an
abbreviation boundary. -/
def ExpandedTarget : Prop :=
  ∀ (E : NontrivialZeroEnumeration) (x : ℝ),
    1 < x →
      (∀ p k : Nat, p.Prime → 0 < k → x ≠ (p ^ k : Nat)) →
        Tendsto (fun N : Nat ↦
          (x : ℂ) - (∑ n ∈ Finset.range N,
            (E.multiplicity n : ℂ) * (x : ℂ) ^ (E.zero n) / E.zero n) -
            Complex.log (2 * Real.pi) -
            (1 / 2 : ℂ) * Complex.log (1 - (x : ℂ) ^ (-2 : ℂ)))
          atTop (nhds (Chebyshev.psi x : ℂ))

theorem target_iff_expanded : RiemannVonMangoldtTarget ↔ ExpandedTarget := by
  rfl

-- Structural mutations separately elaborated and rejected by check_statement.py.
def mutationRemovedLowerBound : Prop :=
  ∀ (E : NontrivialZeroEnumeration) (x : ℝ), IsNotPrimePower x →
    Tendsto (fun N : Nat ↦
      (x : ℂ) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
        (1 / 2 : ℂ) * Complex.log (1 - (x : ℂ) ^ (-2 : ℂ)))
      atTop (nhds (Chebyshev.psi x : ℂ))

def mutationChangedDomain : Prop :=
  ∀ (E : NontrivialZeroEnumeration) (x : Nat),
    1 < x → IsNotPrimePower x →
      Tendsto (fun N : Nat ↦
        (x : ℂ) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
          (1 / 2 : ℂ) * Complex.log (1 - (x : ℂ) ^ (-2 : ℂ)))
        atTop (nhds (Chebyshev.psi x : ℂ))

def mutationChangedBinderScope : Prop :=
  ∀ x : ℝ, 1 < x → IsNotPrimePower x →
    ∀ E : NontrivialZeroEnumeration,
      Tendsto (fun N : Nat ↦
        (x : ℂ) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
          (1 / 2 : ℂ) * Complex.log (1 - (x : ℂ) ^ (-2 : ℂ)))
        atTop (nhds (Chebyshev.psi x : ℂ))

def mutationIncludesPrimePowers : Prop :=
  ∀ (E : NontrivialZeroEnumeration) (x : ℝ), 1 < x →
    Tendsto (fun N : Nat ↦
      (x : ℂ) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
        (1 / 2 : ℂ) * Complex.log (1 - (x : ℂ) ^ (-2 : ℂ)))
      atTop (nhds (Chebyshev.psi x : ℂ))

end Stage1Instances.THM_M_0498

set_option pp.explicit true in
#print Stage1Instances.THM_M_0498.RiemannVonMangoldtTarget
