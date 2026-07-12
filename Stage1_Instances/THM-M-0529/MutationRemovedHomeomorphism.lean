import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

-- This deliberately invalid mutation removes the homeomorphism witness.
example (n : ℕ) (X Y : TopCat) :
    Nonempty
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).obj X ≅
        ((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).obj Y) := by
  infer_instance

end AwesomeTheorems.THM_M_0529
