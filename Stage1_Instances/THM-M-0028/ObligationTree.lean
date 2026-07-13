import Statement
import Mathlib.RingTheory.Noetherian.Defs

/-!
# THM-M-0028 conditional obligation composition

This module checks the exact composition interface frozen by the obligation registry. The two
mathematical bridges are explicit premises: this phase does not install the audited mathlib
candidate as the canonical proof.
-/

namespace Stage1Instances.THM_M_0028.ObligationTree

universe u

/-- The finite-generation bridge required by the exact target. -/
def FiniteGenerationToNoetherian : Prop :=
  forall {R : Type u} [CommRing R],
    (forall I : Ideal R, I.FG) -> IsNoetherianRing R

/-- The ascending-chain bridge required by the exact target. -/
def NoetherianToChainStabilization : Prop :=
  forall {R : Type u} [CommRing R],
    IsNoetherianRing R ->
      forall f : Nat →o Ideal R,
        exists n, forall m, n <= m -> f n = f m

/-- The exact pair of mathematical bridges required by the root composition. -/
def BridgePackage : Prop :=
  FiniteGenerationToNoetherian.{u} /\ NoetherianToChainStabilization.{u}

/-- Checked composition of the two bridge children into their terminal package. -/
theorem bridgePackage_of_bridges
    (finiteGeneration : FiniteGenerationToNoetherian.{u})
    (chainStabilization : NoetherianToChainStabilization.{u}) : BridgePackage.{u} :=
  And.intro finiteGeneration chainStabilization

/-- Checked composition of the terminal bridge package into the canonical root. -/
theorem root_of_bridgePackage
    (bridges : BridgePackage.{u}) :
    Stage1Instances.THM_M_0028.IdealAscendingChainTarget.{u} := by
  intro R _ hfg f
  exact bridges.2 (bridges.1 hfg) f

/-- The complete checked child-to-root composition, with both bridges still explicit premises. -/
theorem root_of_bridges
    (finiteGeneration : FiniteGenerationToNoetherian.{u})
    (chainStabilization : NoetherianToChainStabilization.{u}) :
    Stage1Instances.THM_M_0028.IdealAscendingChainTarget.{u} :=
  root_of_bridgePackage (bridgePackage_of_bridges finiteGeneration chainStabilization)

#check isNoetherianRing_iff_ideal_fg
#check monotone_stabilizes_iff_noetherian
#check isNoetherian_def
#check isNoetherian_iff'
#check Submodule.fg_iff_compact
#check CompleteLattice.wellFoundedGT_characterisations
#check wellFoundedGT_iff_monotone_chain_condition

#print axioms bridgePackage_of_bridges
#print axioms root_of_bridgePackage
#print axioms root_of_bridges

end Stage1Instances.THM_M_0028.ObligationTree
