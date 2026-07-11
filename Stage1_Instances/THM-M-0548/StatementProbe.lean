import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Topology.Category.TopCat.Sphere
import Mathlib.Topology.Homotopy.LocallyContractible

/-!
# THM-M-0548 statement infrastructure probe

This file checks only the pinned APIs needed to describe the intake-selected
sphere subset, its complement, compactness, local contractibility, and ordinary
singular homology. It deliberately does not declare a canonical Alexander
duality target: the coefficient and reduced (co)homology conventions needed for
that target are not fixed by the source record.
-/

noncomputable section

open CategoryTheory AlgebraicTopology

universe w v u

namespace Stage1Instances.THM_M_0548

/-- The sphere object available in the pinned mathlib environment. -/
abbrev Sphere (n : Nat) : TopCat.{w} :=
  TopCat.sphere n

/-- A selected subset with its subtype topology. -/
abbrev SphereSubset (n : Nat) (A : Set (Sphere.{w} n)) : TopCat.{w} :=
  TopCat.of A

/-- The set-theoretic complement with its subtype topology. -/
abbrev SphereSubsetComplement (n : Nat) (A : Set (Sphere.{w} n)) : TopCat.{w} :=
  TopCat.of {x : Sphere.{w} n // x ∉ A}

/-- The unambiguous topological hypotheses from the intake-selected variant. -/
def SubsetHypotheses (n : Nat) (A : Set (Sphere.{w} n)) : Prop :=
  IsCompact A ∧ LocallyContractibleSpace A

/-- Ordinary (not reduced) singular homology is available in the pinned API. -/
abbrev OrdinaryComplementSingularHomology
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C)
    (n degree : Nat) (A : Set (Sphere.{w} n)) : C :=
  (((singularHomologyFunctor C degree).obj R).obj
    (SphereSubsetComplement.{w} n A))

end Stage1Instances.THM_M_0548

#check Stage1Instances.THM_M_0548.SubsetHypotheses
#check Stage1Instances.THM_M_0548.OrdinaryComplementSingularHomology
