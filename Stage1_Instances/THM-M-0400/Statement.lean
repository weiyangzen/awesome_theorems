import Mathlib.FieldTheory.IsAlgClosed.Basic
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# THM-M-0400: Schmidt's Subspace Theorem (statement)

The archimedean product-of-linear-forms formulation over integer vectors.
This file freezes and elaborates the proposition; it does not prove it.
-/

namespace Stage1Rev56.THMM0400

/-- Supremum height of an integer vector. -/
def integerHeight {n : Nat} (x : Fin n → Int) : Real :=
  ((Finset.univ.sup fun j => Int.natAbs (x j) : Nat) : Real)

/-- Evaluation of a complex linear form on an integer vector. -/
noncomputable def evalLinearForm {n : Nat} (a : Fin n → Complex)
    (x : Fin n → Int) : Complex :=
  ∑ j, a j * ((x j : Int) : Complex)

/-- The rational vector represented by an integer vector. -/
def rationalVector {n : Nat} (x : Fin n → Int) : Fin n → Rat :=
  fun j => (x j : Rat)

/--
Schmidt's Subspace Theorem in its standard archimedean product form: for
linearly independent algebraic linear forms and every positive `epsilon`, all
nonzero integral solutions of the product inequality lie in finitely many
proper rational linear subspaces.
-/
def Statement : Prop :=
  ∀ (n : Nat), 2 ≤ n → ∀ (coeff : Fin n → Fin n → Complex),
    (∀ i j, IsAlgebraic Rat (coeff i j)) →
    LinearIndependent Complex coeff →
    ∀ epsilon : Real, 0 < epsilon →
      ∃ exceptional : Finset (Submodule Rat (Fin n → Rat)),
        (∀ V ∈ exceptional, V ≠ ⊤) ∧
        ∀ x : Fin n → Int, x ≠ 0 →
          (∏ i, ‖evalLinearForm (coeff i) x‖) < Real.rpow (integerHeight x) (-epsilon) →
          ∃ V ∈ exceptional, rationalVector x ∈ V

#check Statement

end Stage1Rev56.THMM0400
