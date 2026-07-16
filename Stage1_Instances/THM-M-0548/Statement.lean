import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Topology.Category.TopCat.Sphere
import Mathlib.Topology.Homotopy.LocallyContractible

/-!
# THM-M-0548 statement boundary probe

The repository source record says only "duality for subspaces in a sphere". It does not fix the
coefficient system, reduced theories, grading, naturality scope, or degenerate cases needed for one
Alexander-duality proposition. This module therefore checks only the pinned topological and
ordinary-homology substrate. It deliberately declares no canonical Alexander-duality target,
transport, or mutation fixture.
-/

noncomputable section

open CategoryTheory AlgebraicTopology

universe w v u

namespace Stage1Instances.THM_M_0548

abbrev Sphere (n : Nat) : TopCat.{w} :=
  TopCat.sphere n

abbrev SphereSubset (n : Nat) (A : Set (Sphere.{w} n)) : TopCat.{w} :=
  TopCat.of A

abbrev SphereSubsetComplement (n : Nat) (A : Set (Sphere.{w} n)) : TopCat.{w} :=
  TopCat.of {x : Sphere.{w} n // x ∉ A}

def SubsetHypotheses (n : Nat) (A : Set (Sphere.{w} n)) : Prop :=
  IsCompact A ∧ LocallyContractibleSpace A

abbrev OrdinaryComplementSingularHomology
    (C : Type u) [Category.{v} C] [CategoryTheory.Limits.HasCoproducts.{w} C]
    [Preadditive C] [CategoryWithHomology C] (R : C)
    (n degree : Nat) (A : Set (Sphere.{w} n)) : C :=
  (((singularHomologyFunctor C degree).obj R).obj
    (SphereSubsetComplement.{w} n A))

end Stage1Instances.THM_M_0548

#check Stage1Instances.THM_M_0548.SubsetHypotheses
#check Stage1Instances.THM_M_0548.OrdinaryComplementSingularHomology
