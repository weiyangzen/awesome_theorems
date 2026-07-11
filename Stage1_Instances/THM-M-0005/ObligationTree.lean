import KunnethStatement

/-!
# THM-M-0005 conditional obligation composition

Every field of `NaturalKunnethSequence` is an explicit premise below.  The
constructor checks that the frozen field-level obligations compose to the exact
canonical root; it supplies none of the mathematical premises itself.
-/

noncomputable section

open AlgebraicTopology CategoryTheory CategoryTheory.Limits
open CategoryTheory.MonoidalCategory

universe u

namespace AwesomeTheorems.Stage1.THM_M_0005.ObligationTree

abbrev NKS := AwesomeTheorems.Stage1.THM_M_0005.NaturalKunnethSequence
abbrev TT := AwesomeTheorems.Stage1.THM_M_0005.TensorTerm
abbrev RT := AwesomeTheorems.Stage1.THM_M_0005.TorTerm
abbrev PH := AwesomeTheorems.Stage1.THM_M_0005.ProductHomology
abbrev TD := AwesomeTheorems.Stage1.THM_M_0005.TensorDegrees
abbrev RD := AwesomeTheorems.Stage1.THM_M_0005.TorDegrees
abbrev H := AwesomeTheorems.Stage1.THM_M_0005.Homology

def assemble_sequence
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (inclusion : ∀ (X Y : TopCat.{u}) (n : ℕ), TT R X Y n ⟶ PH R X Y n)
    (projection : ∀ (X Y : TopCat.{u}) (n : ℕ), PH R X Y n ⟶ RT R X Y n)
    (zero : ∀ (X Y : TopCat.{u}) (n : ℕ),
      inclusion X Y n ≫ projection X Y n = 0)
    (shortExact : ∀ (X Y : TopCat.{u}) (n : ℕ),
      (ShortComplex.mk (inclusion X Y n) (projection X Y n) (zero X Y n)).ShortExact)
    (tensorMap : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
      TT R X Y n ⟶ TT R X' Y' n)
    (torMap : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
      RT R X Y n ⟶ RT R X' Y' n)
    (tensorMap_component : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y')
        (n : ℕ) (pq : TD n),
      Sigma.ι (fun pq : TD n ↦ H R pq.1.1 X ⊗ H R pq.1.2 Y) pq ≫ tensorMap f g n =
        (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj (ModuleCat.of R R)).map f ⊗ₘ
          ((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj (ModuleCat.of R R)).map g) ≫
        Sigma.ι (fun pq : TD n ↦ H R pq.1.1 X' ⊗ H R pq.1.2 Y') pq)
    (torMap_component : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y')
        (n : ℕ) (pq : RD n),
      Sigma.ι (fun pq : RD n ↦ ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (H R pq.1.1 X)).obj (H R pq.1.2 Y)) pq ≫ torMap f g n =
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).map
          (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
            (ModuleCat.of R R)).map f)).app (H R pq.1.2 Y) ≫
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj (H R pq.1.1 X')).map
          (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
            (ModuleCat.of R R)).map g) ≫
        Sigma.ι (fun pq : RD n ↦ ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (H R pq.1.1 X')).obj (H R pq.1.2 Y')) pq)
    (inclusion_natural : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
      tensorMap f g n ≫ inclusion X' Y' n = inclusion X Y n ≫
        ((singularHomologyFunctor (ModuleCat.{u} R) n).obj (ModuleCat.of R R)).map
          (Limits.prod.map f g))
    (projection_natural : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
      ((singularHomologyFunctor (ModuleCat.{u} R) n).obj (ModuleCat.of R R)).map
          (Limits.prod.map f g) ≫ projection X' Y' n = projection X Y n ≫ torMap f g n) :
    NKS R :=
  { inclusion := inclusion
    projection := projection
    zero := zero
    shortExact := shortExact
    tensorMap := tensorMap
    torMap := torMap
    tensorMap_component := tensorMap_component
    torMap_component := torMap_component
    inclusion_natural := inclusion_natural
    projection_natural := projection_natural }

theorem root_compose
    (build : ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R], NKS R) :
    ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R], Nonempty (NKS R) :=
  fun R _ _ _ ↦ ⟨build R⟩

#print axioms assemble_sequence
#print axioms root_compose

end AwesomeTheorems.Stage1.THM_M_0005.ObligationTree
