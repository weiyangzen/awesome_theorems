import Mathlib.NumberTheory.Height.NumberField
import Mathlib.Analysis.SpecialFunctions.Complex.Log

/-!
# THM-M-0396 anchor-audit substrate check

This file checks only the pinned mathlib APIs used by the frozen statement and
by plausible future bridges. It deliberately contains no Baker/Matveev theorem
declaration: the pinned source audit found no terminal lower-bound candidate.
-/

#check Height.logHeight₁
#check NumberField
#check Complex.exp
#check Complex.log
#check Module.finrank

