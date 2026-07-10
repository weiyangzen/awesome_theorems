import Mathlib.Analysis.Analytic.IteratedFDeriv
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# S1-M-148 / THM-M-1180: Caffarelli regularity theory

This Stage1 artifact records a conservative Lean 4 statement boundary for Caffarelli-type
interior regularity of the real Monge-Ampere equation.

The pinned mathlib snapshot has finite-dimensional real coordinate spaces, convexity,
`ContDiffOn`, iterated Frechet derivatives, and matrix determinants. It does not expose a
terminal API for Aleksandrov/viscosity Monge-Ampere solutions, sections, Caffarelli localization,
or Schauder-style `C^{2,alpha}` regularity. The declarations below therefore keep the hard PDE
content as hypotheses in a normalized statement shape and provide only low-risk definitional
wrappers around the currently available mathlib objects.
-/

noncomputable section

open Set
open scoped Topology ContDiff

namespace AwesomeTheorems.Stage1.S1_M_148

universe u

/--
Coordinate Hessian entry obtained from mathlib's second iterated Frechet derivative on
`ι -> ℝ`.

This is a classical, coordinate-space expression. It is not an Aleksandrov Hessian measure or a
viscosity-solution definition.
-/
def hessianEntry {ι : Type u} [Fintype ι] [DecidableEq ι]
    (u : (ι -> ℝ) -> ℝ) (x : ι -> ℝ) (i j : ι) : ℝ :=
  iteratedFDeriv ℝ 2 u x
    (fun k : Fin 2 => if k = 0 then Pi.single i (1 : ℝ) else Pi.single j (1 : ℝ))

/-- Coordinate Hessian matrix for a scalar function on finite real coordinate space. -/
def hessianMatrix {ι : Type u} [Fintype ι] [DecidableEq ι]
    (u : (ι -> ℝ) -> ℝ) (x : ι -> ℝ) : Matrix ι ι ℝ :=
  fun i j => hessianEntry u x i j

/--
Classical Monge-Ampere operator represented as the determinant of the coordinate Hessian.

The Stage1 audit uses this only as an object-model anchor. The weak/Aleksandrov solution bridge
needed for Caffarelli's theorem is recorded separately as formalization debt.
-/
def mongeAmpereOperator {ι : Type u} [Fintype ι] [DecidableEq ι]
    (u : (ι -> ℝ) -> ℝ) (x : ι -> ℝ) : ℝ :=
  (hessianMatrix u x).det

/-- Classical pointwise Monge-Ampere equation `det D^2 u = rhs` on a set. -/
def ClassicalMongeAmpereEquation {ι : Type u} [Fintype ι] [DecidableEq ι]
    (u rhs : (ι -> ℝ) -> ℝ) (Ω : Set (ι -> ℝ)) : Prop :=
  ∀ x ∈ Ω, mongeAmpereOperator u x = rhs x

/--
Hypotheses for an interior Caffarelli regularity statement.

The fields split the part available in mathlib (`IsOpen`, `Convex`, `ConvexOn`, `ContinuousOn`,
and the coordinate Monge-Ampere equation) from the missing PDE infrastructure. The abstract
`solution_notion_bridge` and `caffarelli_localization_package` fields mark where a terminal
formalization must supply Aleksandrov/viscosity solution theory, sections, normalization, and
interior estimates.
-/
structure InteriorRegularityHypotheses {ι : Type u} [Fintype ι] [DecidableEq ι]
    (Ω Ω' : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ) : Type u where
  domain_open : IsOpen Ω
  interior_open : IsOpen Ω'
  interior_subset_domain : Ω' ⊆ Ω
  domain_convex : Convex ℝ Ω
  potential_convex : ConvexOn ℝ Ω u
  rhs_continuous : ContinuousOn rhs Ω
  rhs_positive_bounds :
    ∃ lower upper : ℝ, 0 < lower ∧ lower ≤ upper ∧
      ∀ x ∈ Ω, lower ≤ rhs x ∧ rhs x ≤ upper
  classical_pointwise_equation : ClassicalMongeAmpereEquation u rhs Ω
  solution_notion_bridge : Prop
  solution_notion_bridge_proof : solution_notion_bridge
  caffarelli_localization_package : Prop
  caffarelli_localization_package_proof : caffarelli_localization_package

/--
Normalized Stage1 statement shape for a Caffarelli interior regularity theorem.

For every finite real coordinate domain, if the convex potential satisfies the audited
Monge-Ampere hypotheses and the missing weak-solution/localization packages have been supplied,
then the potential is twice continuously differentiable on the chosen interior region.

This is a proposition only. It is not a local proof of Caffarelli regularity.
-/
def StatementShape (ι : Type u) [Fintype ι] [DecidableEq ι] : Prop :=
  ∀ (Ω Ω' : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ),
    InteriorRegularityHypotheses Ω Ω' u rhs -> ContDiffOn ℝ 2 u Ω'

/-- The Monge-Ampere operator unfolds to the determinant of the coordinate Hessian. -/
theorem mongeAmpereOperator_eq_det {ι : Type u} [Fintype ι] [DecidableEq ι]
    (u : (ι -> ℝ) -> ℝ) (x : ι -> ℝ) :
    mongeAmpereOperator u x = (hessianMatrix u x).det :=
  rfl

/-- The classical equation is exactly the pointwise determinant equation on the domain. -/
theorem classicalMongeAmpereEquation_iff {ι : Type u} [Fintype ι] [DecidableEq ι]
    (u rhs : (ι -> ℝ) -> ℝ) (Ω : Set (ι -> ℝ)) :
    ClassicalMongeAmpereEquation u rhs Ω ↔
      ∀ x ∈ Ω, (hessianMatrix u x).det = rhs x :=
  Iff.rfl

/-- Definitional introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro {ι : Type u} [Fintype ι] [DecidableEq ι]
    (h : ∀ (Ω Ω' : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ),
      InteriorRegularityHypotheses Ω Ω' u rhs -> ContDiffOn ℝ 2 u Ω') :
    StatementShape ι :=
  h

/-! ## Solution bridge formalization task -/

/--
Permitted solution-notion routes for the missing bridge from Caffarelli's weak
Monge-Ampere theory to the classical pointwise statement shape above.

This is intentionally a route selector only; it is not a definition of Aleksandrov or viscosity
solutions.
-/
inductive SolutionBridgeRoute where
  | aleksandrov
  | viscosity
deriving DecidableEq, Repr

/--
Machine-checkable task shape for the missing Aleksandrov/viscosity solution bridge.

A future terminal formalization must instantiate this structure for either route by supplying a
solution predicate, proving its compatibility with the classical determinant equation for regular
solutions in the audited coordinate model, and proving that the predicate survives the localization/section
operations used by Caffarelli's proof package.

Keeping these as fields records formalization debt without introducing unsupported assumptions or
pretending that the bridge is currently available in mathlib.
-/
structure SolutionBridgeFormalizationTask {ι : Type u} [Fintype ι] [DecidableEq ι]
    (route : SolutionBridgeRoute) (Ω : Set (ι -> ℝ))
    (u rhs : (ι -> ℝ) -> ℝ) : Type u where
  solutionPredicate :
    ((ι -> ℝ) -> ℝ) -> ((ι -> ℝ) -> ℝ) -> Set (ι -> ℝ) -> Prop
  regular_bridge_to_classical :
    ContDiffOn ℝ 2 u Ω ->
    solutionPredicate u rhs Ω -> ClassicalMongeAmpereEquation u rhs Ω
  classical_to_bridge :
    ClassicalMongeAmpereEquation u rhs Ω -> solutionPredicate u rhs Ω
  stable_under_caffarelli_localization : Prop
  localization_bridge_obligation : stable_under_caffarelli_localization

/-- Aleksandrov route specialization of the solution-bridge formalization task. -/
abbrev AleksandrovSolutionBridgeTask {ι : Type u} [Fintype ι] [DecidableEq ι]
    (Ω : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ) : Type u :=
  SolutionBridgeFormalizationTask SolutionBridgeRoute.aleksandrov Ω u rhs

/-- Viscosity route specialization of the solution-bridge formalization task. -/
abbrev ViscositySolutionBridgeTask {ι : Type u} [Fintype ι] [DecidableEq ι]
    (Ω : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ) : Type u :=
  SolutionBridgeFormalizationTask SolutionBridgeRoute.viscosity Ω u rhs

/--
Open bridge leaf for S1-M-148: supply either an Aleksandrov or viscosity solution package.

This proposition is deliberately not used to close `StatementShape`; it is the integration-ready
Lean target that public planning can reference for `THM-M-1180.solution-bridge`.
-/
def HasAleksandrovOrViscosityBridge {ι : Type u} [Fintype ι] [DecidableEq ι]
    (Ω : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ) : Prop :=
  Nonempty (AleksandrovSolutionBridgeTask Ω u rhs) ∨
    Nonempty (ViscositySolutionBridgeTask Ω u rhs)

/-! ## Caffarelli localization formalization task -/

/--
Machine-checkable task shape for the missing Caffarelli section geometry and normalization
package.

The fields deliberately separate the currently unavailable PDE proof obligations: section
construction, affine normalization, engulfing/covering estimates, compactness/localization, and
transfer of normalized interior estimates back to the original Monge-Ampere problem. Supplying this
structure would not by itself prove `StatementShape`; it records the localization package that a
future terminal proof must combine with a solution-notion bridge and a regularity bootstrap.
-/
structure CaffarelliLocalizationFormalizationTask {ι : Type u} [Fintype ι] [DecidableEq ι]
    (Ω : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ) : Type (u + 1) where
  sectionData : (ι -> ℝ) -> ℝ -> Type u
  sectionSet : ∀ {x : ι -> ℝ} {height : ℝ}, sectionData x height -> Set (ι -> ℝ)
  section_exists : ∀ x ∈ Ω, ∀ height : ℝ, 0 < height -> Nonempty (sectionData x height)
  section_center_mem :
    ∀ {x : ι -> ℝ} {height : ℝ} (_data : sectionData x height), x ∈ Ω
  section_height_pos :
    ∀ {x : ι -> ℝ} {height : ℝ} (_data : sectionData x height), 0 < height
  section_subset_domain :
    ∀ {x : ι -> ℝ} {height : ℝ} (data : sectionData x height), sectionSet data ⊆ Ω
  section_convex :
    ∀ {x : ι -> ℝ} {height : ℝ} (data : sectionData x height),
      Convex ℝ (sectionSet data)
  normalizationData :
    ∀ {x : ι -> ℝ} {height : ℝ}, sectionData x height -> Type u
  normalizedSet :
    ∀ {x : ι -> ℝ} {height : ℝ} {data : sectionData x height},
      normalizationData data -> Set (ι -> ℝ)
  normalizingMap :
    ∀ {x : ι -> ℝ} {height : ℝ} {data : sectionData x height},
      normalizationData data -> (ι -> ℝ) -> (ι -> ℝ)
  inverseNormalizingMap :
    ∀ {x : ι -> ℝ} {height : ℝ} {data : sectionData x height},
      normalizationData data -> (ι -> ℝ) -> (ι -> ℝ)
  normalization_exists :
    ∀ {x : ι -> ℝ} {height : ℝ} (data : sectionData x height),
      Nonempty (normalizationData data)
  maps_section_to_normalized : Prop
  maps_normalized_to_section : Prop
  normalized_geometry_bounds : Prop
  affine_monge_ampere_invariance : Prop
  engulfing_or_covering_estimate : Prop
  compactness_localization_estimate : Prop
  normalized_interior_estimate_transfer : Prop
  maps_section_to_normalized_proof : maps_section_to_normalized
  maps_normalized_to_section_proof : maps_normalized_to_section
  normalized_geometry_bounds_proof : normalized_geometry_bounds
  affine_monge_ampere_invariance_proof : affine_monge_ampere_invariance
  engulfing_or_covering_estimate_proof : engulfing_or_covering_estimate
  compactness_localization_estimate_proof : compactness_localization_estimate
  normalized_interior_estimate_transfer_proof : normalized_interior_estimate_transfer

/--
Open localization leaf for S1-M-148: supply the Caffarelli sections, normalization, and
localization estimates needed by the interior regularity proof package.
-/
def HasCaffarelliLocalizationPackage {ι : Type u} [Fintype ι] [DecidableEq ι]
    (Ω : Set (ι -> ℝ)) (u rhs : (ι -> ℝ) -> ℝ) : Prop :=
  Nonempty (CaffarelliLocalizationFormalizationTask Ω u rhs)

/-! ## Regularity target decision -/

/--
Candidate regularity targets considered for the first terminal Lean theorem in this slot.

The selector is audit metadata: it does not assert any of the PDE estimates.
-/
inductive RegularityTargetChoice where
  | c1Holder
  | w2p
  | c2Holder
  | contDiffOnTwoSurrogate
deriving DecidableEq, Repr

/--
Decision for `THM-M-1180.regularity-target`.

The first repo-local terminal target should be the current `ContDiffOn ℝ 2` statement-shape
surrogate, because it maps directly to available mathlib APIs and avoids claiming Holder or
Sobolev regularity before the Aleksandrov/viscosity bridge, Caffarelli localization package, and
interior estimate stack exist in Lean.
-/
def firstTerminalRegularityTarget : RegularityTargetChoice :=
  RegularityTargetChoice.contDiffOnTwoSurrogate

/--
Textual audit note for the selected first terminal regularity target.

`C^{1,alpha}`, `W^{2,p}`, and `C^{2,alpha}` remain later targets; they require additional Holder or
Sobolev endpoint APIs and the missing nonlinear Monge-Ampere proof packages before this Stage1 item
can be marked terminally closed.
-/
def firstTerminalRegularityTargetRationale : String :=
  "first target: local ContDiffOn R 2 surrogate; C1-alpha, W2p, and C2-alpha remain formalization-debt branches"

/-- Checked metadata equation for the regularity-target decision. -/
theorem firstTerminalRegularityTarget_eq :
    firstTerminalRegularityTarget = RegularityTargetChoice.contDiffOnTwoSurrogate :=
  rfl

/-- Checked metadata equation for the regularity-target rationale. -/
theorem firstTerminalRegularityTargetRationale_eq :
    firstTerminalRegularityTargetRationale =
      "first target: local ContDiffOn R 2 surrogate; C1-alpha, W2p, and C2-alpha remain formalization-debt branches" :=
  rfl

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Analytic.IteratedFDeriv",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Normed.Module.Convex",
  "Mathlib.LinearAlgebra.Matrix.Determinant.Basic",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic"
]

/-- Repository-local Lean toolchain used for the S1-M-148 audit. -/
def auditedLeanToolchain : String := "leanprover/lean4:v4.29.0"

/-- Pinned mathlib revision recorded in `Formalizations/Lean/lake-manifest.json`. -/
def auditedMathlibRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Pinned mathlib repository recorded in `Formalizations/Lean/lake-manifest.json`. -/
def auditedMathlibRepository : String := "https://github.com/leanprover-community/mathlib4.git"

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "iteratedFDeriv",
  "ContDiffOn",
  "Convex",
  "ConvexOn",
  "ContinuousOn",
  "Matrix.det",
  "Pi.single",
  "Distribution",
  "TestFunction",
  "gagliardo_nirenberg_sobolev"
]

/-- Search terms that did not locate a terminal Caffarelli/Monge-Ampere theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Caffarelli",
  "MongeAmpere",
  "Monge-Ampere",
  "Aleksandrov solution",
  "viscosity solution",
  "Caffarelli localization",
  "Caffarelli sections",
  "normalized sections",
  "section geometry",
  "linearized Monge Ampere"
]

/-! ## Integration gate metadata -/

/--
Current machine status for this Stage1 artifact.

The statement shape and audit metadata check locally, but this is not a terminal proof of
Caffarelli regularity.
-/
def machineStatus : String :=
  "statement_shape_local_checked_not_terminal"

/-- Whether this artifact proves the terminal Caffarelli regularity theorem. -/
def terminalTheoremCompleted : Bool :=
  false

/--
Whether this artifact leaves a known external Lean theorem as anchor-only debt while claiming
completion.

The value is `false` because no completion is claimed here. If a future audit locates an external
Lean proof, the integration gate must switch to pin/import/check or record a concrete blocker.
-/
def repoLocalIntegrationDebtResidueInCompletedState : Bool :=
  false

/-- Integration gate status requested by child task `S1-M-148-C006`. -/
def integrationGateStatus : String :=
  "open until a terminal Lean theorem is locally proved or a pinned dependency wrapper validates"

/-- Remaining terminal leaves for the integration gate. -/
def integrationGateRemainingLeaves : List String := [
  "Aleksandrov or viscosity Monge-Ampere solution API",
  "bridge from weak solution notion to classical determinant equation",
  "Caffarelli section geometry and affine normalization package",
  "engulfing covering compactness localization estimates",
  "interior regularity bootstrap to the selected ContDiffOn or stronger target",
  "repo-local terminal theorem or pinned external dependency wrapper",
  "serial public blueprint and todo backfill after validation"
]

/-- Checked metadata equation for the nonterminal machine status. -/
theorem machineStatus_eq :
    machineStatus = "statement_shape_local_checked_not_terminal" :=
  rfl

/-- Checked metadata equation preventing this artifact from being read as terminal completion. -/
theorem terminalTheoremCompleted_eq_false :
    terminalTheoremCompleted = false :=
  rfl

/-- Checked metadata equation for the repo-local integration-debt completion gate. -/
theorem repoLocalIntegrationDebtResidueInCompletedState_eq_false :
    repoLocalIntegrationDebtResidueInCompletedState = false :=
  rfl

/-- Checked metadata equation for the integration gate status. -/
theorem integrationGateStatus_eq :
    integrationGateStatus =
      "open until a terminal Lean theorem is locally proved or a pinned dependency wrapper validates" :=
  rfl

/-- Checked metadata equation for the remaining integration-gate leaves. -/
theorem integrationGateRemainingLeaves_eq :
    integrationGateRemainingLeaves = [
      "Aleksandrov or viscosity Monge-Ampere solution API",
      "bridge from weak solution notion to classical determinant equation",
      "Caffarelli section geometry and affine normalization package",
      "engulfing covering compactness localization estimates",
      "interior regularity bootstrap to the selected ContDiffOn or stronger target",
      "repo-local terminal theorem or pinned external dependency wrapper",
      "serial public blueprint and todo backfill after validation"
    ] :=
  rfl

/-! ## Audit probes -/

#check hessianEntry
#check hessianMatrix
#check mongeAmpereOperator
#check ClassicalMongeAmpereEquation
#check InteriorRegularityHypotheses
#check StatementShape
#check mongeAmpereOperator_eq_det
#check classicalMongeAmpereEquation_iff
#check SolutionBridgeRoute
#check SolutionBridgeFormalizationTask
#check AleksandrovSolutionBridgeTask
#check ViscositySolutionBridgeTask
#check HasAleksandrovOrViscosityBridge
#check CaffarelliLocalizationFormalizationTask
#check HasCaffarelliLocalizationPackage
#check RegularityTargetChoice
#check firstTerminalRegularityTarget
#check firstTerminalRegularityTarget_eq
#check firstTerminalRegularityTargetRationale_eq
#check auditedLeanToolchain
#check auditedMathlibRevision
#check auditedMathlibRepository
#check machineStatus
#check terminalTheoremCompleted
#check repoLocalIntegrationDebtResidueInCompletedState
#check integrationGateStatus
#check integrationGateRemainingLeaves
#check machineStatus_eq
#check terminalTheoremCompleted_eq_false
#check repoLocalIntegrationDebtResidueInCompletedState_eq_false
#check integrationGateStatus_eq
#check integrationGateRemainingLeaves_eq

end AwesomeTheorems.Stage1.S1_M_148
