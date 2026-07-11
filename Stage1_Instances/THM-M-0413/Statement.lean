import Mathlib.NumberTheory.NumberField.Basic

/-!
The exact rev-5.6 statement for THM-M-0413. This module intentionally imports only the mathlib
module that defines number fields, their rings of integers, and the relevant Dedekind instance.
-/

namespace Stage1.THMM0413

universe u

open scoped NumberField

/-- For every number field, its ring of integers is a Dedekind domain. -/
def Statement : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K], IsDedekindDomain (NumberField.RingOfIntegers K)

/-- Checked transport between the named ring of integers and its defining integral closure. -/
theorem statement_iff_integralClosure :
    Statement.{u} ↔
      ∀ (K : Type u) [Field K] [NumberField K],
        IsDedekindDomain (integralClosure ℤ K) :=
  by
    constructor <;> intro h <;> exact h

/-- `K = ℚ` is an included degree-one boundary case, not an excluded special case. -/
example : IsDedekindDomain (NumberField.RingOfIntegers ℚ) := by
  infer_instance

#check Statement
#check statement_iff_integralClosure
set_option pp.universes true in
#print Statement

end Stage1.THMM0413
