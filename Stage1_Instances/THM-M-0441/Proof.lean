import ObligationTree

/-!
# THM-M-0441 partial proof execution

This module closes elementary definitional and bounded-height finiteness leaves
without assuming any of the open Pila-Wilkie parameterization, determinant,
block-decomposition, or dimension-induction packages.
-/

open FirstOrder Set

namespace Stage1Instances.THM_M_0441.Proof

open Stage1Instances.THM_M_0441
open Stage1Instances.THM_M_0441.ObligationTree

/-- A connected, nontrivial semialgebraic subset of `X` lies in the algebraic
part by its defining existential witness. -/
theorem subset_algebraicPart_of_semialgebraic_preconnected_nontrivial
    {A X : Set (Fin n -> Real)} (hAX : A <= X) (hSA : IsSemialgebraic A)
    (hPre : IsPreconnected A) (hNontrivial : A.Nontrivial) :
    A <= algebraicPart X := by
  intro x hx
  exact ⟨A, hAX, hSA, hPre, hNontrivial, hx⟩

/-- The algebraic part is contained in its ambient set. -/
theorem algebraicPart_subset (X : Set (Fin n -> Real)) :
    algebraicPart X <= X := by
  rintro x ⟨A, hAX, _hSA, _hPre, _hNontrivial, hx⟩
  exact hAX hx

/-- The frozen algebraic-part construction is monotone. -/
theorem algebraicPart_mono {X Y : Set (Fin n -> Real)} (hXY : X <= Y) :
    algebraicPart X <= algebraicPart Y := by
  rintro x ⟨A, hAX, hSA, hPre, hNontrivial, hx⟩
  exact ⟨A, hAX.trans hXY, hSA, hPre, hNontrivial, hx⟩

/-- The normalized numerator-denominator representation embeds rationals into
integer pairs. -/
def normalizedRatPair (q : Rat) : Int × Int :=
  (q.num, (q.den : Int))

theorem normalizedRatPair_injective : Function.Injective normalizedRatPair := by
  intro r s h
  apply Rat.ext
  · exact congrArg Prod.fst h
  · have hden : ((r.den : Int) = (s.den : Int)) := by
      simpa [normalizedRatPair] using congrArg Prod.snd h
    exact_mod_cast hden

/-- Integers with bounded absolute value form a finite set. -/
theorem finite_int_natAbs_le (N : Nat) :
    ({z : Int | z.natAbs <= N} : Set Int).Finite := by
  refine (Set.finite_Icc (-(N : Int)) (N : Int)).subset ?_
  intro z hz
  have hcast : (z.natAbs : Int) <= (N : Int) := by
    exact_mod_cast hz
  constructor
  · have hneg : -z <= (z.natAbs : Int) := by
      simpa [Int.natCast_natAbs] using neg_le_abs z
    omega
  · have hle : z <= (z.natAbs : Int) := by
      simpa [Int.natCast_natAbs] using le_abs_self z
    omega

/-- Rationals of bounded affine height form a finite set. -/
theorem finite_rat_height_le (T : Nat) :
    ({q : Rat | rationalHeight q <= T} : Set Rat).Finite := by
  let s : Set (Int × Int) :=
    {p | p.1.natAbs <= T /\ p.2.natAbs <= T}
  have hs : s.Finite := by
    simpa [s, Set.prod] using
      (finite_int_natAbs_le T).prod (finite_int_natAbs_le T)
  refine (hs.preimage normalizedRatPair_injective.injOn).subset ?_
  intro q hq
  exact ⟨le_trans (le_max_left _ _) hq,
    le_trans (le_max_right _ _) hq⟩

/-- Affine rational points with bounded coordinatewise height form a finite set. -/
theorem finite_point_height_le (n T : Nat) :
    ({q : RationalPoint n | pointHeight q <= T} :
      Set (RationalPoint n)).Finite := by
  apply Set.Finite.subset (Set.Finite.pi' fun _ => finite_rat_height_le T)
  intro q hq i
  exact le_trans
    (Finset.le_sup (f := fun j => rationalHeight (q j)) (Finset.mem_univ i)) hq

/-- Every bounded-height slice in the canonical statement is finite; this
discharges the statement's explicit finiteness conjunct independently of the
deep counting estimate. -/
theorem finite_transcendentalRationalPoints
    (X : Set (Fin n -> Real)) (T : Nat) :
    (transcendentalRationalPoints X T).Finite := by
  exact (finite_point_height_le n T).subset fun _q hq => hq.2

/-- The quantitative tail holds when the transcendental part is empty. The
constant is `1` because the frozen target explicitly requires positivity. -/
theorem countingConclusion_of_diff_eq_empty
    {X : Set (Fin n -> Real)} {epsilon : Real}
    (h : X \ algebraicPart X = ∅) : CountingConclusion X epsilon := by
  refine ⟨1, by norm_num, fun T _hT => ?_⟩
  have hpoints : transcendentalRationalPoints X T = ∅ := by
    ext q
    simp [transcendentalRationalPoints, h]
  rw [hpoints]
  constructor
  · exact Set.finite_empty
  · simp only [Set.ncard_empty, Nat.cast_zero, one_mul]
    exact Real.rpow_nonneg (Nat.cast_nonneg T) epsilon

/-- A semialgebraic, preconnected, nontrivial set has empty transcendental part
under the frozen algebraic-part definition. -/
theorem countingConclusion_of_semialgebraic_preconnected_nontrivial
    {X : Set (Fin n -> Real)} {epsilon : Real}
    (hSA : IsSemialgebraic X) (hPre : IsPreconnected X)
    (hNontrivial : X.Nontrivial) : CountingConclusion X epsilon := by
  apply countingConclusion_of_diff_eq_empty
  exact diff_eq_empty.mpr
    (subset_algebraicPart_of_semialgebraic_preconnected_nontrivial
      Subset.rfl hSA hPre hNontrivial)

/-- The empty-set branch of the counting conclusion. -/
theorem countingConclusion_empty {n : Nat} {epsilon : Real} :
    CountingConclusion (∅ : Set (Fin n -> Real)) epsilon := by
  apply countingConclusion_of_diff_eq_empty
  exact diff_eq_empty.mpr (empty_subset _)

#print axioms subset_algebraicPart_of_semialgebraic_preconnected_nontrivial
#print axioms algebraicPart_subset
#print axioms algebraicPart_mono
#print axioms normalizedRatPair_injective
#print axioms finite_int_natAbs_le
#print axioms finite_rat_height_le
#print axioms finite_point_height_le
#print axioms finite_transcendentalRationalPoints
#print axioms countingConclusion_of_diff_eq_empty
#print axioms countingConclusion_of_semialgebraic_preconnected_nontrivial
#print axioms countingConclusion_empty

end Stage1Instances.THM_M_0441.Proof
