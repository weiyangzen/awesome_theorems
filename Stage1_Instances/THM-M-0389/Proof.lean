import Mathlib

/-!
# THM-M-0389: proof bodies

This module proves the three mathematical inputs frozen by the obligation tree
and composes them into the exact statement from `Statement.lean`.
-/

namespace Stage1Instances.THM_M_0389

def MarkovEquation (x y z : Int) : Prop :=
  x ^ 2 + y ^ 2 + z ^ 2 = 3 * x * y * z

inductive GeneratedMarkovTriple : Int -> Int -> Int -> Prop
  | seed : GeneratedMarkovTriple 1 1 1
  | swapXY {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple y x z
  | swapYZ {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x z y
  | mutateX {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple (3 * y * z - x) y z
  | mutateY {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x (3 * x * z - y) z
  | mutateZ {x y z} : GeneratedMarkovTriple x y z -> GeneratedMarkovTriple x y (3 * x * y - z)

def EvenSignVariant (x y z a b c : Int) : Prop :=
  (x = a /\ y = b /\ z = c) \/ (x = a /\ y = -b /\ z = -c) \/
  (x = -a /\ y = b /\ z = -c) \/ (x = -a /\ y = -b /\ z = c)

def IntegerMarkovClassification : Prop :=
  forall x y z : Int, MarkovEquation x y z ->
    (x = 0 /\ y = 0 /\ z = 0) \/
    exists a b c : Int, GeneratedMarkovTriple a b c /\ EvenSignVariant x y z a b c

private theorem zero_of_zero_coordinate {x y z : Int}
    (h : MarkovEquation x y z) (hz : x = 0 \/ y = 0 \/ z = 0) :
    x = 0 /\ y = 0 /\ z = 0 := by
  unfold MarkovEquation at h
  rcases hz with hx0eq | hy0eq | hz0eq
  · subst x
    have hy0 : y = 0 := by nlinarith [sq_nonneg y, sq_nonneg z]
    have hz0 : z = 0 := by nlinarith [sq_nonneg y, sq_nonneg z]
    exact ⟨rfl, hy0, hz0⟩
  · subst y
    have hx0 : x = 0 := by nlinarith [sq_nonneg x, sq_nonneg z]
    have hz0 : z = 0 := by nlinarith [sq_nonneg x, sq_nonneg z]
    exact ⟨hx0, rfl, hz0⟩
  · subst z
    have hx0 : x = 0 := by nlinarith [sq_nonneg x, sq_nonneg y]
    have hy0 : y = 0 := by nlinarith [sq_nonneg x, sq_nonneg y]
    exact ⟨hx0, hy0, rfl⟩

private theorem markov_abs {x y z : Int} (h : MarkovEquation x y z)
    (hp : 0 < x * y * z) :
    MarkovEquation |x| |y| |z| := by
  unfold MarkovEquation at h ⊢
  rw [sq_abs, sq_abs, sq_abs, h]
  have habs : |x| * |y| * |z| = x * y * z := by
    rw [← abs_mul, ← abs_mul, abs_of_pos hp]
  nlinarith

private theorem evenSign_abs {x y z : Int}
    (hp : 0 < x * y * z) : EvenSignVariant x y z |x| |y| |z| := by
  unfold EvenSignVariant
  have hx : x ≠ 0 := by intro h; simp [h] at hp
  have hy : y ≠ 0 := by intro h; simp [h] at hp
  have hz : z ≠ 0 := by intro h; simp [h] at hp
  rcases lt_or_gt_of_ne hx with hxneg | hxpos
  · rcases lt_or_gt_of_ne hy with hyneg | hypos
    · have hzpos : 0 < z := by
        by_contra hn
        have hznonpos : z ≤ 0 := le_of_not_gt hn
        have hxypos : 0 < x * y := mul_pos_of_neg_of_neg hxneg hyneg
        exact (not_lt_of_ge (mul_nonpos_of_nonneg_of_nonpos (le_of_lt hxypos) hznonpos)) hp
      right; right; right
      simp [abs_of_neg hxneg, abs_of_neg hyneg, abs_of_pos hzpos]
    · have hzneg : z < 0 := by
        by_contra hn
        have : 0 ≤ z := le_of_not_gt hn
        exact (not_lt_of_ge (mul_nonpos_of_nonpos_of_nonneg (mul_nonpos_of_nonpos_of_nonneg (le_of_lt hxneg) (le_of_lt hypos)) this)) hp
      right; right; left
      simp [abs_of_neg hxneg, abs_of_pos hypos, abs_of_neg hzneg]
  · rcases lt_or_gt_of_ne hy with hyneg | hypos
    · have hzneg : z < 0 := by
        by_contra hn
        have : 0 ≤ z := le_of_not_gt hn
        exact (not_lt_of_ge (mul_nonpos_of_nonpos_of_nonneg (mul_nonpos_of_nonneg_of_nonpos (le_of_lt hxpos) (le_of_lt hyneg)) this)) hp
      right; left
      simp [abs_of_pos hxpos, abs_of_neg hyneg, abs_of_neg hzneg]
    · have hzpos : 0 < z := by
        by_contra hn
        have : z ≤ 0 := le_of_not_gt hn
        exact (not_lt_of_ge (mul_nonpos_of_nonneg_of_nonpos (mul_nonneg (le_of_lt hxpos) (le_of_lt hypos)) this)) hp
      left
      simp [abs_of_pos hxpos, abs_of_pos hypos, abs_of_pos hzpos]

private theorem orderedGeneration (x y z : Int)
    (hx : 0 < x) (hxy : x ≤ y) (hyz : y ≤ z) (h : MarkovEquation x y z) :
    GeneratedMarkovTriple x y z := by
  by_cases hseed : x = 1 /\ y = 1 /\ z = 1
  · rcases hseed with ⟨rfl, rfl, rfl⟩; exact .seed
  · let z' := 3 * x * y - z
    have hy : 0 < y := lt_of_lt_of_le hx hxy
    have hz : 0 < z := lt_of_lt_of_le hy hyz
    have hEq : x ^ 2 + y ^ 2 + z ^ 2 = 3 * x * y * z := h
    have hprod : z * z' = x ^ 2 + y ^ 2 := by dsimp [z']; nlinarith
    have hz' : 0 < z' := by
      by_contra hn
      have : z * z' ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hz) (le_of_not_gt hn)
      nlinarith [sq_pos_of_pos hx, sq_nonneg y]
    have hz'le : z' ≤ y := by
      by_contra hn
      have hylt : y < z' := lt_of_not_ge hn
      have hx1 : 1 ≤ x := by omega
      have hpoly : x ^ 2 + 2 * y ^ 2 - 3 * x * y ^ 2 ≤ 0 := by
        nlinarith [mul_nonneg (show 0 ≤ x - 1 by omega) (sq_nonneg y),
          mul_nonneg (show 0 ≤ y - x by omega) (show 0 ≤ x + y by omega)]
      have hsum : z + z' = 3 * x * y := by dsimp [z']; ring
      have hzlt : y < z := by
        by_contra hzy
        have hyzEq : y = z := le_antisymm hyz (le_of_not_gt hzy)
        subst z
        have hxEq : x = 1 := by
          by_contra hxne
          have hx2 : 2 ≤ x := by omega
          have hlarge : x ^ 2 < (3 * x - 2) * y ^ 2 := by
            nlinarith [mul_nonneg (show 0 ≤ y - x by omega) (show 0 ≤ y + x by omega),
              mul_pos (show 0 < 3 * x - 3 by omega) (sq_pos_of_pos hy)]
          nlinarith
        subst x
        have hyEq : y = 1 := by nlinarith [sq_nonneg (y - 1)]
        exact hseed ⟨rfl, hyEq, hyEq⟩
      have : 0 < (z - y) * (z' - y) := mul_pos (by omega) (by omega)
      nlinarith
    have hz'lt : z' < z := by
      by_contra hn
      have : z ≤ z' := le_of_not_gt hn
      have hzy : z ≤ y := le_trans this hz'le
      have hyzEq : y = z := le_antisymm hyz hzy
      subst z
      have hzEq : z' = y := le_antisymm hz'le this
      dsimp [z'] at hzEq
      have hx1 : 1 ≤ x := by omega
      have hy1 : 1 ≤ y := by omega
      have hxyOne : x = 1 /\ y = 1 := by nlinarith [sq_nonneg (y - x)]
      exact hseed ⟨hxyOne.1, hxyOne.2, hxyOne.2⟩
    have hdesc : MarkovEquation x y z' := by
      unfold MarkovEquation at h ⊢
      dsimp [z']
      nlinarith
    have hgenDesc : GeneratedMarkovTriple x y z' := by
      by_cases hxz' : x ≤ z'
      · have ih := orderedGeneration x z' y hx hxz' hz'le
          (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using hdesc)
        exact .swapYZ ih
      · have ih := orderedGeneration z' x y hz' (le_of_not_ge hxz') hxy
          (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using hdesc)
        exact .swapYZ (.swapXY ih)
    have hm := GeneratedMarkovTriple.mutateZ hgenDesc
    simpa [z'] using hm
termination_by (x + y + z).toNat
decreasing_by
  all_goals
    exact (Int.toNat_lt_toNat (by omega)).mpr (by omega)

private theorem positiveGeneration {x y z : Int}
    (h : MarkovEquation x y z) (hp : 0 < x /\ 0 < y /\ 0 < z) :
    GeneratedMarkovTriple x y z := by
  rcases hp with ⟨hx, hy, hz⟩
  by_cases hxy : x ≤ y
  · by_cases hyz : y ≤ z
    · exact orderedGeneration x y z hx hxy hyz h
    · by_cases hxz : x ≤ z
      · exact .swapYZ (orderedGeneration x z y hx hxz (le_of_not_ge hyz)
          (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using h))
      · exact .swapYZ (.swapXY (orderedGeneration z x y hz (le_of_not_ge hxz) hxy
          (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using h)))
  · by_cases hxz : x ≤ z
    · exact .swapXY (orderedGeneration y x z hy (le_of_not_ge hxy) hxz
        (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using h))
    · by_cases hyz : y ≤ z
      · exact .swapXY (.swapYZ (orderedGeneration y z x hy hyz (le_of_not_ge hxz)
          (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using h)))
      · exact .swapXY (.swapYZ (.swapXY (orderedGeneration z y x hz (le_of_not_ge hyz) (le_of_not_ge hxy)
          (by simpa [MarkovEquation, add_comm, add_left_comm, add_assoc, mul_comm, mul_left_comm, mul_assoc] using h))))

theorem integerMarkovClassification : IntegerMarkovClassification := by
  intro x y z h
  by_cases hz : x = 0 \/ y = 0 \/ z = 0
  · exact Or.inl (zero_of_zero_coordinate h hz)
  · have hxyz : 0 < x * y * z := by
      have heq : x ^ 2 + y ^ 2 + z ^ 2 = 3 * (x * y * z) := by
        simpa [MarkovEquation, mul_assoc] using h
      have hx : x ≠ 0 := by intro hx; exact hz (Or.inl hx)
      have : 0 < x ^ 2 + y ^ 2 + z ^ 2 := by nlinarith [sq_pos_of_ne_zero hx]
      nlinarith
    refine Or.inr ⟨|x|, |y|, |z|, ?_, evenSign_abs hxyz⟩
    apply positiveGeneration (markov_abs h hxyz)
    exact ⟨abs_pos.mpr (by aesop), abs_pos.mpr (by aesop), abs_pos.mpr (by aesop)⟩

#print axioms integerMarkovClassification

end Stage1Instances.THM_M_0389
