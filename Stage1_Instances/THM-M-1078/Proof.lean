import Mathlib.MeasureTheory.Function.ConditionalExpectation.CondJensen
import Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm
import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1078 proved proof units

This module proves the horizon-local `MemLp` bridge needed by a valid martingale-transform proof.
It deliberately does not instantiate `ObligationTree.EarlierMemLpBridge`: that frozen interface
quantifies over future times and is false. The external Burkholder terminal body remains absent
from the pinned dependency closure, so no exact-root proof is claimed here.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal

namespace Stage1Instances.THM_M_1078.Proof

universe u

/-- Conditional expectation preserves `L^p` for the non-endpoint exponents in the target.

The pinned mathlib API exposes this directly only at exponent two. This proof derives the general
case from conditional Jensen applied to `x |-> ‖x‖ ^ p.toReal`. -/
theorem memLp_condExp_of_one_lt {Omega : Type*} [m : MeasurableSpace Omega]
    {mu : Measure Omega} [IsFiniteMeasure mu] {s : MeasurableSpace Omega}
    (hs : s <= m) [SigmaFinite (mu.trim hs)] {f : Omega -> Real} {p : ENNReal}
    (hp : 1 < p) (hptop : p < ∞) (hf : MemLp f p mu) :
    MemLp (mu[f | s]) p mu := by
  have hp0 : p ≠ 0 := (zero_lt_one.trans hp).ne'
  have hpinf : p ≠ ∞ := ne_of_lt hptop
  have hpreal : 1 < p.toReal := by
    rw [← ENNReal.toReal_one]
    exact (ENNReal.toReal_lt_toReal ENNReal.one_ne_top hpinf).2 hp
  have hfi : Integrable f mu := hf.integrable hp.le
  have hfpow : Integrable (fun x => norm (f x) ^ p.toReal) mu :=
    hf.integrable_norm_rpow hp0 hpinf
  let phi : Real -> Real := fun x => norm x ^ p.toReal
  have hphi_convex : ConvexOn Real univ phi := by
    rw [show phi = (fun x : Real => x ^ p.toReal) ∘ norm by rfl]
    have himage : norm '' (univ : Set Real) = Ici 0 := by
      ext y
      constructor
      · rintro ⟨x, -, rfl⟩
        exact norm_nonneg x
      · intro hy
        exact ⟨y, Set.mem_univ y, by simp [Real.norm_of_nonneg hy]⟩
    refine ConvexOn.comp (s := (univ : Set Real)) ?_ convexOn_univ_norm ?_
    · rw [himage]
      exact convexOn_rpow hpreal.le
    · rw [himage]
      exact Real.monotoneOn_rpow_Ici_of_exponent_nonneg (le_trans zero_le_one hpreal.le)
  have hphi_cont : LowerSemicontinuous phi := by
    exact ((Real.continuous_rpow_const (le_trans zero_le_one hpreal.le)).comp
      continuous_norm).lowerSemicontinuous
  have hjensen : (phi ∘ mu[f | s]) ≤ᵐ[mu] mu[phi ∘ f | s] :=
    hphi_convex.map_condExp_le_univ hs hphi_cont hfi hfpow
  have hcondpow_int : Integrable (mu[phi ∘ f | s]) mu := integrable_condExp
  have hpow_int : Integrable (phi ∘ mu[f | s]) mu := by
    refine Integrable.mono' hcondpow_int ?_ ?_
    · exact (((Real.continuous_rpow_const (le_trans zero_le_one hpreal.le)).comp
        continuous_norm).comp_aestronglyMeasurable
        (((stronglyMeasurable_condExp (m := s) (μ := mu) (f := f)).mono hs).aestronglyMeasurable))
    · filter_upwards [hjensen] with x hx
      have hnonneg : 0 <= phi (mu[f | s] x) := Real.rpow_nonneg (norm_nonneg _) _
      change |phi (mu[f | s] x)| <= mu[phi ∘ f | s] x
      rw [abs_of_nonneg hnonneg]
      exact hx
  exact (integrable_norm_rpow_iff (μ := mu) (p := p)
    (((stronglyMeasurable_condExp (m := s) (μ := mu) (f := f)).mono hs).aestronglyMeasurable)
      hp0 hpinf).1
    (by simpa [phi, Function.comp_def] using hpow_int)

/-- The truthful horizon-local replacement for the frozen all-time bridge. -/
def EarlierMemLpUpTo : Prop :=
  forall p : ENNReal, 1 < p -> p < ∞ ->
    forall (Omega : Type u) (m : MeasurableSpace Omega) (mu : Measure Omega)
      [IsProbabilityMeasure mu] (F : Filtration Nat m)
      (f : Nat -> Omega -> Real) (n : Nat),
      Martingale f F mu -> MemLp (f n) p mu -> forall k, k <= n -> MemLp (f k) p mu

/-- A martingale's terminal `L^p` integrability propagates to every earlier time. -/
theorem earlierMemLpUpTo : EarlierMemLpUpTo.{u} := by
  intro p hp hptop Omega m mu _ F f n hmart hterminal k hkn
  have hce := memLp_condExp_of_one_lt (F.le k) hp hptop hterminal
  exact hce.ae_eq (hmart.condExp_ae_eq hkn)

#check memLp_condExp_of_one_lt
#check earlierMemLpUpTo
#print axioms memLp_condExp_of_one_lt
#print axioms earlierMemLpUpTo

end Stage1Instances.THM_M_1078.Proof
