import Mathlib.Topology.Homotopy.HomotopyGroup
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-!
Elaboration probe for the THM-M-0558 exact-statement blocker.

This checks the independent pinned homotopy-group and integral singular-homology
substrates. It deliberately does not introduce a user-supplied map or call ordinary
homology "reduced": either choice would substitute for the canonical Hurewicz target.
-/

open scoped Topology
open AlgebraicTopology CategoryTheory

namespace Stage1.THM_M_0558

universe u

variable (X : Type u) [TopologicalSpace X] (x : X) (n : Nat)

#check HomotopyGroup.Pi
#check (π_ n X x)
#check singularChainComplexFunctor
#check singularHomologyFunctor

/-- The ordinary integral singular-homology object available in pinned mathlib. -/
noncomputable abbrev OrdinaryIntegralHomology
    (Y : Type) [TopologicalSpace Y] (degree : Nat) : ModuleCat ℤ :=
  (((singularHomologyFunctor (ModuleCat ℤ) degree).obj (ModuleCat.of ℤ ℤ)).obj
    (TopCat.of Y))

#check OrdinaryIntegralHomology

end Stage1.THM_M_0558
