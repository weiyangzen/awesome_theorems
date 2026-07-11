import Mathlib.Data.Int.Basic
import Mathlib.Data.Int.Interval

/-!
# THM-M-0393 independent validation probe

This module independently reconstructs the finite-choice subclaim implemented
in `Proof.lean`. It deliberately does not import that module or assert the open
Thue root.
-/

namespace Stage1.THM_M_0393.Validation

/-- Independent replay of the finite scale-factor claim from `M0393-N1`. -/
theorem independent_finite_pow_divisors
    (n : Nat) (m : Int) (hn : 0 < n) (hm : m ≠ 0) :
    {g : Int | g ^ n ∣ m}.Finite := by
  refine (Set.finite_Icc (-m.natAbs : Int) m.natAbs).subset ?_
  intro g hdiv
  have hpower : g.natAbs ^ n <= m.natAbs := by
    simpa [Int.natAbs_pow] using Int.natAbs_le_of_dvd_ne_zero hdiv hm
  have habs : g.natAbs <= m.natAbs :=
    (Nat.le_pow hn).trans hpower
  constructor
  · have hsign : (-g.natAbs : Int) <= g := by
      rcases Int.natAbs_eq g with h | h <;> omega
    have hmono : (-m.natAbs : Int) <= -g.natAbs := by
      have : (g.natAbs : Int) <= m.natAbs := Int.ofNat_le.mpr habs
      omega
    exact hmono.trans hsign
  · have hsign : g <= (g.natAbs : Int) := by
      rcases Int.natAbs_eq g with h | h <;> omega
    exact hsign.trans (Int.ofNat_le.mpr habs)

#print axioms independent_finite_pow_divisors

end Stage1.THM_M_0393.Validation
