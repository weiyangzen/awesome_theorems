import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.NumberTheory.Real.GoldenRatio

/-!
# THM-M-1441 discovery-only intake probe

These checks authenticate pinned interfaces that could occur in a future secant-method statement.
They do not select a catalog proposition, define the secant recurrence, or prove THM-M-1441.
-/

#check Asymptotics.IsLittleO
#check Asymptotics.isLittleO_iff
#check Filter.Tendsto
#check Filter.atTop
#check Real.goldenRatio
#check Real.one_lt_goldenRatio
#check div_ne_zero
#check Function.iterate_succ_apply
