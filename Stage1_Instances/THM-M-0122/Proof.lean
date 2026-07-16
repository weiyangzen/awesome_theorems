import «ObligationTree»
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0122 proof-phase bodies

This module owns the checked set-theoretic bodies at the end of the frozen
Faltings route. The arithmetic-geometric packages remain explicit premises:
no finite-extension normalization, Jacobian or Abel-Jacobi construction,
Mordell-Weil theorem, or Mordell-Lang theorem is asserted here.
-/

set_option autoImplicit false

noncomputable section

universe u

namespace Stage1Instances.THMM0122.Proof

open Stage1Instances.THMM0122.ObligationTree

/-- A finite codomain and an injective map give a finite domain. -/
theorem finite_of_injective_to {alpha beta : Type u} [Finite beta]
    (f : alpha -> beta) (hf : Function.Injective f) : Finite alpha :=
  Finite.of_injective f hf

/-- The two injection transports used by the frozen normalization/Jacobian
route can be composed without adding an arithmetic-geometric premise. -/
theorem finite_of_two_injections {alpha beta gamma : Type u} [Finite gamma]
    (baseChange : alpha -> beta) (abelJacobi : beta -> gamma)
    (hBaseChange : Function.Injective baseChange)
    (hAbelJacobi : Function.Injective abelJacobi) : Finite alpha := by
  letI : Finite beta := finite_of_injective_to abelJacobi hAbelJacobi
  exact finite_of_injective_to baseChange hBaseChange

/-- Canonical-root assembly from the three exact package interfaces frozen by
the obligation-tree phase. None of those interfaces is manufactured here. -/
theorem faltingsTarget_of_packages
    (normalize : FiniteExtensionNormalization.{u})
    (abelJacobi : AbelJacobiPackage.{u})
    (mordellLang : MordellLangFinitenessPackage.{u}) :
    Stage1Instances.THMM0122.FaltingsTarget.{u} :=
  terminal_of_normalization_abelJacobi_mordellLang
    normalize abelJacobi mordellLang

#check finite_of_injective_to
#check finite_of_two_injections
#check faltingsTarget_of_packages

assert_no_sorry finite_of_injective_to
assert_no_sorry finite_of_two_injections
assert_no_sorry faltingsTarget_of_packages

#print sorries finite_of_injective_to finite_of_two_injections
  faltingsTarget_of_packages
#print axioms finite_of_injective_to
#print axioms finite_of_two_injections
#print axioms faltingsTarget_of_packages

end Stage1Instances.THMM0122.Proof
