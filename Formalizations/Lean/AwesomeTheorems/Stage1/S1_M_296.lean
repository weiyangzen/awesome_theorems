import Mathlib.NumberTheory.Cyclotomic.Basic
import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic
import Mathlib.NumberTheory.NumberField.InfinitePlace.TotallyRealComplex
import Mathlib.NumberTheory.Padics.PadicIntegers
import Mathlib.NumberTheory.Padics.PadicNumbers
import Mathlib.Algebra.Module.Torsion.Basic
import Mathlib.RingTheory.ClassGroup
import Mathlib.RingTheory.Ideal.IsPrincipal
import Mathlib.RingTheory.Noetherian.Basic

/-!
# S1-M-296 / THM-M-0024: Mazur-Wiles theorem

This Stage1 artifact records a Lean 4 statement-shape boundary for the
Mazur-Wiles proof of the Iwasawa main conjecture.  It is not a proof of the
Mazur-Wiles theorem and it is not a proof of the Iwasawa main conjecture.

The checked local content is limited to adjacent mathlib infrastructure:
cyclotomic fields and rings, integral closures in cyclotomic extensions,
number-field class groups/class numbers, `p`-adic numbers/integers, and generic
mathlib algebra/module/ideal APIs.  The terminal completed Iwasawa algebra,
inverse-limit class-group module, characteristic ideal theorem, and `p`-adic
L-function construction remain explicit boundary data.
-/

noncomputable section

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_296

universe uK uΛ uM

/-- A concrete cyclotomic layer already available in mathlib. -/
abbrev CyclotomicLayer (n : ℕ) :=
  CyclotomicField n ℚ

/--
Boundary for the base-field hypotheses in a Mazur-Wiles style statement.

The abelian-over-`ℚ` and totally-real hypotheses are concrete mathlib
predicates.  This still remains a boundary object: the final theorem must
choose the exact number-field formulation and connect it to the downstream
Iwasawa algebra, module, and `p`-adic L-function APIs.
-/
structure MazurWilesBaseFieldBoundary : Type (uK + 1) where
  K : Type uK
  [fieldK : Field K]
  [numberFieldK : NumberField K]
  [abelianExtensionOfRat : IsAbelianGalois ℚ K]
  [totallyReal : NumberField.IsTotallyReal K]

attribute [instance] MazurWilesBaseFieldBoundary.fieldK
attribute [instance] MazurWilesBaseFieldBoundary.numberFieldK
attribute [instance] MazurWilesBaseFieldBoundary.abelianExtensionOfRat
attribute [instance] MazurWilesBaseFieldBoundary.totallyReal

/--
Boundary for the completed Iwasawa algebra used in the main conjecture.

The intended object is a completed group algebra over a `p`-adic coefficient
ring.  This boundary now uses concrete mathlib APIs for the coefficient
algebra, noetherian/domain hypotheses, and ring equivalence to a future
completed group algebra model.  Current local mathlib still has not supplied
the actual Mazur-Wiles completed group algebra construction.
-/
structure IwasawaAlgebraBoundary (p : ℕ) [Fact p.Prime] : Type (uΛ + 1) where
  AlgebraObject : Type uΛ
  [commRing : CommRing AlgebraObject]
  [algebraPadicInt : Algebra ℤ_[p] AlgebraObject]
  [isDomain : IsDomain AlgebraObject]
  [isNoetherianRing : IsNoetherianRing AlgebraObject]
  CompletedGroupAlgebraModel : Type uΛ
  [modelCommRing : CommRing CompletedGroupAlgebraModel]
  completedGroupAlgebraEquiv : CompletedGroupAlgebraModel ≃+* AlgebraObject

attribute [instance] IwasawaAlgebraBoundary.commRing
attribute [instance] IwasawaAlgebraBoundary.algebraPadicInt
attribute [instance] IwasawaAlgebraBoundary.isDomain
attribute [instance] IwasawaAlgebraBoundary.isNoetherianRing
attribute [instance] IwasawaAlgebraBoundary.modelCommRing

/--
Boundary for the Iwasawa module built from inverse limits of class groups.

The module and characteristic ideal now use concrete mathlib APIs.  The
inverse-limit identification is still boundary data because neither mathlib nor
a pinned repo-local dependency currently supplies the class-group tower package
needed by the Mazur-Wiles terminal theorem.
-/
structure ClassGroupIwasawaModuleBoundary (p : ℕ) [Fact p.Prime]
    (Λ : IwasawaAlgebraBoundary.{uΛ} p) : Type (max uM uΛ + 1) where
  ModuleObject : Type uM
  [addCommGroup : AddCommGroup ModuleObject]
  [module : Module Λ.AlgebraObject ModuleObject]
  [finite : Module.Finite Λ.AlgebraObject ModuleObject]
  [torsion : Module.IsTorsion Λ.AlgebraObject ModuleObject]
  FiniteLayerClassGroup : ℕ → Type uM
  [finiteLayerAddCommGroup : ∀ n, AddCommGroup (FiniteLayerClassGroup n)]
  transitionMap : (n : ℕ) → FiniteLayerClassGroup (n + 1) →+ FiniteLayerClassGroup n
  projectionToLayer : (n : ℕ) → ModuleObject →+ FiniteLayerClassGroup n
  inverseLimitCompatibility : Prop
  inverseLimitUniversalProperty : Prop
  characteristicIdeal : Ideal Λ.AlgebraObject
  characteristicIdeal_isPrincipal : Submodule.IsPrincipal characteristicIdeal
  characteristicIdealCorrect : Prop

attribute [instance] ClassGroupIwasawaModuleBoundary.addCommGroup
attribute [instance] ClassGroupIwasawaModuleBoundary.module
attribute [instance] ClassGroupIwasawaModuleBoundary.finite
attribute [instance] ClassGroupIwasawaModuleBoundary.torsion
attribute [instance] ClassGroupIwasawaModuleBoundary.finiteLayerAddCommGroup

/--
Boundary for the `p`-adic L-function side of the Mazur-Wiles theorem.

The function is now over an explicit character-space type and returns values in
`ℚ_[p]`.  The final formalization should replace the generic character space
by the correct measure/distribution or locally analytic character-space object
and prove the interpolation formula, rather than keeping it as proposition data.
-/
structure PadicLFunctionBoundary (p : ℕ) [Fact p.Prime] : Type (uM + 1) where
  CharacterSpace : Type uM
  [topologicalSpaceCharacterSpace : TopologicalSpace CharacterSpace]
  pAdicLFunction : CharacterSpace → ℚ_[p]
  interpolationFormula : Prop
  characterCompatibility : Prop

attribute [instance] PadicLFunctionBoundary.topologicalSpaceCharacterSpace

/--
Boundary package for a Mazur-Wiles Iwasawa-main-conjecture statement.

`pAdicLFunctionGeneratesCharacteristicIdeal` is the target equality/divisibility
statement: the ideal generated by the relevant `p`-adic L-function equals the
characteristic ideal of the class-group Iwasawa module, after the integrator
chooses a concrete formulation.
-/
structure MazurWilesMainConjectureBoundary (p : ℕ) [Fact p.Prime] :
    Type (max (max uK uΛ) uM + 1) where
  baseField : MazurWilesBaseFieldBoundary.{uK}
  oddPrime : p ≠ 2
  Λ : IwasawaAlgebraBoundary.{uΛ} p
  classGroupModule : ClassGroupIwasawaModuleBoundary.{uΛ, uM} p Λ
  pAdicLFunction : PadicLFunctionBoundary.{uM} p
  pAdicLFunctionGeneratesCharacteristicIdeal : Prop

namespace MazurWilesMainConjectureBoundary

variable {p : ℕ} [Fact p.Prime]

/-- Local proposition boundary for the expected Mazur-Wiles conclusion. -/
def expectedMainConjecture
    (D : MazurWilesMainConjectureBoundary.{uK, uΛ, uM} p) : Prop :=
  IsAbelianGalois ℚ D.baseField.K →
    NumberField.IsTotallyReal D.baseField.K →
      D.classGroupModule.inverseLimitCompatibility →
        D.classGroupModule.inverseLimitUniversalProperty →
          D.classGroupModule.characteristicIdealCorrect →
            D.pAdicLFunction.interpolationFormula →
              D.pAdicLFunction.characterCompatibility →
                D.pAdicLFunctionGeneratesCharacteristicIdeal

end MazurWilesMainConjectureBoundary

namespace MazurWilesBaseFieldBoundary

variable (B : MazurWilesBaseFieldBoundary.{uK})

/--
Checked local wrapper for the concrete abelian-over-`ℚ` mathlib predicate used
by the Mazur-Wiles base-field boundary.
-/
theorem abelianOverRat_mathlib_predicate : IsAbelianGalois ℚ B.K :=
  inferInstance

/--
Checked local wrapper for the concrete totally-real mathlib predicate used by
the Mazur-Wiles base-field boundary.
-/
theorem totallyReal_mathlib_predicate : NumberField.IsTotallyReal B.K :=
  inferInstance

/--
The C007 base-field boundary no longer stores placeholder `Prop` fields for
the abelian-over-`ℚ` and totally-real hypotheses.
-/
theorem concreteBaseFieldPredicates :
    IsAbelianGalois ℚ B.K ∧ NumberField.IsTotallyReal B.K :=
  ⟨B.abelianOverRat_mathlib_predicate, B.totallyReal_mathlib_predicate⟩

end MazurWilesBaseFieldBoundary

namespace IwasawaAlgebraBoundary

variable {p : ℕ} [Fact p.Prime] (Λ : IwasawaAlgebraBoundary.{uΛ} p)

/-- Checked local wrapper for the concrete `ℤ_[p]`-algebra API on the boundary algebra. -/
@[reducible]
def padicIntAlgebra_mathlib_api : Algebra ℤ_[p] Λ.AlgebraObject :=
  inferInstance

/-- Checked local wrapper for the concrete domain predicate on the boundary algebra. -/
theorem domain_mathlib_predicate : IsDomain Λ.AlgebraObject :=
  inferInstance

/-- Checked local wrapper for the concrete noetherian-ring predicate on the boundary algebra. -/
theorem noetherianRing_mathlib_predicate : IsNoetherianRing Λ.AlgebraObject :=
  inferInstance

/-- The characteristic-ideal carrier is now the concrete mathlib ideal type. -/
def characteristicIdealType : Type uΛ :=
  Ideal Λ.AlgebraObject

end IwasawaAlgebraBoundary

namespace ClassGroupIwasawaModuleBoundary

variable {p : ℕ} [Fact p.Prime] {Λ : IwasawaAlgebraBoundary.{uΛ} p}
variable (M : ClassGroupIwasawaModuleBoundary.{uΛ, uM} p Λ)

/-- Checked local wrapper for the concrete finite-module API on the Iwasawa module boundary. -/
theorem finiteModule_mathlib_predicate :
    Module.Finite Λ.AlgebraObject M.ModuleObject :=
  inferInstance

/-- Checked local wrapper for the concrete torsion-module API on the Iwasawa module boundary. -/
theorem torsionModule_mathlib_predicate :
    Module.IsTorsion Λ.AlgebraObject M.ModuleObject :=
  M.torsion

/-- Checked local wrapper: the characteristic ideal is a concrete mathlib ideal. -/
def characteristicIdeal_mathlib_api : Ideal Λ.AlgebraObject :=
  M.characteristicIdeal

/-- Checked local wrapper for the principal-ideal API attached to the characteristic ideal. -/
theorem characteristicIdeal_principal_mathlib_predicate :
    Submodule.IsPrincipal M.characteristicIdeal :=
  M.characteristicIdeal_isPrincipal

end ClassGroupIwasawaModuleBoundary

namespace PadicLFunctionBoundary

variable {p : ℕ} [Fact p.Prime] (L : PadicLFunctionBoundary.{uM} p)

/-- Checked local wrapper: the `p`-adic L-function evaluates on its character space. -/
def evaluatesOnCharacterSpace : L.CharacterSpace → ℚ_[p] :=
  L.pAdicLFunction

/-- Checked local wrapper for the topological character-space API. -/
@[reducible]
def characterSpace_topologicalSpace : TopologicalSpace L.CharacterSpace :=
  inferInstance

end PadicLFunctionBoundary

/--
Stage1 normalized statement shape for the source claim: Mazur-Wiles proves the
Iwasawa main conjecture for the selected cyclotomic/abelian number-field
setting.

This is a formalization boundary only.  It is not proved in this file.
-/
def StatementShape : Prop :=
  ∀ (p : ℕ) [Fact p.Prime],
    ∀ D : MazurWilesMainConjectureBoundary.{uK, uΛ, uM} p,
      D.expectedMainConjecture

/-- The statement-shape definition unfolds to the local boundary proposition. -/
theorem statementShape_iff :
    StatementShape.{uK, uΛ, uM} ↔
      ∀ (p : ℕ) [Fact p.Prime],
        ∀ D : MazurWilesMainConjectureBoundary.{uK, uΛ, uM} p,
          D.expectedMainConjecture :=
  Iff.rfl

/-- Checked mathlib wrapper: nonzero cyclotomic fields are cyclotomic extensions. -/
theorem cyclotomicLayer_isCyclotomicExtension_mathlib_wrapper
    (n : ℕ) [NeZero n] :
    letI : Algebra ℚ (CyclotomicLayer n) := CyclotomicField.algebraBase n ℚ ℚ
    IsCyclotomicExtension {n} ℚ (CyclotomicLayer n) := by
  letI : Algebra ℚ (CyclotomicLayer n) := CyclotomicField.algebraBase n ℚ ℚ
  exact CyclotomicField.isCyclotomicExtension n ℚ

/-- Checked mathlib wrapper: cyclotomic fields over `ℚ` are number fields. -/
theorem cyclotomicLayer_numberField_mathlib_wrapper (n : ℕ) :
    NumberField (CyclotomicLayer n) :=
  CyclotomicField.instNumberField n ℚ

/-- Checked mathlib wrapper: the cyclotomic ring is the integral closure in the cyclotomic field. -/
theorem cyclotomicRing_isIntegralClosure_mathlib_wrapper (n : ℕ) [NeZero n] :
    IsIntegralClosure (CyclotomicRing n ℤ ℚ) ℤ (CyclotomicLayer n) :=
  IsCyclotomicExtension.Rat.cyclotomicRing_isIntegralClosure n

/-- Checked mathlib wrapper: class groups of rings of integers are finite objects. -/
theorem classGroup_fintype_mathlib_wrapper
    (K : Type uK) [Field K] [NumberField K] :
    Nonempty (Fintype (ClassGroup (NumberField.RingOfIntegers K))) :=
  ⟨NumberField.RingOfIntegers.instFintypeClassGroup K⟩

/-- Checked mathlib wrapper: number-field class numbers are positive. -/
theorem classNumber_pos_mathlib_wrapper
    (K : Type uK) [Field K] [NumberField K] :
    0 < NumberField.classNumber K :=
  NumberField.classNumber_pos K

/-- Checked mathlib wrapper: the `p`-adic norm of `p` in `ℚ_[p]`. -/
theorem padic_norm_p_mathlib_wrapper (p : ℕ) [Fact p.Prime] :
    ‖(p : ℚ_[p])‖ = (p : ℝ)⁻¹ :=
  Padic.norm_p

/-- Checked mathlib wrapper: the ultrametric inequality on `ℚ_[p]`. -/
theorem padic_nonarchimedean_mathlib_wrapper
    (p : ℕ) [Fact p.Prime] (x y : ℚ_[p]) :
    ‖x + y‖ ≤ max ‖x‖ ‖y‖ :=
  Padic.nonarchimedean x y

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.Cyclotomic.Basic",
  "Mathlib.NumberTheory.NumberField.Cyclotomic.Basic",
  "Mathlib.NumberTheory.NumberField.ClassNumber",
  "Mathlib.NumberTheory.Padics.PadicNumbers",
  "Mathlib.NumberTheory.Padics.PadicIntegers",
  "Mathlib.Algebra.Module.Torsion.Basic",
  "Mathlib.RingTheory.ClassGroup",
  "Mathlib.RingTheory.Ideal.IsPrincipal",
  "Mathlib.RingTheory.Noetherian.Basic",
  "Mathlib.NumberTheory.LSeries.DirichletContinuation",
  "Mathlib.NumberTheory.EulerProduct.DirichletLSeries",
  "Mathlib.GroupTheory.GroupAction.Iwasawa"
]

/-- Search terms that did not locate a terminal Mazur-Wiles/Iwasawa theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "MazurWiles",
  "Mazur-Wiles",
  "Mazur Wiles",
  "IwasawaMainConjecture",
  "Iwasawa main conjecture",
  "pAdicLFunction",
  "PadicLFunction",
  "IwasawaAlgebra",
  "IwasawaModule",
  "characteristic ideal class group"
]

/--
Typed payload for the C005 external Lean 4 primary-source audit.

The entries are evidence records only.  They do not import or validate any
external theorem inside this repository, and therefore cannot close the
Mazur-Wiles/Iwasawa-main-conjecture terminal proof.
-/
structure ExternalLeanPrimarySourceAudit where
  sourceName : String
  sourceKind : String
  urlOrPath : String
  revisionOrSnapshot : String
  searchMethod : String
  exactRequiredIdentifierHits : List String
  adjacentLeanAnchors : List String
  blockerOrConclusion : String

/-- Exact external-search identifiers required by the C005 child task. -/
def externalLeanPrimarySourceSearchTerms : List String := [
  "MazurWiles",
  "IwasawaMainConjecture",
  "IwasawaAlgebra",
  "IwasawaModule",
  "pAdicLFunction"
]

/--
Repo-local, integration-ready summary of the C005 primary-source search.

`exactRequiredIdentifierHits` is empty in every entry because the required exact
identifier search found no external Lean 4 terminal proof.  The `lean-iwasawa`
entry is still useful future integration evidence because it contains adjacent
Iwasawa infrastructure, but it is blocked by placeholder proofs, toolchain
mismatch, and lack of repo-local pin/import/check.
-/
def externalLeanPrimarySourceAudits : List ExternalLeanPrimarySourceAudit := [
  {
    sourceName := "repo-local pinned Lean dependencies",
    sourceKind := "local primary-source search",
    urlOrPath :=
      "Formalizations/Lean/.lake/packages and Formalizations/Lean/.vendor/mathlib4",
    revisionOrSnapshot :=
      "mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; " ++
      "flt-regular 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27; " ++
      "vendor mathlib4 dc7664a302ed42b3acb861ceeacdb5e866358313",
    searchMethod :=
      "rg -n \"MazurWiles|IwasawaMainConjecture|IwasawaAlgebra|" ++
      "IwasawaModule|pAdicLFunction\" over local package sources",
    exactRequiredIdentifierHits := [],
    adjacentLeanAnchors := [
      "Mathlib.NumberTheory.Cyclotomic.Basic",
      "Mathlib.NumberTheory.NumberField.Cyclotomic.Basic",
      "Mathlib.NumberTheory.NumberField.ClassNumber",
      "Mathlib.NumberTheory.Padics.PadicNumbers",
      "Mathlib.RingTheory.ClassGroup"
    ],
    blockerOrConclusion :=
      "No exact required identifiers and no terminal Mazur-Wiles/Iwasawa-main-" ++
      "conjecture theorem were found in repo-local pinned dependencies."
  },
  {
    sourceName := "acmepjz/lean-iwasawa",
    sourceKind := "locally downloaded primary-source archive",
    urlOrPath := "https://github.com/acmepjz/lean-iwasawa",
    revisionOrSnapshot :=
      "master archive downloaded through codeload on 2026-05-01; " ++
      "git ls-remote/clone did not complete in this environment, so the exact " ++
      "commit still must be pinned by an integrator before any dependency use",
    searchMethod :=
      "rg -n over /tmp/s1m296-lean-iwasawa-zip/lean-iwasawa-master",
    exactRequiredIdentifierHits := [],
    adjacentLeanAnchors := [
      "Iwasawalib.Algebra.CompleteGroupAlgebra.Basic: CompleteGroupAlgebra",
      "Iwasawalib.RingTheory.CharacteristicIdeal.Basic: Module.charIdeal",
      "Iwasawalib.FieldTheory.ZpExtension.Cyclotomic: IsCyclotomicPinfExtension",
      "Iwasawalib.NumberTheory.ZpExtension.ClassGroup: " ++
      "MvZpExtension.multiplicity_classNumber_Kn_eq₁"
    ],
    blockerOrConclusion :=
      "Adjacent Iwasawa infrastructure exists, but no exact required " ++
      "Mazur-Wiles/main-conjecture identifiers were found.  The archive " ++
      "contains unresolved placeholder proofs, uses leanprover/lean4:" ++
      "v4.30.0-rc1 while this repository uses v4.29.0, and has not been " ++
      "pinned/imported/checked here.  It is not terminal proof evidence."
  },
  {
    sourceName := "google-deepmind/formal-conjectures",
    sourceKind := "locally downloaded primary-source archive",
    urlOrPath := "https://github.com/google-deepmind/formal-conjectures",
    revisionOrSnapshot :=
      "main archive downloaded through codeload on 2026-05-01",
    searchMethod :=
      "rg -n over /tmp/formal-conjectures-zip/formal-conjectures-main",
    exactRequiredIdentifierHits := [],
    adjacentLeanAnchors := [],
    blockerOrConclusion :=
      "No exact required identifiers or adjacent Mazur-Wiles/Iwasawa anchors " ++
      "were found.  The repository README describes formalized statements of " ++
      "conjectures, not a terminal long-proof source for this theorem."
  }
]

/--
Typed payload for the C006 dependency-integration gate.

This gate is intentionally separate from the C005 source audit.  A future
positive terminal proof hit must not be treated as completion evidence until
the exact URL/revision is pinned and the imported theorem or wrapper checks
inside this repository.
-/
structure ExternalTerminalProofIntegrationGate where
  gateName : String
  triggerCondition : String
  observedExternalTerminalProof : Bool
  currentStatus : String
  requiredRepoLocalAction : String
  remainingIntegrationLeaves : List String

/--
Repo-local checked payload for the C006 integration guard.

The current audit state contains adjacent external Iwasawa infrastructure but
no external Lean 4 terminal proof of Mazur-Wiles or the Iwasawa main
conjecture.  Therefore there is no URL/revision/theorem to pin for completion
in this child pass.
-/
def externalTerminalProofIntegrationGate :
    ExternalTerminalProofIntegrationGate := {
  gateName := "S1-M-296-C006.external-terminal-proof-integration"
  triggerCondition :=
    "If an external Lean 4 terminal proof of Mazur-Wiles or the Iwasawa " ++
    "main conjecture is found, open a dependency-integration task before " ++
    "any completion checkbox changes."
  observedExternalTerminalProof := false
  currentStatus :=
    "No external Lean 4 terminal proof was found by the checked C005 audit; " ++
    "acmepjz/lean-iwasawa is adjacent infrastructure only in this pass."
  requiredRepoLocalAction :=
    "For any future positive terminal proof hit, pin the exact URL and " ++
    "revision, identify module and theorem names, import or vendor the " ++
    "dependency, and run a repo-local Lean check before completion."
  remainingIntegrationLeaves := [
    "[ ] If a future terminal proof is found, pin exact URL, commit, module, and theorem.",
    "[ ] Resolve toolchain, license, dependency, and proof-body blockers before import.",
    "[ ] Run cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_296.lean or a stronger repo-local check after integration."
  ]
}

/--
Typed payload for the public P1-P7 theorem-tree backfill.

Every package below is a planning node for the Mazur-Wiles/Iwasawa-main-
conjecture formalization boundary.  The terminal status is intentionally
`unchecked`: these are not repo-local proof leaves and must not be promoted
until a local proof body, pinned mathlib wrapper, or pinned external dependency
checks in this repository.
-/
structure PublicTheoremTreePackage where
  id : String
  packageName : String
  role : String
  terminalStatus : String
  uncheckedLeaves : List String

/-- Public theorem-tree package expansion for serial blueprint backfill. -/
def publicTheoremTreePackages : List PublicTheoremTreePackage := [
  {
    id := "P1",
    packageName := "Statement and base-field hypotheses",
    role :=
      "Normalize the Mazur-Wiles target into a Lean statement over the chosen " ++
      "abelian/totally-real number-field boundary.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[checked-local] abelianExtensionOfRat uses mathlib IsAbelianGalois ℚ K.",
      "[checked-local] totallyReal uses mathlib NumberField.IsTotallyReal K.",
      "[unchecked] Prove the final statement matches the selected mathematical source."
    ]
  },
  {
    id := "P2",
    packageName := "Cyclotomic and abelian Iwasawa tower",
    role :=
      "Connect the existing cyclotomic mathlib wrappers to the abelian " ++
      "Iwasawa tower used by the main conjecture.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[unchecked] Define the cyclotomic Z_p-extension or pinned equivalent.",
      "[unchecked] Prove compatibility of finite layers and transition maps.",
      "[unchecked] Relate the tower to the base-field boundary from P1."
    ]
  },
  {
    id := "P3",
    packageName := "Completed Iwasawa algebra and ideal theory",
    role :=
      "Replace IwasawaAlgebraBoundary by a concrete completed group algebra " ++
      "with the Noetherian and characteristic-ideal API needed downstream.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[checked-local] The boundary algebra uses mathlib CommRing, Algebra ℤ_[p], IsDomain, and IsNoetherianRing APIs.",
      "[checked-local] Characteristic ideals are represented by mathlib Ideal Λ.AlgebraObject.",
      "[unchecked] Construct or import the completed Iwasawa algebra.",
      "[unchecked] Replace the generic completedGroupAlgebraEquiv field by the selected completed group algebra construction."
    ]
  },
  {
    id := "P4",
    packageName := "Class-group inverse-limit Iwasawa module",
    role :=
      "Replace ClassGroupIwasawaModuleBoundary by the inverse limit of class " ++
      "groups with its torsion module and characteristic ideal data.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[checked-local] The module boundary uses mathlib Module, Module.Finite, Module.IsTorsion, Ideal, and Submodule.IsPrincipal APIs.",
      "[checked-local] The finite layer API exposes class-group-like layer types, transition maps, and projections.",
      "[unchecked] Replace the generic layer types with actual class groups of tower layers.",
      "[unchecked] Prove torsion and characteristicIdealCorrect for the module."
    ]
  },
  {
    id := "P5",
    packageName := "p-adic L-function package",
    role :=
      "Replace PadicLFunctionBoundary by the concrete measure, distribution, " ++
      "or character-space construction of the relevant p-adic L-function.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[checked-local] The boundary exposes an explicit topological character space and a function to ℚ_[p].",
      "[unchecked] Replace the generic character space with the selected measure/distribution or locally analytic character-space API.",
      "[unchecked] Prove the interpolation formula for the required characters.",
      "[unchecked] Prove character and field-extension compatibility."
    ]
  },
  {
    id := "P6",
    packageName := "Mazur-Wiles divisibility and congruence bridge",
    role :=
      "Formalize the proof bridge that compares the algebraic characteristic " ++
      "ideal from P4 with the analytic p-adic L-function side from P5.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[unchecked] State the algebraic-to-analytic divisibility theorem.",
      "[unchecked] State the analytic-to-algebraic divisibility theorem.",
      "[unchecked] Supply the Eisenstein/congruence/control-theorem bridge or pinned equivalent."
    ]
  },
  {
    id := "P7",
    packageName := "Terminal main-conjecture wrapper",
    role :=
      "Assemble P1-P6 into pAdicLFunctionGeneratesCharacteristicIdeal and " ++
      "then into StatementShape, only after every dependency is repo-local checked.",
    terminalStatus := "unchecked",
    uncheckedLeaves := [
      "[unchecked] Convert the two divisibilities into characteristic-ideal equality.",
      "[unchecked] Prove MazurWilesMainConjectureBoundary.expectedMainConjecture.",
      "[unchecked] Close StatementShape without placeholder proofs or anchor-only evidence."
    ]
  }
]

/--
Public caution for serial blueprint backfill.

This string is a checked repo-local payload for the C003 public-doc integration
leaf.  It deliberately keeps the parent theorem open until a terminal proof body
or pinned/imported external theorem validates inside this repository.
-/
def publicCaution : String :=
  "The repo-local Lean artifact Formalizations/Lean/AwesomeTheorems/Stage1/" ++
    "S1_M_296.lean is a checked statement-shape boundary and adjacent " ++
    "mathlib-anchor file only. It is not a proof of the Mazur-Wiles theorem " ++
    "and not a proof of the Iwasawa main conjecture. Keep Stage1 status open " ++
    "until a terminal local proof body, pinned mathlib wrapper, or pinned " ++
    "external Lean 4 dependency is repo-locally import/check validated."

/-! ## Audit probes -/

#check CyclotomicField
#check CyclotomicRing
#check CyclotomicField.isCyclotomicExtension
#check CyclotomicField.instNumberField
#check IsCyclotomicExtension.Rat.cyclotomicRing_isIntegralClosure
#check NumberField.classNumber
#check NumberField.classNumber_pos
#check ClassGroup
#check Padic.norm_p
#check Padic.nonarchimedean
#check MazurWilesBaseFieldBoundary
#check IwasawaAlgebraBoundary
#check ClassGroupIwasawaModuleBoundary
#check PadicLFunctionBoundary
#check MazurWilesMainConjectureBoundary
#check StatementShape
#check publicCaution
#check PublicTheoremTreePackage
#check publicTheoremTreePackages
#check MazurWilesBaseFieldBoundary.abelianOverRat_mathlib_predicate
#check MazurWilesBaseFieldBoundary.totallyReal_mathlib_predicate
#check MazurWilesBaseFieldBoundary.concreteBaseFieldPredicates
#check IwasawaAlgebraBoundary.padicIntAlgebra_mathlib_api
#check IwasawaAlgebraBoundary.domain_mathlib_predicate
#check IwasawaAlgebraBoundary.noetherianRing_mathlib_predicate
#check IwasawaAlgebraBoundary.characteristicIdealType
#check ClassGroupIwasawaModuleBoundary.finiteModule_mathlib_predicate
#check ClassGroupIwasawaModuleBoundary.torsionModule_mathlib_predicate
#check ClassGroupIwasawaModuleBoundary.characteristicIdeal_mathlib_api
#check ClassGroupIwasawaModuleBoundary.characteristicIdeal_principal_mathlib_predicate
#check PadicLFunctionBoundary.evaluatesOnCharacterSpace
#check PadicLFunctionBoundary.characterSpace_topologicalSpace
#check ExternalLeanPrimarySourceAudit
#check externalLeanPrimarySourceSearchTerms
#check externalLeanPrimarySourceAudits
#check ExternalTerminalProofIntegrationGate
#check externalTerminalProofIntegrationGate

end S1_M_296
end Stage1
end AwesomeTheorems
