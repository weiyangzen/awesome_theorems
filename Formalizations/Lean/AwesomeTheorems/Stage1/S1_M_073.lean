import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# S1-M-073 / THM-M-0418

Stage1 statement-shape and mathlib wrapper for the Minkowski bound for ideal
class representatives in a number field.

The imported mathlib module already proves the key theorem
`NumberField.exists_ideal_in_class_of_norm_le`: every class in the ideal class
group of `𝓞 K` has an integral ideal representative with norm bounded by the
standard Minkowski expression.  This file records the Stage1-normalized shape
and checks a thin repo-local wrapper against the pinned mathlib dependency.
-/

open scoped nonZeroDivisors Real

open Module NumberField Ideal Nat

namespace AwesomeTheorems.Stage1.S1_M_073

universe u

/--
The Minkowski bound used by mathlib's number-field class-number API.

For a number field `K`, this is
`(4 / pi) ^ r₂ * n! / n ^ n * sqrt |discr K|`, where `n = [K : Q]` and
`r₂` is the number of complex places.
-/
noncomputable def minkowskiClassBound (K : Type u) [Field K] [NumberField K] : ℝ :=
  (4 / Real.pi) ^ NumberField.InfinitePlace.nrComplexPlaces K *
    ((finrank ℚ K).factorial / (finrank ℚ K) ^ (finrank ℚ K) *
      Real.sqrt |NumberField.discr K|)

/--
Stage1 normalized statement-shape for THM-M-0418.

Every class in the ideal class group of the ring of integers has a nonzero
integral ideal representative whose absolute norm is bounded by the Minkowski
class bound.
-/
def StatementShape (K : Type u) [Field K] [NumberField K] : Prop :=
  ∀ C : ClassGroup (𝓞 K), ∃ I : (Ideal (𝓞 K))⁰,
    ClassGroup.mk0 I = C ∧ absNorm (I : Ideal (𝓞 K)) ≤ minkowskiClassBound K

/--
Checked local wrapper around mathlib's Minkowski class-representative bound.

This closes the Stage1 statement shape against the pinned mathlib theorem.  It
does not add a new proof of the convex-body theorem; that proof body lives
upstream in mathlib's number-field class-number and canonical-embedding files.
-/
theorem statementShape_of_mathlib (K : Type u) [Field K] [NumberField K] :
    StatementShape K := by
  intro C
  simpa [StatementShape, minkowskiClassBound] using
    NumberField.exists_ideal_in_class_of_norm_le (K := K) C

/--
Optional downstream wrapper: a norm-bounded principal-generator criterion for
the ring of integers to be a PID.

The proof body is the pinned mathlib theorem
`RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_norm_le`; this wrapper
only exposes it with the Stage1-normalized Minkowski bound notation.
-/
theorem ringOfIntegers_pid_of_principal_norm_le (K : Type u) [Field K] [NumberField K]
    (h : ∀ ⦃I : (Ideal (𝓞 K))⁰⦄,
      absNorm (I : Ideal (𝓞 K)) ≤ minkowskiClassBound K →
        Submodule.IsPrincipal (I : Ideal (𝓞 K))) :
    IsPrincipalIdealRing (𝓞 K) := by
  simpa [minkowskiClassBound] using
    (RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_norm_le (K := K) h)

/--
Optional downstream wrapper: a finite-prime PID criterion over the interval
`Finset.Icc 1 ⌊minkowskiClassBound K⌋₊`.

This is a thin Stage1 wrapper around
`RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_pow_le_of_mem_primesOver_of_mem_Icc`.
-/
theorem ringOfIntegers_pid_of_principal_primesOver_interval
    (K : Type u) [Field K] [NumberField K]
    (h : ∀ p ∈ Finset.Icc 1 ⌊minkowskiClassBound K⌋₊, p.Prime →
      ∀ (P : Ideal (𝓞 K)),
        P ∈ primesOver (span {(p : ℤ)}) (𝓞 K) →
          p ^ ((span ({(p : ℤ)} : Set ℤ)).inertiaDeg P) ≤ ⌊minkowskiClassBound K⌋₊ →
            Submodule.IsPrincipal P) :
    IsPrincipalIdealRing (𝓞 K) := by
  simpa [minkowskiClassBound] using
    (RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_pow_le_of_mem_primesOver_of_mem_Icc
      (K := K) h)

/--
Optional downstream wrapper: the Galois finite-prime PID criterion over the
interval `Finset.Icc 1 ⌊minkowskiClassBound K⌋₊`.

This is a thin Stage1 wrapper around
`RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_lt_or_isPrincipal_of_mem_primesOver_of_mem_Icc`.
-/
theorem ringOfIntegers_pid_of_galois_principal_or_large_primesOver_interval
    (K : Type u) [Field K] [NumberField K] [IsGalois ℚ K]
    (h : ∀ p ∈ Finset.Icc 1 ⌊minkowskiClassBound K⌋₊, p.Prime →
      ∃ P ∈ primesOver (span {(p : ℤ)}) (𝓞 K),
        ⌊minkowskiClassBound K⌋₊ <
            p ^ ((span ({(p : ℤ)} : Set ℤ)).inertiaDeg P) ∨
          Submodule.IsPrincipal P) :
    IsPrincipalIdealRing (𝓞 K) := by
  simpa [minkowskiClassBound] using
    (RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_lt_or_isPrincipal_of_mem_primesOver_of_mem_Icc
      (K := K) h)

/-- Repository-pinned mathlib revision used for the terminal Stage1 anchor. -/
def mathlibAnchorPin : String :=
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Terminal Lean 4 anchor for the representative-bound form. -/
def terminalRepresentativeBoundAnchor : String :=
  "NumberField.exists_ideal_in_class_of_norm_le"

/-- mathlib theorem names checked as direct anchors for this Stage1 slot. -/
def mathlibAnchorTheorems : List String := [
  "NumberField.exists_ideal_in_class_of_norm_le",
  "NumberField.mixedEmbedding.exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr",
  "NumberField.mixedEmbedding.exists_ne_zero_mem_ideal_of_norm_le",
  "NumberField.mixedEmbedding.minkowskiBound",
  "RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_norm_le",
  "RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_pow_le_of_mem_primesOver_of_mem_Icc",
  "RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_lt_or_isPrincipal_of_mem_primesOver_of_mem_Icc",
  "NumberField.classNumber_eq_one_iff",
  "ClassGroup.mk0_surjective"
]

/-- Optional downstream PID wrappers checked in this repo-local Stage1 artifact. -/
def optionalDownstreamPidWrappers : List String := [
  "ringOfIntegers_pid_of_principal_norm_le",
  "ringOfIntegers_pid_of_principal_primesOver_interval",
  "ringOfIntegers_pid_of_galois_principal_or_large_primesOver_interval"
]

/-- The optional downstream PID wrapper list has exactly three checked entries. -/
theorem optionalDownstreamPidWrappers_length :
    optionalDownstreamPidWrappers.length = 3 :=
  rfl

/-- mathlib modules audited for the local wrapper and upstream proof body. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.NumberField.Discriminant.Basic",
  "Mathlib.NumberTheory.NumberField.CanonicalEmbedding.ConvexBody",
  "Mathlib.NumberTheory.NumberField.FractionalIdeal",
  "Mathlib.NumberTheory.ClassNumber.Finite",
  "Mathlib.RingTheory.ClassGroup"
]

/--
Public theorem-tree package names prepared for the serial Stage1 backfill.

The proof-body packages below are intentionally marked as upstream mathlib
packages.  This repository checks the local wrapper theorem, but it does not
re-prove the convex-body, discriminant, or class-group reduction internals.
-/
def theoremTreePackages : List String := [
  "S1-M-073.P1.statement_normalization",
  "S1-M-073.P2.class_group_object_model",
  "S1-M-073.P3.minkowski_convex_body_core",
  "S1-M-073.P4.discriminant_norm_bridge",
  "S1-M-073.P5.class_representative_reduction",
  "S1-M-073.P6.pid_generator_criteria",
  "S1-M-073.P7.repo_local_wrapper_gate",
  "S1-M-073.P8.public_surface_backfill"
]

/-- The public theorem-tree split has exactly the requested packages P1-P8. -/
theorem theoremTreePackages_length :
    theoremTreePackages.length = 8 :=
  rfl

/-- One integration-ready package row for the public theorem tree. -/
structure TheoremTreePackageRow where
  packageName : String
  localDuty : String
  upstreamInputs : List String
  downstreamOutputs : List String
  currentRepoLocalStatus : String
  publicBackfillNote : String

/--
Integration-ready package split for the public theorem tree.

Rows P3-P5 are proof-body rows supplied by pinned mathlib.  They are not local
proof-body claims; the locally checked item is the wrapper row P7.
-/
def theoremTreePackageSplit : List TheoremTreePackageRow :=
  [ { packageName := "S1-M-073.P1.statement_normalization"
      localDuty :=
        "freeze the number field, ring of integers, class group, ideal norm, discriminant, degree, complex-place count, and Minkowski bound expression"
      upstreamInputs := [ "NumberField", "NumberField.discr", "NumberField.InfinitePlace.nrComplexPlaces" ]
      downstreamOutputs := [ "minkowskiClassBound", "StatementShape" ]
      currentRepoLocalStatus := "checked_local_definition"
      publicBackfillNote := "Public tree may mark this package checked by the local Lean artifact." },
    { packageName := "S1-M-073.P2.class_group_object_model"
      localDuty :=
        "use mathlib's class group of the ring of integers and nonzero integral ideals as the representative objects"
      upstreamInputs := [ "ClassGroup", "ClassGroup.mk0", "(Ideal (𝓞 K))⁰", "absNorm" ]
      downstreamOutputs := [ "class representative statement interface" ]
      currentRepoLocalStatus := "checked_imported_object_model"
      publicBackfillNote := "Public tree may cite the imported object model and local use in StatementShape." },
    { packageName := "S1-M-073.P3.minkowski_convex_body_core"
      localDuty :=
        "supply the canonical-embedding convex-body existence branch used by the upstream theorem"
      upstreamInputs :=
        [ "NumberField.mixedEmbedding.minkowskiBound",
          "NumberField.mixedEmbedding.exists_ne_zero_mem_ideal_of_norm_le" ]
      downstreamOutputs := [ "bounded nonzero element in an ideal" ]
      currentRepoLocalStatus := "mathlib_backed_upstream_proof_body"
      publicBackfillNote := "Mark as mathlib-backed, not locally re-proved in this repository." },
    { packageName := "S1-M-073.P4.discriminant_norm_bridge"
      localDuty :=
        "convert the convex-body estimate into the explicit discriminant and ideal-norm bound"
      upstreamInputs :=
        [ "NumberField.mixedEmbedding.exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr",
          "NumberField.det_basisOfFractionalIdeal_eq_absNorm" ]
      downstreamOutputs := [ "explicit discriminant/norm bound branch" ]
      currentRepoLocalStatus := "mathlib_backed_upstream_proof_body"
      publicBackfillNote := "Mark as mathlib-backed, not locally re-proved in this repository." },
    { packageName := "S1-M-073.P5.class_representative_reduction"
      localDuty :=
        "derive a bounded integral representative for every class in the ideal class group"
      upstreamInputs := [ "ClassGroup.mk0_surjective", "NumberField.exists_ideal_in_class_of_norm_le" ]
      downstreamOutputs := [ "terminal representative-bound theorem" ]
      currentRepoLocalStatus := "mathlib_backed_terminal_anchor"
      publicBackfillNote := "Use NumberField.exists_ideal_in_class_of_norm_le as the terminal Lean 4 anchor." },
    { packageName := "S1-M-073.P6.pid_generator_criteria"
      localDuty :=
        "record optional downstream PID criteria available from the same mathlib class-number file"
      upstreamInputs :=
        [ "RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_norm_le",
          "RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_pow_le_of_mem_primesOver_of_mem_Icc",
          "RingOfIntegers.isPrincipalIdealRing_of_isPrincipal_of_lt_or_isPrincipal_of_mem_primesOver_of_mem_Icc",
          "NumberField.classNumber_eq_one_iff" ]
      downstreamOutputs :=
        [ "ringOfIntegers_pid_of_principal_norm_le",
          "ringOfIntegers_pid_of_principal_primesOver_interval",
          "ringOfIntegers_pid_of_galois_principal_or_large_primesOver_interval" ]
      currentRepoLocalStatus := "checked_optional_downstream_wrappers"
      publicBackfillNote := "Optional downstream PID wrappers are checked locally by the C004 child artifact." },
    { packageName := "S1-M-073.P7.repo_local_wrapper_gate"
      localDuty :=
        "check the Stage1 StatementShape by a thin wrapper over the pinned mathlib theorem"
      upstreamInputs := [ "NumberField.exists_ideal_in_class_of_norm_le" ]
      downstreamOutputs := [ "statementShape_of_mathlib" ]
      currentRepoLocalStatus := "local_wrapper_upstream_mathlib"
      publicBackfillNote := "This is the checked repo-local machine anchor for the representative-bound form." },
    { packageName := "S1-M-073.P8.public_surface_backfill"
      localDuty :=
        "serially merge the machine anchor, theorem tree, validation note, and status boundary into public planning surfaces"
      upstreamInputs := [ "S1-M-073 parent ledger", "S1-M-073 child ledgers" ]
      downstreamOutputs := [ "consistent public blueprint/todo/README status after merge" ]
      currentRepoLocalStatus := "public_integration_open"
      publicBackfillNote := "Public docs are intentionally not edited by this child worker." } ]

/-- The structured package split has exactly the requested packages P1-P8. -/
theorem theoremTreePackageSplit_length :
    theoremTreePackageSplit.length = 8 :=
  rfl

/-- The structured package split preserves the public package names exactly. -/
theorem theoremTreePackageSplit_names :
    theoremTreePackageSplit.map (fun row => row.packageName) = theoremTreePackages :=
  rfl

/-- One local leaf-budget row prepared for public M0387-level backfill. -/
structure LeafBudgetRow where
  leafId : String
  packageName : String
  localBudget : String
  status : String
  proofBodyLocation : String
  note : String

/--
Compact leaf-budget ledger for the public theorem tree.

The upstream mathlib leaves are recorded as mathlib-backed proof-body leaves.
Only the Stage1 statement shape and wrapper leaves are local proof obligations
closed in this repository.
-/
def leafBudgetLedger : List LeafBudgetRow :=
  [ { leafId := "S1-M-073.L001"
      packageName := "S1-M-073.P1.statement_normalization"
      localBudget := "<=100"
      status := "checked"
      proofBodyLocation := "local_definition"
      note := "minkowskiClassBound typechecks as the normalized bound expression." },
    { leafId := "S1-M-073.L002"
      packageName := "S1-M-073.P1.statement_normalization"
      localBudget := "<=100"
      status := "checked"
      proofBodyLocation := "local_definition"
      note := "StatementShape typechecks with explicit class group, ideal, and norm-bound components." },
    { leafId := "S1-M-073.L003"
      packageName := "S1-M-073.P2.class_group_object_model"
      localBudget := "<=100"
      status := "checked"
      proofBodyLocation := "pinned_mathlib_import_used_locally"
      note := "ClassGroup.mk0 and nonzero integral ideals are imported and used in StatementShape." },
    { leafId := "S1-M-073.L004"
      packageName := "S1-M-073.P3.minkowski_convex_body_core"
      localBudget := "<=100"
      status := "mathlib_backed"
      proofBodyLocation := "pinned_mathlib"
      note := "Convex-body branch is upstream mathlib proof body, not locally re-proved here." },
    { leafId := "S1-M-073.L005"
      packageName := "S1-M-073.P4.discriminant_norm_bridge"
      localBudget := "<=100"
      status := "mathlib_backed"
      proofBodyLocation := "pinned_mathlib"
      note := "Discriminant/norm bridge is upstream mathlib proof body, not locally re-proved here." },
    { leafId := "S1-M-073.L006"
      packageName := "S1-M-073.P5.class_representative_reduction"
      localBudget := "<=100"
      status := "mathlib_backed"
      proofBodyLocation := "pinned_mathlib"
      note := "Representative-bound reduction is supplied by NumberField.exists_ideal_in_class_of_norm_le." },
    { leafId := "S1-M-073.L007"
      packageName := "S1-M-073.P6.pid_generator_criteria"
      localBudget := "<=100"
      status := "checked_optional_wrappers"
      proofBodyLocation := "local_wrappers_over_pinned_mathlib"
      note := "Three downstream PID criteria are exposed by local wrappers over pinned mathlib." },
    { leafId := "S1-M-073.L008"
      packageName := "S1-M-073.P7.repo_local_wrapper_gate"
      localBudget := "<=100"
      status := "checked"
      proofBodyLocation := "local_wrapper_over_pinned_mathlib"
      note := "statementShape_of_mathlib closes by direct use of the terminal mathlib theorem." },
    { leafId := "S1-M-073.L009"
      packageName := "S1-M-073.P8.public_surface_backfill"
      localBudget := "<=100"
      status := "open_public_integration"
      proofBodyLocation := "serial_public_doc_merge"
      note := "Public blueprint/todo/README merge is outside this child worker's write scope." } ]

/-- The compact public leaf ledger currently has nine rows. -/
theorem leafBudgetLedger_length :
    leafBudgetLedger.length = 9 :=
  rfl

/--
Public status surfaces that must agree before S1-M-073 is marked publicly
complete.

This child worker does not edit these shared files.  The list is checked here
so the serial integrator can use the Lean artifact as the machine-side source
for the C005 public merge gate.
-/
def publicStatusAgreementSurfaces : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/-- The C005 public status gate names exactly the three required public surfaces. -/
theorem publicStatusAgreementSurfaces_length :
    publicStatusAgreementSurfaces.length = 3 :=
  rfl

/-- Machine-side facts that the later public status merge must preserve. -/
def publicStatusMachineFacts : List String := [
  "machine_status=local_wrapper_upstream_mathlib",
  "local_artifact=Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_073.lean",
  "terminal_anchor=NumberField.exists_ideal_in_class_of_norm_le",
  "mathlib_pin=leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "proof_body_boundary=upstream_mathlib_not_locally_reproved",
  "integration_debt_gate=closed_for_machine_side"
]

/-- The C005 public status gate records six machine-side facts for merge-back. -/
theorem publicStatusMachineFacts_length :
    publicStatusMachineFacts.length = 6 :=
  rfl

end AwesomeTheorems.Stage1.S1_M_073
