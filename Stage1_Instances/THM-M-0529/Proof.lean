import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.AB

/-!
# THM-M-0529 proof implementation

The proof exposes both frozen bridge obligations. A homeomorphism yields an isomorphism in
`TopCat`, and every functor maps an isomorphism to an isomorphism. The root theorem specializes
that generic categorical fact to integral singular homology in each natural-number degree.
-/

namespace AwesomeTheorems.THM_M_0529.Proof

open AlgebraicTopology CategoryTheory

/-- The exact canonical proposition frozen by `Statement.lean`. -/
def CanonicalTarget : Prop :=
  ∀ (n : ℕ) (X Y : TopCat) (e : X ≃ₜ Y),
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom)

/-- `TopCat.isoOfHomeo e` supplies the source-morphism isomorphism instance. -/
theorem homeomorphismHomIsIso (X Y : TopCat) (e : X ≃ₜ Y) :
    IsIso (TopCat.isoOfHomeo e).hom := by
  infer_instance

/-- The exact homology functor preserves the source isomorphism. -/
theorem integralSingularHomologyMapIsIso
    (n : ℕ) (X Y : TopCat) (e : X ≃ₜ Y) :
    IsIso
      (((singularHomologyFunctor AddCommGrpCat n).obj (AddCommGrpCat.of ℤ)).map
        (TopCat.isoOfHomeo e).hom) := by
  letI := homeomorphismHomIsIso X Y e
  infer_instance

/-- Exact root closure and child-to-parent composition certificate. -/
theorem homologyIsHomeomorphismInvariant : CanonicalTarget := by
  intro n X Y e
  exact integralSingularHomologyMapIsIso n X Y e

#print axioms homeomorphismHomIsIso
#print axioms integralSingularHomologyMapIsIso
#print axioms homologyIsHomeomorphismInvariant

end AwesomeTheorems.THM_M_0529.Proof
