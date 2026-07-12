import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

-- This deliberately invalid mutation changes the degree domain from `ℕ` to `ℤ`.
example (n : ℤ) (X Y : TopCat) (e : X ≃ₜ Y) :
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom) := by
  infer_instance

end AwesomeTheorems.THM_M_0529
