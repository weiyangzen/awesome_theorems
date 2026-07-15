import Statement
import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0927 conditional obligation composition

This module checks only the exact child-to-root interfaces selected by the
frozen Binet architecture. The substantive function-equality theorem remains
an explicit premise. Inspecting the pinned candidate here does not install it
as the proof-phase root and supplies no accepted closure.
-/

noncomputable section

namespace Stage1Instances.THM_M_0927.ObligationTree

open Stage1Instances.THM_M_0927

/-- The named-root function equality supplied by the substantive pinned
mathlib body `Real.coe_fib_eq'`. -/
def FunctionNamedRootPackage : Prop :=
  (fun n : Nat => (Nat.fib n : Real)) =
    fun n : Nat =>
      (Real.goldenRatio ^ n - Real.goldenConj ^ n) / Real.sqrt 5

/-- The pointwise named-root form between the function body and the frozen
radical spelling. -/
def PointwiseNamedRootPackage : Prop :=
  forall n : Nat,
    (Nat.fib n : Real) =
      (Real.goldenRatio ^ n - Real.goldenConj ^ n) / Real.sqrt 5

/-- Exact conversion from function equality to pointwise equality. -/
def FunctionToPointwiseTransport : Prop :=
  FunctionNamedRootPackage -> PointwiseNamedRootPackage

/-- Exact conversion from named characteristic roots to the source radical
spelling frozen in `BinetFormulaTarget`. -/
def NamedRootToRadicalTransport : Prop :=
  PointwiseNamedRootPackage -> BinetFormulaTarget

/-- The complete conditional child-to-root composition signature. -/
def RootComposition : Prop :=
  FunctionNamedRootPackage ->
    FunctionToPointwiseTransport ->
      NamedRootToRadicalTransport -> BinetFormulaTarget

/-- Checked function-to-pointwise child transport. -/
theorem functionToPointwiseTransport_checked :
    FunctionToPointwiseTransport := by
  intro functionEquality n
  exact congrFun functionEquality n

/-- Checked named-root-to-radical child transport. It reuses the statement
phase's bidirectional algebraic transport without changing the binder. -/
theorem namedRootToRadicalTransport_checked :
    NamedRootToRadicalTransport := by
  intro namedRoot
  apply binetFormulaTarget_iff_characteristicRootTarget.mpr
  intro n
  simpa [PointwiseNamedRootPackage, CharacteristicRootTarget,
    positiveRoot, conjugateRoot, Real.goldenRatio, Real.goldenConj] using namedRoot n

/-- Checked composition shape. The substantive function theorem and both
transports are consumed and none is manufactured. -/
theorem rootComposition_checked : RootComposition := by
  intro functionBinet functionToPointwise namedRootToRadical
  exact namedRootToRadical (functionToPointwise functionBinet)

/-- Exact abstract-child harness for the root composition certificate. -/
theorem root_of_terminal_packages
    (composition : RootComposition)
    (functionBinet : FunctionNamedRootPackage)
    (functionToPointwise : FunctionToPointwiseTransport)
    (namedRootToRadical : NamedRootToRadicalTransport) :
    BinetFormulaTarget :=
  composition functionBinet functionToPointwise namedRootToRadical

#check Real.coe_fib_eq'
#check Real.coe_fib_eq
#check LinearRecurrence.sol_eq_of_eq_init
#check Real.fib_isSol_fibRec
#check Real.geom_goldenRatio_isSol_fibRec
#check Real.geom_goldenConj_isSol_fibRec
#check functionToPointwiseTransport_checked
#check namedRootToRadicalTransport_checked
#check rootComposition_checked
#check root_of_terminal_packages

#print axioms Real.coe_fib_eq'
#print axioms Real.coe_fib_eq
#print axioms functionToPointwiseTransport_checked
#print axioms namedRootToRadicalTransport_checked
#print axioms rootComposition_checked
#print axioms root_of_terminal_packages

assert_no_sorry Real.coe_fib_eq'
assert_no_sorry Real.coe_fib_eq
assert_no_sorry functionToPointwiseTransport_checked
assert_no_sorry namedRootToRadicalTransport_checked
assert_no_sorry rootComposition_checked
assert_no_sorry root_of_terminal_packages

#print sorries Real.coe_fib_eq'
#print sorries Real.coe_fib_eq
#print sorries functionToPointwiseTransport_checked
#print sorries namedRootToRadicalTransport_checked
#print sorries rootComposition_checked
#print sorries root_of_terminal_packages

end Stage1Instances.THM_M_0927.ObligationTree
