import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-! Checked composition boundary for the frozen singular-homology obligation tree. -/

namespace Stage1.THM_M_0540

open AlgebraicTopology CategoryTheory

/-- Standalone restatement of the exact definitions in `Statement.lean`; validation checks both
files against their recorded hash in the same pinned environment. -/
noncomputable abbrev IntegralSingularChains (X : Type) [TopologicalSpace X] :
    ChainComplex (ModuleCat ℤ) ℕ :=
  (((singularChainComplexFunctor (ModuleCat ℤ)).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

noncomputable abbrev IntegralSingularHomology (X : Type) [TopologicalSpace X] (n : ℕ) :
    ModuleCat ℤ :=
  (((singularHomologyFunctor (ModuleCat ℤ) n).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

def CanonicalTarget : Prop :=
  ∀ (X : Type) [TopologicalSpace X] (n : ℕ),
    IntegralSingularHomology X n =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        (IntegralSingularChains X)

/-- The exact definitional equation consumed by the final binder assembly. It is deliberately left
as an input here: locating an `rfl` anchor during audit does not grant proof-phase credit. -/
def UnfoldingEquation : Prop :=
  ∀ (X : Type) [TopologicalSpace X] (n : ℕ),
    IntegralSingularHomology X n =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        (IntegralSingularChains X)

/-- Checked child-to-parent composition from the exact unfolding obligation to the canonical root.
This theorem does not discharge `UnfoldingEquation`. -/
theorem root_of_unfolding (h : UnfoldingEquation) : CanonicalTarget := h

#print axioms root_of_unfolding

end Stage1.THM_M_0540
