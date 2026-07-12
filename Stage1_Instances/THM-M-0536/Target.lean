import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Homology.ShortComplex.Abelian
import Mathlib.Topology.Homotopy.Equiv

open CategoryTheory

namespace Stage1.THM_M_0536

/-- Integral singular homology in degree `n`, valued in abelian groups. -/
noncomputable abbrev IntegralSingularHomology (n : ℕ) (X : TopCat) : ModuleCat ℤ :=
  (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)).obj X)

/--
The exact Stage1 target: the map on integral singular homology induced by the forward map of a
chosen homotopy equivalence is an isomorphism in every natural-number degree.
-/
def HomotopyInvarianceStatement : Prop :=
  ∀ (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
      (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ),
    IsIso
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
          (ModuleCat.of ℤ ℤ)).map (TopCat.ofHom e.toFun))

#check HomotopyInvarianceStatement

end Stage1.THM_M_0536
