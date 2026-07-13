import ObligationTree

/-!
# THM-M-0028 proof-phase installation

This module installs the two exact pinned mathlib bridges at the interfaces frozen by the
obligation registry, and then composes them to the unchanged canonical ascending-chain target.
The direct root declaration is a second exact-type check over the same deduplicated terminal
proof bodies.
-/

namespace Stage1Instances.THM_M_0028.Proof

open Stage1Instances.THM_M_0028
open Stage1Instances.THM_M_0028.ObligationTree

universe u

/-- The pinned finite-generation bridge installed at its frozen proof interface. -/
theorem finiteGenerationToNoetherian : FiniteGenerationToNoetherian.{u} := by
  intro R _ hfg
  exact (isNoetherianRing_iff_ideal_fg R).mpr hfg

/-- The pinned ascending-chain bridge installed at its frozen proof interface. -/
theorem noetherianToChainStabilization : NoetherianToChainStabilization.{u} := by
  intro R _ hNoetherian f
  exact monotone_stabilizes_iff_noetherian.mpr hNoetherian f

/-- Direct exact-root wrapper over the same two pinned terminal proof bodies. -/
theorem idealAscendingChainTheorem_direct : IdealAscendingChainTarget.{u} := by
  intro R _ hfg f
  have hNoetherian : IsNoetherianRing R :=
    (isNoetherianRing_iff_ideal_fg R).mpr hfg
  exact monotone_stabilizes_iff_noetherian.mpr hNoetherian f

/-- Exact root obtained by consuming both frozen child-to-parent composition interfaces. -/
theorem idealAscendingChainTheorem_via_frozen_composition :
    IdealAscendingChainTarget.{u} :=
  root_of_bridges finiteGenerationToNoetherian noetherianToChainStabilization

#print sorries isNoetherianRing_iff_ideal_fg
#print sorries monotone_stabilizes_iff_noetherian
#print sorries finiteGenerationToNoetherian
#print sorries noetherianToChainStabilization
#print sorries idealAscendingChainTheorem_direct
#print sorries idealAscendingChainTheorem_via_frozen_composition

#print axioms isNoetherianRing_iff_ideal_fg
#print axioms monotone_stabilizes_iff_noetherian
#print axioms finiteGenerationToNoetherian
#print axioms noetherianToChainStabilization
#print axioms idealAscendingChainTheorem_direct
#print axioms idealAscendingChainTheorem_via_frozen_composition

end Stage1Instances.THM_M_0028.Proof
