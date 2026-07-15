/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.MeasureTheory.Constructions.BorelSpace.ContinuousLinearMap
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import ErgodicTheory.Cocycle.Basic

/-!
# Measurability of the L2 operator norm and the matrix inverse

The Oseledets / Furstenberg–Kesten development needs that the (scoped) L2 operator
norm `‖·‖` and the matrix inverse `M ↦ M⁻¹` are measurable as functions on
`Matrix (Fin d) (Fin d) ℝ` equipped with the entrywise (Pi) measurable structure
`ErgodicTheory.instMeasurableSpaceMatrix`.

The subtlety is that Mathlib's `Measurable.norm` is stated for a `BorelSpace`,
whereas the matrix σ-algebra here is the Pi structure. The L2 operator-norm topology
on `Matrix (Fin d) (Fin d) ℝ` is *definitionally* the Pi product topology (it is
installed via `replaceTopology` along the entrywise-continuous identification with
continuous linear maps of `EuclideanSpace`), so the Pi measurable structure is exactly
the Borel structure of the norm topology. We record the corresponding
`OpensMeasurableSpace` instance and deduce measurability of `‖·‖` from continuity;
the matrix inverse is handled entrywise via the adjugate/determinant formula.

## Main results

* `ErgodicTheory.instOpensMeasurableSpaceMatrix`: the Pi measurable structure on square
  real matrices is an `OpensMeasurableSpace` for the L2 operator-norm topology.
* `ErgodicTheory.measurable_l2_opNorm`: the L2 operator norm is measurable.
* `ErgodicTheory.measurable_det`: the determinant is measurable.
* `ErgodicTheory.measurable_inv_matrix`: the matrix inverse `M ↦ M⁻¹` is measurable.
-/

open MeasureTheory
open scoped Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {d : ℕ}

/-- The Pi measurable structure on matrices is the Borel structure of the L2 operator-norm
topology (which is definitionally the Pi product topology), so it is an
`OpensMeasurableSpace`. -/
instance instOpensMeasurableSpaceMatrix :
    OpensMeasurableSpace (Matrix (Fin d) (Fin d) ℝ) :=
  inferInstanceAs (OpensMeasurableSpace (Fin d → Fin d → ℝ))

/-- **Measurability of the L2 operator norm** on the entrywise (Pi) measurable structure. -/
theorem measurable_l2_opNorm :
    Measurable (fun M : Matrix (Fin d) (Fin d) ℝ => ‖M‖) :=
  continuous_norm.measurable

/-- Each matrix entry is measurable. -/
theorem measurable_matrix_entry (i j : Fin d) :
    Measurable (fun M : Matrix (Fin d) (Fin d) ℝ => M i j) :=
  (measurable_pi_apply j).comp (measurable_pi_apply i)

/-- The determinant is measurable (a polynomial in the entries). -/
theorem measurable_det :
    Measurable (fun M : Matrix (Fin d) (Fin d) ℝ => M.det) := by
  simp only [Matrix.det_apply]
  refine Finset.measurable_sum _ fun σ _ => ?_
  refine Measurable.const_smul ?_ _
  exact Finset.measurable_prod _ fun i _ => measurable_matrix_entry _ _

/-- The adjugate is measurable (each entry is a determinant of a row update). -/
theorem measurable_adjugate :
    Measurable (fun M : Matrix (Fin d) (Fin d) ℝ => M.adjugate) := by
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  simp only [Matrix.adjugate_apply, Matrix.det_apply]
  refine Finset.measurable_sum _ fun σ _ => ?_
  refine Measurable.const_smul ?_ _
  refine Finset.measurable_prod _ fun k _ => ?_
  simp only [Matrix.updateRow_apply]
  by_cases h : σ k = j <;> simp only [h, if_true, if_false]
  · exact measurable_const
  · exact measurable_matrix_entry _ _

/-- **Measurability of the matrix inverse** `M ↦ M⁻¹` on the entrywise measurable
structure (`M⁻¹ = (det M)⁻¹ • adjugate M`, entrywise a ratio of polynomials). -/
theorem measurable_inv_matrix :
    Measurable (fun M : Matrix (Fin d) (Fin d) ℝ => M⁻¹) := by
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  simp only [Matrix.inv_def, Matrix.smul_apply, smul_eq_mul, Ring.inverse_eq_inv']
  refine Measurable.mul measurable_det.inv ?_
  exact (measurable_pi_apply j).comp ((measurable_pi_apply i).comp measurable_adjugate)

end ErgodicTheory
