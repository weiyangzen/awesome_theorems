import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.NumberTheory.Height.Projectivization

/-!
# S1-M-093 / THM-M-0451: Neron-Tate height statement boundary

This Stage1 artifact records a conservative Lean 4 statement shape for the
Neron-Tate canonical height on elliptic curves over number fields.

The local mathlib snapshot provides Weierstrass elliptic curves, their rational
point groups, and global height infrastructure over number fields. It does not
provide the canonical height construction or its terminal arithmetic properties,
so the theorem is represented as a precise package of expected properties plus
checked wrappers around available mathlib declarations.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace AwesomeTheorems.Stage1.S1_M_093

universe u

/--
Expected data and properties of the Neron-Tate canonical height on a
Weierstrass elliptic curve over a number field.

The two function fields keep the local formalization boundary explicit:
`naiveHeight` is the comparison height supplied by a future coordinate-height
model, while `canonicalHeight` is the canonical quadratic height. The proposition
fields are not proofs supplied by this repository; they are the normalized shape
that a local proof body or pinned external dependency must eventually inhabit.
-/
structure NeronTateHeightPackage (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  /-- The canonical Neron-Tate height on `E(K)`. -/
  canonicalHeight : E⟮K⟯ → ℝ
  /-- A logarithmic naive height used for bounded-difference comparison. -/
  naiveHeight : E⟮K⟯ → ℝ
  /-- The canonical and naive heights differ by a bounded function. -/
  boundedDifference : ∃ C : ℝ, ∀ P : E⟮K⟯, |canonicalHeight P - naiveHeight P| ≤ C
  /-- The canonical height is nonnegative. -/
  nonnegative : ∀ P : E⟮K⟯, 0 ≤ canonicalHeight P
  /-- The canonical height is quadratic under multiplication by natural numbers. -/
  quadratic_nsmul :
    ∀ (n : ℕ) (P : E⟮K⟯), canonicalHeight (n • P) = (n : ℝ) ^ 2 * canonicalHeight P
  /-- The canonical height satisfies the parallelogram law. -/
  parallelogram :
    ∀ P Q : E⟮K⟯,
      canonicalHeight (P + Q) + canonicalHeight (P - Q) =
        2 * canonicalHeight P + 2 * canonicalHeight Q
  /-- Points of canonical height zero are exactly torsion points. -/
  torsion_iff_height_zero : ∀ P : E⟮K⟯, IsOfFinAddOrder P ↔ canonicalHeight P = 0

/--
Stage1 statement shape: every elliptic curve over a number field admits a
Neron-Tate height package with the expected bounded-difference, quadratic,
parallelogram, nonnegativity, and torsion-kernel properties.
-/
def StatementShape : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], Nonempty (NeronTateHeightPackage K E)

/--
Public Stage1 audit note for this module.

This checked string is intentionally non-mathematical: it gives the serial
public-doc integrator a repo-local anchor for the status boundary without
claiming a proof of `StatementShape`.
-/
def publicStage1AuditNote : String :=
  "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_093.lean compiles as a Stage1 statement-shape artifact, not as a Neron-Tate height proof."

/-- Definitional audit of the public Stage1 status note. -/
theorem publicStage1AuditNote_eq :
    publicStage1AuditNote =
      "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_093.lean compiles as a Stage1 statement-shape artifact, not as a Neron-Tate height proof." :=
  rfl

/-- One row in the Stage1 mathlib-anchor audit table for this statement-shape artifact. -/
structure MathlibAnchorRow where
  /-- The anchor requested by the public Stage1 backfill task. -/
  requestedAnchor : String
  /-- The repo-local import that exposes the anchor. -/
  importPath : String
  /-- The precise local role of the anchor for the Neron-Tate statement shape. -/
  role : String
  /-- Whether this anchor is locally checked by this module rather than merely noted. -/
  localCheck : String
deriving Repr

/--
Integration-ready mathlib anchor table for the Neron-Tate height statement boundary.

These rows are deliberately infrastructure anchors only. They do not construct a
canonical height, prove convergence, or close the Neron-Tate terminal theorem.
-/
def mathlibAnchorTable : List MathlibAnchorRow :=
  [ { requestedAnchor := "WeierstrassCurve",
      importPath := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
      role := "Weierstrass equation object used as the elliptic-curve model.",
      localCheck := "Checked by `weierstrassCurveAnchor`." },
    { requestedAnchor := "WeierstrassCurve.IsElliptic",
      importPath := "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
      role := "Typeclass asserting the discriminant of a Weierstrass curve is a unit.",
      localCheck := "Checked by `elliptic_discriminant_isUnit`." },
    { requestedAnchor := "E⟮K⟯",
      importPath := "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
      role := "Affine nonsingular K-points on a base-changed Weierstrass curve.",
      localCheck := "Checked by `affinePointNotationAnchor`." },
    { requestedAnchor := "WeierstrassCurve.Affine.Point.instAddCommGroup",
      importPath := "Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point",
      role := "Additive commutative group structure on affine nonsingular points.",
      localCheck := "Checked by `pointAddCommGroup`." },
    { requestedAnchor := "Height.logHeight",
      importPath := "Mathlib.NumberTheory.Height.Basic",
      role := "Tuple logarithmic height candidate for local naive-height modeling.",
      localCheck := "Checked by `logHeightAnchor`." },
    { requestedAnchor := "Height.logHeight_nonneg",
      importPath := "Mathlib.NumberTheory.Height.Basic",
      role := "Nonnegativity theorem for tuple logarithmic height.",
      localCheck := "Checked by `logHeight_nonnegative`." },
    { requestedAnchor := "NumberField",
      importPath := "Mathlib.NumberTheory.NumberField.Basic",
      role := "Number-field typeclass for elliptic curves over number fields.",
      localCheck := "Checked by `numberFieldAnchor`." },
    { requestedAnchor := "Height.AdmissibleAbsValues",
      importPath := "Mathlib.NumberTheory.Height.NumberField",
      role := "Admissible absolute values and product formula infrastructure for heights.",
      localCheck := "Checked by `numberFieldAdmissibleAbsValuesAnchor`." } ]

/-- Checked mathlib anchor: the Weierstrass-curve object model is available. -/
@[reducible]
def weierstrassCurveAnchor (K : Type u) : Type u :=
  WeierstrassCurve K

/-- Checked mathlib anchor: the affine point notation resolves to a Lean type. -/
@[reducible]
def affinePointNotationAnchor {K : Type u} [Field K] (E : WeierstrassCurve K) : Type u :=
  E⟮K⟯

/-- Checked mathlib anchor: the tuple logarithmic height is available. -/
@[reducible]
def logHeightAnchor {K : Type u} [Field K] [Height.AdmissibleAbsValues K]
    {ι : Type u} [Fintype ι] (x : ι → K) : ℝ :=
  Height.logHeight x

/-- Checked mathlib anchor: the number-field typeclass has the expected proposition shape. -/
@[reducible]
def numberFieldAnchor (K : Type u) [Field K] : Prop :=
  NumberField K

/--
Checked mathlib anchor: number fields supply the admissible absolute values
needed by `Height.logHeight`.
-/
@[reducible]
def numberFieldAdmissibleAbsValuesAnchor {K : Type u} [Field K] [NumberField K] :
    Height.AdmissibleAbsValues K :=
  inferInstance

/-- Low-risk wrapper: mathlib exposes the point group on a Weierstrass elliptic curve. -/
@[reducible]
def pointAddCommGroup {K : Type u} [Field K] [DecidableEq K]
    (E : WeierstrassCurve K) [E.IsElliptic] : AddCommGroup E⟮K⟯ :=
  inferInstance

/-- Checked mathlib anchor: an elliptic Weierstrass curve has unit discriminant. -/
theorem elliptic_discriminant_isUnit {K : Type u} [Field K] [DecidableEq K]
    (E : WeierstrassCurve K) [E.IsElliptic] : IsUnit E.Δ :=
  E.isUnit_Δ

/-- Checked mathlib anchor: tuple logarithmic heights are nonnegative. -/
theorem logHeight_nonnegative {K : Type u} [Field K] [NumberField K]
    {ι : Type u} [Fintype ι] (x : ι → K) : 0 ≤ Height.logHeight x :=
  Height.logHeight_nonneg x

/--
Candidate object models for the naive height on elliptic-curve points.

The selected Stage1 model stays inside the repo-local mathlib closure:
represent the coordinate data as finite tuples or projective coordinate tuples
and use mathlib's logarithmic height API. The external `Heights` x-coordinate
API remains a possible future replacement only after it is pinned, imported,
and checked against this repository's Lean stack.
-/
inductive NaiveHeightObjectModel where
  /-- Local mathlib tuple/projective logarithmic heights. -/
  | localMathlibTupleOrProjective
  /-- A future pinned external `Heights` x-coordinate height API. -/
  | pinnedExternalHeightsXCoordinate
deriving DecidableEq, Repr

/-- One row in the Stage1 naive-height object-model decision table. -/
structure NaiveHeightModelDecisionRow where
  /-- Candidate object model under consideration. -/
  model : NaiveHeightObjectModel
  /-- Stage1 decision status for this candidate. -/
  status : String
  /-- Repo-local Lean surface currently available for this candidate. -/
  repoLocalSurface : String
  /-- Why this candidate matters for the Neron-Tate height formalization. -/
  role : String
  /-- Remaining blocker before this candidate can close a theorem package. -/
  blocker : String
deriving Repr

/--
Decision table for the naive height on elliptic-curve points.

This is documentation data inside Lean, not a proof of bounded difference from
the canonical height. It records the canonical Stage1 object-model choice and
the exact integration blocker for the external alternative.
-/
def naiveHeightObjectModelDecisionTable : List NaiveHeightModelDecisionRow :=
  [ { model := .localMathlibTupleOrProjective,
      status := "canonical Stage1 object model",
      repoLocalSurface :=
        "`Height.logHeight`, `Height.logHeight_nonneg`, `Projectivization.logHeight`, and `Projectivization.logHeight_nonneg` locally check through mathlib.",
      role :=
        "Use finite coordinate tuples or projective coordinate tuples as the naive-height carrier for future bounded-difference statements.",
      blocker :=
        "Still needs an elliptic-point coordinate projection and a proof that the chosen tuple/projective height is the intended naive height for the selected Weierstrass model." },
    { model := .pinnedExternalHeightsXCoordinate,
      status := "not canonical until pinned/imported/checked",
      repoLocalSurface :=
        "No `MichaelStollBayreuth/Heights` dependency is present in this repo-local validation closure.",
      role :=
        "Could supply an x-coordinate naive-height API if the external project is made compatible with this repository.",
      blocker :=
        "Requires an exact Lake pin, Lean-toolchain compatibility check, imported API names, and a local wrapper theorem; anchor-only evidence is not completion." } ]

/-- Compatibility status for the audited external `MichaelStollBayreuth/Heights` commit. -/
inductive ExternalHeightsCompatibilityStatus where
  /-- The external project is useful anchor-only evidence, but is not in this repo's closure. -/
  | anchorOnlyToolchainMismatch
  /-- A future state after an exact pin/import/check succeeds locally. -/
  | pinnedAndLocallyChecked
deriving DecidableEq, Repr

/-- Machine-readable Stage1 audit record for the external `Heights` candidate. -/
structure ExternalHeightsAudit where
  /-- External repository owner/name. -/
  repository : String
  /-- External commit audited by this Stage1 child. -/
  commit : String
  /-- Lean toolchain recorded by the external project at the audited commit. -/
  externalLeanToolchain : String
  /-- Lean toolchain used by this repository's current Lean project. -/
  repoLeanToolchain : String
  /-- External mathlib revision recorded in the audited Lake manifest. -/
  externalMathlibRev : String
  /-- This repository's mathlib revision recorded in the local Lake file. -/
  repoMathlibRev : String
  /-- External module names relevant to the S1-M-093 height investigation. -/
  relevantExternalSurface : List String
  /-- Stage1 compatibility result. -/
  status : ExternalHeightsCompatibilityStatus
  /-- Why this audit does not close the Neron-Tate theorem in this repository. -/
  blocker : String
deriving Repr

/--
External `Heights` audit for the naive-height alternative.

This is checked documentation data only. It records a concrete integration
blocker and does not import the external project or prove `StatementShape`.
-/
def externalHeightsAudit : ExternalHeightsAudit :=
  { repository := "MichaelStollBayreuth/Heights",
    commit := "688bdb63259556fab4b0f699ce0d10bd2dce23f6",
    externalLeanToolchain := "leanprover/lean4:v4.30.0-rc2",
    repoLeanToolchain := "leanprover/lean4:v4.29.0",
    externalMathlibRev := "6f66e004f0a46a57a8b0d78b28c45e8e74c6d940",
    repoMathlibRev := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    relevantExternalSurface :=
      [ "Heights.Basic",
        "Heights.MvPolynomial",
        "Heights.NumberField",
        "Heights.EllipticCurve",
        "WeierstrassCurve.Affine.Point.naiveHeight",
        "WeierstrassCurve.Affine.approx_parallelogram_law",
        "WeierstrassCurve.Affine.weakMW_implies_MW" ],
    status := .anchorOnlyToolchainMismatch,
    blocker :=
      "The audited external project is not pinned/imported/checked in this repo, targets Lean v4.30.0-rc2 rather than this repo's Lean v4.29.0 stack, and supplies naive-height/Mordell-Weil infrastructure rather than a Neron-Tate canonical-height terminal theorem." }

/-- Definitional audit of the external `Heights` compatibility status. -/
theorem externalHeightsAudit_status :
    externalHeightsAudit.status = .anchorOnlyToolchainMismatch :=
  rfl

/-- Definitional audit of the external `Heights` toolchain mismatch. -/
theorem externalHeightsAudit_toolchains :
    (externalHeightsAudit.externalLeanToolchain, externalHeightsAudit.repoLeanToolchain) =
      ("leanprover/lean4:v4.30.0-rc2", "leanprover/lean4:v4.29.0") :=
  rfl

/-- One term-level row from the C007 primary-source external audit. -/
structure ExternalHeightsSearchAuditRow where
  /-- Search term requested by the Stage1 child task. -/
  searchTerm : String
  /-- Primary source and command class used for the term audit. -/
  primarySourceAudit : String
  /-- Exact result of the primary-source search. -/
  finding : String
  /-- Completion impact under the M0387 repo-local integration gate. -/
  completionImpact : String
deriving Repr

/--
C007 primary-source term audit for the external `Heights` candidate.

The audit was rerun against `MichaelStollBayreuth/Heights` at commit
`688bdb63259556fab4b0f699ce0d10bd2dce23f6`. It found naive-height and
conditional Mordell-Weil infrastructure in `Heights/EllipticCurve.lean`, but no
Neron-Tate canonical-height construction or terminal theorem.
-/
def externalHeightsPrimarySourceSearchAudit : List ExternalHeightsSearchAuditRow :=
  [ { searchTerm := "NeronTate",
      primarySourceAudit :=
        "rg -F --glob '*.lean' 'NeronTate' on the audited external tarball.",
      finding := "No matches in the external Lean source tree.",
      completionImpact :=
        "No external Neron-Tate terminal theorem was found; S1-M-093 remains open formalization_debt." },
    { searchTerm := "canonicalHeight",
      primarySourceAudit :=
        "rg -F --glob '*.lean' 'canonicalHeight' on the audited external tarball.",
      finding := "No matches in the external Lean source tree.",
      completionImpact :=
        "No external canonical-height API was found to pin/import/check." },
    { searchTerm := "canonical height",
      primarySourceAudit :=
        "rg -F --glob '*.lean' 'canonical height' on the audited external tarball.",
      finding := "No matches in the external Lean source tree.",
      completionImpact :=
        "The external project does not supply a commented or named canonical-height construction." },
    { searchTerm := "Tate height",
      primarySourceAudit :=
        "rg -F --glob '*.lean' 'Tate height' on the audited external tarball.",
      finding := "No matches in the external Lean source tree.",
      completionImpact :=
        "The external project does not supply a Tate-height terminal surface for THM-M-0451." },
    { searchTerm := "WeierstrassCurve.Point.naiveHeight",
      primarySourceAudit :=
        "rg -F --glob '*.lean' 'WeierstrassCurve.Point.naiveHeight' and targeted inspection of `Heights/EllipticCurve.lean`.",
      finding :=
        "The exact non-Affine qualified string has no matches; the audited source defines `Point.naiveHeight` inside namespace `WeierstrassCurve.Affine` at `Heights/EllipticCurve.lean:369`.",
      completionImpact :=
        "Useful naive-height infrastructure exists only as anchor-only external evidence until pinned/imported/checked locally." },
    { searchTerm := "weakMW_implies_MW",
      primarySourceAudit :=
        "rg -F --glob '*.lean' 'weakMW_implies_MW' on the audited external tarball.",
      finding :=
        "Found `theorem weakMW_implies_MW` in namespace `WeierstrassCurve.Affine` at `Heights/EllipticCurve.lean:458`; it proves finite generation from weak Mordell-Weil plus height/Northcott inputs.",
      completionImpact :=
        "This is conditional Mordell-Weil infrastructure, not a Neron-Tate canonical-height theorem and not repo-local checked in this project." } ]

/-- The C007 primary-source audit covers exactly the requested search terms. -/
theorem externalHeightsPrimarySourceSearchAudit_terms :
    externalHeightsPrimarySourceSearchAudit.map (fun row => row.searchTerm) =
      [ "NeronTate",
        "canonicalHeight",
        "canonical height",
        "Tate height",
        "WeierstrassCurve.Point.naiveHeight",
        "weakMW_implies_MW" ] :=
  rfl

/-- Integration-gate status for the external `Heights` route. -/
inductive ExternalHeightsIntegrationGateStatus where
  /--
  The external project is useful infrastructure, but the S1-M-093 gate remains
  open until a canonical-height terminal theorem is supplied and checked here.
  -/
  | openUntilCanonicalHeightTerminalTheorem
  /-- A future state after a pinned terminal theorem is imported and locally checked. -/
  | closedByPinnedTerminalTheorem
deriving DecidableEq, Repr

/-- Machine-readable integration-gate note for external `Heights` infrastructure. -/
structure ExternalHeightsIntegrationGate where
  /-- External infrastructure that may be reused by a future formalization. -/
  usefulInfrastructure : String
  /-- The terminal theorem surface still needed for THM-M-0451. -/
  requiredTerminalSurface : String
  /-- Repo-local validation requirement before any completion claim. -/
  repoLocalRequirement : String
  /-- Current status of the integration gate. -/
  status : ExternalHeightsIntegrationGateStatus
  /-- Boundary statement for public backfill and status summaries. -/
  completionBoundary : String
deriving Repr

/--
Integration-gate note for the audited external `Heights` route.

This checked data records that naive-height and Mordell-Weil infrastructure is
not enough to close THM-M-0451. Completion requires a canonical-height terminal
theorem that is pinned/imported or otherwise supplied and locally validated.
-/
def externalHeightsIntegrationGate : ExternalHeightsIntegrationGate :=
  { usefulInfrastructure :=
      "`Heights` naive-height, approximate-parallelogram, finite-height, and Mordell-Weil infrastructure.",
    requiredTerminalSurface :=
      "A Neron-Tate canonical-height construction with terminal bounded-difference, quadraticity, parallelogram, nonnegativity, and torsion-kernel theorems.",
    repoLocalRequirement :=
      "The terminal theorem must be pinned/imported or supplied in this repository and checked by the local Lean validation command.",
    status := .openUntilCanonicalHeightTerminalTheorem,
    completionBoundary :=
      "External `Heights` infrastructure is useful but does not close THM-M-0451 unless a canonical-height terminal theorem is added and locally checked." }

/-- Definitional audit of the current external `Heights` integration-gate status. -/
theorem externalHeightsIntegrationGate_status :
    externalHeightsIntegrationGate.status =
      .openUntilCanonicalHeightTerminalTheorem :=
  rfl

/-- Definitional audit of the S1-M-093 external `Heights` completion boundary. -/
theorem externalHeightsIntegrationGate_completionBoundary :
    externalHeightsIntegrationGate.completionBoundary =
      "External `Heights` infrastructure is useful but does not close THM-M-0451 unless a canonical-height terminal theorem is added and locally checked." :=
  rfl

/--
Canonical Stage1 choice for the naive-height object model.

This chooses the local mathlib tuple/projective height route because it is the
only option currently inside the repo-local Lean validation closure.
-/
def canonicalNaiveHeightObjectModel : NaiveHeightObjectModel :=
  .localMathlibTupleOrProjective

/-- Definitional audit of the canonical naive-height object-model choice. -/
theorem canonicalNaiveHeightObjectModel_eq :
    canonicalNaiveHeightObjectModel = .localMathlibTupleOrProjective :=
  rfl

/-- Checked mathlib anchor: projective logarithmic height is available. -/
@[reducible]
def projectivizationLogHeightAnchor {K : Type u} [Field K] [Height.AdmissibleAbsValues K]
    {ι : Type u} [Fintype ι] (x : Projectivization K (ι → K)) : ℝ :=
  Projectivization.logHeight x

/-- Checked mathlib anchor: projective logarithmic heights are nonnegative. -/
theorem projectivizationLogHeight_nonnegative {K : Type u} [Field K]
    [Height.AdmissibleAbsValues K] {ι : Type u} [Fintype ι]
    (x : Projectivization K (ι → K)) : 0 ≤ Projectivization.logHeight x :=
  Projectivization.logHeight_nonneg x

/-- Wrapper exposing the nonnegativity field of a supplied Neron-Tate package. -/
theorem package_height_nonnegative {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic] (H : NeronTateHeightPackage K E)
    (P : E⟮K⟯) : 0 ≤ H.canonicalHeight P :=
  H.nonnegative P

/-- Wrapper exposing the bounded-difference field of a supplied Neron-Tate package. -/
theorem package_boundedDifference {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic] (H : NeronTateHeightPackage K E) :
    ∃ C : ℝ, ∀ P : E⟮K⟯, |H.canonicalHeight P - H.naiveHeight P| ≤ C :=
  H.boundedDifference

/-- Wrapper exposing the quadraticity field of a supplied Neron-Tate package. -/
theorem package_quadratic_nsmul {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic] (H : NeronTateHeightPackage K E)
    (n : ℕ) (P : E⟮K⟯) :
    H.canonicalHeight (n • P) = (n : ℝ) ^ 2 * H.canonicalHeight P :=
  H.quadratic_nsmul n P

/-- Wrapper exposing the parallelogram field of a supplied Neron-Tate package. -/
theorem package_parallelogram {K : Type u} [Field K] [DecidableEq K] [NumberField K]
    {E : WeierstrassCurve K} [E.IsElliptic] (H : NeronTateHeightPackage K E)
    (P Q : E⟮K⟯) :
    H.canonicalHeight (P + Q) + H.canonicalHeight (P - Q) =
      2 * H.canonicalHeight P + 2 * H.canonicalHeight Q :=
  H.parallelogram P Q

/-- Wrapper exposing the torsion-kernel field of a supplied Neron-Tate package. -/
theorem package_torsion_iff_height_zero {K : Type u} [Field K] [DecidableEq K]
    [NumberField K] {E : WeierstrassCurve K} [E.IsElliptic] (H : NeronTateHeightPackage K E)
    (P : E⟮K⟯) : IsOfFinAddOrder P ↔ H.canonicalHeight P = 0 :=
  H.torsion_iff_height_zero P

/--
Canonical proof-package split for the future Neron-Tate height construction.

These package names are planning metadata, not proof constructors. They give the
serial public-document integrator a checked repo-local vocabulary for the
independent `<=100` leaf ledgers required by the Stage1 backfill task.
-/
inductive CanonicalHeightConstructionPackage where
  /-- Prove the canonical height limit exists from normalized naive heights. -/
  | convergence
  /-- Prove the canonical height differs from the chosen naive height by a bounded function. -/
  | boundedDifference
  /-- Prove quadraticity under natural-number multiplication. -/
  | quadraticity
  /-- Prove the parallelogram law. -/
  | parallelogram
  /-- Prove the height-zero kernel is exactly the torsion subgroup. -/
  | torsionKernel
deriving DecidableEq, Repr

/-- One integration-ready row in the canonical-height package split. -/
structure CanonicalHeightPackageSplitRow where
  /-- The proof package being budgeted. -/
  package : CanonicalHeightConstructionPackage
  /-- Stable private child-ledger anchor for the package. -/
  leafLedgerAnchor : String
  /-- The proof obligation this package must eventually discharge. -/
  proofObligation : String
  /-- Earlier packages or local object-model choices this package depends on. -/
  dependsOn : List CanonicalHeightConstructionPackage
  /-- Maximum permitted proof-process steps for each eventual leaf ledger. -/
  maxLeafSteps : Nat
  /-- Current repo-local proof status. -/
  repoLocalStatus : String
  /-- Concrete blocker before this row can be marked complete. -/
  blocker : String
deriving Repr

/--
Integration-ready package split for the canonical-height construction.

The rows are deliberately all marked `open formalization_debt`: this repository
has a checked statement-shape artifact and wrappers around supplied package
fields, but it does not yet construct the Neron-Tate height or prove these
properties from the local mathlib height surface.
-/
def canonicalHeightPackageSplit : List CanonicalHeightPackageSplitRow :=
  [ { package := .convergence,
      leafLedgerAnchor := "S1-M-093-C005-convergence",
      proofObligation :=
        "Define normalized naive-height approximants and prove pointwise convergence to the canonical height.",
      dependsOn := [],
      maxLeafSteps := 100,
      repoLocalStatus := "open formalization_debt; no local construction proof",
      blocker :=
        "Requires a selected elliptic-point naive-height API and a local convergence theorem for the normalized height sequence." },
    { package := .boundedDifference,
      leafLedgerAnchor := "S1-M-093-C005-bounded-difference",
      proofObligation :=
        "Prove the canonical height and selected naive height differ by a globally bounded function.",
      dependsOn := [.convergence],
      maxLeafSteps := 100,
      repoLocalStatus := "open formalization_debt; wrapper only for supplied package field",
      blocker :=
        "Requires the convergence construction plus local estimates comparing the limit height with the chosen tuple/projective naive height." },
    { package := .quadraticity,
      leafLedgerAnchor := "S1-M-093-C005-quadraticity",
      proofObligation :=
        "Prove `canonicalHeight (n • P) = (n : ℝ) ^ 2 * canonicalHeight P` for natural-number multiplication.",
      dependsOn := [.convergence, .boundedDifference],
      maxLeafSteps := 100,
      repoLocalStatus := "open formalization_debt; wrapper only for supplied package field",
      blocker :=
        "Requires functorial control of the height sequence under multiplication-by-n maps and local algebraic estimates." },
    { package := .parallelogram,
      leafLedgerAnchor := "S1-M-093-C005-parallelogram",
      proofObligation :=
        "Prove the canonical height parallelogram law on the elliptic-curve point group.",
      dependsOn := [.boundedDifference, .quadraticity],
      maxLeafSteps := 100,
      repoLocalStatus := "open formalization_debt; wrapper only for supplied package field",
      blocker :=
        "Requires the elliptic-curve approximate parallelogram estimate and transfer from bounded error to the canonical-height limit." },
    { package := .torsionKernel,
      leafLedgerAnchor := "S1-M-093-C005-torsion-kernel",
      proofObligation :=
        "Prove `IsOfFinAddOrder P ↔ canonicalHeight P = 0`.",
      dependsOn := [.boundedDifference, .quadraticity, .parallelogram],
      maxLeafSteps := 100,
      repoLocalStatus := "open formalization_debt; wrapper only for supplied package field",
      blocker :=
        "Requires nonnegativity, quadraticity, bounded height finiteness/Northcott input, and the torsion argument in the selected point model." } ]

/-- The canonical package split has exactly the five required proof packages. -/
theorem canonicalHeightPackageSplit_packages :
    canonicalHeightPackageSplit.map (fun row => row.package) =
      [ .convergence,
        .boundedDifference,
        .quadraticity,
        .parallelogram,
        .torsionKernel ] :=
  rfl

/-- The planned package split assigns a `<=100` leaf budget to every package row. -/
theorem canonicalHeightPackageSplit_leafBudgets :
    canonicalHeightPackageSplit.all (fun row => row.maxLeafSteps ≤ 100) = true :=
  rfl

end AwesomeTheorems.Stage1.S1_M_093
