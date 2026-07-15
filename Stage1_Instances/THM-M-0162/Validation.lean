import «Stage1_Instances».«THM-M-0162».Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0162 validation probe

This module asks Lean to inspect the existing exact Frenet-Serret proof and the
three frozen equation packages. It intentionally adds no theorem or proof body.

This is a same-worker trust probe, not an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0162.Validation

#check Stage1Instances.THM_M_0162.FrenetSerretTarget
#check Stage1Instances.THM_M_0162.TangentEquationPackage
#check Stage1Instances.THM_M_0162.NormalEquationPackage
#check Stage1Instances.THM_M_0162.BinormalEquationPackage
#check Stage1Instances.THM_M_0162.tangentEquation
#check Stage1Instances.THM_M_0162.normalEquation
#check Stage1Instances.THM_M_0162.binormalEquation
#check Stage1Instances.THM_M_0162.frenetSerret

assert_no_sorry Stage1Instances.THM_M_0162.tangentEquation
assert_no_sorry Stage1Instances.THM_M_0162.normalEquation
assert_no_sorry Stage1Instances.THM_M_0162.binormalEquation
assert_no_sorry Stage1Instances.THM_M_0162.frenetSerret

#print sorries Stage1Instances.THM_M_0162.tangentEquation
#print sorries Stage1Instances.THM_M_0162.normalEquation
#print sorries Stage1Instances.THM_M_0162.binormalEquation
#print sorries Stage1Instances.THM_M_0162.frenetSerret

#print axioms Stage1Instances.THM_M_0162.tangentEquation
#print axioms Stage1Instances.THM_M_0162.normalEquation
#print axioms Stage1Instances.THM_M_0162.binormalEquation
#print axioms Stage1Instances.THM_M_0162.frenetSerret

end Stage1Instances.THM_M_0162.Validation
