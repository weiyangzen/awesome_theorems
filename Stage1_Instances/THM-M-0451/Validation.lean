import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0451 same-worker validation probe

This module reconstructs the final conditional assembly into the exact frozen
target without importing `Proof` or `ObligationTree`. It deliberately consumes
all analytic and arithmetic fields as explicit inputs. It therefore validates
the target adapter, but neither constructs a canonical height nor closes the
Neron-Tate theorem.
-/

noncomputable section

open Filter
open scoped Topology WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0451.Validation

open Stage1Instances.THM_M_0451

universe u

/-- A locally defined split-field interface for the same conditional boundary.
It deliberately keeps the two torsion directions separate. -/
structure ValidationEngine (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  canonicalHeight : E⟮K⟯ → ℝ
  limit_formula : ∀ P : E⟮K⟯,
    Tendsto (fun n : ℕ => (4 : ℝ) ^ (-(n : ℤ)) *
      xHeight (((2 : ℕ) ^ n) • P) / 2) atTop (nhds (canonicalHeight P))
  bounded_difference : ∃ C : ℝ, ∀ P : E⟮K⟯,
    |canonicalHeight P - xHeight P / 2| ≤ C
  quadratic_zsmul : ∀ (m : ℤ) (P : E⟮K⟯),
    canonicalHeight (m • P) = (m : ℝ) ^ 2 * canonicalHeight P
  parallelogram : ∀ P Q : E⟮K⟯,
    canonicalHeight (P + Q) + canonicalHeight (P - Q) =
      2 * canonicalHeight P + 2 * canonicalHeight Q
  nonnegative : ∀ P : E⟮K⟯, 0 ≤ canonicalHeight P
  torsion_to_zero : ∀ P : E⟮K⟯, IsOfFinAddOrder P → canonicalHeight P = 0
  zero_to_torsion : ∀ P : E⟮K⟯, canonicalHeight P = 0 → IsOfFinAddOrder P

/-- Implementation-diverse exact-type probe for the conditional root adapter.

Every substantive height property is an explicit field of `data`; no such
engine is asserted to exist by this declaration. -/
theorem exactTarget_conditional_probe
    (data : forall {K : Type u} [Field K] [DecidableEq K] [NumberField K]
      (E : WeierstrassCurve K) [E.IsElliptic], ValidationEngine K E) :
    NeronTateCanonicalHeightTarget.{u} := by
  intro K _field _decidableEq _numberField E _isElliptic
  let e := data E
  exact Nonempty.intro {
    canonicalHeight := e.canonicalHeight
    limit_formula := e.limit_formula
    bounded_difference := e.bounded_difference
    quadratic_zsmul := e.quadratic_zsmul
    parallelogram := e.parallelogram
    nonnegative := e.nonnegative
    torsion_iff_height_zero := fun P ↦ ⟨e.torsion_to_zero P, e.zero_to_torsion P⟩
  }

assert_no_sorry exactTarget_conditional_probe
#print sorries exactTarget_conditional_probe
#print axioms exactTarget_conditional_probe

end Stage1Instances.THM_M_0451.Validation
