import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.DifferentialForm.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.ENNReal.Basic
import Mathlib.LinearAlgebra.SymplecticGroup
import Mathlib.Topology.MetricSpace.Basic

/-!
# S1-M-256 / THM-M-0612: Gromov nonsqueezing, Stage1 statement boundary

This Stage1 artifact records a conservative Lean 4 boundary for Gromov's
symplectic nonsqueezing theorem.  The local mathlib checkout supplies finite
canonical symplectic matrices, but this audit did not find a terminal theorem
for symplectic capacities, pseudoholomorphic curves, or nonsqueezing of a ball
into a cylinder.

The statement below therefore exposes the standard finite-dimensional
coordinate ball, the target cylinder over one `(q_i, p_i)` coordinate plane,
and a finite-dimensional `ContDiff` symplectic-embedding datum whose
symplectic-form preservation field is the pullback equality for the standard
constant two-form.  It also fixes the Stage1 Gromov-width API: the chosen
capacity is the supremum of normalized areas `π r^2` of standard balls that
symplectically embed into a target set.  It is a checked statement-shape and
mathlib-anchor wrapper, not a proof of nonsqueezing.
-/

noncomputable section

open Matrix
open scoped BigOperators

namespace AwesomeTheorems.Stage1.S1_M_256

universe u

/-! ## Pinned mathlib anchor audit -/

/--
The mathlib revision used for the Stage1 anchor audit.

This matches the repository's Lake pin for mathlib at the time this
statement-boundary artifact was checked.
-/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
The mathlib declarations audited as local anchors for finite canonical
symplectic matrices and the finite symplectic group.
-/
def mathlibAnchorNames : List String :=
  [ "Matrix.J"
  , "Matrix.J_transpose"
  , "Matrix.J_squared"
  , "Matrix.symplecticGroup"
  , "SymplecticGroup.J_mem"
  , "SymplecticGroup.symplectic_det"
  ]

/-! ## Terminal nonsqueezing external-audit marker -/

/--
Date of the repeated Stage1 audit for a terminal Lean 4 proof of Gromov
nonsqueezing.
-/
def terminalNonsqueezingExternalAuditDate : String :=
  "2026-05-01"

/--
Primary-source scope inspected for a terminal Lean 4 nonsqueezing proof.

The audit found mathlib's finite symplectic matrix API but no Lean 4 theorem
closing symplectic capacity, pseudoholomorphic-curve, or ball-into-cylinder
nonsqueezing.
-/
def terminalNonsqueezingExternalAuditScope : List String :=
  [ "repo-local Lake manifest and .lake package closure"
  , "pinned mathlib SymplecticGroup source/docs"
  , "Lean community archive search for nonsqueezing/capacity terms"
  , "GitHub repository search for Lean nonsqueezing/capacity projects"
  ]

/--
Concrete audit outcome for the terminal nonsqueezing proof search.

This string is intentionally conservative: no external proof package was found,
so there is no upstream proof to leave as anchor-only completed evidence.  The
terminal theorem remains formalization debt rather than repo-local integration
debt.
-/
def terminalNonsqueezingExternalAuditOutcome : String :=
  "no terminal Lean 4 nonsqueezing proof found; no pin/import/check target identified"

/-- Standard `2n`-dimensional coordinate phase space, with coordinates `(q, p)`. -/
abbrev CanonicalPhase (Q : Type u) : Type u :=
  Q ⊕ Q → ℝ

/-- Squared Euclidean coordinate norm on the finite canonical phase space. -/
def coordinateNormSq {Q : Type u} [Fintype Q] (x : CanonicalPhase Q) : ℝ :=
  ∑ a : Q ⊕ Q, x a ^ 2

/-- The open ball of radius `r` in standard finite-dimensional coordinates. -/
def standardBall {Q : Type u} [Fintype Q] (r : ℝ) : Set (CanonicalPhase Q) :=
  {x | coordinateNormSq x < r ^ 2}

/--
The standard symplectic cylinder over the coordinate plane indexed by `i`.

Classically this is `B²(R) × ℝ^(2n-2)`: only the `(q_i, p_i)` coordinates are
bounded.
-/
def standardCylinder {Q : Type u} (i : Q) (R : ℝ) : Set (CanonicalPhase Q) :=
  {x | x (Sum.inl i) ^ 2 + x (Sum.inr i) ^ 2 < R ^ 2}

/-- The canonical symplectic matrix on `(q, p)` coordinates. -/
def canonicalSymplecticMatrix (Q : Type u) [DecidableEq Q] :
    Matrix (Q ⊕ Q) (Q ⊕ Q) ℝ :=
  Matrix.J Q ℝ

/-- Unbundled real-valued differential forms on a normed vector space. -/
abbrev RealDifferentialForm
    (Base : Type u) [NormedAddCommGroup Base] [NormedSpace ℝ Base] (degree : ℕ) :=
  Base → Base [⋀^Fin degree]→L[ℝ] ℝ

/-- Real-valued two-forms on the finite canonical phase space. -/
abbrev StandardPhaseTwoForm (Q : Type u) [Fintype Q] :=
  RealDifferentialForm (CanonicalPhase Q) 2

/-- Coordinate projection as a continuous linear functional. -/
def coordinateLinearFunctional
    {Q : Type u} [Fintype Q] (a : Q ⊕ Q) :
    CanonicalPhase Q →L[ℝ] ℝ :=
  ContinuousLinearMap.proj a

/-- The constant coordinate one-form `da` on standard phase space. -/
def canonicalCoordinateOneForm
    {Q : Type u} [Fintype Q] (a : Q ⊕ Q) :
    CanonicalPhase Q [⋀^Fin 1]→L[ℝ] ℝ :=
  ContinuousAlternatingMap.ofSubsingleton ℝ (CanonicalPhase Q) ℝ (0 : Fin 1)
    (coordinateLinearFunctional a)

/-- The coordinate summand `dq_i ∧ dp_i` of the standard symplectic form. -/
noncomputable def standardSymplecticCoordinateTwoForm
    {Q : Type u} [Fintype Q] (i : Q) :
    CanonicalPhase Q [⋀^Fin 2]→L[ℝ] ℝ :=
  ContinuousAlternatingMap.alternatizeUncurryFin
    (ContinuousLinearMap.smulRight
      (coordinateLinearFunctional (Q := Q) (Sum.inl i))
      (canonicalCoordinateOneForm (Q := Q) (Sum.inr i)))

/-- The standard constant symplectic two-form `Σ_i dq_i ∧ dp_i`. -/
noncomputable def standardSymplecticTwoForm
    (Q : Type u) [Fintype Q] : StandardPhaseTwoForm Q :=
  fun _ => ∑ i : Q, standardSymplecticCoordinateTwoForm (Q := Q) i

/--
Pullback of the standard constant two-form along a map of finite standard
phase spaces, expressed in mathlib's unbundled normed-space differential-form
API.
-/
noncomputable def PullbackStandardSymplecticForm
    {Q : Type u} [Fintype Q]
    (f : CanonicalPhase Q → CanonicalPhase Q) : StandardPhaseTwoForm Q :=
  fun x =>
    (standardSymplecticTwoForm Q (f x)).compContinuousLinearMap (fderiv ℝ f x)

/-- Concrete preservation predicate for the standard symplectic two-form. -/
def PreservesStandardSymplecticForm
    {Q : Type u} [Fintype Q]
    (f : CanonicalPhase Q → CanonicalPhase Q) : Prop :=
  PullbackStandardSymplecticForm f = standardSymplecticTwoForm Q

/--
Stage1 datum for a smooth symplectic embedding of standard phase space.

The smoothness field is a real Lean 4 smooth-map hypothesis for the finite
normed vector space `CanonicalPhase Q`, expressed as `ContDiff ℝ ⊤ toFun`.
The `preservesStandardSymplecticForm` field is a concrete pullback equality
for the unbundled standard constant two-form on this finite coordinate model.
-/
structure SymplecticEmbeddingDatum
    (Q : Type u) [DecidableEq Q] [Fintype Q] where
  toFun : CanonicalPhase Q → CanonicalPhase Q
  injective : Function.Injective toFun
  contDiff : ContDiff ℝ ⊤ toFun
  preservesStandardSymplecticForm : PreservesStandardSymplecticForm toFun

/-- The embedding sends the source ball into the target cylinder. -/
def MapsBallIntoCylinder
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (f : SymplecticEmbeddingDatum Q) (i : Q) (r R : ℝ) : Prop :=
  Set.MapsTo f.toFun (standardBall (Q := Q) r) (standardCylinder i R)

/-! ## Gromov-width capacity API -/

/--
Repo-local symplectic embedding predicate between subsets of the same standard
finite phase space.

This deliberately reuses the global `SymplecticEmbeddingDatum` from the current
statement boundary.  A later partial-map/manifold API can refine this predicate
without changing the capacity route's public names.
-/
def SymplecticEmbedsInto
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (source target : Set (CanonicalPhase Q)) : Prop :=
  ∃ f : SymplecticEmbeddingDatum Q, Set.MapsTo f.toFun source target

/-- The selected Stage1 capacity normalization for a radius-`r` ball: `π r^2`. -/
noncomputable def normalizedBallCapacityValue (r : ℝ) : ENNReal :=
  ENNReal.ofReal (Real.pi * r ^ 2)

/--
Admissible values whose supremum defines the Gromov width of a target set.

The value `π r^2` is admissible for `target` when the standard ball of radius
`r` symplectically embeds into `target`.
-/
noncomputable def GromovWidthAdmissibleValues
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (target : Set (CanonicalPhase Q)) : Set ENNReal :=
  {c | ∃ r : ℝ, 0 < r ∧ c = normalizedBallCapacityValue r ∧
      SymplecticEmbedsInto (standardBall (Q := Q) r) target}

/-- The selected Stage1 symplectic capacity API: Gromov width. -/
noncomputable def GromovWidth
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (target : Set (CanonicalPhase Q)) : ENNReal :=
  sSup (GromovWidthAdmissibleValues target)

/-- Stable public name for the chosen capacity API in this Stage1 artifact. -/
noncomputable def ChosenSymplecticCapacity
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    Set (CanonicalPhase Q) → ENNReal :=
  GromovWidth (Q := Q)

/-- Target statement for the later ball-capacity computation child. -/
def BallGromovWidthComputationTarget
    {Q : Type u} [DecidableEq Q] [Fintype Q] (r : ℝ) : Prop :=
  GromovWidth (Q := Q) (standardBall (Q := Q) r) = normalizedBallCapacityValue r

/-- Lower-bound leaf target for the ball-capacity computation. -/
def BallGromovWidthLowerBoundTarget
    {Q : Type u} [DecidableEq Q] [Fintype Q] (r : ℝ) : Prop :=
  normalizedBallCapacityValue r ≤ GromovWidth (Q := Q) (standardBall (Q := Q) r)

/-- Upper-bound leaf target for the ball-capacity computation. -/
def BallGromovWidthUpperBoundTarget
    {Q : Type u} [DecidableEq Q] [Fintype Q] (r : ℝ) : Prop :=
  GromovWidth (Q := Q) (standardBall (Q := Q) r) ≤ normalizedBallCapacityValue r

/-- Target statement for the later cylinder-capacity computation child. -/
def CylinderGromovWidthComputationTarget
    {Q : Type u} [DecidableEq Q] [Fintype Q] (i : Q) (R : ℝ) : Prop :=
  GromovWidth (Q := Q) (standardCylinder i R) = normalizedBallCapacityValue R

/-- Lower-bound leaf target for the cylinder-capacity computation. -/
def CylinderGromovWidthLowerBoundTarget
    {Q : Type u} [DecidableEq Q] [Fintype Q] (i : Q) (R : ℝ) : Prop :=
  normalizedBallCapacityValue R ≤ GromovWidth (Q := Q) (standardCylinder i R)

/-- Upper-bound leaf target for the cylinder-capacity computation. -/
def CylinderGromovWidthUpperBoundTarget
    {Q : Type u} [DecidableEq Q] [Fintype Q] (i : Q) (R : ℝ) : Prop :=
  GromovWidth (Q := Q) (standardCylinder i R) ≤ normalizedBallCapacityValue R

/-- Target statement for the later monotonicity child under symplectic embeddings. -/
def GromovWidthMonotonicityTarget
    (Q : Type u) [DecidableEq Q] [Fintype Q] : Prop :=
  ∀ {source target : Set (CanonicalPhase Q)},
    SymplecticEmbedsInto source target →
      GromovWidth source ≤ GromovWidth target

/--
Leaf target for composing the current global symplectic-embedding datum.

This is the genuine geometric/API blocker for monotonicity: once embeddings
compose in the repo-local datum, admissible balls transfer along embeddings.
-/
def SymplecticEmbeddingTransitivityTarget
    (Q : Type u) [DecidableEq Q] [Fintype Q] : Prop :=
  ∀ {source middle target : Set (CanonicalPhase Q)},
    SymplecticEmbedsInto source middle →
      SymplecticEmbedsInto middle target →
        SymplecticEmbedsInto source target

/--
Leaf target saying admissible Gromov-width values transfer along a
symplectic embedding.
-/
def GromovWidthAdmissibleTransferTarget
    (Q : Type u) [DecidableEq Q] [Fintype Q] : Prop :=
  ∀ {source target : Set (CanonicalPhase Q)},
    SymplecticEmbedsInto source target →
      GromovWidthAdmissibleValues source ⊆ GromovWidthAdmissibleValues target

/--
Order-theoretic leaf target for passing from admissible-value inclusion to
Gromov-width inequality.
-/
def GromovWidthSupremumMonotonicityTarget
    (Q : Type u) [DecidableEq Q] [Fintype Q] : Prop :=
  ∀ {source target : Set (CanonicalPhase Q)},
    GromovWidthAdmissibleValues source ⊆ GromovWidthAdmissibleValues target →
      GromovWidth source ≤ GromovWidth target

/--
Stage1 normalized statement-shape candidate for Gromov nonsqueezing.

For every nonzero finite coordinate set `Q`, no smooth symplectic embedding can
send the standard ball of radius `r` into the standard cylinder of radius `R`
when `0 < R < r`.  The actual symplectic and smoothness content is isolated in
`SymplecticEmbeddingDatum` until the missing capacity/pseudoholomorphic-curve
proof package is available.
-/
def StatementShape : Prop :=
  ∀ (Q : Type u) [DecidableEq Q] [Fintype Q] [Nonempty Q],
    ∀ (i : Q) {r R : ℝ}, 0 < R → R < r →
      ¬ ∃ f : SymplecticEmbeddingDatum Q,
        ContDiff ℝ ⊤ f.toFun ∧ PreservesStandardSymplecticForm f.toFun ∧
          MapsBallIntoCylinder f i r R

/--
Named public boundary for this Stage1 artifact.

This alias is intentionally definitionally equal to `StatementShape`: it gives
blueprint backfill text a stable declaration to cite while keeping the theorem
status as a statement boundary rather than a proved nonsqueezing theorem.
-/
def CurrentRepoLocalStatementBoundary : Prop :=
  StatementShape.{u}

/-- Machine-readable status marker for the current local artifact. -/
inductive RepoLocalClosureState where
  /-- The file checks a statement boundary and supporting wrappers only. -/
  | statementBoundary
  /-- Reserved for a future local proof body or pinned upstream proof closure. -/
  | terminalProofClosed
  deriving DecidableEq

/--
The current repo-local closure state is statement-boundary only, not terminal
proof closure.
-/
def currentRepoLocalClosureState : RepoLocalClosureState :=
  RepoLocalClosureState.statementBoundary

/-- Leaf-budget state for M0387-style local proof ledgers. -/
inductive LeafBudgetStatus where
  /--
  The leaf is not complete: it must remain open until it has an independent
  `<=100` step ledger and the corresponding Lean/formalization work is closed.
  -/
  | unchecked
  deriving DecidableEq

/-- Runtime leaf-budget entry for the currently pending Gromov nonsqueezing leaves. -/
structure PendingLeafBudgetEntry where
  leafId : String
  packageId : String
  budgetCeiling : ℕ
  status : LeafBudgetStatus
  independentLedgerRequired : Bool
  workItem : String
  deriving DecidableEq

/--
Machine-readable local copy of the C010 leaf-budget gate.

These entries intentionally keep `M0612-L014` through `M0612-L023` marked
`unchecked`.  They are not completion evidence; each leaf needs its own
independent `<=100` step ledger before any later status promotion.
-/
def pendingLeafBudgetEntries : List PendingLeafBudgetEntry :=
  [ { leafId := "M0612-L014"
      packageId := "M0612-P3"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Replace smoothness placeholder with actual Lean smooth-map/manifold API." }
  , { leafId := "M0612-L015"
      packageId := "M0612-P3"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Replace symplectic-form placeholder with pullback equality for the standard two-form." }
  , { leafId := "M0612-L016"
      packageId := "M0612-P4"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Define the chosen symplectic capacity or Gromov-width API in Lean 4." }
  , { leafId := "M0612-L017"
      packageId := "M0612-P4"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Prove the standard-ball capacity computation under the selected normalization." }
  , { leafId := "M0612-L018"
      packageId := "M0612-P4"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Prove the standard-cylinder capacity computation under the selected normalization." }
  , { leafId := "M0612-L019"
      packageId := "M0612-P5"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Prove monotonicity of the chosen invariant under symplectic embeddings." }
  , { leafId := "M0612-L020"
      packageId := "M0612-P6"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Audit and prove linear symplectic special cases under the chosen statement." }
  , { leafId := "M0612-L021"
      packageId := "M0612-P7"
      budgetCeiling := 100
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Combine radius inequalities, capacity computations, and monotonicity into nonsqueezing." }
  , { leafId := "M0612-L022"
      packageId := "M0612-P8"
      budgetCeiling := 60
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Merge validation and statement-boundary status into authorized public surfaces." }
  , { leafId := "M0612-L023"
      packageId := "M0612-P8"
      budgetCeiling := 60
      status := LeafBudgetStatus.unchecked
      independentLedgerRequired := true
      workItem := "Pin/import/check any future external Lean 4 proof or record a concrete integration blocker." }
  ]

/-- Compact projection of the pending leaf ids and their explicit statuses. -/
def pendingLeafBudgetStatuses : List (String × LeafBudgetStatus) :=
  pendingLeafBudgetEntries.map fun entry => (entry.leafId, entry.status)

/-- The C010 leaf-budget gate keeps every pending leaf explicitly unchecked. -/
theorem pendingLeafBudgetStatuses_eq_unchecked :
    pendingLeafBudgetStatuses =
      [ ("M0612-L014", LeafBudgetStatus.unchecked)
      , ("M0612-L015", LeafBudgetStatus.unchecked)
      , ("M0612-L016", LeafBudgetStatus.unchecked)
      , ("M0612-L017", LeafBudgetStatus.unchecked)
      , ("M0612-L018", LeafBudgetStatus.unchecked)
      , ("M0612-L019", LeafBudgetStatus.unchecked)
      , ("M0612-L020", LeafBudgetStatus.unchecked)
      , ("M0612-L021", LeafBudgetStatus.unchecked)
      , ("M0612-L022", LeafBudgetStatus.unchecked)
      , ("M0612-L023", LeafBudgetStatus.unchecked)
      ] :=
  rfl

/-- The public boundary alias is exactly `StatementShape`. -/
theorem currentRepoLocalStatementBoundary_iff :
    CurrentRepoLocalStatementBoundary.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/-- This artifact records statement-boundary status, not terminal proof closure. -/
theorem currentRepoLocalClosureState_eq_statementBoundary :
    currentRepoLocalClosureState = RepoLocalClosureState.statementBoundary :=
  rfl

/-- The statement shape unfolds to the expected quantified nonsqueezing form. -/
theorem statementShape_iff_forall_no_embedding :
    StatementShape.{u} ↔
      ∀ (Q : Type u) [DecidableEq Q] [Fintype Q] [Nonempty Q],
        ∀ (i : Q) {r R : ℝ}, 0 < R → R < r →
          ¬ ∃ f : SymplecticEmbeddingDatum Q,
            ContDiff ℝ ⊤ f.toFun ∧ PreservesStandardSymplecticForm f.toFun ∧
              MapsBallIntoCylinder f i r R :=
  Iff.rfl

/-- Membership in the Stage1 coordinate ball is the explicit norm-square inequality. -/
theorem mem_standardBall_iff
    {Q : Type u} [Fintype Q] {x : CanonicalPhase Q} {r : ℝ} :
    x ∈ standardBall (Q := Q) r ↔ coordinateNormSq x < r ^ 2 :=
  Iff.rfl

/-- Membership in the Stage1 cylinder is the explicit coordinate-plane inequality. -/
theorem mem_standardCylinder_iff
    {Q : Type u} {x : CanonicalPhase Q} {i : Q} {R : ℝ} :
    x ∈ standardCylinder i R ↔
      x (Sum.inl i) ^ 2 + x (Sum.inr i) ^ 2 < R ^ 2 :=
  Iff.rfl

/-- The standard symplectic form is the constant sum of coordinate two-form summands. -/
theorem standardSymplecticTwoForm_apply
    {Q : Type u} [Fintype Q] (x : CanonicalPhase Q) :
    standardSymplecticTwoForm Q x =
      ∑ i : Q, standardSymplecticCoordinateTwoForm (Q := Q) i :=
  rfl

/-- The pullback predicate unfolds to equality with the standard two-form. -/
theorem preservesStandardSymplecticForm_iff
    {Q : Type u} [Fintype Q] (f : CanonicalPhase Q → CanonicalPhase Q) :
    PreservesStandardSymplecticForm f ↔
      PullbackStandardSymplecticForm f = standardSymplecticTwoForm Q :=
  Iff.rfl

/-- The origin lies in the source ball for every positive radius. -/
theorem zero_mem_standardBall
    {Q : Type u} [Fintype Q] {r : ℝ} (hr : 0 < r) :
    (0 : CanonicalPhase Q) ∈ standardBall (Q := Q) r := by
  simp [standardBall, coordinateNormSq, sq_pos_of_pos hr]

/-- Project the injectivity field from a Stage1 symplectic embedding datum. -/
theorem SymplecticEmbeddingDatum.injective_toFun
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (f : SymplecticEmbeddingDatum Q) :
    Function.Injective f.toFun :=
  f.injective

/-- Project the continuity field from a Stage1 symplectic embedding datum. -/
theorem SymplecticEmbeddingDatum.continuous_toFun
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (f : SymplecticEmbeddingDatum Q) :
    Continuous f.toFun :=
  f.contDiff.continuous

/-- Project the `C^∞` smoothness field from a Stage1 symplectic embedding datum. -/
theorem SymplecticEmbeddingDatum.contDiff_toFun
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (f : SymplecticEmbeddingDatum Q) :
    ContDiff ℝ ⊤ f.toFun :=
  f.contDiff

/-- Project the concrete standard two-form pullback equality from the datum. -/
theorem SymplecticEmbeddingDatum.preservesStandardSymplecticForm_toFun
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (f : SymplecticEmbeddingDatum Q) :
    PreservesStandardSymplecticForm f.toFun :=
  f.preservesStandardSymplecticForm

/-- Unfold the ball-to-cylinder map condition at a point of the source ball. -/
theorem MapsBallIntoCylinder.apply
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {f : SymplecticEmbeddingDatum Q} {i : Q} {r R : ℝ}
    (h : MapsBallIntoCylinder f i r R)
    {x : CanonicalPhase Q} (hx : x ∈ standardBall (Q := Q) r) :
    f.toFun x ∈ standardCylinder i R :=
  h hx

/-- The subset embedding predicate unfolds to a global datum plus `Set.MapsTo`. -/
theorem symplecticEmbedsInto_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {source target : Set (CanonicalPhase Q)} :
    SymplecticEmbedsInto source target ↔
      ∃ f : SymplecticEmbeddingDatum Q, Set.MapsTo f.toFun source target :=
  Iff.rfl

/-- A ball-to-cylinder map is a subset symplectic embedding into that cylinder. -/
theorem symplecticEmbedsInto_standardBall_standardCylinder_of_mapsTo
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {f : SymplecticEmbeddingDatum Q} {i : Q} {r R : ℝ}
    (h : MapsBallIntoCylinder f i r R) :
    SymplecticEmbedsInto (standardBall (Q := Q) r) (standardCylinder i R) :=
  ⟨f, h⟩

/-- The selected ball-capacity value unfolds to `ENNReal.ofReal (π r^2)`. -/
theorem normalizedBallCapacityValue_eq (r : ℝ) :
    normalizedBallCapacityValue r = ENNReal.ofReal (Real.pi * r ^ 2) :=
  rfl

/-- The admissible-value set unfolds to the selected Gromov-width criterion. -/
theorem mem_GromovWidthAdmissibleValues_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {target : Set (CanonicalPhase Q)} {c : ENNReal} :
    c ∈ GromovWidthAdmissibleValues target ↔
      ∃ r : ℝ, 0 < r ∧ c = normalizedBallCapacityValue r ∧
        SymplecticEmbedsInto (standardBall (Q := Q) r) target :=
  Iff.rfl

/-- A concrete embedded ball contributes its normalized value to the width set. -/
theorem normalizedBallCapacityValue_mem_GromovWidthAdmissibleValues
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {target : Set (CanonicalPhase Q)} {r : ℝ}
    (hr : 0 < r)
    (h : SymplecticEmbedsInto (standardBall (Q := Q) r) target) :
    normalizedBallCapacityValue r ∈ GromovWidthAdmissibleValues target :=
  ⟨r, hr, rfl, h⟩

/-- Gromov width is the supremum of the admissible normalized ball values. -/
theorem GromovWidth_eq_sSup
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (target : Set (CanonicalPhase Q)) :
    GromovWidth target = sSup (GromovWidthAdmissibleValues target) :=
  rfl

/-- The stable chosen-capacity name is definitionally the Gromov width. -/
theorem ChosenSymplecticCapacity_eq_GromovWidth
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    ChosenSymplecticCapacity Q = GromovWidth (Q := Q) :=
  rfl

/-- The later ball computation target unfolds to the selected normalization. -/
theorem BallGromovWidthComputationTarget_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q] {r : ℝ} :
    BallGromovWidthComputationTarget (Q := Q) r ↔
      GromovWidth (Q := Q) (standardBall (Q := Q) r) =
        normalizedBallCapacityValue r :=
  Iff.rfl

/-- The ball computation target is exactly its lower and upper bound leaves. -/
theorem BallGromovWidthComputationTarget_iff_bounds
    {Q : Type u} [DecidableEq Q] [Fintype Q] {r : ℝ} :
    BallGromovWidthComputationTarget (Q := Q) r ↔
      BallGromovWidthLowerBoundTarget (Q := Q) r ∧
        BallGromovWidthUpperBoundTarget (Q := Q) r := by
  constructor
  · intro h
    constructor
    · dsimp [BallGromovWidthLowerBoundTarget, BallGromovWidthComputationTarget] at h ⊢
      rw [h]
    · dsimp [BallGromovWidthUpperBoundTarget, BallGromovWidthComputationTarget] at h ⊢
      rw [h]
  · rintro ⟨hlower, hupper⟩
    dsimp [BallGromovWidthLowerBoundTarget, BallGromovWidthUpperBoundTarget,
      BallGromovWidthComputationTarget] at hlower hupper ⊢
    exact le_antisymm hupper hlower

/-- The later cylinder computation target unfolds to the selected normalization. -/
theorem CylinderGromovWidthComputationTarget_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q] {i : Q} {R : ℝ} :
    CylinderGromovWidthComputationTarget (Q := Q) i R ↔
      GromovWidth (Q := Q) (standardCylinder i R) =
        normalizedBallCapacityValue R :=
  Iff.rfl

/-- The cylinder computation target is exactly its lower and upper bound leaves. -/
theorem CylinderGromovWidthComputationTarget_iff_bounds
    {Q : Type u} [DecidableEq Q] [Fintype Q] {i : Q} {R : ℝ} :
    CylinderGromovWidthComputationTarget (Q := Q) i R ↔
      CylinderGromovWidthLowerBoundTarget (Q := Q) i R ∧
        CylinderGromovWidthUpperBoundTarget (Q := Q) i R := by
  constructor
  · intro h
    constructor
    · dsimp [CylinderGromovWidthLowerBoundTarget, CylinderGromovWidthComputationTarget] at h ⊢
      rw [h]
    · dsimp [CylinderGromovWidthUpperBoundTarget, CylinderGromovWidthComputationTarget] at h ⊢
      rw [h]
  · rintro ⟨hlower, hupper⟩
    dsimp [CylinderGromovWidthLowerBoundTarget, CylinderGromovWidthUpperBoundTarget,
      CylinderGromovWidthComputationTarget] at hlower hupper ⊢
    exact le_antisymm hupper hlower

/-- The later monotonicity target unfolds to monotonicity under symplectic embeddings. -/
theorem GromovWidthMonotonicityTarget_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q] :
    GromovWidthMonotonicityTarget Q ↔
      ∀ {source target : Set (CanonicalPhase Q)},
        SymplecticEmbedsInto source target →
          GromovWidth source ≤ GromovWidth target :=
  Iff.rfl

/-- The symplectic-embedding transitivity target unfolds to composition closure. -/
theorem SymplecticEmbeddingTransitivityTarget_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q] :
    SymplecticEmbeddingTransitivityTarget Q ↔
      ∀ {source middle target : Set (CanonicalPhase Q)},
        SymplecticEmbedsInto source middle →
          SymplecticEmbedsInto middle target →
            SymplecticEmbedsInto source target :=
  Iff.rfl

/-- The admissible-transfer target unfolds to subset inclusion of value sets. -/
theorem GromovWidthAdmissibleTransferTarget_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q] :
    GromovWidthAdmissibleTransferTarget Q ↔
      ∀ {source target : Set (CanonicalPhase Q)},
        SymplecticEmbedsInto source target →
          GromovWidthAdmissibleValues source ⊆ GromovWidthAdmissibleValues target :=
  Iff.rfl

/-- The supremum monotonicity target unfolds to the order-theoretic reduction. -/
theorem GromovWidthSupremumMonotonicityTarget_iff
    {Q : Type u} [DecidableEq Q] [Fintype Q] :
    GromovWidthSupremumMonotonicityTarget Q ↔
      ∀ {source target : Set (CanonicalPhase Q)},
        GromovWidthAdmissibleValues source ⊆ GromovWidthAdmissibleValues target →
          GromovWidth source ≤ GromovWidth target :=
  Iff.rfl

/-- Inclusion of admissible values implies the corresponding Gromov-width inequality. -/
theorem GromovWidth_le_of_admissibleValues_subset
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {source target : Set (CanonicalPhase Q)}
    (h : GromovWidthAdmissibleValues source ⊆ GromovWidthAdmissibleValues target) :
    GromovWidth source ≤ GromovWidth target := by
  dsimp [GromovWidth]
  exact sSup_le_sSup h

/-- The order-theoretic leaf of monotonicity is checked locally. -/
theorem GromovWidthSupremumMonotonicityTarget_checked
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    GromovWidthSupremumMonotonicityTarget Q := by
  intro source target h
  exact GromovWidth_le_of_admissibleValues_subset (Q := Q) h

/--
Embedding transitivity transfers admissible Gromov-width values.

The remaining open work is to prove `SymplecticEmbeddingTransitivityTarget Q`
for the current `SymplecticEmbeddingDatum`.
-/
theorem GromovWidthAdmissibleTransferTarget_of_embedding_transitivity
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (htrans : SymplecticEmbeddingTransitivityTarget Q) :
    GromovWidthAdmissibleTransferTarget Q := by
  intro source target hst c hc
  rcases hc with ⟨r, hr, rfl, hball⟩
  exact ⟨r, hr, rfl, htrans hball hst⟩

/-- Monotonicity follows from admissible-value transfer and the checked supremum leaf. -/
theorem GromovWidthMonotonicityTarget_of_admissible_transfer
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (htransfer : GromovWidthAdmissibleTransferTarget Q) :
    GromovWidthMonotonicityTarget Q := by
  intro source target hst
  exact GromovWidth_le_of_admissibleValues_subset (Q := Q) (htransfer hst)

/-- Monotonicity follows once the current symplectic-embedding datum is transitive. -/
theorem GromovWidthMonotonicityTarget_of_embedding_transitivity
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (htrans : SymplecticEmbeddingTransitivityTarget Q) :
    GromovWidthMonotonicityTarget Q :=
  GromovWidthMonotonicityTarget_of_admissible_transfer
    (GromovWidthAdmissibleTransferTarget_of_embedding_transitivity htrans)

/-- The canonical symplectic matrix is skew-symmetric in mathlib. -/
theorem canonicalSymplecticMatrix_transpose
    (Q : Type u) [DecidableEq Q] :
    (canonicalSymplecticMatrix Q)ᵀ = -canonicalSymplecticMatrix Q :=
  Matrix.J_transpose Q ℝ

/-- The square of the canonical symplectic matrix is `-1` in mathlib. -/
theorem canonicalSymplecticMatrix_squared
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    canonicalSymplecticMatrix Q * canonicalSymplecticMatrix Q = -1 :=
  Matrix.J_squared Q ℝ

/-- The canonical symplectic matrix lies in mathlib's finite symplectic group. -/
theorem canonicalSymplecticMatrix_mem_symplecticGroup
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    canonicalSymplecticMatrix Q ∈ Matrix.symplecticGroup Q ℝ :=
  SymplecticGroup.J_mem Q ℝ

/-- A mathlib symplectic matrix has unit determinant. -/
theorem symplecticMatrix_det_isUnit
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {A : Matrix (Q ⊕ Q) (Q ⊕ Q) ℝ}
    (hA : A ∈ Matrix.symplecticGroup Q ℝ) :
    IsUnit (Matrix.det A) :=
  SymplecticGroup.symplectic_det hA

/-! ## Serialized import-aggregator decision marker -/

/--
Shared-import decision status for child audit `S1-M-256-C011`.

This child is a serialized integration gate, not a terminal nonsqueezing proof.
The current worker validates this file directly and records the exact aggregator
patch plan, while shared import aggregators stay outside this worker's write
scope.
-/
def childC011AggregatorDecisionStatus : String :=
  "serial_integration_ready: add the Stage1 module import only in an authorized serialized aggregator patch"

/-- Whether child audit `S1-M-256-C011` edited a shared Lean import aggregator. -/
def childC011SharedAggregatorEdited : Bool :=
  false

/-- Exact Lean import line proposed for a later serialized aggregator patch. -/
def childC011ProposedAggregatorImportLine : String :=
  "import AwesomeTheorems.Stage1.S1_M_256"

/-- Per-file validation command for the `S1-M-256-C011` aggregator decision gate. -/
def childC011ValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_256.lean"

/-- Aggregate validation command required if the serialized import patch is applied. -/
def childC011PostAggregatorValidationCommand : String :=
  "cd Formalizations/Lean && lake env lean AwesomeTheorems.lean"

/-- Public backfill task text for the later serialized import-aggregator patch. -/
def childC011PublicBackfillTask : String :=
  "In an authorized serialized Lean-aggregator patch, add `import AwesomeTheorems.Stage1.S1_M_256` to the chosen shared aggregator if Stage1 modules are being surfaced there, then rerun both the per-file validation and the aggregate validation."

/-- Repo-local integration-debt gate result for child audit `S1-M-256-C011`. -/
def childC011RepoLocalIntegrationDebtGate : String :=
  "passed: aggregator decision records statement-boundary import planning only; no terminal theorem completion or anchor-only external proof is claimed"

/-- Checked metadata equation for the child `S1-M-256-C011` aggregator decision status. -/
theorem childC011AggregatorDecisionStatus_eq :
    childC011AggregatorDecisionStatus =
      "serial_integration_ready: add the Stage1 module import only in an authorized serialized aggregator patch" :=
  rfl

/-- Checked metadata equation for the child `S1-M-256-C011` shared aggregator edit gate. -/
theorem childC011SharedAggregatorEdited_eq_false :
    childC011SharedAggregatorEdited = false :=
  rfl

/-- Checked metadata equation for the child `S1-M-256-C011` proposed import line. -/
theorem childC011ProposedAggregatorImportLine_eq :
    childC011ProposedAggregatorImportLine =
      "import AwesomeTheorems.Stage1.S1_M_256" :=
  rfl

/-- Checked metadata equation for the child `S1-M-256-C011` validation command. -/
theorem childC011ValidationCommand_eq :
    childC011ValidationCommand =
      "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_256.lean" :=
  rfl

/-- Checked metadata equation for the child `S1-M-256-C011` aggregate validation command. -/
theorem childC011PostAggregatorValidationCommand_eq :
    childC011PostAggregatorValidationCommand =
      "cd Formalizations/Lean && lake env lean AwesomeTheorems.lean" :=
  rfl

/-- Checked metadata equation for the child `S1-M-256-C011` public backfill task. -/
theorem childC011PublicBackfillTask_eq :
    childC011PublicBackfillTask =
      "In an authorized serialized Lean-aggregator patch, add `import AwesomeTheorems.Stage1.S1_M_256` to the chosen shared aggregator if Stage1 modules are being surfaced there, then rerun both the per-file validation and the aggregate validation." :=
  rfl

/-- Checked metadata equation for the child `S1-M-256-C011` integration-debt gate. -/
theorem childC011RepoLocalIntegrationDebtGate_eq :
    childC011RepoLocalIntegrationDebtGate =
      "passed: aggregator decision records statement-boundary import planning only; no terminal theorem completion or anchor-only external proof is claimed" :=
  rfl

/-! ## Audit probes retained in the checked file. -/

#check Matrix.J
#check Matrix.J_transpose
#check Matrix.J_squared
#check Matrix.symplecticGroup
#check SymplecticGroup.J_mem
#check SymplecticGroup.symplectic_det
#check terminalNonsqueezingExternalAuditDate
#check terminalNonsqueezingExternalAuditScope
#check terminalNonsqueezingExternalAuditOutcome
#check ContDiff
#check ContDiff.continuous
#check standardSymplecticTwoForm
#check PullbackStandardSymplecticForm
#check PreservesStandardSymplecticForm
#check SymplecticEmbedsInto
#check LeafBudgetStatus
#check PendingLeafBudgetEntry
#check pendingLeafBudgetEntries
#check pendingLeafBudgetStatuses
#check pendingLeafBudgetStatuses_eq_unchecked
#check normalizedBallCapacityValue
#check GromovWidthAdmissibleValues
#check GromovWidth
#check ChosenSymplecticCapacity
#check BallGromovWidthComputationTarget
#check BallGromovWidthLowerBoundTarget
#check BallGromovWidthUpperBoundTarget
#check CylinderGromovWidthComputationTarget
#check CylinderGromovWidthLowerBoundTarget
#check CylinderGromovWidthUpperBoundTarget
#check GromovWidthMonotonicityTarget
#check SymplecticEmbeddingTransitivityTarget
#check GromovWidthAdmissibleTransferTarget
#check GromovWidthSupremumMonotonicityTarget
#check GromovWidth_le_of_admissibleValues_subset
#check GromovWidthSupremumMonotonicityTarget_checked
#check GromovWidthAdmissibleTransferTarget_of_embedding_transitivity
#check GromovWidthMonotonicityTarget_of_admissible_transfer
#check GromovWidthMonotonicityTarget_of_embedding_transitivity
#check childC011AggregatorDecisionStatus
#check childC011SharedAggregatorEdited
#check childC011ProposedAggregatorImportLine
#check childC011ValidationCommand
#check childC011PostAggregatorValidationCommand
#check childC011PublicBackfillTask
#check childC011RepoLocalIntegrationDebtGate
#check childC011AggregatorDecisionStatus_eq
#check childC011SharedAggregatorEdited_eq_false
#check childC011ProposedAggregatorImportLine_eq
#check childC011ValidationCommand_eq
#check childC011PostAggregatorValidationCommand_eq
#check childC011PublicBackfillTask_eq
#check childC011RepoLocalIntegrationDebtGate_eq
#check StatementShape

end AwesomeTheorems.Stage1.S1_M_256
