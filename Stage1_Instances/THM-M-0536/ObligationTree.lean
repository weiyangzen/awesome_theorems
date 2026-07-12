import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Homology.ShortComplex.Abelian
import Mathlib.Topology.Homotopy.Equiv

open CategoryTheory

namespace Stage1.THM_M_0536

/-- Standalone restatement of the exact proposition in `Target.lean`; the validation receipt checks
both modules under the same pinned imports. -/
def HomotopyInvarianceStatement : Prop :=
  ∀ (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
      (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ),
    IsIso
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
          (ModuleCat.of ℤ ℤ)).map (TopCat.ofHom e.toFun))

/-- The two inverse laws needed after applying integral singular homology. Keeping this package
explicit makes the checked root composition independent of the still-open proof obligations that
derive the laws from the two topological homotopies. -/
def InducedInverseLaws : Prop :=
  ∀ (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
      (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ),
    let F := (AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)
    let f : TopCat.of X ⟶ TopCat.of Y := TopCat.ofHom e.toFun
    let g : TopCat.of Y ⟶ TopCat.of X := TopCat.ofHom e.invFun
    F.map f ≫ F.map g = 𝟙 (F.obj (TopCat.of X)) ∧
      F.map g ≫ F.map f = 𝟙 (F.obj (TopCat.of Y))

/-- Checked child-to-parent composition. It consumes both exact induced inverse laws and yields the
canonical target; it does not prove those laws. -/
theorem root_of_inducedInverseLaws (laws : InducedInverseLaws) :
    HomotopyInvarianceStatement := by
  intro X Y _ _ e n
  let F := (AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
    (ModuleCat.of ℤ ℤ)
  let f : TopCat.of X ⟶ TopCat.of Y := TopCat.ofHom e.toFun
  let g : TopCat.of Y ⟶ TopCat.of X := TopCat.ofHom e.invFun
  have h := laws X Y e n
  change IsIso (F.map f)
  exact ⟨⟨F.map g, h.1, h.2⟩⟩

#print axioms root_of_inducedInverseLaws

end Stage1.THM_M_0536
