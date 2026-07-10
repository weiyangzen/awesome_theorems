import Mathlib.MeasureTheory.Group.GeometryOfNumbers
import Mathlib.Algebra.Module.ZLattice.Covolume
import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# S1-M-072 / THM-M-0417: Minkowski's theorem

This Stage1 artifact records the mathlib statement and wrapper for Minkowski's
convex body theorem: a sufficiently large convex symmetric set contains a
nonzero lattice point.

The proof body is supplied by the pinned mathlib module
`Mathlib.MeasureTheory.Group.GeometryOfNumbers`.
-/

namespace AwesomeTheorems.Stage1.S1_M_072

open MeasureTheory Module
open scoped NNReal Pointwise nonZeroDivisors Real

universe u

/--
Stage1 normalized statement shape for the strict-volume version of Minkowski's
convex body theorem.

The lattice is represented as an additive subgroup `L` of a finite-dimensional
real normed space `E`; its covolume is represented by the measure of an explicit
additive fundamental domain `F`.
-/
def StatementShape
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] : Prop :=
  ∀ (L : AddSubgroup E) [Countable ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ →
      (∀ x ∈ s, -x ∈ s) →
        Convex ℝ s →
          μ F * 2 ^ finrank ℝ E < μ s →
            ∃ x ≠ 0, ((x : L) : E) ∈ s

/--
Stage1 normalized statement shape for mathlib's compact closed-boundary
variant, where the strict measure inequality is replaced by `≤`.
-/
def CompactStatementShape
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional ℝ E] [Nontrivial E]
    (μ : Measure E) [μ.IsAddHaarMeasure] : Prop :=
  ∀ (L : AddSubgroup E) [Countable ↑L] [DiscreteTopology ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ →
      (∀ x ∈ s, -x ∈ s) →
        Convex ℝ s →
          IsCompact s →
            μ F * 2 ^ finrank ℝ E ≤ μ s →
              ∃ x ≠ 0, ((x : L) : E) ∈ s

/--
Repo-local wrapper for mathlib's strict Minkowski convex body theorem.
-/
theorem minkowski_convex_body_strict
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional ℝ E]
    {μ : Measure E} [μ.IsAddHaarMeasure]
    {L : AddSubgroup E} [Countable ↑L] {F s : Set E}
    (fund : IsAddFundamentalDomain L F μ)
    (h_symm : ∀ x ∈ s, -x ∈ s)
    (h_conv : Convex ℝ s)
    (h_measure : μ F * 2 ^ finrank ℝ E < μ s) :
    ∃ x ≠ 0, ((x : L) : E) ∈ s :=
  MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
    fund h_symm h_conv h_measure

/--
The strict Stage1 statement shape is closed by the pinned mathlib wrapper.
-/
theorem statementShape_mathlib
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] :
    StatementShape E μ := by
  intro L _ F s fund h_symm h_conv h_measure
  exact minkowski_convex_body_strict fund h_symm h_conv h_measure

/--
Repo-local wrapper for mathlib's compact non-strict Minkowski convex body theorem.
-/
theorem minkowski_convex_body_compact
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional ℝ E] [Nontrivial E]
    {μ : Measure E} [μ.IsAddHaarMeasure]
    {L : AddSubgroup E} [Countable ↑L] [DiscreteTopology ↑L] {F s : Set E}
    (fund : IsAddFundamentalDomain L F μ)
    (h_symm : ∀ x ∈ s, -x ∈ s)
    (h_conv : Convex ℝ s)
    (h_cpt : IsCompact s)
    (h_measure : μ F * 2 ^ finrank ℝ E ≤ μ s) :
    ∃ x ≠ 0, ((x : L) : E) ∈ s :=
  MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_le_measure
    fund h_symm h_conv h_cpt h_measure

/--
The compact Stage1 statement shape is closed by the pinned mathlib wrapper.
-/
theorem compactStatementShape_mathlib
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional ℝ E] [Nontrivial E]
    (μ : Measure E) [μ.IsAddHaarMeasure] :
    CompactStatementShape E μ := by
  intro L _ _ F s fund h_symm h_conv h_cpt h_measure
  exact minkowski_convex_body_compact fund h_symm h_conv h_cpt h_measure

/--
Repo-local wrapper for mathlib's algebraic-number-theory Minkowski bound:
every fractional ideal class has a nonzero element with norm bounded by the
standard discriminant expression.
-/
theorem numberField_exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr
    (K : Type u) [Field K] [NumberField K]
    (I : (FractionalIdeal (NumberField.RingOfIntegers K)⁰ K)ˣ) :
    ∃ a ∈ (I : FractionalIdeal (NumberField.RingOfIntegers K)⁰ K), a ≠ 0 ∧
      |Algebra.norm ℚ (a : K)| ≤
        (FractionalIdeal.absNorm (I : FractionalIdeal (NumberField.RingOfIntegers K)⁰ K) : ℝ) *
          (4 / Real.pi) ^ NumberField.InfinitePlace.nrComplexPlaces K *
            (finrank ℚ K).factorial / (finrank ℚ K) ^ (finrank ℚ K) *
              Real.sqrt |NumberField.discr K| :=
  NumberField.exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr K I

/--
Repo-local wrapper for mathlib's ideal-class representative form of the
Minkowski bound.
-/
theorem numberField_exists_ideal_in_class_of_norm_le
    (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (NumberField.RingOfIntegers K)) :
    ∃ I : (Ideal (NumberField.RingOfIntegers K))⁰, ClassGroup.mk0 I = C ∧
      (Ideal.absNorm (I : Ideal (NumberField.RingOfIntegers K)) : ℝ) ≤
        (4 / Real.pi) ^ NumberField.InfinitePlace.nrComplexPlaces K *
          ((finrank ℚ K).factorial / (finrank ℚ K) ^ (finrank ℚ K) *
            Real.sqrt |NumberField.discr K|) :=
  NumberField.exists_ideal_in_class_of_norm_le (K := K) C

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Group.GeometryOfNumbers",
  "Mathlib.MeasureTheory.Group.FundamentalDomain",
  "Mathlib.Analysis.Convex.Body",
  "Mathlib.Analysis.Convex.Measure",
  "Mathlib.Algebra.Module.ZLattice.Covolume",
  "Mathlib.NumberTheory.NumberField.CanonicalEmbedding.ConvexBody",
  "Mathlib.NumberTheory.NumberField.Discriminant.Basic",
  "Mathlib.NumberTheory.NumberField.ClassNumber"
]

/-- Checked mathlib theorem names directly relevant to this Stage1 slot. -/
def mathlibAnchorTheorems : List String := [
  "MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd",
  "MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure",
  "MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_le_measure",
  "MeasureTheory.addCovolume",
  "IsAddFundamentalDomain.covolume_eq_volume",
  "ZLattice.covolume",
  "ZLattice.covolume_eq_measure_fundamentalDomain",
  "NumberField.exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr",
  "NumberField.exists_ideal_in_class_of_norm_le"
]

/--
Audit result for `S1-M-072.P2.fundamental_domain_and_covolume`.

The current Minkowski wrappers use the `AddSubgroup`/`IsAddFundamentalDomain`
geometry-of-numbers API, so the theorem hypotheses should keep the explicit
fundamental domain `F` and the measure term `μ F`.  Public prose may identify
`μ F` as the covolume via `IsAddFundamentalDomain.covolume_eq_volume`.

`MeasureTheory.addCovolume` is the generic quotient-action covolume API, while
`ZLattice.covolume` is the real-valued covolume API for `Submodule ℤ E`; the
latter is connected to a chosen fundamental domain by
`ZLattice.covolume_eq_measure_fundamentalDomain`.
-/
def fundamentalDomainCovolumeAudit : List String := [
  "Keep the Stage1 public statement aligned with IsAddFundamentalDomain L F μ and μ F.",
  "Mention that μ F is the covolume of L for the chosen additive fundamental domain.",
  "Cite MeasureTheory.addCovolume only as the generic quotient-action covolume API.",
  "Cite ZLattice.covolume only for the Submodule ℤ E / IsZLattice reformulation."
]

/--
Repo-local closure gate for `S1-M-072.P7.repo_local_closure_gate`.

This is intentionally a Lean-side audit artifact, not a public status update:
public planning surfaces must be synchronized serially before the Stage1 item is
promoted to `local_wrapper_upstream_mathlib`.
-/
def repoLocalClosureGate : List String := [
  "strict convex-body wrapper: local_wrapper_upstream_mathlib after this file validates",
  "compact boundary wrapper: local_wrapper_upstream_mathlib after this file validates",
  "number-field wrappers: checked downstream Minkowski-bound anchors, but optional strengthening must be named separately",
  "public status promotion: allowed only after blueprint, todo, README/meta surfaces agree",
  "unchecked optional strengthening: must not be counted as closed for the convex-body theorem",
  "repo_local_integration_debt: none for the wrapped convex-body theorem because mathlib is pinned, imported, and checked locally"
]

/-! ## Audit probes -/

#check MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd
#check MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
#check MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_le_measure
#check MeasureTheory.addCovolume
#check IsAddFundamentalDomain.covolume_eq_volume
#check ZLattice.covolume
#check ZLattice.covolume_eq_measure_fundamentalDomain
#check NumberField.exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr
#check NumberField.exists_ideal_in_class_of_norm_le
#check StatementShape
#check statementShape_mathlib
#check CompactStatementShape
#check compactStatementShape_mathlib
#check numberField_exists_ne_zero_mem_ideal_of_norm_le_mul_sqrt_discr
#check numberField_exists_ideal_in_class_of_norm_le
#check repoLocalClosureGate

end AwesomeTheorems.Stage1.S1_M_072
