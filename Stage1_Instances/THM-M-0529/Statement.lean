import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

/-- The exact statement target: integral singular homology sends a homeomorphism to an
isomorphism in the category of abelian groups, in every natural-number degree. -/
def CanonicalTarget : Prop :=
  ∀ (n : ℕ) (X Y : TopCat) (e : X ≃ₜ Y),
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom)

#print CanonicalTarget

end AwesomeTheorems.THM_M_0529
