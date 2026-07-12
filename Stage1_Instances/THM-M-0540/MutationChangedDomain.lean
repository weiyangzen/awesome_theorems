import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

set_option autoImplicit false

namespace Stage1.THM_M_0540.MutationChangedDomain

open CategoryTheory

/- This intentionally invalid mutation changes spaces to `Nat` and applies `TopCat.of`. -/
def Target : Prop :=
  ∀ (X : Nat) (n : ℕ),
    (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)).obj (TopCat.of X)) =
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).obj (TopCat.of X))

end Stage1.THM_M_0540.MutationChangedDomain
