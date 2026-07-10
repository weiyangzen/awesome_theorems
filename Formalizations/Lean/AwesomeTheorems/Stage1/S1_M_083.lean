import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.MeasureTheory.Measure.Haar.Basic

/-!
# S1-M-083 / THM-M-0434

Stage1 statement-shape artifact for Ngo Bao Chau's Fundamental Lemma.

The pinned mathlib snapshot has a usable nonarchimedean-local-field substrate, but
the audit did not locate the endoscopy, transfer-factor, orbital-integral, Hitchin
fibration, or trace-formula comparison APIs needed for a terminal theorem.  This
file therefore records an explicit formalization boundary and checked local-field
anchors only.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry
open ValuativeRel
open scoped WithZero

namespace AwesomeTheorems.Stage1.S1_M_083

universe uK uO uC

/-- The scheme-theoretic base `Spec K` for a local field `K`. -/
abbrev LocalFieldBaseScheme (K : Type uK) [Field K] : Scheme.{uK} :=
  Spec (CommRingCat.of K)

/-- The scheme-theoretic base `Spec O` for an integral local model. -/
abbrev IntegralBaseScheme (O : Type uK) [CommRing O] : Scheme.{uK} :=
  Spec (CommRingCat.of O)

/--
Concrete scheme-side replacement boundary for the old type-level group carrier.

The pinned mathlib closure has `Scheme` and morphisms over `Spec K`, but the
search did not locate a ready-made `GroupScheme` or `AlgebraicGroup` class.
This structure therefore records the strongest checkable local API boundary:
a scheme over `Spec K`, an explicit product object over the base, and the
unit/multiplication/inverse morphisms with their over-base equations.  The
remaining group-law and representability refinements stay as explicit `Prop`
fields until mathlib or an imported dependency supplies a terminal group-scheme
API.
-/
structure GroupSchemeModel (K : Type uK) [Field K] : Type (uK + 1) where
  carrier : Scheme.{uK}
  structureMap : carrier ⟶ LocalFieldBaseScheme K
  productOverBase : Scheme.{uK}
  productLeft : productOverBase ⟶ carrier
  productRight : productOverBase ⟶ carrier
  productStructureMap : productOverBase ⟶ LocalFieldBaseScheme K
  product_left_over_base : productLeft ≫ structureMap = productStructureMap
  product_right_over_base : productRight ≫ structureMap = productStructureMap
  multiplication : productOverBase ⟶ carrier
  unit : LocalFieldBaseScheme K ⟶ carrier
  inverse : carrier ⟶ carrier
  multiplication_over_base : multiplication ≫ structureMap = productStructureMap
  unit_over_base : unit ≫ structureMap = 𝟙 (LocalFieldBaseScheme K)
  inverse_over_base : inverse ≫ structureMap = structureMap
  group_laws_over_base : Prop

/--
Statement-boundary carrier for an unramified connected reductive group over a
local field, now backed by concrete scheme-side data over `Spec K`.

The reductive, connected, affine, smooth, finite-type, and unramified conditions
are still explicit predicates rather than terminal mathlib classes.  This keeps
the formalization honest: the old abstract group carrier has been removed, but
the missing algebraic-group theory is not silently treated as solved.
-/
structure ReductiveGroupModel (K : Type uK) [Field K] : Type (uK + 1) where
  toGroupScheme : GroupSchemeModel K
  isSmoothAffineFiniteType : Prop
  geometricFibersConnectedReductive : Prop
  isUnramified : Prop

/--
Integral group-scheme boundary over a candidate ring of integers `O`.

The Stage1 artifact does not assume that mathlib has a dedicated smooth affine
group-scheme API over valuation rings.  This mirrors `GroupSchemeModel` over
`Spec K`, but with base `Spec O`, so later workers can replace these fields by
the selected group-scheme/fiber-product API without changing the public
Fundamental Lemma statement shape.
-/
structure IntegralGroupSchemeModel (O : Type uK) [CommRing O] : Type (uK + 1) where
  carrier : Scheme.{uK}
  structureMap : carrier ⟶ IntegralBaseScheme O
  productOverBase : Scheme.{uK}
  productLeft : productOverBase ⟶ carrier
  productRight : productOverBase ⟶ carrier
  productStructureMap : productOverBase ⟶ IntegralBaseScheme O
  product_left_over_base : productLeft ≫ structureMap = productStructureMap
  product_right_over_base : productRight ≫ structureMap = productStructureMap
  multiplication : productOverBase ⟶ carrier
  unit : IntegralBaseScheme O ⟶ carrier
  inverse : carrier ⟶ carrier
  multiplication_over_base : multiplication ≫ structureMap = productStructureMap
  unit_over_base : unit ≫ structureMap = 𝟙 (IntegralBaseScheme O)
  inverse_over_base : inverse ≫ structureMap = structureMap
  group_laws_over_base : Prop

/--
Integral reductive model of a generic-fiber group `G`.

The fields deliberately separate the generic-fiber identification, smooth affine
finite-type model property, and connected reductive special/geometric fibers.
Those are exactly the API points needed before hyperspecial and parahoric
subgroups can become real Lean objects rather than statement-boundary data.
-/
structure IntegralReductiveModel
    (O K : Type uK) [CommRing O] [Field K] (G : ReductiveGroupModel K) :
    Type (uK + 1) where
  toIntegralGroupScheme : IntegralGroupSchemeModel O
  baseChangeToGenericFiber : Prop
  identifiesGenericFiberWith : Prop
  smoothAffineFiniteTypeOverBase : Prop
  connectedReductiveGeometricFibers : Prop

/--
Parahoric model boundary for a reductive group over a nonarchimedean local field.

The `parahoricSubgroupCarrier` field is only a carrier for the eventual
`O`-points/parahoric subgroup API.  The group structure, Bruhat-Tits building
point, and smooth connected model theorem remain explicit predicates until a
pinned dependency or local API supplies them.
-/
structure ParahoricModel
    (O K : Type uK) [CommRing O] [Field K] (G : ReductiveGroupModel K) :
    Type (uK + 1) where
  toIntegralModel : IntegralReductiveModel O K G
  parahoricSubgroupCarrier : Type uK
  realizesParahoricSubgroup : Prop
  smoothAffineGroupScheme : Prop
  connectedSpecialFiberIdentityComponent : Prop

/--
Hyperspecial model boundary, represented as the reductive parahoric case.

For the Fundamental Lemma, the spherical test function and unramified transfer
statement require a hyperspecial maximal compact/parahoric model.  This
structure marks the exact extra hypotheses beyond a general parahoric model.
-/
structure HyperspecialModel
    (O K : Type uK) [CommRing O] [Field K] (G : ReductiveGroupModel K) :
    Type (uK + 1) where
  toParahoricModel : ParahoricModel O K G
  reductiveSpecialFiber : Prop
  maximalParahoric : Prop
  hyperspecialPoint : Prop

/--
Unramified reductive group package over a local field with a chosen integral
model base `O`.

This is stronger than the bare `ReductiveGroupModel.isUnramified : Prop` field:
it records the integral model and the two standard unramified-group inputs used
by the Fundamental Lemma statement, namely splitting over a finite unramified
extension and existence of a hyperspecial model.
-/
structure UnramifiedReductiveGroup (O K : Type uK) [CommRing O] [Field K] :
    Type (uK + 1) where
  toReductiveGroup : ReductiveGroupModel K
  integralModel : IntegralReductiveModel O K toReductiveGroup
  splitsOverFiniteUnramifiedExtension : Prop
  hyperspecialModel : HyperspecialModel O K toReductiveGroup
  unramified_matches_generic_field :
    toReductiveGroup.isUnramified

/--
Abstract statement-boundary carrier for the endoscopic datum attached to `G`.

The real Fundamental Lemma statement needs pinned definitions of endoscopic
groups, matching regular semisimple classes, transfer factors, and the relevant
normalizations.  Those are kept as explicit fields rather than hidden in prose.
-/
structure EndoscopicDatum
    (K : Type uK) [Field K] (G : ReductiveGroupModel K) : Type (uK + 1) where
  endoscopicGroup : ReductiveGroupModel K
  dualGroupEmbedding : Prop
  semisimpleDualElement : Prop
  galoisEquivariance : Prop
  ellipticityCondition : Prop
  isMatchingDatum : Prop

/--
Statement-boundary API for a regular semisimple locus attached to a reductive
group model.

The eventual Fundamental Lemma formalization must replace `Carrier` by concrete
`K`-points, Lie-algebra points, or conjugacy classes in the selected algebraic
group API.  The predicate fields isolate the exact missing notions of
regularity, semisimplicity, and stable-conjugacy support.
-/
structure RegularSemisimpleLocus
    (K : Type uK) [Field K] (G : ReductiveGroupModel K) : Type (max (uK + 1) (uO + 1)) where
  Carrier : Type uO
  representsGroupOrLiePoints : Prop
  isRegular : Carrier -> Prop
  isSemisimple : Carrier -> Prop
  stableConjugacyClass : Carrier -> Type uO

/--
A regular semisimple element in a chosen statement-boundary locus.
-/
structure RegularSemisimpleElement
    {K : Type uK} [Field K] {G : ReductiveGroupModel K}
    (L : RegularSemisimpleLocus.{uK, uO} K G) : Type uO where
  value : L.Carrier
  regular : L.isRegular value
  semisimple : L.isSemisimple value

/--
Matching regular semisimple elements for an endoscopic datum.

The fields record the two regular semisimple loci and a relation between their
elements.  The relation is intentionally not collapsed to a function: real
endoscopic matching is usually stated on stable conjugacy classes and may require
choices of representatives, transfer-factor normalization, and comparison maps.
-/
structure MatchingRegularSemisimpleData
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G) : Type (max (uK + 1) (uO + 1)) where
  endoscopicLocus : RegularSemisimpleLocus.{uK, uO} K H.endoscopicGroup
  groupLocus : RegularSemisimpleLocus.{uK, uO} K G
  EndoscopicElement : Type uO := RegularSemisimpleElement endoscopicLocus
  GroupElement : Type uO := RegularSemisimpleElement groupLocus
  endoscopicElement_realizes_locus : EndoscopicElement = RegularSemisimpleElement endoscopicLocus
  groupElement_realizes_locus : GroupElement = RegularSemisimpleElement groupLocus
  matchingRelation : EndoscopicElement -> GroupElement -> Prop
  matching_respects_stable_conjugacy_classes : Prop
  matching_respects_endoscopic_datum : H.isMatchingDatum

/--
Concrete Haar-measure normalization boundary for the `K`-points of a group.

This is intentionally a carrier-level package rather than a completed
algebraic-group construction: the current Stage1 file still lacks a terminal
`K`-points API for `ReductiveGroupModel`.  The measure side, however, is tied to
mathlib's actual `Measure` and `Measure.IsHaarMeasure` classes.  The normalized
compact-open subgroup field is the hyperspecial/parahoric normalization used by
the unramified Fundamental Lemma.
-/
structure LocalFieldHaarMeasureNormalization
    (K : Type uK) [Field K] (G : ReductiveGroupModel K) : Type (max (uK + 1) (uO + 1)) where
  GroupPoint : Type uO
  groupPointGroup : Group GroupPoint
  groupPointTopology : TopologicalSpace GroupPoint
  groupPointMeasurable : MeasurableSpace GroupPoint
  haarMeasure : @MeasureTheory.Measure GroupPoint groupPointMeasurable
  isHaarMeasure :
    letI := groupPointGroup
    letI := groupPointTopology
    letI := groupPointMeasurable
    MeasureTheory.Measure.IsHaarMeasure haarMeasure
  compactOpenSubgroup : Set GroupPoint
  compactOpenSubgroup_isSubgroup : Prop
  compactOpenSubgroup_isCompact : @IsCompact GroupPoint groupPointTopology compactOpenSubgroup
  compactOpenSubgroup_isOpen : @IsOpen GroupPoint groupPointTopology compactOpenSubgroup
  normalized_compactOpenSubgroup : haarMeasure compactOpenSubgroup = 1
  realizes_K_points_of_group : Prop

/--
Statement-boundary quotient measure and orbital-integral data.

The quotient/orbit type and the equality to an actual integral remain explicit
`Prop` fields because the repo does not yet have conjugacy-orbit quotients,
centralizer quotients, Bruhat-Tits model points, or locally constant compactly
supported test functions for reductive groups over local fields.  The package
still makes real progress over a bare scalar-valued function by recording the
Haar normalization and the quotient measure that a future integral expression
must use.
-/
structure OrbitalIntegralMeasureModel
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (L : RegularSemisimpleLocus.{uK, uO} K G)
    (Coeff : Type uC) [Field Coeff] :
    Type (max (uK + 1) (uO + 1) (uC + 1)) where
  haarNormalization : LocalFieldHaarMeasureNormalization.{uK, uO} K G
  OrbitQuotient : Type uO
  orbitQuotientMeasurable : MeasurableSpace OrbitQuotient
  quotientMeasure : @MeasureTheory.Measure OrbitQuotient orbitQuotientMeasurable
  elementToGroupPoint : L.Carrier -> haarNormalization.GroupPoint
  orbitMap : L.Carrier -> OrbitQuotient -> haarNormalization.GroupPoint
  testFunction : haarNormalization.GroupPoint -> Coeff
  orbitalIntegral : RegularSemisimpleElement L -> Coeff
  quotient_measure_descends_from_haar : Prop
  quotient_measure_uses_centralizer_normalization : Prop
  testFunction_is_spherical_or_compactly_supported : Prop
  orbitalIntegral_quotient_integral_formula : RegularSemisimpleElement L -> Prop
  orbitalIntegral_represents_quotient_integral :
    forall x : RegularSemisimpleElement L, orbitalIntegral_quotient_integral_formula x

/-- Checked accessor for the compact-open Haar normalization used in this slot. -/
theorem normalized_compactOpenSubgroup_volume
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (N : LocalFieldHaarMeasureNormalization.{uK, uO} K G) :
    N.haarMeasure N.compactOpenSubgroup = 1 :=
  N.normalized_compactOpenSubgroup

/-- Checked accessor for the orbital-integral quotient-measure boundary. -/
theorem orbitalIntegral_represents_quotient_integral
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (L : RegularSemisimpleLocus.{uK, uO} K G)
    (Coeff : Type uC) [Field Coeff]
    (M : OrbitalIntegralMeasureModel.{uK, uO, uC} K G L Coeff)
    (x : RegularSemisimpleElement L) :
    M.orbitalIntegral_quotient_integral_formula x :=
  M.orbitalIntegral_represents_quotient_integral x

/--
Statement-boundary transfer-factor normalization package.

The actual Langlands-Shelstad transfer factor requires pinned dual-group,
Galois-cohomology, splitting, Whittaker, and measure-normalization APIs that are
not available in this Stage1 artifact.  This structure makes the missing
normalization data explicit and ties the transfer-factor function to the
matching regular semisimple package instead of leaving it as an unrelated
scalar-valued function.
-/
structure TransferFactorNormalizationModel
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G)
    (M : MatchingRegularSemisimpleData.{uK, uO} K G H)
    (Coeff : Type uC) [Field Coeff] :
    Type (max (uK + 1) (uO + 1) (uC + 1)) where
  transferFactor : M.EndoscopicElement -> Coeff
  transfer_factor_formula : M.EndoscopicElement -> Prop
  transferFactor_realizes_normalization :
    forall gamma : M.EndoscopicElement, transfer_factor_formula gamma
  normalized_by_endoscopic_datum : H.isMatchingDatum
  normalized_by_hyperspecial_or_transfer_data : Prop
  depends_only_on_matching_stable_classes : Prop
  compatible_with_orbital_integral_measures : Prop

/--
Statement-boundary stable orbital integral package.

The stable sum over a stable conjugacy class is represented by an explicit
fiber of representatives and a formula predicate.  This keeps the object honest:
the repo does not yet have concrete stable-conjugacy quotients or finite
weighted sums of orbital integrals for reductive groups over local fields.
-/
structure StableOrbitalIntegralModel
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G)
    (M : MatchingRegularSemisimpleData.{uK, uO} K G H)
    (Coeff : Type uC) [Field Coeff] :
    Type (max (uK + 1) (uO + 1) (uC + 1)) where
  orbitalMeasure :
    OrbitalIntegralMeasureModel.{uK, uO, uC} K H.endoscopicGroup M.endoscopicLocus Coeff
  stableConjugacyRepresentative : M.EndoscopicElement -> Type uO
  representativeToElement :
    forall gamma : M.EndoscopicElement,
      stableConjugacyRepresentative gamma -> M.EndoscopicElement
  orbitalIntegralContribution :
    forall gamma : M.EndoscopicElement,
      stableConjugacyRepresentative gamma -> Coeff
  stableOrbitalIntegral : M.EndoscopicElement -> Coeff
  stable_sum_formula : M.EndoscopicElement -> Prop
  stableOrbitalIntegral_represents_stable_sum :
    forall gamma : M.EndoscopicElement, stable_sum_formula gamma
  representatives_realize_stable_conjugacy_class : Prop
  stable_sum_uses_haar_normalization : Prop
  stable_sum_uses_endoscopic_orbital_integral : Prop

/-- Checked accessor for the transfer-factor normalization boundary. -/
theorem transferFactor_realizes_normalization
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G)
    (M : MatchingRegularSemisimpleData.{uK, uO} K G H)
    (Coeff : Type uC) [Field Coeff]
    (T : TransferFactorNormalizationModel.{uK, uO, uC} K G H M Coeff)
    (gamma : M.EndoscopicElement) :
    T.transfer_factor_formula gamma :=
  T.transferFactor_realizes_normalization gamma

/-- Checked accessor for the stable-orbital-integral summation boundary. -/
theorem stableOrbitalIntegral_represents_stable_sum
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G)
    (M : MatchingRegularSemisimpleData.{uK, uO} K G H)
    (Coeff : Type uC) [Field Coeff]
    (S : StableOrbitalIntegralModel.{uK, uO, uC} K G H M Coeff)
    (gamma : M.EndoscopicElement) :
    S.stable_sum_formula gamma :=
  S.stableOrbitalIntegral_represents_stable_sum gamma

/--
The orbital-integral comparison package needed by the Lie-algebra/group version
of the Fundamental Lemma.

The coefficient field is abstract because the eventual theorem must choose a
normalization for measures and transfer factors.  The equality below is the
formal boundary: stable orbital integrals on the endoscopic side equal a transfer
factor times orbital integrals on the original group side for matching elements.
-/
structure OrbitalIntegralComparison
    (K : Type uK) [Field K] (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G) :
    Type (max (uK + 1) (uO + 1) (uC + 1)) where
  matchingRegularSemisimpleData : MatchingRegularSemisimpleData.{uK, uO} K G H
  Coeff : Type uC
  coeffField : Field Coeff
  stableOrbitalIntegralModel :
    StableOrbitalIntegralModel.{uK, uO, uC} K G H matchingRegularSemisimpleData Coeff
  transferFactorNormalization :
    TransferFactorNormalizationModel.{uK, uO, uC} K G H matchingRegularSemisimpleData Coeff
  matchingElement :
    matchingRegularSemisimpleData.EndoscopicElement ->
      matchingRegularSemisimpleData.GroupElement
  matchingElement_matches :
    forall gamma : matchingRegularSemisimpleData.EndoscopicElement,
      matchingRegularSemisimpleData.matchingRelation gamma (matchingElement gamma)
  stableOrbitalIntegral : matchingRegularSemisimpleData.EndoscopicElement -> Coeff
  orbitalIntegral : matchingRegularSemisimpleData.GroupElement -> Coeff
  transferFactor : matchingRegularSemisimpleData.EndoscopicElement -> Coeff
  stableOrbitalIntegral_eq_model :
    stableOrbitalIntegral = stableOrbitalIntegralModel.stableOrbitalIntegral
  transferFactor_eq_model :
    transferFactor = transferFactorNormalization.transferFactor

attribute [instance] OrbitalIntegralComparison.coeffField

/--
Lean statement-shape candidate for the Fundamental Lemma.

This is not a proof of the Fundamental Lemma.  It is the smallest checked
repo-local boundary found in this pass: an explicit nonarchimedean local field,
an unramified reductive group model, matching endoscopic data, and the pointwise
orbital-integral identity that a future concrete formalization must instantiate.
-/
def StatementShape
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K]
    (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G)
    (C : OrbitalIntegralComparison.{uK, uO, uC} K G H) : Prop :=
  G.isUnramified ->
    H.isMatchingDatum ->
      forall gamma : C.matchingRegularSemisimpleData.EndoscopicElement,
        C.stableOrbitalIntegral gamma =
          C.transferFactor gamma * C.orbitalIntegral (C.matchingElement gamma)

/--
Statement shape with the unramified reductive group and hyperspecial/parahoric
model data made explicit.

This is still not a proof of the Fundamental Lemma.  It is a checked boundary
showing where the eventual spherical test-function and hyperspecial-model
normalizations attach to the existing pointwise orbital-integral identity.
-/
def StatementShapeWithHyperspecialModel
    (O K : Type uK) [CommRing O] [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K]
    (G : UnramifiedReductiveGroup O K)
    (H : EndoscopicDatum K G.toReductiveGroup)
    (C : OrbitalIntegralComparison.{uK, uO, uC} K G.toReductiveGroup H) : Prop :=
  G.splitsOverFiniteUnramifiedExtension ->
    G.hyperspecialModel.reductiveSpecialFiber ->
      G.hyperspecialModel.maximalParahoric ->
        G.hyperspecialModel.hyperspecialPoint ->
          StatementShape K G.toReductiveGroup H C

/-- Direct wrapper for the pointwise orbital-integral identity. -/
theorem statementShape_of_orbital_integral_identity
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K]
    (G : ReductiveGroupModel K)
    (H : EndoscopicDatum K G)
    (C : OrbitalIntegralComparison.{uK, uO, uC} K G H)
    (h :
      forall gamma : C.matchingRegularSemisimpleData.EndoscopicElement,
        C.stableOrbitalIntegral gamma =
          C.transferFactor gamma * C.orbitalIntegral (C.matchingElement gamma)) :
    StatementShape K G H C := by
  intro _hG _hH gamma
  exact h gamma

/-- Direct wrapper from the base statement shape to the hyperspecial-model shape. -/
theorem statementShapeWithHyperspecialModel_of_statementShape
    (O K : Type uK) [CommRing O] [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K]
    (G : UnramifiedReductiveGroup O K)
    (H : EndoscopicDatum K G.toReductiveGroup)
    (C : OrbitalIntegralComparison.{uK, uO, uC} K G.toReductiveGroup H)
    (h : StatementShape K G.toReductiveGroup H C) :
    StatementShapeWithHyperspecialModel O K G H C := by
  intro _hsplit _hspecial _hmax _hpoint
  exact h

/-- The current mathlib-level local-field value-group normalization, checked locally. -/
theorem localField_valueGroupWithZero_iso_int
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Nonempty (ValueGroupWithZero K ≃*o ℤᵐ⁰) := by
  exact ⟨IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt K⟩

/-- A checked local-field instance that the Fundamental Lemma statement would require. -/
theorem localField_isValuativeTopology
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    IsValuativeTopology K := by
  infer_instance

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.MeasureTheory.Measure.Haar.Basic",
  "Mathlib.MeasureTheory.Measure.Haar.Quotient",
  "Mathlib.NumberTheory.Padics.PadicIntegers",
  "Mathlib.NumberTheory.NumberField.AdeleRing",
  "Mathlib.RingTheory.DedekindDomain.FiniteAdeleRing",
  "Mathlib.MeasureTheory.Group.Measure"
]

/--
Search terms that did not locate a terminal Fundamental Lemma theorem in the
pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "FundamentalLemma",
  "fundamental lemma",
  "Ngo",
  "Ngo Bao Chau",
  "hyperspecial",
  "parahoric",
  "endoscopy",
  "endoscopic",
  "regular semisimple",
  "stable conjugacy",
  "orbital integral",
  "transferFactor",
  "Hitchin",
  "trace formula"
]

/--
Public Lean repository audit sources checked for a terminal Fundamental Lemma
proof before any external dependency pinning.

The GitHub repository searches returned zero matching repositories for the
Lean/Fundamental-Lemma combinations listed here.  GitHub code search was
rate-limited in this unauthenticated execution environment, so it is not used as
completion evidence.  The pinned mathlib tree was searched locally as part of
the repo-local closure.
-/
def externalLeanAuditSources : List String := [
  "https://api.github.com/search/repositories?q=%22fundamental%20lemma%22%20lean",
  "https://api.github.com/search/repositories?q=Ngo%20Lean%20Fundamental%20Lemma",
  "Formalizations/Lean/.lake/packages/mathlib at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95"
]

/--
Result of the public Lean 4 repository audit for this Stage1 child.

No completed public Lean 4 proof of Ngo's Fundamental Lemma was located in the
checked sources.  Consequently there is no external proof dependency to pin,
import, or wrap in this pass.  If a future audit finds such a proof, this slot
must move to a pinned dependency, vendored proof body, repo-local wrapper, or a
concrete integration blocker before any completion-state upgrade.
-/
def externalLeanFundamentalLemmaAuditGate : String :=
  "no completed public Lean 4 Fundamental Lemma proof located; no anchor-only completion claim"

/--
Unchecked proof leaves from the parent ledger that must be split into
independent `<=100` step ledgers before any completion-state upgrade.

These are documentation/process targets, not solved Lean proof obligations.  The
list is kept in the checked Stage1 artifact so that future public backfill can
refer to the same canonical `S1M083-U*` names instead of creating a parallel
node system.
-/
def uncheckedLeafBudgetLedgerBackfillTargets : List String := [
  "S1M083-U01: concrete reductive group or group-scheme API over a local field",
  "S1M083-U02: unramified reductive group predicate and hyperspecial model",
  "S1M083-U03: endoscopic datum definition",
  "S1M083-U04: regular semisimple elements and matching relation",
  "S1M083-U05: Haar measure normalization for orbital integrals",
  "S1M083-U06: orbital integral definition and basic invariance lemmas",
  "S1M083-U07: stable orbital integral definition",
  "S1M083-U08: transfer factor definition and normalization",
  "S1M083-U09: local-to-global or Hitchin-fibration reduction package",
  "S1M083-U10: terminal comparison theorem or pinned upstream wrapper"
]

/--
Completion gate for the unchecked-leaf budget split requested by child
`S1-M-083-C007`.
-/
def uncheckedLeafBudgetLedgerGate : String :=
  "not_completed; every unchecked S1M083-U* leaf must receive an independent <=100 step proof ledger before completion-state upgrade"

/-- Machine proof debt classification for this Stage1 artifact. -/
def machineProofDebtClassification : String :=
  "formalization_debt: scheme-backed group, integral parahoric/hyperspecial model boundary, endoscopic/matching regular semisimple statement boundary, Haar-measure normalization boundary, orbital-integral quotient-measure boundary, transfer-factor normalization boundary, stable-orbital-integral summation boundary, and local-field anchors only; no terminal Fundamental Lemma proof"

/--
Repo-local integration-debt gate.  No completed-state integration debt is claimed
because no external Lean 4 terminal proof was located and pinned into this Lake
closure during this pass.
-/
def repoLocalIntegrationDebtGate : String :=
  "not_completed; no completed-state repo_local_integration_debt retained"

end AwesomeTheorems.Stage1.S1_M_083

end
