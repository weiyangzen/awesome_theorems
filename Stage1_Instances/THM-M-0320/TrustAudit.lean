import Proof

/-!
# THM-M-0320 trust audit surface

This module adds no proof content. It asks Lean to inspect every selected
root-relevant local or vendored declaration after the complete source closure
has been replayed from fresh outputs.
-/

assert_no_sorry Stage1Instances.THM_M_0320.compact_of_closed_bounded
assert_no_sorry Stage1Instances.THM_M_0320.root_of_closedGraph_packages
assert_no_sorry Stage1Instances.THM_M_0320.upperHemicontinuityClosedGraphBridge
assert_no_sorry IndexedLOrder.Scarf
assert_no_sorry IndexedLOrder.GiComponentStructure_holds
assert_no_sorry Brouwer
assert_no_sorry Stage1Instances.THM_M_0320.closedGraphKakutaniCore
assert_no_sorry Stage1Instances.THM_M_0320.kakutaniFixedPoint

#print sorries Stage1Instances.THM_M_0320.compact_of_closed_bounded
#print sorries Stage1Instances.THM_M_0320.root_of_closedGraph_packages
#print sorries Stage1Instances.THM_M_0320.upperHemicontinuityClosedGraphBridge
#print sorries IndexedLOrder.Scarf
#print sorries IndexedLOrder.GiComponentStructure_holds
#print sorries Brouwer
#print sorries Stage1Instances.THM_M_0320.closedGraphKakutaniCore
#print sorries Stage1Instances.THM_M_0320.kakutaniFixedPoint

#print axioms Stage1Instances.THM_M_0320.compact_of_closed_bounded
#print axioms Stage1Instances.THM_M_0320.root_of_closedGraph_packages
#print axioms Stage1Instances.THM_M_0320.upperHemicontinuityClosedGraphBridge
#print axioms IndexedLOrder.Scarf
#print axioms IndexedLOrder.GiComponentStructure_holds
#print axioms Brouwer
#print axioms Stage1Instances.THM_M_0320.closedGraphKakutaniCore
#print axioms Stage1Instances.THM_M_0320.kakutaniFixedPoint
