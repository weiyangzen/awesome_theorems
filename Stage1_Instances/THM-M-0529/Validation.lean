import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

/-!
# THM-M-0529 independent exact-type validation probe

This module does not import the proof-phase module. It reconstructs the exact frozen target from
the pinned categorical instances and therefore detects a missing or mismatched local proof wrapper.
-/

namespace AwesomeTheorems.THM_M_0529.Validation

open AlgebraicTopology CategoryTheory

def IndependentTarget : Prop :=
  ∀ (n : ℕ) (X Y : TopCat) (e : X ≃ₜ Y),
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom)

theorem independentHomologyIsHomeomorphismInvariant : IndependentTarget := by
  intro n X Y e
  haveI : IsIso (TopCat.isoOfHomeo e).hom := (TopCat.isoOfHomeo e).isIso_hom
  exact Functor.map_isIso _ _

#print IndependentTarget
#print axioms independentHomologyIsHomeomorphismInvariant

end AwesomeTheorems.THM_M_0529.Validation
