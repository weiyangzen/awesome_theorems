import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Manifold.Bordism
import Mathlib.Geometry.Manifold.Diffeomorph
import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance
import Mathlib.LinearAlgebra.BilinearForm.Properties
import Mathlib.LinearAlgebra.QuadraticForm.Signature

/-!
# S1-M-252 / THM-M-0615: classification of four-dimensional manifolds

This Stage1 artifact records a conservative Lean 4 statement boundary for the
topological and smooth classification of four-dimensional manifolds.

The pinned mathlib snapshot has finite-dimensional manifold structures,
diffeomorphisms and their underlying homeomorphisms, early bordism/singular
manifold infrastructure, singular homology functors, and quadratic-form
signature APIs.  It does not expose terminal Freedman, Donaldson,
Kirby-Siebenmann, intersection-form classification, gauge-theory, transversality,
or smooth/exotic four-manifold classification theorems.

Accordingly this file gives a typed statement shape and low-risk wrappers around
available mathlib anchors.  It does not prove the classification theorem.
-/

noncomputable section

open scoped Manifold ContDiff
open AlgebraicTopology CategoryTheory
open LinearMap (BilinForm)

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_252

/-- The Euclidean model space for a four-dimensional manifold. -/
abbrev Euclidean4 : Type :=
  EuclideanSpace ℝ (Fin 4)

/-- The standard smooth model with corners used for smooth four-manifolds. -/
abbrev SmoothModel4 : ModelWithCorners ℝ Euclidean4 Euclidean4 :=
  𝓘(ℝ, Euclidean4)

/--
Checked blocker tags for topological invariant APIs needed by the
four-manifold classification statement.

These are not mathematical assumptions.  They record which part of the desired
invariant package is still missing from the current mathlib surface.
-/
inductive TopologicalInvariantApiBlocker : Type
  | singularHomologyNoCanonicalClosedFourManifoldH2
  | kirbySiebenmannNoMathlibCharacteristicClassApi
  deriving DecidableEq, Repr

/--
Checked blocker tags for constructing the four-manifold intersection pairing
from singular homology/cohomology.

These tags deliberately separate the locally checked algebraic bilinear-form
constructor below from the missing topological construction.  A terminal
intersection-form formalization still needs canonical cohomology, cup product,
fundamental-class evaluation, and Poincare-duality APIs for closed oriented
four-manifolds.
-/
inductive IntersectionPairingConstructionBlocker : Type
  | noCanonicalClosedFourManifoldCohomologyH2
  | noCupProductFundamentalClassEvaluationApi
  | noPoincareDualityForClosedFourManifolds
  deriving DecidableEq, Repr

/--
Degree-two singular homology model data for a four-manifold.

Mathlib provides the category-level `singularHomologyFunctor`, but this checkout
does not yet expose a canonical closed-four-manifold API that extracts the
degree-two singular homology object as the bundled `ℤ`-module used by the
intersection-form field below.
-/
structure SingularHomologyModel
    (M : Type u) [TopologicalSpace M]
    (H2 : Type v) [AddCommGroup H2] [Module ℤ H2] : Type where
  degree : ℕ
  degree_eq_two : degree = 2
  apiAnchor : String
  apiAnchor_eq : apiAnchor = "singularHomologyFunctor"
  apiBlocker : TopologicalInvariantApiBlocker
  apiBlocker_eq :
    apiBlocker =
      TopologicalInvariantApiBlocker.singularHomologyNoCanonicalClosedFourManifoldH2

/-- A concrete model of the basepointed fundamental group using mathlib's `FundamentalGroup`. -/
structure FundamentalGroupModel
    (M : Type u) [TopologicalSpace M] : Type (max u (v + 1)) where
  basepoint : M
  groupModel : Type v
  [groupModelGroup : Group groupModel]
  fundamentalGroupEquiv : groupModel ≃* FundamentalGroup M basepoint

attribute [instance] FundamentalGroupModel.groupModelGroup

/--
Kirby-Siebenmann obstruction data.

The value is recorded as a `ZMod 2` class, while the accompanying blocker marks
that mathlib does not currently provide the topological tangent microbundle,
classifying-space, or characteristic-class API needed to define this obstruction
canonically for a closed topological four-manifold.
-/
structure KirbySiebenmannModel
    (M : Type u) [TopologicalSpace M] [ChartedSpace Euclidean4 M] : Type where
  obstruction : ZMod 2
  apiBlocker : TopologicalInvariantApiBlocker
  apiBlocker_eq :
    apiBlocker =
      TopologicalInvariantApiBlocker.kirbySiebenmannNoMathlibCharacteristicClassApi

/--
Build a `BilinForm` from a raw integer-valued pairing once bilinearity in both
arguments has been supplied.

This is the checked algebraic constructor needed by the intersection-form leaf.
It is not, by itself, the topological construction of the pairing from cup
product and fundamental-class evaluation.
-/
def bilinearFormOfPairing
    {R : Type u} [CommRing R]
    {H2 : Type v} [AddCommGroup H2] [Module R H2]
    (b : H2 → H2 → R)
    (map_add_left : ∀ x y z : H2, b (x + y) z = b x z + b y z)
    (map_smul_left : ∀ (a : R) (x y : H2), b (a • x) y = a • b x y)
    (map_add_right : ∀ x y z : H2, b x (y + z) = b x y + b x z)
    (map_smul_right : ∀ (a : R) (x y : H2), b x (a • y) = a • b x y) :
    BilinForm R H2 :=
  { toFun := fun x =>
      { toFun := fun y => b x y
        map_add' := fun y z => map_add_right x y z
        map_smul' := fun a y => map_smul_right a x y }
    map_add' := fun x y => by
      ext z
      exact map_add_left x y z
    map_smul' := fun a x => by
      ext y
      exact map_smul_left a x y }

/-- Raw bilinear-pairing data over a commutative ring. -/
structure BilinearPairingData
    (R : Type u) [CommRing R]
    (H : Type v) [AddCommGroup H] [Module R H] : Type (max u v) where
  rawPairing : H → H → R
  map_add_left : ∀ x y z : H, rawPairing (x + y) z = rawPairing x z + rawPairing y z
  map_smul_left : ∀ (a : R) (x y : H), rawPairing (a • x) y = a • rawPairing x y
  map_add_right : ∀ x y z : H, rawPairing x (y + z) = rawPairing x y + rawPairing x z
  map_smul_right : ∀ (a : R) (x y : H), rawPairing x (a • y) = a • rawPairing x y

namespace BilinearPairingData

/-- Convert raw bilinear-pairing data into mathlib's `BilinForm`. -/
def toBilinForm
    {R : Type u} [CommRing R]
    {H : Type v} [AddCommGroup H] [Module R H]
    (D : BilinearPairingData R H) : BilinForm R H :=
  bilinearFormOfPairing D.rawPairing D.map_add_left D.map_smul_left
    D.map_add_right D.map_smul_right

@[simp]
theorem toBilinForm_apply
    {R : Type u} [CommRing R]
    {H : Type v} [AddCommGroup H] [Module R H]
    (D : BilinearPairingData R H) (x y : H) :
    D.toBilinForm x y = D.rawPairing x y :=
  rfl

end BilinearPairingData

/--
Local construction data for an intersection pairing on the chosen `H2` model.

The `rawPairing` fields give a checked route to a `BilinForm ℤ H2`.  The
`constructionBlockers` field records why this data is still supplied as input:
the current repository/mathlib surface does not yet construct it canonically
from singular cohomology, cup product, Poincare duality, and evaluation on a
fundamental class of a closed oriented four-manifold.
-/
structure IntersectionPairingConstructionData
    (M : Type u) [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    (H2 : Type v) [AddCommGroup H2] [Module ℤ H2] : Type (max u v) where
  homologyModel : SingularHomologyModel M H2
  pairingData : BilinearPairingData ℤ H2
  rawPairing_symm : ∀ x y : H2, pairingData.rawPairing x y = pairingData.rawPairing y x
  toBilinFormNondegenerate : pairingData.toBilinForm.Nondegenerate
  constructionBlockers : List IntersectionPairingConstructionBlocker
  constructionBlockers_eq :
    constructionBlockers = [
      IntersectionPairingConstructionBlocker.noCanonicalClosedFourManifoldCohomologyH2,
      IntersectionPairingConstructionBlocker.noCupProductFundamentalClassEvaluationApi,
      IntersectionPairingConstructionBlocker.noPoincareDualityForClosedFourManifolds
    ]

namespace IntersectionPairingConstructionData

/-- The checked bilinear form produced from the supplied pairing laws. -/
def toBilinForm
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {H2 : Type v} [AddCommGroup H2] [Module ℤ H2]
    (D : IntersectionPairingConstructionData M H2) : BilinForm ℤ H2 :=
  D.pairingData.toBilinForm

@[simp]
theorem toBilinForm_apply
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {H2 : Type v} [AddCommGroup H2] [Module ℤ H2]
    (D : IntersectionPairingConstructionData M H2) (x y : H2) :
    D.toBilinForm x y = D.pairingData.rawPairing x y :=
  rfl

/-- The constructed bilinear form is symmetric when the raw pairing is symmetric. -/
theorem toBilinForm_isSymm
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {H2 : Type v} [AddCommGroup H2] [Module ℤ H2]
    (D : IntersectionPairingConstructionData M H2) :
    D.toBilinForm.IsSymm :=
  ⟨fun x y => D.rawPairing_symm x y⟩

/-- Nondegeneracy is carried from the supplied construction datum. -/
theorem toBilinForm_nondegenerate
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {H2 : Type v} [AddCommGroup H2] [Module ℤ H2]
    (D : IntersectionPairingConstructionData M H2) :
    D.toBilinForm.Nondegenerate :=
  D.toBilinFormNondegenerate

end IntersectionPairingConstructionData

/--
Boundary data for algebraic-topological invariants of a closed topological
four-manifold.

The intended mathematical payload is the second homology module with its
intersection form, the Kirby-Siebenmann obstruction, orientation data, and
basic homology/fundamental-group hypotheses.  The homology and
Kirby-Siebenmann fields carry precise API blockers instead of free proposition
placeholders where this mathlib checkout lacks the desired canonical
four-manifold invariant API.
-/
structure FourManifoldInvariants
    (M : Type u) [TopologicalSpace M] [ChartedSpace Euclidean4 M] : Type (max u (v + 1)) where
  H2 : Type v
  [h2Add : AddCommGroup H2]
  [h2Module : Module ℤ H2]
  intersectionForm : BilinForm ℤ H2
  intersectionFormSymm : intersectionForm.IsSymm
  intersectionFormNondegenerate : intersectionForm.Nondegenerate
  kirbySiebenmann : KirbySiebenmannModel M
  orientationData : Prop
  homologyModel : SingularHomologyModel M H2
  fundamentalGroupModel : FundamentalGroupModel.{u, v} M

attribute [instance] FourManifoldInvariants.h2Add FourManifoldInvariants.h2Module

/--
Build the invariant package from checked intersection-pairing construction
data plus the remaining Kirby-Siebenmann, orientation, and fundamental-group
inputs.

This closes the algebraic packaging step for `S1-M-252.intersection-form`.
It still requires a future topological construction of
`IntersectionPairingConstructionData` from homology/cohomology infrastructure.
-/
def fourManifoldInvariantsOfIntersectionPairingData
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {H2 : Type v} [AddCommGroup H2] [Module ℤ H2]
    (D : IntersectionPairingConstructionData M H2)
    (K : KirbySiebenmannModel M)
    (orientationData : Prop)
    (G : FundamentalGroupModel.{u, v} M) :
    FourManifoldInvariants.{u, v} M where
  H2 := H2
  intersectionForm := D.toBilinForm
  intersectionFormSymm := D.toBilinForm_isSymm
  intersectionFormNondegenerate := D.toBilinForm_nondegenerate
  kirbySiebenmann := K
  orientationData := orientationData
  homologyModel := D.homologyModel
  fundamentalGroupModel := G

/--
Current status of the intersection-form child leaf.

The algebraic conversion from explicit bilinear pairing data to
`BilinForm ℤ H2` is checked in this file, but the topological construction
from homology/cohomology remains open formalization debt.
-/
def intersectionPairingConstructionStatus : String :=
  "checked algebraic BilinForm packaging; canonical cup-product/Poincare-duality construction still missing"

/-- Missing APIs before the intersection pairing is constructed topologically. -/
def intersectionPairingMissingApis : List String := [
  "canonical closed oriented four-manifold H2/cohomology model",
  "singular cohomology cup product for the selected coefficient category",
  "fundamental class and evaluation pairing",
  "Poincare duality for closed oriented four-manifolds",
  "proof that the resulting integral pairing is symmetric and nondegenerate"
]

/-- This child must not be marked completed from the current local evidence alone. -/
def intersectionPairingCompletionClaimAllowed : Bool :=
  false

theorem intersectionPairingMissingApis_eq :
    intersectionPairingMissingApis = [
      "canonical closed oriented four-manifold H2/cohomology model",
      "singular cohomology cup product for the selected coefficient category",
      "fundamental class and evaluation pairing",
      "Poincare duality for closed oriented four-manifolds",
      "proof that the resulting integral pairing is symmetric and nondegenerate"
    ] :=
  rfl

theorem intersectionPairingCompletionClaimAllowed_eq_false :
    intersectionPairingCompletionClaimAllowed = false :=
  rfl

/-- Isometry of the recorded intersection forms, allowing different `H2` models. -/
def IntersectionFormsEquivalent
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Prop :=
  ∃ e : XM.H2 ≃ₗ[ℤ] XN.H2,
    ∀ x y : XM.H2, XN.intersectionForm (e x) (e y) = XM.intersectionForm x y

/-- Compatibility of the recorded degree-two singular homology model anchors. -/
def SingularHomologyModelsCompatible
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Prop :=
  XM.homologyModel.degree = XN.homologyModel.degree ∧
    XM.homologyModel.apiAnchor = XN.homologyModel.apiAnchor ∧
      XM.homologyModel.apiBlocker = XN.homologyModel.apiBlocker

/-- Compatibility of the recorded Kirby-Siebenmann obstruction model anchors. -/
def KirbySiebenmannModelsCompatible
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Prop :=
  XM.kirbySiebenmann.obstruction = XN.kirbySiebenmann.obstruction ∧
    XM.kirbySiebenmann.apiBlocker = XN.kirbySiebenmann.apiBlocker

/-- Equivalence of the concrete basepointed fundamental-group models. -/
def FundamentalGroupModelsEquivalent
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Prop :=
  Nonempty (XM.fundamentalGroupModel.groupModel ≃* XN.fundamentalGroupModel.groupModel)

/--
Sameness of the topological invariant package used by a future Freedman-style
classification statement.
-/
def SameTopologicalInvariants
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Prop :=
  IntersectionFormsEquivalent XM XN ∧
    KirbySiebenmannModelsCompatible XM XN ∧
      (XM.orientationData ↔ XN.orientationData) ∧
        SingularHomologyModelsCompatible XM XN ∧
          FundamentalGroupModelsEquivalent XM XN

/-- Normalized hypotheses for the topological classification boundary. -/
def TopologicalClassificationHypotheses
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Prop :=
  SameTopologicalInvariants XM XN

/-- Conclusion shape for topological classification: a homeomorphism exists. -/
def TopologicalClassificationConclusion
    (M : Type u) (N : Type w) [TopologicalSpace M] [TopologicalSpace N] : Prop :=
  Nonempty (M ≃ₜ N)

/--
Checked blocker tags for the Freedman classification bridge.

These tags record why the current repository cannot turn equality of the
intersection form and Kirby-Siebenmann data into a homeomorphism without a
future local proof body or a pinned/imported/checked external Lean 4 source.
-/
inductive FreedmanBridgeBlocker : Type
  | noRepoLocalFreedmanClassificationTheorem
  | noDiskEmbeddingOrSurgeryPackage
  | noClosedSimplyConnectedTopologicalFourManifoldApi
  | noCanonicalIntersectionFormConstruction
  | noKirbySiebenmannCharacteristicClassApi
  deriving DecidableEq, Repr

/--
Boundary hypotheses for the simply connected Freedman-style bridge.

This deliberately isolates the bridge requested by `S1-M-252.freedman-bridge`:
intersection-form equivalence plus Kirby-Siebenmann compatibility and the
closed simply connected topological four-manifold side conditions should imply
a homeomorphism.  The side conditions remain proposition-valued until mathlib
or a pinned dependency supplies the corresponding canonical APIs.
-/
def FreedmanBridgeHypotheses
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N)
    (closedSimplyConnectedM closedSimplyConnectedN : Prop) : Prop :=
  IntersectionFormsEquivalent XM XN ∧
    KirbySiebenmannModelsCompatible XM XN ∧
      (XM.orientationData ↔ XN.orientationData) ∧
        closedSimplyConnectedM ∧ closedSimplyConnectedN

/--
Formal boundary for a future Freedman classification bridge.

An inhabitant of this structure would be supplied by a future local proof body
or by a pinned/imported/checked external Lean 4 dependency.  This file does not
construct such an inhabitant; it only fixes the interface and the current
integration blockers.
-/
structure FreedmanClassificationBridgeData
    (M : Type u) (N : Type w) [TopologicalSpace M] [TopologicalSpace N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N]
    (XM : FourManifoldInvariants.{u, v} M)
    (XN : FourManifoldInvariants.{w, v} N) : Type (max u v w) where
  closedSimplyConnectedM : Prop
  closedSimplyConnectedN : Prop
  bridge :
    FreedmanBridgeHypotheses XM XN closedSimplyConnectedM closedSimplyConnectedN →
      TopologicalClassificationConclusion M N
  blockers : List FreedmanBridgeBlocker
  blockers_eq :
    blockers = [
      FreedmanBridgeBlocker.noRepoLocalFreedmanClassificationTheorem,
      FreedmanBridgeBlocker.noDiskEmbeddingOrSurgeryPackage,
      FreedmanBridgeBlocker.noClosedSimplyConnectedTopologicalFourManifoldApi,
      FreedmanBridgeBlocker.noCanonicalIntersectionFormConstruction,
      FreedmanBridgeBlocker.noKirbySiebenmannCharacteristicClassApi
    ]
  repoLocalClosureStatus : String
  repoLocalClosureStatus_eq :
    repoLocalClosureStatus =
      "not_repo_local_closed; no local proof body or pinned external Freedman bridge"

namespace FreedmanClassificationBridgeData

/--
If a future checked Freedman bridge datum is supplied, it can be applied to the
recorded intersection-form and Kirby-Siebenmann hypotheses to produce the
topological classification conclusion.
-/
theorem apply
    {M : Type u} {N : Type w} [TopologicalSpace M] [TopologicalSpace N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N]
    {XM : FourManifoldInvariants.{u, v} M}
    {XN : FourManifoldInvariants.{w, v} N}
    (D : FreedmanClassificationBridgeData M N XM XN)
    (hForms : IntersectionFormsEquivalent XM XN)
    (hKS : KirbySiebenmannModelsCompatible XM XN)
    (hOrient : XM.orientationData ↔ XN.orientationData)
    (hM : D.closedSimplyConnectedM)
    (hN : D.closedSimplyConnectedN) :
    TopologicalClassificationConclusion M N :=
  D.bridge ⟨hForms, hKS, hOrient, hM, hN⟩

end FreedmanClassificationBridgeData

/-!
The declarations below are checked audit metadata.  They are not theorem
evidence for Freedman's classification theorem.
-/

/-- Current repo-local status of the Freedman bridge child. -/
def freedmanBridgeStatus : String :=
  "interface_checked_only; terminal Freedman classification bridge remains formalization_debt"

/-- Missing APIs or proof packages before the Freedman bridge can be closed locally. -/
def freedmanBridgeMissingApis : List String := [
  "repo-local or pinned external Lean 4 Freedman classification theorem",
  "closed simply connected topological four-manifold API",
  "topological surgery, h-cobordism, and disk-embedding theorem infrastructure",
  "canonical four-manifold intersection form construction",
  "Kirby-Siebenmann characteristic-class API in H^4(M; ZMod 2)",
  "homeomorphism conclusion specialized to the selected closed simply connected theorem"
]

/-- This child must not be marked completed from the current local evidence alone. -/
def freedmanBridgeCompletionClaimAllowed : Bool :=
  false

theorem freedmanBridgeMissingApis_eq :
    freedmanBridgeMissingApis = [
      "repo-local or pinned external Lean 4 Freedman classification theorem",
      "closed simply connected topological four-manifold API",
      "topological surgery, h-cobordism, and disk-embedding theorem infrastructure",
      "canonical four-manifold intersection form construction",
      "Kirby-Siebenmann characteristic-class API in H^4(M; ZMod 2)",
      "homeomorphism conclusion specialized to the selected closed simply connected theorem"
    ] :=
  rfl

theorem freedmanBridgeCompletionClaimAllowed_eq_false :
    freedmanBridgeCompletionClaimAllowed = false :=
  rfl

/-- Checked bookkeeping record for the external Lean 4 Freedman-source audit. -/
structure FreedmanExternalSearchAudit where
  searchDate : String
  localMathlibRevision : String
  authenticatedGithubCodeSearchAvailable : Bool
  localTerminalLeanProofFound : Bool
  externalTerminalLeanProofFound : Bool
  searchedTerms : List String
  integrationDecision : String

/-- C005 audit result: no terminal Lean 4 Freedman bridge source was found. -/
def freedmanExternalSearchAudit : FreedmanExternalSearchAudit where
  searchDate := "2026-05-01"
  localMathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  authenticatedGithubCodeSearchAvailable := false
  localTerminalLeanProofFound := false
  externalTerminalLeanProofFound := false
  searchedTerms := [
    "Freedman",
    "Kirby-Siebenmann",
    "KirbySiebenmann",
    "fourManifold",
    "four-manifold classification",
    "intersection form classification",
    "Donaldson",
    "SeibergWitten"
  ]
  integrationDecision :=
    "no pin/import/check target identified; keep bridge open as formalization_debt"

theorem freedmanExternalSearchAudit_no_external_terminal :
    freedmanExternalSearchAudit.externalTerminalLeanProofFound = false :=
  rfl

theorem freedmanExternalSearchAudit_no_local_terminal :
    freedmanExternalSearchAudit.localTerminalLeanProofFound = false :=
  rfl

/--
Checked blocker tags for the smooth four-manifold branch.

These tags keep the Donaldson obstruction and smooth/exotic distinguishing
routes separate from any future complete smooth classification theorem.
-/
inductive SmoothBranchBlocker : Type
  | noRepoLocalDonaldsonDiagonalizationTheorem
  | noGaugeTheoryModuliSpaceApi
  | noSmoothIntersectionFormObstructionApi
  | noSeibergWittenOrDonaldsonInvariantApi
  | noExoticSmoothStructureDistinguishingTheorem
  | noCompleteSmoothClassificationInvariant
  deriving DecidableEq, Repr

/--
Boundary data for smooth four-manifold classification branches.

The fields mark formalization gaps.  Donaldson-style obstruction data,
Seiberg-Witten/Donaldson invariant data, and exotic smooth-structure
distinguishing data are recorded as separate proposition-valued branches instead
of being collapsed into a single alleged complete invariant package.
-/
structure SmoothFourManifoldData
    (M : Type u) [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [IsManifold SmoothModel4 ∞ M] : Type (u + 1) where
  smoothInvariantPackage : Prop
  donaldsonGaugeTheoryPackage : Prop
  donaldsonDefiniteIntersectionForm : Prop
  donaldsonDiagonalIntersectionForm : Prop
  seibergWittenGaugeTheoryPackage : Prop
  smoothStructureInvariantPackage : Prop
  exoticSmoothStructureBoundary : Prop
  exoticDistinguishingInvariantMismatch : Prop

/-- Sameness of the currently recorded smooth-invariant packages. -/
def SameSmoothInvariants
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [IsManifold SmoothModel4 ∞ M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    [IsManifold SmoothModel4 ∞ N]
    (SM : SmoothFourManifoldData M) (SN : SmoothFourManifoldData N) : Prop :=
  (SM.smoothInvariantPackage ↔ SN.smoothInvariantPackage) ∧
    (SM.donaldsonGaugeTheoryPackage ↔ SN.donaldsonGaugeTheoryPackage) ∧
      (SM.donaldsonDefiniteIntersectionForm ↔ SN.donaldsonDefiniteIntersectionForm) ∧
        (SM.donaldsonDiagonalIntersectionForm ↔ SN.donaldsonDiagonalIntersectionForm) ∧
          (SM.seibergWittenGaugeTheoryPackage ↔ SN.seibergWittenGaugeTheoryPackage) ∧
            (SM.smoothStructureInvariantPackage ↔ SN.smoothStructureInvariantPackage) ∧
              (SM.exoticSmoothStructureBoundary ↔ SN.exoticSmoothStructureBoundary) ∧
                (SM.exoticDistinguishingInvariantMismatch ↔
                  SN.exoticDistinguishingInvariantMismatch)

/--
Blocked complete-invariant hypotheses for a future smooth classification
bridge.

This definition is retained as an interface only.  It is deliberately not used
by `SmoothStatementShape`, because the current safe Stage1 smooth surface is
split into Donaldson obstruction and exotic/distinguishing branches.
-/
def SmoothClassificationHypotheses
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [IsManifold SmoothModel4 ∞ M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    [IsManifold SmoothModel4 ∞ N]
    (SM : SmoothFourManifoldData M) (SN : SmoothFourManifoldData N) : Prop :=
  SM.smoothInvariantPackage ∧
    SN.smoothInvariantPackage ∧
      SM.donaldsonGaugeTheoryPackage ∧
        SN.donaldsonGaugeTheoryPackage ∧
          SameSmoothInvariants SM SN

/-- Conclusion shape for smooth classification: a diffeomorphism exists. -/
def SmoothClassificationConclusion
    (M : Type u) (N : Type w) [TopologicalSpace M] [TopologicalSpace N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N] : Prop :=
  Nonempty (M ≃ₘ⟮SmoothModel4, SmoothModel4⟯ N)

/-- Hypotheses for the Donaldson diagonalization obstruction branch. -/
def DonaldsonObstructionHypotheses
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [IsManifold SmoothModel4 ∞ M]
    (XM : FourManifoldInvariants.{u, v} M)
    (SM : SmoothFourManifoldData M) : Prop :=
  SM.donaldsonGaugeTheoryPackage ∧
    SM.donaldsonDefiniteIntersectionForm ∧
      XM.intersectionForm.Nondegenerate

/-- Conclusion boundary for the Donaldson obstruction branch. -/
def DonaldsonObstructionConclusion
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [IsManifold SmoothModel4 ∞ M]
    (_XM : FourManifoldInvariants.{u, v} M)
    (SM : SmoothFourManifoldData M) : Prop :=
  SM.donaldsonDiagonalIntersectionForm

/--
Statement shape for the Donaldson obstruction branch.

Mathematically, this is the branch saying that a smooth closed simply connected
four-manifold with definite intersection form is constrained by Donaldson's
diagonalization theorem.  The closed/simply connected side conditions are still
part of the proposition-valued smooth data until a canonical four-manifold API
is available in the local dependency closure.
-/
def DonaldsonObstructionStatementShape : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace Euclidean4 M] [CompactSpace M]
    [IsManifold SmoothModel4 ∞ M],
      ∀ (XM : FourManifoldInvariants.{u, v} M)
        (SM : SmoothFourManifoldData M),
        DonaldsonObstructionHypotheses XM SM →
          DonaldsonObstructionConclusion XM SM

/-- Hypotheses for the smooth/exotic-structure distinguishing branch. -/
def ExoticStructureDistinguishingHypotheses
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [IsManifold SmoothModel4 ∞ M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    [IsManifold SmoothModel4 ∞ N]
    (SM : SmoothFourManifoldData M) (SN : SmoothFourManifoldData N) : Prop :=
  SM.smoothStructureInvariantPackage ∧
    SN.smoothStructureInvariantPackage ∧
      (SM.exoticSmoothStructureBoundary ∨ SN.exoticSmoothStructureBoundary) ∧
        (SM.exoticDistinguishingInvariantMismatch ∨ SN.exoticDistinguishingInvariantMismatch)

/-- Conclusion boundary for distinguishing homeomorphic but non-diffeomorphic structures. -/
def ExoticStructureDistinguishingConclusion
    (M : Type u) (N : Type w) [TopologicalSpace M] [TopologicalSpace N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N] : Prop :=
  TopologicalClassificationConclusion M N ∧ ¬ SmoothClassificationConclusion M N

/--
Statement shape for the smooth/exotic-structure distinguishing branch.

This branch records the valid target shape for exotic phenomena: a topological
identification together with smooth invariants that obstruct a diffeomorphism.
It is intentionally weaker and safer than a complete smooth classification
theorem.
-/
def ExoticStructureDistinguishingStatementShape : Prop :=
  ∀ (M : Type u) (N : Type w) [TopologicalSpace M] [TopologicalSpace N]
    [T2Space M] [T2Space N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N]
    [CompactSpace M] [CompactSpace N]
    [IsManifold SmoothModel4 ∞ M] [IsManifold SmoothModel4 ∞ N],
      ∀ (XM : FourManifoldInvariants.{u, v} M)
        (XN : FourManifoldInvariants.{w, v} N)
        (SM : SmoothFourManifoldData M) (SN : SmoothFourManifoldData N),
        TopologicalClassificationHypotheses XM XN →
          ExoticStructureDistinguishingHypotheses SM SN →
            ExoticStructureDistinguishingConclusion M N

/-- Split smooth statement boundary used by Stage1. -/
def SmoothBranchStatementShape : Prop :=
  DonaldsonObstructionStatementShape.{u, v} ∧
    ExoticStructureDistinguishingStatementShape.{u, v, w}

/--
Topological four-manifold classification statement boundary.

This is a normalized proposition only.  A future proof must supply the actual
Freedman/Kirby-Siebenmann classification bridge under the stated hypotheses.
-/
def TopologicalStatementShape : Prop :=
  ∀ (M : Type u) (N : Type w) [TopologicalSpace M] [TopologicalSpace N]
    [T2Space M] [T2Space N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N]
    [CompactSpace M] [CompactSpace N],
      ∀ (XM : FourManifoldInvariants.{u, v} M)
        (XN : FourManifoldInvariants.{w, v} N),
        TopologicalClassificationHypotheses XM XN →
          TopologicalClassificationConclusion M N

/--
Smooth four-manifold statement boundary.

This is a normalized proposition only.  It splits the smooth side into
Donaldson obstruction and smooth/exotic distinguishing branches, rather than
asserting that one recorded invariant package is a complete smooth
classification invariant.
-/
def SmoothStatementShape : Prop :=
  SmoothBranchStatementShape.{u, v, w}

/-!
The declarations below are checked audit metadata for the smooth branch.  They
are not theorem evidence for Donaldson's theorem, Seiberg-Witten theory, or a
complete smooth classification of four-manifolds.
-/

/-- Current repo-local status of the smooth classification branch. -/
def smoothBranchStatus : String :=
  "split_statement_boundary_only; Donaldson and exotic smooth-structure branches remain formalization_debt"

/-- Missing APIs or proof packages before the smooth branch can be closed locally. -/
def smoothBranchMissingApis : List String := [
  "repo-local or pinned external Lean 4 Donaldson diagonalization theorem",
  "gauge-theory moduli-space and transversality infrastructure",
  "smooth closed simply connected four-manifold API",
  "definite integral intersection-form diagonalization interface",
  "Donaldson or Seiberg-Witten invariant package for distinguishing smooth structures",
  "homeomorphic but non-diffeomorphic exotic smooth-structure theorem"
]

/-- This child must not be marked completed from the current local evidence alone. -/
def smoothBranchCompletionClaimAllowed : Bool :=
  false

/-- A single complete smooth invariant theorem is not available in this repo-local closure. -/
def smoothSingleCompleteInvariantClaimAllowed : Bool :=
  false

theorem smoothBranchMissingApis_eq :
    smoothBranchMissingApis = [
      "repo-local or pinned external Lean 4 Donaldson diagonalization theorem",
      "gauge-theory moduli-space and transversality infrastructure",
      "smooth closed simply connected four-manifold API",
      "definite integral intersection-form diagonalization interface",
      "Donaldson or Seiberg-Witten invariant package for distinguishing smooth structures",
      "homeomorphic but non-diffeomorphic exotic smooth-structure theorem"
    ] :=
  rfl

theorem smoothBranchCompletionClaimAllowed_eq_false :
    smoothBranchCompletionClaimAllowed = false :=
  rfl

theorem smoothSingleCompleteInvariantClaimAllowed_eq_false :
    smoothSingleCompleteInvariantClaimAllowed = false :=
  rfl

/-!
The declarations below are checked audit metadata for the C007 external search
pass.  They record that this worker did not obtain authenticated GitHub code
search results and therefore found no pin/import/check target for a terminal
four-manifold classification proof.
-/

/-- Checked bookkeeping record for the combined external Lean 4 source audit. -/
structure FourManifoldExternalSourceAudit where
  searchDate : String
  localMathlibRevision : String
  githubCliAuthenticated : Bool
  authenticatedGithubCodeSearchAttempted : Bool
  authenticatedGithubCodeSearchAvailable : Bool
  localMathlibTerminalProofFound : Bool
  externalPrimaryLean4SourceFound : Bool
  terminalFourManifoldClassificationProofFound : Bool
  searchedTerms : List String
  foundCommitShas : List String
  foundTheoremNames : List String
  foundToolchains : List String
  integrationFeasibility : String
  repoLocalIntegrationDebtGate : String

/--
C007 audit result for external primary Lean 4 sources.

The required authenticated GitHub code search could not be completed in this
environment because `gh auth status` reported no authenticated GitHub host and
no GitHub token was available.  Fallback local and public-web searches did not
identify a terminal Lean 4 source containing the requested four-manifold
classification components.
-/
def fourManifoldExternalSourceAudit : FourManifoldExternalSourceAudit where
  searchDate := "2026-05-01"
  localMathlibRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  githubCliAuthenticated := false
  authenticatedGithubCodeSearchAttempted := true
  authenticatedGithubCodeSearchAvailable := false
  localMathlibTerminalProofFound := false
  externalPrimaryLean4SourceFound := false
  terminalFourManifoldClassificationProofFound := false
  searchedTerms := [
    "Freedman",
    "Donaldson",
    "KirbySiebenmann",
    "SeibergWitten",
    "fourManifold"
  ]
  foundCommitShas := []
  foundTheoremNames := []
  foundToolchains := []
  integrationFeasibility :=
    "no pin/import/check target identified; authenticated GitHub code search is blocked by missing credentials"
  repoLocalIntegrationDebtGate :=
    "passed for non-completion: no external Lean 4 primary source is claimed as completed or anchor-only integrated"

theorem fourManifoldExternalSourceAudit_no_authenticated_code_search :
    fourManifoldExternalSourceAudit.authenticatedGithubCodeSearchAvailable = false :=
  rfl

theorem fourManifoldExternalSourceAudit_no_terminal_external_proof :
    fourManifoldExternalSourceAudit.terminalFourManifoldClassificationProofFound = false :=
  rfl

theorem fourManifoldExternalSourceAudit_no_anchor_only_completion :
    fourManifoldExternalSourceAudit.repoLocalIntegrationDebtGate =
      "passed for non-completion: no external Lean 4 primary source is claimed as completed or anchor-only integrated" :=
  rfl

/-!
The declarations below are checked audit metadata for the C008 integration
gate.  They keep the public completion state open until the Lean validation
record, theorem-tree ledger, public merge target, and repo-local integration
debt gate are synchronized by a serial integrator.
-/

/-- Checked bookkeeping record for the C008 integration gate. -/
structure IntegrationGateStatus where
  childTask : String
  leanValidationCommand : String
  leanValidationArtifactPresent : Bool
  theoremTreeLedgerPresent : Bool
  terminalTheoremLeavesClosed : Bool
  publicMergeTargetSynchronized : Bool
  terminalRepoLocalClosure : Bool
  repoLocalIntegrationDebtInCompletedState : Bool
  publicStatusMustRemainOpen : Bool
  completionUpgradeAllowed : Bool
  decision : String

/--
C008 integration gate for `S1-M-252`.

This record is intentionally conservative: the repo-local Lean file is a
checked statement-boundary artifact, but it is not a terminal proof of
four-dimensional manifold classification and public docs have not been
serially synchronized by this child worker.
-/
def c008IntegrationGateStatus : IntegrationGateStatus where
  childTask := "S1-M-252-C008.integration-gate"
  leanValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_252.lean"
  leanValidationArtifactPresent := true
  theoremTreeLedgerPresent := true
  terminalTheoremLeavesClosed := false
  publicMergeTargetSynchronized := false
  terminalRepoLocalClosure := false
  repoLocalIntegrationDebtInCompletedState := false
  publicStatusMustRemainOpen := true
  completionUpgradeAllowed := false
  decision :=
    "keep public status open/not completed until terminal repo-local closure and serial public merge-back are synchronized"

theorem c008IntegrationGateStatus_public_open :
    c008IntegrationGateStatus.publicStatusMustRemainOpen = true :=
  rfl

theorem c008IntegrationGateStatus_no_completion_upgrade :
    c008IntegrationGateStatus.completionUpgradeAllowed = false :=
  rfl

theorem c008IntegrationGateStatus_no_completed_integration_debt :
    c008IntegrationGateStatus.repoLocalIntegrationDebtInCompletedState = false :=
  rfl

theorem c008IntegrationGateStatus_public_merge_not_synchronized :
    c008IntegrationGateStatus.publicMergeTargetSynchronized = false :=
  rfl

/-- Canonical Stage1 boundary combining topological and smooth classification. -/
def StatementShape : Prop :=
  TopologicalStatementShape.{u, v, w} ∧ SmoothStatementShape.{u, v, w}

/--
Public Stage1 status note for the statement boundary.

This string is intentionally part of the checked Lean surface so downstream
public-doc integration can quote the exact boundary without treating this file
as a terminal four-manifold classification proof.
-/
def statementShapePublicStatus : String :=
  "AwesomeTheorems.Stage1.S1_M_252.StatementShape is a checked statement boundary, not a terminal four-manifold classification proof."

/-- The combined statement unfolds to the two normalized boundaries. -/
theorem statementShape_iff :
    StatementShape.{u, v, w} ↔
      TopologicalStatementShape.{u, v, w} ∧ SmoothStatementShape.{u, v, w} :=
  Iff.rfl

/--
Checked public anchor for the Stage1 statement boundary.

This theorem proves only that `StatementShape` is the normalized conjunction of
the topological and smooth boundary propositions.  It does not prove either
classification branch.
-/
theorem statementShape_checkedBoundary :
    StatementShape.{u, v, w} =
      (TopologicalStatementShape.{u, v, w} ∧ SmoothStatementShape.{u, v, w}) :=
  rfl

/-- Projection wrapper from the combined boundary to the topological half. -/
theorem statementShape_topological (h : StatementShape.{u, v, w}) :
    TopologicalStatementShape.{u, v, w} :=
  h.1

/-- Projection wrapper from the combined boundary to the smooth half. -/
theorem statementShape_smooth (h : StatementShape.{u, v, w}) :
    SmoothStatementShape.{u, v, w} :=
  h.2

/-- The invariant package exposes symmetry of the recorded intersection form. -/
theorem intersectionForm_isSymm
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    (X : FourManifoldInvariants.{u, v} M) :
    X.intersectionForm.IsSymm :=
  X.intersectionFormSymm

/-- The invariant package exposes nondegeneracy of the recorded intersection form. -/
theorem intersectionForm_nondegenerate
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    (X : FourManifoldInvariants.{u, v} M) :
    X.intersectionForm.Nondegenerate :=
  X.intersectionFormNondegenerate

/-- Projection wrapper: same topological invariants include isometric intersection forms. -/
theorem sameTopologicalInvariants_forms
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    {XM : FourManifoldInvariants.{u, v} M}
    {XN : FourManifoldInvariants.{w, v} N}
    (h : SameTopologicalInvariants XM XN) :
    IntersectionFormsEquivalent XM XN :=
  h.1

/-- Projection wrapper: same topological invariants include equal Kirby-Siebenmann classes. -/
theorem sameTopologicalInvariants_kirbySiebenmann
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    {XM : FourManifoldInvariants.{u, v} M}
    {XN : FourManifoldInvariants.{w, v} N}
    (h : SameTopologicalInvariants XM XN) :
    XM.kirbySiebenmann.obstruction = XN.kirbySiebenmann.obstruction :=
  h.2.1.1

/-- Projection wrapper: same topological invariants include compatible homology anchors. -/
theorem sameTopologicalInvariants_homologyModel
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    {XM : FourManifoldInvariants.{u, v} M}
    {XN : FourManifoldInvariants.{w, v} N}
    (h : SameTopologicalInvariants XM XN) :
    SingularHomologyModelsCompatible XM XN :=
  h.2.2.2.1

/-- Projection wrapper: same topological invariants include equivalent fundamental-group models. -/
theorem sameTopologicalInvariants_fundamentalGroupModel
    {M : Type u} [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    {N : Type w} [TopologicalSpace N] [ChartedSpace Euclidean4 N]
    {XM : FourManifoldInvariants.{u, v} M}
    {XN : FourManifoldInvariants.{w, v} N}
    (h : SameTopologicalInvariants XM XN) :
    FundamentalGroupModelsEquivalent XM XN :=
  h.2.2.2.2

/-- Checked wrapper for the mathlib basepointed fundamental group. -/
abbrev fundamentalGroupWrapper
    (M : Type u) [TopologicalSpace M] (x : M) : Type u :=
  FundamentalGroup M x

/-- Checked wrapper for the induced homomorphism on mathlib fundamental groups. -/
def fundamentalGroupMapWrapper
    {M : Type u} {N : Type w} [TopologicalSpace M] [TopologicalSpace N]
    (f : C(M, N)) (x : M) :
    FundamentalGroup M x →* FundamentalGroup N (f x) :=
  FundamentalGroup.map f x

/-- Checked mathlib wrapper: a smooth diffeomorphism has an underlying homeomorphism. -/
def diffeomorphToHomeomorph
    {M : Type u} {N : Type w} [TopologicalSpace M] [TopologicalSpace N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N]
    (e : M ≃ₘ⟮SmoothModel4, SmoothModel4⟯ N) : M ≃ₜ N :=
  e.toHomeomorph

/-- Checked implication: a smooth classification conclusion implies a topological one. -/
theorem smoothConclusion_to_topologicalConclusion
    {M : Type u} {N : Type w} [TopologicalSpace M] [TopologicalSpace N]
    [ChartedSpace Euclidean4 M] [ChartedSpace Euclidean4 N]
    (h : SmoothClassificationConclusion M N) :
    TopologicalClassificationConclusion M N :=
  h.elim fun e => ⟨diffeomorphToHomeomorph e⟩

/-- Checked mathlib wrapper: functoriality of singular manifolds under continuous maps. -/
def singularManifoldMapWrapper
    {X Y : Type u} [TopologicalSpace X] [TopologicalSpace Y] {k : WithTop ℕ∞}
    {E H : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    (s : SingularManifold X k I) {f : X → Y} (hf : Continuous f) :
    SingularManifold Y k I :=
  s.map hf

/-- Checked mathlib wrapper: the singular homology functor at a fixed degree. -/
abbrev singularHomologyFunctorWrapper
    (C : Type u) [Category.{v} C] [Limits.HasCoproducts C]
    [Preadditive C] [CategoryWithHomology C] (n : ℕ) :
    C ⥤ TopCat ⥤ C :=
  singularHomologyFunctor C n

/-- Checked mathlib wrapper: signature pair of a real quadratic form. -/
def quadraticSignaturePair
    {V : Type u} [AddCommGroup V] [Module ℝ V] (Q : QuadraticForm ℝ V) : ℕ × ℕ :=
  (sigPos Q, sigNeg Q)

theorem quadraticSignaturePair_fst
    {V : Type u} [AddCommGroup V] [Module ℝ V] (Q : QuadraticForm ℝ V) :
    (quadraticSignaturePair Q).1 = sigPos Q :=
  rfl

theorem quadraticSignaturePair_snd
    {V : Type u} [AddCommGroup V] [Module ℝ V] (Q : QuadraticForm ℝ V) :
    (quadraticSignaturePair Q).2 = sigNeg Q :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check Euclidean4
#check SmoothModel4
#check ChartedSpace
#check IsManifold
#check BoundarylessManifold
#check CompactSpace
#check Diffeomorph.toHomeomorph
#check FundamentalGroup
#check FundamentalGroup.map
#check SingularManifold
#check SingularManifold.map
#check singularHomologyFunctor
#check singularChainComplexFunctor
#check QuadraticForm
#check sigPos
#check sigNeg
#check LinearMap.BilinForm.IsSymm
#check LinearMap.BilinForm.Nondegenerate
#check IntersectionPairingConstructionBlocker
#check bilinearFormOfPairing
#check BilinearPairingData
#check BilinearPairingData.toBilinForm
#check IntersectionPairingConstructionData
#check IntersectionPairingConstructionData.toBilinForm
#check fourManifoldInvariantsOfIntersectionPairingData
#check intersectionPairingMissingApis
#check intersectionPairingCompletionClaimAllowed_eq_false
#check FreedmanBridgeBlocker
#check FreedmanBridgeHypotheses
#check FreedmanClassificationBridgeData
#check FreedmanClassificationBridgeData.apply
#check freedmanBridgeMissingApis
#check freedmanBridgeCompletionClaimAllowed_eq_false
#check freedmanExternalSearchAudit
#check freedmanExternalSearchAudit_no_external_terminal
#check SmoothBranchBlocker
#check DonaldsonObstructionHypotheses
#check DonaldsonObstructionConclusion
#check DonaldsonObstructionStatementShape
#check ExoticStructureDistinguishingHypotheses
#check ExoticStructureDistinguishingConclusion
#check ExoticStructureDistinguishingStatementShape
#check SmoothBranchStatementShape
#check smoothBranchCompletionClaimAllowed_eq_false
#check smoothSingleCompleteInvariantClaimAllowed_eq_false
#check fourManifoldExternalSourceAudit
#check fourManifoldExternalSourceAudit_no_authenticated_code_search
#check fourManifoldExternalSourceAudit_no_terminal_external_proof
#check fourManifoldExternalSourceAudit_no_anchor_only_completion
#check IntegrationGateStatus
#check c008IntegrationGateStatus
#check c008IntegrationGateStatus_public_open
#check c008IntegrationGateStatus_no_completion_upgrade
#check c008IntegrationGateStatus_no_completed_integration_debt
#check c008IntegrationGateStatus_public_merge_not_synchronized

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.PiL2",
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.Diffeomorph",
  "Mathlib.Geometry.Manifold.Bordism",
  "Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic",
  "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance",
  "Mathlib.LinearAlgebra.BilinearForm.Properties",
  "Mathlib.LinearAlgebra.QuadraticForm.Signature"
]

/--
Pinned mathlib revision audited for `S1-M-252.mathlib-audit`.

This matches `Formalizations/Lean/lake-manifest.json` for the Stage1 child pass
and is a local audit record only; it is not evidence of a completed
four-manifold classification proof.
-/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact public-backfill module list required by `S1-M-252.mathlib-audit`. -/
def mathlibAuditRequiredModules : List String := [
  "Mathlib.Geometry.Manifold.Diffeomorph",
  "Mathlib.Geometry.Manifold.Bordism",
  "Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup",
  "Mathlib.AlgebraicTopology.SingularHomology.Basic",
  "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance",
  "Mathlib.LinearAlgebra.BilinearForm.Properties",
  "Mathlib.LinearAlgebra.QuadraticForm.Signature"
]

/-- Checked audit equality for the pinned mathlib revision. -/
theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked audit equality for the exact required module list. -/
theorem mathlibAuditRequiredModules_eq :
    mathlibAuditRequiredModules = [
      "Mathlib.Geometry.Manifold.Diffeomorph",
      "Mathlib.Geometry.Manifold.Bordism",
      "Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup",
      "Mathlib.AlgebraicTopology.SingularHomology.Basic",
      "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance",
      "Mathlib.LinearAlgebra.BilinearForm.Properties",
      "Mathlib.LinearAlgebra.QuadraticForm.Signature"
    ] :=
  rfl

/-- Pinned names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ChartedSpace",
  "IsManifold",
  "BoundarylessManifold",
  "CompactSpace",
  "Homeomorph",
  "Diffeomorph",
  "Diffeomorph.toHomeomorph",
  "FundamentalGroup",
  "FundamentalGroup.map",
  "SingularManifold",
  "SingularManifold.map",
  "singularHomologyFunctor",
  "singularChainComplexFunctor",
  "QuadraticForm",
  "sigPos",
  "sigNeg",
  "LinearMap.BilinForm.IsSymm",
  "LinearMap.BilinForm.Nondegenerate",
  "bilinearFormOfPairing",
  "BilinearPairingData",
  "BilinearPairingData.toBilinForm",
  "IntersectionPairingConstructionBlocker",
  "IntersectionPairingConstructionData",
  "IntersectionPairingConstructionData.toBilinForm",
  "fourManifoldInvariantsOfIntersectionPairingData",
  "intersectionPairingCompletionClaimAllowed_eq_false",
  "FreedmanBridgeBlocker",
  "FreedmanBridgeHypotheses",
  "FreedmanClassificationBridgeData",
  "FreedmanClassificationBridgeData.apply",
  "freedmanBridgeCompletionClaimAllowed_eq_false",
  "freedmanExternalSearchAudit_no_external_terminal",
  "SmoothBranchBlocker",
  "DonaldsonObstructionHypotheses",
  "DonaldsonObstructionConclusion",
  "DonaldsonObstructionStatementShape",
  "ExoticStructureDistinguishingHypotheses",
  "ExoticStructureDistinguishingConclusion",
  "ExoticStructureDistinguishingStatementShape",
  "SmoothBranchStatementShape",
  "smoothBranchCompletionClaimAllowed_eq_false",
  "smoothSingleCompleteInvariantClaimAllowed_eq_false",
  "fourManifoldExternalSourceAudit",
  "fourManifoldExternalSourceAudit_no_authenticated_code_search",
  "fourManifoldExternalSourceAudit_no_terminal_external_proof",
  "fourManifoldExternalSourceAudit_no_anchor_only_completion",
  "IntegrationGateStatus",
  "c008IntegrationGateStatus",
  "c008IntegrationGateStatus_public_open",
  "c008IntegrationGateStatus_no_completion_upgrade",
  "c008IntegrationGateStatus_no_completed_integration_debt",
  "c008IntegrationGateStatus_public_merge_not_synchronized",
  "TopologicalInvariantApiBlocker.singularHomologyNoCanonicalClosedFourManifoldH2",
  "TopologicalInvariantApiBlocker.kirbySiebenmannNoMathlibCharacteristicClassApi"
]

/-- Search terms that did not locate a terminal local mathlib classification theorem. -/
def absentTerminalSearchTerms : List String := [
  "Freedman",
  "Donaldson",
  "four manifold classification",
  "4-manifold classification",
  "Kirby-Siebenmann",
  "intersection form classification",
  "Seiberg-Witten",
  "exotic smooth structure",
  "transversality",
  "cobordism ring four manifolds"
]

end S1_M_252
end Stage1
end AwesomeTheorems
