import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper
import Mathlib.CategoryTheory.MorphismProperty.Descent
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.Complex
import Mathlib.RingTheory.AlgebraicIndependent.Basic

/-!
# S1-M-037 / THM-M-0117 statement-shape artifact

Moishezon theorem.

This file deliberately does not claim a proof of the analytic theorem.  It records a
compilable boundary between the missing analytic Moishezon infrastructure and the
scheme-side projectivity/properness APIs currently available in mathlib.
-/

open CategoryTheory AlgebraicGeometry

universe u

namespace AwesomeTheorems.Stage1.S1_M_037

/--
Statement-boundary data for the analytic side of the Moishezon theorem.

The intended replacement is a bundled compact complex manifold equipped with a
statement that its algebraic dimension equals its complex dimension.
-/
structure MoishezonAnalyticData (X : Type u) where
  compact_complex_manifold : Prop
  algebraic_dimension_equals_complex_dimension : Prop

/--
Provisional dimension interface for the Moishezon predicate.

This is intentionally not a concrete analytic definition.  `algebraicDimension`
should later be computed as the transcendence degree of the meromorphic-function
field over constants, and `complexDimension` should later be supplied by the
selected finite-dimensional complex-manifold API.
-/
structure MoishezonDimensionProfile (X : Type u) where
  algebraicDimension : Cardinal
  complexDimension : Cardinal

/--
Moishezon predicate after choosing compatible algebraic- and complex-dimension
APIs: the algebraic dimension equals the complex dimension.

At the current repo-local boundary the dimensions are a profile rather than
concrete mathlib constructions, because the meromorphic-function field on a
compact complex manifold and the corresponding algebraic-dimension API are not
available in the pinned Lean closure.
-/
def MoishezonPredicate (X : Type u) (profile : MoishezonDimensionProfile X) : Prop :=
  profile.algebraicDimension = profile.complexDimension

/-- The provisional Moishezon predicate is exactly equality of the two dimensions. -/
theorem moishezonPredicate_iff_dimension_eq
    (X : Type u) (profile : MoishezonDimensionProfile X) :
    MoishezonPredicate X profile ↔
      profile.algebraicDimension = profile.complexDimension :=
  Iff.rfl

/--
Compatibility constructor tying the older statement-boundary field to the new
dimension-profile predicate.
-/
def MoishezonAnalyticData.withDimensionProfile
    (X : Type u) (compactComplexManifold : Prop) (profile : MoishezonDimensionProfile X) :
    MoishezonAnalyticData X where
  compact_complex_manifold := compactComplexManifold
  algebraic_dimension_equals_complex_dimension := MoishezonPredicate X profile

/-- Boundary object for an algebraic model attached to the analytic space. -/
structure AlgebraicModelData (X : Type u) where
  carrier : Type u
  comparison : X → carrier

/--
Scheme-side projectivity shape: `X` factors through a closed immersion into an
ambient `P` that is proper over the base `S`.

This is only a bridge target.  The missing work is to construct `P`, the closed
immersion, and the comparison from a genuine Moishezon analytic object.
-/
def SchemeProjectiveViaClosedImmersion (S X P : Scheme.{u}) (f : X ⟶ S) : Prop :=
  ∃ (p : P ⟶ S) (i : X ⟶ P), IsClosedImmersion i ∧ IsProper p ∧ i ≫ p = f

/--
Proj-specialized refinement of `SchemeProjectiveViaClosedImmersion` over the
affine degree-zero base of a graded ring.

This is the strongest currently checked repo-local PUB-07 progress: the ambient
scheme is no longer an arbitrary `P`, but the actual mathlib `Proj 𝒜`, and the
structure map is `Proj.toSpecZero 𝒜`.  It is still not the final arbitrary-base
projective-space formulation of projectivity.
-/
def SchemeProjectiveViaProjClosedImmersion
    {σ A : Type u} [CommRing A] [SetLike σ A] [AddSubgroupClass σ A]
    (𝒜 : ℕ → σ) [GradedRing 𝒜] [Algebra.FiniteType (𝒜 0) A]
    (X : Scheme.{u}) (f : X ⟶ Spec (.of <| 𝒜 0)) : Prop :=
  ∃ i : X ⟶ Proj 𝒜, IsClosedImmersion i ∧ i ≫ Proj.toSpecZero 𝒜 = f

/--
Concrete repo-local replacement for the formerly abstract
`ProjectiveAlgebraicModel.projective : Prop` field.

The predicate currently available in this pinned mathlib closure is the
scheme-side factorization through a closed immersion into an ambient scheme that
is proper over the base.  This is deliberately not claimed to be the terminal
Proj/projective-space definition of projectivity; that stronger refinement is
the separate `S1-M-037-PUB-07` leaf.
-/
structure ProjectiveSchemeModelData where
  base : Scheme.{u}
  modelScheme : Scheme.{u}
  ambient : Scheme.{u}
  structureMap : modelScheme ⟶ base
  projectiveWitness :
    SchemeProjectiveViaClosedImmersion base modelScheme ambient structureMap

/--
Boundary object for the projective algebraic model promised by Moishezon's
theorem.

The projectivity field is now concrete scheme data rather than an opaque
proposition.
-/
structure ProjectiveAlgebraicModel (X : Type u) where
  model : AlgebraicModelData X
  projective : ProjectiveSchemeModelData

/--
Statement shape for the analytic theorem: every Moishezon analytic object admits
some projective algebraic model.
-/
def StatementShape : Prop :=
  ∀ {X : Type u}, MoishezonAnalyticData X → Nonempty (ProjectiveAlgebraicModel X)

/--
Scheme bridge statement shape: a future algebraization step should produce a
closed-immersion factorization through a proper ambient scheme.
-/
def SchemeBridgeShape : Prop :=
  ∀ {S X : Scheme.{u}} (f : X ⟶ S),
    IsProper f → ∃ P : Scheme.{u}, SchemeProjectiveViaClosedImmersion S X P f

/-- Closed immersions are proper in the imported mathlib scheme-morphism API. -/
theorem closedImmersion_isProper {X P : Scheme.{u}} (i : X ⟶ P) [IsClosedImmersion i] :
    IsProper i :=
  inferInstance

/--
A closed immersion into an ambient scheme proper over the base makes the induced
map to the base proper.  This is a small checked wrapper around mathlib's proper
morphism stability under composition.
-/
theorem projectiveModelMorphism_isProper {S X P : Scheme.{u}} {f : X ⟶ S} {p : P ⟶ S}
    {i : X ⟶ P} (_hi : IsClosedImmersion i) (_hp : IsProper p) (_hfac : i ≫ p = f) :
    IsProper f := by
  subst f
  infer_instance

/--
Unpacking the scheme-side bridge shape gives only properness of the displayed
morphism.  This is not a projectivity theorem and does not construct the
analytic-to-algebraic comparison required by Moishezon's theorem.
-/
theorem schemeProjectiveViaClosedImmersion_isProper {S X P : Scheme.{u}} {f : X ⟶ S}
    (h : SchemeProjectiveViaClosedImmersion S X P f) : IsProper f := by
  rcases h with ⟨p, i, hi, hp, hfac⟩
  exact projectiveModelMorphism_isProper hi hp hfac

/--
A Proj-specialized closed-immersion factorization is an instance of the abstract
proper-ambient scheme-side wrapper.
-/
theorem schemeProjectiveViaProjClosedImmersion_to_closedImmersion
    {σ A : Type u} [CommRing A] [SetLike σ A] [AddSubgroupClass σ A]
    (𝒜 : ℕ → σ) [GradedRing 𝒜] [Algebra.FiniteType (𝒜 0) A]
    {X : Scheme.{u}} {f : X ⟶ Spec (.of <| 𝒜 0)}
    (h : SchemeProjectiveViaProjClosedImmersion 𝒜 X f) :
    SchemeProjectiveViaClosedImmersion (Spec (.of <| 𝒜 0)) X (Proj 𝒜) f := by
  rcases h with ⟨i, hi, hfac⟩
  exact ⟨Proj.toSpecZero 𝒜, i, hi, inferInstance, hfac⟩

/-- The Proj-specialized factorization also implies properness of the displayed morphism. -/
theorem schemeProjectiveViaProjClosedImmersion_isProper
    {σ A : Type u} [CommRing A] [SetLike σ A] [AddSubgroupClass σ A]
    (𝒜 : ℕ → σ) [GradedRing 𝒜] [Algebra.FiniteType (𝒜 0) A]
    {X : Scheme.{u}} {f : X ⟶ Spec (.of <| 𝒜 0)}
    (h : SchemeProjectiveViaProjClosedImmersion 𝒜 X f) : IsProper f :=
  schemeProjectiveViaClosedImmersion_isProper
    (schemeProjectiveViaProjClosedImmersion_to_closedImmersion 𝒜 h)

/-- The concrete projective-model witness still implies properness of its structure map. -/
theorem ProjectiveSchemeModelData.structureMap_isProper (Y : ProjectiveSchemeModelData) :
    IsProper Y.structureMap :=
  schemeProjectiveViaClosedImmersion_isProper Y.projectiveWitness

/-- mathlib modules audited as repo-local Lean 4 anchors for this repair pass. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper",
  "Mathlib.CategoryTheory.MorphismProperty.Descent",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
  "Mathlib.Geometry.Manifold.Complex"
]

/-- Pinned declaration names checked as object-model anchors for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.IsClosedImmersion",
  "AlgebraicGeometry.IsProper",
  "CategoryTheory.Limits.HasPullbacks"
]

/-- Structured public-backfill row for audited mathlib anchors. -/
structure MathlibAnchorRow where
  requested : String
  moduleName : String
  checkedDeclaration : String
  repoLocalStatus : String
  note : String

/--
Mathlib anchor table prepared for the public `S1-M-037-PUB-02` backfill.

The rows are metadata, while the `#check` probes below validate the declaration
names that can be checked directly in this repository's pinned mathlib closure.
`Geometry.Manifold.Complex` is a module anchor; its checked witness is a theorem
from that module about holomorphic functions on compact complex manifolds.
-/
def mathlibAnchorTable : List MathlibAnchorRow := [
  {
    requested := "Scheme"
    moduleName := "Mathlib.AlgebraicGeometry.Scheme"
    checkedDeclaration := "AlgebraicGeometry.Scheme"
    repoLocalStatus := "checked"
    note := "Core scheme object used by the scheme-side wrapper."
  },
  {
    requested := "IsProper"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Proper"
    checkedDeclaration := "AlgebraicGeometry.IsProper"
    repoLocalStatus := "checked"
    note := "Properness predicate used by the ambient scheme and induced morphism wrappers."
  },
  {
    requested := "IsClosedImmersion"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.ClosedImmersion"
    checkedDeclaration := "AlgebraicGeometry.IsClosedImmersion"
    repoLocalStatus := "checked"
    note := "Closed-immersion predicate used in the projective-model factorization shape."
  },
  {
    requested := "Proj.toSpecZero"
    moduleName := "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic"
    checkedDeclaration := "AlgebraicGeometry.Proj.toSpecZero"
    repoLocalStatus := "checked"
    note := "Structure morphism from Proj to Spec of degree zero, imported through ProjectiveSpectrum.Proper."
  },
  {
    requested := "Sheaf.H"
    moduleName := "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic"
    checkedDeclaration := "CategoryTheory.Sheaf.H"
    repoLocalStatus := "checked"
    note := "Abelian sheaf cohomology type by degree."
  },
  {
    requested := "cohomologyFunctor"
    moduleName := "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic"
    checkedDeclaration := "CategoryTheory.Sheaf.cohomologyFunctor"
    repoLocalStatus := "checked"
    note := "Functorial sheaf cohomology API; the unqualified public name lives under the Sheaf namespace."
  },
  {
    requested := "MorphismProperty.DescendsAlong"
    moduleName := "Mathlib.CategoryTheory.MorphismProperty.Descent"
    checkedDeclaration := "CategoryTheory.MorphismProperty.DescendsAlong"
    repoLocalStatus := "checked"
    note := "Descent class for morphism properties; imported explicitly for this audit."
  },
  {
    requested := "Geometry.Manifold.Complex"
    moduleName := "Mathlib.Geometry.Manifold.Complex"
    checkedDeclaration := "MDifferentiable.exists_eq_const_of_compactSpace"
    repoLocalStatus := "checked_module_with_witness_declaration"
    note := "Complex-manifold module imported; witness theorem checks the compact complex manifold holomorphic-function API, not Moishezon algebraic dimension."
  }
]

/-- Declaration names directly checked for the public mathlib anchor table. -/
def checkedMathlibAnchorNames : List String :=
  mathlibAnchorTable.map (·.checkedDeclaration)

/-- Search terms retained for a later primary-source external Lean 4 audit. -/
def externalLeanAuditSearchTerms : List String := [
  "Moishezon",
  "Moisezon",
  "algebraic dimension",
  "meromorphic function",
  "Kodaira embedding",
  "VeryAmple"
]

/-- Structured public-backfill row for the PUB-04 analytic API audit. -/
structure AnalyticDimensionApiAuditRow where
  requested : String
  moduleName : String
  checkedDeclaration : String
  repoLocalStatus : String
  note : String

/--
S1-M-037-PUB-04 repo-local audit for meromorphic-function and algebraic-dimension APIs.

The available `Meromorphic` API is a one-variable normed-field function API, not
a sheaf or field of meromorphic functions on a complex manifold.  The available
`Algebra.trdeg` API is the correct field-theory substrate for an eventual
algebraic-dimension definition, but it needs a concrete meromorphic-function
field over constants before it can express Moishezon algebraic dimension.
-/
def meromorphicAlgebraicDimensionApiAudit : List AnalyticDimensionApiAuditRow := [
  {
    requested := "Meromorphic functions on normed-field domains"
    moduleName := "Mathlib.Analysis.Meromorphic.Basic"
    checkedDeclaration := "MeromorphicAt; MeromorphicOn; Meromorphic"
    repoLocalStatus := "checked_adjacent_one_variable_api"
    note := "This checks meromorphic functions such as C -> E; it is not a meromorphic-function sheaf or field on a complex manifold."
  },
  {
    requested := "Holomorphic functions on compact complex manifolds"
    moduleName := "Mathlib.Geometry.Manifold.Complex"
    checkedDeclaration := "MDifferentiable.exists_eq_const_of_compactSpace"
    repoLocalStatus := "checked_complex_manifold_holomorphic_anchor"
    note := "Complex-manifold holomorphic anchors exist; the module TODO explicitly leaves holomorphic/meromorphic sheaf development for future work."
  },
  {
    requested := "Algebraic independence and transcendence-degree substrate"
    moduleName := "Mathlib.RingTheory.AlgebraicIndependent.Basic"
    checkedDeclaration := "AlgebraicIndependent; IsTranscendenceBasis; Algebra.trdeg"
    repoLocalStatus := "checked_field_theory_substrate"
    note := "This can support algebraic dimension only after a concrete meromorphic-function field over C is defined."
  },
  {
    requested := "Meromorphic functions on complex manifolds"
    moduleName := "not found in pinned mathlib by repo-local grep"
    checkedDeclaration := "none"
    repoLocalStatus := "missing_concrete_api"
    note := "No bundled sheaf, field, or global API for meromorphic functions on a complex manifold was located in this repo-local pass."
  },
  {
    requested := "Algebraic dimension of compact complex manifolds"
    moduleName := "not found in pinned mathlib by repo-local grep"
    checkedDeclaration := "none"
    repoLocalStatus := "missing_concrete_api"
    note := "No Moishezon algebraic-dimension predicate was located; the intended definition is trdeg over C of the meromorphic-function field once that field exists."
  }
]

/-- PUB-04 checked declaration names that are available in the repo-local Lean closure. -/
def checkedAnalyticDimensionApiNames : List String := [
  "MeromorphicAt",
  "MeromorphicOn",
  "Meromorphic",
  "AlgebraicIndependent",
  "IsTranscendenceBasis",
  "Algebra.trdeg"
]

/--
No concrete repo-local API for meromorphic functions on complex manifolds was
found in this pass.
-/
def hasRepoLocalComplexManifoldMeromorphicApi : Bool := false

/--
No concrete repo-local API for algebraic dimension of compact complex manifolds
was found in this pass.
-/
def hasRepoLocalComplexManifoldAlgebraicDimensionApi : Bool := false

/--
The predicate shape is now repo-local and checked, but its two inputs are still
profile fields rather than concrete analytic APIs.
-/
def hasConcreteMoishezonPredicateInputs : Bool := false

/--
The `ProjectiveAlgebraicModel.projective` field no longer stores an opaque
`Prop`; it stores concrete scheme-side model data and a checked factorization
witness.
-/
def hasConcreteProjectiveAlgebraicModelPredicate : Bool := true

/--
The pinned repo-local closure has a checked Proj-specialized affine-base
refinement of the proper-ambient wrapper.
-/
def hasRepoLocalProjAmbientRefinement : Bool := true

/--
The projective-model field has not yet been globally replaced by a
projective-space/Proj object over an arbitrary base.
-/
def hasProjOrProjectiveSpaceAlgebraicModelPredicate : Bool := false

/-- Checked one-variable meromorphic anchor over `C`; not a complex-manifold API. -/
theorem meromorphic_id_complex_anchor : Meromorphic (fun z : ℂ => z) := by
  intro z
  simpa [id] using (MeromorphicAt.id (𝕜 := ℂ) z)

/--
Field-theory substrate for a future algebraic-dimension definition.

For Moishezon, `F` should eventually be the meromorphic-function field of the
complex analytic object and `K` should be the constant field, typically `C`.
-/
noncomputable abbrev AlgebraicDimensionFieldSubstrate
    (K F : Type u) [CommRing K] [CommRing F] [Algebra K F] : Cardinal :=
  Algebra.trdeg K F

/-- The substrate abbreviation is exactly mathlib's transcendence degree. -/
theorem algebraicDimensionFieldSubstrate_eq_trdeg
    (K F : Type u) [CommRing K] [CommRing F] [Algebra K F] :
    AlgebraicDimensionFieldSubstrate K F = Algebra.trdeg K F :=
  rfl

/-- Pinned mathlib commit used by this repo-local Lean project. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Structured row for `S1-M-037-PUB-08` external Lean 4 primary-source search. -/
structure ExternalLean4SearchAuditRow where
  searchTerm : String
  sourceKind : String
  repositoryUrl : String
  commit : String
  moduleName : String
  theoremName : String
  lakeCompatibility : String
  resultStatus : String
  integrationAction : String

/--
S1-M-037-PUB-08 external Lean 4 audit.

The locally available authenticated GitHub path is blocked: `gh auth status`
reported no logged-in GitHub hosts, and both `GH_TOKEN` and `GITHUB_TOKEN` were
unset.  The rows below therefore separate repo-local pinned source facts from
credential-blocked external code-search probes.  No row is counted as a
completed Moishezon theorem proof.
-/
def externalLean4PrimarySourceAudit : List ExternalLean4SearchAuditRow := [
  {
    searchTerm := "Moishezon"
    sourceKind := "GitHub repository search plus authenticated-code-search credential probe"
    repositoryUrl := "none found by repository search; authenticated GitHub code search unavailable locally"
    commit := "none"
    moduleName := "none"
    theoremName := "none"
    lakeCompatibility := "not_applicable"
    resultStatus := "no Lean 4 theorem candidate located; exact code search requires GitHub authentication"
    integrationAction := "No pin/import/check target exists from this pass; rerun authenticated code search before any completion claim."
  },
  {
    searchTerm := "Moisezon"
    sourceKind := "GitHub repository search plus authenticated-code-search credential probe"
    repositoryUrl := "none found by repository search; authenticated GitHub code search unavailable locally"
    commit := "none"
    moduleName := "none"
    theoremName := "none"
    lakeCompatibility := "not_applicable"
    resultStatus := "no Lean 4 theorem candidate located; exact code search requires GitHub authentication"
    integrationAction := "No pin/import/check target exists from this pass; rerun authenticated code search before any completion claim."
  },
  {
    searchTerm := "algebraic dimension"
    sourceKind := "pinned mathlib source audit plus GitHub repository-search probe"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibPinnedRevision
    moduleName := "Mathlib.RingTheory.AlgebraicIndependent.Basic"
    theoremName := "Algebra.trdeg"
    lakeCompatibility := "compatible_pinned_dependency"
    resultStatus := "field-theory substrate only; no algebraic-dimension API for compact complex manifolds found"
    integrationAction := "Keep as formalization_debt; define meromorphic-function field and algebraic-dimension API before using this substrate."
  },
  {
    searchTerm := "meromorphic"
    sourceKind := "pinned mathlib source audit"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibPinnedRevision
    moduleName := "Mathlib.Analysis.Meromorphic.Basic"
    theoremName := "MeromorphicAt; MeromorphicOn; Meromorphic"
    lakeCompatibility := "compatible_pinned_dependency"
    resultStatus := "one-variable normed-field meromorphic-function API only; no complex-manifold meromorphic sheaf or function field found"
    integrationAction := "Keep as formalization_debt; this adjacent API is not a Moishezon theorem proof."
  },
  {
    searchTerm := "Kodaira embedding"
    sourceKind := "pinned mathlib source audit plus repo-local Stage1 Kodaira audit"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibPinnedRevision
    moduleName := "none for exact Kodaira embedding theorem in pinned mathlib"
    theoremName := "none"
    lakeCompatibility := "not_applicable_for_terminal_theorem"
    resultStatus := "no exact Kodaira embedding theorem anchor found; local S1_M_024 is statement-shape only"
    integrationAction := "No reusable external terminal proof is available for the Moishezon route from this pass."
  },
  {
    searchTerm := "VeryAmple"
    sourceKind := "pinned mathlib source audit plus authenticated-code-search credential probe"
    repositoryUrl := "none found in pinned mathlib exact search; authenticated GitHub code search unavailable locally"
    commit := "none"
    moduleName := "none"
    theoremName := "none"
    lakeCompatibility := "not_applicable"
    resultStatus := "no `VeryAmple` declaration or very-ampleness theorem anchor located in the pinned Lean closure"
    integrationAction := "Leave projective-space/Proj and very-ampleness APIs as future formalization leaves."
  }
]

/-- This pass found no exact external Lean 4 proof of Moishezon's theorem. -/
def c008ExactExternalMoishezonProofFound : Bool := false

/-- Checked non-completion flag for the C008 external-proof audit. -/
theorem c008ExactExternalMoishezonProofFound_eq_false :
    c008ExactExternalMoishezonProofFound = false :=
  rfl

/-- C009 repo-local integration gate: no external Moishezon proof is available to integrate. -/
def c009ExternalMoishezonProofAvailableToIntegrate : Bool := false

/-- Checked non-completion flag for the C009 repo-local integration gate. -/
theorem c009ExternalMoishezonProofAvailableToIntegrate_eq_false :
    c009ExternalMoishezonProofAvailableToIntegrate = false :=
  rfl

/--
S1-M-037-PUB-09 integration action.

Because C008 found no exact external Lean 4 proof of Moishezon's theorem, there
is currently no repository URL, commit, module, theorem name, or Lake-compatible
dependency that can be pinned/imported/checked in this repo.  If such a proof is
found later, the only acceptable next states are a locally checked pinned or
vendored dependency, a locally checked wrapper theorem, or an explicit
dependency/toolchain/license blocker while the theorem remains not completed.
-/
def c009RepoLocalIntegrationGateStatus : String :=
  "pass_noncompletion_no_external_lean4_proof_found"

/-- Integration-ready public wording for `S1-M-037-PUB-09`. -/
def publicExternalProofIntegrationGateBackfillText : String :=
  "PUB-09 integration gate: no exact external Lean 4 proof of Moishezon/Moisezon algebraicity is currently available to pin/import/check from the C008 audit, so there is no active completed-state repo_local_integration_debt. Keep S1-M-037 / THM-M-0117 not completed. If a future audit supplies a concrete repository URL, commit, module, theorem name, and Lake compatibility tuple, the integrator must either add a pinned/vendored dependency or repo-local wrapper and validate it in this repo, or record a concrete dependency/toolchain/license blocker while leaving the theorem not completed. Anchor-only URL or theorem-name evidence must not close the checkbox."

/-- Integration-ready public wording for `S1-M-037-PUB-08`. -/
def publicExternalLean4AuditBackfillText : String :=
  "PUB-08 external Lean 4 audit: repo-local pinned mathlib at commit 8a178386ffc0f5fef0b77738bb5449d50efeea95 provides adjacent APIs `MeromorphicAt`, `MeromorphicOn`, `Meromorphic`, and `Algebra.trdeg`, but no exact Lean 4 proof of Moishezon/Moisezon algebraicity, no compact-complex-manifold algebraic-dimension API, no exact Kodaira embedding theorem, and no `VeryAmple` theorem anchor were found in the checked local closure. GitHub repository-search probes for Moishezon+Lean, Moisezon+Lean, Kodaira embedding+Lean, VeryAmple+Lean, and algebraic dimension+Lean returned no terminal Lean theorem repository candidates; authenticated GitHub code search could not be completed because `gh auth status` reported no logged-in GitHub hosts and `GH_TOKEN`/`GITHUB_TOKEN` were unset. Therefore no external Lean proof is available to pin/import/check from this pass; PUB-08/PUB-09 must remain open until authenticated code search is rerun or a concrete repository URL, commit, module, theorem name, and Lake compatibility tuple is supplied."

/--
Machine proof debt classification for this Stage1 slot.

The module currently validates a statement-shape and a small scheme-side wrapper
only.  No repo-local proof body, checked mathlib terminal theorem, or pinned
external Lean 4 dependency for the analytic Moishezon theorem is present.
-/
def machineProofDebt : String := "formalization_debt"

/--
Repo-local integration-debt gate.

No external Lean 4 closure is integrated by this artifact.  If a complete Lean 4
Moishezon theorem proof is found later, completion requires pin/import/check or
an explicit dependency, toolchain, or license blocker.
-/
def repoLocalIntegrationDebtGate : String :=
  "no completed-state repo_local_integration_debt; no external Lean 4 closure integrated"

/--
Public Stage1 boundary note prepared for serial merge-back.

The checked artifact is a statement-shape and scheme-side wrapper only; it is
not a proof of Moishezon's theorem.
-/
def publicStage1BoundaryNote : String :=
  "S1_M_037 is a statement-shape and scheme-side wrapper only; not a proof of Moishezon's theorem."

/--
Candidate public formal targets for the Moishezon Stage1 line.

The selected target below is the algebraic scheme bridge.  Compact complex
manifolds remain the intended analytic source of the theorem, while compact
complex spaces require analytic APIs that are not present in this repo-local
Lean closure.
-/
inductive PublicFormalTarget where
  | compactComplexManifold
  | compactComplexSpace
  | smoothProjectiveAlgebraicSchemeBridge
  deriving DecidableEq, Repr

/--
S1-M-037-PUB-03 target decision.

Use a smooth/projective algebraic scheme bridge as the public formal target.
The current checked module only validates the first scheme-side properness
wrapper; smoothness, projective-space/Proj projectivity, meromorphic functions,
and algebraic dimension remain future formalization leaves.
-/
def publicFormalTargetDecision : PublicFormalTarget :=
  .smoothProjectiveAlgebraicSchemeBridge

/-- Integration-ready public wording for the target decision. -/
def publicFormalTargetDecisionText : String :=
  "Public formal target: smooth/projective algebraic scheme bridge statement; compact complex manifolds are the analytic source vocabulary, and compact complex spaces are deferred until repo-local complex-space, meromorphic-function, and algebraic-dimension APIs exist."

/-- Repo-local rationale for selecting the scheme bridge target. -/
def publicFormalTargetRationale : String :=
  "The scheme bridge is the strongest currently checkable Lean target because this repo validates Scheme, IsProper, IsClosedImmersion, Proj.toSpecZero, sheaf cohomology, descent, and complex-manifold module anchors. It avoids claiming a proof of the analytic Moishezon theorem while keeping future projective-space/Proj and analytic comparison leaves explicit."

/-- Integration-ready public wording for `S1-M-037-PUB-05`. -/
def publicMoishezonPredicateBackfillText : String :=
  "Define the Moishezon predicate as equality of the selected algebraic-dimension and complex-dimension APIs. Repo-local Lean now records this as `MoishezonDimensionProfile` with fields `algebraicDimension : Cardinal` and `complexDimension : Cardinal`, and `MoishezonPredicate X profile := profile.algebraicDimension = profile.complexDimension`. This is a checked predicate-shape only: `hasConcreteMoishezonPredicateInputs = false`, because the pinned Lean closure still lacks a meromorphic-function field on compact complex manifolds, an algebraic-dimension API built from it, and the matching complex-dimension API selection."

/-- Integration-ready public wording for `S1-M-037-PUB-06`. -/
def publicProjectiveModelPredicateBackfillText : String :=
  "Replace `ProjectiveAlgebraicModel.projective : Prop` with concrete scheme-side data. Repo-local Lean now stores `projective : ProjectiveSchemeModelData`, bundling a base scheme, model scheme, ambient scheme, structure morphism, and a `SchemeProjectiveViaClosedImmersion` witness. The checked predicate gives a closed immersion into an ambient scheme proper over the base and proves `ProjectiveSchemeModelData.structureMap_isProper`; it is not yet the Proj/projective-space definition of projectivity, so `S1-M-037-PUB-07` remains open with `hasProjOrProjectiveSpaceAlgebraicModelPredicate = false`."

/-- Integration-ready public wording for `S1-M-037-PUB-07`. -/
def publicProjAmbientBackfillText : String :=
  "PUB-07 is partially advanced but remains open. Repo-local Lean now defines `SchemeProjectiveViaProjClosedImmersion 𝒜 X f`, replacing the abstract ambient `P` by the concrete mathlib scheme `Proj 𝒜` over the affine degree-zero base `Spec (.of <| 𝒜 0)`, and proves it refines `SchemeProjectiveViaClosedImmersion` via `schemeProjectiveViaProjClosedImmersion_to_closedImmersion` and implies properness via `schemeProjectiveViaProjClosedImmersion_isProper`. This does not yet replace `ProjectiveSchemeModelData.ambient` globally, because the remaining target needs an arbitrary-base/projective-space formulation and the analytic Moishezon comparison data."

/-- Structured package row for the public `MOI-P01` through `MOI-P08` theorem tree. -/
structure MoishezonTheoremTreePackage where
  code : String
  title : String
  proofRole : String
  currentLeafRange : String
  status : String
  leafLedgerRequirement : String
  repoLocalClosed : Bool

/--
Public theorem-tree split prepared for `S1-M-037-PUB-10`.

Every row is an unchecked package boundary, not a completion claim.  The
corresponding future leaves are recorded in `moishezonFutureLeafLedgers` and
must carry independent local ledgers before any public completion state changes.
-/
def moishezonTheoremTreePackages : List MoishezonTheoremTreePackage := [
  {
    code := "MOI-P01"
    title := "statement-normalization"
    proofRole := "Freeze universe parameters, analytic object type, compact complex-manifold assumptions, algebraic-dimension hypothesis, and algebraic/projective conclusion."
    currentLeafRange := "MOI-L001 through MOI-L003"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P02"
    title := "mathlib-object-model"
    proofRole := "Audit exact imports for complex manifolds, sheaves, schemes, morphism properties, Proj, properness, closed immersions, descent, and cohomology."
    currentLeafRange := "MOI-L004 through MOI-L010"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P03"
    title := "meromorphic-function-field"
    proofRole := "Formalize meromorphic functions and algebraic dimension for compact complex manifolds."
    currentLeafRange := "MOI-L011 through MOI-L013"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P04"
    title := "moishezon-algebraic-reduction"
    proofRole := "Encode algebraic reduction and the maximal algebraically independent meromorphic-function package."
    currentLeafRange := "MOI-L014 through MOI-L015"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P05"
    title := "modification-and-resolution"
    proofRole := "State and eventually prove the bimeromorphic modification/resolution package needed to compare the analytic object to an algebraic model."
    currentLeafRange := "MOI-L016 through MOI-L017"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P06"
    title := "analytic-to-scheme-algebraization"
    proofRole := "Bridge compact complex/Moishezon data to a scheme or projective variety model."
    currentLeafRange := "MOI-L018 through MOI-L019"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P07"
    title := "projective-embedding-wrapper"
    proofRole := "Use closed immersion into a Proj/projective ambient object and mathlib properness/projectivity-adjacent APIs."
    currentLeafRange := "MOI-L020 through MOI-L023"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  },
  {
    code := "MOI-P08"
    title := "repo-local-closure-gate"
    proofRole := "Choose local proof body, pinned mathlib wrapper, or pinned external dependency; until this closes with validation, public completion remains blocked."
    currentLeafRange := "MOI-L024 through MOI-L026"
    status := "unchecked"
    leafLedgerRequirement := "each future leaf needs an independent <=100 local ledger"
    repoLocalClosed := false
  }
]

/-- The public Moishezon theorem-tree split has exactly eight package rows. -/
theorem moishezonTheoremTreePackages_length :
    moishezonTheoremTreePackages.length = 8 :=
  rfl

/-- The package codes match the requested `MOI-P01` through `MOI-P08` split. -/
theorem moishezonTheoremTreePackages_codes :
    moishezonTheoremTreePackages.map MoishezonTheoremTreePackage.code =
      ["MOI-P01", "MOI-P02", "MOI-P03", "MOI-P04",
       "MOI-P05", "MOI-P06", "MOI-P07", "MOI-P08"] :=
  rfl

/-- No package row is recorded as repo-locally closed by this planning split. -/
theorem moishezonTheoremTreePackages_no_repoLocalClosed_claim :
    moishezonTheoremTreePackages.map MoishezonTheoremTreePackage.repoLocalClosed =
      [false, false, false, false, false, false, false, false] :=
  rfl

/-- Future leaf ledger row for the `MOI-P01` through `MOI-P08` split. -/
structure MoishezonLeafLedgerRow where
  leafId : String
  packageId : String
  localTarget : String
  maxProofSteps : Nat
  budgetLe100 : Bool
  status : String

/--
Independent future leaf ledgers for `S1-M-037-PUB-10`.

These rows are intentionally `unchecked`: they are integration-ready budget
targets, not verified proof scripts.  A row can be promoted only after its
corresponding machine anchor and human-readable ledger are locally closed.
-/
def moishezonFutureLeafLedgers : List MoishezonLeafLedgerRow := [
  { leafId := "MOI-L001", packageId := "MOI-P01", localTarget := "Define canonical namespace and `StatementShape` for Moishezon algebraicity.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L002", packageId := "MOI-P01", localTarget := "Decide whether the public statement targets compact complex manifolds, irreducible compact complex spaces, or smooth projective varieties.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L003", packageId := "MOI-P01", localTarget := "Freeze whether the conclusion is algebraic, projective, or bimeromorphic/projective model.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L004", packageId := "MOI-P02", localTarget := "Import and check `AlgebraicGeometry.Scheme` and scheme morphism objects.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L005", packageId := "MOI-P02", localTarget := "Import and check `AlgebraicGeometry.IsProper`.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L006", packageId := "MOI-P02", localTarget := "Import and check `AlgebraicGeometry.IsClosedImmersion`.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L007", packageId := "MOI-P02", localTarget := "Import and check `AlgebraicGeometry.Proj.toSpecZero`.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L008", packageId := "MOI-P02", localTarget := "Import and check `CategoryTheory.Sheaf.H` and `Sheaf.cohomologyFunctor`.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L009", packageId := "MOI-P02", localTarget := "Import and check complex-manifold anchors in `Geometry.Manifold.Complex`.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L010", packageId := "MOI-P02", localTarget := "Record absence or presence of Moishezon-specific declarations in pinned mathlib.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L011", packageId := "MOI-P03", localTarget := "Define meromorphic-function placeholder or select an existing API if later found.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L012", packageId := "MOI-P03", localTarget := "Define algebraic dimension as transcendence degree of meromorphic functions over constants.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L013", packageId := "MOI-P03", localTarget := "State equality between algebraic dimension and complex dimension.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L014", packageId := "MOI-P04", localTarget := "State algebraic reduction map from meromorphic-function data.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L015", packageId := "MOI-P04", localTarget := "Prove or anchor stability of the algebraic reduction under bimeromorphic equivalence.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L016", packageId := "MOI-P05", localTarget := "State bimeromorphic modification/resolution input package.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L017", packageId := "MOI-P05", localTarget := "Split resolution package into smoothness, exceptional locus, and comparison leaves.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L018", packageId := "MOI-P06", localTarget := "State analytic-to-scheme algebraization bridge.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L019", packageId := "MOI-P06", localTarget := "Connect analytic compactness/properness to scheme properness or projective target assumptions.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L020", packageId := "MOI-P07", localTarget := "Define scheme-side `SchemeProjectiveViaClosedImmersion`.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L021", packageId := "MOI-P07", localTarget := "Prove closed immersion into proper ambient morphism gives proper composite.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L022", packageId := "MOI-P07", localTarget := "Replace abstract ambient `P` with a concrete Proj/projective-space object once APIs are selected.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L023", packageId := "MOI-P07", localTarget := "Use `Proj.toSpecZero` properness for finite-type graded rings as the first concrete projective ambient sanity check.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L024", packageId := "MOI-P08", localTarget := "Run path-based Lean validation and record output.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L025", packageId := "MOI-P08", localTarget := "If an external Lean 4 closure is found, pin/import/check or record a concrete integration blocker.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" },
  { leafId := "MOI-L026", packageId := "MOI-P08", localTarget := "Merge a human-readable proof-tree summary back to public surface only after integrator review.", maxProofSteps := 100, budgetLe100 := true, status := "unchecked" }
]

/-- The future Moishezon theorem-tree ledger currently contains 26 leaves. -/
theorem moishezonFutureLeafLedgers_length :
    moishezonFutureLeafLedgers.length = 26 :=
  rfl

/-- Every future leaf row records the local `<=100` budget flag. -/
theorem moishezonFutureLeafLedgers_all_budgeted :
    moishezonFutureLeafLedgers.map MoishezonLeafLedgerRow.budgetLe100 =
      List.replicate 26 true :=
  rfl

/-- Every future leaf row remains unchecked in this non-completion split. -/
theorem moishezonFutureLeafLedgers_all_unchecked :
    moishezonFutureLeafLedgers.map MoishezonLeafLedgerRow.status =
      List.replicate 26 "unchecked" :=
  rfl

/-- This theorem-tree split is public-backfill metadata only, not a proof. -/
def c010TheoremTreeSplitClosesMoishezon : Bool := false

/-- Checked non-completion flag for the PUB-10 theorem-tree split. -/
theorem c010TheoremTreeSplitClosesMoishezon_eq_false :
    c010TheoremTreeSplitClosesMoishezon = false :=
  rfl

/-- Integration-ready public wording for `S1-M-037-PUB-10`. -/
def publicMoishezonTheoremTreeBackfillText : String :=
  "PUB-10 theorem-tree split: add root `MOI-ROOT` for Moishezon theorem and package rows `MOI-P01-statement-normalization`, `MOI-P02-mathlib-object-model`, `MOI-P03-meromorphic-function-field`, `MOI-P04-moishezon-algebraic-reduction`, `MOI-P05-modification-and-resolution`, `MOI-P06-analytic-to-scheme-algebraization`, `MOI-P07-projective-embedding-wrapper`, and `MOI-P08-repo-local-closure-gate`. Add an unchecked independent leaf ledger `MOI-L001` through `MOI-L026`, each with budget `<=100`, matching the checked repo-local metadata `moishezonTheoremTreePackages` and `moishezonFutureLeafLedgers` in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_037.lean`. This public split is a planning/audit surface only: `c010TheoremTreeSplitClosesMoishezon = false`, all package rows have `repoLocalClosed := false`, and all leaf rows remain `unchecked`. Do not mark S1-M-037 / THM-M-0117 completed until a local proof body, checked mathlib wrapper, or pinned/imported external Lean dependency validates the terminal theorem and every promoted leaf has its independent <=100 ledger closed."

/-! ## API audit probes -/

#check Scheme
#check IsClosedImmersion
#check IsProper
#check MoishezonDimensionProfile
#check MoishezonPredicate
#check moishezonPredicate_iff_dimension_eq
#check MoishezonAnalyticData.withDimensionProfile
#check ProjectiveSchemeModelData
#check ProjectiveAlgebraicModel
#check StatementShape
#check SchemeProjectiveViaClosedImmersion
#check SchemeProjectiveViaProjClosedImmersion
#check SchemeBridgeShape
#check closedImmersion_isProper
#check projectiveModelMorphism_isProper
#check schemeProjectiveViaClosedImmersion_isProper
#check schemeProjectiveViaProjClosedImmersion_to_closedImmersion
#check schemeProjectiveViaProjClosedImmersion_isProper
#check ProjectiveSchemeModelData.structureMap_isProper
#check mathlibAnchorModules
#check mathlibAnchorNames
#check MathlibAnchorRow
#check mathlibAnchorTable
#check checkedMathlibAnchorNames
#check externalLeanAuditSearchTerms
#check AnalyticDimensionApiAuditRow
#check meromorphicAlgebraicDimensionApiAudit
#check checkedAnalyticDimensionApiNames
#check hasRepoLocalComplexManifoldMeromorphicApi
#check hasRepoLocalComplexManifoldAlgebraicDimensionApi
#check hasConcreteMoishezonPredicateInputs
#check hasConcreteProjectiveAlgebraicModelPredicate
#check hasRepoLocalProjAmbientRefinement
#check hasProjOrProjectiveSpaceAlgebraicModelPredicate
#check meromorphic_id_complex_anchor
#check AlgebraicDimensionFieldSubstrate
#check algebraicDimensionFieldSubstrate_eq_trdeg
#check mathlibPinnedRevision
#check ExternalLean4SearchAuditRow
#check externalLean4PrimarySourceAudit
#check c008ExactExternalMoishezonProofFound
#check c008ExactExternalMoishezonProofFound_eq_false
#check c009ExternalMoishezonProofAvailableToIntegrate
#check c009ExternalMoishezonProofAvailableToIntegrate_eq_false
#check c009RepoLocalIntegrationGateStatus
#check publicExternalProofIntegrationGateBackfillText
#check publicExternalLean4AuditBackfillText
#check machineProofDebt
#check repoLocalIntegrationDebtGate
#check publicStage1BoundaryNote
#check PublicFormalTarget
#check publicFormalTargetDecision
#check publicFormalTargetDecisionText
#check publicFormalTargetRationale
#check publicMoishezonPredicateBackfillText
#check publicProjectiveModelPredicateBackfillText
#check publicProjAmbientBackfillText
#check MoishezonTheoremTreePackage
#check moishezonTheoremTreePackages
#check moishezonTheoremTreePackages_length
#check moishezonTheoremTreePackages_codes
#check moishezonTheoremTreePackages_no_repoLocalClosed_claim
#check MoishezonLeafLedgerRow
#check moishezonFutureLeafLedgers
#check moishezonFutureLeafLedgers_length
#check moishezonFutureLeafLedgers_all_budgeted
#check moishezonFutureLeafLedgers_all_unchecked
#check c010TheoremTreeSplitClosesMoishezon
#check c010TheoremTreeSplitClosesMoishezon_eq_false
#check publicMoishezonTheoremTreeBackfillText
#check Proj.toSpecZero
#check Sheaf.H
#check Sheaf.cohomologyFunctor
#check MorphismProperty.DescendsAlong
#check MDifferentiable.exists_eq_const_of_compactSpace
#check MeromorphicAt
#check MeromorphicOn
#check Meromorphic
#check AlgebraicIndependent
#check IsTranscendenceBasis
#check Algebra.trdeg

end AwesomeTheorems.Stage1.S1_M_037
