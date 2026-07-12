import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

set_option autoImplicit false

namespace Stage1.THM_M_0540.MutationRemovedDegree

open CategoryTheory

/- This intentionally invalid mutation removes the degree binder but still refers to it. -/
def Target : Prop :=
  ∀ (X : Type) [TopologicalSpace X],
    (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)).obj (TopCat.of X)) =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        ((((AlgebraicTopology.singularChainComplexFunctor (ModuleCat ℤ)).obj
          (ModuleCat.of ℤ ℤ)).obj (TopCat.of X)))

end Stage1.THM_M_0540.MutationRemovedDegree
