import Proof
import ObligationTree
import Mathlib.Algebra.Category.ModuleCat.Products
import Mathlib.LinearAlgebra.Finsupp.VectorSpace

/-!
# Additional proof bodies for THM-M-0005

This module strengthens the proof-phase implementation without claiming the unavailable Kunneth
root. It proves degreewise freeness of singular chains, the identity and composition laws for the
implemented tensor and `Tor₁` direct-sum maps, and exact conditional composition of those maps with
the six still-missing Kunneth field families.
-/

noncomputable section

open AlgebraicTopology CategoryTheory CategoryTheory.Limits
open CategoryTheory.MonoidalCategory

universe u

namespace AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21

open AwesomeTheorems.Stage1.THM_M_0005
open AwesomeTheorems.Stage1.THM_M_0005.Proof

/-- Every degree of the singular chain complex is a free module on its singular simplices. -/
theorem singularChains_free
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X : TopCat.{u}) (n : ℕ) :
    Module.Free R ((((singularChainComplexFunctor (ModuleCat.{u} R)).obj
      (ModuleCat.of R R)).obj X).X n) := by
  dsimp [singularChainComplexFunctor, SSet.singularChainComplexFunctor]
  let e : (↑(∐ fun _ : ((TopCat.toSSet.obj X).obj
      (Opposite.op (SimplexCategory.mk n))) ↦ ModuleCat.of R R) : Type u) ≃ₗ[R]
      (((TopCat.toSSet.obj X).obj (Opposite.op (SimplexCategory.mk n))) →₀ R) :=
    (colimit.isoColimitCocone
      ⟨ModuleCat.finsuppCocone R R
        ((TopCat.toSSet.obj X).obj (Opposite.op (SimplexCategory.mk n))),
       ModuleCat.finsuppCoconeIsColimit R R
        ((TopCat.toSSet.obj X).obj (Opposite.op (SimplexCategory.mk n)))⟩).toLinearEquiv
  exact Module.Free.of_equiv'
    (R := R)
    (N := (↑(∐ fun _ : ((TopCat.toSSet.obj X).obj
      (Opposite.op (SimplexCategory.mk n))) ↦ ModuleCat.of R R) : Type u))
    (Module.Free.finsupp _ _ _) e.symm

/-- The singular-chain degree object has both algebraic freeness and categorical projectivity. -/
theorem singularChains_free_and_projective
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X : TopCat.{u}) (n : ℕ) :
    Module.Free R ((((singularChainComplexFunctor (ModuleCat.{u} R)).obj
        (ModuleCat.of R R)).obj X).X n) ∧
      Projective ((((singularChainComplexFunctor (ModuleCat.{u} R)).obj
        (ModuleCat.of R R)).obj X).X n) :=
  ⟨singularChains_free R X n, singularChains_projective R X n⟩

/-- The implemented map on tensor summands preserves identity maps. -/
theorem tensorMap_id
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) (n : ℕ) :
    tensorMap R (𝟙 X) (𝟙 Y) n = 𝟙 (TensorTerm R X Y n) := by
  apply Sigma.hom_ext
  intro pq
  rw [tensorMap_component]
  simp

/-- The implemented map on tensor summands preserves composition in both variables. -/
theorem tensorMap_comp
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    {X X' X'' Y Y' Y'' : TopCat.{u}}
    (f : X ⟶ X') (f' : X' ⟶ X'') (g : Y ⟶ Y') (g' : Y' ⟶ Y'')
    (n : ℕ) :
    tensorMap R (f ≫ f') (g ≫ g') n = tensorMap R f g n ≫ tensorMap R f' g' n := by
  apply Sigma.hom_ext
  intro pq
  rw [tensorMap_component]
  rw [← Category.assoc]
  rw [tensorMap_component]
  rw [Functor.map_comp, Functor.map_comp]
  rw [← tensorHom_comp_tensorHom]
  rw [Category.assoc]
  exact congrArg (fun k ↦
    (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
      (ModuleCat.of R R)).map f ⊗ₘ
    ((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
      (ModuleCat.of R R)).map g) ≫ k)
    (tensorMap_component R f' g' n pq).symm

/-- The implemented map on `Tor₁` summands preserves identity maps. -/
theorem torMap_id
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) (n : ℕ) :
    torMap R (𝟙 X) (𝟙 Y) n = 𝟙 (TorTerm R X Y n) := by
  apply Sigma.hom_ext
  intro pq
  rw [torMap_component]
  change (NatTrans.leftDerived
      ((tensoringLeft (ModuleCat.{u} R)).map
        (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
          (ModuleCat.of R R)).map (𝟙 X))) 1).app (Homology R pq.1.2 Y) ≫
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj (Homology R pq.1.1 X)).map
        (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
          (ModuleCat.of R R)).map (𝟙 Y)) ≫
        Sigma.ι (fun pq : TorDegrees n ↦
          ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
            (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)) pq =
      Sigma.ι (fun pq : TorDegrees n ↦
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)) pq
  simp

/-- The implemented map on `Tor₁` summands preserves composition in both variables. -/
theorem torMap_comp
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    {X X' X'' Y Y' Y'' : TopCat.{u}}
    (f : X ⟶ X') (f' : X' ⟶ X'') (g : Y ⟶ Y') (g' : Y' ⟶ Y'')
    (n : ℕ) :
    torMap R (f ≫ f') (g ≫ g') n = torMap R f g n ≫ torMap R f' g' n := by
  apply Sigma.hom_ext
  intro pq
  rw [← Category.assoc]
  rw [torMap_component]
  rw [torMap_component]
  simp only [Functor.map_comp]
  rw [Category.assoc, Category.assoc, Category.assoc]
  rw [torMap_component]
  simp only [NatTrans.comp_app]
  slice_rhs 2 3 =>
    rw [((CategoryTheory.Tor (ModuleCat.{u} R) 1).map
      (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
        (ModuleCat.of R R)).map f')).naturality
      (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
        (ModuleCat.of R R)).map g)]
  dsimp only [Homology]
  rfl

/-
Exact checked composition of the implemented direct-sum maps with the remaining Kunneth fields.

The six arguments are precisely the unimplemented inclusion, projection, exactness, and naturality
data. This theorem verifies their composition to the unchanged canonical root without supplying or
hiding any of those premises.
-/
theorem kunnethFormula_of_fields
    (inclusion : ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
      (X Y : TopCat.{u}) (n : ℕ),
      TensorTerm R X Y n ⟶ ProductHomology R X Y n)
    (projection : ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
      (X Y : TopCat.{u}) (n : ℕ),
      ProductHomology R X Y n ⟶ TorTerm R X Y n)
    (zero : ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
      (X Y : TopCat.{u}) (n : ℕ),
      inclusion R X Y n ≫ projection R X Y n = 0)
    (shortExact : ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
      (X Y : TopCat.{u}) (n : ℕ),
      (ShortComplex.mk (inclusion R X Y n) (projection R X Y n)
        (zero R X Y n)).ShortExact)
    (inclusion_natural : ∀ (R : Type u) [CommRing R] [IsDomain R]
      [IsPrincipalIdealRing R] {X X' Y Y' : TopCat.{u}}
      (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
      tensorMap R f g n ≫ inclusion R X' Y' n = inclusion R X Y n ≫
        ((singularHomologyFunctor (ModuleCat.{u} R) n).obj
          (ModuleCat.of R R)).map (Limits.prod.map f g))
    (projection_natural : ∀ (R : Type u) [CommRing R] [IsDomain R]
      [IsPrincipalIdealRing R] {X X' Y Y' : TopCat.{u}}
      (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
      ((singularHomologyFunctor (ModuleCat.{u} R) n).obj
          (ModuleCat.of R R)).map (Limits.prod.map f g) ≫ projection R X' Y' n =
        projection R X Y n ≫ torMap R f g n) :
    KunnethFormula.{u} := by
  apply AwesomeTheorems.Stage1.THM_M_0005.ObligationTree.root_compose
  intro R _ _ _
  exact AwesomeTheorems.Stage1.THM_M_0005.ObligationTree.assemble_sequence R
    (inclusion R) (projection R) (zero R) (shortExact R)
    (tensorMap R) (torMap R) (tensorMap_component R) (torMap_component R)
    (inclusion_natural R) (projection_natural R)

#print axioms singularChains_free
#print axioms singularChains_free_and_projective
#print axioms tensorMap_id
#print axioms tensorMap_comp
#print axioms torMap_id
#print axioms torMap_comp
#print axioms kunnethFormula_of_fields

end AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21
