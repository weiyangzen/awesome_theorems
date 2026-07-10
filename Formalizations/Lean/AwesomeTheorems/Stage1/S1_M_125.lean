import Mathlib.Algebra.Homology.EulerCharacteristic
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.CategoryTheory.Sites.SheafCohomology.Cech
import Mathlib.Geometry.Manifold.VectorBundle.Tangent
import Mathlib.GroupTheory.MonoidLocalization.GrothendieckGroup

/-!
# S1-M-125 / THM-M-0176: Hirzebruch-Riemann-Roch theorem

This Stage1 artifact records a conservative Lean 4 boundary for the
Hirzebruch-Riemann-Roch theorem for smooth projective varieties.

The pinned mathlib snapshot provides schemes, sheaves of modules on a scheme,
smooth and proper morphism predicates, generic homological Euler
characteristics, and an algebraic Grothendieck-group construction.  This audit
did not find terminal Lean 4 APIs for coherent sheaf Euler characteristics,
algebraic K-theory of vector bundles or perfect complexes, Chern characters,
Todd classes, Chow/cohomology cycle classes, or integration over a smooth
projective variety.

The declarations below therefore normalize the scheme-theoretic input and the
expected equality shape, while keeping the missing characteristic-class package
explicit.  They introduce no proof placeholders or new axioms.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits AlgebraicGeometry Manifold

universe u v w x

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_125

/--
Geometric input for a future Hirzebruch-Riemann-Roch statement.

The structural morphism `X -> base` is tied to mathlib's current scheme API.
`base_isFieldSpectrum`, `projective`, and `pureDimension` are kept as explicit
data because this audit did not identify a single mature projective-variety API
that packages the classical hypotheses over a field.
-/
structure SmoothProjectiveVarietyInput : Type (u + 1) where
  base : Scheme.{u}
  space : Scheme.{u}
  structuralMorphism : space ⟶ base
  base_isFieldSpectrum : Prop
  smooth : Smooth structuralMorphism
  proper : IsProper structuralMorphism
  locallyOfFiniteType : LocallyOfFiniteType structuralMorphism
  projective : Prop
  pureDimension : ℕ
  coherentOrVectorBundle : space.Modules → Prop

/--
Characteristic-class and Euler-characteristic data expected by
Hirzebruch-Riemann-Roch.

For a sheaf or vector bundle `F`, the classical equality is
`χ(X,F) = ∫_X ch(F) * Td(T_X)`.  The target ring, Chern character, Todd class,
and integration/degree map are abstract here because they are not currently
available as a complete mathlib HRR substrate.
-/
structure HirzebruchRiemannRochPackage
    (D : SmoothProjectiveVarietyInput.{u}) : Type (max (u + 1) (v + 1)) where
  characteristicRing : Type v
  instRing : Ring characteristicRing
  chernCharacter : D.space.Modules → characteristicRing
  toddClassTangent : characteristicRing
  integrateTopClass : characteristicRing → ℚ
  holomorphicEulerCharacteristic : D.space.Modules → ℤ
  hrr_formula :
    ∀ F : D.space.Modules,
      D.coherentOrVectorBundle F →
        letI := instRing
        ((holomorphicEulerCharacteristic F : ℤ) : ℚ) =
          integrateTopClass (chernCharacter F * toddClassTangent)

/-- Formula-level view of the HRR equality for a fixed input package. -/
def HirzebruchRiemannRochFormula
    {D : SmoothProjectiveVarietyInput.{u}}
    (P : HirzebruchRiemannRochPackage.{u, v} D) (F : D.space.Modules) : Prop :=
  letI := P.instRing
  ((P.holomorphicEulerCharacteristic F : ℤ) : ℚ) =
    P.integrateTopClass (P.chernCharacter F * P.toddClassTangent)

/--
Stage1 normalized statement-shape candidate for THM-M-0176.

For every smooth proper finite-type scheme over a field, once it is known to be
projective and the sheaf lies in the intended coherent/vector-bundle class,
there should be a characteristic-class package satisfying the HRR equality.
This is a statement shape, not a completed proof of HRR.
-/
def StatementShape : Prop :=
  ∀ D : SmoothProjectiveVarietyInput.{u},
    D.base_isFieldSpectrum →
      D.projective →
        ∀ F : D.space.Modules,
          D.coherentOrVectorBundle F →
            ∃ P : HirzebruchRiemannRochPackage.{u, v} D,
              HirzebruchRiemannRochFormula P F

/-- The statement-shape definition unfolds to the characteristic-class package. -/
theorem statementShape_iff_exists_package :
    StatementShape.{u, v} ↔
      ∀ D : SmoothProjectiveVarietyInput.{u},
        D.base_isFieldSpectrum →
          D.projective →
            ∀ F : D.space.Modules,
              D.coherentOrVectorBundle F →
                ∃ P : HirzebruchRiemannRochPackage.{u, v} D,
                  HirzebruchRiemannRochFormula P F :=
  Iff.rfl

/-- Checked substrate: a scheme module object is backed by a sheaf condition. -/
theorem module_sheaf_is_sheaf (X : Scheme.{u}) (M : X.Modules) :
    M.presheaf.IsSheaf :=
  Scheme.Modules.isSheaf M

/-- Checked substrate: the stored geometric input exposes mathlib smoothness. -/
theorem structuralMorphism_smooth (D : SmoothProjectiveVarietyInput.{u}) :
    Smooth D.structuralMorphism :=
  D.smooth

/-- Checked substrate: the stored geometric input exposes mathlib properness. -/
theorem structuralMorphism_proper (D : SmoothProjectiveVarietyInput.{u}) :
    IsProper D.structuralMorphism :=
  D.proper

/-- Checked substrate: the stored geometric input exposes finite-type localness. -/
theorem structuralMorphism_locallyOfFiniteType
    (D : SmoothProjectiveVarietyInput.{u}) :
    LocallyOfFiniteType D.structuralMorphism :=
  D.locallyOfFiniteType

/-- A local alias for mathlib's generic homological Euler characteristic. -/
abbrev HomologicalComplexEulerChar
    (R : Type u) [Ring R] {ι : Type v} {c : ComplexShape ι}
    [c.EulerCharSigns] (C : HomologicalComplex (ModuleCat R) c) : ℤ :=
  HomologicalComplex.eulerChar C

/-- A local alias for mathlib's generic homology-side Euler characteristic. -/
abbrev HomologicalComplexHomologyEulerChar
    (R : Type u) [Ring R] {ι : Type v} {c : ComplexShape ι}
    [c.EulerCharSigns] (C : HomologicalComplex (ModuleCat R) c)
    [∀ i : ι, C.HasHomology i] : ℤ :=
  HomologicalComplex.homologyEulerChar C

/-- Local alias for mathlib's site-level cohomology group of an abelian sheaf. -/
abbrev SiteSheafCohomologyGroup
    {C : Type u} [Category.{v} C] {J : GrothendieckTopology C}
    (F : Sheaf J AddCommGrpCat.{v})
    [HasSheafify J AddCommGrpCat.{v}] [HasExt.{w} (Sheaf J AddCommGrpCat.{v})]
    (n : ℕ) : Type w :=
  Sheaf.H F n

/--
Local alias for mathlib's cohomology presheaf attached to an abelian sheaf on a
site. This is generic site cohomology, not yet coherent sheaf cohomology on a
scheme.
-/
abbrev SiteSheafCohomologyPresheaf
    {C : Type u} [Category.{v} C] {J : GrothendieckTopology C}
    [HasSheafify J AddCommGrpCat.{v}] [HasExt.{w} (Sheaf J AddCommGrpCat.{v})]
    (F : Sheaf J AddCommGrpCat.{v}) (n : ℕ) :
    Cᵒᵖ ⥤ AddCommGrpCat.{w} :=
  F.cohomologyPresheaf n

/-- Local alias for mathlib's objectwise site cohomology of an abelian sheaf. -/
abbrev SiteObjectSheafCohomology
    {C : Type u} [Category.{v} C] {J : GrothendieckTopology C}
    [HasSheafify J AddCommGrpCat.{v}] [HasExt.{w} (Sheaf J AddCommGrpCat.{v})]
    (F : Sheaf J AddCommGrpCat.{v}) (n : ℕ) (X : C) :
    AddCommGrpCat.{w} :=
  F.H' n X

/-- Local alias for mathlib's Cech cochain complex functor. -/
abbrev CechCochainComplexFunctor
    {C : Type u} [Category.{v} C] {A : Type u} [Category.{v} A]
    [HasProducts.{w} A] [HasFiniteProducts C] [Preadditive A]
    {ι : Type w} (U : ι → C) :
    (Cᵒᵖ ⥤ A) ⥤ CochainComplex A ℕ :=
  cechComplexFunctor U

/-- A local alias for mathlib's algebraic Grothendieck group of a commutative monoid. -/
abbrev GrothendieckGroupOfCommMonoid (M : Type u) [CommMonoid M] : Type u :=
  Algebra.GrothendieckGroup M

/-- Local alias for mathlib's manifold tangent-space API. -/
abbrev ManifoldTangentSpace
    {𝕜 : Type u} [NontriviallyNormedField 𝕜]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type w} [TopologicalSpace H] (I : ModelWithCorners 𝕜 E H)
    {M : Type x} [TopologicalSpace M] [ChartedSpace H M] (point : M) :
    Type v :=
  TangentSpace I point

/-- Local alias for mathlib's manifold tangent-bundle API. -/
abbrev ManifoldTangentBundle
    {𝕜 : Type u} [NontriviallyNormedField 𝕜]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type w} [TopologicalSpace H] (I : ModelWithCorners 𝕜 E H)
    (M : Type x) [TopologicalSpace M] [ChartedSpace H M] :
    Type (max x v) :=
  TangentBundle I M

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Scheme",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Cech",
  "Mathlib.Algebra.Homology.EulerCharacteristic",
  "Mathlib.GroupTheory.MonoidLocalization.GrothendieckGroup",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.CovariantDerivative.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.Scheme.Modules",
  "AlgebraicGeometry.Scheme.Modules.isSheaf",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.IsProper",
  "AlgebraicGeometry.LocallyOfFiniteType",
  "CategoryTheory.Sheaf.H",
  "CategoryTheory.Sheaf.cohomologyPresheaf",
  "CategoryTheory.Sheaf.H'",
  "CategoryTheory.cechComplexFunctor",
  "HomologicalComplex.eulerChar",
  "HomologicalComplex.homologyEulerChar",
  "HomologicalComplex.homologyEulerChar_eq_sum_finSet_of_finrankSupport_subset",
  "Algebra.GrothendieckGroup",
  "Algebra.GrothendieckGroup.of",
  "TangentSpace",
  "TangentBundle",
  "VectorBundle",
  "ContMDiffVectorBundle",
  "CovariantDerivative"
]

/-- Search terms that did not locate a terminal HRR theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Hirzebruch",
  "RiemannRoch",
  "Riemann-Roch",
  "Grothendieck-Riemann-Roch",
  "Todd",
  "Todd class",
  "Chern character",
  "CharacteristicClass",
  "Chow ring",
  "coherent sheaf cohomology",
  "KTheory",
  "K-theory"
]

/--
Primary-source audit row for the C002 external-source search.

`matchedNames` records Lean declaration names when a source contains a nearby
Riemann-Roch theorem.  Rows with an empty list record source-level evidence
that the requested HRR/Chern/Todd/Chow/K-theory terminal names were absent.
-/
structure ExternalHrrLeanAuditRow where
  repositoryUrl : String
  commit : String
  file : String
  matchedNames : List String
  lakeCompatibility : String
  hrrRelevance : String
  integrationGate : String

/-- Date of the C002 primary-source audit, in ISO format. -/
def externalHrrLeanAuditDate : String :=
  "2026-05-01"

/--
C002 audit of current Lean 4 primary sources for HRR-related terminal names.

The external Riemann-Roch projects found by the audit are intentionally kept as
negative/comparison rows: they do not prove Hirzebruch-Riemann-Roch and they do
not provide Chern-character, Todd-class, Chow, or scheme K-theory targets.
-/
def externalHrrLeanAuditRows : List ExternalHrrLeanAuditRow := [
  {
    repositoryUrl := "https://github.com/leanprover-community/mathlib4",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    file := "Mathlib/*.lean; docs/1000.yaml",
    matchedNames := [],
    lakeCompatibility :=
      "repo-pinned dependency; Lean 4.29.0; local rg found only docs/1000.yaml titles for Grothendieck-Hirzebruch-Riemann-Roch and Hirzebruch-Riemann-Roch, with no matching Lean declarations",
    hrrRelevance :=
      "scheme, smooth/proper, module-sheaf, Euler-characteristic, and Grothendieck-group infrastructure only; no terminal HRR/Chern/Todd/Chow/KTheory theorem",
    integrationGate :=
      "no external theorem to pin; keep StatementShape as formalization_debt"
  },
  {
    repositoryUrl := "https://github.com/leanprover-community/flt-regular",
    commit := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
    file := "*.lean",
    matchedNames := [],
    lakeCompatibility :=
      "repo-pinned dependency; imported through this repository's Lake closure; local rg found no requested HRR-related terminal names",
    hrrRelevance :=
      "number-theory dependency only; no HRR, Chern-character, Todd-class, Chow, or K-theory API",
    integrationGate :=
      "no external theorem to pin for THM-M-0176"
  },
  {
    repositoryUrl := "https://github.com/cguth7/roch-riemann-refactor",
    commit := "8e67e8941a083617a8b34a0da3a35a7c2c845f59",
    file :=
      "RrLean/RiemannRochV2/Adelic/EulerCharacteristic.lean; RrLean/RiemannRochV2/Adelic/AdelicH1v2.lean; RrLean/RiemannRochV2/General/WeilDifferential.lean",
    matchedNames := [
      "RiemannRochV2.euler_characteristic",
      "RiemannRochV2.chi_additive",
      "RiemannRochV2.riemann_roch_from_euler",
      "RiemannRochV2.riemann_roch_from_adelic",
      "RiemannRochV2.riemann_roch_from_weil"
    ],
    lakeCompatibility :=
      "Lean 4.27.0-rc1 with mathlib fe3134f0c3508d2fd6394307be226ffa9b8cb4ba; not Lake-compatible with this repo's Lean 4.29.0/mathlib 8a178386 without a port",
    hrrRelevance :=
      "curve-level Riemann-Roch over Dedekind/function-field style inputs; source README reports custom axioms, and local rg found sorries/axioms; no Hirzebruch/Chern/Todd/Chow/KTheory declarations",
    integrationGate :=
      "not a THM-M-0176 HRR proof; do not pin as HRR closure"
  },
  {
    repositoryUrl := "https://github.com/DhyeyMavani2003/chip-firing-with-lean",
    commit := "b624c3fe19a63ad3cf46c15a243da107234016d2",
    file := "ChipFiringWithLean/RiemannRochForGraphs.lean",
    matchedNames := [
      "riemann_roch_for_graphs",
      "riemann_roch_deg_to_rank_corollary"
    ],
    lakeCompatibility :=
      "Lean 4.29.0 and mathlib v4.29.0/8a178386ffc0f5fef0b77738bb5449d50efeea95; Lake-compatible in version but not imported because the theorem is graph-theoretic",
    hrrRelevance :=
      "Baker-Norine Riemann-Roch for finite graphs; no smooth projective variety HRR, Chern-character, Todd-class, Chow, or KTheory content",
    integrationGate :=
      "not a THM-M-0176 HRR proof; do not pin as HRR closure"
  }
]

/-- Checked guard: the C002 audit found no repo-local or pinnable terminal HRR proof. -/
def externalHrrTerminalProofRepoLocalClosed : Bool :=
  false

theorem externalHrrTerminalProofRepoLocalClosed_eq_false :
    externalHrrTerminalProofRepoLocalClosed = false :=
  rfl

/--
C003 integration-gate blockers for the current external HRR audit.

These are not proof obligations for HRR.  They record why the known Lean 4
sources from the primary-source audit cannot be pinned/imported as a terminal
Hirzebruch-Riemann-Roch closure for THM-M-0176.
-/
def externalHrrC003IntegrationBlockers : List String := [
  "pinned mathlib has HRR/GRR titles only in docs/1000.yaml and no terminal HRR Lean declaration",
  "pinned flt-regular dependency has no HRR, Chern-character, Todd-class, Chow, or K-theory API",
  "cguth7/roch-riemann-refactor is curve-level Riemann-Roch on Lean 4.27.0-rc1/mathlib fe3134f0; it is not HRR and has source-level placeholder blockers",
  "DhyeyMavani2003/chip-firing-with-lean proves graph Riemann-Roch, not HRR for smooth projective varieties"
]

/--
C003 repo-local integration decision.

No external Lean 4 terminal HRR proof body is available to pin/import/check in
this repository pass.  The correct state is therefore non-completion with
formalization debt, not a completed `external_upstream_anchor_only` state.
-/
def externalHrrC003IntegrationDecision : String :=
  "no terminal Lean 4 HRR proof found to pin/import/check; keep THM-M-0176 not_repo_local_closed with formalization_debt"

theorem externalHrrC003IntegrationBlockers_length :
    externalHrrC003IntegrationBlockers.length = 4 :=
  rfl

theorem externalHrrC003_no_repo_local_closed :
    externalHrrTerminalProofRepoLocalClosed = false :=
  externalHrrTerminalProofRepoLocalClosed_eq_false

theorem externalHrrLeanAuditRows_length :
    externalHrrLeanAuditRows.length = 4 :=
  rfl

/-! ## HRR-P03 coherent-sheaf Euler package ledger -/

/--
One integration-ready leaf for the `HRR-P03-coherent-sheaf-euler` package.

The `mathlibAPIs` field names actual declarations in the pinned mathlib
snapshot. The `status` field remains textual because most leaves are blocked by
missing bridge APIs rather than by a local proposition to prove.
-/
structure HRRP03LeafLedgerRow where
  leafId : String
  role : String
  mathlibAPIs : List String
  localBudgetUpperBound : ℕ
  status : String

/--
`<=100`-step leaf ledger for `HRR-P03-coherent-sheaf-euler`.

The checked anchors show that mathlib currently supplies generic site
cohomology for abelian sheaves and generic homological Euler characteristics.
The ledger also records the precise missing bridge from scheme modules/coherent
sheaves to finite-dimensional cohomology groups whose alternating dimension is
the HRR Euler characteristic.
-/
def hrrP03CoherentSheafEulerLedger : List HRRP03LeafLedgerRow := [
  {
    leafId := "HRR-P03-L01-site-cohomology-group",
    role :=
      "Use the generic site-cohomology object for an abelian sheaf in degree n.",
    mathlibAPIs := [
      "CategoryTheory.Sheaf.H",
      "CategoryTheory.Sheaf.cohomologyFunctor"
    ],
    localBudgetUpperBound := 20,
    status := "checked_api_anchor"
  },
  {
    leafId := "HRR-P03-L02-objectwise-cohomology",
    role :=
      "Use objectwise sheaf cohomology H^n(U,F) as the target for restrictions.",
    mathlibAPIs := [
      "CategoryTheory.Sheaf.cohomologyPresheaf",
      "CategoryTheory.Sheaf.H'"
    ],
    localBudgetUpperBound := 20,
    status := "checked_api_anchor"
  },
  {
    leafId := "HRR-P03-L03-cech-complex",
    role :=
      "Use the Cech cochain complex functor as the cover-level computation surface.",
    mathlibAPIs := [
      "CategoryTheory.cechComplexFunctor",
      "CategoryTheory.Limits.FormalCoproduct.cochainComplexFunctor"
    ],
    localBudgetUpperBound := 30,
    status := "checked_api_anchor"
  },
  {
    leafId := "HRR-P03-L04-module-sheaf-anchor",
    role :=
      "Relate a scheme module object to mathlib's sheaf condition before any cohomology bridge.",
    mathlibAPIs := [
      "AlgebraicGeometry.Scheme.Modules",
      "AlgebraicGeometry.Scheme.Modules.isSheaf"
    ],
    localBudgetUpperBound := 15,
    status := "checked_local_wrapper: module_sheaf_is_sheaf"
  },
  {
    leafId := "HRR-P03-L05-abelianization-gap",
    role :=
      "Choose or build the functor from algebraic scheme modules/coherent sheaves to abelian sheaves on the relevant site.",
    mathlibAPIs := [
      "AlgebraicGeometry.Scheme.Modules",
      "CategoryTheory.Sheaf.H"
    ],
    localBudgetUpperBound := 80,
    status := "formalization_debt: no repo-local bridge selected"
  },
  {
    leafId := "HRR-P03-L06-coherence-finiteness-gap",
    role :=
      "Attach a concrete coherent or finite-presentation predicate to the sheaf whose cohomology enters HRR.",
    mathlibAPIs := [
      "AlgebraicGeometry.Scheme.Modules"
    ],
    localBudgetUpperBound := 80,
    status := "formalization_debt: current HRR input keeps coherentOrVectorBundle abstract"
  },
  {
    leafId := "HRR-P03-L07-proper-projective-finite-dimensionality",
    role :=
      "Prove finite-dimensionality of every cohomology group needed for the Euler characteristic.",
    mathlibAPIs := [
      "AlgebraicGeometry.IsProper",
      "CategoryTheory.Sheaf.H'",
      "Module.finrank"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: no projective coherent-cohomology finiteness theorem found"
  },
  {
    leafId := "HRR-P03-L08-vanishing-bound",
    role :=
      "Provide a finite cohomological range so the alternating sum has finite support.",
    mathlibAPIs := [
      "CategoryTheory.Sheaf.H'",
      "GradedObject.finrankSupport"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: no scheme-level coherent cohomology vanishing bound found"
  },
  {
    leafId := "HRR-P03-L09-homology-euler-characteristic",
    role :=
      "Use mathlib's homology-side Euler characteristic once a cohomology complex over a field is available.",
    mathlibAPIs := [
      "HomologicalComplex.homologyEulerChar",
      "HomologicalComplex.homologyEulerChar_eq_sum_finSet_of_finrankSupport_subset"
    ],
    localBudgetUpperBound := 35,
    status := "checked_api_anchor"
  },
  {
    leafId := "HRR-P03-L10-cochain-to-module-complex",
    role :=
      "Convert the selected sheaf cohomology construction into a homological/cochain complex in ModuleCat over the base field.",
    mathlibAPIs := [
      "CategoryTheory.cechComplexFunctor",
      "HomologicalComplex.homologyEulerChar"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: no repo-local conversion for coherent scheme cohomology"
  },
  {
    leafId := "HRR-P03-L11-euler-definition",
    role :=
      "Define chi(X,F) as the finite alternating sum of dimensions of coherent sheaf cohomology.",
    mathlibAPIs := [
      "CategoryTheory.Sheaf.H'",
      "Module.finrank",
      "HomologicalComplex.homologyEulerChar"
    ],
    localBudgetUpperBound := 70,
    status := "formalization_debt: blocked by L05-L10"
  },
  {
    leafId := "HRR-P03-L12-euler-functoriality",
    role :=
      "Expose the Euler characteristic as the input expected by the HRR equality package.",
    mathlibAPIs := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage",
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochFormula"
    ],
    localBudgetUpperBound := 40,
    status := "statement_shape_only: no terminal coherent Euler implementation"
  }
]

/-- Number of P03 leaves in the integration-ready ledger. -/
theorem hrrP03CoherentSheafEulerLedger_length :
    hrrP03CoherentSheafEulerLedger.length = 12 :=
  rfl

/-- Checked guard: all current P03 leaf budgets are at most 100 steps. -/
theorem hrrP03CoherentSheafEulerLedger_budgets :
    (hrrP03CoherentSheafEulerLedger.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true :=
  rfl

/-- Checked guard: P03 is not repo-locally closed by the current anchors. -/
def hrrP03CoherentSheafEulerRepoLocalClosed : Bool :=
  false

theorem hrrP03CoherentSheafEulerRepoLocalClosed_eq_false :
    hrrP03CoherentSheafEulerRepoLocalClosed = false :=
  rfl

/-! ## HRR-P04 K-theory and Chern-character package ledger -/

/--
One integration-ready leaf for the `HRR-P04-k-theory-and-chern-character`
package.

`concreteAnchor` is the current repo-local Lean object or external source that
the leaf can honestly reference.  At this snapshot, only the commutative-monoid
Grothendieck group is a checked local implementation; scheme-level K-theory and
the Chern character remain missing APIs.
-/
structure HRRP04LeafLedgerRow where
  leafId : String
  role : String
  concreteAnchor : List String
  localBudgetUpperBound : ℕ
  status : String

/--
`<=100`-step leaf ledger for `HRR-P04-k-theory-and-chern-character`.

The ledger is tied to the concrete local group-completion implementation
`Algebra.GrothendieckGroup` and to the C002/C003 audit decision that no
pin-ready external Lean 4 HRR/K-theory/Chern-character dependency was found.
It deliberately does not claim that mathlib currently has algebraic K-theory of
vector bundles/perfect complexes or a Chern-character map into Chow/cohomology.
-/
def hrrP04KTheoryChernCharacterLedger : List HRRP04LeafLedgerRow := [
  {
    leafId := "HRR-P04-L01-vector-bundle-or-perfect-carrier",
    role :=
      "Choose the exact input category for K_0: vector bundles, locally free sheaves, or perfect complexes on the smooth projective scheme.",
    concreteAnchor := [
      "AlgebraicGeometry.Scheme.Modules",
      "AwesomeTheorems.Stage1.S1_M_125.SmoothProjectiveVarietyInput.coherentOrVectorBundle"
    ],
    localBudgetUpperBound := 80,
    status := "formalization_debt: current carrier is an abstract predicate on Scheme.Modules"
  },
  {
    leafId := "HRR-P04-L02-direct-sum-commutative-monoid",
    role :=
      "Construct the commutative monoid of isomorphism classes under direct sum for the selected K_0 carrier.",
    concreteAnchor := [
      "Algebra.GrothendieckGroup",
      "Algebra.GrothendieckGroup.of"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: group completion exists, but the geometric monoid is not built"
  },
  {
    leafId := "HRR-P04-L03-group-completion-wrapper",
    role :=
      "Use the checked commutative-monoid Grothendieck group as the local K_0 group-completion surface once the carrier monoid is available.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.GrothendieckGroupOfCommMonoid",
      "Algebra.GrothendieckGroup.of"
    ],
    localBudgetUpperBound := 25,
    status := "checked_local_wrapper"
  },
  {
    leafId := "HRR-P04-L04-class-of-sheaf-map",
    role :=
      "Define the class map sending an admissible vector bundle or perfect complex to its K_0 class.",
    concreteAnchor := [
      "Algebra.GrothendieckGroup.of",
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.chernCharacter"
    ],
    localBudgetUpperBound := 60,
    status := "formalization_debt: blocked by L01-L02"
  },
  {
    leafId := "HRR-P04-L05-exact-sequence-additivity",
    role :=
      "Prove that short exact sequences or distinguished triangles impose the additivity relation used by K_0.",
    concreteAnchor := [
      "Mathlib.Algebra.Homology.ShortComplex.Basic",
      "Mathlib.Algebra.Homology.HomologicalComplex"
    ],
    localBudgetUpperBound := 95,
    status := "formalization_debt: no selected exact/perfect-complex K_0 quotient"
  },
  {
    leafId := "HRR-P04-L06-tensor-product-ring-structure",
    role :=
      "Equip K_0 with the product induced by tensor product so the Chern character can be multiplicative.",
    concreteAnchor := [
      "Algebra.GrothendieckGroup",
      "AlgebraicGeometry.Scheme.Modules"
    ],
    localBudgetUpperBound := 95,
    status := "formalization_debt: no scheme-module tensor K_0 ring package selected"
  },
  {
    leafId := "HRR-P04-L07-target-chow-or-cohomology-ring",
    role :=
      "Select the Chow/cohomology target ring in which ch(F) and Td(T_X) live.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.characteristicRing"
    ],
    localBudgetUpperBound := 75,
    status := "statement_shape_only: target ring remains abstract"
  },
  {
    leafId := "HRR-P04-L08-chern-classes",
    role :=
      "Provide Chern classes for the selected vector bundle/perfect-complex carrier.",
    concreteAnchor := [
      "externalHrrC003IntegrationDecision",
      "absentTerminalSearchTerms"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: no pinned local Chern-class API found for algebraic bundles"
  },
  {
    leafId := "HRR-P04-L09-chern-character-map",
    role :=
      "Define the rational Chern character from K_0 to the selected characteristic ring.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.chernCharacter",
      "externalHrrLeanAuditRows"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: current chernCharacter field is an abstract statement boundary"
  },
  {
    leafId := "HRR-P04-L10-chern-character-additivity",
    role :=
      "Prove that the Chern character descends through K_0 additivity relations.",
    concreteAnchor := [
      "Algebra.GrothendieckGroup.lift",
      "Algebra.GrothendieckGroup.lift_apply"
    ],
    localBudgetUpperBound := 80,
    status := "formalization_debt: lift API exists but no concrete Chern-character monoid map exists"
  },
  {
    leafId := "HRR-P04-L11-chern-character-multiplicativity",
    role :=
      "Prove compatibility of the Chern character with tensor product and cup/intersection product.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochFormula"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: blocked by L06-L09"
  },
  {
    leafId := "HRR-P04-L12-hrr-formula-interface",
    role :=
      "Expose ch(F) in the exact interface consumed by the HRR equality package.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage",
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochFormula"
    ],
    localBudgetUpperBound := 40,
    status := "statement_shape_only: no terminal K-theory/Chern-character implementation"
  }
]

/-- Number of P04 leaves in the integration-ready ledger. -/
theorem hrrP04KTheoryChernCharacterLedger_length :
    hrrP04KTheoryChernCharacterLedger.length = 12 :=
  rfl

/-- Checked guard: all current P04 leaf budgets are at most 100 steps. -/
theorem hrrP04KTheoryChernCharacterLedger_budgets :
    (hrrP04KTheoryChernCharacterLedger.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true :=
  rfl

/-- Checked guard: P04 is not repo-locally closed by the current anchors. -/
def hrrP04KTheoryChernCharacterRepoLocalClosed : Bool :=
  false

theorem hrrP04KTheoryChernCharacterRepoLocalClosed_eq_false :
    hrrP04KTheoryChernCharacterRepoLocalClosed = false :=
  rfl

/--
Checked guard: the P04 split introduces no completed-state
`repo_local_integration_debt`; it records formalization debt instead.
-/
def hrrP04NoCompletedRepoLocalIntegrationDebt : Bool :=
  true

theorem hrrP04NoCompletedRepoLocalIntegrationDebt_eq_true :
    hrrP04NoCompletedRepoLocalIntegrationDebt = true :=
  rfl

/-! ## HRR-P05 Todd-class and tangent-bundle package ledger -/

/--
One integration-ready leaf for the `HRR-P05-todd-and-tangent` package.

`concreteAnchor` names the current repo-local Lean object or audited blocker.
The tangent-bundle rows can point to checked mathlib manifold vector-bundle
objects; the Todd-class rows are explicitly blocked because the pinned snapshot
has no algebraic Todd-class or characteristic-class API for smooth projective
schemes.
-/
structure HRRP05LeafLedgerRow where
  leafId : String
  role : String
  concreteAnchor : List String
  localBudgetUpperBound : ℕ
  status : String

/--
`<=100`-step leaf ledger for `HRR-P05-todd-and-tangent`.

This split is tied to concrete tangent-bundle APIs where the repository can
honestly check them: `TangentSpace`, `TangentBundle`, `VectorBundle`, and
`ContMDiffVectorBundle` in mathlib's manifold hierarchy.  It also records the
precise blocker for HRR: these are not yet the algebraic tangent sheaf/bundle of
a smooth projective scheme, and no repo-local Todd-class API exists.
-/
def hrrP05ToddTangentLedger : List HRRP05LeafLedgerRow := [
  {
    leafId := "HRR-P05-L01-relative-algebraic-tangent-carrier",
    role :=
      "Choose the algebraic tangent object for the smooth structural morphism X -> base.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.SmoothProjectiveVarietyInput.structuralMorphism",
      "AlgebraicGeometry.Smooth",
      "AlgebraicGeometry.Scheme.Modules"
    ],
    localBudgetUpperBound := 85,
    status := "formalization_debt: no selected algebraic tangent sheaf or relative tangent bundle API"
  },
  {
    leafId := "HRR-P05-L02-manifold-tangent-space-anchor",
    role :=
      "Record the checked tangent-space surface available in the pinned mathlib manifold API.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.ManifoldTangentSpace",
      "TangentSpace"
    ],
    localBudgetUpperBound := 20,
    status := "checked_api_anchor: manifold tangent space only"
  },
  {
    leafId := "HRR-P05-L03-manifold-tangent-bundle-anchor",
    role :=
      "Record the checked tangent-bundle surface available in the pinned mathlib manifold API.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.ManifoldTangentBundle",
      "TangentBundle"
    ],
    localBudgetUpperBound := 20,
    status := "checked_api_anchor: manifold tangent bundle only"
  },
  {
    leafId := "HRR-P05-L04-vector-bundle-structure-anchor",
    role :=
      "Track the vector-bundle structure that a future tangent bundle must expose before characteristic classes can apply.",
    concreteAnchor := [
      "VectorBundle",
      "ContMDiffVectorBundle"
    ],
    localBudgetUpperBound := 30,
    status := "checked_api_anchor: differential vector-bundle API, not algebraic vector bundle K_0"
  },
  {
    leafId := "HRR-P05-L05-algebraic-vs-manifold-tangent-bridge",
    role :=
      "Bridge the smooth-scheme tangent carrier to a characteristic-class-ready vector bundle object.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.hrrP04KTheoryChernCharacterLedger",
      "AwesomeTheorems.Stage1.S1_M_125.SmoothProjectiveVarietyInput.coherentOrVectorBundle"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: blocked by missing geometric K_0/vector-bundle carrier"
  },
  {
    leafId := "HRR-P05-L06-canonical-or-relative-tangent-selection",
    role :=
      "Fix whether Td(T_X) is formed from the absolute tangent bundle or the tangent bundle relative to the base field spectrum.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.SmoothProjectiveVarietyInput.base_isFieldSpectrum",
      "AwesomeTheorems.Stage1.S1_M_125.SmoothProjectiveVarietyInput.pureDimension"
    ],
    localBudgetUpperBound := 60,
    status := "statement_shape_only: geometric convention is recorded but not implemented"
  },
  {
    leafId := "HRR-P05-L07-chern-classes-of-tangent",
    role :=
      "Provide Chern classes for the selected tangent bundle before defining the Todd class.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.hrrP04KTheoryChernCharacterLedger",
      "AwesomeTheorems.Stage1.S1_M_125.absentTerminalSearchTerms"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: no algebraic Chern-class API for tangent bundles found"
  },
  {
    leafId := "HRR-P05-L08-todd-power-series",
    role :=
      "Define the rational Todd power series x/(1-exp(-x)) or an equivalent polynomial expression in Chern classes.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.characteristicRing"
    ],
    localBudgetUpperBound := 85,
    status := "formalization_debt: no local Todd power-series API selected"
  },
  {
    leafId := "HRR-P05-L09-todd-class-map",
    role :=
      "Define Td(E) for a characteristic-class-ready vector bundle E.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.toddClassTangent",
      "AwesomeTheorems.Stage1.S1_M_125.externalHrrLeanAuditRows"
    ],
    localBudgetUpperBound := 90,
    status := "formalization_debt: toddClassTangent is currently an abstract field"
  },
  {
    leafId := "HRR-P05-L10-todd-multiplicativity",
    role :=
      "Prove Todd-class compatibility with direct sums or short exact sequences so it descends through the chosen bundle calculus.",
    concreteAnchor := [
      "VectorBundle",
      "Algebra.GrothendieckGroup"
    ],
    localBudgetUpperBound := 95,
    status := "formalization_debt: blocked by missing Chern/Todd class implementation"
  },
  {
    leafId := "HRR-P05-L11-target-ring-and-top-degree",
    role :=
      "Place Td(T_X) in the same Chow/cohomology target ring and top-degree integration interface used by HRR.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.characteristicRing",
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage.integrateTopClass"
    ],
    localBudgetUpperBound := 80,
    status := "statement_shape_only: characteristic ring and integration map remain abstract"
  },
  {
    leafId := "HRR-P05-L12-hrr-todd-interface",
    role :=
      "Expose Td(T_X) through the exact field consumed by ch(F) * Td(T_X) in the HRR equality.",
    concreteAnchor := [
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochPackage",
      "AwesomeTheorems.Stage1.S1_M_125.HirzebruchRiemannRochFormula"
    ],
    localBudgetUpperBound := 35,
    status := "statement_shape_only: no terminal Todd/tangent implementation"
  }
]

/-- Number of P05 leaves in the integration-ready ledger. -/
theorem hrrP05ToddTangentLedger_length :
    hrrP05ToddTangentLedger.length = 12 :=
  rfl

/-- Checked guard: all current P05 leaf budgets are at most 100 steps. -/
theorem hrrP05ToddTangentLedger_budgets :
    (hrrP05ToddTangentLedger.map (fun row => row.localBudgetUpperBound)).all
      (fun n => n ≤ 100) = true :=
  rfl

/-- Checked guard: P05 is not repo-locally closed by the current anchors. -/
def hrrP05ToddTangentRepoLocalClosed : Bool :=
  false

theorem hrrP05ToddTangentRepoLocalClosed_eq_false :
    hrrP05ToddTangentRepoLocalClosed = false :=
  rfl

/--
Checked guard: the P05 split introduces no completed-state
`repo_local_integration_debt`; it records formalization debt instead.
-/
def hrrP05NoCompletedRepoLocalIntegrationDebt : Bool :=
  true

theorem hrrP05NoCompletedRepoLocalIntegrationDebt_eq_true :
    hrrP05NoCompletedRepoLocalIntegrationDebt = true :=
  rfl

/-! ## C007 low-dimensional/projective-space special-case wrapper -/

/--
Tagged input for a future low-dimensional or projective-space HRR special case.

The `projectiveSpaceModel` field is deliberately only a predicate tag in this
Stage1 artifact.  The current repo-local Lean surface has no checked
projective-space-as-smooth-projective-scheme package with Chern character, Todd
class, coherent Euler characteristic, and integration map, so the actual HRR
formula still has to enter through `HirzebruchRiemannRochPackage`.
-/
structure LowDimensionalOrProjectiveSpaceHRRCase : Type (u + 1) where
  toInput : SmoothProjectiveVarietyInput.{u}
  base_isFieldSpectrum : toInput.base_isFieldSpectrum
  projective : toInput.projective
  projectiveSpaceModel : Prop
  lowDimensionalOrProjectiveSpace :
    toInput.pureDimension ≤ 1 ∨ projectiveSpaceModel

/--
Checked C007 wrapper: once the HRR characteristic-class package exists for a
tagged low-dimensional/projective-space case, the formula-level statement is
available for every admissible sheaf.
-/
theorem lowDimensionalOrProjectiveSpace_hrr_formula
    (C : LowDimensionalOrProjectiveSpaceHRRCase.{u})
    (P : HirzebruchRiemannRochPackage.{u, v} C.toInput)
    (F : C.toInput.space.Modules) (hF : C.toInput.coherentOrVectorBundle F) :
    HirzebruchRiemannRochFormula P F :=
  P.hrr_formula F hF

/--
Checked C007 wrapper from the normalized global statement shape to the tagged
low-dimensional/projective-space case.
-/
theorem lowDimensionalOrProjectiveSpace_exists_package_of_statementShape
    (h : StatementShape.{u, v}) (C : LowDimensionalOrProjectiveSpaceHRRCase.{u})
    (F : C.toInput.space.Modules) (hF : C.toInput.coherentOrVectorBundle F) :
    ∃ P : HirzebruchRiemannRochPackage.{u, v} C.toInput,
      HirzebruchRiemannRochFormula P F :=
  h C.toInput C.base_isFieldSpectrum C.projective F hF

/-- Checked guard: C007 adds a wrapper, not a terminal repo-local HRR proof. -/
def hrrC007SpecialCaseWrapperRepoLocalClosed : Bool :=
  false

theorem hrrC007SpecialCaseWrapperRepoLocalClosed_eq_false :
    hrrC007SpecialCaseWrapperRepoLocalClosed = false :=
  rfl

/--
Checked guard: the C007 wrapper leaves no completed-state
`repo_local_integration_debt`; it remains explicit formalization debt.
-/
def hrrC007NoCompletedRepoLocalIntegrationDebt : Bool :=
  true

theorem hrrC007NoCompletedRepoLocalIntegrationDebt_eq_true :
    hrrC007NoCompletedRepoLocalIntegrationDebt = true :=
  rfl

/-! ## Audit probes -/

#check Scheme
#check Scheme.Modules
#check Scheme.Modules.isSheaf
#check Smooth
#check IsProper
#check LocallyOfFiniteType
#check Sheaf.H
#check Sheaf.cohomologyPresheaf
#check Sheaf.H'
#check cechComplexFunctor
#check HomologicalComplex.eulerChar
#check HomologicalComplex.homologyEulerChar
#check HomologicalComplex.homologyEulerChar_eq_sum_finSet_of_finrankSupport_subset
#check Algebra.GrothendieckGroup
#check Algebra.GrothendieckGroup.of
#check TangentSpace
#check TangentBundle
#check VectorBundle
#check ContMDiffVectorBundle
#check StatementShape
#check ExternalHrrLeanAuditRow
#check externalHrrLeanAuditRows
#check externalHrrTerminalProofRepoLocalClosed_eq_false
#check externalHrrC003IntegrationBlockers
#check externalHrrC003IntegrationDecision
#check externalHrrC003_no_repo_local_closed
#check SiteSheafCohomologyGroup
#check SiteSheafCohomologyPresheaf
#check SiteObjectSheafCohomology
#check CechCochainComplexFunctor
#check hrrP03CoherentSheafEulerLedger
#check hrrP03CoherentSheafEulerLedger_budgets
#check hrrP03CoherentSheafEulerRepoLocalClosed_eq_false
#check HRRP04LeafLedgerRow
#check hrrP04KTheoryChernCharacterLedger
#check hrrP04KTheoryChernCharacterLedger_budgets
#check hrrP04KTheoryChernCharacterRepoLocalClosed_eq_false
#check hrrP04NoCompletedRepoLocalIntegrationDebt_eq_true
#check HRRP05LeafLedgerRow
#check ManifoldTangentSpace
#check ManifoldTangentBundle
#check hrrP05ToddTangentLedger
#check hrrP05ToddTangentLedger_budgets
#check hrrP05ToddTangentRepoLocalClosed_eq_false
#check hrrP05NoCompletedRepoLocalIntegrationDebt_eq_true
#check LowDimensionalOrProjectiveSpaceHRRCase
#check lowDimensionalOrProjectiveSpace_hrr_formula
#check lowDimensionalOrProjectiveSpace_exists_package_of_statementShape
#check hrrC007SpecialCaseWrapperRepoLocalClosed_eq_false
#check hrrC007NoCompletedRepoLocalIntegrationDebt_eq_true

end S1_M_125
end Stage1
end AwesomeTheorems
