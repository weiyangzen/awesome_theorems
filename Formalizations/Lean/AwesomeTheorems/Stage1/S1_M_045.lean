import Mathlib.Algebra.Quaternion
import Mathlib.Algebra.QuaternionBasis
import Mathlib.AlgebraicGeometry.Cover.Open
import Mathlib.AlgebraicGeometry.Morphisms.FiniteType
import Mathlib.AlgebraicGeometry.Morphisms.FlatDescent
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Sites.Etale
import Mathlib.AlgebraicGeometry.Sites.Fpqc

/-!
# S1-M-045 / THM-M-0126: Shimura curve theorem, Stage1 boundary

This file is a Stage1 statement-shape artifact.  It records the mathlib objects that can
currently be checked locally: quaternion algebras, schemes, proper/smooth morphisms,
locally finite type and quasi-compact morphisms, smooth morphisms of relative dimension one,
locally noetherian schemes, affine open covers, sheaves of modules, etale/fppf/fpqc topologies,
and the available morphism-property descent substrate.

It defines a deliberately lightweight target predicate for the quaternionic Shimura-curve
moduli problem.  The predicate records the data that the future theorem must refine:
a quaternionic order, a level structure, a moduli functor, the chosen Grothendieck topology,
and the scheme asserted to represent that functor.  It does not assert that mathlib already
contains the full quaternionic Shimura moduli construction.
-/

noncomputable section

open AlgebraicGeometry CategoryTheory Opposite

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_045

/-- Minimal algebraic input for the Stage1 Shimura-curve statement shape. -/
structure QuaternionicModularDatum where
  R : Type u
  instCommRing : CommRing R
  a : R
  b : R
  c : R

attribute [instance] QuaternionicModularDatum.instCommRing

namespace QuaternionicModularDatum

/-- The quaternion algebra supplied by mathlib for the datum. -/
abbrev algebra (D : QuaternionicModularDatum.{u}) : Type u :=
  QuaternionAlgebra D.R D.a D.b D.c

/-- The affine base scheme attached to the coefficient ring of the datum. -/
abbrev baseScheme (D : QuaternionicModularDatum.{u}) : Scheme.{u} :=
  Scheme.Spec.obj (op <| CommRingCat.of D.R)

/-- A local check that the quaternion algebra comes with its standard four-element basis. -/
def quaternionBasis (D : QuaternionicModularDatum.{u}) : Module.Basis (Fin 4) D.R D.algebra :=
  QuaternionAlgebra.basisOneIJK D.a D.b D.c

end QuaternionicModularDatum

/-- The scheme-theoretic properties expected of a Shimura-curve model in the Stage1 boundary. -/
def GeometricCurvePackage (D : QuaternionicModularDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  IsProper π ∧ Smooth π ∧ IsLocallyNoetherian X

/--
Checked strengthening candidate for the geometric part of a Shimura-curve model.

Mathlib's current finite-type scheme API represents "finite type" as the pair
`LocallyOfFiniteType f` and `QuasiCompact f`; there is not a separate public class named
`FiniteType` for scheme morphisms in the checked substrate.  `SmoothOfRelativeDimension 1`
is available and implies `Smooth`, so the existing lightweight `GeometricCurvePackage` can
be strengthened along this axis without changing the public statement hook.
-/
structure GeometricCurvePackageStrengthening (D : QuaternionicModularDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop where
  proper : IsProper π
  locallyOfFiniteType : LocallyOfFiniteType π
  quasiCompact : QuasiCompact π
  smoothRelativeDimensionOne : SmoothOfRelativeDimension 1 π
  locallyNoetherian : IsLocallyNoetherian X

namespace GeometricCurvePackageStrengthening

/-- The strengthened package forgets to the original Stage1 geometric package. -/
theorem toGeometricCurvePackage {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricCurvePackageStrengthening D X π) :
    GeometricCurvePackage D X π := by
  letI : SmoothOfRelativeDimension 1 π := h.smoothRelativeDimensionOne
  exact ⟨h.proper, SmoothOfRelativeDimension.smooth (n := 1) (f := π), h.locallyNoetherian⟩

end GeometricCurvePackageStrengthening

/--
Stage1 placeholder for an order in the quaternion algebra attached to `D`.

This is intentionally weaker than a maximal or Eichler order: mathlib does not currently
provide the Shimura-curve order API needed for the terminal theorem, so this structure only
names the order carrier, its ring structure, and its map into the ambient quaternion algebra.
-/
structure QuaternionicOrder (D : QuaternionicModularDatum.{u}) where
  carrier : Type u
  instRing : Ring carrier
  toQuaternionAlgebra : carrier → D.algebra

attribute [instance] QuaternionicOrder.instRing

/--
Stage1 placeholder for a level structure attached to a quaternionic order.

The `levelCondition` field is a local predicate on order elements rather than a completed
adelic or congruence subgroup definition; it marks the precise target to refine later.
-/
structure QuaternionicLevelStructure (D : QuaternionicModularDatum.{u})
    (O : QuaternionicOrder D) where
  levelIndex : Type u
  levelCondition : O.carrier → Prop

/--
Presheaf-shaped target for the moduli functor of quaternionic abelian varieties.

The fields record the object assignment and pullback operation needed for a future functorial
moduli problem without claiming the full category-theoretic sheaf/stack construction.
-/
structure QuaternionicModuliFunctor (D : QuaternionicModularDatum.{u})
    (O : QuaternionicOrder D) (K : QuaternionicLevelStructure D O) where
  objects : Scheme.{u} → Type (u + 1)
  pullback : {T U : Scheme.{u}} → (T ⟶ U) → objects U → objects T

/--
Integration target for the missing quaternionic Shimura-curve moduli predicate.

`representingObject` and `representingMap` are included explicitly so that the target states
which scheme represents the functor and how it maps to the base.  The heterogeneous equality
field ties that representing pair to the `(X, π)` used by the public statement shape while
remaining lightweight enough for the current mathlib substrate.
-/
structure QuaternionicModuliTarget (D : QuaternionicModularDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) where
  order : QuaternionicOrder D
  levelStructure : QuaternionicLevelStructure D order
  moduliFunctor : QuaternionicModuliFunctor D order levelStructure
  chosenTopology : GrothendieckTopology Scheme.{u}
  representingObject : Scheme.{u}
  representingMap : representingObject ⟶ D.baseScheme
  representingObject_eq : representingObject = X
  representingMap_heq : HEq representingMap π
  isSheafForChosenTopology : Prop
  representsFunctor : Prop

/--
Concrete Stage1 target for `S1-M-045-PUB-03`.

The future theorem should replace the placeholder propositions inside
`QuaternionicModuliTarget` with the real quaternionic Shimura moduli construction and prove
representability.  For now, this predicate fixes the expected inputs and keeps the topology
choice explicit by requiring the big etale topology.
-/
def RepresentsQuaternionicModuli (D : QuaternionicModularDatum.{u}) (X : Scheme.{u})
    (π : X ⟶ D.baseScheme) : Prop :=
  ∃ target : QuaternionicModuliTarget D X π,
    target.chosenTopology = Scheme.etaleTopology ∧
      target.isSheafForChosenTopology ∧
      target.representsFunctor

/--
Statement-shape candidate for the Shimura curve theorem.

The predicate argument is retained as a generic statement-shape hook for downstream audits.
The concrete Stage1 target for this slot is `RepresentsQuaternionicModuli`.
-/
def StatementShape
    (RepresentsQuaternionicModuli :
      (D : QuaternionicModularDatum.{u}) → (X : Scheme.{u}) → (X ⟶ D.baseScheme) → Prop) :
    Prop :=
  ∀ D : QuaternionicModularDatum.{u},
    ∃ X : Scheme.{u}, ∃ π : X ⟶ D.baseScheme,
      GeometricCurvePackage D X π ∧ RepresentsQuaternionicModuli D X π

/-- Statement shape using the concrete quaternionic moduli target introduced in this file. -/
def QuaternionicModuliStatementShape : Prop :=
  StatementShape.{u} RepresentsQuaternionicModuli

/-- mathlib anchor: affine open covers of schemes are available. -/
def affineOpenCoverAnchor (X : Scheme.{u}) : X.OpenCover :=
  X.affineCover

/-- mathlib anchor: the public `Scheme.OpenCover` type family is available. -/
def schemeOpenCoverTypeAnchor (X : Scheme.{u}) : Type _ :=
  Scheme.OpenCover X

/-- mathlib anchor: categories of sheaves of modules on schemes are available. -/
def moduleSheafCategoryAnchor (X : Scheme.{u}) : Type (u + 1) :=
  X.Modules

/-- mathlib anchor: the public `Scheme.Modules` type family is available. -/
def schemeModulesTypeAnchor (X : Scheme.{u}) : Type (u + 1) :=
  Scheme.Modules X

/-- mathlib anchor: the big etale topology on schemes is available. -/
def etaleTopologyAnchor : GrothendieckTopology Scheme.{u} :=
  Scheme.etaleTopology

/-! ## Audit constants -/

/-- The mathlib revision used for the public anchor audit in this Stage1 slot. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Quaternion",
  "Mathlib.Algebra.QuaternionBasis",
  "Mathlib.AlgebraicGeometry.Cover.Open",
  "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
  "Mathlib.AlgebraicGeometry.Morphisms.FlatDescent",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Noetherian",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.AlgebraicGeometry.Sites.Etale",
  "Mathlib.AlgebraicGeometry.Sites.Fpqc"
]

/-- Public mathlib anchor table for `S1-M-045-PUB-02`. -/
def publicMathlibAnchorTable : List (String × String × String) := [
  ("QuaternionAlgebra", "Mathlib.Algebra.Quaternion",
    "quaternion algebra type family for the coefficient datum"),
  ("QuaternionAlgebra.basisOneIJK", "Mathlib.Algebra.QuaternionBasis",
    "standard one/i/j/k basis for the quaternion algebra"),
  ("Scheme", "Mathlib.AlgebraicGeometry.Scheme",
    "category of schemes used for the Stage1 geometric object"),
  ("Scheme.OpenCover", "Mathlib.AlgebraicGeometry.Cover.Open",
    "open covers of schemes, including affine open covers"),
  ("LocallyOfFiniteType", "Mathlib.AlgebraicGeometry.Morphisms.FiniteType",
    "locally finite type component of finite-type scheme morphisms"),
  ("QuasiCompact", "Mathlib.AlgebraicGeometry.Morphisms.QuasiCompact",
    "quasi-compact component of finite-type scheme morphisms"),
  ("IsProper", "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    "properness predicate for the structure morphism"),
  ("Smooth", "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    "smoothness predicate for the structure morphism"),
  ("SmoothOfRelativeDimension", "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    "relative-dimension refinement of smoothness, including dimension one"),
  ("IsLocallyNoetherian", "Mathlib.AlgebraicGeometry.Noetherian",
    "locally noetherian predicate for the scheme model"),
  ("Scheme.Modules", "Mathlib.AlgebraicGeometry.Modules.Sheaf",
    "category of sheaves of modules over a scheme"),
  ("Scheme.etaleTopology", "Mathlib.AlgebraicGeometry.Sites.Etale",
    "big etale Grothendieck topology on schemes"),
  ("Scheme.fppfTopology", "Mathlib.AlgebraicGeometry.Sites.Fpqc",
    "fppf Grothendieck topology on schemes"),
  ("Scheme.fpqcTopology", "Mathlib.AlgebraicGeometry.Sites.Fpqc",
    "fpqc Grothendieck topology on schemes"),
  ("MorphismProperty.DescendsAlong", "Mathlib.CategoryTheory.MorphismProperty.Descent",
    "abstract descent interface for morphism properties")
]

/-- Structured audit row for `S1-M-045-PUB-04`. -/
structure GeometricCurveApiAuditRow where
  requested : String
  moduleName : String
  checkedDeclaration : String
  repoLocalStatus : String
  note : String

/--
Repo-local audit for strengthening `GeometricCurvePackage`.

The result is mixed but useful: finite-type components and smooth relative dimension one
validate locally, so the artifact exposes `GeometricCurvePackageStrengthening`.  Descent is
only partial for the Shimura-curve target: mathlib has the generic descent class, fppf/fpqc
topologies, and fpqc descent for several global morphism properties, but this pass did not
locate a checked one-shot descent theorem for the full package
`IsProper ∧ SmoothOfRelativeDimension 1 ∧ RepresentsQuaternionicModuli`.
-/
def geometricCurvePackageApiAudit : List GeometricCurveApiAuditRow := [
  {
    requested := "finite type for scheme morphisms"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.FiniteType; Mathlib.AlgebraicGeometry.Morphisms.QuasiCompact"
    checkedDeclaration := "AlgebraicGeometry.LocallyOfFiniteType; AlgebraicGeometry.QuasiCompact"
    repoLocalStatus := "checked_as_components"
    note := "The checked API represents finite type for schemes as locally finite type plus quasi-compact, not as a separate `FiniteType` class."
  },
  {
    requested := "relative dimension one"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Smooth"
    checkedDeclaration := "AlgebraicGeometry.SmoothOfRelativeDimension"
    repoLocalStatus := "checked"
    note := "`SmoothOfRelativeDimension 1 π` is available and forgets to `Smooth π` through `SmoothOfRelativeDimension.smooth`."
  },
  {
    requested := "smooth/proper curve package"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Proper; Mathlib.AlgebraicGeometry.Morphisms.Smooth; Mathlib.AlgebraicGeometry.Noetherian"
    checkedDeclaration := "AlgebraicGeometry.IsProper; AlgebraicGeometry.Smooth; AlgebraicGeometry.IsLocallyNoetherian"
    repoLocalStatus := "checked_strengthening_candidate"
    note := "`GeometricCurvePackageStrengthening` records proper, locally finite type, quasi-compact, smooth relative dimension one, and locally noetherian hypotheses and forgets to the older package."
  },
  {
    requested := "descent API for geometric properties"
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.FlatDescent; Mathlib.AlgebraicGeometry.Sites.Fpqc"
    checkedDeclaration := "CategoryTheory.MorphismProperty.DescendsAlong; AlgebraicGeometry.descendsAlong_universallyClosed_surjective_inf_flat_inf_quasicompact; AlgebraicGeometry.Scheme.fppfTopology; AlgebraicGeometry.Scheme.fpqcTopology"
    repoLocalStatus := "checked_partial_not_terminal"
    note := "The generic descent interface and fppf/fpqc topologies are present; this audit does not close descent for the full Shimura moduli representability package."
  }
]

/-- Machine-readable PUB-04 conclusion for the local artifact. -/
def geometricCurvePackageStrengtheningConclusion : String :=
  "finite_type_components_and_relative_dimension_one_checked; descent_substrate_partial; terminal_Shimura_curve_package_not_completed"

/-- Search terms that did not locate a terminal Shimura-curve theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "ShimuraCurve",
  "Shimura curve",
  "QuaternionicModularCurve",
  "quaternionic moduli"
]

/-- Search terms requested by `S1-M-045-PUB-05`. -/
def externalLeanSearchTerms : List String := [
  "ShimuraCurve",
  "Shimura curve",
  "Shimura",
  "QuaternionAlgebra",
  "ModularCurve"
]

/-- Structured row for the external Lean 4 source audit in `S1-M-045-PUB-05`. -/
structure ExternalLeanSourceAuditRow where
  searchTerm : String
  repositoryUrl : String
  commit : String
  moduleName : String
  declarations : String
  lakeCompatibility : String
  terminalShimuraCurveStatus : String

/--
External Lean 4 source audit rows for `S1-M-045-PUB-05`.

This is deliberately not a completion table.  The GitHub CLI was present but not
authenticated in this worker environment, so authenticated GitHub code search remains an
integration blocker.  The rows below record primary sources that were directly inspected:
the pinned local mathlib dependency and a directly cloned external Lean 4 repository that
contains quaternion-algebra automorphic-form code but no terminal Shimura-curve theorem.
-/
def externalLeanSourceAudit : List ExternalLeanSourceAuditRow := [
  {
    searchTerm := "QuaternionAlgebra"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibAnchorRevision
    moduleName := "Mathlib.Algebra.Quaternion; Mathlib.Algebra.QuaternionBasis"
    declarations := "QuaternionAlgebra; QuaternionAlgebra.basisOneIJK"
    lakeCompatibility := "compatible_and_pinned_in_this_repo"
    terminalShimuraCurveStatus := "substrate_only_no_ShimuraCurve_or_ModularCurve_theorem"
  },
  {
    searchTerm := "ShimuraCurve; Shimura curve; Shimura; ModularCurve"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commit := mathlibAnchorRevision
    moduleName := "local source search under Mathlib"
    declarations := "no declarations found for ShimuraCurve, Shimura curve, Shimura, or ModularCurve"
    lakeCompatibility := "compatible_and_pinned_in_this_repo"
    terminalShimuraCurveStatus := "not_found_in_local_mathlib_closure"
  },
  {
    searchTerm := "QuaternionAlgebra"
    repositoryUrl := "https://github.com/ImperialCollegeLondon/FLT"
    commit := "2f4325e3b3e647225890f143d4f2dbf1315d4ebd"
    moduleName := "FLT.Mathlib.Algebra.IsQuaternionAlgebra; FLT.QuaternionAlgebra.NumberField; FLT.AutomorphicForm.QuaternionAlgebra.Defs; FLT.AutomorphicForm.QuaternionAlgebra.HeckeOperators.Concrete"
    declarations := "IsQuaternionAlgebra; IsQuaternionAlgebra.IsTotallyDefinite; IsQuaternionAlgebra.NumberField.Rigidification; IsQuaternionAlgebra.NumberField.IsUnramified; QuaternionAlgebra.TameLevel; TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm; TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicFormOfLevel; TotallyDefiniteQuaternionAlgebra.WeightTwoAutomorphicForm.HeckeAlgebra"
    lakeCompatibility := "not_directly_compatible: upstream uses leanprover/lean4:v4.30.0-rc2 and mathlib 244d9a4c3071a109aa54a41242317594d3c83fb4 while this repo uses leanprover/lean4:v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    terminalShimuraCurveStatus := "adjacent_quaternion_automorphic_code_only; no ShimuraCurve or ModularCurve terminal theorem found; inspected files contain proof placeholders"
  }
]

/-- Authentication state for the external GitHub code-search part of `S1-M-045-PUB-05`. -/
def externalLeanSearchAuthenticationStatus : String :=
  "blocked: gh auth status reports not logged in and GH_TOKEN/GITHUB_TOKEN are unset; GitHub code search page and REST code search require sign-in/authentication"

/-- Machine-readable conclusion for `S1-M-045-PUB-05` and the `PUB-06` gate. -/
def externalLeanSearchConclusion : String :=
  "no_repo_local_completion: no external Lean 4 Shimura-curve proof was found in inspected primary sources; authenticated global GitHub code search still requires credentials; FLT is adjacent only and toolchain-incompatible"

/--
Machine proof debt for this Stage1 artifact.

The human theorem is mathematically known, but this repo-local Lean module only checks the
statement boundary and mathlib substrate wrappers; it does not contain a proof of the
quaternionic Shimura-curve representability theorem.
-/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration gate for this repair pass.

No external Lean 4 proof of the terminal Shimura-curve theorem is pinned into the local Lake
closure here, so the module must remain open rather than completed.
-/
def repoLocalIntegrationDebtGate : String :=
  "not_completed_no_repo_local_integration_debt_claim"

/-- Structured `S1-M-045-PUB-06` integration gate. -/
structure Pub06IntegrationGate where
  externalProofFoundInInspectedSources : Bool
  pinnedDependencyAdded : Bool
  concreteBlockerForFoundProof : String
  completionClaimAllowed : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  note : String

/--
Current `S1-M-045-PUB-06` result.

No proof-bearing external Lean 4 Shimura-curve theorem was found in the inspected primary
sources recorded by `externalLeanSourceAudit`, so there is no pin-ready external dependency
to add in this pass.  The gate remains closed to completion: if authenticated search later
finds such a proof, it must be pinned/imported/checked locally or blocked with a concrete
toolchain, dependency, license, theorem-mismatch, or proof-placeholder reason.
-/
def pub06IntegrationGate : Pub06IntegrationGate := {
  externalProofFoundInInspectedSources := false
  pinnedDependencyAdded := false
  concreteBlockerForFoundProof := "not_applicable_no_proof_bearing_external_Shimura_curve_theorem_found_in_inspected_sources"
  completionClaimAllowed := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  note := "open_formalization_debt; FLT is adjacent quaternion automorphic-form code only and is not a terminal Shimura-curve proof; authenticated GitHub code search still requires credentials"
}

/-- PUB-06 does not allow a theorem-completion claim in the current repo-local state. -/
theorem pub06IntegrationGate_no_completion_claim :
    pub06IntegrationGate.completionClaimAllowed = false :=
  rfl

/-- PUB-06 retains no completed-state `repo_local_integration_debt`. -/
theorem pub06IntegrationGate_no_completed_repoLocalIntegrationDebt :
    pub06IntegrationGate.repoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-- Independent `<= 100` step ledger for one unchecked Stage1 proof leaf. -/
structure Pub07IndependentLeafLedger where
  leafId : String
  parentPackage : String
  target : String
  budgetBound : Nat
  steps : List String
  proofStatus : String
  completionGate : String

/--
Expanded M0387 leaf ledgers for `S1-M-045-L11` through `S1-M-045-L18`.

These ledgers are deliberately process-level artifacts.  They split the remaining unchecked
frontier into independent sub-100-step execution units, but they do not prove the terminal
Shimura-curve theorem and do not authorize a completion claim.
-/
def pub07IndependentLeafLedgers : List Pub07IndependentLeafLedger := [
  {
    leafId := "S1-M-045-L11"
    parentPackage := "P02.quaternion_object_model"
    target := "Define quaternionic orders and optimal embeddings needed by the moduli problem."
    budgetBound := 100
    steps := [
      "Fix the coefficient datum D and ambient quaternion algebra D.algebra.",
      "Choose the exact order notion: carrier, ring structure, and map into D.algebra.",
      "Record whether the map must be injective, algebraic, or merely structural.",
      "Add the maximal/Eichler qualifier as a named refinement rather than overloading the base order.",
      "Define an optimal embedding source order and target quaternionic order.",
      "State the optimality condition as equality with the intersection in the ambient algebra when the required API exists.",
      "Separate the placeholder fields that are already Lean-checkable from future algebra facts.",
      "Expose a small projection/audit table for downstream moduli use.",
      "Validate the order and embedding declarations with the local Lean command.",
      "Keep this leaf open until the optimality condition is proof-bearing rather than metadata-only."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_order_and_optimal_embedding_API_is_proof_bearing"
  },
  {
    leafId := "S1-M-045-L12"
    parentPackage := "P03.scheme_curve_package"
    target := "Add curve-specific finite type / relative dimension / separatedness package."
    budgetBound := 100
    steps := [
      "Fix X and the structural morphism pi to D.baseScheme.",
      "Use LocallyOfFiniteType and QuasiCompact as the checked finite-type components.",
      "Use SmoothOfRelativeDimension 1 as the curve-dimension refinement.",
      "Audit whether the selected target also needs IsSeparated or whether IsProper supplies the needed separatedness.",
      "Package properness, finite-type components, relative dimension one, and local noetherianity in one structure.",
      "Prove the package forgets to the existing GeometricCurvePackage.",
      "Add projection wrappers for every component needed by later leaves.",
      "Record any missing separatedness declaration as an explicit blocker rather than implicit debt.",
      "Validate the strengthened package locally.",
      "Keep this leaf open until the public theorem target chooses the exact curve-property package."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_curve_package_is_selected_and_publicly_merged"
  },
  {
    leafId := "S1-M-045-L13"
    parentPackage := "P04.cover_descent_package"
    target := "Prove relevant proper/smooth/base-change stability wrappers for the selected model."
    budgetBound := 100
    steps := [
      "List each morphism property required by the selected geometric package.",
      "For properness, identify existing mathlib base-change and descent declarations.",
      "For smoothness, identify existing base-change and locality declarations.",
      "For SmoothOfRelativeDimension 1, audit whether base-change stability is directly available.",
      "For finite-type components, align LocallyOfFiniteType and QuasiCompact stability wrappers.",
      "Choose the topology for descent: etale, fppf, or fpqc.",
      "Create one wrapper theorem per property rather than one monolithic package theorem.",
      "Mark any unavailable wrapper as a concrete API blocker with module and searched declaration names.",
      "Validate every wrapper theorem or blocker row locally.",
      "Keep the leaf open until all wrappers required by the final selected package are proof-bearing."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_required_stability_wrappers_are_checked_or_blocked"
  },
  {
    leafId := "S1-M-045-L14"
    parentPackage := "P05.sheaf_cohomology_package"
    target := "Identify the exact sheaf/cohomology API needed for the intended theorem statement."
    budgetBound := 100
    steps := [
      "Decide whether the Stage1 theorem needs only the moduli functor sheaf condition or also cohomology.",
      "Anchor Scheme.Modules and the chosen Grothendieck topology.",
      "Audit available sheaf categories on the chosen site.",
      "Audit whether abelian sheaves, module sheaves, or presheaves suffice for the statement.",
      "Record required pullback functoriality for the moduli functor.",
      "Separate automorphic-form or cohomological applications from representability if they are not needed.",
      "Add checked metadata rows for each API declaration that exists.",
      "Add blocker rows for missing cohomology declarations with exact searched names.",
      "Validate the API table locally.",
      "Keep this leaf open until the theorem statement no longer has an unspecified sheaf/cohomology layer."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_sheaf_or_cohomology_scope_is_fixed"
  },
  {
    leafId := "S1-M-045-L15"
    parentPackage := "P06.moduli_representability_package"
    target := "Define RepresentsQuaternionicModuli without placeholders."
    budgetBound := 100
    steps := [
      "Fix the quaternionic order input from L11.",
      "Fix the level-structure input and its congruence or adelic interpretation.",
      "Define the moduli object assigned to every test scheme.",
      "Define pullback of moduli objects along scheme morphisms.",
      "State functorial identity and composition laws as explicit fields or theorem obligations.",
      "Choose the topology in which the functor is a sheaf.",
      "Define representation by X using a natural equivalence rather than opaque Prop fields.",
      "Tie the representing object and structural morphism to the public X and pi.",
      "Validate the declaration without Prop placeholders standing in for the core construction.",
      "Keep this leaf open until the moduli predicate has proof-bearing construction fields."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_RepresentsQuaternionicModuli_has_no_core_placeholders"
  },
  {
    leafId := "S1-M-045-L16"
    parentPackage := "P06.moduli_representability_package"
    target := "Prove the moduli functor is a sheaf for the selected topology."
    budgetBound := 100
    steps := [
      "Use the topology selected in L14 and L15.",
      "State the covering-family descent datum for moduli objects.",
      "Define restrictions of moduli objects to each cover member.",
      "Define compatibility on pairwise overlaps or pullback intersections.",
      "Prove uniqueness of glued objects when the relevant separatedness data is available.",
      "Prove existence of glued objects from descent data.",
      "Package uniqueness and existence as the sheaf condition expected by mathlib.",
      "Add base-change compatibility of the glued object.",
      "Validate the sheaf theorem locally or record exact missing descent APIs.",
      "Keep this leaf open until the sheaf condition is a checked theorem, not an assumption."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_moduli_sheaf_condition_is_checked"
  },
  {
    leafId := "S1-M-045-L17"
    parentPackage := "P06.moduli_representability_package"
    target := "Prove representability by a scheme/curve."
    budgetBound := 100
    steps := [
      "Choose the construction of the candidate representing scheme X.",
      "Construct the structural morphism pi to D.baseScheme.",
      "Construct the universal moduli object over X.",
      "Define the map from T-points of X to moduli objects over T.",
      "Define the inverse map from moduli objects over T to T-points of X.",
      "Prove the two maps are inverse.",
      "Prove naturality in the test scheme T.",
      "Transfer the geometric curve package to the constructed X.",
      "Validate the representability theorem locally or record exact missing construction APIs.",
      "Keep this leaf open until representability and geometric properties are both checked."
    ]
    proofStatus := "expanded_open_formalization_debt"
    completionGate := "no_completion_claim_until_representability_by_curve_is_checked"
  },
  {
    leafId := "S1-M-045-L18"
    parentPackage := "P07.repo_local_closure_gate"
    target := "If external proof exists, pin/import/check dependency or record exact blocker."
    budgetBound := 100
    steps := [
      "Rerun authenticated GitHub code search for the required Shimura and quaternion terms.",
      "For every proof-bearing candidate, record repository URL, commit, module, theorem names, and license.",
      "Check the candidate for proof placeholders in the relevant terminal modules.",
      "Compare Lean version, mathlib revision, and Lake dependencies with this repository.",
      "If compatible, add a pinned dependency or vendored proof body in the local Lake closure.",
      "If incompatible, record a concrete blocker: toolchain, dependency, license, theorem mismatch, missing export, or placeholder proof.",
      "Add a repo-local wrapper theorem only after the dependency validates locally.",
      "Run the required local Lean validation command.",
      "Update the integration gate so completed state cannot retain repo_local_integration_debt.",
      "Keep this leaf open until pin/import/check succeeds or a concrete blocker is recorded."
    ]
    proofStatus := "expanded_open_external_anchor_gate"
    completionGate := "no_completion_claim_from_anchor_only_evidence"
  }
]

/-- The PUB-07 expansion records exactly the eight requested unchecked leaves. -/
theorem pub07IndependentLeafLedgers_count :
    pub07IndependentLeafLedgers.length = 8 :=
  rfl

/-- Every PUB-07 expanded leaf ledger is below its declared `<= 100` step budget. -/
theorem pub07IndependentLeafLedgers_within_budget :
    pub07IndependentLeafLedgers.all (fun leaf => leaf.steps.length <= leaf.budgetBound) = true :=
  rfl

/-- PUB-07 only expands ledgers; it does not allow a theorem-completion claim. -/
def pub07CompletionClaimAllowed : Bool :=
  false

/-- The PUB-07 ledger expansion keeps the terminal theorem open. -/
theorem pub07_no_completion_claim :
    pub07CompletionClaimAllowed = false :=
  rfl

/-- Projection wrapper for the properness component of the geometric package. -/
theorem properProjectionAnchor {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricCurvePackage D X π) : IsProper π :=
  h.1

/-- Projection wrapper for the smoothness component of the geometric package. -/
theorem smoothProjectionAnchor {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricCurvePackage D X π) : Smooth π :=
  h.2.1

/-- Projection wrapper for the locally noetherian component of the geometric package. -/
theorem locallyNoetherianAnchor {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : GeometricCurvePackage D X π) : IsLocallyNoetherian X :=
  h.2.2

/-- Proper morphisms carry the locally finite type component in mathlib. -/
theorem properLocallyOfFiniteTypeAnchor {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : IsProper π) : LocallyOfFiniteType π := by
  letI : IsProper π := h
  infer_instance

/-- Proper morphisms carry the quasi-compact component in mathlib. -/
theorem properQuasiCompactAnchor {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : IsProper π) : QuasiCompact π := by
  letI : IsProper π := h
  infer_instance

/-- Smooth relative dimension one forgets to smoothness. -/
theorem smoothRelativeDimensionOneAnchor {D : QuaternionicModularDatum.{u}} {X : Scheme.{u}}
    {π : X ⟶ D.baseScheme} (h : SmoothOfRelativeDimension 1 π) : Smooth π := by
  letI : SmoothOfRelativeDimension 1 π := h
  exact SmoothOfRelativeDimension.smooth (n := 1) (f := π)

/-! ## Audit probes -/

#check QuaternionAlgebra
#check QuaternionAlgebra.basisOneIJK
#check Scheme.Spec
#check Scheme.OpenCover
#check LocallyOfFiniteType
#check QuasiCompact
#check IsProper
#check Smooth
#check SmoothOfRelativeDimension
#check IsLocallyNoetherian
#check Scheme.Modules
#check Scheme.etaleTopology
#check Scheme.fppfTopology
#check Scheme.fpqcTopology
#check MorphismProperty.DescendsAlong
#check descendsAlong_universallyClosed_surjective_inf_flat_inf_quasicompact
#check QuaternionicOrder
#check QuaternionicLevelStructure
#check QuaternionicModuliFunctor
#check QuaternionicModuliTarget
#check RepresentsQuaternionicModuli
#check GeometricCurvePackageStrengthening
#check GeometricCurvePackageStrengthening.toGeometricCurvePackage
#check properLocallyOfFiniteTypeAnchor
#check properQuasiCompactAnchor
#check smoothRelativeDimensionOneAnchor
#check geometricCurvePackageApiAudit
#check geometricCurvePackageStrengtheningConclusion
#check externalLeanSearchTerms
#check externalLeanSourceAudit
#check externalLeanSearchAuthenticationStatus
#check externalLeanSearchConclusion
#check Pub06IntegrationGate
#check pub06IntegrationGate
#check pub06IntegrationGate_no_completion_claim
#check pub06IntegrationGate_no_completed_repoLocalIntegrationDebt
#check Pub07IndependentLeafLedger
#check pub07IndependentLeafLedgers
#check pub07IndependentLeafLedgers_count
#check pub07IndependentLeafLedgers_within_budget
#check pub07CompletionClaimAllowed
#check pub07_no_completion_claim
#check StatementShape
#check QuaternionicModuliStatementShape

end S1_M_045
end Stage1
end AwesomeTheorems
