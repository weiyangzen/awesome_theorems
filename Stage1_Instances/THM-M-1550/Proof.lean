import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# THM-M-1550 proof body

This module implements the exact frozen finite-matrix statement.  The Lax
equation remains present in the root, while the explicitly supplied
conjugating evolution provides the unit conjugation used by mathlib's spectrum
theorem.
-/

noncomputable section

namespace Stage1Instances.THM_M_1550.Proof

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
  forall t0, timeDomain t0 -> forall t, timeDomain t -> ConjugatesAt L t0 t

def LaxPairIsospectrality : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n]
    (L P : Real -> LaxMatrix n) (timeDomain : Set Real),
      LaxEquationOn L P timeDomain ->
      ConjugatingEvolutionOn L timeDomain -> IsospectralOn L timeDomain

/-- Thin specialization of the pinned mathlib terminal proof body. -/
theorem spectrumEqOfUnitsConjugate {A : Type u} [Ring A] [Algebra Complex A]
    (a : A) (U : Aˣ) :
    spectrum Complex ((U : A) * a * ((U⁻¹ : Aˣ) : A)) = spectrum Complex a := by
  exact spectrum.units_conjugate

/-- The only mathematical leaf: algebra spectrum is invariant under the exact
unit conjugation used in `ConjugatesAt`. -/
theorem spectrumUnderConjugation {n : Type u} [Fintype n] [DecidableEq n]
    (L : Real -> LaxMatrix n) (t0 t : Real) (h : ConjugatesAt L t0 t) :
    spectrum Complex (L t) = spectrum Complex (L t0) := by
  obtain ⟨U, hU⟩ := h
  calc
    spectrum Complex (L t) =
        spectrum Complex ((U : LaxMatrix n) * L t0 * (U⁻¹ : LaxMatrix n)) :=
      congrArg (spectrum Complex) hU
    _ = spectrum Complex (L t0) := by
      rw [← Matrix.GeneralLinearGroup.coe_inv U]
      exact spectrumEqOfUnitsConjugate (L t0) U

/-- Proof of the exact frozen root.  The equation premise is intentionally
retained, though the stronger evolution premise already implies the result. -/
theorem laxPairIsospectrality : LaxPairIsospectrality.{u} := by
  intro n _ _ L P timeDomain _hLax hEvolution t0 ht0 t ht
  exact spectrumUnderConjugation L t0 t (hEvolution t0 ht0 t ht)

#print axioms spectrumEqOfUnitsConjugate
#print axioms spectrumUnderConjugation
#print axioms laxPairIsospectrality

end Stage1Instances.THM_M_1550.Proof
