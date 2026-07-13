import KunnethStatement

/-!
# Partial proof bodies for THM-M-0005

This module proves a projectivity input and implements the functorial maps on the tensor and `Tor₁`
direct sums with their component formulas.  These are field-level helper bodies toward
`M0005-CHAIN-FREE` and `M0005-COMPONENTS`; they do not close either node without the frozen
dependencies and checked composition.  They also do not construct the Kunneth inclusion or
projection and therefore do not close `M0005-TOP-MAPS` or the root.
-/

noncomputable section

open AlgebraicTopology CategoryTheory CategoryTheory.Limits
open CategoryTheory.MonoidalCategory

universe u

namespace AwesomeTheorems.Stage1.THM_M_0005.Proof

open AwesomeTheorems.Stage1.THM_M_0005

/-- Every degree of the singular chain complex with coefficients in `R` is projective. -/
theorem singularChains_projective
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X : TopCat.{u}) (n : ℕ) :
    Projective ((((singularChainComplexFunctor (ModuleCat.{u} R)).obj
      (ModuleCat.of R R)).obj X).X n) := by
  dsimp [singularChainComplexFunctor, SSet.singularChainComplexFunctor]
  set_option synthInstance.maxHeartbeats 100000 in
  infer_instance

/-- The canonical map on the tensor direct sum induced by maps of both spaces. -/
def tensorMap
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ) :
    TensorTerm R X Y n ⟶ TensorTerm R X' Y' n :=
  Sigma.desc fun pq : TensorDegrees n ↦
    (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
        (ModuleCat.of R R)).map f ⊗ₘ
      ((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
        (ModuleCat.of R R)).map g) ≫
      Sigma.ι (fun pq : TensorDegrees n ↦
        Homology R pq.1.1 X' ⊗ Homology R pq.1.2 Y') pq

theorem tensorMap_component
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y')
    (n : ℕ) (pq : TensorDegrees n) :
    Sigma.ι (fun pq : TensorDegrees n ↦
      Homology R pq.1.1 X ⊗ Homology R pq.1.2 Y) pq ≫ tensorMap R f g n =
      (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
          (ModuleCat.of R R)).map f ⊗ₘ
        ((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
          (ModuleCat.of R R)).map g) ≫
        Sigma.ι (fun pq : TensorDegrees n ↦
          Homology R pq.1.1 X' ⊗ Homology R pq.1.2 Y') pq := by
  apply Sigma.ι_desc

/-- The canonical map on the `Tor₁` direct sum induced by maps of both spaces. -/
def torMap
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ) :
    TorTerm R X Y n ⟶ TorTerm R X' Y' n :=
  Sigma.desc fun pq : TorDegrees n ↦
    ((CategoryTheory.Tor (ModuleCat.{u} R) 1).map
        (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
          (ModuleCat.of R R)).map f)).app (Homology R pq.1.2 Y) ≫
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X')).map
        (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
          (ModuleCat.of R R)).map g) ≫
      Sigma.ι (fun pq : TorDegrees n ↦
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X')).obj (Homology R pq.1.2 Y')) pq

theorem torMap_component
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y')
    (n : ℕ) (pq : TorDegrees n) :
    Sigma.ι (fun pq : TorDegrees n ↦
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)) pq ≫ torMap R f g n =
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).map
          (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
            (ModuleCat.of R R)).map f)).app (Homology R pq.1.2 Y) ≫
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X')).map
          (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
            (ModuleCat.of R R)).map g) ≫
        Sigma.ι (fun pq : TorDegrees n ↦
          ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
            (Homology R pq.1.1 X')).obj (Homology R pq.1.2 Y')) pq := by
  apply Sigma.ι_desc

#print axioms tensorMap
#print axioms tensorMap_component
#print axioms torMap
#print axioms torMap_component
#print axioms singularChains_projective

end AwesomeTheorems.Stage1.THM_M_0005.Proof
