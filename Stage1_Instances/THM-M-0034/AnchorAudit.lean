import Mathlib.Algebra.Module.Projective
import Mathlib.LinearAlgebra.FreeModule.PID
import Mathlib.RingTheory.Flat.Basic
import Mathlib.RingTheory.MvPolynomial.Basic
import Mathlib.RingTheory.LocalRing.Module
import Mathlib.RingTheory.Finiteness.Defs
import Mathlib.RingTheory.Spectrum.Prime.FreeLocus

/-!
# THM-M-0034 pinned anchor probes

This module checks the mathlib interfaces retained by the anchor audit. They define the target
predicates, show the polynomial ring itself is free over its coefficient ring, and prove only the
reverse implication from free to projective. No declaration here proves that every finite
projective module over a polynomial ring is free.
-/

namespace Stage1Instances.THM_M_0034_AnchorAudit

universe u v

/-- A literal audit-local copy of the frozen target. This is a proposition, not a proof. -/
def ExactTarget : Prop :=
  forall (k : Type u) [Field k] (n : Nat) (_ : 0 < n) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
    [Module.Finite (MvPolynomial (Fin n) k) P]
    [Module.Projective (MvPolynomial (Fin n) k) P],
    Module.Free (MvPolynomial (Fin n) k) P

/-- The all-finite-variable form of the exact immutable external field candidate. -/
def ExternalFieldCandidate : Prop :=
  forall (k : Type u) [Field k] (n : Nat) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
    [Module.Finite (MvPolynomial (Fin n) k) P]
    [Module.Projective (MvPolynomial (Fin n) k) P],
    Module.Free (MvPolynomial (Fin n) k) P

/-- Checked boundary transport only: this does not provide the external theorem premise. -/
theorem externalFieldCandidate_implies_exact
    (h : ExternalFieldCandidate.{u, v}) : ExactTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact h k n P

/-- The specialization of the stronger immutable external candidate needed by this target. -/
def ExternalPIDCandidate : Prop :=
  forall (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (sigma : Type) [Fintype sigma] (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial sigma R) P]
    [Module.Finite (MvPolynomial sigma R) P]
    [Module.Projective (MvPolynomial sigma R) P],
    Module.Free (MvPolynomial sigma R) P

/-- Checked statement transport only: this does not provide the external theorem premise. -/
theorem externalPIDCandidate_implies_exact
    (h : ExternalPIDCandidate.{u, v}) : ExactTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact h k (Fin n) P

#check Module.Projective
#check Module.projective_def
#check Module.Projective.iff_split
#check Module.Projective.of_free
#check Module.Flat.of_projective
#check Module.free_of_flat_of_isLocalRing
#check Module.freeLocus_eq_univ_iff
#check Module.free_of_finite_type_torsion_free'
#check Module.Free
#check Module.Finite
#check MvPolynomial.basisMonomials

section MissingBridge

variable (k : Type u) [Field k] (n : Nat) (P : Type v)
  [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
  [Module.Finite (MvPolynomial (Fin n) k) P]
  [Module.Projective (MvPolynomial (Fin n) k) P]

-- Projectivity does reach flatness in the pin, but the global polynomial-ring bridge is absent.
#check (inferInstance : Module.Flat (MvPolynomial (Fin n) k) P)

-- The pinned environment must not silently gain the requested converse as an instance.
#check_failure (inferInstance : Module.Free (MvPolynomial (Fin n) k) P)

end MissingBridge

#print axioms Module.projective_def
#print axioms Module.Projective.iff_split
#print axioms Module.Projective.of_free
#print axioms Module.Flat.of_projective
#print axioms Module.free_of_flat_of_isLocalRing
#print axioms Module.freeLocus_eq_univ_iff
#print axioms Module.free_of_finite_type_torsion_free'
#print axioms externalFieldCandidate_implies_exact
#print axioms externalPIDCandidate_implies_exact

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0034_AnchorAudit
