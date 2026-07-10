import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Geometrically.Basic
import Mathlib.CategoryTheory.Comma.Over.Basic
import Mathlib.NumberTheory.NumberField.Basic

/-!
# S1-M-042 / THM-M-0123: Mordell conjecture statement shape

This file intentionally does not claim a proof of Faltings's theorem.  It records a
kernel-checked Lean 4 statement boundary for the usual form over a number field:
the type of `K`-rational sections of a smooth proper genus-at-least-two curve over
`Spec K` should be finite.

Geometric connectedness is represented by mathlib's generic `geometrically`
morphism-property API applied to the topological property `ConnectedSpace`.
The one-dimensional smooth proper curve condition is represented by a local
wrapper around mathlib's `SmoothOfRelativeDimension 1` and `IsProper`
morphism properties.  The remaining predicate slot is genus, because the
audited mathlib revision has the scheme morphism infrastructure but not a ready
genus-of-curve API suitable for this statement.
-/

noncomputable section

open CategoryTheory
open AlgebraicGeometry

universe u

namespace AwesomeTheorems.Stage1.S1_M_042

/-- The affine base scheme `Spec K`, pinned as an abbreviation for statement normalization. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/-- A `K`-rational point of `X` over `Spec K`, expressed as a section of the structure map. -/
abbrev RationalPointOver {K : Type u} [Field K] (X : Scheme.{u}) (π : X ⟶ SpecOf K) :
    Type u :=
  { p : SpecOf K ⟶ X // p ≫ π = 𝟙 (SpecOf K) }

/--
The slice-category convention for a `K`-rational point of a scheme over `Spec K`.

Mathlib does not expose a named general rational-point type for arbitrary
schemes over a field in the audited local revision.  The canonical categorical
encoding is therefore a morphism in the slice category over `Spec K` from the
terminal object `𝟙 (Spec K)` to the given structure morphism `π`.
-/
abbrev OverSpecRationalPoint {K : Type u} [Field K] (X : Scheme.{u}) (π : X ⟶ SpecOf K) :
    Type u :=
  Over.mk (𝟙 (SpecOf K)) ⟶ Over.mk π

/--
Stable repo-local predicate for the one-dimensional smooth proper curve
condition over `Spec K`.

The relative-dimension field uses mathlib's `SmoothOfRelativeDimension 1`;
the properness field uses mathlib's `IsProper`.
-/
structure SmoothProperCurveOverSpec (K : Type u) [Field K] [NumberField K]
    (X : Scheme.{u}) (π : X ⟶ SpecOf K) : Prop where
  smoothRelativeDimensionOne : SmoothOfRelativeDimension 1 π
  proper : IsProper π

/--
Predicate slots for the part of the Mordell/Faltings curve hypotheses that is
not yet represented here by a stable audited mathlib API.
-/
structure CurvePredicateSlots (K : Type u) [Field K] [NumberField K]
    (X : Scheme.{u}) (π : X ⟶ SpecOf K) where
  genusAtLeastTwo : Prop

/--
The statement-shape hypothesis package.  The `curve` field carries the
mathlib-backed smooth proper relative-dimension-one condition; the
`geometricallyConnected` field uses mathlib's stable geometric-property
interface.  The remaining explicit predicate slot is genus.
-/
structure CurveHypothesesOverNumberField {K : Type u} [Field K] [NumberField K]
    {X : Scheme.{u}} {π : X ⟶ SpecOf K} (slots : CurvePredicateSlots K X π) : Prop where
  curve : SmoothProperCurveOverSpec K X π
  geometricallyConnected : geometrically (ConnectedSpace ·) π
  genusAtLeastTwo : slots.genusAtLeastTwo

/-- The formal Stage1 statement shape for the Mordell conjecture / Faltings theorem. -/
def StatementShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (X : Scheme.{u}) (π : X ⟶ SpecOf K)
    (slots : CurvePredicateSlots K X π),
    CurveHypothesesOverNumberField slots → Finite (RationalPointOver X π)

namespace RationalPointOver

theorem comp_structureMap {K : Type u} [Field K] {X : Scheme.{u}} {π : X ⟶ SpecOf K}
    (p : RationalPointOver X π) :
    p.1 ≫ π = 𝟙 (SpecOf K) :=
  p.2

/--
Equivalence between the local section-subtype model and the slice-category
model of rational points over `Spec K`.
-/
def equivOverSpecRationalPoint {K : Type u} [Field K] {X : Scheme.{u}} {π : X ⟶ SpecOf K} :
    RationalPointOver X π ≃ OverSpecRationalPoint X π where
  toFun p := Over.homMk p.1 p.2
  invFun p := ⟨p.left, by simpa using Over.w p⟩
  left_inv p := by
    ext
    rfl
  right_inv p := by
    ext
    rfl

@[simp]
theorem equivOverSpecRationalPoint_apply_left {K : Type u} [Field K] {X : Scheme.{u}}
    {π : X ⟶ SpecOf K} (p : RationalPointOver X π) :
    (equivOverSpecRationalPoint (X := X) (π := π) p).left = p.1 :=
  rfl

@[simp]
theorem equivOverSpecRationalPoint_symm_coe {K : Type u} [Field K] {X : Scheme.{u}}
    {π : X ⟶ SpecOf K} (p : OverSpecRationalPoint X π) :
    ((equivOverSpecRationalPoint (X := X) (π := π)).symm p).1 = p.left :=
  rfl

end RationalPointOver

namespace CurveHypothesesOverNumberField

theorem smoothRelativeDimensionOne' {K : Type u} [Field K] [NumberField K] {X : Scheme.{u}}
    {π : X ⟶ SpecOf K} {slots : CurvePredicateSlots K X π}
    (h : CurveHypothesesOverNumberField slots) :
    SmoothOfRelativeDimension 1 π :=
  h.curve.smoothRelativeDimensionOne

theorem smooth' {K : Type u} [Field K] [NumberField K] {X : Scheme.{u}} {π : X ⟶ SpecOf K}
    {slots : CurvePredicateSlots K X π} (h : CurveHypothesesOverNumberField slots) :
    Smooth π := by
  haveI : SmoothOfRelativeDimension 1 π := h.smoothRelativeDimensionOne'
  exact SmoothOfRelativeDimension.smooth 1 π

theorem proper' {K : Type u} [Field K] [NumberField K] {X : Scheme.{u}} {π : X ⟶ SpecOf K}
    {slots : CurvePredicateSlots K X π} (h : CurveHypothesesOverNumberField slots) :
    IsProper π :=
  h.curve.proper

theorem geometricallyConnected' {K : Type u} [Field K] [NumberField K] {X : Scheme.{u}}
    {π : X ⟶ SpecOf K} {slots : CurvePredicateSlots K X π}
    (h : CurveHypothesesOverNumberField slots) :
    geometrically (ConnectedSpace ·) π :=
  h.geometricallyConnected

end CurveHypothesesOverNumberField

/-! ## Audit constants -/

/-- Local module used as the checked statement-shape anchor for this slot. -/
def localAnchorModules : List String := [
  "AwesomeTheorems.Stage1.S1_M_042"
]

/-- mathlib modules audited through the local Mordell/Faltings statement boundary. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Comma.Over.Basic",
  "Mathlib.AlgebraicGeometry.Geometrically.Basic",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.NumberTheory.NumberField.Basic"
]

/-- Checked local or mathlib names used by this Stage1 artifact. -/
def checkedAnchorNames : List String := [
  "AwesomeTheorems.Stage1.S1_M_042.SpecOf",
  "AwesomeTheorems.Stage1.S1_M_042.RationalPointOver",
  "AwesomeTheorems.Stage1.S1_M_042.OverSpecRationalPoint",
  "AwesomeTheorems.Stage1.S1_M_042.RationalPointOver.equivOverSpecRationalPoint",
  "AwesomeTheorems.Stage1.S1_M_042.SmoothProperCurveOverSpec",
  "AwesomeTheorems.Stage1.S1_M_042.CurvePredicateSlots",
  "AwesomeTheorems.Stage1.S1_M_042.CurveHypothesesOverNumberField",
  "AwesomeTheorems.Stage1.S1_M_042.StatementShape",
  "AlgebraicGeometry.geometrically",
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.SmoothOfRelativeDimension",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.IsProper",
  "CategoryTheory.Over",
  "CategoryTheory.Over.mk",
  "CategoryTheory.Over.homMk",
  "ConnectedSpace",
  "NumberField",
  "Finite",
  "AwesomeTheorems.Stage1.S1_M_042.c006ExternalTerminalProofCandidate",
  "AwesomeTheorems.Stage1.S1_M_042.c006PinImportCheckBlocker",
  "AwesomeTheorems.Stage1.S1_M_042.c006NoAnchorOnlyCompletion_eq_true",
  "AwesomeTheorems.Stage1.S1_M_042.CompletionEvidence",
  "AwesomeTheorems.Stage1.S1_M_042.noRepoLocalIntegrationDebtForEvidence",
  "AwesomeTheorems.Stage1.S1_M_042.completionCheckboxAllowedForEvidence",
  "AwesomeTheorems.Stage1.S1_M_042.currentCompletionEvidence_not_repoLocalClosed",
  "AwesomeTheorems.Stage1.S1_M_042.currentEvidenceHasNoRepoLocalIntegrationDebt_eq_true",
  "AwesomeTheorems.Stage1.S1_M_042.anchorOnlyCompletionCheckboxAllowed_eq_false",
  "AwesomeTheorems.Stage1.S1_M_042.integrationBlockerCompletionCheckboxAllowed_eq_false",
  "AwesomeTheorems.Stage1.S1_M_042.c007StatementWrapperAuditDate",
  "AwesomeTheorems.Stage1.S1_M_042.c007PredicatePackageStableForWrapper",
  "AwesomeTheorems.Stage1.S1_M_042.c007LakeValidatedWrapperWithoutSorry",
  "AwesomeTheorems.Stage1.S1_M_042.c007TheoremWrapperAllowed",
  "AwesomeTheorems.Stage1.S1_M_042.c007CurrentTheoremWrapperAllowed_eq_false",
  "AwesomeTheorems.Stage1.S1_M_042.c007StatementShapeReplacementDecision"
]

/-- Public search terms reserved for the external Lean 4 anchor audit. -/
def externalLeanSearchTerms : List String := [
  "Lean 4 Faltings theorem formalization",
  "Lean 4 Mordell conjecture formalization",
  "mathlib Faltings theorem Mordell conjecture Lean",
  "github Lean Faltings theorem Mordell conjecture",
  "Faltings language:Lean",
  "Mordell language:Lean",
  "MordellConjecture language:Lean",
  "FaltingsTheorem language:Lean"
]

/-- Date of the child external-source audit, using an absolute date for M0387 traceability. -/
def externalLeanPrimarySourceAuditDate : String :=
  "2026-05-01"

/--
Authenticated GitHub code-search status for the external Lean 4 primary-source audit.

The local `gh` client reported no authenticated GitHub host, and no token-like
environment variable was present except `GH_PAGER`.  GitHub REST code search
also returned HTTP 401 for unauthenticated probes, so this child cannot certify
that authenticated code search was completed.
-/
def githubAuthenticatedCodeSearchStatus : String :=
  "blocked: gh auth status reports no login; GitHub code search API returned HTTP 401 Requires authentication"

/-- Fallback public GitHub/API probes run after authenticated code search was blocked. -/
def externalLeanFallbackAuditResults : List String := [
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95: local rg found only docs/1000.yaml title Faltings's theorem; no Mathlib theorem/module for Faltings or Mordell conjecture",
  "GitHub repository API query \"Faltings theorem\" Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query \"Mordell conjecture\" Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query Faltings Lean: total_count=0 incomplete_results=false",
  "GitHub repository API query Mordell Lean4: found AEjonanonymous/Non-existence-of-Perfect-Cuboids@36fdfb8c662467a5c97413899a60ee675ba90f36, module No Perfect Cuboids.lean, theorem names parity_wall_consistency/perfection_locus_empty/no_perfect_cuboid_final; this is not a Mordell-conjecture or Faltings terminal proof",
  "google-deepmind/formal-conjectures@7871d8fc7a8164a1ac16c3765b40c25ce015b681: public tree-name probe found no path containing Faltings or Mordell"
]

/-- Exact external Lean 4 terminal proof anchors found by this child audit. -/
def externalLeanTerminalProofAnchors : List String := []

/--
Whether this child found a public external Lean 4 terminal proof of the
Mordell/Faltings theorem.
-/
def externalLeanTerminalProofFound : Bool :=
  false

theorem externalLeanTerminalProofFound_eq_false :
    externalLeanTerminalProofFound = false :=
  rfl

/-! ## Child C006 pin/import/check gate -/

/-- Date of the C006 external-proof integration gate audit. -/
def c006PinImportCheckAuditDate : String :=
  "2026-05-01"

/--
External terminal Lean 4 Faltings/Mordell theorem selected for Lake integration.

No candidate is selected because the preceding primary-source audit found no
terminal theorem strong enough to pin/import/check, and authenticated GitHub code
search is still blocked in this local environment.
-/
def c006ExternalTerminalProofCandidate : Option String :=
  none

/--
Concrete blocker for the C006 pin/import/check requirement.

This is not an anchor-only completion note.  It is the reason no Lake dependency
or local wrapper can be added by this child: there is no identified external
terminal theorem/module/name to integrate, and the authenticated GitHub search
needed to close the negative audit is unavailable.
-/
def c006PinImportCheckBlocker : String :=
  "blocked: no external Lean 4 terminal Faltings/Mordell theorem was identified by the recorded fallback probes; gh auth status reports no GitHub login, so authenticated GitHub code search still must be rerun before any completion promotion"

/--
C006 gate: no completed state is justified by anchor-only evidence.

If a future authenticated search locates a terminal Lean 4 theorem, this value
must be replaced by a checked pin/import/wrapper decision or an updated concrete
integration blocker before public completion.
-/
def c006NoAnchorOnlyCompletion : Bool :=
  true

theorem c006NoAnchorOnlyCompletion_eq_true :
    c006NoAnchorOnlyCompletion = true :=
  rfl

/--
Evidence states relevant to completed-state promotion for this Mordell/Faltings
slot.

`externalAnchorOnly` is the forbidden repo-local integration-debt residue: it
records an external URL, revision, module, or theorem name without bringing the
proof into this repository's checked Lake closure.  `integrationBlocker` is an
allowed open state because it states why pin/import/check could not yet be
performed, but it still cannot support a completed checkbox.
-/
inductive CompletionEvidence where
  | noTerminalLeanProofFound
  | externalAnchorOnly
  | externalPinnedImportedChecked
  | integrationBlocker
  | localProofBody
  deriving DecidableEq, Repr

/--
Whether an evidence state avoids repo-local integration debt.

This is only a debt gate.  It does not say that the Mordell/Faltings theorem is
proved in this repository.
-/
def noRepoLocalIntegrationDebtForEvidence : CompletionEvidence → Bool
  | .externalAnchorOnly => false
  | .noTerminalLeanProofFound => true
  | .externalPinnedImportedChecked => true
  | .integrationBlocker => true
  | .localProofBody => true

/-- Whether an evidence state can support a completed checkbox for THM-M-0123. -/
def completionCheckboxAllowedForEvidence : CompletionEvidence → Bool
  | .externalPinnedImportedChecked => true
  | .localProofBody => true
  | .noTerminalLeanProofFound => false
  | .externalAnchorOnly => false
  | .integrationBlocker => false

/--
Current C006 import/pin/check decision in evidence-state form.

No terminal external Lean 4 Faltings/Mordell proof anchor is available in the
audited local evidence, so the current state is open and non-completed rather
than anchor-only completed.
-/
def currentCompletionEvidence : CompletionEvidence :=
  .noTerminalLeanProofFound

theorem currentCompletionEvidence_not_repoLocalClosed :
    completionCheckboxAllowedForEvidence currentCompletionEvidence = false :=
  rfl

theorem currentEvidenceHasNoRepoLocalIntegrationDebt_eq_true :
    noRepoLocalIntegrationDebtForEvidence currentCompletionEvidence = true :=
  rfl

/-- Anchor-only external evidence can never support a completed checkbox. -/
theorem anchorOnlyCompletionCheckboxAllowed_eq_false :
    completionCheckboxAllowedForEvidence .externalAnchorOnly = false :=
  rfl

/--
An explicit integration blocker is a valid open gate result, but not completion
evidence.
-/
theorem integrationBlockerCompletionCheckboxAllowed_eq_false :
    completionCheckboxAllowedForEvidence .integrationBlocker = false :=
  rfl

/-! ## Child C007 theorem-wrapper gate -/

/-- Date of the C007 statement-wrapper replacement gate audit. -/
def c007StatementWrapperAuditDate : String :=
  "2026-05-01"

/--
Whether all predicates needed for replacing `StatementShape` by a theorem
wrapper are stable in the repo-local Lean artifact.

This is currently false because `CurvePredicateSlots.genusAtLeastTwo` remains a
slot pending a stable genus API and normalization proof.
-/
def c007PredicatePackageStableForWrapper : Bool :=
  false

/--
Whether a replacement theorem wrapper has been validated by
`lake env lean AwesomeTheorems/Stage1/S1_M_042.lean` with a closed proof.

No theorem wrapper is present in this file; `StatementShape` remains the honest
boundary until both the predicate package and proof source are closed.
-/
def c007LakeValidatedWrapperWithoutSorry : Bool :=
  false

/--
Gate for replacing `StatementShape` by a completed theorem wrapper.

The gate requires stable predicates, a checked wrapper, and completion evidence
that can support a completed checkbox under the repo-local integration rules.
-/
def c007TheoremWrapperAllowed (predicatesStable wrapperValidated : Bool)
    (evidence : CompletionEvidence) : Bool :=
  predicatesStable && wrapperValidated && completionCheckboxAllowedForEvidence evidence

theorem c007CurrentTheoremWrapperAllowed_eq_false :
    c007TheoremWrapperAllowed c007PredicatePackageStableForWrapper
      c007LakeValidatedWrapperWithoutSorry currentCompletionEvidence = false :=
  rfl

/--
Current C007 replacement decision.

`StatementShape` must not be replaced by a theorem wrapper in this child pass:
the genus predicate is still a slot, no local proof body or pinned upstream proof
is in the Lake closure, and no closed wrapper has been validated.
-/
def c007StatementShapeReplacementDecision : String :=
  "blocked: keep StatementShape; CurvePredicateSlots.genusAtLeastTwo is unresolved, currentCompletionEvidence is not repo-local closed, and no theorem wrapper with a closed proof has been validated"

/-- Pinned mathlib revision used for the local genus API audit. -/
def mathlibGenusAuditRevision : String :=
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Identifier search terms used for the local genus API audit.

At this revision these terms do not expose a general genus invariant for smooth
proper curves over fields; the remaining hits are unrelated topology prose or
elliptic-curve/Weierstrass infrastructure.
-/
def mathlibGenusAuditSearchTerms : List String := [
  "genus",
  "Genus",
  "arithmeticGenus",
  "geometricGenus",
  "smooth proper curve"
]

/-- Result of the local mathlib audit for the Mordell/Faltings genus predicate. -/
def mathlibGenusApiAuditResult : String :=
  "absent: no stable scheme-curve genus API was found for replacing genusAtLeastTwo"

/-- Integration-ready child leaves required before the genus slot can be removed. -/
def genusNormalizationChildLeaves : List String := [
  "define or import a genus invariant for smooth proper geometrically connected curves over fields",
  "connect the invariant to SmoothProperCurveOverSpec and the chosen geometric connectedness predicate",
  "prove the normalization equivalence between the public hypothesis genus > 1 and the Lean predicate 2 <= genus",
  "replace CurvePredicateSlots.genusAtLeastTwo only after the replacement validates with lake env lean"
]

/-- The terminal theorem families still missing from the repo-local Lean closure. -/
def remainingTerminalFamilies : List String := [
  "stable genus API for smooth proper curves over number fields",
  "height and descent package for curves/Jacobians over number fields",
  "Mordell-Weil and abelian-variety finiteness bridge usable for Faltings",
  "terminal finiteness theorem for rational points on genus-at-least-two curves"
]

/-- Machine proof debt classification for this open Stage1 slot. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration gate for completed-state promotion.

No completed state is claimed by this file. If a public Lean 4 terminal proof
is later found, this slot must pin/import/check it or record a concrete
integration blocker before any completed-state promotion.
-/
def repoLocalIntegrationDebtGate : String :=
  "open: no external terminal Lean 4 proof is in the repo-local verification closure; C006 records no pin/import/check candidate and blocks completion until authenticated source search finds a terminal theorem or a concrete upstream integration blocker is recorded"

/-! ## Audit probes retained in the checked file. -/

#check SpecOf
#check RationalPointOver
#check OverSpecRationalPoint
#check RationalPointOver.equivOverSpecRationalPoint
#check RationalPointOver.equivOverSpecRationalPoint_apply_left
#check RationalPointOver.equivOverSpecRationalPoint_symm_coe
#check SmoothProperCurveOverSpec
#check CurvePredicateSlots
#check CurveHypothesesOverNumberField
#check StatementShape
#check RationalPointOver.comp_structureMap
#check CurveHypothesesOverNumberField.smoothRelativeDimensionOne'
#check CurveHypothesesOverNumberField.smooth'
#check CurveHypothesesOverNumberField.proper'
#check CurveHypothesesOverNumberField.geometricallyConnected'
#check AlgebraicGeometry.geometrically
#check AlgebraicGeometry.SmoothOfRelativeDimension
#check ConnectedSpace
#check mathlibGenusAuditRevision
#check mathlibGenusAuditSearchTerms
#check mathlibGenusApiAuditResult
#check genusNormalizationChildLeaves
#check externalLeanPrimarySourceAuditDate
#check githubAuthenticatedCodeSearchStatus
#check externalLeanFallbackAuditResults
#check externalLeanTerminalProofAnchors
#check externalLeanTerminalProofFound_eq_false
#check c006PinImportCheckAuditDate
#check c006ExternalTerminalProofCandidate
#check c006PinImportCheckBlocker
#check c006NoAnchorOnlyCompletion_eq_true
#check CompletionEvidence
#check noRepoLocalIntegrationDebtForEvidence
#check completionCheckboxAllowedForEvidence
#check currentCompletionEvidence
#check currentCompletionEvidence_not_repoLocalClosed
#check currentEvidenceHasNoRepoLocalIntegrationDebt_eq_true
#check anchorOnlyCompletionCheckboxAllowed_eq_false
#check integrationBlockerCompletionCheckboxAllowed_eq_false
#check c007StatementWrapperAuditDate
#check c007PredicatePackageStableForWrapper
#check c007LakeValidatedWrapperWithoutSorry
#check c007TheoremWrapperAllowed
#check c007CurrentTheoremWrapperAllowed_eq_false
#check c007StatementShapeReplacementDecision

end AwesomeTheorems.Stage1.S1_M_042
