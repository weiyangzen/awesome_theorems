import Mathlib.MeasureTheory.Function.Holder

/-!
# THM-M-0310 statement infrastructure probe

This file checks only that the pinned environment exposes the concrete `Lp`, continuous-dual,
and Holder-pairing interfaces relevant to the intended theorem family. It is not a canonical
statement and contains no proof or assumed form of `Lp` duality.
-/

#check MeasureTheory.Lp
#check StrongDual
#check ContinuousLinearMap.lpPairing
#check ContinuousLinearMap.lpPairing_eq_integral
