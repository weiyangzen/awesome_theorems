import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# S1-M-115 / THM-M-0580: Perelman's theorem

This Stage1 file records a conservative Lean boundary for the 3-dimensional
Poincare conjecture.  The imported mathlib module has the canonical surrounding
objects and statement text, but at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` its Perelman statements are
`proof_wanted` entries rather than a terminal proof body in this pinned
dependency.

The declarations below therefore normalize the intended statements and expose
small adjacent wrappers only.  They do not prove Perelman's theorem.
-/

noncomputable section

open scoped Manifold ContDiff
open Metric (sphere)

universe u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_115

/-- The Euclidean model space for a 3-manifold. -/
abbrev Euclidean3 : Type :=
  EuclideanSpace ℝ (Fin 3)

/-- The topological 3-sphere used by mathlib's Poincare-conjecture statement. -/
abbrev Sphere3 : Type :=
  sphere (0 : EuclideanSpace ℝ (Fin 4)) 1

/--
Topological 3-dimensional Poincare-conjecture statement shape.

This is the local Stage1 normalization of Perelman's theorem: every compact
Hausdorff simply connected topological 3-manifold is homeomorphic to `S^3`.
-/
def TopologicalPoincare3Statement : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [ChartedSpace Euclidean3 M]
    [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (M ≃ₜ Sphere3)

/--
Smooth 3-dimensional Poincare-conjecture statement shape.

This records the diffeomorphic conclusion for a smooth 3-manifold.  It is a
statement boundary, not a proof.
-/
def SmoothPoincare3Statement : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [ChartedSpace Euclidean3 M]
    [IsManifold (𝓡 3) ∞ M] [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (M ≃ₘ⟮𝓡 3, 𝓡 3⟯ Sphere3)

/--
Generalized topological Poincare-conjecture statement shape, matching the
mathlib module's surrounding API without using its `≃ₕ` notation.
-/
def GeneralizedTopologicalPoincareStatement : Prop :=
  ∀ (n : ℕ) (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace (EuclideanSpace ℝ (Fin n)) M],
    ContinuousMap.HomotopyEquiv M (sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1) →
      Nonempty (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin (n + 1))) 1)

/--
Canonical Stage1 public Lean statement boundary for `S1-M-115 / THM-M-0580`.

This declaration only names the topological 3-dimensional Poincare-conjecture
statement shape used for Perelman's theorem.  It is not a proof of Perelman's
theorem and it is not evidence that the repo-local theorem is closed.
-/
def StatementShape : Prop :=
  TopologicalPoincare3Statement.{u}

/--
Public audit note for integrators: the checked Lean surface in this file is a
statement boundary and adjacent substrate only, not a Perelman proof.
-/
def statementShapePublicBoundaryNote : String :=
  "AwesomeTheorems.Stage1.S1_M_115.StatementShape is the public Lean statement boundary for THM-M-0580; it is not a proof of Perelman's theorem."

/--
mathlib adjacent wrapper: contractibility implies simple connectedness.

This is useful substrate for later low-dimensional special-case work, but it is
not a proof of the Poincare-conjecture statement.
-/
theorem contractibleSpace_to_simplyConnected (X : Type u) [TopologicalSpace X]
    [ContractibleSpace X] : SimplyConnectedSpace X := by
  infer_instance

/-- Conditional wrapper from the normalized topological statement to the Stage1 boundary. -/
theorem statementShape_from_topological
    (h : TopologicalPoincare3Statement.{u}) : StatementShape.{u} :=
  h

/-- Identity wrapper keeping the smooth variant checkable without asserting it. -/
theorem smoothStatementShape_from_smooth
    (h : SmoothPoincare3Statement.{u}) : SmoothPoincare3Statement.{u} :=
  h

/-! ## Audit constants -/

/-- mathlib source module used as the local Stage1 anchor for this theorem family. -/
def mathlibAnchorModules : List String :=
  ["Mathlib.Geometry.Manifold.PoincareConjecture"]

/-- Pinned mathlib revision audited for the Stage1 Perelman/Poincare boundary. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Source-level markers observed in the pinned mathlib Poincare-conjecture module.
They are recorded as audit evidence, not as retained proof constants.
-/
def mathlibProofWantedMarkers : List String :=
  [ "ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere",
    "SimplyConnectedSpace.nonempty_homeomorph_sphere_three",
    "SimplyConnectedSpace.nonempty_diffeomorph_sphere_three" ]

/--
Audit classification for `Mathlib.Geometry.Manifold.PoincareConjecture` at
`mathlibPinnedRevision`: the Poincare entries above are source-level
`proof_wanted` declarations, not terminal proof constants available for a
repo-local wrapper proof.
-/
def mathlibPoincareAuditClassification : String :=
  "proof_wanted source entries only; no terminal Perelman/Poincare proof constants"

/--
External primary-source repository audited for possible Lean 4 Perelman/Poincare
closure.
-/
def leanMillenniumPrizeProblemsRepository : String :=
  "https://github.com/lean-dojo/LeanMillenniumPrizeProblems"

/-- Pinned external revision audited for the LeanMillenniumPrizeProblems source. -/
def leanMillenniumPrizeProblemsRevision : String :=
  "540da94826f70f3edf4d4fc66ce6cda20e903f61"

/-- Poincare source file audited in LeanMillenniumPrizeProblems. -/
def leanMillenniumPrizeProblemsPoincareFile : String :=
  "Problems/Poincare/Millennium.lean"

/-- Raw primary-source URL for the audited LeanMillenniumPrizeProblems Poincare file. -/
def leanMillenniumPrizeProblemsPoincareRawUrl : String :=
  "https://raw.githubusercontent.com/lean-dojo/LeanMillenniumPrizeProblems/540da94826f70f3edf4d4fc66ce6cda20e903f61/Problems/Poincare/Millennium.lean"

/--
Source-level declarations observed in the audited LeanMillenniumPrizeProblems
Poincare file.
-/
def leanMillenniumPrizeProblemsPoincareDeclarations : List String :=
  [ "MillenniumPoincare.PoincareConjecture3",
    "MillenniumPoincare.GeneralizedPoincareConjecture",
    "MillenniumPoincare.ContinuousMap.Homotopic.eq_of_discrete",
    "MillenniumPoincare.homotopyEquiv_nonempty_homeomorph_of_discrete",
    "MillenniumPoincare.generalizedPoincareConjecture_zero" ]

/--
External-audit classification for LeanMillenniumPrizeProblems at the pinned
revision: it restates the 3-dimensional Poincare proposition and proves only a
dimension-0 generalized special case, so it is not a terminal Lean proof of
Perelman's theorem.
-/
def leanMillenniumPrizeProblemsPoincareAuditClassification : String :=
  "restate 3D proposition plus dimension-0 generalized special case only; no terminal Perelman proof"

/-- M0387 external-audit gate: this anchor is not a completion claim. -/
def leanMillenniumPrizeProblemsAllowsCompletionClaim : Bool :=
  false

/--
M0387 integration gate for any future external Lean 4 Perelman proof.

If such a proof is found, this Stage1 item may be marked complete only after the
external source is pinned and either imported or vendored into this repository's
Lean validation closure, with a repo-local check command passing.  A URL,
commit hash, module name, theorem name, or source note by itself is
anchor-only evidence and cannot close `S1-M-115`.
-/
def futureExternalPerelmanProofIntegrationGate : List String :=
  [ "pin the external Lean 4 repository or proof artifact to an exact revision",
    "import or vendor the proof into this repository's Lean validation closure",
    "prove or expose a repo-local checked wrapper for the Perelman/Poincare target",
    "run the repo-local Lean validation command and record its passing result",
    "keep the public completion checkbox open if only anchor-only evidence is available" ]

/-- Anchor-only external evidence must not be treated as completed proof closure. -/
def futureExternalPerelmanAnchorOnlyAllowsCompletion : Bool :=
  false

/--
Positive form of the gate: completion requires repo-local pin/import/check or a
concrete recorded blocker explaining why that integration is currently
impossible.
-/
def futureExternalPerelmanRequiresRepoLocalCheck : Bool :=
  true

/--
Completed-state repo-local integration-debt guard.

This child records the rule only; it does not claim that an external Lean 4
Perelman proof has been found or integrated.
-/
def completedStateRetainsRepoLocalIntegrationDebt : Bool :=
  false

/-! ## Smooth versus topological target decision -/

/--
Decision for `S1-M-115.smooth-vs-topological`.

The public root should close the topological homeomorphism statement first:
`StatementShape` is definitionally `TopologicalPoincare3Statement`.  The smooth
diffeomorphism variant should remain a separate unchecked child target until a
repo-local Lean bridge from topological 3-dimensional Poincare closure to the
smooth diffeomorphism conclusion is pinned, imported, and checked.
-/
def smoothVsTopologicalDecision : String :=
  "Track the topological homeomorphism statement as the public root first; keep the smooth diffeomorphism variant as a separate unchecked child/bridge target until a repo-local checked topological-to-smooth upgrade is available."

/-- Ordered public target plan for the topological and smooth variants. -/
def smoothVsTopologicalPublicTargetOrder : List String :=
  [ "root: TopologicalPoincare3Statement / StatementShape",
    "separate unchecked child: bridge from topological Poincare closure to SmoothPoincare3Statement",
    "completion gate: pin/import/check a Moise/unique-smooth-structure or equivalent Lean bridge before closing the smooth child" ]

/-- The smooth diffeomorphism variant is not closed by the root statement alone. -/
def smoothVariantRequiresSeparateChildTarget : Bool :=
  true

/-- This file does not derive the smooth variant from the topological statement. -/
def smoothVariantDerivedFromTopologicalInCurrentFile : Bool :=
  false

/-- Closing the topological root alone is not a completion claim for the smooth child. -/
def topologicalRootCompletionClosesSmoothVariant : Bool :=
  false

/-- Concrete current blocker for deriving the smooth statement inside this repository. -/
def smoothTopologicalBridgeRepoLocalBlocker : String :=
  "No repo-local checked Lean bridge is present for upgrading a homeomorphism-to-Sphere3 result on a smooth 3-manifold to the stated diffeomorphism-to-Sphere3 conclusion."

/--
Search terms for future audits of retained terminal theorem constants or external
Lean 4 proof bodies.
-/
def absentTerminalSearchTerms : List String :=
  ["Poincare conjecture", "Perelman theorem", "Geometrization theorem", "Ricci flow"]

/-! ## Public leaf-ledger backfill metadata -/

/--
Checked leaf ids from the private Stage1 worker ledger.  These are statement,
audit, and wrapper leaves only; they are not a proof of Perelman's theorem.
-/
def checkedLeafLedgerIds : List String :=
  [ "S1-M-115.L001",
    "S1-M-115.L002",
    "S1-M-115.L003",
    "S1-M-115.L004",
    "S1-M-115.L005",
    "S1-M-115.L006",
    "S1-M-115.L007",
    "S1-M-115.L008",
    "S1-M-115.L009",
    "S1-M-115.L010" ]

/--
Unchecked leaf ids that must remain open in the public Stage1 task tree until a
terminal local proof body, pinned mathlib proof, or pinned external Lean proof is
validated in this repository.
-/
def uncheckedLeafLedgerIds : List String :=
  [ "S1-M-115.L011",
    "S1-M-115.L012",
    "S1-M-115.L013",
    "S1-M-115.L014",
    "S1-M-115.L015",
    "S1-M-115.L016" ]

/-- Integration-ready checked/unchecked leaf ledger for public backfill. -/
def publicLeafLedgerBackfill : List String :=
  [ "S1-M-115.L001 | P0 | <=20 | checked | Define Euclidean3 and Sphere3.",
    "S1-M-115.L002 | P0 | <=30 | checked | Define TopologicalPoincare3Statement.",
    "S1-M-115.L003 | P0 | <=30 | checked | Define SmoothPoincare3Statement.",
    "S1-M-115.L004 | P0 | <=30 | checked | Define GeneralizedTopologicalPoincareStatement.",
    "S1-M-115.L005 | P0 | <=10 | checked | Define canonical StatementShape.",
    "S1-M-115.L006 | P2 | <=20 | checked | Prove ContractibleSpace to SimplyConnectedSpace by instance.",
    "S1-M-115.L007 | P2 | <=10 | checked | Conditional wrapper from topological statement to StatementShape.",
    "S1-M-115.L008 | P2 | <=10 | checked | Identity wrapper for smooth statement boundary.",
    "S1-M-115.L009 | P1 | <=20 | checked | Check mathlib adjacent anchors.",
    "S1-M-115.L010 | P1 | <=50 | checked | Record proof_wanted status for mathlib Poincare targets.",
    "S1-M-115.L011 | P3 | <=100 | unchecked | Define Ricci-flow-with-surgery state space and time-slice predicates in Lean.",
    "S1-M-115.L012 | P3 | <=100 | unchecked | Formalize canonical neighborhood assumptions needed for extinction/classification.",
    "S1-M-115.L013 | P3 | <=100 | unchecked | Build bridge from surgery extinction to spherical space-form/topological classification.",
    "S1-M-115.L014 | P3 | <=100 | unchecked | Specialize classification to simply connected compact 3-manifolds.",
    "S1-M-115.L015 | P4 | <=100 | unchecked | Prove or import bridge from topological homeomorphism closure to the smooth diffeomorphism variant.",
    "S1-M-115.L016 | P5 | <=100 | unchecked | If an external Lean proof appears, pin dependency and prove repo-local wrapper." ]

/--
Public backfill gate for `S1-M-115.leaf-ledger`: the checked/unchecked ledger can
be copied into public planning docs, but `S1-M-115.L011` through
`S1-M-115.L016` must remain unchecked.
-/
def publicLeafLedgerBackfillNote : String :=
  "Copy S1-M-115.L001 through S1-M-115.L016 into the public Stage1 task tree; keep S1-M-115.L011 through S1-M-115.L016 unchecked."

/-! ## Audit probes -/

#check TopologicalPoincare3Statement
#check SmoothPoincare3Statement
#check GeneralizedTopologicalPoincareStatement
#check StatementShape
#check statementShapePublicBoundaryNote
#check mathlibAnchorModules
#check mathlibPinnedRevision
#check mathlibProofWantedMarkers
#check mathlibPoincareAuditClassification
#check leanMillenniumPrizeProblemsRepository
#check leanMillenniumPrizeProblemsRevision
#check leanMillenniumPrizeProblemsPoincareFile
#check leanMillenniumPrizeProblemsPoincareRawUrl
#check leanMillenniumPrizeProblemsPoincareDeclarations
#check leanMillenniumPrizeProblemsPoincareAuditClassification
#check leanMillenniumPrizeProblemsAllowsCompletionClaim
#check futureExternalPerelmanProofIntegrationGate
#check futureExternalPerelmanAnchorOnlyAllowsCompletion
#check futureExternalPerelmanRequiresRepoLocalCheck
#check completedStateRetainsRepoLocalIntegrationDebt
#check smoothVsTopologicalDecision
#check smoothVsTopologicalPublicTargetOrder
#check smoothVariantRequiresSeparateChildTarget
#check smoothVariantDerivedFromTopologicalInCurrentFile
#check topologicalRootCompletionClosesSmoothVariant
#check smoothTopologicalBridgeRepoLocalBlocker
#check absentTerminalSearchTerms
#check checkedLeafLedgerIds
#check uncheckedLeafLedgerIds
#check publicLeafLedgerBackfill
#check publicLeafLedgerBackfillNote
#check ContinuousMap.HomotopyEquiv.NonemptyDiffeomorphSphere
#check SimplyConnectedSpace.ofContractible
#check ContinuousMap.HomotopyEquiv.simplyConnectedSpace_iff
#check ContractibleSpace.hequiv_unit

end S1_M_115
end Stage1
end AwesomeTheorems
