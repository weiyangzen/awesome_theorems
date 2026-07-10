import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# S1-M-070 / THM-M-0415: finiteness of the ideal class group

This Stage1 file records a locally checked Lean 4 wrapper for the theorem that the
ideal class group of the ring of integers of a number field is finite.

The proof body is supplied by the pinned mathlib theorem/instance
`NumberField.RingOfIntegers.instFintypeClassGroup`, imported through
`Mathlib.NumberTheory.NumberField.ClassNumber`.
-/

open scoped NumberField

universe u

noncomputable section

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_070

variable (K : Type u) [Field K] [NumberField K]

/-- The ideal class group of the ring of integers of the number field `K`. -/
abbrev IdealClassGroup : Type u :=
  ClassGroup (𝓞 K)

/--
Normalized Stage1 statement shape for THM-M-0415.

For a number field `K`, the ideal class group of its ring of integers is finite.
-/
def StatementShape : Prop :=
  Finite (IdealClassGroup K)

/--
The checked mathlib `Fintype` instance for the ideal class group of `𝓞 K`.

This is an upstream-mathlib wrapper, not a new local proof of Minkowski's theorem.
-/
abbrev idealClassGroupFintype : Fintype (IdealClassGroup K) :=
  NumberField.RingOfIntegers.instFintypeClassGroup K

/-- The ideal class group of a number field is finite. -/
theorem idealClassGroup_finite : StatementShape K := by
  exact (inferInstance : Finite (IdealClassGroup K))

/-- mathlib's class number definition is the cardinality of the ideal class group. -/
theorem classNumber_def :
    NumberField.classNumber K = Fintype.card (IdealClassGroup K) :=
  rfl

/-- The checked mathlib positivity theorem for the class number. -/
theorem classNumber_pos :
    0 < NumberField.classNumber K :=
  NumberField.classNumber_pos K

/-- The checked mathlib bridge between class number one and principality of `𝓞 K`. -/
theorem classNumber_eq_one_iff_pid :
    NumberField.classNumber K = 1 ↔ IsPrincipalIdealRing (𝓞 K) :=
  NumberField.classNumber_eq_one_iff

/-- Modules checked while locating the terminal mathlib anchor for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.ClassNumber.Finite",
  "Mathlib.RingTheory.ClassGroup",
  "Mathlib.NumberTheory.NumberField.Basic"
]

/-- Terminal pinned mathlib theorem/instance anchor for this Stage1 slot. -/
def terminalLeanAnchor : String :=
  "NumberField.RingOfIntegers.instFintypeClassGroup"

/-- Checked upstream route from the general class-number theorem to the local wrapper. -/
def upstreamAnchorRoute : List String := [
  "ClassGroup.fintypeOfAdmissibleOfFinite",
  "NumberField.RingOfIntegers.instFintypeClassGroup",
  "AwesomeTheorems.Stage1.S1_M_070.idealClassGroup_finite"
]

/--
Integration-ready public theorem-tree note for the Stage1 blueprint.

This records the proof-route granularity expected by the M0387-style public
surface without editing the shared public planning documents from this worker.
-/
def publicTheoremTreeRouteNote : List String := [
  "Root: ideal class group finiteness for a number field K, normalized locally as Finite (ClassGroup (𝓞 K)).",
  "Upstream leaf: ClassGroup.fintypeOfAdmissibleOfFinite proves finiteness of the class group for an integral closure in a finite extension when an admissible absolute value is available.",
  "Number-field specialization: NumberField.RingOfIntegers.instFintypeClassGroup applies that theorem over ℚ with AbsoluteValue.absIsAdmissible to obtain Fintype (ClassGroup (𝓞 K)).",
  "Local wrapper: AwesomeTheorems.Stage1.S1_M_070.idealClassGroup_finite converts the Fintype instance into the normalized Finite statement by inferInstance."
]

/-- Search terms used for the local mathlib anchor audit. -/
def localAnchorSearchTerms : List String := [
  "NumberField.RingOfIntegers.instFintypeClassGroup",
  "ClassGroup.fintypeOfAdmissibleOfFinite",
  "NumberField.classNumber",
  "ClassGroup",
  "ringOfIntegers",
  "ideal class"
]

/-- Pinned mathlib revision used by the repo-local wrapper audit. -/
def pinnedMathlibCommit : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- M0387-style machine status after this file validates repo-locally. -/
def machineStatus : String :=
  "local_wrapper_upstream_mathlib"

/-- Local validation command for this Stage1 wrapper. -/
def localValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_070.lean"

/--
Repo-local integration-debt gate for the machine side.

The terminal proof body is in pinned mathlib and this file imports/checks the
local wrapper, so the machine closure is not anchor-only evidence.
-/
def repoLocalIntegrationDebtGate : String :=
  "passed: no completed-state repo_local_integration_debt for the checked wrapper"

/--
Public surfaces that must be synchronized by a serialized integrator before any
public completion claim for this Stage1 slot.
-/
def publicCompletionSurfaces : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md",
  "meta/status surfaces",
  "chosen shared Lean aggregator, if public completion includes aggregator import"
]

/--
C005 public-backfill gate: the machine wrapper is closed, but public completion
still requires serialized synchronization of public checklist/status surfaces.
-/
def publicStatusSynchronizationGate : String :=
  "open until blueprint, todo, README/meta/status surfaces have no stale open checklist for S1-M-070"

end S1_M_070
end Stage1
end AwesomeTheorems
