import Mathlib.Algebra.Field.Basic
import Mathlib.GroupTheory.OrderOfElement

/-!
# THM-M-0403: canonical Schlickewei--Evertse statement

This module freezes and elaborates only the exact simple nondegenerate
exponential-polynomial zero-finiteness target. It does not prove that target.
-/

open scoped BigOperators

namespace Stage1.THM_M_0403

universe u

/-- The coefficients and characteristic roots of a simple exponential polynomial. -/
structure ExponentialPolynomialData (K : Type u) [Field K] (r : Nat) where
  coeff : Fin r -> K
  root : Fin r -> K
  coeff_ne_zero : forall i, coeff i ≠ 0
  root_ne_zero : forall i, root i ≠ 0
  ratio_nontorsion : forall i j, i ≠ j -> ¬ IsOfFinOrder (root i / root j)

/-- Evaluate the exponential polynomial at a natural-number index. -/
def ExponentialPolynomialData.eval {K : Type u} [Field K] {r : Nat}
    (D : ExponentialPolynomialData K r) (n : Nat) : K :=
  Finset.univ.sum (fun i => D.coeff i * D.root i ^ n)

/-- The natural-number zero indices of an exponential polynomial. -/
def zeroSet {K : Type u} [Field K] {r : Nat}
    (D : ExponentialPolynomialData K r) : Set Nat :=
  {n | D.eval n = 0}

/--
The exact Lean target: over any characteristic-zero field, a nonempty simple
exponential polynomial with nonzero coefficients and roots and nontorsion
quotients between distinct roots has only finitely many natural-number zeros.
-/
def SchlickeweiEvertseStatement (K : Type u) [Field K] [CharZero K] : Prop :=
  forall r : Nat, 0 < r ->
    forall D : ExponentialPolynomialData K r, (zeroSet D).Finite

/-- Checked unfolding of membership in the canonical zero set. -/
theorem mem_zeroSet_iff {K : Type u} [Field K] {r : Nat}
    (D : ExponentialPolynomialData K r) (n : Nat) :
    n ∈ zeroSet D <-> D.eval n = 0 :=
  Iff.rfl

/-- Exact-type fixture: changing a canonical binder or hypothesis breaks this check. -/
theorem schlickeweiEvertseStatement_exact_type
    (K : Type u) [Field K] [CharZero K] :
    SchlickeweiEvertseStatement K =
      (forall r : Nat, 0 < r ->
        forall D : ExponentialPolynomialData K r, (zeroSet D).Finite) :=
  rfl

end Stage1.THM_M_0403
