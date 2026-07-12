import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

example :
    IsIso
      (((singularHomologyFunctor AddCommGrpCat 0).obj (AddCommGrpCat.of ℤ)).map
        (Iso.refl (TopCat.of Empty)).hom) := by
  infer_instance

end AwesomeTheorems.THM_M_0529
