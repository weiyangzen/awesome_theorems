import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.Normed.Module.WeakDual
import Mathlib.Analysis.Normed.Operator.Compact
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.Topology.Compactification.OnePoint.Basic
import Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli
import Mathlib.Topology.Sequences
import Mathlib.Topology.UniformSpace.Ascoli

/-!
# S1-M-174 / THM-M-1294: global compactness

This Stage1 file records a conservative Lean 4 boundary for the source item
"global compactness", glossed in the Stage1 queue as compactifying noncompact
PDE problems.

The pinned mathlib snapshot contains strong adjacent compactness infrastructure:
one-point compactification, compact images under continuous maps, compact
operators on normed spaces, Arzela-Ascoli, distribution objects, and a
Gagliardo-Nirenberg-Sobolev inequality.  This file does not assert a terminal
PDE compactness theorem.  Instead it freezes a normalized statement shape in
which the PDE equation, energy estimate, weak formulation bridge, and
regularity branch remain explicit proof packages for later replacement.
-/

noncomputable section

open MeasureTheory
open Filter Set
open scoped ENNReal Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_174

universe u v

/--
Candidate readings for the ambiguous source phrase "global compactness".

The source queue places THM-M-1294 in a PDE cluster next to Struwe compactness,
Lions concentration compactness, bubble decomposition, and profile
decomposition.  Therefore this slot should not be normalized as a bare
topological compactification theorem unless a later source audit overturns
that context.
-/
inductive GlobalCompactnessVariant where
  | topologicalOnePoint
  | compactOperatorClosedBall
  | arzelaAscoliEquicontinuity
  | weakStarDualBall
  | prokhorovTightness
  | aubinLionsEvolutionCompactness
  | rellichKondrachovCompactEmbedding
  | struweLionsPalaisSmaleBubbleDecomposition
  deriving DecidableEq, Repr

/--
Statement-normalization choice for `THM-M-1294`.

The intended mathematical variant is the PDE-specific Struwe/Lions global
compactness principle: bounded Palais-Smale or critical-growth approximation
sequences are compact only after extracting a weak limit and finitely/countably
many concentration bubbles/profiles.  This is compactness modulo defect
profiles, not the coarse `OnePoint` compactification, not compact-operator
compactness, not Arzela-Ascoli alone, not weak-star compactness alone, not
Prokhorov tightness alone, and not a plain Rellich/Aubin-Lions theorem.
-/
def selectedGlobalCompactnessVariant : GlobalCompactnessVariant :=
  GlobalCompactnessVariant.struweLionsPalaisSmaleBubbleDecomposition

/-- Checked witness for the selected statement-normalization branch. -/
theorem selectedGlobalCompactnessVariant_eq :
    selectedGlobalCompactnessVariant =
      GlobalCompactnessVariant.struweLionsPalaisSmaleBubbleDecomposition :=
  rfl

/--
Human-readable non-target list for public backfill.

These compactness tools may be auxiliary branches in a future proof, but they
are not the normalized root theorem selected for THM-M-1294.
-/
def nonTargetVariantLabels : List String := [
  "one-point compactification as terminal theorem",
  "compact-operator closed-ball compactness as terminal theorem",
  "Arzela-Ascoli equicontinuity compactness as terminal theorem",
  "weak-star dual-ball compactness as terminal theorem",
  "Prokhorov/tightness compactness as terminal theorem",
  "Aubin-Lions evolution compactness as terminal theorem",
  "Rellich-Kondrachov compact embedding as terminal theorem"
]

/--
Selected compactness mechanism for the normalized Struwe/Lions reading.

The terminal theorem is not ordinary one-point compactification.  The selected
mechanism is a profile or bubble compactification: the raw PDE state is mapped
into a compact profile-configuration space that records the weak limit together
with concentration defects.  Later children must replace the current abstract
fields with the actual PDE profile parameters, extraction theorem, energy
splitting, and limit-passage package.
-/
structure ProfileCompactnessMechanism
    (State : Type u) [TopologicalSpace State] : Type (max u (v + 1)) where
  Compactified : Type v
  compactifiedTopologicalSpace : TopologicalSpace Compactified
  compactifiedCompactSpace : CompactSpace Compactified
  compactificationMap : State → Compactified
  compactificationMap_continuous : by
    letI := compactifiedTopologicalSpace
    exact Continuous compactificationMap
  profilePayload : Type v
  mechanismLabel : String

/--
The compactness theorem carried by a selected profile compactness mechanism.

This is repo-local evidence that `GlobalCompactnessProblem` no longer quantifies
over an arbitrary `Compactified` parameter.  It does not prove the missing
Struwe/Lions extraction theorem; the compact profile space itself is still a
package to be instantiated by the PDE model.
-/
theorem profileCompactification_univ_isCompact
    {State : Type u} [TopologicalSpace State]
    (M : ProfileCompactnessMechanism.{u, v} State) :
    letI := M.compactifiedTopologicalSpace
    IsCompact (Set.univ : Set M.Compactified) := by
  letI := M.compactifiedTopologicalSpace
  letI := M.compactifiedCompactSpace
  exact isCompact_univ

/-- The compactification map supplied by a profile compactness mechanism is continuous. -/
theorem profileCompactificationMap_continuous
    {State : Type u} [TopologicalSpace State]
    (M : ProfileCompactnessMechanism.{u, v} State) :
    letI := M.compactifiedTopologicalSpace
    Continuous M.compactificationMap := by
  letI := M.compactifiedTopologicalSpace
  exact M.compactificationMap_continuous

/--
Auxiliary one-point compactification mechanism.

This is included as a checked comparison branch and imported compactness witness.
It is not the selected terminal interpretation of THM-M-1294.
-/
def onePointAuxiliaryMechanism
    (State : Type u) [TopologicalSpace State] :
    ProfileCompactnessMechanism.{u, u} State where
  Compactified := OnePoint State
  compactifiedTopologicalSpace := inferInstance
  compactifiedCompactSpace := inferInstance
  compactificationMap := ((↑) : State → OnePoint State)
  compactificationMap_continuous := OnePoint.continuous_coe
  profilePayload := PUnit
  mechanismLabel := "auxiliary one-point compactification, not terminal Struwe/Lions compactness"

/--
Concrete checked compactness for the auxiliary one-point mechanism.

The selected PDE profile mechanism must eventually supply an analogous
compactness theorem for its profile-configuration space.
-/
theorem onePointAuxiliaryMechanism_univ_isCompact
    (State : Type u) [TopologicalSpace State] :
    letI := (onePointAuxiliaryMechanism State).compactifiedTopologicalSpace
    IsCompact (Set.univ : Set (onePointAuxiliaryMechanism State).Compactified) :=
  profileCompactification_univ_isCompact (onePointAuxiliaryMechanism State)

/--
Data for a global compactness theorem after the compactification-model child.

`State` is the original, usually noncompact, PDE state space.  `M` is the
selected compactness mechanism; for the normalized theorem it must become a
profile/bubble compactification rather than a freely quantified target type.
The proposition-valued fields mark the currently missing PDE packages: they
must eventually be replaced by concrete weak-solution, boundary-condition,
energy, and regularity statements rather than treated as completed proof
content.
-/
structure GlobalCompactnessProblem
    (State : Type u) [TopologicalSpace State]
    (M : ProfileCompactnessMechanism.{u, v} State) : Type (max u v) where
  approximants : ℕ → State
  admissible : State → Prop
  weakFormulation : State → Prop
  boundaryCondition : State → Prop
  energyBound : Prop
  tightnessOrCoercivity : Prop
  regularityOrEquicontinuity : Prop
  weakClassicalBridge : Prop
  limitCandidate : M.Compactified
  limitSolvesProblem : Prop

/-! ## Concrete PDE object model for child C005 -/

/-- Euclidean spatial domain used by the concrete PDE state-space boundary. -/
abbrev PDESpace (n : ℕ) : Type :=
  EuclideanSpace ℝ (Fin n)

/-- Space-time domain for the concrete PDE model. -/
abbrev PDESpaceTime (n : ℕ) : Type :=
  ℝ × PDESpace n

/--
Concrete scalar PDE states over Euclidean space-time.

This is intentionally a function-space boundary, not a Sobolev-space API.  The
current mathlib snapshot supplies `MemLp`, distributions, and test functions,
but no terminal Struwe/Lions global compactness theorem or profile-space API.
-/
abbrev PDEState (n : ℕ) : Type :=
  PDESpaceTime n → ℝ

/-- The whole Euclidean space-time domain as a mathlib open set. -/
def wholePDESpaceTimeOpen (n : ℕ) : TopologicalSpace.Opens (PDESpaceTime n) :=
  ⟨Set.univ, isOpen_univ⟩

/-- Scalar test functions for weak PDE residuals on the whole space-time domain. -/
abbrev PDEScalarTestFunction (n : ℕ) : Type :=
  TestFunction (wholePDESpaceTimeOpen n) ℝ ⊤

/-- Scalar distributions for weak PDE residuals on the whole space-time domain. -/
abbrev PDEScalarDistribution (n : ℕ) : Type :=
  Distribution (wholePDESpaceTimeOpen n) ℝ ⊤

/--
Concrete admissibility data for a PDE state.

The mandatory part is a mathlib `MemLp` condition for a chosen measure and
exponent.  `sideCondition` records equation-specific membership constraints
that mathlib does not currently bundle as a named Sobolev/profile space.
-/
structure PDEAdmissibilityData (n : ℕ) where
  exponent : ℝ≥0∞
  measure : Measure (PDESpaceTime n)
  sideCondition : PDEState n → Prop

/-- Concrete admissibility predicate for the C005 PDE model. -/
def IsPDEAdmissible {n : ℕ} (A : PDEAdmissibilityData n) (u : PDEState n) : Prop :=
  MemLp u A.exponent A.measure ∧ A.sideCondition u

/--
Weak/distributional formulation data for the concrete PDE model.

`residual u` is a scalar distribution; the weak equation says that it evaluates
to zero on every compactly supported smooth test function.
-/
structure PDEWeakFormulationData (n : ℕ) where
  residual : PDEState n → PDEScalarDistribution n

/-- Concrete weak formulation predicate using mathlib distributions and test functions. -/
def SatisfiesPDEWeakFormulation {n : ℕ}
    (W : PDEWeakFormulationData n) (u : PDEState n) : Prop :=
  ∀ φ : PDEScalarTestFunction n, W.residual u φ = 0

/--
Boundary-condition data for the concrete PDE model.

The explicit `boundarySet`, `boundaryValue`, and `trace` fields keep the
Dirichlet/trace boundary condition in concrete function-space terms while
leaving the analytic trace theorem as a later proof package.
-/
structure PDEBoundaryData (n : ℕ) where
  boundarySet : Set (PDESpaceTime n)
  boundaryValue : PDESpaceTime n → ℝ
  trace : PDEState n → PDESpaceTime n → ℝ

/-- Concrete boundary-condition predicate attached to `PDEBoundaryData`. -/
def SatisfiesPDEBoundaryCondition {n : ℕ}
    (B : PDEBoundaryData n) (u : PDEState n) : Prop :=
  ∀ z : PDESpaceTime n, z ∈ B.boundarySet → B.trace u z = B.boundaryValue z

/--
Concrete PDE model package for the global compactness statement boundary.

The limit predicate combines the concrete state-space, admissibility,
weak-formulation, and boundary-condition objects with one extra regularity
predicate reserved for the selected Struwe/Lions profile compactness branch.
-/
structure ConcretePDEModel (n : ℕ) where
  admissibility : PDEAdmissibilityData n
  weakFormulation : PDEWeakFormulationData n
  boundaryCondition : PDEBoundaryData n
  extraLimitRegularity : PDEState n → Prop

/-- Concrete limit-solution predicate for a PDE state. -/
def IsPDELimitSolution {n : ℕ} (D : ConcretePDEModel n) (u : PDEState n) : Prop :=
  IsPDEAdmissible D.admissibility u ∧
    SatisfiesPDEWeakFormulation D.weakFormulation u ∧
      SatisfiesPDEBoundaryCondition D.boundaryCondition u ∧
        D.extraLimitRegularity u

/-- `IsPDEAdmissible` exposes its concrete `MemLp` component. -/
theorem IsPDEAdmissible.memLp {n : ℕ} {A : PDEAdmissibilityData n}
    {u : PDEState n} (h : IsPDEAdmissible A u) :
    MemLp u A.exponent A.measure :=
  h.1

/-- `IsPDEAdmissible` exposes the equation-specific side condition. -/
theorem IsPDEAdmissible.sideCondition {n : ℕ} {A : PDEAdmissibilityData n}
    {u : PDEState n} (h : IsPDEAdmissible A u) :
    A.sideCondition u :=
  h.2

/-- The concrete weak formulation unfolds to residual vanishing on test functions. -/
theorem satisfiesPDEWeakFormulation_iff {n : ℕ}
    (W : PDEWeakFormulationData n) (u : PDEState n) :
    SatisfiesPDEWeakFormulation W u ↔
      ∀ φ : PDEScalarTestFunction n, W.residual u φ = 0 :=
  Iff.rfl

/-- The concrete boundary condition unfolds to the stored trace equality. -/
theorem satisfiesPDEBoundaryCondition_iff {n : ℕ}
    (B : PDEBoundaryData n) (u : PDEState n) :
    SatisfiesPDEBoundaryCondition B u ↔
      ∀ z : PDESpaceTime n, z ∈ B.boundarySet → B.trace u z = B.boundaryValue z :=
  Iff.rfl

/-- A concrete limit solution is admissible. -/
theorem IsPDELimitSolution.admissible {n : ℕ} {D : ConcretePDEModel n}
    {u : PDEState n} (h : IsPDELimitSolution D u) :
    IsPDEAdmissible D.admissibility u :=
  h.1

/-- A concrete limit solution satisfies the weak formulation. -/
theorem IsPDELimitSolution.weakFormulation {n : ℕ} {D : ConcretePDEModel n}
    {u : PDEState n} (h : IsPDELimitSolution D u) :
    SatisfiesPDEWeakFormulation D.weakFormulation u :=
  h.2.1

/-- A concrete limit solution satisfies the boundary condition. -/
theorem IsPDELimitSolution.boundaryCondition {n : ℕ} {D : ConcretePDEModel n}
    {u : PDEState n} (h : IsPDELimitSolution D u) :
    SatisfiesPDEBoundaryCondition D.boundaryCondition u :=
  h.2.2.1

/-- A concrete limit solution has the extra regularity required by the chosen PDE branch. -/
theorem IsPDELimitSolution.extraLimitRegularity {n : ℕ} {D : ConcretePDEModel n}
    {u : PDEState n} (h : IsPDELimitSolution D u) :
    D.extraLimitRegularity u :=
  h.2.2.2

/--
Concrete PDE global-compactness problem over the checked Euclidean state space.

This packages the C005 instantiation and adapts it to the abstract
`GlobalCompactnessProblem` surface without claiming the missing compactness,
coercivity, or limit-passage theorems.
-/
structure ConcretePDEGlobalCompactnessProblem (n : ℕ)
    (M : ProfileCompactnessMechanism.{0, v} (PDEState n)) : Type (v + 1) where
  model : ConcretePDEModel n
  approximants : ℕ → PDEState n
  energyBound : Prop
  tightnessOrCoercivity : Prop
  regularityOrEquicontinuity : Prop
  weakClassicalBridge : Prop
  limitCandidate : M.Compactified
  compactifiedLimitSolves : M.Compactified → Prop

/-- Adapter from the concrete PDE model into the generic global compactness interface. -/
def ConcretePDEGlobalCompactnessProblem.toGlobalCompactnessProblem
    {n : ℕ} {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) :
    GlobalCompactnessProblem (PDEState n) M where
  approximants := P.approximants
  admissible := IsPDEAdmissible P.model.admissibility
  weakFormulation := SatisfiesPDEWeakFormulation P.model.weakFormulation
  boundaryCondition := SatisfiesPDEBoundaryCondition P.model.boundaryCondition
  energyBound := P.energyBound
  tightnessOrCoercivity := P.tightnessOrCoercivity
  regularityOrEquicontinuity := P.regularityOrEquicontinuity
  weakClassicalBridge := P.weakClassicalBridge
  limitCandidate := P.limitCandidate
  limitSolvesProblem := P.compactifiedLimitSolves P.limitCandidate

/-- The adapter uses the concrete `MemLp`-based admissibility predicate. -/
theorem concretePDE_toGlobal_admissible {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) (u : PDEState n) :
    P.toGlobalCompactnessProblem.admissible u ↔
      IsPDEAdmissible P.model.admissibility u :=
  Iff.rfl

/-- The adapter uses the concrete distributional weak formulation predicate. -/
theorem concretePDE_toGlobal_weakFormulation {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) (u : PDEState n) :
    P.toGlobalCompactnessProblem.weakFormulation u ↔
      SatisfiesPDEWeakFormulation P.model.weakFormulation u :=
  Iff.rfl

/-- The adapter uses the concrete trace-style boundary predicate. -/
theorem concretePDE_toGlobal_boundaryCondition {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) (u : PDEState n) :
    P.toGlobalCompactnessProblem.boundaryCondition u ↔
      SatisfiesPDEBoundaryCondition P.model.boundaryCondition u :=
  Iff.rfl

/-- The adapter transports the compactified limit-solution predicate. -/
theorem concretePDE_toGlobal_limitSolvesProblem {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) :
    P.toGlobalCompactnessProblem.limitSolvesProblem ↔
      P.compactifiedLimitSolves P.limitCandidate :=
  Iff.rfl

/-- M0387-level child leaves for the C005 concrete PDE model split. -/
inductive PDEModelLeaf : Type where
  | stateSpace
  | admissibilityPredicate
  | weakFormulationPredicate
  | boundaryConditionPredicate
  | limitSolutionPredicate
  | abstractProblemAdapter
  deriving DecidableEq, Repr

/-- Stable public id for each C005 PDE-model leaf. -/
def PDEModelLeaf.stableId : PDEModelLeaf → String
  | .stateSpace => "S1-M-174-C005-L01.state_space"
  | .admissibilityPredicate => "S1-M-174-C005-L02.admissibility_predicate"
  | .weakFormulationPredicate => "S1-M-174-C005-L03.weak_formulation"
  | .boundaryConditionPredicate => "S1-M-174-C005-L04.boundary_condition"
  | .limitSolutionPredicate => "S1-M-174-C005-L05.limit_solution_predicate"
  | .abstractProblemAdapter => "S1-M-174-C005-L06.abstract_problem_adapter"

/-- Local proof-step budget for each C005 PDE-model leaf. -/
def PDEModelLeaf.proofStepBudget : PDEModelLeaf → Nat
  | .stateSpace => 25
  | .admissibilityPredicate => 35
  | .weakFormulationPredicate => 40
  | .boundaryConditionPredicate => 35
  | .limitSolutionPredicate => 45
  | .abstractProblemAdapter => 45

/-- Every C005 local child leaf is budgeted at `<= 100` steps. -/
theorem PDEModelLeaf.proofStepBudget_le_100 (leaf : PDEModelLeaf) :
    leaf.proofStepBudget ≤ 100 := by
  cases leaf <;> decide

/-- Ordered C005 theorem-tree leaves for the concrete PDE model package. -/
def pdeModelLeaves : List PDEModelLeaf := [
  .stateSpace,
  .admissibilityPredicate,
  .weakFormulationPredicate,
  .boundaryConditionPredicate,
  .limitSolutionPredicate,
  .abstractProblemAdapter
]

/-- The C005 PDE-model package has six budgeted leaves. -/
theorem pdeModelLeaves_length : pdeModelLeaves.length = 6 :=
  rfl

/-- Repo-local theorem-tree package metadata for child C005. -/
structure PDEModelTheoremTree where
  root : String
  leaves : List PDEModelLeaf
  allLeavesBudgeted : ∀ leaf ∈ leaves, leaf.proofStepBudget ≤ 100
  completionStatus : String

/--
C005 closes the concrete object-model interface only.  The terminal global
compactness proof remains open formalization debt.
-/
def c005PDEModelTheoremTree : PDEModelTheoremTree where
  root := "concrete PDE object model for the Struwe/Lions global compactness boundary"
  leaves := pdeModelLeaves
  allLeavesBudgeted := by
    intro leaf _hleaf
    exact PDEModelLeaf.proofStepBudget_le_100 leaf
  completionStatus := "object_model_checked_terminal_compactness_still_formalization_debt"

/-- The C005 theorem-tree metadata records six leaves. -/
theorem c005PDEModelTheoremTree_leaf_count :
    c005PDEModelTheoremTree.leaves.length = 6 :=
  rfl

/-- The compactified subsequential-convergence conclusion expected from compactness. -/
def HasCompactifiedSubsequence
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    (P : GlobalCompactnessProblem State M) : Prop :=
  letI := M.compactifiedTopologicalSpace
  ∃ phi : ℕ → ℕ,
    StrictMono phi ∧
      Tendsto
        (fun k => M.compactificationMap (P.approximants (phi k)))
        atTop
        (𝓝 P.limitCandidate)

/-- The abstract PDE-side hypotheses that a terminal formalization must discharge. -/
def GlobalCompactnessHypotheses
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    (P : GlobalCompactnessProblem State M) : Prop :=
  (∀ n, P.admissible (P.approximants n)) ∧
    (∀ n, P.weakFormulation (P.approximants n)) ∧
      (∀ n, P.boundaryCondition (P.approximants n)) ∧
        P.energyBound ∧
          P.tightnessOrCoercivity ∧
            P.regularityOrEquicontinuity ∧
              P.weakClassicalBridge

/--
Normalized Stage1 statement shape for global compactness.

For every explicit profile compactness mechanism over a PDE state space,
admissible approximants satisfying the weak equation, boundary conditions,
energy control, tightness/coercivity, regularity/equicontinuity, and
weak/classical bridge packages yield a compactified/profile convergent
subsequence whose limit solves the problem.  The proposition is intentionally a
statement boundary, not a proof.
-/
def StatementShape : Prop :=
  ∀ (State : Type u) [TopologicalSpace State]
    (M : ProfileCompactnessMechanism.{u, v} State)
    (P : GlobalCompactnessProblem State M),
      GlobalCompactnessHypotheses P →
        HasCompactifiedSubsequence P ∧ P.limitSolvesProblem

/--
Selected Stage1 statement boundary after statement normalization.

This is still the abstract `StatementShape`: the child pass has selected the
Struwe/Lions bubble-decomposition variant, but the concrete PDE state space,
profile space, bubble parameters, energy splitting, and limit-passage theorem
are not yet implemented.
-/
def SelectedStatementShape : Prop :=
  StatementShape.{u, v}

/-- The selected boundary is definitionally the current statement shape. -/
theorem selectedStatementShape_eq_statementShape :
    @SelectedStatementShape.{u, v} ↔ @StatementShape.{u, v} :=
  by
    unfold SelectedStatementShape
    rfl

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_problem :
    @StatementShape.{u, v} ↔
      ∀ (State : Type u) [TopologicalSpace State]
        (M : ProfileCompactnessMechanism.{u, v} State)
        (P : GlobalCompactnessProblem State M),
          GlobalCompactnessHypotheses P →
            HasCompactifiedSubsequence P ∧ P.limitSolvesProblem :=
  by
    unfold StatementShape
    rfl

/-- mathlib compactification anchor: `OnePoint X` is compact for any topological space `X`. -/
theorem onePoint_compactSpace (X : Type u) [TopologicalSpace X] :
    CompactSpace (OnePoint X) := by
  infer_instance

/-- mathlib compactification anchor: the canonical map into `OnePoint X` is continuous. -/
theorem onePoint_continuous_coe (X : Type u) [TopologicalSpace X] :
    Continuous ((↑) : X → OnePoint X) :=
  OnePoint.continuous_coe

/--
mathlib compactification anchor: for a noncompact space, the original space is
dense in its one-point compactification.
-/
theorem onePoint_denseRange_coe
    (X : Type u) [TopologicalSpace X] [NoncompactSpace X] :
    DenseRange ((↑) : X → OnePoint X) :=
  OnePoint.denseRange_coe

/-- General compactness anchor: compact sets have compact continuous images. -/
theorem compact_image_of_continuous
    {X : Type u} {Y : Type v} [TopologicalSpace X] [TopologicalSpace Y]
    {s : Set X} {f : X → Y} (hs : IsCompact s) (hf : Continuous f) :
    IsCompact (f '' s) :=
  hs.image hf

/--
Sequential compactness anchor available in pseudo-metrizable spaces.

This is often the local form wanted for compactness extractions from
approximating sequences.
-/
theorem compact_iff_seqCompact
    {X : Type u} [TopologicalSpace X] [TopologicalSpace.PseudoMetrizableSpace X]
    {s : Set X} :
    IsCompact s ↔ IsSeqCompact s :=
  isCompact_iff_isSeqCompact

/--
Compact-operator anchor: a compact linear operator maps closed balls into a
subset of a compact set.
-/
theorem compactOperator_image_closedBall_subset_compact
    {E : Type u} {F : Type v}
    [SeminormedAddCommGroup E] [NormedSpace ℝ E]
    [SeminormedAddCommGroup F] [NormedSpace ℝ F]
    (T : E →L[ℝ] F) (hT : IsCompactOperator T) (r : ℝ) :
    ∃ K : Set F, IsCompact K ∧ T '' Metric.closedBall (0 : E) r ⊆ K :=
  hT.image_closedBall_subset_compact r

/-- Weak-star compactness anchor: Banach-Alaoglu for weak-dual closed balls. -/
theorem weakDual_isCompact_closedBall
    {𝕜 : Type u} [NontriviallyNormedField 𝕜] [ProperSpace 𝕜]
    {E : Type v} [SeminormedAddCommGroup E] [NormedSpace 𝕜 E]
    (x' : StrongDual 𝕜 E) (r : ℝ) :
    IsCompact (WeakDual.toStrongDual ⁻¹' Metric.closedBall x' r) :=
  WeakDual.isCompact_closedBall x' r

/-- Weak-star compactness anchor: Banach-Alaoglu for polars of neighborhoods of zero. -/
theorem weakDual_isCompact_polar
    {𝕜 : Type u} [NontriviallyNormedField 𝕜] [ProperSpace 𝕜]
    {E : Type v} [SeminormedAddCommGroup E] [NormedSpace 𝕜 E]
    {s : Set E} (hs : s ∈ 𝓝 (0 : E)) :
    IsCompact (WeakDual.polar 𝕜 s) :=
  WeakDual.isCompact_polar 𝕜 hs

/-! ## Energy/coercivity interface for child C006 -/

/--
Generic energy/coercivity branch for the selected global compactness boundary.

The branch records an explicit real-valued energy functional, a level bound,
and the two proof bridges that the selected PDE must eventually provide:
the uniform estimate must discharge both `P.energyBound` and
`P.tightnessOrCoercivity`.  This is a checked interface, not the missing
Struwe/Lions energy estimate or profile-tightness theorem.
-/
structure EnergyCoercivityBranch
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    (P : GlobalCompactnessProblem State M) where
  energy : State → ℝ
  level : ℝ
  approximants_energy_le : ∀ n, energy (P.approximants n) ≤ level
  estimateDischargesEnergyBound :
    (∀ n, energy (P.approximants n) ≤ level) → P.energyBound
  estimateDischargesTightnessOrCoercivity :
    (∀ n, energy (P.approximants n) ≤ level) → P.tightnessOrCoercivity
  branchLabel : String

/-- Projection: a C006 energy/coercivity branch supplies the `energyBound` hypothesis. -/
theorem EnergyCoercivityBranch.energyBound
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (E : EnergyCoercivityBranch P) :
    P.energyBound :=
  E.estimateDischargesEnergyBound E.approximants_energy_le

/--
Projection: a C006 energy/coercivity branch supplies the
`tightnessOrCoercivity` hypothesis.
-/
theorem EnergyCoercivityBranch.tightnessOrCoercivity
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (E : EnergyCoercivityBranch P) :
    P.tightnessOrCoercivity :=
  E.estimateDischargesTightnessOrCoercivity E.approximants_energy_le

/--
Assembler for the abstract hypotheses once the C006 energy/coercivity branch is
available alongside the still-separate admissibility, weak-formulation,
boundary, regularity, and weak/classical bridge packages.
-/
theorem globalHypotheses_of_energyCoercivityBranch
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (hadm : ∀ n, P.admissible (P.approximants n))
    (hweak : ∀ n, P.weakFormulation (P.approximants n))
    (hboundary : ∀ n, P.boundaryCondition (P.approximants n))
    (hregularity : P.regularityOrEquicontinuity)
    (hbridge : P.weakClassicalBridge)
    (E : EnergyCoercivityBranch P) :
    GlobalCompactnessHypotheses P := by
  exact ⟨hadm, hweak, hboundary, E.energyBound, E.tightnessOrCoercivity,
    hregularity, hbridge⟩

/-- Concrete PDE energy functionals for the C006 branch. -/
abbrev PDEEnergyFunctional (n : ℕ) : Type :=
  PDEState n → ℝ

/--
Concrete PDE energy/coercivity branch over the C005 Euclidean PDE model.

This connects an explicit energy functional on `PDEState n` to the abstract
`energyBound` and `tightnessOrCoercivity` fields of
`ConcretePDEGlobalCompactnessProblem`.  The actual analytic inequality and the
coercivity/tightness theorem remain open until a selected PDE model supplies
the two bridge fields.
-/
structure ConcretePDEEnergyCoercivityBranch {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) where
  energy : PDEEnergyFunctional n
  level : ℝ
  approximants_energy_le : ∀ k, energy (P.approximants k) ≤ level
  estimateDischargesEnergyBound :
    (∀ k, energy (P.approximants k) ≤ level) → P.energyBound
  estimateDischargesTightnessOrCoercivity :
    (∀ k, energy (P.approximants k) ≤ level) → P.tightnessOrCoercivity
  branchLabel : String

/-- Adapter from the concrete C006 PDE branch to the abstract global compactness interface. -/
def ConcretePDEEnergyCoercivityBranch.toEnergyCoercivityBranch {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (E : ConcretePDEEnergyCoercivityBranch P) :
    EnergyCoercivityBranch P.toGlobalCompactnessProblem where
  energy := E.energy
  level := E.level
  approximants_energy_le := E.approximants_energy_le
  estimateDischargesEnergyBound := E.estimateDischargesEnergyBound
  estimateDischargesTightnessOrCoercivity := E.estimateDischargesTightnessOrCoercivity
  branchLabel := E.branchLabel

/-- The concrete C006 branch discharges the adapted abstract `energyBound` field. -/
theorem ConcretePDEEnergyCoercivityBranch.energyBound {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (E : ConcretePDEEnergyCoercivityBranch P) :
    P.toGlobalCompactnessProblem.energyBound :=
  E.toEnergyCoercivityBranch.energyBound

/-- The concrete C006 branch discharges the adapted abstract coercivity/tightness field. -/
theorem ConcretePDEEnergyCoercivityBranch.tightnessOrCoercivity {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (E : ConcretePDEEnergyCoercivityBranch P) :
    P.toGlobalCompactnessProblem.tightnessOrCoercivity :=
  E.toEnergyCoercivityBranch.tightnessOrCoercivity

/-- M0387-level child leaves for the C006 energy/coercivity branch. -/
inductive EnergyCoercivityLeaf : Type where
  | energyFunctionalBoundary
  | energyBoundProjection
  | tightnessCoercivityProjection
  | concretePDEAdapter
  | selectedPDEEnergyEstimate
  | profileTightnessTheorem
  deriving DecidableEq, Repr

/-- Stable public id for each C006 energy/coercivity leaf. -/
def EnergyCoercivityLeaf.stableId : EnergyCoercivityLeaf → String
  | .energyFunctionalBoundary => "S1-M-174-C006-L01.energy_functional_boundary"
  | .energyBoundProjection => "S1-M-174-C006-L02.energy_bound_projection"
  | .tightnessCoercivityProjection => "S1-M-174-C006-L03.tightness_coercivity_projection"
  | .concretePDEAdapter => "S1-M-174-C006-L04.concrete_pde_adapter"
  | .selectedPDEEnergyEstimate => "S1-M-174-C006-L05.selected_pde_energy_estimate"
  | .profileTightnessTheorem => "S1-M-174-C006-L06.profile_tightness_theorem"

/-- Local proof-step budget for each C006 energy/coercivity leaf. -/
def EnergyCoercivityLeaf.proofStepBudget : EnergyCoercivityLeaf → Nat
  | .energyFunctionalBoundary => 35
  | .energyBoundProjection => 20
  | .tightnessCoercivityProjection => 20
  | .concretePDEAdapter => 35
  | .selectedPDEEnergyEstimate => 100
  | .profileTightnessTheorem => 100

/-- Every C006 local child leaf is budgeted at `<= 100` steps. -/
theorem EnergyCoercivityLeaf.proofStepBudget_le_100
    (leaf : EnergyCoercivityLeaf) :
    leaf.proofStepBudget ≤ 100 := by
  cases leaf <;> decide

/-- Ordered C006 theorem-tree leaves for the energy/coercivity package. -/
def energyCoercivityLeaves : List EnergyCoercivityLeaf := [
  .energyFunctionalBoundary,
  .energyBoundProjection,
  .tightnessCoercivityProjection,
  .concretePDEAdapter,
  .selectedPDEEnergyEstimate,
  .profileTightnessTheorem
]

/-- The C006 energy/coercivity package has six budgeted leaves. -/
theorem energyCoercivityLeaves_length :
    energyCoercivityLeaves.length = 6 :=
  rfl

/-- Repo-local theorem-tree package metadata for child C006. -/
structure EnergyCoercivityTheoremTree where
  root : String
  leaves : List EnergyCoercivityLeaf
  allLeavesBudgeted : ∀ leaf ∈ leaves, leaf.proofStepBudget ≤ 100
  completionStatus : String

/--
C006 closes only the checked interface between explicit energy estimates and
the abstract compactness hypotheses.  The selected PDE estimate and the theorem
turning that estimate into profile tightness/coercivity remain formalization
debt.
-/
def c006EnergyCoercivityTheoremTree : EnergyCoercivityTheoremTree where
  root := "energy estimate and coercivity/tightness branch feeding compactness extraction"
  leaves := energyCoercivityLeaves
  allLeavesBudgeted := by
    intro leaf _hleaf
    exact EnergyCoercivityLeaf.proofStepBudget_le_100 leaf
  completionStatus :=
    "checked_interface_only_selected_pde_estimate_and_profile_tightness_still_formalization_debt"

/-- The C006 theorem-tree metadata records six leaves. -/
theorem c006EnergyCoercivityTheoremTree_leaf_count :
    c006EnergyCoercivityTheoremTree.leaves.length = 6 :=
  rfl

/-- C006 integration gate rows for the public-doc integrator. -/
def c006EnergyCoercivityGate : List String := [
  "checked: EnergyCoercivityBranch records an explicit functional, level bound, and bridges to energyBound and tightnessOrCoercivity",
  "checked: ConcretePDEEnergyCoercivityBranch adapts the C005 PDE state model to the abstract global compactness interface",
  "open: no selected PDE-specific energy inequality is proved in this repository",
  "open: no theorem deriving Struwe/Lions profile tightness or coercivity from the energy estimate is proved or pinned here",
  "gate: S1-M-174 remains not_repo_local_closed and must not be marked completed from this C006 interface alone"
]

/-- The C006 gate records actionable rows for the integrator. -/
theorem c006EnergyCoercivityGate_nonempty :
    c006EnergyCoercivityGate ≠ [] := by
  decide

/-! ## Limit-passage interface for child C007 -/

/--
Generic extracted-limit package for the selected global compactness boundary.

The package records the subsequence selected by compactness, its convergence in
the compactified/profile space, the proof that the compactified limit solves
the problem, and the weak/classical bridge proof.  This is a checked interface
for the C007 child task; it does not prove the missing Struwe/Lions analytic
limit-passage theorem.
-/
structure ExtractedLimitPassage
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    (P : GlobalCompactnessProblem State M) where
  subsequence : ℕ → ℕ
  subsequence_strictMono : StrictMono subsequence
  compactified_tendsto : by
    letI := M.compactifiedTopologicalSpace
    exact
      Tendsto
        (fun k => M.compactificationMap (P.approximants (subsequence k)))
        atTop
        (𝓝 P.limitCandidate)
  weakLimitPassage : P.limitSolvesProblem
  weakClassicalBridgeProof : P.weakClassicalBridge
  passageLabel : String

/-- Projection: an extracted-limit package supplies compactified subsequential convergence. -/
theorem ExtractedLimitPassage.hasCompactifiedSubsequence
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (L : ExtractedLimitPassage P) :
    HasCompactifiedSubsequence P := by
  refine ⟨L.subsequence, L.subsequence_strictMono, ?_⟩
  exact L.compactified_tendsto

/-- Projection: an extracted-limit package supplies the weak limit-passage conclusion. -/
theorem ExtractedLimitPassage.limitSolvesProblem
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (L : ExtractedLimitPassage P) :
    P.limitSolvesProblem :=
  L.weakLimitPassage

/-- Projection: an extracted-limit package supplies the weak/classical bridge hypothesis. -/
theorem ExtractedLimitPassage.weakClassicalBridge
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (L : ExtractedLimitPassage P) :
    P.weakClassicalBridge :=
  L.weakClassicalBridgeProof

/--
Assembler for the terminal conclusion once the C007 extracted-limit package is
available.  The proof is local bookkeeping; constructing `L` for a real
Struwe/Lions PDE remains formalization debt.
-/
theorem globalConclusion_of_extractedLimitPassage
    {State : Type u} [TopologicalSpace State]
    {M : ProfileCompactnessMechanism.{u, v} State}
    {P : GlobalCompactnessProblem State M}
    (L : ExtractedLimitPassage P) :
    HasCompactifiedSubsequence P ∧ P.limitSolvesProblem :=
  ⟨L.hasCompactifiedSubsequence, L.limitSolvesProblem⟩

/--
Concrete PDE extracted-limit package over the C005 Euclidean PDE model.

This adapts the C007 limit-passage interface to the concrete PDE object model:
the limit predicate is `P.compactifiedLimitSolves P.limitCandidate`, and the
weak/classical bridge is the concrete problem's stored bridge field.
-/
structure ConcretePDEExtractedLimitPassage {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    (P : ConcretePDEGlobalCompactnessProblem.{v} n M) where
  subsequence : ℕ → ℕ
  subsequence_strictMono : StrictMono subsequence
  compactified_tendsto : by
    letI := M.compactifiedTopologicalSpace
    exact
      Tendsto
        (fun k => M.compactificationMap (P.approximants (subsequence k)))
        atTop
        (𝓝 P.limitCandidate)
  compactifiedLimitSolves : P.compactifiedLimitSolves P.limitCandidate
  weakClassicalBridgeProof : P.weakClassicalBridge
  passageLabel : String

/-- Adapter from the concrete C007 PDE package to the abstract global compactness interface. -/
def ConcretePDEExtractedLimitPassage.toExtractedLimitPassage {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (L : ConcretePDEExtractedLimitPassage P) :
    ExtractedLimitPassage P.toGlobalCompactnessProblem where
  subsequence := L.subsequence
  subsequence_strictMono := L.subsequence_strictMono
  compactified_tendsto := L.compactified_tendsto
  weakLimitPassage := L.compactifiedLimitSolves
  weakClassicalBridgeProof := L.weakClassicalBridgeProof
  passageLabel := L.passageLabel

/-- The concrete C007 package supplies compactified subsequential convergence. -/
theorem ConcretePDEExtractedLimitPassage.hasCompactifiedSubsequence {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (L : ConcretePDEExtractedLimitPassage P) :
    HasCompactifiedSubsequence P.toGlobalCompactnessProblem :=
  L.toExtractedLimitPassage.hasCompactifiedSubsequence

/-- The concrete C007 package supplies the adapted compactified limit predicate. -/
theorem ConcretePDEExtractedLimitPassage.limitSolvesProblem {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (L : ConcretePDEExtractedLimitPassage P) :
    P.toGlobalCompactnessProblem.limitSolvesProblem :=
  L.toExtractedLimitPassage.limitSolvesProblem

/-- The concrete C007 package supplies the weak/classical bridge field. -/
theorem ConcretePDEExtractedLimitPassage.weakClassicalBridge {n : ℕ}
    {M : ProfileCompactnessMechanism.{0, v} (PDEState n)}
    {P : ConcretePDEGlobalCompactnessProblem.{v} n M}
    (L : ConcretePDEExtractedLimitPassage P) :
    P.toGlobalCompactnessProblem.weakClassicalBridge :=
  L.toExtractedLimitPassage.weakClassicalBridge

/-- M0387-level child leaves for the C007 extracted-limit passage branch. -/
inductive LimitPassageLeaf : Type where
  | extractedSubsequenceConvergence
  | weakLimitSolvesProblem
  | weakClassicalBridgeProjection
  | concretePDEAdapter
  | selectedPDEWeakLimitTheorem
  | selectedPDEClassicalRegularityBridge
  deriving DecidableEq, Repr

/-- Stable public id for each C007 limit-passage leaf. -/
def LimitPassageLeaf.stableId : LimitPassageLeaf → String
  | .extractedSubsequenceConvergence =>
      "S1-M-174-C007-L01.extracted_subsequence_convergence"
  | .weakLimitSolvesProblem =>
      "S1-M-174-C007-L02.weak_limit_solves_problem"
  | .weakClassicalBridgeProjection =>
      "S1-M-174-C007-L03.weak_classical_bridge_projection"
  | .concretePDEAdapter =>
      "S1-M-174-C007-L04.concrete_pde_adapter"
  | .selectedPDEWeakLimitTheorem =>
      "S1-M-174-C007-L05.selected_pde_weak_limit_theorem"
  | .selectedPDEClassicalRegularityBridge =>
      "S1-M-174-C007-L06.selected_pde_classical_regularity_bridge"

/-- Local proof-step budget for each C007 limit-passage leaf. -/
def LimitPassageLeaf.proofStepBudget : LimitPassageLeaf → Nat
  | .extractedSubsequenceConvergence => 30
  | .weakLimitSolvesProblem => 20
  | .weakClassicalBridgeProjection => 20
  | .concretePDEAdapter => 35
  | .selectedPDEWeakLimitTheorem => 100
  | .selectedPDEClassicalRegularityBridge => 100

/-- Every C007 local child leaf is budgeted at `<= 100` steps. -/
theorem LimitPassageLeaf.proofStepBudget_le_100
    (leaf : LimitPassageLeaf) :
    leaf.proofStepBudget ≤ 100 := by
  cases leaf <;> decide

/-- Ordered C007 theorem-tree leaves for the extracted-limit passage package. -/
def limitPassageLeaves : List LimitPassageLeaf := [
  .extractedSubsequenceConvergence,
  .weakLimitSolvesProblem,
  .weakClassicalBridgeProjection,
  .concretePDEAdapter,
  .selectedPDEWeakLimitTheorem,
  .selectedPDEClassicalRegularityBridge
]

/-- The C007 limit-passage package has six budgeted leaves. -/
theorem limitPassageLeaves_length :
    limitPassageLeaves.length = 6 :=
  rfl

/-- Repo-local theorem-tree package metadata for child C007. -/
structure LimitPassageTheoremTree where
  root : String
  leaves : List LimitPassageLeaf
  allLeavesBudgeted : ∀ leaf ∈ leaves, leaf.proofStepBudget ≤ 100
  completionStatus : String

/--
C007 closes only the checked interface for carrying an extracted limit through
the abstract statement.  The selected PDE weak-limit theorem and the
weak/classical regularity bridge remain formalization debt.
-/
def c007LimitPassageTheoremTree : LimitPassageTheoremTree where
  root := "weak limit passage and weak/classical bridge for the extracted compactified limit"
  leaves := limitPassageLeaves
  allLeavesBudgeted := by
    intro leaf _hleaf
    exact LimitPassageLeaf.proofStepBudget_le_100 leaf
  completionStatus :=
    "checked_interface_only_selected_pde_weak_limit_and_classical_bridge_still_formalization_debt"

/-- The C007 theorem-tree metadata records six leaves. -/
theorem c007LimitPassageTheoremTree_leaf_count :
    c007LimitPassageTheoremTree.leaves.length = 6 :=
  rfl

/-- C007 integration gate rows for the public-doc integrator. -/
def c007LimitPassageGate : List String := [
  "checked: ExtractedLimitPassage records a strict subsequence, compactified convergence, limit-solution proof, and weak/classical bridge proof",
  "checked: ConcretePDEExtractedLimitPassage adapts the C005 PDE state model to the abstract global compactness interface",
  "open: no selected PDE-specific theorem proving weak residual passage to the extracted limit is proved in this repository",
  "open: no selected PDE-specific regularity theorem upgrading the weak extracted limit to the required classical/strong solution notion is proved or pinned here",
  "gate: S1-M-174 remains not_repo_local_closed and must not be marked completed from this C007 interface alone"
]

/-- The C007 gate records actionable rows for the integrator. -/
theorem c007LimitPassageGate_nonempty :
    c007LimitPassageGate ≠ [] := by
  decide

/-! ## Pinned mathlib audit rows -/

/-- The exact mathlib revision audited for this Stage1 slot. -/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- A compact machine-readable row for the local mathlib anchor audit. -/
structure MathlibAnchorAuditRow where
  branch : String
  module : String
  names : List String
  status : String
  diagnosis : String
  deriving Repr

/-- Exact repo-local anchor audit against `mathlibAuditRevision`. -/
def mathlibAnchorAuditRows : List MathlibAnchorAuditRow := [
  {
    branch := "OnePoint",
    module := "Mathlib.Topology.Compactification.OnePoint.Basic",
    names := [
      "OnePoint",
      "OnePoint.infty",
      "OnePoint.instTopologicalSpace",
      "OnePoint.instCompactSpace",
      "OnePoint.continuous_coe",
      "OnePoint.denseRange_coe"
    ],
    status := "available",
    diagnosis := "Topological one-point compactification infrastructure is present and locally checked, but it is only an auxiliary branch for THM-M-1294."
  },
  {
    branch := "compact images",
    module := "Mathlib.Topology.Compactness.Compact",
    names := [
      "IsCompact.image",
      "IsCompact.image_of_continuousOn"
    ],
    status := "available",
    diagnosis := "Continuous images of compact sets are available as general topology infrastructure."
  },
  {
    branch := "sequential compactness",
    module := "Mathlib.Topology.Sequences",
    names := [
      "isCompact_iff_isSeqCompact",
      "IsSeqCompact"
    ],
    status := "available_with_pseudo_metrizable_hypothesis",
    diagnosis := "`isCompact_iff_isSeqCompact` is available under `TopologicalSpace.PseudoMetrizableSpace`; it is not a PDE compactness extraction theorem by itself."
  },
  {
    branch := "bounded continuous Arzela-Ascoli",
    module := "Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli",
    names := [
      "BoundedContinuousFunction.arzela_ascoli₁",
      "BoundedContinuousFunction.arzela_ascoli₂",
      "BoundedContinuousFunction.arzela_ascoli"
    ],
    status := "available",
    diagnosis := "Compact-domain bounded-continuous-function Arzela-Ascoli is present."
  },
  {
    branch := "uniform-space Arzela-Ascoli",
    module := "Mathlib.Topology.UniformSpace.Ascoli",
    names := [
      "Equicontinuous.comap_uniformFun_eq",
      "Equicontinuous.isUniformInducing_uniformFun_iff_pi",
      "Equicontinuous.inducing_uniformFun_iff_pi",
      "Equicontinuous.tendsto_uniformFun_iff_pi",
      "EquicontinuousOn.comap_uniformOnFun_eq",
      "ArzelaAscoli.compactSpace_of_closed_inducing'",
      "ArzelaAscoli.compactSpace_of_isClosedEmbedding",
      "ArzelaAscoli.isCompact_closure_of_isClosedEmbedding",
      "ArzelaAscoli.isCompact_of_equicontinuous"
    ],
    status := "available",
    diagnosis := "General uniform-space Ascoli infrastructure is present, including closed-embedding and equicontinuous compactness forms."
  },
  {
    branch := "compact operators",
    module := "Mathlib.Analysis.Normed.Operator.Compact",
    names := [
      "IsCompactOperator",
      "IsCompactOperator.image_closedBall_subset_compact",
      "IsCompactOperator.isCompact_closure_image_closedBall",
      "isCompactOperator_iff_image_closedBall_subset_compact",
      "isCompactOperator_iff_isCompact_closure_image_closedBall",
      "IsCompactOperator.comp_clm",
      "IsCompactOperator.clm_comp"
    ],
    status := "available",
    diagnosis := "Compact-operator API is present for images of bounded balls and closure compactness."
  },
  {
    branch := "weak dual / Banach-Alaoglu",
    module := "Mathlib.Analysis.Normed.Module.WeakDual",
    names := [
      "WeakDual",
      "StrongDual.toWeakDual",
      "WeakDual.toStrongDual",
      "NormedSpace.Dual.toWeakDual_continuous",
      "WeakDual.isBounded_iff_isVonNBounded",
      "WeakDual.polar",
      "WeakDual.isCompact_polar",
      "WeakDual.isCompact_closedBall",
      "WeakDual.isSeqCompact_polar",
      "WeakDual.isSeqCompact_closedBall"
    ],
    status := "available",
    diagnosis := "Weak-star compactness is available through Banach-Alaoglu anchors; this does not supply a Struwe/Lions bubble decomposition."
  },
  {
    branch := "distributions",
    module := "Mathlib.Analysis.Distribution.Distribution",
    names := [
      "Distribution",
      "Distribution.mapCLM",
      "Distribution.mapCLM_apply"
    ],
    status := "available",
    diagnosis := "Distribution objects over open domains and continuous-linear-map postcomposition are available."
  },
  {
    branch := "test functions",
    module := "Mathlib.Analysis.Distribution.TestFunction",
    names := [
      "TestFunction",
      "TestFunctionClass",
      "TestFunction.fderivCLM",
      "TestFunction.fderivCLM_apply",
      "TestFunction.fderivCLM_apply_of_le",
      "TestFunction.fderivCLM_apply_of_gt"
    ],
    status := "available",
    diagnosis := "Bundled compactly supported smooth/test functions and derivative CLMs are available."
  },
  {
    branch := "Sobolev/Gagliardo-Nirenberg first derivative inequality",
    module := "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
    names := [
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le",
      "MeasureTheory.eLpNorm_le_eLpNorm_fderiv"
    ],
    status := "available",
    diagnosis := "First-derivative Sobolev inequality infrastructure is present; it is not a compact embedding or concentration-compactness theorem."
  }
]

/-- Missing mathlib branches needed before the selected PDE global compactness theorem can close. -/
def missingGlobalCompactnessBranches : List String := [
  "No `GlobalCompactness` or Struwe/Lions global compactness theorem was found in the pinned mathlib checkout.",
  "No `AubinLions` theorem or named evolution compactness package was found in the pinned mathlib checkout.",
  "No named `RellichKondrachov` theorem or compact Sobolev embedding theorem was found in the pinned mathlib checkout.",
  "No named concentration-compactness, profile-decomposition, bubble-decomposition, or Palais-Smale compactness package was found in the pinned mathlib checkout.",
  "The current `SelectedStatementShape` still has abstract PDE state, profile/compactification space, energy/coercivity, weak formulation, and limit-passage packages."
]

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Topology.Compactification.OnePoint.Basic",
  "Mathlib.Topology.Compactness.Compact",
  "Mathlib.Topology.Sequences",
  "Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli",
  "Mathlib.Topology.UniformSpace.Ascoli",
  "Mathlib.Analysis.Normed.Operator.Compact",
  "Mathlib.Analysis.Normed.Module.WeakDual",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "OnePoint",
  "OnePoint.instCompactSpace",
  "OnePoint.continuous_coe",
  "OnePoint.denseRange_coe",
  "IsCompact.image",
  "IsCompact.image_of_continuousOn",
  "isCompact_iff_isSeqCompact",
  "BoundedContinuousFunction.arzela_ascoli₁",
  "BoundedContinuousFunction.arzela_ascoli₂",
  "BoundedContinuousFunction.arzela_ascoli",
  "Equicontinuous.comap_uniformFun_eq",
  "Equicontinuous.tendsto_uniformFun_iff_pi",
  "ArzelaAscoli.compactSpace_of_closed_inducing'",
  "ArzelaAscoli.compactSpace_of_isClosedEmbedding",
  "ArzelaAscoli.isCompact_closure_of_isClosedEmbedding",
  "ArzelaAscoli.isCompact_of_equicontinuous",
  "IsCompactOperator.image_closedBall_subset_compact",
  "IsCompactOperator.isCompact_closure_image_closedBall",
  "isCompactOperator_iff_image_closedBall_subset_compact",
  "isCompactOperator_iff_isCompact_closure_image_closedBall",
  "StrongDual.toWeakDual",
  "WeakDual.toStrongDual",
  "NormedSpace.Dual.toWeakDual_continuous",
  "WeakDual.isCompact_closedBall",
  "WeakDual.isCompact_polar",
  "WeakDual.isSeqCompact_closedBall",
  "Distribution",
  "Distribution.mapCLM",
  "TestFunction",
  "TestFunction.fderivCLM",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv"
]

/--
Search terms that did not locate a terminal global PDE compactness theorem in
the pinned local mathlib checkout.
-/
def absentTerminalSearchTerms : List String := [
  "global compactness",
  "GlobalCompactness",
  "compactification PDE",
  "Aubin Lions",
  "AubinLions",
  "Rellich Kondrachov",
  "RellichKondrachov",
  "Struwe global compactness Lean",
  "Palais Smale bubble decomposition Lean",
  "Lions concentration compactness Lean",
  "profile decomposition Lean",
  "compact embedding",
  "weak compactness PDE",
  "energy compactness",
  "noncompact compactification"
]

/-! ## External Lean 4 audit rows -/

/-- Machine-status vocabulary for external Lean 4 audit candidates. -/
inductive ExternalLeanAuditStatus where
  | externalUpstreamAnchorOnly
  | exactSearchTermNotFound
  deriving DecidableEq, Repr

/-- A compact repo-local row for public Lean 4 repository audit results. -/
structure ExternalLeanAuditRow where
  searchTerm : String
  status : ExternalLeanAuditStatus
  repository : String
  commit : String
  moduleName : String
  theoremName : String
  license : String
  toolchain : String
  lakeCompatibility : String
  diagnosis : String
  deriving Repr

/--
External Lean 4 audit rows for `S1-M-174.external-lean-audit`.

The Rellich-Kondrachov project is a genuine public Lean 4 compact-embedding
candidate, but it is not a terminal Struwe/Lions global compactness theorem and
is not pinned, imported, or checked in this repository.
-/
def externalLeanAuditRows : List ExternalLeanAuditRow := [
  {
    searchTerm := "RellichKondrachov",
    status := ExternalLeanAuditStatus.externalUpstreamAnchorOnly,
    repository := "https://github.com/abenenson/rellich-kondrachov",
    commit := "85f2c2e943404e5ba92911346874d8961e137b60",
    moduleName :=
      "RellichKondrachov.Geometry.Manifold.Sobolev.RellichKondrachovRiemannian.Global",
    theoremName :=
      "RellichKondrachov.Geometry.Manifold.Sobolev.RiemannianFiniteChartData.isCompactOperator_h1ToL2_riemannianVolume",
    license :=
      "Source headers say Apache 2.0; no LICENSE file was present at the audited commit.",
    toolchain := "leanprover/lean4:v4.29.0-rc7",
    lakeCompatibility :=
      "Lake project requires mathlib inputRev v4.29.0-rc7; this repository is pinned to mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 / Lean v4.29.0, so direct import requires a compatibility pin or port.",
    diagnosis :=
      "Relevant compact-embedding upstream anchor only. It proves compactness of the H1-to-L2 operator on compact Riemannian manifolds, not Struwe/Lions global compactness modulo bubbles/profiles."
  },
  {
    searchTerm := "CompactEmbedding",
    status := ExternalLeanAuditStatus.exactSearchTermNotFound,
    repository := "https://github.com/abenenson/rellich-kondrachov",
    commit := "85f2c2e943404e5ba92911346874d8961e137b60",
    moduleName := "RellichKondrachov.lean",
    theoremName := "no exact `CompactEmbedding` declaration found",
    license :=
      "Source headers say Apache 2.0; no LICENSE file was present at the audited commit.",
    toolchain := "leanprover/lean4:v4.29.0-rc7",
    lakeCompatibility :=
      "The project expresses compact embedding through `IsCompactOperator` theorems rather than an exact `CompactEmbedding` symbol.",
    diagnosis :=
      "Exact requested symbol was not found, but the repository is relevant through compact-operator formulations of Rellich-Kondrachov."
  },
  {
    searchTerm := "AubinLions",
    status := ExternalLeanAuditStatus.exactSearchTermNotFound,
    repository := "",
    commit := "",
    moduleName := "",
    theoremName := "",
    license := "",
    toolchain := "",
    lakeCompatibility := "No public Lean 4 candidate was located in this child audit.",
    diagnosis :=
      "No Aubin-Lions evolution compactness theorem or module was found during the primary-source audit."
  },
  {
    searchTerm := "PDECompactness",
    status := ExternalLeanAuditStatus.exactSearchTermNotFound,
    repository := "",
    commit := "",
    moduleName := "",
    theoremName := "",
    license := "",
    toolchain := "",
    lakeCompatibility := "No public Lean 4 candidate was located in this child audit.",
    diagnosis :=
      "No exact `PDECompactness` Lean 4 declaration or module was found during the primary-source audit."
  },
  {
    searchTerm := "GlobalCompactness",
    status := ExternalLeanAuditStatus.exactSearchTermNotFound,
    repository := "",
    commit := "",
    moduleName := "",
    theoremName := "",
    license := "",
    toolchain := "",
    lakeCompatibility := "No public Lean 4 candidate was located in this child audit.",
    diagnosis :=
      "No exact `GlobalCompactness` Lean 4 declaration or Struwe/Lions terminal global compactness theorem was found during the primary-source audit."
  }
]

theorem externalLeanAuditRows_nonempty : externalLeanAuditRows ≠ [] := by
  decide

/-! ## Integration gate for child C008 -/

/-- Repo-local closure status used by the C008 integration gate. -/
inductive RepoLocalClosureStatus where
  | notRepoLocalClosed
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnlyBlocked
  deriving DecidableEq, Repr

/--
Checked integration-gate certificate for `S1-M-174-C008`.

The gate deliberately separates three facts:
1. this repository has checked local infrastructure and statement boundaries;
2. an external Rellich-Kondrachov compact-embedding anchor exists only as an
   upstream URL/commit/module/theorem row;
3. the terminal Struwe/Lions global compactness theorem is not locally proved
   and no external terminal proof is pinned/imported/checked.
-/
structure IntegrationGateCertificate where
  closureStatus : RepoLocalClosureStatus
  hasLocalTerminalProofBody : Bool
  hasPinnedExternalTerminalProof : Bool
  hasAnchorOnlyExternalCandidate : Bool
  mayMarkCompleted : Bool
  blocker : String
  diagnosis : String
  deriving Repr

/--
C008 gate certificate for the current repository state.

The Rellich-Kondrachov upstream candidate is relevant compactness
infrastructure, but it is not in this Lake dependency closure and it is not the
selected Struwe/Lions terminal theorem.  Therefore it is recorded as an
integration blocker, not completion evidence.
-/
def s1m174IntegrationGateCertificate : IntegrationGateCertificate where
  closureStatus := RepoLocalClosureStatus.externalUpstreamAnchorOnlyBlocked
  hasLocalTerminalProofBody := false
  hasPinnedExternalTerminalProof := false
  hasAnchorOnlyExternalCandidate := true
  mayMarkCompleted := false
  blocker :=
    "External Rellich-Kondrachov compact-embedding anchor at abenenson/rellich-kondrachov commit 85f2c2e943404e5ba92911346874d8961e137b60 is not pinned/imported/checked here; it uses Lean v4.29.0-rc7/mathlib inputRev v4.29.0-rc7 and is not a terminal Struwe/Lions global compactness theorem."
  diagnosis :=
    "S1-M-174 remains not repo-local closed: no local terminal proof body and no pinned/imported/checked external terminal proof."

/-- C008 does not permit a public completion claim. -/
theorem s1m174IntegrationGate_not_completed :
    s1m174IntegrationGateCertificate.mayMarkCompleted = false :=
  rfl

/-- C008 records that no local terminal proof body exists in this artifact. -/
theorem s1m174IntegrationGate_no_local_terminal_proof :
    s1m174IntegrationGateCertificate.hasLocalTerminalProofBody = false :=
  rfl

/-- C008 records that no external terminal proof has been pinned and checked. -/
theorem s1m174IntegrationGate_no_pinned_external_terminal_proof :
    s1m174IntegrationGateCertificate.hasPinnedExternalTerminalProof = false :=
  rfl

/-- C008 records the anchor-only external candidate together with a concrete blocker. -/
theorem s1m174IntegrationGate_anchor_only_has_blocker :
    s1m174IntegrationGateCertificate.hasAnchorOnlyExternalCandidate = true ∧
      s1m174IntegrationGateCertificate.blocker =
        "External Rellich-Kondrachov compact-embedding anchor at abenenson/rellich-kondrachov commit 85f2c2e943404e5ba92911346874d8961e137b60 is not pinned/imported/checked here; it uses Lean v4.29.0-rc7/mathlib inputRev v4.29.0-rc7 and is not a terminal Struwe/Lions global compactness theorem." := by
  constructor <;> rfl

/-- Integration-gate rows ready for public-doc backfill by a serial integrator. -/
def s1m174IntegrationGateRows : List String := [
  "checked: S1-M-174-C008 adds a repo-local Lean integration-gate certificate.",
  "checked: local statement-shape, compactness-anchor, PDE-model, energy/coercivity, and limit-passage interfaces compile, but they are not a terminal global compactness proof.",
  "blocked: the external Rellich-Kondrachov Lean 4 compact-embedding candidate is anchor-only, not pinned/imported/checked in this repository, and not the selected Struwe/Lions terminal theorem.",
  "gate: do not mark S1-M-174 complete until a local terminal proof body validates or an external terminal Lean 4 proof is pinned/imported/checked; anchor-only evidence remains open with the recorded blocker."
]

/-- The C008 integration gate has actionable rows for the public integrator. -/
theorem s1m174IntegrationGateRows_nonempty :
    s1m174IntegrationGateRows ≠ [] := by
  decide

/-! ## Audit probes -/

#check OnePoint
#check GlobalCompactnessVariant
#check selectedGlobalCompactnessVariant
#check selectedGlobalCompactnessVariant_eq
#check ProfileCompactnessMechanism
#check profileCompactification_univ_isCompact
#check profileCompactificationMap_continuous
#check onePointAuxiliaryMechanism
#check onePointAuxiliaryMechanism_univ_isCompact
#check GlobalCompactnessProblem
#check PDEState
#check PDEAdmissibilityData
#check IsPDEAdmissible
#check PDEWeakFormulationData
#check SatisfiesPDEWeakFormulation
#check PDEBoundaryData
#check SatisfiesPDEBoundaryCondition
#check ConcretePDEModel
#check IsPDELimitSolution
#check ConcretePDEGlobalCompactnessProblem
#check ConcretePDEGlobalCompactnessProblem.toGlobalCompactnessProblem
#check PDEModelLeaf
#check c005PDEModelTheoremTree
#check SelectedStatementShape
#check OnePoint.continuous_coe
#check OnePoint.denseRange_coe
#check IsCompact.image
#check BoundedContinuousFunction.arzela_ascoli
#check ArzelaAscoli.compactSpace_of_isClosedEmbedding
#check ArzelaAscoli.isCompact_closure_of_isClosedEmbedding
#check ArzelaAscoli.isCompact_of_equicontinuous
#check IsCompactOperator.image_closedBall_subset_compact
#check IsCompactOperator.isCompact_closure_image_closedBall
#check WeakDual.isCompact_closedBall
#check WeakDual.isCompact_polar
#check WeakDual.isSeqCompact_closedBall
#check Distribution
#check Distribution.mapCLM
#check TestFunction
#check TestFunction.fderivCLM
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check EnergyCoercivityBranch
#check EnergyCoercivityBranch.energyBound
#check EnergyCoercivityBranch.tightnessOrCoercivity
#check globalHypotheses_of_energyCoercivityBranch
#check ConcretePDEEnergyCoercivityBranch
#check ConcretePDEEnergyCoercivityBranch.toEnergyCoercivityBranch
#check ConcretePDEEnergyCoercivityBranch.energyBound
#check ConcretePDEEnergyCoercivityBranch.tightnessOrCoercivity
#check EnergyCoercivityLeaf
#check c006EnergyCoercivityTheoremTree
#check c006EnergyCoercivityGate
#check c006EnergyCoercivityGate_nonempty
#check ExtractedLimitPassage
#check ExtractedLimitPassage.hasCompactifiedSubsequence
#check ExtractedLimitPassage.limitSolvesProblem
#check ExtractedLimitPassage.weakClassicalBridge
#check globalConclusion_of_extractedLimitPassage
#check ConcretePDEExtractedLimitPassage
#check ConcretePDEExtractedLimitPassage.toExtractedLimitPassage
#check ConcretePDEExtractedLimitPassage.hasCompactifiedSubsequence
#check ConcretePDEExtractedLimitPassage.limitSolvesProblem
#check ConcretePDEExtractedLimitPassage.weakClassicalBridge
#check LimitPassageLeaf
#check c007LimitPassageTheoremTree
#check c007LimitPassageGate
#check c007LimitPassageGate_nonempty
#check ExternalLeanAuditRow
#check externalLeanAuditRows
#check externalLeanAuditRows_nonempty
#check RepoLocalClosureStatus
#check IntegrationGateCertificate
#check s1m174IntegrationGateCertificate
#check s1m174IntegrationGate_not_completed
#check s1m174IntegrationGate_no_local_terminal_proof
#check s1m174IntegrationGate_no_pinned_external_terminal_proof
#check s1m174IntegrationGate_anchor_only_has_blocker
#check s1m174IntegrationGateRows
#check s1m174IntegrationGateRows_nonempty

end S1_M_174
end Stage1
end AwesomeTheorems
