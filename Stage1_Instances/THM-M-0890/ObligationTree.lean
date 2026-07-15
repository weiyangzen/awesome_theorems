import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0890 obligation composition harness

This module fixes the exact two terminal interfaces selected by the frozen Hoffman-bound
architecture. Both interfaces remain explicit premises. The checked terms validate only
child-to-parent composition and the final division transport; they do not prove either premise or
Hoffman's ratio bound.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0890_Obligations

open Stage1Instances.THM_M_0890

universe u

/-- Positivity of the exact denominator appearing in the canonical target. -/
def DenominatorPositiveTarget : Prop :=
  forall {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat),
    G.IsRegularOfDegree k ->
    0 < k ->
    0 < (k : Real) - leastAdjacencyEigenvalue G

/-- The source inequality after clearing the positive denominator, at the exact root binders. -/
def DivisionFreeInequalityTarget : Prop :=
  forall {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat),
    G.IsRegularOfDegree k ->
    0 < k ->
    (G.indepNum : Real) * ((k : Real) - leastAdjacencyEigenvalue G) <=
      Fintype.card V * (-leastAdjacencyEigenvalue G)

/-- A maximum independent-set witness with the exact cardinality used by `indepNum`. -/
def MaximumIndependentSetWitnessTarget : Prop :=
  forall {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj],
    exists s : Finset V, G.IsIndepSet s /\ s.card = G.indepNum

/-- The source-facing division-free estimate for a selected maximum independent set. -/
def MaximumIndependentSetEstimateTarget : Prop :=
  forall {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat) (s : Finset V),
    G.IsRegularOfDegree k ->
    0 < k ->
    G.IsIndepSet s ->
    s.card = G.indepNum ->
    (s.card : Real) * ((k : Real) - leastAdjacencyEigenvalue G) <=
      Fintype.card V * (-leastAdjacencyEigenvalue G)

/-- The exact pair consumed by the final ratio-bound transport. -/
def RatioAssemblyTarget : Prop :=
  DenominatorPositiveTarget.{u} /\ DivisionFreeInequalityTarget.{u}

/-- A source-facing scalar estimate produced by the positive-semidefinite principal-submatrix
route. This remains an open interface and is not used as a hidden premise by the checked root. -/
def PSDScalarEstimateTarget : Prop :=
  forall {V : Type u} [Fintype V] [Nonempty V] [DecidableEq V]
    (G : SimpleGraph V) [DecidableRel G.Adj] (k : Nat),
    G.IsRegularOfDegree k ->
    0 < k ->
    0 <= (G.indepNum : Real) *
      (-leastAdjacencyEigenvalue G -
        (G.indepNum : Real) * ((k : Real) - leastAdjacencyEigenvalue G) /
          Fintype.card V)

/-- Checked wrapper around the pinned maximum-independent-set interface. This authenticates only
the witness transport; it is not the spectral estimate. -/
theorem maximumIndependentSetWitness_checked :
    MaximumIndependentSetWitnessTarget.{u} := by
  intro V _ _ _ G _
  obtain ⟨s, hs⟩ := G.exists_isNIndepSet_indepNum
  exact ⟨s, hs.isIndepSet, hs.card_eq⟩

/-- Exact maximum-witness transport into the division-free root child. Both the witness package and
the spectral estimate remain explicit inputs. -/
theorem divisionFree_of_maximumEstimate
    (maximum : MaximumIndependentSetWitnessTarget.{u})
    (estimate : MaximumIndependentSetEstimateTarget.{u}) :
    DivisionFreeInequalityTarget.{u} := by
  intro V _ _ _ G _ k hRegular hPositive
  obtain ⟨s, hIndependent, hCard⟩ := maximum G
  simpa [hCard] using estimate G k s hRegular hPositive hIndependent hCard

/-- Conditional child-to-assembly certificate. Both children are named and consumed. -/
theorem assembly_of_children
    (denominator : DenominatorPositiveTarget.{u})
    (divisionFree : DivisionFreeInequalityTarget.{u}) :
    RatioAssemblyTarget.{u} :=
  And.intro denominator divisionFree

/-- Exact transport from the two terminal products to the frozen canonical proposition. -/
theorem root_of_ratio_assembly
    (assembly : RatioAssemblyTarget.{u}) :
    HoffmanRatioBoundTarget.{u} := by
  intro V _ _ _ G _ k hRegular hPositive
  have hDenominator := assembly.1 G k hRegular hPositive
  have hDivisionFree := assembly.2 G k hRegular hPositive
  calc
    (G.indepNum : Real) <=
        (Fintype.card V * (-leastAdjacencyEigenvalue G)) /
          ((k : Real) - leastAdjacencyEigenvalue G) :=
      (le_div_iff₀ hDenominator).2 hDivisionFree
    _ = Fintype.card V *
        (-leastAdjacencyEigenvalue G / (k - leastAdjacencyEigenvalue G)) := by
      ring

/-- Combined conditional harness, useful for detecting an unused or mismatched terminal child. -/
theorem root_of_children
    (denominator : DenominatorPositiveTarget.{u})
    (divisionFree : DivisionFreeInequalityTarget.{u}) :
    HoffmanRatioBoundTarget.{u} :=
  root_of_ratio_assembly (assembly_of_children denominator divisionFree)

#check DenominatorPositiveTarget
#check DivisionFreeInequalityTarget
#check MaximumIndependentSetWitnessTarget
#check MaximumIndependentSetEstimateTarget
#check RatioAssemblyTarget
#check PSDScalarEstimateTarget
#check maximumIndependentSetWitness_checked
#check divisionFree_of_maximumEstimate
#check assembly_of_children
#check root_of_ratio_assembly
#check root_of_children

assert_no_sorry assembly_of_children
assert_no_sorry maximumIndependentSetWitness_checked
assert_no_sorry divisionFree_of_maximumEstimate
assert_no_sorry root_of_ratio_assembly
assert_no_sorry root_of_children

#print sorries maximumIndependentSetWitness_checked divisionFree_of_maximumEstimate
  assembly_of_children root_of_ratio_assembly root_of_children
#print axioms maximumIndependentSetWitness_checked
#print axioms divisionFree_of_maximumEstimate
#print axioms assembly_of_children
#print axioms root_of_ratio_assembly
#print axioms root_of_children

end Stage1Instances.THM_M_0890_Obligations
