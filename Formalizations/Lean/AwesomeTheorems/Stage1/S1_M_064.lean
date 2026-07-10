import Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass
import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic
import Mathlib.NumberTheory.FLT.Basic
import Mathlib.NumberTheory.FLT.Four
import Mathlib.NumberTheory.FLT.MasonStothers
import Mathlib.NumberTheory.FLT.Polynomial
import Mathlib.NumberTheory.FLT.Three
import Mathlib.NumberTheory.ModularForms.Basic
import Mathlib.NumberTheory.ModularForms.CongruenceSubgroups
import Mathlib.NumberTheory.ModularForms.QExpansion
import Mathlib.RepresentationTheory.Basic

/-!
# S1-M-064 / THM-M-0446: Wiles--Taylor theorem

This Stage1 artifact records a conservative statement boundary for the
Wiles--Taylor modularity-lifting theorem.  The pinned mathlib environment has
ordinary modular forms, Weierstrass elliptic-curve data, absolute Galois groups,
`GL_2`, and plain representation objects.  It does not currently expose the
semistable elliptic-curve modularity theorem or the Taylor--Wiles
modularity-lifting theorem as a terminal theorem.

The declarations below therefore name the formalization boundary without using
kernel holes or axiomatizing the theorem.

## Public statement-normalization note

`StatementShape.{u}` is a Stage1 statement-shape artifact, not a proof of the
Wiles--Taylor theorem.  The universe parameter `u` is explicit in the
semistable elliptic-curve input and modular-form target, while the auxiliary
`TaylorWilesPackage` keeps separate universes `u`, `v`, and `w` for the base
field, coefficient semiring, and representation module.

The semistable elliptic-curve input is recorded by
`SemistableEllipticCurveInput.{u}` with fields `curve : WeierstrassCurve ℚ`,
`isElliptic : curve.IsElliptic`, `semistable : Prop`, `conductor : ℕ`,
`residualRepresentationTag : Type u`, and
`residualRepresentationAttached : Prop`.  The modular-form output is recorded
by `ModularFormTarget E` with fields `targetGroup : Subgroup (GL2 ℝ)`,
`targetWeight : ℤ`, `form : ModularForm targetGroup targetWeight`,
`lFunctionCompatibility : Prop`, `conductorCompatibility : Prop`, and
`galoisRepresentationCompatibility : Prop`.

Consequently the normalized statement only says that every such semistable
input satisfying the future formal hypotheses has a nonempty modular-form
target.  It deliberately does not assert a modularity-lifting proof, a
semistable modularity theorem, or a repo-local closure theorem.

## Adjacent FLT infrastructure caution

The imported mathlib FLT modules `Mathlib.NumberTheory.FLT.Basic`,
`Mathlib.NumberTheory.FLT.Three`, `Mathlib.NumberTheory.FLT.Four`,
`Mathlib.NumberTheory.FLT.Polynomial`, and
`Mathlib.NumberTheory.FLT.MasonStothers` are adjacent infrastructure only.
They cover FLT statement/reduction APIs, checked small-exponent branches, and
polynomial/Mason-Stothers variants.  They do not provide the semistable
elliptic-curve modularity theorem, residual modularity, deformation-ring and
Hecke-algebra comparison, Taylor--Wiles patching, or a terminal
Wiles--Taylor modularity-lifting theorem.
-/

open Complex UpperHalfPlane Matrix.SpecialLinearGroup
open scoped MatrixGroups ModularForm

noncomputable section

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_064

universe u v w

/-- The absolute Galois group object currently available in mathlib. -/
abbrev AbsoluteGaloisGroup (K : Type u) [Field K] : Type u :=
  Field.absoluteGaloisGroup K

/-- The `GL_2` object used for a future two-dimensional automorphic target. -/
abbrev GL2 (R : Type u) [Semiring R] : Type u :=
  Matrix.GeneralLinearGroup (Fin 2) R

/--
Plain Galois-side representation data over a field `K`.

This is intentionally weaker than the residual and `p`-adic Galois
representations used in Taylor--Wiles theory; it records the nearest current
mathlib representation substrate.
-/
abbrev GaloisRepresentation
    (K : Type u) (E : Type v) (V : Type w)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V] :
    Type (max u w) :=
  Representation E (AbsoluteGaloisGroup K) V

/--
Semistable elliptic-curve input for the classical Wiles--Taylor application.

The Weierstrass curve and ellipticity predicate use mathlib objects.  The
semistability/conductor/Galois-representation interface is kept as explicit
proposition and data fields because the terminal theorem needs arithmetic
geometry APIs beyond the current local substrate.
-/
structure SemistableEllipticCurveInput where
  curve : WeierstrassCurve ℚ
  isElliptic : curve.IsElliptic
  semistable : Prop
  conductor : ℕ
  residualRepresentationTag : Type u
  residualRepresentationAttached : Prop

/--
Ordinary modular-form output expected from the modularity theorem.

The target uses mathlib's checked `ModularForm` object.  The equality of
L-functions, conductor-level compatibility, and Galois-representation
compatibility are statement-boundary predicates for later replacement by
concrete APIs or a pinned upstream theorem.
-/
structure ModularFormTarget (E : SemistableEllipticCurveInput.{u}) where
  targetGroup : Subgroup (GL2 ℝ)
  targetWeight : ℤ
  form : ModularForm targetGroup targetWeight
  lFunctionCompatibility : Prop
  conductorCompatibility : Prop
  galoisRepresentationCompatibility : Prop

/--
Abstract Taylor--Wiles package for a fixed Galois representation.

The fields isolate the usual proof obligations: residual modularity,
deformation/Hecke comparison, local deformation conditions, and the final
modularity conclusion.
-/
structure TaylorWilesPackage
    (K : Type u) (E : Type v) (V : Type w)
    [Field K] [Semiring E] [AddCommMonoid V] [Module E V]
    (ρ : GaloisRepresentation K E V) : Type (max u v w) where
  residualModularity : Prop
  deformationCondition : Prop
  heckeAlgebraCondition : Prop
  localConditionAtBadPrimes : Prop
  patchingComparison : Prop
  provesModularity : Prop

/--
Stage1 statement-shape candidate for the Wiles--Taylor theorem in its
semistable elliptic-curve modularity form.

This is not a proof of modularity.  It is a precise `Prop` saying that a
semistable elliptic curve satisfying the future formal hypotheses admits a
mathlib ordinary modular-form target with the expected compatibility fields.
-/
def StatementShape : Prop :=
  ∀ E : SemistableEllipticCurveInput.{u},
    E.semistable →
      E.residualRepresentationAttached →
        Nonempty (ModularFormTarget E)

/-- The statement-shape definition unfolds to the named semistable modularity boundary. -/
theorem statementShape_iff :
    StatementShape.{u} ↔
      ∀ E : SemistableEllipticCurveInput.{u},
        E.semistable →
          E.residualRepresentationAttached →
            Nonempty (ModularFormTarget E) :=
  Iff.rfl

/-- A mathlib-backed sanity target: ordinary modular-form spaces are available as checked objects. -/
def OrdinaryModularTargetAvailable (Γ : Subgroup (GL2 ℝ)) (k : ℤ) : Prop :=
  Nonempty (ModularForm Γ k)

/-- The zero modular form provides a low-risk kernel-checked wrapper for the ordinary target type. -/
theorem ordinaryModularTargetAvailable (Γ : Subgroup (GL2 ℝ)) (k : ℤ) :
    OrdinaryModularTargetAvailable Γ k :=
  ⟨0⟩

/-- The zero cusp form is also available in the pinned ordinary modular-form API. -/
theorem ordinaryCuspFormTargetAvailable (Γ : Subgroup (GL2 ℝ)) (k : ℤ) :
    Nonempty (CuspForm Γ k) :=
  ⟨0⟩

/-- The pinned mathlib revision audited for the public S1-M-064-PUB-02 backfill. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Public mathlib anchor modules requested for the Wiles--Taylor Stage1 audit. -/
def publicMathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.NumberTheory.ModularForms.Basic",
  "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups",
  "Mathlib.NumberTheory.ModularForms.QExpansion",
  "Mathlib.RepresentationTheory.Basic"
]

/--
mathlib FLT modules audited for the S1-M-064-PUB-03 caution.

These modules are intentionally recorded as adjacent evidence only, not as a
proof route for Wiles--Taylor modularity lifting.
-/
def adjacentFltInfrastructureModules : List String := [
  "Mathlib.NumberTheory.FLT.Basic",
  "Mathlib.NumberTheory.FLT.Three",
  "Mathlib.NumberTheory.FLT.Four",
  "Mathlib.NumberTheory.FLT.Polynomial",
  "Mathlib.NumberTheory.FLT.MasonStothers"
]

/-- Integration-ready caution rows for the adjacent mathlib FLT infrastructure. -/
def adjacentFltInfrastructureCautionRows : List String := [
  "Mathlib.NumberTheory.FLT.Basic | statement/reduction APIs such as FermatLastTheorem, FermatLastTheoremFor, and FermatLastTheoremWith; not a modularity-lifting theorem",
  "Mathlib.NumberTheory.FLT.Three | checked n = 3 branch via fermatLastTheoremThree; adjacent special-case FLT evidence only",
  "Mathlib.NumberTheory.FLT.Four | checked n = 4 branch via fermatLastTheoremFour and reduction support; adjacent special-case FLT evidence only",
  "Mathlib.NumberTheory.FLT.Polynomial | polynomial-ring FLT variants using Mason-Stothers style infrastructure; not a natural-number Wiles--Taylor proof",
  "Mathlib.NumberTheory.FLT.MasonStothers | Mason-Stothers infrastructure for polynomial/function-field arguments; not semistable elliptic-curve modularity or Taylor--Wiles patching"
]

/-- External ImperialCollegeLondon/FLT revision audited for S1-M-064-PUB-04. -/
def imperialFltAuditRevision : String :=
  "2f4325e3b3e647225890f143d4f2dbf1315d4ebd"

/-- External mathlib revision pinned by the audited ImperialCollegeLondon/FLT lakefile. -/
def imperialFltExternalMathlibRevision : String :=
  "244d9a4c3071a109aa54a41242317594d3c83fb4"

/--
Primary-source rows for the ImperialCollegeLondon/FLT external audit.

This is anchor evidence only.  The terminal theorem is blocked by `sorryAx`,
so it is not a repo-local completion witness for Wiles--Taylor.
-/
def imperialFltPrimarySourceAuditRows : List String := [
  "ImperialCollegeLondon/FLT @ 2f4325e3b3e647225890f143d4f2dbf1315d4ebd | lean-toolchain: leanprover/lean4:v4.30.0-rc2",
  "lakefile.toml | requires mathlib at 244d9a4c3071a109aa54a41242317594d3c83fb4; not this repository's pinned mathlib revision",
  "FermatsLastTheorem.lean | imports FLT, states PNat.pow_add_pow_ne_pow from Wiles_Taylor_Wiles, and prints axioms for the terminal positive-natural FLT theorem",
  "FermatsLastTheorem.lean | printed axioms for PNat.pow_add_pow_ne_pow include [propext, sorryAx, Classical.choice, Quot.sound]",
  "FLT.lean | aggregate imports include FLT.Basic.Reductions, FLT.GaloisRepresentation.Automorphic, deformation packages, patching packages, and assumption modules",
  "blocker | current terminal route is external_upstream_anchor_only with a sorryAx dependency; create a pin/import/check task only after sorryAx disappears or record a concrete compatibility blocker"
]

/-- Terminal Wiles--Taylor ingredients not supplied by the adjacent mathlib FLT modules. -/
def wilesTaylorIngredientsAbsentFromFltInfrastructure : List String := [
  "semistable elliptic-curve modularity theorem",
  "residual modularity theorem for the attached Galois representation",
  "deformation-ring local/global condition package",
  "Hecke-algebra comparison theorem",
  "Taylor--Wiles patching argument",
  "terminal Wiles--Taylor modularity-lifting theorem"
]

/--
Nine-package public theorem-tree split requested by `S1-M-064-PUB-05`.

These are public-backfill package names, not completed theorem names.  The
split keeps the statement boundary, object model, arithmetic input, `R = T`
machinery, modularity conclusion, and repo-local validation gate distinct.
-/
inductive PublicWilesTaylorTheoremTreePackage where
  | statementNormalization
  | mathlibObjectModel
  | galoisRepresentationAttachment
  | residualModularity
  | deformationRings
  | heckeAlgebras
  | taylorWilesPatching
  | modularityConclusion
  | repoLocalClosureGate
  deriving DecidableEq, Repr

/--
One integration-ready row for the Wiles--Taylor public theorem tree.

Every row is deliberately `unchecked` and `repoLocalClosed = false`; the rows
are Stage1/M0387 process scaffolding rather than a proof of Wiles--Taylor.
-/
structure PublicWilesTaylorTheoremTreeRow where
  package : PublicWilesTaylorTheoremTreePackage
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
Integration-ready public theorem-tree rows for the Wiles--Taylor theorem.

The rows are safe to merge into the public blueprint as an open theorem tree.
They must not be used as a completion claim until a local proof body, mathlib
wrapper, or pinned external dependency validates in this repository.
-/
def publicWilesTaylorTheoremTreeRows : List PublicWilesTaylorTheoremTreeRow := [
  {
    package := PublicWilesTaylorTheoremTreePackage.statementNormalization
    code := "WT-PKG-01"
    title := "statement normalization"
    responsibility :=
      "Freeze the root as semistable elliptic-curve modularity plus a Taylor--Wiles modularity-lifting interface."
    upstreamInputs :=
      "SemistableEllipticCurveInput, ModularFormTarget, StatementShape, and the explicit universe policy in this file."
    downstreamOutput :=
      "Canonical public statement boundary, with no proof claim and no hidden modularity-lifting assumption."
    status := "unchecked"
    leafBudgetGate :=
      "Split semistable input fields, modular-form target fields, and compatibility predicates into <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.mathlibObjectModel
    code := "WT-PKG-02"
    title := "mathlib object model"
    responsibility :=
      "Align Weierstrass elliptic curves, absolute Galois groups, GL2, ordinary modular forms, q-expansion infrastructure, and plain representation objects with concrete mathlib declarations."
    upstreamInputs :=
      "publicMathlibAnchorModules, mathlibAnchorRevision, and the local wrappers AbsoluteGaloisGroup, GL2, GaloisRepresentation, OrdinaryModularTargetAvailable."
    downstreamOutput :=
      "A checked object-model audit separating available support APIs from missing terminal Wiles--Taylor APIs."
    status := "unchecked"
    leafBudgetGate :=
      "Keep support-object checks separate from terminal theorem anchors; adjacent FLT modules cannot close this package."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.galoisRepresentationAttachment
    code := "WT-PKG-03"
    title := "Galois representation attachment"
    responsibility :=
      "Define the two-dimensional Galois representation attached to a semistable elliptic curve and its residual representation hypotheses."
    upstreamInputs :=
      "The semistable elliptic-curve input, AbsoluteGaloisGroup, GL2, and the current residualRepresentationTag/residualRepresentationAttached placeholders."
    downstreamOutput :=
      "Concrete attached and residual representation interfaces, including irreducibility and oddness predicates for later lifting."
    status := "unchecked"
    leafBudgetGate :=
      "Attachment, residual reduction, irreducibility, oddness, and compatibility with the elliptic curve need independent <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.residualModularity
    code := "WT-PKG-04"
    title := "residual modularity"
    responsibility :=
      "Formalize the residual modularity input, including the mod-3 or mod-p branch used by the Wiles--Taylor argument."
    upstreamInputs :=
      "Concrete residual representation data from WT-PKG-03 and modular-form support from WT-PKG-02."
    downstreamOutput :=
      "Residual modularity theorem or imported wrapper satisfying the lifting-theorem hypotheses."
    status := "unchecked"
    leafBudgetGate :=
      "Split residual theorem statement, branch hypotheses, and compatibility transfer into <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.deformationRings
    code := "WT-PKG-05"
    title := "deformation rings"
    responsibility :=
      "Define deformation functors, universal deformation rings, local conditions, and bad-prime deformation constraints."
    upstreamInputs :=
      "Attached residual representation data from WT-PKG-03 and residual modularity hypotheses from WT-PKG-04."
    downstreamOutput :=
      "Global and local deformation-ring package usable by the Hecke comparison and patching steps."
    status := "unchecked"
    leafBudgetGate :=
      "Functor definition, representability, local conditions, universal ring, and bad-prime branches remain separate open leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.heckeAlgebras
    code := "WT-PKG-06"
    title := "Hecke algebras"
    responsibility :=
      "Define the relevant Hecke algebras on modular-form spaces, their Galois-deformation comparison maps, and local/global compatibility."
    upstreamInputs :=
      "Modular-form object model from WT-PKG-02 and deformation-ring package from WT-PKG-05."
    downstreamOutput :=
      "Hecke action and comparison-map interface feeding the Taylor--Wiles patching and R = T branch."
    status := "unchecked"
    leafBudgetGate :=
      "Hecke action, algebra construction, comparison map, localization, and compatibility each need <=100-step leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.taylorWilesPatching
    code := "WT-PKG-07"
    title := "Taylor--Wiles patching"
    responsibility :=
      "Formalize auxiliary prime selection, patched modules/rings, numerical criterion, complete-intersection branch, and R = T comparison."
    upstreamInputs :=
      "Deformation-ring package from WT-PKG-05 and Hecke-algebra package from WT-PKG-06."
    downstreamOutput :=
      "Patching comparison theorem strong enough to imply the modularity-lifting conclusion."
    status := "unchecked"
    leafBudgetGate :=
      "Auxiliary primes, patching system, numerical criterion, complete intersection, and R = T comparison remain open leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.modularityConclusion
    code := "WT-PKG-08"
    title := "modularity conclusion"
    responsibility :=
      "Derive modularity of the semistable elliptic curve and the L-function, conductor, and Galois-representation compatibility fields."
    upstreamInputs :=
      "Residual modularity from WT-PKG-04 and Taylor--Wiles patching/R = T output from WT-PKG-07."
    downstreamOutput :=
      "A proof of StatementShape or a theorem wrapper producing Nonempty (ModularFormTarget E) for every eligible semistable input."
    status := "unchecked"
    leafBudgetGate :=
      "Modularity lifting, target construction, L-function compatibility, conductor compatibility, and Galois compatibility need separate leaves."
    repoLocalClosed := false
  },
  {
    package := PublicWilesTaylorTheoremTreePackage.repoLocalClosureGate
    code := "WT-PKG-09"
    title := "repo-local closure gate"
    responsibility :=
      "Close only through a local proof body, local wrapper around pinned mathlib, or pinned/vendored external dependency validated by lake env lean."
    upstreamInputs :=
      "Closed WT-PKG-01 through WT-PKG-08, or a sorryAx-free external theorem with concrete Lake/toolchain/license integration."
    downstreamOutput :=
      "Repo-local completion record with no anchor-only evidence and no completed state retaining repo_local_integration_debt."
    status := "unchecked"
    leafBudgetGate :=
      "Do not mark complete until the local validation command passes and every required M0387 completion gate is explicitly satisfied."
    repoLocalClosed := false
  }
]

/-- The Wiles--Taylor public theorem tree contains exactly nine packages. -/
theorem publicWilesTaylorTheoremTreeRows_length :
    publicWilesTaylorTheoremTreeRows.length = 9 :=
  rfl

/-- The Wiles--Taylor public theorem-tree package codes are `WT-PKG-01` through `WT-PKG-09`. -/
theorem publicWilesTaylorTheoremTreeRows_codes :
    publicWilesTaylorTheoremTreeRows.map PublicWilesTaylorTheoremTreeRow.code =
      ["WT-PKG-01", "WT-PKG-02", "WT-PKG-03", "WT-PKG-04", "WT-PKG-05",
        "WT-PKG-06", "WT-PKG-07", "WT-PKG-08", "WT-PKG-09"] :=
  rfl

/-- Every Wiles--Taylor public theorem-tree package remains unchecked. -/
theorem publicWilesTaylorTheoremTreeRows_statuses_unchecked :
    publicWilesTaylorTheoremTreeRows.map PublicWilesTaylorTheoremTreeRow.status =
      ["unchecked", "unchecked", "unchecked", "unchecked", "unchecked",
        "unchecked", "unchecked", "unchecked", "unchecked"] :=
  rfl

/-- No Wiles--Taylor public theorem-tree row is a repo-local completion claim. -/
theorem publicWilesTaylorTheoremTreeRows_no_repoLocalClosed_claim :
    publicWilesTaylorTheoremTreeRows.map PublicWilesTaylorTheoremTreeRow.repoLocalClosed =
      [false, false, false, false, false, false, false, false, false] :=
  rfl

/--
Authoritative PUB-06 status gate for the Wiles--Taylor Stage1 slot.

This is checked process metadata, not a proof of modularity.  It records that
the public status must stay open as formalization debt until one of the three
accepted repo-local closure routes is available and validated.
-/
structure AuthoritativeFormalizationDebtGate where
  publicTask : String
  authoritativeStatus : String
  machineState : String
  requiredClosureEvidence : List String
  currentClosureEvidence : String
  statusCanCloseNow : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  deriving DecidableEq, Repr

/--
PUB-06 gate value: Wiles--Taylor remains open `formalization_debt`.

The only accepted completion routes are a local proof body, a local wrapper
around a pinned mathlib theorem, or a pinned/vendored external dependency that
validates with the repository's `lake env lean` command.
-/
def pub06AuthoritativeFormalizationDebtGate : AuthoritativeFormalizationDebtGate := {
  publicTask :=
    "S1-M-064-PUB-06"
  authoritativeStatus :=
    "open formalization_debt"
  machineState :=
    "not_repo_local_closed"
  requiredClosureEvidence := [
    "local_proof_body validated by cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_064.lean",
    "local_wrapper_upstream_mathlib around a pinned terminal Wiles--Taylor theorem validated by the same command",
    "external_upstream_pinned or vendored dependency without sorryAx/admit/axiom blockers validated by the same command"
  ]
  currentClosureEvidence :=
    "none: only statement-shape, support-object anchors, theorem-tree metadata, and anchor-only external FLT audit with sorryAx blocker are present"
  statusCanCloseNow :=
    false
  completedStateRetainsRepoLocalIntegrationDebt :=
    false
}

/-- PUB-06 keeps the authoritative public status open as formalization debt. -/
theorem pub06_authoritativeStatus_open_formalizationDebt :
    pub06AuthoritativeFormalizationDebtGate.authoritativeStatus =
      "open formalization_debt" :=
  rfl

/-- PUB-06 records that the Wiles--Taylor slot is not repo-local closed. -/
theorem pub06_machineState_notRepoLocalClosed :
    pub06AuthoritativeFormalizationDebtGate.machineState =
      "not_repo_local_closed" :=
  rfl

/-- PUB-06 has exactly the three M0387-accepted closure routes. -/
theorem pub06_requiredClosureEvidence_length :
    pub06AuthoritativeFormalizationDebtGate.requiredClosureEvidence.length = 3 :=
  rfl

/-- PUB-06 is not currently a completion claim. -/
theorem pub06_statusCanCloseNow_false :
    pub06AuthoritativeFormalizationDebtGate.statusCanCloseNow = false :=
  rfl

/-- PUB-06 leaves no completed-state repo-local integration debt. -/
theorem pub06_no_completedState_repoLocalIntegrationDebt :
    pub06AuthoritativeFormalizationDebtGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/--
M0387 completion gates for PUB-06.

Every positive completion route is currently false; the only passed item is the
negative safety gate that no completed state is claimed with retained
repo-local integration debt.
-/
def pub06M0387GateRows : List (String × Bool) := [
  ("local proof body for StatementShape validates in this repository", false),
  ("local wrapper around a pinned mathlib terminal theorem validates in this repository", false),
  ("pinned or vendored external theorem dependency validates in this repository", false),
  ("external anchor-only evidence is treated as completion evidence", false),
  ("completed state retains repo_local_integration_debt", false)
]

/-- PUB-06 currently satisfies no positive closure row. -/
theorem pub06M0387GateRows_all_false :
    pub06M0387GateRows.map Prod.snd = [false, false, false, false, false] :=
  rfl

/--
PUB-07 trigger gate for the external ImperialCollegeLondon/FLT route.

This is checked process metadata, not a dependency integration.  The current
upstream source still reports `sorryAx` for the terminal positive-natural FLT
theorem, so the required pinned dependency task is recorded as a future trigger
rather than being marked complete from anchor-only evidence.
-/
structure Pub07ExternalFltIntegrationGate where
  publicTask : String
  upstreamProject : String
  latestAuditDate : String
  auditedSourceFiles : List String
  currentSorryAxStatus : String
  triggerCondition : String
  requiredIntegrationTask : String
  allowedOutcomes : List String
  anchorOnlyCompletionAllowed : Bool
  createPinnedDependencyTaskNow : Bool
  repoLocalClosedNow : Bool
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  deriving DecidableEq, Repr

/--
PUB-07 current gate value.

The 2026-05-01 raw upstream audit still shows `sorryAx` in
`FermatsLastTheorem.lean`, while `lakefile.toml` still pins mathlib at
`244d9a4c3071a109aa54a41242317594d3c83fb4` and `lean-toolchain` still uses
`leanprover/lean4:v4.30.0-rc2`.  Therefore this repository must keep the route
open as formalization debt and must not treat the external anchor as a completed
repo-local proof.
-/
def pub07ExternalFltIntegrationGate : Pub07ExternalFltIntegrationGate := {
  publicTask :=
    "S1-M-064-PUB-07"
  upstreamProject :=
    "ImperialCollegeLondon/FLT"
  latestAuditDate :=
    "2026-05-01"
  auditedSourceFiles := [
    "FermatsLastTheorem.lean",
    "FLT.lean",
    "lakefile.toml",
    "lean-toolchain"
  ]
  currentSorryAxStatus :=
    "still_present: FermatsLastTheorem.lean reports PNat.pow_add_pow_ne_pow depends on [propext, sorryAx, Classical.choice, Quot.sound]"
  triggerCondition :=
    "When #print axioms PNat.pow_add_pow_ne_pow no longer includes sorryAx on the Wiles_Taylor_Wiles path"
  requiredIntegrationTask :=
    "Create a pinned dependency or vendored proof-body task with exact upstream commit, Lean toolchain, mathlib revision, imported module path, terminal theorem name, license check, lake manifest update plan, and repo-local validation command"
  allowedOutcomes := [
    "external_upstream_pinned after pin/import/check validates in this repository",
    "local_wrapper_upstream_external after a wrapper around the pinned dependency validates in this repository",
    "integration_blocker if Lean/toolchain/mathlib/API/license incompatibility prevents immediate pin/import/check"
  ]
  anchorOnlyCompletionAllowed :=
    false
  createPinnedDependencyTaskNow :=
    false
  repoLocalClosedNow :=
    false
  completedStateRetainsRepoLocalIntegrationDebt :=
    false
}

/-- PUB-07 records that anchor-only external evidence is not completion evidence. -/
theorem pub07_anchorOnlyCompletionAllowed_false :
    pub07ExternalFltIntegrationGate.anchorOnlyCompletionAllowed = false :=
  rfl

/-- PUB-07 does not create a pinned dependency task while the audited route still has `sorryAx`. -/
theorem pub07_createPinnedDependencyTaskNow_false :
    pub07ExternalFltIntegrationGate.createPinnedDependencyTaskNow = false :=
  rfl

/-- PUB-07 records that the external route is not repo-local closed now. -/
theorem pub07_repoLocalClosedNow_false :
    pub07ExternalFltIntegrationGate.repoLocalClosedNow = false :=
  rfl

/-- PUB-07 leaves no completed-state repo-local integration debt. -/
theorem pub07_no_completedState_repoLocalIntegrationDebt :
    pub07ExternalFltIntegrationGate.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- PUB-07 lists exactly the three allowed follow-up outcomes after the `sorryAx` trigger changes. -/
theorem pub07_allowedOutcomes_length :
    pub07ExternalFltIntegrationGate.allowedOutcomes.length = 3 :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
  "Mathlib.FieldTheory.AbsoluteGaloisGroup",
  "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic",
  "Mathlib.NumberTheory.FLT.Basic",
  "Mathlib.NumberTheory.FLT.Three",
  "Mathlib.NumberTheory.FLT.Four",
  "Mathlib.NumberTheory.FLT.Polynomial",
  "Mathlib.NumberTheory.FLT.MasonStothers",
  "Mathlib.NumberTheory.ModularForms.Basic",
  "Mathlib.NumberTheory.ModularForms.CongruenceSubgroups",
  "Mathlib.NumberTheory.ModularForms.QExpansion",
  "Mathlib.RepresentationTheory.Basic"
]

/-- Search terms that did not locate a terminal Wiles--Taylor theorem in the pinned mathlib tree. -/
def absentTerminalSearchTerms : List String := [
  "Wiles",
  "TaylorWiles",
  "Taylor-Wiles",
  "modularity lifting",
  "semistable modularity",
  "GaloisRepresentation.Automorphic"
]

end S1_M_064
end Stage1
end AwesomeTheorems
