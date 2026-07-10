import Mathlib.NumberTheory.ModularForms.Cusps

/-!
# S1-M-043 / THM-M-0124: Manin-Drinfeld theorem

This Stage1 file records a Lean 4 statement-shape boundary for the Manin-Drinfeld theorem:
differences of cusps on a modular curve map to torsion points in its Jacobian.

The local mathlib dependency already supplies arithmetic-subgroup cusp objects and finite cusp
orbits. It does not yet supply the compactified modular curve, Jacobian/Picard target, cuspidal
divisor class, or Abel-Jacobi map needed for a terminal theorem, so the final theorem is
intentionally represented as checked abstract interfaces plus a `Prop` statement shape.
-/

namespace AwesomeTheorems.Stage1.S1_M_043

universe u

/-- The image of `SL(2, Z)` inside `GL(2, R)`, with all parameters made explicit. -/
abbrev SL2ZInGL2R : Subgroup (GL (Fin 2) ℝ) :=
  (Matrix.SpecialLinearGroup.mapGL (n := Fin 2) (R := ℤ) ℝ).range

/-- Additive torsion point predicate, phrased without committing to a Jacobian implementation. -/
def IsAddTorsionPoint {A : Type u} [AddMonoid A] (x : A) : Prop :=
  ∃ n : ℕ, n ≠ 0 ∧ n • x = 0

/--
Stage1 interface for a compactified modular curve whose boundary cusps are indexed by mathlib
`CuspOrbits Γ`.

The `Point` type is intentionally abstract: mathlib currently provides cusp orbits for arithmetic
subgroups, but not a compactified modular curve object that receives them as points.
-/
structure CompactifiedModularCurve (Γ : Subgroup (GL (Fin 2) ℝ)) where
  Point : Type u
  cuspPoint : CuspOrbits Γ → Point

/--
Stage1 tag for the eventual target receiving cuspidal divisor classes.

The terminal formalization should select a concrete target, most likely the Jacobian of the
compactified modular curve or its degree-zero Picard group. This tag keeps the checked statement
honest about that unresolved choice without pretending that mathlib already exposes the object.
-/
inductive DivisorClassTargetKind where
  | jacobian
  | degreeZeroPicard
  | divisorClassGroup
  | albanese
  deriving DecidableEq

/--
Abstract additive Jacobian/Picard target for cusp divisor classes.

This replaces the old all-in-one `ManinDrinfeldDatum` target field with a dedicated target
interface. The `Carrier` is intentionally only an additive commutative group: that is the structure
needed to state torsion of divisor-class differences, while the geometry remains a follow-on import
or construction task.
-/
structure JacobianPicardTarget where
  Carrier : Type u
  [instCarrier : AddCommGroup Carrier]
  kind : DivisorClassTargetKind

attribute [instance] JacobianPicardTarget.instCarrier

/--
Stage1 interface for the cusp divisor-class map.

The map is deliberately from compactified-curve points rather than directly from `CuspOrbits Γ`.
The induced `cuspClass` below composes this divisor-class map with the compactified curve's cusp
inclusion, so later work can replace both fields with concrete Picard/Jacobian constructions.
-/
structure CuspDivisorClassMap (Γ : Subgroup (GL (Fin 2) ℝ))
    (X : CompactifiedModularCurve.{u} Γ) where
  target : JacobianPicardTarget.{u}
  divisorClass : X.Point → target.Carrier

/-- The divisor class of a cusp, routed through the compactified-curve cusp map. -/
def CuspDivisorClassMap.cuspClass {Γ : Subgroup (GL (Fin 2) ℝ)}
    {X : CompactifiedModularCurve.{u} Γ} (M : CuspDivisorClassMap.{u} Γ X)
    (c : CuspOrbits Γ) : M.target.Carrier :=
  M.divisorClass (X.cuspPoint c)

/-- The Manin-Drinfeld conclusion for an already supplied cusp-class map. -/
def PairwiseCuspDifferenceTorsion {Γ : Subgroup (GL (Fin 2) ℝ)}
    {X : CompactifiedModularCurve.{u} Γ} (M : CuspDivisorClassMap.{u} Γ X) : Prop :=
  ∀ c d : CuspOrbits Γ, IsAddTorsionPoint (M.cuspClass c - M.cuspClass d)

/-- Unfolded form of the pairwise cusp-difference torsion conclusion. -/
theorem pairwiseCuspDifferenceTorsion_iff {Γ : Subgroup (GL (Fin 2) ℝ)}
    {X : CompactifiedModularCurve.{u} Γ} (M : CuspDivisorClassMap.{u} Γ X) :
    PairwiseCuspDifferenceTorsion M ↔
      ∀ c d : CuspOrbits Γ,
        ∃ n : ℕ, n ≠ 0 ∧ n • (M.cuspClass c - M.cuspClass d) = 0 := by
  rfl

/-- Apply the pairwise torsion conclusion to a specified ordered pair of cusps. -/
theorem pairwiseCuspDifferenceTorsion_apply {Γ : Subgroup (GL (Fin 2) ℝ)}
    {X : CompactifiedModularCurve.{u} Γ} {M : CuspDivisorClassMap.{u} Γ X}
    (h : PairwiseCuspDifferenceTorsion M) (c d : CuspOrbits Γ) :
    IsAddTorsionPoint (M.cuspClass c - M.cuspClass d) :=
  h c d

/--
Stage1 statement shape for the Manin-Drinfeld theorem.

For every arithmetic subgroup, once a compatible compactified modular curve, Jacobian/Picard target,
and divisor-class map are available, every difference of two cusp classes should be torsion.
-/
def StatementShape : Prop :=
  ∀ (Γ : Subgroup (GL (Fin 2) ℝ)) [Γ.IsArithmetic]
    (X : CompactifiedModularCurve.{u} Γ) (M : CuspDivisorClassMap.{u} Γ X),
      PairwiseCuspDifferenceTorsion M

/--
Candidate public root statement shapes for the Manin-Drinfeld theorem.

The decision recorded below distinguishes the public mathematical theorem target from the
current repo-local Lean skeleton.  The skeleton is phrased over arithmetic subgroups because
mathlib's checked cusp-orbit API is currently exposed there; the public theorem should be
phrased for congruence subgroups, with `X_0(N)` and `X_1(N)` as later specializations.
-/
inductive PublicRootStatementChoice where
  | arithmeticSubgroup
  | congruenceSubgroup
  | x0Level
  | x1Level
  deriving DecidableEq

/--
C006 decision record for the public root statement of THM-M-0124.

`currentRepoLocalBoundaryName` names the checked `StatementShape` skeleton, so this record does
not assert a completed theorem.  It records that the eventual public root should use congruence
subgroups rather than specializing the root to only `X_0(N)` or only `X_1(N)`.
-/
structure PublicRootStatementDecision where
  selected : PublicRootStatementChoice
  currentRepoLocalBoundaryName : String
  requiresConcreteCongruencePredicate : Bool
  x0x1AreSpecializations : Bool
  arithmeticBoundaryRole : String
  rationale : String

/--
C006 public-root decision: use a congruence-subgroup root, keep the arithmetic-subgroup
`StatementShape` as the current checked repo-local skeleton, and treat `X_0(N)`/`X_1(N)` as
specialized follow-up theorem wrappers.
-/
def c006PublicRootStatementDecision : PublicRootStatementDecision where
  selected := .congruenceSubgroup
  currentRepoLocalBoundaryName := "AwesomeTheorems.Stage1.S1_M_043.StatementShape"
  requiresConcreteCongruencePredicate := true
  x0x1AreSpecializations := true
  arithmeticBoundaryRole :=
    "current mathlib CuspOrbits substrate and possible later generality, not the public root target"
  rationale :=
    "Use the congruence-subgroup formulation as the public Manin-Drinfeld root; " ++
    "keep the arithmetic-subgroup Lean skeleton until the compactified modular curve, " ++
    "Jacobian/Picard target, and congruence predicate are selected; track X_0(N) and X_1(N) " ++
    "as specialization wrappers."

theorem c006_selectsCongruenceSubgroup :
    c006PublicRootStatementDecision.selected =
      PublicRootStatementChoice.congruenceSubgroup :=
  rfl

/-- The current repo-local boundary named by the C006 decision is definitionally `StatementShape`. -/
abbrev C006CurrentRepoLocalBoundary : Prop :=
  StatementShape.{u}

theorem c006_currentBoundary_iff_statementShape :
    C006CurrentRepoLocalBoundary.{u} ↔ StatementShape.{u} :=
  Iff.rfl

theorem c006_requiresConcreteCongruencePredicate :
    c006PublicRootStatementDecision.requiresConcreteCongruencePredicate = true :=
  rfl

theorem c006_x0x1AreSpecializations :
    c006PublicRootStatementDecision.x0x1AreSpecializations = true :=
  rfl

/--
Machine-proof boundary status for a public blueprint merge.

`statementShapeOnly` means the local Lean file validates interfaces and statement shape, but not
the Manin-Drinfeld theorem.  `terminalProofReady` is reserved for a later local proof body,
mathlib wrapper, or pinned external dependency proving the terminal theorem.
-/
inductive MachineProofBoundaryStatus where
  | statementShapeOnly
  | terminalProofReady
  deriving DecidableEq

/--
C007 public-backfill gate for merging the checked statement-shape file into public surfaces.

The gate is metadata for the serial integrator.  It records that the current Lean artifact is ready
to cite as a checked statement-shape boundary, while the public blueprint must not mark the theorem
complete until an integrator confirms the exact machine-proof boundary.
-/
structure PublicBlueprintMergeGate where
  checkedBoundaryName : String
  boundaryStatus : MachineProofBoundaryStatus
  requiresIntegratorBoundaryConfirmation : Bool
  mayMarkTheoremCompleted : Bool
  publicMergeTarget : String
  completionBlocker : String
  proposedChecklistText : String

/--
C007 merge gate: the local statement-shape file may be backfilled into public documentation only as
statement-shape evidence.  It is not terminal Manin-Drinfeld proof evidence.
-/
def c007PublicBlueprintMergeGate : PublicBlueprintMergeGate where
  checkedBoundaryName := "AwesomeTheorems.Stage1.S1_M_043.StatementShape"
  boundaryStatus := .statementShapeOnly
  requiresIntegratorBoundaryConfirmation := true
  mayMarkTheoremCompleted := false
  publicMergeTarget := "Docs/Stage1_Blueprint.md:719"
  completionBlocker :=
    "integrator must confirm the exact machine-proof boundary before public merge; " ++
    "current file checks only the statement shape and supporting metadata"
  proposedChecklistText :=
    "- [ ] Add a Stage1 child task for THM-M-0124 to merge the local checked " ++
    "statement-shape file into the public blueprint surface only after an integrator " ++
    "confirms the exact machine-proof boundary. Ready-to-merge C007 gate: " ++
    "`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_043.lean` validates " ++
    "`StatementShape` and C005/C006/C007 metadata only; it does not prove " ++
    "Manin-Drinfeld. Public backfill may cite the file as statement-shape evidence, " ++
    "but parent status must remain open / not_repo_local_closed with formalization_debt " ++
    "until a local proof body, pinned mathlib wrapper, or pinned external proof validates."

theorem c007_boundaryStatus_statementShapeOnly :
    c007PublicBlueprintMergeGate.boundaryStatus =
      MachineProofBoundaryStatus.statementShapeOnly :=
  rfl

theorem c007_requiresIntegratorBoundaryConfirmation :
    c007PublicBlueprintMergeGate.requiresIntegratorBoundaryConfirmation = true :=
  rfl

theorem c007_mayNotMarkTheoremCompleted :
    c007PublicBlueprintMergeGate.mayMarkTheoremCompleted = false :=
  rfl

/-- The checked boundary named by the C007 public-backfill gate is `StatementShape`. -/
abbrev C007CheckedStatementShapeBoundary : Prop :=
  StatementShape.{u}

theorem c007_checkedBoundary_iff_statementShape :
    C007CheckedStatementShapeBoundary.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/--
Machine-readable audit record for the external-proof pin/import/check gate.

This is metadata, not mathematical evidence for Manin-Drinfeld.  It exists so the Stage1 child
ledger can point to a checked repo-local declaration recording that no external Lean 4 proof has
yet been discovered and integrated.
-/
structure ExternalProofIntegrationAudit where
  searchedTerms : List String
  discoveredExternalLeanProof : Bool
  authenticatedSourceSearchComplete : Bool
  repoLocalClosureStatus : String
  concreteBlocker : String
  requiredNextStep : String

/--
C005 integration-gate decision: there is currently no discovered external Lean 4 proof to
pin/import/check, and unauthenticated GitHub code search is not enough to close the gate.
-/
def c005ExternalProofIntegrationAudit : ExternalProofIntegrationAudit where
  searchedTerms := [
    "Manin-Drinfeld",
    "manin_drinfeld",
    "cuspidal divisor",
    "modular curve Jacobian"
  ]
  discoveredExternalLeanProof := false
  authenticatedSourceSearchComplete := false
  repoLocalClosureStatus := "not_repo_local_closed"
  concreteBlocker :=
    "no authenticated GitHub code-search session is available; prior REST code search returned 401"
  requiredNextStep :=
    "rerun authenticated source search, then pin/import/check any discovered Lean 4 proof or record a concrete dependency, toolchain, or license blocker"

/-- Specialize the abstract Manin-Drinfeld statement shape to one cusp-class map. -/
theorem statementShape_pairwise (h : StatementShape.{u})
    (Γ : Subgroup (GL (Fin 2) ℝ)) [Γ.IsArithmetic]
    (X : CompactifiedModularCurve.{u} Γ) (M : CuspDivisorClassMap.{u} Γ X) :
    PairwiseCuspDifferenceTorsion M :=
  h Γ X M

/-- Mathlib wrapper: arithmetic subgroups have finitely many cusp orbits. -/
theorem cuspOrbits_finite (Γ : Subgroup (GL (Fin 2) ℝ)) [Γ.IsArithmetic] :
    Finite (CuspOrbits Γ) := by
  infer_instance

/-- Mathlib wrapper: the cusps of `SL(2, Z)` are exactly the rational projective points. -/
theorem cusp_SL2Z_iff_rational {c : OnePoint ℝ} :
    IsCusp c SL2ZInGL2R ↔ c ∈ Set.range (OnePoint.map Rat.cast) := by
  exact isCusp_SL2Z_iff (c := c)

/-- Mathlib wrapper: arithmetic subgroups have the same cusp set as `SL(2, Z)`. -/
theorem arithmetic_isCusp_iff_SL2Z (Γ : Subgroup (GL (Fin 2) ℝ)) [Γ.IsArithmetic]
    {c : OnePoint ℝ} :
    IsCusp c Γ ↔ IsCusp c SL2ZInGL2R := by
  exact Subgroup.IsArithmetic.isCusp_iff_isCusp_SL2Z Γ (c := c)

#check c005ExternalProofIntegrationAudit
#check c006PublicRootStatementDecision
#check c006_selectsCongruenceSubgroup
#check C006CurrentRepoLocalBoundary
#check c006_currentBoundary_iff_statementShape
#check c007PublicBlueprintMergeGate
#check c007_boundaryStatus_statementShapeOnly
#check c007_requiresIntegratorBoundaryConfirmation
#check c007_mayNotMarkTheoremCompleted
#check C007CheckedStatementShapeBoundary
#check c007_checkedBoundary_iff_statementShape

end AwesomeTheorems.Stage1.S1_M_043
