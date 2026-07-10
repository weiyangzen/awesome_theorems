import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.RingTheory.AdicCompletion.Basic
import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction
import Mathlib.NumberTheory.ModularForms.Basic
import Mathlib.NumberTheory.RamificationInertia.Basic
import Mathlib.NumberTheory.RamificationInertia.Galois
import Mathlib.RepresentationTheory.Basic
import Mathlib.RepresentationTheory.Irreducible

/-!
# S1-M-065 / THM-M-0447

Stage1 statement-shape artifact for the Taylor-Wiles method: modularity
lifting for Galois representations.

The current repo-local dependency closure contains number-field, local-field,
adic-completion, ideal, adele, modular-form, and elliptic-curve infrastructure,
but no terminal Taylor-Wiles modularity-lifting theorem.  The declarations below
therefore keep the statement boundary explicit and add only low-risk wrappers
around mathlib facts that compile without proof placeholders.
-/

namespace AwesomeTheorems.Stage1.S1_M_065

universe uK uCoeff uResidue uG uRep uMod uLocal uHecke uDef uAux

/--
Statement-normalization choice made for `S1-M-065.P1`.

The Stage1 target is the classical minimal Taylor-Wiles modularity-lifting
variant over `ℚ`: a two-dimensional odd `p`-adic lift of an absolutely
irreducible odd residual representation of `G_ℚ`, with complete Noetherian
local coefficients, residual modularity, minimal local deformation conditions,
and an `R = T` patching conclusion implying modularity of the lift.
-/
inductive TaylorWilesVariantChoice where
  | minimalTwoDimensionalOddOverQ
  deriving DecidableEq, Repr

/-- Base-field normalization for the selected Taylor-Wiles variant. -/
abbrev SelectedBaseField := ℚ

/-- Canonical P1 choice: minimal two-dimensional odd Taylor-Wiles over `ℚ`. -/
def selectedTaylorWilesVariant : TaylorWilesVariantChoice :=
  TaylorWilesVariantChoice.minimalTwoDimensionalOddOverQ

/--
Abstract global Galois group boundary for a number field.

mathlib has finite Galois-extension APIs, but this Stage1 audit did not locate a
global absolute Galois group object model suitable for a Taylor-Wiles theorem.
-/
structure GlobalGaloisGroupData (K : Type uK) where
  Carrier : Type uG
  instCarrierGroup : Group Carrier
  continuousArithmetic : Carrier → Prop

/--
Abstract coefficient system for a modularity-lifting theorem.

The intended future replacement is a complete Noetherian local coefficient ring,
typically a finite extension of `ℤ_p` or its ring of integers, with residue field.
-/
structure TaylorWilesCoefficientData where
  Coeff : Type uCoeff
  Residue : Type uResidue
  instCoeffCommRing : CommRing Coeff
  instResidueField : Field Residue
  maximalIdeal : Ideal Coeff
  residueMap : Coeff →+* Residue
  isCompleteNoetherianLocal : Prop
  isAdicallyComplete : Prop
  residueCharacteristicOdd : Prop

attribute [instance] TaylorWilesCoefficientData.instCoeffCommRing
attribute [instance] TaylorWilesCoefficientData.instResidueField

/--
Abstract `n`-dimensional Galois representation together with its residual
representation and local conditions.

The predicates are intentionally fields rather than assumptions on a concrete
representation API: no suitable mathlib object for the terminal theorem was found.
-/
structure GaloisRepresentationData
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K) where
  Rep : Type uRep
  rank : ℕ
  residualRep : Type uResidue
  isContinuous : Rep → Prop
  isOdd : Rep → Prop
  isIrreducibleResidual : Prop
  isAbsolutelyIrreducibleResidual : Prop
  isOddResidual : Prop
  minimallyRamified : Rep → Prop
  localCondition : Type uLocal
  satisfiesLocalCondition : Rep → localCondition → Prop

/--
Abstract automorphic/modular side for the expected modular source of a Galois
representation.
-/
structure ModularSourceData
    (K : Type uK) (coeffs : TaylorWilesCoefficientData) where
  ModularObject : Type uMod
  HeckeAlgebra : Type uHecke
  instHeckeCommRing : CommRing HeckeAlgebra
  level : ModularObject → ℕ
  weight : ModularObject → ℕ
  heckeEigenCompatible : ModularObject → Prop

attribute [instance] ModularSourceData.instHeckeCommRing

/--
Abstract Taylor-Wiles deformation patching package.

This packages the deformation ring, Hecke algebra, local deformation conditions,
and the eventual `R = T` bridge as data/predicates, without asserting that the
Taylor-Wiles method has been formalized in this repository.
-/
structure TaylorWilesPatchingData
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs) where
  DeformationRing : Type uDef
  instDeformationCommRing : CommRing DeformationRing
  deformationIdeal : Ideal DeformationRing
  auxiliaryPrimeSystem : Type uAux
  minimalLocalDeformationConditions : Prop
  ordinaryOrFiniteFlatAtP : Prop
  taylorWilesNumericalCriterion : Prop
  patchedModuleFaithful : Prop
  deformationToHecke : DeformationRing → M.HeckeAlgebra
  isREqualsT : Prop

attribute [instance] TaylorWilesPatchingData.instDeformationCommRing

/--
Compatibility predicate between a Galois representation and a modular source.

Future work should replace this with equality of Frobenius characteristic
polynomials / Hecke eigenvalues at unramified primes and the required local
ramification conditions.
-/
def IsModularLift
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs) : Prop :=
  ∃ f : M.ModularObject, M.heckeEigenCompatible f ∧ 0 < M.weight f ∧ ρ.rank = 2

/--
Residual modularity predicate for the mod-`p` representation.  This is separate
from `IsModularLift` so the statement shape does not assume the desired terminal
conclusion as a hypothesis.
-/
def IsResiduallyModular
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs) : Prop :=
  ∃ f : M.ModularObject, M.heckeEigenCompatible f ∧ ρ.rank = 2

/--
Residual hypotheses selected by the P1 normalization.

This records the mathematical boundary without asserting a concrete residual
representation API: the residual representation is two-dimensional, odd,
irreducible, absolutely irreducible, and already modular.
-/
def SelectedResidualHypotheses
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs) : Prop :=
  ρ.rank = 2 ∧
    ρ.isIrreducibleResidual ∧
      ρ.isAbsolutelyIrreducibleResidual ∧
        ρ.isOddResidual ∧ IsResiduallyModular ρ M

/--
Local deformation hypotheses selected by the P1 normalization.

The chosen variant is the minimal Taylor-Wiles package: minimal ramification
away from `p`, an ordinary-or-finite-flat condition at `p`, and the local
deformation conditions used by the patching package.
-/
def SelectedLocalHypotheses
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    (patch : TaylorWilesPatchingData K coeffs G ρ M)
    (lift : ρ.Rep) : Prop :=
  ρ.minimallyRamified lift ∧
    patch.minimalLocalDeformationConditions ∧ patch.ordinaryOrFiniteFlatAtP

/--
Lean statement-shape candidate for the Taylor-Wiles modularity-lifting theorem.

The statement is deliberately explicit about the global field, coefficient
system, absolute-Galois-group boundary, residual hypotheses, local hypotheses,
patched deformation/Hecke package, and final modularity conclusion.
-/
def StatementShape
    (K : Type uK) [Field K] [NumberField K]
    (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs)
    (patch : TaylorWilesPatchingData K coeffs G ρ M)
    (lift : ρ.Rep) : Prop :=
  coeffs.isCompleteNoetherianLocal →
    coeffs.isAdicallyComplete →
      coeffs.residueCharacteristicOdd →
        SelectedResidualHypotheses ρ M →
          SelectedLocalHypotheses patch lift →
        ρ.isContinuous lift →
          ρ.isOdd lift →
            (patch.taylorWilesNumericalCriterion ∧
              patch.patchedModuleFaithful ∧ patch.isREqualsT) →
              IsModularLift ρ M

/--
Selected P1 statement shape with the base field specialized to `ℚ`.

This is the integration-ready normalized target for
`S1-M-065.P1.statement_normalization`; it is not a proof of the Taylor-Wiles
method.
-/
def SelectedStatementShape
    (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData SelectedBaseField)
    (ρ : GaloisRepresentationData SelectedBaseField coeffs G)
    (M : ModularSourceData SelectedBaseField coeffs)
    (patch : TaylorWilesPatchingData SelectedBaseField coeffs G ρ M)
    (lift : ρ.Rep) : Prop :=
  StatementShape SelectedBaseField coeffs G ρ M patch lift

/-- Checked definitional witness for the P1 statement-normalization choice. -/
theorem selectedStatementShape_eq_statementShape
    (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData SelectedBaseField)
    (ρ : GaloisRepresentationData SelectedBaseField coeffs G)
    (M : ModularSourceData SelectedBaseField coeffs)
    (patch : TaylorWilesPatchingData SelectedBaseField coeffs G ρ M)
    (lift : ρ.Rep) :
    SelectedStatementShape coeffs G ρ M patch lift =
      StatementShape SelectedBaseField coeffs G ρ M patch lift :=
  rfl

/--
Checked mathlib wrapper: the diagonal embedding of a number field into its adele
ring is injective.

This is infrastructure relevant to automorphic/adelic statements, not a
Taylor-Wiles modularity-lifting theorem.
-/
theorem adeleRing_algebraMap_injective
    (R K : Type*) [CommRing R] [IsDedekindDomain R] [Field K]
    [Algebra R K] [IsFractionRing R K] [NumberField K] :
    Function.Injective (algebraMap K (NumberField.AdeleRing R K)) :=
  NumberField.AdeleRing.algebraMap_injective R K

/--
Checked mathlib wrapper: the Hausdorff part of an adic-completion hypothesis is
equivalent to the expected separatedness condition.

This records a low-level commutative-algebra anchor for deformation rings.
-/
theorem adicHausdorff_iff
    {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M] (I : Ideal R) :
    IsHausdorff I M ↔
      ∀ x : M, (∀ n : ℕ, x ≡ 0 [SMOD (I ^ n • ⊤ : Submodule R M)]) → x = 0 :=
  isHausdorff_iff (I := I) (M := M)

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.NumberField.Basic",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.RingTheory.AdicCompletion.Basic",
  "Mathlib.RingTheory.AdicCompletion.RingHom",
  "Mathlib.RingTheory.DedekindDomain.FiniteAdeleRing",
  "Mathlib.NumberTheory.ModularForms.Basic",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction",
  "Mathlib.NumberTheory.RamificationInertia.Basic"
]

/-!
## P2 mathlib object-model audit

The following declarations are documentation-grade Lean data.  They keep the P2
object-model audit in the repo-local artifact while avoiding any claim that the
Taylor-Wiles method has been formalized.
-/

/-- Status of a mathlib component for Taylor-Wiles object modeling. -/
inductive ObjectModelAuditStatus where
  | reusableSubstrate
  | partialSubstrate
  | missingTaylorWilesInterface
  deriving DecidableEq, Repr

/-- One row of the P2 mathlib object-model audit. -/
structure MathlibObjectModelAuditRow where
  component : String
  importedModule : String
  reusableApis : List String
  missingInterfaces : List String
  status : ObjectModelAuditStatus
  deriving Repr

/--
P2 audit rows for the mathlib object model requested by
`S1-M-065.P2.mathlib_object_model`.

These rows are intentionally descriptive: the imported modules and the checked
wrappers above verify low-level availability, while the missing-interface column
records the remaining Taylor-Wiles-specific API work.
-/
def p2MathlibObjectModelAudit : List MathlibObjectModelAuditRow := [
  {
    component := "NumberField"
    importedModule := "Mathlib.NumberTheory.NumberField.Basic"
    reusableApis := [
      "NumberField",
      "NumberField.RingOfIntegers",
      "notation 𝓞"
    ]
    missingInterfaces := [
      "absolute Galois group of a number field as a topological profinite group",
      "global-to-local place package specialized to Galois representations"
    ]
    status := ObjectModelAuditStatus.partialSubstrate
  },
  {
    component := "AdeleRing"
    importedModule := "Mathlib.NumberTheory.NumberField.AdeleRing"
    reusableApis := [
      "NumberField.AdeleRing",
      "NumberField.AdeleRing.algebraMap_injective",
      "NumberField.AdeleRing.principalSubgroup"
    ]
    missingInterfaces := [
      "automorphic representation or Hecke-eigenpacket interface over adeles",
      "compatibility bridge from adelic data to Galois representations"
    ]
    status := ObjectModelAuditStatus.reusableSubstrate
  },
  {
    component := "IsNonarchimedeanLocalField"
    importedModule := "Mathlib.NumberTheory.LocalField.Basic"
    reusableApis := [
      "IsNonarchimedeanLocalField",
      "IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt"
    ]
    missingInterfaces := [
      "local Galois/decomposition/inertia groups attached to a place",
      "Taylor-Wiles local deformation-condition predicates"
    ]
    status := ObjectModelAuditStatus.partialSubstrate
  },
  {
    component := "IsAdicComplete"
    importedModule := "Mathlib.RingTheory.AdicCompletion.Basic"
    reusableApis := [
      "IsHausdorff",
      "IsPrecomplete",
      "IsAdicComplete",
      "IsAdicComplete.lift"
    ]
    missingInterfaces := [
      "complete Noetherian local coefficient-ring structure with residue field",
      "universal deformation-ring API and tangent-space comparison"
    ]
    status := ObjectModelAuditStatus.reusableSubstrate
  },
  {
    component := "ModularForm"
    importedModule := "Mathlib.NumberTheory.ModularForms.Basic"
    reusableApis := [
      "ModularForm",
      "ModularFormClass",
      "graded modular-form operations"
    ]
    missingInterfaces := [
      "Hecke algebra/eigenpacket package suitable for modularity lifting",
      "residual modularity predicate linked to Galois representations"
    ]
    status := ObjectModelAuditStatus.partialSubstrate
  },
  {
    component := "EllipticCurve and Weierstrass reduction"
    importedModule := "Mathlib.AlgebraicGeometry.EllipticCurve.Reduction"
    reusableApis := [
      "WeierstrassCurve",
      "WeierstrassCurve.IsIntegral",
      "WeierstrassCurve.IsMinimal",
      "WeierstrassCurve.reduction"
    ]
    missingInterfaces := [
      "elliptic-curve Galois representation attachment",
      "semistable/minimal local hypotheses connected to modularity lifting"
    ]
    status := ObjectModelAuditStatus.partialSubstrate
  },
  {
    component := "RamificationInertia"
    importedModule := "Mathlib.NumberTheory.RamificationInertia.Basic"
    reusableApis := [
      "Ideal.ramificationIdx",
      "Ideal.inertiaDeg",
      "IsDedekindDomain.sum_ramification_inertia"
    ]
    missingInterfaces := [
      "ramification predicates for continuous residual Galois representations",
      "decomposition/inertia action API for Taylor-Wiles local conditions"
    ]
    status := ObjectModelAuditStatus.partialSubstrate
  }
]

/-- The P2 object-model audit covers the seven requested component families. -/
def p2MathlibObjectModelAuditRowCount : Nat :=
  p2MathlibObjectModelAudit.length

/-- Checked row-count witness for the P2 mathlib object-model audit. -/
theorem p2MathlibObjectModelAuditRowCount_eq :
    p2MathlibObjectModelAuditRowCount = 7 :=
  rfl

/--
P2 completion status: the object model has reusable mathlib substrate, but the
Taylor-Wiles-specific theorem interfaces remain formalization debt.
-/
def p2ObjectModelCompletionStatus : String :=
  "partial_substrate_only; formalization_debt; not_repo_local_closed"

/-!
## P3 Galois-representation-side API audit

The following declarations select the strongest repo-local Lean 4 substrate
available for the Galois-representation side.  They intentionally stop at
checked object-model anchors and abstract predicates; they are not a
Taylor-Wiles modularity-lifting proof.
-/

/-- The absolute Galois group object currently available in mathlib. -/
abbrev TaylorWilesAbsoluteGaloisGroup (K : Type uK) [Field K] : Type uK :=
  Field.absoluteGaloisGroup K

/-- mathlib supplies the Krull topological-group structure on the absolute Galois group. -/
theorem taylorWilesAbsoluteGaloisGroup_isTopologicalGroup
    (K : Type uK) [Field K] :
    IsTopologicalGroup (TaylorWilesAbsoluteGaloisGroup K) := by
  infer_instance

/--
Plain linear representations of the selected absolute Galois group.

This is the nearest checked mathlib representation substrate.  Continuity,
`p`-adic coefficient topology, residual reduction, finite ramification, and
local restrictions are recorded separately below because they are not supplied
by this ordinary `Representation` alias.
-/
abbrev TaylorWilesPlainGaloisRepresentation
    (K : Type uK) (E : Type uCoeff) (V : Type uRep)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V] :
    Type (max uK uRep) :=
  Representation E (TaylorWilesAbsoluteGaloisGroup K) V

/-- The plain Galois-representation alias unfolds to mathlib's `Representation`. -/
theorem taylorWilesPlainGaloisRepresentation_def
    (K : Type uK) (E : Type uCoeff) (V : Type uRep)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V] :
    TaylorWilesPlainGaloisRepresentation K E V =
      Representation E (Field.absoluteGaloisGroup K) V :=
  rfl

/-- Irreducibility predicate available for the plain representation substrate. -/
def TaylorWilesPlainGaloisRepresentation.IsIrreducible
    {K : Type uK} {E : Type uCoeff} {V : Type uRep}
    [Field K] [Field E] [AddCommGroup V] [Module E V]
    (ρ : TaylorWilesPlainGaloisRepresentation K E V) : Prop :=
  Representation.IsIrreducible ρ

/--
Continuous Galois-representation boundary over the checked plain representation
substrate.

The continuity field remains a proposition-level slot until a concrete topology
on the coefficient module and a continuous-hom representation API are selected.
-/
structure ContinuousTaylorWilesGaloisRepresentation
    (K : Type uK) (E : Type uCoeff) (V : Type uRep)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V] where
  toRepresentation : TaylorWilesPlainGaloisRepresentation K E V
  isContinuous : Prop

/-- Residual representation package needed by the Taylor-Wiles hypotheses. -/
structure TaylorWilesResidualRepresentationData
    (K : Type uK) (κ : Type uResidue) (Vbar : Type uRep)
    [Field K] [Field κ] [AddCommGroup Vbar] [Module κ Vbar] where
  representation : TaylorWilesPlainGaloisRepresentation K κ Vbar
  residualCharacteristic : ℕ
  isIrreducible : Prop
  isAbsolutelyIrreducible : Prop
  isOdd : Prop

/--
Complex-conjugation slot for oddness.

For the selected `GL₂/ℚ` variant, this should later be replaced by the concrete
conjugacy class and determinant/eigenvalue condition at complex conjugation.
-/
structure TaylorWilesComplexConjugationData
    (K : Type uK) [Field K] where
  element : TaylorWilesAbsoluteGaloisGroup K
  squaresToOne : element * element = 1

/-- Oddness boundary for a two-dimensional Galois representation. -/
structure TaylorWilesOddnessData
    (K : Type uK) (E : Type uCoeff) (V : Type uRep)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V] where
  complexConjugation : TaylorWilesComplexConjugationData K
  representation : TaylorWilesPlainGaloisRepresentation K E V
  determinantAtComplexConjugationIsNegOne : Prop

/--
Local ramification/restriction boundary for the Galois side.

mathlib has finite-extension ramification and inertia groups, but this Stage1
artifact did not locate the place-indexed absolute decomposition/inertia-group
API needed to restrict a global `p`-adic representation at every local place.
-/
structure TaylorWilesLocalRamificationData
    (K : Type uK) [Field K] where
  Place : Type uLocal
  DecompositionGroup : Place → Type uG
  InertiaGroup : Place → Type uG
  instDecompositionGroup : (v : Place) → Group (DecompositionGroup v)
  instInertiaGroup : (v : Place) → Group (InertiaGroup v)
  restrictionToDecompositionGroup : Place → Prop
  inertiaActionTrivialAtUnramifiedPlaces : Prop
  minimallyRamifiedAtBadPlaces : Prop

/-- Status of a P3 Galois-representation-side API component. -/
inductive GaloisRepresentationSideAuditStatus where
  | checkedMathlibAnchor
  | abstractBoundary
  | missingTaylorWilesInterface
  deriving DecidableEq, Repr

/-- One row of the P3 Galois-representation-side audit. -/
structure GaloisRepresentationSideAuditRow where
  component : String
  repoLocalAnchors : List String
  selectedApi : String
  missingInterfaces : List String
  status : GaloisRepresentationSideAuditStatus
  deriving Repr

/--
P3 audit rows for absolute Galois groups, continuous representations, residual
representations, oddness, irreducibility, and local ramification.
-/
def p3GaloisRepresentationSideAudit : List GaloisRepresentationSideAuditRow := [
  {
    component := "absolute Galois group"
    repoLocalAnchors := [
      "Mathlib.FieldTheory.AbsoluteGaloisGroup",
      "Field.absoluteGaloisGroup",
      "TaylorWilesAbsoluteGaloisGroup",
      "taylorWilesAbsoluteGaloisGroup_isTopologicalGroup"
    ]
    selectedApi := "use Field.absoluteGaloisGroup K as the checked global absolute-Galois substrate"
    missingInterfaces := [
      "number-field-specialized place restrictions",
      "absolute decomposition and inertia subgroups for each local place"
    ]
    status := GaloisRepresentationSideAuditStatus.checkedMathlibAnchor
  },
  {
    component := "plain linear representations"
    repoLocalAnchors := [
      "Mathlib.RepresentationTheory.Basic",
      "Representation",
      "TaylorWilesPlainGaloisRepresentation",
      "taylorWilesPlainGaloisRepresentation_def"
    ]
    selectedApi := "use Representation E (Field.absoluteGaloisGroup K) V as the nearest checked substrate"
    missingInterfaces := [
      "continuous homomorphism to automorphisms or GL(V)",
      "coefficient-module topology and p-adic Banach/lattice structure"
    ]
    status := GaloisRepresentationSideAuditStatus.checkedMathlibAnchor
  },
  {
    component := "continuity"
    repoLocalAnchors := [
      "ContinuousTaylorWilesGaloisRepresentation.isContinuous"
    ]
    selectedApi := "record continuity as an explicit Prop field until a concrete continuous-representation API exists"
    missingInterfaces := [
      "bundled continuous representation object",
      "topology on endomorphism/automorphism targets compatible with Representation"
    ]
    status := GaloisRepresentationSideAuditStatus.abstractBoundary
  },
  {
    component := "residual representations"
    repoLocalAnchors := [
      "TaylorWilesResidualRepresentationData"
    ]
    selectedApi := "package the residual Representation over a residue field with irreducibility, absolute irreducibility, and oddness predicates"
    missingInterfaces := [
      "reduction map from integral p-adic lattices to residual representations",
      "semisimplification and residual determinant APIs"
    ]
    status := GaloisRepresentationSideAuditStatus.abstractBoundary
  },
  {
    component := "oddness"
    repoLocalAnchors := [
      "TaylorWilesComplexConjugationData",
      "TaylorWilesOddnessData"
    ]
    selectedApi := "record complex conjugation and determinant-at-complex-conjugation as explicit data"
    missingInterfaces := [
      "canonical complex-conjugation conjugacy class for G_Q",
      "determinant/trace interface for two-dimensional Galois representations"
    ]
    status := GaloisRepresentationSideAuditStatus.abstractBoundary
  },
  {
    component := "irreducibility"
    repoLocalAnchors := [
      "Mathlib.RepresentationTheory.Irreducible",
      "Representation.IsIrreducible",
      "TaylorWilesPlainGaloisRepresentation.IsIrreducible"
    ]
    selectedApi := "reuse Representation.IsIrreducible for the plain residual substrate"
    missingInterfaces := [
      "absolute irreducibility after scalar extension",
      "large-image or adequacy hypotheses used in modern Taylor-Wiles variants"
    ]
    status := GaloisRepresentationSideAuditStatus.checkedMathlibAnchor
  },
  {
    component := "local ramification"
    repoLocalAnchors := [
      "Mathlib.NumberTheory.RamificationInertia.Basic",
      "Mathlib.NumberTheory.RamificationInertia.Galois",
      "Ideal.ramificationIdx",
      "Ideal.inertiaDeg",
      "inertia",
      "TaylorWilesLocalRamificationData"
    ]
    selectedApi := "reuse finite-extension ramification/inertia anchors and keep absolute local restriction data abstract"
    missingInterfaces := [
      "decomposition/inertia subgroups inside absolute Galois groups of completions",
      "unramified and minimally ramified predicates for continuous residual representations"
    ]
    status := GaloisRepresentationSideAuditStatus.abstractBoundary
  }
]

/-- The P3 Galois-representation-side audit covers the seven requested component families. -/
def p3GaloisRepresentationSideAuditRowCount : Nat :=
  p3GaloisRepresentationSideAudit.length

/-- Checked row-count witness for the P3 Galois-representation-side audit. -/
theorem p3GaloisRepresentationSideAuditRowCount_eq :
    p3GaloisRepresentationSideAuditRowCount = 7 :=
  rfl

/--
P3 completion status: checked anchors exist for absolute Galois groups, plain
representations, representation irreducibility, and finite-extension
ramification/inertia, but the Taylor-Wiles-specific representation API remains
formalization debt.
-/
def p3GaloisRepresentationSideCompletionStatus : String :=
  "checked_substrate_plus_abstract_boundaries; formalization_debt; not_repo_local_closed"

/-!
## P4 deformation-functor package

The following declarations make the deformation side explicit enough for the
Stage1 child package: complete local coefficient rings, Artinian test algebras,
deformation functors, universal deformation rings, tangent spaces, and minimal
local deformation conditions.  They intentionally remain an object model and
audit surface, not a proof of representability or of the Taylor-Wiles method.
-/

/--
Complete local coefficient-ring boundary for deformation theory.

This refines `TaylorWilesCoefficientData` with the local/Noetherian/Hausdorff
conditions normally bundled into the Mazur deformation category.
-/
structure CompleteLocalCoefficientRingData where
  Carrier : Type uCoeff
  ResidueField : Type uResidue
  instCarrierCommRing : CommRing Carrier
  instResidueField : Field ResidueField
  maximalIdeal : Ideal Carrier
  residueMap : Carrier →+* ResidueField
  isLocalRing : Prop
  isNoetherianRing : Prop
  isMaximalAdicallyComplete : Prop
  isMaximalAdicallyHausdorff : Prop

attribute [instance] CompleteLocalCoefficientRingData.instCarrierCommRing
attribute [instance] CompleteLocalCoefficientRingData.instResidueField

/-- A checked bridge from the original coefficient data into the P4 boundary. -/
def coefficientDataToCompleteLocalBoundary
    (coeffs : TaylorWilesCoefficientData) : CompleteLocalCoefficientRingData where
  Carrier := coeffs.Coeff
  ResidueField := coeffs.Residue
  instCarrierCommRing := coeffs.instCoeffCommRing
  instResidueField := coeffs.instResidueField
  maximalIdeal := coeffs.maximalIdeal
  residueMap := coeffs.residueMap
  isLocalRing := coeffs.isCompleteNoetherianLocal
  isNoetherianRing := coeffs.isCompleteNoetherianLocal
  isMaximalAdicallyComplete := coeffs.isAdicallyComplete
  isMaximalAdicallyHausdorff := coeffs.isAdicallyComplete

/-- View a P4 complete-local boundary as the existing coefficient-data package. -/
def completeLocalBoundaryAsCoefficientData
    (coeffs : CompleteLocalCoefficientRingData) : TaylorWilesCoefficientData where
  Coeff := coeffs.Carrier
  Residue := coeffs.ResidueField
  instCoeffCommRing := coeffs.instCarrierCommRing
  instResidueField := coeffs.instResidueField
  maximalIdeal := coeffs.maximalIdeal
  residueMap := coeffs.residueMap
  isCompleteNoetherianLocal := coeffs.isLocalRing ∧ coeffs.isNoetherianRing
  isAdicallyComplete :=
    coeffs.isMaximalAdicallyComplete ∧ coeffs.isMaximalAdicallyHausdorff
  residueCharacteristicOdd := True

/--
Artinian local coefficient algebra used as a test object for a deformation
functor.
-/
structure TaylorWilesArtinianLocalAlgebra
    (coeffs : CompleteLocalCoefficientRingData) where
  Carrier : Type uDef
  instCarrierCommRing : CommRing Carrier
  coefficientMap : coeffs.Carrier →+* Carrier
  maximalIdeal : Ideal Carrier
  residueMap : Carrier →+* coeffs.ResidueField
  isLocalRing : Prop
  isArtinianRing : Prop
  residueMapCompatible : Prop

attribute [instance] TaylorWilesArtinianLocalAlgebra.instCarrierCommRing

/--
Abstract deformation functor on Artinian local coefficient algebras.

`mapAlong` records functorial transport along ring maps between test algebras;
the identity and composition laws are left as proposition fields until the
concrete category of local Artinian coefficient algebras is selected.
-/
structure TaylorWilesDeformationFunctor
    (coeffs : CompleteLocalCoefficientRingData)
    (K : Type uK) (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K (completeLocalBoundaryAsCoefficientData coeffs) G) where
  Object : TaylorWilesArtinianLocalAlgebra.{uDef, uCoeff, uResidue} coeffs → Type uDef
  mapAlong :
    {A B : TaylorWilesArtinianLocalAlgebra.{uDef, uCoeff, uResidue} coeffs} →
      (A.Carrier →+* B.Carrier) → Object A → Object B
  respectsIdentityMaps : Prop
  respectsComposition : Prop
  preservesResidualRepresentation : Prop

/--
Universal deformation-ring package for a deformation functor.

The representability statement is recorded as data, not asserted as a theorem.
Future work must replace these proposition fields with a concrete natural
equivalence between the functor and ring maps out of `Ring`.
-/
structure UniversalDeformationRingPackage
    (coeffs : CompleteLocalCoefficientRingData)
    (K : Type uK) (G : GlobalGaloisGroupData K)
    {ρ : GaloisRepresentationData K (completeLocalBoundaryAsCoefficientData coeffs) G}
    (F : TaylorWilesDeformationFunctor coeffs K G ρ) where
  Ring : Type uDef
  instRingCommRing : CommRing Ring
  maximalIdeal : Ideal Ring
  residueMap : Ring →+* coeffs.ResidueField
  isCompleteNoetherianLocal : Prop
  proRepresentsFunctor : Prop
  universalLiftExists : Prop
  naturalityInTestAlgebras : Prop

/-- Tangent-space package attached to a deformation functor. -/
structure TaylorWilesTangentSpaceData
    (coeffs : CompleteLocalCoefficientRingData)
    (K : Type uK) (G : GlobalGaloisGroupData K)
    {ρ : GaloisRepresentationData K (completeLocalBoundaryAsCoefficientData coeffs) G}
    (F : TaylorWilesDeformationFunctor coeffs K G ρ) where
  dualNumbers : TaylorWilesArtinianLocalAlgebra.{uDef, uCoeff, uResidue} coeffs
  TangentSpace : Type uLocal
  instTangentAddCommGroup : AddCommGroup TangentSpace
  scalarActionByResidueField : coeffs.ResidueField → TangentSpace → TangentSpace
  tangentEquiv : F.Object dualNumbers ≃ TangentSpace
  tangentDimension : ℕ
  tangentDimensionFormula : Prop

/--
Minimal local deformation conditions for the Taylor-Wiles deformation functor.

This records the local-place family, condition predicates, tangent subspaces,
and determinant/ramification constraints needed by the minimal variant.
-/
structure TaylorWilesMinimalLocalDeformationCondition
    (coeffs : CompleteLocalCoefficientRingData)
    (K : Type uK) (G : GlobalGaloisGroupData K)
    {ρ : GaloisRepresentationData K (completeLocalBoundaryAsCoefficientData coeffs) G}
    (F : TaylorWilesDeformationFunctor coeffs K G ρ) where
  Place : Type uLocal
  localConditionAt : Place → Type uDef
  satisfiesAt :
    (v : Place) → {A : TaylorWilesArtinianLocalAlgebra.{uDef, uCoeff, uResidue} coeffs} →
      F.Object A → localConditionAt v → Prop
  tangentSubspaceAt : Place → Type uLocal
  isMinimalAt : Place → Prop
  unramifiedOutsideMinimalSet : Prop
  fixedDeterminantCondition : Prop
  localTangentDimensionFormula : Prop
  compatibleWithPatchingData : Prop

/-- Status of a P4 deformation-functor package component. -/
inductive DeformationFunctorPackageAuditStatus where
  | checkedBoundaryData
  | abstractBoundary
  | missingTaylorWilesInterface
  deriving DecidableEq, Repr

/-- One row of the P4 deformation-functor package audit. -/
structure DeformationFunctorPackageAuditRow where
  component : String
  repoLocalAnchors : List String
  selectedApi : String
  missingInterfaces : List String
  status : DeformationFunctorPackageAuditStatus
  deriving Repr

/--
P4 audit rows for complete local coefficient rings, deformation functors,
universal deformation rings, tangent spaces, and minimal local conditions.
-/
def p4DeformationFunctorPackageAudit : List DeformationFunctorPackageAuditRow := [
  {
    component := "complete local coefficient rings"
    repoLocalAnchors := [
      "TaylorWilesCoefficientData",
      "CompleteLocalCoefficientRingData",
      "coefficientDataToCompleteLocalBoundary",
      "Mathlib.RingTheory.AdicCompletion.Basic",
      "adicHausdorff_iff"
    ]
    selectedApi := "reuse checked adic-completion anchors and package complete Noetherian local hypotheses explicitly"
    missingInterfaces := [
      "bundled complete Noetherian local coefficient-ring class with residue field",
      "proof that common p-adic coefficient rings satisfy the selected package"
    ]
    status := DeformationFunctorPackageAuditStatus.checkedBoundaryData
  },
  {
    component := "Artinian local test algebras"
    repoLocalAnchors := [
      "TaylorWilesArtinianLocalAlgebra"
    ]
    selectedApi := "model test objects as coefficient algebras with local, Artinian, and residue-compatibility fields"
    missingInterfaces := [
      "category of local Artinian coefficient algebras",
      "morphisms constrained to preserve coefficient and residue maps"
    ]
    status := DeformationFunctorPackageAuditStatus.abstractBoundary
  },
  {
    component := "deformation functors"
    repoLocalAnchors := [
      "TaylorWilesDeformationFunctor"
    ]
    selectedApi := "encode object assignment and transport along test-algebra maps as checked Lean data"
    missingInterfaces := [
      "quotient by strict equivalence of lifts",
      "Schlessinger/Mazur functoriality and continuity conditions as proved typeclass-style laws"
    ]
    status := DeformationFunctorPackageAuditStatus.abstractBoundary
  },
  {
    component := "universal deformation rings"
    repoLocalAnchors := [
      "UniversalDeformationRingPackage"
    ]
    selectedApi := "record complete local ring data and pro-representability as explicit fields"
    missingInterfaces := [
      "natural equivalence between deformations over A and local ring maps R -> A",
      "representability theorem under residual absolute irreducibility hypotheses"
    ]
    status := DeformationFunctorPackageAuditStatus.missingTaylorWilesInterface
  },
  {
    component := "tangent spaces"
    repoLocalAnchors := [
      "TaylorWilesTangentSpaceData"
    ]
    selectedApi := "identify tangent vectors with deformations over dual numbers and record dimension formulas"
    missingInterfaces := [
      "dual-number algebra over the residue field as a concrete Artinian test algebra",
      "cohomological tangent-space comparison with H^1 and local Selmer conditions"
    ]
    status := DeformationFunctorPackageAuditStatus.abstractBoundary
  },
  {
    component := "minimal local deformation conditions"
    repoLocalAnchors := [
      "TaylorWilesMinimalLocalDeformationCondition",
      "TaylorWilesPatchingData.minimalLocalDeformationConditions"
    ]
    selectedApi := "record a place-indexed family of local conditions compatible with the patching package"
    missingInterfaces := [
      "place-indexed local deformation rings and restriction functors",
      "minimal ramification and fixed-determinant tangent-dimension proofs"
    ]
    status := DeformationFunctorPackageAuditStatus.abstractBoundary
  }
]

/-- The P4 deformation-functor audit covers the six requested component families. -/
def p4DeformationFunctorPackageAuditRowCount : Nat :=
  p4DeformationFunctorPackageAudit.length

/-- Checked row-count witness for the P4 deformation-functor package audit. -/
theorem p4DeformationFunctorPackageAuditRowCount_eq :
    p4DeformationFunctorPackageAuditRowCount = 6 :=
  rfl

/--
P4 completion status: the repo now has a checked deformation-side object model,
but representability, universal deformation rings, tangent-space comparisons,
and minimal local deformation proofs remain formalization debt.
-/
def p4DeformationFunctorPackageCompletionStatus : String :=
  "checked_deformation_object_model; formalization_debt; not_repo_local_closed"

/-!
## P5 modular Hecke/eigenpacket side

The following declarations refine the modular side needed by the residual
modularity hypothesis.  They make Hecke algebras, systems of eigenvalues,
residual eigenpackets, and Galois-side compatibility explicit as Lean data while
remaining below a terminal Taylor-Wiles proof.
-/

/--
Hecke-algebra boundary attached to the selected modular source.

The algebra itself is the one already carried by `ModularSourceData`; this
package records the missing operator family, coefficient structure, finite
generation, and action data needed by an eventual `R = T` comparison.
-/
structure TaylorWilesHeckeAlgebraData
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (M : ModularSourceData K coeffs) where
  coefficientMap : coeffs.Coeff →+* M.HeckeAlgebra
  OperatorIndex : Type uLocal
  standardOperator : OperatorIndex → M.HeckeAlgebra
  actsOnModularObjects : M.HeckeAlgebra → M.ModularObject → M.ModularObject
  actionPreservesLevel : Prop
  actionPreservesWeight : Prop
  standardOperatorsCommute : Prop
  generatedByStandardOperators : Prop
  finiteOverCoefficientRing : Prop

/--
Hecke eigenpacket over the coefficient ring and its residual reduction.

The two ring homomorphisms are the coefficient-valued and residual systems of
eigenvalues.  Their compatibility with actual Hecke action and residual
reduction is recorded as proposition fields until a concrete Hecke-operator API
is selected.
-/
structure TaylorWilesHeckeEigenpacket
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (M : ModularSourceData K coeffs)
    (H : TaylorWilesHeckeAlgebraData K coeffs M) where
  modularObject : M.ModularObject
  coefficientEigencharacter : M.HeckeAlgebra →+* coeffs.Coeff
  residualEigencharacter : M.HeckeAlgebra →+* coeffs.Residue
  eigenvectorForHeckeAction : Prop
  residualReductionCompatible : Prop
  levelCompatible : Prop
  weightCompatible : Prop

/--
Residual Hecke ideal associated to an eigenpacket.

This is the kernel of the residual eigencharacter and is the localizing ideal
that should eventually connect the Hecke algebra to a residual Galois
representation.
-/
def TaylorWilesHeckeEigenpacket.residualHeckeIdeal
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {M : ModularSourceData K coeffs}
    {H : TaylorWilesHeckeAlgebraData K coeffs M}
    (packet : TaylorWilesHeckeEigenpacket K coeffs M H) : Ideal M.HeckeAlgebra :=
  RingHom.ker packet.residualEigencharacter

/--
Compatibility between the residual Galois representation and a residual
Hecke eigenpacket.

Future work should replace the trace/determinant functions by characteristic
polynomials of Frobenius elements and standard Hecke operators at unramified
places.
-/
structure TaylorWilesResidualHeckeGaloisCompatibility
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs)
    (H : TaylorWilesHeckeAlgebraData K coeffs M)
    (packet : TaylorWilesHeckeEigenpacket K coeffs M H) where
  UnramifiedPlace : Type uLocal
  frobeniusTrace : UnramifiedPlace → coeffs.Residue
  heckeTrace : UnramifiedPlace → coeffs.Residue
  frobeniusDeterminant : UnramifiedPlace → coeffs.Residue
  heckeDeterminant : UnramifiedPlace → coeffs.Residue
  traceCompatibility : Prop
  determinantCompatibility : Prop
  residualRepresentationMatchesEigenpacket : Prop
  localConditionsCompatible : Prop

/--
Predicate saying that a concrete residual Hecke eigenpacket supports the
existing residual modularity hypothesis.
-/
def HeckeEigenpacketSupportsResidualModularity
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs)
    (H : TaylorWilesHeckeAlgebraData K coeffs M)
    (packet : TaylorWilesHeckeEigenpacket K coeffs M H)
    (compat :
      TaylorWilesResidualHeckeGaloisCompatibility K coeffs G ρ M H packet) : Prop :=
  M.heckeEigenCompatible packet.modularObject ∧
    ρ.rank = 2 ∧
      packet.residualReductionCompatible ∧
        compat.residualRepresentationMatchesEigenpacket

/--
Checked bridge: a residual Hecke eigenpacket satisfying the compatibility
predicate implies the existing abstract `IsResiduallyModular` hypothesis.
-/
theorem heckeEigenpacketSupportsResidualModularity_isResiduallyModular
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {H : TaylorWilesHeckeAlgebraData K coeffs M}
    {packet : TaylorWilesHeckeEigenpacket K coeffs M H}
    {compat :
      TaylorWilesResidualHeckeGaloisCompatibility K coeffs G ρ M H packet} :
    HeckeEigenpacketSupportsResidualModularity ρ M H packet compat →
      IsResiduallyModular ρ M := by
  intro h
  exact ⟨packet.modularObject, h.1, h.2.1⟩

/-- Status of a P5 modular Hecke/eigenpacket component. -/
inductive ModularHeckeSideAuditStatus where
  | checkedBoundaryData
  | abstractBoundary
  | missingTaylorWilesInterface
  deriving DecidableEq, Repr

/-- One row of the P5 modular Hecke/eigenpacket-side audit. -/
structure ModularHeckeSideAuditRow where
  component : String
  repoLocalAnchors : List String
  selectedApi : String
  missingInterfaces : List String
  status : ModularHeckeSideAuditStatus
  deriving Repr

/--
P5 audit rows for modular objects, Hecke algebras, Hecke eigenpackets, residual
modularity, and compatibility with the Galois-representation side.
-/
def p5ModularHeckeSideAudit : List ModularHeckeSideAuditRow := [
  {
    component := "modular-form source substrate"
    repoLocalAnchors := [
      "Mathlib.NumberTheory.ModularForms.Basic",
      "ModularSourceData",
      "ModularSourceData.heckeEigenCompatible"
    ]
    selectedApi := "keep the modular object abstract but tied to checked mathlib modular-form imports"
    missingInterfaces := [
      "newform/cuspform/eigenform hierarchy with level and weight",
      "coefficient field and q-expansion API connected to Galois representations"
    ]
    status := ModularHeckeSideAuditStatus.abstractBoundary
  },
  {
    component := "Hecke algebra and operators"
    repoLocalAnchors := [
      "ModularSourceData.HeckeAlgebra",
      "TaylorWilesHeckeAlgebraData"
    ]
    selectedApi := "record coefficient map, standard Hecke operators, action on modular objects, and finite generation"
    missingInterfaces := [
      "concrete Hecke operators on modular-form spaces",
      "proof that standard operators commute and generate the localized Hecke algebra"
    ]
    status := ModularHeckeSideAuditStatus.abstractBoundary
  },
  {
    component := "Hecke eigenpackets"
    repoLocalAnchors := [
      "TaylorWilesHeckeEigenpacket",
      "TaylorWilesHeckeEigenpacket.residualHeckeIdeal"
    ]
    selectedApi := "represent coefficient and residual systems of eigenvalues as ring homomorphisms"
    missingInterfaces := [
      "simultaneous eigenspace construction for the commuting Hecke operators",
      "localization/completion of the Hecke algebra at the residual maximal ideal"
    ]
    status := ModularHeckeSideAuditStatus.checkedBoundaryData
  },
  {
    component := "residual modularity predicate"
    repoLocalAnchors := [
      "IsResiduallyModular",
      "HeckeEigenpacketSupportsResidualModularity",
      "heckeEigenpacketSupportsResidualModularity_isResiduallyModular"
    ]
    selectedApi := "bridge a compatible residual Hecke eigenpacket to the existing residual modularity hypothesis"
    missingInterfaces := [
      "proof that the selected residual representation is attached to the eigenpacket",
      "residual semisimplification and determinant compatibility"
    ]
    status := ModularHeckeSideAuditStatus.checkedBoundaryData
  },
  {
    component := "Galois/Hecke compatibility"
    repoLocalAnchors := [
      "TaylorWilesResidualHeckeGaloisCompatibility"
    ]
    selectedApi := "record trace and determinant compatibility at unramified places"
    missingInterfaces := [
      "Frobenius conjugacy classes and characteristic polynomials in the residual representation",
      "standard T_l and diamond-operator eigenvalue formulas"
    ]
    status := ModularHeckeSideAuditStatus.abstractBoundary
  },
  {
    component := "R = T interface"
    repoLocalAnchors := [
      "TaylorWilesPatchingData.deformationToHecke",
      "TaylorWilesPatchingData.isREqualsT"
    ]
    selectedApi := "keep the deformation-to-Hecke map in the patching package and expose the Hecke side needed to localize it"
    missingInterfaces := [
      "completed local Hecke algebra at the residual maximal ideal",
      "surjectivity/injectivity comparison with the universal deformation ring"
    ]
    status := ModularHeckeSideAuditStatus.missingTaylorWilesInterface
  }
]

/-- The P5 modular Hecke/eigenpacket audit covers the six requested component families. -/
def p5ModularHeckeSideAuditRowCount : Nat :=
  p5ModularHeckeSideAudit.length

/-- Checked row-count witness for the P5 modular Hecke/eigenpacket audit. -/
theorem p5ModularHeckeSideAuditRowCount_eq :
    p5ModularHeckeSideAuditRowCount = 6 :=
  rfl

/--
P5 completion status: the repo now has checked Hecke/eigenpacket boundary data
and a bridge into residual modularity, but concrete Hecke operators, localized
Hecke algebras, Galois attachment, and `R = T` remain formalization debt.
-/
def p5ModularHeckeSideCompletionStatus : String :=
  "checked_hecke_eigenpacket_boundary; formalization_debt; not_repo_local_closed"

/-!
## P6 Taylor-Wiles auxiliary-prime system

The following declarations encode the auxiliary prime sets used in the
Taylor-Wiles patching argument.  They make the local congruence/Frobenius
conditions and the global Selmer-killing condition explicit, and prove checked
bridges from packaged witness data to the compatibility predicates consumed by
the existing patching boundary.  The concrete Chebotarev, local deformation,
and global cohomology arguments remain future formalization work.
-/

/--
One finite Taylor-Wiles auxiliary prime set at a chosen level.

The `Place` type is intentionally abstract because the current repo-local
dependencies do not expose the place-indexed absolute decomposition-group API
needed for the concrete number-field statement.  The proposition fields record
the standard local conditions: auxiliary primes are outside the minimal bad
set, have residue cardinality congruent to `1` modulo the selected level, the
residual representation is unramified there, Frobenius has the prescribed
eigenvalue shape, and the local deformation condition is the Taylor-Wiles one.
-/
structure TaylorWilesAuxiliaryPrimeSet
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K coeffs G)
    (Place : Type uAux) where
  primes : List Place
  residualCharacteristic : ℕ
  levelExponent : ℕ
  isAuxiliaryPrime : Place → Prop
  outsideMinimalRamificationSet : Place → Prop
  residueCardinalityCongruentOne : Place → Prop
  residualRepresentationUnramifiedAt : Place → Prop
  frobeniusHasTaylorWilesEigenvalues : Place → Prop
  localDeformationConditionSmoothAt : Place → Prop
  localDeformationConditionMatchesResidualAt : Place → Prop
  primesAreDistinct : primes.Nodup
  primesAreAuxiliary : ∀ v, v ∈ primes → isAuxiliaryPrime v

/--
Local compatibility for a Taylor-Wiles auxiliary prime set.

Every chosen auxiliary prime is outside the minimal bad set, has the required
congruence condition, is unramified for the residual representation, has the
prescribed Frobenius eigenvalue behavior, and has a smooth local deformation
condition compatible with the residual representation.
-/
def TaylorWilesAuxiliaryPrimeSet.LocalCompatibility
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {Place : Type uAux}
    (Q : TaylorWilesAuxiliaryPrimeSet K coeffs G ρ Place) : Prop :=
  ∀ v, v ∈ Q.primes →
    Q.outsideMinimalRamificationSet v ∧
      Q.residueCardinalityCongruentOne v ∧
        Q.residualRepresentationUnramifiedAt v ∧
          Q.frobeniusHasTaylorWilesEigenvalues v ∧
            Q.localDeformationConditionSmoothAt v ∧
              Q.localDeformationConditionMatchesResidualAt v

/--
Global compatibility for a Taylor-Wiles auxiliary prime set.

The set must have the required cardinality, be disjoint from the minimal
ramification set, kill the selected dual Selmer quotient, and keep the patched
global deformation problem compatible with the numerical criterion.
-/
structure TaylorWilesAuxiliaryPrimeGlobalCompatibility
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {Place : Type uAux}
    (Q : TaylorWilesAuxiliaryPrimeSet K coeffs G ρ Place) where
  cardinalityMatchesDualSelmerRank : Prop
  disjointFromMinimalRamificationSet : Prop
  killsDualSelmerQuotient : Prop
  globalDeformationProblemCompatible : Prop
  numericalCriterionUnaffected : Prop

/-- The bundled global compatibility record interpreted as a proposition. -/
def TaylorWilesAuxiliaryPrimeSet.GlobalCompatibility
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {Place : Type uAux}
    (Q : TaylorWilesAuxiliaryPrimeSet K coeffs G ρ Place) : Prop :=
  ∃ global : TaylorWilesAuxiliaryPrimeGlobalCompatibility Q,
    global.cardinalityMatchesDualSelmerRank ∧
      global.disjointFromMinimalRamificationSet ∧
        global.killsDualSelmerQuotient ∧
          global.globalDeformationProblemCompatible ∧
            global.numericalCriterionUnaffected

/--
Bundled Taylor-Wiles auxiliary prime system attached to the existing patching
package.

The fields `localCompatibilityWitness` and `globalCompatibilityWitness` are the
mathematical obligations still requiring concrete Chebotarev/local-global
formalization.  The theorems below expose them as checked bridges into the
public predicates used by the Stage1 artifact.
-/
structure TaylorWilesAuxiliaryPrimeSystem
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs)
    (patch : TaylorWilesPatchingData K coeffs G ρ M)
    (Place : Type uAux) where
  auxiliarySet : TaylorWilesAuxiliaryPrimeSet K coeffs G ρ Place
  patchingAuxiliaryObject : patch.auxiliaryPrimeSystem
  localCompatibilityWitness : auxiliarySet.LocalCompatibility
  globalCompatibilityWitness : auxiliarySet.GlobalCompatibility
  compatibleWithMinimalLocalConditions : patch.minimalLocalDeformationConditions
  compatibleWithNumericalCriterion : patch.taylorWilesNumericalCriterion

/--
Compatibility predicate saying that the auxiliary prime system supplies both the
local and global inputs needed by the patching boundary.
-/
def TaylorWilesAuxiliaryPrimeSystem.SupportsPatching
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {Place : Type uAux}
    (system : TaylorWilesAuxiliaryPrimeSystem K coeffs G ρ M patch Place) : Prop :=
  system.auxiliarySet.LocalCompatibility ∧
    system.auxiliarySet.GlobalCompatibility ∧
      patch.minimalLocalDeformationConditions ∧
        patch.taylorWilesNumericalCriterion

/-- Checked bridge from a bundled auxiliary system to its local compatibility predicate. -/
theorem taylorWilesAuxiliaryPrimeSystem_localCompatibility
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {Place : Type uAux}
    (system : TaylorWilesAuxiliaryPrimeSystem K coeffs G ρ M patch Place) :
    system.auxiliarySet.LocalCompatibility :=
  system.localCompatibilityWitness

/-- Checked bridge from a bundled auxiliary system to its global compatibility predicate. -/
theorem taylorWilesAuxiliaryPrimeSystem_globalCompatibility
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {Place : Type uAux}
    (system : TaylorWilesAuxiliaryPrimeSystem K coeffs G ρ M patch Place) :
    system.auxiliarySet.GlobalCompatibility :=
  system.globalCompatibilityWitness

/--
Checked bridge: the bundled system supplies the auxiliary object and the
local/global compatibility data expected by the patching boundary.
-/
theorem taylorWilesAuxiliaryPrimeSystem_supportsPatching
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {Place : Type uAux}
    (system : TaylorWilesAuxiliaryPrimeSystem K coeffs G ρ M patch Place) :
    system.SupportsPatching := by
  exact ⟨system.localCompatibilityWitness,
    system.globalCompatibilityWitness,
    system.compatibleWithMinimalLocalConditions,
    system.compatibleWithNumericalCriterion⟩

/-- A bundled auxiliary prime system gives an inhabitant of the patching package's auxiliary type. -/
theorem taylorWilesAuxiliaryPrimeSystem_hasPatchingAuxiliaryObject
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {Place : Type uAux}
    (system : TaylorWilesAuxiliaryPrimeSystem K coeffs G ρ M patch Place) :
    Nonempty patch.auxiliaryPrimeSystem :=
  ⟨system.patchingAuxiliaryObject⟩

/-- Status of a P6 Taylor-Wiles auxiliary-prime component. -/
inductive AuxiliaryPrimeSystemAuditStatus where
  | checkedBoundaryData
  | abstractCompatibilityBoundary
  | missingTaylorWilesProof
  deriving DecidableEq, Repr

/-- One row of the P6 auxiliary-prime-system audit. -/
structure AuxiliaryPrimeSystemAuditRow where
  component : String
  repoLocalAnchors : List String
  selectedApi : String
  missingInterfaces : List String
  status : AuxiliaryPrimeSystemAuditStatus
  deriving Repr

/--
P6 audit rows for Taylor-Wiles auxiliary prime sets and their local/global
compatibility conditions.
-/
def p6AuxiliaryPrimeSystemAudit : List AuxiliaryPrimeSystemAuditRow := [
  {
    component := "finite auxiliary prime sets"
    repoLocalAnchors := [
      "TaylorWilesAuxiliaryPrimeSet",
      "TaylorWilesAuxiliaryPrimeSet.primes",
      "TaylorWilesAuxiliaryPrimeSet.primesAreDistinct"
    ]
    selectedApi := "encode each Taylor-Wiles level as a list of abstract places with a no-duplicate proof"
    missingInterfaces := [
      "concrete number-field prime/place API connected to decomposition groups",
      "finite-set cardinality theorem for the selected place representation"
    ]
    status := AuxiliaryPrimeSystemAuditStatus.checkedBoundaryData
  },
  {
    component := "local congruence and Frobenius conditions"
    repoLocalAnchors := [
      "TaylorWilesAuxiliaryPrimeSet.LocalCompatibility",
      "taylorWilesAuxiliaryPrimeSystem_localCompatibility"
    ]
    selectedApi := "record residue-cardinality congruence, unramifiedness, Frobenius eigenvalue shape, and smooth local deformation data for every selected prime"
    missingInterfaces := [
      "residue-field cardinality and congruence modulo powers of p",
      "Frobenius elements and characteristic-polynomial/eigenvalue formulas"
    ]
    status := AuxiliaryPrimeSystemAuditStatus.abstractCompatibilityBoundary
  },
  {
    component := "global Selmer-killing condition"
    repoLocalAnchors := [
      "TaylorWilesAuxiliaryPrimeGlobalCompatibility",
      "TaylorWilesAuxiliaryPrimeSet.GlobalCompatibility",
      "taylorWilesAuxiliaryPrimeSystem_globalCompatibility"
    ]
    selectedApi := "bundle cardinality, disjointness, dual-Selmer-killing, and numerical-criterion preservation as the global compatibility predicate"
    missingInterfaces := [
      "global Galois cohomology and Selmer/dual-Selmer groups",
      "Chebotarev argument proving enough auxiliary primes exist"
    ]
    status := AuxiliaryPrimeSystemAuditStatus.abstractCompatibilityBoundary
  },
  {
    component := "patching-package interface"
    repoLocalAnchors := [
      "TaylorWilesPatchingData.auxiliaryPrimeSystem",
      "TaylorWilesAuxiliaryPrimeSystem",
      "TaylorWilesAuxiliaryPrimeSystem.SupportsPatching",
      "taylorWilesAuxiliaryPrimeSystem_supportsPatching",
      "taylorWilesAuxiliaryPrimeSystem_hasPatchingAuxiliaryObject"
    ]
    selectedApi := "connect the auxiliary-prime system to the existing patching object, minimal local conditions, and numerical criterion fields"
    missingInterfaces := [
      "construction of patched modules from the tower of auxiliary levels",
      "proof that the auxiliary levels preserve the R = T numerical criterion"
    ]
    status := AuxiliaryPrimeSystemAuditStatus.checkedBoundaryData
  },
  {
    component := "existence theorem for Taylor-Wiles primes"
    repoLocalAnchors := [
      "absentTerminalSearchTerms"
    ]
    selectedApi := "no repo-local existence theorem is claimed; keep the Chebotarev/Selmer argument as formalization debt"
    missingInterfaces := [
      "large-image or adequacy hypotheses needed for the auxiliary prime construction",
      "formal proof choosing primes satisfying all local and global constraints"
    ]
    status := AuxiliaryPrimeSystemAuditStatus.missingTaylorWilesProof
  }
]

/-- The P6 auxiliary-prime-system audit covers the five requested component families. -/
def p6AuxiliaryPrimeSystemAuditRowCount : Nat :=
  p6AuxiliaryPrimeSystemAudit.length

/-- Checked row-count witness for the P6 auxiliary-prime-system audit. -/
theorem p6AuxiliaryPrimeSystemAuditRowCount_eq :
    p6AuxiliaryPrimeSystemAuditRowCount = 5 :=
  rfl

/--
P6 completion status: the repo now has checked auxiliary-prime boundary data and
compatibility bridges, but concrete prime existence, Chebotarev, Frobenius,
local deformation, and Selmer-killing proofs remain formalization debt.
-/
def p6AuxiliaryPrimeSystemCompletionStatus : String :=
  "checked_auxiliary_prime_boundary; formalization_debt; not_repo_local_closed"

/-!
## P7 patched modules and numerical criterion

The following declarations make the patched-module and numerical-criterion
boundary explicit.  They connect the auxiliary-prime interface to the existing
`TaylorWilesPatchingData` fields and prove checked extraction lemmas from a
bundled numerical-criterion witness to the `R = T` proposition already used by
`StatementShape`.  The real commutative-algebra proof, length comparison,
Fitting/congruence-ideal computation, and construction of patched modules remain
formalization debt.
-/

/--
Patched module package for a Taylor-Wiles patching datum.

The module is recorded with actions of both the universal deformation ring and
the Hecke algebra.  The proposition fields name the standard patching
obligations: compatibility through the auxiliary-level tower, finite generation,
balancedness, near-faithfulness/support control, Hecke/deformation compatibility,
and specialization back to the classical module.
-/
structure TaylorWilesPatchedModuleData
    (K : Type uK) (coeffs : TaylorWilesCoefficientData)
    (G : GlobalGaloisGroupData K)
    (ρ : GaloisRepresentationData K coeffs G)
    (M : ModularSourceData K coeffs)
    (patch : TaylorWilesPatchingData K coeffs G ρ M) where
  PatchedModule : Type uMod
  instPatchedAddCommGroup : AddCommGroup PatchedModule
  instPatchedDeformationModule : Module patch.DeformationRing PatchedModule
  instPatchedHeckeModule : Module M.HeckeAlgebra PatchedModule
  patchingLevelTower : Type uAux
  auxiliaryTowerCompatible : Prop
  transitionMapsCompatible : Prop
  finiteGeneratedOverDeformationRing : Prop
  balancedOverPowerSeriesAlgebra : Prop
  nearlyFaithfulOverDeformationRing : Prop
  supportControlsDeformationRing : Prop
  heckeActionCompatibleWithDeformationMap : Prop
  specializationRecoversClassicalModule : Prop

attribute [instance] TaylorWilesPatchedModuleData.instPatchedAddCommGroup
attribute [instance] TaylorWilesPatchedModuleData.instPatchedDeformationModule
attribute [instance] TaylorWilesPatchedModuleData.instPatchedHeckeModule

/--
The patched module supplies the module-theoretic hypotheses used by the
Taylor-Wiles numerical criterion.
-/
def TaylorWilesPatchedModuleData.SupportsNumericalCriterion
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    (patched : TaylorWilesPatchedModuleData K coeffs G ρ M patch) : Prop :=
  patched.auxiliaryTowerCompatible ∧
    patched.transitionMapsCompatible ∧
      patched.finiteGeneratedOverDeformationRing ∧
        patched.balancedOverPowerSeriesAlgebra ∧
          patched.nearlyFaithfulOverDeformationRing ∧
            patched.supportControlsDeformationRing ∧
              patched.heckeActionCompatibleWithDeformationMap ∧
                patched.specializationRecoversClassicalModule

/--
Bundled commutative-algebra numerical criterion for the Taylor-Wiles method.

The final three fields intentionally mirror the existing patching package:
`patch.taylorWilesNumericalCriterion`, `patch.patchedModuleFaithful`, and
`patch.isREqualsT`.  Until the length/Fitting/congruence-ideal arguments are
formalized, this structure is a checked obligation boundary rather than a proof
of the numerical criterion from first principles.
-/
structure TaylorWilesNumericalCriterionData
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    (patched : TaylorWilesPatchedModuleData K coeffs G ρ M patch) where
  patchedModuleSupportsCriterion : patched.SupportsNumericalCriterion
  cotangentDimensionBound : Prop
  congruenceIdealLengthFormula : Prop
  fittingIdealControl : Prop
  completeIntersectionDeformationRing : Prop
  heckeAlgebraFiniteOverCoefficients : Prop
  deformationToHeckeSurjective : Prop
  kernelControlledByLengthComparison : Prop
  numericalEquality : Prop
  patchingNumericalCriterion : patch.taylorWilesNumericalCriterion
  patchedModuleFaithful : patch.patchedModuleFaithful
  rEqualsT : patch.isREqualsT

/--
All commutative-algebra obligations contained in a bundled numerical criterion.
-/
def TaylorWilesNumericalCriterionData.SatisfiesCommutativeAlgebraInputs
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {patched : TaylorWilesPatchedModuleData K coeffs G ρ M patch}
    (criterion : TaylorWilesNumericalCriterionData patched) : Prop :=
  patched.SupportsNumericalCriterion ∧
    criterion.cotangentDimensionBound ∧
      criterion.congruenceIdealLengthFormula ∧
        criterion.fittingIdealControl ∧
          criterion.completeIntersectionDeformationRing ∧
            criterion.heckeAlgebraFiniteOverCoefficients ∧
              criterion.deformationToHeckeSurjective ∧
                criterion.kernelControlledByLengthComparison ∧
                  criterion.numericalEquality

/--
Checked bridge from the bundled numerical criterion to the three patching fields
consumed by the statement shape.
-/
theorem taylorWilesNumericalCriterion_to_patchingTriple
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {patched : TaylorWilesPatchedModuleData K coeffs G ρ M patch}
    (criterion : TaylorWilesNumericalCriterionData patched) :
    patch.taylorWilesNumericalCriterion ∧
      patch.patchedModuleFaithful ∧ patch.isREqualsT :=
  ⟨criterion.patchingNumericalCriterion,
    criterion.patchedModuleFaithful,
    criterion.rEqualsT⟩

/--
Checked bridge: a bundled numerical criterion yields the existing `R = T`
proposition in the patching package.
-/
theorem taylorWilesNumericalCriterion_yields_REqualsT
    {K : Type uK} {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {patched : TaylorWilesPatchedModuleData K coeffs G ρ M patch}
    (criterion : TaylorWilesNumericalCriterionData patched) :
    patch.isREqualsT :=
  criterion.rEqualsT

/-- Status of a P7 patched-module/numerical-criterion component. -/
inductive PatchingNumericalCriterionAuditStatus where
  | checkedBoundaryData
  | abstractCriterionBoundary
  | missingCommutativeAlgebraProof
  deriving DecidableEq, Repr

/-- One row of the P7 patching and numerical-criterion audit. -/
structure PatchingNumericalCriterionAuditRow where
  component : String
  repoLocalAnchors : List String
  selectedApi : String
  missingInterfaces : List String
  status : PatchingNumericalCriterionAuditStatus
  deriving Repr

/--
P7 audit rows for patched modules and the commutative-algebra numerical
criterion yielding `R = T`.
-/
def p7PatchingNumericalCriterionAudit : List PatchingNumericalCriterionAuditRow := [
  {
    component := "patched module object"
    repoLocalAnchors := [
      "TaylorWilesPatchedModuleData",
      "TaylorWilesPatchedModuleData.instPatchedDeformationModule",
      "TaylorWilesPatchedModuleData.instPatchedHeckeModule"
    ]
    selectedApi := "package a patched module with deformation-ring and Hecke-algebra module structures"
    missingInterfaces := [
      "construction of the inverse-limit patched module from finite-level cohomology",
      "topological completed tensor products and power-series algebra actions"
    ]
    status := PatchingNumericalCriterionAuditStatus.checkedBoundaryData
  },
  {
    component := "auxiliary-level tower compatibility"
    repoLocalAnchors := [
      "TaylorWilesAuxiliaryPrimeSystem",
      "TaylorWilesPatchedModuleData.patchingLevelTower",
      "TaylorWilesPatchedModuleData.SupportsNumericalCriterion"
    ]
    selectedApi := "record compatibility of the patched module with the Taylor-Wiles auxiliary-prime tower"
    missingInterfaces := [
      "finite-level module system indexed by auxiliary prime sets",
      "transition-map exactness and specialization theorems"
    ]
    status := PatchingNumericalCriterionAuditStatus.abstractCriterionBoundary
  },
  {
    component := "module finiteness and faithfulness"
    repoLocalAnchors := [
      "TaylorWilesPatchedModuleData.finiteGeneratedOverDeformationRing",
      "TaylorWilesPatchedModuleData.nearlyFaithfulOverDeformationRing",
      "TaylorWilesPatchedModuleData.supportControlsDeformationRing"
    ]
    selectedApi := "name the finite-generation, balancedness, near-faithfulness, and support-control hypotheses used by patching"
    missingInterfaces := [
      "finite-generation proof over the patched deformation ring",
      "commutative-algebra support and near-faithfulness lemmas"
    ]
    status := PatchingNumericalCriterionAuditStatus.abstractCriterionBoundary
  },
  {
    component := "numerical criterion inputs"
    repoLocalAnchors := [
      "TaylorWilesNumericalCriterionData",
      "TaylorWilesNumericalCriterionData.SatisfiesCommutativeAlgebraInputs"
    ]
    selectedApi := "bundle cotangent-dimension bounds, congruence-ideal length formulas, Fitting-ideal control, complete-intersection facts, and length comparison"
    missingInterfaces := [
      "cotangent-space and tangent-space dimension comparison",
      "proved congruence-ideal/Fitting-ideal length equality"
    ]
    status := PatchingNumericalCriterionAuditStatus.abstractCriterionBoundary
  },
  {
    component := "R equals T extraction"
    repoLocalAnchors := [
      "TaylorWilesPatchingData.deformationToHecke",
      "TaylorWilesPatchingData.isREqualsT",
      "taylorWilesNumericalCriterion_to_patchingTriple",
      "taylorWilesNumericalCriterion_yields_REqualsT"
    ]
    selectedApi := "provide checked bridge lemmas from a bundled numerical-criterion witness to the existing R = T proposition"
    missingInterfaces := [
      "proof that deformation-to-Hecke is an isomorphism rather than an abstract map with a proposition field",
      "ring-isomorphism-level replacement for the current proposition-valued R = T slot"
    ]
    status := PatchingNumericalCriterionAuditStatus.checkedBoundaryData
  },
  {
    component := "terminal commutative-algebra proof"
    repoLocalAnchors := [
      "absentTerminalSearchTerms"
    ]
    selectedApi := "no repo-local proof of the Taylor-Wiles numerical criterion is claimed"
    missingInterfaces := [
      "complete proof of the Wiles numerical criterion or patched-module variant",
      "integration of any external Lean proof by pin/import/check if one is later found"
    ]
    status := PatchingNumericalCriterionAuditStatus.missingCommutativeAlgebraProof
  }
]

/-- The P7 patching/numerical-criterion audit covers the six requested component families. -/
def p7PatchingNumericalCriterionAuditRowCount : Nat :=
  p7PatchingNumericalCriterionAudit.length

/-- Checked row-count witness for the P7 patching/numerical-criterion audit. -/
theorem p7PatchingNumericalCriterionAuditRowCount_eq :
    p7PatchingNumericalCriterionAuditRowCount = 6 :=
  rfl

/--
P7 completion status: the repo now has checked patched-module and numerical
criterion boundary data with bridge lemmas into the existing `R = T` slot, but
the real patched-module construction and commutative-algebra proof remain
formalization debt.
-/
def p7PatchingNumericalCriterionCompletionStatus : String :=
  "checked_patching_numerical_boundary; formalization_debt; not_repo_local_closed"

/-!
## P8 terminal modularity-lifting bridge

The following declarations isolate the final use of the Taylor-Wiles method:
once the residual modularity, local hypotheses, continuity/oddness of the lift,
and the `R = T` patching triple are available, a supplied terminal
`StatementShape` theorem yields modularity of the lift.  These lemmas are
checked applications of the statement boundary; they do not prove the missing
Taylor-Wiles theorem itself.
-/

/--
Terminal inputs consumed by the modularity-lifting conclusion.

This record is intentionally just the hypotheses already appearing in
`StatementShape`, bundled so the P8 package can pass them to a future terminal
Taylor-Wiles theorem without changing the public statement boundary.
-/
structure TerminalModularityLiftingInputs
    {K : Type uK} [Field K] [NumberField K]
    {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    (patch : TaylorWilesPatchingData K coeffs G ρ M)
    (lift : ρ.Rep) where
  coefficientRingComplete : coeffs.isCompleteNoetherianLocal
  coefficientRingAdicallyComplete : coeffs.isAdicallyComplete
  residueCharacteristicOdd : coeffs.residueCharacteristicOdd
  residualHypotheses : SelectedResidualHypotheses ρ M
  localHypotheses : SelectedLocalHypotheses patch lift
  liftContinuous : ρ.isContinuous lift
  liftOdd : ρ.isOdd lift
  patchingTriple :
    patch.taylorWilesNumericalCriterion ∧
      patch.patchedModuleFaithful ∧ patch.isREqualsT

/--
Checked P8 application lemma: a terminal `StatementShape` theorem applied to
the bundled residual, local, continuity, oddness, and `R = T` inputs gives the
modularity of the lift.
-/
theorem terminalModularityLifting_from_statementShape
    {K : Type uK} [Field K] [NumberField K]
    {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData K}
    {ρ : GaloisRepresentationData K coeffs G}
    {M : ModularSourceData K coeffs}
    {patch : TaylorWilesPatchingData K coeffs G ρ M}
    {lift : ρ.Rep}
    (terminalBridge : StatementShape K coeffs G ρ M patch lift)
    (inputs : TerminalModularityLiftingInputs patch lift) :
    IsModularLift ρ M :=
  terminalBridge
    inputs.coefficientRingComplete
    inputs.coefficientRingAdicallyComplete
    inputs.residueCharacteristicOdd
    inputs.residualHypotheses
    inputs.localHypotheses
    inputs.liftContinuous
    inputs.liftOdd
    inputs.patchingTriple

/--
Checked P8 application lemma for the selected `ℚ` variant.

This is the integration point a future proof should target after P1-P7 supply
the concrete theorem body behind `SelectedStatementShape`.
-/
theorem selectedTerminalModularityLifting_from_selectedStatementShape
    {coeffs : TaylorWilesCoefficientData}
    {G : GlobalGaloisGroupData SelectedBaseField}
    {ρ : GaloisRepresentationData SelectedBaseField coeffs G}
    {M : ModularSourceData SelectedBaseField coeffs}
    {patch : TaylorWilesPatchingData SelectedBaseField coeffs G ρ M}
    {lift : ρ.Rep}
    (terminalBridge : SelectedStatementShape coeffs G ρ M patch lift)
    (inputs : TerminalModularityLiftingInputs patch lift) :
    IsModularLift ρ M :=
  terminalModularityLifting_from_statementShape
    (K := SelectedBaseField)
    (terminalBridge := terminalBridge)
    inputs

/-- Status of a P8 terminal modularity-lifting component. -/
inductive TerminalModularityLiftingAuditStatus where
  | checkedApplicationBoundary
  | awaitingUpstreamPackage
  | missingTerminalProof
  deriving DecidableEq, Repr

/-- One row of the P8 terminal modularity-lifting audit. -/
structure TerminalModularityLiftingAuditRow where
  component : String
  repoLocalAnchors : List String
  selectedApi : String
  missingInterfaces : List String
  status : TerminalModularityLiftingAuditStatus
  deriving Repr

/--
P8 audit rows for deriving modularity of the lift from residual modularity,
local hypotheses, and the `R = T` package.
-/
def p8TerminalModularityLiftingAudit : List TerminalModularityLiftingAuditRow := [
  {
    component := "terminal input bundle"
    repoLocalAnchors := [
      "TerminalModularityLiftingInputs",
      "SelectedResidualHypotheses",
      "SelectedLocalHypotheses"
    ]
    selectedApi := "bundle exactly the residual, local, continuity, oddness, coefficient, and patching hypotheses consumed by StatementShape"
    missingInterfaces := [
      "concrete proofs of the residual and local hypotheses for a selected lift",
      "replacement of abstract proposition fields by the final Galois/Hecke/deformation APIs"
    ]
    status := TerminalModularityLiftingAuditStatus.checkedApplicationBoundary
  },
  {
    component := "R equals T terminal input"
    repoLocalAnchors := [
      "TaylorWilesNumericalCriterionData",
      "taylorWilesNumericalCriterion_to_patchingTriple",
      "TerminalModularityLiftingInputs.patchingTriple"
    ]
    selectedApi := "consume the same patching triple used by the P7 numerical-criterion bridge"
    missingInterfaces := [
      "ring-isomorphism-level R = T theorem",
      "proof that the selected lift corresponds to the localized Hecke eigenpacket through R = T"
    ]
    status := TerminalModularityLiftingAuditStatus.awaitingUpstreamPackage
  },
  {
    component := "generic terminal application"
    repoLocalAnchors := [
      "StatementShape",
      "terminalModularityLifting_from_statementShape"
    ]
    selectedApi := "apply a supplied terminal StatementShape theorem to the bundled inputs"
    missingInterfaces := [
      "proof of StatementShape from the Taylor-Wiles method",
      "full upstream P3-P7 proof packages feeding the terminal theorem"
    ]
    status := TerminalModularityLiftingAuditStatus.checkedApplicationBoundary
  },
  {
    component := "selected Q-variant terminal application"
    repoLocalAnchors := [
      "SelectedStatementShape",
      "selectedTerminalModularityLifting_from_selectedStatementShape"
    ]
    selectedApi := "specialize the terminal application to the selected minimal two-dimensional odd variant over Q"
    missingInterfaces := [
      "concrete SelectedStatementShape proof body",
      "repo-local pin/import/check of any external Lean 4 Taylor-Wiles proof if one is later found"
    ]
    status := TerminalModularityLiftingAuditStatus.checkedApplicationBoundary
  },
  {
    component := "terminal Taylor-Wiles proof"
    repoLocalAnchors := [
      "absentTerminalSearchTerms"
    ]
    selectedApi := "no repo-local terminal proof is claimed; the current artifact only fixes the final application interface"
    missingInterfaces := [
      "complete Lean 4 proof that residual modularity, local hypotheses, patching, and R = T imply IsModularLift",
      "public merge of P8 status after machine validation"
    ]
    status := TerminalModularityLiftingAuditStatus.missingTerminalProof
  }
]

/-- The P8 terminal modularity-lifting audit covers the five requested component families. -/
def p8TerminalModularityLiftingAuditRowCount : Nat :=
  p8TerminalModularityLiftingAudit.length

/-- Checked row-count witness for the P8 terminal modularity-lifting audit. -/
theorem p8TerminalModularityLiftingAuditRowCount_eq :
    p8TerminalModularityLiftingAuditRowCount = 5 :=
  rfl

/--
P8 completion status: the repo now has a checked terminal application boundary,
but the actual Taylor-Wiles theorem proving `StatementShape` remains
formalization debt.
-/
def p8TerminalModularityLiftingCompletionStatus : String :=
  "checked_terminal_application_boundary; formalization_debt; not_repo_local_closed"

/--
Search terms that did not locate a terminal Taylor-Wiles theorem in the current
repo-local Lean dependency closure.
-/
def absentTerminalSearchTerms : List String := [
  "Taylor-Wiles",
  "Taylor Wiles",
  "modularity lifting",
  "GaloisRepresentation",
  "deformation ring",
  "Hecke algebra",
  "R equals T",
  "minimal deformation",
  "semistable modularity"
]

/-!
## P9 repo-local closure gate

This section records the closure-gate audit requested by
`S1-M-065.P9.repo_local_closure_gate`.  The recorded external candidate is a
primary Lean 4 source branch, but it is not a completed terminal proof and must
not be used to mark the Taylor-Wiles theorem complete.
-/

/-- Status of an external Lean 4 terminal-proof candidate. -/
inductive ExternalTerminalProofStatus where
  | closedNoSorry
  | statementOrScaffoldOnly
  | blockedBySorryAx
  | notImported
  deriving DecidableEq, Repr

/-- One row in the P9 external-terminal-proof audit. -/
structure ExternalTerminalProofAuditRow where
  project : String
  repository : String
  ref : String
  fixedCommit : String
  relevantModules : List String
  observedEvidence : List String
  repoLocalAction : String
  status : ExternalTerminalProofStatus
  deriving Repr

/--
P9 external audit at fixed commits.

The FLT branch listed here is the strongest primary Lean 4 source located during
this child pass.  It is an integration blocker rather than a proof dependency:
the branch is an open PR adding a statement/scaffold and its exported FLT theorem
still reports `sorryAx` in the axiom list.
-/
def p9ExternalTerminalProofAudit : List ExternalTerminalProofAuditRow := [
  {
    project := "ImperialCollegeLondon/FLT"
    repository := "https://github.com/ImperialCollegeLondon/FLT"
    ref := "pull/757 branch kbuzzard-modularity-lifting-theorem"
    fixedCommit := "706be0f33118c4b502955c30768a82a7b35c9c03"
    relevantModules := [
      "FLT/GaloisRepresentation/ModularityLiftingTheorem.lean",
      "FLT/Basic/Reductions.lean",
      "FermatsLastTheorem.lean"
    ]
    observedEvidence := [
      "ModularityLiftingTheorem.lean contains a documented theorem-shape discussion, with the concrete definition commented out",
      "FermatsLastTheorem.lean prints that PNat.pow_add_pow_ne_pow depends on sorryAx",
      "lakefile.toml disables placeholder-proof warnings"
    ]
    repoLocalAction := "do not pin/import as a terminal proof; wait for a placeholder-free, no-new-axiom Lean 4 theorem and then test Lake pin/import/check before any public completion checkbox"
    status := ExternalTerminalProofStatus.blockedBySorryAx
  },
  {
    project := "repo-local pinned mathlib"
    repository := "https://github.com/leanprover-community/mathlib4"
    ref := "v4.29.0"
    fixedCommit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    relevantModules := [
      "Mathlib.FieldTheory.AbsoluteGaloisGroup",
      "Mathlib.NumberTheory.NumberField.AdeleRing",
      "Mathlib.NumberTheory.ModularForms.Basic",
      "Mathlib.NumberTheory.RamificationInertia.Basic"
    ]
    observedEvidence := [
      "local rg search found Taylor calculus and bibliography entries but no Taylor-Wiles modularity-lifting terminal theorem",
      "S1_M_065 imports checked object-model substrate only"
    ]
    repoLocalAction := "keep StatementShape and P1-P8 wrappers as formalization boundaries; no terminal wrapper can be written from mathlib alone"
    status := ExternalTerminalProofStatus.statementOrScaffoldOnly
  }
]

/-- The P9 external-terminal-proof audit records the FLT branch and pinned mathlib check. -/
def p9ExternalTerminalProofAuditRowCount : Nat :=
  p9ExternalTerminalProofAudit.length

/-- Checked row-count witness for the P9 external-terminal-proof audit. -/
theorem p9ExternalTerminalProofAuditRowCount_eq :
    p9ExternalTerminalProofAuditRowCount = 2 :=
  rfl

/--
P9 repo-local closure gate.

The gate is intentionally closed: no completed upstream Lean 4 terminal
Taylor-Wiles proof has been found and validated through this repository.
-/
def p9RepoLocalClosureGateAllowsCompletion : Bool :=
  false

/-- Checked witness that P9 does not allow a completion claim. -/
theorem p9RepoLocalClosureGateAllowsCompletion_eq_false :
    p9RepoLocalClosureGateAllowsCompletion = false :=
  rfl

/--
P9 debt result: there is no completed external proof to integrate yet, so the
remaining debt is formalization debt, not a completed-state
`repo_local_integration_debt`.
-/
def p9RepoLocalIntegrationDebtGateResult : String :=
  "open; no closed external Lean 4 terminal Taylor-Wiles proof located; formalization_debt remains; no completion checkbox may be set"

end AwesomeTheorems.Stage1.S1_M_065
