import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Homology.ShortComplex.Abelian
import Mathlib.Topology.Homotopy.Equiv

open CategoryTheory

namespace Stage1.THM_M_0536

/-- The exact frozen target, repeated because the dossier is outside the Lake source tree. -/
def HomotopyInvarianceStatement : Prop :=
  ∀ (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
      (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ),
    IsIso
      (((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
          (ModuleCat.of ℤ ℤ)).map (TopCat.ofHom e.toFun))

/-- The forward-then-inverse homotopy gives the first induced inverse law. -/
theorem induced_left_identity
    (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
    (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ) :
    let F := (AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)
    let f : TopCat.of X ⟶ TopCat.of Y := TopCat.ofHom e.toFun
    let g : TopCat.of Y ⟶ TopCat.of X := TopCat.ofHom e.invFun
    F.map f ≫ F.map g = 𝟙 (F.obj (TopCat.of X)) := by
  dsimp only
  rw [← Functor.map_comp]
  obtain ⟨H⟩ := e.left_inv
  have H' : TopCat.Homotopy
      ((TopCat.ofHom e.toFun) ≫ (TopCat.ofHom e.invFun)) (𝟙 (TopCat.of X)) := H
  have h := TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor H'
    (ModuleCat.of ℤ ℤ) n
  rw [show
    ((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).map
          ((TopCat.ofHom e.toFun) ≫ (TopCat.ofHom e.invFun)) =
      ((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).map (𝟙 (TopCat.of X)) by
        simpa [AlgebraicTopology.singularHomologyFunctor] using h]
  exact ((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
    (ModuleCat.of ℤ ℤ)).map_id _

/-- The inverse-then-forward homotopy gives the second induced inverse law. -/
theorem induced_right_identity
    (X Y : Type) [TopologicalSpace X] [TopologicalSpace Y]
    (e : ContinuousMap.HomotopyEquiv X Y) (n : ℕ) :
    let F := (AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
      (ModuleCat.of ℤ ℤ)
    let f : TopCat.of X ⟶ TopCat.of Y := TopCat.ofHom e.toFun
    let g : TopCat.of Y ⟶ TopCat.of X := TopCat.ofHom e.invFun
    F.map g ≫ F.map f = 𝟙 (F.obj (TopCat.of Y)) := by
  dsimp only
  rw [← Functor.map_comp]
  obtain ⟨H⟩ := e.right_inv
  have H' : TopCat.Homotopy
      ((TopCat.ofHom e.invFun) ≫ (TopCat.ofHom e.toFun)) (𝟙 (TopCat.of Y)) := H
  have h := TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor H'
    (ModuleCat.of ℤ ℤ) n
  rw [show
    ((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).map
          ((TopCat.ofHom e.invFun) ≫ (TopCat.ofHom e.toFun)) =
      ((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
        (ModuleCat.of ℤ ℤ)).map (𝟙 (TopCat.of Y)) by
        simpa [AlgebraicTopology.singularHomologyFunctor] using h]
  exact ((AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
    (ModuleCat.of ℤ ℤ)).map_id _

/-- Exact root proof: the map induced by the chosen forward equivalence has the map induced by
the chosen inverse as a two-sided inverse. -/
theorem homotopyInvariance : HomotopyInvarianceStatement := by
  intro X Y _ _ e n
  let F := (AlgebraicTopology.singularHomologyFunctor (ModuleCat ℤ) n).obj
    (ModuleCat.of ℤ ℤ)
  let f : TopCat.of X ⟶ TopCat.of Y := TopCat.ofHom e.toFun
  let g : TopCat.of Y ⟶ TopCat.of X := TopCat.ofHom e.invFun
  change IsIso (F.map f)
  exact ⟨⟨F.map g, induced_left_identity X Y e n, induced_right_identity X Y e n⟩⟩

#print axioms induced_left_identity
#print axioms induced_right_identity
#print axioms homotopyInvariance

end Stage1.THM_M_0536
