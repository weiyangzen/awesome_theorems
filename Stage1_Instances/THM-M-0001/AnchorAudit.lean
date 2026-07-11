import Mathlib.Algebra.Homology.HomologySequence

/-!
# THM-M-0001 anchor-audit probes

This file checks the exact types of the pinned mathlib declarations needed by
the frozen target. The examples are candidate adapters, not accepted proof or
release declarations.
-/

universe v u w

namespace Stage1Instances.THM_M_0001.AnchorAudit

open CategoryTheory
open CategoryTheory.Limits
open HomologicalComplex

variable {C : Type u} [Category.{v} C] [Abelian C]
variable {ι : Type w} {c : ComplexShape ι}
variable {S : ShortComplex (HomologicalComplex C c)}

#check CategoryTheory.ShortComplex.ShortExact.δ
#check CategoryTheory.ShortComplex.ShortExact.comp_δ
#check CategoryTheory.ShortComplex.ShortExact.δ_comp
#check CategoryTheory.ShortComplex.ShortExact.homology_exact₁
#check CategoryTheory.ShortComplex.ShortExact.homology_exact₂
#check CategoryTheory.ShortComplex.ShortExact.homology_exact₃

example (hS : S.ShortExact) (i : ι) :
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.f i)
      (HomologicalComplex.homologyMap S.g i)
      (by
        rw [← HomologicalComplex.homologyMap_comp, S.zero,
          HomologicalComplex.homologyMap_zero])).Exact := by
  exact hS.homology_exact₂ i

example (hS : S.ShortExact) (i j : ι) (hij : c.Rel i j) :
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.g i)
      (hS.δ i j hij)
      (hS.comp_δ i j hij)).Exact := by
  exact hS.homology_exact₃ i j hij

example (hS : S.ShortExact) (i j : ι) (hij : c.Rel i j) :
    (ShortComplex.mk
      (hS.δ i j hij)
      (HomologicalComplex.homologyMap S.f j)
      (hS.δ_comp i j hij)).Exact := by
  exact hS.homology_exact₁ i j hij

#print axioms CategoryTheory.ShortComplex.ShortExact.homology_exact₁
#print axioms CategoryTheory.ShortComplex.ShortExact.homology_exact₂
#print axioms CategoryTheory.ShortComplex.ShortExact.homology_exact₃

end Stage1Instances.THM_M_0001.AnchorAudit
