import Mathlib.AlgebraicTopology.ModelCategory.Homotopy
import Mathlib.Topology.CWComplex.Classical.Basic
import Mathlib.Topology.Homotopy.Equiv
import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0559 anchor audit

This file checks the public interfaces of the two repo-local mathlib candidates. It deliberately
does not wrap either candidate: the model-category theorem has a different category-level weak
equivalence premise, while the topology CW API contains no Whitehead theorem at the pinned
revision.
-/

open CategoryTheory HomotopicalAlgebra

#check RightHomotopyClass.whitehead
#check LeftHomotopyClass.whitehead
#check Topology.CWComplex
#check HomotopyGroup.Pi
#check ContinuousMap.HomotopyEquiv

-- Freeze the exact model-category candidate type rather than relying on its name.
example {C : Type*} [Category C] [HomotopicalAlgebra.ModelCategory C]
    {X Y : C} [IsCofibrant X] [IsCofibrant Y] [IsFibrant X] [IsFibrant Y]
    (f : X ⟶ Y) [WeakEquivalence f] :
    ∃ (g : Y ⟶ X), RightHomotopyRel (f ≫ g) (𝟙 X) ∧
      RightHomotopyRel (g ≫ f) (𝟙 Y) :=
  RightHomotopyClass.whitehead f
