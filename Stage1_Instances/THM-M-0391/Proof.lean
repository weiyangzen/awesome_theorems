import Mathlib.Tactic

/-!
# THM-M-0391 proof execution

This module contains genuine proof bodies completed during the rev-5.6 proof
phase. It deliberately does not declare the still-open Mihailescu root.
-/

namespace Stage1Instances.THMM0391.Proof

/-- The even/even normalized branch is impossible: two nontrivial natural
squares cannot differ by one. This closes frozen obligation `M0391-B-EE`.
-/
theorem evenEvenImpossible {X Y : Nat}
    (_hX : 1 < X) (hY : 1 < Y) (hpow : X ^ 2 = Y ^ 2 + 1) : False := by
  have hyx : Y < X := by
    by_contra h
    have hxy : X ≤ Y := Nat.le_of_not_gt h
    have hsquares : X ^ 2 ≤ Y ^ 2 := Nat.pow_le_pow_left hxy 2
    omega
  have hsucc : Y + 1 ≤ X := Nat.succ_le_iff.mpr hyx
  have hsquares : (Y + 1) ^ 2 ≤ X ^ 2 := Nat.pow_le_pow_left hsucc 2
  have hexpand : (Y + 1) ^ 2 = Y ^ 2 + 2 * Y + 1 := by ring
  omega

#print axioms evenEvenImpossible

end Stage1Instances.THMM0391.Proof
