import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.RamificationInertia.Unramified

/-!
# THM-M-0420: pinned mathlib anchor probes

These declarations support the frozen Hilbert class field statement. None
constructs a Hilbert class field or proves global Artin reciprocity.
-/

#check ClassGroup
#check NumberField.classNumber
#check NumberField.classNumber_ne_zero
#check NumberField.classNumber_pos
#check Algebra.IsUnramifiedAt
#check Algebra.isUnramifiedAt_iff_of_isDedekindDomain
#check Ideal.ramificationIdx
#check Ideal.primesOver
#check IsGalois
#check AlgEquiv
