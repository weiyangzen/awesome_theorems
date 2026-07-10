import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.RamificationInertia.Unramified

/-!
# S1-M-075 / THM-M-0420: Hilbert class field

This Stage1 artifact records a Lean 4 statement-shape boundary for the Hilbert
class field theorem: the maximal everywhere-unramified abelian extension of a
number field.  The pinned mathlib snapshot has number fields, rings of integers,
class groups, finite-prime ramification and unramifiedness, but no terminal class
field theory theorem or Hilbert-class-field construction.
-/

open scoped NumberField

universe uK uL uM

namespace AwesomeTheorems.Stage1.S1_M_075

/--
Finite-prime unramifiedness for an extension of number fields, expressed using
mathlib's ring-of-integers and commutative-algebra predicate
`Algebra.IsUnramifiedAt`.

This deliberately ranges over nonzero prime ideals of `𝓞 L`.  It does not try to
encode infinite-place behavior; the Hilbert class field is unramified at finite
places in the usual algebraic-number-theory statement.
-/
def IsEverywhereUnramifiedAtFinitePrimes
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] : Prop :=
  ∀ (P : Ideal (𝓞 L)) [P.IsPrime], P ≠ ⊥ → Algebra.IsUnramifiedAt (𝓞 K) P

/-- Abelianity of the finite Galois group of a number-field extension. -/
def IsAbelianGaloisExtension
    (K : Type uK) (L : Type uL) [Field K] [Field L] [Algebra K L] : Prop :=
  IsGalois K L ∧ ∀ σ τ : L ≃ₐ[K] L, σ * τ = τ * σ

/--
Stage1 core statement for a candidate Hilbert class field `L/K`.

The fields record the three theorem-level requirements usually packaged as
"the Hilbert class field":

* `L/K` is finite Galois with abelian Galois group;
* it is unramified at all finite primes;
* its Galois group is identified with the ideal class group of `K`;
* it is maximal among finite everywhere-unramified abelian extensions, expressed
  as the existence of a `K`-algebra embedding into `L`.

This is a statement-shape, not a construction or proof.  A later proof can
replace it by a concrete mathlib theorem, a pinned external theorem, or a local
construction plus Artin reciprocity.
-/
structure HilbertClassFieldCore
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L] : Prop where
  isAbelianGalois : IsAbelianGaloisExtension K L
  unramifiedAtFinitePrimes : IsEverywhereUnramifiedAtFinitePrimes K L
  classGroupEquiv : Nonempty ((L ≃ₐ[K] L) ≃* ClassGroup (𝓞 K))
  maximal :
    ∀ (M : Type uM) [Field M] [NumberField M] [Algebra K M] [Module.Finite K M],
      IsAbelianGaloisExtension K M →
      IsEverywhereUnramifiedAtFinitePrimes K M →
      Nonempty (M →ₐ[K] L)

/--
Lean statement-shape candidate for `L` being the Hilbert class field of `K`.

The extension field `L` remains an explicit parameter because mathlib currently
does not expose a Hilbert-class-field object.  A terminal formalization should
either quantify over such an `L` with a uniqueness clause, define a canonical
object, or import a pinned upstream construction.
-/
def StatementShape
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L] : Prop :=
  Nonempty (HilbertClassFieldCore.{uK, uL, uM} K L)

/-! ## Statement-orientation decision for child `S1-M-075-C001` -/

/--
Canonical Stage1 orientation selected for the Hilbert-class-field statement.

The checked file keeps `L` explicit in `StatementShape K L`, then exposes an
existential theorem-root wrapper below.  This avoids pretending that the pinned
mathlib snapshot already provides a constructed canonical Hilbert-class-field
object.
-/
inductive StatementOrientationDecision where
  | explicitCandidatePredicateWithExistentialRoot
  | constructedCanonicalObject
  deriving DecidableEq, Repr

/-- Child `S1-M-075-C001` selects the explicit-candidate orientation. -/
def canonicalStatementOrientation : StatementOrientationDecision :=
  .explicitCandidatePredicateWithExistentialRoot

/-- Repo-local check of the selected Hilbert-class-field statement orientation. -/
theorem canonicalStatementOrientation_eq_explicitCandidate :
    canonicalStatementOrientation =
      .explicitCandidatePredicateWithExistentialRoot := rfl

/--
Root existence statement for a Hilbert class field of `K` under the selected
orientation.

This still does not construct `L`.  It packages the theorem root as "there
exists an explicit finite number-field extension candidate satisfying
`StatementShape`", while downstream proof leaves can keep working with the
explicit parameter `L`.
-/
def HilbertClassFieldExists
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (L : Type uL) (_ : Field L) (_ : NumberField L) (_ : Algebra K L)
    (_ : Module.Finite K L), StatementShape.{uK, uL, uM} K L

/--
Any checked explicit candidate proves the existential root statement.  This is
only a packaging lemma for the selected orientation, not a proof that such an
`L` exists.
-/
theorem statementShape_implies_hilbertClassFieldExists
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L]
    (h : StatementShape.{uK, uL, uM} K L) :
    HilbertClassFieldExists.{uK, uL, uM} K := by
  exact ⟨L, inferInstance, inferInstance, inferInstance, inferInstance, h⟩

/-- The selected orientation does not use a constructed canonical object. -/
def usesConstructedHilbertClassFieldObject : Bool := false

/-- Repo-local check that the selected orientation keeps `L` explicit. -/
theorem usesConstructedHilbertClassFieldObject_eq_false :
    usesConstructedHilbertClassFieldObject = false := rfl

/-- Public child-task text for later serial blueprint/todo backfill. -/
def statementOrientationPublicTask : String :=
  "Backfill S1-M-075-C001 as completed for statement orientation: keep L explicit via StatementShape K L and use HilbertClassFieldExists only as an existential root wrapper; do not claim a constructed Hilbert-class-field object until a pinned/imported/checked construction exists."

/-- Checked mathlib anchor: the ring of integers of a number field is Dedekind. -/
theorem ringOfIntegers_isDedekind
    (K : Type uK) [Field K] [NumberField K] :
    IsDedekindDomain (𝓞 K) := by
  infer_instance

/-- Checked mathlib anchor: the number-field class number is the class-group cardinality. -/
theorem classNumber_def
    (K : Type uK) [Field K] [NumberField K] :
    NumberField.classNumber K = Fintype.card (ClassGroup (𝓞 K)) :=
  rfl

/-- Checked mathlib wrapper: class number one is equivalent to PID for `𝓞 K`. -/
theorem classNumber_eq_one_iff_pid
    (K : Type uK) [Field K] [NumberField K] :
    NumberField.classNumber K = 1 ↔ IsPrincipalIdealRing (𝓞 K) :=
  NumberField.classNumber_eq_one_iff

/-- Checked mathlib wrapper: the base case `ℚ` has class number one. -/
theorem rat_classNumber_eq_one : NumberField.classNumber ℚ = 1 :=
  Rat.classNumber_eq

/--
Checked mathlib wrapper: for rings of integers, finite-prime unramifiedness is
equivalent to ramification index one.

This is not the Hilbert class field theorem.  It records the local finite-prime
predicate that the final theorem must quantify over.
-/
theorem isUnramifiedAt_iff_ramificationIdx_eq_one
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L]
    {P : Ideal (𝓞 L)} [P.IsPrime] (hP : P ≠ ⊥) :
    Algebra.IsUnramifiedAt (𝓞 K) P ↔
      Ideal.ramificationIdx (Ideal.under (𝓞 K) P) P = 1 :=
  Algebra.isUnramifiedAt_iff_of_isDedekindDomain (R := 𝓞 K) (S := 𝓞 L) (p := P) hP

/-! ## Finite-prime ramification branch for child `S1-M-075-C004` -/

/--
For a fixed finite prime `p` of the base ring of integers, every prime of
`𝓞 L` lying above `p` is unramified over `𝓞 K`.

This is the `Ideal.primesOver`-indexed form needed by the Hilbert-class-field
finite-prime branch.
-/
def IsUnramifiedOverBasePrime
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] (p : Ideal (𝓞 K)) [p.IsPrime] : Prop :=
  ∀ P : Ideal.primesOver p (𝓞 L), Algebra.IsUnramifiedAt (𝓞 K) (P : Ideal (𝓞 L))

/--
For a fixed finite prime `p` of the base ring of integers, every prime of
`𝓞 L` lying above `p` has ramification index one.
-/
def HasRamificationIdxOneOverBasePrime
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] (p : Ideal (𝓞 K)) [p.IsPrime] : Prop :=
  ∀ P : Ideal.primesOver p (𝓞 L),
    Ideal.ramificationIdx p (P : Ideal (𝓞 L)) = 1

/--
Single-base-prime wrapper for the finite-prime branch: over a nonzero base
prime `p`, the `Ideal.primesOver`-indexed unramified predicate is equivalent to
ramification index one at every prime above `p`.
-/
theorem isUnramifiedOverBasePrime_iff_ramificationIdx_eq_one
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L]
    {p : Ideal (𝓞 K)} [p.IsPrime] (hp : p ≠ ⊥) :
    IsUnramifiedOverBasePrime K L p ↔
      HasRamificationIdxOneOverBasePrime K L p := by
  constructor
  · intro h P
    have hPne : (P : Ideal (𝓞 L)) ≠ ⊥ :=
      Ideal.ne_bot_of_mem_primesOver hp P.2
    have hiff :=
      isUnramifiedAt_iff_ramificationIdx_eq_one K L
        (P := (P : Ideal (𝓞 L))) hPne
    have hram :
        Ideal.ramificationIdx (Ideal.under (𝓞 K) (P : Ideal (𝓞 L)))
            (P : Ideal (𝓞 L)) = 1 :=
      hiff.mp (h P)
    have hunder : Ideal.under (𝓞 K) (P : Ideal (𝓞 L)) = p :=
      (Ideal.LiesOver.over (P := (P : Ideal (𝓞 L))) (p := p)).symm
    simpa [hunder] using hram
  · intro h P
    have hPne : (P : Ideal (𝓞 L)) ≠ ⊥ :=
      Ideal.ne_bot_of_mem_primesOver hp P.2
    have hiff :=
      isUnramifiedAt_iff_ramificationIdx_eq_one K L
        (P := (P : Ideal (𝓞 L))) hPne
    have hunder : Ideal.under (𝓞 K) (P : Ideal (𝓞 L)) = p :=
      (Ideal.LiesOver.over (P := (P : Ideal (𝓞 L))) (p := p)).symm
    exact hiff.mpr (by simpa [hunder] using h P)

/--
All nonzero finite base primes have ramification index one at all primes above
them.
-/
def AllPrimesOverHaveRamificationIdxOne
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] : Prop :=
  ∀ (p : Ideal (𝓞 K)) [p.IsPrime], p ≠ ⊥ →
    HasRamificationIdxOneOverBasePrime K L p

/--
Global finite-prime branch wrapper: finite-prime unramifiedness for every
nonzero prime of `𝓞 L` is equivalent to ramification index one over every
nonzero base prime and every prime in `Ideal.primesOver`.

This is a checked local algebraic-number-theory bridge only.  It does not prove
Hilbert class field existence, Artin reciprocity, maximality, or uniqueness.
-/
theorem everywhereUnramifiedAtFinitePrimes_iff_all_primesOver_ramificationIdx_eq_one
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L] :
    IsEverywhereUnramifiedAtFinitePrimes K L ↔
      AllPrimesOverHaveRamificationIdxOne K L := by
  constructor
  · intro h p hpprime hp P
    have hPne : (P : Ideal (𝓞 L)) ≠ ⊥ :=
      Ideal.ne_bot_of_mem_primesOver hp P.2
    have hiff :=
      isUnramifiedAt_iff_ramificationIdx_eq_one K L
        (P := (P : Ideal (𝓞 L))) hPne
    have hram :
        Ideal.ramificationIdx (Ideal.under (𝓞 K) (P : Ideal (𝓞 L)))
            (P : Ideal (𝓞 L)) = 1 :=
      hiff.mp (h (P : Ideal (𝓞 L)) hPne)
    have hunder : Ideal.under (𝓞 K) (P : Ideal (𝓞 L)) = p :=
      (Ideal.LiesOver.over (P := (P : Ideal (𝓞 L))) (p := p)).symm
    simpa [hunder] using hram
  · intro h P hPprime hPne
    let p : Ideal (𝓞 K) := Ideal.under (𝓞 K) P
    have hpne : p ≠ ⊥ := Ideal.under_ne_bot (A := 𝓞 K) hPne
    have hram :
        Ideal.ramificationIdx p P = 1 :=
      h p hpne (Ideal.primesOver.mk p P)
    exact
      (isUnramifiedAt_iff_ramificationIdx_eq_one K L (P := P) hPne).mpr hram

/-- Child `S1-M-075-C004` has a checked finite-prime branch wrapper. -/
def finitePrimeUnramifiedBranchUsesPrimesOver : Bool := true

/-- Repo-local check for the C004 finite-prime branch marker. -/
theorem finitePrimeUnramifiedBranchUsesPrimesOver_eq_true :
    finitePrimeUnramifiedBranchUsesPrimesOver = true := rfl

/-- Public child-task text for later serial blueprint/todo backfill of `S1-M-075-C004`. -/
def finitePrimeUnramifiedBranchPublicTask : String :=
  "Backfill S1-M-075-C004 as completed for the finite-prime unramified branch wrapper: add the checked predicates IsUnramifiedOverBasePrime, HasRamificationIdxOneOverBasePrime, and AllPrimesOverHaveRamificationIdxOne, plus the checked bridges isUnramifiedOverBasePrime_iff_ramificationIdx_eq_one and everywhereUnramifiedAtFinitePrimes_iff_all_primesOver_ramificationIdx_eq_one. These use Algebra.isUnramifiedAt_iff_of_isDedekindDomain, Ideal.ramificationIdx, and Ideal.primesOver. Keep THM-M-0420 open because this branch is supporting infrastructure, not Hilbert class field existence, Artin reciprocity, maximality, or uniqueness."

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.NumberField.FinitePlaces",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.RamificationInertia.Basic",
  "Mathlib.NumberTheory.RamificationInertia.Galois",
  "Mathlib.NumberTheory.RamificationInertia.Unramified",
  "Mathlib.RingTheory.ClassGroup"
]

/-- Search terms that did not locate a terminal Hilbert class field theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Hilbert class field",
  "HilbertClassField",
  "ClassField",
  "class field theory",
  "maximal unramified abelian",
  "Artin reciprocity"
]

/-! ## External primary-source audit for child `S1-M-075-C002` -/

/--
One row of the Stage1 external-anchor audit.

This is deliberately metadata, not theorem evidence.  A row only becomes a
completion anchor after the referenced project is pinned/imported into this
repository and a local Lean command checks the imported theorem.
-/
structure ExternalPrimarySourceAuditRow where
  repositoryUrl : String
  commitHash : String
  leanGeneration : String
  relevantNames : List String
  sorryStatus : String
  repoLocalIntegrationStatus : String
  conclusion : String
  deriving Repr

/--
Primary-source audit rows for global class field theory / Hilbert class fields.

The rows record exact repositories, commits, relevant declarations, and
placeholder status found during child task `S1-M-075-C002`.  None is a checked
repo-local proof of the Hilbert class field theorem.
-/
def externalPrimarySourceAuditRows : List ExternalPrimarySourceAuditRow := [
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commitHash := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    leanGeneration := "Lean 4, pinned local mathlib dependency",
    relevantNames := [
      "Algebra.isUnramifiedAt_iff_of_isDedekindDomain",
      "Ideal.ramificationIdx",
      "Ideal.primesOver",
      "ClassGroup",
      "NumberField.classNumber"
    ],
    sorryStatus := "No terminal global class field theory or HilbertClassField theorem found in the local pinned tree.",
    repoLocalIntegrationStatus := "local_wrapper_upstream_mathlib only for supporting finite-prime/class-group anchors",
    conclusion := "supporting anchors only; not a Hilbert class field completion"
  },
  {
    repositoryUrl := "https://github.com/kbuzzard/ClassFieldTheory",
    commitHash := "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa",
    leanGeneration := "Lean 4, leanprover/lean4:v4.29.0",
    relevantNames := [
      "ClassFieldTheory.Cohomology.SplittingModule.reciprocityIso",
      "ClassFieldTheory.IsNonarchimedeanLocalField.Unramified.UnramifiedExtension.splits",
      "ClassFieldTheory.IsNonarchimedeanLocalField.Unramified.maximalUnramified",
      "ClassFieldTheory.IsNonarchimedeanLocalField.Unramified.le_maximalUnramified_iff"
    ],
    sorryStatus := "Active source tree contains 27 `sorry` occurrences; no Hilbert class field or global CFT terminal theorem found.",
    repoLocalIntegrationStatus := "not imported; project mathlib manifest uses 3bd2603b817feffa4cc0ce9f5d6bad4094ca746e, not the repo pin",
    conclusion := "useful future local-CFT/cohomology source; current blocker is active sorry plus dependency mismatch"
  },
  {
    repositoryUrl := "https://github.com/mariainesdff/LocalClassFieldTheory",
    commitHash := "9ebdafa0b464df096037c10a2597c40f7e046602",
    leanGeneration := "Lean 4, leanprover/lean4:v4.22.0-rc2",
    relevantNames := [
      "LocalClassFieldTheory.LocalField.Basic",
      "LocalClassFieldTheory.LocalField.GaloisConnection",
      "LocalClassFieldTheory.DiscreteValuationRing.Ramification",
      "LocalClassFieldTheory.DiscreteValuationRing.Extensions"
    ],
    sorryStatus := "Active source tree contains 114 `sorry` occurrences; scope is local-field infrastructure, not a global Hilbert class field theorem.",
    repoLocalIntegrationStatus := "not imported; project mathlib manifest uses 81a4b04c3ae8a45c367ee1664e82b618694462c4, not the repo pin",
    conclusion := "not a repo-local completion anchor for THM-M-0420"
  },
  {
    repositoryUrl := "https://github.com/mariainesdff/ideles-journal",
    commitHash := "fe49f5246910592f8ac56c5470b34f2c66a23220",
    leanGeneration := "Lean 3.42.1",
    relevantNames := [
      "main_theorem_of_global_CFT.group_isomorphism",
      "main_theorem_of_global_CFT.homeomorph",
      "G_K_ab",
      "C_K.map_to_class_group"
    ],
    sorryStatus := "`main_theorem_of_global_CFT.group_isomorphism` and continuity fields in `homeomorph` are `sorry`; active src tree has 3 `sorry` occurrences.",
    repoLocalIntegrationStatus := "not Lean 4 and not importable into the current Lake project",
    conclusion := "historical Lean 3 statement/idele anchor only; no Lean 4 completion"
  },
  {
    repositoryUrl := "https://github.com/mariainesdff/ideles",
    commitHash := "b85d242f18cbdb7a8755c048c2d4cb7b3c675127",
    leanGeneration := "Lean 3.51.1",
    relevantNames := [
      "idele and class-group infrastructure"
    ],
    sorryStatus := "Lean 3 project; no Lean 4 Hilbert class field theorem checked for this Stage1 slot.",
    repoLocalIntegrationStatus := "not Lean 4 and not importable into the current Lake project",
    conclusion := "not a repo-local completion anchor for THM-M-0420"
  }
]

/-- Child `S1-M-075-C002` found no external repo-local completion anchor. -/
def externalPrimarySourceAuditHasRepoLocalHilbertClassFieldCompletion : Bool := false

/--
Public child-task text for later serial blueprint/todo backfill of
`S1-M-075-C002`.
-/
def externalPrimarySourceAuditPublicTask : String :=
  "Backfill S1-M-075-C002 as an external-anchor audit task: record mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95 as supporting finite-prime/class-group infrastructure only; record kbuzzard/ClassFieldTheory@11f0a7f3874b6891e8e8290d1e645d61ed06e1aa as Lean 4 in-progress with active sorry and a mismatched mathlib pin; record mariainesdff/LocalClassFieldTheory@9ebdafa0b464df096037c10a2597c40f7e046602 as Lean 4 local-field infrastructure with active sorry and a mismatched mathlib pin; record mariainesdff/ideles-journal@fe49f5246910592f8ac56c5470b34f2c66a23220 and mariainesdff/ideles@b85d242f18cbdb7a8755c048c2d4cb7b3c675127 as Lean 3 ideles/global-CFT statement anchors only. Keep THM-M-0420 open because no external Lean 4 Hilbert class field theorem was pinned, imported, and checked repo-locally."

/-! ## Lake dependency-compatibility audit for child `S1-M-075-C003` -/

/--
One row of the Stage1 Lake dependency-compatibility audit.

This records whether an external Lean 4 class-field-theory project can be added
as a dependency without changing this repository's pinned mathlib revision.
-/
structure ExternalLakeDependencyCompatibilityRow where
  repositoryUrl : String
  commitHash : String
  projectLeanToolchain : String
  projectMathlibRevision : String
  repoMathlibRevision : String
  canAddWithoutPinnedMathlibConflict : Bool
  activeSorryStatus : String
  terminalHilbertClassFieldTheorem : String
  dependencyDecision : String
  blocker : String
  deriving Repr

/--
Compatibility rows for external Lean 4 class-field-theory projects checked for
child `S1-M-075-C003`.

The local repository currently pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.  Neither Lean 4 candidate below
uses that revision in its manifest, so neither can be added as a direct Lake
dependency without a dependency-resolution conflict or a porting step.
-/
def externalLakeDependencyCompatibilityRows : List ExternalLakeDependencyCompatibilityRow := [
  {
    repositoryUrl := "https://github.com/kbuzzard/ClassFieldTheory",
    commitHash := "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa",
    projectLeanToolchain := "leanprover/lean4:v4.29.0",
    projectMathlibRevision := "3bd2603b817feffa4cc0ce9f5d6bad4094ca746e",
    repoMathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    canAddWithoutPinnedMathlibConflict := false,
    activeSorryStatus := "27 `sorry` occurrences in the active source tree during C002 audit",
    terminalHilbertClassFieldTheorem := "No terminal global CFT / Hilbert class field theorem found for THM-M-0420",
    dependencyDecision := "do not add as direct Lake dependency for this child",
    blocker := "Same Lean toolchain as this repo, but mathlib revision differs; also active sorry and no terminal Hilbert class field target"
  },
  {
    repositoryUrl := "https://github.com/mariainesdff/LocalClassFieldTheory",
    commitHash := "9ebdafa0b464df096037c10a2597c40f7e046602",
    projectLeanToolchain := "leanprover/lean4:v4.22.0-rc2",
    projectMathlibRevision := "81a4b04c3ae8a45c367ee1664e82b618694462c4",
    repoMathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    canAddWithoutPinnedMathlibConflict := false,
    activeSorryStatus := "114 `sorry` occurrences in the active source tree during C002 audit",
    terminalHilbertClassFieldTheorem := "Local-field / DVR infrastructure only; no global Hilbert class field theorem",
    dependencyDecision := "do not add as direct Lake dependency for this child",
    blocker := "Lean toolchain and mathlib revision both differ from this repo; active sorry; scope is local rather than global Hilbert class fields"
  }
]

/-- Child `S1-M-075-C003` found no direct external Lake dependency candidate. -/
def externalLakeDependencyCompatibilityHasImportableCandidate : Bool := false

/-- Repo-local check that the dependency-compatibility audit remains open. -/
theorem externalLakeDependencyCompatibilityHasImportableCandidate_eq_false :
    externalLakeDependencyCompatibilityHasImportableCandidate = false := rfl

/--
Public child-task text for later serial blueprint/todo backfill of
`S1-M-075-C003`.
-/
def externalLakeDependencyCompatibilityPublicTask : String :=
  "Backfill S1-M-075-C003 as completed for dependency-compatibility auditing but not as a Hilbert class field theorem completion: this repository pins mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95. kbuzzard/ClassFieldTheory@11f0a7f3874b6891e8e8290d1e645d61ed06e1aa uses Lean 4 v4.29.0 but pins mathlib@3bd2603b817feffa4cc0ce9f5d6bad4094ca746e, has active sorry, and has no terminal Hilbert class field theorem target, so it should not be added as a direct Lake dependency without a port/pin plan. mariainesdff/LocalClassFieldTheory@9ebdafa0b464df096037c10a2597c40f7e046602 uses Lean 4 v4.22.0-rc2 and mathlib@81a4b04c3ae8a45c367ee1664e82b618694462c4, has active sorry, and covers local-field infrastructure rather than global Hilbert class fields, so it is also blocked. No external Lean 4 class-field-theory dependency is currently importable without conflicting with the pinned mathlib revision."

/-! ## Artin reciprocity map interface for child `S1-M-075-C005` -/

/--
Statement-shape type for the Hilbert-class-field Artin reciprocity map.

The map is oriented from the ideal class group of the base number field to the
`K`-algebra automorphism group of the candidate extension `L/K`, as requested by
the public Stage1 child task.  This is only the interface type; the pinned local
mathlib snapshot does not provide a global Artin reciprocity construction or
proof that this is the Hilbert-class-field Artin map.
-/
abbrev ArtinReciprocityMapShape
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] : Type _ :=
  ClassGroup (𝓞 K) →* (L ≃ₐ[K] L)

/--
Extract the Artin-map orientation from a multiplicative equivalence between the
Galois group and the ideal class group.

This lemma is structural only: it converts the existing `HilbertClassFieldCore`
class-group equivalence orientation into a monoid homomorphism
`ClassGroup (𝓞 K) →* L ≃ₐ[K] L`.  It is not a construction of the Artin
reciprocity map from ideals/Frobenius elements.
-/
noncomputable def artinReciprocityMapFromClassGroupEquiv
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L]
    (e : (L ≃ₐ[K] L) ≃* ClassGroup (𝓞 K)) :
    ArtinReciprocityMapShape K L :=
  e.symm.toMonoidHom

/--
Any checked `HilbertClassFieldCore` witness supplies an Artin-map-shaped
homomorphism in the requested direction.

This packages an already-supplied class-group equivalence; it does not prove
Hilbert class field existence and does not close Artin reciprocity.
-/
theorem hilbertClassFieldCore_nonempty_artinReciprocityMapShape
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L]
    (h : HilbertClassFieldCore.{uK, uL, uM} K L) :
    Nonempty (ArtinReciprocityMapShape K L) := by
  rcases h.classGroupEquiv with ⟨e⟩
  exact ⟨artinReciprocityMapFromClassGroupEquiv K L e⟩

/--
Child `S1-M-075-C005` has only a repo-local Artin-map interface, not a checked
global Artin reciprocity theorem.
-/
def hasRepoLocalGlobalArtinReciprocityTheorem : Bool := false

/--
Repo-local gate check: no terminal Artin reciprocity theorem is being claimed
for the Hilbert class field slot.
-/
theorem hasRepoLocalGlobalArtinReciprocityTheorem_eq_false :
    hasRepoLocalGlobalArtinReciprocityTheorem = false := rfl

/--
Public child-task text for later serial blueprint/todo backfill of
`S1-M-075-C005`.
-/
def artinReciprocityMapPublicTask : String :=
  "Backfill S1-M-075-C005 as completed only for the repo-local Artin-map interface: add ArtinReciprocityMapShape K L := ClassGroup (𝓞 K) →* (L ≃ₐ[K] L), oriented from the base ideal class group to the K-algebra automorphism group, plus the checked structural wrapper artinReciprocityMapFromClassGroupEquiv and hilbertClassFieldCore_nonempty_artinReciprocityMapShape. Keep the Artin reciprocity theorem itself open: no pinned/imported/checked Lean 4 global class field theory theorem currently constructs this map from ideals/Frobenius elements or proves reciprocity for THM-M-0420."

/-! ## Artin reciprocity isomorphism split for child `S1-M-075-C006` -/

/--
One M0387-style leaf in the future proof of
`HCF.L015.unchecked.artin_reciprocity_isomorphism`.

These rows are a checked theorem-tree planning surface.  They do not assert the
existence of an Artin reciprocity isomorphism and do not prove any of the four
listed properties.
-/
structure ArtinReciprocityIsomorphismLeaf where
  nodeId : String
  parentNode : String
  leafName : String
  proofTarget : String
  status : String
  debtClass : String
  maxStepBudget : Nat
  repoLocalClosed : Bool
  deriving Repr

/--
Independent leaves for splitting
`HCF.L015.unchecked.artin_reciprocity_isomorphism`.

The split is intentionally property-oriented: homomorphism, injectivity,
surjectivity, and Hilbert-class-field compatibility can be assigned and closed
separately before any final isomorphism wrapper is claimed.
-/
def artinReciprocityIsomorphismLeaves : List ArtinReciprocityIsomorphismLeaf := [
  {
    nodeId := "HCF.L015.HOM",
    parentNode := "HCF.L015.unchecked.artin_reciprocity_isomorphism",
    leafName := "homomorphism",
    proofTarget := "Prove the Artin map ClassGroup (O K) ->* (L ~=_[K] L) respects multiplication.",
    status := "unchecked",
    debtClass := "formalization_debt",
    maxStepBudget := 100,
    repoLocalClosed := false
  },
  {
    nodeId := "HCF.L015.INJ",
    parentNode := "HCF.L015.unchecked.artin_reciprocity_isomorphism",
    leafName := "injectivity",
    proofTarget := "Prove the kernel of the Artin map is trivial.",
    status := "unchecked",
    debtClass := "formalization_debt",
    maxStepBudget := 100,
    repoLocalClosed := false
  },
  {
    nodeId := "HCF.L015.SURJ",
    parentNode := "HCF.L015.unchecked.artin_reciprocity_isomorphism",
    leafName := "surjectivity",
    proofTarget := "Prove every K-algebra automorphism of L is in the image of the Artin map.",
    status := "unchecked",
    debtClass := "formalization_debt",
    maxStepBudget := 100,
    repoLocalClosed := false
  },
  {
    nodeId := "HCF.L015.COMPAT",
    parentNode := "HCF.L015.unchecked.artin_reciprocity_isomorphism",
    leafName := "compatibility",
    proofTarget := "Prove compatibility with the finite-prime Frobenius and Hilbert-class-field unramified/maximality interfaces.",
    status := "unchecked",
    debtClass := "formalization_debt",
    maxStepBudget := 100,
    repoLocalClosed := false
  }
]

/-- Repo-local check: C006 split has exactly the four requested independent leaves. -/
theorem artinReciprocityIsomorphismLeaves_nodeIds :
    artinReciprocityIsomorphismLeaves.map (fun row => row.nodeId) =
      ["HCF.L015.HOM", "HCF.L015.INJ", "HCF.L015.SURJ", "HCF.L015.COMPAT"] := rfl

/-- Repo-local check: every C006 leaf currently has an unchecked status. -/
theorem artinReciprocityIsomorphismLeaves_statuses :
    artinReciprocityIsomorphismLeaves.map (fun row => row.status) =
      ["unchecked", "unchecked", "unchecked", "unchecked"] := rfl

/-- Repo-local check: every C006 leaf has a local proof budget of at most 100 steps. -/
theorem artinReciprocityIsomorphismLeaves_budgets :
    artinReciprocityIsomorphismLeaves.map (fun row => row.maxStepBudget) =
      [100, 100, 100, 100] := rfl

/--
Repo-local gate check: the C006 split is not a completed Artin reciprocity
isomorphism proof.
-/
theorem artinReciprocityIsomorphismLeaves_repoLocalClosed :
    artinReciprocityIsomorphismLeaves.map (fun row => row.repoLocalClosed) =
      [false, false, false, false] := rfl

/-- Child `S1-M-075-C006` provides only a checked split, not a proof closure. -/
def hasRepoLocalArtinReciprocityIsomorphismProof : Bool := false

/-- Checked gate for the C006 non-completion boundary. -/
theorem hasRepoLocalArtinReciprocityIsomorphismProof_eq_false :
    hasRepoLocalArtinReciprocityIsomorphismProof = false := rfl

/--
Public child-task text for later serial blueprint/todo backfill of
`S1-M-075-C006`.
-/
def artinReciprocityIsomorphismSplitPublicTask : String :=
  "Backfill S1-M-075-C006 as completed for theorem-tree splitting only: HCF.L015.unchecked.artin_reciprocity_isomorphism is split into HCF.L015.HOM, HCF.L015.INJ, HCF.L015.SURJ, and HCF.L015.COMPAT, covering homomorphism, injectivity, surjectivity, and compatibility leaves. Each leaf has status unchecked, debt class formalization_debt, repoLocalClosed false, and a <=100-step local budget. Keep the Artin reciprocity isomorphism theorem and THM-M-0420 open until those leaves are replaced by repo-local checked proof bodies or pinned/imported/checked upstream proofs."

/-! ## Maximality embedding interface for child `S1-M-075-C007` -/

/--
The finite everywhere-unramified abelian extension hypothesis for a candidate
extension `M/K`.

Finiteness is carried by the `[Module.Finite K M]` instance in this predicate's
context.  The proposition itself packages only the abelian Galois and
finite-prime unramified hypotheses.
-/
def IsFiniteEverywhereUnramifiedAbelianExtension
    (K : Type uK) (M : Type uM) [Field K] [NumberField K] [Field M]
    [NumberField M] [Algebra K M] [Module.Finite K M] : Prop :=
  IsAbelianGaloisExtension K M ∧ IsEverywhereUnramifiedAtFinitePrimes K M

/--
The requested embedding conclusion for maximality of a Hilbert-class-field
candidate `L/K` against another finite everywhere-unramified abelian extension
`M/K`.
-/
abbrev HilbertClassFieldMaximalityEmbeddingConclusion
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [NumberField K]
    [Field L] [NumberField L] [Algebra K L] [Field M] [NumberField M]
    [Algebra K M] : Prop :=
  Nonempty (M →ₐ[K] L)

/--
Standalone maximality predicate for a candidate Hilbert class field `L/K`.

This isolates the maximality branch from the larger `HilbertClassFieldCore`
record: every finite everywhere-unramified abelian extension `M/K` admits a
`K`-algebra embedding into `L`.
-/
def IsMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] : Prop :=
  ∀ (M : Type uM) [Field M] [NumberField M] [Algebra K M] [Module.Finite K M],
    IsFiniteEverywhereUnramifiedAbelianExtension K M →
      HilbertClassFieldMaximalityEmbeddingConclusion K L M

/--
Checked extraction of the standalone maximality predicate from a
`HilbertClassFieldCore` witness.

This is not an independent proof of the Hilbert-class-field maximality theorem:
it repackages the `maximal` field already required by the core statement.
-/
theorem hilbertClassFieldCore_isMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions
    (K : Type uK) (L : Type uL) [Field K] [NumberField K] [Field L]
    [NumberField L] [Algebra K L] [Module.Finite K L]
    (h : HilbertClassFieldCore.{uK, uL, uM} K L) :
    IsMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions.{uK, uL, uM} K L := by
  intro M _ _ _ _ hM
  exact h.maximal M hM.1 hM.2

/--
Embedding theorem form requested by child `S1-M-075-C007`.

Given a checked `HilbertClassFieldCore` witness for `L/K` and a finite
everywhere-unramified abelian extension `M/K`, produce the Stage1 maximality
conclusion `Nonempty (M →ₐ[K] L)`.
-/
theorem hilbertClassFieldCore_unramifiedAbelianExtension_embeds
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [NumberField K]
    [Field L] [NumberField L] [Algebra K L] [Module.Finite K L]
    [Field M] [NumberField M] [Algebra K M] [Module.Finite K M]
    (hL : HilbertClassFieldCore.{uK, uL, uM} K L)
    (hM : IsFiniteEverywhereUnramifiedAbelianExtension K M) :
    Nonempty (M →ₐ[K] L) :=
  hL.maximal M hM.1 hM.2

/--
Child `S1-M-075-C007` has a checked maximality embedding interface, but no
independent proof that any candidate `L` satisfies maximality.
-/
def hasRepoLocalIndependentHilbertClassFieldMaximalityProof : Bool := false

/-- Checked gate for the C007 non-completion boundary. -/
theorem hasRepoLocalIndependentHilbertClassFieldMaximalityProof_eq_false :
    hasRepoLocalIndependentHilbertClassFieldMaximalityProof = false := rfl

/--
Public child-task text for later serial blueprint/todo backfill of
`S1-M-075-C007`.
-/
def maximalityEmbeddingPublicTask : String :=
  "Backfill S1-M-075-C007 as completed only for the checked maximality embedding interface: add IsFiniteEverywhereUnramifiedAbelianExtension, HilbertClassFieldMaximalityEmbeddingConclusion, IsMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions, and the extraction theorems hilbertClassFieldCore_isMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions and hilbertClassFieldCore_unramifiedAbelianExtension_embeds, whose conclusion is Nonempty (M ->a[K] L). Keep the independent maximality proof and THM-M-0420 open: the checked theorem repackages the maximal field required by HilbertClassFieldCore and does not construct the embedding from class field theory or Artin reciprocity."

/-! ## Uniqueness interface for child `S1-M-075-C008` -/

/--
Uniqueness target for Hilbert class fields: two candidate Hilbert class fields
over the same base `K` should be equivalent as `K`-algebras.

This is the exact final conclusion requested by child `S1-M-075-C008`; the
checked file below proves only the reductions to and from the maximality
interface, not the finite-extension Cantor-Bernstein bridge itself.
-/
abbrev HilbertClassFieldUniquenessConclusion
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [Field L]
    [Algebra K L] [Field M] [Algebra K M] : Prop :=
  Nonempty (L ≃ₐ[K] M)

/--
The mutual embedding package produced by maximality for two candidate Hilbert
class fields.

For two finite everywhere-unramified abelian maximal extensions `L/K` and
`M/K`, maximality gives a `K`-algebra embedding in each direction.  Turning
these two embeddings into a `K`-algebra equivalence is kept as a separate proof
leaf because it needs the finite-extension dimension/cardinality argument.
-/
structure MutualKAlgebraEmbeddings
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [Field L]
    [Algebra K L] [Field M] [Algebra K M] : Prop where
  embedsLeftToRight : Nonempty (L →ₐ[K] M)
  embedsRightToLeft : Nonempty (M →ₐ[K] L)

/--
The remaining algebraic bridge needed after maximality has supplied embeddings
both ways.

This is intentionally an explicit proposition instead of an axiom: future work
must replace this bridge by a checked proof, likely via finite-dimensional
linear algebra for finite extensions of the same base field.
-/
def MutualKAlgebraEmbeddingsImplyEquivalence
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [Field L]
    [Algebra K L] [Field M] [Algebra K M] : Prop :=
  MutualKAlgebraEmbeddings K L M → HilbertClassFieldUniquenessConclusion K L M

/--
Checked extraction of the mutual-embedding package from two
`HilbertClassFieldCore` witnesses.

This is the part of uniqueness that follows directly from the maximality field
already present in the statement shape.
-/
theorem hilbertClassFieldCore_mutualKAlgebraEmbeddings
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [NumberField K]
    [Field L] [NumberField L] [Algebra K L] [Module.Finite K L]
    [Field M] [NumberField M] [Algebra K M] [Module.Finite K M]
    (hL : HilbertClassFieldCore.{uK, uL, uM} K L)
    (hM : HilbertClassFieldCore.{uK, uM, uL} K M) :
    MutualKAlgebraEmbeddings K L M := by
  exact
    { embedsLeftToRight :=
        hM.maximal L hL.isAbelianGalois hL.unramifiedAtFinitePrimes
      embedsRightToLeft :=
        hL.maximal M hM.isAbelianGalois hM.unramifiedAtFinitePrimes }

/--
Checked wrapper for the final uniqueness theorem once the finite-extension
mutual-embedding bridge is available.

The hypothesis `hBridge` is the only unproved mathematical/formalization leaf
left by this child task.  Without that bridge, this theorem does not claim
Hilbert class field uniqueness.
-/
theorem hilbertClassFieldCore_uniqueUpToKAlgEquiv_of_mutualEmbeddingBridge
    (K : Type uK) (L : Type uL) (M : Type uM) [Field K] [NumberField K]
    [Field L] [NumberField L] [Algebra K L] [Module.Finite K L]
    [Field M] [NumberField M] [Algebra K M] [Module.Finite K M]
    (hBridge : MutualKAlgebraEmbeddingsImplyEquivalence K L M)
    (hL : HilbertClassFieldCore.{uK, uL, uM} K L)
    (hM : HilbertClassFieldCore.{uK, uM, uL} K M) :
    HilbertClassFieldUniquenessConclusion K L M :=
  hBridge (hilbertClassFieldCore_mutualKAlgebraEmbeddings K L M hL hM)

/--
One M0387-style leaf in the future proof of Hilbert-class-field uniqueness.
-/
structure HilbertClassFieldUniquenessLeaf where
  nodeId : String
  parentNode : String
  leafName : String
  proofTarget : String
  status : String
  debtClass : String
  maxStepBudget : Nat
  repoLocalClosed : Bool
  deriving Repr

/--
The C008 uniqueness proof split.

The first leaf is checked by
`hilbertClassFieldCore_mutualKAlgebraEmbeddings`.  The second leaf remains
unchecked and must be discharged before uniqueness can be claimed.
-/
def hilbertClassFieldUniquenessLeaves : List HilbertClassFieldUniquenessLeaf := [
  {
    nodeId := "HCF.L020.MUTUAL_EMBEDDINGS",
    parentNode := "HCF.L020.unchecked.uniqueness_up_to_K_alg_equiv",
    leafName := "maximality gives mutual embeddings",
    proofTarget := "From HilbertClassFieldCore witnesses for L/K and M/K, use maximality twice to obtain Nonempty (L ->a[K] M) and Nonempty (M ->a[K] L).",
    status := "checked",
    debtClass := "local_proof_body",
    maxStepBudget := 100,
    repoLocalClosed := true
  },
  {
    nodeId := "HCF.L020.EMBEDDING_BRIDGE",
    parentNode := "HCF.L020.unchecked.uniqueness_up_to_K_alg_equiv",
    leafName := "mutual finite K-algebra embeddings imply equivalence",
    proofTarget := "For finite field extensions L/K and M/K, prove MutualKAlgebraEmbeddings K L M -> Nonempty (L ~=_[K] M), probably by finite-dimensional linear algebra plus AlgEquiv.ofBijective.",
    status := "unchecked",
    debtClass := "formalization_debt",
    maxStepBudget := 100,
    repoLocalClosed := false
  }
]

/-- Repo-local check: C008 uniqueness split has the two intended leaves. -/
theorem hilbertClassFieldUniquenessLeaves_nodeIds :
    hilbertClassFieldUniquenessLeaves.map (fun row => row.nodeId) =
      ["HCF.L020.MUTUAL_EMBEDDINGS", "HCF.L020.EMBEDDING_BRIDGE"] := rfl

/-- Repo-local check: C008 records exactly one checked reduction and one unchecked bridge. -/
theorem hilbertClassFieldUniquenessLeaves_statuses :
    hilbertClassFieldUniquenessLeaves.map (fun row => row.status) =
      ["checked", "unchecked"] := rfl

/-- Repo-local check: each C008 leaf has a local proof budget of at most 100 steps. -/
theorem hilbertClassFieldUniquenessLeaves_budgets :
    hilbertClassFieldUniquenessLeaves.map (fun row => row.maxStepBudget) =
      [100, 100] := rfl

/--
Repo-local gate check: child C008 does not yet contain a complete uniqueness
proof, because the finite-extension embedding bridge is still unchecked.
-/
theorem hilbertClassFieldUniquenessLeaves_repoLocalClosed :
    hilbertClassFieldUniquenessLeaves.map (fun row => row.repoLocalClosed) =
      [true, false] := rfl

/-- Child `S1-M-075-C008` has a checked reduction, not a full uniqueness proof. -/
def hasRepoLocalHilbertClassFieldUniquenessProof : Bool := false

/-- Checked gate for the C008 non-completion boundary. -/
theorem hasRepoLocalHilbertClassFieldUniquenessProof_eq_false :
    hasRepoLocalHilbertClassFieldUniquenessProof = false := rfl

/--
Public child-task text for later serial blueprint/todo backfill of
`S1-M-075-C008`.
-/
def uniquenessUpToKAlgEquivPublicTask : String :=
  "Backfill S1-M-075-C008 as partially advanced, not completed: add HilbertClassFieldUniquenessConclusion K L M := Nonempty (L ~=_[K] M), MutualKAlgebraEmbeddings, MutualKAlgebraEmbeddingsImplyEquivalence, the checked reduction hilbertClassFieldCore_mutualKAlgebraEmbeddings using maximality twice, and the checked wrapper hilbertClassFieldCore_uniqueUpToKAlgEquiv_of_mutualEmbeddingBridge. Keep HCF.L020.EMBEDDING_BRIDGE open with formalization_debt: finite K-algebra embeddings both ways between finite extensions must still be turned into a K-algebra equivalence before uniqueness of Hilbert class fields can be claimed."

/-! ## Audit probes for checked local names -/

#check StatementShape
#check StatementOrientationDecision
#check canonicalStatementOrientation
#check canonicalStatementOrientation_eq_explicitCandidate
#check HilbertClassFieldExists
#check statementShape_implies_hilbertClassFieldExists
#check usesConstructedHilbertClassFieldObject
#check usesConstructedHilbertClassFieldObject_eq_false
#check statementOrientationPublicTask
#check ExternalPrimarySourceAuditRow
#check externalPrimarySourceAuditRows
#check externalPrimarySourceAuditHasRepoLocalHilbertClassFieldCompletion
#check externalPrimarySourceAuditPublicTask
#check ExternalLakeDependencyCompatibilityRow
#check externalLakeDependencyCompatibilityRows
#check externalLakeDependencyCompatibilityHasImportableCandidate
#check externalLakeDependencyCompatibilityHasImportableCandidate_eq_false
#check externalLakeDependencyCompatibilityPublicTask
#check IsUnramifiedOverBasePrime
#check HasRamificationIdxOneOverBasePrime
#check isUnramifiedOverBasePrime_iff_ramificationIdx_eq_one
#check AllPrimesOverHaveRamificationIdxOne
#check everywhereUnramifiedAtFinitePrimes_iff_all_primesOver_ramificationIdx_eq_one
#check finitePrimeUnramifiedBranchUsesPrimesOver
#check finitePrimeUnramifiedBranchUsesPrimesOver_eq_true
#check finitePrimeUnramifiedBranchPublicTask
#check ArtinReciprocityMapShape
#check artinReciprocityMapFromClassGroupEquiv
#check hilbertClassFieldCore_nonempty_artinReciprocityMapShape
#check hasRepoLocalGlobalArtinReciprocityTheorem
#check hasRepoLocalGlobalArtinReciprocityTheorem_eq_false
#check artinReciprocityMapPublicTask
#check ArtinReciprocityIsomorphismLeaf
#check artinReciprocityIsomorphismLeaves
#check artinReciprocityIsomorphismLeaves_nodeIds
#check artinReciprocityIsomorphismLeaves_statuses
#check artinReciprocityIsomorphismLeaves_budgets
#check artinReciprocityIsomorphismLeaves_repoLocalClosed
#check hasRepoLocalArtinReciprocityIsomorphismProof
#check hasRepoLocalArtinReciprocityIsomorphismProof_eq_false
#check artinReciprocityIsomorphismSplitPublicTask
#check IsFiniteEverywhereUnramifiedAbelianExtension
#check HilbertClassFieldMaximalityEmbeddingConclusion
#check IsMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions
#check hilbertClassFieldCore_isMaximalAmongFiniteEverywhereUnramifiedAbelianExtensions
#check hilbertClassFieldCore_unramifiedAbelianExtension_embeds
#check hasRepoLocalIndependentHilbertClassFieldMaximalityProof
#check hasRepoLocalIndependentHilbertClassFieldMaximalityProof_eq_false
#check maximalityEmbeddingPublicTask
#check HilbertClassFieldUniquenessConclusion
#check MutualKAlgebraEmbeddings
#check MutualKAlgebraEmbeddingsImplyEquivalence
#check hilbertClassFieldCore_mutualKAlgebraEmbeddings
#check hilbertClassFieldCore_uniqueUpToKAlgEquiv_of_mutualEmbeddingBridge
#check HilbertClassFieldUniquenessLeaf
#check hilbertClassFieldUniquenessLeaves
#check hilbertClassFieldUniquenessLeaves_nodeIds
#check hilbertClassFieldUniquenessLeaves_statuses
#check hilbertClassFieldUniquenessLeaves_budgets
#check hilbertClassFieldUniquenessLeaves_repoLocalClosed
#check hasRepoLocalHilbertClassFieldUniquenessProof
#check hasRepoLocalHilbertClassFieldUniquenessProof_eq_false
#check uniquenessUpToKAlgEquivPublicTask

end AwesomeTheorems.Stage1.S1_M_075
