import Statement

/-!
# THM-M-1084 finite covering nets

This module implements the cardinality-certified finite-net construction for the custom open-ball
covering number frozen by `Statement.lean`.
-/

noncomputable section

open Set

namespace Stage1Instances.THM_M_1084.Proof

universe u

/-- Total boundedness supplies a finite open-ball cover at every positive radius. -/
theorem exists_openBallCover {T : Type u} [PseudoMetricSpace T]
    (hTotallyBounded : TotallyBounded (univ : Set T))
    {epsilon : Real} (hepsilon : 0 < epsilon) :
    exists centers : Finset T, IsOpenBallCover epsilon centers := by
  obtain ⟨centers, -, hfinite, hcover⟩ :=
    Metric.finite_approx_of_totallyBounded hTotallyBounded epsilon hepsilon
  refine ⟨hfinite.toFinset, ?_⟩
  intro t
  have ht : t ∈ ⋃ c ∈ centers, Metric.ball c epsilon := hcover (mem_univ t)
  simp only [mem_iUnion, Metric.mem_ball] at ht
  obtain ⟨c, hc, hdist⟩ := ht
  exact ⟨c, by simpa using hc, by simpa [dist_comm] using hdist⟩

/-- The custom natural covering number is attained by a finite open-ball cover. -/
theorem exists_minimal_openBallCover {T : Type u} [PseudoMetricSpace T]
    (hTotallyBounded : TotallyBounded (univ : Set T))
    {epsilon : Real} (hepsilon : 0 < epsilon) :
    exists centers : Finset T,
      centers.card = coveringNumber (T := T) epsilon ∧ IsOpenBallCover epsilon centers := by
  let sizes : Set Nat := {n : Nat | exists centers : Finset T,
    centers.card = n ∧ IsOpenBallCover epsilon centers}
  have hsizes : sizes.Nonempty := by
    obtain ⟨centers, hcenters⟩ := exists_openBallCover hTotallyBounded hepsilon
    exact ⟨centers.card, centers, rfl, hcenters⟩
  have hmem : sInf sizes ∈ sizes := Nat.sInf_mem hsizes
  simpa only [coveringNumber] using hmem

/-- A nonempty totally bounded space needs at least one center at every positive radius. -/
theorem coveringNumber_pos {T : Type u} [PseudoMetricSpace T] [Nonempty T]
    (hTotallyBounded : TotallyBounded (univ : Set T))
    {epsilon : Real} (hepsilon : 0 < epsilon) :
    0 < coveringNumber (T := T) epsilon := by
  obtain ⟨centers, hcard, hcover⟩ :=
    exists_minimal_openBallCover hTotallyBounded hepsilon
  rw [← hcard]
  apply Finset.card_pos.mpr
  obtain ⟨c, hc, -⟩ := hcover (Classical.choice inferInstance)
  exact ⟨c, hc⟩

#print sorries exists_openBallCover
#print axioms exists_openBallCover
#print sorries exists_minimal_openBallCover
#print axioms exists_minimal_openBallCover
#print sorries coveringNumber_pos
#print axioms coveringNumber_pos

end Stage1Instances.THM_M_1084.Proof
