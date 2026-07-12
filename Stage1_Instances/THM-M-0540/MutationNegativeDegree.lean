import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

set_option autoImplicit false

namespace Stage1.THM_M_0540.MutationNegativeDegree

/- This intentionally invalid boundary mutation asks the Nat-graded API for an Int degree. -/
def Target : Prop :=
  ∀ (X : Type) [TopologicalSpace X] (n : Int),
    (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)).obj (TopCat.of X)) =
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).obj (TopCat.of X))

end Stage1.THM_M_0540.MutationNegativeDegree
