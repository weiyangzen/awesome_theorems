import Mathlib.Analysis.Normed.Operator.BoundedLinearMaps
import Mathlib.Analysis.Normed.Module.WeakDual
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.Topology.Algebra.Module.StrongTopology
import Mathlib.Topology.Algebra.InfiniteSum.Module

/-!
# S1-M-215 / THM-M-0326: Grothendieck theorem, nuclear spaces and approximation

This Stage1 artifact records a conservative Lean 4 boundary for the functional
analysis statement summarized as "nuclear spaces have the approximation
property".

The pinned mathlib snapshot has continuous linear maps, operator-norm estimates,
weak duals, locally convex weak-dual infrastructure, infinite sums through
continuous linear maps, and Bochner integration commuting with continuous linear
maps.  It does not expose a terminal `NuclearSpace` API, a canonical
`ApproximationProperty` predicate, or a Grothendieck approximation theorem.
Accordingly, the terminal theorem is represented as an explicit statement
shape, while available normed-space, summation, finite-dimensional, weak-dual,
and Bochner-integral substrates are checked by low-risk wrappers below.
-/

noncomputable section

open Filter MeasureTheory
open scoped CompactConvergenceCLM ENNReal NNReal BigOperators Topology

namespace AwesomeTheorems.Stage1.S1_M_215

universe uK uE uF uG uX uI

/--
A concrete normed-space nuclearity witness for this Stage1 boundary.

This local definition says that the identity map has a summable rank-one
decomposition through continuous linear functionals.  It is a useful
normed-space target, but it is not claimed to be the terminal locally convex
`NuclearSpace` API for Grothendieck's theorem.
-/
structure NuclearNormedIdentityDecomposition
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] : Type (max uK uE) where
  coefficient : ℕ → E →L[K] K
  vector : ℕ → E
  normProductSummable : Summable (fun n => ‖coefficient n‖ * ‖vector n‖)
  hasSum_apply : ∀ x : E, HasSum (fun n => (coefficient n x) • vector n) x

/--
Concrete normed-space nuclearity predicate used by the local Stage1 statement
shape.  It records the available identity-decomposition formulation without
pretending that mathlib already has a canonical locally convex nuclear-space
class.
-/
def NuclearNormedSpace
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] : Prop :=
  Nonempty (NuclearNormedIdentityDecomposition K E)

/--
Boundary hypotheses for a future formalization of Grothendieck's theorem that
nuclear spaces have the approximation property.

The nuclearity field now uses the concrete normed-space identity-decomposition
predicate above.  The remaining proposition-valued topology field records any
terminal compatibility condition needed to compare that normed-space boundary
with the compact-convergence approximation target selected below.
-/
structure GrothendieckNuclearApproximationHypotheses
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] : Type uE where
  nuclearSpace : NuclearNormedSpace K E
  approximationTopologyCompatible : Prop
  approximationTopologyCompatible_holds : approximationTopologyCompatible

/-- The concrete nuclearity witness carried by the Stage1 hypotheses. -/
theorem GrothendieckNuclearApproximationHypotheses.exists_nuclear_decomposition
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (h : GrothendieckNuclearApproximationHypotheses K E) :
    Nonempty (NuclearNormedIdentityDecomposition K E) :=
  h.nuclearSpace

/--
Local finite-rank predicate for bundled continuous linear maps.

The pinned mathlib snapshot used by this Stage1 artifact does not expose a
canonical finite-rank predicate for `E →L[K] F`.  This definition follows the
standard linear-map range API: a continuous linear map is finite-rank when the
range of its underlying `LinearMap` is finite-dimensional.
-/
def FiniteRankContinuousLinearMap
    (K : Type uK) (E : Type uE) (F : Type uF)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [NormedAddCommGroup F] [NormedSpace K F]
    (T : E →L[K] F) : Prop :=
  FiniteDimensional K (LinearMap.range T.toLinearMap)

/--
Range-containment bridge for the local finite-rank predicate: if the algebraic
range of a bundled continuous linear map lies in a finite-dimensional
submodule, then the map is finite-rank.
-/
theorem finiteRankContinuousLinearMap_of_range_le_finiteDimensional
    {K : Type uK} {E : Type uE} {F : Type uF}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [NormedAddCommGroup F] [NormedSpace K F]
    (T : E →L[K] F) (S : Submodule K F) [FiniteDimensional K S]
    (hT : LinearMap.range T.toLinearMap ≤ S) :
    FiniteRankContinuousLinearMap K E F T := by
  dsimp [FiniteRankContinuousLinearMap]
  exact Submodule.finiteDimensional_of_le hT

/--
Rank-one endomorphism associated to a continuous linear functional and a vector.
This is the local finite-rank summand used by the nuclear-decomposition proof
tree.
-/
def rankOneEndomorphism
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : E →L[K] K) (v : E) : E →L[K] E :=
  φ.smulRight v

@[simp]
theorem rankOneEndomorphism_apply
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : E →L[K] K) (v x : E) :
    rankOneEndomorphism (K := K) φ v x = (φ x) • v :=
  rfl

/-- The range of a rank-one endomorphism is contained in the span of its vector. -/
theorem rankOneEndomorphism_range_le_span
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : E →L[K] K) (v : E) :
    LinearMap.range (rankOneEndomorphism (K := K) φ v).toLinearMap ≤ K ∙ v := by
  rintro y ⟨x, rfl⟩
  exact Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self v)

/-- Every rank-one endomorphism satisfies the local finite-rank predicate. -/
theorem rankOneEndomorphism_finiteRank
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : E →L[K] K) (v : E) :
    FiniteRankContinuousLinearMap K E E (rankOneEndomorphism (K := K) φ v) :=
  finiteRankContinuousLinearMap_of_range_le_finiteDimensional
    (rankOneEndomorphism (K := K) φ v) (K ∙ v)
    (rankOneEndomorphism_range_le_span (K := K) φ v)

/--
Finite partial sum of rank-one endomorphisms.  These are the finite-rank
truncation operators in the nuclear-decomposition proof tree.
-/
def nuclearPartialSum
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : ℕ → E →L[K] K) (v : ℕ → E) (s : Finset ℕ) : E →L[K] E :=
  s.sum fun n => rankOneEndomorphism (K := K) (φ n) (v n)

@[simp]
theorem nuclearPartialSum_apply
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : ℕ → E →L[K] K) (v : ℕ → E) (s : Finset ℕ) (x : E) :
    nuclearPartialSum (K := K) φ v s x = s.sum (fun n => (φ n x) • v n) := by
  simp [nuclearPartialSum]

/--
The range of a finite partial sum is contained in the span of the finitely many
vectors appearing in that sum.
-/
theorem nuclearPartialSum_range_le_span_image
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : ℕ → E →L[K] K) (v : ℕ → E) (s : Finset ℕ) :
    LinearMap.range (nuclearPartialSum (K := K) φ v s).toLinearMap ≤
      Submodule.span K (v '' (s : Set ℕ)) := by
  rintro y ⟨x, rfl⟩
  simpa [nuclearPartialSum] using
    (Submodule.sum_mem (Submodule.span K (v '' (s : Set ℕ))) fun n hn =>
      Submodule.smul_mem (Submodule.span K (v '' (s : Set ℕ))) (φ n x)
        (Submodule.subset_span ⟨n, hn, rfl⟩))

/-- Every finite partial sum of rank-one endomorphisms is finite-rank. -/
theorem nuclearPartialSum_finiteRank
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (φ : ℕ → E →L[K] K) (v : ℕ → E) (s : Finset ℕ) :
    FiniteRankContinuousLinearMap K E E (nuclearPartialSum (K := K) φ v s) := by
  let S : Submodule K E := Submodule.span K (v '' (s : Set ℕ))
  have hS : FiniteDimensional K S :=
    FiniteDimensional.span_of_finite K (s.finite_toSet.image v)
  exact finiteRankContinuousLinearMap_of_range_le_finiteDimensional
    (nuclearPartialSum (K := K) φ v s) S
    (nuclearPartialSum_range_le_span_image (K := K) φ v s)

/--
Finite partial sum extracted from a concrete nuclear identity-decomposition
witness.
-/
def nuclearDecompositionPartialSum
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (d : NuclearNormedIdentityDecomposition K E) (s : Finset ℕ) : E →L[K] E :=
  nuclearPartialSum (K := K) d.coefficient d.vector s

@[simp]
theorem nuclearDecompositionPartialSum_apply
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (d : NuclearNormedIdentityDecomposition K E) (s : Finset ℕ) (x : E) :
    nuclearDecompositionPartialSum (K := K) d s x =
      s.sum (fun n => (d.coefficient n x) • d.vector n) := by
  simp [nuclearDecompositionPartialSum]

/--
Checked finite-rank leaf for the nuclear-decomposition proof tree: every finite
truncation of a nuclear identity decomposition is finite-rank.
-/
theorem nuclearDecompositionPartialSum_finiteRank
    {K : Type uK} {E : Type uE}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    (d : NuclearNormedIdentityDecomposition K E) (s : Finset ℕ) :
    FiniteRankContinuousLinearMap K E E (nuclearDecompositionPartialSum (K := K) d s) :=
  nuclearPartialSum_finiteRank d.coefficient d.vector s

/--
Checked local bridge: every continuous linear map out of a finite-dimensional
domain has finite-dimensional algebraic range, hence satisfies the local
finite-rank predicate.
-/
theorem finiteRankContinuousLinearMap_of_finiteDimensional_domain
    {K : Type uK} {E : Type uE} {F : Type uF}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [NormedAddCommGroup F] [NormedSpace K F]
    [FiniteDimensional K E] (T : E →L[K] F) :
    FiniteRankContinuousLinearMap K E F T := by
  dsimp [FiniteRankContinuousLinearMap]
  infer_instance

/--
Reusable finite-rank wrapper for the identity endomorphism on a
finite-dimensional normed space.
-/
theorem finiteRankContinuousLinearMap_id_of_finiteDimensional
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E] :
    FiniteRankContinuousLinearMap K E E (ContinuousLinearMap.id K E) :=
  finiteRankContinuousLinearMap_of_finiteDimensional_domain
    (ContinuousLinearMap.id K E)

/--
The selected Stage1 approximation-property topology on endomorphisms.

For Grothendieck's theorem, the safe general approximation-property target is
not a sequence converging in operator norm.  It is a net/filter of finite-rank
endomorphisms converging to the identity in the topology of compact convergence,
equivalently uniform convergence on compact subsets.  Mathlib exposes this
topology through `CompactConvergenceCLM`, with notation `E →L_c[K] E`.
-/
abbrev CompactConvergenceEndomorphism
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] :=
  E →L_c[K] E

/--
Checked characterization of the selected topology: convergence in
`CompactConvergenceEndomorphism K E` is convergence uniformly on every compact
subset of `E`.
-/
theorem compactConvergenceEndomorphism_tendsto_iff_tendstoUniformlyOn_compacts
    {K : Type uK} {E : Type uE} {ι : Type uI}
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    {l : Filter ι}
    {A : ι → CompactConvergenceEndomorphism K E}
    {T : CompactConvergenceEndomorphism K E} :
    Tendsto A l (𝓝 T) ↔
      ∀ C : Set E, IsCompact C →
        TendstoUniformlyOn (fun i x => A i x) T l C := by
  simpa [CompactConvergenceEndomorphism] using
    (UniformConvergenceCLM.tendsto_iff_tendstoUniformlyOn (RingHom.id K) E
      ({S : Set E | IsCompact S}) (a := A) (a₀ := T) (p := l))

/--
Filter-indexed approximation-property witness in compact-convergence topology.

The `filter_neBot` field rules out vacuous convergence along the bottom filter.
This is the selected Stage1 target for the parent theorem statement shape.
-/
structure FilteredCompactConvergenceApproximationWitness
    (K : Type uK) (E : Type uE) (ι : Type uI)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] : Type (max uE uI) where
  filter : Filter ι
  filter_neBot : NeBot filter
  approximant : ι → CompactConvergenceEndomorphism K E
  finiteRankApproximant_holds :
    ∀ i, FiniteRankContinuousLinearMap K E E (approximant i)
  approximatesIdentity :
    Tendsto approximant filter
      (𝓝 (ContinuousLinearMap.id K E : CompactConvergenceEndomorphism K E))

/--
The selected approximation property for this Stage1 artifact: some nontrivial
filter-indexed family of finite-rank endomorphisms converges to the identity in
compact-convergence topology.
-/
def CompactConvergenceApproximationProperty
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] : Prop :=
  ∃ ι : Type uE, Nonempty (FilteredCompactConvergenceApproximationWitness K E ι)

/--
A sequential approximation-property witness in the normed-space object model.

The approximants are concrete continuous linear endomorphisms and the
convergence-to-identity statement uses mathlib's topology on bundled continuous
linear maps, i.e. the bounded/operator-norm topology for normed spaces.  This is
kept as a stronger special-case target, while the parent theorem shape below
uses the general filter-indexed compact-convergence target.
-/
structure SequentialApproximationWitness
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] : Type uE where
  approximant : ℕ → E →L[K] E
  finiteRankApproximant_holds :
    ∀ n, FiniteRankContinuousLinearMap K E E (approximant n)
  approximatesIdentity :
    Tendsto approximant atTop (𝓝 (ContinuousLinearMap.id K E))

/--
Stage1 normalized statement shape for Grothendieck's approximation theorem.

In a future terminal formalization, `GrothendieckNuclearApproximationHypotheses`
should be replaced by concrete nuclear locally convex hypotheses, and
`CompactConvergenceApproximationProperty` should be connected to the standard
locally convex approximation-property API once that API exists.
-/
def StatementShape : Prop :=
  ∀ (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E] [CompleteSpace E],
      GrothendieckNuclearApproximationHypotheses K E →
        CompactConvergenceApproximationProperty K E

/--
Finite-dimensional normed spaces supply a checked special-case approximation
witness: the constant sequence at the identity converges to the identity.  The
finite-rank predicate is represented by the available `FiniteDimensional`
typeclass for this Stage1 boundary.
-/
def finiteDimensionalApproximationWitness
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E] :
    SequentialApproximationWitness K E where
  approximant := fun _ => ContinuousLinearMap.id K E
  finiteRankApproximant_holds := fun _ =>
    finiteRankContinuousLinearMap_id_of_finiteDimensional K E
  approximatesIdentity := tendsto_const_nhds

/-- Checked special case: finite-dimensional normed spaces have this witness. -/
theorem finiteDimensional_hasSequentialApproximationWitness
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E] :
    Nonempty (SequentialApproximationWitness K E) :=
  ⟨finiteDimensionalApproximationWitness K E⟩

/--
Reusable finite-dimensional compact-convergence wrapper: along any nontrivial
filter, the constant identity family is a finite-rank approximation witness.
-/
def finiteDimensionalConstantIdentityCompactConvergenceApproximationWitness
    (K : Type uK) (E : Type uE) (ι : Type uI)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E]
    (l : Filter ι) [NeBot l] :
    FilteredCompactConvergenceApproximationWitness K E ι where
  filter := l
  filter_neBot := inferInstance
  approximant := fun _ => ContinuousLinearMap.id K E
  finiteRankApproximant_holds := fun _ =>
    finiteRankContinuousLinearMap_id_of_finiteDimensional K E
  approximatesIdentity := tendsto_const_nhds

/--
Checked reusable wrapper theorem for finite-dimensional compact-convergence
approximation witnesses over an arbitrary nontrivial filter.
-/
theorem finiteDimensional_hasFilteredCompactConvergenceApproximationWitness
    (K : Type uK) (E : Type uE) (ι : Type uI)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E]
    (l : Filter ι) [NeBot l] :
    Nonempty (FilteredCompactConvergenceApproximationWitness K E ι) :=
  ⟨finiteDimensionalConstantIdentityCompactConvergenceApproximationWitness K E ι l⟩

/--
Finite-dimensional normed spaces also supply the selected filter-indexed
compact-convergence witness: the constant net at the identity along the top
filter on a lifted copy of `ℕ`.
-/
def finiteDimensionalCompactConvergenceApproximationWitness
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E] :
    FilteredCompactConvergenceApproximationWitness K E (ULift.{uE, 0} ℕ) where
  filter := ⊤
  filter_neBot := inferInstance
  approximant := fun _ => ContinuousLinearMap.id K E
  finiteRankApproximant_holds := fun _ =>
    finiteRankContinuousLinearMap_id_of_finiteDimensional K E
  approximatesIdentity := tendsto_const_nhds

/-- Checked special case for the selected compact-convergence approximation property. -/
theorem finiteDimensional_hasCompactConvergenceApproximationProperty
    (K : Type uK) (E : Type uE)
    [RCLike K] [NormedAddCommGroup E] [NormedSpace K E]
    [FiniteDimensional K E] :
    CompactConvergenceApproximationProperty K E :=
  ⟨ULift.{uE, 0} ℕ, ⟨finiteDimensionalCompactConvergenceApproximationWitness K E⟩⟩

section ContinuousLinearMapAnchors

variable {K : Type uK} [RCLike K]
variable {E : Type uE} [NormedAddCommGroup E] [NormedSpace K E]
variable {F : Type uF} [NormedAddCommGroup F] [NormedSpace K F]
variable {G : Type uG} [NormedAddCommGroup G] [NormedSpace K G]

/-- Checked mathlib anchor: the bundled continuous-linear identity is pointwise identity. -/
theorem continuousLinearMap_id_apply_wrapper (x : E) :
    (ContinuousLinearMap.id K E) x = x :=
  ContinuousLinearMap.id_apply x

/-- Checked mathlib anchor: composition of bundled continuous linear maps is pointwise composition. -/
theorem continuousLinearMap_comp_apply_wrapper
    (g : F →L[K] G) (f : E →L[K] F) (x : E) :
    (g.comp f) x = g (f x) :=
  rfl

/-- Checked mathlib anchor: operator norm of a composition is submultiplicative. -/
theorem continuousLinearMap_opNorm_comp_le_wrapper
    (g : F →L[K] G) (f : E →L[K] F) :
    ‖g.comp f‖ ≤ ‖g‖ * ‖f‖ :=
  g.opNorm_comp_le f

/-- Checked mathlib anchor: continuous linear maps preserve `HasSum`. -/
theorem continuousLinearMap_hasSum_wrapper
    {ι : Type uI} {f : ι → E} {x : E}
    (L : E →L[K] F) (hf : HasSum f x) :
    HasSum (fun i => L (f i)) (L x) :=
  L.hasSum hf

/-- Checked mathlib anchor: continuous linear maps commute with `tsum` for summable families. -/
theorem continuousLinearMap_map_tsum_wrapper
    {ι : Type uI} [T2Space F] {f : ι → E}
    (L : E →L[K] F) (hf : Summable f) :
    L (∑' i, f i) = ∑' i, L (f i) :=
  L.map_tsum hf

end ContinuousLinearMapAnchors

section BochnerIntegralAnchor

variable {X : Type uX} [MeasurableSpace X] {μ : Measure X}
variable {K : Type uK} [RCLike K]
variable {E : Type uE} [NormedAddCommGroup E] [NormedSpace K E]
variable {F : Type uF} [NormedAddCommGroup F] [NormedSpace K F]

/--
Checked mathlib anchor: Bochner integration commutes with a continuous linear
map under the standard completeness and real-normed-space assumptions.
-/
theorem continuousLinearMap_integral_comp_comm_wrapper
    [NormedSpace ℝ E] [NormedSpace ℝ F] [CompleteSpace E] [CompleteSpace F]
    (L : E →L[K] F) {φ : X → E} (hφ : Integrable φ μ) :
    ∫ x, L (φ x) ∂μ = L (∫ x, φ x ∂μ) :=
  ContinuousLinearMap.integral_comp_comm L hφ

end BochnerIntegralAnchor

section WeakDualAnchors

variable {K : Type uK} [NontriviallyNormedField K]
variable {E : Type uE} [SeminormedAddCommGroup E] [NormedSpace K E]

/-- Checked mathlib anchor: the weak-dual-to-strong-dual equivalence is pointwise identity. -/
theorem weakDual_toStrongDual_apply_wrapper
    (x : WeakDual K E) (y : E) :
    (WeakDual.toStrongDual x) y = x y :=
  WeakDual.toStrongDual_apply x y

/--
Checked mathlib anchor: on a Banach space, boundedness in the inherited norm
bornology on the weak dual matches von Neumann boundedness.
-/
theorem weakDual_isBounded_iff_isVonNBounded_wrapper
    [CompleteSpace E] {s : Set (WeakDual K E)} :
    Bornology.IsBounded s ↔ Bornology.IsVonNBounded K s :=
  WeakDual.isBounded_iff_isVonNBounded

end WeakDualAnchors

/-- Mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Normed.Operator.BoundedLinearMaps",
  "Mathlib.Analysis.Normed.Operator.Basic",
  "Mathlib.Analysis.Normed.Module.WeakDual",
  "Mathlib.Analysis.LocallyConvex.WeakDual",
  "Mathlib.LinearAlgebra.FiniteDimensional.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.Bochner.Set",
  "Mathlib.Topology.Algebra.Module.StrongTopology",
  "Mathlib.Topology.UniformSpace.UniformConvergence",
  "Mathlib.Topology.Algebra.InfiniteSum.Module",
  "Mathlib.Analysis.Normed.Module.PiTensorProduct.ProjectiveSeminorm",
  "Mathlib.Analysis.Normed.Module.PiTensorProduct.InjectiveSeminorm"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ContinuousLinearMap",
  "ContinuousLinearMap.id",
  "ContinuousLinearMap.id_apply",
  "ContinuousLinearMap.comp",
  "ContinuousLinearMap.toLinearMap",
  "ContinuousLinearMap.opNorm_comp_le",
  "ContinuousLinearMap.hasSum",
  "ContinuousLinearMap.map_tsum",
  "ContinuousLinearMap.integral_comp_comm",
  "LinearMap.range",
  "rankOneEndomorphism",
  "rankOneEndomorphism_finiteRank",
  "nuclearPartialSum",
  "nuclearPartialSum_finiteRank",
  "nuclearDecompositionPartialSum",
  "nuclearDecompositionPartialSum_finiteRank",
  "CompactConvergenceCLM",
  "UniformConvergenceCLM.tendsto_iff_tendstoUniformlyOn",
  "TendstoUniformlyOn",
  "WeakDual",
  "WeakDual.toStrongDual",
  "WeakDual.toStrongDual_apply",
  "WeakDual.isBounded_iff_isVonNBounded",
  "FiniteRankContinuousLinearMap",
  "finiteRankContinuousLinearMap_id_of_finiteDimensional",
  "finiteDimensionalConstantIdentityCompactConvergenceApproximationWitness",
  "finiteDimensional_hasFilteredCompactConvergenceApproximationWitness",
  "FiniteDimensional",
  "HasSum",
  "Summable",
  "Tendsto",
  "MeasureTheory.Integrable"
]

/--
Decision for the approximation-property target in this Stage1 artifact.

The general target is net/filter-indexed compact convergence on `E →L[K] E`,
represented by `CompactConvergenceEndomorphism K E = E →L_c[K] E`.  The older
sequence-indexed operator-norm witness remains only as a stronger special case.
-/
def approximationTopologyDecision : String :=
  "filter-indexed compact convergence on `E ->L[K] E`, via `E ->L_c[K] E`"

/--
Search terms that did not locate a terminal Grothendieck nuclear-space
approximation theorem in the local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "Grothendieck theorem",
  "Grothendieck approximation theorem",
  "GrothendieckTheorem",
  "NuclearSpace",
  "nuclear space",
  "nuclear locally convex",
  "ApproximationProperty",
  "approximation property",
  "finite-rank approximation",
  "nuclear operator"
]

/--
Exact blocker for upgrading the local normed-space nuclearity predicate to a
terminal locally convex Grothendieck theorem.
-/
def nuclearSpaceApiBlockers : List String := [
  "no canonical mathlib `NuclearSpace` predicate or typeclass for locally convex spaces was found",
  "no canonical nuclear continuous-linear-map/operator-ideal API was found",
  "no canonical mathlib finite-rank predicate for bundled continuous linear maps was found; the local predicate uses `FiniteDimensional K (LinearMap.range T.toLinearMap)`",
  "no completed locally convex projective/injective tensor-product API was found",
  "no mathlib theorem connecting nuclear identity decompositions to the approximation property was found"
]

/-- The nuclear-space API blocker list is intentionally explicit and nonempty. -/
theorem nuclearSpaceApiBlockers_length :
    nuclearSpaceApiBlockers.length = 5 := by
  native_decide

/--
C006 proof-tree split from nuclear decomposition to finite-rank approximation.

The first four leaves are now represented by checked declarations in this file.
The last three remain formalization debt because the current local
normed-space witness gives pointwise `HasSum`, while the selected theorem target
requires compact-convergence of finite-rank endomorphisms.
-/
def nuclearToFiniteRankProofTreeC006 : List String := [
  "C006.P1.rank_one_summand: define `rankOneEndomorphism φ v = φ.smulRight v`",
  "C006.P2.rank_one_range: prove its range is contained in `K ∙ v`",
  "C006.P3.rank_one_finite_rank: close finite-rank using finite-dimensional span of one vector",
  "C006.P4.partial_sum_finite_rank: define `nuclearPartialSum` and prove finite-rank through finite span of vectors indexed by a finset",
  "C006.P5.decomposition_truncations: specialize partial sums to `NuclearNormedIdentityDecomposition`",
  "C006.P6.pointwise_limit: use `hasSum_apply` to identify the pointwise limit with the identity",
  "C006.P7.compact_convergence_upgrade: prove uniform convergence on compact sets or replace the local nuclear predicate with a stronger summability API",
  "C006.P8.approximation_witness: package a nontrivial filter-indexed compact-convergence approximation witness"
]

/-- Leaf-budget ledger for the C006 proof-tree split. -/
def nuclearToFiniteRankLeafBudgetC006 : List String := [
  "C006-L01 checked <=20: `rankOneEndomorphism_apply`",
  "C006-L02 checked <=30: `rankOneEndomorphism_range_le_span`",
  "C006-L03 checked <=30: `rankOneEndomorphism_finiteRank`",
  "C006-L04 checked <=40: `nuclearPartialSum_range_le_span_image`",
  "C006-L05 checked <=40: `nuclearPartialSum_finiteRank`",
  "C006-L06 checked <=20: `nuclearDecompositionPartialSum_apply`",
  "C006-L07 checked <=20: `nuclearDecompositionPartialSum_finiteRank`",
  "C006-L08 unchecked <=100: convert pointwise `HasSum` of decomposition tails into the selected compact-convergence target",
  "C006-L09 unchecked <=100: package the finite truncations as `FilteredCompactConvergenceApproximationWitness` once convergence is available"
]

/-- The C006 proof tree has eight package nodes. -/
theorem nuclearToFiniteRankProofTreeC006_length :
    nuclearToFiniteRankProofTreeC006.length = 8 := by
  native_decide

/-- The C006 leaf-budget ledger has nine leaves. -/
theorem nuclearToFiniteRankLeafBudgetC006_length :
    nuclearToFiniteRankLeafBudgetC006.length = 9 := by
  native_decide

/--
Public Lean 4 source audit for the C005 external-anchor pass.

This records source-level evidence only.  None of these entries is promoted to
terminal Grothendieck approximation theorem completion in this repository.
-/
def externalLeanAuditSourcesC005 : List String := [
  "mathlib4 at 8a178386ffc0f5fef0b77738bb5449d50efeea95: local rg found compact convergence, weak dual, Bochner integral, continuous-linear-map, finite-dimensional, and tensor-seminorm substrate, but no `NuclearSpace`, `ApproximationProperty`, `GrothendieckApproximation`, or terminal nuclear-space approximation theorem",
  "Loogle public declaration search on 2026-05-01: `NuclearSpace`, `ApproximationProperty`, and `GrothendieckApproximation` were unknown identifiers; quoted `nuclear operator` returned zero declaration hits; `Grothendieck` suggestions were unrelated category-theory declarations",
  "GitHub code-search API probes for exact Lean strings returned 401 `Requires authentication`, so those failed probes are recorded only as an audit limitation, not as negative theorem evidence",
  "mrdouglasny/bochner public README: contains `Minlos.NuclearSpace`, `IsHilbertNuclear`, `isHilbertNuclear_of_nuclear`, and `minlos_theorem`, with Lean v4.28.0-rc1 according to the README; this is nuclear-space/Minlos infrastructure, not Grothendieck's approximation-property theorem",
  "mrdouglasny/gaussian-field public sources: contain `Nuclear.NuclearSpace`, `DyninMityaginSpace.toNuclearSpace`, `DyninMityaginSpace.hasSum_basis`, `NuclearTensorProduct`, and nuclear-operator/SVD files; Lean toolchain is v4.29.0, but the project does not expose `ApproximationProperty` or `GrothendieckApproximation` in the public README audit",
  "mrdouglasny/OSforGFF public README: depends on `bochner` and `gaussian-field` for nuclear-space and Minlos infrastructure and uses Lean v4.29.0, but it is a Gaussian-free-field project, not a terminal proof of nuclear spaces having the approximation property"
]

/-- The C005 external audit found six distinct source/status records. -/
theorem externalLeanAuditSourcesC005_length :
    externalLeanAuditSourcesC005.length = 6 := by
  native_decide

/--
C005 integration blocker for any future public Lean 4 proof evidence.

If an external theorem proving exactly the Grothendieck nuclear-space
approximation theorem is later identified, the parent cannot be marked
completed until that source is pinned, imported, and checked in this repository,
or until an exact toolchain/API/license blocker is recorded.
-/
def externalProofIntegrationBlockerC005 : String :=
  "no public Lean 4 proof of the terminal Grothendieck nuclear-space approximation theorem was identified; adjacent public nuclear-space and nuclear-operator infrastructure is not an approximation-property proof and is not pinned/imported/checked here"

/-- Machine proof debt classification for the current Stage1 boundary. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Repo-local integration gate: this module is not a completed terminal proof and
does not claim anchor-only external evidence as repo-local closure.
-/
def repoLocalIntegrationDebtGate : String :=
  "not_completed; no external Lean 4 terminal proof was identified or integrated"

/--
C007 public-surface backfill proposal.

This child is intentionally not allowed to edit public blueprint, todo, or
README surfaces directly.  It records the serial integrator patch target that
becomes actionable only after a terminal local proof body, checked upstream
wrapper, or pinned external theorem lands.
-/
def publicBackfillProposalC007 : List String := [
  "Blueprint: keep S1-M-215 C007 unchecked until a terminal local proof body, pinned upstream theorem, or checked wrapper lands; after that, update `Docs/Stage1_Blueprint.md` in the serial integrator pass with the exact theorem names and validation command.",
  "Todo: mirror the same S1-M-215 terminal-status wording in `Docs/todos_20260430.md`; if no terminal theorem has landed, retain formalization_debt and do not mark the public-doc integration item complete.",
  "README: mention only the checked Stage1 boundary declarations from `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_215.lean` until the terminal Grothendieck approximation theorem is repo-local closed."
]

/-- The C007 public backfill proposal has one line for each public surface. -/
theorem publicBackfillProposalC007_length :
    publicBackfillProposalC007.length = 3 := by
  native_decide

/-- C005 gate: the external-anchor audit is nonempty but records no completion claim. -/
def externalAuditC005NoCompletionClaim : Bool :=
  externalLeanAuditSourcesC005.length = 6 &&
    externalProofIntegrationBlockerC005.length > 0

/-! ## Audit probes -/

#check StatementShape
#check NuclearNormedIdentityDecomposition
#check NuclearNormedSpace
#check GrothendieckNuclearApproximationHypotheses
#check GrothendieckNuclearApproximationHypotheses.exists_nuclear_decomposition
#check FiniteRankContinuousLinearMap
#check finiteRankContinuousLinearMap_of_range_le_finiteDimensional
#check rankOneEndomorphism
#check rankOneEndomorphism_apply
#check rankOneEndomorphism_range_le_span
#check rankOneEndomorphism_finiteRank
#check nuclearPartialSum
#check nuclearPartialSum_apply
#check nuclearPartialSum_range_le_span_image
#check nuclearPartialSum_finiteRank
#check nuclearDecompositionPartialSum
#check nuclearDecompositionPartialSum_apply
#check nuclearDecompositionPartialSum_finiteRank
#check finiteRankContinuousLinearMap_of_finiteDimensional_domain
#check finiteRankContinuousLinearMap_id_of_finiteDimensional
#check CompactConvergenceEndomorphism
#check compactConvergenceEndomorphism_tendsto_iff_tendstoUniformlyOn_compacts
#check FilteredCompactConvergenceApproximationWitness
#check CompactConvergenceApproximationProperty
#check SequentialApproximationWitness
#check finiteDimensionalApproximationWitness
#check finiteDimensional_hasSequentialApproximationWitness
#check finiteDimensionalConstantIdentityCompactConvergenceApproximationWitness
#check finiteDimensional_hasFilteredCompactConvergenceApproximationWitness
#check finiteDimensionalCompactConvergenceApproximationWitness
#check finiteDimensional_hasCompactConvergenceApproximationProperty
#check continuousLinearMap_id_apply_wrapper
#check continuousLinearMap_comp_apply_wrapper
#check continuousLinearMap_opNorm_comp_le_wrapper
#check continuousLinearMap_hasSum_wrapper
#check continuousLinearMap_map_tsum_wrapper
#check continuousLinearMap_integral_comp_comm_wrapper
#check weakDual_toStrongDual_apply_wrapper
#check weakDual_isBounded_iff_isVonNBounded_wrapper
#check ContinuousLinearMap.integral_comp_comm
#check ContinuousLinearMap.map_tsum
#check WeakDual.isBounded_iff_isVonNBounded
#check CompactConvergenceCLM
#check UniformConvergenceCLM.tendsto_iff_tendstoUniformlyOn
#check nuclearSpaceApiBlockers
#check nuclearSpaceApiBlockers_length
#check nuclearToFiniteRankProofTreeC006
#check nuclearToFiniteRankProofTreeC006_length
#check nuclearToFiniteRankLeafBudgetC006
#check nuclearToFiniteRankLeafBudgetC006_length
#check externalLeanAuditSourcesC005
#check externalLeanAuditSourcesC005_length
#check externalProofIntegrationBlockerC005
#check externalAuditC005NoCompletionClaim
#check approximationTopologyDecision
#check machineProofDebtClassification
#check repoLocalIntegrationDebtGate
#check publicBackfillProposalC007
#check publicBackfillProposalC007_length

end AwesomeTheorems.Stage1.S1_M_215
