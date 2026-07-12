import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-!
# THM-M-0540 proof implementation

This module closes the frozen construction-level target by exposing the definitional equation in
`singularHomologyFunctor`, then composing that equation with the exact root proposition.
-/

namespace Stage1.THM_M_0540.Proof

open AlgebraicTopology CategoryTheory

/-- Integral singular chains, matching the frozen statement exactly. -/
noncomputable abbrev IntegralSingularChains (X : Type) [TopologicalSpace X] :
    ChainComplex (ModuleCat ℤ) ℕ :=
  (((singularChainComplexFunctor (ModuleCat ℤ)).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

/-- Integral singular homology, matching the frozen statement exactly. -/
noncomputable abbrev IntegralSingularHomology (X : Type) [TopologicalSpace X] (n : ℕ) :
    ModuleCat ℤ :=
  (((singularHomologyFunctor (ModuleCat ℤ) n).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

/-- The exact canonical proposition frozen by `Statement.lean`. -/
def CanonicalTarget : Prop :=
  ∀ (X : Type) [TopologicalSpace X] (n : ℕ),
    IntegralSingularHomology X n =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        (IntegralSingularChains X)

/-- Frozen terminal obligation: unfold the pinned singular-homology functor at the chosen
coefficient object, space, and degree. -/
theorem unfoldingEquation
    (X : Type) [TopologicalSpace X] (n : ℕ) :
    IntegralSingularHomology X n =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        (IntegralSingularChains X) := by
  rfl

/-- Exact child-to-root composition certificate. -/
theorem integralSingularHomology_eq_homology : CanonicalTarget := by
  intro X _ n
  exact unfoldingEquation X n

#print axioms unfoldingEquation
#print axioms integralSingularHomology_eq_homology

end Stage1.THM_M_0540.Proof
