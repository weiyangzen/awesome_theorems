import Mathlib.LinearAlgebra.FreeModule.PID

/-!
# THM-M-0060 discovery-only intake probe

These checks authenticate the pinned Smith-normal-form basis/submodule interfaces. They do not
select the underspecified integer-matrix source claim, establish a matrix/module transport, add a
divisibility or uniqueness condition, or credit any declaration as the exact root proof.
-/

#check Module.Basis.SmithNormalForm
#check Module.Basis.SmithNormalForm.bM
#check Module.Basis.SmithNormalForm.bN
#check Module.Basis.SmithNormalForm.f
#check Module.Basis.SmithNormalForm.a
#check Module.Basis.SmithNormalForm.snf
#check @Submodule.exists_smith_normal_form_of_le
#check @Submodule.smithNormalFormOfLE
#check @Submodule.smithNormalForm
#check Matrix.toLin'
#check LinearMap.toMatrix

#print axioms Submodule.exists_smith_normal_form_of_le
