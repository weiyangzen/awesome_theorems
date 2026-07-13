import Statement
import Mathlib.LinearAlgebra.FreeModule.PID

/-!
# THM-M-0034 conditional obligation composition

This module checks only the statement transports and child-to-root composition frozen by the
obligation registry. The external Quillen-Suslin theorem remains an explicit premise. Its source
tree is not imported here, so this module does not prove the canonical target.
-/

namespace Stage1Instances.THM_M_0034.ObligationTree

universe u v

/-- Exact type of the selected field candidate. It is stronger than the root only at `n = 0`. -/
def ExternalFieldCandidate : Prop :=
  forall (k : Type u) [Field k] (n : Nat) (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial (Fin n) k) P]
    [Module.Finite (MvPolynomial (Fin n) k) P]
    [Module.Projective (MvPolynomial (Fin n) k) P],
    Module.Free (MvPolynomial (Fin n) k) P

/-- Type of the stronger alternate PID candidate, retained as a nonselected transport. -/
def ExternalPIDCandidate : Prop :=
  forall (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (sigma : Type) [Fintype sigma] (P : Type v)
    [AddCommGroup P] [Module (MvPolynomial sigma R) P]
    [Module.Finite (MvPolynomial sigma R) P]
    [Module.Projective (MvPolynomial sigma R) P],
    Module.Free (MvPolynomial sigma R) P

/-- The selected candidate after the positive-variable boundary adapter. -/
def AdaptedPositiveCandidate : Prop :=
  Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v}

/-- Checked boundary transport from the selected candidate type to the positive-variable root. -/
theorem externalFieldCandidate_implies_target
    (external : ExternalFieldCandidate.{u, v}) :
    Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact external k n P

/-- Composition certificate for `T-ADAPTER`: consume the external-body conclusion exactly. -/
theorem externalFieldCandidate_implies_adapted
    (external : ExternalFieldCandidate.{u, v}) : AdaptedPositiveCandidate.{u, v} :=
  externalFieldCandidate_implies_target external

/-- Checked specialization of the alternate PID candidate. It supplies no external proof body. -/
theorem externalPIDCandidate_implies_target
    (external : ExternalPIDCandidate.{u, v}) :
    Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact external k (Fin n) P

/-- Composition certificate for `T-ROOT`: consume the adapted conclusion exactly. -/
theorem terminalTarget_of_adapted
    (adapted : AdaptedPositiveCandidate.{u, v}) :
    Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v} :=
  adapted

/-- Composition certificate for `ROOT`: consume the terminal conclusion exactly. -/
theorem root_of_terminalTarget
    (terminal : Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v}) :
    Stage1Instances.THM_M_0034.QuillenSuslinTarget.{u, v} :=
  terminal

#print axioms externalFieldCandidate_implies_target
#print axioms externalFieldCandidate_implies_adapted
#print axioms externalPIDCandidate_implies_target
#print axioms terminalTarget_of_adapted
#print axioms root_of_terminalTarget

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0034.QuillenSuslinTarget

end Stage1Instances.THM_M_0034.ObligationTree
