import Mathlib.NumberTheory.ModularForms.Basic
import Mathlib.NumberTheory.DirichletCharacter.Basic

/-!
# THM-M-0129 statement-infrastructure probe

This module checks the native ordinary modular-form and Dirichlet-character surfaces available in
the pinned closure. It deliberately declares no Shimura-lift target: the closure has no native
half-integral-weight source space, theta-multiplier slash action, or source Hecke operators, and
abstract proposition fields would not encode the source theorem.
-/

namespace Stage1Instances.THM_M_0129.StatementInfrastructure

#check CuspForm
#check DirichletCharacter
#check DirichletCharacter.conductor

set_option autoImplicit false in
#check_failure HalfIntegralWeightModularForm
set_option autoImplicit false in
#check_failure ShimuraLift
set_option autoImplicit false in
#check_failure ShimuraCorrespondence

end Stage1Instances.THM_M_0129.StatementInfrastructure
