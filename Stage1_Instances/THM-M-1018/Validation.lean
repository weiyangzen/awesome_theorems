import Statement
import ObligationTree
import Mathlib.MeasureTheory.Measure.Portmanteau
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-1018 validation probes

This module independently reconstructs two partial proof results and checks the
conditional bridge from the frozen analytic interface to the canonical target.
It deliberately does not import `Proof`; the analytic inversion premise remains
open and no premise-free proof of `LevyInversionTarget` is asserted.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1018.Validation

open Stage1Instances.THM_M_1018

/-- Independent reconstruction of the endpoint-frontier calculation. -/
theorem frontier_Ioc_null_direct
    (mu : Measure Real) [IsProbabilityMeasure mu] {a b : Real}
    (hab : a < b) (ha : mu {a} = 0) (hb : mu {b} = 0) :
    mu (frontier (Set.Ioc a b)) = 0 := by
  rw [frontier_Ioc hab, pair_comm]
  simpa using (measure_union_null ha hb)

/-- Independent reconstruction of the conditional Portmanteau step. -/
theorem tendsto_Ioc_mass_of_tendsto_direct
    {iota : Type*} {l : Filter iota}
    (mu : Measure Real) [IsProbabilityMeasure mu]
    (mus : iota -> ProbabilityMeasure Real)
    (hmu : Tendsto mus l (nhds (show ProbabilityMeasure Real from ⟨mu, inferInstance⟩)))
    {a b : Real} (hab : a < b) (ha : mu {a} = 0) (hb : mu {b} = 0) :
    Tendsto (fun i => ((mus i : Measure Real) (Set.Ioc a b))) l
      (nhds (mu (Set.Ioc a b))) := by
  exact ProbabilityMeasure.tendsto_measure_of_null_frontier_of_tendsto'
    hmu (frontier_Ioc_null_direct mu hab ha hb)

/-- The frozen obligation-tree interface is definitionally the canonical target
once its full fixed-data analytic premise is supplied. This is a composition
check only: `analytic` is precisely the still-open inversion theorem. -/
theorem conditionalCanonicalBridge
    (analytic : forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
      a < b -> mu {a} = 0 -> mu {b} = 0 ->
        ObligationTree.InversionFor mu a b) :
    LevyInversionTarget := by
  intro mu _ a b hab ha hb
  exact analytic mu a b hab ha hb

#print sorries frontier_Ioc_null_direct
#print axioms frontier_Ioc_null_direct
#print sorries tendsto_Ioc_mass_of_tendsto_direct
#print axioms tendsto_Ioc_mass_of_tendsto_direct
#print sorries conditionalCanonicalBridge
#print axioms conditionalCanonicalBridge

end Stage1Instances.THM_M_1018.Validation
