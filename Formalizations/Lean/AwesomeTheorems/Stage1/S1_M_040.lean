import Mathlib.AlgebraicGeometry.RationalMap
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
Stage1 artifact for S1-M-040 / THM-M-0121, Mori rationality theorem.

The current mathlib anchor covers scheme rational maps, their dense domains,
and the function-field correspondence for integral source schemes and locally
finite-type targets.  It does not define Fano varieties or prove Mori's
rationality theorem, so the main theorem shape below keeps the Fano input and
the intended rationality conclusion as explicit predicates.

The Stage1 normalization deliberately does not read the Japanese label
"Mori rationality theorem" as the false unqualified statement "all Fano
varieties are rational".  Until the source statement is fixed, the admissible
readings are rational curves on Fano varieties, uniruledness/rational
connectedness, or nef-threshold rationality.
-/

open CategoryTheory
open AlgebraicGeometry

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_040

/--
How this Stage1 artifact is exposed during the child pass.  The aggregator path
is reserved for a serial integrator; this worker keeps the file as a scoped
validation target checked directly by `lake env lean`.
-/
inductive Stage1SurfaceMode where
  | scopedValidationFile
  | aggregatorImport
  deriving DecidableEq, Repr

/--
Current child-task decision: keep `S1_M_040.lean` as a scoped validation file
rather than editing a shared import aggregator in a parallel worker pass.
-/
def selectedStage1SurfaceMode : Stage1SurfaceMode :=
  .scopedValidationFile

theorem selectedStage1SurfaceMode_eq :
    selectedStage1SurfaceMode = Stage1SurfaceMode.scopedValidationFile := rfl

/--
External-proof integration status for this scoped Stage1 artifact.

This records a repo-local audit state, not a mathematical theorem: this pass
did not locate a complete Lean 4 proof of Mori's rationality theorem that could
be pinned, imported, and checked inside the current Lake project.
-/
inductive ExternalProofIntegrationStatus where
  | noCompleteLean4ProofLocated
  | completeProofPinnedAndChecked
  | concreteIntegrationBlockerRecorded
  deriving DecidableEq, Repr

/--
Current C005 decision: no complete external Lean 4 proof was located in the
repo-local validation closure, so no anchor-only completion is claimed.
-/
def selectedExternalProofIntegrationStatus : ExternalProofIntegrationStatus :=
  .noCompleteLean4ProofLocated

theorem selectedExternalProofIntegrationStatus_eq :
    selectedExternalProofIntegrationStatus =
      ExternalProofIntegrationStatus.noCompleteLean4ProofLocated := rfl

/--
Statement-disambiguation choices for the overloaded Stage1 label
`THM-M-0121`, "Mori rationality theorem".
-/
inductive MoriRationalityReading where
  | rationalCurvesOnFano
  | uniruledOrRationalConnected
  | nefThresholdRationality
  | unqualifiedAllFanoRational
  deriving DecidableEq, Repr

/--
Local guard used by this Stage1 artifact: the first three readings are possible
normalization targets, while the unqualified assertion that every Fano variety
is rational is intentionally rejected unless a later public task supplies extra
hypotheses and a different formal statement.
-/
def MoriRationalityReadingAllowed : MoriRationalityReading → Prop
  | .rationalCurvesOnFano => True
  | .uniruledOrRationalConnected => True
  | .nefThresholdRationality => True
  | .unqualifiedAllFanoRational => False

theorem unqualifiedAllFanoRational_notAllowed :
    ¬ MoriRationalityReadingAllowed
      MoriRationalityReading.unqualifiedAllFanoRational := by
  intro h
  exact h

/--
Parametric normalized statement shape for a future Mori rationality theorem.

`FanoInput f` is the still-missing formal Fano/Mori hypothesis package, and
`RationalityConclusion f` is the target conclusion, e.g. a rational-curve,
uniruledness, or nef-threshold rationality formulation selected by the
integrator after the source statement is disambiguated.

Both inputs intentionally remain parameters. Current mathlib imports in this
repo-local artifact support rational maps and proper/finite-type morphisms, but
they do not yet provide a selected Fano hypothesis package, a Mori program
package, or a canonical conclusion package for rational curves, uniruledness,
rational connectedness, or nef-threshold rationality. Hard-coding either side
here would choose a theorem reading before the public Stage1 normalization task
has fixed the mathematical target.
-/
def MoriRationalityStatementShape
    (FanoInput RationalityConclusion :
      {S X : Scheme.{u}} → (X ⟶ S) → Prop) : Prop :=
  ∀ ⦃S X : Scheme.{u}⦄ (f : X ⟶ S), FanoInput f → RationalityConclusion f

/--
Checked normalization note for `MoriRationalityStatementShape`: after the
source theorem reading is chosen, the statement must specialize this exact
parametric implication by supplying a concrete `FanoInput` and a concrete
`RationalityConclusion`. This lemma records that the current Stage1 artifact
adds no hidden assumptions or built-in conclusion beyond that implication.
-/
theorem MoriRationalityStatementShape_iff
    (FanoInput RationalityConclusion :
      {S X : Scheme.{u}} → (X ⟶ S) → Prop) :
    MoriRationalityStatementShape FanoInput RationalityConclusion ↔
      ∀ ⦃S X : Scheme.{u}⦄ (f : X ⟶ S),
        FanoInput f → RationalityConclusion f := Iff.rfl

/--
A low-risk mathlib-backed input package that is often part of the geometric
boundary for Fano-style statements.  This is not a definition of Fano.
-/
def ProperFiniteTypeIntegralInput {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  IsProper f ∧ LocallyOfFiniteType f ∧ IsIntegral X

/--
Repo-local status of a geometric API needed for a concrete Fano hypothesis
package.  `mathlibBacked` means the predicate is supplied by an imported
mathlib declaration and can be used in checked statements; `externalSelected`
is reserved for a future pinned dependency; `missing` keeps the current
artifact from silently treating a placeholder as a completed formal input.
-/
inductive FanoApiSelectionStatus where
  | mathlibBacked
  | externalSelected
  | missing
  deriving DecidableEq, Repr

/--
The selected API predicates for a future Fano hypothesis package over schemes.

`smoothMorphism` is backed by mathlib's `AlgebraicGeometry.Smooth`; the other
predicate fields are explicit slots because this local mathlib snapshot does
not yet provide selected scheme-level projective morphism, normal scheme,
canonical divisor/sheaf, or anticanonical positivity APIs for this theorem.
-/
structure FanoHypothesisApiSelection where
  smoothStatus : FanoApiSelectionStatus
  projectiveStatus : FanoApiSelectionStatus
  normalStatus : FanoApiSelectionStatus
  canonicalStatus : FanoApiSelectionStatus
  anticanonicalPositivityStatus : FanoApiSelectionStatus
  smoothMorphism : {S X : Scheme.{u}} → (X ⟶ S) → Prop
  projectiveMorphism : {S X : Scheme.{u}} → (X ⟶ S) → Prop
  normalScheme : Scheme.{u} → Prop
  canonicalClassOrSheafSelected : {S X : Scheme.{u}} → (X ⟶ S) → Prop
  anticanonicalPositive : {S X : Scheme.{u}} → (X ⟶ S) → Prop

namespace FanoHypothesisApiSelection

/--
Minimum gate for treating a Fano input package as API-selected rather than
placeholder-backed.  A smooth route or a normal route may supply the
regularity slot, but projectivity, canonical class/sheaf, and anticanonical
positivity must all be selected.
-/
def closed (apis : FanoHypothesisApiSelection) : Prop :=
  apis.projectiveStatus ≠ FanoApiSelectionStatus.missing ∧
    (apis.smoothStatus ≠ FanoApiSelectionStatus.missing ∨
      apis.normalStatus ≠ FanoApiSelectionStatus.missing) ∧
    apis.canonicalStatus ≠ FanoApiSelectionStatus.missing ∧
    apis.anticanonicalPositivityStatus ≠ FanoApiSelectionStatus.missing

end FanoHypothesisApiSelection

/--
Current repo-local API selection for the C006 child pass.

Only the smoothness slot is mathlib-backed.  The missing slots are deliberately
defined as `False` predicates so no later theorem can accidentally discharge a
Fano hypothesis package while projective, canonical, and positivity APIs remain
unselected.
-/
def currentFanoHypothesisApiSelection : FanoHypothesisApiSelection where
  smoothStatus := .mathlibBacked
  projectiveStatus := .missing
  normalStatus := .missing
  canonicalStatus := .missing
  anticanonicalPositivityStatus := .missing
  smoothMorphism := fun f => Smooth f
  projectiveMorphism := fun _ => False
  normalScheme := fun _ => False
  canonicalClassOrSheafSelected := fun _ => False
  anticanonicalPositive := fun _ => False

theorem currentFanoHypothesisApiSelection_smooth_iff
    {S X : Scheme.{u}} (f : X ⟶ S) :
    currentFanoHypothesisApiSelection.smoothMorphism f ↔ Smooth f := Iff.rfl

theorem currentFanoHypothesisApiSelection_notClosed :
    ¬ currentFanoHypothesisApiSelection.closed := by
  intro h
  exact h.1 rfl

/--
Concrete Stage1 shape of a Fano hypothesis package over `Scheme` once the
remaining projective/canonical/positivity APIs are selected.

This is intentionally a hypothesis package, not a theorem asserting examples.
It combines currently available scheme facts (`IsProper`, `Smooth`,
`IsIntegral`) with the selected API slots for projectivity, normality as an
alternative regularity route, canonical class/sheaf selection, and
anticanonical positivity.
-/
structure FanoHypothesisPackage
    (apis : FanoHypothesisApiSelection) {S X : Scheme.{u}} (f : X ⟶ S) : Prop where
  proper : IsProper f
  integralSource : IsIntegral X
  regularity : apis.smoothMorphism f ∨ apis.normalScheme X
  projective : apis.projectiveMorphism f
  canonicalClassOrSheaf : apis.canonicalClassOrSheafSelected f
  anticanonicalPositive : apis.anticanonicalPositive f

/--
The Fano package specializes the existing low-risk proper/finite-type/integral
boundary whenever the package is available.
-/
theorem FanoHypothesisPackage.toProperFiniteTypeIntegralInput
    (apis : FanoHypothesisApiSelection) {S X : Scheme.{u}} {f : X ⟶ S}
    (h : FanoHypothesisPackage apis f) :
    ProperFiniteTypeIntegralInput f := by
  letI : IsProper f := h.proper
  exact ⟨h.proper, inferInstance, h.integralSource⟩

/--
The concrete Fano input predicate to pass into
`MoriRationalityStatementShape` after API selection closes.
-/
def ConcreteFanoInput
    (apis : FanoHypothesisApiSelection) {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  FanoHypothesisPackage apis f

theorem ConcreteFanoInput_iff
    (apis : FanoHypothesisApiSelection) {S X : Scheme.{u}} (f : X ⟶ S) :
    ConcreteFanoInput apis f ↔ FanoHypothesisPackage apis f := Iff.rfl

/--
Repo-local status of a geometric API needed for a concrete rationality
conclusion package.  The current local artifact has no selected APIs for
rational-curve coverage, uniruledness, rational connectedness, or rational
nef-thresholds, so missing slots remain explicit blockers.
-/
inductive RationalityConclusionApiSelectionStatus where
  | mathlibBacked
  | externalSelected
  | missing
  deriving DecidableEq, Repr

/--
The selected API predicates for the conclusion side of a future Mori
rationality statement.

The three admissible readings from `MoriRationalityReading` require different
conclusion predicates:

* `rationalCurveCoverage` for rational curves on Fano-type varieties;
* `uniruled` or `rationalConnected` for the corresponding coverage/chain
  connectedness reading;
* `rationalNefThreshold` for the Mori-Kawamata-Shokurov nef-threshold
  rationality reading.

The predicates are fields rather than axioms.  A package is closed only when
the selected reading has a non-missing API status.
-/
structure RationalityConclusionApiSelection where
  rationalCurveCoverageStatus : RationalityConclusionApiSelectionStatus
  uniruledStatus : RationalityConclusionApiSelectionStatus
  rationalConnectedStatus : RationalityConclusionApiSelectionStatus
  nefThresholdStatus : RationalityConclusionApiSelectionStatus
  rationalCurveCoverage : {S X : Scheme.{u}} → (X ⟶ S) → Prop
  uniruled : {S X : Scheme.{u}} → (X ⟶ S) → Prop
  rationalConnected : {S X : Scheme.{u}} → (X ⟶ S) → Prop
  rationalNefThreshold : {S X : Scheme.{u}} → (X ⟶ S) → Prop

namespace RationalityConclusionApiSelection

/--
Closure gate for the conclusion package matching a selected theorem reading.
The rejected unqualified "all Fano varieties are rational" reading is never
closed by this Stage1 artifact.
-/
def closedFor
    (reading : MoriRationalityReading)
    (apis : RationalityConclusionApiSelection) : Prop :=
  match reading with
  | .rationalCurvesOnFano =>
      apis.rationalCurveCoverageStatus ≠
        RationalityConclusionApiSelectionStatus.missing
  | .uniruledOrRationalConnected =>
      apis.uniruledStatus ≠ RationalityConclusionApiSelectionStatus.missing ∨
        apis.rationalConnectedStatus ≠ RationalityConclusionApiSelectionStatus.missing
  | .nefThresholdRationality =>
      apis.nefThresholdStatus ≠ RationalityConclusionApiSelectionStatus.missing
  | .unqualifiedAllFanoRational => False

end RationalityConclusionApiSelection

/--
Current repo-local API selection for the C007 child pass.

All conclusion slots are deliberately `missing` and implemented as `False`
predicates because the local dependency audit did not locate selected
rational-curve, uniruledness, rational-connectedness, or nef-threshold APIs.
-/
def currentRationalityConclusionApiSelection : RationalityConclusionApiSelection where
  rationalCurveCoverageStatus := .missing
  uniruledStatus := .missing
  rationalConnectedStatus := .missing
  nefThresholdStatus := .missing
  rationalCurveCoverage := fun _ => False
  uniruled := fun _ => False
  rationalConnected := fun _ => False
  rationalNefThreshold := fun _ => False

theorem currentRationalityConclusionApiSelection_notClosedFor
    (reading : MoriRationalityReading)
    (h : MoriRationalityReadingAllowed reading) :
    ¬ RationalityConclusionApiSelection.closedFor reading
      currentRationalityConclusionApiSelection := by
  cases reading <;>
    simp [MoriRationalityReadingAllowed, RationalityConclusionApiSelection.closedFor,
      currentRationalityConclusionApiSelection] at h ⊢

/--
Reading-specific rational-curve coverage conclusion package.
-/
def RationalCurveCoverageConclusion
    (apis : RationalityConclusionApiSelection)
    {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  apis.rationalCurveCoverage f

/--
Reading-specific uniruledness/rational-connectedness conclusion package.
-/
def UniruledOrRationalConnectedConclusion
    (apis : RationalityConclusionApiSelection)
    {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  apis.uniruled f ∨ apis.rationalConnected f

/--
Reading-specific rational nef-threshold conclusion package.
-/
def RationalNefThresholdConclusion
    (apis : RationalityConclusionApiSelection)
    {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  apis.rationalNefThreshold f

/--
Concrete conclusion package to pass into `MoriRationalityStatementShape` after
the source reading and the matching conclusion APIs are selected.

This is a checked package boundary, not a proof of Mori's rationality theorem:
constructing it requires an allowed reading, the corresponding `closedFor`
gate, and the actual conclusion predicate for that reading.
-/
def RationalityConclusionPackage
    (apis : RationalityConclusionApiSelection)
    {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  ∃ selectedReading : MoriRationalityReading,
    MoriRationalityReadingAllowed selectedReading ∧
      RationalityConclusionApiSelection.closedFor selectedReading apis ∧
        match selectedReading with
        | .rationalCurvesOnFano => RationalCurveCoverageConclusion apis f
        | .uniruledOrRationalConnected => UniruledOrRationalConnectedConclusion apis f
        | .nefThresholdRationality => RationalNefThresholdConclusion apis f
        | .unqualifiedAllFanoRational => False

/--
The concrete rationality conclusion predicate to pass into
`MoriRationalityStatementShape` after conclusion API selection closes.
-/
def ConcreteRationalityConclusion
    (apis : RationalityConclusionApiSelection)
    {S X : Scheme.{u}} (f : X ⟶ S) : Prop :=
  RationalityConclusionPackage apis f

theorem ConcreteRationalityConclusion_iff
    (apis : RationalityConclusionApiSelection) {S X : Scheme.{u}} (f : X ⟶ S) :
    ConcreteRationalityConclusion apis f ↔
      RationalityConclusionPackage apis f := Iff.rfl

theorem currentRationalityConclusionApiSelection_noPackage
    {S X : Scheme.{u}} (f : X ⟶ S) :
    ¬ ConcreteRationalityConclusion currentRationalityConclusionApiSelection f := by
  intro h
  rcases h with ⟨selectedReading, readingAllowed, selectionClosed, _conclusion⟩
  exact currentRationalityConclusionApiSelection_notClosedFor
    selectedReading readingAllowed selectionClosed

/--
Existing mathlib rational-map fact used as a local Stage1 anchor: every scheme
rational map has a dense domain of definition.
-/
def RationalMapDomainDenseStatement : Prop :=
  ∀ (X Y : Scheme.{u}) (φ : X ⤏ Y), Dense (X := X) φ.domain

theorem rationalMapDomainDense : RationalMapDomainDenseStatement := by
  intro X Y φ
  exact Scheme.RationalMap.dense_domain φ

/--
Existing mathlib bridge: for integral `X` and locally finite-type `Y` over a
base `S`, morphisms from the function field of `X` to `Y` correspond to
`S`-rational maps `X ⤏ Y`.
-/
def FunctionFieldRationalMapBridgeStatement : Prop :=
  ∀ {S X Y : Scheme.{u}} (sX : X ⟶ S) (sY : Y ⟶ S)
    [IsIntegral X] [LocallyOfFiniteType sY],
      Nonempty ({ f : Spec X.functionField ⟶ Y //
          f ≫ sY = X.fromSpecStalk _ ≫ sX } ≃
        { f : X ⤏ Y // f.compHom sY = sX.toRationalMap })

theorem functionFieldRationalMapBridge :
    FunctionFieldRationalMapBridgeStatement := by
  intro S X Y sX sY _ _
  exact ⟨Scheme.RationalMap.equivFunctionField sX sY⟩

/--
Named packages for the main proof tree.  This is a Stage1 budgeting artifact:
it fixes the local proof-work decomposition before any public checklist can be
marked completed.
-/
inductive MoriProofPackage where
  | sourceDisambiguation
  | statementNormalization
  | mathlibObjectModel
  | fanoPackage
  | rationalityConclusionPackage
  | bridgeToExistingMathlib
  | mainProofBranch
  | repoLocalClosureGate
  deriving DecidableEq, Repr

/--
Closure state for a named proof-tree leaf in this local artifact.
-/
inductive MoriProofLeafStatus where
  | checkedLocalStatementShape
  | checkedLocalWrapper
  | checkedLocalValidation
  | unchecked
  | blockedByMissingApiSelection
  | publicIntegratorGateOpen
  deriving DecidableEq, Repr

/--
Named leaves for the main proof tree.  The labels intentionally mirror the
private ledger ids, but the public blueprint remains owned by a later serial
integrator.
-/
inductive MoriProofLeaf where
  | MR_L001_sourceTerminology
  | MR_L002_rejectFalseAllFanoRationalReading
  | MR_L003_universeSchemeStatementShape
  | MR_L004_parametricFanoAndConclusionBoundary
  | MR_L005_rationalMapNotationAnchor
  | MR_L006_rationalMapDenseDomainAnchor
  | MR_L007_functionFieldRationalMapBridgeAnchor
  | MR_L008_properFiniteTypeMorphismAnchors
  | MR_L009_integralSchemeAnchor
  | MR_L010_projectiveEncodingSelection
  | MR_L011_smoothNormalKltSelection
  | MR_L012_canonicalClassOrSheafSelection
  | MR_L013_anticanonicalPositivitySelection
  | MR_L014_rationalCurveConclusionSelection
  | MR_L015_uniruledRationalConnectedSelection
  | MR_L016_nefThresholdConclusionSelection
  | MR_L017_denseDomainTransportLeaf
  | MR_L018_functionFieldBridgeTransportLeaf
  | MR_L019_firstMainProofBranchSelection
  | MR_L020_bendAndBreakOrThresholdSublemmaSplit
  | MR_L021_scopedLeanValidation
  | MR_L022_publicAggregatorDecision
  deriving DecidableEq, Repr

namespace MoriProofLeaf

/--
The package that owns each proof-tree leaf.
-/
def package : MoriProofLeaf → MoriProofPackage
  | .MR_L001_sourceTerminology => .sourceDisambiguation
  | .MR_L002_rejectFalseAllFanoRationalReading => .sourceDisambiguation
  | .MR_L003_universeSchemeStatementShape => .statementNormalization
  | .MR_L004_parametricFanoAndConclusionBoundary => .statementNormalization
  | .MR_L005_rationalMapNotationAnchor => .mathlibObjectModel
  | .MR_L006_rationalMapDenseDomainAnchor => .mathlibObjectModel
  | .MR_L007_functionFieldRationalMapBridgeAnchor => .mathlibObjectModel
  | .MR_L008_properFiniteTypeMorphismAnchors => .mathlibObjectModel
  | .MR_L009_integralSchemeAnchor => .mathlibObjectModel
  | .MR_L010_projectiveEncodingSelection => .fanoPackage
  | .MR_L011_smoothNormalKltSelection => .fanoPackage
  | .MR_L012_canonicalClassOrSheafSelection => .fanoPackage
  | .MR_L013_anticanonicalPositivitySelection => .fanoPackage
  | .MR_L014_rationalCurveConclusionSelection => .rationalityConclusionPackage
  | .MR_L015_uniruledRationalConnectedSelection => .rationalityConclusionPackage
  | .MR_L016_nefThresholdConclusionSelection => .rationalityConclusionPackage
  | .MR_L017_denseDomainTransportLeaf => .bridgeToExistingMathlib
  | .MR_L018_functionFieldBridgeTransportLeaf => .bridgeToExistingMathlib
  | .MR_L019_firstMainProofBranchSelection => .mainProofBranch
  | .MR_L020_bendAndBreakOrThresholdSublemmaSplit => .mainProofBranch
  | .MR_L021_scopedLeanValidation => .repoLocalClosureGate
  | .MR_L022_publicAggregatorDecision => .repoLocalClosureGate

/--
Local target proof-step budget for each named leaf.  These are budgets for
future local leaf proofs, not a claim that the missing Fano/Mori proof branches
have been completed.
-/
def targetStepBudget : MoriProofLeaf → Nat
  | .MR_L001_sourceTerminology => 30
  | .MR_L002_rejectFalseAllFanoRationalReading => 20
  | .MR_L003_universeSchemeStatementShape => 15
  | .MR_L004_parametricFanoAndConclusionBoundary => 20
  | .MR_L005_rationalMapNotationAnchor => 15
  | .MR_L006_rationalMapDenseDomainAnchor => 20
  | .MR_L007_functionFieldRationalMapBridgeAnchor => 25
  | .MR_L008_properFiniteTypeMorphismAnchors => 20
  | .MR_L009_integralSchemeAnchor => 15
  | .MR_L010_projectiveEncodingSelection => 60
  | .MR_L011_smoothNormalKltSelection => 70
  | .MR_L012_canonicalClassOrSheafSelection => 80
  | .MR_L013_anticanonicalPositivitySelection => 80
  | .MR_L014_rationalCurveConclusionSelection => 70
  | .MR_L015_uniruledRationalConnectedSelection => 80
  | .MR_L016_nefThresholdConclusionSelection => 80
  | .MR_L017_denseDomainTransportLeaf => 20
  | .MR_L018_functionFieldBridgeTransportLeaf => 25
  | .MR_L019_firstMainProofBranchSelection => 80
  | .MR_L020_bendAndBreakOrThresholdSublemmaSplit => 90
  | .MR_L021_scopedLeanValidation => 20
  | .MR_L022_publicAggregatorDecision => 40

/--
Current repo-local status of each named leaf.  Missing API selections and the
main Mori proof branch stay open; checked statuses are limited to this file's
statement-shape and mathlib-wrapper facts.
-/
def status : MoriProofLeaf → MoriProofLeafStatus
  | .MR_L001_sourceTerminology => .unchecked
  | .MR_L002_rejectFalseAllFanoRationalReading => .checkedLocalStatementShape
  | .MR_L003_universeSchemeStatementShape => .checkedLocalStatementShape
  | .MR_L004_parametricFanoAndConclusionBoundary => .checkedLocalStatementShape
  | .MR_L005_rationalMapNotationAnchor => .checkedLocalWrapper
  | .MR_L006_rationalMapDenseDomainAnchor => .checkedLocalWrapper
  | .MR_L007_functionFieldRationalMapBridgeAnchor => .checkedLocalWrapper
  | .MR_L008_properFiniteTypeMorphismAnchors => .checkedLocalStatementShape
  | .MR_L009_integralSchemeAnchor => .checkedLocalStatementShape
  | .MR_L010_projectiveEncodingSelection => .blockedByMissingApiSelection
  | .MR_L011_smoothNormalKltSelection => .blockedByMissingApiSelection
  | .MR_L012_canonicalClassOrSheafSelection => .blockedByMissingApiSelection
  | .MR_L013_anticanonicalPositivitySelection => .blockedByMissingApiSelection
  | .MR_L014_rationalCurveConclusionSelection => .blockedByMissingApiSelection
  | .MR_L015_uniruledRationalConnectedSelection => .blockedByMissingApiSelection
  | .MR_L016_nefThresholdConclusionSelection => .blockedByMissingApiSelection
  | .MR_L017_denseDomainTransportLeaf => .checkedLocalWrapper
  | .MR_L018_functionFieldBridgeTransportLeaf => .checkedLocalWrapper
  | .MR_L019_firstMainProofBranchSelection => .unchecked
  | .MR_L020_bendAndBreakOrThresholdSublemmaSplit => .unchecked
  | .MR_L021_scopedLeanValidation => .checkedLocalValidation
  | .MR_L022_publicAggregatorDecision => .publicIntegratorGateOpen

theorem targetStepBudget_le_100 (leaf : MoriProofLeaf) :
    leaf.targetStepBudget ≤ 100 := by
  cases leaf <;> decide

end MoriProofLeaf

/--
The complete local named-leaf inventory for the Stage1 child split.
-/
def moriProofLeafInventory : List MoriProofLeaf :=
  [ MoriProofLeaf.MR_L001_sourceTerminology
  , MoriProofLeaf.MR_L002_rejectFalseAllFanoRationalReading
  , MoriProofLeaf.MR_L003_universeSchemeStatementShape
  , MoriProofLeaf.MR_L004_parametricFanoAndConclusionBoundary
  , MoriProofLeaf.MR_L005_rationalMapNotationAnchor
  , MoriProofLeaf.MR_L006_rationalMapDenseDomainAnchor
  , MoriProofLeaf.MR_L007_functionFieldRationalMapBridgeAnchor
  , MoriProofLeaf.MR_L008_properFiniteTypeMorphismAnchors
  , MoriProofLeaf.MR_L009_integralSchemeAnchor
  , MoriProofLeaf.MR_L010_projectiveEncodingSelection
  , MoriProofLeaf.MR_L011_smoothNormalKltSelection
  , MoriProofLeaf.MR_L012_canonicalClassOrSheafSelection
  , MoriProofLeaf.MR_L013_anticanonicalPositivitySelection
  , MoriProofLeaf.MR_L014_rationalCurveConclusionSelection
  , MoriProofLeaf.MR_L015_uniruledRationalConnectedSelection
  , MoriProofLeaf.MR_L016_nefThresholdConclusionSelection
  , MoriProofLeaf.MR_L017_denseDomainTransportLeaf
  , MoriProofLeaf.MR_L018_functionFieldBridgeTransportLeaf
  , MoriProofLeaf.MR_L019_firstMainProofBranchSelection
  , MoriProofLeaf.MR_L020_bendAndBreakOrThresholdSublemmaSplit
  , MoriProofLeaf.MR_L021_scopedLeanValidation
  , MoriProofLeaf.MR_L022_publicAggregatorDecision
  ]

theorem moriProofLeafInventory_length :
    moriProofLeafInventory.length = 22 := rfl

/--
Every named leaf in this local inventory has a declared target proof-step
budget of at most 100.
-/
theorem moriProofLeafInventory_budgeted :
    ∀ leaf ∈ moriProofLeafInventory, leaf.targetStepBudget ≤ 100 := by
  intro leaf _h
  exact MoriProofLeaf.targetStepBudget_le_100 leaf

end S1_M_040
end Stage1
end AwesomeTheorems
