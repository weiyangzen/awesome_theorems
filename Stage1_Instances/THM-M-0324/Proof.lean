import ObligationTree
import Mathlib.Topology.Algebra.Module.StrongTopology
import Mathlib.Topology.UniformSpace.Ascoli

/-!
# THM-M-0324 proof-phase progress

This module implements the Schauder-projection branch of the frozen proof
architecture. It proves that the partial-sum projections of a Schauder basis
are finite-rank and converge to the identity uniformly on compact subsets.

It does not construct Enflo's Banach space or prove that such a space fails
the approximation property, so the exact existential root remains open.
-/

noncomputable section

open Filter Topology
open scoped CompactConvergenceCLM

namespace Stage1Instances.THM_M_0324

universe u

/-- Continuous linear endomorphisms with finite-dimensional algebraic range. -/
def FiniteRankEndomorphism (E : Type u) [NormedAddCommGroup E]
    [NormedSpace Real E] (T : E →L[Real] E) : Prop :=
  FiniteDimensional Real (LinearMap.range T.toLinearMap)

/-- A sequential finite-rank approximation to the identity, with convergence
uniform on every compact subset. This technical predicate is not credited as
Enflo's exact source convention until the source crosswalk is completed. -/
structure CompactApproximationWitness (E : Type u)
    [NormedAddCommGroup E] [NormedSpace Real E] : Type u where
  approximant : Nat → E →L_c[Real] E
  finiteRank : ∀ n, FiniteRankEndomorphism E (approximant n)
  convergesCompactly :
    Tendsto approximant atTop (nhds (ContinuousLinearMap.id Real E : E →L_c[Real] E))

/-- Existence of the local compact-convergence approximation package. -/
def HasCompactApproximationProperty (E : Type u)
    [NormedAddCommGroup E] [NormedSpace Real E] : Prop :=
  Nonempty (CompactApproximationWitness E)

/-- A Schauder basis supplies finite-rank partial-sum projections converging
to the identity uniformly on compact subsets. -/
theorem schauderBasis_hasCompactApproximationProperty (E : Type u)
    [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
    (b : SchauderBasis Real E) : HasCompactApproximationProperty E := by
  obtain ⟨C, hC⟩ := b.exists_norm_proj_le
  have hbounded : ∃ C : Real, ∀ n : Nat, ‖b.proj n‖ ≤ C := ⟨C, hC⟩
  have heq : Equicontinuous ((↑) ∘ b.proj : Nat → E → E) :=
    ((NormedSpace.equicontinuous_TFAE b.proj).out 5 1).mp hbounded
  refine ⟨{
    approximant := b.proj
    finiteRank := ?_
    convergesCompactly := ?_
  }⟩
  · intro n
    rw [FiniteRankEndomorphism, b.range_proj_eq_span]
    exact FiniteDimensional.span_of_finite Real
      ((Finset.finite_toSet (Finset.range n)).image b)
  · rw [UniformConvergenceCLM.tendsto_iff_tendstoUniformlyOn
      (RingHom.id Real) E ({S : Set E | IsCompact S})]
    intro K hK
    haveI : CompactSpace K := isCompact_iff_compactSpace.mp hK
    rw [tendstoUniformlyOn_iff_tendstoUniformly_comp_coe]
    change TendstoUniformly
      (UniformFun.toFun ∘ (fun n => UniformFun.ofFun (fun x : K => b.proj n x)))
      (UniformFun.toFun
        (UniformFun.ofFun (fun x : K => (ContinuousLinearMap.id Real E) x))) atTop
    rw [← UniformFun.tendsto_iff_tendstoUniformly]
    have heqK : Equicontinuous (fun (n : Nat) (x : K) => b.proj n x) := by
      convert ((equicontinuous_restrict_iff _).mpr (heq.equicontinuousOn K)) using 1
    have hu := heqK.tendsto_uniformFun_iff_pi atTop
      (fun x : K => (ContinuousLinearMap.id Real E) x)
    change Tendsto (UniformFun.ofFun ∘ (fun (n : Nat) (x : K) => b.proj n x)) atTop
      (nhds (UniformFun.ofFun (fun x : K => (ContinuousLinearMap.id Real E) x)))
    rw [hu]
    rw [tendsto_pi_nhds]
    intro x
    exact b.tendsto_proj x

/-- Checked specialization of the frozen logical composer: failure of the
local compact-approximation predicate rules out every Schauder basis. -/
theorem noSchauderBasis_of_not_compactApproximationProperty (E : Type u)
    [NormedAddCommGroup E] [NormedSpace Real E] [CompleteSpace E]
    (propertyFails : ¬ HasCompactApproximationProperty E) :
    ¬ Nonempty (SchauderBasis Real E) := by
  exact noBasis_of_basis_implies_property
    { carrier := E
      normedAddCommGroup := inferInstance
      normedSpace := inferInstance
      completeSpace := inferInstance }
    (HasCompactApproximationProperty E) propertyFails fun basis => by
      rcases basis with ⟨b⟩
      exact schauderBasis_hasCompactApproximationProperty E b

#check schauderBasis_hasCompactApproximationProperty
#check noSchauderBasis_of_not_compactApproximationProperty

#print axioms schauderBasis_hasCompactApproximationProperty
#print axioms noSchauderBasis_of_not_compactApproximationProperty

end Stage1Instances.THM_M_0324
