import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-! Narrow probes for the immutable formal-anchor audit. -/

namespace Stage1.THM_M_0540.AnchorAudit

open AlgebraicTopology CategoryTheory

noncomputable abbrev IntegralChains (X : Type) [TopologicalSpace X] :
    ChainComplex (ModuleCat ℤ) ℕ :=
  (((singularChainComplexFunctor (ModuleCat ℤ)).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

noncomputable abbrev IntegralHomology (X : Type) [TopologicalSpace X] (n : ℕ) :
    ModuleCat ℤ :=
  (((singularHomologyFunctor (ModuleCat ℤ) n).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

/-- The pinned definition is an exact terminal anchor for the frozen construction identity. -/
theorem pinned_mathlib_exact_anchor (X : Type) [TopologicalSpace X] (n : ℕ) :
    IntegralHomology X n =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        (IntegralChains X) := by
  rfl

#check SSet.singularChainComplexFunctor
#check singularChainComplexFunctor
#check singularHomologyFunctor
#print axioms pinned_mathlib_exact_anchor

end Stage1.THM_M_0540.AnchorAudit
