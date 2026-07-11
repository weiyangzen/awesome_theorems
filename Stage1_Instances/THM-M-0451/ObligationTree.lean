import Statement

/-!
# THM-M-0451 conditional obligation composition

This module freezes a typed boundary between the analytic construction and the
six properties in the exact target.  The engine is deliberately uninhabited:
the checked composition below is not a proof of the Neron-Tate theorem.
-/

noncomputable section

open Filter
open scoped Topology WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0451.ObligationTree

universe u

/-- The open mathematical obligations, with the two directions of the torsion
kernel separated so that neither direction can be hidden in an `iff`. -/
structure CanonicalHeightEngine (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  canonicalHeight : E⟮K⟯ -> Real
  limit_formula : forall P : E⟮K⟯,
    Tendsto (fun n : Nat => (4 : Real) ^ (-(n : Int)) *
      xHeight (((2 : Nat) ^ n) • P) / 2) atTop (nhds (canonicalHeight P))
  bounded_difference : exists C : Real, forall P : E⟮K⟯,
    |canonicalHeight P - xHeight P / 2| <= C
  quadratic_zsmul : forall (m : Int) (P : E⟮K⟯),
    canonicalHeight (m • P) = (m : Real) ^ 2 * canonicalHeight P
  parallelogram : forall P Q : E⟮K⟯,
    canonicalHeight (P + Q) + canonicalHeight (P - Q) =
      2 * canonicalHeight P + 2 * canonicalHeight Q
  nonnegative : forall P : E⟮K⟯, 0 <= canonicalHeight P
  torsion_to_zero : forall P : E⟮K⟯, IsOfFinAddOrder P -> canonicalHeight P = 0
  zero_to_torsion : forall P : E⟮K⟯, canonicalHeight P = 0 -> IsOfFinAddOrder P

/-- Binder- and normalization-preserving conditional assembly into the exact
canonical target. -/
theorem engine_compose
    (engine : forall {K : Type u} [Field K] [DecidableEq K] [NumberField K]
      (E : WeierstrassCurve K) [E.IsElliptic], CanonicalHeightEngine K E) :
    NeronTateCanonicalHeightTarget.{u} := by
  intro K _field _decidableEq _numberField E _isElliptic
  let e := engine E
  exact Nonempty.intro {
    canonicalHeight := e.canonicalHeight
    limit_formula := e.limit_formula
    bounded_difference := e.bounded_difference
    quadratic_zsmul := e.quadratic_zsmul
    parallelogram := e.parallelogram
    nonnegative := e.nonnegative
    torsion_iff_height_zero := fun P => ⟨e.torsion_to_zero P, e.zero_to_torsion P⟩
  }

#check CanonicalHeightEngine
#check engine_compose
#print axioms engine_compose

end Stage1Instances.THM_M_0451.ObligationTree
