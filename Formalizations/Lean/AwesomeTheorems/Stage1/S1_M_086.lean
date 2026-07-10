import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.AlgebraicGeometry.Group.Abelian
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.RingTheory.ClassGroup

/-!
# S1-M-086 / THM-M-0438: Shida periods

This Stage1 file records a conservative Lean boundary for period integrals on
Shida varieties.  The pinned mathlib snapshot has useful substrate for number
fields, schemes, group schemes, class groups, and Bochner integrals.  It does not
currently expose Shida varieties, their automorphic/cohomological period
integrals, or a terminal Shida-period theorem.

The declarations below are therefore statement-shape and object-model anchors
only.  They contain no proof of the target theorem.
-/

noncomputable section

open AlgebraicGeometry CategoryTheory MeasureTheory
open scoped NumberField

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_086

/-- The affine base scheme attached to a field. -/
abbrev FieldBaseScheme (K : Type u) [Field K] : Scheme.{u} :=
  Spec (.of K)

/--
Minimal period-integral package backed by mathlib's Bochner integral.

For the target theorem this is intended to be replaced by a concrete cycle,
differential form, automorphic form, or cohomology-class integral on a Shida
variety.  Here it only freezes the checked analytic substrate.
-/
structure PeriodIntegralPackage (Ω : Type v) [MeasurableSpace Ω] where
  μ : Measure Ω
  integrand : Ω → ℂ
  integrable : Integrable integrand μ

/-- The mathlib-backed Bochner integral attached to a period package. -/
def PeriodIntegral {Ω : Type v} [MeasurableSpace Ω]
    (P : PeriodIntegralPackage Ω) : ℂ :=
  ∫ x, P.integrand x ∂P.μ

/-- The zero period package is available in the imported Bochner-integral API. -/
def zeroPeriodPackage (Ω : Type v) [MeasurableSpace Ω] :
    PeriodIntegralPackage Ω where
  μ := 0
  integrand := fun _ => 0
  integrable := by simp

/-- Smoke-test wrapper: the zero period integral evaluates to zero. -/
theorem periodIntegral_zero (Ω : Type v) [MeasurableSpace Ω] :
    PeriodIntegral (zeroPeriodPackage Ω) = 0 := by
  simp [PeriodIntegral, zeroPeriodPackage]

/--
Input data for a future precise Shida-period statement.

The predicate fields are intentionally explicit placeholders: the pinned mathlib
tree does not define Shida varieties, their canonical models, the relevant
automorphic/cohomological classes, or the expected period relation.
-/
structure ShidaPeriodDatum where
  K : Type u
  field_K : Field K
  numberField_K : NumberField K
  shidaVariety : Scheme.{u}
  structureMap : shidaVariety ⟶ FieldBaseScheme K
  periodDomain : Type v
  measurablePeriodDomain : MeasurableSpace periodDomain
  periodPackage : @PeriodIntegralPackage.{v} periodDomain measurablePeriodDomain
  hasShidaVarietyModel : Prop
  hasCanonicalModel : Prop
  hasAutomorphicInput : Prop
  hasCohomologicalCycle : Prop
  hasPeriodComparison : Prop

attribute [instance] ShidaPeriodDatum.field_K
attribute [instance] ShidaPeriodDatum.numberField_K

namespace ShidaPeriodDatum

instance (D : ShidaPeriodDatum.{u, v}) : MeasurableSpace D.periodDomain :=
  D.measurablePeriodDomain

/-- The actual complex value represented by the current abstract period package. -/
def periodValue (D : ShidaPeriodDatum.{u, v}) : ℂ :=
  PeriodIntegral D.periodPackage

/-- A mathlib-backed class-group object attached to the number field in the datum. -/
def classGroupAvailable (D : ShidaPeriodDatum.{u, v}) : Prop :=
  Nonempty (ClassGroup (𝓞 D.K))

/-- The class group object is nonempty in the local mathlib environment. -/
theorem classGroupAvailable_intro (D : ShidaPeriodDatum.{u, v}) :
    D.classGroupAvailable :=
  show Nonempty (ClassGroup (𝓞 D.K)) from inferInstance

end ShidaPeriodDatum

/--
Geometric properties expected of a future Shida-variety model over its number-field
base.  This is substrate only; it is not the moduli interpretation.
-/
def GeometricShidaModel (D : ShidaPeriodDatum.{u, v}) : Prop :=
  IsProper D.structureMap ∧ Smooth D.structureMap

/--
Statement-shape candidate for THM-M-0438.

It says that if the Shida variety model, canonical model, automorphic input, and
cohomological cycle have all been supplied, then the packaged period value
participates in the expected comparison/period relation.  The comparison itself
is kept as a proposition field until a concrete Shida-period theorem or pinned
Lean dependency is available.
-/
def StatementShape : Prop :=
  ∀ D : ShidaPeriodDatum.{u, v},
    GeometricShidaModel D →
      D.hasShidaVarietyModel →
        D.hasCanonicalModel →
          D.hasAutomorphicInput →
            D.hasCohomologicalCycle →
              D.hasPeriodComparison

/--
Public statement-normalization note for integrators.

`StatementShape` is the checked Stage1 boundary for naming the Shida-period
slot in this repository.  It normalizes the hypotheses and target relation that
must later be supplied by Shida-variety, canonical-model, automorphic,
cohomological, and period-comparison APIs.  It is not a terminal proof of a
Shida-period theorem.
-/
def statementNormalizationNote : String :=
  "StatementShape is a statement-shape boundary for THM-M-0438, not a terminal Shida-period proof."

/-! ## Missing API split for the Shida-period package -/

/--
Expected model data for the Shida variety itself.

The fields are deliberately proof obligations rather than constructed objects:
the current local mathlib closure has schemes, properness, and smoothness, but
not the Shida-variety moduli construction.
-/
structure ShidaVarietyModelData (D : ShidaPeriodDatum.{u, v}) where
  modelScheme : Scheme.{u}
  toBase : modelScheme ⟶ FieldBaseScheme D.K
  identifiesWithDatum : modelScheme = D.shidaVariety
  structureMap_compatible :
    identifiesWithDatum ▸ toBase = D.structureMap
  properModel : IsProper toBase
  smoothModel : Smooth toBase
  moduliInterpretation : Prop

/-- A Shida-variety model supplies the legacy model predicate in the datum. -/
def ShidaVarietyModelData.suppliesLegacyPredicate
    {D : ShidaPeriodDatum.{u, v}} (_M : ShidaVarietyModelData D) : Prop :=
  D.hasShidaVarietyModel

/-- Expected canonical-model, level, and reflex-field data. -/
structure CanonicalModelLevelReflexData (D : ShidaPeriodDatum.{u, v}) where
  canonicalModel : Scheme.{u}
  canonicalMap : canonicalModel ⟶ FieldBaseScheme D.K
  levelCarrier : Type v
  reflexField : Type u
  reflexField_field : Field reflexField
  reflexField_numberField : NumberField reflexField
  descentDatum : Prop
  levelCompatibility : Prop
  reciprocityLaw : Prop
  suppliesCanonicalModel : D.hasCanonicalModel

attribute [instance] CanonicalModelLevelReflexData.reflexField_field
attribute [instance] CanonicalModelLevelReflexData.reflexField_numberField

namespace CanonicalModelLevelReflexData

/-- Class-group substrate is available for the abstract reflex field. -/
def reflexClassGroupAvailable
    {D : ShidaPeriodDatum.{u, v}} (C : CanonicalModelLevelReflexData D) : Prop :=
  Nonempty (ClassGroup (𝓞 C.reflexField))

/-- The reflex-field class group object is nonempty in the local mathlib environment. -/
theorem reflexClassGroupAvailable_intro
    {D : ShidaPeriodDatum.{u, v}} (C : CanonicalModelLevelReflexData D) :
    C.reflexClassGroupAvailable :=
  show Nonempty (ClassGroup (𝓞 C.reflexField)) from inferInstance

end CanonicalModelLevelReflexData

/-- Expected concrete period cycle and measurable domain data. -/
structure PeriodCycleDomainData (D : ShidaPeriodDatum.{u, v}) where
  cycleCarrier : Type v
  domainCarrier : Type v
  domainMeasurable : MeasurableSpace domainCarrier
  cycleMeasure : Measure domainCarrier
  cycleMap : cycleCarrier → domainCarrier
  domainEquivalentToDatum : domainCarrier = D.periodDomain
  cycleAdmissible : Prop
  orientationOrMeasureChoice : Prop

attribute [instance] PeriodCycleDomainData.domainMeasurable

/-- Expected differential, cohomology class, and automorphic integrand data. -/
structure AutomorphicCohomologyIntegrandData
    (D : ShidaPeriodDatum.{u, v}) (P : PeriodCycleDomainData D) where
  differentialCarrier : Type v
  cohomologyClassCarrier : Type v
  automorphicFormCarrier : Type v
  differentialForm : P.domainCarrier → differentialCarrier
  cohomologyClass : cohomologyClassCarrier
  automorphicForm : automorphicFormCarrier
  integrand : P.domainCarrier → ℂ
  integrable : Integrable integrand P.cycleMeasure
  integrandMatchesDatum : Prop
  suppliesAutomorphicInput : D.hasAutomorphicInput
  suppliesCohomologicalCycle : D.hasCohomologicalCycle

/--
The automorphic/cohomological API split can reconstruct a period package on the
new concrete domain.
-/
def AutomorphicCohomologyIntegrandData.toPeriodPackage
    {D : ShidaPeriodDatum.{u, v}} {P : PeriodCycleDomainData D}
    (A : AutomorphicCohomologyIntegrandData D P) :
    PeriodIntegralPackage P.domainCarrier where
  μ := P.cycleMeasure
  integrand := A.integrand
  integrable := A.integrable

/-- Expected arithmetic factors appearing in the comparison formula. -/
structure ArithmeticFactorData (D : ShidaPeriodDatum.{u, v}) where
  algebraicFactor : ℂ
  localEulerFactor : ℂ
  classGroupFactor : ClassGroup (𝓞 D.K) → ℂ
  conductorFactor : ℂ
  galoisCharacterCarrier : Type v
  arithmeticNormalization : Prop
  nonzeroDenominators : Prop

/-- The value of the arithmetic multiplier selected by the abstract package. -/
def ArithmeticFactorData.totalFactor
    {D : ShidaPeriodDatum.{u, v}} (A : ArithmeticFactorData D)
    (c : ClassGroup (𝓞 D.K)) : ℂ :=
  A.algebraicFactor * A.localEulerFactor * A.classGroupFactor c * A.conductorFactor

/-- Expected terminal comparison formula data for the Shida-period theorem. -/
structure ShidaPeriodComparisonFormulaData
    (D : ShidaPeriodDatum.{u, v})
    (M : ShidaVarietyModelData D)
    (C : CanonicalModelLevelReflexData D)
    (P : PeriodCycleDomainData D)
    (A : AutomorphicCohomologyIntegrandData D P)
    (F : ArithmeticFactorData D) where
  normalizedPeriod : ℂ
  comparisonTarget : ℂ
  comparisonRelation : Prop
  periodMatchesIntegral :
    normalizedPeriod = PeriodIntegral (AutomorphicCohomologyIntegrandData.toPeriodPackage A)
  usesModelData : D.hasShidaVarietyModel
  usesCanonicalData : D.hasCanonicalModel
  usesAutomorphicData : D.hasAutomorphicInput
  usesCohomologicalData : D.hasCohomologicalCycle
  usesArithmeticFactors : F.arithmeticNormalization
  provesLegacyComparison : D.hasPeriodComparison

/--
Bundled nonterminal API package for the future Shida-period theorem.

This records the dependency order that the missing API split must eventually
close; it is not a construction of any of the objects.
-/
structure ShidaPeriodMissingApiPackage (D : ShidaPeriodDatum.{u, v}) where
  model : ShidaVarietyModelData D
  canonicalLevelReflex : CanonicalModelLevelReflexData D
  periodCycleDomain : PeriodCycleDomainData D
  automorphicCohomologyIntegrand :
    AutomorphicCohomologyIntegrandData D periodCycleDomain
  arithmeticFactors : ArithmeticFactorData D
  comparisonFormula :
    ShidaPeriodComparisonFormulaData D model canonicalLevelReflex periodCycleDomain
      automorphicCohomologyIntegrand arithmeticFactors

namespace ShidaPeriodMissingApiPackage

/-- The bundled missing-API package supplies all legacy predicates used by `StatementShape`. -/
theorem supplies_statement_shape_inputs
    {D : ShidaPeriodDatum.{u, v}} (P : ShidaPeriodMissingApiPackage D) :
    D.hasShidaVarietyModel ∧ D.hasCanonicalModel ∧ D.hasAutomorphicInput ∧
      D.hasCohomologicalCycle ∧ D.hasPeriodComparison :=
  ⟨P.comparisonFormula.usesModelData, P.comparisonFormula.usesCanonicalData,
    P.comparisonFormula.usesAutomorphicData, P.comparisonFormula.usesCohomologicalData,
    P.comparisonFormula.provesLegacyComparison⟩

end ShidaPeriodMissingApiPackage

/-- M0387-style child leaf row for the Shida-period missing-API split. -/
structure MissingApiLeaf where
  leafId : String
  package : String
  expectedApi : String
  status : String
  debtClass : String
  localBudget : Nat

/-- Integration-ready missing-API leaves for `THM-M-0438.missing-api`. -/
def shidaPeriodMissingApiLeaves : List MissingApiLeaf :=
  [ { leafId := "M0438-API-L01",
      package := "Shida-variety model",
      expectedApi := "Define the Shida variety as a concrete scheme/moduli object over the number-field base and prove the selected structure morphism is the expected one.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100 },
    { leafId := "M0438-API-L02",
      package := "Canonical model, level, and reflex data",
      expectedApi := "Define the canonical model, level structure, reflex field, descent datum, and reciprocity/field-of-definition obligations.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100 },
    { leafId := "M0438-API-L03",
      package := "Concrete period cycle and domain",
      expectedApi := "Define the period cycle, measurable/integration domain, cycle map, orientation or measure choices, and the bridge to the datum's period domain.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100 },
    { leafId := "M0438-API-L04",
      package := "Differential, cohomology, and automorphic integrand",
      expectedApi := "Define the differential form, cohomology class, automorphic form, concrete integrand, integrability proof, and bridge to the datum's period package.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100 },
    { leafId := "M0438-API-L05",
      package := "Arithmetic factors",
      expectedApi := "Define algebraic, local Euler, class-group, conductor, and Galois-character factors with normalization and nonzero-denominator obligations.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100 },
    { leafId := "M0438-API-L06",
      package := "Comparison formula",
      expectedApi := "State and prove the terminal Shida-period comparison relating the normalized period integral to the arithmetic target.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100 } ]

/-- The missing-API split contains the six packages requested by the child task. -/
theorem shidaPeriodMissingApiLeaves_length :
    shidaPeriodMissingApiLeaves.length = 6 := by
  rfl

/-- All current missing-API leaves are explicitly unchecked, not completed. -/
theorem shidaPeriodMissingApiLeaves_statuses :
    shidaPeriodMissingApiLeaves.map MissingApiLeaf.status =
      ["unchecked", "unchecked", "unchecked", "unchecked", "unchecked", "unchecked"] := by
  rfl

/-- Each current missing-API leaf carries the M0387 local budget cap. -/
theorem shidaPeriodMissingApiLeaves_budgets :
    shidaPeriodMissingApiLeaves.map MissingApiLeaf.localBudget =
      [100, 100, 100, 100, 100, 100] := by
  rfl

/-- Projection wrapper for the properness part of the geometric package. -/
theorem geometricShidaModel_proper {D : ShidaPeriodDatum.{u, v}}
    (h : GeometricShidaModel D) : IsProper D.structureMap :=
  h.1

/-- Projection wrapper for the smoothness part of the geometric package. -/
theorem geometricShidaModel_smooth {D : ShidaPeriodDatum.{u, v}}
    (h : GeometricShidaModel D) : Smooth D.structureMap :=
  h.2

/--
mathlib anchor: a proper geometrically integral group scheme over a field is
commutative.  This is adjacent abelian/group-scheme infrastructure, not a
definition or theorem about Shida varieties.
-/
theorem proper_geometricallyIntegral_group_commutative
    (K : Type u) [Field K] (G : Over (FieldBaseScheme K))
    [IsProper G.hom] [GeometricallyIntegral G.hom] [GrpObj G] :
    IsCommMonObj G :=
  isCommMonObj_of_isProper_of_geometricallyIntegral G

/-! ## Stage1 audit constants -/

/-- Pinned mathlib revision audited for the Stage1 Shida-period substrate. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Machine-proof debt classification for the current repo-local artifact.

The human theorem is treated as known mathematics, while this Lean module only
checks statement-shape and adjacent mathlib substrate.
-/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration gate for completion claims.

This slot has no pinned external Lean 4 terminal Shida-period proof in the local
Lake closure.  If a later audit finds one, completion requires pin/import/check
or an explicit integration blocker.
-/
def repoLocalIntegrationDebtGate : String :=
  "not_completed; no repo_local_integration_debt completion claim"

/-- M0387-style wrapper-gate status for the Shida-period slot. -/
structure WrapperGateStatus where
  upstreamProofFound : Bool
  localIntegrationRoute : String
  debtClass : String
  completionClaimAllowed : Bool

/--
Current wrapper-gate diagnosis for `THM-M-0438.wrapper-gate`.

No terminal Lean 4 Shida-period proof has been identified in the local Lake
closure.  Therefore there is no proof body to wrap in this repository, and the
slot remains noncompleted formalization debt.  If a future primary-source audit
finds a closed upstream proof, this status must be replaced by a pinned
dependency, vendored proof body, or a concrete integration blocker.
-/
def wrapperGateStatus : WrapperGateStatus where
  upstreamProofFound := false
  localIntegrationRoute :=
    "none; no terminal Lean 4 Shida-period proof is currently in the local Lake closure"
  debtClass := "formalization_debt"
  completionClaimAllowed := false

/-- The current wrapper gate records no upstream terminal proof to wrap. -/
theorem wrapperGate_no_upstreamProofFound :
    wrapperGateStatus.upstreamProofFound = false := by
  rfl

/-- The current wrapper gate keeps the slot in formalization debt. -/
theorem wrapperGate_debtClass :
    wrapperGateStatus.debtClass = "formalization_debt" := by
  rfl

/-- The current wrapper gate explicitly forbids a completion claim. -/
theorem wrapperGate_no_completionClaim :
    wrapperGateStatus.completionClaimAllowed = false := by
  rfl

/--
Mathlib modules currently imported as checked substrate for this Stage1 slot.

The public task names `Morphism.Proper/Smooth` as shorthand; the actual mathlib
module paths at the pinned revision are `Morphisms.Proper` and
`Morphisms.Smooth`.
-/
def mathlibAnchorModules : List String :=
  [ "Mathlib.AlgebraicGeometry.Scheme",
    "Mathlib.AlgebraicGeometry.Group.Abelian",
    "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    "Mathlib.MeasureTheory.Integral.Bochner.Basic",
    "Mathlib.NumberTheory.NumberField.Basic",
    "Mathlib.RingTheory.ClassGroup" ]

/-- Integration-ready audit rows pairing requested module labels with imports. -/
def mathlibModuleAuditRows : List (String × String) :=
  [ ("AlgebraicGeometry.Scheme",
      "Mathlib.AlgebraicGeometry.Scheme"),
    ("AlgebraicGeometry.Group.Abelian",
      "Mathlib.AlgebraicGeometry.Group.Abelian"),
    ("Morphism.Proper",
      "Mathlib.AlgebraicGeometry.Morphisms.Proper"),
    ("Morphism.Smooth",
      "Mathlib.AlgebraicGeometry.Morphisms.Smooth"),
    ("MeasureTheory.Integral.Bochner.Basic",
      "Mathlib.MeasureTheory.Integral.Bochner.Basic"),
    ("NumberField.Basic",
      "Mathlib.NumberTheory.NumberField.Basic"),
    ("RingTheory.ClassGroup",
      "Mathlib.RingTheory.ClassGroup") ]

/-- Search terms for a later public Lean 4 external-anchor audit. -/
def externalLeanAuditSearchTerms : List String :=
  [ "Shida",
    "ShidaPeriod",
    "Shida variety",
    "period integral",
    "ShimuraVariety",
    "AbelianVariety",
    "Automorphic",
    "GaloisRepresentation" ]

/-! ## Leaf-ledger expansion for public backfill item `THM-M-0438.leaf-ledger` -/

/-- M0387-style proof/process ledger row for the open Shida-period leaves. -/
structure ProofProcessLeafLedger where
  leafId : String
  package : String
  proofOrProcessTarget : String
  closureGate : String
  status : String
  debtClass : String
  localBudget : Nat
  publicCompletionAllowed : Bool

/--
Independent `<=100` proof/process ledgers for `M0438-L009` through `M0438-L022`.

These rows are integration-ready process boundaries, not completed proof leaves.
They deliberately keep all rows `unchecked` and disallow public completion until
the corresponding concrete Lean object, proof, wrapper, or serial public merge
has been supplied and locally validated.
-/
def shidaPeriodProofProcessLeafLedgers : List ProofProcessLeafLedger :=
  [ { leafId := "M0438-L009",
      package := "P2 Shida-variety carrier",
      proofOrProcessTarget :=
        "Identify the source definition of the relevant Shida variety and choose the Lean carrier object or pinned upstream declaration.",
      closureGate :=
        "A concrete Scheme/moduli carrier or pinned theorem namespace is available in the local Lake closure, with source citation and no placeholder proof.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L010",
      package := "P2 canonical model and level data",
      proofOrProcessTarget :=
        "Define or pin canonical model, level structure, reflex-field data, descent datum, and reciprocity obligations.",
      closureGate :=
        "Concrete structures or imported declarations replace proposition-valued placeholders for canonical model, level, reflex field, and reciprocity data.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L011",
      package := "P2 geometric hypotheses",
      proofOrProcessTarget :=
        "Prove or import properness, smoothness, and any required geometric hypotheses for the chosen Shida model.",
      closureGate :=
        "The selected structure morphism has checked local proofs or pinned wrappers for all geometric hypotheses used by the period theorem.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L012",
      package := "P3 period cycle and domain",
      proofOrProcessTarget :=
        "Define the cycle, chain, or integration domain used in the Shida-period integral, including measure/orientation choices.",
      closureGate :=
        "A concrete domain and cycle package replaces the abstract period-domain field and validates measurability or orientation side conditions.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L013",
      package := "P3 integrand data",
      proofOrProcessTarget :=
        "Define the differential form, cohomology class, automorphic form, or kernel being integrated.",
      closureGate :=
        "Concrete integrand data are supplied with checked typing against the selected domain and cycle package.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L014",
      package := "P3 integral bridge",
      proofOrProcessTarget :=
        "Connect the concrete Shida-period integral to `PeriodIntegralPackage` or replace that package with the correct domain-specific integral API.",
      closureGate :=
        "The concrete integral, integrability proof, and bridge to the datum's period value are locally checked.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L015",
      package := "P4 arithmetic factors",
      proofOrProcessTarget :=
        "Define local and global arithmetic factors required by the comparison formula.",
      closureGate :=
        "Algebraic, Euler, conductor, class-group, and normalization factors are concrete Lean data with their side conditions.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L016",
      package := "P4 L-function API audit",
      proofOrProcessTarget :=
        "Audit whether existing Dirichlet, L-function, or related analytic APIs are relevant or insufficient for the intended formula.",
      closureGate :=
        "The audit records exact module paths, theorem names, and a clear use-or-insufficient decision for each candidate API.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L017",
      package := "P4 representation side conditions",
      proofOrProcessTarget :=
        "Define required Galois-representation, automorphic-representation, character, or field-of-definition side conditions.",
      closureGate :=
        "All representation-theoretic side conditions used by the terminal statement are concrete structures or pinned imports.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L018",
      package := "P5 comparison statement",
      proofOrProcessTarget :=
        "State the exact period comparison, equality, nonvanishing, algebraicity, or normalization conclusion.",
      closureGate :=
        "The target relation is no longer `hasPeriodComparison : Prop`; it is a precise Lean proposition over concrete data.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L019",
      package := "P5 comparison proof",
      proofOrProcessTarget :=
        "Prove the comparison formula after all objects are concrete, or wrap a checked upstream theorem.",
      closureGate :=
        "A local proof body, pinned mathlib wrapper, or pinned external wrapper validates without unchecked placeholders or new axioms.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 100,
      publicCompletionAllowed := false },
    { leafId := "M0438-L020",
      package := "P6 external proof integration",
      proofOrProcessTarget :=
        "If an external Lean 4 proof is found, pin/import/check it or record a precise integration blocker.",
      closureGate :=
        "The external proof is in the local Lake closure, or the blocker names exact toolchain, dependency, license, or API incompatibility.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 80,
      publicCompletionAllowed := false },
    { leafId := "M0438-L021",
      package := "P6 terminal wrapper validation",
      proofOrProcessTarget :=
        "Add a local wrapper theorem with no placeholders and rerun the Stage1 validation command.",
      closureGate :=
        "`lake env lean AwesomeTheorems/Stage1/S1_M_086.lean` passes after the wrapper enters the file.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 60,
      publicCompletionAllowed := false },
    { leafId := "M0438-L022",
      package := "P7 public merge",
      proofOrProcessTarget :=
        "Merge stable facts into public blueprint, todo, and README surfaces only after machine anchor and ledger agree.",
      closureGate :=
        "A serial integrator updates public surfaces after validation, debt classification, and checklist consistency are satisfied.",
      status := "unchecked",
      debtClass := "formalization_debt",
      localBudget := 50,
      publicCompletionAllowed := false } ]

/-- The child leaf-ledger expansion covers exactly `M0438-L009` through `M0438-L022`. -/
theorem shidaPeriodProofProcessLeafLedgers_length :
    shidaPeriodProofProcessLeafLedgers.length = 14 := by
  rfl

/-- All expanded proof/process leaves remain unchecked. -/
theorem shidaPeriodProofProcessLeafLedgers_statuses :
    shidaPeriodProofProcessLeafLedgers.map ProofProcessLeafLedger.status =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked" ] := by
  rfl

/-- Every expanded proof/process leaf is budgeted at or below the M0387 cap. -/
theorem shidaPeriodProofProcessLeafLedgers_budgets_within_cap :
    (shidaPeriodProofProcessLeafLedgers.map ProofProcessLeafLedger.localBudget).all
      (fun n => decide (n <= 100)) = true := by
  rfl

/-- No expanded proof/process leaf authorizes public completion in the current state. -/
theorem shidaPeriodProofProcessLeafLedgers_no_completion :
    shidaPeriodProofProcessLeafLedgers.map ProofProcessLeafLedger.publicCompletionAllowed =
      [ false, false, false, false, false, false, false, false, false, false,
        false, false, false, false ] := by
  rfl

/-! ## Audit probes -/

#check FieldBaseScheme
#check PeriodIntegral
#check ShidaPeriodDatum.periodValue
#check ShidaPeriodDatum.classGroupAvailable
#check StatementShape
#check statementNormalizationNote
#check ShidaVarietyModelData
#check CanonicalModelLevelReflexData
#check CanonicalModelLevelReflexData.reflexClassGroupAvailable
#check PeriodCycleDomainData
#check AutomorphicCohomologyIntegrandData
#check AutomorphicCohomologyIntegrandData.toPeriodPackage
#check ArithmeticFactorData
#check ArithmeticFactorData.totalFactor
#check ShidaPeriodComparisonFormulaData
#check ShidaPeriodMissingApiPackage
#check ShidaPeriodMissingApiPackage.supplies_statement_shape_inputs
#check shidaPeriodMissingApiLeaves
#check shidaPeriodMissingApiLeaves_length
#check shidaPeriodMissingApiLeaves_statuses
#check shidaPeriodMissingApiLeaves_budgets
#check proper_geometricallyIntegral_group_commutative
#check pinnedMathlibRevision
#check machineProofDebtClassification
#check repoLocalIntegrationDebtGate
#check WrapperGateStatus
#check wrapperGateStatus
#check wrapperGate_no_upstreamProofFound
#check wrapperGate_debtClass
#check wrapperGate_no_completionClaim
#check mathlibAnchorModules
#check mathlibModuleAuditRows
#check externalLeanAuditSearchTerms
#check ProofProcessLeafLedger
#check shidaPeriodProofProcessLeafLedgers
#check shidaPeriodProofProcessLeafLedgers_length
#check shidaPeriodProofProcessLeafLedgers_statuses
#check shidaPeriodProofProcessLeafLedgers_budgets_within_cap
#check shidaPeriodProofProcessLeafLedgers_no_completion

end S1_M_086
end Stage1
end AwesomeTheorems
