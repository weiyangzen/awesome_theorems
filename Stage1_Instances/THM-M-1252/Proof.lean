import Statement
import ObligationTree

/-!
# THM-M-1252 proof execution

This module installs the pinned mathlib support theorem at the exact frozen target and checks the
frozen specialization and child-to-parent composition interfaces. The terminal proof body remains
`Distribution.dsupport_compl_eq` in the pinned mathlib dependency.
-/

noncomputable section

open Set TopologicalSpace
open scoped Distributions

namespace Stage1Instances.THM_M_1252.Proof

universe u

/-- Exact specialization of the pinned generic support theorem. This closes `M1252-N-SPECIALIZE`
using the body tracked by `M1252-L-UPSTREAM`. -/
theorem specializedAnchor : ObligationTree.SpecializedAnchor.{u} := by
  intro E _ _ _ Omega T
  exact Distribution.dsupport_compl_eq

/-- The exact canonical target, closed through the frozen child-to-parent composition certificate. -/
theorem distributionSupportLocalization :
    DistributionSupportLocalizationTarget.{u} := by
  exact ObligationTree.root_of_specializedAnchor specializedAnchor

/-- The checked test-function expansion derived from the installed exact root. -/
theorem distributionSupportLocalization_expanded : ExpandedTarget.{u} := by
  exact distributionSupportLocalizationTarget_iff_expandedTarget.mp
    distributionSupportLocalization

#print axioms Distribution.dsupport_compl_eq
#print axioms specializedAnchor
#print axioms distributionSupportLocalization
#print axioms distributionSupportLocalization_expanded

end Stage1Instances.THM_M_1252.Proof
