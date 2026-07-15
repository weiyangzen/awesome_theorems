import Statement

/-!
# THM-M-0346 proof-phase adapter bodies

These checked bodies discharge the local representative, exponent, cutoff,
and almost-everywhere composition interfaces. The analytic Carleson-Hunt
theorem remains an explicit input because its audited upstream package is not
available in the repository's pinned dependency closure.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1.THM_M_0346

noncomputable section

local instance : Fact (0 < (1 : ℝ)) := ⟨by norm_num⟩

/-- The partial-sum interface used by the audited Carleson-Hunt theorem. This
local definition is definitionally aligned with the upstream definition. -/
def upstreamPartialFourierSum {T : ℝ} [Fact (0 < T)]
    (N : ℕ) (g : AddCircle T → ℂ) : C(AddCircle T, ℂ) :=
  ∑ n ∈ Finset.Icc (-Int.ofNat N) N, fourierCoeff g n • fourier n

/-- Exact local contract of the missing analytic theorem, before adapting an
`Lp` element to its canonical representative. -/
def RawCarlesonHunt : Prop :=
  ∀ (g : AddCircle (1 : ℝ) → ℂ),
    MemLp g 2 (@AddCircle.haarAddCircle (1 : ℝ) inferInstance) →
    ∀ᵐ x ∂(@AddCircle.haarAddCircle (1 : ℝ) inferInstance),
      Tendsto (fun N : ℕ ↦ upstreamPartialFourierSum N g x) atTop (nhds (g x))

/-- The coercion of an `Lp` class is a valid `L²` representative. -/
theorem lp_coe_memLp
    (f : Lp ℂ 2 (@AddCircle.haarAddCircle (1 : ℝ) inferInstance)) :
    MemLp (fun x ↦ f x) 2 (@AddCircle.haarAddCircle (1 : ℝ) inferInstance) := by
  exact Lp.memLp f

/-- The period-one instance needed to specialize the upstream theorem. -/
theorem fact_unit_period : Fact (0 < (1 : ℝ)) := by
  constructor
  norm_num

/-- The upstream exponent side condition at `p = 2`. -/
theorem exponent_two_gt_one : (1 : ENNReal) < (2 : ENNReal) := by
  norm_num

/-- Specialize an imported Carleson-Hunt declaration to the period-one,
`p = 2` raw contract. The argument deliberately remains explicit: this is an
integration adapter, not a local proof of the analytic theorem. -/
theorem upstream_carleson_hunt_adapter
    (upstream : ∀ {T : ℝ} [Fact (0 < T)] {g : AddCircle T → ℂ}
      {p : ENNReal}, 1 < p → MemLp g p (@AddCircle.haarAddCircle T inferInstance) →
        ∀ᵐ x ∂(@AddCircle.haarAddCircle T inferInstance),
          Tendsto (fun N : ℕ ↦ upstreamPartialFourierSum N g x) atTop (nhds (g x))) :
    RawCarlesonHunt := by
  intro g hg
  exact upstream (T := (1 : ℝ)) (p := (2 : ENNReal)) exponent_two_gt_one hg

/-- The upstream cutoff `Finset.Icc (-Int.ofNat N) N` is exactly the frozen
inclusive cutoff `Finset.Icc (-(N : ℤ)) (N : ℤ)`. -/
theorem upstreamPartialFourierSum_apply_eq_symmetricPartialSum
    (f : Lp ℂ 2 (@AddCircle.haarAddCircle (1 : ℝ) inferInstance))
    (N : ℕ) (x : AddCircle (1 : ℝ)) :
    upstreamPartialFourierSum N (fun y ↦ f y) x = symmetricPartialSum f N x := by
  simp only [upstreamPartialFourierSum, symmetricPartialSum, Int.ofNat_eq_natCast,
    ContinuousMap.coe_sum, ContinuousMap.coe_smul, Finset.sum_apply, Pi.smul_apply,
    smul_eq_mul]

/-- Compose the raw theorem with the canonical `Lp` representative and exact
cutoff equality to obtain the frozen target. -/
theorem carlesonTarget_of_rawCarlesonHunt (h : RawCarlesonHunt) : CarlesonTarget := by
  intro f
  filter_upwards [h (fun x ↦ f x) (lp_coe_memLp f)] with x hx
  convert hx using 1
  funext N
  exact (upstreamPartialFourierSum_apply_eq_symmetricPartialSum f N x).symm

#check carlesonTarget_of_rawCarlesonHunt
#print axioms lp_coe_memLp
#print axioms fact_unit_period
#print axioms exponent_two_gt_one
#print axioms upstream_carleson_hunt_adapter
#print axioms upstreamPartialFourierSum_apply_eq_symmetricPartialSum
#print axioms carlesonTarget_of_rawCarlesonHunt
#print sorries lp_coe_memLp
#print sorries fact_unit_period
#print sorries exponent_two_gt_one
#print sorries upstream_carleson_hunt_adapter
#print sorries upstreamPartialFourierSum_apply_eq_symmetricPartialSum
#print sorries carlesonTarget_of_rawCarlesonHunt

end

end Stage1.THM_M_0346
