import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0822 proof execution

This module installs the target-owned star witness and the pinned mathlib
Erdos-Ko-Rado upper bound into the interfaces frozen by
`ObligationTree.lean`. The exact root proof consumes both packages through
the checked child-to-parent composition declarations.
-/

namespace Stage1Instances.THM_M_0822.Proof

open Stage1Instances.THM_M_0822.ObligationTree

/-- Admissible parameters provide an element of the finite ground set. -/
theorem groundElement : GroundElementPackage := by
  intro n r hr hhalf
  have hn2 : 0 < n / 2 := lt_of_lt_of_le Nat.zero_lt_one (hr.trans hhalf)
  exact ⟨⟨0, Nat.pos_of_div_pos hn2⟩⟩

/-- The ground element selects the canonical star construction. -/
theorem starConstruction : StarConstructionPackage :=
  starConstruction_of_groundElement groundElement

/-- The star image representation is installed at its frozen package interface. -/
theorem starImage : StarImagePackage :=
  Stage1Instances.THM_M_0822.erdosKoRadoStar_eq_image

/-- Every selected star is intersecting. -/
theorem starIntersecting : StarIntersectingPackage :=
  Stage1Instances.THM_M_0822.erdosKoRadoStar_intersecting

/-- Every selected star is uniformly of rank `r`. -/
theorem starSized : StarSizedPackage :=
  Stage1Instances.THM_M_0822.erdosKoRadoStar_sized

/-- The star image calculation yields the exact binomial cardinality. -/
theorem starCard : StarCardPackage :=
  starCard_of_image starImage

/-- A canonical star supplies the exact attaining-family package. -/
theorem starAttainment : AttainmentPackage :=
  attainment_of_starPackages starConstruction starIntersecting starSized starCard

/-- The pinned mathlib declaration installed at its exact terminal interface. -/
theorem mathlibUpperBound : MathlibUpperBoundTerminal :=
  pinnedMathlibUpperBound

/-- The universal upper-bound package, backed by pinned mathlib's EKR theorem. -/
theorem universalUpperBound : UpperBoundPackage :=
  upperBound_of_mathlibTerminal mathlibUpperBound

/-- Both mathematical packages assemble the exact frozen target expression. -/
theorem exactAssembly : ExactAssembly :=
  composeRoot starAttainment universalUpperBound

/-- Exact kernel closure of the frozen maximum-value target. -/
theorem erdosKoRadoMaximum :
    Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget :=
  rootOfExactAssembly exactAssembly

#check Finset.erdos_ko_rado
#check groundElement
#check starConstruction
#check starImage
#check starIntersecting
#check starSized
#check starCard
#check starAttainment
#check mathlibUpperBound
#check universalUpperBound
#check exactAssembly
#check erdosKoRadoMaximum

assert_no_sorry Finset.erdos_ko_rado
assert_no_sorry groundElement
assert_no_sorry starConstruction
assert_no_sorry starImage
assert_no_sorry starIntersecting
assert_no_sorry starSized
assert_no_sorry starCard
assert_no_sorry starAttainment
assert_no_sorry mathlibUpperBound
assert_no_sorry universalUpperBound
assert_no_sorry exactAssembly
assert_no_sorry erdosKoRadoMaximum

#print sorries Finset.erdos_ko_rado
#print sorries groundElement
#print sorries starConstruction
#print sorries starImage
#print sorries starIntersecting
#print sorries starSized
#print sorries starCard
#print sorries starAttainment
#print sorries mathlibUpperBound
#print sorries universalUpperBound
#print sorries exactAssembly
#print sorries erdosKoRadoMaximum

#print axioms Finset.erdos_ko_rado
#print axioms groundElement
#print axioms starConstruction
#print axioms starImage
#print axioms starIntersecting
#print axioms starSized
#print axioms starCard
#print axioms starAttainment
#print axioms mathlibUpperBound
#print axioms universalUpperBound
#print axioms exactAssembly
#print axioms erdosKoRadoMaximum

end Stage1Instances.THM_M_0822.Proof
