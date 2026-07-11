import Mathlib.Tactic

/-!
# THM-M-0391 independent validation probe

This probe independently checks the exact type of the one obligation closed by
`Proof.lean`. It intentionally does not declare the open Mihailescu root.
-/

namespace Stage1Instances.THMM0391.Validation

/-- Independent reconstruction of frozen obligation `M0391-B-EE`. Unlike the
proof-phase body, this proof moves to integers and uses the factorization of a
difference of squares. -/
theorem independentEvenEvenImpossible {X Y : Nat}
    (_hX : 1 < X) (hY : 1 < Y) (hpow : X ^ 2 = Y ^ 2 + 1) : False := by
  have hsq : (X : Int) ^ 2 = (Y : Int) ^ 2 + 1 := by
    exact_mod_cast hpow
  have hy : (2 : Int) ≤ Y := by exact_mod_cast hY
  have hxy : (Y : Int) < X := by nlinarith
  have hgap : (1 : Int) ≤ X - Y := by omega
  have hsum : (4 : Int) ≤ X + Y := by omega
  have hmul : (4 : Int) ≤ (X - Y) * (X + Y) := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hgap) (sub_nonneg.mpr hsum)]
  nlinarith [hmul]

#check independentEvenEvenImpossible
#print axioms independentEvenEvenImpossible

end Stage1Instances.THMM0391.Validation
