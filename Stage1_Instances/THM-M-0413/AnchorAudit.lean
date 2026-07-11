import Mathlib.NumberTheory.NumberField.Basic

/-!
Kernel probes for the rev-5.6 anchor audit of THM-M-0413. The two wrappers deliberately name
both the number-field instance and its terminal integral-closure theorem rather than relying only
on an opaque typeclass search result.
-/

namespace Stage1.THMM0413.AnchorAudit

universe u

open scoped NumberField

/-- Exact mathlib instance anchor for the frozen target. -/
theorem viaNumberFieldInstance (K : Type u) [Field K] [NumberField K] :
    IsDedekindDomain (NumberField.RingOfIntegers K) :=
  NumberField.RingOfIntegers.instIsDedekindDomain K

/-- Terminal generic theorem used by the number-field instance. -/
theorem viaIntegralClosureTheorem (K : Type u) [Field K] [NumberField K] :
    IsDedekindDomain (NumberField.RingOfIntegers K) :=
  IsIntegralClosure.isDedekindDomain ℤ ℚ K (NumberField.RingOfIntegers K)

#check NumberField.RingOfIntegers.instIsDedekindDomain
#check IsIntegralClosure.isDedekindDomain
#print NumberField.RingOfIntegers.instIsDedekindDomain
#print IsIntegralClosure.isDedekindDomain
#print axioms NumberField.RingOfIntegers.instIsDedekindDomain
#print axioms IsIntegralClosure.isDedekindDomain
#print axioms viaNumberFieldInstance
#print axioms viaIntegralClosureTheorem

end Stage1.THMM0413.AnchorAudit
