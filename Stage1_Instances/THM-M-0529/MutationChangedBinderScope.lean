import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

-- This deliberately invalid mutation moves the witness before the spaces it relates.
def ChangedBinderScope : Prop :=
  ∀ (e : X ≃ₜ Y) (n : ℕ) (X Y : TopCat),
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom)

end AwesomeTheorems.THM_M_0529
