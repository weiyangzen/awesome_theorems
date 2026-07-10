import Mathlib.Probability.StrongLaw

/-!
# S1-M-265 / THM-M-0985: Kolmogorov strong law of large numbers

This Stage1 artifact records a checked Lean 4 wrapper for the Kolmogorov
strong law of large numbers.  The pinned mathlib theorem
`ProbabilityTheory.strong_law_ae` proves the Banach-valued iid integrable
version, and in fact only needs pairwise independence internally.

The statement shape below uses the more standard iid interface:
`ProbabilityTheory.iIndepFun` for independence of the whole sequence and
`ProbabilityTheory.IdentDistrib` for identical distribution.  The local wrapper
bridges `iIndepFun` to the pairwise independence hypothesis used by mathlib and
then calls the pinned theorem.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped MeasureTheory ProbabilityTheory Topology ENNReal NNReal
open scoped Function

namespace AwesomeTheorems.Stage1.S1_M_265

universe u v

/-- Empirical average of the first `n` values of a Banach-valued random sequence. -/
def empiricalAverage
    {Ω : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (X : ℕ → Ω → E) (n : ℕ) (ω : Ω) : E :=
  (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, X i ω)

/--
Normalized iid data for Kolmogorov's strong law.

The `isProbability` field records the classical probability-space boundary of
the theorem.  The pinned mathlib proof can derive this in the nontrivial case,
but retaining the field makes the Stage1 statement match the usual source
formulation.
-/
structure KolmogorovStrongLawData
    (Ω : Type u) [MeasurableSpace Ω]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E] where
  μ : Measure Ω
  isProbability : IsProbabilityMeasure μ
  X : ℕ → Ω → E
  integrable_zero : Integrable (X 0) μ
  independent : ProbabilityTheory.iIndepFun X μ
  identically_distributed : ∀ i, ProbabilityTheory.IdentDistrib (X i) (X 0) μ μ

/-- Almost-sure convergence conclusion of Kolmogorov's strong law. -/
def KolmogorovStrongLawConclusion
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) : Prop :=
  ∀ᵐ ω ∂D.μ,
    Tendsto (fun n : ℕ => empiricalAverage D.X n ω) atTop (𝓝 D.μ[D.X 0])

/--
Stage1 normalized statement shape for the iid Kolmogorov strong law of large
numbers.

This is closed below by a repo-local wrapper around pinned mathlib, so it is
not merely a proposition stub.
-/
def StatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
      [MeasurableSpace E] [BorelSpace E],
      ∀ D : KolmogorovStrongLawData Ω E,
        KolmogorovStrongLawConclusion D

/-- Real-valued classical specialization of the normalized Stage1 statement. -/
def RealStatementShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω],
    ∀ D : KolmogorovStrongLawData Ω ℝ,
      KolmogorovStrongLawConclusion D

/-- The statement-shape definition unfolds to the explicit normalized form. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (Ω : Type u) [MeasurableSpace Ω],
        ∀ (E : Type v) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
          [MeasurableSpace E] [BorelSpace E],
          ∀ D : KolmogorovStrongLawData Ω E,
            KolmogorovStrongLawConclusion D :=
  Iff.rfl

/-- Project the probability-space hypothesis from the normalized data package. -/
theorem isProbability
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) :
    IsProbabilityMeasure D.μ :=
  D.isProbability

/-- Project the integrability hypothesis from the normalized data package. -/
theorem integrable_zero
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) :
    Integrable (D.X 0) D.μ :=
  D.integrable_zero

/--
The iid independence interface gives the pairwise independence hypothesis used
by mathlib's Etemadi-style strong-law theorem.
-/
theorem pairwise_independent
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) :
    Pairwise (Function.onFun (fun Y Z => Y ⟂ᵢ[D.μ] Z) D.X) := by
  intro i j hij
  exact D.independent.indepFun hij

/-- Project identical distribution of each coordinate with the reference variable. -/
theorem identically_distributed
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) (i : ℕ) :
    ProbabilityTheory.IdentDistrib (D.X i) (D.X 0) D.μ D.μ :=
  D.identically_distributed i

/-- The empirical-average notation unfolds to mathlib's strong-law average. -/
theorem empiricalAverage_apply
    {Ω : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (X : ℕ → Ω → E) (n : ℕ) (ω : Ω) :
    empiricalAverage X n ω = (n : ℝ)⁻¹ • (∑ i ∈ Finset.range n, X i ω) :=
  rfl

/--
Checked repo-local wrapper around mathlib's almost-sure Kolmogorov strong law
of large numbers.
-/
theorem kolmogorovStrongLaw_ae_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) :
    KolmogorovStrongLawConclusion D :=
  ProbabilityTheory.strong_law_ae D.X D.integrable_zero
    (pairwise_independent D) D.identically_distributed

/-- Checked closure of the normalized Banach-valued Stage1 statement shape. -/
theorem statementShape_mathlib_wrapper :
    StatementShape.{u, v} := by
  intro Ω _mΩ E _add _space _complete _meas _borel D
  exact kolmogorovStrongLaw_ae_mathlib_wrapper D

/-- Checked closure of the classical real-valued statement shape. -/
theorem realStatementShape_mathlib_wrapper :
    RealStatementShape.{u} := by
  intro Ω _mΩ D
  exact kolmogorovStrongLaw_ae_mathlib_wrapper D

/-- Lp convergence conclusion for the same iid data, as supplied by mathlib. -/
def KolmogorovStrongLawLpConclusion
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) (p : ℝ≥0∞) : Prop :=
  Tendsto
    (fun n : ℕ =>
      eLpNorm (fun ω => empiricalAverage D.X n ω - D.μ[D.X 0]) p D.μ)
    atTop (𝓝 0)

/-- Checked wrapper around mathlib's Lp strong-law theorem. -/
theorem kolmogorovStrongLaw_Lp_mathlib_wrapper
    {Ω : Type u} [MeasurableSpace Ω]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E]
    (D : KolmogorovStrongLawData Ω E) {p : ℝ≥0∞}
    (hp : 1 ≤ p) (hp_ne_top : p ≠ ∞) (hLp : MemLp (D.X 0) p D.μ) :
    KolmogorovStrongLawLpConclusion D p :=
  ProbabilityTheory.strong_law_Lp hp hp_ne_top D.X hLp
    (pairwise_independent D) D.identically_distributed

/-- mathlib modules checked while locating repo-local Kolmogorov strong-law anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.StrongLaw",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.IdentDistribIndep",
  "Mathlib.Probability.Independence.Basic",
  "Mathlib.Probability.Independence.Integrable",
  "Mathlib.MeasureTheory.Function.UniformIntegrable",
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.MeasureTheory.Integral.DominatedConvergence",
  "Mathlib.Analysis.PSeries",
  "Mathlib.Analysis.Asymptotics.SpecificAsymptotics"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.strong_law_ae",
  "ProbabilityTheory.strong_law_ae_real",
  "ProbabilityTheory.strong_law_Lp",
  "ProbabilityTheory.strong_law_ae_of_measurable",
  "ProbabilityTheory.strong_law_ae_simpleFunc_comp",
  "ProbabilityTheory.iIndepFun",
  "ProbabilityTheory.iIndepFun.indepFun",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.IdentDistrib.integral_eq",
  "ProbabilityTheory.IdentDistrib.integrable_iff",
  "ProbabilityTheory.IdentDistrib.truncation",
  "ProbabilityTheory.truncation",
  "MeasureTheory.Integrable.isProbabilityMeasure_of_indepFun",
  "MeasureTheory.MemLp.isProbabilityMeasure_of_indepFun"
]

/-- One row in the Stage1 mathlib anchor table for this slot. -/
structure MathlibAnchorRow where
  anchor : String
  kind : String
  importedBy : String
  repoRole : String

/-- Required mathlib anchors for the S1-M-265 public backfill item. -/
def requiredMathlibAnchorTable : List MathlibAnchorRow := [
  {
    anchor := "Mathlib.Probability.StrongLaw",
    kind := "module",
    importedBy := "direct import",
    repoRole := "supplies the pinned strong-law theorem family used by this local wrapper"
  },
  {
    anchor := "ProbabilityTheory.strong_law_ae",
    kind := "theorem",
    importedBy := "Mathlib.Probability.StrongLaw",
    repoRole := "terminal almost-sure Kolmogorov strong-law theorem used by kolmogorovStrongLaw_ae_mathlib_wrapper"
  },
  {
    anchor := "ProbabilityTheory.strong_law_ae_real",
    kind := "theorem",
    importedBy := "Mathlib.Probability.StrongLaw",
    repoRole := "audited real-valued specialization of the strong law"
  },
  {
    anchor := "ProbabilityTheory.strong_law_Lp",
    kind := "theorem",
    importedBy := "Mathlib.Probability.StrongLaw",
    repoRole := "Lp strengthening used by kolmogorovStrongLaw_Lp_mathlib_wrapper"
  },
  {
    anchor := "ProbabilityTheory.iIndepFun.indepFun",
    kind := "theorem",
    importedBy := "Mathlib.Probability.StrongLaw",
    repoRole := "bridge from full iid independence to mathlib's pairwise independence hypothesis"
  },
  {
    anchor := "ProbabilityTheory.IdentDistrib",
    kind := "structure",
    importedBy := "Mathlib.Probability.StrongLaw",
    repoRole := "identical-distribution hypothesis in KolmogorovStrongLawData"
  }
]

/--
Search terms checked for the strong-law anchor audit.  The local pinned mathlib
wrapper closes the main target, so these are audit metadata rather than
blockers.
-/
def auditSearchTerms : List String := [
  "Kolmogorov strong law of large numbers",
  "strong law of large numbers",
  "strong_law_ae",
  "strong_law_ae_real",
  "strong_law_Lp",
  "iIndepFun",
  "Pairwise IndepFun",
  "IdentDistrib",
  "iid integrable random variables",
  "almost sure convergence"
]

/-! ## Stage1 closure metadata. -/

/-- Stage1 machine state for this checked local wrapper. -/
def machineState : String := "local_wrapper_upstream_mathlib"

/-- Lean version requested by the Stage1 parent validation record. -/
def pinnedLeanVersion : String := "4.29.0"

/-- mathlib revision requested by the Stage1 parent validation record. -/
def pinnedMathlibCommit : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Repo-local completion boundary represented by this Stage1 artifact. -/
def closedStatementBoundary : String :=
  "iid integrable Banach-valued Kolmogorov strong law via mathlib strong_law_ae"

/-- Proof-body location for the local wrapper. -/
def proofBodyLocation : String :=
  "upstream mathlib theorem ProbabilityTheory.strong_law_ae imported by Mathlib.Probability.StrongLaw"

/-- Checked child-local proof leaves, each below the M0387 <=100-step budget. -/
def checkedProofTreeLeaves : List String := [
  "isProbability: projection from KolmogorovStrongLawData",
  "integrable_zero: projection from KolmogorovStrongLawData",
  "pairwise_independent: iIndepFun.indepFun bridge to Pairwise IndepFun",
  "identically_distributed: projection from KolmogorovStrongLawData",
  "empiricalAverage_apply: definitional unfolding",
  "kolmogorovStrongLaw_ae_mathlib_wrapper: local call to ProbabilityTheory.strong_law_ae",
  "statementShape_mathlib_wrapper: normalized Banach-valued statement closure",
  "realStatementShape_mathlib_wrapper: real-valued specialization closure",
  "kolmogorovStrongLaw_Lp_mathlib_wrapper: local call to ProbabilityTheory.strong_law_Lp"
]

/-- One row in the checked Stage1 leaf-budget ledger. -/
structure ProofLeafBudgetRow where
  leafId : String
  proofPackage : String
  budget : String
  status : String
  artifact : String

/-- Full checked local leaf-budget ledger for the public proof-tree backfill. -/
def checkedLeafBudgetLedger : List ProofLeafBudgetRow := [
  {
    leafId := "S1-M-265.L001.empirical_average_def",
    proofPackage := "P1.statement_normalization",
    budget := "<=5",
    status := "checked",
    artifact := "empiricalAverage"
  },
  {
    leafId := "S1-M-265.L002.data_package",
    proofPackage := "P1.statement_normalization",
    budget := "<=10",
    status := "checked",
    artifact := "KolmogorovStrongLawData"
  },
  {
    leafId := "S1-M-265.L003.ae_conclusion",
    proofPackage := "P1.statement_normalization",
    budget := "<=10",
    status := "checked",
    artifact := "KolmogorovStrongLawConclusion"
  },
  {
    leafId := "S1-M-265.L004.statement_shape",
    proofPackage := "P1.statement_normalization",
    budget := "<=10",
    status := "checked",
    artifact := "StatementShape"
  },
  {
    leafId := "S1-M-265.L005.real_statement_shape",
    proofPackage := "P4.real_classical_specialization",
    budget := "<=10",
    status := "checked",
    artifact := "RealStatementShape"
  },
  {
    leafId := "S1-M-265.L006.statement_unfold",
    proofPackage := "P1.statement_normalization",
    budget := "<=5",
    status := "checked",
    artifact := "statementShape_iff"
  },
  {
    leafId := "S1-M-265.L007.probability_projection",
    proofPackage := "P1.statement_normalization",
    budget := "<=5",
    status := "checked",
    artifact := "isProbability"
  },
  {
    leafId := "S1-M-265.L008.integrability_projection",
    proofPackage := "P1.statement_normalization",
    budget := "<=5",
    status := "checked",
    artifact := "integrable_zero"
  },
  {
    leafId := "S1-M-265.L009.iindep_to_pairwise",
    proofPackage := "P2.independence_interface_bridge",
    budget := "<=10",
    status := "checked",
    artifact := "pairwise_independent"
  },
  {
    leafId := "S1-M-265.L010.ident_distrib_projection",
    proofPackage := "P1.statement_normalization",
    budget := "<=5",
    status := "checked",
    artifact := "identically_distributed"
  },
  {
    leafId := "S1-M-265.L011.average_unfold",
    proofPackage := "P1.statement_normalization",
    budget := "<=5",
    status := "checked",
    artifact := "empiricalAverage_apply"
  },
  {
    leafId := "S1-M-265.L012.ae_mathlib_wrapper",
    proofPackage := "P3.mathlib_terminal_wrapper",
    budget := "<=10",
    status := "checked",
    artifact := "kolmogorovStrongLaw_ae_mathlib_wrapper"
  },
  {
    leafId := "S1-M-265.L013.statement_shape_wrapper",
    proofPackage := "P3.mathlib_terminal_wrapper",
    budget := "<=10",
    status := "checked",
    artifact := "statementShape_mathlib_wrapper"
  },
  {
    leafId := "S1-M-265.L014.real_statement_wrapper",
    proofPackage := "P4.real_classical_specialization",
    budget := "<=10",
    status := "checked",
    artifact := "realStatementShape_mathlib_wrapper"
  },
  {
    leafId := "S1-M-265.L015.lp_conclusion",
    proofPackage := "P5.lp_adjacent_strengthening",
    budget := "<=10",
    status := "checked",
    artifact := "KolmogorovStrongLawLpConclusion"
  },
  {
    leafId := "S1-M-265.L016.lp_mathlib_wrapper",
    proofPackage := "P5.lp_adjacent_strengthening",
    budget := "<=10",
    status := "checked",
    artifact := "kolmogorovStrongLaw_Lp_mathlib_wrapper"
  },
  {
    leafId := "S1-M-265.L017.anchor_metadata",
    proofPackage := "P3.mathlib_terminal_wrapper",
    budget := "<=10",
    status := "checked",
    artifact := "mathlibAnchorModules, mathlibAnchorNames, auditSearchTerms"
  }
]

/-! ## Audit probes retained in the checked file. -/

#check empiricalAverage
#check KolmogorovStrongLawData
#check KolmogorovStrongLawConclusion
#check StatementShape
#check RealStatementShape
#check pairwise_independent
#check kolmogorovStrongLaw_ae_mathlib_wrapper
#check statementShape_mathlib_wrapper
#check realStatementShape_mathlib_wrapper
#check KolmogorovStrongLawLpConclusion
#check kolmogorovStrongLaw_Lp_mathlib_wrapper
#check ProbabilityTheory.strong_law_ae
#check ProbabilityTheory.strong_law_ae_real
#check ProbabilityTheory.strong_law_Lp
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.indepFun
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.IdentDistrib.integral_eq
#check ProbabilityTheory.IdentDistrib.integrable_iff
#check MathlibAnchorRow
#check requiredMathlibAnchorTable
#check machineState
#check pinnedLeanVersion
#check pinnedMathlibCommit
#check closedStatementBoundary
#check proofBodyLocation
#check checkedProofTreeLeaves
#check ProofLeafBudgetRow
#check checkedLeafBudgetLedger

end AwesomeTheorems.Stage1.S1_M_265
