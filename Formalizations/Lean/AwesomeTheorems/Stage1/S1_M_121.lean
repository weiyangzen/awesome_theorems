import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.Algebra.Category.ModuleCat.Sheaf.Quasicoherent
import Mathlib.Algebra.Homology.EulerCharacteristic

/-!
# S1-M-121 / THM-M-0177: Grothendieck-Riemann-Roch

This Stage1 file records a conservative Lean 4 statement-shape boundary for
Grothendieck-Riemann-Roch for a proper morphism of schemes.

The pinned mathlib snapshot
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has useful scheme-morphism
infrastructure (`Scheme`, `IsProper`, `Smooth`, sheaves of modules,
quasicoherence, and Euler characteristics of homological complexes).  This audit
did not find a terminal Grothendieck-Riemann-Roch theorem, nor the K-theory,
Chow-ring, Chern-character, Todd-class, derived pushforward, and cycle
pushforward APIs required to state the classical theorem concretely.

The declarations below therefore avoid proof placeholders and false completion
claims.  They normalize the morphism-side hypotheses using existing mathlib
objects, keep the characteristic-class side as explicit future data, and include
only small checked wrappers around available mathlib facts.
-/

noncomputable section

open CategoryTheory
open AlgebraicGeometry

universe w v u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_121

/--
Geometric input for a Grothendieck-Riemann-Roch statement.

The classical statement has variants for proper morphisms with regularity,
smoothness, finite Tor dimension, or quasi-projectivity hypotheses depending on
the chosen K-theory/Chow-theory formulation.  The fields below pin the part that
is currently concrete in mathlib (`Scheme`, morphisms, `IsProper`, `Smooth`) and
leave the remaining algebro-geometric finiteness/regularity requirements as
explicit propositions until the corresponding APIs are selected.
-/
structure GRRInput : Type (u + 1) where
  source : Scheme.{u}
  target : Scheme.{u}
  morphism : source ⟶ target
  proper : IsProper morphism
  smooth : Smooth morphism
  sourceRegular : Prop
  targetRegular : Prop
  finiteTorDimension : Prop
  quasiProjectiveOrFiniteType : Prop
  sourceRegular_holds : sourceRegular
  targetRegular_holds : targetRegular
  finiteTorDimension_holds : finiteTorDimension
  quasiProjectiveOrFiniteType_holds : quasiProjectiveOrFiniteType

/--
Future characteristic-class and pushforward data needed to state GRR.

`KTheory`, `ChowTheory`, `chernCharacter`, `toddClass`, and the two pushforward
maps are intentionally parameters.  The current local mathlib snapshot does not
provide a concrete K_0/Chow-ring/Chern-character/Todd-class object model for
schemes, so a terminal proof must replace this structure by imported concrete
APIs or by a pinned upstream theorem.
-/
structure GRRFormalData (I : GRRInput.{u}) : Type (max (u + 1) (v + 1) (w + 1)) where
  KTheory : Scheme.{u} → Type v
  ChowTheory : Scheme.{u} → Type w
  cycleMul : ∀ Z : Scheme.{u}, ChowTheory Z → ChowTheory Z → ChowTheory Z
  kPushforward : KTheory I.source → KTheory I.target
  cyclePushforward : ChowTheory I.source → ChowTheory I.target
  chernCharacter : ∀ Z : Scheme.{u}, KTheory Z → ChowTheory Z
  toddClass : ∀ Z : Scheme.{u}, ChowTheory Z

/--
Normalized Stage1 statement shape for Grothendieck-Riemann-Roch.

For a proper smooth morphism `f : X ⟶ Y`, and for every K-theory class `α` on
`X`, the Chern character of the K-theoretic pushforward, multiplied by the Todd
class of `Y`, equals the cycle-theoretic pushforward of the Chern character of
`α` multiplied by the Todd class of `X`.

This is only a statement shape: the operations in `GRRFormalData` are abstract
because the current local mathlib snapshot does not expose the terminal GRR
object model.
-/
def StatementShape (I : GRRInput.{u}) (D : GRRFormalData.{w, v, u} I) : Prop :=
  ∀ α : D.KTheory I.source,
    D.cycleMul I.target (D.chernCharacter I.target (D.kPushforward α)) (D.toddClass I.target) =
      D.cyclePushforward
        (D.cycleMul I.source (D.chernCharacter I.source α) (D.toddClass I.source))

/--
Terminal package expected from a full GRR formalization.

The proposition fields are separated from the identity so a later integrator can
replace them with concrete naturality, projection-formula, and compatibility
lemmas rather than treating the abstract statement shape as a completed theorem.
-/
structure GRRPackage (I : GRRInput.{u}) : Type (max (u + 1) (v + 1) (w + 1)) where
  data : GRRFormalData.{w, v, u} I
  grr_identity : StatementShape I data
  compatibleWithComposition : Prop
  compatibleWithBaseChange : Prop
  compatibleWithProjectionFormula : Prop
  compatibleWithComposition_holds : compatibleWithComposition
  compatibleWithBaseChange_holds : compatibleWithBaseChange
  compatibleWithProjectionFormula_holds : compatibleWithProjectionFormula

/-- The statement-shape definition unfolds to the normalized GRR identity. -/
theorem statementShape_iff (I : GRRInput.{u}) (D : GRRFormalData.{w, v, u} I) :
    StatementShape I D ↔
      ∀ α : D.KTheory I.source,
        D.cycleMul I.target (D.chernCharacter I.target (D.kPushforward α))
            (D.toddClass I.target) =
          D.cyclePushforward
            (D.cycleMul I.source (D.chernCharacter I.source α) (D.toddClass I.source)) :=
  Iff.rfl

/-!
## Public statement-normalization boundary

`AwesomeTheorems.Stage1.S1_M_121.StatementShape` is the current repo-local Lean
statement boundary for the Stage1 Grothendieck-Riemann-Roch slot.  It normalizes
the expected GRR identity only relative to abstract `GRRInput` and
`GRRFormalData` packages.

This boundary is not a terminal Grothendieck-Riemann-Roch theorem: a completed
formalization still needs concrete K-theory, Chow/cohomology, Chern-character,
Todd-class, proper-pushforward, cycle-pushforward, projection-formula, and
compatibility APIs, or a pinned/imported external Lean proof supplying them.
-/

/--
Integration-ready public statement-normalization note for `THM-M-0177.statement`.

This string is checked by Lean as repo-local metadata.  It is intended for a
serial public-doc integrator to copy into the Stage1 blueprint/todo surfaces
without upgrading the parent theorem to completed.
-/
def statementShapeNormalizationNote : String :=
  "THM-M-0177.statement: AwesomeTheorems.Stage1.S1_M_121.StatementShape is the current repo-local Lean statement boundary for Grothendieck-Riemann-Roch. It states the GRR identity only relative to an abstract GRRInput and GRRFormalData package for K-theory, Chow/cycle theory, Chern character, Todd class, and pushforwards. This is not a terminal Grothendieck-Riemann-Roch theorem: the concrete K-theory, Chow/cohomology, Chern-character, Todd-class, derived/proper pushforward, cycle-pushforward, projection-formula, base-change, and composition-compatibility APIs remain unformalized or unintegrated for this repo-local slot."

/-- Declarations that define the checked local statement-normalization surface. -/
def statementShapeNormalizationDeclarations : List String := [
  "AwesomeTheorems.Stage1.S1_M_121.GRRInput",
  "AwesomeTheorems.Stage1.S1_M_121.GRRFormalData",
  "AwesomeTheorems.Stage1.S1_M_121.StatementShape",
  "AwesomeTheorems.Stage1.S1_M_121.statementShape_iff",
  "AwesomeTheorems.Stage1.S1_M_121.statementShapeNormalizationNote"
]

/-- Checked wrapper: proper morphisms of schemes are closed under composition. -/
theorem isProper_comp {X Y Z : Scheme.{u}} (f : X ⟶ Y) (g : Y ⟶ Z)
    [IsProper f] [IsProper g] :
    IsProper (f ≫ g) := by
  infer_instance

/-- Checked wrapper: smooth morphisms of schemes are closed under composition. -/
theorem smooth_comp {X Y Z : Scheme.{u}} (f : X ⟶ Y) (g : Y ⟶ Z)
    [Smooth f] [Smooth g] :
    Smooth (f ≫ g) := by
  infer_instance

/-- Checked wrapper: finite morphisms are proper in the current mathlib API. -/
theorem isProper_of_isFinite {X Y : Scheme.{u}} (f : X ⟶ Y) [IsFinite f] :
    IsProper f := by
  infer_instance

/--
Checked wrapper around mathlib's cancellation criterion for composition with a
proper target morphism.
-/
theorem isProper_comp_iff_of_proper_target {X Y Z : Scheme.{u}}
    {f : X ⟶ Y} {g : Y ⟶ Z} [IsProper g] :
    IsProper (f ≫ g) ↔ IsProper f :=
  IsProper.comp_iff

/-- Pinned mathlib revision audited for this Stage1 slot. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper",
  "Mathlib.Algebra.Category.ModuleCat.Sheaf.Quasicoherent",
  "Mathlib.Algebra.Category.ModuleCat.Sheaf.PullbackFree",
  "Mathlib.Algebra.Homology.EulerCharacteristic",
  "Mathlib.Algebra.Homology.DerivedCategory.Basic",
  "Mathlib.CategoryTheory.Sites.SheafCohomology.Cech",
  "Mathlib.AlgebraicGeometry.Sites.ElladicCohomology"
]

/--
Integration-ready public mathlib-audit note for `THM-M-0177.mathlib-audit`.

The named modules are available in the pinned local mathlib source tree.  The
imports at the top of this file keep the repo-local wrappers lightweight; this
metadata records the broader audit surface without treating those anchors as a
terminal Grothendieck-Riemann-Roch proof.
-/
def mathlibAuditNote : String :=
  "THM-M-0177.mathlib-audit: at pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95, the local mathlib source tree contains Mathlib.AlgebraicGeometry.Scheme, Mathlib.AlgebraicGeometry.Morphisms.Proper, Mathlib.AlgebraicGeometry.Morphisms.Smooth, Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper, Mathlib.Algebra.Category.ModuleCat.Sheaf.Quasicoherent, Mathlib.Algebra.Category.ModuleCat.Sheaf.PullbackFree, Mathlib.Algebra.Homology.EulerCharacteristic, Mathlib.Algebra.Homology.DerivedCategory.Basic, Mathlib.CategoryTheory.Sites.SheafCohomology.Cech, and Mathlib.AlgebraicGeometry.Sites.ElladicCohomology. These modules provide useful scheme, morphism, sheaf, homology, derived-category, Cech, and ell-adic cohomology anchors, but they do not by themselves close a terminal Grothendieck-Riemann-Roch theorem in this repository."

/--
Coherent list of formal API leaves still missing before the abstract
`StatementShape` can be replaced by a concrete Grothendieck-Riemann-Roch theorem.
-/
inductive GRRMissingAPI where
  | coherentAlgebraicKTheory
  | kTheoreticProperPushforward
  | chowCohomologyTarget
  | cyclePushforward
  | chernCharacter
  | toddClass
  | derivedPushforwardEulerCharacteristic
  | projectionFormula
  | baseChangeCompositionCompatibility
  deriving DecidableEq, Repr

/-- Stable public label for each missing GRR API leaf. -/
def GRRMissingAPI.label : GRRMissingAPI → String
  | coherentAlgebraicKTheory => "coherent/algebraic K-theory"
  | kTheoreticProperPushforward => "K-theoretic proper pushforward"
  | chowCohomologyTarget => "Chow/cohomology target"
  | cyclePushforward => "cycle pushforward"
  | chernCharacter => "Chern character"
  | toddClass => "Todd class"
  | derivedPushforwardEulerCharacteristic => "derived pushforward/Euler characteristic"
  | projectionFormula => "projection formula"
  | baseChangeCompositionCompatibility => "base-change/composition compatibility"

/-- Concrete integration blocker attached to each missing GRR API leaf. -/
def GRRMissingAPI.integrationBlocker : GRRMissingAPI → String
  | coherentAlgebraicKTheory =>
      "No repo-local concrete K_0 or coherent/algebraic K-theory object for schemes is available."
  | kTheoreticProperPushforward =>
      "No repo-local proper pushforward on the chosen K-theory object is available."
  | chowCohomologyTarget =>
      "No repo-local Chow ring, cycle group, or replacement cohomology target with GRR operations is available."
  | cyclePushforward =>
      "No repo-local proper pushforward on the Chow/cycle/cohomology target is available."
  | chernCharacter =>
      "No repo-local Chern character from the chosen K-theory object to the Chow/cohomology target is available."
  | toddClass =>
      "No repo-local Todd class for the tangent or relative tangent data required by GRR is available."
  | derivedPushforwardEulerCharacteristic =>
      "No repo-local bridge from derived pushforward or Euler characteristic to the K-theory pushforward is available."
  | projectionFormula =>
      "No repo-local projection-formula lemma tying multiplication and proper pushforward to the GRR identity is available."
  | baseChangeCompositionCompatibility =>
      "No repo-local base-change and composition compatibility package for the GRR pushforwards and characteristic classes is available."

/-- Checked Stage1 split for `THM-M-0177.missing-api`. -/
def missingAPISplit : List GRRMissingAPI := [
  .coherentAlgebraicKTheory,
  .kTheoreticProperPushforward,
  .chowCohomologyTarget,
  .cyclePushforward,
  .chernCharacter,
  .toddClass,
  .derivedPushforwardEulerCharacteristic,
  .projectionFormula,
  .baseChangeCompositionCompatibility
]

/-- Human-readable checked metadata for the missing GRR API leaves. -/
def missingAPISplitTable : List (String × String) :=
  missingAPISplit.map fun api => (api.label, api.integrationBlocker)

/-- The requested missing-API split has nine leaves. -/
theorem missingAPISplit_length : missingAPISplit.length = 9 :=
  rfl

/--
Integration-ready public missing-API note for `THM-M-0177.missing-api`.

This is checked metadata only.  It records formalization blockers and does not
turn the abstract `StatementShape` into a terminal GRR theorem.
-/
def missingAPISplitNote : String :=
  "THM-M-0177.missing-api: the missing formal API surface is split into nine repo-local leaves: coherent/algebraic K-theory; K-theoretic proper pushforward; Chow/cohomology target; cycle pushforward; Chern character; Todd class; derived pushforward/Euler characteristic; projection formula; and base-change/composition compatibility. These leaves are recorded in AwesomeTheorems.Stage1.S1_M_121.GRRMissingAPI, missingAPISplit, missingAPISplitTable, and missingAPISplit_length. This is formalization debt and not repo-local integration closure: no concrete Lean K-theory/Chow/Chern/Todd/pushforward/projection-formula/base-change package has been pinned, imported, or proved locally for terminal Grothendieck-Riemann-Roch."

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.IsProper",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.IsFinite",
  "AlgebraicGeometry.IsProper.comp_iff",
  "SheafOfModules.IsQuasicoherent",
  "SheafOfModules.IsFinitePresentation",
  "HomologicalComplex.eulerChar",
  "HomologicalComplex.homologyEulerChar"
]

/-- Search terms that did not locate a terminal Grothendieck-Riemann-Roch theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Grothendieck-Riemann-Roch",
  "Grothendieck Riemann Roch",
  "GrothendieckRiemannRoch",
  "RiemannRoch",
  "Riemann-Roch",
  "GRR",
  "Todd class",
  "ToddClass",
  "Chern character",
  "ChernCharacter",
  "Chow ring",
  "ChowRing",
  "KTheory",
  "K-theory",
  "K0"
]

/-- Exact external Lean 4 search terms requested for `THM-M-0177.external-audit`. -/
def externalAuditSearchTerms : List String := [
  "GrothendieckRiemannRoch",
  "\"Grothendieck-Riemann-Roch\"",
  "\"Grothendieck Riemann Roch\"",
  "RiemannRoch",
  "\"Riemann-Roch\"",
  "ToddClass",
  "\"Todd class\"",
  "ChernCharacter",
  "\"Chern character\"",
  "ChowRing",
  "KTheory",
  "K0"
]

/--
Checked metadata for the external-audit pass.

The runtime had no authenticated GitHub CLI/API token, so authenticated primary
code search could not be completed inside the repo-local closure.  Pinned local
mathlib searches and directly inspected public Lean 4 sources found no terminal
Grothendieck-Riemann-Roch theorem to pin, import, and check.
-/
def externalAuditNote : String :=
  "THM-M-0177.external-audit: exact requested Lean 4 search terms are recorded in externalAuditSearchTerms. In this child runtime, gh auth status reported no logged-in GitHub host and no GH_TOKEN/GITHUB_TOKEN environment variable was present, so authenticated GitHub code search is an integration blocker rather than a completed gate. Supplementary pinned local mathlib searches at 8a178386ffc0f5fef0b77738bb5449d50efeea95 and directly inspected public Lean 4 sources found no terminal Grothendieck-Riemann-Roch theorem. No external Lean 4 closure has been pinned, imported, or checked for THM-M-0177."

/--
Machine status for the `THM-M-0177.integration-gate` child.

The current repo-local artifact is a checked statement-shape and audit surface,
not a local proof body, not a mathlib wrapper for GRR, and not a pinned external
GRR dependency.
-/
def integrationGateMachineStatus : String :=
  "not_repo_local_closed"

/--
Integration gate note for `THM-M-0177.integration-gate`.

No external Lean 4 closure for terminal Grothendieck-Riemann-Roch is currently
available in the local Lake closure or in the audited local mathlib snapshot.
Therefore there is no external theorem to mark `external_upstream_pinned`.
Anchor-only evidence is not accepted as completion for this Stage1 slot: if a
future authenticated primary-source audit finds a closed external Lean 4 GRR
theorem, the next integration step must either pin/import/check that project in
this repository or record a concrete blocker such as toolchain incompatibility,
license/dependency conflict, or an upstream placeholder proof.
-/
def integrationGateNote : String :=
  "THM-M-0177.integration-gate: no terminal external Lean 4 Grothendieck-Riemann-Roch closure has been verified in the local Lake closure or pinned mathlib snapshot, so no external_upstream_anchor_only evidence is being counted as completed. Current machine status is not_repo_local_closed / formalization_debt. If a future authenticated primary-source search finds a closed Lean 4 GRR theorem, a public completion claim requires either pin/import/check in this repository or a concrete integration blocker such as toolchain incompatibility, license/dependency conflict, or upstream placeholder status."

/--
Checked gate proposition: this child makes no completed theorem claim that
retains repo-local integration debt.
-/
def integrationGateNoCompletedRepoLocalIntegrationDebt : Prop :=
  True

/-- The integration-gate proposition is intentionally only a status gate. -/
theorem integrationGateNoCompletedRepoLocalIntegrationDebt_holds :
    integrationGateNoCompletedRepoLocalIntegrationDebt :=
  trivial

end S1_M_121
end Stage1
end AwesomeTheorems
