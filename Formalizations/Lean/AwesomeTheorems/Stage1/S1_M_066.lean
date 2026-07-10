import Mathlib.Algebra.Quaternion
import Mathlib.Algebra.QuaternionBasis
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.Sites.Etale
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.CMField
import Mathlib.RingTheory.ClassGroup

/-!
# S1-M-066 / THM-M-0437: Shida varieties

Stage1 statement-shape artifact for the source claim "construction of
Hodge-type Shida varieties" (`Hodge型志田簇的构造`).

The file records a precise Lean boundary and a few low-level mathlib anchors:
quaternion algebras, schemes and geometric morphism predicates, number fields,
CM-field predicates, adeles, class groups, and the etale topology.  It also
records checked Stage1 structure boundaries for the Hodge-type datum, Hodge
embedding, tensors/Hodge cycles, reflex field, level structure, the
abelian-scheme moduli problem, and the canonical-model/descent compatibility
package.  The actual moduli representability theorem, canonical-model theorem,
and construction theorem remain explicit predicates, because no terminal Shida
/ Shimura-variety construction theorem was found in the local dependency
closure.
-/

noncomputable section

open AlgebraicGeometry CategoryTheory Opposite ValuativeRel
open scoped WithZero

universe u

namespace AwesomeTheorems.Stage1.S1_M_066

/--
Public spelling decision for the source phrase `Hodge型志田簇的构造`.

The local source notes attribute the item to Goro Shimura, and the mathematical
phrase "Hodge-type ... varieties" matches the standard Hodge-type Shimura
variety construction target.  Thus the Stage1 public spelling should be
normalized as a Shimura/Hodge-type variant, while this file keeps the existing
`Shida` namespace and structure names as stable Stage1 identifiers until a
serial public-document merge can rename them consistently.
-/
inductive PublicSpellingInterpretation where
  | literalShida
  | hodgeTypeShimuraVariant
  | unresolved
  deriving DecidableEq, Repr

/-- Checked record of the P1 statement-normalization decision. -/
structure StatementNormalizationDecision where
  publicPhrase : String
  canonicalStage1IdSpelling : String
  selectedVariant : PublicSpellingInterpretation
  normalizedMathematicalTarget : String
  spellingBoundary : String
  completionBoundary : String

/--
P1 decision: read `志田簇` in this slot as the Hodge-type Shimura-variety
construction target, not as an independently verified literal "Shida variety"
theorem.
-/
def statementNormalizationDecision : StatementNormalizationDecision where
  publicPhrase := "Hodge型志田簇的构造"
  canonicalStage1IdSpelling := "S1-M-066 / THM-M-0437 uses Shida in current local identifiers"
  selectedVariant := PublicSpellingInterpretation.hodgeTypeShimuraVariant
  normalizedMathematicalTarget :=
    "construction/existence of Hodge-type Shimura varieties over the reflex field"
  spellingBoundary :=
    "treat 志田 as the current public-source spelling for this slot; use Shimura/Hodge-type as the mathematical target in future public backfill"
  completionBoundary :=
    "statement-normalization metadata only; no Hodge-type Shimura-variety construction theorem is proved"

/-- Projection check for the selected statement-normalization variant. -/
theorem statementNormalization_selects_hodgeTypeShimura :
    statementNormalizationDecision.selectedVariant =
      PublicSpellingInterpretation.hodgeTypeShimuraVariant := rfl

/--
Minimal arithmetic input for a Hodge-type Shida-variety statement.

The quaternion algebra is included as a checked mathlib object.  The Hodge-type
condition, level data, and PEL/moduli interpretation remain propositions until a
future formalization chooses concrete definitions or imports a pinned upstream
model.
-/
structure ShidaDatum where
  K : Type u
  instField_K : Field K
  instNumberField_K : NumberField K
  a : K
  b : K
  c : K
  ReflexField : Type u
  instField_ReflexField : Field ReflexField
  instNumberField_ReflexField : NumberField ReflexField
  isHodgeTypeDatum : Prop
  hasShidaLevelStructure : Prop
  hasPELModuliInterpretation : Prop

attribute [instance] ShidaDatum.instField_K
attribute [instance] ShidaDatum.instNumberField_K
attribute [instance] ShidaDatum.instField_ReflexField
attribute [instance] ShidaDatum.instNumberField_ReflexField

namespace ShidaDatum

/-- The quaternion algebra supplied by mathlib for the arithmetic datum. -/
abbrev quaternionAlgebra (D : ShidaDatum.{u}) : Type u :=
  QuaternionAlgebra D.K D.a D.b D.c

/-- The affine base scheme attached to the reflex field. -/
abbrev baseScheme (D : ShidaDatum.{u}) : Scheme.{u} :=
  Scheme.Spec.obj (op <| CommRingCat.of D.ReflexField)

/-- Checked mathlib anchor: the standard four-element quaternion basis. -/
def quaternionBasis (D : ShidaDatum.{u}) : Module.Basis (Fin 4) D.K D.quaternionAlgebra :=
  QuaternionAlgebra.basisOneIJK D.a D.b D.c

/-- Checked mathlib anchor: the number-field adele ring of the reflex field. -/
abbrev reflexAdeles (D : ShidaDatum.{u}) : Type u :=
  NumberField.AdeleRing (NumberField.RingOfIntegers D.ReflexField) D.ReflexField

/-- Checked mathlib anchor: the class group of the reflex field's ring of integers. -/
abbrev reflexClassGroup (D : ShidaDatum.{u}) : Type u :=
  ClassGroup (NumberField.RingOfIntegers D.ReflexField)

/--
Checked mathlib wrapper: the diagonal map from the reflex field into its adeles
is injective.  This is infrastructure only, not a Shida-variety construction.
-/
theorem reflexAdeles_algebraMap_injective (D : ShidaDatum.{u}) :
    Function.Injective (algebraMap D.ReflexField D.reflexAdeles) := by
  exact NumberField.AdeleRing.algebraMap_injective
    (NumberField.RingOfIntegers D.ReflexField) D.ReflexField

/-- Predicate boundary for later CM-reflex-field refinements. -/
def ReflexFieldIsCM (D : ShidaDatum.{u}) : Prop :=
  NumberField.IsCMField D.ReflexField

end ShidaDatum

/--
Stage1 P3 tensor package for a Hodge-type realization.

The carrier `V` is the representation space on which the selected tensors act.
This is a concrete checked structure, but it is intentionally not a theorem that
mathlib already has Hodge cycles for Shida/Shimura varieties.
-/
structure HodgeTensorPackage (V : Type u) : Type (u + 1) where
  Tensor : Type u
  actionOnRealization : Tensor → V → V
  hodgeCycle : Tensor → Prop
  definingTensorSet : Set Tensor
  definingTensors_are_hodgeCycles :
    ∀ t : Tensor, t ∈ definingTensorSet → hodgeCycle t
  tensorsCutOutHodgeGroup : Prop

namespace HodgeTensorPackage

/-- Membership in the selected defining tensor set implies the Hodge-cycle predicate. -/
theorem hodgeCycle_of_mem_definingTensorSet {V : Type u}
    (T : HodgeTensorPackage V) {t : T.Tensor} (ht : t ∈ T.definingTensorSet) :
    T.hodgeCycle t :=
  T.definingTensors_are_hodgeCycles t ht

end HodgeTensorPackage

/--
Stage1 P3 Hodge embedding datum.

The source and target groups are kept as concrete carriers with an injective map
and a tensor package on the target.  Replacing these carriers by a future
Shimura-datum/Siegel-moduli API is a downstream formalization leaf, not a fact
proved here.
-/
structure HodgeEmbeddingData : Type (u + 1) where
  ShimuraGroup : Type u
  SiegelGroup : Type u
  embedding : ShimuraGroup → SiegelGroup
  embedding_injective : Function.Injective embedding
  targetTensors : HodgeTensorPackage SiegelGroup
  imageStabilizesTargetTensors : Prop
  imageIsCutOutByTargetTensors : Prop

namespace HodgeEmbeddingData

/-- The checked embedding map for the P3 Hodge embedding boundary. -/
abbrev toFun (E : HodgeEmbeddingData.{u}) : E.ShimuraGroup → E.SiegelGroup :=
  E.embedding

/-- Projection wrapper for the injectivity condition of the Hodge embedding. -/
theorem injective (E : HodgeEmbeddingData.{u}) : Function.Injective E.toFun :=
  E.embedding_injective

end HodgeEmbeddingData

/--
Stage1 P3 reflex-field datum for the Hodge-type structure.

The current `ShidaDatum` already contains a reflex-field carrier.  This record
pins the stronger P3 boundary: a checked number-field carrier, an equivalence
with the existing datum field, and the two reflex-field obligations that future
formalization must discharge.
-/
structure ReflexFieldDatum (D : ShidaDatum.{u}) : Type (u + 1) where
  Carrier : Type u
  instField_Carrier : Field Carrier
  instNumberField_Carrier : NumberField Carrier
  identifiesWithDatumReflexField : Carrier ≃ D.ReflexField
  isFieldOfDefinitionForHodgeCocharacter : Prop
  definesHodgeTensorsAndLevel : Prop

attribute [instance] ReflexFieldDatum.instField_Carrier
attribute [instance] ReflexFieldDatum.instNumberField_Carrier

namespace ReflexFieldDatum

/-- The number-field adele ring attached to the pinned P3 reflex-field carrier. -/
abbrev adeles {D : ShidaDatum.{u}} (R : ReflexFieldDatum D) : Type u :=
  NumberField.AdeleRing (NumberField.RingOfIntegers R.Carrier) R.Carrier

/-- The class group attached to the pinned P3 reflex-field carrier. -/
abbrev classGroup {D : ShidaDatum.{u}} (R : ReflexFieldDatum D) : Type u :=
  ClassGroup (NumberField.RingOfIntegers R.Carrier)

/-- Checked wrapper: the P3 reflex-field carrier maps injectively to its adeles. -/
theorem adeles_algebraMap_injective {D : ShidaDatum.{u}} (R : ReflexFieldDatum D) :
    Function.Injective (algebraMap R.Carrier R.adeles) := by
  exact NumberField.AdeleRing.algebraMap_injective
    (NumberField.RingOfIntegers R.Carrier) R.Carrier

end ReflexFieldDatum

/--
Stage1 P3 level-structure datum attached to the Hodge embedding.

This structure records the level subgroup carrier, its map into the Hodge-type
source group, and the compact-open/neat/tensor-compatibility obligations.  The
topological compact-open API for the actual adelic group is not constructed in
this file.
-/
structure LevelStructureDatum (E : HodgeEmbeddingData.{u}) : Type (u + 1) where
  LevelSubgroup : Type u
  inclusionToShimuraGroup : LevelSubgroup → E.ShimuraGroup
  inclusion_injective : Function.Injective inclusionToShimuraGroup
  compactOpenCondition : Prop
  neatCondition : Prop
  compatibleWithHodgeTensors : Prop
  integralModelLevelCondition : Prop

namespace LevelStructureDatum

/-- Projection wrapper for the injectivity condition of the level inclusion. -/
theorem injective {E : HodgeEmbeddingData.{u}} (K : LevelStructureDatum E) :
    Function.Injective K.inclusionToShimuraGroup :=
  K.inclusion_injective

end LevelStructureDatum

/--
Concrete Stage1 P3 Hodge-type datum bundle.

This is the strongest repo-local P3 progress available without importing a
terminal Hodge-type Shimura-variety library: the datum has actual Lean carriers
for the representation, Hodge embedding, tensors, reflex field, and level
structure, and it implies the older proposition-valued `D.isHodgeTypeDatum`
boundary used by `StatementShape`.
-/
structure HodgeTypeDatum (D : ShidaDatum.{u}) : Type (u + 1) where
  RationalRepresentation : Type u
  hodgeCocharacterCarrier : Type u
  hodgeCocharacter : hodgeCocharacterCarrier → RationalRepresentation
  hodgeEmbedding : HodgeEmbeddingData.{u}
  tensors : HodgeTensorPackage RationalRepresentation
  reflexField : ReflexFieldDatum D
  levelStructure : LevelStructureDatum hodgeEmbedding
  hodgeAxioms : Prop
  realizesLegacyHodgeTypePredicate : D.isHodgeTypeDatum

namespace HodgeTypeDatum

/-- A datum with a concrete P3 Hodge-type bundle satisfies the legacy predicate. -/
theorem legacyPredicate {D : ShidaDatum.{u}} (H : HodgeTypeDatum D) :
    D.isHodgeTypeDatum :=
  H.realizesLegacyHodgeTypePredicate

/-- The Hodge embedding exposed by the concrete P3 bundle. -/
abbrev embedding {D : ShidaDatum.{u}} (H : HodgeTypeDatum D) : H.hodgeEmbedding.ShimuraGroup →
    H.hodgeEmbedding.SiegelGroup :=
  H.hodgeEmbedding.embedding

/-- The level subgroup carrier exposed by the concrete P3 bundle. -/
abbrev LevelSubgroup {D : ShidaDatum.{u}} (H : HodgeTypeDatum D) : Type u :=
  H.levelStructure.LevelSubgroup

end HodgeTypeDatum

/-- Proposition boundary saying that `D` has a concrete Stage1 P3 Hodge-type datum. -/
def HasConcreteHodgeTypeDatum (D : ShidaDatum.{u}) : Prop :=
  Nonempty (HodgeTypeDatum D)

/--
Checked bridge from the concrete P3 structure boundary back to the existing
statement-shape predicate.
-/
theorem hasConcreteHodgeTypeDatum_isHodgeTypeDatum {D : ShidaDatum.{u}}
    (h : HasConcreteHodgeTypeDatum D) : D.isHodgeTypeDatum :=
  h.elim HodgeTypeDatum.legacyPredicate

/-- One M0387-style leaf row for the future concrete Hodge-type datum split. -/
structure HodgeTypeDatumLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  currentRepoAnchor : String
  downstreamOutputs : List String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
  deriving Repr, DecidableEq

/--
Integration-ready P3 theorem-tree split.

Every row remains `unchecked` for theorem-completion purposes.  The structures
above are checked API boundaries; they do not construct a Hodge-type Shimura
variety or prove the selected tensors, reflex field, and level data satisfy the
full mathematical package.
-/
def hodgeTypeDatumLeaves : List HodgeTypeDatumLeaf := [
  {
    packageId := "SHIDA-P3-L01",
    leafLedgerId := "SHIDA-P3-hodge-datum",
    title := "Hodge-type datum bundle",
    localDuty :=
      "replace the legacy proposition-valued Hodge predicate with a concrete datum carrying the representation, cocharacter, embedding, tensor package, reflex field, and level structure",
    currentRepoAnchor := "HodgeTypeDatum; HasConcreteHodgeTypeDatum; hasConcreteHodgeTypeDatum_isHodgeTypeDatum",
    downstreamOutputs := [ "StatementShape Hodge-type hypothesis", "geometric construction input" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "the selected Hodge-type datum validates with concrete Shimura-datum semantics, not only Stage1 carriers"
  },
  {
    packageId := "SHIDA-P3-L02",
    leafLedgerId := "SHIDA-P3-hodge-embedding",
    title := "Hodge embedding",
    localDuty :=
      "instantiate the injective Hodge embedding into the selected Siegel target and prove the image is the tensor stabilizer required by Hodge type",
    currentRepoAnchor := "HodgeEmbeddingData; HodgeEmbeddingData.injective",
    downstreamOutputs := [ "HodgeTypeDatum.hodgeEmbedding", "tensor-stabilizer branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "embedding and tensor-stabilizer statement validate against concrete group/scheme APIs"
  },
  {
    packageId := "SHIDA-P3-L03",
    leafLedgerId := "SHIDA-P3-tensors-cycles",
    title := "tensors and Hodge cycles",
    localDuty :=
      "define the selected tensors, prove the defining tensor set consists of Hodge cycles, and connect those tensors to the Hodge group",
    currentRepoAnchor := "HodgeTensorPackage; HodgeTensorPackage.hodgeCycle_of_mem_definingTensorSet",
    downstreamOutputs := [ "HodgeTypeDatum.tensors", "HodgeEmbeddingData.targetTensors" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "all selected tensor/Hodge-cycle leaves validate with concrete realization APIs"
  },
  {
    packageId := "SHIDA-P3-L04",
    leafLedgerId := "SHIDA-P3-reflex-field",
    title := "reflex field",
    localDuty :=
      "pin the reflex field as a number field, identify it with the datum field, and prove the field-of-definition obligations for cocharacters, tensors, and level",
    currentRepoAnchor := "ReflexFieldDatum; ReflexFieldDatum.adeles; ReflexFieldDatum.adeles_algebraMap_injective",
    downstreamOutputs := [ "HodgeTypeDatum.reflexField", "baseScheme and canonical-model branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "reflex-field universal property and field-of-definition obligations validate repo-locally"
  },
  {
    packageId := "SHIDA-P3-L05",
    leafLedgerId := "SHIDA-P3-level-structure",
    title := "level structure",
    localDuty :=
      "define the level subgroup, inject it into the source group, and prove compact-open, neatness, tensor-compatibility, and integral-model level conditions",
    currentRepoAnchor := "LevelStructureDatum; LevelStructureDatum.injective",
    downstreamOutputs := [ "HodgeTypeDatum.levelStructure", "moduli and integral-model branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "level structure validates against concrete adelic/topological group APIs"
  }
]

/-- The P3 Hodge-type datum split has the requested five rows. -/
theorem hodgeTypeDatumLeaves_length : hodgeTypeDatumLeaves.length = 5 :=
  rfl

/-- All current P3 Hodge-type datum leaves remain unchecked for terminal theorem status. -/
theorem hodgeTypeDatumLeaves_statuses :
    hodgeTypeDatumLeaves.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each proposed P3 leaf ledger is budgeted at at most 100 local proof steps. -/
theorem hodgeTypeDatumLeaves_budgets :
    hodgeTypeDatumLeaves.map (fun row => row.localStepBudget) =
      [100, 100, 100, 100, 100] :=
  rfl

/--
Stage1 P4 abelian-scheme boundary over a base scheme.

Mathlib in the current dependency closure provides the scheme and morphism
infrastructure used here, but not a terminal abelian-scheme API.  The group-law
and fiber conditions are therefore explicit obligations carried by this record.
-/
structure AbelianSchemeData (S : Scheme.{u}) : Type (u + 1) where
  totalSpace : Scheme.{u}
  structuralMap : totalSpace ⟶ S
  zeroSection : S ⟶ totalSpace
  negation : totalSpace ⟶ totalSpace
  additionLaw : Prop
  groupSchemeAxioms : Prop
  properMap : IsProper structuralMap
  smoothMap : Smooth structuralMap
  geometricallyConnectedFibers : Prop
  relativeDimension : Nat

namespace AbelianSchemeData

/-- Projection wrapper for the properness component of a Stage1 abelian scheme. -/
theorem proper {S : Scheme.{u}} (A : AbelianSchemeData S) : IsProper A.structuralMap :=
  A.properMap

/-- Projection wrapper for the smoothness component of a Stage1 abelian scheme. -/
theorem smooth {S : Scheme.{u}} (A : AbelianSchemeData S) : Smooth A.structuralMap :=
  A.smoothMap

end AbelianSchemeData

/-- The base scheme of an abelian variety over a field. -/
abbrev abelianVarietyBaseScheme (k : Type u) [Field k] : Scheme.{u} :=
  Scheme.Spec.obj (op <| CommRingCat.of k)

/--
Stage1 P4 abelian-variety boundary over a field.

This pins the expected specialization of an abelian scheme to `Spec k` while
leaving projectivity/geometric-integrality style obligations explicit.
-/
structure AbelianVarietyData (k : Type u) [Field k] : Type (u + 1) where
  toAbelianScheme : AbelianSchemeData (abelianVarietyBaseScheme k)
  projectiveModel : Prop
  geometricallyIntegral : Prop
  completeGroupVariety : Prop
  positiveDimension : Prop

namespace AbelianVarietyData

/-- The structural morphism of the abelian scheme underlying an abelian variety. -/
abbrev structuralMap {k : Type u} [Field k] (A : AbelianVarietyData k) :
    A.toAbelianScheme.totalSpace ⟶ abelianVarietyBaseScheme k :=
  A.toAbelianScheme.structuralMap

end AbelianVarietyData

/--
Stage1 P4 polarization boundary for an abelian scheme.

The dual abelian scheme and morphism-to-dual are concrete carriers; ampleness,
symmetry, finite-kernel, and principal-polarization conditions remain explicit
formalization obligations.
-/
structure PolarizationData {S : Scheme.{u}} (A : AbelianSchemeData S) : Type (u + 1) where
  dualAbelianScheme : AbelianSchemeData S
  morphismToDual : A.totalSpace ⟶ dualAbelianScheme.totalSpace
  compatibleWithBase : morphismToDual ≫ dualAbelianScheme.structuralMap = A.structuralMap
  finiteKernel : Prop
  ampleLineBundle : Prop
  symmetric : Prop
  principal : Prop
  degree : Nat

namespace PolarizationData

/-- Projection wrapper for the base-compatibility of a Stage1 polarization. -/
theorem base_compatible {S : Scheme.{u}} {A : AbelianSchemeData S} (pol : PolarizationData A) :
    pol.morphismToDual ≫ pol.dualAbelianScheme.structuralMap = A.structuralMap :=
  pol.compatibleWithBase

end PolarizationData

/--
Stage1 P4 endomorphism-action boundary for an abelian scheme.

The carrier is a checked ring, and every endomorphism is a scheme endomorphism
over the base.  Additive/multiplicative compatibility and Rosati compatibility
are retained as explicit obligations for a future concrete PEL API.
-/
structure EndomorphismAction {S : Scheme.{u}} (A : AbelianSchemeData S) : Type (u + 1) where
  EndCarrier : Type u
  instRing_EndCarrier : Ring EndCarrier
  toEndomorphism : EndCarrier → (A.totalSpace ⟶ A.totalSpace)
  preservesStructureMap : ∀ r : EndCarrier, toEndomorphism r ≫ A.structuralMap = A.structuralMap
  respectsZero : Prop
  respectsOne : Prop
  respectsAdd : Prop
  respectsMul : Prop
  compatibleWithRosati : Prop

attribute [instance] EndomorphismAction.instRing_EndCarrier

namespace EndomorphismAction

/-- Projection wrapper: each selected endomorphism lies over the same base. -/
theorem over_base {S : Scheme.{u}} {A : AbelianSchemeData S} (endo : EndomorphismAction A)
    (r : endo.EndCarrier) :
    endo.toEndomorphism r ≫ A.structuralMap = A.structuralMap :=
  endo.preservesStructureMap r

end EndomorphismAction

/--
Stage1 P4 abelian-scheme level-structure boundary.

This is separate from the P3 Hodge-type level subgroup.  It is the moduli-side
level data on torsion/Tate-module realizations of the universal abelian scheme,
with compatibility obligations for the polarization and endomorphism action.
-/
structure AbelianLevelStructureData {S : Scheme.{u}} (A : AbelianSchemeData S)
    (pol : PolarizationData A) (endo : EndomorphismAction A) : Type (u + 1) where
  LevelIndex : Type u
  TorsionCarrier : Type u
  trivialization : LevelIndex → TorsionCarrier → TorsionCarrier
  faithfulTrivialization : Prop
  finiteLevel : Prop
  primeToResidueCharacteristics : Prop
  symplecticForPolarization : Prop
  endomorphismEquivariant : Prop
  fineModuliCondition : Prop

namespace AbelianLevelStructureData

/-- The selected torsion/Tate-module carrier exposed by the P4 level structure. -/
abbrev carrier {S : Scheme.{u}} {A : AbelianSchemeData S} {pol : PolarizationData A}
    {endo : EndomorphismAction A} (level : AbelianLevelStructureData A pol endo) : Type u :=
  level.TorsionCarrier

end AbelianLevelStructureData

/--
Stage1 P4 moduli-problem package over the candidate representing scheme.

The universal abelian scheme, polarization, endomorphism action, and level
structure are concrete dependent fields.  Representability and PEL/Shimura
compatibility remain obligations, and the last field bridges back to the legacy
`D.hasPELModuliInterpretation` predicate used by `StatementShape`.
-/
structure ShidaModuliProblemData (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Type (u + 1) where
  universalAbelianScheme : AbelianSchemeData X
  polarization : PolarizationData universalAbelianScheme
  endomorphismAction : EndomorphismAction universalAbelianScheme
  levelStructure :
    AbelianLevelStructureData universalAbelianScheme polarization endomorphismAction
  moduliFunctor : Scheme.{u} → Type u
  universalFamilyRepresentsFunctor : Prop
  compatibleWithBaseMap : Prop
  satisfiesPELConditions : Prop
  satisfiesHodgeTypeConditions : Prop
  realizesLegacyPELModuliPredicate : D.hasPELModuliInterpretation

namespace ShidaModuliProblemData

/-- A concrete P4 moduli package implies the legacy PEL/moduli predicate. -/
theorem legacyPredicate {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (M : ShidaModuliProblemData D X π) : D.hasPELModuliInterpretation :=
  M.realizesLegacyPELModuliPredicate

/-- The universal abelian scheme over the representing candidate. -/
abbrev universalFamily {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (M : ShidaModuliProblemData D X π) : AbelianSchemeData X :=
  M.universalAbelianScheme

end ShidaModuliProblemData

/-- Proposition boundary saying that `X` carries a concrete P4 abelian moduli package. -/
def RepresentsShidaModuliViaAbelianData (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  Nonempty (ShidaModuliProblemData D X π)

/--
Checked bridge from a concrete P4 abelian moduli package back to the existing
statement-shape predicate.
-/
theorem representsShidaModuliViaAbelianData_hasPEL {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : RepresentsShidaModuliViaAbelianData D X π) :
    D.hasPELModuliInterpretation :=
  h.elim (fun M => ShidaModuliProblemData.legacyPredicate M)

/-- One M0387-style leaf row for the future concrete P4 moduli-problem split. -/
structure ModuliProblemLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  currentRepoAnchor : String
  downstreamOutputs : List String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
  deriving Repr, DecidableEq

/--
Integration-ready P4 theorem-tree split.

The rows are unchecked for theorem-completion purposes.  The records above are
checked API boundaries; they do not prove the abelian moduli problem is
represented by a Shida/Hodge-type Shimura variety.
-/
def moduliProblemLeaves : List ModuliProblemLeaf := [
  {
    packageId := "SHIDA-P4-L01",
    leafLedgerId := "SHIDA-P4-abelian-scheme-variety",
    title := "abelian scheme and abelian variety API",
    localDuty :=
      "replace the abstract moduli carrier with concrete abelian-scheme and abelian-variety records over schemes and fields",
    currentRepoAnchor := "AbelianSchemeData; AbelianVarietyData; AbelianSchemeData.proper; AbelianSchemeData.smooth",
    downstreamOutputs := [ "universal family", "geometric construction branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "group-scheme laws and fiber conditions validate against a concrete abelian-scheme API"
  },
  {
    packageId := "SHIDA-P4-L02",
    leafLedgerId := "SHIDA-P4-polarization",
    title := "polarization API",
    localDuty :=
      "define the dual abelian scheme and polarization morphism, then prove base compatibility, ampleness, symmetry, finite-kernel, and principal-polarization conditions",
    currentRepoAnchor := "PolarizationData; PolarizationData.base_compatible",
    downstreamOutputs := [ "PEL moduli branch", "Rosati compatibility branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "polarization obligations validate over the chosen universal abelian scheme"
  },
  {
    packageId := "SHIDA-P4-L03",
    leafLedgerId := "SHIDA-P4-endomorphisms",
    title := "endomorphism action API",
    localDuty :=
      "define the selected endomorphism ring action on the universal abelian scheme and prove it is over the base and compatible with the polarization/Rosati involution",
    currentRepoAnchor := "EndomorphismAction; EndomorphismAction.over_base",
    downstreamOutputs := [ "PEL moduli branch", "Shimura datum compatibility" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "endomorphism action validates as a concrete ring action on the abelian scheme"
  },
  {
    packageId := "SHIDA-P4-L04",
    leafLedgerId := "SHIDA-P4-level-structure",
    title := "moduli level structure API",
    localDuty :=
      "define the torsion/Tate-module level structure and prove faithfulness, finiteness, prime-to-characteristic, symplectic, and endomorphism-equivariant conditions",
    currentRepoAnchor := "AbelianLevelStructureData; AbelianLevelStructureData.carrier",
    downstreamOutputs := [ "fine moduli condition", "comparison with P3 level data" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "level structure validates against concrete torsion or Tate-module APIs"
  },
  {
    packageId := "SHIDA-P4-L05",
    leafLedgerId := "SHIDA-P4-representability",
    title := "abelian PEL moduli representability",
    localDuty :=
      "state the moduli functor, attach the universal abelian scheme with polarization, endomorphisms, and level data, and prove the candidate scheme represents it",
    currentRepoAnchor := "ShidaModuliProblemData; RepresentsShidaModuliViaAbelianData; representsShidaModuliViaAbelianData_hasPEL",
    downstreamOutputs := [ "StatementShape RepresentsShidaModuli predicate", "geometric and canonical-model branches" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "representability of the abelian PEL/Hodge-type moduli problem validates repo-locally"
  }
]

/-- The P4 moduli-problem split has the requested five rows. -/
theorem moduliProblemLeaves_length : moduliProblemLeaves.length = 5 :=
  rfl

/-- All current P4 moduli-problem leaves remain unchecked for terminal theorem status. -/
theorem moduliProblemLeaves_statuses :
    moduliProblemLeaves.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each proposed P4 leaf ledger is budgeted at at most 100 local proof steps. -/
theorem moduliProblemLeaves_budgets :
    moduliProblemLeaves.map (fun row => row.localStepBudget) =
      [100, 100, 100, 100, 100] :=
  rfl

/--
Scheme-theoretic properties expected from a constructed Shida-variety model.
The moduli and canonical-model properties are deliberately separate from these
basic geometric predicates.
-/
def GeometricModelPackage (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  IsProper π ∧ Smooth π ∧ IsLocallyNoetherian X

/--
Stage1 P5 construction-data boundary for a candidate geometric model.

This record is intentionally indexed by an already selected scheme `X` and
structural morphism `π : X ⟶ D.baseScheme`.  It proves the selected geometric
properties once such a candidate and its construction data are supplied, but it
does not assert that the Hodge-type Shimura/Shida construction has been carried
out for every datum.
-/
structure GeometricConstructionData (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Type (u + 1) where
  geometricPackage : GeometricModelPackage D X π
  moduliPackage : RepresentsShidaModuliViaAbelianData D X π
  hodgeTypeRealization : Prop
  hodgeTypeRealizationProof : hodgeTypeRealization
  constructedOverReflexField : Prop
  constructedOverReflexFieldProof : constructedOverReflexField

namespace GeometricConstructionData

/-- Properness of the structural map follows from the P5 geometric package. -/
theorem proper {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (G : GeometricConstructionData D X π) : IsProper π :=
  G.geometricPackage.1

/-- Smoothness of the structural map follows from the P5 geometric package. -/
theorem smooth {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (G : GeometricConstructionData D X π) : Smooth π :=
  G.geometricPackage.2.1

/-- Local noetherianity of the model follows from the P5 geometric package. -/
theorem locallyNoetherian {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (G : GeometricConstructionData D X π) : IsLocallyNoetherian X :=
  G.geometricPackage.2.2

/-- The construction data includes the P4 abelian moduli package. -/
theorem representsModuli {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (G : GeometricConstructionData D X π) : RepresentsShidaModuliViaAbelianData D X π :=
  G.moduliPackage

end GeometricConstructionData

/-- Proposition boundary saying that `X` has the checked Stage1 P5 construction data. -/
def HasGeometricConstructionData (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  Nonempty (GeometricConstructionData D X π)

/-- A bundled candidate model over the reflex-field base scheme. -/
structure GeometricModelOverReflexField (D : ShidaDatum.{u}) : Type (u + 1) where
  model : Scheme.{u}
  projection : model ⟶ D.baseScheme
  constructionData : GeometricConstructionData D model projection

namespace GeometricModelOverReflexField

/-- The bundled model is proper over the reflex-field base. -/
theorem proper {D : ShidaDatum.{u}} (G : GeometricModelOverReflexField D) :
    IsProper G.projection :=
  G.constructionData.proper

/-- The bundled model is smooth over the reflex-field base. -/
theorem smooth {D : ShidaDatum.{u}} (G : GeometricModelOverReflexField D) :
    Smooth G.projection :=
  G.constructionData.smooth

/-- The bundled model is locally noetherian. -/
theorem locallyNoetherian {D : ShidaDatum.{u}} (G : GeometricModelOverReflexField D) :
    IsLocallyNoetherian G.model :=
  G.constructionData.locallyNoetherian

/-- The bundled model carries the P4 abelian moduli package. -/
theorem representsModuli {D : ShidaDatum.{u}} (G : GeometricModelOverReflexField D) :
    RepresentsShidaModuliViaAbelianData D G.model G.projection :=
  G.constructionData.representsModuli

end GeometricModelOverReflexField

/-- One M0387-style leaf row for the future concrete P5 geometric construction split. -/
structure GeometricConstructionLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  currentRepoAnchor : String
  downstreamOutputs : List String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
  deriving Repr, DecidableEq

/--
Integration-ready P5 theorem-tree split.

The rows remain `unchecked` for theorem-completion purposes.  The P5 records and
projection lemmas above are checked repo-local Lean boundaries; they are not a
terminal construction of Hodge-type Shimura/Shida varieties over the reflex
field.
-/
def geometricConstructionLeaves : List GeometricConstructionLeaf := [
  {
    packageId := "SHIDA-P5-L01",
    leafLedgerId := "SHIDA-P5-candidate-model",
    title := "candidate scheme/model",
    localDuty :=
      "construct the candidate scheme carrying the Hodge-type Shida/Shimura moduli interpretation over the reflex-field base",
    currentRepoAnchor := "GeometricModelOverReflexField.model; GeometricModelOverReflexField.projection",
    downstreamOutputs := [ "StatementShape existence witness", "canonical-model branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "a concrete construction supplies `GeometricModelOverReflexField D` for each datum satisfying the hypotheses"
  },
  {
    packageId := "SHIDA-P5-L02",
    leafLedgerId := "SHIDA-P5-reflex-field-structural-map",
    title := "structural morphism over the reflex field",
    localDuty :=
      "identify the base as `Spec` of the reflex field and prove the constructed model's structural morphism is over that base",
    currentRepoAnchor := "ShidaDatum.baseScheme; GeometricModelOverReflexField.projection",
    downstreamOutputs := [ "proper/smooth property branch", "descent and canonical-model branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "the reflex-field base and structural morphism are produced by the concrete construction, not only indexed as fields"
  },
  {
    packageId := "SHIDA-P5-L03",
    leafLedgerId := "SHIDA-P5-geometric-properties",
    title := "proper smooth locally noetherian properties",
    localDuty :=
      "prove the selected scheme-theoretic properties of the constructed model over the reflex-field base",
    currentRepoAnchor := "GeometricConstructionData.proper; GeometricConstructionData.smooth; GeometricConstructionData.locallyNoetherian",
    downstreamOutputs := [ "GeometricModelPackage", "StatementShape geometric conjunct" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "properness, smoothness, and local noetherianity validate for the actually constructed morphism"
  },
  {
    packageId := "SHIDA-P5-L04",
    leafLedgerId := "SHIDA-P5-moduli-compatibility",
    title := "moduli and Hodge-realization compatibility",
    localDuty :=
      "connect the geometric model to the P4 abelian moduli package and the P3 Hodge-type realization",
    currentRepoAnchor := "GeometricConstructionData.representsModuli; GeometricConstructionData.hodgeTypeRealizationProof",
    downstreamOutputs := [ "StatementShape moduli conjunct", "StatementShape Hodge-realization conjunct" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "the constructed model represents the selected moduli problem and realizes the selected Hodge tensors"
  },
  {
    packageId := "SHIDA-P5-L05",
    leafLedgerId := "SHIDA-P5-construction-existence",
    title := "existence under the normalized hypotheses",
    localDuty :=
      "derive the model-existence witness from `isHodgeTypeDatum`, level structure, and PEL/moduli hypotheses",
    currentRepoAnchor := "HasGeometricConstructionData; GeometricModelOverReflexField",
    downstreamOutputs := [ "StatementShape existential witness", "P6 canonical-model/descent input" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "for every normalized datum satisfying the hypotheses, repo-local Lean constructs the model and all P5 properties"
  }
]

/-- The P5 geometric-construction split has the requested five rows. -/
theorem geometricConstructionLeaves_length : geometricConstructionLeaves.length = 5 :=
  rfl

/-- All current P5 geometric-construction leaves remain unchecked for terminal theorem status. -/
theorem geometricConstructionLeaves_statuses :
    geometricConstructionLeaves.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each proposed P5 leaf ledger is budgeted at at most 100 local proof steps. -/
theorem geometricConstructionLeaves_budgets :
    geometricConstructionLeaves.map (fun row => row.localStepBudget) =
      [100, 100, 100, 100, 100] :=
  rfl

/--
Stage1 P6 descent datum for a candidate model over the reflex-field base.

The cover and pullback model are concrete scheme carriers.  The descent cocycle,
effectivity, and reflex-field descent theorem remain explicit obligations until
a concrete Shimura-variety canonical-model API is imported or formalized.
-/
structure ReflexFieldDescentDatum (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Type (u + 1) where
  descentCover : Scheme.{u}
  coverMap : descentCover ⟶ D.baseScheme
  pulledBackModel : Scheme.{u}
  pullbackProjection : pulledBackModel ⟶ descentCover
  descentCocycleCondition : Prop
  descentCocycleConditionProof : descentCocycleCondition
  effectiveDescent : Prop
  effectiveDescentProof : effectiveDescent
  descendsToReflexField : Prop
  descendsToReflexFieldProof : descendsToReflexField
  compatibleWithEtaleTopology : Prop
  compatibleWithEtaleTopologyProof : compatibleWithEtaleTopology

namespace ReflexFieldDescentDatum

/-- Projection wrapper for the P6 descent cocycle condition. -/
theorem cocycle {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (R : ReflexFieldDescentDatum D X π) : R.descentCocycleCondition :=
  R.descentCocycleConditionProof

/-- Projection wrapper for effective descent of the P6 candidate model. -/
theorem effective {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (R : ReflexFieldDescentDatum D X π) : R.effectiveDescent :=
  R.effectiveDescentProof

/-- Projection wrapper for descent to the reflex field. -/
theorem descends {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (R : ReflexFieldDescentDatum D X π) : R.descendsToReflexField :=
  R.descendsToReflexFieldProof

/-- Projection wrapper for compatibility with the etale topology. -/
theorem etaleCompatible {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (R : ReflexFieldDescentDatum D X π) : R.compatibleWithEtaleTopology :=
  R.compatibleWithEtaleTopologyProof

end ReflexFieldDescentDatum

/--
Stage1 P6 canonical-model and compatibility boundary.

This record packages the canonical-model property together with descent and the
compatibilities expected of a Hodge-type Shimura/Shida canonical model.  It is
indexed by a candidate model and its structural morphism; it does not construct
that model or prove the terminal canonical-model theorem for all data.
-/
structure CanonicalModelDescentData (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Type (u + 1) where
  geometricConstruction : GeometricConstructionData D X π
  descentDatum : ReflexFieldDescentDatum D X π
  canonicalModelProperty : Prop
  canonicalModelPropertyProof : canonicalModelProperty
  reflexFieldIsFieldOfDefinition : Prop
  reflexFieldIsFieldOfDefinitionProof : reflexFieldIsFieldOfDefinition
  compatibleWithBaseChange : Prop
  compatibleWithBaseChangeProof : compatibleWithBaseChange
  compatibleWithModuliInterpretation : Prop
  compatibleWithModuliInterpretationProof : compatibleWithModuliInterpretation
  compatibleWithHodgeRealization : Prop
  compatibleWithHodgeRealizationProof : compatibleWithHodgeRealization
  compatibleWithHeckeCorrespondences : Prop
  compatibleWithHeckeCorrespondencesProof : compatibleWithHeckeCorrespondences

namespace CanonicalModelDescentData

/-- The P6 package includes the P5 geometric construction data. -/
theorem hasGeometricConstruction {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (C : CanonicalModelDescentData D X π) :
    HasGeometricConstructionData D X π :=
  ⟨C.geometricConstruction⟩

/-- Projection wrapper for the canonical-model property. -/
theorem canonical {D : ShidaDatum.{u}} {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (C : CanonicalModelDescentData D X π) : C.canonicalModelProperty :=
  C.canonicalModelPropertyProof

/-- Projection wrapper for the reflex field as a field of definition. -/
theorem reflexFieldDefinition {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (C : CanonicalModelDescentData D X π) :
    C.reflexFieldIsFieldOfDefinition :=
  C.reflexFieldIsFieldOfDefinitionProof

/-- Projection wrapper for base-change compatibility. -/
theorem baseChangeCompatible {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (C : CanonicalModelDescentData D X π) :
    C.compatibleWithBaseChange :=
  C.compatibleWithBaseChangeProof

/-- Projection wrapper for compatibility with the abelian moduli interpretation. -/
theorem moduliCompatible {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (C : CanonicalModelDescentData D X π) :
    C.compatibleWithModuliInterpretation :=
  C.compatibleWithModuliInterpretationProof

/-- Projection wrapper for compatibility with the Hodge-type realization. -/
theorem hodgeCompatible {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (C : CanonicalModelDescentData D X π) :
    C.compatibleWithHodgeRealization :=
  C.compatibleWithHodgeRealizationProof

/-- Projection wrapper for compatibility with Hecke correspondences. -/
theorem heckeCompatible {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (C : CanonicalModelDescentData D X π) :
    C.compatibleWithHeckeCorrespondences :=
  C.compatibleWithHeckeCorrespondencesProof

end CanonicalModelDescentData

/-- Proposition boundary saying that `X` carries the checked Stage1 P6 package. -/
def HasCanonicalModelDescentData (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  Nonempty (CanonicalModelDescentData D X π)

/--
Predicate suitable for the `StatementShape` canonical-model slot when the P6
boundary is used as the concrete local witness.
-/
def HasCanonicalModelPropertyViaDescent (D : ShidaDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  HasCanonicalModelDescentData D X π

/-- Checked bridge from the P6 package boundary to the P5 construction boundary. -/
theorem hasCanonicalModelDescentData_hasGeometricConstruction {D : ShidaDatum.{u}}
    {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (h : HasCanonicalModelDescentData D X π) : HasGeometricConstructionData D X π :=
  h.elim (fun C => C.hasGeometricConstruction)

/--
Checked extraction of the canonical-model property recorded inside a P6 witness.

This is an extraction theorem from supplied data, not a construction theorem for
Hodge-type Shimura/Shida canonical models.
-/
theorem hasCanonicalModelDescentData_canonicalProperty {D : ShidaDatum.{u}}
    {X : Scheme.{u}} {π : X ⟶ D.baseScheme}
    (h : HasCanonicalModelDescentData D X π) :
    ∃ C : CanonicalModelDescentData D X π, C.canonicalModelProperty :=
  h.elim (fun C => ⟨C, C.canonical⟩)

/-- One M0387-style leaf row for the future concrete P6 canonical-model split. -/
structure CanonicalModelDescentLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  currentRepoAnchor : String
  downstreamOutputs : List String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
  deriving Repr, DecidableEq

/--
Integration-ready P6 theorem-tree split.

The rows remain `unchecked` for theorem-completion purposes.  The P6 records and
projection lemmas above are checked repo-local Lean boundaries; they do not
prove the terminal canonical-model or descent theorem.
-/
def canonicalModelDescentLeaves : List CanonicalModelDescentLeaf := [
  {
    packageId := "SHIDA-P6-L01",
    leafLedgerId := "SHIDA-P6-canonical-model-property",
    title := "canonical model property",
    localDuty :=
      "state the canonical-model property for the constructed Hodge-type Shida/Shimura model over the reflex field",
    currentRepoAnchor := "CanonicalModelDescentData; CanonicalModelDescentData.canonical",
    downstreamOutputs := [ "StatementShape canonical-model conjunct", "external audit comparison" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "the canonical-model property validates for the concrete constructed model, not only as a supplied field"
  },
  {
    packageId := "SHIDA-P6-L02",
    leafLedgerId := "SHIDA-P6-reflex-field-descent",
    title := "reflex-field descent",
    localDuty :=
      "construct the descent datum, prove the cocycle condition and effectivity, and identify the descended field as the reflex field",
    currentRepoAnchor := "ReflexFieldDescentDatum; ReflexFieldDescentDatum.cocycle; ReflexFieldDescentDatum.effective; ReflexFieldDescentDatum.descends",
    downstreamOutputs := [ "canonical model field-of-definition branch", "base-change branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "descent data and effectivity validate through concrete scheme/topology APIs"
  },
  {
    packageId := "SHIDA-P6-L03",
    leafLedgerId := "SHIDA-P6-base-change-compatibility",
    title := "base-change compatibility",
    localDuty :=
      "prove the canonical model is compatible with the expected base changes from the reflex field",
    currentRepoAnchor := "CanonicalModelDescentData.baseChangeCompatible",
    downstreamOutputs := [ "comparison with geometric construction", "canonical-model uniqueness branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "base-change compatibility validates for the actual morphisms and comparison maps"
  },
  {
    packageId := "SHIDA-P6-L04",
    leafLedgerId := "SHIDA-P6-moduli-hodge-compatibility",
    title := "moduli and Hodge compatibility",
    localDuty :=
      "prove the canonical model is compatible with the abelian moduli interpretation and Hodge-type realization",
    currentRepoAnchor := "CanonicalModelDescentData.moduliCompatible; CanonicalModelDescentData.hodgeCompatible",
    downstreamOutputs := [ "P4 moduli branch", "P3 Hodge tensor branch" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "compatibility validates against concrete P4 moduli and P3 Hodge-type data"
  },
  {
    packageId := "SHIDA-P6-L05",
    leafLedgerId := "SHIDA-P6-hecke-etale-compatibility",
    title := "Hecke and etale compatibility",
    localDuty :=
      "prove compatibility with Hecke correspondences and the etale descent topology used by the canonical-model construction",
    currentRepoAnchor := "CanonicalModelDescentData.heckeCompatible; ReflexFieldDescentDatum.etaleCompatible; etaleTopologyAnchor",
    downstreamOutputs := [ "canonical-model uniqueness branch", "external theorem matching" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "Hecke correspondence and etale descent compatibility validate through concrete local APIs or a pinned upstream proof"
  }
]

/-- The P6 canonical-model/descent split has the requested five rows. -/
theorem canonicalModelDescentLeaves_length : canonicalModelDescentLeaves.length = 5 :=
  rfl

/-- All current P6 canonical-model/descent leaves remain unchecked for terminal theorem status. -/
theorem canonicalModelDescentLeaves_statuses :
    canonicalModelDescentLeaves.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each proposed P6 leaf ledger is budgeted at at most 100 local proof steps. -/
theorem canonicalModelDescentLeaves_budgets :
    canonicalModelDescentLeaves.map (fun row => row.localStepBudget) =
      [100, 100, 100, 100, 100] :=
  rfl

/--
Stage1 normalized statement-shape candidate.

For each arithmetic datum with Hodge-type, level, and PEL/moduli hypotheses, a
terminal theorem would construct a scheme over the reflex field with geometric,
moduli, Hodge-realization, and canonical-model properties.  The three predicate
parameters mark the current formalization boundary.
-/
def StatementShape
    (RepresentsShidaModuli :
      (D : ShidaDatum.{u}) → (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop)
    (HasHodgeTypeRealization :
      (D : ShidaDatum.{u}) → (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop)
    (HasCanonicalModelProperty :
      (D : ShidaDatum.{u}) → (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop) :
    Prop :=
  ∀ D : ShidaDatum.{u},
    D.isHodgeTypeDatum →
    D.hasShidaLevelStructure →
    D.hasPELModuliInterpretation →
      ∃ X : Scheme.{u}, ∃ π : X ⟶ D.baseScheme,
        GeometricModelPackage D X π ∧
          RepresentsShidaModuli D X π ∧
          HasHodgeTypeRealization D X π ∧
          HasCanonicalModelProperty D X π

/-- Checked mathlib anchor: the big etale topology on schemes is available. -/
def etaleTopologyAnchor : GrothendieckTopology Scheme.{u} :=
  Scheme.etaleTopology

/-- Checked mathlib anchor: a normalized value-group witness for nonarchimedean local fields. -/
theorem nonarchimedeanLocalField_valueGroupAnchor
    (K : Type u) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Nonempty (ValueGroupWithZero K ≃*o ℤᵐ⁰) := by
  exact ⟨IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt K⟩

/-- Projection wrapper for the properness component of the geometric package. -/
theorem properProjectionAnchor {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricModelPackage D X π) : IsProper π :=
  h.1

/-- Projection wrapper for the smoothness component of the geometric package. -/
theorem smoothProjectionAnchor {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricModelPackage D X π) : Smooth π :=
  h.2.1

/-- Projection wrapper for the locally noetherian component of the geometric package. -/
theorem locallyNoetherianProjectionAnchor {D : ShidaDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricModelPackage D X π) : IsLocallyNoetherian X :=
  h.2.2

/--
One row in the Stage1 mathlib object-model anchor table.

Rows are documentation data inside the checked Lean artifact.  The actual object
names are also exercised by the typed wrappers above, but the table records the
public merge text at the pinned mathlib revision requested by `S1-M-066.P2`.
-/
structure MathlibAnchorRow where
  requestedName : String
  importModule : String
  pinnedRevision : String
  repoLocalEvidence : String
  completionBoundary : String
  deriving Repr

/-- Pinned mathlib revision used for the S1-M-066.P2 object-model audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Stage1 P2 mathlib object-model anchor table.

Every row is an upstream mathlib object available through the repo-local Lean
dependency closure and checked by this file's imports/wrappers.  None of these
rows is a terminal Shida/Hodge-type Shimura-variety construction theorem.
-/
def mathlibObjectModelAnchorTable : List MathlibAnchorRow := [
  {
    requestedName := "QuaternionAlgebra",
    importModule := "Mathlib.Algebra.Quaternion",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.quaternionAlgebra",
    completionBoundary := "object-model anchor only; no moduli construction"
  },
  {
    requestedName := "QuaternionAlgebra.basisOneIJK",
    importModule := "Mathlib.Algebra.QuaternionBasis",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.quaternionBasis",
    completionBoundary := "basis anchor only; no Hodge tensors or cycles"
  },
  {
    requestedName := "Scheme.Spec",
    importModule := "Mathlib.AlgebraicGeometry.Scheme",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.baseScheme",
    completionBoundary := "base-scheme anchor only; no integral/canonical model"
  },
  {
    requestedName := "IsProper",
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by GeometricModelPackage and properProjectionAnchor",
    completionBoundary := "predicate anchor only; no constructed proper morphism"
  },
  {
    requestedName := "Smooth",
    importModule := "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by GeometricModelPackage and smoothProjectionAnchor",
    completionBoundary := "predicate anchor only; no constructed smooth morphism"
  },
  {
    requestedName := "IsLocallyNoetherian",
    importModule := "Mathlib.AlgebraicGeometry.Noetherian",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by GeometricModelPackage and locallyNoetherianProjectionAnchor",
    completionBoundary := "predicate anchor only; no noetherian model proof"
  },
  {
    requestedName := "Scheme.etaleTopology",
    importModule := "Mathlib.AlgebraicGeometry.Sites.Etale",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by etaleTopologyAnchor",
    completionBoundary := "site anchor only; no descent/canonical-model theorem"
  },
  {
    requestedName := "NumberField",
    importModule := "Mathlib.NumberTheory.NumberField.Basic",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.instNumberField_K and ShidaDatum.instNumberField_ReflexField",
    completionBoundary := "field-class anchor only; no reflex-field construction"
  },
  {
    requestedName := "NumberField.IsCMField",
    importModule := "Mathlib.NumberTheory.NumberField.CMField",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.ReflexFieldIsCM",
    completionBoundary := "CM predicate anchor only; no proof the reflex field is CM"
  },
  {
    requestedName := "NumberField.AdeleRing",
    importModule := "Mathlib.NumberTheory.NumberField.AdeleRing",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.reflexAdeles and reflexAdeles_algebraMap_injective",
    completionBoundary := "adele-ring anchor only; no automorphic/canonical model argument"
  },
  {
    requestedName := "ClassGroup",
    importModule := "Mathlib.RingTheory.ClassGroup",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by ShidaDatum.reflexClassGroup",
    completionBoundary := "class-group anchor only; no class-field or moduli theorem"
  },
  {
    requestedName := "IsNonarchimedeanLocalField",
    importModule := "Mathlib.NumberTheory.LocalField.Basic",
    pinnedRevision := mathlibAnchorRevision,
    repoLocalEvidence := "typed by nonarchimedeanLocalField_valueGroupAnchor",
    completionBoundary := "local-field anchor only; no local-model or p-adic uniformization proof"
  }
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Quaternion",
  "Mathlib.Algebra.QuaternionBasis",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Noetherian",
  "Mathlib.AlgebraicGeometry.Sites.Etale",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.NumberField.CMField",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.RingTheory.ClassGroup"
]

/-- Search terms that did not locate a terminal Shida/Shimura-variety theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Shida",
  "Hida",
  "ShimuraVariety",
  "HodgeTypeShimura",
  "Shimura datum",
  "abelian variety",
  "PEL",
  "canonical model"
]

/-- One row in the S1-M-066.P7 external/named-project audit. -/
structure ExternalAuditSearchRow where
  searchTerm : String
  namedProjectScope : String
  namedProjectResult : String
  integrationGate : String
  deriving Repr, DecidableEq

/--
Status of the authenticated GitHub code-search branch of the P7 audit.

The local GitHub CLI session is not authenticated, and unauthenticated GitHub
REST code-search was unavailable in this environment.  The checked progress in
this file is therefore the named-project search over the repo-pinned Lean
dependencies, not an authenticated global code-search completion claim.
-/
def githubAuthenticatedCodeSearchStatus : String :=
  "not run: gh auth status reports no authenticated GitHub host; unauthenticated REST code-search was rate-limited"

/--
Named-project Lean 4 source audit for `S1-M-066.P7.external_audit`.

Scope checked on 2026-05-01: repo-pinned `mathlib` and `flt-regular` Lean
sources.  The only relevant hit among the requested terms was mathlib's
`Mathlib.AlgebraicGeometry.Group.Abelian` file heading for abelian varieties;
that file provides group-scheme infrastructure, not a Shida/Hodge-type
Shimura-variety construction theorem.  Hence no external proof is pinned,
imported, or checked here, and no completion state is claimed.
-/
def externalAuditSearchRows : List ExternalAuditSearchRow := [
  {
    searchTerm := "Shida",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact source hit for a terminal Shida-variety theorem",
    integrationGate := "no external proof candidate to pin/import/check"
  },
  {
    searchTerm := "Hida",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact source hit for a terminal Hida/Shida-variety theorem",
    integrationGate := "no external proof candidate to pin/import/check"
  },
  {
    searchTerm := "ShimuraVariety",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact declaration or module hit",
    integrationGate := "no external proof candidate to pin/import/check"
  },
  {
    searchTerm := "HodgeTypeShimura",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact declaration or module hit",
    integrationGate := "no external proof candidate to pin/import/check"
  },
  {
    searchTerm := "Shimura datum",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact source hit for a Shimura-datum API",
    integrationGate := "no external proof candidate to pin/import/check"
  },
  {
    searchTerm := "abelian variety",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult :=
      "mathlib has Mathlib.AlgebraicGeometry.Group.Abelian headed 'Abelian varieties', but no abelian-variety moduli or Shida construction theorem was found",
    integrationGate := "mathlib infrastructure only; not a terminal proof candidate"
  },
  {
    searchTerm := "PEL",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact source hit for a PEL moduli API or construction theorem",
    integrationGate := "no external proof candidate to pin/import/check"
  },
  {
    searchTerm := "canonical model",
    namedProjectScope := "mathlib and flt-regular Lean sources",
    namedProjectResult := "no exact source hit for a Shimura-variety canonical-model theorem",
    integrationGate := "no external proof candidate to pin/import/check"
  }
]

/-- The P7 external-audit table covers the eight requested search terms. -/
theorem externalAuditSearchRows_length : externalAuditSearchRows.length = 8 :=
  rfl

/-- The P7 absent-terminal-term list covers the eight requested search terms. -/
theorem absentTerminalSearchTerms_length : absentTerminalSearchTerms.length = 8 :=
  rfl

/-- P7 audit status: no terminal external proof candidate is known in the checked scope. -/
def externalAuditTerminalProofStatus : String :=
  "no terminal Lean 4 proof candidate found in checked named projects; authenticated global GitHub code search remains blocked by missing local auth"

/-- Validation command required before any S1-M-066 completion checkbox is set. -/
def repoLocalClosureValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_066.lean"

/-- One row in the S1-M-066.P7 repo-local closure gate. -/
structure RepoLocalClosureGateRow where
  gateId : String
  gateName : String
  requiredEvidence : String
  currentStatus : String
  completionEffect : String
  deriving Repr, DecidableEq

/--
Repo-local closure gate for `S1-M-066.P7.repo_local_closure_gate`.

These rows are checked metadata for the public backfill.  They do not upgrade
the parent theorem: completion still requires a repo-local Lean validation run,
all M0387 public merge gates, and the absence of completed-state
`repo_local_integration_debt`.
-/
def repoLocalClosureGateRows : List RepoLocalClosureGateRow := [
  {
    gateId := "SHIDA-CLOSURE-G01",
    gateName := "owned Lean artifact validates",
    requiredEvidence := repoLocalClosureValidationCommand,
    currentStatus := "required before any public completion checkbox is set",
    completionEffect := "blocks completion unless the current artifact or successor wrapper validates repo-locally"
  },
  {
    gateId := "SHIDA-CLOSURE-G02",
    gateName := "successor wrapper option",
    requiredEvidence :=
      "if this file is replaced by a narrower wrapper, run the corresponding Lake/Lean command and record the exact command and exit status",
    currentStatus := "not used in this child; primary command targets AwesomeTheorems/Stage1/S1_M_066.lean",
    completionEffect := "allows a future wrapper only if it is inside the repo-local verification closure"
  },
  {
    gateId := "SHIDA-CLOSURE-G03",
    gateName := "M0387 public merge gate",
    requiredEvidence :=
      "machine anchor, theorem-tree ledger, <=100-step leaves where applicable, and public backfill merged by a serial integrator",
    currentStatus := "public docs are not edited by this child worker",
    completionEffect := "blocks completion until private runtime evidence is serially merged into the public surface"
  },
  {
    gateId := "SHIDA-CLOSURE-G04",
    gateName := "repo-local integration debt gate",
    requiredEvidence :=
      "external proof candidates, if found, are pinned/imported/checked or have a concrete integration blocker",
    currentStatus := externalAuditTerminalProofStatus,
    completionEffect := "anchor-only external evidence cannot be marked completed"
  }
]

/-- The P7 repo-local closure gate records four blocking rows. -/
theorem repoLocalClosureGateRows_length : repoLocalClosureGateRows.length = 4 :=
  rfl

/-- The canonical closure validation command is the requested Stage1 command. -/
theorem repoLocalClosureValidationCommand_eq :
    repoLocalClosureValidationCommand =
      "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_066.lean" :=
  rfl

/--
The closure gate currently remains a non-completion gate.

This constant is intentionally a string status rather than a proof of the
terminal construction theorem; the parent theorem remains formalization debt.
-/
def repoLocalClosureGateCompletionStatus : String :=
  "gate recorded and validation required; parent theorem not marked completed"

end AwesomeTheorems.Stage1.S1_M_066
