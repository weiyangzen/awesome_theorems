import Mathlib.Probability.IdentDistribIndep
import Mathlib.GroupTheory.Perm.Support

/-!
# S1-M-288 / THM-M-1008: Hewitt-Savage zero-one law

This Stage1 artifact records a conservative Lean 4 boundary for the
Hewitt-Savage zero-one law.  The local mathlib snapshot provides independence
and identical-distribution APIs for infinite product laws, but no terminal
Hewitt-Savage theorem was located in the pinned dependency closure.

The file therefore packages a precise statement shape and proves only
low-risk wrappers around available mathlib facts: an iid coordinate process has
the same path law after any coordinate permutation, and measurable exchangeable
events have equal probability under the original and permuted path maps.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_288

universe u v

/-- The path of a discrete stochastic process as a point of sequence space. -/
def processPath {Ω : Type u} {E : Type v} (X : ℕ → Ω → E) (ω : Ω) : ℕ → E :=
  fun n => X n ω

/-- Reindex a sequence by a permutation of the coordinate set. -/
def permutedPath {E : Type v} (σ : Equiv.Perm ℕ) (x : ℕ → E) : ℕ → E :=
  fun n => x (σ n)

/--
A coordinate permutation is finite when all but finitely many natural-number
coordinates are fixed.
-/
def FiniteSupportPermutation (σ : Equiv.Perm ℕ) : Prop :=
  ∃ s : Finset ℕ, ∀ n, n ∉ s → σ n = n

/-- A path event is invariant under every finite coordinate permutation. -/
def ExchangeableEvent {E : Type v} (event : Set (ℕ → E)) : Prop :=
  ∀ σ : Equiv.Perm ℕ, FiniteSupportPermutation σ →
    ∀ x : ℕ → E, x ∈ event ↔ permutedPath σ x ∈ event

/-- Data for the standard iid-process form of the Hewitt-Savage zero-one law. -/
structure HewittSavageData (Ω : Type u) (E : Type v) [MeasurableSpace Ω]
    [MeasurableSpace E] : Type (max u v) where
  μ : Measure Ω
  isProbability : IsProbabilityMeasure μ
  X : ℕ → Ω → E
  independent : iIndepFun X μ
  identicallyDistributed : ∀ i j : ℕ, IdentDistrib (X i) (X j) μ μ
  event : Set (ℕ → E)
  eventMeasurable : MeasurableSet event
  exchangeable : ExchangeableEvent event

/--
The zero-one conclusion for the event pulled back from sequence space along the
sample-path map.
-/
def ZeroOneConclusion {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) : Prop :=
  D.μ {ω | processPath D.X ω ∈ D.event} = 0 ∨
    D.μ {ω | processPath D.X ω ∈ D.event} = 1

/--
Stage1 normalized statement-shape candidate for the Hewitt-Savage zero-one law:
every measurable finite-permutation-invariant event of an iid sequence has
probability zero or one.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [MeasurableSpace E],
    ∀ D : HewittSavageData Ω E,
      ZeroOneConclusion D

/--
Candidate public theorem surfaces for the Hewitt-Savage zero-one law.

The current Stage1 artifact chooses the path-space event surface: the event is
`Set (ℕ → E)`, and the probability statement is made after pulling it back
along `processPath`.  Tail-sigma-field and generated exchangeable-sigma-field
formulations remain proof-route or future-equivalence surfaces until the
corresponding repo-local sigma-field API is closed.
-/
inductive PublicTheoremSurface where
  | pathSpaceEvent
  | sampleSpacePreimage
  | tailSigmaField
  | generatedExchangeableSigmaField
  deriving DecidableEq, Repr

/-- The four public formulation candidates audited by `S1-M-288-PUB-04`. -/
def publicTheoremSurfaceCandidates : List PublicTheoremSurface := [
  PublicTheoremSurface.pathSpaceEvent,
  PublicTheoremSurface.sampleSpacePreimage,
  PublicTheoremSurface.tailSigmaField,
  PublicTheoremSurface.generatedExchangeableSigmaField
]

/--
Repo-local Stage1 decision for the public theorem surface.

Use path-space events as the canonical public statement.  The sample-space
preimage appears in `ZeroOneConclusion`; it is not the primary event object.
-/
def chosenPublicTheoremSurface : PublicTheoremSurface :=
  PublicTheoremSurface.pathSpaceEvent

/-- `S1-M-288-PUB-04` selects the path-space event surface. -/
theorem chosenPublicTheoremSurface_eq_pathSpaceEvent :
    chosenPublicTheoremSurface = PublicTheoremSurface.pathSpaceEvent :=
  rfl

/-- The chosen public surface is exactly the existing normalized statement. -/
def ChosenPathSpaceEventSurface : Prop :=
  StatementShape.{u, v}

/--
The selected path-space event formulation unfolds definitionally to
`StatementShape`.
-/
theorem chosenPathSpaceEventSurface_iff_statementShape :
    ChosenPathSpaceEventSurface.{u, v} ↔ StatementShape.{u, v} :=
  Iff.rfl

/-- Integration notes for the public formulation decision. -/
def publicTheoremSurfaceDecisionNotes : List String := [
  "canonical public event object: path-space event Set (Nat -> E)",
  "sample-space event appears as the preimage {omega | processPath D.X omega in D.event}",
  "tail sigma-field formulation remains a proof-route/equivalence target, not the selected public surface",
  "generated exchangeable sigma-field formulation remains future API work, not the selected public surface"
]

/-- The statement shape unfolds to the explicit iid-process zero-one statement. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [MeasurableSpace E],
        ∀ D : HewittSavageData Ω E,
          ZeroOneConclusion D :=
  Iff.rfl

/-- Project the probability-space hypothesis from the normalized data. -/
theorem isProbabilityMeasure {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) :
    IsProbabilityMeasure D.μ :=
  D.isProbability

/-- Project the independent-family hypothesis from the normalized data. -/
theorem independent {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) :
    iIndepFun D.X D.μ :=
  D.independent

/-- Project the identical-distribution hypothesis from the normalized data. -/
theorem identicallyDistributed {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) :
    ∀ i j : ℕ, IdentDistrib (D.X i) (D.X j) D.μ D.μ :=
  D.identicallyDistributed

/-- Project event measurability from the normalized data. -/
theorem eventMeasurable {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) :
    MeasurableSet D.event :=
  D.eventMeasurable

/-- Project finite-permutation invariance from the normalized data. -/
theorem exchangeable {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) :
    ExchangeableEvent D.event :=
  D.exchangeable

/-- The identity permutation has finite support. -/
theorem finiteSupport_refl : FiniteSupportPermutation (Equiv.refl ℕ) := by
  refine ⟨∅, ?_⟩
  intro n hn
  rfl

/--
Checked mathlib anchor: reindexing an independent family by a permutation
preserves independence.
-/
theorem independent_permuted {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) (σ : Equiv.Perm ℕ) :
    iIndepFun (fun n => D.X (σ n)) D.μ :=
  D.independent.precomp σ.injective

/--
Checked mathlib anchor: an iid process and any coordinate permutation of it
have identically distributed path laws.
-/
theorem path_identDistrib_permuted {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] (D : HewittSavageData Ω E)
    (σ : Equiv.Perm ℕ) :
    IdentDistrib
      (fun ω => processPath D.X ω)
      (fun ω => processPath (fun n => D.X (σ n)) ω) D.μ D.μ :=
  IdentDistrib.pi
    (fun n => D.identicallyDistributed n (σ n))
    D.independent
    (independent_permuted D σ)

/--
Checked wrapper: a measurable path event has the same probability under the
original iid path law and under any coordinate-permuted path law.
-/
theorem measure_event_eq_permuted {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] (D : HewittSavageData Ω E)
    (σ : Equiv.Perm ℕ) :
    D.μ {ω | processPath D.X ω ∈ D.event} =
      D.μ {ω | processPath (fun n => D.X (σ n)) ω ∈ D.event} :=
  (path_identDistrib_permuted D σ).measure_preimage_eq D.eventMeasurable

/-- Membership in an exchangeable event is unchanged by a finite permutation. -/
theorem event_mem_iff_permuted {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] (D : HewittSavageData Ω E)
    {σ : Equiv.Perm ℕ} (hσ : FiniteSupportPermutation σ) (x : ℕ → E) :
    x ∈ D.event ↔ permutedPath σ x ∈ D.event :=
  D.exchangeable σ hσ x

/-! ## Audit probes retained in the checked file. -/

#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.precomp
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.IdentDistrib.pi
#check ProbabilityTheory.IdentDistrib.measure_preimage_eq
#check Equiv.Perm
#check Equiv.Perm.support

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.InfinitePi",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.IdentDistribIndep",
  "Mathlib.Probability.ProductMeasure",
  "Mathlib.Probability.BorelCantelli",
  "Mathlib.GroupTheory.Perm.Support"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.precomp",
  "ProbabilityTheory.iIndepFun_iff_map_fun_eq_infinitePi_map",
  "ProbabilityTheory.iIndepFun_iff_map_fun_eq_infinitePi_map₀'",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.IdentDistrib.pi",
  "ProbabilityTheory.IdentDistrib.measure_preimage_eq",
  "ProbabilityTheory.infinitePi",
  "Equiv.Perm",
  "Equiv.Perm.support"
]

/-- Search terms that did not locate a terminal Hewitt-Savage theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Hewitt",
  "Savage",
  "Hewitt-Savage",
  "zero-one law",
  "zero_one_law",
  "exchangeable event",
  "finite permutation invariant",
  "tail event",
  "exchangeable sigma"
]

/--
Primary Lean 4 source repositories audited for `S1-M-288-PUB-05`.

Each row records repository, checked commit, Lake package, module/theorem result,
placeholder status, Lean toolchain, license, and import feasibility.
-/
def primaryExternalAuditRows : List String := [
  "repo=https://github.com/leanprover-community/mathlib4; commit=177caf0bccd154a7e9ce7f82eba9399c25d697a8; package=mathlib; module_result=no Hewitt-Savage terminal module or theorem found; related_nonterminal=Mathlib.Probability.Independence.ZeroOne / measure_zero_or_one_of_measurableSet_limsup_atTop; placeholder_status=no Hewitt-Savage placeholder found; toolchain=leanprover/lean4:v4.30.0-rc2; license=Apache-2.0; import_feasibility=proof-route anchor only, no terminal theorem to import",
  "repo=https://github.com/wellecks/lean4_information_theory; commit=2c2cc3894f747d81cb2ad46b6d59638d8b345968; package=information_theory; module_result=no Hewitt-Savage terminal module or theorem found; theorem_name=none; placeholder_status=none found; toolchain=leanprover/lean4:v4.24.0; license=NOASSERTION; import_feasibility=no terminal theorem to import",
  "repo=https://github.com/mlinegar/FormalProbability; commit=718126e150c4798739b585f9505176ce8cf5ae3b; package=FormalProbability; module_result=no Hewitt-Savage terminal module or theorem found; theorem_name=none; placeholder_status=none found; toolchain=leanprover/lean4:v4.27.0-rc1; license=MIT; import_feasibility=no terminal theorem to import",
  "repo=https://github.com/BasharHamade12/MarkovChain_Formalisation_Lean; commit=24d6140363c42bb4d3931afda66f4d1f3ef62eed; package=probability; module_result=no Hewitt-Savage terminal module or theorem found; theorem_name=none; placeholder_status=none found; toolchain=leanprover/lean4:v4.24.0; license=NOASSERTION; import_feasibility=no terminal theorem to import",
  "repo=https://github.com/abenenson/channel-capacity; commit=a212a605d3ec5a23034e0c40f51b2b92d594efa5; package=channel-capacity; module_result=no Hewitt-Savage terminal module or theorem found; theorem_name=none; placeholder_status=none found; toolchain=leanprover/lean4:v4.29.1; license=Apache-2.0; import_feasibility=no terminal theorem to import",
  "repo=https://github.com/slink/LeanLevy; commit=b71b38e93b75a7089391131c0c24dade0c6fdef2; package=leanlevy; module_result=no Hewitt-Savage terminal module or theorem found; theorem_name=none; placeholder_status=none found; toolchain=leanprover/lean4:v4.29.0-rc3; license=MIT; import_feasibility=no terminal theorem to import",
  "repo=https://github.com/zzhisthebest/ConvexAndProbability-lean4; commit=b141c8203b31437aef7063924caeaa1ca1bbbe2c; package=unread because checkout requires git-lfs; module_result=not audited past checkout blocker; theorem_name=unknown; placeholder_status=unknown; toolchain=unknown; license=NOASSERTION; import_feasibility=blocked by missing local git-lfs checkout, and no repository-search evidence indicated a Hewitt-Savage theorem"
]

/-- `S1-M-288-PUB-05` audit conclusion: no terminal Lean 4 theorem was found. -/
def externalAuditTerminalHewittSavageTheoremFound : Bool := false

/--
Consequence of the external audit for the M0387 integration-debt gate.

Because no terminal external Lean 4 proof was found in the audited primary
sources, this slot does not create completed-state `repo_local_integration_debt`.
The parent theorem remains open `formalization_debt`, with mathlib's
Kolmogorov zero-one law serving only as a proof-route anchor.
-/
def externalAuditIntegrationGate : String :=
  "no terminal external Lean 4 Hewitt-Savage theorem found; no pin/import/check target available"

/--
`S1-M-288-PUB-06` integration action after the primary external audit.

The negative case is explicit so that the public completion gate cannot be
misread as an anchor-only external proof claim.
-/
inductive ExternalProofIntegrationDecision where
  | noTerminalExternalProofFound
  | terminalProofImportedAndChecked
  | terminalProofBlocked
  deriving DecidableEq, Repr

/--
Checked PUB-06 decision: no terminal external Lean 4 Hewitt-Savage proof was
found, so there is no external theorem target to pin, import, or check locally.
-/
def pub06ExternalProofIntegrationDecision : ExternalProofIntegrationDecision :=
  ExternalProofIntegrationDecision.noTerminalExternalProofFound

/-- The PUB-06 decision is the audited negative branch. -/
theorem pub06ExternalProofIntegrationDecision_eq :
    pub06ExternalProofIntegrationDecision =
      ExternalProofIntegrationDecision.noTerminalExternalProofFound :=
  rfl

/--
Concrete integration blocker for PUB-06, if a terminal external theorem has
been found but cannot yet enter the repo-local Lake closure.

The value is `none` because the audited branch found no terminal external proof.
The `zzhisthebest/ConvexAndProbability-lean4` git-lfs checkout issue remains a
repository audit blocker from PUB-05, not an integration blocker for a concrete
terminal Hewitt-Savage theorem.
-/
def pub06ConcreteIntegrationBlocker : Option String :=
  none

/-- Repo-local integration-debt gate text for `S1-M-288-PUB-06`. -/
def pub06IntegrationDebtGate : String :=
  "PUB-06 closed as conditional-negative: no terminal external Lean 4 Hewitt-Savage proof was found, so no anchor-only external theorem is counted as completed"

/-! ## PUB-07 monotone-class / tail-triviality route expansion. -/

/-- The sample-space event obtained by pulling a path event back along the iid path map. -/
def pulledBackEvent {Ω : Type u} {E : Type v} [MeasurableSpace Ω]
    [MeasurableSpace E] (D : HewittSavageData Ω E) : Set Ω :=
  {ω | processPath D.X ω ∈ D.event}

/--
Checked terminal algebra leaf: if an event in a probability space is independent
of itself, then its measure is zero or one.

This is the final algebraic step needed after a monotone-class/tail argument
has supplied self-independence of the pulled-back exchangeable event.
-/
theorem measure_zero_or_one_of_indepSet_self {Ω : Type u} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] {s : Set Ω}
    (h : IndepSets {s} {s} μ) :
    μ s = 0 ∨ μ s = 1 := by
  have hmul : μ s = μ s * μ s := by
    have h' := (indepSets_singleton_iff (μ := μ) (s := s) (t := s)).1 h
    simpa [Set.inter_self] using h'
  by_cases hzero : μ s = 0
  · exact Or.inl hzero
  · right
    have hle : μ s ≤ 1 := by
      simpa using (measure_mono (Set.subset_univ s) : μ s ≤ μ Set.univ)
    have htop : μ s ≠ ∞ :=
      ne_top_of_le_ne_top ENNReal.one_ne_top hle
    have hcancel := congrArg (fun x => x * (μ s)⁻¹) hmul
    have hleft : μ s * (μ s)⁻¹ = 1 :=
      ENNReal.mul_inv_cancel hzero htop
    have hright : (μ s * μ s) * (μ s)⁻¹ = μ s := by
      rw [mul_assoc, ENNReal.mul_inv_cancel hzero htop, mul_one]
    exact (hleft.symm.trans (hcancel.trans hright)).symm

/--
Checked wrapper for the pulled-back event: self-independence of that event is
sufficient for the Stage1 zero-one conclusion.
-/
theorem zeroOneConclusion_of_indep_pulledBackEvent_self {Ω : Type u} {E : Type v}
    [MeasurableSpace Ω] [MeasurableSpace E] (D : HewittSavageData Ω E)
    (h : IndepSets {pulledBackEvent D} {pulledBackEvent D} D.μ) :
    ZeroOneConclusion D := by
  letI : IsProbabilityMeasure D.μ := D.isProbability
  simpa [ZeroOneConclusion, pulledBackEvent]
    using measure_zero_or_one_of_indepSet_self D.μ h

/-- Status labels for the PUB-07 theorem-tree leaves. -/
inductive Pub07LeafStatus where
  | checkedLocal
  | openFormalizationDebt
  deriving DecidableEq, Repr

/-- Metadata for an independent `<=100` proof leaf in the PUB-07 route. -/
structure Pub07Leaf where
  id : String
  refines : String
  budget : Nat
  status : Pub07LeafStatus
  target : String
  input : String
  output : String
  blocker : String
  deriving Repr

/--
Expanded independent `<=100` proof leaves for `S1-M-288-L020` through
`S1-M-288-L024`, following the monotone-class / tail-triviality route.

Open leaves are route-level formalization debt, not completion claims.  The
two checked leaves at the end close only the generic self-independence algebra
step and its application to `ZeroOneConclusion`.
-/
def pub07MonotoneClassTailLeaves : List Pub07Leaf := [
  {
    id := "S1-M-288-L020a",
    refines := "S1-M-288-L020",
    budget := 60,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Define the finite-coordinate cylinder pi-system for path space",
    input := "path-space event surface Set (Nat -> E)",
    output := "pi-system/generator for events depending on coordinates in a Finset Nat",
    blocker := "needs repo-local choice of product-measurable cylinder API"
  },
  {
    id := "S1-M-288-L020b",
    refines := "S1-M-288-L020",
    budget := 70,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Prove finite-support coordinate permutations preserve cylinder measurability",
    input := "FiniteSupportPermutation, permutedPath, cylinder generator",
    output := "measurability transport for permuted cylinder events",
    blocker := "depends on L020a cylinder generator"
  },
  {
    id := "S1-M-288-L020c",
    refines := "S1-M-288-L020",
    budget := 80,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Package finite-permutation-invariant events as a stable Dynkin/monotone class",
    input := "ExchangeableEvent and measurable path events",
    output := "closure class usable by monotone-class induction",
    blocker := "needs selected Dynkin/monotone-class API"
  },
  {
    id := "S1-M-288-L020d",
    refines := "S1-M-288-L020",
    budget := 80,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Show the exchangeable class contains the finite-coordinate generator after index separation",
    input := "finite cylinder generator and finite-support permutation action",
    output := "generator membership statements for the exchangeable bridge",
    blocker := "depends on L020a-L020c"
  },
  {
    id := "S1-M-288-L021a",
    refines := "S1-M-288-L021",
    budget := 60,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Define the tail sigma-field as the infimum of sigma-fields generated by coordinates n >= k",
    input := "coordinate maps on Nat -> E",
    output := "repo-local tail-sigma-field definition for paths",
    blocker := "needs final API choice for coordinate-generated sigma-fields"
  },
  {
    id := "S1-M-288-L021b",
    refines := "S1-M-288-L021",
    budget := 70,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Prove finite coordinate changes do not affect tail-sigma membership",
    input := "FiniteSupportPermutation and tail sigma-field definition",
    output := "permutation invariance of tail-measurable events",
    blocker := "depends on L021a"
  },
  {
    id := "S1-M-288-L021c",
    refines := "S1-M-288-L021",
    budget := 90,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Bridge exchangeable measurable path events into the tail sigma-field",
    input := "monotone-class exchangeable bridge and tail sigma-field",
    output := "D.event is tail-measurable in path space",
    blocker := "core Hewitt-Savage monotone-class formalization remains missing"
  },
  {
    id := "S1-M-288-L022a",
    refines := "S1-M-288-L022",
    budget := 70,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Express iid coordinates as independent generated coordinate sigma-fields",
    input := "D.independent and mathlib iIndep/iIndepFun APIs",
    output := "iIndep over coordinate-generated sigma-fields",
    blocker := "needs exact comap/generateFrom statement matching mathlib"
  },
  {
    id := "S1-M-288-L022b",
    refines := "S1-M-288-L022",
    budget := 80,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Prove finite initial-coordinate sigma-field is independent of each sufficiently far tail block",
    input := "iIndep coordinate sigma-fields and disjoint index sets",
    output := "Indep between finite initial sigma-field and tail block sigma-field",
    blocker := "depends on L022a and mathlib disjoint-index independence lemmas"
  },
  {
    id := "S1-M-288-L022c",
    refines := "S1-M-288-L022",
    budget := 90,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Pass independence from tail blocks to the tail sigma-field",
    input := "L022b and monotone/iInf closure of IndepSets",
    output := "finite initial sigma-field independent of tail sigma-field",
    blocker := "needs sigma-field iInf independence closure instantiated locally"
  },
  {
    id := "S1-M-288-L022d",
    refines := "S1-M-288-L022",
    budget := 90,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Specialize finite-initial/tail independence to the pulled-back exchangeable event",
    input := "tail-measurability of D.event and finite initial sigma-field independence",
    output := "pulledBackEvent D independent of finite-coordinate approximants",
    blocker := "depends on L021c and L022c"
  },
  {
    id := "S1-M-288-L023a",
    refines := "S1-M-288-L023",
    budget := 80,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Approximate a measurable exchangeable event by finite-coordinate generator events in the monotone class",
    input := "eventMeasurable and path-space generator",
    output := "approximation family compatible with independence transfer",
    blocker := "requires completed monotone-class bridge"
  },
  {
    id := "S1-M-288-L023b",
    refines := "S1-M-288-L023",
    budget := 90,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Lift independence from approximants to the pulled-back event",
    input := "finite approximants and L022d",
    output := "IndepSets {pulledBackEvent D} tail/pulled-back event class",
    blocker := "needs independence closure under generated class"
  },
  {
    id := "S1-M-288-L023c",
    refines := "S1-M-288-L023",
    budget := 70,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Conclude self-independence of pulledBackEvent D",
    input := "L023b specialized to D.event itself",
    output := "IndepSets {pulledBackEvent D} {pulledBackEvent D} D.mu",
    blocker := "depends on L023a-L023b"
  },
  {
    id := "S1-M-288-L024a",
    refines := "S1-M-288-L024",
    budget := 45,
    status := Pub07LeafStatus.checkedLocal,
    target := "Prove self-independence forces measure zero or one",
    input := "IndepSets {s} {s} mu and IsProbabilityMeasure mu",
    output := "measure_zero_or_one_of_indepSet_self",
    blocker := "closed locally"
  },
  {
    id := "S1-M-288-L024b",
    refines := "S1-M-288-L024",
    budget := 30,
    status := Pub07LeafStatus.checkedLocal,
    target := "Apply the self-independence algebra leaf to the pulled-back Hewitt-Savage event",
    input := "IndepSets {pulledBackEvent D} {pulledBackEvent D} D.mu",
    output := "zeroOneConclusion_of_indep_pulledBackEvent_self",
    blocker := "closed locally"
  }
]

/-- Number of PUB-07 route leaves recorded in the checked artifact. -/
def pub07MonotoneClassTailLeafCount : Nat :=
  pub07MonotoneClassTailLeaves.length

/-- The PUB-07 expansion currently records sixteen route leaves. -/
theorem pub07MonotoneClassTailLeafCount_eq :
    pub07MonotoneClassTailLeafCount = 16 :=
  rfl

/-- PUB-07 status: expanded route leaves exist, but the terminal theorem remains open. -/
def pub07ExpansionGate : String :=
  "S1-M-288-L020 through L024 expanded into independent <=100 route leaves; only L024a-L024b are checked local algebra/application leaves; terminal Hewitt-Savage remains formalization_debt"

/-! ## PUB-08 finite-valued / countable-discrete special-case backfill. -/

/--
Finite-valued specialization of the selected Hewitt-Savage statement surface.

This is a genuine checked Lean statement boundary, not a proof of the
finite-valued Hewitt-Savage theorem.  The terminal zero-one argument still
needs the exchangeable-to-tail/self-independence bridge.
-/
def FiniteValuedStatementShape : Prop :=
  ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [MeasurableSpace E]
    [Fintype E] [MeasurableSingletonClass E],
    ∀ D : HewittSavageData Ω E,
      ZeroOneConclusion D

/--
Countable-discrete specialization of the selected Hewitt-Savage statement
surface.

The `MeasurableSingletonClass` assumption records the intended discrete
measurability substrate; the current backfill does not assert that this
specialization is already proved.
-/
def CountableDiscreteStatementShape : Prop :=
  ∀ (Ω : Type u) (E : Type v) [MeasurableSpace Ω] [MeasurableSpace E]
    [Countable E] [MeasurableSingletonClass E],
    ∀ D : HewittSavageData Ω E,
      ZeroOneConclusion D

/-- The full statement immediately specializes to the finite-valued statement. -/
theorem finiteValuedStatementShape_of_statementShape
    (h : StatementShape.{u, v}) :
    FiniteValuedStatementShape.{u, v} := by
  intro Ω E _ _ _ _ D
  exact h Ω E D

/-- The full statement immediately specializes to the countable-discrete statement. -/
theorem countableDiscreteStatementShape_of_statementShape
    (h : StatementShape.{u, v}) :
    CountableDiscreteStatementShape.{u, v} := by
  intro Ω E _ _ _ _ D
  exact h Ω E D

/--
The finite-valued special case is a subcase of the countable-discrete
specialization.
-/
theorem finiteValuedStatementShape_of_countableDiscreteStatementShape
    (h : CountableDiscreteStatementShape.{u, v}) :
    FiniteValuedStatementShape.{u, v} := by
  intro Ω E _ _ _ _ D
  exact h Ω E D

/--
`S1-M-288-PUB-08` decision: the finite/countable-discrete branch is useful as
a lower-risk local statement and API boundary, but it is not yet a terminal
proof route because the same exchangeable-to-tail/self-independence bridge is
still missing.
-/
def pub08FiniteDiscreteBackfillGate : String :=
  "finite-valued and countable-discrete statement boundaries are checked; terminal special-case zero-one proof remains formalization_debt"

/--
Independent `<=100` leaves for the PUB-08 finite/countable-discrete branch.

The checked leaves are statement specializations and reductions.  The open
leaves are the genuine proof work needed before any finite-valued or
countable-discrete zero-one completion can be claimed.
-/
def pub08FiniteDiscreteLeaves : List Pub07Leaf := [
  {
    id := "S1-M-288-L025a",
    refines := "S1-M-288-L025",
    budget := 20,
    status := Pub07LeafStatus.checkedLocal,
    target := "Define the finite-valued path-space statement boundary",
    input := "HewittSavageData, ZeroOneConclusion, Fintype E, MeasurableSingletonClass E",
    output := "FiniteValuedStatementShape",
    blocker := "closed locally"
  },
  {
    id := "S1-M-288-L025b",
    refines := "S1-M-288-L025",
    budget := 20,
    status := Pub07LeafStatus.checkedLocal,
    target := "Define the countable-discrete path-space statement boundary",
    input := "HewittSavageData, ZeroOneConclusion, Countable E, MeasurableSingletonClass E",
    output := "CountableDiscreteStatementShape",
    blocker := "closed locally"
  },
  {
    id := "S1-M-288-L025c",
    refines := "S1-M-288-L025",
    budget := 20,
    status := Pub07LeafStatus.checkedLocal,
    target := "Show the full Hewitt-Savage statement specializes to the finite-valued boundary",
    input := "StatementShape",
    output := "finiteValuedStatementShape_of_statementShape",
    blocker := "closed locally"
  },
  {
    id := "S1-M-288-L025d",
    refines := "S1-M-288-L025",
    budget := 20,
    status := Pub07LeafStatus.checkedLocal,
    target := "Show the full Hewitt-Savage statement specializes to the countable-discrete boundary",
    input := "StatementShape",
    output := "countableDiscreteStatementShape_of_statementShape",
    blocker := "closed locally"
  },
  {
    id := "S1-M-288-L025e",
    refines := "S1-M-288-L025",
    budget := 20,
    status := Pub07LeafStatus.checkedLocal,
    target := "Reduce the finite-valued branch to the countable-discrete branch",
    input := "CountableDiscreteStatementShape and Fintype E",
    output := "finiteValuedStatementShape_of_countableDiscreteStatementShape",
    blocker := "closed locally"
  },
  {
    id := "S1-M-288-L025f",
    refines := "S1-M-288-L025",
    budget := 80,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Build the countable atom/cylinder generator for discrete path space",
    input := "Countable E and MeasurableSingletonClass E",
    output := "countable cylinder generator for events in Set (Nat -> E)",
    blocker := "needs selected product-measurable generator API for discrete sequence spaces"
  },
  {
    id := "S1-M-288-L025g",
    refines := "S1-M-288-L025",
    budget := 90,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Prove finite-permutation-invariant discrete events are tail-measurable/self-independent",
    input := "discrete cylinder generator, ExchangeableEvent, D.independent",
    output := "IndepSets {pulledBackEvent D} {pulledBackEvent D} D.mu for the discrete branch",
    blocker := "core exchangeable-to-tail/self-independence bridge remains unproved"
  },
  {
    id := "S1-M-288-L025h",
    refines := "S1-M-288-L025",
    budget := 30,
    status := Pub07LeafStatus.openFormalizationDebt,
    target := "Apply the checked self-independence algebra leaf to the discrete branch",
    input := "L025g and zeroOneConclusion_of_indep_pulledBackEvent_self",
    output := "FiniteValuedStatementShape or CountableDiscreteStatementShape terminal theorem",
    blocker := "blocked only by L025g; final algebra/application wrapper already exists"
  }
]

/-- Number of PUB-08 finite/discrete leaves recorded in the checked artifact. -/
def pub08FiniteDiscreteLeafCount : Nat :=
  pub08FiniteDiscreteLeaves.length

/-- The PUB-08 backfill currently records eight finite/discrete leaves. -/
theorem pub08FiniteDiscreteLeafCount_eq :
    pub08FiniteDiscreteLeafCount = 8 :=
  rfl

/-! ## PUB-09 public-open completion gate. -/

/-- Completion gates that must all close before the public Stage1 item can be checked. -/
inductive Pub09CompletionGate where
  | terminalTheorem
  | publicMergeBack
  | localValidationBackfill
  | statusSynchronization
  deriving DecidableEq, Repr

/-- PUB-09 gate status: every listed gate remains open in this child pass. -/
def pub09OpenCompletionGates : List Pub09CompletionGate := [
  Pub09CompletionGate.terminalTheorem,
  Pub09CompletionGate.publicMergeBack,
  Pub09CompletionGate.localValidationBackfill,
  Pub09CompletionGate.statusSynchronization
]

/-- There are four PUB-09 gates keeping the public item open. -/
theorem pub09OpenCompletionGateCount_eq :
    pub09OpenCompletionGates.length = 4 :=
  rfl

/--
PUB-09 decision for the serialized public surface: keep the public Stage1 item
open until the terminal theorem, public merge-back, local validation, and status
synchronization gates are all satisfied.
-/
def pub09PublicItemStatus : String :=
  "open: terminal theorem, public merge-back, local validation backfill, and status synchronization are not all satisfied"

/-! ## PUB-10 serialized public-document synchronization gate. -/

/-- Public documents that must be synchronized by a later serialized integrator. -/
inductive Pub10PublicSyncTarget where
  | stage1Blueprint
  | todos20260430
  | readme
  deriving DecidableEq, Repr

/-- The exact public surfaces covered by `S1-M-288-PUB-10`. -/
def pub10PublicSyncTargets : List Pub10PublicSyncTarget := [
  Pub10PublicSyncTarget.stage1Blueprint,
  Pub10PublicSyncTarget.todos20260430,
  Pub10PublicSyncTarget.readme
]

/-- PUB-10 records three public synchronization targets. -/
theorem pub10PublicSyncTargetCount_eq :
    pub10PublicSyncTargets.length = 3 :=
  rfl

/--
PUB-10 decision: public-document synchronization is deferred to a serialized
integrator pass and must not mark the parent theorem complete unless all
completion gates have closed.
-/
def pub10SerializedSyncGate : String :=
  "defer Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, and README.md synchronization until terminal theorem, public merge-back, local validation, status synchronization, and no-residual-repo-local-integration-debt gates are satisfied"

end S1_M_288
end Stage1
end AwesomeTheorems
