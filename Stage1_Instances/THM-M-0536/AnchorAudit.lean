import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Homology.ShortComplex.Abelian
import Mathlib.Topology.Homotopy.Equiv

open CategoryTheory

namespace Stage1.THM_M_0536

#check AlgebraicTopology.singularHomologyFunctor
#check TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor
#check ContinuousMap.HomotopyEquiv.left_inv
#check ContinuousMap.HomotopyEquiv.right_inv

/-- A checked audit candidate showing that the pinned mathlib homotopy-invariance lemma and the
homotopy-equivalence laws compose to the exact induced-map shape. This is anchor evidence, not the
accepted proof-phase declaration. -/
theorem anchorCandidate
    (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
    (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ) :
    IsIso
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
          (ModuleCat.of ℤ ℤ)).map (TopCat.ofHom e.toFun)) := by
  let F := (AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
    (ModuleCat.of ℤ ℤ)
  let f : TopCat.of X ⟶ TopCat.of Y := TopCat.ofHom e.toFun
  let g : TopCat.of Y ⟶ TopCat.of X := TopCat.ofHom e.invFun
  refine ⟨⟨F.map g, ?_, ?_⟩⟩
  · rw [← F.map_comp]
    obtain ⟨H⟩ := e.left_inv
    have H' : TopCat.Homotopy (f ≫ g) (𝟙 (TopCat.of X)) := H
    have h := TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor H'
      (ModuleCat.of ℤ ℤ) n
    change F.map (f ≫ g) = 𝟙 (F.obj (TopCat.of X))
    rw [show F.map (f ≫ g) = F.map (𝟙 (TopCat.of X)) by
      simpa [F, f, g, AlgebraicTopology.singularHomologyFunctor] using h]
    exact F.map_id _
  · rw [← F.map_comp]
    obtain ⟨H⟩ := e.right_inv
    have H' : TopCat.Homotopy (g ≫ f) (𝟙 (TopCat.of Y)) := H
    have h := TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor H'
      (ModuleCat.of ℤ ℤ) n
    change F.map (g ≫ f) = 𝟙 (F.obj (TopCat.of Y))
    rw [show F.map (g ≫ f) = F.map (𝟙 (TopCat.of Y)) by
      simpa [F, f, g, AlgebraicTopology.singularHomologyFunctor] using h]
    exact F.map_id _

#print axioms anchorCandidate

end Stage1.THM_M_0536
