import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

#check TopCat.isoOfHomeo
#check Iso.isIso_hom
#check Functor.map_isIso
#check singularHomologyFunctor

/-- Audit probe for the exact candidate composition. This is evidence for anchor selection, not the
accepted proof-phase declaration. -/
theorem anchorCandidate
    (n : ℕ) (X Y : TopCat) (e : X ≃ₜ Y) :
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom) := by
  infer_instance

#print axioms anchorCandidate

end AwesomeTheorems.THM_M_0529
