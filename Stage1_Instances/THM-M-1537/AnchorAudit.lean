import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Data.Real.Basic

/-!
# THM-M-1537 pinned anchor probes

These declarations are entropy and real-arithmetic substrate in the pinned
mathlib snapshot. None states the Bekenstein-Hawking area law or relates a
black-hole entropy to horizon area.
-/

#check Real.binEntropy
#check Real.binEntropy_nonneg
#check Real.binEntropy_le_log_two
#check Real.binEntropy_continuous
#check Real.log
#check div_eq_mul_inv
