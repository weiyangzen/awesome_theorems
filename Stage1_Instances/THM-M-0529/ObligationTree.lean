import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

namespace AwesomeTheorems.THM_M_0529

open AlgebraicTopology CategoryTheory

#check TopCat.isoOfHomeo
#check Functor.map_isIso

/-- Composition certificate for the frozen proof graph.  It deliberately assumes the source-map
`IsIso` obligation; discharging that obligation belongs to the later proof phase. -/
theorem map_isIso_of_source_isIso
    (n : ℕ) (X Y : TopCat) (e : X ≃ₜ Y)
    [IsIso (TopCat.isoOfHomeo e).hom] :
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom) := by
  infer_instance

#print axioms map_isIso_of_source_isIso

end AwesomeTheorems.THM_M_0529
