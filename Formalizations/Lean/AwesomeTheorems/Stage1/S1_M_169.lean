import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Measure.LevyConvergence
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Bochner.VitaliCaratheodory
import Mathlib.Topology.Semicontinuity.Basic
import Mathlib.Analysis.Convex.StoneSeparation
import Mathlib.Analysis.LocallyConvex.Separation

/-!
# S1-M-169 / THM-M-1184: Kantorovich duality

This Stage1 artifact records a conservative Lean 4 statement-shape boundary for
Kantorovich duality in optimal transport.

The pinned mathlib snapshot has probability measures, product measures,
marginal maps, lower semicontinuity, nonnegative extended integrals, and order
suprema/infima.  This audit did not find a terminal theorem proving the
Kantorovich primal-dual equality.

The declarations below therefore normalize the primal transport plans, dual
feasible potentials, primal infimum, dual supremum, and the missing equality
package without adding proof placeholders.  The checked theorems are wrappers
around available mathlib facts or definitional order facts.

Child task `S1-M-169-C001` fixes the Stage1 target signature as the compact
metric specialization below: Borel probability measures on compact metric
spaces, lower-semicontinuous nonnegative extended-real cost, and measurable
`ENNReal` dual potentials.  The signed-real continuous or integrable potential
formulation is left as a later bridge theorem because the current local
measure/integral surface can state and validate the `ENNReal` interface without
new axioms or placeholders.

Child task `S1-M-169-C003` proves the weak-duality branch for this chosen
`ENNReal` formal statement: marginal push-forwards transport the two potential
`lintegral`s to the plan measure, and pointwise dual feasibility integrates to
`DualSup μ ν c ≤ PrimalInf μ ν c`.

Child task `S1-M-169-C004` adds repo-local wrappers for the compactness/tightness
branch available from pinned mathlib: transport plans are viewed as a subset of
`ProbabilityMeasure (X × Y)`, compact product spaces make the corresponding
measure set tight, and Prokhorov's compactness API gives compactness of the
closure of that set. The fixed-marginal subset closedness needed for actual
attainment remains an explicit formalization leaf rather than being treated as
completed.

Child task `S1-M-169-C005` adds the safe repo-local lower-semicontinuity slice
currently available from pinned mathlib's Portmanteau API: weak convergence of
product probability measures gives the liminf inequality for lintegrals of
nonnegative continuous real costs. The full lower-semicontinuous `ENNReal`
primal-cost theorem remains a formalization leaf because this local closure has
not yet connected `LowerSemicontinuous c` to a monotone approximation by such
continuous costs along weakly convergent transport plans.

Child task `S1-M-169-C006` records the reverse-inequality/no-gap boundary:
pinned mathlib supplies generic Stone and Hahn-Banach separation tools, but this
pass did not find or construct the optimal-transport-specific separation,
c-transform, or dual-potential approximation theorem needed to prove
`PrimalInf μ ν c ≤ DualSup μ ν c`.  The local certificate and no-gap wrappers
below are therefore checked integration targets, not a completed Kantorovich
duality proof.

Child task `S1-M-169-C007` records the external-proof integration gate.  This
pass did not locate a Lean 4 proof of Kantorovich duality that can be pinned in
Lake, imported, and checked locally.  The theorem therefore remains
`formalization_debt`, not completed and not `repo_local_integration_debt`.
Any future external proof must enter this repository's validation closure before
the Stage1 theorem can be marked complete.

Child task `S1-M-169-C008` removes the raw primal-dual equality field from the
Stage1 data package.  The data package now carries the remaining reverse
inequality proof obligation, while the equality itself is exposed only through
the checked local theorem wrapper `primalInf_eq_dualSup_of_data`, whose proof
combines that reverse inequality with the repo-local weak-duality theorem.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace AwesomeTheorems.Stage1.S1_M_169

universe u v

variable {X : Type u} {Y : Type v} [MeasurableSpace X] [MeasurableSpace Y]

/--
A transport plan between two probability measures.

The plan is a probability measure on the product whose two coordinate
push-forwards are the prescribed marginals.
-/
structure TransportPlan (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Type (max u v) where
  plan : Measure (X × Y)
  isProbability : IsProbabilityMeasure plan
  fst_marginal : Measure.map Prod.fst plan = (μ : Measure X)
  snd_marginal : Measure.map Prod.snd plan = (ν : Measure Y)

instance (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (γ : TransportPlan μ ν) : IsProbabilityMeasure γ.plan :=
  γ.isProbability

/-- View a transport plan as a probability measure on the product. -/
def TransportPlan.toProbabilityMeasure {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) : ProbabilityMeasure (X × Y) :=
  ⟨γ.plan, γ.isProbability⟩

/--
The independent product coupling, checked against mathlib's product-measure
marginal theorems.
-/
def independentPlan (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    TransportPlan μ ν where
  plan := (μ : Measure X).prod (ν : Measure Y)
  isProbability := by infer_instance
  fst_marginal := by
    rw [Measure.map_fst_prod]
    simp
  snd_marginal := by
    rw [Measure.map_snd_prod]
    simp

/--
A nonnegative extended-real dual feasible pair.

This is a statement-shape candidate rather than the final most general
Kantorovich-duality interface: classical presentations often use signed
integrable or continuous potentials.  The nonnegative extended-real version is
kept here because it is directly expressible with the current local mathlib
measure/integral APIs and still exposes the primal-dual formalization boundary.
-/
structure KantorovichDualPair (c : X × Y → ℝ≥0∞) : Type (max u v) where
  phi : X → ℝ≥0∞
  psi : Y → ℝ≥0∞
  phi_measurable : Measurable phi
  psi_measurable : Measurable psi
  feasible : ∀ x y, phi x + psi y ≤ c (x, y)

/-- The zero pair is always dual feasible for an `ENNReal` cost. -/
def zeroDualPair (c : X × Y → ℝ≥0∞) : KantorovichDualPair c where
  phi := fun _ => 0
  psi := fun _ => 0
  phi_measurable := measurable_const
  psi_measurable := measurable_const
  feasible := by simp

/-- The primal cost of a transport plan. -/
def PrimalValue {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (γ : TransportPlan μ ν) : ℝ≥0∞ :=
  ∫⁻ z, c z ∂γ.plan

/-- The dual objective value of a feasible pair. -/
def DualValue (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) (p : KantorovichDualPair c) : ℝ≥0∞ :=
  (∫⁻ x, p.phi x ∂(μ : Measure X)) + (∫⁻ y, p.psi y ∂(ν : Measure Y))

/-- The primal optimal-transport value as an infimum over transport plans. -/
def PrimalInf (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) : ℝ≥0∞ :=
  ⨅ γ : TransportPlan μ ν, PrimalValue c γ

/-- The dual value as a supremum over feasible potential pairs. -/
def DualSup (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) : ℝ≥0∞ :=
  ⨆ p : KantorovichDualPair c, DualValue μ ν c p

/--
Data package for the remaining Kantorovich-duality proof obligations.

A terminal formalization should replace the abstract compactness, tightness, and
dual approximation fields by concrete hypotheses and prove
`reverse_inequality`.  The primal-dual equality is deliberately not a field of
this structure; it is derived by the local theorem wrapper
`primalInf_eq_dualSup_of_data`.
-/
structure KantorovichDualityData
    [TopologicalSpace X] [TopologicalSpace Y]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) : Type (max u v) where
  cost_lowerSemicontinuous : LowerSemicontinuous c
  primal_admissible : TransportPlan μ ν
  dual_admissible : KantorovichDualPair c
  tightness_or_compactness_package : Prop
  tightness_or_compactness_proof : tightness_or_compactness_package
  dual_attainment_or_approximation_package : Prop
  dual_attainment_or_approximation_proof : dual_attainment_or_approximation_package
  weak_duality_package : Prop
  weak_duality_proof : weak_duality_package
  reverse_inequality : PrimalInf μ ν c ≤ DualSup μ ν c

/--
Normalized Stage1 statement shape for Kantorovich duality.

For every pair of probability measures on Borel topological spaces and every
lower-semicontinuous nonnegative extended cost, the theorem asserts that the
transport-cost infimum equals the supremum of feasible dual potentials, packaged
with the auxiliary compactness and approximation data needed by a future
terminal proof.
-/
def StatementShape
    (X : Type u) (Y : Type v)
    [TopologicalSpace X] [MeasurableSpace X] [BorelSpace X]
    [TopologicalSpace Y] [MeasurableSpace Y] [BorelSpace Y] : Prop :=
  ∀ (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞),
    LowerSemicontinuous c →
      Nonempty (KantorovichDualityData μ ν c)

/-- The statement shape unfolds to the normalized duality-data package. -/
theorem statementShape_iff
    (X : Type u) (Y : Type v)
    [TopologicalSpace X] [MeasurableSpace X] [BorelSpace X]
    [TopologicalSpace Y] [MeasurableSpace Y] [BorelSpace Y] :
    StatementShape X Y ↔
      ∀ (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
        (c : X × Y → ℝ≥0∞),
        LowerSemicontinuous c →
          Nonempty (KantorovichDualityData μ ν c) :=
  Iff.rfl

/--
Final Stage1 signature selected by child task `S1-M-169-C001`.

The first terminal target is the compact metric case.  This keeps transport-plan
compactness/tightness as a compact-space branch and uses `ENNReal` objectives
throughout, avoiding a premature signed-real potential API before the
lintegral-to-integral bridge has been proved or imported.
-/
def CompactMetricStatementShape
    (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y] :
    Prop :=
  ∀ (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞),
    LowerSemicontinuous c →
      Nonempty (KantorovichDualityData μ ν c)

/--
The compact metric signature is exactly the normalized statement-shape package
under compact metric hypotheses.
-/
theorem compactMetricStatementShape_iff_statementShape
    (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y] :
    CompactMetricStatementShape X Y ↔ StatementShape X Y :=
  Iff.rfl

/-- The first marginal field is available as a theorem wrapper. -/
theorem fst_marginal_eq {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) :
    Measure.map Prod.fst γ.plan = (μ : Measure X) :=
  γ.fst_marginal

/-- The second marginal field is available as a theorem wrapper. -/
theorem snd_marginal_eq {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) :
    Measure.map Prod.snd γ.plan = (ν : Measure Y) :=
  γ.snd_marginal

/-- The product coupling has the expected first marginal. -/
theorem independentPlan_fst (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Measure.map Prod.fst (independentPlan μ ν).plan = (μ : Measure X) :=
  (independentPlan μ ν).fst_marginal

/-- The product coupling has the expected second marginal. -/
theorem independentPlan_snd (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Measure.map Prod.snd (independentPlan μ ν).plan = (ν : Measure Y) :=
  (independentPlan μ ν).snd_marginal

/-- The primal infimum is bounded by the value of each admissible plan. -/
theorem primalInf_le_plan {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (γ : TransportPlan μ ν) :
    PrimalInf μ ν c ≤ PrimalValue c γ :=
  iInf_le _ γ

/-- Every dual feasible pair has value bounded above by the dual supremum. -/
theorem dualValue_le_dualSup {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (p : KantorovichDualPair c) :
    DualValue μ ν c p ≤ DualSup μ ν c :=
  le_iSup _ p

/-- The zero feasible pair has zero dual objective value. -/
theorem zeroDualPair_value (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) :
    DualValue μ ν c (zeroDualPair c) = 0 := by
  simp [DualValue, zeroDualPair]

/--
First-marginal change of variables for a transport plan.

This is the marginal-pushforward leaf used by weak duality.
-/
theorem lintegral_fst_of_transportPlan {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) {f : X → ℝ≥0∞} (hf : Measurable f) :
    (∫⁻ z, f z.1 ∂γ.plan) = ∫⁻ x, f x ∂(μ : Measure X) := by
  rw [← γ.fst_marginal]
  exact (lintegral_map hf measurable_fst).symm

/--
Second-marginal change of variables for a transport plan.

This is the second marginal-pushforward leaf used by weak duality.
-/
theorem lintegral_snd_of_transportPlan {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) {g : Y → ℝ≥0∞} (hg : Measurable g) :
    (∫⁻ z, g z.2 ∂γ.plan) = ∫⁻ y, g y ∂(ν : Measure Y) := by
  rw [← γ.snd_marginal]
  exact (lintegral_map hg measurable_snd).symm

/--
Weak duality against a fixed transport plan.

The proof splits into the two marginal `lintegral` leaves above, additivity of
`lintegral` for measurable `ENNReal` functions, and monotonicity from pointwise
dual feasibility.
-/
theorem weakDuality_dualValue_le_primalValue
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (p : KantorovichDualPair c) (γ : TransportPlan μ ν) :
    DualValue μ ν c p ≤ PrimalValue c γ := by
  calc
    DualValue μ ν c p
        = (∫⁻ x, p.phi x ∂(μ : Measure X)) + ∫⁻ y, p.psi y ∂(ν : Measure Y) := by
            rfl
    _   = (∫⁻ z, p.phi z.1 ∂γ.plan) + ∫⁻ z, p.psi z.2 ∂γ.plan := by
            rw [lintegral_fst_of_transportPlan γ p.phi_measurable,
              lintegral_snd_of_transportPlan γ p.psi_measurable]
    _ = ∫⁻ z, p.phi z.1 + p.psi z.2 ∂γ.plan := by
          exact (lintegral_add_left (p.phi_measurable.comp measurable_fst) _).symm
    _ ≤ PrimalValue c γ := by
          exact lintegral_mono fun z => p.feasible z.1 z.2

/-- Weak duality for one feasible dual pair against the primal infimum. -/
theorem dualValue_le_primalInf {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) (p : KantorovichDualPair c) :
    DualValue μ ν c p ≤ PrimalInf μ ν c :=
  le_iInf fun γ => weakDuality_dualValue_le_primalValue c p γ

/-- Repo-local weak duality for the selected `ENNReal` Stage1 statement. -/
theorem weakDuality_dualSup_le_primalInf {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) :
    DualSup μ ν c ≤ PrimalInf μ ν c :=
  iSup_le fun p => dualValue_le_primalInf c p

/--
The reverse inequality needed for Kantorovich no-duality-gap.

This is the branch targeted by KDT-06.  The current file does not prove this
property for lower-semicontinuous costs; it only names the exact repo-local gate
that a future separation/c-transform construction must close.
-/
def ReverseDualInequality {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ≥0∞) : Prop :=
  PrimalInf μ ν c ≤ DualSup μ ν c

/--
Checked certificate shape for the KDT-06 dual approximation/separation branch.

The abstract package fields are deliberately not used as axioms: constructing a
value of this structure still requires an actual proof of `reverse_inequality`.
They record the two mathematical subpackages expected in a terminal proof:
separation of the primal feasible-cost cone and construction/approximation of
admissible dual potentials.
-/
structure DualApproximationSeparationCertificate
    [TopologicalSpace X] [TopologicalSpace Y]
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y)
    (c : X × Y → ℝ≥0∞) : Type (max u v) where
  cost_lowerSemicontinuous : LowerSemicontinuous c
  separation_package : Prop
  separation_proof : separation_package
  potential_approximation_package : Prop
  potential_approximation_proof : potential_approximation_package
  reverse_inequality : ReverseDualInequality (μ := μ) (ν := ν) c

/-- A completed KDT-06 certificate yields the reverse primal-dual inequality. -/
theorem primalInf_le_dualSup_of_dualApproximationSeparationCertificate
    [TopologicalSpace X] [TopologicalSpace Y]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {c : X × Y → ℝ≥0∞}
    (cert : DualApproximationSeparationCertificate μ ν c) :
    PrimalInf μ ν c ≤ DualSup μ ν c :=
  cert.reverse_inequality

/--
No duality gap follows from a completed KDT-06 certificate together with the
repo-local weak-duality theorem.
-/
theorem primalInf_eq_dualSup_of_dualApproximationSeparationCertificate
    [TopologicalSpace X] [TopologicalSpace Y]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {c : X × Y → ℝ≥0∞}
    (cert : DualApproximationSeparationCertificate μ ν c) :
    PrimalInf μ ν c = DualSup μ ν c :=
  le_antisymm cert.reverse_inequality (weakDuality_dualSup_le_primalInf c)

/-- Local wrapper for mathlib's Stone convex separation theorem. -/
theorem stoneSeparation_convex_convex_compl_subset
    {𝕜 : Type*} {E : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜]
    [AddCommGroup E] [Module 𝕜 E] {s t : Set E}
    (hs : Convex 𝕜 s) (ht : Convex 𝕜 t) (hst : Disjoint s t) :
    ∃ C : Set E, Convex 𝕜 C ∧ Convex 𝕜 Cᶜ ∧ s ⊆ C ∧ t ⊆ Cᶜ :=
  exists_convex_convex_compl_subset hs ht hst

/-- Local wrapper for the open-set Hahn-Banach separation theorem. -/
theorem hahnBanach_open_separation_anchor
    {E : Type*} [TopologicalSpace E] [AddCommGroup E] [Module ℝ E]
    [IsTopologicalAddGroup E] [ContinuousSMul ℝ E] {s t : Set E}
    (hs_conv : Convex ℝ s) (hs_open : IsOpen s) (ht_conv : Convex ℝ t)
    (hst : Disjoint s t) :
    ∃ (f : StrongDual ℝ E) (u : ℝ),
      (∀ a ∈ s, f a < u) ∧ ∀ b ∈ t, u ≤ f b :=
  geometric_hahn_banach_open hs_conv hs_open ht_conv hst

/-- Local wrapper for the compact/closed Hahn-Banach separation theorem. -/
theorem hahnBanach_compact_closed_separation_anchor
    {E : Type*} [TopologicalSpace E] [AddCommGroup E] [Module ℝ E]
    [IsTopologicalAddGroup E] [ContinuousSMul ℝ E] [LocallyConvexSpace ℝ E]
    {s t : Set E}
    (hs_conv : Convex ℝ s) (hs_compact : IsCompact s)
    (ht_conv : Convex ℝ t) (ht_closed : IsClosed t) (hst : Disjoint s t) :
    ∃ (f : StrongDual ℝ E) (u v : ℝ),
      (∀ a ∈ s, f a < u) ∧ u < v ∧ ∀ b ∈ t, v < f b :=
  geometric_hahn_banach_compact_closed hs_conv hs_compact ht_conv ht_closed hst

/--
Local theorem wrapper deriving the primal-dual equality from terminal data.

KDT-08 requires the equality to live in a theorem body rather than as a raw data
field.  The proof is repo-local: the terminal data supplies only the reverse
inequality branch, and `weakDuality_dualSup_le_primalInf` supplies the checked
weak-duality branch.
-/
theorem primalInf_eq_dualSup_of_data
    [TopologicalSpace X] [TopologicalSpace Y]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {c : X × Y → ℝ≥0∞}
    (d : KantorovichDualityData μ ν c) :
    PrimalInf μ ν c = DualSup μ ν c :=
  le_antisymm d.reverse_inequality (weakDuality_dualSup_le_primalInf c)

/-- The set of product probability measures coming from admissible transport plans. -/
def transportPlanProbabilityMeasureSet (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    Set (ProbabilityMeasure (X × Y)) :=
  {π | ∃ γ : TransportPlan μ ν, γ.toProbabilityMeasure = π}

/-- The admissible transport-plan probability-measure set is nonempty. -/
theorem transportPlanProbabilityMeasureSet_nonempty
    (μ : ProbabilityMeasure X) (ν : ProbabilityMeasure Y) :
    (transportPlanProbabilityMeasureSet μ ν).Nonempty := by
  refine ⟨(independentPlan μ ν).toProbabilityMeasure, ?_⟩
  exact ⟨independentPlan μ ν, rfl⟩

/-- The probability-measure space on a compact product is compact by mathlib's Prokhorov API. -/
theorem compactSpace_probabilityMeasure_product
    [TopologicalSpace (X × Y)] [T2Space (X × Y)] [BorelSpace (X × Y)]
    [CompactSpace (X × Y)] :
    CompactSpace (ProbabilityMeasure (X × Y)) :=
  inferInstance

/-- In a compact product space, the family of transport-plan measures is tight. -/
theorem transportPlan_measureSet_tight_of_compactSpace
    [TopologicalSpace (X × Y)] [CompactSpace (X × Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y} :
    IsTightMeasureSet {m : Measure (X × Y) | ∃ γ : TransportPlan μ ν, γ.plan = m} :=
  IsTightMeasureSet.of_compactSpace

/-- Coercing the probability-measure view of a transport plan recovers its underlying measure. -/
theorem TransportPlan.coe_toProbabilityMeasure {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (γ : TransportPlan μ ν) :
    (γ.toProbabilityMeasure : Measure (X × Y)) = γ.plan :=
  rfl

/--
In a compact product space, the probability measures arising from admissible
transport plans form a tight measure set after coercion to `Measure`.
-/
theorem transportPlan_probabilityMeasureSet_tight_of_compactSpace
    [TopologicalSpace (X × Y)] [CompactSpace (X × Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y} :
    IsTightMeasureSet
      {m : Measure (X × Y) |
        ∃ π ∈ transportPlanProbabilityMeasureSet μ ν, (π : Measure (X × Y)) = m} :=
  IsTightMeasureSet.of_compactSpace

/--
Prokhorov compactness wrapper for the admissible transport-plan locus.

This proves compactness of the closure of the repo-local transport-plan subset
in `ProbabilityMeasure (X × Y)`. Turning this into compactness of the exact
fixed-marginal subtype still requires a closedness proof for the marginal
constraints.
-/
theorem transportPlan_probabilityMeasureSet_closure_isCompact_of_compactSpace
    [TopologicalSpace (X × Y)] [T2Space (X × Y)] [BorelSpace (X × Y)]
    [CompactSpace (X × Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y} :
    IsCompact (closure (transportPlanProbabilityMeasureSet μ ν)) :=
  isCompact_closure_of_isTightMeasureSet
    transportPlan_probabilityMeasureSet_tight_of_compactSpace

/--
Primal value for a real-valued cost, coerced to the nonnegative extended-real
integrand used by `PrimalValue`.

This is the checked approximation interface used by the C005 Portmanteau leaf:
continuous nonnegative real costs are a safe repo-local slice of the eventual
lower-semicontinuous `ENNReal` cost theorem.
-/
def PrimalValueOfReal {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    (c : X × Y → ℝ) (γ : TransportPlan μ ν) : ℝ≥0∞ :=
  ∫⁻ z, ENNReal.ofReal (c z) ∂γ.plan

/--
Portmanteau lower-bound wrapper for nonnegative continuous real costs.

This is a direct wrapper around
`MeasureTheory.lintegral_le_liminf_lintegral_of_forall_isOpen_measure_le_liminf_measure`
and
`MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto`.
-/
theorem lintegral_ofReal_le_liminf_of_tendsto_probabilityMeasure
    {Ω : Type*} [MeasurableSpace Ω] [TopologicalSpace Ω]
    [OpensMeasurableSpace Ω] [HasOuterApproxClosed Ω]
    {ρ : ProbabilityMeasure Ω} {ρs : ℕ → ProbabilityMeasure Ω}
    {c : Ω → ℝ} (hc_cont : Continuous c) (hc_nonneg : 0 ≤ c)
    (hρs : Filter.Tendsto ρs Filter.atTop (nhds ρ)) :
    ∫⁻ z, ENNReal.ofReal (c z) ∂(ρ : Measure Ω) ≤
      Filter.liminf
    (fun n => ∫⁻ z, ENNReal.ofReal (c z) ∂(ρs n : Measure Ω)) Filter.atTop :=
  MeasureTheory.lintegral_le_liminf_lintegral_of_forall_isOpen_measure_le_liminf_measure
    hc_cont hc_nonneg
    (fun _G hG => MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto hρs hG)

/--
Transport-plan lower-bound wrapper for nonnegative continuous real costs.

The theorem is intentionally limited to `ENNReal.ofReal c` for continuous
nonnegative real `c`.  It records the checked Portmanteau leaf needed before a
future monotone-approximation step can prove lower semicontinuity for arbitrary
lower-semicontinuous `ENNReal` costs.
-/
theorem primalValueOfReal_le_liminf_of_tendsto_transportPlan
    [TopologicalSpace (X × Y)] [OpensMeasurableSpace (X × Y)]
    [HasOuterApproxClosed (X × Y)]
    {μ : ProbabilityMeasure X} {ν : ProbabilityMeasure Y}
    {γ : TransportPlan μ ν} {γs : ℕ → TransportPlan μ ν}
    {c : X × Y → ℝ} (hc_cont : Continuous c) (hc_nonneg : 0 ≤ c)
    (hγs : Filter.Tendsto (fun n => (γs n).toProbabilityMeasure) Filter.atTop
      (nhds γ.toProbabilityMeasure)) :
    PrimalValueOfReal c γ ≤
      Filter.liminf (fun n => PrimalValueOfReal c (γs n)) Filter.atTop := by
  simpa [PrimalValueOfReal, TransportPlan.toProbabilityMeasure] using
    lintegral_ofReal_le_liminf_of_tendsto_probabilityMeasure
      (ρ := γ.toProbabilityMeasure) (ρs := fun n => (γs n).toProbabilityMeasure)
      hc_cont hc_nonneg hγs

/-- M0387-level local leaf ledger for the C005 lower-semicontinuity branch. -/
def lowerSemicontinuityLeafLedger : List String := [
  "KDT05-L01 local_wrapper_upstream_mathlib: lintegral_ofReal_le_liminf_of_tendsto_probabilityMeasure wraps Portmanteau open-set liminf for nonnegative continuous real costs.",
  "KDT05-L02 local_proof_body: primalValueOfReal_le_liminf_of_tendsto_transportPlan specializes the Portmanteau wrapper to weakly convergent transport plans.",
  "KDT05-L03 unchecked formalization_debt: lift from continuous nonnegative real costs to lower-semicontinuous ENNReal costs via monotone approximation or a direct Portmanteau theorem.",
  "KDT05-L04 unchecked formalization_debt: combine the lower-semicontinuity theorem with compactness of the exact fixed-marginal transport-plan locus once KDT04-L07/L08 are closed.",
  "KDT05-L05 unchecked formalization_debt: expose the completed lower-semicontinuity package as a concrete field replacing the abstract primal branch in KantorovichDualityData."
]

/-- M0387-level local leaf ledger for the C006 reverse-inequality/separation branch. -/
def dualApproximationSeparationLeafLedger : List String := [
  "KDT06-L01 local_proof_body: ReverseDualInequality names the exact PrimalInf <= DualSup target required for no duality gap.",
  "KDT06-L02 local_proof_body: DualApproximationSeparationCertificate packages the future separation and potential-approximation proof obligations without adding axioms.",
  "KDT06-L03 local_proof_body: primalInf_le_dualSup_of_dualApproximationSeparationCertificate extracts the reverse inequality from a completed certificate.",
  "KDT06-L04 local_proof_body: primalInf_eq_dualSup_of_dualApproximationSeparationCertificate combines the certificate with checked weakDuality_dualSup_le_primalInf.",
  "KDT06-L05 local_wrapper_upstream_mathlib: stoneSeparation_convex_convex_compl_subset wraps exists_convex_convex_compl_subset.",
  "KDT06-L06 local_wrapper_upstream_mathlib: hahnBanach_open_separation_anchor wraps geometric_hahn_banach_open.",
  "KDT06-L07 local_wrapper_upstream_mathlib: hahnBanach_compact_closed_separation_anchor wraps geometric_hahn_banach_compact_closed.",
  "KDT06-L08 unchecked formalization_debt: construct the locally convex primal/dual cone or epigraph space for the selected compact-metric transport statement.",
  "KDT06-L09 unchecked formalization_debt: prove convexity, topological closure/openness, and disjointness hypotheses needed to apply a separation theorem to the optimal-transport cone.",
  "KDT06-L10 unchecked formalization_debt: turn the separating functional into measurable ENNReal dual potentials satisfying phi x + psi y <= c (x, y).",
  "KDT06-L11 unchecked formalization_debt: prove the approximation/supremum argument yielding PrimalInf μ ν c <= DualSup μ ν c.",
  "KDT06-L12 unchecked formalization_debt: replace the abstract certificate with a local proof body or a pinned external dependency if one is found."
]

/--
M0387-level local leaf ledger for the C007 external-proof integration gate.

This ledger is intentionally documentary.  It does not assert theorem closure:
it records that no external Lean 4 Kantorovich-duality proof body was located
for pin/import/check during this child pass, so there is no anchor-only evidence
to count as completion.
-/
def externalProofIntegrationLeafLedger : List String := [
  "KDT07-L01 local_audit: pinned mathlib at 8a178386ffc0f5fef0b77738bb5449d50efeea95 has adjacent probability, tightness, Portmanteau, and separation APIs, but no terminal Kantorovich-duality theorem was located.",
  "KDT07-L02 local_audit: repo-local search found transport artifacts S1_M_151, S1_M_169, and S1_M_280, but no completed proof of PrimalInf = DualSup for Kantorovich duality.",
  "KDT07-L03 external_audit: public web search for Lean 4 Kantorovich duality did not locate a primary Lean 4 source repository with a terminal theorem to pin.",
  "KDT07-L04 external_audit_blocker: unauthenticated GitHub code search was rate-limited on 2026-05-01; authenticated source search remains a required follow-up before any completion claim.",
  "KDT07-L05 external_nonmatch: GitHub repository search for Kantorovich Lean returned victorliu5296/newton-kantorovich-theorem, which concerns the Newton-Kantorovich theorem and is not an optimal-transport Kantorovich-duality proof.",
  "KDT07-L06 gate: no external_upstream_anchor_only evidence is counted as completion, and no repo_local_integration_debt is allowed in a completed state.",
  "KDT07-L07 unchecked formalization_debt: if a future external Lean 4 proof is located, pin/import/check it through Lake or record a concrete blocker such as toolchain mismatch, dependency conflict, missing license permission, or incompatible theorem signature."
]

/-- Current C007 machine-status classification for the external-proof gate. -/
def externalProofIntegrationStatus : String :=
  "not_completed_formalization_debt_no_external_lean4_proof_located_to_pin_import_check"

/--
M0387-level local leaf ledger for the C008 equality-field replacement gate.

This is code/proof progress, but not terminal theorem completion: the raw data
equality field has been removed and replaced by a theorem wrapper, while the
reverse inequality remains a formalization-debt proof obligation unless supplied
by a local proof body or a pinned dependency.
-/
def dataPackageEqualityReplacementLeafLedger : List String := [
  "KDT08-L01 local_proof_body: KantorovichDualityData no longer contains the raw field primal_dual_equality.",
  "KDT08-L02 local_proof_body: KantorovichDualityData carries only the remaining reverse_inequality proof obligation PrimalInf μ ν c <= DualSup μ ν c.",
  "KDT08-L03 local_proof_body: primalInf_eq_dualSup_of_data is the theorem wrapper deriving equality by le_antisymm from reverse_inequality and weakDuality_dualSup_le_primalInf.",
  "KDT08-L04 unchecked formalization_debt: replace reverse_inequality by a concrete compactness/lower-semicontinuity/separation proof package or a pinned external theorem before claiming terminal Kantorovich-duality completion.",
  "KDT08-L05 gate: no completed-state repo_local_integration_debt is retained; this wrapper is local but the parent theorem remains not completed until the reverse branch is repo-locally closed."
]

/-- Current C008 machine-status classification for the equality-field replacement. -/
def dataPackageEqualityReplacementStatus : String :=
  "local_theorem_wrapper_added_parent_not_completed_reverse_inequality_formalization_debt"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.MeasureTheory.Measure.Prod",
  "Mathlib.MeasureTheory.Measure.Prokhorov",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.LevyConvergence",
  "Mathlib.MeasureTheory.Measure.LevyProkhorovMetric",
  "Mathlib.MeasureTheory.Measure.Tight",
  "Mathlib.MeasureTheory.Measure.Regular",
  "Mathlib.MeasureTheory.Integral.Lebesgue.Map",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.VitaliCaratheodory",
  "Mathlib.Topology.Semicontinuity.Basic",
  "Mathlib.Analysis.Convex.StoneSeparation",
  "Mathlib.Analysis.LocallyConvex.Separation"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.ProbabilityMeasure",
  "MeasureTheory.IsProbabilityMeasure",
  "MeasureTheory.Measure.prod",
  "MeasureTheory.Measure.map_fst_prod",
  "MeasureTheory.Measure.map_snd_prod",
  "MeasureTheory.IsTightMeasureSet",
  "MeasureTheory.isTightMeasureSet_iff_exists_isCompact_measure_compl_le",
  "MeasureTheory.IsTightMeasureSet.of_compactSpace",
  "isCompact_closure_of_isTightMeasureSet",
  "isCompact_setOf_probabilityMeasure_mass_eq_compl_isCompact_le",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto",
  "MeasureTheory.ProbabilityMeasure.limsup_measure_closed_le_of_tendsto",
  "MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto",
  "MeasureTheory.tendsto_of_forall_isOpen_le_liminf",
  "MeasureTheory.lintegral_le_liminf_lintegral_of_forall_isOpen_measure_le_liminf_measure",
  "MeasureTheory.levyProkhorovEDist",
  "MeasureTheory.levyProkhorovDist",
  "MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure",
  "MeasureTheory.LevyProkhorov.levyProkhorovDist_metricSpace_probabilityMeasure",
  "MeasureTheory.LevyProkhorov.le_convergenceInDistribution",
  "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
  "MeasureTheory.exists_le_lowerSemicontinuous_lintegral_ge",
  "MeasureTheory.exists_lt_lowerSemicontinuous_integral_lt",
  "MeasureTheory.exists_upperSemicontinuous_lt_integral_gt",
  "MeasureTheory.lintegral_map",
  "MeasureTheory.lintegral_add_left",
  "MeasureTheory.lintegral_mono",
  "stoneSeparation_convex_convex_compl_subset",
  "hahnBanach_open_separation_anchor",
  "hahnBanach_compact_closed_separation_anchor",
  "geometric_hahn_banach_open",
  "geometric_hahn_banach_compact_closed",
  "exists_convex_convex_compl_subset",
  "MeasureTheory.Measure.InnerRegular",
  "MeasureTheory.isTightMeasureSet_singleton_of_innerRegular",
  "MetricSpace",
  "CompactSpace",
  "LowerSemicontinuous",
  "lintegral",
  "iInf",
  "iSup"
]

/-- M0387-level local leaf ledger for the compactness/tightness child branch. -/
def compactnessTightnessLeafLedger : List String := [
  "KDT04-L01 local_proof_body: transportPlanProbabilityMeasureSet packages admissible plans as product probability measures.",
  "KDT04-L02 local_proof_body: transportPlanProbabilityMeasureSet_nonempty uses independentPlan.",
  "KDT04-L03 local_wrapper_upstream_mathlib: compactSpace_probabilityMeasure_product uses ProbabilityMeasure compactness from Prokhorov API.",
  "KDT04-L04 local_wrapper_upstream_mathlib: transportPlan_measureSet_tight_of_compactSpace uses IsTightMeasureSet.of_compactSpace.",
  "KDT04-L05 local_wrapper_upstream_mathlib: transportPlan_probabilityMeasureSet_tight_of_compactSpace uses IsTightMeasureSet.of_compactSpace after coercion.",
  "KDT04-L06 local_wrapper_upstream_mathlib: transportPlan_probabilityMeasureSet_closure_isCompact_of_compactSpace uses isCompact_closure_of_isTightMeasureSet.",
  "KDT04-L07 unchecked formalization_debt: prove closedness of fixed-marginal constraints under weak convergence.",
  "KDT04-L08 unchecked formalization_debt: upgrade closure compactness to compactness of the exact transport-plan subtype or closed set."
]

/--
Search terms that did not locate a terminal Kantorovich-duality theorem in
pinned mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Kantorovich",
  "Kantorovich duality",
  "OptimalTransport",
  "optimal transport",
  "Monge",
  "Wasserstein",
  "transport plan",
  "coupling",
  "dual potential",
  "c-transform",
  "cTransform",
  "Kantorovich potential",
  "cyclically monotone",
  "primal dual"
]

/--
Audit gaps after the expanded anchor pass.

The checked mathlib surface has tightness, Prokhorov compactness,
Levy-Prokhorov metrization, portmanteau/weak-convergence lemmas,
Vitali-Caratheodory semicontinuous integral approximation, and general convex
separation tools.  This pass did not find an optimal-transport-specific
transport-plan compactness theorem, c-transform API, or terminal
Kantorovich-duality theorem in pinned mathlib.
-/
def remainingAnchorGaps : List String := [
  "closedness/compactness of the subtype of probability measures with fixed product marginals",
  "lower-semicontinuity of the primal cost functional along weakly convergent transport plans",
  "Kantorovich c-transform and c-concave potential API",
  "dual reverse inequality/no-gap theorem specialized to optimal transport",
  "terminal theorem named Kantorovich duality or equivalent"
]

/-! ## Audit probes -/

#check TransportPlan
#check KantorovichDualPair
#check zeroDualPair
#check PrimalValue
#check DualValue
#check PrimalInf
#check DualSup
#check KantorovichDualityData
#check StatementShape
#check statementShape_iff
#check CompactMetricStatementShape
#check compactMetricStatementShape_iff_statementShape
#check independentPlan
#check primalInf_le_plan
#check dualValue_le_dualSup
#check zeroDualPair_value
#check lintegral_fst_of_transportPlan
#check lintegral_snd_of_transportPlan
#check weakDuality_dualValue_le_primalValue
#check dualValue_le_primalInf
#check weakDuality_dualSup_le_primalInf
#check ReverseDualInequality
#check DualApproximationSeparationCertificate
#check primalInf_le_dualSup_of_dualApproximationSeparationCertificate
#check primalInf_eq_dualSup_of_dualApproximationSeparationCertificate
#check stoneSeparation_convex_convex_compl_subset
#check hahnBanach_open_separation_anchor
#check hahnBanach_compact_closed_separation_anchor
#check primalInf_eq_dualSup_of_data
#check TransportPlan.toProbabilityMeasure
#check TransportPlan.coe_toProbabilityMeasure
#check transportPlanProbabilityMeasureSet
#check transportPlanProbabilityMeasureSet_nonempty
#check compactSpace_probabilityMeasure_product
#check transportPlan_measureSet_tight_of_compactSpace
#check transportPlan_probabilityMeasureSet_tight_of_compactSpace
#check transportPlan_probabilityMeasureSet_closure_isCompact_of_compactSpace
#check PrimalValueOfReal
#check lintegral_ofReal_le_liminf_of_tendsto_probabilityMeasure
#check primalValueOfReal_le_liminf_of_tendsto_transportPlan
#check compactnessTightnessLeafLedger
#check lowerSemicontinuityLeafLedger
#check dualApproximationSeparationLeafLedger
#check externalProofIntegrationLeafLedger
#check externalProofIntegrationStatus
#check dataPackageEqualityReplacementLeafLedger
#check dataPackageEqualityReplacementStatus
#check MeasureTheory.ProbabilityMeasure
#check MeasureTheory.IsTightMeasureSet
#check MeasureTheory.isTightMeasureSet_iff_exists_isCompact_measure_compl_le
#check MeasureTheory.IsTightMeasureSet.of_compactSpace
#check isCompact_closure_of_isTightMeasureSet
#check isCompact_setOf_probabilityMeasure_mass_eq_compl_isCompact_le
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto
#check MeasureTheory.ProbabilityMeasure.limsup_measure_closed_le_of_tendsto
#check MeasureTheory.ProbabilityMeasure.le_liminf_measure_open_of_tendsto
#check MeasureTheory.tendsto_of_forall_isOpen_le_liminf
#check MeasureTheory.lintegral_le_liminf_lintegral_of_forall_isOpen_measure_le_liminf_measure
#check MeasureTheory.levyProkhorovEDist
#check MeasureTheory.levyProkhorovDist
#check MeasureTheory.LevyProkhorov.instPseudoMetricSpaceProbabilityMeasure
#check MeasureTheory.LevyProkhorov.levyProkhorovDist_metricSpace_probabilityMeasure
#check MeasureTheory.LevyProkhorov.le_convergenceInDistribution
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#check MeasureTheory.exists_le_lowerSemicontinuous_lintegral_ge
#check MeasureTheory.exists_lt_lowerSemicontinuous_integral_lt
#check MeasureTheory.exists_upperSemicontinuous_lt_integral_gt
#check MeasureTheory.lintegral_map
#check MeasureTheory.lintegral_add_left
#check MeasureTheory.lintegral_mono
#check LowerSemicontinuous
#check geometric_hahn_banach_open
#check geometric_hahn_banach_compact_closed
#check exists_convex_convex_compl_subset

end AwesomeTheorems.Stage1.S1_M_169
