import Mathlib.Algebra.Module.Projective
import Mathlib.Algebra.MvPolynomial.Basic
import Mathlib.RingTheory.Finiteness.Defs

/-!
# THM-M-0034 canonical Lean statement

This module freezes the finite-variable, field-coefficient module statement selected from
Suslin's 1976 paper. It contains statement-identity mutations but no proof of Quillen-Suslin.
-/

namespace Stage1Instances.THM_M_0034

universe u v

/-- Every finitely generated projective module over a polynomial ring in a positive finite number of variables
over a field is free. -/
def QuillenSuslinTarget : Prop :=
  forall (k : Type u) [Field k] (n : Nat) (_ : 0 < n) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
    [Module.Finite (MvPolynomial (Fin n) k) P]
    [Module.Projective (MvPolynomial (Fin n) k) P],
    Module.Free (MvPolynomial (Fin n) k) P

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedFiniteGeneration : Prop :=
  forall (k : Type u) [Field k] (n : Nat) (_ : 0 < n) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
    [Module.Projective (MvPolynomial (Fin n) k) P],
    Module.Free (MvPolynomial (Fin n) k) P

def mutationChangedDomainToCommRing : Prop :=
  forall (R : Type u) [CommRing R] (n : Nat) (_ : 0 < n) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) R) P]
    [Module.Finite (MvPolynomial (Fin n) R) P]
    [Module.Projective (MvPolynomial (Fin n) R) P],
    Module.Free (MvPolynomial (Fin n) R) P

def mutationChangedBinderScope : Prop :=
  forall (k : Type u) [Field k],
    exists n : Nat,
      0 < n ∧ forall (P : Type v) [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
        [Module.Finite (MvPolynomial (Fin n) k) P]
        [Module.Projective (MvPolynomial (Fin n) k) P],
        Module.Free (MvPolynomial (Fin n) k) P

def mutationIncludedZeroVariables : Prop :=
  forall (k : Type u) [Field k] (n : Nat) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
    [Module.Finite (MvPolynomial (Fin n) k) P]
    [Module.Projective (MvPolynomial (Fin n) k) P],
    Module.Free (MvPolynomial (Fin n) k) P

variable (hRemoved : mutationRemovedFiniteGeneration.{u, v})
#check_failure (show QuillenSuslinTarget.{u, v} from hRemoved)

variable (hDomain : mutationChangedDomainToCommRing.{u, v})
#check_failure (show QuillenSuslinTarget.{u, v} from hDomain)

variable (hScope : mutationChangedBinderScope.{u, v})
#check_failure (show QuillenSuslinTarget.{u, v} from hScope)

variable (hBoundary : mutationIncludedZeroVariables.{u, v})
#check_failure (show QuillenSuslinTarget.{u, v} from hBoundary)

set_option pp.universes true in
set_option pp.explicit true in
#print QuillenSuslinTarget

end Stage1Instances.THM_M_0034
