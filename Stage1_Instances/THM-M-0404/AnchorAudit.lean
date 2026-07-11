import Mathlib.Algebra.LinearRecurrence

/-!
# THM-M-0404: pinned anchor probes

This file checks the declarations retained by the rev-5.6 anchor audit. The
mathlib declarations are recurrence infrastructure, not a proof of the
Skolem-Mahler-Lech target.
-/

#check LinearRecurrence
#check LinearRecurrence.IsSolution
#check LinearRecurrence.mkSol
#check LinearRecurrence.is_sol_mkSol
#check LinearRecurrence.eq_mk_of_is_sol_of_eq_init
#check LinearRecurrence.solSpace
#check LinearRecurrence.toInit
#check LinearRecurrence.tupleSucc
#check LinearRecurrence.charPoly
#check LinearRecurrence.charPoly_monic
#check LinearRecurrence.geom_sol_iff_root_charPoly
