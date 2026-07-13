import Statement
import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0498 validation probes

This module imports neither `Proof` nor `ObligationTree`. It independently
rechecks the pinned logarithmic-derivative bridge and the conditional
composition into the exact frozen root. The analytic explicit-formula package
is still an input to the composition probe; no proof of that package or of the
root is supplied here.

These are same-worker differential probes, not a distinct terminal proof body
or an independent-runner attestation.
-/

noncomputable section

open Complex Filter Nat
open scoped Topology

namespace Stage1Instances.THM_M_0498.Validation

open Stage1Instances.THM_M_0498

/-- A separately written exact-type wrapper over the pinned mathlib body. -/
theorem logDerivativeDirect {s : Complex} (hs : 1 < s.re) :
    LSeries (fun n : Nat => ((ArithmeticFunction.vonMangoldt n : Real) : Complex)) s =
      -deriv riemannZeta s / riemannZeta s := by
  exact ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div hs

/-- The exact analytic premise consumed by this validation-only composition
probe. Its proof remains the root-critical open obligation. -/
def AnalyticPackageProbe : Prop :=
  forall (E : NontrivialZeroEnumeration) (x : Real),
    1 < x -> IsNotPrimePower x ->
      Tendsto (fun N : Nat =>
          (x : Complex) - zeroPartialSum E x N - Complex.log (2 * Real.pi) -
            (1 / 2 : Complex) * Complex.log (1 - (x : Complex) ^ (-2 : Complex)))
        atTop (nhds (Chebyshev.psi x : Complex))

/-- Independent exact-type reconstruction of conditional root composition.
This proves the root only from the still-unproved analytic package. -/
theorem rootConditionalProbe (analytic : AnalyticPackageProbe) :
    RiemannVonMangoldtTarget := by
  intro E x hx hpp
  exact analytic E x hx hpp

#check logDerivativeDirect
#check rootConditionalProbe

assert_no_sorry ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
assert_no_sorry logDerivativeDirect
assert_no_sorry rootConditionalProbe

#print sorries ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
  logDerivativeDirect rootConditionalProbe

#print axioms ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
#print axioms logDerivativeDirect
#print axioms rootConditionalProbe

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div,
    ``Stage1Instances.THM_M_0498.Validation.logDerivativeDirect,
    ``Stage1Instances.THM_M_0498.Validation.rootConditionalProbe
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0498.Validation
