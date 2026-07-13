import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0821 proof execution

This module installs the lower-middle-layer witness and the pinned mathlib
Sperner bound into the interfaces frozen by `ObligationTree.lean`. The root
proof deliberately follows every checked package-composition certificate.
-/

namespace Stage1Instances.THM_M_0821.Proof

universe u

open Stage1Instances.THM_M_0821_Obligations

/-- The lower-middle powerset slice supplies the exact attaining package. -/
theorem middleLayerAttainment : AttainmentPackage.{u} :=
  attainment_of_middleLayer
    pinned_middleLayerDefinition
    (middleLayerAntichain_of_sized pinned_middleLayerSized)
    pinned_middleLayerCardinality

/-- The universal upper package, backed by pinned mathlib's `IsAntichain.sperner`. -/
theorem universalUpperBound : UpperBoundPackage.{u} :=
  upperBound_of_sperner pinned_upperBound

/-- Exact kernel closure of the frozen maximum-size target. -/
theorem spernerMaximum :
    Stage1Instances.THM_M_0821.SpernerMaximumTarget.{u} :=
  root_of_terminal <| compose_root <|
    maximumSplit_of_packages middleLayerAttainment universalUpperBound

assert_no_sorry IsAntichain.sperner
assert_no_sorry middleLayerAttainment
assert_no_sorry universalUpperBound
assert_no_sorry spernerMaximum

#print sorries IsAntichain.sperner
#print sorries middleLayerAttainment
#print sorries universalUpperBound
#print sorries spernerMaximum

#print axioms IsAntichain.sperner
#print axioms middleLayerAttainment
#print axioms universalUpperBound
#print axioms spernerMaximum

end Stage1Instances.THM_M_0821.Proof
