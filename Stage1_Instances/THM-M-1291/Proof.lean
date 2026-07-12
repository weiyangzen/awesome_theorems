import Statement

/-!
# THM-M-1291 proof execution

This module implements the pointwise analytic leaf of the frozen obligation
tree.  It does not declare the Brezis-Lieb root: the uniform-integral bridge
remains open in the pinned dependency closure.
-/

namespace Stage1Instances.THM_M_1291

open Filter
open scoped Topology

universe u

/-- Pointwise convergence of `fseq` gives convergence of the corrected
`p`-power density.  This is the kernel-checked body for
`M1291-L-POINTWISE`; it is valid for every positive real exponent and hence
serves both exponent branches in the frozen tree. -/
theorem tendsto_pPower_sub_pPower_sub
    {alpha : Type u} {p : Real} (hp : 0 < p)
    {f : alpha -> Complex} {fseq : Nat -> alpha -> Complex} {x : alpha}
    (h : Tendsto (fun n => fseq n x) atTop (nhds (f x))) :
    Tendsto
      (fun n => pPower p (fseq n) x -
        pPower p (fun y => fseq n y - f y) x)
      atTop (nhds (pPower p f x)) := by
  have hsub : Tendsto (fun n => fseq n x - f x) atTop (nhds 0) := by
    simpa using h.sub (tendsto_const_nhds : Tendsto (fun _ : Nat => f x) atTop (nhds (f x)))
  have hnorm : Tendsto (fun n => ‖fseq n x‖) atTop (nhds ‖f x‖) :=
    (continuous_norm.tendsto (f x)).comp h
  have hnorm_sub : Tendsto (fun n => ‖fseq n x - f x‖) atTop (nhds 0) := by
    simpa using (continuous_norm.tendsto (0 : Complex)).comp hsub
  have hpow : Tendsto (fun n => Real.rpow ‖fseq n x‖ p) atTop
      (nhds (Real.rpow ‖f x‖ p)) := by
    exact ((Real.continuous_rpow_const hp.le).tendsto ‖f x‖).comp hnorm
  have hpow_sub : Tendsto (fun n => Real.rpow ‖fseq n x - f x‖ p) atTop
      (nhds 0) := by
    simpa [Real.zero_rpow hp.ne'] using
      ((Real.continuous_rpow_const hp.le).tendsto 0).comp hnorm_sub
  simpa [pPower] using hpow.sub hpow_sub

/-- Almost-everywhere form used by the integral branch of the frozen proof
architecture. -/
theorem ae_tendsto_pPower_sub_pPower_sub
    {alpha : Type u} [MeasurableSpace alpha] {mu : MeasureTheory.Measure alpha}
    {p : Real} (hp : 0 < p) {f : alpha -> Complex}
    {fseq : Nat -> alpha -> Complex}
    (h : ∀ᵐ x ∂mu, Tendsto (fun n => fseq n x) atTop (nhds (f x))) :
    ∀ᵐ x ∂mu,
      Tendsto
        (fun n => pPower p (fseq n) x -
          pPower p (fun y => fseq n y - f y) x)
        atTop (nhds (pPower p f x)) :=
  h.mono fun _ hx => tendsto_pPower_sub_pPower_sub hp hx

#check tendsto_pPower_sub_pPower_sub
#check ae_tendsto_pPower_sub_pPower_sub
#print axioms tendsto_pPower_sub_pPower_sub
#print axioms ae_tendsto_pPower_sub_pPower_sub

end Stage1Instances.THM_M_1291
