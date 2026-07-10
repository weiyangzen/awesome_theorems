import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Measure.Prokhorov

/-!
# S1-M-173 / THM-M-1293: Lions concentration-compactness principle

This Stage1 artifact records a conservative Lean 4 boundary for the Lions
concentration-compactness principle in critical-growth PDE problems.

The pinned mathlib snapshot has substantial adjacent infrastructure:
`MemLp`, `Lp`, `eLpNorm`, restriction of `Lp` functions to measurable regions,
finite-dimensional Gagliardo-Nirenberg-Sobolev estimates, weak convergence of
probability measures, and Prokhorov-style compactness infrastructure.  This
audit did not find a terminal Lions concentration-compactness theorem or a
Sobolev critical compact embedding theorem in the local dependency closure.

The declarations below therefore avoid proof placeholders and false completion
claims.  They normalize the trichotomy/compactness interface and include only
small checked wrappers around available mathlib facts.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_173

universe u v

variable {X : Type u} [MeasurableSpace X]
variable {F : Type v} [NormedAddCommGroup F]

/--
Local `L^p` mass of a function on a region.

For a later Lions formalization this is the low-level object behind
concentration functions such as `sup_y ∫_{B(y,R)} |u_n|^p`.
-/
def LocalLpMass (μ : Measure X) (p : ℝ≥0∞) (u : X → F) (s : Set X) : ℝ≥0∞ :=
  eLpNorm (s.indicator u) p μ

/--
Concrete Sobolev/PDE state model for a critical-growth concentration-compactness
problem.

The state is now an actual function `X → F` over a measured domain.  The
remaining proposition-valued fields are the PDE-side bridges that mathlib does
not yet provide as a unified Sobolev solution API in this Stage1 slot.
-/
structure SobolevStateModel (X : Type u) [MeasurableSpace X]
    (F : Type v) [NormedAddCommGroup F] : Type (max u v) where
  domain : Set X
  domainMeasurable : MeasurableSet domain
  measure : Measure X
  criticalExponent : ℝ≥0∞
  energy : (X → F) → ℝ≥0∞
  admissible : (X → F) → Prop
  weakFormulation : (X → F) → Prop
  criticalGrowthEstimate : (ℕ → X → F) → Prop

/-- Local critical `L^p` mass, restricted to the modeled Sobolev domain. -/
def SobolevStateModel.localCriticalMass
    (M : SobolevStateModel X F) (u : X → F) (s : Set X) : ℝ≥0∞ :=
  LocalLpMass M.measure M.criticalExponent u (s ∩ M.domain)

/-- Sequence-level bounded-energy hypothesis for the concrete Sobolev model. -/
def SobolevStateModel.boundedEnergy
    (M : SobolevStateModel X F) (u : ℕ → X → F) : Prop :=
  ∃ C : ℝ≥0∞, ∀ n : ℕ, M.energy (u n) ≤ C

/--
State-level admissibility package used by the Lions statement shape: the state
must satisfy the model's admissibility predicate, weak PDE formulation, and
critical `L^p` membership on the modeled measure space.
-/
def SobolevStateModel.stateAdmissible
    (M : SobolevStateModel X F) (u : X → F) : Prop :=
  M.admissible u ∧ M.weakFormulation u ∧ MemLp u M.criticalExponent M.measure

/-- The concrete local-mass projection is definitionally the low-level `LocalLpMass`. -/
theorem SobolevStateModel.localCriticalMass_eq
    (M : SobolevStateModel X F) (u : X → F) (s : Set X) :
    M.localCriticalMass u s =
      LocalLpMass M.measure M.criticalExponent u (s ∩ M.domain) :=
  rfl

/-- The bounded-energy package is the expected uniform bound on the energy functional. -/
theorem SobolevStateModel.boundedEnergy_iff
    (M : SobolevStateModel X F) (u : ℕ → X → F) :
    M.boundedEnergy u ↔ ∃ C : ℝ≥0∞, ∀ n : ℕ, M.energy (u n) ≤ C :=
  Iff.rfl

/--
Concrete local-critical-mass vanishing predicate.

The family `regions` stands for the local windows used by a later PDE
instantiation, for example balls of a fixed radius or compact neighborhoods.
This is the Lions vanishing branch at the level available in this Stage1 file:
uniform decay of all modeled local critical `L^p` masses along the sequence.
-/
def LocalCriticalMassVanishing
    (M : SobolevStateModel X F) (u : ℕ → X → F)
    (regions : Set (Set X)) : Prop :=
  ∀ ε : ℝ≥0∞, 0 < ε →
    ∃ N : ℕ, ∀ n : ℕ, N ≤ n →
      ∀ s : Set X, s ∈ regions → M.localCriticalMass (u n) s < ε

/--
Persistent local mass, the minimal PDE-side hypothesis needed to exclude the
local-critical-mass vanishing predicate without importing a full Lions proof.
-/
def PersistentLocalCriticalMass
    (M : SobolevStateModel X F) (u : ℕ → X → F)
    (regions : Set (Set X)) : Prop :=
  ∃ η : ℝ≥0∞, 0 < η ∧
    ∀ N : ℕ, ∃ n : ℕ, N ≤ n ∧
      ∃ s : Set X, s ∈ regions ∧ η ≤ M.localCriticalMass (u n) s

/--
Explicit vanishing-exclusion package.

For a concrete PDE this field should be supplied by a nonzero mass,
normalization, or energy-threshold argument.  Keeping it explicit avoids a false
claim that the present Stage1 artifact proves the PDE estimate itself.
-/
structure VanishingExclusionHypotheses
    (M : SobolevStateModel X F) (u : ℕ → X → F)
    (regions : Set (Set X)) : Prop where
  persistentLocalMass : PersistentLocalCriticalMass M u regions

/-- Persistent local critical mass excludes concrete local-mass vanishing. -/
theorem not_localCriticalMassVanishing_of_persistentLocalCriticalMass
    (M : SobolevStateModel X F) (u : ℕ → X → F)
    (regions : Set (Set X))
    (h : PersistentLocalCriticalMass M u regions) :
    ¬ LocalCriticalMassVanishing M u regions := by
  rcases h with ⟨η, hηpos, hpersistent⟩
  intro hvanish
  rcases hvanish η hηpos with ⟨N, hN⟩
  rcases hpersistent N with ⟨n, hnN, s, hsregions, hmass⟩
  exact not_lt_of_ge hmass (hN n hnN s hsregions)

/-- The explicit PDE-side vanishing-exclusion package excludes vanishing. -/
theorem not_localCriticalMassVanishing_of_exclusionHypotheses
    (M : SobolevStateModel X F) (u : ℕ → X → F)
    (regions : Set (Set X))
    (h : VanishingExclusionHypotheses M u regions) :
    ¬ LocalCriticalMassVanishing M u regions :=
  not_localCriticalMassVanishing_of_persistentLocalCriticalMass M u regions
    h.persistentLocalMass

/--
Concrete witness for the Lions dichotomy branch at the Stage1 boundary.

It records two separated local regions with persistent positive local critical
mass and an asymptotic energy-splitting estimate.  The `separation` field is an
explicit geometry/PDE hook because this file has not selected a metric,
translation group, or ball API for THM-M-1293.
-/
structure EnergySplittingWitness
    (M : SobolevStateModel X F) (u : ℕ → X → F) : Type (max u v) where
  leftRegion : ℕ → Set X
  rightRegion : ℕ → Set X
  leftEnergy : ℝ≥0∞
  rightEnergy : ℝ≥0∞
  separation : Prop
  separation_holds : separation
  leftMassPositive :
    ∃ η : ℝ≥0∞, 0 < η ∧
      ∀ n : ℕ, η ≤ M.localCriticalMass (u n) (leftRegion n)
  rightMassPositive :
    ∃ η : ℝ≥0∞, 0 < η ∧
      ∀ n : ℕ, η ≤ M.localCriticalMass (u n) (rightRegion n)
  energySplits :
    ∀ ε : ℝ≥0∞, 0 < ε →
      ∃ N : ℕ, ∀ n : ℕ, N ≤ n →
        M.energy (u n) ≤ leftEnergy + rightEnergy + ε ∧
          leftEnergy ≤ M.energy (u n) + ε ∧
            rightEnergy ≤ M.energy (u n) + ε

/-- Concrete dichotomy predicate: an energy-splitting witness exists. -/
def DichotomyByEnergySplitting
    (M : SobolevStateModel X F) (u : ℕ → X → F) : Prop :=
  Nonempty (EnergySplittingWitness M u)

/--
Explicit dichotomy-exclusion package.

For a terminal Lions/PDE proof this should be discharged by strict
subadditivity, a sharp threshold, or another checked PDE-side estimate.
-/
structure DichotomyExclusionHypotheses
    (M : SobolevStateModel X F) (u : ℕ → X → F) : Prop where
  noEnergySplittingWitness : ∀ _W : EnergySplittingWitness M u, False

/-- The explicit PDE-side dichotomy-exclusion package excludes dichotomy. -/
theorem not_dichotomyByEnergySplitting_of_exclusionHypotheses
    (M : SobolevStateModel X F) (u : ℕ → X → F)
    (h : DichotomyExclusionHypotheses M u) :
    ¬ DichotomyByEnergySplitting M u := by
  intro hdichotomy
  rcases hdichotomy with ⟨W⟩
  exact h.noEnergySplittingWitness W

/--
Concrete problem data for a critical-growth concentration-compactness theorem.

The model fixes the domain, measure, critical exponent, admissibility predicate,
energy functional, local critical mass, and weak formulation for states
`X → F`.  Vanishing and dichotomy are now tied to concrete local-mass and
energy-splitting predicates; the exclusion proofs still require explicit
PDE-side hypotheses supplied by a future terminal formalization.
-/
structure ConcentrationCompactnessProblem
    (X : Type u) [MeasurableSpace X]
    (F : Type v) [NormedAddCommGroup F] : Type (max u v) where
  model : SobolevStateModel X F
  tightUpToSymmetry : (ℕ → X → F) → Prop
  localMassRegions : Set (Set X)
  vanishing : (ℕ → X → F) → Prop
  vanishing_eq_localCriticalMassVanishing :
    ∀ u : ℕ → X → F, vanishing u ↔
      LocalCriticalMassVanishing model u localMassRegions
  dichotomy : (ℕ → X → F) → Prop
  dichotomy_eq_energySplitting :
    ∀ u : ℕ → X → F, dichotomy u ↔ DichotomyByEnergySplitting model u
  compactnessConclusion : (ℕ → X → F) → Prop

/-- The problem-level vanishing branch is the concrete local-critical-mass predicate. -/
theorem ConcentrationCompactnessProblem.vanishing_iff_localCriticalMassVanishing
    (P : ConcentrationCompactnessProblem X F) (u : ℕ → X → F) :
    P.vanishing u ↔
      LocalCriticalMassVanishing P.model u P.localMassRegions :=
  P.vanishing_eq_localCriticalMassVanishing u

/-- The problem-level dichotomy branch is the concrete energy-splitting predicate. -/
theorem ConcentrationCompactnessProblem.dichotomy_iff_energySplitting
    (P : ConcentrationCompactnessProblem X F) (u : ℕ → X → F) :
    P.dichotomy u ↔ DichotomyByEnergySplitting P.model u :=
  P.dichotomy_eq_energySplitting u

/-- The three named alternatives in the Lions concentration-compactness split. -/
inductive LionsAlternative where
  | compactness
  | vanishing
  | dichotomy
  deriving DecidableEq, Repr

/-- Interpret a named Lions alternative for a fixed sequence. -/
def AlternativeHolds
    (P : ConcentrationCompactnessProblem X F)
    (u : ℕ → X → F) : LionsAlternative → Prop
  | .compactness => P.compactnessConclusion u
  | .vanishing => P.vanishing u
  | .dichotomy => P.dichotomy u

/--
Trichotomy statement-shape: every admissible bounded critical sequence has one
of the three concentration-compactness alternatives.
-/
def TrichotomyShape
    (P : ConcentrationCompactnessProblem X F) : Prop :=
  ∀ u : ℕ → X → F,
    (∀ n, P.model.stateAdmissible (u n)) →
      P.model.boundedEnergy u →
        P.model.criticalGrowthEstimate u →
          P.compactnessConclusion u ∨ P.vanishing u ∨ P.dichotomy u

/--
Compactness-after-excluding-defects statement-shape: after ruling out vanishing
and dichotomy, bounded critical sequences are compact modulo the selected
symmetries.
-/
def CompactnessShape
    (P : ConcentrationCompactnessProblem X F) : Prop :=
  ∀ u : ℕ → X → F,
    (∀ n, P.model.stateAdmissible (u n)) →
      P.model.boundedEnergy u →
        P.model.criticalGrowthEstimate u →
          ¬ P.vanishing u →
            ¬ P.dichotomy u →
              P.tightUpToSymmetry u →
                P.compactnessConclusion u

/--
Normalized Stage1 statement shape for Lions concentration-compactness in a
critical-growth PDE setting.

The full Lions content is the conjunction of a trichotomy branch and the
compactness branch after excluding the two noncompact alternatives.
-/
def StatementShape
    (P : ConcentrationCompactnessProblem X F) : Prop :=
  TrichotomyShape P ∧ CompactnessShape P

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    {P : ConcentrationCompactnessProblem X F}
    (htri : TrichotomyShape P) (hcompact : CompactnessShape P) :
    StatementShape P :=
  ⟨htri, hcompact⟩

/-!
## Public statement normalization

These declarations give the serial public-doc integrator a stable checked name
to cite while keeping the parent theorem explicitly nonterminal.
-/

/-- Public Stage1 alias for the current repo-local statement boundary. -/
def PublicStatementNormalization
    (P : ConcentrationCompactnessProblem X F) : Prop :=
  StatementShape P

/-- The public Stage1 alias is definitionally the checked statement shape. -/
theorem publicStatementNormalization_iff_statementShape
    {P : ConcentrationCompactnessProblem X F} :
    PublicStatementNormalization P ↔ StatementShape P :=
  Iff.rfl

/-- Canonical checked declaration name for public Stage1 backfill. -/
def publicStatementBoundaryName : String :=
  "AwesomeTheorems.Stage1.S1_M_173.StatementShape"

/-- Integration-ready nonterminal summary for the public Stage1 surface. -/
def publicStatementNormalizationNotes : List String := [
  "StatementShape is the current repo-local Lean boundary for Lions concentration-compactness.",
  "It packages a concrete Sobolev/PDE state model with the trichotomy branch and compactness after excluding vanishing and dichotomy.",
  "SobolevStateModel fixes the domain, measure, critical exponent, energy functional, admissibility, local critical Lp mass, and weak formulation for states X -> F.",
  "LocalCriticalMassVanishing and DichotomyByEnergySplitting are concrete Stage1 predicates for the two defect alternatives.",
  "The checked exclusion wrappers require explicit PDE-side hypotheses; the artifact does not prove the sharp PDE estimates that would discharge those hypotheses.",
  "The checked anchors cover local Lp mass, restriction monotonicity, Prokhorov-adjacent measure infrastructure, and a Sobolev inequality wrapper.",
  "This artifact is not a terminal Lions theorem, profile decomposition, Rellich-Kondrachov theorem, or compact Sobolev embedding proof."
]

/-- Explicit nonterminal gate for public integration text. -/
def publicStatementNormalizationIsTerminal : Bool := false

/-- Checked reminder that the Stage1 statement-normalization artifact is nonterminal. -/
theorem publicStatementNormalizationIsTerminal_eq_false :
    publicStatementNormalizationIsTerminal = false :=
  rfl

/-!
## C004 concrete defect alternatives

The C004 child pass replaces the previous abstract defect-alternative boundary
with concrete predicates for vanishing and dichotomy.  It also records the
checked exclusion lemmas that are available once a future PDE formalization
supplies the required nonzero-local-mass or no-energy-splitting hypotheses.
-/

/-- C004 declarations that make the vanishing branch concrete. -/
def c004ConcreteVanishingDeclarations : List String := [
  "LocalCriticalMassVanishing",
  "PersistentLocalCriticalMass",
  "VanishingExclusionHypotheses",
  "not_localCriticalMassVanishing_of_persistentLocalCriticalMass",
  "not_localCriticalMassVanishing_of_exclusionHypotheses",
  "ConcentrationCompactnessProblem.vanishing_iff_localCriticalMassVanishing"
]

/-- C004 declarations that make the dichotomy branch concrete. -/
def c004ConcreteDichotomyDeclarations : List String := [
  "EnergySplittingWitness",
  "DichotomyByEnergySplitting",
  "DichotomyExclusionHypotheses",
  "not_dichotomyByEnergySplitting_of_exclusionHypotheses",
  "ConcentrationCompactnessProblem.dichotomy_iff_energySplitting"
]

/--
C004 terminal-proof gate: the concrete predicates and conditional exclusion
wrappers are checked, but no terminal Lions/PDE exclusion proof was imported or
completed in this repository.
-/
def c004TerminalPdeExclusionProofImportedOrCompleted : Bool :=
  false

/-- Checked reminder that C004 remains a nonterminal formalization-debt step. -/
theorem c004TerminalPdeExclusionProofImportedOrCompleted_eq_false :
    c004TerminalPdeExclusionProofImportedOrCompleted = false :=
  rfl

/-- C004 integration diagnosis under the M0387 debt taxonomy. -/
def c004RepoLocalDiagnosis : String :=
  "formalization_debt / not_repo_local_closed; concrete defect predicates are checked, but terminal PDE-side exclusion proofs remain open."

/-!
## C005 Prokhorov/tight-measure concentration branch

Prokhorov compactness can support a genuine measure-level subpackage for the
concentration branch: a tight family of probability measures has compact
closure in the weak topology.  This is still not a terminal Lions/PDE
subpackage, because the Sobolev sequence must first be converted into
probability measures that represent critical local mass, and the resulting weak
measure compactness must then be bridged back to profile decomposition or strong
Sobolev compactness.
-/

section C005

variable [TopologicalSpace X]

/-- The probability measures associated to a sequence, as a set of measures. -/
def ProbabilityMeasureSequenceRange (ν : ℕ → ProbabilityMeasure X) :
    Set (ProbabilityMeasure X) :=
  Set.range ν

/--
Tightness predicate for the measure-level concentration package.

It is expressed using mathlib's `IsTightMeasureSet` on the coercions of the
probability measures to ordinary measures, matching the hypothesis expected by
the local Prokhorov compactness theorem.
-/
def ProbabilityMeasureSequenceTight (ν : ℕ → ProbabilityMeasure X) : Prop :=
  IsTightMeasureSet {((μ : ProbabilityMeasure X) : Measure X) |
    μ ∈ ProbabilityMeasureSequenceRange ν}

/-- The tightness predicate is exactly the mathlib compact-window formulation. -/
theorem probabilityMeasureSequenceTight_iff_exists_compact_measure_compl_le
    (ν : ℕ → ProbabilityMeasure X) :
    ProbabilityMeasureSequenceTight ν ↔
      ∀ ε : ℝ≥0∞, 0 < ε →
        ∃ K : Set X, IsCompact K ∧
          ∀ μ : ProbabilityMeasure X, μ ∈ ProbabilityMeasureSequenceRange ν →
            ((μ : ProbabilityMeasure X) : Measure X) (Kᶜ) ≤ ε :=
  by
    rw [ProbabilityMeasureSequenceTight,
      isTightMeasureSet_iff_exists_isCompact_measure_compl_le]
    constructor
    · intro h ε hε
      rcases h ε hε with ⟨K, hK, hμ⟩
      exact ⟨K, hK, fun μ hμν => hμ (μ : Measure X) ⟨μ, hμν, rfl⟩⟩
    · intro h ε hε
      rcases h ε hε with ⟨K, hK, hμ⟩
      refine ⟨K, hK, ?_⟩
      rintro _ ⟨μ, hμν, rfl⟩
      exact hμ μ hμν

/--
Checked Prokhorov wrapper: tightness of the associated probability measures
gives compactness of their weak closure.
-/
theorem probabilityMeasureSequence_compact_closure_of_tight
    [T2Space X] [BorelSpace X]
    (ν : ℕ → ProbabilityMeasure X)
    (hν : ProbabilityMeasureSequenceTight ν) :
    IsCompact (closure (ProbabilityMeasureSequenceRange ν)) :=
  isCompact_closure_of_isTightMeasureSet hν

/--
Shape of the missing bridge from a Sobolev sequence to probability measures.

The bridge is deliberately explicit: Prokhorov acts on probability measures,
while Lions concentration-compactness for critical PDE states needs a critical
mass construction, compatibility with local `L^p` mass, and a return map from
measure compactness to Sobolev/profile compactness.
-/
structure SobolevToProbabilityMeasureBridge
    [T2Space X] [BorelSpace X]
    (M : SobolevStateModel X F) (u : ℕ → X → F) : Type (max u v) where
  probabilityMeasures : ℕ → ProbabilityMeasure X
  representsCriticalLocalMass : Prop
  tightnessFollowsFromConcentrationHypotheses :
    ProbabilityMeasureSequenceTight probabilityMeasures
  compactMeasureLimitSupportsConcentrationBranch :
    IsCompact (closure (ProbabilityMeasureSequenceRange probabilityMeasures)) →
      M.boundedEnergy u →
        M.criticalGrowthEstimate u →
          Prop
  measureCompactnessToSobolevProfileCompactness :
    Prop

/-- Any completed bridge supplies the measure-level Prokhorov compactness input. -/
theorem SobolevToProbabilityMeasureBridge.compact_measure_closure
    [T2Space X] [BorelSpace X]
    {M : SobolevStateModel X F} {u : ℕ → X → F}
    (B : SobolevToProbabilityMeasureBridge M u) :
    IsCompact (closure (ProbabilityMeasureSequenceRange B.probabilityMeasures)) :=
  probabilityMeasureSequence_compact_closure_of_tight B.probabilityMeasures
    B.tightnessFollowsFromConcentrationHypotheses

/-- C005 decision: Prokhorov supports only the measure-level compactness subpackage. -/
def c005ProkhorovSupportsMeasureLevelCompactness : Bool :=
  true

/-- Checked C005 positive gate for measure-level compactness support. -/
theorem c005ProkhorovSupportsMeasureLevelCompactness_eq_true :
    c005ProkhorovSupportsMeasureLevelCompactness = true :=
  rfl

/--
C005 decision: the measure-level package alone is not a terminal
Sobolev/profile-decomposition formalization.
-/
def c005MeasureLevelPackageIsTerminalSobolevFormalization : Bool :=
  false

/-- Checked C005 nonterminal gate for the Sobolev/profile branch. -/
theorem c005MeasureLevelPackageIsTerminalSobolevFormalization_eq_false :
    c005MeasureLevelPackageIsTerminalSobolevFormalization = false :=
  rfl

/-- C005 integration diagnosis under the M0387 debt taxonomy. -/
def c005RepoLocalDiagnosis : String :=
  "formalization_debt / not_repo_local_closed; Prokhorov gives checked tight probability-measure compactness, but a separate Sobolev critical-mass/profile-decomposition bridge is still required."

end C005

/-!
## External anchor integration gate

M0387-level completion cannot rest on an external anchor unless the proof is
imported into the repo-local validation closure or a concrete blocker is named.
-/

/-- Minimal audit record for any future external terminal Lean proof candidate. -/
structure ExternalLeanAnchorAudit : Type where
  exactTerminalProofFound : Prop
  importedIntoRepoLocalClosure : Prop
  concreteIntegrationBlocker : Prop

/-- No completed state may retain unresolved repo-local integration debt. -/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactTerminalProofFound →
    A.importedIntoRepoLocalClosure ∨ A.concreteIntegrationBlocker

/-- The integration-debt gate is vacuous when no exact external terminal proof is known. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : ¬ A.exactTerminalProofFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-- Extract the trichotomy branch from the normalized statement package. -/
theorem StatementShape.trichotomy
    {P : ConcentrationCompactnessProblem X F}
    (h : StatementShape P) :
    TrichotomyShape P :=
  h.1

/-- Extract the compactness-after-excluding-defects branch. -/
theorem StatementShape.compactness
    {P : ConcentrationCompactnessProblem X F}
    (h : StatementShape P) :
    CompactnessShape P :=
  h.2

/-- A checked wrapper around mathlib: `MemLp` restricts to any measurable subset. -/
theorem memLp_restrict_anchor {μ : Measure X} {p : ℝ≥0∞} {f : X → F}
    (hf : MemLp f p μ) (s : Set X) :
    MemLp f p (μ.restrict s) :=
  hf.restrict s

/-- A checked wrapper around mathlib: restricting the measure cannot increase `eLpNorm`. -/
theorem eLpNorm_restrict_le_anchor {μ : Measure X} {p : ℝ≥0∞} (f : X → F)
    (s : Set X) :
    eLpNorm f p (μ.restrict s) ≤ eLpNorm f p μ :=
  eLpNorm_mono_measure f Measure.restrict_le_self

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
variable {G : Type v} [NormedAddCommGroup G] [NormedSpace ℝ G]

/--
Checked Sobolev-infrastructure anchor available in the pinned mathlib snapshot.

This is a first-derivative Gagliardo-Nirenberg-Sobolev inequality for compactly
supported smooth functions.  It is useful for a future concentration-compactness
package, but it is not itself the Lions theorem.
-/
theorem sobolev_firstDerivative_anchor
    (μ : Measure E) [μ.IsAddHaarMeasure] [FiniteDimensional ℝ G]
    {u : E → G} (hu : ContDiff ℝ 1 u) (h2u : HasCompactSupport u)
    {p p' : ℝ≥0} (hp : 1 ≤ p) (hn : 0 < Module.finrank ℝ E)
    (hp' : (p' : ℝ)⁻¹ = (p : ℝ)⁻¹ - (Module.finrank ℝ E : ℝ)⁻¹) :
    eLpNorm u p' μ ≤
      SNormLESNormFDerivOfEqConst G μ p * eLpNorm (fderiv ℝ u) p μ :=
  MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq μ hu h2u hp hn hp'

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Set",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Measure.TightNormed",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.MeasureTheory.Function.UnifTight",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Topology.Compactness.Basic",
  "Mathlib.Topology.Sequences"
]

/-- Checked declaration names used or audited as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.Lp",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.MemLp.restrict",
  "MeasureTheory.eLpNorm_mono_measure",
  "MeasureTheory.LpToLpRestrictCLM",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
  "MeasureTheory.IsTightMeasureSet",
  "MeasureTheory.isCompact_closure_of_isTightMeasureSet",
  "MeasureTheory.levyProkhorovEDist",
  "MeasureTheory.LevyProkhorov.probabilityMeasureHomeomorph",
  "MeasureTheory.ProbabilityMeasure.tendsto_of_tight_of_separatesPoints",
  "MeasureTheory.UnifTight",
  "MeasureTheory.tendstoInMeasure_iff_tendsto_Lp",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "Distribution",
  "TemperedDistribution"
]

/--
Search terms that did not locate a terminal Lions concentration-compactness
theorem in the pinned local mathlib checkout.
-/
def absentTerminalSearchTerms : List String := [
  "concentration compactness",
  "ConcentrationCompactness",
  "Lions",
  "profile decomposition",
  "vanishing dichotomy compactness",
  "critical Sobolev compactness",
  "Rellich",
  "compact embedding",
  "Sobolev compact",
  "Palais Smale critical"
]

/-!
## C002 pinned mathlib API audit

The C002 child pass audited the local mathlib checkout at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.  The result is negative for a
terminal proof-wrapper target, but positive for several adjacent packages.
-/

/-- Exact mathlib revision audited for the C002 API-search child. -/
def c002AuditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Search categories required by the C002 child task. -/
def c002RequiredApiSearchCategories : List String := [
  "Rellich-Kondrachov",
  "compact Sobolev embedding",
  "profile decomposition",
  "Lions concentration-compactness"
]

/-- C002 audit result: no terminal mathlib API was found for the requested theorem family. -/
def c002TerminalApiFound : Bool :=
  false

/-- Checked nonterminal gate for the C002 API audit. -/
theorem c002TerminalApiFound_eq_false :
    c002TerminalApiFound = false :=
  rfl

/-- Adjacent mathlib infrastructure found by the C002 API audit. -/
def c002AdjacentMathlibInfrastructure : List String := [
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality: finite-dimensional first-derivative Sobolev/Gagliardo-Nirenberg-Sobolev inequalities for compactly supported smooth functions.",
  "Mathlib.MeasureTheory.Integral.Bochner.Set: restriction of Lp functions to measurable regions via LpToLpRestrictCLM.",
  "Mathlib.MeasureTheory.Measure.Tight and Prokhorov: tight sets of probability measures and compactness of their closure.",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric and LevyConvergence: convergence-in-distribution topology and tightness criteria for probability measures.",
  "Mathlib.MeasureTheory.Function.UnifTight: uniform tightness for Lp-function families and Vitali-style Lp convergence criteria."
]

/-- Terms that produced only unrelated or adjacent hits in the C002 audit. -/
def c002FalsePositiveOrAdjacentHits : List String := [
  "`dichotomy` occurs in generic ENNReal/Lp parameter case splits, not Lions dichotomy.",
  "`vanishing` occurs throughout algebra, analysis, and topology, not as local critical-mass vanishing.",
  "`concentration` occurs in Fourier/probability prose, not as concentration-compactness.",
  "`compact` appears broadly in topology/operator modules, not as Rellich-Kondrachov compact Sobolev embedding."
]

/--
C002 proof-wrapper decision: do not attempt a Lions proof wrapper from the
pinned mathlib snapshot alone.
-/
def c002ProofWrapperAttempted : Bool :=
  false

/-- Checked record that C002 deliberately did not attempt a false wrapper. -/
theorem c002ProofWrapperAttempted_eq_false :
    c002ProofWrapperAttempted = false :=
  rfl

/--
C002 integration diagnosis: the parent remains formalization debt, not
repo-local completed, because no terminal local or pinned upstream Lions theorem
was found.
-/
def c002RepoLocalDiagnosis : String :=
  "formalization_debt / not_repo_local_closed; no repo-local integration debt was introduced."

/-!
## C006 parent completion gate

The C006 child pass records the M0387-level rule that this parent theorem must
remain open until there is a terminal local proof body, a pinned upstream
wrapper, or a concrete integration blocker for an exact external terminal proof.
The current artifact satisfies none of those terminal closure routes.
-/

/-- Boolean fields used to audit whether the parent can be marked completed. -/
structure C006CompletionGate : Type where
  terminalLocalProofBody : Bool
  pinnedUpstreamWrapper : Bool
  exactExternalTerminalProofKnown : Bool
  externalProofImportedIntoRepoClosure : Bool
  externalProofConcreteIntegrationBlocker : Bool
  publicSurfaceMerged : Bool
  leafBudgetClosed : Bool
  deriving Repr

/-- Terminal closure route accepted by the M0387 completion gate. -/
def C006CompletionGate.terminalClosureRouteAvailable
    (G : C006CompletionGate) : Bool :=
  G.terminalLocalProofBody ||
    G.pinnedUpstreamWrapper ||
      (G.exactExternalTerminalProofKnown &&
        (G.externalProofImportedIntoRepoClosure ||
          G.externalProofConcreteIntegrationBlocker))

/-- The parent completion gate: all terminal closure routes remain unavailable. -/
def c006ParentCompletionGate : C006CompletionGate where
  terminalLocalProofBody := false
  pinnedUpstreamWrapper := false
  exactExternalTerminalProofKnown := false
  externalProofImportedIntoRepoClosure := false
  externalProofConcreteIntegrationBlocker := false
  publicSurfaceMerged := false
  leafBudgetClosed := false

/-- Checked gate: no M0387 terminal closure route is currently available. -/
theorem c006ParentCompletionGate_terminalClosureRouteAvailable_eq_false :
    c006ParentCompletionGate.terminalClosureRouteAvailable = false :=
  rfl

/-- Checked gate: the parent Stage1 item must remain open in the public surface. -/
def c006ParentMustRemainOpen : Bool :=
  true

/-- The C006 noncompletion gate is active. -/
theorem c006ParentMustRemainOpen_eq_true :
    c006ParentMustRemainOpen = true :=
  rfl

/--
Checked C006 integration-debt result.

No completed state is claimed, so this artifact does not retain completed-state
`repo_local_integration_debt`.  If a future exact external terminal proof is
found, it must be imported into the repo-local validation closure or blocked by
a concrete integration reason before any completion claim.
-/
def c006CompletedStateHasRepoLocalIntegrationDebt : Bool :=
  false

/-- Checked record that C006 leaves no completed-state repo-local integration debt. -/
theorem c006CompletedStateHasRepoLocalIntegrationDebt_eq_false :
    c006CompletedStateHasRepoLocalIntegrationDebt = false :=
  rfl

/-- C006 diagnosis under the M0387 completion taxonomy. -/
def c006RepoLocalDiagnosis : String :=
  "formalization_debt / not_repo_local_closed; keep S1-M-173 open because no terminal local proof body, pinned upstream wrapper, or exact external-proof integration blocker is present."

end S1_M_173
end Stage1
end AwesomeTheorems
