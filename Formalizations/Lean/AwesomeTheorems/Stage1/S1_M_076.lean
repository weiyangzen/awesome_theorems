import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.FieldTheory.Galois.Basic
import Mathlib.RingTheory.Norm.Basic
import Mathlib.Topology.Algebra.OpenSubgroup

/-!
# S1-M-076 / THM-M-0421

Stage1 statement-shape artifact for local class field theory.

The current repo-local mathlib closure has nonarchimedean local fields and
finite Galois groups, but no Artin reciprocity / local class field theory
terminal theorem.  The declarations below keep the expected formal boundary
explicit and add only wrappers that are already supplied by pinned mathlib.
-/

open ValuativeRel Valued.integer

open scoped WithZero

namespace AwesomeTheorems.Stage1.S1_M_076

universe uK uL

/--
A finite abelian extension `L/K`, phrased using mathlib's finite-dimensional
field extension and Galois APIs.
-/
structure FiniteAbelianExtensionData
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L] : Prop where
  finiteDimensional : FiniteDimensional K L
  isGalois : IsGalois K L
  galoisGroup_comm : ∀ σ τ : L ≃ₐ[K] L, σ * τ = τ * σ

/--
The field norm, restricted to unit groups.

For the local-class-field-theory use case this is applied only when `L/K` is
finite-dimensional, as packaged by `FiniteAbelianExtensionData`.  The underlying
mathlib map `Algebra.norm K : L →* K` is available without that hypothesis.
-/
noncomputable def unitNormMap
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L] :
    Lˣ →* Kˣ :=
  Units.map (Algebra.norm K (S := L))

/-- The norm subgroup of `Kˣ` attached to the unit norm map `Lˣ → Kˣ`. -/
noncomputable def unitNormSubgroup
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L] :
    Subgroup Kˣ :=
  (unitNormMap K L).range

@[simp]
theorem unitNormMap_coe
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L]
    (x : Lˣ) :
    ((unitNormMap K L x : Kˣ) : K) = Algebra.norm K (x : L) :=
  rfl

theorem mem_unitNormSubgroup
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L]
    (x : Kˣ) :
    x ∈ unitNormSubgroup K L ↔ ∃ y : Lˣ, unitNormMap K L y = x :=
  MonoidHom.mem_range

/--
Statement-level package for a local reciprocity map attached to a finite
abelian local-field extension.

The `normSubgroup` field is kept explicit so the reciprocity-kernel statement
can refer to it directly, but it is no longer abstract: the field
`normSubgroup_eq_unitNormSubgroup` forces it to be the image of the unit norm
map `Lˣ → Kˣ`.
-/
structure LocalReciprocityData
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L] where
  normSubgroup : Subgroup Kˣ
  normSubgroup_eq_unitNormSubgroup : normSubgroup = unitNormSubgroup K L
  reciprocity : Kˣ →* (L ≃ₐ[K] L)
  kernel_eq_normSubgroup : reciprocity.ker = normSubgroup
  surjective : Function.Surjective reciprocity

namespace LocalReciprocityData

variable {K : Type uK} {L : Type uL} [Field K] [Field L] [Algebra K L]

/-- The statement-level norm subgroup is exactly the image of the unit norm map. -/
theorem normSubgroup_mem_iff (data : LocalReciprocityData K L) (x : Kˣ) :
    x ∈ data.normSubgroup ↔ ∃ y : Lˣ, unitNormMap K L y = x := by
  rw [data.normSubgroup_eq_unitNormSubgroup]
  exact mem_unitNormSubgroup K L x

/-- The reciprocity kernel can equivalently be stated using the concrete norm subgroup. -/
theorem kernel_eq_unitNormSubgroup (data : LocalReciprocityData K L) :
    data.reciprocity.ker = unitNormSubgroup K L := by
  rw [data.kernel_eq_normSubgroup, data.normSubgroup_eq_unitNormSubgroup]

end LocalReciprocityData

/--
An open finite-index subgroup of `Kˣ`, phrased with mathlib's topological
subgroup and subgroup-index APIs.
-/
structure OpenFiniteIndexSubgroupData
    (K : Type uK) [Field K] [TopologicalSpace K] where
  openSubgroup : OpenSubgroup Kˣ
  finiteIndex : openSubgroup.toSubgroup.FiniteIndex

namespace OpenFiniteIndexSubgroupData

variable (K : Type uK) [Field K] [TopologicalSpace K]

/-- The underlying subgroup of `Kˣ`. -/
def carrier (U : OpenFiniteIndexSubgroupData K) : Subgroup Kˣ :=
  U.openSubgroup.toSubgroup

/-- The underlying subgroup is open in the unit-group topology. -/
theorem isOpen (U : OpenFiniteIndexSubgroupData K) :
    IsOpen ((U.carrier : Subgroup Kˣ) : Set Kˣ) := by
  exact U.openSubgroup.isOpen

/-- The underlying subgroup has finite index in `Kˣ`. -/
theorem carrier_finiteIndex (U : OpenFiniteIndexSubgroupData K) :
    (U.carrier : Subgroup Kˣ).FiniteIndex :=
  U.finiteIndex

/-- The quotient by an open finite-index subgroup of `Kˣ` is finite. -/
instance finiteQuotient (U : OpenFiniteIndexSubgroupData K) :
    Finite (Kˣ ⧸ (U.carrier : Subgroup Kˣ)) :=
  letI : (U.carrier : Subgroup Kˣ).FiniteIndex := U.finiteIndex
  Subgroup.finite_quotient_of_finiteIndex

end OpenFiniteIndexSubgroupData

/--
Lean statement-shape candidate for local class field theory over a
nonarchimedean local field.

It has two expected directions:

* every finite abelian extension has a local reciprocity map with kernel the
  norm subgroup;
* every open finite-index subgroup of `Kˣ` should arise as such a norm subgroup.

The second direction is expressed through abstract extension witnesses because
the current repo-local dependency closure has no terminal class-field-theory
construction theorem to instantiate them.
-/
def StatementShape
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] : Prop :=
  (∀ (L : Type uL) [Field L] [Algebra K L],
      FiniteAbelianExtensionData K L → Nonempty (LocalReciprocityData K L)) ∧
    (∀ U : OpenFiniteIndexSubgroupData K,
      ∃ (L : Type uL) (_ : Field L) (_ : Algebra K L),
        Nonempty (FiniteAbelianExtensionData K L) ∧
          ∃ data : LocalReciprocityData K L, data.normSubgroup = U.carrier)

/--
Trivial wrapper showing that `StatementShape` is exactly the pair of data
families described above.  This is a local compile gate, not a proof of local
class field theory.
-/
theorem statementShape_of_reciprocity_and_existence
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K]
    (hReciprocity :
      ∀ (L : Type uL) [Field L] [Algebra K L],
        FiniteAbelianExtensionData K L → Nonempty (LocalReciprocityData K L))
    (hExistence :
      ∀ U : OpenFiniteIndexSubgroupData K,
        ∃ (L : Type uL) (_ : Field L) (_ : Algebra K L),
          Nonempty (FiniteAbelianExtensionData K L) ∧
            ∃ data : LocalReciprocityData K L, data.normSubgroup = U.carrier) :
    @StatementShape.{uK, uL} K _ _ _ _ :=
  ⟨hReciprocity, hExistence⟩

/-! ## Low-level mathlib anchors for local fields -/

/-- A nonarchimedean local field has a discrete valuation ring of integers. -/
theorem localField_integer_isDiscreteValuationRing
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    IsDiscreteValuationRing 𝒪[K] :=
  inferInstance

/-- A nonarchimedean local field has finite residue field. -/
theorem localField_residueField_finite
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Finite 𝓀[K] :=
  inferInstance

/-- The value group of a nonarchimedean local field is isomorphic to `ℤᵐ⁰`. -/
theorem localField_valueGroupWithZeroIsoInt_nonempty
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Nonempty (ValueGroupWithZero K ≃*o ℤᵐ⁰) :=
  ⟨IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt K⟩

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.FieldTheory.Galois.Basic",
  "Mathlib.FieldTheory.Galois.Infinite",
  "Mathlib.NumberTheory.RamificationInertia.Basic",
  "Mathlib.NumberTheory.RamificationInertia.Galois"
]

/-- Search terms that did not locate a terminal local class field theory theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "ClassField",
  "LocalClassFieldTheory",
  "ArtinReciprocity",
  "ReciprocityMap",
  "NormSubgroup",
  "WeilGroup",
  "LocalLanglands"
]

/-!
External audit note for `kbuzzard/ClassFieldTheory`.

Reservoir version `5017044` resolves to commit
`501704442c392704de327d45636951a62af20154`.  That revision contains a local
class field theory blueprint but no closed local Artin reciprocity theorem in
the Lean sources: its local-field files retain proof placeholders, and the
cohomological `reciprocity_iso` itself also uses a proof placeholder.  A newer checked revision,
`11f0a7f3874b6891e8e8290d1e645d61ed06e1aa`, closes a general cohomological
`Rep.reciprocityIso` from a `FiniteClassFormation` hypothesis, but this audit
did not find a Lean theorem instantiating that hypothesis for finite extensions
of nonarchimedean local fields.
-/
def kbuzzardClassFieldTheoryAudit : List String := [
  "501704442c392704de327d45636951a62af20154: no closed local Artin reciprocity theorem found",
  "501704442c392704de327d45636951a62af20154: Rep.split.reciprocity_iso contains a proof placeholder",
  "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa: Rep.reciprocityIso is general finite-class-formation infrastructure",
  "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa: no local finite-class-formation instantiation found"
]

/-!
Dependency pin audit for `kbuzzard/ClassFieldTheory`.

This records a repo-local Lake compatibility test without adding the dependency
to the shared `lakefile.lean`.  In a temporary copy of this repository's Lean
configuration, adding Reservoir commit `501704442c392704de327d45636951a62af20154`
as a git dependency made `lake update ClassFieldTheory` fail under Lean
`v4.29.0`: the imported closure pulled older transitive packages and failed
while building `Batteries.Data.String.Basic` and `Batteries.Data.Array.Match`.

The upstream `v4.29.0` tag dereferences to
`11f0a7f3874b6891e8e8290d1e645d61ed06e1aa`, but that revision's manifest pins
mathlib to `3bd2603b817feffa4cc0ce9f5d6bad4094ca746e`, not this repository's
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; a temporary git-resolution retry was
blocked by a network `git fetch` failure before an import/build result was
obtained.  Therefore no `external_upstream_pinned` status is recorded here.
-/
def kbuzzardClassFieldTheoryDependencyPinAudit : List String := [
  "501704442c392704de327d45636951a62af20154: lake update ClassFieldTheory failed under Lean v4.29.0",
  "501704442c392704de327d45636951a62af20154: failure occurred in older Batteries transitive files",
  "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa: upstream v4.29.0 tag exists",
  "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa: upstream manifest mathlib rev differs from repo mathlib rev",
  "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa: no repo-local import/build validation obtained in this pass"
]

/-!
Stage1 child `S1-M-076-C005` integration gate.

No external terminal Lean theorem for local Artin reciprocity over finite
extensions of nonarchimedean local fields is claimed here.  If a later worker
finds one, the item may only advance after a repo-local pin/import/check
passes; otherwise the exact blocker must remain visible and the parent item
must stay open.
-/
def externalTerminalProofIntegrationGate : List String := [
  "no external terminal local Artin reciprocity theorem is imported into this repository",
  "nearest checked upstream item found in this pass is cohomological finite-class-formation infrastructure, not a local-field terminal theorem",
  "local finite-class-formation instantiation for finite nonarchimedean local field extensions was not found",
  "kbuzzard/ClassFieldTheory 501704442c392704de327d45636951a62af20154 failed Lake resolution under repo Lean v4.29.0",
  "kbuzzard/ClassFieldTheory 11f0a7f3874b6891e8e8290d1e645d61ed06e1aa has a different upstream mathlib revision and no repo-local import validation in this pass",
  "therefore anchor-only external evidence must not be marked completed"
]

/-! ## C006 theorem-tree backfill for local class field theory -/

/-- Status labels for the C006 local-CFT theorem-tree backfill. -/
inductive C006LocalCftStatus where
  /-- The row is backed by declarations or metadata in this file. -/
  | checkedBoundary
  /-- The row remains future formalization work, not a completed theorem claim. -/
  | formalizationDebt
  deriving DecidableEq, Repr

/-- One top-level proof package in the local class field theory theorem tree. -/
structure C006LocalCftPackageRow where
  packageId : String
  packageName : String
  responsibility : String
  repoLocalBoundary : String
  downstreamInterface : String
  status : C006LocalCftStatus
  independentLeafLedger : String
  deriving Repr

/--
C006 package split for local class field theory.

These rows are an integration-ready theorem-tree boundary only.  They do not
claim local Artin reciprocity, Frobenius normalization, ramified compatibility,
or the local existence theorem has been proved in this repository.
-/
def c006LocalCftPackageSplit : List C006LocalCftPackageRow := [
  {
    packageId := "LCFT-P01-norm-subgroups",
    packageName := "norm subgroups",
    responsibility :=
      "identify the statement-level norm subgroup with the image of Lˣ -> Kˣ",
    repoLocalBoundary :=
      "unitNormMap, unitNormSubgroup, LocalReciprocityData.normSubgroup_mem_iff",
    downstreamInterface :=
      "kernel statements can refer to a concrete unit-norm image",
    status := C006LocalCftStatus.checkedBoundary,
    independentLeafLedger := "LCFT-L001 through LCFT-L004, each budgeted <=100"
  },
  {
    packageId := "LCFT-P02-local-reciprocity",
    packageName := "local reciprocity",
    responsibility :=
      "construct or import the local Artin map for finite abelian local extensions",
    repoLocalBoundary :=
      "LocalReciprocityData records the map, kernel equality, and surjectivity fields",
    downstreamInterface :=
      "terminal reciprocity theorem supplying Nonempty (LocalReciprocityData K L)",
    status := C006LocalCftStatus.formalizationDebt,
    independentLeafLedger := "LCFT-L005 through LCFT-L008, each budgeted <=100"
  },
  {
    packageId := "LCFT-P03-unramified-frobenius",
    packageName := "unramified Frobenius normalization",
    responsibility :=
      "normalize uniformizers against arithmetic Frobenius in unramified extensions",
    repoLocalBoundary :=
      "local-field residue/value-group anchors exist; no Frobenius-normalization theorem yet",
    downstreamInterface :=
      "reciprocity sends a chosen uniformizer to the normalized Frobenius element",
    status := C006LocalCftStatus.formalizationDebt,
    independentLeafLedger := "LCFT-L009 through LCFT-L012, each budgeted <=100"
  },
  {
    packageId := "LCFT-P04-ramified-compatibility",
    packageName := "ramified compatibility",
    responsibility :=
      "prove unit filtration, inertia, and norm-compatibility branches for ramified extensions",
    repoLocalBoundary :=
      "ramification/inertia modules were audited, but no LCFT compatibility theorem is imported",
    downstreamInterface :=
      "reciprocity respects inertia, unit filtrations, towers, and norm maps",
    status := C006LocalCftStatus.formalizationDebt,
    independentLeafLedger := "LCFT-L013 through LCFT-L016, each budgeted <=100"
  },
  {
    packageId := "LCFT-P05-existence-theorem",
    packageName := "existence theorem",
    responsibility :=
      "construct the finite abelian local extension attached to an open finite-index subgroup",
    repoLocalBoundary :=
      "OpenFiniteIndexSubgroupData is concrete, but the extension-construction theorem is absent",
    downstreamInterface :=
      "the second component of StatementShape for all open finite-index subgroups of Kˣ",
    status := C006LocalCftStatus.formalizationDebt,
    independentLeafLedger := "LCFT-L017 through LCFT-L020, each budgeted <=100"
  }
]

/-- The C006 local-CFT split has exactly the five requested packages. -/
theorem c006LocalCftPackageSplit_length :
    c006LocalCftPackageSplit.length = 5 := by
  native_decide

/-- One leaf in the C006 local `<=100` theorem-tree ledger. -/
structure C006LocalCftLeafRow where
  leafId : String
  packageId : String
  statementTarget : String
  machineAnchorBoundary : String
  budgetLimit : Nat
  status : C006LocalCftStatus
  deriving Repr

/--
C006 independent local-CFT leaf ledger.

Rows marked `formalizationDebt` are future proof leaves, not completed repo-local
proofs.  The checked norm-subgroup rows are boundary/API rows only; they do not
close local class field theory.
-/
def c006LocalCftLeafLedger : List C006LocalCftLeafRow := [
  {
    leafId := "LCFT-L001",
    packageId := "LCFT-P01-norm-subgroups",
    statementTarget := "define the unit norm map Lˣ -> Kˣ using Algebra.norm",
    machineAnchorBoundary := "checked by unitNormMap",
    budgetLimit := 100,
    status := C006LocalCftStatus.checkedBoundary
  },
  {
    leafId := "LCFT-L002",
    packageId := "LCFT-P01-norm-subgroups",
    statementTarget := "define the concrete norm subgroup as the range of the unit norm map",
    machineAnchorBoundary := "checked by unitNormSubgroup",
    budgetLimit := 100,
    status := C006LocalCftStatus.checkedBoundary
  },
  {
    leafId := "LCFT-L003",
    packageId := "LCFT-P01-norm-subgroups",
    statementTarget := "rewrite membership in the statement norm subgroup as unit-norm membership",
    machineAnchorBoundary := "checked by LocalReciprocityData.normSubgroup_mem_iff",
    budgetLimit := 100,
    status := C006LocalCftStatus.checkedBoundary
  },
  {
    leafId := "LCFT-L004",
    packageId := "LCFT-P01-norm-subgroups",
    statementTarget := "rewrite the reciprocity kernel as the concrete unit norm subgroup",
    machineAnchorBoundary := "checked by LocalReciprocityData.kernel_eq_unitNormSubgroup",
    budgetLimit := 100,
    status := C006LocalCftStatus.checkedBoundary
  },
  {
    leafId := "LCFT-L005",
    packageId := "LCFT-P02-local-reciprocity",
    statementTarget := "state the local Artin map for each finite abelian extension L/K",
    machineAnchorBoundary := "LocalReciprocityData has a field, but no constructor theorem",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L006",
    packageId := "LCFT-P02-local-reciprocity",
    statementTarget := "prove the local Artin map is a group homomorphism",
    machineAnchorBoundary := "requires imported or newly formalized local Artin reciprocity",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L007",
    packageId := "LCFT-P02-local-reciprocity",
    statementTarget := "prove the kernel of local reciprocity is the norm subgroup",
    machineAnchorBoundary := "statement field exists; proof source is absent",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L008",
    packageId := "LCFT-P02-local-reciprocity",
    statementTarget := "prove surjectivity onto Gal(L/K)",
    machineAnchorBoundary := "statement field exists; no terminal local CFT proof imported",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L009",
    packageId := "LCFT-P03-unramified-frobenius",
    statementTarget := "choose the unramified finite-extension branch and residue-field Frobenius target",
    machineAnchorBoundary := "requires unramified-extension and residue automorphism APIs",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L010",
    packageId := "LCFT-P03-unramified-frobenius",
    statementTarget := "prove uniformizer valuation normalization for reciprocity",
    machineAnchorBoundary := "requires local reciprocity construction and value-group normalization",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L011",
    packageId := "LCFT-P03-unramified-frobenius",
    statementTarget := "identify the image of a uniformizer with arithmetic Frobenius",
    machineAnchorBoundary := "no Frobenius-normalization theorem is present in local mathlib closure",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L012",
    packageId := "LCFT-P03-unramified-frobenius",
    statementTarget := "prove residue-degree compatibility in the unramified branch",
    machineAnchorBoundary := "requires residue extension and Galois action compatibility",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L013",
    packageId := "LCFT-P04-ramified-compatibility",
    statementTarget := "state unit-filtration compatibility for ramified extensions",
    machineAnchorBoundary := "unit filtration API has not been integrated into this artifact",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L014",
    packageId := "LCFT-P04-ramified-compatibility",
    statementTarget := "prove inertia compatibility of the local Artin map",
    machineAnchorBoundary := "requires ramification/inertia theorem links plus local reciprocity",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L015",
    packageId := "LCFT-P04-ramified-compatibility",
    statementTarget := "prove tower functoriality for local reciprocity under restriction",
    machineAnchorBoundary := "requires Artin-map functoriality for finite extension towers",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L016",
    packageId := "LCFT-P04-ramified-compatibility",
    statementTarget := "prove local norm-map compatibility for ramified towers",
    machineAnchorBoundary := "requires concrete finite-extension unit norm APIs and reciprocity functoriality",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L017",
    packageId := "LCFT-P05-existence-theorem",
    statementTarget := "state the extension-existence target for every open finite-index subgroup of Kˣ",
    machineAnchorBoundary := "OpenFiniteIndexSubgroupData is checked; construction theorem is absent",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L018",
    packageId := "LCFT-P05-existence-theorem",
    statementTarget := "construct or import the finite abelian extension attached to a subgroup",
    machineAnchorBoundary := "requires local CFT existence theorem or pinned dependency",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L019",
    packageId := "LCFT-P05-existence-theorem",
    statementTarget := "prove the constructed extension has the requested norm subgroup",
    machineAnchorBoundary := "requires norm-subgroup kernel theorem for the constructed extension",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  },
  {
    leafId := "LCFT-L020",
    packageId := "LCFT-P05-existence-theorem",
    statementTarget := "assemble the existence half of StatementShape",
    machineAnchorBoundary := "terminal wrapper waits on LCFT-P01 through LCFT-P05",
    budgetLimit := 100,
    status := C006LocalCftStatus.formalizationDebt
  }
]

/-- The C006 local-CFT ledger records twenty independent leaves. -/
theorem c006LocalCftLeafLedger_length :
    c006LocalCftLeafLedger.length = 20 := by
  native_decide

/-- Every C006 local-CFT leaf is budgeted at most 100 local proof steps. -/
theorem c006LocalCftLeafLedger_budget_le_100 :
    (c006LocalCftLeafLedger.map (fun row => row.budgetLimit)).all
      (fun n => decide (n <= 100)) = true := by
  native_decide

/-- The norm-subgroup package has its own four-leaf ledger. -/
theorem c006NormSubgroupsLeafCount :
    (c006LocalCftLeafLedger.filter
      (fun row => row.packageId == "LCFT-P01-norm-subgroups")).length = 4 := by
  native_decide

/-- The local-reciprocity package has its own four-leaf ledger. -/
theorem c006LocalReciprocityLeafCount :
    (c006LocalCftLeafLedger.filter
      (fun row => row.packageId == "LCFT-P02-local-reciprocity")).length = 4 := by
  native_decide

/-- The unramified-Frobenius package has its own four-leaf ledger. -/
theorem c006UnramifiedFrobeniusLeafCount :
    (c006LocalCftLeafLedger.filter
      (fun row => row.packageId == "LCFT-P03-unramified-frobenius")).length = 4 := by
  native_decide

/-- The ramified-compatibility package has its own four-leaf ledger. -/
theorem c006RamifiedCompatibilityLeafCount :
    (c006LocalCftLeafLedger.filter
      (fun row => row.packageId == "LCFT-P04-ramified-compatibility")).length = 4 := by
  native_decide

/-- The existence-theorem package has its own four-leaf ledger. -/
theorem c006ExistenceTheoremLeafCount :
    (c006LocalCftLeafLedger.filter
      (fun row => row.packageId == "LCFT-P05-existence-theorem")).length = 4 := by
  native_decide

/--
C006 completion gate.

This is deliberately false: this child creates a checked split/ledger surface,
but no terminal local class field theory theorem or pinned external proof
closure has been integrated.
-/
def c006RepoLocalCompletionGate : Bool := false

/-- C006 must not be treated as a completed local CFT proof. -/
theorem c006RepoLocalCompletionGate_eq_false :
    c006RepoLocalCompletionGate = false := rfl

/-! ## Audit probes -/

#check IsNonarchimedeanLocalField
#check IsGalois
#check FiniteAbelianExtensionData
#check unitNormMap
#check unitNormSubgroup
#check mem_unitNormSubgroup
#check LocalReciprocityData
#check LocalReciprocityData.normSubgroup_mem_iff
#check LocalReciprocityData.kernel_eq_unitNormSubgroup
#check StatementShape
#check kbuzzardClassFieldTheoryAudit
#check kbuzzardClassFieldTheoryDependencyPinAudit
#check externalTerminalProofIntegrationGate
#check c006LocalCftPackageSplit
#check c006LocalCftPackageSplit_length
#check c006LocalCftLeafLedger
#check c006LocalCftLeafLedger_length
#check c006LocalCftLeafLedger_budget_le_100
#check c006RepoLocalCompletionGate_eq_false
#check localField_integer_isDiscreteValuationRing
#check localField_residueField_finite
#check localField_valueGroupWithZeroIsoInt_nonempty

end AwesomeTheorems.Stage1.S1_M_076
