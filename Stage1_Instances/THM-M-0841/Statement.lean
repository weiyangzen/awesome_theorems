import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite

/-!
# THM-M-0841: exact 1946 Erdos-Stone statement

This module freezes the sparse, complementary-graph form printed on page 1087 of Erdos and
Stone's 1946 paper. It contains no proof of the theorem.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0841

open scoped SimpleGraph

/-- The paper's iterated natural logarithm: `l_0(x) = x` and
`l_(j+1)(x) = log(l_j(x))`. -/
noncomputable def iteratedLog (iterations : Nat) (x : Real) : Real :=
  Real.log^[iterations] x

/-- Erdos and Stone's 1946 theorem in its original sparse form.

For every `0 < epsilon < 1` and integer `r >= 2`, all sufficiently large `n`-vertex simple graphs
with fewer than `(1 / (2 * (r - 1)) - epsilon) * n^2` edges contain `r` disjoint equal-size
vertex groups with no edges between distinct groups. Containment of the complete equipartite graph
in the complement expresses exactly those groups.
-/
def ErdosStoneTarget : Prop :=
  forall (epsilon : Real) (r : Nat),
    0 < epsilon ->
    epsilon < 1 ->
    2 <= r ->
    exists n0 : Nat, 0 < n0 /\ forall n : Nat, n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        (G.edgeFinset.card : Real) <
            ((1 : Real) / (2 * (r - 1 : Nat)) - epsilon) * (n : Real) ^ 2 ->
          exists k : Nat, 0 < k /\
            Real.sqrt (iteratedLog (r - 1) (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ

/-- The same source statement with the part-size definition expanded. -/
def ExpandedSourceTarget : Prop :=
  forall (epsilon : Real) (r : Nat),
    0 < epsilon ->
    epsilon < 1 ->
    2 <= r ->
    exists n0 : Nat, 0 < n0 /\ forall n : Nat, n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        (G.edgeFinset.card : Real) <
            ((1 : Real) / (2 * (r - 1 : Nat)) - epsilon) * (n : Real) ^ 2 ->
          exists k : Nat, 0 < k /\
            Real.sqrt (Real.log^[r - 1] (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ

/-- Checked unfolding transport to the source-expanded spelling. -/
theorem erdosStoneTarget_iff_expandedSourceTarget :
    ErdosStoneTarget <-> ExpandedSourceTarget := by
  simp only [ErdosStoneTarget, ExpandedSourceTarget, iteratedLog]

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: the source's upper bound `epsilon < 1` is omitted. -/
def mutationRemovedEpsilonUpperBound : Prop :=
  forall (epsilon : Real) (r : Nat),
    0 < epsilon ->
    2 <= r ->
    exists n0 : Nat, 0 < n0 /\ forall n : Nat, n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        (G.edgeFinset.card : Real) <
            ((1 : Real) / (2 * (r - 1 : Nat)) - epsilon) * (n : Real) ^ 2 ->
          exists k : Nat, 0 < k /\
            Real.sqrt (iteratedLog (r - 1) (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ

/-- Changed-domain mutation: the tolerance is rational rather than real. -/
def mutationRationalTolerance : Prop :=
  forall (epsilon : Rat) (r : Nat),
    0 < epsilon ->
    epsilon < 1 ->
    2 <= r ->
    exists n0 : Nat, 0 < n0 /\ forall n : Nat, n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        (G.edgeFinset.card : Real) <
            ((1 : Real) / (2 * (r - 1 : Nat)) - (epsilon : Real)) * (n : Real) ^ 2 ->
          exists k : Nat, 0 < k /\
            Real.sqrt (iteratedLog (r - 1) (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ

/-- Changed-binder-scope mutation: one threshold must work for every tolerance and part count. -/
def mutationUniformThreshold : Prop :=
  exists n0 : Nat, 0 < n0 /\ forall (epsilon : Real) (r n : Nat),
    0 < epsilon ->
    epsilon < 1 ->
    2 <= r ->
    n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        (G.edgeFinset.card : Real) <
            ((1 : Real) / (2 * (r - 1 : Nat)) - epsilon) * (n : Real) ^ 2 ->
          exists k : Nat, 0 < k /\
            Real.sqrt (iteratedLog (r - 1) (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ

/-- Boundary mutation: it admits the source-excluded endpoint `epsilon = 0`. -/
def mutationAllowsZeroTolerance : Prop :=
  forall (epsilon : Real) (r : Nat),
    0 <= epsilon ->
    epsilon < 1 ->
    2 <= r ->
    exists n0 : Nat, 0 < n0 /\ forall n : Nat, n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        (G.edgeFinset.card : Real) <
            ((1 : Real) / (2 * (r - 1 : Nat)) - epsilon) * (n : Real) ^ 2 ->
          exists k : Nat, 0 < k /\
            Real.sqrt (iteratedLog (r - 1) (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ Gᶜ

#check_failure (rfl : ErdosStoneTarget = mutationRemovedEpsilonUpperBound)
#check_failure (rfl : ErdosStoneTarget = mutationRationalTolerance)
#check_failure (rfl : ErdosStoneTarget = mutationUniformThreshold)
#check_failure (rfl : ErdosStoneTarget = mutationAllowsZeroTolerance)

/-! Boundary checks for the exact source conventions. -/

/-- Zero iterations leave the argument unchanged. -/
theorem iteratedLog_zero (x : Real) : iteratedLog 0 x = x := by
  rfl

/-- One iteration is the natural logarithm. -/
theorem iteratedLog_one (x : Real) : iteratedLog 1 x = Real.log x := by
  rfl

/-- The hypotheses exclude `r = 1`, where natural subtraction would make the denominator zero. -/
theorem one_part_excluded : Not (2 <= (1 : Nat)) := by
  decide

/-- The source's lower endpoint `epsilon = 0` is excluded. -/
theorem zero_tolerance_excluded : Not ((0 : Real) < 0) := by
  exact lt_irrefl 0

/-- The source's upper endpoint `epsilon = 1` is excluded. -/
theorem one_tolerance_excluded : Not ((1 : Real) < 1) := by
  exact lt_irrefl 1

#print axioms erdosStoneTarget_iff_expandedSourceTarget

end Stage1Instances.THM_M_0841

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0841.ErdosStoneTarget
