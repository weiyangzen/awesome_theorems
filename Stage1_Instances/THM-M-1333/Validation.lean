import Statement

/-!
# THM-M-1333 independent validation probes

These probes reconstruct the checked zero-dimensional branch directly from
the frozen statement.  They intentionally do not import `Proof` or
`ObligationTree`, and do not close the positive-dimensional Peano theorem.
-/

namespace Stage1Instances.THM_M_1333

theorem peanoExistenceFinZeroDirect
    (U : Set (Real × StateSpace 0))
    (f : Real -> StateSpace 0 -> StateSpace 0) (t0 : Real) (x0 : StateSpace 0)
    (hU : IsOpen U) (hx0 : (t0, x0) ∈ U) :
    ∃ epsilon : Real, 0 < epsilon ∧
      ∃ x : Real -> StateSpace 0,
        x t0 = x0 ∧
        IsSolutionWithin U f (Set.Icc (t0 - epsilon) (t0 + epsilon)) x := by
  let graph : Real -> Real × StateSpace 0 := fun t => (t, x0)
  have hopen : IsOpen (graph ⁻¹' U) :=
    hU.preimage (continuous_id.prodMk continuous_const)
  obtain ⟨radius, hradius, hball⟩ :=
    Metric.mem_nhds_iff.mp (hopen.mem_nhds hx0)
  refine ⟨radius / 2, half_pos hradius, fun _ => x0, rfl, ?_⟩
  intro t ht
  have hdist : dist t t0 < radius := by
    rw [Real.dist_eq, abs_lt]
    constructor <;> linarith [ht.1, ht.2, hradius]
  refine ⟨hball hdist, ?_⟩
  have hfzero : f t x0 = 0 := Subsingleton.elim _ _
  rw [hfzero]
  exact (hasDerivAt_const t x0).hasDerivWithinAt

theorem peanoExistenceTargetConditionalDirect
    (hpositive :
      ∀ (n : Nat) (U : Set (Real × StateSpace n))
        (f : Real -> StateSpace n -> StateSpace n)
        (t0 : Real) (x0 : StateSpace n),
          0 < n -> IsOpen U -> (t0, x0) ∈ U ->
          ContinuousOn (fun p : Real × StateSpace n => f p.1 p.2) U ->
          ∃ epsilon : Real, 0 < epsilon ∧
            ∃ x : Real -> StateSpace n,
              x t0 = x0 ∧
              IsSolutionWithin U f
                (Set.Icc (t0 - epsilon) (t0 + epsilon)) x) :
    PeanoExistenceTarget := by
  intro n U f t0 x0 hU hx0 hf
  by_cases hn : n = 0
  · subst n
    exact peanoExistenceFinZeroDirect U f t0 x0 hU hx0
  · exact hpositive n U f t0 x0 (Nat.pos_of_ne_zero hn) hU hx0 hf

#print axioms peanoExistenceFinZeroDirect
#print axioms peanoExistenceTargetConditionalDirect

end Stage1Instances.THM_M_1333
