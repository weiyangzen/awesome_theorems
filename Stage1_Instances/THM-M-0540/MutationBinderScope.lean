import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

set_option autoImplicit false

namespace Stage1.THM_M_0540.MutationBinderScope

/- This intentionally invalid mutation moves the topology binder outside `X`'s scope. -/
def Target : Prop :=
  [TopologicalSpace X] → ∀ (X : Type) (n : ℕ),
    (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)).obj (TopCat.of X)) =
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).obj (TopCat.of X))

end Stage1.THM_M_0540.MutationBinderScope
