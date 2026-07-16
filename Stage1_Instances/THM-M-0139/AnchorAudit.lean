import Mathlib.GroupTheory.Coxeter.Length
import Mathlib.GroupTheory.Coxeter.Inversion
import Mathlib.RingTheory.Polynomial.Basic
import Mathlib.CategoryTheory.Simple
import Mathlib.CategoryTheory.Noetherian

/-!
# THM-M-0139 anchor probes

These checks expose the strongest pinned mathlib substrate found by the
anchor audit. They do not define category `O`, Verma modules, Kazhdan-Lusztig
polynomials, the source-native Conjecture 1.5 target, or a proof of it.
-/

namespace Stage1Instances.THM_M_0139.AnchorAudit

#check CoxeterSystem.length
#check CoxeterSystem.IsLeftDescent
#check CoxeterSystem.IsRightInversion
#check Polynomial.eval
#check CategoryTheory.Simple
#check CategoryTheory.IsArtinianObject
#check CategoryTheory.IsNoetherianObject

#print axioms CoxeterSystem.length
#print axioms CoxeterSystem.IsLeftDescent
#print axioms CoxeterSystem.IsRightInversion
#print axioms Polynomial.eval
#print axioms CategoryTheory.Simple
#print axioms CategoryTheory.IsArtinianObject
#print axioms CategoryTheory.IsNoetherianObject

#print sorries CoxeterSystem.length
#print sorries CoxeterSystem.IsLeftDescent
#print sorries CoxeterSystem.IsRightInversion
#print sorries Polynomial.eval
#print sorries CategoryTheory.Simple
#print sorries CategoryTheory.IsArtinianObject
#print sorries CategoryTheory.IsNoetherianObject

end Stage1Instances.THM_M_0139.AnchorAudit
