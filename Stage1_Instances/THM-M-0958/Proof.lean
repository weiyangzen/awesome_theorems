import Statement
import Mathlib.Combinatorics.Additive.AP.Three.Behrend

/-!
# THM-M-0958 proof execution

This module installs the exact base-radix embedding subpackage used by the
frozen Elkin route. It proves injectivity, no-carry preservation of arithmetic
progressions, cardinality preservation, the numeric range bound, and the
one-based interval transport. It does not assert the open annulus,
discrepancy, or asymptotic witness packages.
-/

noncomputable section

open Finset

namespace Stage1Instances.THM_M_0958.Proof

/-- Pinned Behrend's base evaluator is injective on digit vectors whose
coordinates are strictly below half the radix. -/
theorem map_injOn_digit_box {k y : Nat} :
    Set.InjOn (Behrend.map (2 * y))
      {x : Fin k -> Nat | forall i, x i < y} := by
  exact Behrend.map_injOn.mono (by
    intro x hx i
    exact (hx i).trans_le (Nat.le_mul_of_pos_left y Nat.zero_lt_two))

/-- The pinned evaluator preserves addition. This is the algebraic interface
used by the no-carry argument. -/
theorem map_add_eq {k y : Nat} (x z : Fin k -> Nat) :
    Behrend.map (2 * y) (x + z) =
      Behrend.map (2 * y) x + Behrend.map (2 * y) z := by
  exact map_add (Behrend.map (2 * y)) x z

/-- If every coordinate is below `y`, sums of two coordinates are below the
radix `2 * y`. Hence a progression equation in the image lifts to the digit
vectors, and progression-freeness is preserved. -/
theorem map_image_threeAPFree {k y : Nat} {s : Finset (Fin k -> Nat)}
    (hdigits : forall x, x ∈ s -> forall i, x i < y)
    (hfree : ThreeAPFree (s : Set (Fin k -> Nat))) :
    ThreeAPFree ((s.image (Behrend.map (2 * y))) : Set Nat) := by
  rw [coe_image]
  apply ThreeAPFree.image' (Behrend.map (2 * y)) _ hfree
  intro a ha b hb hab
  obtain ⟨a1, ha1, a2, ha2, rfl⟩ := ha
  obtain ⟨b1, hb1, b2, hb2, rfl⟩ := hb
  exact Behrend.map_injOn
    (fun j => by
      change a1 j + a2 j < 2 * y
      have h1 := hdigits a1 ha1 j
      have h2 := hdigits a2 ha2 j
      omega)
    (fun j => by
      change b1 j + b2 j < 2 * y
      have h1 := hdigits b1 hb1 j
      have h2 := hdigits b2 hb2 j
      omega)
    (by simpa only [map_add] using hab)

/-- Injectivity on the digit box makes the finite image cardinality exact. -/
theorem card_map_image {k y : Nat} {s : Finset (Fin k -> Nat)}
    (hdigits : forall x, x ∈ s -> forall i, x i < y) :
    (s.image (Behrend.map (2 * y))).card = s.card := by
  apply Finset.card_image_of_injOn
  exact map_injOn_digit_box.mono (by
    intro x hx
    exact hdigits x hx)

/-- A `k`-digit vector with digits below `y` evaluates below `(2 * y)^k`.
The proof keeps the natural-number floor boundary explicit. -/
theorem map_image_lt_pow {k y : Nat} {s : Finset (Fin k -> Nat)}
    (hy : 0 < y)
    (hdigits : forall x, x ∈ s -> forall i, x i < y) :
    forall z, z ∈ s.image (Behrend.map (2 * y)) -> z < (2 * y) ^ k := by
  intro z hz
  obtain ⟨x, hx, rfl⟩ := Finset.mem_image.mp hz
  calc
    Behrend.map (2 * y) x
        <= ∑ i : Fin k, (y - 1) * (2 * y) ^ (i : Nat) := by
          change (∑ i : Fin k, x i * (2 * y) ^ (i : Nat)) <= _
          exact Finset.sum_le_sum (fun i _ =>
            Nat.mul_le_mul_right _ (Nat.le_sub_one_of_lt (hdigits x hx i)))
    _ < (2 * y) ^ k := by
      rw [Fin.sum_univ_eq_sum_range (fun i => (y - 1) * (2 * y) ^ i)]
      calc
        _ <= ∑ i ∈ Finset.range k, ((2 * y) - 1) * (2 * y) ^ i := by
          gcongr
          omega
        _ = (2 * y) ^ k - 1 := by
          rw [Finset.sum_congr rfl (fun i _ => mul_comm _ _), <- Finset.sum_mul,
            Nat.geomSum_eq (by omega), Nat.div_mul_cancel]
          exact Nat.sub_one_dvd_pow_sub_one (2 * y) k
        _ < (2 * y) ^ k := Nat.sub_one_lt (pow_ne_zero k (by omega))

/-- Shift the zero-based radix image by one to match the source interval. -/
def oneBasedDigitImage {k y : Nat} (s : Finset (Fin k -> Nat)) : Finset Nat :=
  (s.image (Behrend.map (2 * y))).image (1 + .)

/-- A fitting radix power places the shifted image in `{1, ..., n}`. -/
theorem oneBasedDigitImage_subset {k y n : Nat} {s : Finset (Fin k -> Nat)}
    (hy : 0 < y)
    (hdigits : forall x, x ∈ s -> forall i, x i < y)
    (hpow : (2 * y) ^ k <= n) :
    oneBasedDigitImage (y := y) s ⊆ Finset.Ico 1 (n + 1) := by
  intro z hz
  obtain ⟨w, hw, rfl⟩ := Finset.mem_image.mp hz
  rw [Finset.mem_Ico]
  constructor
  · omega
  · simpa [Nat.add_comm] using
      Nat.add_lt_add_right ((map_image_lt_pow hy hdigits w hw).trans_le hpow) 1

/-- The one-based shift also preserves the image cardinality. -/
theorem card_oneBasedDigitImage {k y : Nat} {s : Finset (Fin k -> Nat)}
    (hdigits : forall x, x ∈ s -> forall i, x i < y) :
    (oneBasedDigitImage (y := y) s).card = s.card := by
  rw [oneBasedDigitImage, Finset.card_image_of_injective _
      (fun _ _ h => Nat.add_left_cancel h), card_map_image hdigits]

/-- Translating by one preserves progression-freeness over naturals. -/
theorem oneBasedDigitImage_progressionFree {k y : Nat}
    {s : Finset (Fin k -> Nat)}
    (hdigits : forall x, x ∈ s -> forall i, x i < y)
    (hfree : ThreeAPFree (s : Set (Fin k -> Nat))) :
    ThreeAPFree (oneBasedDigitImage (y := y) s : Set Nat) := by
  rw [oneBasedDigitImage, coe_image]
  rintro _ ⟨a, ha, rfl⟩ _ ⟨b, hb, rfl⟩ _ ⟨c, hc, rfl⟩ habc
  apply congrArg (1 + .)
  apply map_image_threeAPFree hdigits hfree ha hb hc
  change 1 + a + (1 + c) = 1 + b + (1 + b) at habc
  omega

/-- Exact typed input to the checked digit-embedding composition. The hard
construction route must produce this package; it is not manufactured here. -/
structure DigitEmbeddingPackage (k y n : Nat)
    (s : Finset (Fin k -> Nat)) : Prop where
  digits : forall x, x ∈ s -> forall i, x i < y
  y_pos : 0 < y
  radix_fits : (2 * y) ^ k <= n
  vector_progression_free : ThreeAPFree (s : Set (Fin k -> Nat))

/-- Exact local composition for the new radix embedding subpackage. It
consumes the digit, positivity, range, and vector-freeness children and returns
a one-based finite progression-free set with unchanged cardinality. This is
not a closure certificate for the broader frozen prose-level parent. -/
theorem digitEmbeddingPackage_checked {k y n : Nat}
    {s : Finset (Fin k -> Nat)} (h : DigitEmbeddingPackage k y n s) :
    exists t : Finset Nat,
      t ⊆ Finset.Ico 1 (n + 1) /\
      ThreeAPFree (t : Set Nat) /\
      t.card = s.card := by
  exact ⟨oneBasedDigitImage (y := y) s,
    oneBasedDigitImage_subset h.y_pos h.digits h.radix_fits,
    oneBasedDigitImage_progressionFree h.digits h.vector_progression_free,
    card_oneBasedDigitImage h.digits⟩

#print axioms map_injOn_digit_box
#print axioms map_add_eq
#print axioms map_image_threeAPFree
#print axioms card_map_image
#print axioms map_image_lt_pow
#print axioms oneBasedDigitImage_subset
#print axioms card_oneBasedDigitImage
#print axioms oneBasedDigitImage_progressionFree
#print axioms digitEmbeddingPackage_checked

end Stage1Instances.THM_M_0958.Proof
