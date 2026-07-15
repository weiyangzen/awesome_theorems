import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite
import Mathlib.Combinatorics.SimpleGraph.Extremal.TuranDensity
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0841 immutable anchor probe

This module checks the closest proof-bearing interfaces available at the pinned mathlib revision.
None of them proves the frozen page-1087 sparse, growing-part target, so this file intentionally
contains no inhabitant of `ErdosStoneTarget`.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0841_AnchorAudit

open scoped SimpleGraph

/-- A literal audit copy of the frozen statement. It is printed so the checker can compare the
fully explicit expression with `Statement.lean` without importing an unaccepted proof. -/
noncomputable def iteratedLog (iterations : Nat) (x : Real) : Real :=
  Real.log^[iterations] x

def ExactTarget : Prop :=
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

#check SimpleGraph.completeEquipartiteGraph
#check SimpleGraph.card_edgeFinset_completeEquipartiteGraph
#check SimpleGraph.completeEquipartiteGraph_isContained_iff
#check SimpleGraph.completeEquipartiteGraph_succ_isContained_iff
#check SimpleGraph.completeMultipartiteGraph.chromaticNumber
#check SimpleGraph.turanDensity
#check SimpleGraph.tendsto_turanDensity
#check SimpleGraph.isEquivalent_extremalNumber
#check SimpleGraph.eventually_isContained_of_card_edgeFinset
#check SimpleGraph.isContained_of_card_edgeFinset
#check_failure SimpleGraph.eventually_completeEquipartiteGraph_isContained_of_minDegree
#check_failure SimpleGraph.ErdosStone.filter

assert_no_sorry SimpleGraph.card_edgeFinset_completeEquipartiteGraph
assert_no_sorry SimpleGraph.completeEquipartiteGraph_isContained_iff
assert_no_sorry SimpleGraph.completeMultipartiteGraph.chromaticNumber
assert_no_sorry SimpleGraph.eventually_isContained_of_card_edgeFinset
assert_no_sorry SimpleGraph.isContained_of_card_edgeFinset

#print axioms SimpleGraph.card_edgeFinset_completeEquipartiteGraph
#print axioms SimpleGraph.completeEquipartiteGraph_isContained_iff
#print axioms SimpleGraph.completeMultipartiteGraph.chromaticNumber
#print axioms SimpleGraph.eventually_isContained_of_card_edgeFinset
#print axioms SimpleGraph.isContained_of_card_edgeFinset

end Stage1Instances.THM_M_0841_AnchorAudit

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0841_AnchorAudit.ExactTarget
