import Mathlib.NumberTheory.NumberField.Basic

/-!
# S1-M-068 / THM-M-0413: the ring of integers of a number field is Dedekind

This Stage1 file records a compile-checked Lean 4 wrapper for the source claim
"the ring of algebraic integers in a number field is a Dedekind domain".

The proof body is the pinned mathlib instance from
`Mathlib.NumberTheory.NumberField.Basic`.
-/

namespace AwesomeTheorems.Stage1.S1_M_068

universe u

open scoped NumberField

/-- Stage1 normalized statement shape for THM-M-0413. -/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K], IsDedekindDomain (𝓞 K)

/--
mathlib wrapper for the theorem that the ring of integers of a number field is a
Dedekind domain.
-/
theorem ringOfIntegers_isDedekindDomain (K : Type u) [Field K] [NumberField K] :
    IsDedekindDomain (𝓞 K) :=
  inferInstance

/-- The Stage1 statement shape is closed by the pinned mathlib wrapper. -/
theorem statementShape_mathlib : StatementShape := by
  intro K _ _
  exact ringOfIntegers_isDedekindDomain K

/--
Auxiliary anchor: mathlib identifies `𝓞 K` as the integral closure of `ℤ` in
the number field `K`.
-/
theorem ringOfIntegers_isIntegralClosure (K : Type u) [Field K] :
    IsIntegralClosure (𝓞 K) ℤ K :=
  inferInstance

/-! ## Machine-readable audit metadata -/

/-- Exact pinned mathlib revision audited for this Stage1 artifact. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.RingTheory.DedekindDomain.IntegralClosure"
]

/-- Pinned mathlib declarations used or audited for this Stage1 artifact. -/
def mathlibAnchorNames : List String := [
  "NumberField",
  "NumberField.RingOfIntegers",
  "NumberField.RingOfIntegers.instIsDedekindDomain",
  "NumberField.RingOfIntegers.instIsIntegralClosureInt",
  "IsIntegralClosure.isDedekindDomain"
]

/-- Public Stage1 anchor rows proposed for the serialized blueprint backfill. -/
def stage1PublicAnchorRows : List String := [
  "mathlib revision | 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "module | Mathlib.NumberTheory.NumberField.Basic",
  "object | NumberField.RingOfIntegers",
  "integral-closure anchor | IsIntegralClosure (𝓞 K) ℤ K",
  "terminal instance | IsDedekindDomain (𝓞 K)"
]

/-- Public theorem-tree package split proposed for the serialized blueprint backfill. -/
def stage1TheoremTreePackages : List String := [
  "P01.statement_normalization | checked | StatementShape fixes K, [Field K], [NumberField K], and IsDedekindDomain (𝓞 K)",
  "P02.mathlib_object_model | checked | NumberField, NumberField.RingOfIntegers, and 𝓞 K imported from Mathlib.NumberTheory.NumberField.Basic",
  "P03.integral_closure_bridge | checked | ringOfIntegers_isIntegralClosure wraps IsIntegralClosure (𝓞 K) ℤ K",
  "P04.repo_local_dedekind_wrapper | checked | ringOfIntegers_isDedekindDomain and statementShape_mathlib validate locally",
  "P05.public_merge_back | unchecked | only serialized public blueprint/todo/README merge-back leaves remain unchecked"
]

/-- Public merge-back leaves that must stay unchecked until serialized docs are updated. -/
def stage1PublicMergeBackUncheckedLeaves : List String := [
  "M0413-L010.public_blueprint_theorem_tree_merge",
  "M0413-L011.public_todo_readme_status_sync"
]

/-- Machine proof debt classification for this checked Stage1 wrapper. -/
def machineProofDebtClassification : List String := [
  "local_wrapper_upstream_mathlib: the terminal source statement is closed by a checked wrapper",
  "proof_body_upstream_mathlib: the Dedekind-domain instance is provided by pinned mathlib",
  "no_repo_local_integration_debt_for_checked_wrapper"
]

/-- Repo-local integration-debt gate for this repair artifact. -/
def repoLocalIntegrationDebtGate : String :=
  "passed for the checked mathlib wrapper; public completion still requires M0387 merge-back and leaf-ledger synchronization"

/-! ## Audit probes -/

#check mathlibPinnedRevision
#check mathlibAnchorModules
#check mathlibAnchorNames
#check stage1PublicAnchorRows
#check stage1TheoremTreePackages
#check stage1PublicMergeBackUncheckedLeaves
#check machineProofDebtClassification
#check repoLocalIntegrationDebtGate

#check NumberField
#check NumberField.RingOfIntegers
#check NumberField.RingOfIntegers.instIsDedekindDomain
#check NumberField.RingOfIntegers.instIsIntegralClosureInt
#check IsIntegralClosure.isDedekindDomain
#check ringOfIntegers_isDedekindDomain
#check statementShape_mathlib

end AwesomeTheorems.Stage1.S1_M_068
