import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0841 conditional obligation composition

This module fixes exact interfaces for the original-paper induction architecture.  The base case,
induction step, and sparse-to-dense transport remain explicit premises.  The terms below validate
only child-to-parent composition; they do not prove Erdos-Stone or close any mathematical child.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0841_Obligations

open scoped SimpleGraph
open Stage1Instances.THM_M_0841

/-- The selected page-1087 proposition, used as the exact root interface. -/
def ExactRoot : Prop :=
  ErdosStoneTarget

/-- Dense-complement member of the same indexed theorem family.  This representation makes the
paper's induction on the number of parts explicit without pretending that the transport is proved. -/
def DenseClaim (r : Nat) : Prop :=
  forall epsilon : Real,
    0 < epsilon ->
    epsilon < 1 ->
    2 <= r ->
    exists n0 : Nat, 0 < n0 /\ forall n : Nat, n0 < n ->
      forall (G : SimpleGraph (Fin n)) [DecidableRel G.Adj],
        ((1 : Real) / 2 - (1 : Real) / (2 * (r - 1 : Nat)) + epsilon) *
              (n : Real) ^ 2 <= (G.edgeFinset.card : Real) ->
          exists k : Nat, 0 < k /\
            Real.sqrt (iteratedLog (r - 1) (n : Real)) <= (k : Real) /\
            SimpleGraph.completeEquipartiteGraph r k ⊑ G

/-- Exact base product needed by strong induction. -/
def DenseBase : Prop :=
  DenseClaim 2

/-- Exact strong-induction step product.  All smaller valid part counts are explicit premises. -/
def DenseStep : Prop :=
  forall r : Nat,
    3 <= r ->
    (forall s : Nat, 2 <= s -> s < r -> DenseClaim s) ->
    DenseClaim r

/-- The complete dense indexed family delivered by the base and strong-induction products. -/
def DenseFamily : Prop :=
  forall r : Nat, 2 <= r -> DenseClaim r

/-- Exact bridge from the dense complement family back to the frozen sparse root. -/
def SparseFromDense : Prop :=
  DenseFamily -> ExactRoot

/-- Checked strong-induction composition.  Both mathematical products remain hypotheses. -/
theorem denseFamily_compose (base : DenseBase) (step : DenseStep) : DenseFamily := by
  intro r hr
  induction r using Nat.strong_induction_on with
  | h r ih =>
      by_cases htwo : r = 2
      · simpa [DenseBase, htwo] using base
      · have hthree : 3 <= r := by omega
        exact step r hthree (fun s hs hsr => ih s hsr hs)

/-- Checked transport composition.  The transport theorem itself remains a named premise. -/
theorem sparse_compose (transport : SparseFromDense) (dense : DenseFamily) : ExactRoot :=
  transport dense

/-- Convenience composition exposing the full conditional route in one declaration. -/
theorem compose_root
    (base : DenseBase) (step : DenseStep) (transport : SparseFromDense) : ExactRoot :=
  transport (denseFamily_compose base step)

/-- Identity certificate binding the terminal node to the canonical declaration. -/
theorem exactRoot_iff_canonical : ExactRoot <-> ErdosStoneTarget :=
  Iff.rfl

/-- Root-level child consumption: the terminal child's exact output is the canonical root. -/
theorem root_of_terminal (terminal : ExactRoot) : ExactRoot :=
  terminal

#check DenseBase
#check DenseStep
#check DenseFamily
#check SparseFromDense
#check denseFamily_compose
#check sparse_compose
#check compose_root
#check exactRoot_iff_canonical
#check root_of_terminal

assert_no_sorry denseFamily_compose
assert_no_sorry sparse_compose
assert_no_sorry compose_root
assert_no_sorry exactRoot_iff_canonical
assert_no_sorry root_of_terminal

#print sorries denseFamily_compose sparse_compose compose_root exactRoot_iff_canonical root_of_terminal
#print axioms denseFamily_compose
#print axioms sparse_compose
#print axioms compose_root
#print axioms exactRoot_iff_canonical
#print axioms root_of_terminal

end Stage1Instances.THM_M_0841_Obligations
