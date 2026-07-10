import Mathlib.AlgebraicGeometry.Morphisms.Etale
import Mathlib.AlgebraicGeometry.Sites.ElladicCohomology
import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.FieldTheory.Galois.Profinite
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.RepresentationTheory.Basic
import Mathlib.RepresentationTheory.Rep.Basic

/-!
# S1-M-062 / THM-M-0448: Harris--Taylor theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Harris--Taylor proof of the local Langlands correspondence for `GL n` over a
`p`-adic local field.

The current pinned mathlib closure exposes useful local-field, absolute Galois
group, `GL n`, and ordinary representation infrastructure.  It does not expose
the Shimura-variety/cohomology package or the Weil--Deligne and smooth
admissible representation categories needed for a terminal Harris--Taylor
theorem.  The declarations below therefore keep the boundary explicit and avoid
proof placeholders.
-/

open ValuativeRel
open scoped MatrixGroups WithZero

universe uK uι uV uW

namespace AwesomeTheorems.Stage1.S1_M_062

/-- Pinned mathlib revision used for the Stage1 Harris--Taylor module audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- The `GL_n(K)` substrate currently available from mathlib. -/
abbrev GLn (n : Type uι) (K : Type uK) [Fintype n] [DecidableEq n] [Semiring K] :
    Type (max uι uK) :=
  Matrix.GeneralLinearGroup n K

/-- The absolute Galois group object currently available from mathlib. -/
abbrev AbsoluteGaloisGroup (K : Type uK) [Field K] : Type uK :=
  Field.absoluteGaloisGroup K

/--
Plain Galois-side representations available in mathlib.

This is weaker than the Weil--Deligne side of Harris--Taylor local Langlands,
but it fixes the closest current mathlib Galois representation substrate.
-/
abbrev PlainGaloisRepresentation
    (K : Type uK) (E : Type uι) (V : Type uV)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V] :
    Type (max uK uV) :=
  Representation E (AbsoluteGaloisGroup K) V

/--
Plain `GL_n(K)` representations available in mathlib.

This does not encode smoothness, admissibility, irreducibility, equivalence
classes, supercuspidal support, or Harris--Taylor normalizations.
-/
abbrev PlainGLRepresentation
    (n : Type uι) (K : Type uK) (E : Type uW) (V : Type uW)
    [Fintype n] [DecidableEq n] [Field K] [Semiring E] [AddCommMonoid V] [Module E V] :
    Type (max uι uK uW) :=
  Representation E (GLn n K) V

/--
Abstract Weil-group endpoint API missing from the current Harris--Taylor
formalization boundary.

The current pinned mathlib closure exposes absolute Galois groups, but this
Stage1 slot still needs a concrete Weil group object with its map to the
absolute Galois group before a terminal local Langlands statement can be made.
-/
structure WeilGroupEndpoint
    (K : Type uK) [Field K] : Type (max uK (uι + 1)) where
  WeilGroup : Type uι
  weilGroupGroup : Group WeilGroup
  toAbsoluteGaloisGroup : WeilGroup → AbsoluteGaloisGroup K

/--
Abstract Weil--Deligne endpoint API for the Galois side.

This separates the Weil group, the type of Weil--Deligne representations,
Frobenius semisimplicity, and equivalence of parameters.  It is intentionally
an API boundary only; it does not construct these objects.
-/
structure WeilDeligneEndpoint
    (K : Type uK) [Field K] : Type (max uK (uι + 1)) where
  weilGroupEndpoint : WeilGroupEndpoint.{uK, uι} K
  WeilDeligneRepresentation : Type uι
  IsFrobeniusSemisimple : WeilDeligneRepresentation → Prop
  equivalence : Setoid WeilDeligneRepresentation

namespace WeilDeligneEndpoint

/-- Equivalence classes in the abstract Weil--Deligne endpoint. -/
abbrev EquivalenceClass
    {K : Type uK} [Field K] (endpoint : WeilDeligneEndpoint.{uK, uι} K) : Type uι :=
  Quotient endpoint.equivalence

end WeilDeligneEndpoint

/--
Abstract smooth `GL_n(K)` representation endpoint API for the automorphic side.

This records the missing representation category separately from its predicates:
smoothness, admissibility, irreducibility, and equivalence of representations.
It is weaker than a concrete category of smooth admissible representations, but
it gives downstream tasks a checked place to attach those APIs.
-/
structure SmoothGLnEndpoint
    (n : Type uι) (K : Type uK) : Type (max uK (uι + 1)) where
  SmoothRepresentation : Type uι
  IsSmooth : SmoothRepresentation → Prop
  IsAdmissible : SmoothRepresentation → Prop
  IsIrreducible : SmoothRepresentation → Prop
  equivalence : Setoid SmoothRepresentation

namespace SmoothGLnEndpoint

/-- Equivalence classes in the abstract smooth `GL_n(K)` endpoint. -/
abbrev EquivalenceClass
    {n : Type uι} {K : Type uK} (endpoint : SmoothGLnEndpoint n K) : Type uι :=
  Quotient endpoint.equivalence

end SmoothGLnEndpoint

/--
The split endpoint categories needed by a terminal Harris--Taylor statement.

The automorphic and Galois sides are recorded independently so that future
children can replace the abstract endpoints with concrete smooth
representation and Weil--Deligne APIs, or with checked upstream imports.
-/
structure LocalLanglandsEndpointCategories
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  rank : ℕ
  rank_pos : 0 < rank
  RankIndex : Type uι
  rankIndexFintype : Fintype RankIndex
  rankIndexDecidableEq : DecidableEq RankIndex
  rankIndexCard_eq_rank : Fintype.card RankIndex = rank
  automorphic : SmoothGLnEndpoint RankIndex K
  galois : WeilDeligneEndpoint.{uK, uι} K

/--
Abstract local correspondence data for the Harris--Taylor target theorem.

The fields deliberately use abstract parameter types.  A terminal formalization
must replace them with concrete smooth irreducible admissible `GL_n(K)`
representations and Frobenius-semisimple Weil--Deligne parameters, or with a
checked upstream theorem providing those objects.
-/
structure LocalLanglandsData
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  endpoints : LocalLanglandsEndpointCategories K ι
  AutomorphicParameter : Type uι
  GaloisParameter : Type uι
  automorphicParameterEquiv :
    AutomorphicParameter ≃ SmoothGLnEndpoint.EquivalenceClass endpoints.automorphic
  galoisParameterEquiv :
    GaloisParameter ≃ WeilDeligneEndpoint.EquivalenceClass endpoints.galois
  IsSmoothIrreducibleAdmissible : AutomorphicParameter → Prop
  IsFrobeniusSemisimpleWeilDeligne : GaloisParameter → Prop
  Corresponds : AutomorphicParameter → GaloisParameter → Prop
  preservesLocalFactors : AutomorphicParameter → GaloisParameter → Prop

/--
Simple Shimura-variety input for the Harris--Taylor geometry branch.

This is an API boundary only.  It records the missing datum, level, model, and
bad-reduction shape that a terminal proof must later construct or import.
-/
structure SimpleShimuraVarietyInput
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  ShimuraDatum : Type uι
  LevelStructure : Type uι
  SimpleShimuraVariety : Type uι
  hasSimplePELDatum : Prop
  hasCanonicalModel : Prop
  hasBadReductionPlace : Prop

/--
Integral-model input for the simple Shimura variety used by Harris--Taylor.

The current repository has no concrete construction of these models; the fields
name the exact objects and properties needed before nearby cycles or Igusa
towers can be attached.
-/
structure IntegralModelInput
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (simple : SimpleShimuraVarietyInput K ι) : Type (max uK (uι + 1)) where
  IntegralModel : Type uι
  GenericFiber : Type uι
  SpecialFiber : Type uι
  extendsSimpleShimuraVariety : Prop
  hasFlatProperFiniteTypePackage : Prop
  hasBadReductionStratification : Prop

/--
Igusa-variety and tower input over the integral model.

Harris--Taylor uses Igusa varieties/towers to analyze strata and group actions.
This record keeps the tower, levels, transition maps, and action compatibility
separate from the integral-model obligations.
-/
structure IgusaTowerInput
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    {simple : SimpleShimuraVarietyInput K ι}
    (model : IntegralModelInput simple) : Type (max uK (uι + 1)) where
  IgusaVariety : Type uι
  IgusaTower : Type uι
  IgusaLevel : Type uι
  hasFiniteEtaleTransitions : Prop
  coversRelevantStrata : Prop
  carriesHeckeAndGaloisActions : Prop

/--
Nearby-cycles input for the integral model.

This is the local cohomological bridge from bad reduction geometry to trace
terms.  It remains abstract until mathlib or a pinned dependency supplies the
relevant derived or sheaf-theoretic construction.
-/
structure NearbyCyclesInput
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    {simple : SimpleShimuraVarietyInput K ι}
    (model : IntegralModelInput simple) : Type (max uK (uι + 1)) where
  NearbyCycles : Type uι
  SpecializationMap : Type uι
  InertiaAction : Type uι
  compatibleWithStratification : Prop
  hasTraceFormulaContribution : Prop

/--
`l`-adic cohomology realization input for extracting local parameters.

The local mathlib closure imports ell-adic cohomology infrastructure, but not a
Harris--Taylor realization theorem.  This record names the realization, action
data, and local-global compatibility obligations separately.
-/
structure LadicCohomologyRealizationInput
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    {simple : SimpleShimuraVarietyInput K ι} {model : IntegralModelInput simple}
    (nearby : NearbyCyclesInput model) : Type (max uK (uι + 1)) where
  CohomologyRealization : Type uι
  CoefficientField : Type uι
  CohomologicalDegree : Type uι
  GaloisAction : Type uι
  HeckeAction : Type uι
  realizesWeilDeligneParameters : Prop
  hasLocalGlobalCompatibility : Prop

/--
The five-way split of Harris--Taylor geometric prerequisites requested by the
Stage1 geometry child task.

Each component is dependent on the preceding construction, mirroring the proof
flow: simple Shimura variety, integral model, Igusa tower, nearby cycles, then
`l`-adic cohomology realization.
-/
structure HarrisTaylorGeometryPrerequisites
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  simpleShimura : SimpleShimuraVarietyInput K ι
  integralModel : IntegralModelInput simpleShimura
  igusaTower : IgusaTowerInput integralModel
  nearbyCycles : NearbyCyclesInput integralModel
  ladicCohomology : LadicCohomologyRealizationInput nearbyCycles

/--
Abstract geometric/cohomological input for the Harris--Taylor proof strategy.

This isolates the proof-specific infrastructure absent from the current local
mathlib closure: simple Shimura varieties, integral models, Igusa varieties and
towers, nearby cycles, trace formula comparison, and extraction of local
parameters from `l`-adic cohomology.
-/
structure HarrisTaylorGeometricInput
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  prerequisites : HarrisTaylorGeometryPrerequisites K ι
  hasBadReductionGeometry : Prop
  hasTraceFormulaComparison : Prop
  realizesLocalParameters : Prop

namespace HarrisTaylorGeometricInput

/-- The simple Shimura-variety object exposed by a geometric input package. -/
abbrev SimpleShimuraVariety
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (geometry : HarrisTaylorGeometricInput K ι) : Type uι :=
  geometry.prerequisites.simpleShimura.SimpleShimuraVariety

/-- The integral model object exposed by a geometric input package. -/
abbrev IntegralModel
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (geometry : HarrisTaylorGeometricInput K ι) : Type uι :=
  geometry.prerequisites.integralModel.IntegralModel

/-- The Igusa tower object exposed by a geometric input package. -/
abbrev IgusaTower
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (geometry : HarrisTaylorGeometricInput K ι) : Type uι :=
  geometry.prerequisites.igusaTower.IgusaTower

/-- The nearby-cycles object exposed by a geometric input package. -/
abbrev NearbyCycles
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (geometry : HarrisTaylorGeometricInput K ι) : Type uι :=
  geometry.prerequisites.nearbyCycles.NearbyCycles

/-- The `l`-adic cohomology realization exposed by a geometric input package. -/
abbrev CohomologyRealization
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (geometry : HarrisTaylorGeometricInput K ι) : Type uι :=
  geometry.prerequisites.ladicCohomology.CohomologyRealization

end HarrisTaylorGeometricInput

/-- One M0387-style leaf row for the Harris--Taylor geometry prerequisite split. -/
structure HarrisTaylorGeometryLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  upstreamInputs : List String
  downstreamOutputs : List String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
deriving Repr, DecidableEq

/--
Integration-ready theorem-tree split for the Harris--Taylor geometry branch.

Every row remains `unchecked`: this file records a checked boundary and does not
construct the Harris--Taylor Shimura varieties, integral models, Igusa towers,
nearby-cycles complexes, or `l`-adic cohomological realization theorem.
-/
def harrisTaylorGeometryLeaves : List HarrisTaylorGeometryLeaf := [
  {
    packageId := "HT-GEO-P01",
    leafLedgerId := "HT-GEO-L01",
    title := "simple Shimura varieties",
    localDuty :=
      "define or import the simple PEL-type Shimura datum, level data, canonical model, and bad-reduction place used in Harris--Taylor",
    upstreamInputs := [ "local field K", "Shimura datum API", "level structure API" ],
    downstreamOutputs := [ "SimpleShimuraVarietyInput", "integral-model branch input" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "concrete simple Shimura-variety construction validates repo-locally without Prop-only core placeholders"
  },
  {
    packageId := "HT-GEO-P02",
    leafLedgerId := "HT-GEO-L02",
    title := "integral models",
    localDuty :=
      "construct the integral model, identify generic and special fibers, and prove the flat/proper/finite-type and bad-reduction stratification package",
    upstreamInputs := [ "HT-GEO-P01", "scheme/integral-model APIs" ],
    downstreamOutputs := [ "IntegralModelInput", "Igusa and nearby-cycles branch inputs" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "integral model and its structural properties validate as local proof bodies or checked dependencies"
  },
  {
    packageId := "HT-GEO-P03",
    leafLedgerId := "HT-GEO-L03",
    title := "Igusa varieties and towers",
    localDuty :=
      "define Igusa varieties, the level tower, finite-etale transition maps, strata coverage, and Hecke/Galois action compatibility",
    upstreamInputs := [ "HT-GEO-P02", "finite-etale morphism APIs", "group-action APIs" ],
    downstreamOutputs := [ "IgusaTowerInput", "trace and cohomology branch data" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "Igusa tower construction and action compatibility validate in the local Lake closure"
  },
  {
    packageId := "HT-GEO-P04",
    leafLedgerId := "HT-GEO-L04",
    title := "nearby cycles",
    localDuty :=
      "construct the nearby-cycles object, specialization map, inertia action, stratification compatibility, and trace-formula contribution",
    upstreamInputs := [ "HT-GEO-P02", "sheaf or derived-category APIs", "stratification data" ],
    downstreamOutputs := [ "NearbyCyclesInput", "trace comparison branch input" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "nearby-cycles package validates with concrete sheaf/cohomology APIs or a checked upstream import"
  },
  {
    packageId := "HT-GEO-P05",
    leafLedgerId := "HT-GEO-L05",
    title := "l-adic cohomology realization",
    localDuty :=
      "realize local Weil--Deligne parameters in l-adic cohomology with compatible Galois and Hecke actions and local-global compatibility",
    upstreamInputs := [ "HT-GEO-P03", "HT-GEO-P04", "ell-adic cohomology APIs", "endpoint categories" ],
    downstreamOutputs := [ "LadicCohomologyRealizationInput", "HarrisTaylorGeometricInput.realizesLocalParameters" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "cohomological realization theorem validates repo-locally and links to concrete endpoint categories"
  }
]

/-- The Harris--Taylor geometry split has exactly the requested five rows. -/
theorem harrisTaylorGeometryLeaves_length :
    harrisTaylorGeometryLeaves.length = 5 :=
  rfl

/-- All current Harris--Taylor geometry leaves are explicitly unchecked. -/
theorem harrisTaylorGeometryLeaves_statuses :
    harrisTaylorGeometryLeaves.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each Harris--Taylor geometry leaf is budgeted at at most 100 local proof steps. -/
theorem harrisTaylorGeometryLeaves_budgets :
    harrisTaylorGeometryLeaves.map (fun row => row.localStepBudget) =
      [100, 100, 100, 100, 100] :=
  rfl

/--
Trace-formula comparison input for the Harris--Taylor proof strategy.

This is an interface, not a construction.  It separates the geometric trace
terms coming from nearby cycles and Igusa towers from the automorphic and
Galois trace terms that must be compared before local parameters can be
extracted.
-/
structure TraceFormulaComparisonInput
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (localData : LocalLanglandsData K ι)
    (geometry : HarrisTaylorGeometricInput K ι) : Type (max uK (uι + 1)) where
  GeometricTraceTerm : Type uι
  AutomorphicTraceTerm : Type uι
  GaloisTraceTerm : Type uι
  geometricTermFromCohomology :
    HarrisTaylorGeometricInput.CohomologyRealization geometry → GeometricTraceTerm
  compareToAutomorphic : GeometricTraceTerm → AutomorphicTraceTerm
  compareToGalois : GeometricTraceTerm → GaloisTraceTerm
  hasArthurSelbergTraceIdentity : Prop
  hasLefschetzTraceIdentity : Prop
  compatibleWithHeckeOperators : Prop
  compatibleWithFrobeniusTraces : Prop
  identifiesMatchingTraceTerms : Prop

/--
Cohomological extraction interface for local Langlands parameters.

Given the abstract cohomology realization from the geometry branch, this record
names the classes contributing to local Langlands and the maps extracting the
automorphic and Galois parameters.  The proof obligations keep smooth
irreducible admissibility, Frobenius semisimplicity, correspondence, and local
factor compatibility explicit.
-/
structure CohomologicalParameterExtractionInput
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (localData : LocalLanglandsData K ι)
    (geometry : HarrisTaylorGeometricInput K ι) : Type (max uK (uι + 1)) where
  CohomologyClass : Type uι
  classFromRealization :
    HarrisTaylorGeometricInput.CohomologyRealization geometry → CohomologyClass
  IsRelevantClass : CohomologyClass → Prop
  toAutomorphicParameter : CohomologyClass → localData.AutomorphicParameter
  toGaloisParameter : CohomologyClass → localData.GaloisParameter
  relevant_automorphic :
    ∀ c, IsRelevantClass c →
      localData.IsSmoothIrreducibleAdmissible (toAutomorphicParameter c)
  relevant_galois :
    ∀ c, IsRelevantClass c →
      localData.IsFrobeniusSemisimpleWeilDeligne (toGaloisParameter c)
  relevant_corresponds :
    ∀ c, IsRelevantClass c →
      localData.Corresponds (toAutomorphicParameter c) (toGaloisParameter c)
  relevant_preservesLocalFactors :
    ∀ c, IsRelevantClass c →
      localData.preservesLocalFactors (toAutomorphicParameter c) (toGaloisParameter c)

/--
Combined trace/cohomology bridge needed by the Harris--Taylor package.

The bridge records how trace comparison feeds the cohomological extraction of
local Langlands parameters.  It remains abstract until concrete trace-formula,
nearby-cycles, and `l`-adic cohomology APIs or a checked upstream dependency
provide the proof bodies.
-/
structure HarrisTaylorTraceCohomologyBridge
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    (localData : LocalLanglandsData K ι)
    (geometry : HarrisTaylorGeometricInput K ι) : Type (max uK (uι + 1)) where
  traceComparison : TraceFormulaComparisonInput localData geometry
  parameterExtraction : CohomologicalParameterExtractionInput localData geometry
  traceComparisonFeedsCohomology : Prop
  extractionCoversRelevantAutomorphicParameters : Prop
  extractionCoversRelevantGaloisParameters : Prop
  extractsLocalLanglandsCorrespondence : Prop
  preservesLocalFactorsAfterExtraction : Prop

namespace HarrisTaylorTraceCohomologyBridge

/-- The automorphic parameter extracted from a cohomology class by a bridge. -/
abbrev AutomorphicParameter
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    {localData : LocalLanglandsData K ι} {geometry : HarrisTaylorGeometricInput K ι}
    (bridge : HarrisTaylorTraceCohomologyBridge localData geometry)
    (c : bridge.parameterExtraction.CohomologyClass) :
    localData.AutomorphicParameter :=
  bridge.parameterExtraction.toAutomorphicParameter c

/-- The Galois parameter extracted from a cohomology class by a bridge. -/
abbrev GaloisParameter
    {K : Type uK} [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] {ι : Type uι}
    {localData : LocalLanglandsData K ι} {geometry : HarrisTaylorGeometricInput K ι}
    (bridge : HarrisTaylorTraceCohomologyBridge localData geometry)
    (c : bridge.parameterExtraction.CohomologyClass) :
    localData.GaloisParameter :=
  bridge.parameterExtraction.toGaloisParameter c

end HarrisTaylorTraceCohomologyBridge

/-- One M0387-style leaf row for the Harris--Taylor trace/cohomology bridge. -/
structure HarrisTaylorTraceBridgeLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  upstreamInputs : List String
  downstreamOutputs : List String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
deriving Repr, DecidableEq

/--
Integration-ready theorem-tree split for the trace-formula and cohomological
extraction bridge.

Every row remains `unchecked`: this file provides a checked formal interface,
not the Harris--Taylor trace comparison or parameter-extraction proof.
-/
def harrisTaylorTraceBridgeLeaves : List HarrisTaylorTraceBridgeLeaf := [
  {
    packageId := "HT-TRACE-P01",
    leafLedgerId := "HT-TRACE-L01",
    title := "geometric trace terms from nearby cycles and Igusa towers",
    localDuty :=
      "define the geometric trace terms produced by nearby cycles, Igusa towers, and l-adic cohomology realization",
    upstreamInputs := [ "HT-GEO-P03", "HT-GEO-P04", "HT-GEO-P05" ],
    downstreamOutputs := [ "TraceFormulaComparisonInput.GeometricTraceTerm" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "geometric trace terms are constructed from concrete cohomology APIs and validate repo-locally"
  },
  {
    packageId := "HT-TRACE-P02",
    leafLedgerId := "HT-TRACE-L02",
    title := "automorphic trace comparison",
    localDuty :=
      "construct automorphic trace terms and prove compatibility with Hecke operators and the Arthur-Selberg trace identity",
    upstreamInputs := [ "HT-TRACE-P01", "smooth GL_n representation endpoint", "Hecke operator APIs" ],
    downstreamOutputs := [ "TraceFormulaComparisonInput.AutomorphicTraceTerm", "compareToAutomorphic" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "automorphic trace comparison validates as a local proof body or checked dependency"
  },
  {
    packageId := "HT-TRACE-P03",
    leafLedgerId := "HT-TRACE-L03",
    title := "Galois trace comparison",
    localDuty :=
      "construct Galois-side trace terms and prove compatibility with Frobenius traces and Weil--Deligne endpoint data",
    upstreamInputs := [ "HT-TRACE-P01", "Weil--Deligne endpoint", "Frobenius trace APIs" ],
    downstreamOutputs := [ "TraceFormulaComparisonInput.GaloisTraceTerm", "compareToGalois" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "Galois trace comparison validates against concrete Weil--Deligne and Frobenius APIs"
  },
  {
    packageId := "HT-TRACE-P04",
    leafLedgerId := "HT-TRACE-L04",
    title := "cohomological extraction of parameter pairs",
    localDuty :=
      "extract automorphic and Galois parameters from relevant cohomology classes and prove smooth admissible and Frobenius-semisimple side conditions",
    upstreamInputs := [ "HT-TRACE-P02", "HT-TRACE-P03", "LadicCohomologyRealizationInput" ],
    downstreamOutputs := [ "CohomologicalParameterExtractionInput" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "parameter extraction maps and side-condition proofs validate repo-locally"
  },
  {
    packageId := "HT-TRACE-P05",
    leafLedgerId := "HT-TRACE-L05",
    title := "local correspondence and factor compatibility from extraction",
    localDuty :=
      "prove that the extracted parameter pairs satisfy local Langlands correspondence and preserve local factors",
    upstreamInputs := [ "HT-TRACE-P04", "LocalLanglandsData.Corresponds", "local factor APIs" ],
    downstreamOutputs := [ "HarrisTaylorTraceCohomologyBridge", "HarrisTaylorPackage.traceBridgeReady" ],
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "trace/cohomology bridge closes the correspondence and local-factor obligations in the local Lake closure"
  }
]

/-- The Harris--Taylor trace bridge split has exactly the requested five rows. -/
theorem harrisTaylorTraceBridgeLeaves_length :
    harrisTaylorTraceBridgeLeaves.length = 5 :=
  rfl

/-- All current Harris--Taylor trace bridge leaves are explicitly unchecked. -/
theorem harrisTaylorTraceBridgeLeaves_statuses :
    harrisTaylorTraceBridgeLeaves.map (fun row => row.status) =
      [ "unchecked", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each Harris--Taylor trace bridge leaf is budgeted at at most 100 local proof steps. -/
theorem harrisTaylorTraceBridgeLeaves_budgets :
    harrisTaylorTraceBridgeLeaves.map (fun row => row.localStepBudget) =
      [100, 100, 100, 100, 100] :=
  rfl

/--
Canonical one-element index type for the rank-one branch.

For `n = 1`, the automorphic side should reduce from `GL_n(K)` to `GL_1(K)`,
and then to the multiplicative group `Kˣ`.  This alias fixes the checked
rank-one index without claiming the `GL_1(K) ≃ Kˣ` identification.
-/
abbrev RankOneIndex : Type :=
  PUnit

/-- The checked cardinality normalization for the rank-one index. -/
theorem rankOneIndex_card :
    Fintype.card RankOneIndex = 1 := by
  simp [RankOneIndex]

/-- The current repo-local `GL_1(K)` substrate, expressed using the rank-one index. -/
abbrev RankOneGL
    (K : Type uK) [Field K] : Type uK :=
  GLn RankOneIndex K

/-- The multiplicative group of the local field, the expected automorphic substrate for `n = 1`. -/
abbrev RankOneFieldUnits
    (K : Type uK) [Field K] : Type uK :=
  Kˣ

/--
The available abelian Galois-side substrate for the local class-field-theory branch.

Pinned mathlib exposes the topological abelianization of the absolute Galois
group.  The local reciprocity map from `Kˣ` to this object is not present in the
repo-local closure.
-/
abbrev RankOneAbelianizedGalois
    (K : Type uK) [Field K] : Type uK :=
  Field.absoluteGaloisGroupAbelianization K

/--
Abstract local class-field-theory endpoint for the rank-one branch.

This records exactly the `n = 1` route that would close local Langlands via
local reciprocity.  It remains an API boundary: the current repository does not
construct the reciprocity map or prove the finite-level compatibility and
character correspondence laws.
-/
structure RankOneLocalClassFieldEndpoint
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  AutomorphicCharacter : Type uι
  GaloisCharacter : Type uι
  localReciprocityMap : RankOneFieldUnits K →* RankOneAbelianizedGalois K
  IsContinuousReciprocityMap : Prop
  hasDenseImageOrFiniteLevelSurjectivity : Prop
  compatibleWithFiniteAbelianExtensions : Prop
  pullbackAlongReciprocity : GaloisCharacter → AutomorphicCharacter
  pushforwardAlongReciprocity : AutomorphicCharacter → GaloisCharacter
  pullback_pushforward_inverse : Prop
  pushforward_pullback_inverse : Prop

/--
The isolated `n = 1` local Langlands branch.

This branch is intentionally separate from the Harris--Taylor geometric route:
mathematically it should be supplied by local class field theory.  Repo-locally
it is not closed, because the `GL_1(K) ≃ Kˣ` endpoint identification, local
reciprocity theorem, and character-correspondence proof are not available as
checked Lean declarations or pinned dependencies.
-/
structure RankOneLocalLanglandsBranch
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  endpoints : LocalLanglandsEndpointCategories K ι
  rank_eq_one : endpoints.rank = 1
  rankIndexEquiv : endpoints.RankIndex ≃ RankOneIndex
  classFieldEndpoint : RankOneLocalClassFieldEndpoint K ι
  identifiesGL1WithFieldUnits : Prop
  identifiesGaloisSideWithAbelianizedAbsoluteGalois : Prop
  rankOneCorrespondenceFromLocalReciprocity : Prop
  preservesRankOneLocalFactors : Prop

/-- One M0387-style leaf row for the `n = 1` local class-field-theory branch. -/
structure RankOneLocalCFTLeaf where
  packageId : String
  leafLedgerId : String
  title : String
  localDuty : String
  repoLocalAnchor : String
  missingClosure : String
  localStepBudget : Nat
  status : String
  debtClass : String
  completionGate : String
deriving Repr, DecidableEq

/--
Integration-ready theorem-tree split for the rank-one local class-field-theory
branch.

Only the rank-one index and the available substrates are checked locally.  The
actual local class-field-theory closure remains formalization debt in this
repo-local Lean dependency closure.
-/
def rankOneLocalCFTLeaves : List RankOneLocalCFTLeaf := [
  {
    packageId := "HT-LR-P01",
    leafLedgerId := "HT-LR-L01",
    title := "rank-one index and substrates",
    localDuty :=
      "fix the one-element rank index and name the repo-local substrates GL_1(K), K^*, and the abelianized absolute Galois group",
    repoLocalAnchor :=
      "RankOneIndex, rankOneIndex_card, RankOneGL, RankOneFieldUnits, RankOneAbelianizedGalois",
    missingClosure :=
      "no terminal local Langlands theorem is implied by the substrate names",
    localStepBudget := 20,
    status := "checked-local-boundary",
    debtClass := "none_for_boundary",
    completionGate :=
      "rank-one index normalization validates with lake env lean"
  },
  {
    packageId := "HT-LR-P02",
    leafLedgerId := "HT-LR-L02",
    title := "GL_1(K) to field units",
    localDuty :=
      "provide a checked multiplicative equivalence between GL_1(K) and K^* compatible with the endpoint category",
    repoLocalAnchor :=
      "RankOneGL and RankOneFieldUnits are named, but no equivalence proof is provided",
    missingClosure :=
      "checked GL_1(K) ≃* K^* endpoint identification",
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "the GL_1-to-units equivalence validates as a local proof body or checked imported theorem"
  },
  {
    packageId := "HT-LR-P03",
    leafLedgerId := "HT-LR-L03",
    title := "local reciprocity map",
    localDuty :=
      "construct the local reciprocity map from K^* to the abelianized absolute Galois group with the required continuity and finite-level compatibility",
    repoLocalAnchor :=
      "Field.absoluteGaloisGroupAbelianization is available from pinned mathlib",
    missingClosure :=
      "no repo-local local reciprocity map or local class field theory theorem was located",
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "local reciprocity and finite abelian extension compatibility validate repo-locally"
  },
  {
    packageId := "HT-LR-P04",
    leafLedgerId := "HT-LR-L04",
    title := "character correspondence",
    localDuty :=
      "prove that pullback and pushforward along local reciprocity give inverse automorphic/Galois character correspondences",
    repoLocalAnchor :=
      "RankOneLocalClassFieldEndpoint names pullbackAlongReciprocity and pushforwardAlongReciprocity",
    missingClosure :=
      "no concrete character categories or inverse correspondence proof are available",
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "rank-one character correspondence validates against concrete character APIs"
  },
  {
    packageId := "HT-LR-P05",
    leafLedgerId := "HT-LR-L05",
    title := "rank-one local Langlands wrapper",
    localDuty :=
      "wrap local class field theory as the n = 1 local Langlands branch and link it back to the parent endpoint categories",
    repoLocalAnchor :=
      "RankOneLocalLanglandsBranch records the intended wrapper boundary",
    missingClosure :=
      "no local proof body or pinned upstream Lean 4 dependency closes the wrapper",
    localStepBudget := 100,
    status := "unchecked",
    debtClass := "formalization_debt",
    completionGate :=
      "a local wrapper theorem validates after the GL_1, reciprocity, and character-correspondence leaves are checked"
  }
]

/-- The rank-one local class-field-theory split has exactly five rows. -/
theorem rankOneLocalCFTLeaves_length :
    rankOneLocalCFTLeaves.length = 5 :=
  rfl

/-- The rank-one branch has one checked boundary row and four unchecked proof rows. -/
theorem rankOneLocalCFTLeaves_statuses :
    rankOneLocalCFTLeaves.map (fun row => row.status) =
      [ "checked-local-boundary", "unchecked", "unchecked", "unchecked", "unchecked" ] :=
  rfl

/-- Each rank-one local class-field-theory leaf is budgeted at at most 100 local proof steps. -/
theorem rankOneLocalCFTLeaves_budgets :
    rankOneLocalCFTLeaves.map (fun row => row.localStepBudget) =
      [20, 100, 100, 100, 100] :=
  rfl

/-- Machine status for the isolated rank-one branch in the current repo-local closure. -/
def rankOneLocalCFTMachineStatus : String :=
  "not_repo_local_closed"

/-- Debt classification for the isolated rank-one branch in the current repo-local closure. -/
def rankOneLocalCFTDebtClass : String :=
  "formalization_debt"

/-- Search terms used for the rank-one local class-field-theory closure decision. -/
def rankOneLocalCFTSearchTerms : List String := [
  "ClassField",
  "LocalClassField",
  "local class field",
  "local reciprocity",
  "reciprocity",
  "Artin",
  "WeilGroup",
  "WeilDeligne",
  "LocalLanglands"
]

/--
Repo-local closure decision for the `n = 1` local class-field-theory branch.

No Lean 4 closure for local class field theory or rank-one local Langlands is
present in the current repository dependencies.  Since no external checked Lean
4 proof is being claimed, this is formalization debt rather than a completed
state with repo-local integration debt.
-/
def rankOneLocalCFTClosureDecision : String :=
  "No repo-local Lean 4 local class-field-theory closure was located; the n = 1 branch remains formalization_debt."

/--
Statement-shape package for Harris--Taylor.

`Nonempty (HarrisTaylorPackage K ι)` is the current Stage1 normalized boundary:
it says that the local correspondence data and the Harris--Taylor geometric
machinery have been instantiated and that the expected existence, uniqueness,
and local-factor compatibility laws are available.  This file does not prove
that package exists.
-/
structure HarrisTaylorPackage
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  localData : LocalLanglandsData K ι
  geometry : HarrisTaylorGeometricInput K ι
  traceBridge : HarrisTaylorTraceCohomologyBridge localData geometry
  geometricInputReady :
    geometry.hasBadReductionGeometry ∧
      geometry.hasTraceFormulaComparison ∧
        geometry.realizesLocalParameters
  traceBridgeReady :
    traceBridge.traceComparison.identifiesMatchingTraceTerms ∧
      traceBridge.traceComparisonFeedsCohomology ∧
        traceBridge.extractsLocalLanglandsCorrespondence ∧
          traceBridge.preservesLocalFactorsAfterExtraction
  exists_galois :
    ∀ a : localData.AutomorphicParameter,
      localData.IsSmoothIrreducibleAdmissible a →
        ∃ g : localData.GaloisParameter,
          localData.Corresponds a g ∧ localData.preservesLocalFactors a g
  exists_automorphic :
    ∀ g : localData.GaloisParameter,
      localData.IsFrobeniusSemisimpleWeilDeligne g →
        ∃ a : localData.AutomorphicParameter,
          localData.Corresponds a g ∧ localData.preservesLocalFactors a g
  functional :
    ∀ a g₁ g₂,
      localData.Corresponds a g₁ →
        localData.Corresponds a g₂ → g₁ = g₂
  injective :
    ∀ a₁ a₂ g,
      localData.Corresponds a₁ g →
        localData.Corresponds a₂ g → a₁ = a₂

/--
Lean statement-shape candidate for the Harris--Taylor theorem.

The theorem source is normalized as a proposition over an explicit
nonarchimedean local field `K` and coefficient/index universe `ι`.  A future
terminal artifact should either prove this proposition from concrete definitions
or wrap a pinned upstream Lean 4 theorem.
-/
def StatementShape
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Prop :=
  Nonempty (HarrisTaylorPackage K ι)

/-- The statement-shape definition unfolds to nonemptiness of the proof package. -/
theorem statementShape_iff_nonempty
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) :
    StatementShape K ι ↔ Nonempty (HarrisTaylorPackage K ι) :=
  Iff.rfl

/--
Introduction form for the current statement-normalization boundary.

This packages a concrete `HarrisTaylorPackage` as `StatementShape`.  It is only
a boundary helper: it does not construct the package and is not a terminal
Harris--Taylor/local-Langlands proof.
-/
theorem statementShape_of_package
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι)
    (pkg : HarrisTaylorPackage K ι) :
    StatementShape K ι :=
  ⟨pkg⟩

/--
Elimination form for the current statement-normalization boundary.

Any future terminal proof or pinned upstream wrapper for Harris--Taylor must
provide enough concrete data to inhabit `HarrisTaylorPackage`; this theorem
only exposes that obligation from `StatementShape`.
-/
theorem package_nonempty_of_statementShape
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) :
    StatementShape K ι → Nonempty (HarrisTaylorPackage K ι) :=
  id

/-- A locally checked mathlib anchor: the residue field of a nonarchimedean local field is finite. -/
theorem residueField_finite
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Finite 𝓀[K] := by
  infer_instance

/-- A locally checked mathlib anchor: the normalized value group is isomorphic to `ℤᵐ⁰`. -/
theorem valueGroupWithZero_iso_int
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] :
    Nonempty (ValueGroupWithZero K ≃*o ℤᵐ⁰) := by
  exact ⟨IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt K⟩

/--
mathlib modules checked while locating repo-local anchors for this slot.

These imports are audited anchors only.  They expose local-field, absolute
Galois group, profinite Galois, general linear group, ordinary representation,
`Rep`, etale, ell-adic cohomology, and adele-ring infrastructure in the pinned
mathlib closure; they do not provide a terminal Harris--Taylor theorem.
-/
def mathlibAnchorModules : List String := [
  "Mathlib.NumberTheory.LocalField.Basic",
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.FieldTheory.Galois.Profinite",
  "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic",
  "Mathlib.RepresentationTheory.Basic",
  "Mathlib.RepresentationTheory.Rep.Basic",
  "Mathlib.AlgebraicGeometry.Sites.ElladicCohomology",
  "Mathlib.AlgebraicGeometry.Morphisms.Etale",
  "Mathlib.NumberTheory.NumberField.AdeleRing"
]

/-- Search terms that did not locate a terminal Harris--Taylor theorem in the pinned closure. -/
def absentTerminalSearchTerms : List String := [
  "Harris",
  "Taylor",
  "HarrisTaylor",
  "Langlands",
  "LocalLanglands",
  "WeilDeligne",
  "WeilGroup",
  "Shimura",
  "Igusa",
  "Automorphic",
  "smooth representation"
]

/-- One primary-source Lean 4 external-audit row for the Harris--Taylor slot. -/
structure ExternalLeanAuditRow where
  searchTerm : String
  repoURL : String
  commit : String
  moduleOrTheoremNames : List String
  toolchain : String
  lakeDependencyFeasibility : String
  status : String
  notes : String
deriving Repr, DecidableEq

/-- Exact C007 search terms requested by the Stage1 external-audit child. -/
def c007ExternalAuditSearchTerms : List String := [
  "HarrisTaylor",
  "Harris-Taylor",
  "LocalLanglands",
  "WeilDeligne",
  "WeilGroup",
  "Igusa",
  "nearby cycles"
]

/--
Authentication status for the C007 external Lean 4 audit.

The environment had no logged-in GitHub CLI host, and the unauthenticated GitHub
code-search API was rate-limited.  The audit therefore records primary-source
fallbacks but does not claim that an authenticated global code search certified
absence of an upstream proof.
-/
def c007ExternalAuditAuthenticationStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub hosts; unauthenticated GitHub code search was rate-limited"

/--
Primary-source Lean 4 audit rows for C007.

No row supplies a terminal Harris--Taylor/local-Langlands theorem.  The mathlib
row is already pinned in this repository but has only substrate APIs.  The
`ClassFieldTheory` row is a relevant Lean 4 local-CFT source candidate, but it
contains proof placeholders and no terminal Harris--Taylor or local Langlands
theorem, so it is not pin-ready completion evidence.
-/
def c007ExternalLeanAuditRows : List ExternalLeanAuditRow := [
  {
    searchTerm := "HarrisTaylor; Harris-Taylor; LocalLanglands; WeilDeligne; WeilGroup; Igusa; nearby cycles",
    repoURL := "https://github.com/leanprover-community/mathlib4",
    commit := pinnedMathlibRevision,
    moduleOrTheoremNames := [
      "Mathlib.NumberTheory.LocalField.Basic",
      "Mathlib.FieldTheory.AbsoluteGaloisGroup",
      "Mathlib.FieldTheory.Galois.Profinite",
      "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic",
      "Mathlib.RepresentationTheory.Basic",
      "Mathlib.RepresentationTheory.Rep.Basic",
      "Mathlib.AlgebraicGeometry.Sites.ElladicCohomology",
      "Mathlib.AlgebraicGeometry.Morphisms.Etale",
      "Mathlib.NumberTheory.NumberField.AdeleRing",
      "IsNonarchimedeanLocalField.valueGroupWithZeroIsoInt",
      "Field.absoluteGaloisGroup",
      "Matrix.GeneralLinearGroup",
      "Representation"
    ],
    toolchain := "Lean 4.29.0 in this repository",
    lakeDependencyFeasibility :=
      "already pinned in this repository; no terminal Harris--Taylor theorem is present to wrap",
    status := "substrate_only_not_terminal",
    notes :=
      "repo-local search found local-field, Galois, GL_n, representation, etale, ell-adic, and adele substrates, but no terminal Harris--Taylor/local-Langlands declaration"
  },
  {
    searchTerm := "LocalClassField; local CFT; local reciprocity; LocalLanglands",
    repoURL := "https://github.com/kbuzzard/ClassFieldTheory",
    commit := "11f0a7f3874b6891e8e8290d1e645d61ed06e1aa",
    moduleOrTheoremNames := [
      "ClassFieldTheory.LocalCFT.Continuity.continuous_algebraMap_of_density",
      "ClassFieldTheory.LocalCFT.Teichmuller",
      "ClassFieldTheory.IsNonarchimedeanLocalField.HerbrandQuotient.Rep.herbrandQuotient_isNonarchimedeanLocalField_integer_units"
    ],
    toolchain := "leanprover/lean4:v4.29.0",
    lakeDependencyFeasibility :=
      "not completion-feasible for this slot: no terminal Harris--Taylor/local-Langlands theorem, proof placeholders remain, and its mathlib pin differs from this repository",
    status := "candidate_not_terminal_not_pin_ready",
    notes :=
      "primary-source clone disables proof-placeholder warnings and contains proof placeholders; it is not anchor-only completion evidence"
  },
  {
    searchTerm := "authenticated GitHub code search for the seven requested strings",
    repoURL := "not_available",
    commit := "not_available",
    moduleOrTheoremNames := [],
    toolchain := "not_available",
    lakeDependencyFeasibility :=
      "blocked until a GitHub-authenticated code search can run and any candidate can be pinned/imported/checked",
    status := "authentication_blocked",
    notes :=
      "gh auth status reported no logged-in hosts; unauthenticated GitHub code search returned a rate-limit error"
  }
]

/-- C007 conclusion: no terminal external Lean 4 closure was verified. -/
def c007ExternalAuditTerminalClosureFound : Bool := false

/-- C007 does not claim repo-local completion from anchor-only external evidence. -/
def c007ExternalAuditRepoLocalCompletionClaimed : Bool := false

/-- Machine status after the C007 external audit. -/
def c007ExternalAuditMachineStatus : String :=
  "not_repo_local_closed"

/-- Debt class after the C007 external audit. -/
def c007ExternalAuditDebtClass : String :=
  "formalization_debt"

/-- The C007 audit records exactly the seven requested search terms. -/
theorem c007ExternalAuditSearchTerms_length :
    c007ExternalAuditSearchTerms.length = 7 :=
  rfl

/-- The C007 audit has no verified terminal external Lean 4 proof closure. -/
theorem c007ExternalAuditTerminalClosureFound_eq_false :
    c007ExternalAuditTerminalClosureFound = false :=
  rfl

/-- C007 keeps anchor-only external evidence out of completed repo-local status. -/
theorem c007ExternalAuditRepoLocalCompletionClaimed_eq_false :
    c007ExternalAuditRepoLocalCompletionClaimed = false :=
  rfl

/--
Required shape of a future pinned upstream wrapper for the Harris--Taylor slot.

This structure is only a gate target.  It does not assert that such an upstream
proof exists.  A future completion claim must populate the source coordinates,
bring the dependency or vendored proof body into this repository's Lake closure,
and provide a checked local wrapper for `StatementShape`.
-/
structure PinnedHarrisTaylorWrapperGate
    (K : Type uK) [Field K] [ValuativeRel K] [TopologicalSpace K]
    [IsNonarchimedeanLocalField K] (ι : Type uι) : Type (max uK (uι + 1)) where
  upstreamRepoURL : String
  upstreamCommit : String
  upstreamModule : String
  upstreamTheoremName : String
  dependencyOrVendorPath : String
  localValidationCommand : String
  localWrapper : StatementShape K ι

/-- One C008 wrapper-gate row for repo-local completion control. -/
structure WrapperGateRow where
  gateId : String
  condition : String
  requiredRepoLocalAction : String
  currentEvidence : String
  gateStatus : String
  debtClass : String
  completionAllowed : Bool
deriving Repr, DecidableEq

/--
C008 wrapper-gate rows.

The gate is not triggered in the current artifact because C007 did not verify a
terminal upstream Lean 4 Harris--Taylor/local-Langlands closure.  Therefore no
pinned dependency, vendored proof body, or terminal local wrapper is claimed
here.
-/
def c008WrapperGateRows : List WrapperGateRow := [
  {
    gateId := "HT-WRAP-G01",
    condition := "terminal Lean 4 Harris--Taylor or local-Langlands upstream closure found",
    requiredRepoLocalAction :=
      "pin a Lake dependency or vendor the proof body, then expose a checked local wrapper inhabiting StatementShape",
    currentEvidence := "c007ExternalAuditTerminalClosureFound = false",
    gateStatus := "not_triggered_no_upstream_closure_verified",
    debtClass := "formalization_debt",
    completionAllowed := false
  },
  {
    gateId := "HT-WRAP-G02",
    condition := "anchor-only external evidence exists",
    requiredRepoLocalAction :=
      "do not mark completed; either import/check the upstream proof or record a concrete integration blocker",
    currentEvidence := "no terminal external theorem row is present in c007ExternalLeanAuditRows",
    gateStatus := "anchor_only_completion_forbidden",
    debtClass := "no_completed_repo_local_integration_debt",
    completionAllowed := false
  },
  {
    gateId := "HT-WRAP-G03",
    condition := "future wrapper or dependency changes this Lean artifact",
    requiredRepoLocalAction :=
      "rerun cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_062.lean",
    currentEvidence := "current child adds gate metadata only",
    gateStatus := "validation_required_for_future_wrapper",
    debtClass := "formalization_debt_until_wrapper_validates",
    completionAllowed := false
  }
]

/-- C008 gate trigger mirrors the C007 terminal-closure decision. -/
def c008WrapperGateTriggered : Bool :=
  c007ExternalAuditTerminalClosureFound

/-- No C008 pinned dependency was added, because no terminal upstream closure was verified. -/
def c008PinnedDependencyAdded : Bool := false

/-- No C008 vendored proof body was added, because no terminal upstream closure was verified. -/
def c008VendoredProofBodyAdded : Bool := false

/-- No C008 terminal local wrapper was added, because no proof body is available to wrap. -/
def c008LocalTerminalWrapperAdded : Bool := false

/-- C008 current completion gate: completion requires trigger, proof source, and local wrapper. -/
def c008WrapperGateCompletionAllowed : Bool :=
  c008WrapperGateTriggered &&
    (c008PinnedDependencyAdded || c008VendoredProofBodyAdded) &&
      c008LocalTerminalWrapperAdded

/-- Machine status for the C008 wrapper gate in the current repo-local closure. -/
def c008WrapperGateMachineStatus : String :=
  "not_repo_local_closed"

/-- Debt class for the C008 wrapper gate in the current repo-local closure. -/
def c008WrapperGateDebtClass : String :=
  "formalization_debt"

/-- Repo-local integration-debt gate result for C008. -/
def c008WrapperGateRepoLocalIntegrationDebtGate : String :=
  "passed_no_completion_claim: no external upstream closure is claimed, and anchor-only evidence is not treated as completed"

/-- The C008 wrapper gate has exactly the three current control rows. -/
theorem c008WrapperGateRows_length :
    c008WrapperGateRows.length = 3 :=
  rfl

/-- C008 is not triggered because C007 did not verify a terminal upstream closure. -/
theorem c008WrapperGateTriggered_eq_false :
    c008WrapperGateTriggered = false :=
  rfl

/-- C008 has no pinned dependency in the current repo-local closure. -/
theorem c008PinnedDependencyAdded_eq_false :
    c008PinnedDependencyAdded = false :=
  rfl

/-- C008 has no vendored proof body in the current repo-local closure. -/
theorem c008VendoredProofBodyAdded_eq_false :
    c008VendoredProofBodyAdded = false :=
  rfl

/-- C008 has no terminal local wrapper in the current repo-local closure. -/
theorem c008LocalTerminalWrapperAdded_eq_false :
    c008LocalTerminalWrapperAdded = false :=
  rfl

/-- C008 currently forbids a public completion claim. -/
theorem c008WrapperGateCompletionAllowed_eq_false :
    c008WrapperGateCompletionAllowed = false :=
  rfl

/-- One C009 validation row for the Harris--Taylor Stage1 Lean artifact. -/
structure ValidationGateRow where
  gateId : String
  artifactPath : String
  validationCommand : String
  validationDuty : String
  expectedPassingResult : String
  completionClaimAllowed : Bool
  debtGate : String
deriving Repr, DecidableEq

/--
C009 validation gate for this Stage1 artifact.

This records the exact repo-local command that must be rerun after every change
to this file.  It is a validation/control surface only; it does not upgrade the
Harris--Taylor theorem beyond the checked statement-boundary and audit records
above.
-/
def c009ValidationGateRows : List ValidationGateRow := [
  {
    gateId := "HT-VALID-C009",
    artifactPath := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_062.lean",
    validationCommand := "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_062.lean",
    validationDuty :=
      "rerun the targeted Lean command after every Lean artifact change and record the exact exit status and output in the private child ledger",
    expectedPassingResult := "exit code 0 with no Lean output",
    completionClaimAllowed := false,
    debtGate :=
      "passed only as a checked formal boundary; no terminal Harris--Taylor proof or external upstream closure is claimed"
  }
]

/-- C009 validates exactly one current artifact-command pair. -/
theorem c009ValidationGateRows_length :
    c009ValidationGateRows.length = 1 :=
  rfl

/-- C009 does not permit a theorem-completion claim from validation alone. -/
theorem c009ValidationGateCompletionClaimAllowed_eq_false :
    (c009ValidationGateRows.map (fun row => row.completionClaimAllowed)) = [false] :=
  rfl

/-- Repo-local integration-debt gate result for C009. -/
def c009RepoLocalIntegrationDebtGate : String :=
  "passed_no_completion_claim: validation checks the local boundary only, and no anchor-only external proof evidence is treated as completed"

end AwesomeTheorems.Stage1.S1_M_062
