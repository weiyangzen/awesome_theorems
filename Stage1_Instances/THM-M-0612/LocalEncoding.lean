import Statement

/-!
# THM-M-0612 local-encoding proof fragments

These lemmas discharge exact preliminary facts about the frozen local-domain
encoding. They do not prove the nonlinear radius obstruction or nonsqueezing.
-/

noncomputable section

open scoped BigOperators

namespace Stage1.THM_M_0612

universe u

/-- The canonical local embedding hypotheses are inhabited at equal radii. -/
theorem identity_isSymplecticEmbeddingOnBall
    {Q : Type u} [Fintype Q] (r : Real) :
    IsSymplecticEmbeddingOnBall r (id : PhaseSpace Q -> PhaseSpace Q) := by
  refine ⟨contDiff_id.contDiffOn, ?_, ?_⟩
  · intro x _ y _ hxy
    exact hxy
  · intro x _ v w
    simp [standardForm]

/-- In real dimension two, the identity maps the unit ball to the unit cylinder. -/
theorem identity_maps_unitBall_to_unitCylinder_dimTwo :
    Set.MapsTo (id : PhaseSpace (Fin 1) -> PhaseSpace (Fin 1))
      (ball 1) (cylinder 0 1) := by
  intro x hx
  simpa [ball, cylinder, normSq] using hx

/-- A positive-radius source ball contains the origin. -/
theorem zero_mem_ball
    {Q : Type u} [Fintype Q] {r : Real} (hr : 0 < r) :
    (0 : PhaseSpace Q) ∈ ball r := by
  simp [ball, normSq, sq_pos_of_pos hr]

/-- The squared coordinate norm in the canonical statement is continuous. -/
theorem continuous_normSq {Q : Type u} [Fintype Q] :
    Continuous (@normSq Q _) := by
  unfold normSq
  fun_prop

/-- The strict coordinate ball used by the canonical statement is open. -/
theorem isOpen_ball {Q : Type u} [Fintype Q] (r : Real) :
    IsOpen (@ball Q _ r) := by
  exact isOpen_lt continuous_normSq continuous_const

/--
Local smoothness on the open ball supplies the ambient derivative appearing in
`IsSymplecticEmbeddingOnBall`; no regularity outside the ball is used.
-/
theorem hasFDerivAt_of_contDiffOn_ball
    {Q : Type u} [Fintype Q] {r : Real}
    {f : PhaseSpace Q -> PhaseSpace Q}
    (hf : ContDiffOn Real ⊤ f (ball r)) {x : PhaseSpace Q} (hx : x ∈ ball r) :
    HasFDerivAt f (fderiv Real f x) x := by
  have hdWithin : DifferentiableWithinAt Real f (ball r) x :=
    (hf x hx).differentiableWithinAt (by simp)
  exact (hdWithin.differentiableAt ((isOpen_ball r).mem_nhds hx)).hasFDerivAt

#print axioms identity_isSymplecticEmbeddingOnBall
#print axioms identity_maps_unitBall_to_unitCylinder_dimTwo
#print axioms zero_mem_ball
#print axioms continuous_normSq
#print axioms isOpen_ball
#print axioms hasFDerivAt_of_contDiffOn_ball

end Stage1.THM_M_0612
