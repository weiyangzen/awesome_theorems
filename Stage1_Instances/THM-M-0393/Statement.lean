import Mathlib.RingTheory.MvPolynomial.Homogeneous

/-!
# THM-M-0393: canonical statement of Thue's theorem

This module freezes only the exact target. It does not assert or prove the target.
-/

namespace Stage1.THM_M_0393

/-- Evaluate an integral binary form at an ordered pair of integers. -/
def evalBinary (F : MvPolynomial (Fin 2) Int) (p : Int × Int) : Int :=
  MvPolynomial.eval (fun i => if i = 0 then p.1 else p.2) F

/-- The integral solutions of the Thue equation `F(x,y) = m`. -/
def solutionSet (F : MvPolynomial (Fin 2) Int) (m : Int) : Set (Int × Int) :=
  {p | evalBinary F p = m}

/--
The canonical Lean target for Thue's theorem: for a nonzero integer `m`, an
integral homogeneous binary form of degree at least three which is irreducible
after extension of coefficients to `ℚ` has only finitely many integral
solutions to `F(x,y) = m`.
-/
def ThueStatement : Prop :=
  ∀ (n : Nat) (F : MvPolynomial (Fin 2) Int) (m : Int),
    3 ≤ n →
    F.IsHomogeneous n →
    Irreducible (F.map (Int.castRingHom Rat)) →
    m ≠ 0 →
    (solutionSet F m).Finite

/-- Checked unfolding of membership in the canonical solution set. -/
theorem mem_solutionSet_iff (F : MvPolynomial (Fin 2) Int) (m : Int) (p : Int × Int) :
    p ∈ solutionSet F m ↔ evalBinary F p = m :=
  Iff.rfl

/-- Exact-type fixture: changes to any canonical binder or hypothesis break this check. -/
theorem thueStatement_exact_type :
    ThueStatement =
      (∀ (n : Nat) (F : MvPolynomial (Fin 2) Int) (m : Int),
        3 ≤ n →
        F.IsHomogeneous n →
        Irreducible (F.map (Int.castRingHom Rat)) →
        m ≠ 0 →
        (solutionSet F m).Finite) :=
  rfl

end Stage1.THM_M_0393
