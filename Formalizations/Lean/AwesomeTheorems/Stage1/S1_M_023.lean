import Mathlib.AlgebraicGeometry.Noetherian
import Mathlib.AlgebraicGeometry.Pullbacks
import Mathlib.AlgebraicGeometry.Cover.Open
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Modules.Tilde
import Mathlib.Algebra.Homology.DerivedCategory.HomologySequence
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic

/-!
# S1-M-023 / THM-M-0115: Grothendieck-Riemann-Roch theorem

This Stage1 repair artifact records a conservative Lean 4 boundary for the
Grothendieck-Riemann-Roch formula for schemes.

The file does not claim a repo-local proof of GRR.  It freezes a precise
statement-shape around mathlib's current scheme, morphism, noetherian, cover,
and pullback APIs, and names the unavailable K-theory/Chow/Chern/Todd layers as
explicit proposition boundaries for later replacement by concrete APIs or a
pinned upstream theorem.
-/

open CategoryTheory
open CategoryTheory.Limits
open AlgebraicGeometry

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_023

universe u v w w'

/--
Input package for the Grothendieck-Riemann-Roch formula.

The scheme objects, morphism, noetherian hypotheses, properness, and finite
presentation hypotheses use current mathlib APIs.  The GRR-specific cycle,
K-theory, Chern-character, Todd-class, and equality targets are deliberately
kept as named proposition fields because the current repo-local dependency
closure does not expose a terminal GRR theorem or a complete cycle/K-theory
interface for this statement.
-/
structure GrothendieckRiemannRochInput where
  base : Scheme.{u}
  source : Scheme.{u}
  target : Scheme.{u}
  sourceToBase : source ⟶ base
  targetToBase : target ⟶ base
  map : source ⟶ target
  map_commutes : sourceToBase = map ≫ targetToBase
  sourceNoetherian : IsNoetherian source
  targetNoetherian : IsNoetherian target
  proper : IsProper map
  finitePresentation : LocallyOfFinitePresentation map
  perfectOrCoherentInput : Prop
  kTheoryPushforwardDefined : Prop
  chowOrCohomologyPushforwardDefined : Prop
  chernCharacterDefined : Prop
  toddClassDefined : Prop
  virtualTangentClassDefined : Prop
  grrIdentity : Prop

/--
Root Stage1 statement shape for GRR.

Informally this is the equality

`ch (f_! x) * Td(Y) = f_* (ch x * Td(X))`

for a proper morphism of suitable noetherian schemes.  The Lean boundary below
keeps the existing mathlib-backed scheme and morphism hypotheses in the input
structure and exposes the unavailable GRR-specific operations as explicit
premises.
-/
def StatementShape : Prop :=
  ∀ D : GrothendieckRiemannRochInput.{u},
    D.perfectOrCoherentInput →
      D.kTheoryPushforwardDefined →
        D.chowOrCohomologyPushforwardDefined →
          D.chernCharacterDefined →
            D.toddClassDefined →
              D.virtualTangentClassDefined →
                D.grrIdentity

/-! ## Statement-normalization candidates -/

/--
Candidate A: a mathematically faithful GRR formula boundary.

This freezes the intended equality

`ch_Y (f_! x) * Td(Y) = f_* (ch_X x * Td(X))`

without pretending that the current repo-local mathlib closure provides the
required K-theory, Chow/cohomology target, Chern character, Todd class, or
proper pushforward APIs.
-/
structure CandidateAFormulaInput where
  source : Scheme.{u}
  target : Scheme.{u}
  map : source ⟶ target
  proper : IsProper map
  perfectOrLciHypothesis : Prop
  kSource : Type u
  kTarget : Type u
  cycleSource : Type u
  cycleTarget : Type u
  kTheoryPushforward : kSource → kTarget
  cyclePushforward : cycleSource → cycleTarget
  chernCharacterSource : kSource → cycleSource
  chernCharacterTarget : kTarget → cycleTarget
  toddSource : cycleSource
  toddTarget : cycleTarget
  cycleMulSource : cycleSource → cycleSource → cycleSource
  cycleMulTarget : cycleTarget → cycleTarget → cycleTarget

/-- Candidate A statement shape for the classical GRR formula. -/
def CandidateAStatementShape : Prop :=
  ∀ D : CandidateAFormulaInput.{u},
    D.perfectOrLciHypothesis →
      ∀ x : D.kSource,
        D.cycleMulTarget (D.chernCharacterTarget (D.kTheoryPushforward x)) D.toddTarget =
          D.cyclePushforward (D.cycleMulSource (D.chernCharacterSource x) D.toddSource)

/--
Candidate B: a Todd-twisted naturality boundary.

This is the better target if an imported project states GRR as commutation of a
Todd-twisted transformation with proper pushforward, rather than as a literal
expanded `ch * Td` equality.
-/
structure CandidateBNaturalityInput where
  source : Scheme.{u}
  target : Scheme.{u}
  map : source ⟶ target
  proper : IsProper map
  kSource : Type u
  kTarget : Type u
  targetTheorySource : Type u
  targetTheoryTarget : Type u
  kTheoryPushforward : kSource → kTarget
  targetTheoryPushforward : targetTheorySource → targetTheoryTarget
  toddTwistedTransformSource : kSource → targetTheorySource
  toddTwistedTransformTarget : kTarget → targetTheoryTarget

/-- Candidate B statement shape for Todd-twisted pushforward naturality. -/
def CandidateBStatementShape : Prop :=
  ∀ D : CandidateBNaturalityInput.{u},
    ∀ x : D.kSource,
      D.toddTwistedTransformTarget (D.kTheoryPushforward x) =
        D.targetTheoryPushforward (D.toddTwistedTransformSource x)

/--
Explicit structures still missing before either Candidate A or Candidate B can
be upgraded from a statement boundary to a terminal GRR theorem in this repo.
-/
def statementNormalizationMissingStructures : List String := [
  "K_0 or G-theory object for schemes/perfect complexes",
  "proper pushforward f_! on K-theory or G-theory",
  "Chow, operational Chow, or cohomological target theory with rational coefficients",
  "proper pushforward on the selected Chow/cohomology target",
  "Chern character from K-theory/perfect complexes to the target theory",
  "Todd class or Todd-twisted transformation",
  "multiplicative structure and grading on the target theory",
  "virtual tangent or relative cotangent complex package",
  "comparison theorem between Candidate A and Candidate B if both are retained",
  "terminal GRR theorem name from a pinned local or external Lean dependency"
]

/-! ## Public object-model audit payload -/

/--
Object-model rows required by the public `THM-M-0115` Stage1 backfill.

These rows are intentionally about mathlib surface area only.  They do not
assert a Grothendieck-Riemann-Roch theorem.
-/
inductive MathlibObjectModelTarget where
  | scheme
  | isProper
  | schemeModules
  | modulesPushforward
  | modulesPullback
  | quasiCoherentSheaves
  | sheafCohomology
  | derivedCategories
  deriving DecidableEq, Repr

/-- One public-audit row for the GRR mathlib object model. -/
structure MathlibObjectModelAuditRow where
  target : MathlibObjectModelTarget
  publicName : String
  modulePath : String
  checkedAnchor : String
  localWrapper : String
  grrUse : String
  status : String
  nextGate : String
  repoLocalGRRClosed : Bool
  deriving DecidableEq, Repr

/--
Integration-ready mathlib object-model audit table for the public blueprint.

Every row is import-checkable support or a formalization-debt boundary.  The
final GRR theorem remains open until K-theory/Chow/Chern/Todd/pushforward
layers and the terminal identity are supplied by local proof or pinned imports.
-/
def mathlibObjectModelAuditTable : List MathlibObjectModelAuditRow := [
  {
    target := MathlibObjectModelTarget.scheme
    publicName := "Scheme"
    modulePath := "Mathlib.AlgebraicGeometry.Scheme plus Noetherian/Pullbacks/Cover.Open imports"
    checkedAnchor := "AlgebraicGeometry.Scheme"
    localWrapper := "scheme_has_pullbacks; affineOpenCoverWrapper"
    grrUse := "Source and target objects X,Y and base-change squares for the GRR statement."
    status := "checked_support"
    nextGate := "Choose the exact base-change square API used by the terminal statement."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.isProper
    publicName := "IsProper"
    modulePath := "Mathlib.AlgebraicGeometry.Morphisms.Proper"
    checkedAnchor := "AlgebraicGeometry.IsProper"
    localWrapper := "identity_isProper"
    grrUse := "Proper morphism hypothesis needed for f_! and target-side pushforward."
    status := "checked_support"
    nextGate := "Connect properness to the selected K-theory and Chow/cohomology pushforward APIs."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.schemeModules
    publicName := "X.Modules"
    modulePath := "Mathlib.AlgebraicGeometry.Modules.Sheaf"
    checkedAnchor := "AlgebraicGeometry.Scheme.Modules"
    localWrapper := "schemeModules_abelian; schemeModules_hasLimits; schemeModules_hasColimits"
    grrUse := "Sheaves of modules over schemes; substrate for coherent/perfect inputs and derived functors."
    status := "checked_support"
    nextGate := "Audit the coherent/perfect subcategory selected for K-theory or G-theory."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.modulesPushforward
    publicName := "Scheme.Modules.pushforward"
    modulePath := "Mathlib.AlgebraicGeometry.Modules.Sheaf"
    checkedAnchor := "AlgebraicGeometry.Scheme.Modules.pushforward"
    localWrapper := "modulesPushforwardWrapper"
    grrUse := "Sheaf-module direct image along a scheme morphism."
    status := "checked_support"
    nextGate := "Do not confuse sheaf pushforward with K-theory f_!; audit the derived/exactness bridge."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.modulesPullback
    publicName := "Scheme.Modules.pullback"
    modulePath := "Mathlib.AlgebraicGeometry.Modules.Sheaf"
    checkedAnchor := "AlgebraicGeometry.Scheme.Modules.pullback and pullbackPushforwardAdjunction"
    localWrapper := "modulesPullbackWrapper; modulesPullbackPushforwardAdjunctionWrapper"
    grrUse := "Inverse-image side and adjunction substrate for projection-formula-style infrastructure."
    status := "checked_support"
    nextGate := "Audit projection formula and derived pullback/pushforward statements before GRR use."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.quasiCoherentSheaves
    publicName := "quasi-coherent sheaves"
    modulePath := "Mathlib.AlgebraicGeometry.Modules.Tilde"
    checkedAnchor := "AlgebraicGeometry.tilde; SheafOfModules.IsQuasicoherent"
    localWrapper := "tilde_isQuasicoherent"
    grrUse := "Affine quasi-coherent examples and presentation API for coherent/perfect sheaf inputs."
    status := "partial_checked_support"
    nextGate := "Audit the scheme-global QCoh category and exact/coherent/perfect closure properties."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.sheafCohomology
    publicName := "sheaf cohomology"
    modulePath := "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic"
    checkedAnchor := "CategoryTheory.Sheaf.H; CategoryTheory.Sheaf.cohomologyFunctor"
    localWrapper := "sheafCohomologyTypeWrapper; sheafCohomologyFunctorWrapper"
    grrUse := "Candidate cohomological target infrastructure, not yet a Chow/GRR target."
    status := "checked_support_with_target_gap"
    nextGate := "Select whether GRR target is Chow, operational Chow, or sheaf/cohomological theory."
    repoLocalGRRClosed := false
  },
  {
    target := MathlibObjectModelTarget.derivedCategories
    publicName := "derived categories"
    modulePath := "Mathlib.Algebra.Homology.DerivedCategory.HomologySequence"
    checkedAnchor := "DerivedCategory; HasDerivedCategory; DerivedCategory.homologyFunctor"
    localWrapper := "derivedCategoryWrapper; derivedHomologyFunctorWrapper"
    grrUse := "Derived-category substrate for perfect complexes and derived pushforward candidates."
    status := "checked_support_with_target_gap"
    nextGate := "Import or define perfect complexes and derived pushforward compatible with the selected statement."
    repoLocalGRRClosed := false
  }
]

/-- The public object-model audit table covers the eight requested rows. -/
theorem mathlibObjectModelAuditTable_length : mathlibObjectModelAuditTable.length = 8 :=
  rfl

/-- The audit rows occur in the requested public order. -/
theorem mathlibObjectModelAuditTable_targets :
    mathlibObjectModelAuditTable.map MathlibObjectModelAuditRow.target =
      [ MathlibObjectModelTarget.scheme,
        MathlibObjectModelTarget.isProper,
        MathlibObjectModelTarget.schemeModules,
        MathlibObjectModelTarget.modulesPushforward,
        MathlibObjectModelTarget.modulesPullback,
        MathlibObjectModelTarget.quasiCoherentSheaves,
        MathlibObjectModelTarget.sheafCohomology,
        MathlibObjectModelTarget.derivedCategories ] :=
  rfl

/-- No object-model audit row is a claim that GRR is repo-locally closed. -/
theorem mathlibObjectModelAuditTable_no_repoLocalGRRClosed_claim :
    mathlibObjectModelAuditTable.map MathlibObjectModelAuditRow.repoLocalGRRClosed =
      [false, false, false, false, false, false, false, false] :=
  rfl

/-- The scheme object and morphism layer imported from mathlib for this slot. -/
def SchemeMorphismObjectLayer : Prop :=
  ∀ X Y : Scheme.{u}, Nonempty (X ⟶ Y) → True

/-- The noetherian source/target layer needed by the classical GRR statement. -/
def NoetherianHypothesisLayer : Prop :=
  ∀ X : Scheme.{u}, IsNoetherian X → IsLocallyNoetherian X

/-- The proper finite-presentation morphism layer used to state pushforwards. -/
def ProperFinitePresentationLayer : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y),
    IsProper f → LocallyOfFinitePresentation f → True

/-- Statement boundary for the functorial pushforward on K-theory/G-theory. -/
def KTheoryPushforwardLayer : Prop :=
  ∀ D : GrothendieckRiemannRochInput.{u}, D.kTheoryPushforwardDefined

/-- Statement boundary for the cycle or cohomology pushforward side. -/
def CyclePushforwardLayer : Prop :=
  ∀ D : GrothendieckRiemannRochInput.{u}, D.chowOrCohomologyPushforwardDefined

/-- Statement boundary for the Chern character used in GRR. -/
def ChernCharacterLayer : Prop :=
  ∀ D : GrothendieckRiemannRochInput.{u}, D.chernCharacterDefined

/-- Statement boundary for Todd classes and virtual tangent classes. -/
def ToddAndVirtualTangentLayer : Prop :=
  ∀ D : GrothendieckRiemannRochInput.{u},
    D.toddClassDefined ∧ D.virtualTangentClassDefined

/-- Statement boundary for the final GRR equality after all operations are available. -/
def RiemannRochIdentityLayer : Prop :=
  ∀ D : GrothendieckRiemannRochInput.{u}, D.grrIdentity

/-! ## Checked local wrappers around imported mathlib anchors -/

/-- Checked wrapper: the category of schemes has pullbacks in the current mathlib closure. -/
theorem scheme_has_pullbacks : HasPullbacks Scheme :=
  inferInstance

/-- Checked wrapper: every noetherian scheme is locally noetherian. -/
theorem noetherian_to_locally_noetherian (X : Scheme.{u}) [IsNoetherian X] :
    IsLocallyNoetherian X :=
  inferInstance

/-- Checked wrapper: every scheme has the chosen affine open cover supplied by mathlib. -/
noncomputable def affineOpenCoverWrapper (X : Scheme.{u}) : X.OpenCover :=
  X.affineCover

/-- Checked wrapper: the identity morphism is proper. -/
theorem identity_isProper (X : Scheme.{u}) : IsProper (𝟙 X) :=
  inferInstance

/-- Checked wrapper: the identity morphism is locally of finite presentation. -/
theorem identity_locallyOfFinitePresentation (X : Scheme.{u}) :
    LocallyOfFinitePresentation (𝟙 X) :=
  inferInstance

/-- Checked wrapper: the identity morphism is smooth. -/
theorem identity_smooth (X : Scheme.{u}) : Smooth (𝟙 X) :=
  inferInstance

/-! ## Checked local wrappers for the public object-model audit table -/

/-- Checked wrapper: `X.Modules` is an abelian category in the current mathlib closure. -/
@[reducible]
noncomputable def schemeModules_abelian (X : Scheme.{u}) : Abelian X.Modules :=
  inferInstance

/-- Checked wrapper: `X.Modules` has limits. -/
theorem schemeModules_hasLimits (X : Scheme.{u}) : HasLimits X.Modules :=
  inferInstance

/-- Checked wrapper: `X.Modules` has colimits. -/
theorem schemeModules_hasColimits (X : Scheme.{u}) : HasColimits X.Modules :=
  inferInstance

/-- Checked wrapper: mathlib's sheaf-module pushforward along a scheme morphism. -/
noncomputable def modulesPushforwardWrapper {X Y : Scheme.{u}} (f : X ⟶ Y) :
    X.Modules ⥤ Y.Modules :=
  Scheme.Modules.pushforward f

/-- Checked wrapper: mathlib's sheaf-module pullback along a scheme morphism. -/
noncomputable def modulesPullbackWrapper {X Y : Scheme.{u}} (f : X ⟶ Y) :
    Y.Modules ⥤ X.Modules :=
  Scheme.Modules.pullback f

/-- Checked wrapper: pullback is left adjoint to pushforward for scheme modules. -/
noncomputable def modulesPullbackPushforwardAdjunctionWrapper {X Y : Scheme.{u}} (f : X ⟶ Y) :
    Scheme.Modules.pullback f ⊣ Scheme.Modules.pushforward f :=
  Scheme.Modules.pullbackPushforwardAdjunction f

/-- Checked wrapper: affine tilde modules are quasi-coherent in the imported API. -/
theorem tilde_isQuasicoherent (R : CommRingCat.{u}) (M : ModuleCat.{u} R) :
    (tilde M).IsQuasicoherent :=
  inferInstance

/-- Checked wrapper: the sheaf cohomology type exposed by mathlib. -/
def sheafCohomologyTypeWrapper {C : Type u} [Category.{v} C]
    (J : GrothendieckTopology C) (F : Sheaf J AddCommGrpCat.{w})
    [HasSheafify J AddCommGrpCat.{w}] [HasExt.{w'} (Sheaf J AddCommGrpCat.{w})]
    (n : ℕ) : Type w' :=
  F.H n

/-- Checked wrapper: the sheaf cohomology functor exposed by mathlib. -/
noncomputable def sheafCohomologyFunctorWrapper {C : Type u} [Category.{v} C]
    (J : GrothendieckTopology C)
    [HasSheafify J AddCommGrpCat.{w}] [HasExt.{w'} (Sheaf J AddCommGrpCat.{w})]
    (n : ℕ) : Sheaf J AddCommGrpCat.{w} ⥤ AddCommGrpCat.{w'} :=
  CategoryTheory.Sheaf.cohomologyFunctor J n

/-- Checked wrapper: the derived category object exposed by mathlib. -/
def derivedCategoryWrapper (C : Type u) [Category.{v} C] [Abelian C]
    [HasDerivedCategory.{w} C] : Type (max u v) :=
  DerivedCategory C

/-- Checked wrapper: the homology functor on mathlib's derived category. -/
noncomputable def derivedHomologyFunctorWrapper (C : Type u) [Category.{v} C] [Abelian C]
    [HasDerivedCategory.{w} C] (n : ℤ) : DerivedCategory C ⥤ C :=
  DerivedCategory.homologyFunctor C n

/-- The statement-shape identity used by audit tooling. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ D : GrothendieckRiemannRochInput.{u},
        D.perfectOrCoherentInput →
          D.kTheoryPushforwardDefined →
            D.chowOrCohomologyPushforwardDefined →
              D.chernCharacterDefined →
                D.toddClassDefined →
                  D.virtualTangentClassDefined →
                    D.grrIdentity :=
  Iff.rfl

/-! ## Scheme/cohomology proof-package split -/

/--
One package in the M0387-level GRR proof frontier.

These are ledger rows, not proof assumptions.  A row can be listed here while
remaining open formalization debt.
-/
inductive GRRProofPackage where
  | schemeMorphismAndBaseChange
  | noetherianProperFinitePresentation
  | perfectComplexAndKTheory
  | cohomologyOrChowTarget
  | cohomologicalPushforward
  | chernCharacterToddClass
  | grrIdentityComparison
  | repoLocalClosureGate
  deriving DecidableEq, Repr

/--
Typed metadata for the GRR scheme/cohomology package split.

`repoLocalClosed` is intentionally `false` in every row: this file records the
next proof packages and their gates, but does not provide a terminal proof of
Grothendieck-Riemann-Roch.
-/
structure GRRProofPackageAudit where
  package : GRRProofPackage
  code : String
  title : String
  schemeLayer : String
  cohomologyLayer : String
  currentStatus : String
  nextGate : String
  leafBudgetStatus : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
M0387-level proof-package queue for `THM-M-0115`.

The split follows the public `GRR-PKG-01` through `GRR-PKG-08` shape and keeps
all non-imported proof obligations explicitly unchecked until a local proof
body, pinned mathlib theorem, or pinned external dependency is validated.
-/
def grrProofPackageLedger : List GRRProofPackageAudit := [
  {
    package := GRRProofPackage.schemeMorphismAndBaseChange
    code := "GRR-PKG-01"
    title := "scheme morphism, composition, pullback, and base-change object model"
    schemeLayer :=
      "Scheme objects, morphisms, composition, pullbacks, affine covers, and the chosen base scheme."
    cohomologyLayer :=
      "Only target-selection metadata; no cycle or sheaf-cohomology theorem is claimed in this package."
    currentStatus :=
      "partial_checked_support: Scheme, morphisms, pullbacks, and affine open covers are locally import-checkable."
    nextGate :=
      "Choose the canonical base-change square API used by the future GRR statement and audit exact theorem names."
    leafBudgetStatus :=
      "support rows are checked; terminal base-change proof leaves remain unchecked."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.noetherianProperFinitePresentation
    code := "GRR-PKG-02"
    title := "noetherian, proper, and finite-presentation morphism hypotheses"
    schemeLayer :=
      "Noetherian source/target schemes plus proper and locally finite-presentation morphisms."
    cohomologyLayer :=
      "These hypotheses are the finiteness substrate for K-theory, pushforward, and cohomology packages."
    currentStatus :=
      "partial_checked_support: IsNoetherian, IsLocallyNoetherian, IsProper, LocallyOfFinitePresentation, and Smooth wrappers validate locally."
    nextGate :=
      "Prove or import the exact hypothesis bridge required by the selected K-theory/cohomology target."
    leafBudgetStatus :=
      "support wrappers are checked; bridge leaves remain unchecked."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.perfectComplexAndKTheory
    code := "GRR-PKG-03"
    title := "perfect/coherent input object and K-theory or G-theory pushforward"
    schemeLayer :=
      "Perfect, coherent, or lci input over schemes, including the morphism hypotheses needed for f_!."
    cohomologyLayer :=
      "K_0 or G-theory object and proper pushforward on that object."
    currentStatus :=
      "formalization_debt: current repo-local dependency closure has no terminal scheme K-theory/G-theory GRR input package."
    nextGate :=
      "Define or import K_0/G-theory for the selected scheme class and validate the pushforward theorem."
    leafBudgetStatus :=
      "unchecked; split construction, functoriality, and pushforward into <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.cohomologyOrChowTarget
    code := "GRR-PKG-04"
    title := "Chow, operational Chow, or cohomological target with rational coefficients"
    schemeLayer :=
      "Target theory must be attached functorially to the source and target schemes."
    cohomologyLayer :=
      "Chow/cohomology groups or rings, rational coefficients, grading, multiplication, and functorial maps."
    currentStatus :=
      "formalization_debt: no repo-local Chow/cohomology target for the GRR equality has been closed."
    nextGate :=
      "Select Chow versus cohomology target, then pin/import/check its object model and ring structure."
    leafBudgetStatus :=
      "unchecked; object, coefficients, grading, and multiplication need separate leaves."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.cohomologicalPushforward
    code := "GRR-PKG-05"
    title := "proper pushforward on the Chow/cohomology target"
    schemeLayer :=
      "Proper morphism hypotheses must feed the target-side pushforward functor."
    cohomologyLayer :=
      "Target pushforward f_* and its compatibility with composition, identities, and products/projection formula inputs."
    currentStatus :=
      "formalization_debt: the selected target-side f_* has not been implemented or imported in this repo."
    nextGate :=
      "Validate pushforward identities and the projection-formula-style lemmas needed by Candidate A or B."
    leafBudgetStatus :=
      "unchecked; split functoriality, identity, composition, and projection formula branches."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.chernCharacterToddClass
    code := "GRR-PKG-06"
    title := "Chern character, Todd class, and virtual tangent/cotangent package"
    schemeLayer :=
      "Virtual tangent or relative cotangent complex data for the morphism or lci/perfect context."
    cohomologyLayer :=
      "Chern character from K-theory to the target theory and Todd class or Todd-twisted transformation."
    currentStatus :=
      "formalization_debt: Chern character, Todd class, and virtual tangent package are placeholder fields only."
    nextGate :=
      "Provide checked definitions and multiplicativity/naturality lemmas for the chosen target theory."
    leafBudgetStatus :=
      "unchecked; each characteristic-class law needs its own <=100-step ledger."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.grrIdentityComparison
    code := "GRR-PKG-07"
    title := "GRR identity and Candidate A/B comparison"
    schemeLayer :=
      "Connect the scheme-side morphism package to the exact hypotheses of the terminal GRR statement."
    cohomologyLayer :=
      "Prove the expanded ch times Td equality or the Todd-twisted naturality square, plus any equivalence between them."
    currentStatus :=
      "formalization_debt: CandidateAStatementShape and CandidateBStatementShape are statement boundaries, not proofs."
    nextGate :=
      "Choose a canonical target shape or prove a checked comparison theorem between the two shapes."
    leafBudgetStatus :=
      "unchecked; terminal identity branch exceeds a single leaf."
    repoLocalClosed := false
  },
  {
    package := GRRProofPackage.repoLocalClosureGate
    code := "GRR-PKG-08"
    title := "repo-local proof closure and public completion gate"
    schemeLayer :=
      "All scheme and morphism assumptions must be supplied by local proof bodies or pinned imports."
    cohomologyLayer :=
      "All K-theory, Chow/cohomology, Chern, Todd, pushforward, and identity theorems must validate in this repo."
    currentStatus :=
      "not_repo_local_closed: no terminal GRR proof body or pinned external dependency is validated here."
    nextGate :=
      "Run local Lean validation after local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned closure."
    leafBudgetStatus :=
      "gate leaf is open; no completion state is claimed."
    repoLocalClosed := false
  }
]

/-- The child pass records exactly eight GRR proof packages. -/
theorem grrProofPackageLedger_length : grrProofPackageLedger.length = 8 :=
  rfl

/-- No package in this ledger is claimed as repo-local theorem closure. -/
theorem grrProofPackageLedger_no_repoLocalClosed_claim :
    grrProofPackageLedger.map GRRProofPackageAudit.repoLocalClosed =
      [false, false, false, false, false, false, false, false] :=
  rfl

/-- The package codes are the public `GRR-PKG-01` through `GRR-PKG-08` queue. -/
theorem grrProofPackageLedger_codes :
    grrProofPackageLedger.map GRRProofPackageAudit.code =
      ["GRR-PKG-01", "GRR-PKG-02", "GRR-PKG-03", "GRR-PKG-04",
        "GRR-PKG-05", "GRR-PKG-06", "GRR-PKG-07", "GRR-PKG-08"] :=
  rfl

/-! ## Public theorem-tree split payload -/

/--
Public theorem-tree package names for the serial blueprint backfill.

This mirrors the integration-facing `GRR-PKG-01` through `GRR-PKG-08` split.
It is separate from the scheme/cohomology support ledger above because the
public tree must preserve the classical proof-process packages, including
local-computation and descent/gluing packages that are not locally closed here.
-/
inductive PublicGRRTheoremTreePackage where
  | statementNormalization
  | objectModelAndAnchorAudit
  | kTheoryPerfectComplex
  | chowCycleBivariantTarget
  | chernCharacterTodd
  | localComputationReduction
  | baseChangeDescentGluing
  | mainTheoremAssembly
  deriving DecidableEq, Repr

/--
One integration-ready public theorem-tree row.

`status` is deliberately a string so the public backfill text can retain the
literal `unchecked` status required by the Stage1/M0387 gate until the relevant
proof or process ledger is actually closed.
-/
structure PublicGRRTheoremTreeRow where
  package : PublicGRRTheoremTreePackage
  code : String
  title : String
  responsibility : String
  upstreamInputs : String
  downstreamOutput : String
  status : String
  leafBudgetGate : String
  repoLocalClosed : Bool
  deriving DecidableEq, Repr

/--
Integration-ready public theorem-tree split for `THM-M-0115`.

All rows remain `unchecked`.  The row data is safe to merge into the public
blueprint only as an open theorem tree, not as proof completion.
-/
def publicGRRTheoremTreeRows : List PublicGRRTheoremTreeRow := [
  {
    package := PublicGRRTheoremTreePackage.statementNormalization
    code := "GRR-PKG-01"
    title := "statement normalization and notation freeze"
    responsibility :=
      "Fix universe levels, scheme objects, morphism hypotheses, Candidate A/B shape, and notation for the terminal equality."
    upstreamInputs :=
      "CandidateAStatementShape, CandidateBStatementShape, and statementNormalizationMissingStructures."
    downstreamOutput :=
      "Canonical public statement target and missing-structure list for later proof packages."
    status := "unchecked"
    leafBudgetGate :=
      "Split universe/signature, hypothesis, and equality-target choices into <=100-step process leaves."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.objectModelAndAnchorAudit
    code := "GRR-PKG-02"
    title := "mathlib object model and imported-theorem audit"
    responsibility :=
      "Audit Scheme, IsProper, X.Modules, module pullback/pushforward, quasi-coherent sheaves, sheaf cohomology, derived categories, and external theorem anchors."
    upstreamInputs :=
      "mathlibObjectModelAuditTable, negativeLocalAnchorAuditTable, and externalLean4PrimarySourceAuditTable."
    downstreamOutput :=
      "Checked support anchors plus explicit formalization gaps for GRR-specific structures."
    status := "unchecked"
    leafBudgetGate :=
      "Keep support-anchor rows separate from terminal theorem anchors; no anchor-only completion."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.kTheoryPerfectComplex
    code := "GRR-PKG-03"
    title := "K-theory or perfect-complex layer"
    responsibility :=
      "Define or import K_0/G-theory or perfect-complex input objects and the proper pushforward f_!."
    upstreamInputs :=
      "Chosen scheme hypotheses from GRR-PKG-01 and support anchors from GRR-PKG-02."
    downstreamOutput :=
      "K-theory input, exact/additive relations, pushforward, and functoriality interface."
    status := "unchecked"
    leafBudgetGate :=
      "Construction, exactness/additivity, f_!, and functoriality each need <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.chowCycleBivariantTarget
    code := "GRR-PKG-04"
    title := "Chow, cycle, or bivariant target layer"
    responsibility :=
      "Define or import the target theory, coefficients, grading, multiplication, and proper pushforward target objects."
    upstreamInputs :=
      "Statement target selected in GRR-PKG-01 and object-model support from GRR-PKG-02."
    downstreamOutput :=
      "Target-side groups/rings or bivariant theory with functorial maps needed by Candidate A or B."
    status := "unchecked"
    leafBudgetGate :=
      "Object, rational coefficients, grading/multiplication, and pushforward leaves remain open."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.chernCharacterTodd
    code := "GRR-PKG-05"
    title := "Chern character and Todd class"
    responsibility :=
      "Define or import Chern character, Todd class or Todd-twisted transformation, and virtual tangent/cotangent data."
    upstreamInputs :=
      "K-theory interface from GRR-PKG-03 and target theory from GRR-PKG-04."
    downstreamOutput :=
      "Characteristic-class maps and multiplicativity/naturality laws needed for the GRR identity."
    status := "unchecked"
    leafBudgetGate :=
      "Definitions, additivity, multiplicativity, pullback compatibility, and Todd laws need separate leaves."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.localComputationReduction
    code := "GRR-PKG-06"
    title := "local computation, splitting, and deformation package"
    responsibility :=
      "Reduce the theorem to vector bundle, projective bundle, regular embedding, or deformation-to-normal-cone computations as required by the chosen proof route."
    upstreamInputs :=
      "Packages GRR-PKG-03 through GRR-PKG-05 plus the selected classical or bivariant proof route."
    downstreamOutput :=
      "Local computation theorems and reduction bridges feeding the global assembly."
    status := "unchecked"
    leafBudgetGate :=
      "Projective bundle/splitting, regular embedding, and deformation/excess-intersection branches remain open."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.baseChangeDescentGluing
    code := "GRR-PKG-07"
    title := "base change, descent, and gluing package"
    responsibility :=
      "Prove local-on-source/target stability, base-change compatibility, and descent/gluing for all selected structures."
    upstreamInputs :=
      "Scheme morphism support plus local computation interfaces from GRR-PKG-06."
    downstreamOutput :=
      "Globalization bridge that transports local GRR computations to the final theorem."
    status := "unchecked"
    leafBudgetGate :=
      "Locality, descent, gluing, and base-change compatibility need independent <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := PublicGRRTheoremTreePackage.mainTheoremAssembly
    code := "GRR-PKG-08"
    title := "main theorem assembly and repo-local closure gate"
    responsibility :=
      "Assemble the selected GRR statement, compare Candidate A/B if both remain, add the wrapper theorem, and run repo-local validation."
    upstreamInputs :=
      "Closed packages GRR-PKG-01 through GRR-PKG-07 or a pinned/imported upstream theorem satisfying the same interfaces."
    downstreamOutput :=
      "Terminal GRR theorem or checked wrapper/dependency closure plus public build-validation record."
    status := "unchecked"
    leafBudgetGate :=
      "Cannot close until local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned validation passes."
    repoLocalClosed := false
  }
]

/-- The public theorem-tree split contains exactly eight packages. -/
theorem publicGRRTheoremTreeRows_length : publicGRRTheoremTreeRows.length = 8 :=
  rfl

/-- The public theorem-tree package codes are `GRR-PKG-01` through `GRR-PKG-08`. -/
theorem publicGRRTheoremTreeRows_codes :
    publicGRRTheoremTreeRows.map PublicGRRTheoremTreeRow.code =
      ["GRR-PKG-01", "GRR-PKG-02", "GRR-PKG-03", "GRR-PKG-04",
        "GRR-PKG-05", "GRR-PKG-06", "GRR-PKG-07", "GRR-PKG-08"] :=
  rfl

/-- Every public theorem-tree row deliberately preserves the `unchecked` status. -/
theorem publicGRRTheoremTreeRows_statuses_unchecked :
    publicGRRTheoremTreeRows.map PublicGRRTheoremTreeRow.status =
      ["unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked"] :=
  rfl

/-- No public theorem-tree row is a repo-local completion claim. -/
theorem publicGRRTheoremTreeRows_no_repoLocalClosed_claim :
    publicGRRTheoremTreeRows.map PublicGRRTheoremTreeRow.repoLocalClosed =
      [false, false, false, false, false, false, false, false] :=
  rfl

/-! ## Audit constants retained for Stage1 repair bookkeeping -/

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Noetherian",
  "Mathlib.AlgebraicGeometry.Pullbacks",
  "Mathlib.AlgebraicGeometry.Cover.Open",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.AlgebraicGeometry.Modules.Tilde",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
  "Mathlib.Algebra.Homology.DerivedCategory.HomologySequence"
]

/-- Pinned theorem or definition names used by this local artifact. -/
def repoLocalAnchorNames : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.Scheme.OpenCover",
  "AlgebraicGeometry.Scheme.affineCover",
  "AlgebraicGeometry.IsNoetherian",
  "AlgebraicGeometry.IsLocallyNoetherian",
  "AlgebraicGeometry.IsProper",
  "AlgebraicGeometry.LocallyOfFinitePresentation",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.Scheme.Modules",
  "AlgebraicGeometry.Scheme.Modules.pushforward",
  "AlgebraicGeometry.Scheme.Modules.pullback",
  "AlgebraicGeometry.Scheme.Modules.pullbackPushforwardAdjunction",
  "AlgebraicGeometry.tilde",
  "SheafOfModules.IsQuasicoherent",
  "CategoryTheory.Sheaf.H",
  "CategoryTheory.Sheaf.cohomologyFunctor",
  "DerivedCategory",
  "DerivedCategory.homologyFunctor",
  "CategoryTheory.Limits.HasPullbacks"
]

/-- Search terms used in the pinned local mathlib tree for the GRR anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "Grothendieck-Riemann-Roch",
  "Riemann Roch",
  "Chow",
  "KTheory",
  "Chern character",
  "Todd class",
  "Euler characteristic",
  "derived pushforward"
]

/-! ## Negative local-anchor audit for GRR-specific names -/

/-- The pinned mathlib revision used for the negative local-anchor audit. -/
def mathlibNegativeAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- GRR-specific theorem-family names that were searched in the local closure. -/
inductive NegativeAnchorTarget where
  | grothendieckRiemannRoch
  | schemeKTheory
  | chowTheory
  | chernCharacter
  | toddClass
  deriving DecidableEq, Repr

/- One row of the local negative-anchor audit.

The row records a source-tree/name audit, not a logical nonexistence theorem.
It is intentionally separate from the checked positive object-model wrappers
above because absence of a local declaration is a planning datum, not a proof
of Grothendieck-Riemann-Roch.
-/
structure NegativeAnchorAuditRow where
  target : NegativeAnchorTarget
  mathlibRevision : String
  searchedScope : String
  searchTerms : List String
  observedLocalNames : List String
  diagnosis : String
  status : String
  nextGate : String
  repoLocalGRRClosed : Bool
  deriving DecidableEq, Repr

/- Integration-ready negative-anchor rows for the public backfill.

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, local source
searches for declaration/name anchors in mathlib's algebraic-geometry,
homological-algebra, and category-theory tree did not locate terminal GRR,
scheme K-theory, Chow, Chern-character, or Todd-class names.  A broader
whole-mathlib text search has unrelated prose or author-name hits; those are
not usable theorem anchors for this Stage1 slot.
-/
def negativeLocalAnchorAuditTable : List NegativeAnchorAuditRow := [
  {
    target := NegativeAnchorTarget.grothendieckRiemannRoch
    mathlibRevision := mathlibNegativeAnchorRevision
    searchedScope :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib at the pinned Lake revision"
    searchTerms := [
      "Grothendieck-Riemann-Roch",
      "GrothendieckRiemannRoch",
      "RiemannRoch",
      "Riemann Roch"
    ]
    observedLocalNames := []
    diagnosis :=
      "No local mathlib declaration name or terminal theorem anchor for Grothendieck-Riemann-Roch was found."
    status := "negative_anchor; formalization_debt"
    nextGate :=
      "Do not mark completed; choose a wrapper target or pin/import/check an external GRR theorem if one is found."
    repoLocalGRRClosed := false
  },
  {
    target := NegativeAnchorTarget.schemeKTheory
    mathlibRevision := mathlibNegativeAnchorRevision
    searchedScope :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib at the pinned Lake revision"
    searchTerms := [
      "KTheory",
      "K-theory",
      "G-theory",
      "K_0"
    ]
    observedLocalNames := []
    diagnosis :=
      "No local scheme K-theory/G-theory declaration family or proper K-theory pushforward anchor was found."
    status := "negative_anchor; formalization_debt"
    nextGate :=
      "Define or import the selected K_0/G-theory object and f_! pushforward before using Candidate A or B."
    repoLocalGRRClosed := false
  },
  {
    target := NegativeAnchorTarget.chowTheory
    mathlibRevision := mathlibNegativeAnchorRevision
    searchedScope :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicGeometry plus homological/category-theory support"
    searchTerms := [
      "Chow",
      "OperationalChow",
      "ChowGroup",
      "ChowRing"
    ]
    observedLocalNames := []
    diagnosis :=
      "No local Chow/operational-Chow group or ring declaration anchor suitable as a GRR target was found."
    status := "negative_anchor; formalization_debt"
    nextGate :=
      "Select Chow, operational Chow, or another cohomological target and validate its coefficients, grading, products, and pushforward."
    repoLocalGRRClosed := false
  },
  {
    target := NegativeAnchorTarget.chernCharacter
    mathlibRevision := mathlibNegativeAnchorRevision
    searchedScope :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib at the pinned Lake revision"
    searchTerms := [
      "Chern",
      "chernCharacter",
      "ChernCharacter",
      "ch"
    ]
    observedLocalNames := []
    diagnosis :=
      "No local Chern-character declaration anchor from K-theory/perfect complexes to a GRR target was found."
    status := "negative_anchor; formalization_debt"
    nextGate :=
      "Import or define the Chern character and its functorial/multiplicative laws for the selected target theory."
    repoLocalGRRClosed := false
  },
  {
    target := NegativeAnchorTarget.toddClass
    mathlibRevision := mathlibNegativeAnchorRevision
    searchedScope :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib at the pinned Lake revision"
    searchTerms := [
      "Todd",
      "ToddClass",
      "toddClass",
      "Todd class"
    ]
    observedLocalNames := []
    diagnosis :=
      "No local Todd-class or Todd-twisted-transformation declaration anchor usable for GRR was found."
    status := "negative_anchor; formalization_debt"
    nextGate :=
      "Import or define Todd classes, virtual tangent/cotangent inputs, and the Todd-twisted naturality laws."
    repoLocalGRRClosed := false
  }
]

/-- The negative-anchor audit records exactly the five requested GRR-specific rows. -/
theorem negativeLocalAnchorAuditTable_length : negativeLocalAnchorAuditTable.length = 5 :=
  rfl

/-- The negative-anchor rows occur in the requested public order. -/
theorem negativeLocalAnchorAuditTable_targets :
    negativeLocalAnchorAuditTable.map NegativeAnchorAuditRow.target =
      [ NegativeAnchorTarget.grothendieckRiemannRoch,
        NegativeAnchorTarget.schemeKTheory,
        NegativeAnchorTarget.chowTheory,
        NegativeAnchorTarget.chernCharacter,
        NegativeAnchorTarget.toddClass ] :=
  rfl

/-- No negative-anchor row is a claim that GRR is repo-locally closed. -/
theorem negativeLocalAnchorAuditTable_no_repoLocalGRRClosed_claim :
    negativeLocalAnchorAuditTable.map NegativeAnchorAuditRow.repoLocalGRRClosed =
      [false, false, false, false, false] :=
  rfl

/-- Machine proof debt classification for this Stage1 slot. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration-debt gate for this repair pass.

No complete Lean 4 GRR proof was found in the current Lake dependency closure.
This artifact is therefore not a completed wrapper and carries no completed
state with repo-local integration debt.
-/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no completed state retains repo_local_integration_debt"

/-! ## External Lean 4 source audit payload -/

/-- One primary-source external Lean 4 audit row for this GRR slot. -/
structure ExternalLean4AuditRow where
  sourceKind : String
  repositoryUrl : String
  commitOrRevision : String
  moduleOrFile : String
  theoremNames : List String
  auditMethod : String
  diagnosis : String
  integrationStatus : String
  repoLocalGRRClosed : Bool
  deriving DecidableEq, Repr

/-- Date of the external Lean 4 audit performed for child `S1-M-023-C005`. -/
def externalLean4AuditDate : String :=
  "2026-05-01"

/--
Authenticated GitHub search status for the child audit.

The local `gh` client was installed but not logged in.  GitHub web code search
required sign-in for code results, and unauthenticated REST code search was
rate-limited.  This blocks a global absence claim, but it does not create a
positive external theorem anchor.
-/
def authenticatedGitHubAuditStatus : String :=
  "blocked: gh auth status reported no logged-in GitHub host; GitHub web code search required sign-in; unauthenticated REST code search was rate-limited"

/--
External Lean 4 source audit rows for `THM-M-0115`.

The only source-level Lean theorem hit found in this child pass was a different
Riemann-Roch theorem for finite graphs.  It is recorded exactly as a false
positive so that integrators do not treat it as a GRR anchor.
-/
def externalLean4PrimarySourceAuditTable : List ExternalLean4AuditRow := [
  {
    sourceKind := "local pinned dependency"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4"
    commitOrRevision := mathlibNegativeAnchorRevision
    moduleOrFile :=
      "Formalizations/Lean/.lake/packages/mathlib/Mathlib plus import-check probes in this file"
    theoremNames := []
    auditMethod :=
      "repo-local source search and Lean import checks against the pinned Lake dependency closure"
    diagnosis :=
      "No terminal Grothendieck-Riemann-Roch theorem, scheme K-theory/G-theory pushforward, Chow target, Chern character, or Todd class anchor was found in the local mathlib closure."
    integrationStatus :=
      "formalization_debt; no external_upstream_anchor_only completion claim"
    repoLocalGRRClosed := false
  },
  {
    sourceKind := "external related false positive"
    repositoryUrl := "https://github.com/DhyeyMavani2003/chip-firing-with-lean"
    commitOrRevision := "b624c3fe19a63ad3cf46c15a243da107234016d2"
    moduleOrFile := "ChipFiringWithLean/RiemannRochForGraphs.lean"
    theoremNames := [
      "riemann_roch_for_graphs",
      "maximal_unwinnable_symmetry",
      "clifford_theorem",
      "riemann_roch_deg_to_rank_corollary"
    ]
    auditMethod :=
      "GitHub repository search result plus raw source inspection at the recorded commit"
    diagnosis :=
      "This project formalizes Baker-Norine Riemann-Roch for finite graphs, not Grothendieck-Riemann-Roch for schemes; it is not a theorem anchor for THM-M-0115."
    integrationStatus :=
      "rejected_false_positive; no repo_local_integration_debt for GRR"
    repoLocalGRRClosed := false
  },
  {
    sourceKind := "authenticated GitHub code-search gate"
    repositoryUrl :=
      "https://github.com/search?q=%22Grothendieck-Riemann-Roch%22+language%3ALean&type=code"
    commitOrRevision := "not_applicable"
    moduleOrFile := "GitHub code search"
    theoremNames := []
    auditMethod :=
      "gh auth status; GitHub web code-search page; GitHub REST code-search attempts"
    diagnosis :=
      "Authenticated GitHub code search was unavailable in this environment, so this child cannot certify global absence of external Lean 4 GRR sources."
    integrationStatus :=
      "open_access_blocker_for_global_absence_claim; keep Stage1 slot unchecked"
    repoLocalGRRClosed := false
  }
]

/-- The external audit records local mathlib, one false positive, and the auth gate. -/
theorem externalLean4PrimarySourceAuditTable_length :
    externalLean4PrimarySourceAuditTable.length = 3 :=
  rfl

/-- No external audit row is a repo-local GRR closure claim. -/
theorem externalLean4PrimarySourceAuditTable_no_repoLocalGRRClosed_claim :
    externalLean4PrimarySourceAuditTable.map ExternalLean4AuditRow.repoLocalGRRClosed =
      [false, false, false] :=
  rfl

/-! ## First public Lean target decision -/

/--
Available routes for the first public Lean target of `THM-M-0115`.

This is a route-selection audit, not a proof of Grothendieck-Riemann-Roch.
-/
inductive FirstPublicLeanTarget where
  | weakImportCheckableWrapper
  | realImportedExternalTheorem
  deriving DecidableEq, Repr

/--
Child `S1-M-023-C006` decision.

The first public Lean target should be a weak import-checkable wrapper around
the repo-local scheme/sheaf/cohomology object model, not a real imported GRR
theorem.  The reason is that the current local closure has no terminal GRR
anchor, and the external audit has not produced a primary-source Lean 4 GRR
project with repository URL, commit, module path, theorem name, and Lake
integration feasibility.
-/
def firstPublicLeanTargetDecision : FirstPublicLeanTarget :=
  FirstPublicLeanTarget.weakImportCheckableWrapper

/-- Machine-readable diagnosis attached to the first-target route decision. -/
def firstPublicLeanTargetDecisionDiagnosis : String :=
  "choose weak import-checkable wrapper; no real imported external GRR theorem is currently pin/import/check ready"

/-- Integration blocker for the real-imported-theorem route. -/
def realImportedExternalGRRTheoremBlocker : String :=
  "blocked until primary-source audit finds a Lean 4 GRR theorem and the repo pins/imports/checks it or records a concrete incompatibility"

/-- The selected first target is the weak wrapper route. -/
theorem firstPublicLeanTargetDecision_is_weak_wrapper :
    firstPublicLeanTargetDecision = FirstPublicLeanTarget.weakImportCheckableWrapper :=
  rfl

/-- The selected first target is not a real imported external theorem. -/
theorem firstPublicLeanTargetDecision_not_real_imported_theorem :
    firstPublicLeanTargetDecision ≠ FirstPublicLeanTarget.realImportedExternalTheorem := by
  decide

/-! ## Build-validation record for child `S1-M-023-C008` -/

/--
Repo-local build-validation record for the selected weak wrapper target.

This is a record of the local command that checked the wrapper/dependency
closure.  It is not a proof of Grothendieck-Riemann-Roch and does not close the
formalization-debt packages above.
-/
structure BuildValidationRecord where
  childId : String
  validationDate : String
  workingDirectory : String
  command : String
  checkedTarget : String
  result : String
  validatesTerminalGRR : Bool
  repoLocalGRRClosed : Bool
  repoLocalIntegrationDebtGate : String
  deriving DecidableEq, Repr

/--
Build-validation record added only after
`cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_023.lean`
completed with exit code 0 on 2026-05-01.
-/
def childC008BuildValidationRecord : BuildValidationRecord := {
  childId := "S1-M-023-C008"
  validationDate := "2026-05-01"
  workingDirectory := "Formalizations/Lean"
  command := "lake env lean AwesomeTheorems/Stage1/S1_M_023.lean"
  checkedTarget :=
    "weak import-checkable wrapper and dependency closure for S1_M_023"
  result := "passed with exit code 0"
  validatesTerminalGRR := false
  repoLocalGRRClosed := false
  repoLocalIntegrationDebtGate :=
    "no completed state; no repo_local_integration_debt retained as completion"
}

/-- The build-validation record is not a terminal GRR proof-completion claim. -/
theorem childC008BuildValidationRecord_not_terminal_GRR :
    childC008BuildValidationRecord.validatesTerminalGRR = false ∧
      childC008BuildValidationRecord.repoLocalGRRClosed = false :=
  ⟨rfl, rfl⟩

#check Scheme
#check Scheme.OpenCover
#check Scheme.affineCover
#check IsNoetherian
#check IsLocallyNoetherian
#check IsProper
#check LocallyOfFinitePresentation
#check Smooth
#check HasPullbacks Scheme
#check GrothendieckRiemannRochInput
#check StatementShape
#check CandidateAFormulaInput
#check CandidateAStatementShape
#check CandidateBNaturalityInput
#check CandidateBStatementShape
#check statementNormalizationMissingStructures
#check MathlibObjectModelTarget
#check MathlibObjectModelAuditRow
#check mathlibObjectModelAuditTable
#check mathlibObjectModelAuditTable_length
#check mathlibObjectModelAuditTable_targets
#check mathlibObjectModelAuditTable_no_repoLocalGRRClosed_claim
#check GRRProofPackage
#check GRRProofPackageAudit
#check grrProofPackageLedger
#check grrProofPackageLedger_length
#check grrProofPackageLedger_no_repoLocalClosed_claim
#check grrProofPackageLedger_codes
#check PublicGRRTheoremTreePackage
#check PublicGRRTheoremTreeRow
#check publicGRRTheoremTreeRows
#check publicGRRTheoremTreeRows_length
#check publicGRRTheoremTreeRows_codes
#check publicGRRTheoremTreeRows_statuses_unchecked
#check publicGRRTheoremTreeRows_no_repoLocalClosed_claim
#check mathlibNegativeAnchorRevision
#check NegativeAnchorTarget
#check NegativeAnchorAuditRow
#check negativeLocalAnchorAuditTable
#check negativeLocalAnchorAuditTable_length
#check negativeLocalAnchorAuditTable_targets
#check negativeLocalAnchorAuditTable_no_repoLocalGRRClosed_claim
#check ExternalLean4AuditRow
#check externalLean4AuditDate
#check authenticatedGitHubAuditStatus
#check externalLean4PrimarySourceAuditTable
#check externalLean4PrimarySourceAuditTable_length
#check externalLean4PrimarySourceAuditTable_no_repoLocalGRRClosed_claim
#check FirstPublicLeanTarget
#check firstPublicLeanTargetDecision
#check firstPublicLeanTargetDecisionDiagnosis
#check realImportedExternalGRRTheoremBlocker
#check firstPublicLeanTargetDecision_is_weak_wrapper
#check firstPublicLeanTargetDecision_not_real_imported_theorem
#check BuildValidationRecord
#check childC008BuildValidationRecord
#check childC008BuildValidationRecord_not_terminal_GRR
#check scheme_has_pullbacks
#check noetherian_to_locally_noetherian
#check affineOpenCoverWrapper
#check identity_isProper
#check identity_locallyOfFinitePresentation
#check identity_smooth
#check schemeModules_abelian
#check schemeModules_hasLimits
#check schemeModules_hasColimits
#check modulesPushforwardWrapper
#check modulesPullbackWrapper
#check modulesPullbackPushforwardAdjunctionWrapper
#check tilde_isQuasicoherent
#check sheafCohomologyTypeWrapper
#check sheafCohomologyFunctorWrapper
#check derivedCategoryWrapper
#check derivedHomologyFunctorWrapper

end S1_M_023
end Stage1
end AwesomeTheorems
