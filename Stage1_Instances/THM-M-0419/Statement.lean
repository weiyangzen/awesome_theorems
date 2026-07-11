import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic

/-!
# THM-M-0419: Kronecker-Weber statement

This file freezes the containment form of the theorem. It defines a proposition
but does not assert that proposition or provide a proof of it.
-/

namespace Stage1.THM_M_0419

universe uK

/--
The Kronecker-Weber target for one presented finite abelian extension of `ℚ`.
The explicit local algebra instance fixes the splitting-field algebra structure
used by mathlib's cyclotomic-field API.
-/
def StatementShape
    (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
    [IsAbelianGalois ℚ K] : Prop :=
  ∃ n : ℕ, n ≠ 0 ∧
    letI : Algebra ℚ (CyclotomicField n ℚ) :=
      CyclotomicField.algebraBase n ℚ ℚ
    Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)

/-- Exact closed target, with the carrier and all structure binders explicit. -/
def Statement : Prop :=
  ∀ (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
      [IsAbelianGalois ℚ K],
    StatementShape K

/-- Checked expansion fixing binder order, scope, conductor boundary, and conclusion. -/
theorem statement_iff :
    Statement.{uK} ↔
      ∀ (K : Type uK) [Field K] [Algebra ℚ K] [NumberField K]
          [IsAbelianGalois ℚ K],
        ∃ n : ℕ, n ≠ 0 ∧
          letI : Algebra ℚ (CyclotomicField n ℚ) :=
            CyclotomicField.algebraBase n ℚ ℚ
          Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ) := by
  simp only [Statement, StatementShape]

#check Statement
#check StatementShape
set_option pp.universes true in
#print Statement

end Stage1.THM_M_0419
