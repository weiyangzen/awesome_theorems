import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-!
The exact statement gate for ordinary unreduced singular homology with integer coefficients.
The right-hand side deliberately exposes the homology of the singular chain complex rather than
introducing a second, competing definition.
-/

namespace Stage1.THM_M_0540

open AlgebraicTopology CategoryTheory

/-- Integral singular chains on a topological space. -/
noncomputable abbrev IntegralSingularChains (X : Type) [TopologicalSpace X] :
    ChainComplex (ModuleCat ℤ) ℕ :=
  (((singularChainComplexFunctor (ModuleCat ℤ)).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

/-- Integral singular homology in degree `n`. -/
noncomputable abbrev IntegralSingularHomology (X : Type) [TopologicalSpace X] (n : ℕ) :
    ModuleCat ℤ :=
  (((singularHomologyFunctor (ModuleCat ℤ) n).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of X))

/-- Canonical target: integral singular homology is the degree-`n` homology of the integral
singular chain complex. -/
def CanonicalTarget : Prop :=
  ∀ (X : Type) [TopologicalSpace X] (n : ℕ),
    IntegralSingularHomology X n =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
        (IntegralSingularChains X)

/-- Checked witness for the canonical target. This declaration checks statement coherence only;
its definitional body is not proof credit for the later proof phase. -/
theorem canonicalTarget_elaborates : CanonicalTarget := by
  intro X _ n
  rfl

/-- Checked transport to the direct mathlib expression used as an alternate encoding. -/
theorem canonicalTarget_iff_direct :
    CanonicalTarget ↔
      ∀ (X : Type) [TopologicalSpace X] (n : ℕ),
        (((singularHomologyFunctor (ModuleCat ℤ) n).obj (ModuleCat.of ℤ ℤ)).obj
            (TopCat.of X)) =
          (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) n).obj
            ((((singularChainComplexFunctor (ModuleCat ℤ)).obj (ModuleCat.of ℤ ℤ)).obj
              (TopCat.of X))) :=
  Iff.rfl

/-- Boundary fixture: degree zero and the empty space remain inside the quantified target. -/
example :
    IntegralSingularHomology Empty 0 =
      (HomologicalComplex.homologyFunctor (ModuleCat ℤ) (ComplexShape.down ℕ) 0).obj
        (IntegralSingularChains Empty) :=
  canonicalTarget_elaborates Empty 0

end Stage1.THM_M_0540

#print Stage1.THM_M_0540.CanonicalTarget
