import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.RepresentationTheory.Irreducible
import Mathlib.RepresentationTheory.Rep.Basic

/-!
Kernel-checked infrastructure probe for the THM-M-0134 statement gate.

The repository record does not identify an exact Burnside--Young theorem. This module therefore
does not declare a canonical target. It checks only that the pinned environment can express the
object model used by the intake's candidate interpretation: partitions and isomorphism classes of
irreducible finite-dimensional complex representations of a finite symmetric group.
-/

open CategoryTheory

namespace Stage1Instances.THM_M_0134.StatementInfrastructure

/-- The finite symmetric group model available in pinned mathlib. -/
abbrev SymmetricGroup (n : Nat) := Equiv.Perm (Fin n)

/-- Bundled complex representations of the finite symmetric group. -/
abbrev ComplexRep (n : Nat) : Type 1 := Rep.{0} ℂ (SymmetricGroup n)

/-- Bundled irreducible representations in the candidate object model. -/
abbrev IrreducibleRep (n : Nat) : Type 1 :=
  { A : ComplexRep n // Representation.IsIrreducible A.ρ }

/-- Isomorphism of underlying bundled representations. -/
def IrreducibleRepIsoRel (n : Nat) (A B : IrreducibleRep n) : Prop :=
  Nonempty ((A : ComplexRep n) ≅ (B : ComplexRep n))

/-- The checked quotient object for candidate isomorphism classes. -/
instance irreducibleRepIsoSetoid (n : Nat) : Setoid (IrreducibleRep n) where
  r := IrreducibleRepIsoRel n
  iseqv := by
    refine ⟨?_, ?_, ?_⟩
    · intro A
      exact ⟨Iso.refl (A : ComplexRep n)⟩
    · rintro A B ⟨e⟩
      exact ⟨e.symm⟩
    · rintro A B C ⟨eAB⟩ ⟨eBC⟩
      exact ⟨eAB.trans eBC⟩

abbrev IrreducibleRepIsoClass (n : Nat) : Type 1 :=
  Quotient (irreducibleRepIsoSetoid n)

#check Nat.Partition
#check SymmetricGroup
#check ComplexRep
#check IrreducibleRepIsoClass

end Stage1Instances.THM_M_0134.StatementInfrastructure
