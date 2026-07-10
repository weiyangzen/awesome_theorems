import Mathlib.RingTheory.ClassGroup
import Mathlib.RingTheory.DedekindDomain.Factorization
import Mathlib.RingTheory.DedekindDomain.SInteger
import Mathlib.NumberTheory.NumberField.Units.DirichletTheorem

/-!
# S1-M-015 / THM-M-0402: Evertse theorem statement boundary

This Stage1 artifact records a conservative Lean 4 statement shape for the
two-variable S-unit equation finiteness theorem associated with Evertse's
Diophantine work.  The pinned mathlib dependency supplies the S-integer and
S-unit object model over fraction fields of Dedekind domains, but this local
pass did not locate a terminal theorem proving Evertse's S-unit equation bound.

The file therefore keeps the theorem as a precise `StatementShape : Prop` and
checks only wrappers around available S-unit infrastructure.
-/

noncomputable section

open IsDedekindDomain

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_015

universe u v

/-- Audit identifier for the source theorem. -/
def theoremUID : String := "THM-M-0402"

/-- Current machine-proof debt classification for this Stage1 artifact. -/
def machineProofDebt : String := "formalization_debt"

/--
This artifact does not retain repo-local integration debt: no external Lean 4
proof of Evertse's S-unit equation theorem has been pinned into this
repository, and this file makes no completed-state theorem claim.
-/
def repoLocalIntegrationDebtRetained : Bool := false

/-- Current repo-local machine status for the terminal theorem. -/
def currentMachineStatus : String := "not_repo_local_closed"

/-- The repo-local integration-debt gate is closed only in the negative sense recorded above. -/
theorem repoLocalIntegrationDebtRetained_eq_false :
    repoLocalIntegrationDebtRetained = false :=
  rfl

/-- Primary mathematical/source anchors for the statement-boundary audit. -/
def primarySourceAnchors : List String := [
  "Jan-Hendrik Evertse, On sums of S-units and linear recurrences, Compositio Mathematica 53 (1984), no. 2, 225-244",
  "Numdam item CM_1984__53_2_225_0",
  "mathlib4 Mathlib.RingTheory.DedekindDomain.SInteger at the pinned repository revision"
]

/-- The theorem-package split used by the Stage1 public-backfill plan. -/
inductive ProofPackage where
  | statementNormalization
  | mathlibObjectModelAudit
  | coefficientSupportReduction
  | elementaryWrappers
  | heightAndFiniteGenerationBridge
  | evertseCoreOrExternalDependency
  | terminalWrapperAndPublicBackfill
  deriving DecidableEq, Repr

/-- Canonical proof-package order for later public ledger backfill. -/
def proofPackageOrder : List ProofPackage := [
  ProofPackage.statementNormalization,
  ProofPackage.mathlibObjectModelAudit,
  ProofPackage.coefficientSupportReduction,
  ProofPackage.elementaryWrappers,
  ProofPackage.heightAndFiniteGenerationBridge,
  ProofPackage.evertseCoreOrExternalDependency,
  ProofPackage.terminalWrapperAndPublicBackfill
]

/-- Package order starts with statement normalization. -/
theorem proofPackageOrder_head? :
    proofPackageOrder.head? = some ProofPackage.statementNormalization :=
  rfl

/--
M0387-level completion gates that remain required before this Stage1 slot can
be promoted beyond statement/audit status.
-/
def m0387CompletionGates : List String := [
  "machine anchor for a terminal Evertse S-unit theorem must be identified",
  "any external Lean 4 proof must be pinned/imported/checked or recorded as a concrete integration blocker",
  "repo-local Lean validation must pass for the terminal wrapper",
  "human-readable statement/audit/proof-package split must be merged to the public surface",
  "each theorem-tree leaf must have an independent <=100 step ledger",
  "README/meta/blueprint status surfaces must agree before completion"
]

/-- Integration-ready public child leaves for this theorem slot. -/
def publicBackfillLeaves : List String := [
  "THM-M-0402-P0: Add a public statement-shape note defining the Lean object model for S.unit, UnitEquationSolutions, and weighted equation solutions.",
  "THM-M-0402-P1: Add a public mathlib anchor audit table for Mathlib.RingTheory.DedekindDomain.SInteger, number-field units, finite-place support, and class-group infrastructure.",
  "THM-M-0402-P2: Keep this checked Lean statement-only wrapper under the Stage1 namespace, with no proof claim.",
  "THM-M-0402-P3: Prove or import coefficient-support enlargement lemmas for reducing weighted equations to normalized S-unit equations.",
  "THM-M-0402-P4: Re-audit public Lean 4 projects for a complete Evertse or subspace-theorem dependency and record commit/toolchain/module/theorem names.",
  "THM-M-0402-P5: If a checked external proof exists, add it as a pinned Lake dependency or mark a concrete integration blocker.",
  "THM-M-0402-P6: Backfill public theorem-tree and <=100 leaf ledger only after machine anchor status is known."
]

variable {R : Type u} [CommRing R] [IsDedekindDomain R]
variable {K : Type v} [Field K] [Algebra R K] [IsFractionRing R K]

/-! ## P0 statement-shape object model

The public Stage1 object model for this slot is:

* `S : Set (HeightOneSpectrum R)` is the finite set of height-one places that
  may support nontrivial valuations.
* `S.unit K` is mathlib's subgroup of `Kˣ` consisting of S-units.
* `SUnitPair S` is the pair type for the two S-unit unknowns.
* `SUnitFieldValue S x` is the field element represented by an S-unit; all
  equation predicates below use this coercion surface.
* `UnitEquationSolutions S` models the normalized equation `x + y = 1`.
* `WeightedUnitEquationSolutions S a b c` models `a * x + b * y = c`.

The weighted-to-normalized reduction is intentionally not claimed here: it
requires coefficient-support enlargement lemmas before it can be promoted to a
proof package.
-/

/-- Pair type for the two unknowns in an S-unit equation. -/
abbrev SUnitPair (S : Set (HeightOneSpectrum R)) : Type v :=
  (S.unit K) × (S.unit K)

/-- The field element represented by a mathlib S-unit. -/
def SUnitFieldValue (S : Set (HeightOneSpectrum R)) (x : S.unit K) : K :=
  ((x : Kˣ) : K)

/--
Solutions to the weighted two-variable S-unit equation
`a * x + b * y = c`, represented as pairs of elements of mathlib's `S.unit K`
subgroup.
-/
def WeightedUnitEquationSolutions
    (S : Set (HeightOneSpectrum R)) (a b c : K) :
    Set (SUnitPair (R := R) (K := K) S) :=
  {uv | a * SUnitFieldValue (R := R) (K := K) S uv.1 +
      b * SUnitFieldValue (R := R) (K := K) S uv.2 = c}

theorem mem_weightedUnitEquationSolutions_iff
    (S : Set (HeightOneSpectrum R)) (a b c : K)
    (uv : SUnitPair (R := R) (K := K) S) :
    uv ∈ WeightedUnitEquationSolutions (R := R) (K := K) S a b c ↔
      a * SUnitFieldValue (R := R) (K := K) S uv.1 +
        b * SUnitFieldValue (R := R) (K := K) S uv.2 = c :=
  Iff.rfl

/--
Solutions to the normalized two-variable S-unit equation `x + y = 1`.

This is the cleanest source-faithful local statement surface.  Weighted
equations should reduce to this only after coefficient-support enlargement has
been proved or imported.
-/
def UnitEquationSolutions (S : Set (HeightOneSpectrum R)) :
    Set (SUnitPair (R := R) (K := K) S) :=
  {uv | SUnitFieldValue (R := R) (K := K) S uv.1 +
      SUnitFieldValue (R := R) (K := K) S uv.2 = 1}

theorem mem_unitEquationSolutions_iff
    (S : Set (HeightOneSpectrum R))
    (uv : SUnitPair (R := R) (K := K) S) :
    uv ∈ UnitEquationSolutions (R := R) (K := K) S ↔
      SUnitFieldValue (R := R) (K := K) S uv.1 +
        SUnitFieldValue (R := R) (K := K) S uv.2 = 1 :=
  Iff.rfl

/--
Stage1 normalized statement-shape candidate: for every finite set of places
`S`, the solution set of every nonzero weighted two-variable S-unit equation is
finite.

This is a statement boundary only.  It is not a local proof of Evertse's
theorem.
-/
def StatementShape : Prop :=
  ∀ (S : Set (HeightOneSpectrum R)), S.Finite →
    ∀ a b c : K, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      (WeightedUnitEquationSolutions (R := R) (K := K) S a b c).Finite

/-- The normalized statement shape unfolds to the explicit finite-solution claim. -/
theorem statementShape_iff :
    StatementShape (R := R) (K := K) ↔
      ∀ (S : Set (HeightOneSpectrum R)), S.Finite →
        ∀ a b c : K, a ≠ 0 → b ≠ 0 → c ≠ 0 →
          (WeightedUnitEquationSolutions (R := R) (K := K) S a b c).Finite :=
  Iff.rfl

/-! ## P2 statement-only wrapper

This section gives the P2 child a stable checked name for the intended Lean
statement surface.  The definition below is only an alias for `StatementShape`;
it is not a proof of the proposition and it is not a completion claim for
Evertse's theorem.
-/

/-- P2 checked statement-only wrapper for the Evertse S-unit equation surface. -/
def EvertseSUnitEquationStatementOnly : Prop :=
  StatementShape (R := R) (K := K)

/-- P2 status retained in Lean data: this wrapper has no proof claim. -/
def p2StatementOnlyWrapperStatus : String :=
  "checked_statement_only_wrapper_no_proof_claim"

/-- Boolean gate recording that P2 intentionally makes no theorem proof claim. -/
def p2MakesNoProofClaim : Bool := true

/-- The P2 no-proof-claim gate is definitionally true. -/
theorem p2MakesNoProofClaim_eq_true :
    p2MakesNoProofClaim = true :=
  rfl

/-- The P2 wrapper unfolds to the explicit weighted S-unit finiteness statement. -/
theorem evertseSUnitEquationStatementOnly_iff :
    EvertseSUnitEquationStatementOnly (R := R) (K := K) ↔
      ∀ (S : Set (HeightOneSpectrum R)), S.Finite →
        ∀ a b c : K, a ≠ 0 → b ≠ 0 → c ≠ 0 →
          (WeightedUnitEquationSolutions (R := R) (K := K) S a b c).Finite :=
  Iff.rfl

/-- Projection wrapper for later theorem-tree leaves once a terminal proof is supplied. -/
theorem finite_weighted_solutions_of_statementShape
    (h : StatementShape (R := R) (K := K))
    (S : Set (HeightOneSpectrum R)) (hS : S.Finite)
    (a b c : K) (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) :
    (WeightedUnitEquationSolutions (R := R) (K := K) S a b c).Finite :=
  h S hS a b c ha hb hc

/-- Checked mathlib anchor: S-units have valuation one away from `S`. -/
theorem unit_valuation_eq_one_wrapper
    (S : Set (HeightOneSpectrum R)) (x : S.unit K)
    {w : HeightOneSpectrum R} (hw : w ∉ S) :
    w.valuation K ((x : Kˣ) : K) = 1 :=
  Set.unit_valuation_eq_one S K x hw

/-- Checked mathlib anchor: S-units are units of the ring of S-integers. -/
def unitEquivUnitsInteger_wrapper
    (S : Set (HeightOneSpectrum R)) :
    S.unit K ≃* (S.integer K)ˣ :=
  Set.unitEquivUnitsInteger S K

/-- The normalized equation is the weighted equation with all coefficients equal to one. -/
theorem normalized_eq_weighted_one
    (S : Set (HeightOneSpectrum R)) :
    UnitEquationSolutions (R := R) (K := K) S =
      WeightedUnitEquationSolutions (R := R) (K := K) S 1 1 1 := by
  ext uv
  simp [UnitEquationSolutions, WeightedUnitEquationSolutions, SUnitFieldValue]

/-! ## P3 coefficient-support enlargement support lemmas

The classical weighted-to-normalized S-unit equation reduction enlarges the
finite support so that the nonzero coefficients become units.  This file does
not prove that arithmetic coefficient-support construction.  It does check the
repo-local Lean transport layer needed after such an enlargement has been
supplied: S-units remain units over a larger support, solution pairs transport
along that inclusion, and unit coefficients can be divided into the equation to
produce a normalized S-unit pair over the enlarged support.
-/

/-- P3 status retained in Lean data: local support transport is checked, not the full reduction. -/
def p3CoefficientSupportStatus : String :=
  "partial_checked_support: support-monotonic S-unit transport and unit-coefficient normalization are local; coefficient support construction remains formalization_debt"

/-- P3 leaves that remain after the checked transport lemmas below. -/
def p3RemainingLeaves : List String := [
  "construct a finite enlarged support containing the prime support of each nonzero coefficient",
  "prove each coefficient is a unit for the enlarged support",
  "combine coefficient support construction with the checked unit-coefficient normalization map",
  "connect the normalized equation finiteness theorem to weighted equation finiteness through this map"
]

/-- S-units remain S-units after enlarging the permitted support. -/
theorem enlargedSUnit_mem_of_subset
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T) (x : S.unit K) :
    (x : Kˣ) ∈ T.unit K := by
  change ∀ v : HeightOneSpectrum R, v ∉ T → v.valuation K (x : Kˣ) = 1
  intro v hvT
  exact Set.unit_valuation_eq_one S K x (fun hvS => hvT (hST hvS))

/-- The actual coerced S-unit over an enlarged support. -/
def enlargedSUnitOfSubset
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T) (x : S.unit K) : T.unit K :=
  ⟨(x : Kˣ), enlargedSUnit_mem_of_subset (R := R) (K := K) hST x⟩

/-- Enlarging support does not change the underlying field element. -/
theorem enlargedSUnitOfSubset_fieldValue
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T) (x : S.unit K) :
    SUnitFieldValue (R := R) (K := K) T (enlargedSUnitOfSubset (R := R) (K := K) hST x) =
      SUnitFieldValue (R := R) (K := K) S x :=
  rfl

/-- Transport an S-unit solution pair to a larger support. -/
def enlargeSUnitPairOfSubset
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T)
    (uv : SUnitPair (R := R) (K := K) S) :
    SUnitPair (R := R) (K := K) T :=
  (enlargedSUnitOfSubset (R := R) (K := K) hST uv.1,
    enlargedSUnitOfSubset (R := R) (K := K) hST uv.2)

/-- Pair transport along support enlargement preserves the weighted equation predicate. -/
theorem enlargeSUnitPairOfSubset_mem_weighted_iff
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T)
    (a b c : K) (uv : SUnitPair (R := R) (K := K) S) :
    enlargeSUnitPairOfSubset (R := R) (K := K) hST uv ∈
        WeightedUnitEquationSolutions (R := R) (K := K) T a b c ↔
      uv ∈ WeightedUnitEquationSolutions (R := R) (K := K) S a b c := by
  rfl

/--
Normalize a weighted equation after the coefficients have already been shown to
be units for the enlarged support.

For coefficient units `A`, `B`, and `C`, this sends `(x, y)` to
`(C⁻¹ A x, C⁻¹ B y)`.
-/
def coefficientNormalizedPairOfSubset
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T)
    (A B C : T.unit K) (uv : SUnitPair (R := R) (K := K) S) :
    SUnitPair (R := R) (K := K) T :=
  ((C⁻¹ * A) * enlargedSUnitOfSubset (R := R) (K := K) hST uv.1,
    (C⁻¹ * B) * enlargedSUnitOfSubset (R := R) (K := K) hST uv.2)

/--
Once the coefficients are units for the enlarged support, weighted solutions
map to normalized S-unit solutions over that support.
-/
theorem coefficientNormalizedPair_mem_unitEquationSolutions_of_mem_weighted
    {S T : Set (HeightOneSpectrum R)} (hST : S ⊆ T)
    (A B C : T.unit K) (uv : SUnitPair (R := R) (K := K) S)
    (hweighted : uv ∈ WeightedUnitEquationSolutions (R := R) (K := K) S
      ((A : Kˣ) : K) ((B : Kˣ) : K) ((C : Kˣ) : K)) :
    coefficientNormalizedPairOfSubset (R := R) (K := K) hST A B C uv ∈
      UnitEquationSolutions (R := R) (K := K) T := by
  rw [mem_unitEquationSolutions_iff]
  rw [mem_weightedUnitEquationSolutions_iff] at hweighted
  have hC : ((C : Kˣ) : K) ≠ 0 := Units.ne_zero (C : Kˣ)
  dsimp [coefficientNormalizedPairOfSubset, SUnitFieldValue]
  calc
    (((((C⁻¹ * A) * enlargedSUnitOfSubset (R := R) (K := K) hST uv.1 : T.unit K) :
          Kˣ) : K) +
        ((((C⁻¹ * B) * enlargedSUnitOfSubset (R := R) (K := K) hST uv.2 : T.unit K) :
          Kˣ) : K)) =
        ((C : Kˣ) : K)⁻¹ *
          (((A : Kˣ) : K) * SUnitFieldValue (R := R) (K := K) S uv.1 +
            ((B : Kˣ) : K) * SUnitFieldValue (R := R) (K := K) S uv.2) := by
      simp [SUnitFieldValue, enlargedSUnitOfSubset, mul_add, mul_assoc]
    _ = ((C : Kˣ) : K)⁻¹ * ((C : Kˣ) : K) := by
      rw [hweighted]
    _ = 1 := inv_mul_cancel₀ hC

/-! ## Audit probes retained in the checked file. -/

#check HeightOneSpectrum
#check Set.integer
#check Set.unit
#check SUnitPair
#check SUnitFieldValue
#check Set.unit_valuation_eq_one
#check Set.unitEquivUnitsInteger
#check theoremUID
#check machineProofDebt
#check repoLocalIntegrationDebtRetained
#check currentMachineStatus
#check primarySourceAnchors
#check ProofPackage
#check proofPackageOrder
#check m0387CompletionGates
#check publicBackfillLeaves
#check EvertseSUnitEquationStatementOnly
#check p2StatementOnlyWrapperStatus
#check p2MakesNoProofClaim
#check evertseSUnitEquationStatementOnly_iff
#check p3CoefficientSupportStatus
#check p3RemainingLeaves
#check enlargedSUnit_mem_of_subset
#check enlargedSUnitOfSubset
#check enlargeSUnitPairOfSubset
#check enlargeSUnitPairOfSubset_mem_weighted_iff
#check coefficientNormalizedPairOfSubset
#check coefficientNormalizedPair_mem_unitEquationSolutions_of_mem_weighted

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.RingTheory.DedekindDomain.SInteger",
  "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem",
  "Mathlib.NumberTheory.Height.Basic",
  "Mathlib.NumberTheory.Height.NumberField",
  "Mathlib.NumberTheory.Height.Northcott",
  "Mathlib.RingTheory.ClassGroup",
  "Mathlib.RingTheory.DedekindDomain.Factorization",
  "Mathlib.RingTheory.DedekindDomain.SelmerGroup"
]

/-- Pinned declarations used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "Set.integer",
  "Set.unit",
  "Set.integer_valuation_le_one",
  "Set.unit_valuation_eq_one",
  "Set.unitEquivUnitsInteger",
  "IsDedekindDomain.integer_univ",
  "IsDedekindDomain.integer_empty"
]

/-- Search terms that did not locate a terminal Evertse theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Evertse",
  "SUnit",
  "S-unit",
  "unit equation",
  "UnitEquation",
  "SubspaceTheorem",
  "Schlickewei"
]

/-! ## P1 mathlib anchor audit table

This table is intentionally an anchor audit, not a proof claim.  The rows
separate object-model support that is checked in this file from infrastructure
that would still need substantial bridge lemmas before it could contribute to
an Evertse theorem proof.
-/

/-- One row in the P1 mathlib anchor audit table. -/
structure MathlibAnchorAuditRow where
  area : String
  moduleName : String
  declarations : List String
  checkedLocally : Bool
  role : String
  closureStatus : String
  deriving Repr

/-- Public-documentation-ready P1 anchor audit table, retained as checked Lean data. -/
def mathlibAnchorAuditTable : List MathlibAnchorAuditRow := [
  {
    area := "S-integers and S-units",
    moduleName := "Mathlib.RingTheory.DedekindDomain.SInteger",
    declarations := [
      "Set.integer",
      "Set.unit",
      "Set.integer_valuation_le_one",
      "Set.unit_valuation_eq_one",
      "Set.unitEquivUnitsInteger",
      "IsDedekindDomain.integer_univ",
      "IsDedekindDomain.integer_empty"
    ],
    checkedLocally := true,
    role := "Object model for S-integers, S-units, and valuation-one outside S.",
    closureStatus := "usable anchor; the module comments leave finite generation of S-units and Dirichlet S-unit theorem as TODOs"
  },
  {
    area := "number-field units",
    moduleName := "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem",
    declarations := [
      "NumberField.Units.rank",
      "NumberField.Units.fundSystem",
      "NumberField.Units.basisModTorsion",
      "NumberField.Units.rank_modTorsion",
      "NumberField.Units.exist_unique_eq_mul_prod"
    ],
    checkedLocally := true,
    role := "Dirichlet unit theorem infrastructure for ordinary units of the ring of integers.",
    closureStatus := "adjacent infrastructure only; not an S-unit finite-solution theorem"
  },
  {
    area := "finite-place support",
    moduleName := "Mathlib.RingTheory.DedekindDomain.Factorization",
    declarations := [
      "Ideal.hasFiniteMulSupport",
      "FractionalIdeal.finite_factors",
      "Ideal.finite_factors"
    ],
    checkedLocally := true,
    role := "Finite support bookkeeping for height-one prime/valuation support.",
    closureStatus := "bridge input for coefficient-support enlargement; weighted-to-normalized reduction remains open"
  },
  {
    area := "class-group infrastructure",
    moduleName := "Mathlib.RingTheory.ClassGroup",
    declarations := [
      "ClassGroup",
      "ClassGroup.mk",
      "ClassGroup.mk0",
      "ClassGroup.mk0_surjective",
      "ClassGroup.mk_eq_one_iff",
      "card_classGroup_eq_one"
    ],
    checkedLocally := true,
    role := "Class-group objects and quotient maps used by number-field arithmetic infrastructure.",
    closureStatus := "adjacent infrastructure only; no finite class-group theorem or Evertse closure is claimed here"
  }
]

/-- P1 status string: checked anchors are infrastructure, not terminal Evertse proof evidence. -/
def mathlibAnchorAuditStatus : String :=
  "P1 anchors checked locally; terminal Evertse S-unit equation theorem remains not_repo_local_closed"

/-- Checked finite-place support wrapper for nonzero ideals over a Dedekind domain. -/
theorem ideal_finite_factors_wrapper {I : Ideal R} (hI : I ≠ 0) :
    {v : HeightOneSpectrum R | v.asIdeal ∣ I}.Finite :=
  Ideal.finite_factors hI

#check NumberField.Units.rank
#check NumberField.Units.fundSystem
#check NumberField.Units.basisModTorsion
#check NumberField.Units.rank_modTorsion
#check NumberField.Units.exist_unique_eq_mul_prod
#check Ideal.hasFiniteMulSupport
#check Ideal.finite_factors
#check FractionalIdeal.finite_factors
#check ClassGroup
#check ClassGroup.mk
#check ClassGroup.mk0
#check ClassGroup.mk0_surjective
#check ClassGroup.mk_eq_one_iff
#check card_classGroup_eq_one
#check MathlibAnchorAuditRow
#check mathlibAnchorAuditTable
#check mathlibAnchorAuditStatus
#check ideal_finite_factors_wrapper

/-! ## P4 external Lean 4 project audit

This section records the May 1, 2026 external-anchor audit for a complete
Evertse S-unit equation theorem or a usable Schmidt Subspace Theorem dependency.
It is checked metadata only. It does not claim that the public Lean ecosystem
has been exhaustively searched: unauthenticated GitHub code search was blocked
by the current environment, so an authenticated rerun remains a concrete P4
leaf before any public completion claim.
-/

/-- One row in the P4 external Lean 4 project audit table. -/
structure ExternalLeanProjectAuditRow where
  source : String
  repositoryURL : String
  commitOrSnapshot : String
  toolchain : String
  searchedSurface : String
  moduleNames : List String
  theoremNames : List String
  result : String
  integrationAction : String
  deriving Repr

/-- P4 audit rows for complete Evertse/Subspace-Theorem Lean 4 dependencies. -/
def externalLeanProjectAuditRows : List ExternalLeanProjectAuditRow := [
  {
    source := "repo-local pinned mathlib4 dependency",
    repositoryURL := "https://github.com/leanprover-community/mathlib4.git",
    commitOrSnapshot := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    toolchain := "leanprover/lean4:v4.29.0",
    searchedSurface :=
      "rg over pinned Mathlib Lean sources plus Loogle declaration-name probes for Evertse, SubspaceTheorem, SUnit, UnitEquation, Schlickewei, and EvertseFerretti",
    moduleNames := [
      "Mathlib.RingTheory.DedekindDomain.SInteger",
      "Mathlib.NumberTheory.NumberField.Units.DirichletTheorem",
      "Mathlib.NumberTheory.Height.Basic",
      "Mathlib.NumberTheory.Height.NumberField",
      "Mathlib.NumberTheory.Height.Northcott",
      "Mathlib.NumberTheory.DiophantineApproximation.Basic"
    ],
    theoremNames := [
      "Set.integer",
      "Set.unit",
      "Set.unit_valuation_eq_one",
      "Set.unitEquivUnitsInteger",
      "NumberField.Units.rank",
      "NumberField.Units.exist_unique_eq_mul_prod"
    ],
    result :=
      "infrastructure anchors only; no declaration/module named Evertse, SubspaceTheorem, UnitEquation, Schlickewei, or EvertseFerretti was found, and SInteger explicitly leaves finite generation of S-units and Dirichlet's S-unit theorem as TODO",
    integrationAction :=
      "no external proof to pin; terminal theorem remains formalization_debt/not_repo_local_closed"
  },
  {
    source := "repo-local pinned flt-regular dependency",
    repositoryURL := "https://github.com/leanprover-community/flt-regular.git",
    commitOrSnapshot := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
    toolchain := "leanprover/lean4:v4.29.0",
    searchedSurface :=
      "rg over all pinned flt-regular Lean sources for Evertse, SUnit, S-unit, unit equation, UnitEquation, SubspaceTheorem, subspace theorem, Schlickewei, and EvertseFerretti",
    moduleNames := [],
    theoremNames := [],
    result := "no Evertse, S-unit equation, or Subspace Theorem dependency found",
    integrationAction := "no integration target"
  },
  {
    source := "Loogle public mathlib declaration search",
    repositoryURL := "https://loogle.lean-lang.org/json",
    commitOrSnapshot := "public search snapshot queried on 2026-05-01; no commit hash exposed by the JSON endpoint",
    toolchain := "not exposed by endpoint",
    searchedSurface :=
      "declaration-name queries for quoted strings Evertse, SubspaceTheorem, SUnit, and UnitEquation",
    moduleNames := [],
    theoremNames := [],
    result :=
      "0 declarations named with Evertse, 0 with SubspaceTheorem, 0 with UnitEquation; SUnit query only produced generic IsUnit-family noise and not a terminal S-unit equation theorem",
    integrationAction := "negative public mathlib discovery evidence only; not a pin/import target"
  },
  {
    source := "GitHub repository search API",
    repositoryURL := "https://api.github.com/search/repositories",
    commitOrSnapshot := "queried on 2026-05-01",
    toolchain := "not applicable",
    searchedSurface :=
      "repository queries: Evertse Lean; \"Subspace Theorem\" Lean",
    moduleNames := [],
    theoremNames := [],
    result := "both repository queries returned total_count 0",
    integrationAction := "no candidate repository identified by repository search"
  },
  {
    source := "GitHub code search API and gh CLI",
    repositoryURL := "https://api.github.com/search/code",
    commitOrSnapshot := "queried on 2026-05-01",
    toolchain := "not applicable",
    searchedSurface :=
      "code queries for Evertse, SubspaceTheorem, and SUnit in language:Lean",
    moduleNames := [],
    theoremNames := [],
    result :=
      "blocked: gh auth status reported no logged-in host, and unauthenticated REST code search returned GitHub API rate-limit exhaustion",
    integrationAction :=
      "concrete P4 blocker: rerun authenticated GitHub code search before marking P4 complete"
  }
]

/-- P4 status string: no complete external proof was found or imported in this audit pass. -/
def externalLeanProjectAuditStatus : String :=
  "P4 partially audited on 2026-05-01; no complete Evertse/Subspace-Theorem Lean 4 dependency found, authenticated GitHub code search remains blocked"

/-- P4 gate: this audit found no external proof that could leave repo-local integration debt. -/
def p4FoundExternalProofBody : Bool := false

/-- The P4 external-proof-body gate is definitionally negative in this audit pass. -/
theorem p4FoundExternalProofBody_eq_false :
    p4FoundExternalProofBody = false :=
  rfl

#check ExternalLeanProjectAuditRow
#check externalLeanProjectAuditRows
#check externalLeanProjectAuditStatus
#check p4FoundExternalProofBody
#check p4FoundExternalProofBody_eq_false

/-! ## P5 pin/import/check gate

This section records the integration decision forced by the P4 audit rows. No
checked external proof body has been located, so this child cannot add a new
Lake dependency or wrapper theorem. The remaining blocker is concrete and
procedural: authenticated GitHub code search must be rerun, and any candidate
proof found there must be pinned, imported, checked, and audited for placeholder
declarations before any completion claim.
-/

/-- One row in the P5 external-proof integration gate. -/
structure P5IntegrationGateRow where
  gate : String
  currentEvidence : String
  requiredAction : String
  closedForCompletion : Bool
  deriving Repr

/-- P5 gate rows for the current no-pin integration decision. -/
def p5IntegrationGateRows : List P5IntegrationGateRow := [
  {
    gate := "external proof body discovery",
    currentEvidence :=
      "P4 found no complete Evertse S-unit equation or Subspace Theorem Lean 4 proof body in pinned mathlib, pinned flt-regular, Loogle declaration search, or GitHub repository search",
    requiredAction :=
      "rerun authenticated GitHub code search for Evertse, S-unit, SUnit, UnitEquation, SubspaceTheorem, subspace theorem, Schlickewei, and EvertseFerretti before public completion",
    closedForCompletion := false
  },
  {
    gate := "Lake dependency pin/import/check",
    currentEvidence :=
      "no candidate repository, commit, module, or theorem name is available to add to lakefile.lean",
    requiredAction :=
      "if a candidate is found, add a pinned dependency or vendor the proof, import the exact module, and validate a repo-local wrapper theorem",
    closedForCompletion := false
  },
  {
    gate := "placeholder and compatibility audit",
    currentEvidence :=
      "no external source tree is available for placeholder scan, license review, or Lean toolchain compatibility check",
    requiredAction :=
      "for any candidate proof, record repository URL, commit, lean-toolchain, lakefile/lake-manifest compatibility, module path, theorem names, license, and placeholder scan result",
    closedForCompletion := false
  },
  {
    gate := "repo-local integration-debt completion rule",
    currentEvidence :=
      "no anchor-only external proof is being treated as completion evidence; current status remains formalization_debt/not_repo_local_closed",
    requiredAction :=
      "keep the public parent item open until a local proof body, mathlib wrapper, or pinned external dependency validates in this repository",
    closedForCompletion := false
  }
]

/-- P5 status string: no pin/import/check action is available in this pass. -/
def p5PinImportCheckStatus : String :=
  "P5 open on 2026-05-01: no checked external proof body located; no Lake dependency added; authenticated GitHub code search remains the concrete blocker"

/-- P5 gate: no checked external proof body is currently available to pin. -/
def p5CheckedExternalProofLocated : Bool := false

/-- P5 gate: no new Lake dependency was added for THM-M-0402 in this child. -/
def p5PinnedLakeDependencyAdded : Bool := false

/-- P5 gate: no anchor-only external proof is retained as completed evidence. -/
def p5AnchorOnlyCompletionEvidenceRetained : Bool := false

/-- The P5 external-proof discovery gate is definitionally negative in this pass. -/
theorem p5CheckedExternalProofLocated_eq_false :
    p5CheckedExternalProofLocated = false :=
  rfl

/-- The P5 dependency-addition gate is definitionally negative in this pass. -/
theorem p5PinnedLakeDependencyAdded_eq_false :
    p5PinnedLakeDependencyAdded = false :=
  rfl

/-- The P5 anchor-only completion-evidence gate is definitionally negative in this pass. -/
theorem p5AnchorOnlyCompletionEvidenceRetained_eq_false :
    p5AnchorOnlyCompletionEvidenceRetained = false :=
  rfl

#check P5IntegrationGateRow
#check p5IntegrationGateRows
#check p5PinImportCheckStatus
#check p5CheckedExternalProofLocated
#check p5PinnedLakeDependencyAdded
#check p5AnchorOnlyCompletionEvidenceRetained
#check p5CheckedExternalProofLocated_eq_false
#check p5PinnedLakeDependencyAdded_eq_false
#check p5AnchorOnlyCompletionEvidenceRetained_eq_false

/-! ## P6 public theorem-tree backfill gate

P6 is a public-documentation integration task, not a proof task.  The checked
data below records that the theorem-tree and `<=100` leaf ledger are ready as a
proposal, but must not be merged as a public completion surface until the P4
and P5 machine-anchor gates are settled.
-/

/-- One public-backfill readiness gate for P6. -/
structure P6PublicBackfillGateRow where
  gate : String
  currentEvidence : String
  requiredAction : String
  closedForPublicBackfill : Bool
  deriving Repr

/-- P6 public-backfill gates.  The public merge is intentionally blocked. -/
def p6PublicBackfillGateRows : List P6PublicBackfillGateRow := [
  {
    gate := "machine anchor status",
    currentEvidence :=
      "currentMachineStatus is not_repo_local_closed, P4 found no proof body in checked local/published surfaces, and authenticated GitHub code search remains blocked",
    requiredAction :=
      "rerun authenticated GitHub code search and settle P4 before treating the machine-anchor status as public-backfill-ready",
    closedForPublicBackfill := false
  },
  {
    gate := "external proof integration",
    currentEvidence :=
      "p5CheckedExternalProofLocated and p5PinnedLakeDependencyAdded are both false; no external dependency was added",
    requiredAction :=
      "if an external proof is found, pin/import/check it or record the concrete integration blocker before any completion claim",
    closedForPublicBackfill := false
  },
  {
    gate := "repo-local integration-debt rule",
    currentEvidence :=
      "p5AnchorOnlyCompletionEvidenceRetained is false, so no anchor-only evidence is being counted as completed",
    requiredAction :=
      "keep the public checkbox open unless a local proof body, mathlib wrapper, or pinned external dependency validates in this repository",
    closedForPublicBackfill := true
  },
  {
    gate := "private-to-public merge discipline",
    currentEvidence :=
      "this worker owns only the private child ledger and the Stage1 Lean artifact, not the shared public blueprint or todo surfaces",
    requiredAction :=
      "serial integrator should merge the proposal text after machine-anchor status is settled",
    closedForPublicBackfill := false
  }
]

/-- P6 status string: integration-ready proposal exists, but public backfill is blocked. -/
def p6PublicBackfillStatus : String :=
  "P6 open on 2026-05-01: theorem-tree and <=100 leaf ledger proposal recorded; public backfill blocked until P4/P5 machine-anchor status is settled"

/-- P6 gate: machine anchor status is not settled enough for public completion backfill. -/
def p6MachineAnchorStatusSettledForPublicBackfill : Bool := false

/-- P6 gate: public blueprint/todo backfill was not performed by this child. -/
def p6PublicDocsBackfilledByChild : Bool := false

/-- P6 gate: this child makes no theorem completion claim. -/
def p6MakesNoCompletionClaim : Bool := true

/-- The P6 machine-anchor gate remains open. -/
theorem p6MachineAnchorStatusSettledForPublicBackfill_eq_false :
    p6MachineAnchorStatusSettledForPublicBackfill = false :=
  rfl

/-- The P6 public-doc write gate is definitionally negative for this child. -/
theorem p6PublicDocsBackfilledByChild_eq_false :
    p6PublicDocsBackfilledByChild = false :=
  rfl

/-- The P6 no-completion-claim gate is definitionally true. -/
theorem p6MakesNoCompletionClaim_eq_true :
    p6MakesNoCompletionClaim = true :=
  rfl

/-- One proposed public theorem-tree node for the later serial backfill. -/
structure P6TheoremTreeNode where
  nodeId : String
  parentId : String
  packageLabel : String
  obligation : String
  machineStatus : String
  publicMergeStatus : String
  deriving Repr

/-- Integration-ready theorem-tree package split for THM-M-0402. -/
def p6ProposedTheoremTree : List P6TheoremTreeNode := [
  {
    nodeId := "THM-M-0402",
    parentId := "root",
    packageLabel := "terminal theorem",
    obligation := "finite solutions to the two-variable weighted S-unit equation over a finite support",
    machineStatus := "not_repo_local_closed",
    publicMergeStatus := "keep open; no terminal Lean proof body or pinned dependency"
  },
  {
    nodeId := "THM-M-0402-P0",
    parentId := "THM-M-0402",
    packageLabel := "statement normalization",
    obligation := "define S.unit, SUnitPair, UnitEquationSolutions, and WeightedUnitEquationSolutions",
    machineStatus := "checked statement/object model in this file",
    publicMergeStatus := "merge as statement-shape evidence only"
  },
  {
    nodeId := "THM-M-0402-P1",
    parentId := "THM-M-0402",
    packageLabel := "mathlib anchor audit",
    obligation := "audit SInteger, number-field units, finite support, and class-group infrastructure",
    machineStatus := "checked infrastructure anchors only",
    publicMergeStatus := "merge as non-terminal anchor table"
  },
  {
    nodeId := "THM-M-0402-P2",
    parentId := "THM-M-0402",
    packageLabel := "statement-only wrapper",
    obligation := "provide a checked Stage1 proposition alias with no proof claim",
    machineStatus := "checked statement-only wrapper",
    publicMergeStatus := "merge without marking theorem complete"
  },
  {
    nodeId := "THM-M-0402-P3",
    parentId := "THM-M-0402",
    packageLabel := "coefficient-support reduction",
    obligation := "transport S-units across support enlargement and reduce unit coefficients to normalized form",
    machineStatus := "partial checked transport; coefficient-support construction remains formalization_debt",
    publicMergeStatus := "merge as partial reduction only"
  },
  {
    nodeId := "THM-M-0402-P4",
    parentId := "THM-M-0402",
    packageLabel := "external Lean project audit",
    obligation := "find or rule out a complete Evertse/Subspace-Theorem Lean dependency",
    machineStatus := "partial negative audit; authenticated GitHub code search blocked",
    publicMergeStatus := "keep open until authenticated search is rerun"
  },
  {
    nodeId := "THM-M-0402-P5",
    parentId := "THM-M-0402",
    packageLabel := "pin/import/check gate",
    obligation := "pin a located external proof or record a concrete integration blocker",
    machineStatus := "no checked external proof located; no Lake dependency added",
    publicMergeStatus := "keep open"
  },
  {
    nodeId := "THM-M-0402-P6",
    parentId := "THM-M-0402",
    packageLabel := "public backfill gate",
    obligation := "backfill public theorem tree and <=100 leaf ledger after machine-anchor status is settled",
    machineStatus := "this proposal is checked metadata only",
    publicMergeStatus := "blocked until P4/P5 are settled"
  }
]

/-- One proposed `<=100` public leaf-ledger row for the later serial backfill. -/
structure P6LeafLedgerRow where
  leafId : String
  packageId : String
  obligation : String
  budget : String
  status : String
  deriving Repr

/-- Integration-ready `<=100` leaf ledger summary for THM-M-0402. -/
def p6ProposedLeafLedger : List P6LeafLedgerRow := [
  {
    leafId := "L-0402-001",
    packageId := "P0",
    obligation := "checked object model for S-unit pairs, field values, normalized solutions, and weighted solutions",
    budget := "<=100",
    status := "checked in this file as statement-shape infrastructure"
  },
  {
    leafId := "L-0402-002",
    packageId := "P1",
    obligation := "checked wrappers for Set.unit_valuation_eq_one, Set.unitEquivUnitsInteger, and finite ideal support",
    budget := "<=100",
    status := "checked infrastructure anchor"
  },
  {
    leafId := "L-0402-003",
    packageId := "P2",
    obligation := "checked proposition alias EvertseSUnitEquationStatementOnly and projection wrapper from StatementShape",
    budget := "<=100",
    status := "checked statement-only wrapper; no proof claim"
  },
  {
    leafId := "L-0402-004",
    packageId := "P3",
    obligation := "checked support-enlargement transport and unit-coefficient normalization map",
    budget := "<=100",
    status := "partial checked reduction support"
  },
  {
    leafId := "L-0402-005",
    packageId := "P3",
    obligation := "construct finite coefficient support for arbitrary nonzero coefficients",
    budget := "<=100",
    status := "open formalization_debt"
  },
  {
    leafId := "L-0402-006",
    packageId := "P4",
    obligation := "rerun authenticated GitHub code search for Evertse/S-unit/Subspace-Theorem Lean sources",
    budget := "<=100",
    status := "open audit blocker"
  },
  {
    leafId := "L-0402-007",
    packageId := "P5",
    obligation := "pin/import/check any found external proof or record exact integration blocker",
    budget := "<=100",
    status := "open; no candidate currently located"
  },
  {
    leafId := "L-0402-008",
    packageId := "P6",
    obligation := "serially merge public theorem-tree and leaf ledger after P4/P5 are settled",
    budget := "<=100",
    status := "open public-doc integration task"
  }
]

#check P6PublicBackfillGateRow
#check p6PublicBackfillGateRows
#check p6PublicBackfillStatus
#check p6MachineAnchorStatusSettledForPublicBackfill
#check p6PublicDocsBackfilledByChild
#check p6MakesNoCompletionClaim
#check p6MachineAnchorStatusSettledForPublicBackfill_eq_false
#check p6PublicDocsBackfilledByChild_eq_false
#check p6MakesNoCompletionClaim_eq_true
#check P6TheoremTreeNode
#check p6ProposedTheoremTree
#check P6LeafLedgerRow
#check p6ProposedLeafLedger

end S1_M_015
end Stage1
end AwesomeTheorems
