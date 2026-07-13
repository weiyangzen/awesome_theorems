import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Combinatorics.SimpleGraph.LapMatrix

/-!
# THM-M-0890: Hoffman's ratio bound statement

This module freezes the finite regular-graph ratio-bound proposition selected from Haemers,
Theorem 1. It defines and mutation-tests the target only; it contains no proof of the bound.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0890

universe u

/-- The least real eigenvalue of the adjacency matrix, using mathlib's descending Hermitian
eigenvalue enumeration. `Nonempty V` makes the last finite index well typed. -/
noncomputable def leastAdjacencyEigenvalue
    {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] : Real :=
  (G.isHermitian_adjMatrix Real).eigenvalues₀
    ⟨Fintype.card V - 1, Nat.sub_lt Fintype.card_pos Nat.zero_lt_one⟩

/-- The exact statement target for Hoffman's regular-graph independence-number ratio bound.

The positive-degree premise excludes precisely the regular edgeless case in which the printed
quotient has denominator zero. The later source audit must review this explicit formal boundary.
-/
def HoffmanRatioBoundTarget : Prop :=
  ∀ {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat),
    G.IsRegularOfDegree k →
    0 < k →
    (G.indepNum : Real) ≤
      Fintype.card V *
        (-leastAdjacencyEigenvalue G / (k - leastAdjacencyEigenvalue G))

/-! Structural mutations used by the statement validator. -/

/-- Removed-hypothesis mutation: positive degree is omitted. -/
def mutationRemovedPositiveDegree : Prop :=
  ∀ {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat),
    G.IsRegularOfDegree k →
    (G.indepNum : Real) ≤
      Fintype.card V *
        (-leastAdjacencyEigenvalue G / (k - leastAdjacencyEigenvalue G))

/-- Changed-domain mutation: the conclusion is a rational inequality with an explicit rational
spectral parameter instead of the real least eigenvalue of the adjacency matrix. -/
def mutationRationalSpectralDomain : Prop :=
  ∀ {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat) (lambdaMin : Rat),
    G.IsRegularOfDegree k →
    0 < k →
    (G.indepNum : Rat) ≤
      Fintype.card V * (-lambdaMin / (k - lambdaMin))

/-- Changed-scope mutation: one vertex carrier and graph are chosen outside the universal binder. -/
def mutationExistentialGraphScope : Prop :=
  ∃ (V : Type u) (_ : Fintype V) (_ : Nonempty V) (_ : DecidableEq V)
    (G : SimpleGraph V) (_ : DecidableRel G.Adj),
    ∀ k : Nat,
      G.IsRegularOfDegree k →
      0 < k →
      (G.indepNum : Real) ≤
        Fintype.card V *
          (-leastAdjacencyEigenvalue G / (k - leastAdjacencyEigenvalue G))

/-- Boundary mutation: only regular graphs of degree at least two are admitted. -/
def mutationDegreeAtLeastTwo : Prop :=
  ∀ {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat),
    G.IsRegularOfDegree k →
    2 ≤ k →
    (G.indepNum : Real) ≤
      Fintype.card V *
        (-leastAdjacencyEigenvalue G / (k - leastAdjacencyEigenvalue G))

#check_failure
  (rfl : HoffmanRatioBoundTarget.{u} = mutationRemovedPositiveDegree.{u})
#check_failure
  (rfl : HoffmanRatioBoundTarget.{u} = mutationRationalSpectralDomain.{u})
#check_failure
  (rfl : HoffmanRatioBoundTarget.{u} = mutationExistentialGraphScope.{u})
#check_failure
  (rfl : HoffmanRatioBoundTarget.{u} = mutationDegreeAtLeastTwo.{u})

/-! Boundary checks for the selected positive-degree convention. -/

/-- Removing positive degree admits the nonempty edgeless graph on one vertex. -/
example :
    (⊥ : SimpleGraph (Fin 1)).IsRegularOfDegree 0 := by
  intro v
  have hNeighbor : (⊥ : SimpleGraph (Fin 1)).neighborFinset v = ∅ := by
    ext w
    simp
  exact (congrArg Finset.card hNeighbor).trans (Finset.card_empty)

/-- The selected positive-degree premise rejects that edgeless boundary. -/
example : ¬ (0 : Nat) < 0 := by simp

/-- Degree one remains in scope; the boundary is not silently strengthened to degree two. -/
example : (0 : Nat) < 1 ∧ ¬ (2 : Nat) ≤ 1 := by simp

end Stage1Instances.THM_M_0890

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget
