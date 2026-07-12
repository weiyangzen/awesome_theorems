import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# THM-M-1550: exact finite-matrix Lax statement boundary

This module freezes the conservative isospectrality implication selected at
intake. It does not assert that every integrable system admits a Lax pair and
does not construct conjugating evolution from the Lax differential equation.
-/

noncomputable section

namespace Stage1Instances.THM_M_1550

universe u

abbrev LaxMatrix (n : Type u) := Matrix n n Complex

def MatrixCommutator {n : Type u} [Fintype n] [DecidableEq n]
    (A B : LaxMatrix n) : LaxMatrix n :=
  A * B - B * A

def LaxEquationOn {n : Type u} [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real) : Prop :=
  forall t, timeDomain t ->
    HasDerivWithinAt L (MatrixCommutator (P t) (L t)) timeDomain t

def IsospectralOn {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (timeDomain : Set Real) : Prop :=
  forall t0, timeDomain t0 -> forall t, timeDomain t ->
    spectrum Complex (L t) = spectrum Complex (L t0)

def ConjugatesAt {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (t0 t : Real) : Prop :=
  exists U : (LaxMatrix n)ˣ,
    L t = (U : LaxMatrix n) * L t0 * (U⁻¹ : LaxMatrix n)

def ConjugatingEvolutionOn {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (timeDomain : Set Real) : Prop :=
  forall t0, timeDomain t0 -> forall t, timeDomain t ->
    ConjugatesAt L t0 t

/-- Exact statement selected at intake: a finite complex matrix Lax equation,
together with explicitly supplied conjugating evolution, is isospectral. -/
def LaxPairIsospectrality : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real),
      LaxEquationOn L P timeDomain ->
      ConjugatingEvolutionOn L timeDomain ->
      IsospectralOn L timeDomain

/-- Direct expansion of the historical finite-matrix candidate boundary. -/
def PinnedCandidateSourceShape : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> Matrix n n Complex) (timeDomain : Set Real),
      (forall t, timeDomain t ->
        HasDerivWithinAt L (P t * L t - L t * P t) timeDomain t) ->
      (forall t0, timeDomain t0 -> forall t, timeDomain t ->
        exists U : (Matrix n n Complex)ˣ,
          L t = (U : Matrix n n Complex) * L t0 * (U⁻¹ : Matrix n n Complex)) ->
      (forall t0, timeDomain t0 -> forall t, timeDomain t ->
        spectrum Complex (L t) = spectrum Complex (L t0))

/-- Checked transport from the named predicates to their direct expansion. -/
theorem laxPairIsospectrality_iff_pinnedCandidateSourceShape :
    LaxPairIsospectrality.{u} <-> PinnedCandidateSourceShape.{u} := by
  rfl

-- Structural mutations: the validator requires distinct elaborated targets.
def mutationRemovedLaxEquation : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (timeDomain : Set Real),
      ConjugatingEvolutionOn L timeDomain -> IsospectralOn L timeDomain

def mutationChangedIndexDomain : Prop :=
  forall (n : Nat) (L P : Real -> Matrix (Fin n) (Fin n) Complex)
    (timeDomain : Set Real),
      LaxEquationOn L P timeDomain ->
      ConjugatingEvolutionOn L timeDomain -> IsospectralOn L timeDomain

def mutationChangedBinderScope : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real),
      LaxEquationOn L P timeDomain ->
      (exists U : (LaxMatrix n)ˣ, forall t0, timeDomain t0 ->
        forall t, timeDomain t ->
          L t = (U : LaxMatrix n) * L t0 * (U⁻¹ : LaxMatrix n)) ->
      IsospectralOn L timeDomain

def mutationChangedBoundaryPolicy : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real),
      timeDomain.Nonempty ->
      LaxEquationOn L P timeDomain ->
      ConjugatingEvolutionOn L timeDomain -> IsospectralOn L timeDomain

/-- The selected conclusion deliberately admits the empty time domain. -/
theorem emptyTimeDomainBoundary {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) : IsospectralOn L {t | False} := by
  intro t0 ht0
  exact False.elim ht0

/-- The selected conclusion admits the zero-dimensional finite matrix model. -/
example (L : Real -> Matrix (Fin 0) (Fin 0) Complex) (s : Set Real) :
    IsospectralOn L s <->
      forall t0, s t0 -> forall t, s t ->
        spectrum Complex (L t) = spectrum Complex (L t0) := by
  rfl

end Stage1Instances.THM_M_1550

set_option pp.explicit true in
#print Stage1Instances.THM_M_1550.LaxPairIsospectrality

set_option pp.explicit true in
#print Stage1Instances.THM_M_1550.mutationRemovedLaxEquation

set_option pp.explicit true in
#print Stage1Instances.THM_M_1550.mutationChangedIndexDomain

set_option pp.explicit true in
#print Stage1Instances.THM_M_1550.mutationChangedBinderScope

set_option pp.explicit true in
#print Stage1Instances.THM_M_1550.mutationChangedBoundaryPolicy
