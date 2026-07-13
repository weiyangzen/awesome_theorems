import Mathlib.Topology.Order.IntermediateValue

/-!
# THM-M-0634 discovery-only intake probe

These checks authenticate adjacent continuous-image and intermediate-value interfaces in the
pinned mathlib snapshot. They do not select the catalog's exact proposition, perform the scheduled
anchor audit, or supply source-fidelity or proof credit.
-/

#check IsConnected.image
#check IsPreconnected.image
#check IsPreconnected.intermediate_value
#check intermediate_value_univ
#check intermediate_value_Icc
#check intermediate_value_Icc'
#check intermediate_value_uIcc

#print axioms IsConnected.image
#print axioms intermediate_value_univ
