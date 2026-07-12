import Statement

/-!
# THM-M-1333 proof bodies

This module closes the zero-dimensional branch of the frozen Peano-existence
architecture. The positive-dimensional approximation and compactness route
remains open.
-/

namespace Stage1Instances.THM_M_1333

/-- Peano existence in the degenerate state space `Fin 0 -> Real`.

Openness supplies a positive time neighborhood on which the graph of the
constant curve stays in `U`. Both the vector field value and the derivative
of that curve are the unique element of the zero-dimensional state space. -/
theorem peanoExistence_fin_zero
    (U : Set (Real × StateSpace 0))
    (f : Real -> StateSpace 0 -> StateSpace 0) (t0 : Real) (x0 : StateSpace 0)
    (hU : IsOpen U) (hx0 : (t0, x0) ∈ U) :
    ∃ epsilon : Real, 0 < epsilon ∧
      ∃ x : Real -> StateSpace 0,
        x t0 = x0 ∧
        IsSolutionWithin U f (Set.Icc (t0 - epsilon) (t0 + epsilon)) x := by
  let graph : Real → Real × StateSpace 0 := fun t => (t, x0)
  have hgraph : Continuous graph := continuous_id.prodMk continuous_const
  have hopen : IsOpen (graph ⁻¹' U) := hU.preimage hgraph
  have ht0 : t0 ∈ graph ⁻¹' U := hx0
  obtain ⟨radius, hradius, hball⟩ :=
    Metric.mem_nhds_iff.mp (hopen.mem_nhds ht0)
  refine ⟨radius / 2, half_pos hradius, fun _ => x0, rfl, ?_⟩
  intro t ht
  have hdist : dist t t0 < radius := by
    rw [Real.dist_eq, abs_lt]
    constructor <;> linarith [ht.1, ht.2, hradius]
  constructor
  · exact hball hdist
  · have hfzero : f t x0 = 0 := Subsingleton.elim _ _
    rw [hfzero]
    exact (hasDerivAt_const t x0).hasDerivWithinAt

/-- Exhaustive dimension recomposition. The explicit premise is precisely the
still-open positive-dimensional branch; no existence content is hidden in
this composition theorem. -/
theorem peanoExistenceTarget_of_positive_dimension
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
    exact peanoExistence_fin_zero U f t0 x0 hU hx0
  · exact hpositive n U f t0 x0 (Nat.pos_of_ne_zero hn) hU hx0 hf

#print axioms peanoExistence_fin_zero
#print axioms peanoExistenceTarget_of_positive_dimension

end Stage1Instances.THM_M_1333
