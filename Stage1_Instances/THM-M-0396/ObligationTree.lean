import Statement

/-!
# THM-M-0396 conditional root composition

This module checks the binder-level composition between a parameterwise
Matveev estimate and the frozen canonical target.  `coreEstimate` is an
explicit premise: this file does not prove the analytic estimate.
-/

noncomputable section

open scoped BigOperators

namespace Stage1Rev56.THMM0396.ObligationTree

universe u

open Stage1Rev56.THMM0396

/-- The unresolved estimate after fixing all parameters of the root theorem. -/
def CoreEstimate (n : Nat) (K : Type u) [Field K] [NumberField K]
    (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
    (A : Fin n → Real) (B : Real) : Prop :=
  (1 ≤ n) →
  (∀ i, 0 < embedding (alpha i)) →
  (∀ i, max (Height.logHeight₁ (alpha i))
      |Real.log (embedding (alpha i))| ≤ A i) →
  (∀ i, (16 / 100 : Real) ≤ A i) →
  (1 : Real) ≤ B →
  (∀ i, (Int.natAbs (coeff i) : Real) ≤ B) →
  linearFormValue embedding alpha coeff ≠ 0 →
  -exponentBound n (Module.finrank Rat K : Real) B A <
    Real.log |linearFormValue embedding alpha coeff|

/-- Conditional certificate that the parameterwise terminal estimate yields
the exact frozen root, without an extra premise or a weakened conclusion. -/
theorem root_compose
    (core : ∀ (n : Nat) (K : Type u) [Field K] [NumberField K]
      (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
      (A : Fin n → Real) (B : Real),
      CoreEstimate n K embedding alpha coeff A B) : Statement.{u} := by
  intro n hn K _ _ embedding alpha coeff A B hpos hheight hA hB hcoeff hnonzero
  exact core n K embedding alpha coeff A B hn hpos hheight hA hB hcoeff hnonzero

theorem core_iff_statement :
    (∀ (n : Nat) (K : Type u) [Field K] [NumberField K]
      (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
      (A : Fin n → Real) (B : Real),
      CoreEstimate n K embedding alpha coeff A B) ↔ Statement.{u} := by
  constructor
  · exact root_compose
  · intro h n K _ _ embedding alpha coeff A B hn
    exact h n hn K embedding alpha coeff A B

#print root_compose
#print axioms root_compose

end Stage1Rev56.THMM0396.ObligationTree
