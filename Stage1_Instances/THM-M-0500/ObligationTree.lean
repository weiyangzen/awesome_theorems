import Mathlib.NumberTheory.LSeries.PrimesInAP

/-!
# THM-M-0500 conditional obligation composition

This module checks the final composition selected by the frozen architecture. The analytic
non-summability and support-identification packages remain explicit premises; this file does not
claim to implement either package or to close the canonical theorem.
-/

namespace Stage1Instances.THM_M_0500

/-- The canonical target, repeated verbatim because the dossier is outside the Lake source root. -/
def DirichletPrimesInAPTarget : Prop :=
  forall (q : Nat) [NeZero q] (a : ZMod q), IsUnit a ->
    {p : Nat | p.Prime ∧ (p : ZMod q) = a}.Infinite

namespace ObligationTree

open ArithmeticFunction

/-- The analytic terminal result needed by the finite-support contradiction. -/
def PrimeResidueNonSummabilityPackage : Prop :=
  forall (q : Nat) [NeZero q] (a : ZMod q), IsUnit a ->
    ¬ Summable (fun n : Nat =>
      (if n.Prime then vonMangoldt.residueClass a n else 0) / n)

/-- The exact support bridge between the weighted series and the target prime set. -/
def PrimeResidueSupportPackage : Prop :=
  forall (q : Nat) [NeZero q] (a : ZMod q),
    Function.support (fun n : Nat =>
      (if n.Prime then vonMangoldt.residueClass a n else 0) / n) =
      {p : Nat | p.Prime ∧ (p : ZMod q) = a}

/-- Checked child-to-parent composition into the exact canonical target. -/
theorem root_of_terminal_packages
    (nonSummable : PrimeResidueNonSummabilityPackage)
    (support : PrimeResidueSupportPackage) :
    DirichletPrimesInAPTarget := by
  intro q _ a ha
  by_contra! finiteTarget
  apply nonSummable q a ha
  apply summable_of_hasFiniteSupport
  show (Function.support fun n : Nat =>
    (if n.Prime then vonMangoldt.residueClass a n else 0) / n).Finite
  rw [support q a]
  exact finiteTarget

#check ArithmeticFunction.vonMangoldt.not_summable_residueClass_prime_div
#check ArithmeticFunction.vonMangoldt.support_residueClass_prime_div
#print axioms root_of_terminal_packages

end ObligationTree
end Stage1Instances.THM_M_0500
